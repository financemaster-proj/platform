# 0006 — Package by feature, not by layer

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
The conventional Spring Boot tutorial layout groups by technical layer:

```
com.example.app
├── controller/
├── service/
├── repository/
└── model/
```

This scatters a single feature across four packages, tells a reader nothing
about the domain, and makes every package a dumping ground that grows without
bound. Nothing can be made package-private, so every class is public and every
boundary is a convention rather than a constraint.

## Decision
Group by feature. Within a feature, separate by role:

```
com.financemaster.expense
├── expense/
│   ├── domain/              pure Java — no Spring, no JPA imports
│   ├── application/         use cases; the @Transactional boundary
│   └── adapter/
│       ├── in/web/          controller, request/response DTOs
│       ├── out/persistence/ JPA entity, repository
│       └── out/messaging/   outbox writer
├── category/
└── budget/
```

## Consequences

**Benefits**
- The package tree names the domain, so the structure is documentation.
- A feature can be understood, moved or deleted in one place.
- Cross-feature access becomes visible and reviewable rather than ambient.
- Classes can be package-private, making boundaries real.

**Accepted costs**
- More directories for a small feature.
- Where a feature genuinely belongs to two aggregates, placement requires a judgement call.
- Unfamiliar to anyone who has only seen the layered tutorial layout.

## Related
ADR-0008 decides how strictly `domain/` is kept free of persistence concerns,
which is a separate question from this layout.
