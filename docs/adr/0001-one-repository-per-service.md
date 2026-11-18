# 0001 — One repository per service

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
Six deployable units are planned. Two layouts were considered: a single monorepo
with one subproject per service, or one git repository per service.

A monorepo was recommended, on the grounds that a solo developer gets atomic
cross-service changes, one CI configuration and one command to boot everything,
while still producing independently deployable artifacts.

## Decision
One repository per service, under the `financemaster-proj` GitHub organisation,
all public:

| Repo | |
|---|---|
| `api-gateway-backend` | edge routing and JWT validation |
| `auth-service-backend` | identity and tokens |
| `expense-service-backend` | expenses, categories, budgets |
| `investment-service-backend` | holdings, trades, valuations |
| `analytics-service-backend` | read models and reports |
| `platform` | infrastructure, contracts, docs, tracker |

Deployable services carry a `-backend` suffix so they stay distinguishable once
frontend repos exist alongside them. `platform` does not, because it is not a
backend service — it holds documentation, infrastructure and the tracker.

Note the distinction used throughout these docs: the **service** is
`auth-service`, the **repository** that contains it is `auth-service-backend`.

## Consequences

**Accepted costs**
- A change spanning producer and consumer requires two pull requests and cannot
  be atomic.
- CI configuration must be shared via reusable workflows or duplicated.
- Nothing runs locally without the `platform` repo cloned alongside.
- Contract-breaking changes cannot be caught by a compiler across the boundary.

**Benefits**
- Changing a producer and its consumer atomically is *impossible*, which forces
  backward-compatible schema evolution — expand/contract, additive-only, versioned
  events. A monorepo permits cheating here; this layout does not. Given that
  learning contract versioning is an explicit project goal, this is the main
  argument in favour.
- Each service has genuinely independent history and release cadence.

**Mitigations**
- `platform/.github/workflows/java-service.yml` as a reusable workflow (FM-007).
- Event schemas in `platform/contracts/` as the single source of truth.
- All six repos cloned as siblings locally so tooling can see across them.

## Reversibility
Cheap in both directions. `git filter-repo` merges repos into a monorepo, or
`git subtree split` extracts one, both preserving history.
