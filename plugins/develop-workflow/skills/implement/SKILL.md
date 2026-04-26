---
name: implement
description: OOP/SOLID 경계, 보안 기본값, 성능을 고려한 데이터 접근, 집중 테스트를 포함해 백엔드 코드를 구현/수정할 때 사용. 쿼리 변경은 persistence-query-review, 테스트 전용은 backend-test-strategy를 우선 사용.
argument-hint: "[구현 작업]"
---

# Backend Implementation Workflow

## 설명

사용자 요청을 기존 코드베이스에 맞는 가장 작은 응집도 높은 변경으로 구현한다. 더 좁은 전문 skill이 맞으면 그 skill을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- Spring/Kotlin/JPA/Gradle이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. module layout, service/use-case style, tests, validator, auth helper, transaction convention, repository pattern을 먼저 읽는다.
2. 프로젝트 관례가 다르지 않다면 domain rule을 controller와 infrastructure adapter 밖으로 유지한다.
3. authentication, authorization, input validation, sensitive logging, secret handling, error response를 명시적으로 처리한다.
4. query shape, pagination/limit, index, timeout, retry, transaction scope, cache correctness를 확인한다.
5. OOP/SOLID를 지킨다: 작은 cohesive class, 명시적 collaborator, 외부 시스템 abstraction, testable behavior.
6. Kotlin/Java에서는 코드 본문이나 하단 영역에 `com.example.Foo` 같은 fully qualified reference를 직접 쓰지 않는다. 클래스/enum/object/top-level function은 파일 상단 import로 올리고, Java static member는 `import static`을 사용한다.
7. changed behavior와 주요 failure/security edge case에 집중 테스트를 추가/수정한다.
8. 가장 좁은 validation을 먼저 실행하고, shared contract나 infrastructure가 바뀐 경우에만 확장한다.

## 검증

- 영향 모듈 compile/test를 우선한다.
- 실행 불가 시 이유와 residual risk를 남긴다.

## 주의사항

- 실수 방지 가드레일: 변경 동작을 증명하는 테스트와 영향을 받은 routing/hook/fixture/policy 검증을 함께 확인한다.
- 비즈니스 로직, 분기, 인가, 쿼리, 오류 처리, 회귀 위험이 없으면 새 테스트를 억지로 만들지 않는다.
- 관련 없는 리팩터와 metadata churn을 피한다.
- 보안 검증이나 authorization boundary를 테스트 없이 신뢰하지 않는다.
- 쿼리 변경은 result cardinality, pagination, N+1, index 영향을 함께 확인한다.

## 출력

변경된 동작, 수행한 검증, 남은 보안/성능/아키텍처 리스크를 요약한다. 보안이 “보장”된다고 말하지 않는다.
