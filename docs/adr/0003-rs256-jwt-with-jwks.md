# 0003 — RS256 JWT with JWKS, validated locally

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
Four services behind a gateway must all establish caller identity. Options:

1. **Opaque tokens, introspected at auth-service.** Every request in the system
   becomes a synchronous call to auth-service. Easy revocation, but auth-service
   becomes a single point of failure on the hot path of every request.
2. **Symmetric JWT (HS256), shared secret.** No network calls, but the signing
   secret must be distributed to all five services, and any one of them could
   then mint tokens. A compromise anywhere is a compromise everywhere.
3. **Asymmetric JWT (RS256) with published JWKS.** auth-service holds the private
   key alone; every other service validates locally with the public key.

## Decision
Option 3. auth-service signs with an RSA private key and publishes the public key
at `GET /.well-known/jwks.json`. Every other service fetches and caches it, and
validates tokens locally with no network call.

Token design:

| | Lifetime | Storage |
|---|---|---|
| Access token | 15 minutes | Stateless JWT, never persisted |
| Refresh token | 30 days | Opaque random string, stored **hashed** in Redis, rotated on every use |

Refresh rotation uses reuse detection: a token presented twice revokes the whole
family, on the assumption it was stolen.

## Consequences

**Benefits**
- auth-service being down does not break already-authenticated requests anywhere.
- Only auth-service can mint tokens. No shared signing secret exists.
- Validation costs no network round trip.

**Accepted costs**
- An access token cannot be revoked before it expires. The 15-minute lifetime is
  what bounds that exposure, and is the reason it is short.
- Key rotation requires a `kid`-aware JWKS with an overlap window.
- Services must handle JWKS fetch failure on cold start.

## Related
ADR-0004 — the gateway validates *and forwards* the token; each service validates
independently. Defence in depth, and it keeps services safe if reached directly.
