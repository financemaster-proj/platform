# 0008 — Domain/persistence separation per service

- **Status:** Proposed — awaiting decision
- **Date:** 2026-11-18

## Context
ADR-0006 fixes the package layout but leaves open how strictly `domain/` is kept
free of persistence concerns. Two positions:

**Strict.** `domain/` contains pure Java with no Spring or JPA imports. A separate
JPA entity lives in `adapter/out/persistence/`, and mapping code moves between
them. Forces the realisation that a domain model and a persistence model are
different things — arguably the largest single step from "Spring Boot CRUD" to
designing real systems. Costs real mapping boilerplate.

**Pragmatic.** The JPA entity *is* the domain object, with behaviour on it. Far
less code. Persistence concerns leak into the domain: lazy loading, the no-arg
constructor requirement, mutable setters JPA needs, and annotations that bind the
model to a schema.

## Proposed decision
Split by service, chosen on the richness of each domain:

- **`expense-service`** — strict. Budgets, recurring rules and money arithmetic
  carry enough behaviour to justify the ceremony.
- **`auth-service`** — pragmatic. A `User` is close to a row; a second model would
  be mapping code with no insight attached.
- **`investment-service`** — decide after expense-service is built, with evidence.

Judging *when* the ceremony earns its cost is more valuable than applying one
rule uniformly.

## Open question
Confirm this split, or choose one approach for every service.

## Consequences if adopted
- Two services with different internal conventions; the reason must be documented
  in each README or the difference reads as inconsistency.
- A direct comparison of both approaches in one codebase, which is the point.
