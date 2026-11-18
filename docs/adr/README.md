# Architecture Decision Records

One file per significant decision, in [Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
Never delete or rewrite an accepted ADR — supersede it with a new one and update
the status. The value is the record of *why*, including the options rejected.

| # | Decision | Status |
|---|---|---|
| [0001](0001-one-repository-per-service.md) | One repository per service | Accepted |
| [0002](0002-microservices-from-day-one.md) | Microservices from day one | Accepted |
| [0003](0003-rs256-jwt-with-jwks.md) | RS256 JWT with JWKS, validated locally | Accepted |
| [0004](0004-no-synchronous-service-calls.md) | No synchronous service-to-service calls | Accepted |
| [0005](0005-transactional-outbox.md) | Transactional outbox for event publication | Accepted |
| [0006](0006-package-by-feature.md) | Package by feature, not by layer | Accepted |
| [0007](0007-docs-as-code-and-file-tracker.md) | Docs-as-code and a file-based tracker | Accepted |
| [0008](0008-domain-persistence-separation.md) | Domain/persistence separation per service | **Proposed** |
