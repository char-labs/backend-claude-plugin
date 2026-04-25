---
name: backend-test-strategy
description: 백엔드 단위/통합/Repository/API contract/회귀/엣지/인가/failure-mode 테스트를 설계하거나 작성할 때 사용. 테스트가 없거나 변경 검증이 필요할 때 우선 사용.
argument-hint: "[테스트 작업]"
---

# Backend Test Strategy

## 설명

`$ARGUMENTS`에서 백엔드 테스트 설계 또는 작성이 필요한 경우 사용한다. 단위, 통합, Repository, API contract, 회귀, 엣지/경계값, authorization, failure-mode 테스트를 다룬다.

## 상세 자료

- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- JVM/Spring 테스트면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 기존 test framework, naming, fixture, module layout을 확인한다.
2. 증명할 동작을 정한다: success, invalid input, authorization, missing resource, conflict, timeout/retry, regression.
3. 가장 좁은 테스트 유형을 선택한다: unit, repository slice, API contract, integration, full app.
4. clock, ID, randomness, external client를 제어해 deterministic하게 만든다.
5. 영향 모듈의 scoped validation을 먼저 실행하고, shared behavior가 바뀌었을 때만 확장한다.

## 검증

- `./gradlew :{module}:test` 또는 repo의 기존 테스트 명령을 우선한다.
- Spring/JPA 쿼리면 repository slice 또는 `@DataJpaTest` 계열을 검토한다.

## 주의사항

- 구현 세부사항보다 외부에서 관찰되는 동작을 검증한다.
- 느린 통합 테스트는 구체적 위험이 있을 때만 추가한다.

## 출력

테스트 시나리오와 필요한 경우 로컬 컨벤션에 맞춘 집중 테스트를 작성한다.
