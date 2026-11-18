# Creating a new service

The recipe, written from what `expense-service-backend` actually needed. Follow
it for `auth`, `investment`, `analytics` and `api-gateway`.

Polyrepo means no shared build logic across repos (ADR-0001), so this document
*is* the shared build logic. Keep it current.

## 1. Spring Initializr

| Field | Value |
|---|---|
| Project | Gradle — **Kotlin** |
| Language | Java |
| Spring Boot | latest **stable** — never SNAPSHOT or RC |
| Group | `com.financemaster` |
| Artifact | `<name>-service` — **no** `-backend` suffix; that is a repo convention, not the app's identity |
| Package name | `com.financemaster.<name>` |
| Packaging | Jar · **Java 21** · Config **YAML** |

Baseline dependencies: `Spring Web` · `Spring Data JPA` · `PostgreSQL Driver` ·
`Flyway Migration` · `Validation` · `Spring Boot Actuator` · `Testcontainers`

**Do not add:** Lombok (Java 21 records cover DTOs, and `@Data` on a JPA entity
breaks entity identity), Spring Security until auth exists, Kafka until sprint 4,
Docker Compose Support (fights the explicit infra stack), DevTools (its restart
classloader confuses Testcontainers and JPA).

Not in Initializr, added by hand: **springdoc-openapi**.

## 2. Three things to fix immediately after unzipping

These bit us once each. They will bite again.

1. **The `.gitignore` is overwritten.** Initializr ships its own, which has no
   concept of secrets. Re-append `.env`, `.env.local`, `*.pem`, `*.key`. These
   repos are public. Verify with `git check-ignore -v .env` — reading the file
   is not proof.
2. **Check the package name.** Editing the Artifact field *regenerates* the
   package name from it, converting hyphens to underscores. You can end up with
   `com.financemaster.expense_service` even though the form said otherwise.
3. **Pin the Testcontainers image.** Generated code uses `postgres:latest`,
   which silently changes under you and will not match the compose stack. Pin
   to the same version compose runs — currently `postgres:17-alpine`.

Then delete `HELP.md`.

## 3. Spring Boot 4 starter names

Boot 4 renamed things. Most tutorials you find online are Boot 3 and will not
match what Initializr gives you:

| Boot 3 | Boot 4 |
|---|---|
| `spring-boot-starter-web` | `spring-boot-starter-webmvc` |
| `flyway-core`, added manually | `spring-boot-starter-flyway` |
| one `spring-boot-starter-test` | modular: `-webmvc-test`, `-data-jpa-test`, `-flyway-test`, `-actuator-test` |
| `org.testcontainers:postgresql` | `org.testcontainers:testcontainers-postgresql` |
| `org.testcontainers.containers.PostgreSQLContainer` | `org.testcontainers.postgresql.PostgreSQLContainer` |

## 4. The integrationTest suite

Use Gradle **JVM Test Suites** (`testing { suites { ... } }`), not a hand-rolled
`sourceSets` block.

Three things must be wired, in the order they break:

1. **`implementation(project())`** — a new suite starts with an empty classpath.
   Without this it cannot see `main`'s classes or `application.yaml`.
2. **Its own test dependencies** — nothing is inherited from `test`. Testcontainers
   dependencies go in `integrationTest` **and nowhere else**: if they sit on the
   `test` classpath, a stray `@Testcontainers` quietly puts Docker back in the
   fast path.
3. **`shouldRunAfter(tasks.named("test"))`** — fail on a broken unit test before
   paying for a container.

Keep `test` deliberately minimal — `webmvc-test` and `validation-test` only.
Anything needing a real database belongs in `integrationTest`.

`TestcontainersConfiguration` is generated package-private. Make it `public`
(and its `@Bean` method too) or integration tests in sub-packages cannot
`@Import` it.

**`integrationTest` is not wired into `check`** — see FM-002. `./gradlew build`
stays container-free, and CI calls `./gradlew integrationTest` as its own
explicit step. That step is load-bearing; do not remove it as redundant.

## 5. Verify, do not assume

```bash
./gradlew tasks --all | grep -i integrationTest   # task exists
./gradlew clean test                              # ~1s, no container
./gradlew integrationTest                         # starts Postgres, passes
./gradlew build                                   # no container
```

To prove the container claim rather than trusting it, watch Docker while the
build runs — and filter, or you will catch unrelated containers on the machine:

```bash
docker events --filter type=container --format '{{.Action}} {{.Actor.Attributes.image}}' \
  | grep -Ei 'postgres|ryuk|testcontainers'
```

Finally, the clean-clone check — it catches files that are needed but ignored or
uncommitted:

```bash
git clone <repo> /tmp/cc && cd /tmp/cc && ./gradlew build
```

## 6. Ports

| Service | Port |
|---|---|
| api-gateway | 8080 |
| auth-service | 8081 |
| expense-service | 8082 |
| investment-service | 8083 |
| analytics-service | 8084 |

A **native PostgreSQL is running on this machine** holding `127.0.0.1:5432`, so
the compose stack maps Postgres to a different host port — see FM-003.
