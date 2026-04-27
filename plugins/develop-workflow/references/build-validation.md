# 빌드 검증 참고 자료

build, CI, generated source, dependency, validation workflow 결정을 할 때 이 자료를 사용한다.

## 명령 탐색

- `./gradlew`, `./mvnw`, repo script, package-manager script 같은 project wrapper를 우선한다.
- path와 기존 build file을 기준으로 변경된 module을 감지한다.
- protobuf/OpenAPI/schema generation이 변경되면 dependent module보다 generated source를 먼저 검증한다.
- dependency를 자동 설치하지 않는다. 명시적 command만 추천한다.

## JVM 백엔드 기본값

- Gradle compile: `./gradlew :module:compileKotlin` 또는 `./gradlew :module:compileJava`.
- 테스트: `./gradlew :module:test`.
- Kotlin lint/static analysis: 존재한다면 `./gradlew ktlintCheck`, `./gradlew detekt`, 또는 local equivalent.
- Protobuf: generated stub을 소비하는 module보다 protobuf module을 먼저 build한다.

## 실패 분류

- source compile error, generated source error, dependency resolution, test failure, lint/style, environment failure를 구분한다.
- 첫 실패 module, 의미 있는 첫 stack/error line, likely owner, 다음 command를 보고한다.
- 환경 또는 network limit 때문에 command를 실행할 수 없으면 residual risk를 명시한다.
