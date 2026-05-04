# Backend Claude Plugin 설치 가이드

이 저장소는 `char-labs/backend-claude-plugin` marketplace 안에 여러 Claude Code plugin을 배포하는 구조를 기준으로 한다.

## 0. Plugin 구성

| Plugin | 권장 여부 | 설명 |
|---|---|---|
| `develop-workflow` | 권장 | 설계, 구현, 리뷰를 통합한 백엔드 개발 workflow |
| `git-utils` | 권장 | 브랜치, 커밋, 푸시, PR workflow와 안전 guard |
| `workflow-guide` | 권장 | 에이전트 설계 원칙, 룰, 스캐폴딩 가이드 |

신규 설치는 `develop-workflow`, `git-utils`, `workflow-guide` 3개를 기본으로 권장한다. 백엔드 품질/보안/성능/OOP/Spring-Kotlin 컨텍스트는 `develop-workflow`에 통합되어 있다.

## 1. 터미널에서 설치

터미널 zsh/bash에서는 slash command가 아니라 `claude plugin ...` CLI를 사용한다.

```bash
claude plugin marketplace add char-labs/backend-claude-plugin
claude plugin install develop-workflow@backend-claude-plugin --scope user
claude plugin install git-utils@backend-claude-plugin --scope user
claude plugin install workflow-guide@backend-claude-plugin --scope user
```

scope 선택 기준:

- `--scope user`: 내 모든 프로젝트에서 사용한다.
- `--scope project`: 현재 프로젝트의 `.claude/settings.json`에 기록해 팀과 공유한다.
- `--scope local`: 현재 프로젝트에서 나만 사용한다. 보통 gitignore 대상이다.

## 2. Claude Code 안에서 설치

Claude Code 세션 안에서는 `/plugin` slash command를 사용한다. 이 명령은 터미널에서 실행하면 `zsh: no such file or directory: /plugin` 오류가 난다.

```text
/plugin marketplace add char-labs/backend-claude-plugin
/plugin install develop-workflow@backend-claude-plugin
/plugin install git-utils@backend-claude-plugin
/plugin install workflow-guide@backend-claude-plugin
/reload-plugins
```

## 3. 로컬 marketplace로 설치 테스트

개발 중인 로컬 repository를 marketplace로 등록한다.

```bash
claude plugin marketplace add .
```

plugin을 설치한다.

```bash
claude plugin install develop-workflow@backend-claude-plugin --scope user
claude plugin install git-utils@backend-claude-plugin --scope user
claude plugin install workflow-guide@backend-claude-plugin --scope user
```

## 4. 설치 확인

설치 후 새 Claude Code 세션에서 확인한다.

```text
/plugin
/help
/agents
```

확인 대상:

- `/develop-workflow:design`
- `/develop-workflow:implement`
- `/develop-workflow:review`
- `/develop-workflow:persistence-query-review`
- `/develop-workflow:kotlin-backend-workflow`
- `/develop-workflow:spring-coroutine-concurrency`
- `/git-utils:git-safe-workflow`
- `/workflow-guide:backend-skill-authoring`
- `backend-reviewer`
- `kotlin-specialist`
- `coroutine-concurrency-specialist`
- `security-reviewer`
- `persistence-query-specialist`

대표 프롬프트로 `develop-workflow` routing hook 동작을 확인한다.

```text
UserRepository 쿼리가 느려. N+1이 있는지 리뷰해줘.
```

```text
Spring Kotlin coroutineScope 코드에서 Dispatchers.IO가 필요한 blocking 호출인지 리뷰해줘.
```

```text
전략 패턴과 템플릿 메서드 패턴을 활용해서 객체지향 백엔드 설계해줘.
```

기대 동작:

- 쿼리 프롬프트는 `persistence-query-specialist`와 `persistence-query-review`로 분류된다.
- coroutine 프롬프트는 `coroutine-concurrency-specialist`와 `spring-coroutine-concurrency`로 분류된다.
- Kotlin idiom/nullability 프롬프트는 `kotlin-specialist`와 `kotlin-backend-workflow`로 분류된다.
- 디자인 패턴 프롬프트는 `backend-architect`와 `design`으로 분류된다.
- backend 관련 요청에만 routing protocol이 출력된다.

## 5. 로컬 개발 검증

플러그인 구조와 manifest를 먼저 검증한다.

```bash
claude plugin validate ./plugins/develop-workflow
claude plugin validate ./plugins/git-utils
claude plugin validate ./plugins/workflow-guide
```

스크립트 문법과 hook JSON을 확인한다.

```bash
python3 -m py_compile \
  plugins/develop-workflow/scripts/route-user-prompt.py \
  plugins/develop-workflow/scripts/advisory-feedback.py \
  plugins/git-utils/scripts/guard-tool-use.py \
  plugins/git-utils/scripts/detect-validation-tools.py

python3 -m json.tool plugins/develop-workflow/hooks/hooks.json
python3 -m json.tool plugins/git-utils/hooks/hooks.json
```

플러그인 회귀 테스트를 실행한다.

```bash
./plugins/develop-workflow/tests/run-guardrail-policy-tests.py
./plugins/develop-workflow/tests/eval/routing/run-routing-tests.py
./plugins/develop-workflow/tests/run-hook-tests.py
./plugins/git-utils/tests/run-hook-tests.py
```

현재 작업 중인 plugin directory를 세션에만 임시 로드할 수도 있다.

```bash
claude --plugin-dir ./plugins/develop-workflow --debug
```

## 6. 업데이트

marketplace catalog를 갱신한다.

```bash
claude plugin marketplace update backend-claude-plugin
```

권장 plugin을 업데이트한다.

```bash
claude plugin update develop-workflow@backend-claude-plugin
claude plugin update git-utils@backend-claude-plugin
claude plugin update workflow-guide@backend-claude-plugin
```

`plugin.json`의 `version`이 같으면 Claude Code가 최신 버전으로 판단할 수 있으므로, 배포 변경 시 각 plugin의 `version`을 올린다.

## 7. 제거

```bash
claude plugin uninstall develop-workflow@backend-claude-plugin --scope user
claude plugin uninstall git-utils@backend-claude-plugin --scope user
claude plugin uninstall workflow-guide@backend-claude-plugin --scope user
```

marketplace까지 제거하려면 다음을 실행한다.

```bash
claude plugin marketplace remove backend-claude-plugin
```

## 주의사항

- `/plugin ...` 명령은 Claude Code 안에서만 동작한다. 터미널에서는 `claude plugin ...` CLI를 사용한다.
- `git-utils`는 `PreToolUse` hook으로 위험한 Bash, 민감 파일 read/write, `.env`, private key, credentials 접근을 선택적으로 차단한다.
- 보안 리뷰는 취약점 가능성을 줄이는 workflow이지 무취약성을 보장하지 않는다.
- 외부 scanner나 dependency는 자동 설치하지 않는다. 기존 도구가 있을 때만 검증 명령을 권장한다.
