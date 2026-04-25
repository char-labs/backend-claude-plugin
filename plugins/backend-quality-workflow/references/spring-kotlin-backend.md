# Spring/Kotlin Backend Appendix

Use this reference when the target backend uses Kotlin, Spring Boot, Spring Security, JPA/Hibernate, Gradle, or related JVM infrastructure.

## Kotlin Style

- Prefer top-of-file imports over inline fully qualified class, enum, or object references in executable code.
- Keep fully qualified names only where the language or framework requires them, such as JPQL constructor expressions or string-based class names.
- Use Kotlin nullability as a contract. Avoid `!!` unless the invariant is proven locally and a better type cannot express it.
- Prefer immutable data for request commands and value objects.
- Keep extension functions discoverable and domain-relevant. Avoid hiding important dependencies in extensions.

## Spring Layering

- Controllers should be thin: request validation, auth context extraction, use-case call, response mapping.
- Services/use cases own transactions and orchestration.
- Repositories own persistence access only. Do not put authorization or workflow state machines in repository code.
- Configuration classes should not contain business logic.

## Spring Security

- Require explicit authorization for protected endpoints. Do not rely on route naming or UI-only controls.
- Check method-level security for use cases that can be reached from multiple adapters.
- Validate tenant/account ownership in the use case, not only in the controller.
- Avoid broad `permitAll`, wildcard CORS with credentials, disabled CSRF for cookie flows, and role checks that skip object-level authorization.

## JPA And Hibernate

- Review lazy loading triggered by DTO mappers, JSON serialization, logging, and loops.
- Use fetch joins, entity graphs, projections, or batch size intentionally. Do not fetch entire graphs by default.
- Avoid `open-in-view` as a way to hide transaction boundary problems.
- Watch `@Transactional(readOnly = true)` for reads and use write transactions for state changes.
- Avoid long transactions around remote calls or event publishing.
- Native queries and JPQL must bind parameters. Dynamic identifiers need allowlists.
- For bulk updates, account for persistence context staleness and domain event consistency.

## Gradle And Validation

- Prefer repo wrappers: `./gradlew test`, `./gradlew ktlintCheck`, `./gradlew detekt`, or project-specific tasks when present.
- Do not add plugins or dependencies automatically. Recommend additions with rationale.
- If a module path exists, scope validation to the affected module first, then broaden if shared contracts changed.

## Common Spring/Kotlin Findings

- N+1 from repository calls inside `map`, `forEach`, resolver methods, or lazy collection access.
- Missing object-level authorization after loading by ID.
- `@Transactional` missing around multi-step write use cases.
- Catch-all exception handlers returning internal messages.
- Logging request bodies, tokens, authorization headers, or entity snapshots with PII.
- Inline fully qualified names in executable Kotlin code where an import should be used.
