# Local setup

Everything the services depend on runs in Docker. **The services themselves do
not** — they run on the host via `./gradlew bootRun`. Containerising them
locally destroys the iteration loop; they get images in sprint 9 (FM-011).

## First run

```bash
cd platform/infra
cp .env.example .env     # then set real passwords
docker compose up -d
docker compose ps        # wait for healthy, not just running
```

Compose refuses to start if a required variable is missing, naming it:

```
required variable ANALYTICS_DB_PASSWORD is missing a value: set in infra/.env
```

That is deliberate — better than booting Postgres with a blank password.

## Daily commands

```bash
docker compose up -d                          # start core stack
docker compose --profile observability up -d  # + Prometheus and Grafana
docker compose ps                             # status and health
docker compose logs -f kafka                  # follow one service
docker compose down                           # stop, keep all data
docker compose down -v                        # stop and WIPE all data
```

## What runs where

| Service | Host port | Notes |
|---|---|---|
| Postgres | **15432** | not 5432 — see below |
| Redis | 6379 | |
| Kafka | 9092 | from the host |
| kafka-ui | 8090 | <http://localhost:8090> |
| Prometheus | 9090 | profile `observability` |
| Grafana | 3000 | profile `observability` |

### Postgres is on 15432, not 5432

This machine runs a **native postgresql service** holding `127.0.0.1:5432`, so
the container is published on 15432 to avoid the clash. The port is
`POSTGRES_PORT` in `.env`. Inside the compose network it is still 5432.

### Databases

Four databases, four roles, one per service. A role can reach **only** its own
database:

| Database | Role | Service |
|---|---|---|
| `fm_auth` | `fm_auth` | auth-service |
| `fm_expense` | `fm_expense` | expense-service |
| `fm_investment` | `fm_investment` | investment-service |
| `fm_analytics` | `fm_analytics` | analytics-service |

A service's JDBC URL is therefore:

```
jdbc:postgresql://localhost:15432/fm_expense
```

## The one gotcha that will cost you an hour

**Postgres init scripts run exactly once** — only when the data volume is
empty. Edit `postgres/init/01-databases.sh` after a successful `up` and nothing
happens; your change is silently ignored and the script looks broken.

```bash
docker compose down -v && docker compose up -d
```

## Verifying isolation

Four roles and four databases are not isolation on their own: Postgres grants
`CONNECT` on every database to `PUBLIC` by default. The init script revokes it.
To confirm it is still true, the **negative** test must fail:

```bash
docker compose exec -e PGPASSWORD=<fm_expense password> postgres \
  psql -U fm_expense -d fm_auth -c '\dt'
```

```
psql: error: FATAL:  permission denied for database "fm_auth"
DETAIL:  User does not have CONNECT privilege.
```

That error is the pass condition. Then check the positive case too, or you may
have locked out everything including the service itself:

```bash
docker compose exec -e PGPASSWORD=<fm_expense password> postgres \
  psql -U fm_expense -d fm_expense -c 'CREATE TABLE _probe(id int); DROP TABLE _probe;'
```

## Kafka: two listeners, two addresses

Kafka tells a client where to reconnect, and the right answer depends on who is
asking:

| Client | Bootstrap address |
|---|---|
| Spring services (**on the host**) | `localhost:9092` |
| kafka-ui (**inside the network**) | `kafka:29092` |

One advertised address cannot serve both. If a client connects fine and then
times out on its first produce, this is why.

Topic auto-creation is **off**. Topics are created explicitly — a typo in a
topic name should fail loudly, not silently create a new topic.

Testing from the host without installing the Kafka CLI:

```bash
docker run --rm -i --network host apache/kafka:4.4.0 \
  /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic my.topic
```

Note the **`-i`**. Without it `docker run` does not attach stdin, so the
producer reads EOF immediately, writes nothing, and still exits 0. Check what
actually landed rather than trusting the exit code:

```bash
docker run --rm --network host apache/kafka:4.4.0 \
  /opt/kafka/bin/kafka-get-offsets.sh --bootstrap-server localhost:9092 --topic my.topic
```

## Troubleshooting

| Symptom | Cause |
|---|---|
| `address already in use` on 5432 | the native postgresql service; use 15432 |
| Init script changes ignored | volume not empty — `down -v` |
| Flyway: permission denied for schema public | role does not own its database |
| Kafka client connects then times out | advertised listener mismatch |
| Producer exits 0, nothing stored | missing `-i` on `docker run` |
| Grafana not responding for ~30s on first boot | normal — it runs its SQLite migrations |
