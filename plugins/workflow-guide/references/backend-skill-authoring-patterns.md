# 백엔드 스킬 작성 패턴

이 문서는 백엔드 프로젝트 전용 스킬을 `Entity Skill` 예시 같은 뉘앙스로 만들기 위한 작성 패턴이다.

## 목차

- 핵심 구조
- SKILL.md 작성 패턴
- 좋은 description 규칙
- 컨텍스트 캐시 친화성
- 실수 방지 가드레일
- 상세 자료 분리 기준
- 백엔드 도메인 스킬 유형
- Kotlin/Spring 백엔드 필수 체크
- Entity Skill 뉘앙스 추출

## 핵심 구조

스킬은 짧은 실행 가이드와 긴 상세 자료로 나눈다.

```text
skills/{skill-name}/
  SKILL.md
  references/
    full-workflow.md
    examples.md
```

- `SKILL.md`: 언제 쓰는지, 실행 순서, 위치/명명 규칙, 검증, 주의사항.
- `references/full-workflow.md`: 상세 코드 예시, 예외 케이스, 깊은 설명.
- `references/examples.md`: 실제 Entity/Repository/GraphQL/gRPC/Test 예시.

플러그인 공용 스킬이면 상세 자료는 `${CLAUDE_PLUGIN_ROOT}/references/...`에 두고, 프로젝트 로컬 스킬이면 해당 skill의 `references/` 하위에 둔다.

## SKILL.md 작성 패턴

Frontmatter:

```markdown
---
name: entity-skill
description: JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 새로 만들거나 수정할 때 사용. Entity infrastructure/db-core 위치, BaseEntity, 순수 domain data class, toDomain mapping, scalar FK, 관계 어노테이션 지양, 연결 엔티티, `*Repository` 포트, `*CoreRepository` 구현체, `*JpaRepository` 분리, QueryDSL 필요 여부를 함께 판단한다.
---
```

본문 구성:

```markdown
# Entity Skill

## 설명
새로운 JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 작성한다.

## 실행 절차
1. 기존 유사 도메인의 Entity/Repository 패턴 확인
2. JPA Entity는 infrastructure/db-core 위치로 결정하고, domain에는 순수 data class를 둔다
3. BaseEntity가 필요하면 `@MappedSuperclass`, `AuditingEntityListener`, `GenerationType.IDENTITY`, audit/soft delete, id 기반 `equals/hashCode` 기준 확인
4. ID, 필드 nullability, scalar FK, audit 필드 작성
5. Entity `toDomain()`으로 domain 객체 변환 작성
6. 다대다는 `@ManyToMany`가 아니라 연결 엔티티로 작성
7. `*Repository` 도메인 포트와 `*CoreRepository : *Repository` infrastructure 구현체 작성
8. `*JpaRepository`/`*CustomRepository`/QueryDSL은 `*CoreRepository` 내부 위임으로 분리
9. 보안/인가, 쿼리 병목, 트랜잭션 경계 확인
10. 컴파일/테스트 실행

## 검증
`./gradlew :domain:compileKotlin`

## 주의사항
- var 최소화, val 우선
- JPA Entity는 domain에 두지 않고 infrastructure/db-core에 둔다. domain에는 JPA annotation 없는 순수 data class만 둔다.
- BaseEntity는 persistence support package에 두고 domain에는 두지 않는다. `equals`는 같은 class와 같은 id에서 true가 되어야 하며, `deletedAt`/`softDelete`만으로 soft delete 조회 정책이 완성됐다고 쓰지 않는다.
- Entity는 `toDomain()`으로 domain 객체로 변환한다.
- 신규 Entity는 관계 어노테이션보다 `userId`, `postId` 같은 scalar FK 우선
- 다대다는 `@ManyToMany` 대신 연결 엔티티 우선
- `*Repository`는 추상화된 포트, `*CoreRepository`는 구현체, `*JpaRepository`는 내부 구현 세부사항
- userId/tenantId 등 소유권 필터 누락 금지
- 상세 패턴은 references/full-workflow.md 참조
```

