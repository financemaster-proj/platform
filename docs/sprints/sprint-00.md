# Sprint 0 — Foundations

- **Goal:** `auth-service` boots, reaches a real Postgres through Flyway, has one
  green integration test against a container, and CI proves it on every push.
- **Committed:** 29 points across 10 tickets
- **Status:** not started

## Sprint goal in one sentence
A fresh clone plus `cp .env.example .env` plus `docker compose up` plus
`./gradlew bootRun` produces a running, self-documenting, tested service.

## Committed tickets

| ID | Title | Type | Pts |
|---|---|---|---|
| FM-001 | Create the six GitHub repositories | task | 1 |
| FM-002 | Gradle build conventions for a Spring Boot service | task | 3 |
| FM-003 | Local infrastructure stack via Docker Compose | task | 5 |
| FM-004 | auth-service boots with health check and OpenAPI | story | 3 |
| FM-005 | Flyway baseline migration for fm_auth | task | 2 |
| FM-006 | Testcontainers integration test harness | task | 5 |
| FM-007 | Reusable GitHub Actions CI workflow | task | 3 |
| FM-008 | Structured JSON logging with correlation IDs | task | 3 |
| FM-009 | RFC 9457 Problem Details error handling | task | 2 |
| FM-010 | Externalised configuration and .env.example | task | 2 |

Suggested order: FM-001 → FM-002 → FM-003 → FM-004 → FM-005 → FM-010 → FM-009
→ FM-008 → FM-006 → FM-007.

## On the estimate

29 points in a first sprint, part-time, with no velocity history, is very
probably an over-commitment. That is left deliberately uncorrected. The purpose
of the first sprint is to *measure* velocity, not to hit a number — finishing 18
of 29 points is a successful sprint that produces a real figure to plan sprint 1
with. Carry whatever does not finish.

Estimates being wrong is the lesson. Moving the goalposts to hide it is not.

## Retro

_To be completed at sprint close._

- What worked
- What did not
- One change for next sprint
