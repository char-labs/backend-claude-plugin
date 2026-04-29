# JPA BaseEntity Reference

## 적용 원칙

- BaseEntity는 JPA Entity 공통 superclass이며 domain model이 아니다.
- 위치는 `infrastructure`, `db-core`, `storage`, `persistence adapter` 같은 JPA 의존 모듈의 support package를 우선한다.
- Pida-Server 예시는 `com.pida.storage.db.core.support.BaseEntity`처럼 persistence module 안의 support package에 둔다.
- 프로젝트가 UUID나 assigned id를 명시하지 않았다면 신규 BaseEntity는 `GenerationType.IDENTITY`와 nullable `Long?` id를 우선한다.

## 권장 템플릿

```kotlin
package com.example.storage.persistence.support

import jakarta.persistence.Column
import jakarta.persistence.EntityListeners
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.MappedSuperclass
import org.hibernate.annotations.CreationTimestamp
import org.hibernate.annotations.UpdateTimestamp
import org.springframework.data.jpa.domain.support.AuditingEntityListener
import java.time.LocalDateTime

@MappedSuperclass
@EntityListeners(value = [AuditingEntityListener::class])
abstract class BaseEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long? = null

    @CreationTimestamp
    @Column(updatable = false)
    val createdAt: LocalDateTime = LocalDateTime.now()

    @UpdateTimestamp
    @Column
    var updatedAt: LocalDateTime? = null
        protected set

    @Column
    var deletedAt: LocalDateTime? = null
        protected set

    fun softDelete() {
        this.deletedAt = LocalDateTime.now()
    }

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is BaseEntity) return false
        if (this::class != other::class) return false
        if (id == null || other.id == null) return false
        return id == other.id
    }

    override fun hashCode(): Int = id?.hashCode() ?: 0
}
```

## Pida-Server식 변형 기준

- `@MappedSuperclass`와 `AuditingEntityListener`를 사용한다.
- `createdAt`은 `@CreationTimestamp`, `updatedAt`은 `@UpdateTimestamp`를 사용한다.
- `updatedAt`, `deletedAt` setter는 `protected set`으로 제한한다.
- `softDelete()`는 `deletedAt`만 갱신한다. cascade delete나 연관 그래프 삭제 책임을 숨기지 않는다.
- `equals`/`hashCode`는 persisted id 기반으로 제한한다.

## equals/hashCode 가드레일

- 제공 예시처럼 `kotlin.reflect.full.isSubclassOf`를 쓸 수는 있지만, 조건식이 같은 class에서 `false`를 반환하지 않는지 반드시 확인한다.
- `if (!this::class.isSubclassOf(other::class) || other::class.isSubclassOf(this::class)) return false` 형태는 같은 class끼리도 두 번째 조건이 true가 되어 동등성을 깨뜨릴 수 있다.
- kotlin-reflect 의존이 없다면 `this::class != other::class`처럼 단순 class 비교를 우선한다.
- Hibernate proxy까지 고려해야 하는 프로젝트라면 기존 프로젝트 convention을 먼저 따르고, 필요 시 `Hibernate.getClass(...)` 기반 비교를 검토한다.
- id가 null인 transient Entity끼리는 같지 않게 둔다. hashCode는 mutable business field를 쓰지 않는다.

## soft delete 체크리스트

- 모든 read query가 `deletedAt is null` 또는 프로젝트의 삭제 제외 convention을 적용한다.
- unique constraint, index, admin 복구, hard delete batch 정책을 확인한다.
- `softDelete()`만으로 repository 조회 정책이 자동 적용된다고 가정하지 않는다.
- domain 객체로 변환하는 `toDomain()`은 `deletedAt`을 domain에서 필요로 할 때만 포함하고, lazy association traversal을 하지 않는다.

## 리뷰 Finding 후보

- BaseEntity가 domain module/package에 존재한다.
- `@MappedSuperclass` 없이 단순 abstract class로 JPA id/auditing을 공유하려 한다.
- id 전략이 프로젝트 DB와 맞지 않는다.
- `createdAt`, `updatedAt`, `deletedAt`가 public mutable setter로 열려 있다.
- soft delete field는 있지만 repository/query에서 삭제 row 제외가 없다.
- `equals`가 같은 class와 같은 id에서 `false`가 된다.
- `hashCode`가 mutable timestamp/name/status를 사용한다.
