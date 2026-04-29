# Spring Persistence Config Reference

## 적용 원칙

- 이 문서는 Pida-Server식 `DataSourceConfig`, `JpaConfig`, yml 구성을 일반화한 기준이다.
- `db-core`, `db.core`, `core`는 예시 이름이다. 실제 프로젝트의 module name, package root, bounded context, datasource purpose에 맞게 바꾼다.
- 설정은 JPA Entity와 `*JpaRepository`가 있는 infrastructure/db-core/persistence adapter 모듈에 둔다. domain module에는 JPA 설정, `@EntityScan`, `@EnableJpaRepositories`, DataSource bean을 두지 않는다.
- yml의 민감 값은 환경변수 placeholder로만 둔다. 실제 JDBC URL, username, password, token을 커밋하지 않는다.
- Flyway/Liquibase 같은 migration tool이 있으면 DataSource/JPA 설정과 함께 migration datasource, locations, schema/table, baseline, validation 정책을 맞춘다. 실제 스키마 변경 전략, backfill, rollout/rollback 계획은 `migration-adr` 범위로 분리한다.

## 조사 순서

1. `settings.gradle*`, `build.gradle*`, module directory를 확인한다.
2. `src/main/kotlin`의 package root와 config package convention을 확인한다.
3. 기존 `application.yml`, `application-*.yml`, module-specific yml, config import convention을 확인한다.
4. Entity package, `*JpaRepository` package, `*CoreRepository` package를 확인한다.
5. datasource가 하나인지 여러 개인지 확인한다.
6. profile 이름(`local`, `dev`, `prod`, `test`)과 secret 주입 방식을 확인한다.
7. Flyway/Liquibase dependency, `spring.flyway.*` 또는 custom Flyway bean, migration script path(`db/migration` 등), baseline/validate/clean 정책을 확인한다.

## DataSourceConfig 패턴

```kotlin
package com.example.storage.persistence.config

import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import org.springframework.beans.factory.annotation.Qualifier
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
internal class PersistenceDataSourceConfig {
    @Bean
    @ConfigurationProperties(prefix = "datasource.persistence.main")
    fun persistenceHikariConfig(): HikariConfig = HikariConfig()

    @Bean
    fun persistenceDataSource(
        @Qualifier("persistenceHikariConfig") config: HikariConfig,
    ): HikariDataSource = HikariDataSource(config)
}
```

선택 기준:

- prefix는 `datasource.{context}`, `datasource.db.{context}`, `storage.datasource.{context}` 중 프로젝트 yml convention과 가장 가까운 형태를 쓴다.
- bean name은 context를 드러낸다. 예: `memberDataSource`, `paymentDataSource`, `coreDataSource`.
- datasource가 하나뿐이면 `@Primary`가 불필요할 수 있다. 여러 개면 `@Primary`, transaction manager, entity manager factory 이름을 명시한다.
- `internal` 사용 여부는 기존 Kotlin config class convention을 따른다.

## JpaConfig 패턴

```kotlin
package com.example.storage.persistence.config

import org.springframework.boot.autoconfigure.domain.EntityScan
import org.springframework.context.annotation.Configuration
import org.springframework.data.jpa.repository.config.EnableJpaRepositories
import org.springframework.transaction.annotation.EnableTransactionManagement

@Configuration
@EnableTransactionManagement
@EntityScan(
    basePackages = [
        "com.example.storage.persistence",
    ],
)
@EnableJpaRepositories(
    basePackages = [
        "com.example.storage.persistence",
    ],
)
class PersistenceJpaConfig
```

검토 기준:

- `basePackages`는 JPA Entity와 Spring Data `*JpaRepository`가 있는 infrastructure package root를 가리킨다.
- `domain`, `application`, `api`, `presentation` package를 넓게 scan하지 않는다.
- repository port인 `*Repository`가 domain/application에 있다면 `@EnableJpaRepositories` 대상이 아니다.
- multi datasource면 단순 `@EnableJpaRepositories`만으로 충분하지 않을 수 있다. `entityManagerFactoryRef`, `transactionManagerRef`, `basePackages`를 datasource별로 분리한다.

## yml 패턴

