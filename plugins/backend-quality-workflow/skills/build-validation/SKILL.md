---
name: build-validation
description: Gradle, Maven, CI 실패, dependency 변경, compile/test 실패, protobuf/generated source, lint, static analysis, scoped command 검증을 진단하거나 계획할 때 사용.
argument-hint: "[빌드, CI, 검증 작업]"
---

# Build Validation

## 설명

`$ARGUMENTS`가 build, test, generated source, dependency, CI validation과 관련될 때 사용한다. Gradle/Maven, protobuf generation, lint/static analysis, compile/test failure를 다룬다.

## 상세 자료

- `${CLAUDE_PLUGIN_ROOT}/references/build-validation.md`
- Gradle/Kotlin/Spring 프로젝트면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. build file, wrapper, module, generated-source task, existing script를 확인한다.
2. 실패 유형을 분류한다: dependency resolution, source compile, generated source, test, lint/static analysis, environment, CI-only.
3. 가장 좁은 관련 명령부터 실행하거나 제안한다.
4. protobuf/API generation 변경이면 consumer module보다 generator module을 먼저 검증한다.
5. 도구를 자동 설치하지 않고, 필요한 추가 도구는 근거와 함께 제안한다.

## 검증

- JVM 기본: `./gradlew :{module}:compileKotlin`, `./gradlew :{module}:test`
- Proto 기본: `./gradlew :protobuf:build` 후 소비 모듈 검증

## 주의사항

- 첫 번째 의미 있는 실패를 기준으로 원인을 좁힌다.
- 환경/네트워크 제약으로 실행 불가하면 residual risk를 명시한다.

## 출력

첫 실패 모듈, 가능성 높은 원인, 명령 증거, 다음 검증 명령을 요약한다.
