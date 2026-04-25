# Backend Testing Strategy

Use this reference when designing or writing backend tests.

## Test Selection

- Unit tests: domain rules, pure functions, use-case branching, authorization decisions, retry/idempotency decisions.
- Repository/integration tests: query behavior, mappings, transactions, constraints, migrations, serialization, and generated clients.
- API contract tests: GraphQL schema, REST/OpenAPI, gRPC/protobuf compatibility, error shape, and auth boundaries.
- Regression tests: defects, security bugs, N+1 fixes, race conditions, and previously missing edge cases.

## Required Scenarios

- Happy path with realistic input.
- Invalid input and boundary values.
- Unauthorized and forbidden access, especially object-level authorization.
- Missing resource, conflict, duplicate, and partial failure behavior.
- Timeouts/retries/idempotency where external calls exist.

## Test Hygiene

- Match existing test frameworks and naming.
- Keep tests deterministic: control clocks, IDs, randomness, and external clients.
- Prefer focused fixtures over broad application boot where possible.
- Do not assert implementation details unless they are the behavior being protected.

## Spring/Kotlin

- Use JUnit 5, Mockito/MockK, Spring test slices, or project conventions already present.
- Prefer `@DataJpaTest` or repository slice tests for query behavior.
- Use `@SpringBootTest` only when wiring, config, or full integration is the behavior under test.
- Kotlin test names may use backticks if that is already the local style.
