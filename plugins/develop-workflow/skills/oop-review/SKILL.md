---
name: oop-review
description: 백엔드 코드의 class responsibility, dependency direction, abstraction, domain modeling, cohesion, coupling, testability를 OOP/SOLID 관점으로 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 클래스, 모듈, 리뷰 범위]"
---

# OOP/SOLID 리뷰

## 설명

사용자 요청을 유지보수 가능한 객체지향 백엔드 설계 관점으로 검토한다. 구조 변경 제안은 구체적 correctness, testability, coupling 영향이 있을 때만 낸다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/references/oop-design-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- JVM/Spring/Kotlin 코드면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. class responsibility와 cohesion을 확인한다. validation, authorization, orchestration, persistence, mapping, IO, response formatting이 이유 없이 한 class에 섞이면 표시한다.
2. dependency inversion을 확인한다. 고수준 정책이 concrete infrastructure에 직접 묶여 testability를 해치면 port/interface를 검토한다.
3. interface size와 substitutability를 확인한다. 구현체는 contract, nullability, error behavior, side effect를 지켜야 한다.
4. domain model 표현력을 확인한다. business invariant가 controller, mapper, repository에 흩어져 있으면 찾는다.
5. private method chain이 별도 책임을 숨기는지 확인한다. 회원 생성, 글 삭제, 쿠폰 발급처럼 이름 붙일 수 있는 행동은 `UserCreator`, `PostDeleter`, `CouponIssuer` 같은 컴포넌트로 드러내는 편을 우선한다.
6. Facade/Service 경계를 확인한다. 복잡한 비즈니스 흐름은 Facade, 단일 도메인 책임은 Service가 맡고, Facade는 Service만 의존해야 한다.
7. 반복되는 private helper나 흩어진 메서드가 call depth를 늘리는지 확인한다. 순수 재사용 패턴이면 공용/도메인 확장 함수로 추출하는 fix를 제안한다.
8. Kotlin idiom을 확인한다. scope function, `when`, `is` smart cast, collection operation으로 더 명확해지는 Java식 분기/변환/타입 처리가 있는지 본다.
9. kt 파일의 여러 data class가 서로 다른 컨텍스트를 섞는지 확인한다. 같은 부모 컨텍스트의 nested type 또는 응답 wrapper + DTO는 허용하되, 독립 개념이면 파일을 분리하도록 제안한다.
10. 정적 팩토리와 application message type을 확인한다. 생성 의도는 `from`/`of`/`create`로 드러내고, Service 결과는 `*Result`, write/read/filter 입력은 `*Command`/`*Query`/`*Criteria`로 분리하는지 본다.
11. 디자인 패턴 후보를 확인한다: Strategy, Template Method, State, Specification/Policy, Adapter/Port, Decorator, Chain/Pipeline, Factory, Command Handler가 변경 축과 테스트 가능성을 개선하는지 본다.
12. testability를 확인한다. 핵심 동작은 network, wall clock, random ID, real DB 없이 검증 가능한지 본다.

## 검증

- 제안한 리팩터가 기존 테스트로 보호되는지 확인한다.
- 테스트가 없으면 최소 unit 또는 slice test를 제안한다.

## 주의사항

- 실수 방지 가드레일: 리팩터 제안은 테스트 가능성과 회귀 검증 방법이 있을 때 우선순위를 높인다.
- 추상화는 실제 중복, 변경 가능성, 테스트 장벽을 줄일 때만 제안한다.
- 광범위한 architecture rewrite보다 국소적인 책임 분리를 우선한다.
- `private` 자체를 금지하지 않는다. 다만 private가 비즈니스 책임을 숨기거나 테스트 가능한 협력자를 가리는 경우 finding으로 본다.
- Facade가 Repository, client, mapper, port를 직접 의존하면 layer boundary finding으로 본다.
- 확장 함수가 의존성, IO, transaction, authorization, business policy를 숨기면 finding으로 본다.
- scope function 과사용도 finding이 될 수 있다. 중첩 receiver, 모호한 `it`, side effect가 숨겨지는 chain은 명시적 코드가 낫다.
- 정적 팩토리나 `*Result`/`*Command`/`*Query`/`*Criteria` 제안은 생성 의도, layer ownership, 테스트 가능성이 실제로 좋아지는 경우에 우선한다.
- Strategy는 열린 변경 축에, Template Method는 안정된 워크플로우 골격에, State는 생명주기 상태 행위에, Specification/Policy는 이름 붙일 비즈니스 조건에 우선 고려한다.
- 디자인 패턴 과잉 설계를 finding으로 볼 수 있다. 단일 구현 interface, 불필요한 abstract class, 테스트되지 않은 pipeline 순서, 숨겨진 decorator side effect를 확인한다.

## 출력

구체적 maintainability, correctness, testability impact가 있는 finding만 반환한다.
