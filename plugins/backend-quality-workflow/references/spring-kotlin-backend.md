# Spring/Kotlin Backend Appendix

Use this reference when the target backend uses Kotlin, Spring Boot, Spring Security, JPA/Hibernate, Gradle, or related JVM infrastructure.

## Kotlin/Java Import Style

- 코드 본문, 함수 내부, 테스트 본문, 타입 선언 하단 영역에 `com.example.Foo`처럼 fully qualified name을 직접 쓰지 않는다.
- 클래스, enum, object, companion object member, top-level function, 테스트 헬퍼는 언어가 허용하는 한 파일 상단 import로 올린다.
- Java static member, assertion helper, Mockito/AssertJ/JUnit static helper는 본문에서 `org.example.Type.member`로 쓰지 말고 `import static`을 사용한다.
- Kotlin에서는 Java의 `import static` 대신 일반 import로 object/companion/top-level member를 직접 import할 수 있으면 그렇게 한다.
- Fully qualified name은 언어/프레임워크가 요구하는 경우에만 남긴다. 예: package/import 선언, JPQL/HQL constructor expression 문자열, string 기반 framework 설정, reflection/generator가 canonical class name 문자열을 요구하는 경우.

## Kotlin Style

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

## Spring/Kotlin Test Guardrails

- 테스트 코드는 실 DB, 공유 개발 DB, 운영 DB에 직접 연결하지 않는다.
- 테스트 코드에는 `@Transactional`을 붙여 rollback에 의존하지 않는다. 데이터 격리는 명시적 setup/cleanup, fake/mock, 또는 repo convention의 disposable test DB로 처리한다.
- Presentation/Controller 테스트는 선택 항목이다. 작성 전 사용자에게 확인하고, 기본은 Service/UseCase/Domain 테스트를 우선한다.

## Common Spring/Kotlin Findings

- N+1 from repository calls inside `map`, `forEach`, resolver methods, or lazy collection access.
- Missing object-level authorization after loading by ID.
- `@Transactional` missing around multi-step write use cases.
- Catch-all exception handlers returning internal messages.
- Logging request bodies, tokens, authorization headers, or entity snapshots with PII.
- 본문/하단 영역의 inline fully qualified name. Java static member는 `import static`, Kotlin member/top-level reference는 파일 상단 import를 써야 한다.
