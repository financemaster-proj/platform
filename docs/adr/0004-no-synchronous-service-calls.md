# 0004 — No synchronous service-to-service calls

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
The most common failure mode of a microservice architecture is a mesh of
synchronous HTTP calls between services. The result has the operational cost of
distribution and the coupling of a monolith, plus cascading failure: any service
being slow makes every service upstream of it slow.

Examined honestly, no part of this domain needs fresh data from another service.
Analytics being seconds behind is acceptable, which is unusually convenient.

## Decision
No service calls another service synchronously. Ever.

Permitted traffic:
- Gateway → service (synchronous HTTP, the only inbound path)
- Service → Kafka (asynchronous publish)
- Kafka → service (asynchronous consume)
- Service → auth-service JWKS (cached, on startup and on key rotation)

## Consequences

**Benefits**
- No cascading failures between business services.
- The dependency graph has no cycles and no runtime coupling.
- Each service is independently deployable in practice, not just in theory.

**Accepted costs**
- Data a service needs must be in its own database or arrive by event.
- Some duplication across service databases is expected and correct.
- Operations spanning services become sagas, with no transaction to roll back.

## Enforcement
Reaching for a synchronous call is a signal that a boundary is wrong. Treat it as
a design review trigger, not a thing to work around. No HTTP client pointing at
another service passes review.
