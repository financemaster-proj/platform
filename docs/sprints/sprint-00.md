# Sprint 0 — Foundations

- **Goal:** `expense-service` boots, reaches a real Postgres through Flyway, has
  green integration tests against a container, and CI proves it on every push.
- **Committed:** 26 points across 10 tickets
- **Status:** in progress — 9 of 26 points done

Originally planned against `auth-service`. Retargeted to `expense-service`,
which is now the first service built; `auth-service` follows in sprint 1.

## Sprint goal in one sentence
A fresh clone plus `cp .env.example .env` plus `docker compose up` plus
`./gradlew bootRun` produces a running, self-documenting, tested service.

## Committed tickets

| ID | Title | Type | Pts | Status |
|---|---|---|---|---|
| FM-001 | Create the six GitHub repositories | task | 1 | done |
| FM-002 | Gradle build conventions for a Spring Boot service | task | 3 | done |
| FM-003 | Local infrastructure stack via Docker Compose | task | 5 | done |
| FM-004 | Externalised configuration and .env.example | task | 2 | ready |
| FM-005 | Flyway baseline migration for fm_expense | task | 2 | ready |
| FM-006 | Testcontainers integration test harness | task | 3 | ready |
| FM-007 | expense-service boots with health check and OpenAPI | story | 2 | ready |
| FM-008 | Structured JSON logging with correlation IDs | task | 3 | ready |
| FM-009 | RFC 9457 Problem Details error handling | task | 2 | ready |
| FM-010 | Reusable GitHub Actions CI workflow | task | 3 | ready |

**Ticket ids are in execution order.** The remaining seven run FM-004 → FM-010.

Three dependencies make that order load-bearing rather than arbitrary:

- FM-004 first, because `application.yaml` already references `${DB_URL}` with
  nothing defining it and no profile split. Nothing below boots until it does.
- FM-008 before FM-009, because the Problem Details 500 response carries the
  correlation ID, which has to exist first.
- FM-010 last, because there is no point wiring CI before there is a green
  integration suite for it to run.

## On the estimate

The original commitment was 29 points across 10 tickets. It is now 26 across the
same 10 — not because the goalposts moved, but because FM-004 and FM-007 are
partly built and were re-estimated down from 3 to 2 each, and FM-006's harness
had already been started.

29 points in a first sprint, part-time, with no velocity history, was very
probably an over-commitment. That remains deliberately uncorrected. The purpose
of sprint 0 is to **measure** velocity, not to hit a number — finishing 18 of 26
is a successful sprint that produces a real figure to plan sprint 3 with. Carry
whatever does not finish.

Estimates being wrong is the lesson. Moving the goalposts to hide it is not.

## Progress notes

**FM-003** surfaced a machine-specific obstacle worth remembering: a native
PostgreSQL service holds `127.0.0.1:5432` on this laptop, so the compose
container is mapped to a different host port and that port belongs in `.env` as
`DB_PORT`. Per-database role isolation was verified with a failed cross-database
connect, which is what makes "database per service" a property rather than a
comment. Grafana is unverified and is left for sprint 7.

**FM-007** verified health behaviour ahead of its ticket: 503 rather than
200-with-a-DOWN-body, failing in ~4ms rather than blocking on Hikari's timeout,
and self-recovering when Postgres returned. Details are in the ticket.

**Known risk carried into FM-007:** springdoc 2.8.6 is pinned by hand and
targets Spring Framework 6, while this service runs Boot 4.1.2 on Framework 7.
That combination is unverified upstream.

## Retro

_To be completed at sprint close._

- What worked
- What did not
- One change for next sprint
