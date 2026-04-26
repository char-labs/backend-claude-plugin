# Backend Architecture Principles

Use this reference when designing, implementing, or reviewing backend code for maintainability, testability, and clear ownership.

## Core Rules

- Keep dependency direction stable: delivery adapters depend on application use cases, application depends on domain ports, infrastructure implements ports.
- Keep domain behavior close to the domain model. Avoid services that only shuttle data between repositories and DTOs.
- Separate external DTOs, persistence entities, commands, queries, and domain models unless the codebase already has a narrower established pattern.
- Put transaction ownership at the application/use-case boundary. Avoid starting transactions in low-level helpers or mixing remote calls inside long database transactions.
- Prefer explicit interfaces for external systems, clocks, ID generators, and persistence boundaries when behavior must be tested or swapped.
- Keep error boundaries intentional: domain errors should not leak framework exceptions, SQL exceptions, HTTP client details, or stack traces to callers.
- Favor small cohesive classes. A class that validates, authorizes, orchestrates, maps, persists, sends events, and formats responses is doing too much.

## SOLID Review

- Single Responsibility: each class should have one reason to change.
- Open/Closed: add new behavior with cohesive extension points, not scattered conditionals across unrelated layers.
- Liskov Substitution: subclasses and implementations must preserve contracts, nullability, error behavior, and side effects.
- Interface Segregation: do not force clients to depend on methods they do not use.
- Dependency Inversion: high-level policy should depend on abstractions, not concrete infrastructure.

## Layering Checks

- Controllers should validate transport shape, authenticate/authorize at the boundary, call one use case, and map the result.
- Use cases should coordinate domain behavior, transactions, repositories, and side effects.
- Domain objects should avoid framework annotations unless the project intentionally uses an active-record or entity-domain model.
- Repositories should not contain business decisions beyond persistence-specific query shape.
- Infrastructure adapters should isolate vendor SDKs, SQL/JPA details, HTTP clients, and serialization quirks.

## Failure Mode Checks

- Every external call has timeout, retry policy where appropriate, and typed error handling.
- Retries are idempotent or protected by idempotency keys.
- Partial failure paths are explicit for database write plus event publish, file write plus metadata persist, and remote call plus local state update.
- Logs include correlation context but never secrets or sensitive payloads.

## Review Heuristics

- Look for cyclic dependencies, framework leakage into domain code, hidden global state, magic strings for business rules, and static helpers that hide dependencies.
- Prefer a small concrete fix over a broad rewrite. Recommend refactors only when the current change increases coupling or makes important behavior untestable.
- If the repository has a clear local convention, apply it unless it conflicts with security or correctness.