## 좋은 description 규칙

description은 선택률에 큰 영향을 준다. 제목형보다 트리거형으로 쓴다.

좋음:

- `JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 새로 만들거나 수정할 때 사용.`
- `Entity를 domain이 아니라 infrastructure/db-core에 두고 toDomain으로 변환하는 구조를 설계할 때 사용.`
- `Repository 포트, CoreRepository 구현체, JpaRepository 분리, QueryDSL 쿼리 구조를 정리할 때 사용.`
- `GraphQL 스키마, Query/Mutation, input/output, resolver 경계 설계 시 사용.`
- `gRPC proto 필드/메서드 추가, 하위 호환성, 서버/클라이언트 에러 처리 설계 시 사용.`

피함:

- `Entity 가이드`
- `개발 가이드`
- `백엔드 참고 문서`

## 컨텍스트 캐시 친화성

Claude prompt caching은 정적 prefix가 100% 동일할 때 가장 잘 맞는다. 스킬 문서는 요청마다 바뀌는 값을 앞쪽에 두지 않는다.

원칙:

- `SKILL.md` 본문에는 `$ARGUMENTS`, 사용자 원문, timestamp, 오늘 날짜, 개인 로컬 절대경로를 넣지 않는다.
- 요청 대상을 가리킬 때는 `사용자 요청`, `입력된 작업`, `대상 코드`처럼 정적인 표현을 쓴다.
- section 순서를 고정한다: `설명 → 상세 자료 → 실행 절차 → 검증 → 주의사항 → 출력`.
- 상세 자료는 필요한 파일만 읽게 하고, 항상 같은 순서로 나열한다.
- 프로젝트별 경로, catalog, 긴 예시는 reference나 context pack으로 분리한다.
- 자주 바뀌는 운영 상태, 최신 버전, 현재 이슈 목록은 plugin 문서에 고정하지 말고 사용자 요청 또는 repo 상태에서 확인하게 한다.

## 실수 방지 가드레일

모든 skill과 agent는 작업 자체의 결과뿐 아니라 회귀 방지 장치를 함께 다룬다.

- routing, hook, fixture, 문서 정책, cache hygiene에 영향이 있으면 관련 테스트를 함께 갱신한다.
- 가능한 검증은 code-based grading으로 둔다: JSON schema, string match, exit code, fixture assertion.
- LLM judge나 prompt/agent hook은 기본 차단 gate가 아니라 advisory로 둔다.
- hook은 입력 JSON 검증, shell quoting, path traversal 차단, 민감 파일 보호를 기본 규칙으로 둔다.
- 공통 세부 원칙은 `${CLAUDE_PLUGIN_ROOT}/references/quality-guardrails.md`를 따른다.

## 상세 자료로 빼야 하는 내용

- 긴 Kotlin 코드 예시
- QueryDSL/Native Query 패턴
- gRPC 서버/클라이언트 에러 처리
- 트랜잭션 예시
- 프로젝트별 catalog 표
- 모듈별 경로와 build command
- 자주 발생하는 anti-pattern

이런 내용은 `SKILL.md`에 모두 넣으면 context를 낭비한다. `SKILL.md`에서는 “언제 어떤 상세 자료를 읽을지”만 알려준다.

## 백엔드 도메인 스킬 유형

| 유형 | 예시 | SKILL.md에 둘 내용 | 상세 자료에 둘 내용 |
|---|---|---|---|
| 생성/수정 | Entity, GraphQL, gRPC | 실행 순서, 위치, 검증 | 상세 코드 예시, 예외 |
| 설정 | DataSourceConfig, JpaConfig, yml, Flyway | 프로젝트 구조 확인, prefix/package/profile 선택, migration target 확인, 검증 | HikariConfig, ConfigurationProperties, EntityScan, EnableJpaRepositories, open-in-view, Flyway locations/baseline/validate 예시 |
| 리뷰 | Security, Query, OOP | 체크 순서, 심각도 | 체크리스트, 사례 |
| 검증 | Gradle, Test | 명령 선택 기준 | 실패 triage, 모듈별 명령 |
| 문서화 | ADR, Migration | 문서 구조, 의사결정 기준 | 템플릿, 배포 계획 예시 |

