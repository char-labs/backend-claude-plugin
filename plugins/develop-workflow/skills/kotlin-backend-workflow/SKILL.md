---
name: kotlin-backend-workflow
description: Kotlin/JVM 또는 Spring Kotlin 백엔드에서 idiomatic Kotlin, nullability, scope function, sealed/value/data class, extension function, coroutine/Flow, Gradle module validation을 설계·구현·리뷰할 때 사용. 순수 coroutine 동시성은 spring-coroutine-concurrency, Spring/JPA 리뷰는 spring-kotlin-review, 빌드 실패 분석은 build-validation을 우선 고려한다.
argument-hint: "[Kotlin 설계, 구현, 리뷰, 검증 작업]"
---

# Kotlin 백엔드 워크플로우

## 설명

Kotlin/JVM 또는 Spring Kotlin 백엔드 작업에서 Kotlin 언어 기능, coroutine/reactive 흐름, Gradle 검증 범위를 기존 코드베이스 관례에 맞춰 결정한다. 특정 프로젝트 이름이나 모듈 규칙을 전제하지 않고, 저장소에서 발견한 module layout과 build convention을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- `${CLAUDE_PLUGIN_ROOT}/references/build-validation.md`
- coroutine/concurrency가 핵심이면 `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- Spring/JPA 계층 경계가 포함되면 `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- 리뷰 finding을 작성하면 `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`

## 실행 절차

1. `settings.gradle.kts`, `build.gradle.kts`, module directory, source/test layout, ktlint/detekt/test convention을 먼저 확인한다.
2. Kotlin nullability를 contract로 사용하고, 불필요한 `!!`, unsafe cast, Java식 null/branch 처리를 줄인다.
3. scope function은 의도별로 사용한다: `apply`는 설정, `also`는 side-effect checkpoint, `let`은 nullable/짧은 변환, `run`은 receiver computation, `with`는 기존 receiver 묶음에 사용한다.
4. enum/sealed/status/type 분기는 가능한 exhaustive `when`과 `is` smart cast로 표현한다.
5. sealed class/interface, enum, value class, data class, extension function은 domain state와 call-site intent를 선명하게 만들 때만 도입한다.
6. extension function은 작고 stateless하며 dependency-free하게 유지한다. authorization, transaction, repository/client 호출, business policy는 Service나 역할 컴포넌트가 소유한다.
7. coroutine, Flow, StateFlow/SharedFlow, reactive pipeline은 cancellation, timeout, backpressure/state ownership, dispatcher 선택, thread/memory tradeoff를 함께 검토한다.
8. blocking IO는 가장 좁은 구간만 `Dispatchers.IO`로 격리하고, true suspend/non-blocking client 주변에서는 불필요한 dispatcher switch를 피한다.
9. Kotlin/Java에서는 코드 본문이나 하단 영역에 inline fully qualified reference를 쓰지 말고, 가능한 경우 파일 상단 import로 올린다. Java static member는 `import static`을 사용한다.
10. Kotlin 테스트 파일을 변경했으면 편집 파일에서 root 방향으로 가장 가까운 Gradle module을 추정해 `./gradlew :{module}:compileTestKotlin` 같은 좁은 validation을 우선한다.
11. build task가 불명확하면 자동 실행하지 말고, 발견한 wrapper/module 근거와 함께 후보 명령을 제안한다.

## 검증

- Kotlin compile: `./gradlew :{module}:compileKotlin`
- Kotlin test source compile: `./gradlew :{module}:compileTestKotlin`
- 동작 검증: `./gradlew :{module}:test`
- style/static analysis: 존재하면 `./gradlew ktlintCheck`, `./gradlew detekt`, 또는 repository-local equivalent

## 주의사항

- 실수 방지 가드레일: Kotlin 언어 기능은 가독성, null-safety, domain intent, 테스트 가능성이 실제로 좋아질 때만 사용한다.
- 프로젝트 고유 module prefix나 repository name을 전제하지 않는다.
- dependency나 plugin을 자동 설치하지 않는다. 필요하면 근거와 함께 제안한다.
- coroutine 도입은 성능 보장 장치가 아니다. blocking 여부, DB connection pool, external rate limit, cancellation, timeout을 함께 확인한다.
- 단순 DTO, 상수, 설정 이름 변경에는 새 테스트를 억지로 만들지 않고 compile/static validation을 우선한다.

## 출력

Kotlin 관점의 결정, 적용한 idiom 또는 피한 idiom, 선택한 Gradle 검증 범위, 수행/제안한 검증 명령, 남은 risk를 간결하게 보고한다.
