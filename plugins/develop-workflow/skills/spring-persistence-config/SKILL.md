---
name: spring-persistence-config
description: Spring/Kotlin 프로젝트에서 DataSourceConfig, JpaConfig, HikariConfig, ConfigurationProperties, EntityScan, EnableJpaRepositories, Flyway, datasource yml/profile/env 설정을 프로젝트 모듈명과 package root에 맞게 만들거나 리뷰할 때 사용. Pida-Server식 db-core 구조를 참고하되 db-core, db.core 이름을 강제하지 않는다.
argument-hint: "[Spring persistence 설정 작업]"
---

# Spring Persistence Config

## 설명

Spring/Kotlin persistence 모듈의 DataSource/JPA/Flyway 설정 클래스와 yml 설정을 프로젝트 성격에 맞게 작성하거나 리뷰한다. `db-core`, `db.core` 같은 이름은 예시일 뿐이며, 기존 모듈명, package root, datasource prefix, profile convention을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/spring-persistence-config.md`
- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- 검증 명령이 필요하면 `${CLAUDE_PLUGIN_ROOT}/references/build-validation.md`

## 실행 절차

1. Gradle/Maven module, package root, existing `application*.yml`, `bootstrap*.yml`, config class, profile naming, Flyway dependency와 `spring.flyway.*` 설정을 먼저 확인한다.
2. persistence owner module을 정한다. JPA Entity가 있는 infrastructure/db-core/persistence adapter 모듈에 설정을 둔다.
3. datasource prefix를 프로젝트 이름에 맞게 정한다. 예: `datasource.core`, `datasource.db.member`, `storage.datasource.main`.
4. `HikariConfig` bean은 `@ConfigurationProperties(prefix = "...")`로 yml과 바인딩한다.
5. `DataSource` bean 이름, `@Qualifier`, transaction manager/entity manager factory가 있으면 기존 naming convention과 충돌하지 않게 맞춘다.
6. `@EntityScan`과 `@EnableJpaRepositories`의 `basePackages`는 실제 Entity/JpaRepository package root를 가리키게 한다. `domain` package를 scan 대상에 넣지 않는다.
7. yml은 profile별 값과 공통 JPA property를 분리하고, JDBC URL/username/password는 환경변수 placeholder로만 둔다.
8. `spring.jpa.open-in-view: false`, batch fetch size, dialect, ddl-auto 정책을 환경별 risk에 맞게 명시한다.
9. Flyway를 쓰면 `enabled`, `locations`, `baseline-on-migrate`, `validate-on-migrate`, `clean-disabled`, datasource/schema/table 대상을 함께 확인한다. 여러 datasource면 migration target이 의도한 datasource인지 명시한다.
10. 신규 설정이 repository port/CoreRepository 정책과 충돌하지 않는지 확인한다. Service/use-case에는 `*Repository` 포트만 보이게 한다.
11. 가장 좁은 compile/config validation을 실행하거나 제안한다.

## 검증

- Kotlin compile: `./gradlew :{module}:compileKotlin`
- Spring context test가 있으면 해당 모듈의 가장 좁은 test task
- yml 변경은 profile별 placeholder, secret 노출, prefix와 `@ConfigurationProperties`, `spring.flyway.*` 일치를 확인
- Flyway 설정 변경은 migration script path가 runtime classpath에 포함되는지, 운영 profile에서 `clean-disabled: true`와 `validate-on-migrate: true`가 유지되는지 확인

## 주의사항

- 실수 방지 가드레일: 설정 클래스와 yml을 추가하면 prefix, bean name, package scan, profile, env var, 검증 명령을 한 세트로 확인한다.
- `db-core`, `db.core`, `coreDataSource` 같은 이름을 그대로 복사하지 않는다. 프로젝트 모듈명과 bounded context에 맞게 바꾼다.
- password, token, JDBC URL 실값을 커밋하지 않는다. yml에는 `${ENV_NAME}` placeholder만 둔다.
- `show-sql`, `format_sql`, `ddl-auto`는 prod에서 위험할 수 있으므로 환경별 차이를 확인한다.
- Flyway의 `baseline-on-migrate`, `out-of-order`, `clean`은 운영에서 위험할 수 있다. destructive DDL, backfill, rollout/rollback 판단이 필요하면 `migration-adr`로 분리한다.
- `@EntityScan`이 domain package까지 넓게 잡히면 JPA Entity/domain 경계가 무너진 것으로 본다.
- `@EnableJpaRepositories`는 Spring Data `*JpaRepository`가 있는 infrastructure package를 대상으로 하고, domain `*Repository` 포트를 대상으로 삼지 않는다.
- 여러 datasource면 bean name, `@Primary`, transaction manager, entity manager factory, Flyway 대상 datasource/schema/table을 명시한다.

## 출력

생성/수정할 설정 클래스, yml prefix/profile, scan package, Flyway locations/target, env var 목록, 검증 명령, 남은 설정 리스크를 요약한다.
