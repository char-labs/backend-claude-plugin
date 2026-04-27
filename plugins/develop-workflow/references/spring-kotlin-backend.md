# Spring/Kotlin 백엔드 부록

대상 백엔드가 Kotlin, Spring Boot, Spring Security, JPA/Hibernate, Gradle 또는 관련 JVM infrastructure를 사용할 때 이 자료를 사용한다.

## Kotlin/Java import 스타일

- 코드 본문, 함수 내부, 테스트 본문, 타입 선언 하단 영역에 `com.example.Foo`처럼 fully qualified name을 직접 쓰지 않는다.
- 클래스, enum, object, companion object member, top-level function, 테스트 헬퍼는 언어가 허용하는 한 파일 상단 import로 올린다.
- Java static member, assertion helper, Mockito/AssertJ/JUnit static helper는 본문에서 `org.example.Type.member`로 쓰지 말고 `import static`을 사용한다.
- Kotlin에서는 Java의 `import static` 대신 일반 import로 object/companion/top-level member를 직접 import할 수 있으면 그렇게 한다.
- Fully qualified name은 언어/프레임워크가 요구하는 경우에만 남긴다. 예: package/import 선언, JPQL/HQL constructor expression 문자열, string 기반 framework 설정, reflection/generator가 canonical class name 문자열을 요구하는 경우.

## Kotlin 스타일

- Kotlin nullability를 contract로 사용한다. invariant가 locally 증명되고 더 나은 type으로 표현할 수 없는 경우가 아니라면 `!!`를 피한다.
- request command와 value object에는 immutable data를 우선한다.
- extension function은 discoverable하고 domain-relevant하게 유지한다. 중요한 dependency를 extension 안에 숨기지 않는다.
- 여러 class에 private helper나 흩어진 method pattern이 나타날 가능성이 높다면 공통 operation을 추론해 top-level extension function으로 추출한다.
- 넓게 재사용되는 extension function은 프로젝트의 기존 `common`, `support`, `util` package에 둔다. convention이 domain-local이면 global dumping ground를 만들지 말고 domain support package를 사용한다.
- extension function은 작고 stateless하며 dependency-free해야 한다. authorization, transaction, repository access, remote client call, business policy를 extension에 넣지 않는다.
- extension function은 파일 상단에서 import한다. inline fully qualified name으로 호출하지 않는다.
- readability와 maintenance가 좋아질 때 idiomatic Kotlin을 우선한다: scope function, `when`, `is` smart cast, null-safety operator, collection operation.
- scope function은 의도별로 사용한다. `apply`는 receiver 설정, `also`는 side-effect checkpoint, `let`은 nullable 또는 짧은 transformation, `run`은 receiver-scoped computation, `with`는 기존 receiver에 대한 grouped operation에 사용한다.
- 깊게 중첩된 scope function, 모호한 nested `it`, side effect를 숨기는 긴 chain을 피한다. readability가 좋아지면 named lambda parameter나 local variable을 사용한다.
- enum, sealed hierarchy, status, type branching에는 exhaustive `when` expression을 우선한다. `when`이 domain state를 더 잘 표현한다면 흩어진 `if/else` chain을 피한다.
- unsafe cast나 반복 manual casting 대신 `is` smart cast를 사용한다.
- 명확한 in-memory transformation에는 Kotlin collection operation을 우선하지만, `map`, `forEach`, nested collection chain 안에 repository call, lazy loading, N+1 behavior를 숨기지 않는다.
- 서로 다른 개념을 나타내는 class라면 `.kt` 파일 하나에 하나의 primary top-level public data class를 우선한다.
- 같은 좁은 context를 공유할 때만 한 `.kt` 파일에 여러 data class를 허용한다. 예: parent concept 안의 nested command/info/result type, API response wrapper와 강하게 결합된 response DTO.
- 여러 data class가 독립적으로 재사용될 수 있거나, 서로 다른 API action에 속하거나, 파일 scan을 어렵게 만들면 별도 파일로 분리한다.
- `NotificationStored.Create`, `NotificationStored.Info`, `NotificationStored.Result`처럼 parent context에 명확히 속한 nested DTO는 허용한다.
- `FlowerSpotAllResponse`와 `FlowerSpotResponseDto`처럼 wrapper가 해당 DTO의 list/envelope만 담기 위해 존재하는 response wrapper 파일은 허용한다.

