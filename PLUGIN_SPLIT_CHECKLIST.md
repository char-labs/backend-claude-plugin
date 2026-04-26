# 3-Plugin 분리 최소 스캐폴드 체크리스트

이 문서는 현재 `backend-quality-workflow` 단일 플러그인을 아래 3개로 분리할 때,
필수 누락을 방지하기 위한 최소 기준을 정리한다.

- develop-workflow: 설계/리뷰/구현 통합 워크플로우
- git-utils: 브랜치/커밋/PR 자동화 워크플로우
- workflow-guide: 에이전트 설계 원칙/룰/스캐폴딩 가이드

## 1) 공통 필수 (모든 신규 플러그인)

각 플러그인 디렉토리에 아래가 있어야 한다.

- `.claude-plugin/plugin.json`
- `skills/` (최소 1개 이상 `SKILL.md`)

권장(초기부터 포함 권장):

- `agents/`
- `hooks/`
- `templates/`
- `references/`
- `tests/`

## 2) 플러그인별 최소 디렉토리

### A. `plugins/develop-workflow`

필수:

- `.claude-plugin/plugin.json`
- `agents/`
- `skills/`
- `hooks/`

권장:

- `commands/`
- `templates/`
- `references/`
- `scripts/`
- `tests/`

초기 이관 후보(현재 `backend-quality-workflow` 기준):

- `skills/design/`
- `skills/implement/`
- `skills/review/`
- `skills/api-contract-design/`
- `skills/build-validation/`
- `skills/migration-adr/`
- `skills/oop-review/`
- `skills/security-review/`
- `skills/performance-review/`
- `skills/persistence-query-review/`
- `skills/spring-kotlin-review/`
- `skills/backend-test-strategy/`
- `skills/clarify-requirements/` (develop 라우팅의 vague backend 요청 처리용)
- `agents/api-contract-designer.md`
- `agents/backend-architect.md`
- `agents/backend-coder.md`
- `agents/backend-reviewer.md`
- `agents/security-reviewer.md`
- `agents/performance-reviewer.md`
- `agents/persistence-query-specialist.md`
- `agents/backend-test-writer.md`
- `agents/build-validation-specialist.md`
- `agents/migration-planner.md`
- `agents/oop-solid-reviewer.md`
- `hooks/hooks.json`
- `scripts/route-user-prompt.py`
- `scripts/advisory-feedback.py`

### B. `plugins/git-utils`

필수:

- `.claude-plugin/plugin.json`
- `skills/`
- `scripts/`

권장:

- `commands/`
- `hooks/`
- `tests/`
- `references/`
- `templates/`

초기 이관 후보:

- `skills/git-safe-workflow/`
- `scripts/detect-validation-tools.py`
- `scripts/guard-tool-use.py`
- `hooks/hooks.json` (PreToolUse safety guard만 유지)

### C. `plugins/workflow-guide`

필수:

- `.claude-plugin/plugin.json`
- `skills/`

권장:

- `rules/`
- `templates/`
- `references/`
- `agents/`
- `commands/`
- `tests/`

초기 이관 후보:

- `skills/backend-skill-authoring/`
- `skills/clarify-requirements/`
- `templates/*.md`
- `references/backend-skill-authoring-patterns.md`

## 2-1) 현재 스캐폴드 보완 기준

분리 초기에는 아래 디렉토리를 빈 상태라도 유지한다.

- `plugins/develop-workflow/commands/`: `/design`, `/implement`, `/review` 같은 slash command UX 확장 지점
- `plugins/git-utils/templates/`: 커밋 메시지, PR 본문, 릴리즈 노트 템플릿 확장 지점
- `plugins/workflow-guide/references/`: 룰과 분리된 배경 설명, 작성 패턴, 예시 문서 보관 지점

## 2-2) 1차 이관 정책

- 원본 `plugins/backend-quality-workflow`는 즉시 삭제하지 않고 호환 레이어로 유지한다.
- 신규 3개 플러그인에는 우선 copy-only 방식으로 자산을 넣어 설치/검증 리스크를 줄인다.
- `develop-workflow` hook은 사용자 프롬프트 라우팅과 백엔드 변경 피드백만 담당한다.
- `git-utils` hook은 위험 Bash 명령과 민감 파일 접근 차단만 담당한다.
- `workflow-guide`는 스킬 작성/요구사항 명확화/템플릿/참조 문서의 기준 저장소로 둔다.

## 3) 마켓플레이스 메타데이터 체크

루트 `.claude-plugin/marketplace.json`에서 아래를 반영한다.

- `plugins[]`에 3개 엔트리 추가
- 각 엔트리의 `name`, `source`, `description`, `version`, `author`, `homepage`
- 각 플러그인의 `.claude-plugin/plugin.json`과 버전 정합성 유지

## 4) 권장 분리 순서 (리스크 최소화)

1. `develop-workflow` 생성 + 핵심 skills/agents 이관
2. `git-utils` 생성 + git-safe-workflow 및 스크립트 분리
3. `workflow-guide` 생성 + 스킬 작성 가이드/템플릿 분리
4. 마지막에 `backend-quality-workflow`를 호환 레이어(또는 deprecate 안내)로 정리

## 5) 검증 체크리스트

공통:

- `claude plugin validate ./plugins/<plugin-name>`
- 설치 후 `/help`, `/agents` 노출 확인
- hook이 있는 플러그인은 안전 정책 회귀 테스트 수행

현재 저장소에서 바로 실행 가능한 검증:

- `./plugins/backend-quality-workflow/tests/run-guardrail-policy-tests.py`
- `./plugins/backend-quality-workflow/tests/eval/routing/run-routing-tests.py`
- `./plugins/backend-quality-workflow/tests/run-hook-tests.py`

## 6) 누락 방지 규칙

- 신규 skill/agent 추가 시 routing fixture와 문서 정책 테스트를 함께 갱신한다.
- 보안/인가, 트랜잭션 경계, 쿼리 병목, 테스트 명령 중 하나라도 빠지면 리뷰 게이트에서 경고한다.
- `commands/`는 선택사항이지만, slash command UX를 목표로 하면 각 플러그인에 도입한다.

## 7) 완료 정의 (Definition of Done)

아래를 모두 만족하면 분리 완료로 본다.

- 3개 플러그인이 각각 validate 통과
- 설치 후 스킬/에이전트 discovery 정상
- 기존 대표 요청(설계/구현/리뷰/Git 작업/가이드 생성)이 올바른 플러그인으로 라우팅
- README/INSTALL의 설치 예시가 3플러그인 기준으로 갱신됨
