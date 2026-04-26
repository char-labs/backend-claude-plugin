# Persistence Query Patterns

Use this reference for Repository, SQL, JPQL, QueryDSL, JPA/Hibernate, and query-performance work.

## Query Safety

- Bind parameters. Never concatenate user input into SQL, JPQL, QueryDSL expressions, native query strings, or sorting expressions.
- Allowlist dynamic identifiers such as table names, column names, sort fields, and filter keys.
- Apply tenant/account/user ownership filters in data access or use-case logic before returning protected rows.

## Query Shape

- Bound collection reads with pagination or explicit limits.
- Avoid broad `findAll` calls on request paths.
- Prefer projections when callers need a small subset of columns.
- Use fetch joins, entity graphs, batch size, or explicit queries to avoid N+1 access.
- Avoid lazy loading triggered from DTO mappers, JSON serializers, log statements, and loops.

## Index And Plan Checks

- Verify indexes for frequent filters, joins, ordering, uniqueness checks, and foreign keys.
- Watch leading wildcard searches, functions on indexed columns, implicit casts, and non-sargable predicates.
- Avoid expensive counts on hot paths unless required and indexed.

## Transactions

- Keep transactions at use-case/service boundaries.
- Do not hold transactions around remote calls or slow IO.
- Avoid per-row flushes and writes in loops. Batch when safe.
- For bulk updates, account for stale persistence context and domain event consistency.

## Spring/JPA Notes

- Use `@Transactional(readOnly = true)` for read use cases where local convention supports it.
- Avoid relying on open-in-view to mask transaction boundary problems.
- Kotlin/Java 코드에서는 쿼리 DTO, projection, enum, static helper를 본문에서 fully qualified name으로 쓰지 말고 파일 상단 import로 올린다. Java static member는 `import static`을 사용한다.
