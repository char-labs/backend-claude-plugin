# Backend Domain Skill Template

아래 템플릿은 프로젝트 전용 백엔드 스킬을 만들 때 사용한다.

```markdown
---
name: {skill-name}
description: {언제 이 스킬을 써야 하는지 한 문장. 대상 작업, 트리거 키워드, 다른 스킬과의 경계를 포함한다.}
argument-hint: "[{작업 대상}]"
---

# {Skill Title}

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
4. 프로젝트 컨벤션에 맞게 구현 또는 설계를 작성한다.
5. 집중 테스트와 최소 검증 명령을 수행한다.

## 위치/명명 규칙

| 대상 | 위치 | 명명 |
|---|---|---|
| Entity | `{module}/src/main/kotlin/.../entity/` | `{Domain}Entity` |
| Repository | `{module}/src/main/kotlin/.../repository/` | `{Domain}Repository` |
| Service/UseCase | `{module}/src/main/kotlin/.../service/` | `{Domain}Service` |

## 검증

```bash
./gradlew :{module}:compileKotlin
./gradlew :{module}:test
```

## 주의사항

- 요청 원문, `$ARGUMENTS`, 날짜, 개인 로컬 절대경로처럼 호출마다 달라지는 값은 `SKILL.md` 앞쪽에 넣지 않는다.
- 실수 방지 가드레일: 변경이 routing, hook, fixture, 문서 정책에 영향을 주면 관련 회귀 테스트와 정책 테스트를 함께 갱신한다.
- Kotlin 코드는 top-of-file import를 우선한다.
- 민감정보 로그, 권한 누락, unbounded query, N+1을 기본 위험으로 본다.
- 상세 예시는 reference에 둔다.
```
```

## Reference Template

`references/full-workflow.md`는 다음 구조를 권장한다.

```markdown
# {Skill Title} Full Workflow Reference

## 1. 설계 상세

## 2. 구현 패턴

## 3. 에러 처리

## 4. 트랜잭션/성능 패턴

## 5. 테스트/검증

## 6. Anti-pattern
```
