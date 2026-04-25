---
name: review
description: 백엔드 코드를 architecture, SOLID/OOP, security, query bottleneck, application performance, missing tests 관점으로 종합 리뷰할 때 사용. 보안/성능/쿼리/OOP/Spring-Kotlin 단일 범위는 focused review skill을 우선 사용.
argument-hint: "[파일, diff, PR, 리뷰 범위]"
---

# Backend Quality Review

## 설명

사용자 요청을 backend quality 관점으로 종합 리뷰한다. 넓은 조언보다 concrete evidence가 있는 finding을 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- Repository/query code가 있으면 `${CLAUDE_PLUGIN_ROOT}/references/persistence-query-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/testing-strategy.md`
- Spring/Kotlin/JPA/Gradle code가 있으면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 변경 범위와 user-facing behavior를 확인한다.
2. architecture boundary, dependency direction, transaction ownership, error boundary, testability를 확인한다.
3. OOP/SOLID 위반으로 coupling, hidden dependency, 테스트 난이도가 증가하는지 본다.
4. authn/authz, injection, SSRF, path traversal, secret handling, logging, crypto/token, CORS/CSRF, rate limit, supply-chain risk를 확인한다.
5. DB bottleneck을 확인한다: N+1, pagination/limit 누락, index 누락, non-sargable predicate, lock scope, batch behavior, transaction length.
6. application bottleneck을 확인한다: blocking IO, memory pressure, unbounded aggregation, cache stampede, timeout/retry 누락, expensive hot-loop work.
7. business rule, authorization boundary, failure mode, query behavior를 증명하는 test가 있는지 확인한다.

## 검증

- finding마다 재현 가능 증거, 영향, concrete fix, test expectation을 포함한다.
- 검증 명령은 repo에 이미 존재하는 도구를 기준으로 제안한다.

## 주의사항

- 실수 방지 가드레일: finding마다 재현 증거, concrete fix, test expectation이 없으면 심각도를 낮추거나 residual risk로 둔다.
- 심각도가 낮은 style preference로 high severity finding을 만들지 않는다.
- 보안은 “완전 보장”이 아니라 발견 가능한 위험을 낮추는 방식으로 표현한다.
- focused scope가 명확하면 `security-review`, `performance-review`, `persistence-query-review`, `oop-review`, `spring-kotlin-review`를 우선 고려한다.

## 출력

review finding template을 사용한다. findings first, severity 순서로 반환한다. blocking finding이 없으면 그렇게 말하고 residual risk 또는 validation gap을 남긴다.
