---
name: oop-review
description: 백엔드 코드의 class responsibility, dependency direction, abstraction, domain modeling, cohesion, coupling, testability를 OOP/SOLID 관점으로 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 클래스, 모듈, 리뷰 범위]"
---

# OOP/SOLID Review

## 설명

사용자 요청을 유지보수 가능한 객체지향 백엔드 설계 관점으로 검토한다. 구조 변경 제안은 구체적 correctness, testability, coupling 영향이 있을 때만 낸다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- JVM/Spring/Kotlin 코드면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. class responsibility와 cohesion을 확인한다. validation, authorization, orchestration, persistence, mapping, IO, response formatting이 이유 없이 한 class에 섞이면 표시한다.
2. dependency inversion을 확인한다. 고수준 정책이 concrete infrastructure에 직접 묶여 testability를 해치면 port/interface를 검토한다.
3. interface size와 substitutability를 확인한다. 구현체는 contract, nullability, error behavior, side effect를 지켜야 한다.
4. domain model 표현력을 확인한다. business invariant가 controller, mapper, repository에 흩어져 있으면 찾는다.
5. testability를 확인한다. 핵심 동작은 network, wall clock, random ID, real DB 없이 검증 가능한지 본다.

## 검증

- 제안한 리팩터가 기존 테스트로 보호되는지 확인한다.
- 테스트가 없으면 최소 unit 또는 slice test를 제안한다.

## 주의사항

- 실수 방지 가드레일: 리팩터 제안은 테스트 가능성과 회귀 검증 방법이 있을 때 우선순위를 높인다.
- 추상화는 실제 중복, 변경 가능성, 테스트 장벽을 줄일 때만 제안한다.
- 광범위한 architecture rewrite보다 국소적인 책임 분리를 우선한다.

## 출력

구체적 maintainability, correctness, testability impact가 있는 finding만 반환한다.
