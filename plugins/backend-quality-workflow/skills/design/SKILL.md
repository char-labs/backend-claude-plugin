---
name: design
description: 서비스/도메인/트랜잭션/인가/영속성 경계를 포함한 백엔드 아키텍처를 설계할 때 사용. API wire schema는 api-contract-design, 단계적 이관은 migration-adr를 우선 사용.
argument-hint: "[기능 또는 설계 요청]"
---

# Backend Design Workflow

## 설명

사용자 요청을 백엔드 아키텍처 제안으로 설계한다. 서비스 경계, 도메인 모델, 트랜잭션, authorization ownership, persistence boundary, performance, test strategy를 결정한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- API contract가 포함되면 `${CLAUDE_PLUGIN_ROOT}/references/api-protocols.md`
- Spring/Kotlin/JPA/Gradle/JVM이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/design-decision-template.md`

## 실행 절차

1. 구조를 제안하기 전 기존 코드베이스를 확인한다.
2. 목표, 성공 기준, 제약, 영향 boundary를 명시한다.
3. validation, authorization, transaction control, persistence, external call, error handling의 소유 계층을 정한다.
4. unbounded read, N+1, missing index, long transaction 같은 query/application performance risk를 포함한다.
5. authn/authz, input validation, secret, logging, SSRF/file handling, rate limit 보안 통제를 포함한다.
6. Spring/Kotlin이면 `@Transactional`, Spring Security, DTO/domain/entity 분리, JPA fetch strategy, Gradle validation, Kotlin import style을 명시한다.
7. 기존 도구에 맞는 test와 validation command로 마무리한다.

## 검증

- 설계 결과가 구현자가 추가 결정을 하지 않아도 될 만큼 decision-complete인지 확인한다.
- 필요한 경우 ADR 작성 여부를 판단한다.

## 주의사항

- 실수 방지 가드레일: 설계 결정에는 검증 방법, 회귀 위험, 필요한 fixture 또는 테스트 위치를 함께 포함한다.
- 보안, 쿼리 성능, 트랜잭션 경계를 “구현 시 고려”로 미루지 말고 설계 결정에 포함한다.
- 특정 framework나 layer를 도입하기 전 기존 프로젝트 관례를 우선한다.
- 요구사항이 불명확하면 `clarify-requirements`로 범위와 성공 기준을 먼저 좁힌다.

## 출력

design decision template을 사용해 결정 완료형 설계를 반환한다.
