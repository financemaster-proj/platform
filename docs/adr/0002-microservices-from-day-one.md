# 0002 — Microservices from day one

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
Finance Master is a single-user personal finance application. Its four modules
— expense, investments, analytics, auth — would comfortably fit in one process.

A modular monolith with enforced boundaries was recommended, with a deliberate
extraction of one service in a later phase.

The explicit purpose of this project, however, is to learn backend engineering,
not to ship the smallest sufficient system.

## Decision
Four business services plus an API gateway, separate databases and Kafka from
the start.

## Consequences

**Accepted costs**
- A substantial share of effort goes to distributed-systems plumbing the domain
  does not require.
- Debugging spans multiple processes and a message broker.
- Local development needs Postgres, Redis and Kafka running.
- The highest risk is not technical: it is losing momentum in infrastructure and
  never reaching the interesting domain work.

**Benefits**
- The transactional outbox, CQRS read models and zero-downtime migrations across
  independently deployed services cannot be learned in a monolith. These are the
  curriculum.

**Mitigations**
- Every sprint must ship something that works end to end.
- Infrastructure is introduced only in the sprint that needs it: Kafka in
  sprint 4, not sprint 0.
- ADR-0004 forbids synchronous service-to-service calls, which prevents the
  distributed monolith this architecture otherwise tends toward.
