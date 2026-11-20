# Sprint 3 — Expense service

- **Goal:** the expense domain, end to end: categories, expenses, budgets and
  recurring rules, with money arithmetic, cursor pagination, idempotent writes
  and a measured query plan.
- **Planned:** 43 points across 13 tickets — **more than one sprint**. See the
  commit line below.
- **Status:** not started

Sprints 1 (auth) and 2 (gateway) come first in the roadmap. This plan is written
now because sprint 0's foundation tickets are shaped by it — FM-005's partial
unique index exists because of the soft-delete decision taken here.

The domain model, the decisions behind it and what is deliberately excluded are
in [`docs/domain/expense.md`](../domain/expense.md).

## Planned tickets

| ID | Title | Type | Pts |
|---|---|---|---|
| FM-011 | Record ADR-0008 as accepted — pragmatic domain model | task | 1 |
| FM-012 | Money as an embeddable value object, INR-only at the boundary | story | 3 |
| FM-013 | Category CRUD — the first full feature slice | story | 5 |
| FM-014 | Migration — expenses and the idempotency table | task | 2 |
| FM-015 | Record an expense — POST with Idempotency-Key | story | 5 |
| FM-016 | Read, update and soft-delete a single expense | story | 3 |
| FM-017 | List expenses — cursor pagination and filters | story | 5 |
| FM-018 | N+1 on the expense list — reproduce it, then fix it | story | 3 |
| FM-019 | Index and query plan for the expense list path | task | 2 |
| FM-020 | Budget aggregate — set a monthly budget per category | story | 3 |
| FM-021 | Budget consumption — spent against limit in one query | story | 3 |
| FM-022 | Recurring expense rules — model and CRUD | story | 3 |
| FM-023 | Materialise recurring expenses — safe under double runs | story | 5 |

Ticket ids are in dependency order. FM-011 blocks everything — a domain model
written before that decision gets rewritten after it.

## The commit line

**Do not commit all 43 points.** Sprint 0's actual velocity sets the number, and
that figure does not exist yet.

Three natural cut points, in order of preference:

1. **FM-011 → FM-019 (29 pts).** Categories and expenses complete, with
   pagination, the N+1 lesson and a measured query plan. Budgets and recurring
   rules carry to sprint 4 or later. This is the coherent slice: a working
   expense tracker.
2. **FM-011 → FM-021 (35 pts).** Adds budgets, which is what sprint 4's
   `BudgetExceeded` event needs. Choose this only if sprint 0 comes in above 20
   points.
3. **All 13 (43 pts).** Only with real velocity evidence supporting it.

Recurring rules (FM-022, FM-023) are the first thing to drop. They were pulled
into sprint 3 by choice rather than by dependency, and FM-023 is the one ticket
here whose correctness does not come from a request/response cycle.

## What this sprint teaches

| Concept | Where it lands |
|---|---|
| Money that cannot be got wrong | FM-012 |
| User scoping, and 404 over 403 | FM-013, every ticket after |
| The real cost of soft delete | FM-005, FM-013, FM-014 |
| Date vs instant | FM-014, FM-021 |
| Idempotent writes | FM-015 |
| Optimistic locking | FM-016 |
| Cursor pagination over a total order | FM-017 |
| N+1, measured rather than assumed | FM-018 |
| Reading a query plan, and composite index order | FM-019 |
| Invariants on the entity | FM-020 |
| Aggregating in SQL, not in Java | FM-021 |
| Correctness from a constraint rather than a lock | FM-023 |

## Retro

_To be completed at sprint close._
