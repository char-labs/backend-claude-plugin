---
name: spring-coroutine-concurrency
description: Spring Boot + Kotlin coroutine, suspend function, coroutineScope/supervisorScope, Dispatchers.IO, blocking IO, structured concurrency, thread/memory tradeoff를 설계·구현·리뷰할 때 사용.
argument-hint: "[파일, diff, 엔드포인트, 비동기 처리 범위]"
---

# Spring Coroutine 동시성

## 설명

Spring Boot + Kotlin에서 coroutine 도입 여부와 구현 방식을 판단한다. 독립 IO 병렬화, blocking 격리, dispatcher 선택, structured concurrency, thread/memory tradeoff를 함께 검토한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`

## 실행 절차

1. 대상 프로젝트가 MVC/JPA/JDBC 중심인지, WebFlux/R2DBC/suspend client 중심인지 먼저 추론한다.
2. coroutine이 필요한 이유를 확인한다: 독립 외부 IO 병렬화, latency 절감, cancellation/timeout 전파, non-blocking stack 활용.
3. blocking 요소를 찾는다: JPA/JDBC, blocking HTTP client, file IO, Redis/Kafka sync client, lock/synchronized, `Thread.sleep`, `.block()`, `runBlocking`.
4. dispatcher를 결정한다: blocking IO는 `withContext(Dispatchers.IO)`, CPU-bound 작업은 `Dispatchers.Default`, suspend client는 불필요한 dispatcher 전환을 피한다.
5. structured concurrency를 적용한다: 모두 성공해야 하면 `coroutineScope`, 부분 실패 격리가 필요하면 `supervisorScope`, 독립 작업은 bounded `async/await`.
6. thread/memory tradeoff를 확인한다: fan-out 수, DB connection pool, external rate limit, heap allocation, scheduler overhead, backpressure.
7. timeout, cancellation, retry idempotency, fallback, metrics를 설계 또는 finding에 포함한다.

## 검증

- 영향 module의 compile/test를 우선한다.
- coroutine 변경이면 timeout/cancellation/failure propagation 테스트를 검토한다.
- 성능 목적이면 latency, thread usage, connection pool saturation, external call count를 검증 지표로 둔다.

## 주의사항

- 실수 방지 가드레일: coroutine 도입은 항상 blocking 여부, dispatcher 선택, bounded concurrency, cancellation, 메모리/스레드 영향과 함께 판단한다.
- 단일 서버 모놀리식 + blocking JPA 중심이면 coroutine이 필요 없을 수 있다. 다만 독립 IO 병렬화가 명확하면 제한적으로 사용한다.
- `Dispatchers.IO`는 blocking 격리 수단이지 성능 보장 수단이 아니다. DB pool이나 외부 API limit을 넘는 fan-out을 만들지 않는다.
- `GlobalScope`, request path의 `runBlocking`, unbounded `async`, transaction 내부 remote call, coroutine 안의 lazy loading을 피한다.
- coroutine context 전환으로 transaction/security/MDC context가 사라질 수 있는지 확인한다.

## 출력

도입 여부, blocking 요소, dispatcher/structured concurrency 선택, bounded concurrency 기준, 검증 방법, 남은 thread/memory risk를 요약한다.
