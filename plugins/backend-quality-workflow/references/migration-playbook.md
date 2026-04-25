# Migration Playbook

Use this reference for schema, data, storage, service, or contract migrations.

## Plan Shape

- Current state: data model, traffic, writers/readers, owners, dependencies, and known risks.
- Target state: desired model, compatibility contract, operational requirements, and acceptance criteria.
- Strategy: expand/contract, dual-write, backfill, replay, blue-green, strangler, or big-bang with explicit rationale.
- Rollout: stages, feature flags, traffic slices, validation gates, and rollback points.
- Observability: metrics, logs, alerts, dashboards, and manual checks.

## Data Safety

- Define source of truth during each phase.
- Make backfills idempotent and resumable.
- Protect against duplicate writes, lost updates, partial replay, and out-of-order events.
- Validate counts, checksums, constraints, and business invariants.

## Compatibility

- Preserve API/protobuf/schema compatibility unless a breaking change is approved.
- Support old and new readers/writers during transition when needed.
- Version messages, columns, events, or endpoints only when additive compatibility is insufficient.

## ADR Triggers

- New storage technology, new service boundary, major schema redesign, auth model change, consistency model change, or external provider replacement.
