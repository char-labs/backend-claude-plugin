# 백엔드 도메인 스킬 템플릿

아래 템플릿은 프로젝트 전용 백엔드 스킬을 만들 때 사용한다.

```markdown
---
name: {skill-name}
description: {언제 이 스킬을 써야 하는지 한 문장. 대상 작업, 트리거 키워드, 다른 스킬과의 경계를 포함한다.}
argument-hint: "[{작업 대상}]"
---

# {스킬 제목}

## 설명

{이 스킬이 해결하는 백엔드 작업을 2-3문장으로 설명한다.}

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `references/full-workflow.md`
- `references/examples.md`

## 실행 절차

1. 기존 유사 코드와 프로젝트 컨벤션을 먼저 확인한다.
2. 변경 대상 계층과 소유 책임을 정한다.
3. 보안/인가, 입력 검증, 트랜잭션, 쿼리 병목을 함께 확인한다.
4. 비즈니스 책임이 있는 행동은 private method로 숨기지 않고 역할 컴포넌트로 분리한다.
5. 복잡한 비즈니스 조합은 Facade, 단일 도메인 책임은 Service로 나누고 Facade는 Service만 의존하게 한다.
6. 여러 class에서 반복될 순수 helper는 private method로 흩어 두지 않고 확장 함수 후보로 분리한다.
7. Kotlin이면 scope function, `when`, `is` smart cast, null-safety, collection operation을 활용해 가독성과 재사용성을 높인다.
8. 생성 의도나 invariant가 있는 객체는 companion object 정적 팩토리(`from`, `of`, `create`)를 우선한다.
9. Entity/input model/command-like data class에서 domain model로 가는 순수 변환은 `toDomain()`으로 모은다.
10. Service/use-case 결과는 `*Result`, 입력 목적은 `*Command`, `*Query`, `*Criteria`로 분리한다.
11. 반복 분기, provider 선택, 상태별 행위, 워크플로우 골격이 있으면 Strategy, Template Method, State, Specification/Policy, Adapter/Port, Chain/Pipeline 등 필요한 디자인 패턴을 검토한다.
12. coroutine/concurrency가 있으면 blocking 요소, dispatcher, structured concurrency, bounded fan-out, thread/memory tradeoff를 확인한다.
13. 프로젝트 컨벤션에 맞게 구현 또는 설계를 작성한다.
14. 집중 테스트와 최소 검증 명령을 수행한다.

## 위치/명명 규칙

| 대상 | 위치 | 이름 규칙 |
|---|---|---|
| 엔티티 | `{module}/src/main/kotlin/.../entity/` | `{Domain}Entity` |
| 리포지토리 | `{module}/src/main/kotlin/.../repository/` | `{Domain}Repository` |
| 서비스/유스케이스 | `{module}/src/main/kotlin/.../service/` | `{Domain}Service` |
| 파사드 | `{module}/src/main/kotlin/.../facade/` | `{Flow}Facade` 또는 `{Domain}Facade` |
| 역할 컴포넌트 | `{module}/src/main/kotlin/.../{domain}/` | `{Domain}{Actioner}` 예: `UserCreator`, `PostDeleter` |
| Command | `{module}/src/main/kotlin/.../{domain}/` 또는 application input package | `{Action}{Domain}Command` 또는 `{Domain}{Action}Command` |
| Query | `{module}/src/main/kotlin/.../{domain}/` 또는 application input package | `{Domain}{Action}Query` |
| Criteria | `{module}/src/main/kotlin/.../{domain}/` 또는 query package | `{Domain}Criteria` 또는 `{Domain}{Search}Criteria` |
| Result | `{module}/src/main/kotlin/.../{domain}/` 또는 application output package | `{Domain}{Action}Result` |
| 확장 함수 | `{module}/src/main/kotlin/.../common/`, `support/`, `util/` 또는 도메인 support | `{Type}Extensions.kt` 또는 `{Domain}Extensions.kt` |

## 검증

```bash
./gradlew :{module}:compileKotlin
./gradlew :{module}:test
```

## 주의사항

- 요청 원문, `$ARGUMENTS`, 날짜, 개인 로컬 절대경로처럼 호출마다 달라지는 값은 `SKILL.md` 앞쪽에 넣지 않는다.
- 실수 방지 가드레일: 변경이 routing, hook, fixture, 문서 정책에 영향을 주면 관련 회귀 테스트와 정책 테스트를 함께 갱신한다.
- Kotlin/Java 코드는 본문/하단 영역에 `com.example.Foo` 같은 fully qualified reference를 직접 쓰지 않고 파일 상단 import를 우선한다. Java static member는 `import static`을 사용한다.
- `private`는 정말 내부적인 작은 세부 구현에만 사용한다. 이름 붙일 수 있는 비즈니스 행동은 역할 컴포넌트로 추출한다.
- Facade는 여러 Service를 조합하는 계층으로만 사용한다. Facade에는 Service만 주입하고 Repository, EntityManager, client, mapper, port를 직접 주입하지 않는다.
- 단일 도메인 책임은 Facade가 아니라 Service에 둔다.
- 확장 함수는 여러 class에서 반복될 순수 변환/포맷팅/collection/null-safety helper에 사용한다. 의존성, IO, transaction, authorization, business policy를 숨기지 않는다.
- scope function은 의도별로 사용한다. `apply`는 설정, `also`는 side effect checkpoint, `let`은 nullable/변환, `run`은 계산, `with`는 receiver grouping에 쓴다.
- `when`은 enum/sealed/status/type 분기를 표현하고, `is` smart cast로 안전한 타입 분기를 작성한다.
- 정적 팩토리는 생성 의도, mapping, 기본값, invariant가 있는 경우 적극 사용한다. 단순 값 보관용 constructor까지 기계적으로 감싸지는 않는다.
- `toDomain()`은 현재 객체 값만 사용하는 순수 mapping에만 사용한다. repository/client 호출, 인가, 트랜잭션, lazy association traversal, 외부 ID/clock 호출이 필요하면 Service나 factory로 이동한다.
- Service는 entity, response DTO, primitive bundle, `Pair`/`Triple` 대신 명시적인 `*Result`를 반환하도록 작성한다.
- `Command`, `Query`, `Criteria`, `Result`는 immutable로 두고 API request/response DTO나 persistence entity와 겸용하지 않는다.
- 디자인 패턴은 variation point와 테스트 가능성이 있을 때만 적용한다. 단일 구현 interface, 불필요한 abstract class, 테스트되지 않은 pipeline, 숨겨진 decorator side effect를 피한다.
- Template Method는 안정된 생명주기 골격에만 사용한다. 단순 변형은 Strategy나 역할 컴포넌트 조합을 우선한다.
- coroutine에서는 `Dispatchers.IO`를 blocking 격리 수단으로만 사용하고, `coroutineScope`/`supervisorScope`/bounded `async`를 실패 전파와 리소스 제한 기준에 맞게 선택한다.
- kt 파일에 독립적인 public data class를 여러 개 두는 것을 지양한다. 같은 부모 컨텍스트의 nested command/info/result 또는 응답 wrapper + DTO만 예외로 허용한다.
- 민감정보 로그, 권한 누락, 무제한 쿼리, N+1을 기본 위험으로 본다.
- 상세 예시는 별도 상세 자료에 둔다.
```
```

## 상세 자료 템플릿

`references/full-workflow.md`는 다음 구조를 권장한다.

```markdown
# {스킬 제목} 상세 워크플로우 자료

## 1. 설계 상세

## 2. 구현 패턴

## 3. 에러 처리

## 4. 트랜잭션/성능 패턴

## 5. 테스트/검증

## 6. 안티패턴
```
