# 객체지향 디자인 패턴

명시적 디자인 패턴이 도움이 되는 객체지향 백엔드 코드를 설계, 구현, 리뷰할 때 이 자료를 사용한다.

## 선택 규칙

- 변경 축, 생명주기, 소유권, 테스트 용이성 문제에서 출발한다. 이름이 익숙하다는 이유만으로 패턴을 도입하지 않는다.
- repository에 명확한 기존 접근법이 있으면 local convention을 우선한다.
- 흩어진 conditional을 제거하거나, 변경 축을 격리하거나, domain language를 선명하게 하거나, 동작을 테스트하기 쉬워질 때 interface, abstract class, pattern structure를 도입한다.
- 안정적인 단일 구현 주변에 파일만 늘리는 패턴을 피한다. 단순 function, role component, sealed type, exhaustive `when`으로 충분할 수 있다.
- 패턴 경계는 layer를 위반하면 안 된다. repository, client, transaction, authorization은 각자의 owning layer에 남아야 한다.

## 권장 패턴

| 패턴 | 사용할 때 | 피할 때 |
|---|---|---|
| Strategy | domain condition에 따라 여러 policy, calculation, routing rule, validator, algorithm이 교체 가능하게 달라질 때 | 구현이 하나뿐이고 실제 variation이 예상되지 않을 때 |
| Template Method | 워크플로우 골격은 안정적이지만 일부 step만 subclass에서 달라질 때 | composition이 variation을 더 단순히 표현하거나 inheritance가 취약한 protected hook을 만들 때 |
| Static Factory Method | construction에 mapping, default value, invariant, naming value, 여러 source가 있을 때 | constructor call이 trivial하고 local할 때 |
| Factory / Domain Factory | creation에 domain policy, dependency, generated ID, clock, object family가 필요할 때 | 의도 없이 constructor만 감쌀 때 |
| State | 생명주기 상태에 따라 동작이 바뀌고 상태별 로직이 흩어질 때 | 작은 exhaustive `when`이 더 명확하고 커질 가능성이 낮을 때 |
| Specification / Policy | business predicate에 이름, composition, reuse, isolated test가 필요할 때 | predicate가 재사용이나 domain meaning이 없는 한 곳의 local condition일 때 |
| Adapter / Port | external system, vendor, persistence, clock, ID generator를 application/domain contract 뒤로 격리해야 할 때 | method 이름만 바꾸고 boundary value가 없을 때 |
| Decorator | cache, metering, logging, retry처럼 optional cross-cutting behavior가 interface를 감쌀 때 | caller가 알아야 하는 business side effect나 ordering을 숨길 때 |
| Chain / Pipeline | 순서 있는 validation, enrichment, approval, handler step에 독립 테스트와 확장이 필요할 때 | step order가 business-critical인데 명시적으로 보이지 않거나 테스트되지 않을 때 |
| Command Handler | action을 자체 validation, permission, transaction boundary를 가진 실행 가능한 동작으로 표현해야 할 때 | `*Command` data object만으로 충분하고 behavior object가 필요 없을 때 |

## Kotlin/Spring 가이드

- Template Method가 안정된 생명주기를 명확히 모델링하지 않는다면 inheritance보다 composition을 우선한다.
- closed state set에는 큰 Strategy hierarchy보다 Kotlin sealed interface와 exhaustive `when`이 더 나은 경우가 많다.
- open-ended variation, plugin-like policy, configuration/domain data로 선택되는 behavior에는 Strategy를 사용한다.
- Template Method abstract class는 작게 유지한다. protected hook은 domain step 이름으로 명명하고 테스트로 보호한다.
- Specification과 Policy는 가능하면 dependency-free하게 유지한다. repository, clock, client가 필요하면 orchestration을 Service나 role component로 옮긴다.
- Strategy/Policy/Specification 구현은 설명하는 domain 가까이에 둔다. `common`, `support`, `util`은 진짜 공유되는 technical pattern에만 사용한다.
- pattern 선택은 기존 naming rule과 함께 맞춘다: `*Command`, `*Query`, `*Criteria`, `*Result`, role component, Facade/Service boundary, static factory.

## 리뷰 휴리스틱

- 여러 class에서 같은 type/status에 대한 `if/else` 또는 `when`이 흩어져 있으면 Strategy, State, Specification 후보일 수 있다.
- 안정된 sequence와 달라지는 step을 가진 긴 service method는 Template Method 후보일 수 있지만, 먼저 role component + composition이 더 단순한지 확인한다.
- default, mapping, invariant check를 포함한 construction code가 반복되면 Static Factory 또는 Domain Factory 후보일 수 있다.
- external provider name이나 channel type에 대한 switch는 Adapter + Strategy 후보일 수 있다.
- 독립적으로 바뀔 수 있는 step을 가진 validation list나 approval flow는 Chain/Pipeline 후보일 수 있다.
- 패턴은 결과 코드의 책임이 더 명확해지고, 변경 지점이 줄고, test seam이 좋아지고, domain language가 강해질 때만 성공한 것이다.
