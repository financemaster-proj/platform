# Finance Master — documentation

A personal finance system, built as a vehicle for learning backend engineering
properly. Java 21, Spring Boot, four services, Kafka, Postgres.

## Start here

| | |
|---|---|
| [Architecture overview](architecture/overview.md) | Services, boundaries, events, conventions |
| [Decision records](adr/README.md) | Every significant decision and why |
| [Definition of Done](definition-of-done.md) | What "finished" means on this project |
| [Roadmap](sprints/README.md) | Ten sprints, and the concept each one teaches |
| [Expense domain](domain/expense.md) | Aggregates, invariants and the decisions behind sprint 3 |
| [Board](../tracker/BOARD.md) | Current tickets |
| [Tracker conventions](../tracker/README.md) | Ticket format and workflow |

## Repositories

All under [`financemaster-proj`](https://github.com/financemaster-proj), cloned
as siblings under one local parent folder.

| Repo | Responsibility |
|---|---|
| `platform` | infrastructure, event contracts, docs, tracker |
| `api-gateway-backend` | edge routing, JWT validation, rate limiting |
| `auth-service-backend` | identity and tokens |
| `expense-service-backend` | expenses, categories, budgets |
| `investment-service-backend` | holdings, trades, valuations |
| `analytics-service-backend` | read models and reports |

## Working agreement

- **Claude** plans, writes tickets and docs, estimates, and reviews code.
- **Nithish** writes all production code.

The split is deliberate. Code that arrives already written teaches nothing, so
the pattern per concept is: discuss the concept, you implement it, it gets
reviewed like a senior would review it.
