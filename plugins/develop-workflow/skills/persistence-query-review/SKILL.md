---
name: persistence-query-review
description: Repository, SQL, JPQL, QueryDSL, JPA/Hibernate, fetch strategy, N+1 수정, pagination, index, projection, 트랜잭션 경계 등 쿼리 중심 백엔드 작업을 리뷰하거나 설계할 때 사용.
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
3. 검색/필터 조건은 immutable `*Criteria`, 읽기 의도는 `*Query`로 표현하고 API request DTO나 entity를 그대로 쿼리 경계에 흘리지 않는지 확인한다.
4. projection/result mapping에 의미가 있으면 `from`/`of` 정적 팩토리를 우선하고, Service read 결과는 `*Result`로 경계를 드러낸다.
5. N+1, lazy load, unbounded read, pagination 누락, broad fetch, index 누락, expensive count를 확인한다.
6. transaction scope, per-row write, batch behavior, stale persistence context risk를 확인한다.
7. query result correctness, authorization boundary, pagination/limit, bottleneck regression 테스트를 제안한다.

## 검증

- query result와 ownership boundary를 테스트로 확인한다.
- pagination/limit과 sort/filter allowlist를 검증한다.
- 가능한 경우 query plan, integration test, repository slice test를 활용한다.

## 주의사항

- 실수 방지 가드레일: 쿼리 변경은 result correctness, ownership boundary, pagination/limit 회귀 테스트를 함께 본다.
- 동적 SQL/정렬은 문자열 결합보다 parameter binding과 allowlist를 우선한다.
- fetch join은 pagination, duplicate row, cartesian product 위험을 함께 본다.
- Repository가 authorization 누락을 숨기면 보안 finding으로 본다.
- `Criteria`는 optional filter/sort/pagination/search 조건을 담고, query builder나 repository 의존성을 품지 않게 한다.
- 쿼리 DTO, projection, enum, static helper는 코드 본문/하단 영역에 fully qualified name으로 쓰지 않는다. 파일 상단 import를 우선하고, Java static member는 `import static`을 사용한다.

## 출력

evidence, query-shape impact, concrete fix, validation command를 포함해 반환한다.
