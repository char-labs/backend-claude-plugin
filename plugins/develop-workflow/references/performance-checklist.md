# 백엔드 성능 체크리스트

쿼리, 애플리케이션, 동시성, 리소스 병목 리뷰에서 이 자료를 사용한다.

## 데이터베이스와 쿼리 병목

- lazy loading, row별 repository call, resolver loop, mapper-triggered fetch에서 N+1 query pattern을 찾는다.
- unbounded read, pagination 누락, limit 누락, 넓은 `findAll`, 전체 object graph loading을 확인한다.
- 자주 쓰이는 filter, join, ordering, uniqueness check, foreign key에 필요한 index를 확인한다.
- non-sargable predicate, leading wildcard search, indexed column에 대한 function, implicit cast, 불안정한 query plan을 찾는다.
- 필요하고 index가 준비된 경우가 아니라면 hot path의 count query를 피한다.
- 적절한 경우 write/read를 batch 처리한다. loop 안의 item별 flush와 transaction을 피한다.

## 트랜잭션과 락

- transaction은 짧게 유지한다. 의도적인 consistency pattern이 아니라면 remote call, 느린 serialization, file IO, message publishing을 감싼 채 database transaction을 잡지 않는다.
- hot table의 pessimistic lock, 높은 isolation level, 넓은 update statement를 주의한다.
- retry는 idempotent하고 bounded하게 만든다. 장애 중 backoff가 부하를 증폭하지 않아야 한다.

## 애플리케이션 병목

- event-loop 또는 제한된 worker thread에서 blocking IO를 피한다.
- export, upload, report, search result, JSON aggregation의 memory 사용량을 제한한다.
- framework가 지원하면 큰 file과 response는 streaming한다.
- hot loop에서 비싼 parsing, reflection, serialization, regex compilation, object mapping을 반복하지 않는다.
- 안정적이고 공유해도 안전한 데이터만 cache한다. TTL, invalidation, stampede protection, tenant/user scoping을 정의한다.

## Coroutine과 스레드 리소스

- coroutine이 실제로 latency를 줄이거나 cancellation을 개선하는지 확인한다. blocking code를 비동기처럼 보이게 하려고 coroutine을 추가하지 않는다.
- `Dispatchers.IO`는 제한된 request/event-loop thread를 blocking work로부터 보호하지만 DB pool, external rate limit, lock, memory constraint를 제거하지는 않는다.
- coroutine fan-out은 batch size, semaphore, `limitedParallelism`, 기존 pool/queue limit으로 제한한다.
- event-loop/default dispatcher에서 JPA/JDBC, blocking HTTP client, file IO, sync messaging client, `.block()`, `Thread.sleep` 같은 blocking call을 피한다.
- 각 concurrent child task의 timeout, cancellation, retry, partial failure 동작을 추적한다.
- 많은 coroutine, captured object, 큰 response aggregation, 큰 collection에 대한 `awaitAll`로 생기는 memory pressure를 검토한다.

## 외부 호출

- 모든 HTTP/RPC/client call에는 timeout, bounded retry, 필요한 경우 circuit breaker 또는 bulkhead, fallback/error behavior가 있어야 한다.
- 독립 호출을 안전하게 batch 또는 parallel 처리할 수 있다면 sequential remote call을 피한다.
- domain getter, mapper, logging 안에 remote call을 숨기지 않는다.

## 성능 관측성

- latency, throughput, queue depth, error rate, timeout count, retry count, cache hit ratio, database pool saturation 지표를 추가한다.
- log는 민감정보를 남기지 않으면서 slow path를 식별할 수 있어야 한다.
- 성능 finding에는 query shape, loop boundary, missing limit, lock scope, allocation risk, missing timeout 같은 evidence를 포함한다.