## Kotlin/Spring 백엔드 스킬 필수 체크

- Kotlin/Java 코드에서는 본문/하단 영역의 inline FQCN을 금지하고 파일 상단 import를 우선한다. Java static member는 `import static`을 사용하도록 스킬에 명시한다.
- class 내부의 private method로 비즈니스 책임을 숨기지 않는다. `private`는 정말 내부적인 작은 세부 구현에만 쓰고, 이름 붙일 수 있는 행동은 `UserCreator`, `PostDeleter`, `CouponIssuer` 같은 역할 컴포넌트로 추출하도록 스킬에 명시한다.
- 복잡한 비즈니스 로직은 Facade 패턴으로 여러 Service를 조합하고, 단일 도메인 책임은 Service 패턴으로 구현하도록 명시한다.
- Facade는 Service만 의존해야 한다. Repository, EntityManager, 외부 client, mapper, port, 역할 컴포넌트는 Facade에 직접 주입하지 않는다.
- 여러 class에서 반복될 Kotlin helper는 private method나 흩어진 메서드로 두지 않고 `common`, `support`, `util` 또는 도메인 support 패키지의 top-level 확장 함수로 추출하도록 명시한다.
- Kotlin scope function, `when`, `is` smart cast, null-safety, collection operation을 활용해 가독성, 유지보수성, 재사용성을 높이는 기준을 포함한다.
- Spring Boot + Kotlin coroutine/concurrency 스킬은 coroutine 도입 이유, blocking 요소, dispatcher 선택, structured concurrency, bounded fan-out, thread/memory tradeoff를 반드시 포함한다.
- kt 파일에는 독립적인 public data class를 여러 개 넣는 것을 기본 지양한다. 같은 부모 컨텍스트의 nested command/info/result 또는 응답 wrapper + DTO처럼 강하게 결합된 경우만 예외로 허용한다.
- Controller는 얇게 유지하고, Service/UseCase가 트랜잭션과 비즈니스 흐름을 소유한다.
- Repository는 persistence 접근을 소유하되 인가/도메인 결정을 숨기지 않는다.
- JPA Entity는 infrastructure/db-core/persistence adapter에 둔다. domain에는 JPA annotation 없는 순수 data class/domain object를 두고 Entity `toDomain()`으로 변환한다.
- BaseEntity 스킬이나 Entity 스킬에는 `@MappedSuperclass`, `AuditingEntityListener`, `GenerationType.IDENTITY`, `CreationTimestamp`, `UpdateTimestamp`, `softDelete`, id 기반 `equals/hashCode` 기준을 포함한다.
- Spring persistence 설정 스킬은 `db-core`, `db.core`, `coreDataSource` 같은 예시 이름을 그대로 복사하지 않고 프로젝트 module/package/profile/prefix에 맞추도록 명시한다. `HikariConfig`, `ConfigurationProperties`, `EntityScan`, `EnableJpaRepositories`, `open-in-view`, Flyway locations/baseline/validate/clean-disabled, 환경변수 placeholder를 함께 다룬다.
- `*Repository`는 추상화된 도메인/application 포트 인터페이스로 둔다. Service/UseCase는 이 포트에 의존하고 `*CoreRepository`, `*JpaRepository`, `EntityManager`, QueryDSL factory를 직접 주입받지 않는다.
- `*CoreRepository`는 `*Repository`를 상속/구현한 infrastructure adapter로 둔다. 내부에서 `*JpaRepository`, `*CustomRepository`, QueryDSL, Redis/client adapter를 조합한다.
- `*JpaRepository`는 Spring Data 구현 세부사항이므로 infrastructure package 밖으로 노출하지 않는다.
- JPA 신규 Entity는 `FetchType.LAZY` 관계 어노테이션을 기본값으로 두지 않는다. `userId`, `postId` 같은 scalar FK와 Repository/QueryDSL 명시 조인을 우선하고, 관계 어노테이션은 legacy/명시 승인 예외로만 다룬다.
- `@ManyToMany`는 신규 코드에서 사용하지 않고 연결 엔티티로 풀어 audit, 권한, 삭제 정책, index를 드러낸다.
- QueryDSL/Native Query는 parameter binding을 사용하고 동적 정렬/필터는 allowlist로 제한한다.
- 사용자/tenant/account 소유권 필터는 누락되면 보안 finding으로 본다.
- 변경 후 최소 검증 명령을 스킬에 명시한다.

