# 영속성 쿼리 패턴

Repository, SQL, JPQL, QueryDSL, JPA/Hibernate, 쿼리 성능 작업에서 이 자료를 사용한다.

## 쿼리 안전성

- parameter binding을 사용한다. 사용자 입력을 SQL, JPQL, QueryDSL expression, native query string, sort expression에 문자열 결합으로 넣지 않는다.
- table name, column name, sort field, filter key 같은 dynamic identifier는 allowlist로 제한한다.
- 보호 대상 row를 반환하기 전에 data access 또는 use-case logic에서 tenant/account/user ownership filter를 적용한다.

## 쿼리 형태

- 신규 Entity 관계는 객체 참조보다 scalar FK를 우선한다. `PostEntity.userId`, `CommentEntity.postId`처럼 외래키 값을 직접 두고 query boundary에서 명시 조인한다.
- `@ManyToOne`, `@OneToMany`, `@ManyToMany` 관계 어노테이션 탐색에 기대어 read model을 만들지 않는다. 필요한 데이터는 QueryDSL, SQL, JPQL, projection, explicit DTO mapping으로 가져온다.
- 다대다는 `@ManyToMany` 대신 연결 엔티티를 둔다. 예: `PostTagEntity(postId, tagId)`.
- collection read는 pagination 또는 명시적 limit으로 제한한다.
- request path에서 넓은 범위의 `findAll` 호출을 피한다.
- caller가 일부 column만 필요로 하면 projection을 우선한다.
- N+1 access를 피하기 위해 fetch join, entity graph, batch size, explicit query를 의도적으로 사용한다.
- DTO mapper, JSON serializer, log statement, loop에서 lazy loading이 트리거되지 않게 한다.

## Criteria와 Query 메시지 타입

- optional filter, sort, pagination, search condition에는 immutable `*Criteria`를 사용한다.
- caller가 특정 read model 또는 lookup flow를 요청한다면 read intent를 `*Query`로 표현한다.
- Criteria/Query에는 repository, QueryDSL builder, entity manager, authorization, transaction behavior를 넣지 않는다.
- request parameter를 Criteria/Query 객체로 변환할 때는 `from(request)`, `of(...)`, `create(...)` 같은 정적 팩토리를 우선한다.
- read-side Service 출력은 presentation mapping 전에 명시적인 `*Result` 타입으로 매핑한다.

## 인덱스와 실행 계획 확인

- 자주 쓰이는 filter, join, ordering, uniqueness check, foreign key에 필요한 index를 확인한다.
- leading wildcard search, indexed column에 대한 function, implicit cast, non-sargable predicate를 주의한다.
- 필요하고 index가 준비된 경우가 아니라면 hot path의 비싼 count를 피한다.

## 트랜잭션

- transaction은 use-case/service boundary에 둔다.
- remote call이나 느린 IO를 감싼 채 transaction을 오래 잡지 않는다.
- loop 안에서 row별 flush/write를 피한다. 안전하면 batch 처리한다.
- bulk update에서는 stale persistence context와 domain event consistency를 고려한다.

## Spring/JPA 참고

- local convention이 허용한다면 read use case에 `@Transactional(readOnly = true)`를 사용한다.
- 트랜잭션 경계 문제를 숨기기 위해 open-in-view에 의존하지 않는다.
- 관계 어노테이션은 legacy 호환 또는 명시 승인된 예외로 취급한다. 예외 사용 시 lazy loading, cascade, orphanRemoval, serializer 노출, test fixture 비용을 finding 후보로 검토한다.
- Kotlin/Java 코드에서는 쿼리 DTO, projection, enum, static helper를 본문에서 fully qualified name으로 쓰지 말고 파일 상단 import로 올린다. Java static member는 `import static`을 사용한다.
