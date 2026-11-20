# Expense domain model

What `expense-service` owns, the invariants it enforces, and the decisions taken
on 2026-11-20 that the sprint 3 tickets are built on.

Scope boundary: this service owns expenses, categories, budgets and recurring
rules. It does **not** own reports — "spending by category over time" belongs to
`analytics-service`. Budget *consumption* stays here, because it is an invariant
of the budget aggregate and the input to `BudgetExceeded`.

## Aggregates

| Aggregate | Owns | Key invariant |
|---|---|---|
| `Category` | a user's spending categories | name unique per user, among non-deleted rows |
| `Expense` | one recorded spend | non-negative amount, a real category, a date not in the future |
| `Budget` | a limit for one category in one month | one budget per (user, category, month) |
| `RecurringRule` | a repeating expense description | materialises each occurrence at most once |

`user_id` is a UUID on every table with **no foreign key** — the users table
lives in `auth-service`'s database and a cross-database FK cannot exist
([ADR-0004](../adr/0004-no-synchronous-service-calls.md)). Every query filters by
it, and another user's record returns **404, not 403**.

## Decisions taken

### Pragmatic domain model
The JPA entity *is* the domain object, with behaviour on it.
[ADR-0008](../adr/0008-domain-persistence-separation.md) proposed a strict split
for this service; pragmatic was chosen instead, for every service. FM-011
records it and carries the guardrails that keep it from decaying into a layered
CRUD app — chiefly that behaviour lives on the entity, and that anything with an
invariant exposes intention-named methods rather than setters.

### Single currency, explicitly
INR only. A non-INR amount is rejected at the web boundary. Currency remains
explicit in the column, in the `Money` type and in the JSON, so a second
currency is a migration and a validation change rather than a redesign. No FX
rate exists anywhere in this service.

### Soft delete everywhere
`deleted_at` on every table. Three consequences, each costing something:

1. **Uniqueness becomes partial.** `UNIQUE (user_id, name) WHERE deleted_at IS
   NULL`, or a deleted "Groceries" permanently reserves the name.
2. **Every read needs two predicates.** `user_id` *and* `deleted_at IS NULL`.
   Forgetting the second is the same class of bug as forgetting the first:
   invisible in testing, serious in production. Where that predicate lives is
   decided once in FM-013 and documented, not scattered by hand.
3. **Account deletion must still hard-delete.** The sprint 9 `UserDeleted` saga
   purges rows; soft-deleting on account deletion is not deletion, and
   `UserDataPurged` would be a false claim.

### An expense happens on a date, not an instant
`spent_on` is `DATE`. Audit columns (`created_at`, `updated_at`) are
`TIMESTAMPTZ`. "I bought coffee on the 14th" is true regardless of UTC offset;
storing it as an instant invents a whose-midnight question that then silently
decides which month a late-evening expense lands in — which changes budget
totals.

### Money
`@Embeddable`, `BigDecimal` with scale set explicitly to 2 on construction,
currency non-null, negative amounts rejected. `NUMERIC(19,2)` in Postgres —
never `float8`, never Postgres's `money` type. On the wire:
`{"amount": "1234.50", "currency": "INR"}`, amount a **string**.

### Recurring rules are in sprint 3, made safe by a constraint
The roadmap puts scheduled work in sprint 5. Pulling materialisation forward is
a deliberate choice, so the design must be one that cannot duplicate rather than
one unlikely to: a unique constraint on `(rule_id, occurrence_date)` makes a
double run *harmless*. Locking and leader election become a sprint 5
optimisation rather than a correctness fix.

This is the third appearance of one idea — `Idempotency-Key` on writes (FM-015),
`eventId` for idempotent consumers (sprint 4), and the occurrence constraint
here. All three push correctness to the one place that genuinely serialises.

## API surface after sprint 3

```
POST   /api/v1/categories                   201, Location
GET    /api/v1/categories
GET    /api/v1/categories/{id}
PATCH  /api/v1/categories/{id}
DELETE /api/v1/categories/{id}              204, soft

POST   /api/v1/expenses                     201, Idempotency-Key required
GET    /api/v1/expenses                     cursor paginated, filtered
GET    /api/v1/expenses/{id}
PATCH  /api/v1/expenses/{id}
DELETE /api/v1/expenses/{id}                204, soft

POST   /api/v1/budgets
GET    /api/v1/budgets?month=2026-03
PUT    /api/v1/budgets/{id}
DELETE /api/v1/budgets/{id}
GET    /api/v1/budgets/{id}/consumption
GET    /api/v1/budgets/consumption?month=2026-03

CRUD   /api/v1/recurring-rules
GET    /api/v1/recurring-rules/{id}/preview?months=3
```

Cursor sort key is `(spent_on DESC, id DESC)` — a total order. `spent_on` alone
is not, and a cursor over a non-total order skips or repeats rows.

## Explicitly out of scope for sprint 3

- **Events.** `ExpenseRecorded`, `ExpenseUpdated`, `ExpenseDeleted` and
  `BudgetExceeded` are sprint 4's outbox work
  ([ADR-0005](../adr/0005-transactional-outbox.md)). Writing the publish side
  now means writing the dual-write bug the outbox exists to fix.
- **Reports.** `analytics-service` owns them, built from those events.
- **Real authentication.** `user_id` comes from a stub behind one interface until
  sprint 1, so that sprint replaces one class rather than every controller.
- **Attachments, splitting an expense between categories, multi-currency, FX.**
