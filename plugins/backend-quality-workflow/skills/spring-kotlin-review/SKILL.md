---
name: spring-kotlin-review
description: Spring Security, JPA/Hibernate query behavior, transaction boundary, Gradle validation, Kotlin nullability, DTO/domain/entity separation, import style을 Spring/Kotlin 관점으로 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 엔드포인트, 모듈, 리뷰 범위]"
---

# Spring/Kotlin Backend Review

## 설명

`$ARGUMENTS`를 Spring/Kotlin 특화 관점으로 검토한다. 일반 리뷰보다 Spring Security, JPA/Hibernate, transaction, Gradle/Kotlin convention을 우선한다.

## 상세 자료

- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`

## 실행 절차

1. Spring Security를 확인한다: route protection, method security, ownership check, CSRF/CORS behavior, overly broad `permitAll`.
2. JPA/Hibernate를 확인한다: N+1, mapper/serializer/logging lazy loading, fetch join/entity graph/projection, bulk update, `open-in-view` reliance.
3. transaction을 확인한다: use-case ownership, `readOnly`, write boundary, transaction 내부 remote call, event consistency.
4. Kotlin을 확인한다: nullability contract, 불필요한 `!!`, immutable command/value object, executable code에서 inline fully qualified reference 대신 top-of-file import 사용.
5. Gradle validation을 확인한다: existing `./gradlew` task, scoped module test, ktlint/detekt 존재 여부, 자동 dependency 설치 금지.

## 검증

- 영향 module의 compile/test를 우선 제안한다.
- Spring/JPA 변경이면 repository slice 또는 integration test를 검토한다.
- Kotlin style은 ktlint/detekt가 있으면 해당 명령을 사용한다.

## 주의사항

- Spring annotation만 보고 보안/트랜잭션이 충분하다고 가정하지 않는다.
- Entity를 API response로 직접 노출하거나 lazy association을 serialization에 맡기지 않는다.
- import style은 프로젝트 지시대로 top-of-file import를 우선한다.

## 출력

review finding template을 사용한다. 각 finding에는 정확한 Spring/Kotlin mechanism을 포함해 fix가 바로 실행 가능하도록 한다.
