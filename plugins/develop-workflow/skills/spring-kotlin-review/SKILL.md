---
name: spring-kotlin-review
description: Spring Security, JPA Entity infrastructure/db-core 위치, BaseEntity, 순수 domain data class, toDomain mapping, Repository 포트/CoreRepository 구현체/JpaRepository 분리, JPA/Hibernate 쿼리 동작, scalar FK 기반 Entity, 관계 어노테이션 지양, 트랜잭션 경계, Gradle 검증, Kotlin nullability, DTO/domain/entity 분리, import 스타일을 Spring/Kotlin 관점으로 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 엔드포인트, 모듈, 리뷰 범위]"
---

# Spring/Kotlin 백엔드 리뷰

## 설명

사용자 요청을 Spring/Kotlin 특화 관점으로 검토한다. 일반 리뷰보다 Spring Security, JPA/Hibernate, transaction, Gradle/Kotlin convention을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- 객체지향 디자인 패턴이 핵심이면 `${CLAUDE_PLUGIN_ROOT}/references/oop-design-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- Spring/Kotlin coroutine/concurrency이면 `spring-coroutine-concurrency` skill 기준을 함께 적용한다.

## 실행 절차

1. Spring Security를 확인한다: route protection, method security, ownership check, CSRF/CORS behavior, overly broad `permitAll`.
2. Repository 경계를 확인한다: `*Repository` 도메인 포트, `*CoreRepository : *Repository` infrastructure 구현체, `*JpaRepository`/`*CustomRepository` 내부 위임, Service/use-case의 포트 의존.
3. domain/JPA Entity 경계를 확인한다: JPA Entity는 infrastructure/db-core에 있고 domain에는 순수 data class가 있으며, `toDomain()`으로만 domain 객체로 변환되는지 본다.
4. BaseEntity를 확인한다: `@MappedSuperclass`, `AuditingEntityListener`, `GenerationType.IDENTITY`, `createdAt`/`updatedAt`/`deletedAt`, `softDelete`, id 기반 `equals/hashCode`가 안전한지 본다.
5. JPA/Hibernate를 확인한다: 신규 Entity의 scalar FK 우선 여부, `@ManyToOne`/`@OneToMany`/`@ManyToMany`/`JoinColumn` 관계 어노테이션 남용, N+1, mapper/serializer/logging lazy loading, fetch join/entity graph/projection, bulk update, `open-in-view` reliance.
6. transaction을 확인한다: use-case ownership, `readOnly`, write boundary, transaction 내부 remote call, event consistency.
7. Kotlin/Java import를 확인한다: nullability contract, 불필요한 `!!`, immutable command/value object, 코드 본문/하단 영역의 inline fully qualified reference 금지, Java static member의 `import static` 사용.
8. Kotlin 파일 구성을 확인한다: 여러 data class는 기본 지양하되 같은 부모 컨텍스트의 nested type 또는 응답 wrapper + DTO는 허용한다.
9. service 내부 private method가 비즈니스 책임을 숨기는지 확인하고, 필요한 경우 역할 컴포넌트 추출을 제안한다.
10. Facade/Service 패턴을 확인한다: 복잡한 비즈니스 조합은 Facade, 단일 도메인 책임은 Service를 사용하고 Facade는 Service만 의존한다.
11. Kotlin 확장 함수 패턴을 확인한다: 여러 class에서 반복될 순수 helper는 `common`, `support`, `util` 또는 도메인 support 패키지의 top-level extension으로 둔다.
12. Kotlin idiom을 확인한다: scope function은 의도별로 쓰고, enum/sealed/status/type 분기는 exhaustive `when`과 `is` smart cast를 우선 고려한다.
13. 정적 팩토리와 message type을 확인한다: 의미 있는 생성은 `from`/`of`/`create`, Service 결과는 `*Result`, 입력 목적은 `*Command`/`*Query`/`*Criteria`로 드러낸다.
14. `toDomain()` 변환을 확인한다: Entity/input model/command-like data class의 순수 domain mapping은 현재 값과 scalar FK 기반 `toDomain()`으로 모으고, repository/client 호출, 인가, 트랜잭션, lazy association traversal, 관계 어노테이션 탐색은 넣지 않는다.
15. 반복 분기와 생명주기 행위를 확인한다: Strategy, Template Method, State, Specification/Policy, Adapter/Port가 Spring 계층 경계를 선명하게 하는지 본다.
16. coroutine/concurrency를 확인한다: `coroutineScope`, `supervisorScope`, `Dispatchers.IO`, blocking 요소, bounded fan-out, cancellation/timeout.
17. Gradle validation을 확인한다: existing `./gradlew` task, scoped module test, ktlint/detekt 존재 여부, 자동 dependency 설치 금지.

## 검증

- 영향 module의 compile/test를 우선 제안한다.
- Spring/JPA 변경이면 repository slice 또는 integration test를 검토한다.
- Kotlin style은 ktlint/detekt가 있으면 해당 명령을 사용한다.

## 주의사항

- 실수 방지 가드레일: Spring/Kotlin finding은 관련 Gradle 검증, slice/integration test, import/style check를 함께 연결한다.
- Spring annotation만 보고 보안/트랜잭션이 충분하다고 가정하지 않는다.
- Entity를 API response로 직접 노출하거나 lazy association을 serialization에 맡기지 않는다.
- JPA Entity는 infrastructure/db-core 소유다. domain package에는 JPA annotation이 없는 순수 data class를 두고, Entity는 `toDomain()`으로 domain 객체로 변환한다.
- BaseEntity는 domain package가 아니라 persistence support package에 둔다. 같은 class와 같은 id에서 `equals`가 true인지, `hashCode`가 mutable field를 쓰지 않는지, `softDelete` 조회 필터가 있는지 확인한다.
- `*Repository`는 추상화된 포트, `*CoreRepository`는 그 구현체, `*JpaRepository`는 내부 위임 대상으로 둔다. Service/use-case/Facade가 구체 구현이나 Spring Data repository를 직접 의존하면 finding 후보로 본다.
- 신규 Entity의 관계 어노테이션은 finding 후보로 본다. 기본 fix는 `userId`, `postId` 같은 scalar FK와 Repository 명시 조인/projection이다.
- `@ManyToMany`는 신규 코드에서 허용하지 않는다. 연결 엔티티로 풀고 unique/index, audit, 권한, 삭제 정책을 명시한다.
- import style은 엄격히 적용한다. 코드 본문/하단 영역에 `com.example.Foo`처럼 직접 쓰지 말고 파일 상단 import로 올리며, Java static member는 `import static`을 사용한다.
- data class를 여러 개 넣는 파일은 같은 API/도메인 컨텍스트인지 확인한다. 독립적으로 재사용될 수 있으면 분리한다.
- Facade는 Service만 constructor dependency로 받는다. Repository, EntityManager, client, mapper, port가 필요하면 Service 뒤로 이동시킨다.
- 확장 함수에는 repository/client 호출, transaction, authorization, business policy를 넣지 않는다. 그런 로직은 Service나 역할 컴포넌트가 소유한다.
- scope function은 가독성을 높일 때 적극 사용한다. 다만 중첩 `it`, 모호한 receiver, side effect가 숨겨지는 긴 chain은 피한다.
- companion object 정적 팩토리와 `*Result`/`*Command`/`*Query`/`*Criteria`는 Spring/Kotlin application boundary를 선명하게 하는 기본 선호 규칙으로 본다.
- `toDomain()`은 infrastructure/db-core Entity에서 domain의 순수 data class로 넘어가는 현재 객체 값만 사용하는 순수 변환으로 유지한다. 생성 정책이나 invariant가 복잡하면 `Domain.create(...)` 또는 별도 factory로 이동한다.
- 디자인 패턴은 Spring component graph와 transaction boundary를 흐리지 않아야 한다. Pattern 구현이 Repository/client/transaction을 숨기면 Service나 Adapter로 이동시킨다.
- coroutine은 blocking 여부, dispatcher 선택, transaction/security/MDC context, thread/memory tradeoff를 함께 검토한다.

## 출력

review finding template을 사용한다. 각 finding에는 정확한 Spring/Kotlin mechanism을 포함해 fix가 바로 실행 가능하도록 한다.
