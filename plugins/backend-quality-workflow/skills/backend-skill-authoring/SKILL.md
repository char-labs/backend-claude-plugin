---
name: backend-skill-authoring
description: 백엔드 도메인 컨벤션 스킬 작성/개선 가이드. Entity, Repository, QueryDSL, GraphQL, gRPC, Gradle, 테스트, ADR 같은 프로젝트 전용 SKILL.md와 상세 reference를 만들거나 정리할 때 사용.
argument-hint: "[스킬로 만들 백엔드 컨벤션 또는 기존 SKILL.md]"
---

# Backend Skill Authoring

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
5. Kotlin/Spring 스킬이라면 top-of-file import, 트랜잭션 경계, 보안/인가, 쿼리 병목, 테스트 명령을 포함한다.
6. Maum 같은 특정 프로젝트 규칙은 그대로 복사하지 말고 placeholder 또는 context pack 템플릿으로 일반화한다.

## 검증

- frontmatter에 `name`, `description`, 필요한 경우 `argument-hint`가 있는지 확인한다.
- description이 “언제 쓰는지”를 한글 키워드 중심으로 설명하는지 확인한다.
- `SKILL.md`가 너무 길면 상세 예시를 reference로 분리한다.

## 주의사항

- 실수 방지 가드레일: 새 스킬이나 에이전트를 추가하면 routing fixture, frontmatter 검증, 문서 정책 테스트를 함께 갱신한다.
- 특정 회사/서비스 경로, catalog, 정책은 범용 plugin에 직접 고정하지 않는다.
- 보안/인가, 쿼리 병목, 트랜잭션 경계, 검증 명령이 빠진 개발 스킬은 불완전한 것으로 본다.
- 서브에이전트가 사용할 skill이면 `<!-- skill: skill-name -->` 힌트와 함께 직접 활성화할 수 있게 설명한다.

## 출력

새 스킬 구조, `SKILL.md` 초안, 필요한 reference 목록, 검증 방법을 함께 제시한다.