```yaml
spring:
  jpa:
    open-in-view: false
    properties:
      hibernate:
        default_batch_fetch_size: 100
    hibernate:
      ddl-auto: ${SPRING_JPA_HIBERNATE_DDL_AUTO:validate}
    database-platform: org.hibernate.dialect.PostgreSQLDialect
  flyway:
    enabled: ${SPRING_FLYWAY_ENABLED:true}
    locations: classpath:db/migration
    baseline-on-migrate: ${SPRING_FLYWAY_BASELINE_ON_MIGRATE:false}
    validate-on-migrate: true
    clean-disabled: true

---
spring:
  config:
    activate:
      on-profile: local
datasource:
  persistence:
    main:
      driver-class-name: org.postgresql.Driver
      jdbc-url: ${DATASOURCE_PERSISTENCE_MAIN_JDBC_URL}
      username: ${DATASOURCE_PERSISTENCE_MAIN_USERNAME}
      password: ${DATASOURCE_PERSISTENCE_MAIN_PASSWORD}
      pool-name: persistence-main-pool
      maximum-pool-size: 10
      connection-timeout: 1500
      keepalive-time: 30000
      validation-timeout: 1000
      max-lifetime: 600000
```

## Flyway 마이그레이션 설정

- 단일 datasource이고 Spring Boot auto-configuration을 쓰면 `spring.flyway.*`와 primary `DataSource` 연결이 의도와 맞는지 확인한다.
- 여러 datasource면 Flyway가 어떤 datasource/schema에 실행되는지 명시한다. 필요하면 `@FlywayDataSource`, custom `Flyway` bean, 또는 `spring.flyway.url`/`user`/`password` 환경변수 placeholder를 사용한다.
- `locations`는 실제 runtime classpath에 포함되는 module resource path와 맞춘다. 예: `classpath:db/migration`, `classpath:db/migration/core`.
- 운영 profile에서는 `clean-disabled: true`, `validate-on-migrate: true`를 기본값으로 둔다. `baseline-on-migrate`와 `out-of-order`는 기존 DB 도입/운영 절차가 명확할 때만 켠다.
- migration script는 `V{version}__{description}.sql` 같은 기존 convention을 따른다. repeatable migration이나 placeholder를 쓰면 owner와 재실행 영향을 명시한다.
- test profile은 실 DB나 공유 개발 DB에 migration을 실행하지 않게 별도 datasource 또는 container/local fixture convention을 확인한다.
- destructive DDL, 대량 backfill, 장시간 lock 가능성이 있으면 이 문서에서 즉시 구현하지 말고 `migration-adr`로 rollout/rollback, lock, 배치 크기, 관측 지표를 먼저 정한다.

환경별 기준:

- `local`: 개발 편의 설정은 허용하되 실제 secret은 env/local secret file로 둔다.
- `dev`: 운영과 비슷한 pool/timeouts를 쓰되 관측 가능한 로그 정책을 둔다.
- `prod`: `show-sql`, `format_sql`, broad logging, `ddl-auto: update/create`를 피한다.
- `test`: 실 DB 접근이 기본값이 되지 않게 별도 test datasource 또는 slice test convention을 확인한다.

## 체크리스트

- `ConfigurationProperties` prefix와 yml path가 정확히 일치한다.
- profile별 datasource 설정이 같은 key shape를 유지한다.
- secret 실값이 없다.
- `open-in-view: false`가 명시되어 있다.
- dialect와 driver가 실제 DB와 맞는다.
- prod `ddl-auto`가 안전하다.
- Flyway를 사용한다면 `spring.flyway.enabled`, `locations`, `baseline-on-migrate`, `validate-on-migrate`, `clean-disabled`가 profile별 의도와 맞는다.
- multi datasource에서 Flyway target datasource/schema/table이 JPA datasource와 충돌하지 않는다.
- migration script path가 runtime classpath에 포함되고 파일명 convention이 기존 프로젝트와 맞는다.
- `EntityScan`이 infrastructure package만 가리킨다.
- `EnableJpaRepositories`가 `*JpaRepository` package만 가리킨다.
- JPA Entity는 infrastructure/db-core/persistence adapter에 있고 domain은 순수 data class를 유지한다.
- `*CoreRepository`가 JPA 세부 구현을 감싸고 Service/use-case는 `*Repository` 포트만 본다.