## 도메인 데이터와 팩토리 패턴

- domain object, DTO, command, query, criteria, result의 construction에 intent, default value, mapping, invariant, naming value가 있으면 Kotlin `companion object`의 static factory method를 우선한다.
- factory name은 일관되게 사용한다. 단일 source mapping은 `from(source)`, 직접 값 조합은 `of(...)`, 새 domain/action 생성은 `create(command)`, `restore`, `empty`, `default` 같은 명시적 이름은 상태가 domain-meaningful할 때만 사용한다.
- trivial local test data나 invariant가 없는 작은 immutable value에는 direct constructor도 허용한다. 다만 public application/domain construction에서 call site intent가 좋아진다면 named factory를 우선한다.
- Service return value는 명시적인 `*Result` 타입이어야 한다. `UserCreateResult`, `PostDeleteResult`, `NotificationSendResult`처럼 action과 domain을 드러내는 이름을 우선하고, 하나의 parent concept에 강하게 묶이면 nested `Domain.Result`도 허용한다.
- write intent는 `*Command`, read intent는 `*Query`, filtering/search condition은 `*Criteria`로 표현한다. repository에 더 좁은 기존 convention이 없다면 하나의 request DTO를 command, query, persistence, API layer에 걸쳐 과도하게 재사용하지 않는다.
- `Criteria`는 optional filter, sorting, pagination, search condition을 model해야 한다. immutable하게 유지하고 repository/query-builder behavior를 넣지 않는다.
- `Command`는 use-case execution 전에 validate되어야 하며, persistence entity shape가 아니라 user intent를 담아야 한다.
- `Query`는 read-side intent와 expected lookup shape를 표현해야 한다. security/ownership check는 query DTO construction 안에 숨기지 말고 use case 또는 Service에 둔다.
- Entity, input model, command-like data class에서 domain object로 변환할 때는 관례가 다르지 않다면 `toDomain()`을 우선한다. `toDomain()`은 현재 객체의 값만 사용해 domain model을 만드는 순수 mapping이어야 한다.
- `toDomain()`에는 repository/client 호출, authorization, transaction, lazy association traversal, 외부 clock/ID generator 호출을 넣지 않는다. 그런 책임은 Service, role component, domain factory가 소유한다.
- 새 domain object의 기본값이 명확한 경우 `id = 0`, `deletedAt = null`, `thumbnailUrl = null`처럼 domain convention을 드러내는 값은 `toDomain()`에서 세팅할 수 있다. 다만 invariant 검증이나 생성 정책이 복잡하면 `Domain.create(command)` 또는 factory로 이동한다.
- `../Pida-Server`, `../Sseudam-Server` 같은 sibling example repository에 접근할 수 있으면 새 local convention을 도입하기 전에 대표 `*Command`, `*Query`, `*Criteria`, `*Result`, companion factory example을 읽는다.

```kotlin
package com.pida.flowerevent

import com.pida.support.geo.GeoJson
import com.pida.support.geo.Region
import java.time.LocalDate

data class NewFlowerEvent(
    val name: String,
    val address: String?,
    val longitude: Double,
    val latitude: Double,
    val region: Region,
    val homepageUrl: String?,
    val startDate: LocalDate,
    val endDate: LocalDate,
    val categoryId: Long,
) {
    fun toDomain(): FlowerEvent =
        FlowerEvent(
            id = 0,
            name = name,
            address = address,
            thumbnailUrl = null,
            pinPoint = GeoJson.Point(listOf(longitude, latitude)),
            region = region,
            homepageUrl = homepageUrl,
            startDate = startDate,
            endDate = endDate,
            categoryId = categoryId,
            deletedAt = null,
        )
}
```

## Spring 계층화

