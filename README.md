# platform

Infrastructure, event contracts, documentation and the tracker for
**Finance Master** — a personal finance system built as four backend services
behind an API gateway, used as a vehicle for learning backend engineering.

This repo is not a deployable service. Nothing here runs in production; it is
what makes the other five repos work together.

## What's here

| | |
|---|---|
| [`docs/`](docs/README.md) | Architecture, decision records, roadmap, runbooks |
| [`docs/adr/`](docs/adr/README.md) | Every significant decision and why — including the options rejected |
| [`tracker/`](tracker/README.md) | File-based issue tracker with a local web UI |
| `infra/` | Docker Compose stack: Postgres, Redis, Kafka, observability |
| `contracts/` | JSON Schema for every Kafka event — the single source of truth |

## The services

| Repo | Owns | Port |
|---|---|---|
| [`api-gateway-backend`](https://github.com/financemaster-proj/api-gateway-backend) | nothing — routing, edge JWT validation, rate limiting | 8080 |
| [`auth-service-backend`](https://github.com/financemaster-proj/auth-service-backend) | users, credentials, roles, refresh tokens | 8081 |
| [`expense-service-backend`](https://github.com/financemaster-proj/expense-service-backend) | expenses, categories, budgets | 8082 |
| [`investment-service-backend`](https://github.com/financemaster-proj/investment-service-backend) | instruments, holdings, trades, valuations | 8083 |
| [`analytics-service-backend`](https://github.com/financemaster-proj/analytics-service-backend) | read models and reports | 8084 |

Clone all six as siblings in one parent folder.

## Start here

- **[Architecture overview](docs/architecture/overview.md)** — boundaries, events, API conventions
- **[Roadmap](docs/sprints/README.md)** — ten sprints and the concept each one teaches
- **[Board](tracker/BOARD.md)** — current tickets

## Tracker

```bash
python3 tracker/serve.py     # web UI at http://127.0.0.1:7777
python3 tracker/board.py ls  # or from the command line
```

## The short version of the architecture

Four services, a database each, Kafka between them, and **no synchronous calls
between business services** — ever. That rule is what stops a microservice
architecture collapsing into a distributed monolith, and it is enforced in
review.
