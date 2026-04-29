---
name: implement
description: OOP/SOLID 경계, 보안 기본값, Repository 포트/CoreRepository 어댑터, 성능을 고려한 데이터 접근, scalar FK 기반 Entity, 집중 테스트를 포함해 백엔드 코드를 구현/수정할 때 사용. 쿼리 변경은 persistence-query-review, 테스트 전용은 backend-test-strategy를 우선 사용.
argument-hint: "[구현 작업]"
---

# 백엔드 구현 워크플로우

## 설명

사용자 요청을 기존 코드베이스에 맞는 가장 작은 응집도 높은 변경으로 구현한다. 더 좁은 전문 skill이 맞으면 그 skill을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- 객체지향 디자인 패턴이 필요하면 `${CLAUDE_PLUGIN_ROOT}/references/oop-design-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- Spring/Kotlin/JPA/Gradle이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- Spring/Kotlin coroutine/concurrency이면 `spring-coroutine-concurrency` skill 기준을 함께 적용한다.

## 실행 절차

1. module layout, service/use-case style, tests, validator, auth helper, transaction convention, repository pattern을 먼저 읽는다.
2. 프로젝트 관례가 다르지 않다면 domain rule을 controller와 infrastructure adapter 밖으로 유지한다.
3. authentication, authorization, input validation, sensitive logging, secret handling, error response를 명시적으로 처리한다.
4. query shape, pagination/limit, index, timeout, retry, transaction scope, cache correctness를 확인한다.
5. OOP/SOLID를 지킨다: 작은 cohesive class, 명시적 collaborator, 외부 시스템 abstraction, testable behavior.
6. 비즈니스 책임을 private method chain에 숨기지 않는다. 회원 생성은 `UserCreator`, 글 삭제는 `PostDeleter`처럼 역할과 책임이 드러나는 컴포넌트로 분리한다.
7. 복잡한 비즈니스 orchestration은 Facade로 구현하고, 단일 도메인 책임은 Service로 구현한다. Facade는 Service만 의존하며 repository/client/mapper/port를 직접 받지 않는다.
8. 여러 class에서 반복될 변환, 포맷팅, collection, null-safety helper는 private method나 흩어진 메서드로 두지 않고 top-level 확장 함수로 추출한다.
9. Kotlin에서는 scope function, `when`, `is` smart cast, null-safety, collection operation을 우선 고려해 가독성과 재사용성을 높인다.
10. 생성 의도, mapping, 기본값, invariant가 있으면 constructor 직접 호출보다 companion object 정적 팩토리(`from`, `of`, `create`)를 우선 사용한다.
11. 신규 JPA Entity는 관계 어노테이션보다 scalar FK를 우선 구현한다. 예: `PostEntity(val userId: Long, ...)`, `CommentEntity(val postId: Long, val userId: Long, ...)`.
12. `@ManyToOne`, `@OneToMany`, `@ManyToMany`, `JoinColumn`은 legacy 호환이나 명시 승인 예외가 아니면 추가하지 않는다. 필요한 조합은 Repository/QueryDSL/JPQL/SQL 명시 조인과 projection으로 구현한다.
13. Entity/input model/command-like data class에서 domain model로 가는 순수 변환은 `toDomain()`으로 모은다. repository/client 호출, 인가, 트랜잭션, lazy association traversal, 관계 어노테이션 탐색이 필요하면 Service나 factory로 이동한다.
14. Repository 구현은 Pida-Server식 포트/어댑터 구조를 우선한다. 도메인/application에는 `*Repository` 인터페이스를 두고, infrastructure에는 `class *CoreRepository(...) : *Repository` 구현체를 두며, `*JpaRepository`/`*CustomRepository`는 구현 내부로 숨긴다.
15. Service/use-case 결과는 `*Result`로 반환하고, 입력 목적은 `*Command`, `*Query`, `*Criteria`로 분리한다.
16. 반복 조건문, provider 분기, 상태별 행위, 워크플로우 골격이 보이면 Strategy, Template Method, State, Specification/Policy, Adapter/Port, Decorator, Chain/Pipeline, Factory 중 가장 단순한 패턴을 적용한다.
17. coroutine을 쓰면 blocking 구간은 `withContext(Dispatchers.IO)`로 좁게 격리하고, `coroutineScope`/`supervisorScope`/bounded `async`를 목적에 맞게 사용한다.
18. Kotlin/Java에서는 코드 본문이나 하단 영역에 `com.example.Foo` 같은 fully qualified reference를 직접 쓰지 않는다. 클래스/enum/object/top-level function은 파일 상단 import로 올리고, Java static member는 `import static`을 사용한다.
19. kt 파일의 여러 data class는 기본 지양한다. 같은 부모 컨텍스트의 nested command/info/result 또는 응답 wrapper + DTO처럼 강하게 결합된 경우에만 허용한다.
20. changed behavior와 주요 failure/security edge case에 집중 테스트를 추가/수정한다.
21. 가장 좁은 validation을 먼저 실행하고, shared contract나 infrastructure가 바뀐 경우에만 확장한다.

## 검증

- 영향 모듈 compile/test를 우선한다.
- 실행 불가 시 이유와 residual risk를 남긴다.

## 주의사항

- 실수 방지 가드레일: 변경 동작을 증명하는 테스트와 영향을 받은 routing/hook/fixture/policy 검증을 함께 확인한다.
- 비즈니스 로직, 분기, 인가, 쿼리, 오류 처리, 회귀 위험이 없으면 새 테스트를 억지로 만들지 않는다.
- 관련 없는 리팩터와 metadata churn을 피한다.
- 보안 검증이나 authorization boundary를 테스트 없이 신뢰하지 않는다.
- 쿼리 변경은 result cardinality, pagination, N+1, index 영향을 함께 확인한다.
- Service/use-case/Facade에 `*JpaRepository`, `*CoreRepository`, `EntityManager`, QueryDSL factory를 직접 주입하지 않는다. `*Repository` 포트 뒤에 둔다.
- `*Repository` 인터페이스는 Spring Data `JpaRepository`를 상속하지 않는다. Spring Data interface는 `*JpaRepository`로 infrastructure 내부에 두고 `*CoreRepository`가 위임한다.
- 신규 Entity에 `@ManyToOne`, `@OneToMany`, `@ManyToMany`를 추가하지 않는다. scalar FK + 명시 조인/projection이 기본값이다.
- 다대다 관계는 `@ManyToMany` 대신 연결 엔티티를 구현한다. 연결 엔티티에는 양쪽 FK, unique/index, audit/delete policy를 드러낸다.
- `private`는 외부 협력자가 될 수 없는 작은 로컬 세부 구현에만 사용한다. 역할 이름이 붙는 행동이면 컴포넌트로 추출한다.
- Facade에 Service가 아닌 의존성이 필요해지면 해당 책임을 Service로 내리고 Facade는 조합만 담당하게 한다.
- 확장 함수는 순수하고 의존성 없는 공통 동작에만 사용한다. 비즈니스 정책이나 외부 협력 조합이면 Service/컴포넌트로 둔다.
- scope function은 `apply`/`also`/`let`/`run`/`with`의 의도에 맞게 선택한다. 중첩 scope와 모호한 `it`은 피한다.
- enum/sealed/status/type 분기는 가능한 exhaustive `when`과 `is` smart cast로 표현한다.
- 정적 팩토리는 생성 의도를 드러내는 장치로 사용한다. 단순 값 전달만 하는 모든 data class constructor를 기계적으로 감싸지 않는다.
- `toDomain()`은 순수 mapping에만 사용한다. 새 domain 기본값(`id = 0`, `deletedAt = null`)은 명확하면 허용하지만, 생성 정책이나 invariant가 복잡하면 domain factory를 우선한다.
- Service에서 entity, response DTO, primitive bundle, `Pair`/`Triple`을 그대로 반환하지 말고 application contract인 `*Result`를 우선 작성한다.
- API request DTO를 그대로 Command/Query/Criteria로 재사용하기 전에 layer ownership과 validation 위치가 흐려지는지 확인한다.
- Strategy와 Template Method를 우선 후보로 보되, inheritance보다 composition이 단순하면 composition을 선택한다.
- Pattern은 테스트 가능한 variation point를 만들 때만 추가한다. 단일 구현에 이름만 붙이는 wrapper는 피한다.
- coroutine에서는 `GlobalScope`, request path의 `runBlocking`, unbounded `async`, transaction 내부 remote call, `.block()`을 피한다.

## 출력

변경된 동작, 수행한 검증, 남은 보안/성능/아키텍처 리스크를 요약한다. 보안이 “보장”된다고 말하지 않는다.
