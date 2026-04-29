# 백엔드 아키텍처 원칙

유지보수성, 테스트 가능성, 명확한 소유권을 기준으로 백엔드 코드를 설계, 구현, 리뷰할 때 이 자료를 사용한다.

## 핵심 규칙

- 의존성 방향을 안정적으로 유지한다. delivery adapter는 application use case에 의존하고, application은 domain port에 의존하며, infrastructure는 port를 구현한다.
- 저장소 경계도 같은 방향을 따른다. `*Repository`는 도메인/application 포트 인터페이스이고, `*CoreRepository`는 infrastructure adapter로 `*Repository`를 구현하며, `*JpaRepository`/`*CustomRepository`는 `*CoreRepository` 내부 구현 세부사항으로 숨긴다.
- JPA Entity는 domain model이 아니라 infrastructure/db-core/persistence adapter 소유 모델이다. domain에는 JPA annotation이나 persistence lifecycle이 없는 순수 data class 객체를 두고, Entity는 `toDomain()`으로 domain 객체로 변환해 사용한다.
- 도메인 동작은 도메인 모델 가까이에 둔다. repository와 DTO 사이에서 데이터만 옮기는 service를 피한다.
- codebase에 더 좁고 명확한 기존 패턴이 없다면 external DTO, persistence entity, command, query, domain model을 분리한다.
- 트랜잭션 소유권은 application/use-case 경계에 둔다. low-level helper에서 transaction을 시작하거나 긴 database transaction 안에 remote call을 섞지 않는다.
- 외부 시스템, clock, ID generator, persistence boundary는 테스트하거나 교체해야 하는 동작이면 명시적 interface를 우선한다.
- 오류 경계를 의도적으로 유지한다. 도메인 오류가 framework exception, SQL exception, HTTP client detail, stack trace로 호출자에게 새지 않게 한다.
- 작고 응집도 높은 class를 선호한다. validation, authorization, orchestration, mapping, persistence, event 전송, response formatting을 모두 하는 class는 너무 많은 책임을 가진다.
- 의미 있는 책임을 private helper method에 숨기지 않는다. `private`는 class 내부에 진짜로 국소적인 작은 invariant-preserving detail에만 사용한다.
- 동작에 비즈니스 역할이 있거나 독립적으로 변할 수 있으면 이름 있는 책임 컴포넌트로 추출한다. 넓은 service method나 숨겨진 private workflow보다 `UserCreator`, `PostDeleter`, `OrderCanceller`, `CouponIssuer` 같은 역할 이름을 우선한다.
- Facade는 여러 domain service나 cross-cutting side effect를 조율하는 복잡한 비즈니스 workflow에만 사용한다. 단일 도메인 책임은 Service에 둔다.
- 여러 class에서 같은 low-level transformation, formatting, collection, null-safety helper가 쓰일 가능성이 높다면 흩어진 private helper보다 프로젝트의 `common`, `support`, `util` package에 찾기 쉬운 top-level extension function을 둔다.
- 의미 있는 객체 생성에는 이름 있는 static factory를 우선한다. constructor call을 흩뿌리는 대신 `from`, `of`, `create`, domain-specific factory name으로 mapping, default, invariant를 드러낸다.
- application message type을 명시한다. write intent는 `*Command`, read intent는 `*Query`, filtering/search condition은 `*Criteria`, Service/use-case output은 `*Result`를 사용한다.
- 실제 변경 축, 안정된 워크플로우, 생명주기 상태, 외부 경계를 명확하게 만들 때 객체지향 디자인 패턴을 사용한다. 결합도를 줄이거나 테스트 용이성을 높일 때만 Strategy, Template Method, State, Specification/Policy, Adapter/Port, Decorator, Chain/Pipeline, Factory, Command Handler를 우선한다.

## SOLID 리뷰

- Single Responsibility: 각 class는 변경될 이유가 하나여야 한다.
- Open/Closed: 새 동작은 관련 없는 layer에 흩어진 conditional이 아니라 응집도 높은 extension point로 추가한다.
- Liskov Substitution: subclass와 implementation은 contract, nullability, error behavior, side effect를 보존해야 한다.
- Interface Segregation: client가 사용하지 않는 method에 의존하도록 강제하지 않는다.
- Dependency Inversion: high-level policy는 concrete infrastructure가 아니라 abstraction에 의존해야 한다.

## 계층 점검