- Controller는 얇게 유지한다: request validation, auth context extraction, use-case call, response mapping.
- Service/use case는 transaction과 orchestration을 소유한다.
- Repository는 persistence access만 소유한다. repository code에 authorization이나 workflow state machine을 넣지 않는다.
- Configuration class에는 business logic을 넣지 않는다.
- non-trivial business action을 큰 service 내부의 private method에 묻지 않는다. `UserCreator`, `PostDeleter`, `NotificationSender`, `FlowerSpotReader`처럼 role-oriented name을 가진 응집도 높은 component로 추출한다.
- `private`는 local detail에만 사용한다. 작은 pure helper, invariant-preserving transformation, named collaborator로 의미가 없는 code가 대상이다.
- 여러 Service, domain, transaction, side effect를 조율하는 복잡한 business flow에는 Facade를 사용한다.
- validation, policy, state transition, repository access, port/adaptor coordination 같은 single-domain responsibility에는 Service를 사용한다.
- Facade constructor는 Service에만 의존해야 한다. `Repository`, `EntityManager`, external client, mapper, port, role component를 Facade에 직접 주입하지 말고 해당 작업을 Service를 통해 노출한다.

## Coroutine과 동시성

- independent IO parallelism, cancellation/timeout propagation, suspend/non-blocking stack 연동을 명확히 개선할 때 coroutine을 우선한다.
- 대부분 Spring MVC + JPA/JDBC blocking IO인 단일 서버 monolith에서는 coroutine이 불필요할 수 있다. 독립 external IO를 안전하게 병렬 실행할 수 있을 때 선택적으로 사용한다.
- 모든 child task가 함께 성공해야 하면 `coroutineScope`를 사용한다. child failure를 격리하고 독립적으로 처리해야 하면 `supervisorScope`를 사용한다.
- 독립 작업에는 bounded `async/await`를 사용한다. user input, database row, 큰 collection에 대한 unbounded fan-out을 피한다.
- JPA/JDBC, blocking HTTP client, file IO, sync Redis/Kafka client, legacy SDK call 같은 blocking IO에는 `withContext(Dispatchers.IO)`를 사용한다.
- blocking section을 식별하지 않은 채 controller나 service 전체를 `Dispatchers.IO`로 감싸지 않는다. 가장 작은 blocking block만 격리한다.
- CPU-bound 작업에는 `Dispatchers.Default`를 사용한다. CPU-heavy loop를 `Dispatchers.IO`에 넣지 않는다.
- WebClient suspend API나 R2DBC 같은 true suspend/non-blocking client 주변에서 불필요한 dispatcher switch를 피한다.
- `GlobalScope`, request-path의 `runBlocking`, `Thread.sleep`, `.block()`, transaction-internal remote call, coroutine fan-out 내부 lazy loading을 피한다.
- coroutine boundary를 넘는 transaction, SecurityContext, MDC/logging context, request cancellation behavior를 확인한다.
- thread/memory tradeoff를 항상 검토한다: coroutine count, heap allocation, scheduler overhead, DB connection pool, external rate limit, timeout, retry amplification.

## Spring Security

- protected endpoint에는 명시적 authorization이 필요하다. route naming이나 UI-only control에 의존하지 않는다.
- 여러 adapter에서 도달할 수 있는 use case는 method-level security를 확인한다.
- tenant/account ownership은 controller뿐 아니라 use case에서 검증한다.
- broad `permitAll`, credential과 함께 쓰는 wildcard CORS, cookie flow에서 disabled CSRF, object-level authorization을 건너뛰는 role check를 피한다.

## JPA와 Hibernate

- DTO mapper, JSON serialization, logging, loop에서 트리거되는 lazy loading을 검토한다.
- fetch join, entity graph, projection, batch size를 의도적으로 사용한다. 기본값으로 전체 graph를 fetch하지 않는다.
- 트랜잭션 경계 문제를 숨기기 위한 `open-in-view` 의존을 피한다.
- read에는 `@Transactional(readOnly = true)`를 검토하고, state change에는 write transaction을 사용한다.
- remote call이나 event publishing을 감싸는 긴 transaction을 피한다.
- native query와 JPQL은 parameter를 bind해야 한다. dynamic identifier에는 allowlist가 필요하다.
- bulk update에서는 persistence context staleness와 domain event consistency를 고려한다.

