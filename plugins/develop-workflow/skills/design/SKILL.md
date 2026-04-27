---
name: design
description: 서비스/도메인/트랜잭션/인가/영속성 경계를 포함한 백엔드 아키텍처를 설계할 때 사용. API wire schema는 api-contract-design, 단계적 이관은 migration-adr를 우선 사용.
argument-hint: "[기능 또는 설계 요청]"
---

# 백엔드 설계 워크플로우

## 설명

사용자 요청을 백엔드 아키텍처 제안으로 설계한다. 서비스 경계, 도메인 모델, 트랜잭션, 인가 소유권, 영속성 경계, 성능, 테스트 전략을 결정한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- 객체지향 디자인 패턴이 필요하면 `${CLAUDE_PLUGIN_ROOT}/references/oop-design-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- API contract가 포함되면 `${CLAUDE_PLUGIN_ROOT}/references/api-protocols.md`
- Spring/Kotlin/JPA/Gradle/JVM이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- Spring/Kotlin coroutine/concurrency이면 `spring-coroutine-concurrency` skill 기준을 함께 적용한다.
- `${CLAUDE_PLUGIN_ROOT}/templates/design-decision-template.md`

## 실행 절차

1. 구조를 제안하기 전 기존 코드베이스를 확인한다.
2. 목표, 성공 기준, 제약, 영향 boundary를 명시한다.
3. validation, authorization, transaction control, persistence, external call, error handling의 소유 계층을 정한다.
4. unbounded read, N+1, missing index, long transaction 같은 query/application performance risk를 포함한다.
5. authn/authz, input validation, secret, logging, SSRF/file handling, rate limit 보안 통제를 포함한다.
6. 비즈니스 책임이 있는 흐름은 private method로 숨기지 않고 `UserCreator`, `PostDeleter`처럼 역할 이름을 가진 컴포넌트로 설계한다. `private`는 정말 class 내부의 작은 세부 구현에만 쓴다.
7. 복잡한 비즈니스 흐름은 Facade로 조합하고, 단일 도메인 책임은 Service에 둔다. Facade는 Service만 의존하도록 경계를 설계한다.
8. 여러 class에서 반복될 Kotlin helper 패턴은 private method로 흩어 두지 않고 `common`, `support`, `util` 또는 도메인 support 패키지의 확장 함수 후보로 설계한다.
9. Kotlin이면 scope function, `when`, `is` smart cast, null-safety, collection operation을 활용해 분기와 변환을 읽기 쉽게 설계한다.
10. 생성 의도나 invariant가 있는 객체는 companion object 정적 팩토리(`from`, `of`, `create`)를 우선 설계한다.
11. Entity/input model/command-like data class에서 domain model로 가는 순수 변환은 `toDomain()`으로 설계한다. 생성 정책이 복잡하면 domain factory로 분리한다.
12. Service/use-case 출력은 명시적 `*Result`로 설계하고, write/read/filter 입력은 `*Command`, `*Query`, `*Criteria`로 목적을 분리한다.
13. 반복 분기, 정책 선택, 안정된 워크플로우, 상태별 행위, 외부 provider 경계가 있으면 Strategy, Template Method, State, Specification/Policy, Adapter/Port, Decorator, Chain/Pipeline, Factory 중 필요한 패턴을 검토한다.
14. coroutine을 쓰면 도입 이유, blocking 요소, dispatcher 선택, structured concurrency, bounded fan-out, thread/memory tradeoff를 명시한다.
15. Spring/Kotlin/Java이면 `@Transactional`, Spring Security, DTO/domain/entity 분리, JPA fetch strategy, Gradle validation, 파일 상단 import, Java `import static`, data class 파일 분리/중첩 허용 기준을 명시한다.
16. 기존 도구에 맞는 test와 validation command로 마무리한다.

## 검증

- 설계 결과가 구현자가 추가 결정을 하지 않아도 될 만큼 decision-complete인지 확인한다.
- 필요한 경우 ADR 작성 여부를 판단한다.

## 주의사항

- 실수 방지 가드레일: 설계 결정에는 검증 방법, 회귀 위험, 필요한 fixture 또는 테스트 위치를 함께 포함한다.
- 보안, 쿼리 성능, 트랜잭션 경계를 “구현 시 고려”로 미루지 말고 설계 결정에 포함한다.
- 특정 framework나 layer를 도입하기 전 기존 프로젝트 관례를 우선한다.
- 여러 data class를 한 `.kt` 파일에 둘 때는 같은 컨텍스트의 nested command/info/result 또는 응답 wrapper + DTO처럼 응집된 경우에만 허용한다.
- Facade는 여러 Service를 엮는 조합 계층으로만 둔다. Repository, EntityManager, 외부 client, mapper, port를 Facade에 직접 주입하지 않는다.
- 확장 함수에는 외부 의존성, repository/client 호출, 인가, 트랜잭션, 비즈니스 정책을 숨기지 않는다.
- scope function은 의도를 드러낼 때 사용한다. 중첩 `it`이나 긴 chain으로 receiver와 side effect가 흐려지면 지역 변수나 명시적 lambda name을 쓴다.
- 정적 팩토리는 생성 의미가 있는 곳에 적극 사용한다. 단순 테스트 fixture나 의미 없는 값 보관용 constructor까지 억지로 감싸지는 않는다.
- `toDomain()`은 순수 mapping으로 설계한다. repository/client 호출, 인가, 트랜잭션, lazy loading이 필요한 변환이면 Service나 factory 책임으로 올린다.
- `Criteria`는 검색/필터 조건, `Command`는 쓰기 의도, `Query`는 읽기 의도, `Result`는 Service 결과를 표현하게 한다.
- 디자인 패턴은 문제를 먼저 찾고 나중에 선택한다. 단일 구현에 interface/abstract class만 추가하는 패턴 과잉 설계는 피한다.
- Template Method는 생명주기 골격이 안정적일 때만 쓰고, 단순 변형은 Strategy나 역할 컴포넌트 조합을 우선한다.
- 단일 서버 모놀리식 + blocking JPA 중심이면 coroutine이 필요 없을 수 있다. 독립 IO 병렬화가 명확할 때만 적극 적용한다.
- 요구사항이 불명확하면 `clarify-requirements`로 범위와 성공 기준을 먼저 좁힌다.

## 출력

설계 결정 템플릿을 사용해 결정 완료형 설계를 반환한다.