## Facade/Service 적용 기준

Facade와 Service는 책임 범위로 구분한다.

| 상황 | 권장 패턴 | 의존성 규칙 |
|---|---|---|
| 여러 도메인/외부 side effect/정책을 엮는 복잡한 흐름 | `OrderCheckoutFacade`, `SignupFacade` | Service만 의존 |
| 단일 도메인의 정책, 검증, 상태 변경, 저장 | `UserService`, `PostService` | `*Repository` port 의존 가능 |
| 세부 비즈니스 행동이 커지는 경우 | `UserCreator`, `PostDeleter` 같은 내부 역할 컴포넌트 | Service 내부 협력자로 제한 |

규칙:

- Facade는 orchestration 계층이다. 직접 조회/저장/외부 호출/DTO mapping을 담당하지 않는다.
- Facade constructor에는 `*Service`만 들어가야 한다.
- Facade가 Repository, EntityManager, client, mapper, port를 필요로 하면 그 책임을 Service로 내린다.
- Service가 persistence에 접근할 때도 구체 구현체가 아니라 `*Repository` 포트에 의존한다. `*CoreRepository`와 `*JpaRepository`는 infrastructure adapter 내부에 머문다.
- 단일 도메인 로직을 Facade로 만들지 않는다. 중요한 흐름이어도 하나의 도메인 책임이면 Service에 둔다.
- Service가 여러 도메인 Service를 조합하기 시작하면 Facade 추출 후보로 본다.

## Kotlin 확장 함수 적용 기준

확장 함수는 반복되는 순수 helper를 드러내는 도구다.

| 상황 | 권장 위치 | 주의 |
|---|---|---|
| 문자열/날짜/숫자/collection/null-safety 변환이 여러 class에서 반복됨 | `common`, `support`, `util` 패키지 | 순수 함수로 유지 |
| 특정 도메인 타입의 표현/계산 helper가 여러 도메인 class에서 반복됨 | 도메인 support 또는 `{domain}/util` 패키지 | 도메인 밖으로 과도하게 노출하지 않음 |
| 테스트 fixture나 assertion helper가 반복됨 | test `support` 또는 `fixture` 패키지 | production util과 분리 |

규칙:

- 두 곳 이상에서 반복될 가능성이 높거나 call depth를 늘리는 private helper는 확장 함수 후보로 본다.
- 프로젝트에 이미 `common`, `support`, `util` convention이 있으면 그것을 우선한다.
- 전역 util dumping ground를 만들지 않는다. 수신 타입과 도메인 컨텍스트가 드러나는 파일명을 쓴다. 예: `StringExtensions.kt`, `CollectionExtensions.kt`, `UserExtensions.kt`.
- 확장 함수는 top-level로 두고 파일 상단 import로 사용한다.
- repository/client 호출, transaction, authorization, business policy, 외부 협력 조합은 확장 함수에 넣지 않는다.
- 그런 로직은 Service, 역할 컴포넌트, Facade/Service 경계 안에 둔다.

## Kotlin 관용 표현 적용 기준

Kotlin 문법은 의도를 더 선명하게 만들 때 적극 사용한다.

