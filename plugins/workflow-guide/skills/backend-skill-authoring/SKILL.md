---
name: backend-skill-authoring
description: 백엔드 도메인 컨벤션 스킬 작성/개선 가이드. Entity, scalar FK, 관계 어노테이션 지양, 연결 엔티티, Repository, QueryDSL, GraphQL, gRPC, Gradle, 테스트, ADR 같은 프로젝트 전용 SKILL.md와 상세 reference를 만들거나 정리할 때 사용.
argument-hint: "[스킬로 만들 백엔드 컨벤션 또는 기존 SKILL.md]"
---

# 백엔드 스킬 작성

## 설명

사용자 요청을 백엔드 도메인 스킬로 정리하거나 기존 스킬을 개선할 때 사용한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/backend-skill-authoring-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/backend-domain-skill-template.md`

## 실행 절차

1. 만들 스킬의 사용 시점을 한 문장으로 확정한다.
2. `SKILL.md`에는 트리거 설명, 핵심 실행 절차, 검증, 주의사항만 둔다.
3. 긴 코드 예시, 상세 워크플로우, 프로젝트별 경로/카탈로그/예외 규칙은 `references/`로 분리한다.
4. description은 제목형보다 “언제 사용해야 하는지”가 드러나게 쓴다.
5. Kotlin/Spring/Java 스킬이라면 코드 본문/하단 영역의 inline FQCN 금지, 파일 상단 import, Java `import static`, 트랜잭션 경계, 보안/인가, 쿼리 병목, 테스트 명령을 포함한다.
6. 비즈니스 책임을 private method로 숨기지 않고 `UserCreator`, `PostDeleter` 같은 역할 컴포넌트로 드러내는 기준을 포함한다.
7. 복잡한 비즈니스 흐름은 Facade, 단일 도메인 책임은 Service로 나누고 Facade는 Service만 의존한다는 기준을 포함한다.
8. 반복될 Kotlin helper는 private method로 흩지 않고 `common`, `support`, `util` 또는 도메인 support 패키지의 확장 함수로 추출하는 기준을 포함한다.
9. scope function, `when`, `is` smart cast, null-safety, collection operation 같은 Kotlin idiom을 가독성/유지보수성 기준과 함께 포함한다.
10. companion object 정적 팩토리(`from`, `of`, `create`), `toDomain()` 순수 mapping, Service `*Result`, `*Command`, `*Query`, `*Criteria` 기준을 포함한다.
11. JPA Entity 스킬이면 관계 어노테이션보다 scalar FK를 우선하고, 다대다는 `@ManyToMany` 대신 연결 엔티티를 쓰는 기준을 포함한다.
12. 객체지향 디자인 패턴 기준을 포함한다: Strategy, Template Method, State, Specification/Policy, Adapter/Port, Decorator, Chain/Pipeline, Factory를 문제 축과 함께 설명한다.
13. coroutine 스킬이면 blocking 요소, dispatcher 선택, structured concurrency, bounded fan-out, thread/memory tradeoff를 포함한다.
14. kt 파일의 여러 data class는 기본 지양하되, 같은 부모 컨텍스트의 nested command/info/result 또는 응답 wrapper + DTO 예외를 명시한다.
15. Maum 같은 특정 프로젝트 규칙은 그대로 복사하지 말고 placeholder 또는 context pack 템플릿으로 일반화한다.

## 검증

- frontmatter에 `name`, `description`, 필요한 경우 `argument-hint`가 있는지 확인한다.
- description이 “언제 쓰는지”를 한글 키워드 중심으로 설명하는지 확인한다.
- `SKILL.md`가 너무 길면 상세 예시를 reference로 분리한다.

## 주의사항

- 실수 방지 가드레일: 새 스킬이나 에이전트를 추가하면 routing fixture, frontmatter 검증, 문서 정책 테스트를 함께 갱신한다.
- 특정 회사/서비스 경로, catalog, 정책은 범용 plugin에 직접 고정하지 않는다.
- 보안/인가, 쿼리 병목, 트랜잭션 경계, 검증 명령이 빠진 개발 스킬은 불완전한 것으로 본다.
- Entity 예시에는 `@ManyToOne`, `@OneToMany`, `@ManyToMany`, `JoinColumn` 관계 어노테이션을 기본값처럼 넣지 않는다. `userId`, `postId` 같은 scalar FK와 명시 조인/projection을 먼저 보여준다.
- 다대다 관계는 연결 엔티티로 설명한다. 관계 어노테이션 예시는 legacy/명시 승인 예외 섹션으로 분리한다.
- 역할 컴포넌트와 data class 파일 구성 규칙은 agent가 설계/구현/리뷰에서 사용할 수 있게 명시적으로 적는다.
- Facade/Service 분리 기준과 Facade 의존성 제한은 agent가 architecture boundary로 리뷰할 수 있게 적는다.
- 확장 함수 기준은 중복과 call depth를 줄이는 경우에만 적용한다. 비즈니스 정책이나 외부 의존성은 extension으로 숨기지 않는다.
- Kotlin idiom 기준은 scope function 과사용이 아니라 읽기 쉬운 분기, 변환, null 처리, 타입 처리를 만드는 방향으로 적는다.
- 정적 팩토리, `toDomain()`, `*Result`/`*Command`/`*Query`/`*Criteria` 기준은 생성 의도, layer ownership, validation 위치를 선명하게 만드는 방향으로 적는다.
- `toDomain()`은 순수 mapping으로 제한하고, repository/client 호출, 인가, 트랜잭션, lazy association traversal은 금지 조건으로 함께 적는다.
- 디자인 패턴 기준은 패턴 이름을 먼저 고르는 방식이 아니라 변경 축, 안정된 워크플로우, 생명주기 상태, provider 경계, 테스트 용이성 문제를 해결하는 방향으로 적는다.
- Template Method는 상속 hook이 필요한 안정된 생명주기에만 권장하고, 단순 변형은 Strategy나 composition을 우선하게 적는다.
- coroutine 기준은 적극 활용을 허용하되 `Dispatchers.IO` 남용, unbounded fan-out, blocking call 은닉을 방지하는 guardrail과 함께 적는다.
- 서브에이전트가 사용할 skill이면 `<!-- skill: skill-name -->` 힌트와 함께 직접 활성화할 수 있게 설명한다.

## 출력

새 스킬 구조, `SKILL.md` 초안, 필요한 reference 목록, 검증 방법을 함께 제시한다.