## Gradle과 검증

- `./gradlew test`, `./gradlew ktlintCheck`, `./gradlew detekt`, project-specific task가 있으면 repo wrapper를 우선한다.
- plugin이나 dependency를 자동으로 추가하지 않는다. 추가가 필요하면 근거와 함께 추천한다.
- module path가 있으면 먼저 affected module로 validation scope를 좁히고, shared contract가 바뀐 경우에만 넓힌다.

## Spring/Kotlin 테스트 가드레일

- 테스트 코드는 실 DB, 공유 개발 DB, 운영 DB에 직접 연결하지 않는다.
- 테스트 코드에는 `@Transactional`을 붙여 rollback에 의존하지 않는다. 데이터 격리는 명시적 setup/cleanup, fake/mock, 또는 repo convention의 disposable test DB로 처리한다.
- Presentation/Controller 테스트는 선택 항목이다. 작성 전 사용자에게 확인하고, 기본은 Service/UseCase/Domain 테스트를 우선한다.

## 흔한 Spring/Kotlin Finding

- `map`, `forEach`, resolver method, lazy collection access 내부의 repository call로 발생하는 N+1.
- ID로 loading한 뒤 object-level authorization이 누락된 구조.
- multi-step write use case 주변에 `@Transactional`이 누락된 구조.
- internal message를 반환하는 catch-all exception handler.
- request body, token, authorization header, PII가 포함된 entity snapshot을 logging하는 구조.
- 본문/하단 영역의 inline fully qualified name. Java static member는 `import static`, Kotlin member/top-level reference는 파일 상단 import를 써야 한다.
- 비즈니스 책임을 private method chain에 숨기는 큰 service. 역할 이름을 가진 컴포넌트로 분리해야 한다.
- 서로 다른 컨텍스트의 여러 public data class를 한 `.kt` 파일에 모아 scan과 변경 영향 범위를 흐리는 구조.
- Facade가 Service가 아닌 Repository, EntityManager, client, mapper, port, 역할 컴포넌트를 직접 의존하는 구조.
- 단일 도메인 책임을 Facade로 올려 layer 의미를 흐리는 구조. 단일 도메인은 Service에 둔다.
- 여러 class에 반복되는 private helper, 변환/포맷팅/collection 처리, null-safety helper를 흩어 놓는 구조. 순수 재사용 패턴이면 `common`, `support`, `util` 또는 도메인 support 패키지의 확장 함수로 올린다.
- Java식 null/branch/type 처리로 Kotlin의 scope function, `when`, `is` smart cast, collection operation을 쓰면 더 읽기 쉬운 구조.
- 중첩 scope function이나 긴 chain으로 receiver와 `it` 의미가 불명확하거나 side effect가 숨겨지는 구조.
- enum/sealed/status 분기를 흩어진 `if/else`로 처리해 상태 추가 시 누락 위험이 커지는 구조. 가능한 exhaustive `when`을 쓴다.
- 생성 의도, invariant, mapping이 있는 객체를 public constructor 직접 호출로 흩어 놓는 구조. companion object의 `from`, `of`, `create` 같은 정적 팩토리로 intent를 드러낸다.
- Entity/input model/domain command에서 domain model로 가는 변환이 흩어진 mapper나 Service 내부 constructor 호출로 반복되는 구조. 순수 변환이면 `toDomain()`으로 모으고, 생성 정책이 복잡하면 domain factory로 올린다.
- Service 결과가 primitive, tuple, API response DTO, entity 그대로 반환되어 application boundary가 흐려지는 구조. 명시적 `*Result` 타입을 우선한다.
- write/read/filter intent를 하나의 DTO로 섞는 구조. `*Command`, `*Query`, `*Criteria`로 목적을 나눈다.
- coroutine 도입 이유 없이 blocking MVC/JPA 흐름을 suspend로 감싼 구조.
- `Dispatchers.IO`를 성능 보장 장치처럼 사용하거나, DB pool/external limit보다 큰 unbounded fan-out을 만드는 구조.
- request path의 `runBlocking`, `GlobalScope`, `.block()`, coroutine 내부 lazy loading, transaction 내부 remote call.