| 패턴 | 권장 사용 | 주의 |
|---|---|---|
| `apply` | 객체 생성 직후 receiver 설정 | 비즈니스 절차를 숨기지 않음 |
| `also` | logging, metric, validation checkpoint 같은 side effect | 핵심 상태 변경을 몰래 넣지 않음 |
| `let` | nullable 값 처리, 짧은 변환 | 중첩 `it`를 만들지 않음 |
| `run` | receiver 기반 계산 후 결과 반환 | 긴 orchestration을 숨기지 않음 |
| `with` | 이미 존재하는 receiver의 여러 연산 grouping | receiver가 모호하면 피함 |
| `when` | enum/sealed/status/type 분기 | 가능한 exhaustive expression으로 사용 |
| `is` smart cast | 타입별 분기와 안전한 cast | unsafe cast와 중복 cast를 피함 |
| collection operation | in-memory `map`, `filter`, `associateBy`, `groupBy`, `flatMap` | DB lazy loading/N+1을 숨기지 않음 |

규칙:

- scope function은 Kotlin의 장점을 살려 가독성과 유지보수성을 높일 때 우선 고려한다.
- 중첩 scope function, 모호한 `it`, receiver shadowing, side effect가 많은 긴 chain은 피한다.
- enum, sealed class, 상태값 분기는 흩어진 `if/else`보다 exhaustive `when`을 우선한다.
- 타입 분기는 `is` smart cast로 boilerplate와 unsafe cast를 줄인다.
- null 처리에는 safe call, Elvis, `let`, `takeIf`, `takeUnless`를 검토한다.
- collection operation은 순수 in-memory 변환에 적합하다. repository 호출, lazy association 접근, 외부 IO를 숨기지 않는다.

## Spring Coroutine 스킬 작성 기준

coroutine 스킬은 성능 최적화 문법이 아니라 동시성 설계 기준으로 작성한다.

| 주제 | 포함할 기준 |
|---|---|
| 도입 판단 | 단일 MVC/JPA 모놀리식이면 불필요할 수 있고, 독립 IO 병렬화나 suspend stack이 명확하면 적극 검토 |
| Dispatcher | blocking IO는 `Dispatchers.IO`, CPU-bound는 `Dispatchers.Default`, suspend client는 불필요한 전환 회피 |
| Structured concurrency | 모두 성공해야 하면 `coroutineScope`, 부분 실패 격리는 `supervisorScope`, 독립 작업은 bounded `async/await` |
| Blocking detector | JPA/JDBC, blocking HTTP client, file IO, sync Redis/Kafka, `.block()`, `Thread.sleep`, request path `runBlocking` |
| 리소스 tradeoff | coroutine fan-out, DB connection pool, external rate limit, heap allocation, scheduler overhead, retry amplification |
| Failure mode | timeout, cancellation propagation, idempotent retry, fallback, metrics |

규칙:

- `Dispatchers.IO`는 blocking 격리 수단이지 성능 보장 수단이 아니다.
- unbounded fan-out을 금지하고 batch size, `Semaphore`, `limitedParallelism`, queue/pool limit을 검토한다.
- transaction, SecurityContext, MDC/logging context가 coroutine boundary에서 유지되는지 확인한다.
- coroutine 안에서 lazy loading, transaction 내부 remote call, 외부 IO를 숨기지 않는다.
- 테스트 기준에는 timeout, cancellation, partial failure, dispatcher/test scheduler convention을 포함한다.

## 책임 컴포넌트 명명 규칙

역할 컴포넌트는 동작과 책임이 이름에서 드러나야 한다.

| 상황 | 권장 이름 | 피할 이름 |
|---|---|---|
| 회원 생성 | `UserCreator` | `UserService.createUser` 내부 private chain |
| 글 삭제 | `PostDeleter` | `PostService.deleteInternal` |
| 쿠폰 발급 | `CouponIssuer` | `CouponHelper.process` |
| 주문 취소 | `OrderCanceller` | `OrderManager.handle` |

규칙:

