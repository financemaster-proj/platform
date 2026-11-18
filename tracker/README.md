# Finance Master — Tracker

A file-based issue tracker. One markdown file per ticket in `tickets/`, with YAML
frontmatter for the structured fields and markdown for everything else.

## Three ways to use it

### Web UI — the easy one

```bash
python3 platform/tracker/serve.py
```

Then open <http://127.0.0.1:7777>. Drag cards between columns, click a card to
edit its fields, tick acceptance criteria, write notes. Every change writes
straight back to the markdown file and regenerates `BOARD.md`.

Binds to localhost only. Nothing is exposed to your network.

### Command line

```bash
python3 platform/tracker/board.py                      # regenerate BOARD.md
python3 platform/tracker/board.py ls                   # list all tickets
python3 platform/tracker/board.py ls ready             # list by status
python3 platform/tracker/board.py status FM-001 in-progress
python3 platform/tracker/board.py set FM-001 points 3
```

Invalid statuses, types, epics and non-editable fields are rejected rather than
silently written.

### Editing the markdown directly

Always fine — the files are the source of truth. Run `board.py` afterwards so
`BOARD.md` matches.

`BOARD.md` is **generated**. Never edit it by hand; your changes will be lost.

## Why one file per ticket

Ticket history lives in git, per ticket. Editing one ticket produces a one-file
diff instead of rewriting a 2000-line backlog, and two people (or a human and an
agent) can touch different tickets without conflicts.

## Ticket format

```markdown
---
id: FM-012
title: Issue access and refresh tokens on login
type: story
epic: auth
service: auth-service
points: 5
status: backlog
sprint: 1
created: 2026-11-18
---

## Context
Why this ticket exists.

## Acceptance criteria
- [ ] Observable, testable statements

## Learning notes
The backend concepts this ticket is here to teach.
```

## Field vocabulary

| Field | Allowed values |
|---|---|
| `type` | `story` · `task` · `spike` · `bug` |
| `status` | `backlog` · `ready` · `in-progress` · `in-review` · `done` · `blocked` |
| `epic` | `auth` · `expense` · `investment` · `analytics` · `platform` · `observability` · `security` |
| `service` | repo name, or `-` for cross-cutting work |
| `points` | Fibonacci: 1, 2, 3, 5, 8, 13 |
| `sprint` | integer, or `-` for unscheduled backlog |

### What the types mean

- **story** — delivers user-observable behaviour. Has acceptance criteria.
- **task** — necessary engineering work with no user-visible outcome (CI, build config).
- **spike** — time-boxed investigation. Output is a decision or an ADR, *not* code.
- **bug** — something built that doesn't work as specified.

Using spikes properly matters. "Investigate outbox vs Debezium" is a spike whose
deliverable is `docs/adr/00XX-....md`. If you find yourself writing production
code inside a spike, it should have been a story.

## Workflow

```
backlog → ready → in-progress → in-review → done
```

- **backlog** — exists, not committed to a sprint
- **ready** — groomed: has acceptance criteria, is estimated, nothing blocks it
- **in-progress** — branch open
- **in-review** — PR open
- **done** — merged, and the Definition of Done is met

Branch naming: `feature/FM-012-short-slug`, `fix/FM-031-short-slug`.
Commit messages start with the ticket id: `FM-012: issue refresh token on login`.

## Roles

- **Claude** — writes and grooms tickets, sets estimates, writes docs and ADRs, reviews code.
- **Nithish** — writes all production code, moves ticket status, closes tickets.
