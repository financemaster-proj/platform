# 0005 — Transactional outbox for event publication

- **Status:** Accepted
- **Date:** 2026-11-18

## Context
When `expense-service` records an expense, two things must happen: a row is
written, and an `ExpenseRecorded` event is published so analytics can react.

Writing to the database and publishing to Kafka are two separate systems and
cannot share a transaction. This is the **dual-write problem**. If the database
commits and the Kafka publish then fails, analytics never learns about the
expense and is silently, permanently wrong. Reversing the order is no better: a
published event for a transaction that then rolls back describes something that
never happened.

Retrying the publish inside the transaction does not solve it either — the
process can die between commit and publish.

## Decision
The transactional outbox pattern.

1. In one database transaction, write the domain row **and** an `outbox` row.
2. A separate poller reads unpublished outbox rows, publishes to Kafka, marks
   them published.

Started as a Spring `@Scheduled` poller. Debezium CDC is a possible later
refinement and would be its own ADR.

## Consequences

**Benefits**
- The event is as durable as the data. One transaction, no window to lose it.
- Survives Kafka being down entirely — events accumulate and drain on recovery.

**Accepted costs**
- Delivery becomes **at-least-once**, never exactly-once. A publish can succeed
  and the "mark published" update can fail, so the event goes out twice.
  Therefore **every consumer must be idempotent**, keyed on `eventId` against a
  `processed_events` table. This is not optional; it is the other half of the pattern.
- Added latency equal to the poll interval.
- The outbox table needs a cleanup job or it grows without bound.
- Ordering is only guaranteed per Kafka partition key, i.e. per aggregate.

## Related
ADR-0004 — events are the only cross-service communication, which makes this
pattern load-bearing rather than incidental.
