# Finance Master

A personal finance system built as a vehicle for learning backend engineering.
Java 21, Spring Boot, four services, Kafka, Postgres. Polyrepo: six public repos
under the `financemaster-proj` GitHub org, cloned as siblings in this folder.

Deployable services use a `-backend` suffix (`auth-service-backend`); `platform`
does not. The **service** is `auth-service`; its **repo** is
`auth-service-backend`. Keep that distinction in docs.

## Working agreement — important

- **Claude plans. Nithish codes.**
- **Commits: `platform` is Claude's, the service repos are Nithish's.**
  Claude commits and pushes in `platform` (docs, ADRs, tracker - its own work).
  Claude **never** commits or pushes in any `*-backend` repo; it leaves changes
  in the working tree and says what changed and why, so Nithish can write the
  commit message from it.
- Claude writes tickets, estimates, docs, ADRs, and reviews code like a senior engineer would.
- Claude does **not** write production code unless explicitly asked for a specific snippet.
- Tracker and project tooling (`platform/tracker/`) are Claude's to maintain.
- When teaching a concept: discuss it, Nithish implements, Claude reviews.

## Read before planning work

- `platform/docs/architecture/overview.md` — boundaries, events, API conventions
- `platform/docs/adr/README.md` — every decision and its rationale
- `platform/docs/definition-of-done.md` — what finished means
- `platform/tracker/README.md` — ticket format and workflow

## Non-negotiables

- **No synchronous service-to-service HTTP calls.** Ever. (ADR-0004)
- **Money is `BigDecimal` with explicit scale and explicit currency.** Never `double`.
  On the wire it is a JSON *string*.
- **Schema changes are Flyway migrations.** `ddl-auto` stays `validate`. Never edit an applied migration.
- **No secrets committed.** `.env` is gitignored; `.env.example` is the documentation.
- **Every query is user-scoped**, and another user's record returns 404, not 403.
- **Package by feature, not by layer.** (ADR-0006)
- Integration tests use Testcontainers against real Postgres. Never H2.

## Tracker

Tickets are markdown files in `platform/tracker/tickets/FM-NNN.md` with YAML
frontmatter. After any ticket change, regenerate the board:

```bash
python3 platform/tracker/board.py
```

`BOARD.md` is generated — never hand-edit it. The script also validates
frontmatter and reports problems.

Branches: `feature/FM-012-short-slug`. Commits start with the ticket id.

## Open decisions

- **ADR-0008** — **decided 2026-11-20: pragmatic in every service** — the JPA
  entity is the domain object. ADR-0008 still says Proposed; FM-011 updates it.
- **Investment market scope** — Indian equities and mutual funds in INR, or US
  equities? Determines the market data provider and the whole investment domain
  model (NAV-based MF units, SIPs and corporate actions vs simple ticker prices).
