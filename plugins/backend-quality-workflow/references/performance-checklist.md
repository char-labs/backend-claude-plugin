# Backend Performance Checklist

Use this reference for query, application, concurrency, and resource bottleneck reviews.

## Database And Query Bottlenecks

- Identify N+1 query patterns from lazy loading, per-row repository calls, resolver loops, and mapper-triggered fetches.
- Check unbounded reads, missing pagination, missing limits, broad `findAll`, and loading entire object graphs.
- Verify indexes for frequent filters, joins, ordering, uniqueness checks, and foreign keys.
- Look for non-sargable predicates, leading wildcard searches, functions on indexed columns, implicit casts, and unstable query plans.
- Avoid count queries on hot paths unless required and indexed.
- Batch writes and reads where appropriate. Avoid per-item flushes and transactions in loops.

## Transactions And Locking

- Keep transactions short. Do not hold database transactions around remote calls, slow serialization, file IO, or message publishing unless there is a deliberate consistency pattern.
- Watch pessimistic locks, high isolation levels, and broad update statements on hot tables.
- Make retries idempotent and bounded. Backoff should not amplify load during incidents.

## Application Bottlenecks

- Avoid blocking IO on event-loop or limited worker threads.
- Bound memory use for exports, uploads, reports, search results, and JSON aggregation.
- Stream large files and responses where the framework supports it.
- Avoid repeated expensive parsing, reflection, serialization, regex compilation, and object mapping in hot loops.
- Cache only stable, safe-to-share data. Define TTL, invalidation, stampede protection, and tenant/user scoping.

## External Calls

- Every HTTP/RPC/client call should have timeout, bounded retry, circuit breaker or bulkhead where appropriate, and fallback/error behavior.
- Avoid sequential remote calls when independent calls can be batched or parallelized safely.
- Do not hide remote calls in domain getters, mappers, or logging.

## Observability For Performance

- Add metrics around latency, throughput, queue depth, error rates, timeout counts, retry counts, cache hit ratio, and database pool saturation.
- Logs should identify slow paths without logging sensitive data.
- Performance findings should include evidence: query shape, loop boundary, missing limit, lock scope, allocation risk, or missing timeout.
