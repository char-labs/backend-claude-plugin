---
name: jpa-base-entity
description: Spring/Kotlin JPA BaseEntity, @MappedSuperclass, AuditingEntityListener, GenerationType.IDENTITY id, createdAt/updatedAt/deletedAt, softDelete, equals/hashCode 기준을 프로젝트 persistence 모듈에 맞게 만들거나 리뷰할 때 사용. Pida-Server식 BaseEntity 구조를 참고하되 package와 auditing 방식은 프로젝트 convention에 맞춘다.
argument-hint: "[BaseEntity 작업]"
---

# JPA BaseEntity

## 설명

JPA Entity 공통 superclass를 infrastructure/db-core/persistence adapter에 작성하거나 리뷰한다. domain에는 BaseEntity를 두지 않고, JPA Entity만 BaseEntity를 상속한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/jpa-base-entity.md`
- `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 기존 persistence module, support/config package, JPA auditing 설정 여부를 확인한다.
2. BaseEntity 위치는 JPA Entity가 있는 infrastructure/db-core/persistence adapter 하위 support package로 둔다.
3. 기본 id 전략은 프로젝트가 다르게 정하지 않았다면 `@GeneratedValue(strategy = GenerationType.IDENTITY)`와 nullable `Long?` id를 우선한다.
4. 감사 필드는 `createdAt`, `updatedAt`, `deletedAt`를 둔다. `createdAt`은 생성 후 변경하지 않고, `updatedAt`/`deletedAt`은 외부 setter를 막는다.
5. 생성/수정 시간은 기존 convention에 맞춰 `@CreationTimestamp`/`@UpdateTimestamp` 또는 Spring Data auditing을 선택한다.
6. soft delete는 `softDelete()`가 `deletedAt = LocalDateTime.now()`를 설정하게 둔다. 실제 삭제 쿼리와 조회 필터는 repository/query 정책에서 별도로 확인한다.
7. `equals`/`hashCode`는 id가 null이면 동등하지 않게 하고, persisted id가 같을 때만 같게 한다.
8. 제공 예시의 `isSubclassOf` 조건을 그대로 복사하지 말고 같은 class/proxy 처리에서 항상 true가 되는지 검증한다.
9. Kotlin import는 파일 상단에 둔다. inline fully qualified name을 쓰지 않는다.
10. 가장 좁은 compile validation을 실행하거나 제안한다.

## 검증

- `./gradlew :{persistence-module}:compileKotlin`
- BaseEntity를 상속한 대표 Entity compile
- auditing 사용 시 `@EnableJpaAuditing` 또는 equivalent 설정 존재 여부

## 주의사항

- 실수 방지 가드레일: BaseEntity를 추가하면 위치, id 전략, auditing annotation, soft delete 조회 필터, equals/hashCode, compile validation을 함께 확인한다.
- BaseEntity는 domain model이 아니다. domain package/module에 두지 않는다.
- `deletedAt`만 추가하고 모든 조회에서 삭제 row를 제외하지 않으면 soft delete가 완성된 것이 아니다.
- `equals`가 같은 class와 같은 id에서 `true`가 되는지 확인한다. `!this::class.isSubclassOf(other::class) || other::class.isSubclassOf(this::class)` 같은 조건은 같은 class도 false가 될 수 있으므로 사용하지 않는다.
- `hashCode`는 mutable field를 사용하지 않는다. id 기반으로 제한한다.
- `LocalDateTime.now()`는 domain 생성 정책이 아니라 persistence timestamp default로만 사용한다.

## 출력

BaseEntity 위치, 코드 변경, 필요한 auditing 설정, soft delete 조회 필터 영향, 검증 명령을 요약한다.
