# Definition of Done

A ticket is done when **all** of the following hold. This is deliberately strict:
the discipline is the point, and "I'll add tests later" is how a learning project
becomes an unmaintainable one.

- [ ] Acceptance criteria on the ticket are all met
- [ ] Unit tests cover the domain logic, and `./gradlew test` runs in under 5 seconds
- [ ] Integration tests cover the happy path and at least one failure path, against real Postgres via Testcontainers
- [ ] Any schema change is a Flyway migration — never `ddl-auto`, never an edited applied migration
- [ ] OpenAPI reflects any API change
- [ ] Errors return RFC 9457 Problem Details and leak no internals
- [ ] New log lines are structured and carry the correlation id; no secrets logged
- [ ] Any architectural decision made along the way is recorded as an ADR
- [ ] CI is green on the branch
- [ ] PR description references the ticket id and says what was *decided*, not only what changed
- [ ] Ticket `status` set to `done` and `tracker/board.py` re-run

## Additionally, for anything touching money
- [ ] `BigDecimal` with explicit scale, never `double` or `float`
- [ ] Currency explicit on every amount — no implicit default
- [ ] A test asserting that rounding behaves as specified at the scale boundary

## Additionally, for anything user-scoped
- [ ] Every query filters by `user_id`
- [ ] A test proving another user's record returns 404, not 403 — a 403 confirms the record exists