- 생성, 삭제, 발급, 취소, 승인, 정산처럼 도메인 동작이 명확하면 컴포넌트 이름에 동사를 반영한다.
- 컴포넌트는 하나의 유스케이스나 정책을 중심으로 응집시킨다.
- 단순 한 줄 위임이나 불변식 보존용 작은 계산은 private로 남겨도 된다.
- private method가 테스트하고 싶은 행동, 정책 판단, 외부 협력 조합을 담고 있다면 컴포넌트 추출 후보로 본다.

## Kotlin 데이터 클래스 파일 구성

기본 원칙:

- 독립적인 public data class는 파일을 분리한다.
- 같은 `.kt` 파일에 여러 data class를 두는 것은 기본적으로 지양한다.
- 같은 컨텍스트 안에서만 읽히는 하위 타입은 nested data class로 묶을 수 있다.
- API 응답 wrapper와 그 wrapper 전용 DTO처럼 강하게 결합된 경우에는 같은 response 파일에 둘 수 있다.

허용 예:

- `NotificationStored.Create`, `NotificationStored.Info`, `NotificationStored.Result`처럼 부모 개념 아래의 command/info/result 타입.
- `FlowerSpotAllResponse`와 `FlowerSpotResponseDto`처럼 list/envelope 응답과 해당 응답 전용 DTO.

분리 권장:

- 서로 다른 API action의 request/response가 한 파일에 모인 경우.
- 여러 domain concept의 DTO가 편의상 한 파일에 모인 경우.
- 다른 package나 use case에서 독립적으로 재사용될 수 있는 data class.

## 정적 팩토리와 Message Type 규칙

정적 팩토리는 생성 의도, mapping, 기본값, invariant를 call site에 드러내기 위해 적극 사용한다.

| 상황 | 권장 패턴 | 설명 |
|---|---|---|
| 단일 source mapping | `companion object { fun from(source: Source): Target }` | domain/request에서 변환할 때 사용 |
| 값 조합 | `of(...)` | 이미 검증된 값들을 조합할 때 사용 |
| 새 도메인 생성 | `create(command)` | invariant, 기본값, 상태 초기화를 함께 담을 때 사용 |
| 복원/특수 상태 | `restore`, `empty`, `default` | 상태 의미가 도메인에 있을 때만 사용 |

JPA Entity/input model/command-like data class에서 domain model로 가는 순수 변환은 `toDomain()`으로 모은다. JPA Entity는 infrastructure/db-core에 있고 domain에는 순수 data class가 있어야 한다. `toDomain()`에는 repository/client 호출, 인가, 트랜잭션, lazy association traversal, 외부 ID/clock 호출을 넣지 않는다. 생성 정책이나 invariant가 복잡하면 `Domain.create(...)` 또는 별도 factory를 우선한다.

Message type 권장:

- write intent는 `*Command`.
- read intent는 `*Query`.
- 검색/필터/정렬/페이지 조건은 `*Criteria`.
- Service/use-case 결과는 `*Result`.
- `Command`, `Query`, `Criteria`, `Result`는 immutable data class를 기본으로 한다.
- API request/response DTO, persistence entity, domain object를 한 타입으로 겸용하지 않는다.
- Service가 entity, response DTO, primitive bundle, `Pair`/`Triple`을 그대로 반환하면 `*Result`로 경계를 드러내도록 유도한다.
- `../Pida-Server`, `../Sseudam-Server` 같은 sibling 예시 repo가 접근 가능하면 새 규칙을 만들기 전에 `*Command`, `*Query`, `*Criteria`, `*Result`, companion factory 사례를 먼저 확인한다.

## 객체지향 디자인 패턴 작성 기준

디자인 패턴은 패턴 이름보다 문제 축을 먼저 적는다.

