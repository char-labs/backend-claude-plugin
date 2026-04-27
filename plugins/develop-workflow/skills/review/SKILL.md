---
name: review
description: 백엔드 코드를 architecture, SOLID/OOP, security, query bottleneck, application performance, missing tests 관점으로 종합 리뷰할 때 사용. 보안/성능/쿼리/OOP/Spring-Kotlin 단일 범위는 focused review skill을 우선 사용.
argument-hint: "[파일, diff, PR, 리뷰 범위]"
---

# 백엔드 품질 리뷰

## 설명

사용자 요청을 backend quality 관점으로 종합 리뷰한다. 넓은 조언보다 concrete evidence가 있는 finding을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- 객체지향 디자인 패턴이 핵심이면 `${CLAUDE_PLUGIN_ROOT}/references/oop-design-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- Repository/query code가 있으면 `${CLAUDE_PLUGIN_ROOT}/references/persistence-query-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- Spring/Kotlin/JPA/Gradle code가 있으면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- Spring/Kotlin coroutine/concurrency이면 `spring-coroutine-concurrency` skill 기준을 함께 적용한다.

## 실행 절차

1. 변경 범위와 user-facing behavior를 확인한다.
2. architecture boundary, dependency direction, transaction ownership, error boundary, testability를 확인한다.
3. OOP/SOLID 위반으로 coupling, hidden dependency, 테스트 난이도가 증가하는지 본다.
4. private method chain에 비즈니스 책임이 숨겨졌는지 확인한다. 이름 붙일 수 있는 행동은 역할 컴포넌트로 분리하는 fix를 우선 제안한다.
5. Facade/Service 경계를 확인한다. 복잡한 비즈니스 조합은 Facade, 단일 도메인 책임은 Service로 두며 Facade는 Service만 의존해야 한다.
6. 반복되는 private helper나 흩어진 메서드가 있으면 확장 함수 후보인지 확인한다. 순수 재사용 패턴이면 `common`/`support`/`util` 또는 도메인 support 패키지로 이동을 제안한다.
7. Kotlin idiom을 확인한다. scope function, exhaustive `when`, `is` smart cast, null-safety, collection operation으로 readability와 유지보수성이 좋아질 수 있는지 본다.
8. kt 파일의 여러 data class가 같은 컨텍스트인지 확인한다. nested command/info/result 또는 응답 wrapper + DTO는 허용하고, 독립 개념이면 분리를 제안한다.
9. `toDomain()` mapping을 확인한다. Entity/input model/command-like data class에서 domain model로 가는 순수 변환은 `toDomain()`으로 모이고, Service 내부 constructor 호출로 반복되지 않는지 본다.
10. 정적 팩토리와 message type을 확인한다. 의미 있는 생성은 `from`/`of`/`create`, Service 결과는 `*Result`, 입력 목적은 `*Command`/`*Query`/`*Criteria`로 드러나는지 본다.
11. 디자인 패턴 적용 여부를 확인한다. 반복 조건문은 Strategy/State/Specification, 안정된 워크플로우는 Template Method, 외부 provider는 Adapter/Port, 순차 검증은 Chain/Pipeline 후보인지 본다.
12. authn/authz, injection, SSRF, path traversal, secret handling, logging, crypto/token, CORS/CSRF, rate limit, supply-chain risk를 확인한다.
13. DB bottleneck을 확인한다: N+1, pagination/limit 누락, index 누락, non-sargable predicate, lock scope, batch behavior, transaction length.
14. application bottleneck을 확인한다: blocking IO, memory pressure, unbounded aggregation, cache stampede, timeout/retry 누락, expensive hot-loop work.
15. coroutine/concurrency를 확인한다: `Dispatchers.IO`, blocking call, unbounded `async`, `runBlocking`, cancellation, timeout, thread/memory tradeoff.
16. business rule, authorization boundary, failure mode, query behavior를 증명하는 test가 있는지 확인한다.

## 검증

- finding마다 재현 가능 증거, 영향, concrete fix, test expectation을 포함한다.
- 검증 명령은 repo에 이미 존재하는 도구를 기준으로 제안한다.

## 주의사항

- 실수 방지 가드레일: finding마다 재현 증거, concrete fix, test expectation이 없으면 심각도를 낮추거나 residual risk로 둔다.
- 심각도가 낮은 style preference로 high severity finding을 만들지 않는다.
- data class 파일 구성은 팀 컨벤션 영역이므로 같은 컨텍스트라면 지적하지 않는다. scan과 변경 영향이 나빠지는 경우에만 finding으로 올린다.
- Facade가 Service 외 의존성을 직접 받는 경우는 단순 style이 아니라 계층 경계 위험으로 본다.
- 확장 함수 추출은 중복과 call depth를 줄이는 경우에만 제안한다. 한 class에만 필요한 작은 helper는 private로 남겨도 된다.
- Kotlin idiom 제안은 가독성, 유지보수성, 재사용성이 실제로 좋아질 때만 한다. scope function 중첩으로 더 어려워지면 제안하지 않는다.
- 정적 팩토리, `*Result`, `*Command`, `*Query`, `*Criteria`는 layer ownership과 intent를 선명하게 할 때 finding으로 제안한다. 단순 취향 수준이면 낮은 severity로 둔다.
- `toDomain()`은 순수 mapping일 때만 권장한다. repository/client 호출, 인가, 트랜잭션, lazy association traversal을 포함하면 더 높은 위험으로 본다.
- 디자인 패턴 finding은 중복 분기, 변경 축, 테스트 어려움, layer boundary 문제처럼 concrete impact가 있을 때만 낸다. 패턴 이름만 붙이는 제안은 피한다.
- coroutine finding은 blocking 여부와 dispatcher 선택뿐 아니라 DB pool, external rate limit, cancellation, 메모리 영향까지 함께 본다.
- 보안은 “완전 보장”이 아니라 발견 가능한 위험을 낮추는 방식으로 표현한다.
- focused scope가 명확하면 `security-review`, `performance-review`, `persistence-query-review`, `oop-review`, `spring-kotlin-review`를 우선 고려한다.

## 출력

review finding template을 사용한다. findings first, severity 순서로 반환한다. blocking finding이 없으면 그렇게 말하고 residual risk 또는 validation gap을 남긴다.
