---
name: performance-review
description: 쿼리 병목, JPA Entity infrastructure/db-core 위치, toDomain mapping, 관계 어노테이션 기반 lazy loading, N+1, pagination/index 누락, transaction/lock scope, blocking IO, memory pressure, caching, timeout, retry 등 백엔드 성능 위험을 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 엔드포인트, 쿼리, 리뷰 범위]"
---

# 백엔드 성능 리뷰

## 설명

사용자 요청을 query bottleneck과 application bottleneck 관점으로 검토한다. 데이터 분포나 운영 index가 보이지 않아 확정할 수 없는 경우 residual risk로 표시한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- Spring/JPA/Kotlin persistence면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- Spring/Kotlin coroutine/concurrency이면 `spring-coroutine-concurrency` skill 기준을 함께 적용한다.

## 실행 절차

1. hot path, loop, repository call, serializer, mapper, remote call을 식별한다.
2. query shape을 확인한다: N+1, limit 누락, pagination 누락, index 누락, non-sargable predicate, count query, broad object graph loading.
3. transaction을 확인한다: lock scope, isolation level, transaction 내부 remote call, per-row flush/write, retry behavior.
4. application resource를 확인한다: blocking IO, memory aggregation, expensive hot-loop work, cache correctness, timeout, circuit breaker, bounded retry.
5. JPA/Hibernate에서는 `@ManyToOne`, `@OneToMany`, `@ManyToMany` 관계 어노테이션이 mapper, JSON serialization, logging, DTO construction, collection iteration에서 lazy loading 또는 broad graph fetch를 유발하는지 본다.
6. JPA Entity는 infrastructure/db-core에 두고 domain에는 순수 data class를 둔다. Entity `toDomain()`이 lazy association traversal로 성능 문제를 숨기지 않는지 확인한다.
7. 신규 Entity 성능 fix는 scalar FK + 명시 조인/projection을 우선한다. 다대다는 `@ManyToMany` 대신 연결 엔티티를 전제로 검토한다.
8. coroutine이면 dispatcher 선택, `Dispatchers.IO` blocking 격리, unbounded fan-out, cancellation/timeout, thread/memory tradeoff를 확인한다.

## 검증

- 가능한 경우 기존 benchmark, query plan, test, log, metric으로 확인한다.
- 운영 데이터 shape/index가 필요하면 확인 방법을 명시한다.

## 주의사항

- 실수 방지 가드레일: 성능 finding은 재현 조건, 측정 지표, 회귀 검증 방법을 함께 요구한다.
- 미세 최적화보다 사용자 영향, 부하 상황, 확장성에 영향을 주는 병목을 우선한다.
- 캐시는 stale data, stampede, invalidation, authorization leakage 위험을 함께 검토한다.
- 관계 어노테이션 기반 객체 그래프 탐색을 성능 편의 기능으로 보지 않는다. hot path에서는 scalar FK, 명시 조인, projection, pagination을 우선한다.
- domain의 순수 data class와 infrastructure/db-core Entity 경계를 섞어 lazy loading이나 serializer fetch를 숨기지 않는다. `toDomain()`은 현재 값만 사용하는 순수 mapping이어야 한다.
- `Dispatchers.IO`는 DB pool, 외부 API limit, lock, heap pressure를 해결하지 못하므로 fan-out 경계를 함께 본다.

## 출력

finding에는 concrete evidence와 likely runtime impact를 포함한다. 확정 불가 항목은 residual risk와 검증 방법을 제시한다.
