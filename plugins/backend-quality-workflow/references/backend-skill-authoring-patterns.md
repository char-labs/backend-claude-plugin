# Backend Skill Authoring Patterns

이 문서는 백엔드 프로젝트 전용 스킬을 `Entity Skill` 예시 같은 뉘앙스로 만들기 위한 작성 패턴이다.

## 핵심 구조

스킬은 짧은 실행 가이드와 긴 상세 reference로 나눈다.

```text
skills/{skill-name}/
  SKILL.md
  references/
    full-workflow.md
    examples.md
```

- `SKILL.md`: 언제 쓰는지, 실행 순서, 위치/명명 규칙, 검증, 주의사항.
- `references/full-workflow.md`: 상세 코드 예시, 예외 케이스, 깊은 설명.
- `references/examples.md`: 실제 Entity/Repository/GraphQL/gRPC/Test 예시.

플러그인 공용 스킬이면 reference는 `${CLAUDE_PLUGIN_ROOT}/references/...`에 두고, 프로젝트 로컬 스킬이면 해당 skill의 `references/` 하위에 둔다.

## SKILL.md 작성 패턴

Frontmatter:

```markdown
---
name: entity-skill
description: JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 새로 만들거나 수정할 때 사용. Entity 관계 매핑, catalog 선택, Repository 메서드, QueryDSL 필요 여부를 함께 판단한다.
---
```

본문 구성:

```markdown
# Entity Skill

## 설명
새로운 JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 작성한다.

## 실행 절차
1. 기존 유사 도메인의 Entity/Repository 패턴 확인
2. Entity 위치와 catalog 결정
3. ID, 필드 nullability, 관계 매핑, audit 필드 작성
4. Repository와 필요한 CustomRepository/QueryDSL 작성
5. 보안/인가, 쿼리 병목, 트랜잭션 경계 확인
6. 컴파일/테스트 실행

## 검증
`./gradlew :domain:compileKotlin`

## 주의사항
- var 최소화, val 우선
- 양방향 관계보다 단방향 우선
- userId/tenantId 등 소유권 필터 누락 금지
- 상세 패턴은 references/full-workflow.md 참조
```

## 좋은 description 규칙

description은 선택률에 큰 영향을 준다. 제목형보다 트리거형으로 쓴다.

좋음:

- `JPA Entity와 Repository를 프로젝트 컨벤션에 맞게 새로 만들거나 수정할 때 사용.`
- `GraphQL 스키마, Query/Mutation, input/output, resolver 경계 설계 시 사용.`
- `gRPC proto 필드/메서드 추가, 하위 호환성, 서버/클라이언트 에러 처리 설계 시 사용.`

피함:

- `Entity 가이드`
- `개발 가이드`
- `백엔드 참고 문서`

## 상세 reference로 빼야 하는 내용

- 긴 Kotlin 코드 예시
- QueryDSL/Native Query 패턴
- gRPC 서버/클라이언트 에러 처리
- 트랜잭션 예시
- 프로젝트별 catalog 표
- 모듈별 경로와 build command
- 자주 발생하는 anti-pattern

이런 내용은 `SKILL.md`에 모두 넣으면 context를 낭비한다. `SKILL.md`에서는 “언제 어떤 reference를 읽을지”만 알려준다.

## 백엔드 도메인 스킬 유형

| 유형 | 예시 | SKILL.md에 둘 내용 | reference에 둘 내용 |
|---|---|---|---|
| 생성/수정 | Entity, GraphQL, gRPC | 실행 순서, 위치, 검증 | 상세 코드 예시, 예외 |
| 리뷰 | Security, Query, OOP | 체크 순서, severity | 체크리스트, 사례 |
| 검증 | Gradle, Test | 명령 선택 기준 | 실패 triage, 모듈별 명령 |
| 문서화 | ADR, Migration | 문서 구조, 의사결정 기준 | 템플릿, rollout 예시 |

## Kotlin/Spring 백엔드 스킬 필수 체크

- Kotlin executable code에서는 inline FQCN보다 top-of-file import를 우선한다.
- Controller는 얇게 유지하고, Service/UseCase가 트랜잭션과 비즈니스 흐름을 소유한다.
- Repository는 persistence 접근을 소유하되 인가/도메인 결정을 숨기지 않는다.
- JPA 관계는 기본적으로 `FetchType.LAZY`를 우선하고 N+1 위험을 별도로 검토한다.
- QueryDSL/Native Query는 parameter binding을 사용하고 동적 정렬/필터는 allowlist로 제한한다.
- 사용자/tenant/account 소유권 필터는 누락되면 보안 finding으로 본다.
- 변경 후 최소 검증 명령을 스킬에 명시한다.

## Entity Skill 뉘앙스 추출

예시의 좋은 점:

- 위치가 명확하다: `domain/src/main/kotlin/.../entity/{도메인}/`
- 실행 절차가 번호로 고정되어 있다.
- 코드 예시가 바로 적용 가능한 형태다.
- catalog 선택, compile command, 주의사항이 있다.
- 상세 워크플로우는 별도 reference로 분리되어 있다.

일반화할 때:

- 특정 회사/서비스명은 placeholder로 바꾼다.
- catalog 표는 프로젝트 context pack으로 둔다.
- 보안/성능/테스트 체크를 기본 절차에 추가한다.
- 긴 예시는 `references/full-workflow.md`로 옮긴다.