| 문제 축 | 우선 검토 패턴 | 기준 |
|---|---|---|
| 정책/알고리즘이 여러 방식으로 바뀜 | Strategy | 결제, 알림 채널, 점수 계산, 권한 정책처럼 교체 가능한 행위 |
| 워크플로우 골격은 고정, 일부 단계만 다름 | Template Method | 생명주기가 안정적이고 상속 hook이 작게 유지될 때만 |
| 상태별 행위가 흩어짐 | State | 상태 추가 시 변경 위치를 줄일 수 있을 때 |
| business predicate가 재사용/조합됨 | Specification / Policy | 조건에 도메인 이름과 테스트가 필요할 때 |
| 외부 vendor/provider 경계 | Adapter / Port | vendor SDK, HTTP client, persistence 세부 구현을 격리할 때 |
| 선택적 cross-cutting wrapper | Decorator | cache, metric, retry, logging이 interface 주변에 붙을 때 |
| 순서 있는 검증/처리 단계 | Chain / Pipeline | 단계별 테스트와 명시적 순서가 필요할 때 |
| 생성 정책/객체군 | Factory / Domain Factory | clock, id, policy, dependency가 생성에 필요할 때 |

규칙:

- Strategy와 정적 팩토리는 기본 후보로 둘 수 있지만, 단일 구현에 interface만 추가하는 구조는 피한다.
- Template Method는 상속이 워크플로우 생명주기를 실제로 잘 표현할 때만 사용한다. 단순 변형이면 Strategy나 역할 컴포넌트 조합을 우선한다.
- Kotlin sealed interface와 exhaustive `when`이 더 단순한 closed set이면 다형성 hierarchy보다 우선할 수 있다.
- 패턴 구현은 계층 경계를 흐리지 않아야 한다. Repository/client/transaction/authorization을 숨기면 Service, Adapter, Port로 이동한다.
- Skill에는 “언제 어떤 패턴을 쓰는지”, “언제 쓰지 않는지”, “테스트 기준”을 함께 적는다.
- Agent 규칙에는 패턴 과사용도 리뷰 지적사항으로 볼 수 있게 단일 구현 interface, 불필요한 abstract class, 숨겨진 decorator 부수 효과, 테스트되지 않은 pipeline 순서를 명시한다.

## Entity Skill 뉘앙스 추출

예시의 좋은 점:

- 위치가 명확하다. 다만 예시의 `domain/src/main/kotlin/.../entity/{도메인}/`는 그대로 따르지 않고, JPA Entity는 `infrastructure`, `db-core`, `storage` 같은 JPA 의존 모듈로 이동한다.
- 실행 절차가 번호로 고정되어 있다.
- 코드 예시가 바로 적용 가능한 형태다.
- catalog 선택, compile command, 주의사항이 있다.
- 상세 워크플로우는 별도 상세 자료로 분리되어 있다.

일반화할 때:

- 특정 회사/서비스명은 placeholder로 바꾼다.
- catalog 표는 프로젝트 context pack으로 둔다.
- Entity 위치 예시는 infrastructure/db-core 기준으로 쓴다. domain 예시는 JPA annotation 없는 순수 data class로 분리한다.
- BaseEntity 예시는 infrastructure/db-core support package 기준으로 쓰고, equals/hashCode와 soft delete 조회 필터 가드레일을 포함한다.
- Entity 예시에는 `toDomain()` 변환을 포함한다.
- Entity 예시는 관계 어노테이션보다 scalar FK를 먼저 보여준다. 예: `PostEntity(val userId: Long, ...)`.
- Repository 예시는 `*Repository` 추상 포트, `*CoreRepository : *Repository` 구현체, `*JpaRepository` 내부 위임 구조를 먼저 보여준다.
- 다대다 예시는 `PostTagEntity(postId, tagId)` 같은 연결 엔티티를 보여주고, `@ManyToMany`는 예외/legacy 섹션으로 내린다.
- 보안/성능/테스트 체크를 기본 절차에 추가한다.
- 긴 예시는 `references/full-workflow.md`로 옮긴다.
- 캐시 hit를 위해 사용자 입력값은 문서 앞쪽에 직접 삽입하지 않는다.
