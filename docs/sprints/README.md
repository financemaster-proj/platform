# Roadmap

Ten sprints of two weeks. Each exists to teach something specific, and each ships
something that works end to end — [ADR-0002](../adr/0002-microservices-from-day-one.md)
names loss of momentum in infrastructure as this project's main risk, and this
sequencing is the mitigation.

| # | Sprint | Concept focus |
|---|---|---|
| 0 | Foundations | Build tooling, containerised infra, externalised config, CI, Testcontainers, docs-as-code |
| 1 | Auth service | Spring Security filter chain internals, Argon2, access/refresh token design, rotation with reuse detection |
| 2 | Gateway | Edge security, identity propagation, Redis rate limiting, correlation IDs across services |
| 3 | Expense service | Domain modelling, money arithmetic, JPA properly, N+1, cursor pagination, idempotent writes |
| 4 | Events | The dual-write problem, transactional outbox, at-least-once delivery, idempotent consumers, schema evolution |
| 5 | Investment service | Cost basis, realised vs unrealised P&L, resilient external integration, caching, scheduled work without duplicate runs |
| 6 | Analytics service | CQRS, eventual consistency, read-model replay and rebuild, async report generation |
| 7 | Observability | Metrics, structured logs and distributed traces across process boundaries; SLOs |
| 8 | Hardening | Load testing, connection pool and index tuning, security review, secrets management |
| 9 | Deployment | Containerising services, CI/CD with a staging environment, zero-downtime migrations, account-deletion saga |

Sprints 4, 6 and 9 are where the microservices choice pays for itself. The
outbox pattern, a replayable read model and zero-downtime migrations across
independently deployed services genuinely cannot be learned in a monolith.

## Sprint notes

One file per sprint: `sprint-NN.md`, holding the goal, the committed tickets,
what actually happened, and the retro. Written at planning, closed at review.
