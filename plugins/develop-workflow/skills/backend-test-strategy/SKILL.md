---
name: backend-test-strategy
description: 백엔드 단위/통합/Repository/API contract/회귀/엣지/인가/failure-mode 테스트를 설계하거나 작성할 때 사용. 실 DB와 테스트 @Transactional을 피하고, 비즈니스 로직/회귀 위험이 있을 때만 테스트하며, Presentation/Controller 테스트는 작성 전 선택 확인한다.
argument-hint: "[테스트 작업]"
---

# 백엔드 테스트 전략

## 설명

사용자 요청에서 백엔드 테스트 설계 또는 작성이 필요한 경우 사용한다. 단위, 통합, Repository, API contract, 회귀, 엣지/경계값, authorization, failure-mode 테스트를 다룬다. 비즈니스 로직이나 회귀 위험이 없는 단순 코드에는 테스트를 추가하지 않는 결정을 명시할 수 있다. 테스트는 실 DB에 직접 연결하지 않고, 테스트 코드에서 `@Transactional` rollback에 의존하지 않는다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- JVM/Spring 테스트면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 기존 test framework, naming, fixture, module layout을 확인한다.
2. 테스트 가치가 있는 동작인지 먼저 판단한다: 비즈니스 규칙, 분기, authorization, query behavior, transaction, error mapping, external call, regression.
3. 단순 DTO, constant, configuration wiring, getter/setter, framework annotation만 바뀐 경우에는 별도 테스트를 만들지 않고 기존 compile/static validation을 우선한다.
4. Presentation/Controller layer 테스트가 필요해 보이면 바로 작성하지 말고 사용자에게 선택 여부를 묻는다.
5. 증명할 동작을 정한다: success, invalid input, authorization, missing resource, conflict, timeout/retry, regression.
6. 가장 좁은 테스트 유형을 선택한다: unit, repository slice, API contract, integration, full app.
7. DB 동작 검증이 꼭 필요하면 실 DB가 아니라 repo가 제공하는 isolated disposable test DB 또는 test double을 사용하고, 테스트 `@Transactional` rollback에 의존하지 않는다.
8. clock, ID, randomness, external client를 제어해 deterministic하게 만든다.
9. 영향 모듈의 scoped validation을 먼저 실행하고, shared behavior가 바뀌었을 때만 확장한다.

## 검증

- `./gradlew :{module}:test` 또는 repo의 기존 테스트 명령을 우선한다.
- Spring/JPA 쿼리면 repository slice 또는 `@DataJpaTest` 계열을 검토한다.
- 실 DB 연결이 필요한 명령은 실행하지 않는다.

## 주의사항

- 실수 방지 가드레일: 테스트 추가 시 실패해야 하는 회귀 케이스와 성공해야 하는 정상 케이스를 함께 둔다.
- 비즈니스 로직, 분기, 인가, 쿼리, 오류 처리, 회귀 위험이 없으면 테스트를 억지로 추가하지 않는다.
- 테스트 코드에 `@Transactional`을 붙여 rollback에 의존하지 않는다. 데이터 격리는 명시적 setup/cleanup 또는 disposable test DB로 처리한다.
- Presentation/Controller 테스트는 선택 항목이다. 작성 전 “Controller/Presentation layer 테스트까지 작성할까요?”라고 확인한다.
- 구현 세부사항보다 외부에서 관찰되는 동작을 검증한다.
- 느린 통합 테스트는 구체적 위험이 있을 때만 추가한다.

## 출력

테스트 시나리오와 필요한 경우 로컬 컨벤션에 맞춘 집중 테스트를 작성한다. 테스트를 만들지 않는 경우에는 비즈니스 로직 또는 회귀 위험이 없다는 근거와 대신 수행할 compile/static validation을 제시한다.
