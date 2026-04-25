# Backend Testing Strategy

Use this reference when designing or writing backend tests.

## Test Selection

- Unit tests: domain rules, pure functions, use-case branching, authorization decisions, retry/idempotency decisions.
- Repository/integration tests: query behavior, mappings, transactions, constraints, migrations, serialization, and generated clients.
- API contract tests: GraphQL schema, REST/OpenAPI, gRPC/protobuf compatibility, error shape, and auth boundaries.
- Regression tests: defects, security bugs, N+1 fixes, race conditions, and previously missing edge cases.

## DB And Transaction Policy

- 테스트는 실 DB, 공유 개발 DB, 운영 DB에 직접 연결하지 않는다.
- DB 동작 검증이 꼭 필요하면 repo가 이미 제공하는 isolated disposable test DB, embedded DB, Testcontainers, 또는 test double을 사용한다.
- 테스트 코드에 `@Transactional`을 붙여 rollback에 의존하지 않는다.
- 데이터 격리는 명시적 setup/cleanup, fixture lifecycle, schema reset, container 재생성 중 repo convention에 맞는 방식을 사용한다.
- 이 정책은 테스트 코드 기준이다. production use case의 transaction boundary 설계는 별도 아키텍처 규칙을 따른다.

## Presentation And Controller Tests

- Presentation/Controller layer 테스트는 선택 항목이다.
- 작성 전 사용자에게 “Controller/Presentation layer 테스트까지 작성할까요?”라고 확인한다.
- 확인 전에는 Service/UseCase/Domain 중심 테스트와 API contract 검증을 우선 제안한다.
- Controller 테스트가 필요한 경우는 request validation, auth context extraction, serialization/error shape, route binding이 실제 회귀 위험일 때다.

## When Not To Add Tests

- Do not add tests just to increase test count.
- 테스트는 비즈니스 로직, 분기, 인가, 쿼리, 오류 처리, 외부 호출, 회귀 위험을 보호할 때 작성한다.
- Do not add new tests for simple DTOs, constants, getters/setters, trivial constructors, framework annotations, or configuration wiring unless they encode business behavior or previously failed.
- Prefer compile, lint, schema generation, or existing smoke validation when there is no business logic, branch, authorization decision, query behavior, error mapping, external call, or regression risk.
- If skipping tests, state the reason and name the lighter validation that covers the change.

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
