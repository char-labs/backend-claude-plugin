---
name: persistence-query-review
description: Repository 포트, CoreRepository 구현체, JpaRepository 분리, JPA Entity infrastructure/db-core 위치, toDomain mapping, SQL, JPQL, QueryDSL, JPA/Hibernate, scalar FK, 관계 어노테이션 지양, fetch strategy, N+1 수정, pagination, index, projection, 트랜잭션 경계 등 쿼리 중심 백엔드 작업을 리뷰하거나 설계할 때 사용.
argument-hint: "[쿼리, Repository, 영속성 작업]"
---

# 영속성/쿼리 리뷰

## 설명

사용자 요청에서 persistence 또는 query shape이 핵심일 때 사용한다. 단순 성능 리뷰가 아니라 데이터 접근 권한, result cardinality, transaction boundary까지 함께 본다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/persistence-query-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- JPA/Hibernate/Kotlin이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. input, filter, ownership constraint, cardinality, expected result size, hot path 여부를 식별한다.
2. parameter binding, allowlisted dynamic filter/sort, tenant/account scoping, object-level authorization을 확인한다.
3. `*Repository`가 도메인/application 포트인지, `*CoreRepository : *Repository`가 infrastructure 구현체인지, `*JpaRepository`/`*CustomRepository`가 구현 내부에 숨었는지 확인한다.
4. Service/use-case/Facade가 `*JpaRepository`, `*CoreRepository`, `EntityManager`, QueryDSL factory에 직접 의존하면 `*Repository` 포트 뒤로 이동하도록 제안한다.
5. JPA Entity가 domain package/module에 들어갔는지 확인한다. Entity는 infrastructure/db-core에 두고 domain에는 순수 data class를 둔 뒤 `toDomain()`으로 변환하도록 제안한다.
6. 검색/필터 조건은 immutable `*Criteria`, 읽기 의도는 `*Query`로 표현하고 API request DTO나 entity를 그대로 쿼리 경계에 흘리지 않는지 확인한다.
7. projection/result mapping에 의미가 있으면 `from`/`of` 정적 팩토리를 우선하고, Service read 결과는 `*Result`로 경계를 드러낸다.
8. JPA Entity가 `@ManyToOne`, `@OneToMany`, `@ManyToMany`, `JoinColumn`에 의존하는지 확인하고, 신규 코드는 scalar FK + 명시 조인/projection으로 바꾸도록 제안한다.
9. 다대다는 `@ManyToMany` 대신 연결 엔티티와 양쪽 FK로 모델링하는지 확인한다.
10. N+1, lazy load, unbounded read, pagination 누락, broad fetch, index 누락, expensive count를 확인한다.
11. transaction scope, per-row write, batch behavior, stale persistence context risk를 확인한다.
12. query result correctness, authorization boundary, pagination/limit, bottleneck regression 테스트를 제안한다.

## 검증

- query result와 ownership boundary를 테스트로 확인한다.
- pagination/limit과 sort/filter allowlist를 검증한다.
- 가능한 경우 query plan, integration test, repository slice test를 활용한다.

## 주의사항

- 실수 방지 가드레일: 쿼리 변경은 result correctness, ownership boundary, pagination/limit 회귀 테스트를 함께 본다.
- 동적 SQL/정렬은 문자열 결합보다 parameter binding과 allowlist를 우선한다.
- fetch join은 pagination, duplicate row, cartesian product 위험을 함께 본다.
- Repository가 authorization 누락을 숨기면 보안 finding으로 본다.
- `*Repository`는 추상화된 포트로 유지한다. `*JpaRepository` 상속, Spring Data type 노출, `*CoreRepository` 직접 주입은 경계 누수로 본다.
- `*CoreRepository`는 `*Repository` 구현체로 `*JpaRepository`/`*CustomRepository`/QueryDSL 위임과 infrastructure/db-core Entity `toDomain()` mapping을 소유한다.
- domain에는 JPA annotation이 없는 순수 data class를 둔다. `@Entity`, `@Table`, `@Column`, `@Id`는 infrastructure/db-core Entity에만 허용한다.
- 관계 어노테이션은 legacy 호환 또는 명시 승인 예외로만 본다. 신규 read model은 scalar FK, 명시 조인, projection, `*Result` mapping으로 만든다.
- `@ManyToMany`는 신규 코드에서 사용하지 않는다. 연결 엔티티가 audit, 권한, 삭제/수정 lifecycle을 소유해야 한다.
- `Criteria`는 optional filter/sort/pagination/search 조건을 담고, query builder나 repository 의존성을 품지 않게 한다.
- 쿼리 DTO, projection, enum, static helper는 코드 본문/하단 영역에 fully qualified name으로 쓰지 않는다. 파일 상단 import를 우선하고, Java static member는 `import static`을 사용한다.

## 출력

evidence, query-shape impact, concrete fix, validation command를 포함해 반환한다.