- Controller는 transport shape 검증, boundary의 authentication/authorization, 하나의 use case 호출, result mapping만 담당해야 한다.
- Use case는 도메인 동작, transaction, repository, side effect를 조율해야 한다.
- Domain object는 framework annotation, JPA lifecycle, persistence schema shape를 피한 순수 data class/domain model이어야 한다. `@Entity`, `@Table`, `@Column`, `@Id`가 붙은 JPA Entity는 domain package가 아니라 infrastructure/db-core/persistence package에 둔다.
- Repository는 persistence-specific query shape를 넘어서는 business decision을 담지 않는다.
- Service/use case는 `*Repository` 포트에 의존하고, `*CoreRepository`, `*JpaRepository`, `EntityManager`, QueryDSL factory 같은 구체 infrastructure 타입에 직접 의존하지 않는다.
- `*CoreRepository`는 `*Repository`를 구현하며 JPA Entity와 domain/result mapping, `toDomain()` 변환, `*JpaRepository` 위임, 필요한 `*CustomRepository`/QueryDSL 조합을 소유한다. Spring Data type, `Pageable`, `EntityManager`, JPA annotation 의존이 domain 포트로 새면 boundary finding으로 본다.
- Infrastructure adapter는 vendor SDK, SQL/JPA detail, HTTP client, serialization quirk를 격리해야 한다.
- Application/use-case component는 이름으로 의도를 드러내야 한다. 생성, 삭제, 취소, 발급, 승인, 정산 flow가 단순 한 줄 위임보다 크다면 응집도 높은 component로 표현한다.
- Facade는 Service만 orchestration한다. repository, entity manager, vendor client, mapper, port, low-level role component를 Facade에 직접 주입하지 말고 Service 뒤로 숨긴다.
- Service는 단일 도메인 business responsibility를 소유하고, 필요하면 repository, port, adapter, internal role component에 의존할 수 있다.
- Service는 API response DTO, persistence entity, primitive bundle, transport-specific shape를 application boundary 밖으로 새게 하지 말고 `*Result` 타입을 반환해야 한다.
- Command, Query, Criteria, Result는 immutable하고 intent가 드러나는 이름을 가져야 하며, construction이 trivial하지 않으면 static factory로 mapping한다.
- Extension function은 stateless하고 dependency-free해야 한다. authorization, transaction, persistence, remote call, business policy를 extension function 안에 숨기지 않는다.
- 패턴 구현은 해당 동작을 소유한 layer 안에 있어야 한다. Strategy/Policy/Specification은 도메인 동작 가까이에, Adapter/Port는 외부 경계에, Template Method는 안정된 생명주기가 실제로 공유되는 곳에만 둔다.

## 실패 모드 점검

- 모든 외부 호출에는 timeout, 필요한 경우 retry policy, typed error handling이 있다.
- retry는 idempotent하거나 idempotency key로 보호되어야 한다.
- database write + event publish, file write + metadata persist, remote call + local state update의 partial failure path를 명시한다.
- log에는 correlation context를 포함하되 secret이나 sensitive payload는 절대 포함하지 않는다.

## 리뷰 휴리스틱

- cyclic dependency, domain code로의 framework leakage, hidden global state, business rule용 magic string, dependency를 숨기는 static helper를 찾는다.
- 별도 책임을 encoding하는 private method chain을 찾는다. method name이 business action, policy, reusable orchestration step이라면 명시적 role을 가진 component 추출을 우선한다.
- Service가 아닌 것에 의존하는 Facade, 또는 flow가 중요해 보인다는 이유만으로 Facade에 들어간 single-domain logic을 찾는다.
- call chain을 깊게 만드는 반복 private helper나 흩어진 method를 찾는다. 순수 reusable operation이면 common/support/util package의 named extension function으로 추출하는 편을 우선한다.
- mapping이나 invariant 결정을 숨기는 direct constructor call을 찾는다. construction에 의미가 있으면 `from`, `of`, `create` 같은 companion factory를 우선한다.
- `*Result`가 application contract를 명확히 만들 수 있는데 Service가 entity, response DTO, primitive, pair/triple을 반환하는지 찾는다.
- request DTO가 Command, Query, Criteria, Result로 동시에 재사용되는지 찾는다. layer ownership과 validation clarity가 좋아지면 intent별로 분리한다.
- `*Repository`가 Spring Data `JpaRepository`를 직접 상속하거나 Service가 `*JpaRepository`/`*CoreRepository`를 직접 주입받는 구조를 찾는다. 기본 fix는 domain `*Repository` 포트와 infrastructure `*CoreRepository : *Repository` adapter로 분리하는 것이다.
- domain package 또는 domain module 안의 `*Entity`, `@Entity`, `@Table`, `@Column`, `@Id`를 찾는다. 기본 fix는 JPA Entity를 infrastructure/db-core로 이동하고 domain에는 순수 data class를 둔 뒤 Entity `toDomain()` 변환을 통해 사용하게 하는 것이다.
- 같은 type/status/provider에 대한 반복 conditional을 찾는다. variation point에 따라 Strategy, State, Specification, Adapter, 또는 exhaustive `when`을 가진 sealed type을 우선한다.
- step이 달라지는 안정된 워크플로우 골격을 찾는다. inheritance가 role component 조합보다 생명주기를 더 잘 모델링할 때만 Template Method를 고려한다.
- 패턴 과사용을 찾는다. 안정적인 구현 하나뿐인 interface, fragile protected hook을 가진 abstract class, business side effect를 숨기는 decorator, ordering이 테스트되지 않은 pipeline을 확인한다.
- broad rewrite보다 작은 concrete fix를 우선한다. 현재 변경이 결합도를 늘리거나 중요한 동작을 테스트하기 어렵게 만들 때만 refactor를 추천한다.
- repository에 명확한 local convention이 있으면 security나 correctness와 충돌하지 않는 한 적용한다.
