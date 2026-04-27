# 백엔드 테스트 전략

백엔드 테스트를 설계하거나 작성할 때 이 자료를 사용한다.

## 테스트 선택 기준

- 단위 테스트: 도메인 규칙, 순수 함수, 유스케이스 분기, 인가 결정, retry/idempotency 결정.
- Repository/통합 테스트: 쿼리 동작, mapping, transaction, constraint, migration, serialization, generated client.
- API contract 테스트: GraphQL schema, REST/OpenAPI, gRPC/protobuf 호환성, error shape, auth boundary.
- 회귀 테스트: defect, security bug, N+1 수정, race condition, 이전에 누락된 edge case.

## DB와 트랜잭션 정책

- 테스트는 실 DB, 공유 개발 DB, 운영 DB에 직접 연결하지 않는다.
- DB 동작 검증이 꼭 필요하면 repo가 이미 제공하는 isolated disposable test DB, embedded DB, Testcontainers, 또는 test double을 사용한다.
- 테스트 코드에 `@Transactional`을 붙여 rollback에 의존하지 않는다.
- 데이터 격리는 명시적 setup/cleanup, fixture 생명주기, schema reset, container 재생성 중 repo convention에 맞는 방식을 사용한다.
- 이 정책은 테스트 코드 기준이다. production use case의 트랜잭션 경계 설계는 별도 아키텍처 규칙을 따른다.

## Presentation/Controller 테스트

- Presentation/Controller layer 테스트는 선택 항목이다.
- 작성 전 사용자에게 “Controller/Presentation layer 테스트까지 작성할까요?”라고 확인한다.
- 확인 전에는 Service/UseCase/Domain 중심 테스트와 API contract 검증을 우선 제안한다.
- Controller 테스트가 필요한 경우는 request validation, auth context extraction, serialization/error shape, route binding이 실제 회귀 위험일 때다.

## 테스트를 추가하지 않아도 되는 경우

- 테스트 개수만 늘리기 위해 테스트를 추가하지 않는다.
- 테스트는 비즈니스 로직, 분기, 인가, 쿼리, 오류 처리, 외부 호출, 회귀 위험을 보호할 때 작성한다.
- 단순 DTO(simple DTOs), constants, getter/setter, trivial constructor, framework annotation, configuration wiring은 비즈니스 동작을 담거나 과거에 실패한 이력이 없다면 새 테스트를 추가하지 않는다.
- 비즈니스 로직, 분기, 인가 결정, 쿼리 동작, 오류 mapping, 외부 호출, 회귀 위험이 없다면 compile, lint, schema generation, 기존 smoke validation을 우선한다.
- 테스트를 생략한다면 이유와 변경을 커버하는 더 가벼운 검증 방법을 명시한다.

## 필수 시나리오

- 현실적인 입력을 사용한 happy path.
- invalid input과 boundary value.
- unauthorized/forbidden access, 특히 object-level authorization.
- missing resource, conflict, duplicate, partial failure 동작.
- 외부 호출이 있는 경우 timeout, retry, idempotency.

## 테스트 위생

- 기존 test framework와 naming을 따른다.
- clock, ID, randomness, external client를 제어해 테스트를 deterministic하게 유지한다.
- 가능하면 넓은 application boot보다 focused fixture를 우선한다.
- 보호하려는 동작 자체가 아니라면 구현 세부사항을 assert하지 않는다.

## Spring/Kotlin

- JUnit 5, Mockito/MockK, Spring test slice, 또는 프로젝트에 이미 있는 convention을 사용한다.
- 쿼리 동작은 `@DataJpaTest` 또는 repository slice test를 우선한다.
- wiring, config, full integration 자체가 검증 대상일 때만 `@SpringBootTest`를 사용한다.
- Kotlin test name은 로컬 스타일이 이미 그렇다면 backtick을 사용할 수 있다.
