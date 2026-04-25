# Build Validation Reference

Use this reference for build, CI, generated source, dependency, and validation workflow decisions.

## Command Discovery

- Prefer project wrappers: `./gradlew`, `./mvnw`, repo scripts, package-manager scripts.
- Detect changed modules from paths and existing build files.
- Validate generated sources before dependent modules when protobuf/OpenAPI/schema generation changed.
- Do not install dependencies automatically. Recommend explicit commands only.

## JVM Backend Defaults

- Gradle compile: `./gradlew :module:compileKotlin` or `./gradlew :module:compileJava`.
- Tests: `./gradlew :module:test`.
- Kotlin lint/static analysis: `./gradlew ktlintCheck`, `./gradlew detekt`, or local equivalents when present.
- Protobuf: build the protobuf module before modules that consume generated stubs.

## Failure Triage

- Separate source compile errors, generated source errors, dependency resolution, test failure, lint/style, and environment failure.
- Report first failing module, first meaningful stack/error line, likely owner, and next command.
- If a command cannot run due environment or network limits, state the residual risk.
