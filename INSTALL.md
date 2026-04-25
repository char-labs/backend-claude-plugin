# Backend Claude Plugin 설치 가이드

이 저장소는 `char-labs/backend-claude-plugin` marketplace 안에 `backend-quality-workflow` plugin을 배포하는 구조를 기준으로 한다.

## 1. 로컬 개발 검증

플러그인 구조와 manifest를 먼저 검증한다.

```bash
claude plugin validate "/Users/yunbeom/Documents/New project/backend-claude-plugin/plugins/backend-quality-workflow"
```

현재 작업 중인 plugin directory를 세션에만 임시 로드한다.

```bash
claude --plugin-dir "/Users/yunbeom/Documents/New project/backend-claude-plugin/plugins/backend-quality-workflow" --debug
```

Claude Code 안에서 다음을 확인한다.

```text
/help
/agents
/plugin
```

확인 대상:

- `/backend-quality-workflow:design`
- `/backend-quality-workflow:implement`
- `/backend-quality-workflow:review`
- `/backend-quality-workflow:security-review`
- `/backend-quality-workflow:performance-review`
- `backend-reviewer`
- `security-reviewer`
- `persistence-query-specialist`

## 2. 로컬 marketplace로 설치

개발 중인 로컬 repository를 marketplace로 등록한다.

```bash
claude plugin marketplace add "/Users/yunbeom/Documents/New project/backend-claude-plugin"
```

plugin을 설치한다.

```bash
claude plugin install backend-quality-workflow@backend-claude-plugin --scope user
```

scope 선택 기준:

- `--scope user`: 내 모든 프로젝트에서 사용한다.
- `--scope project`: 현재 프로젝트의 `.claude/settings.json`에 기록해 팀과 공유한다.
- `--scope local`: 현재 프로젝트에서 나만 사용한다. 보통 gitignore 대상이다.

## 3. GitHub marketplace로 설치

저장소가 `char-labs/backend-claude-plugin`로 push된 뒤에는 GitHub marketplace로 등록한다.

```bash
claude plugin marketplace add char-labs/backend-claude-plugin
```

plugin을 설치한다.

```bash
claude plugin install backend-quality-workflow@backend-claude-plugin --scope user
```

팀 repository에서 기본 사용을 권장하려면 project scope를 사용한다.

```bash
claude plugin marketplace add char-labs/backend-claude-plugin --scope project
claude plugin install backend-quality-workflow@backend-claude-plugin --scope project
```

## 4. 설치 확인

설치 후 새 Claude Code 세션에서 확인한다.

```text
/plugin
/help
/agents
```

대표 프롬프트로 routing hook 동작을 확인한다.

```text
UserRepository 쿼리가 느려. N+1이 있는지 리뷰해줘.
```

기대 동작:

- `persistence-query-specialist`가 후보로 선택된다.
- `persistence-query-review` skill 힌트가 주입된다.
- backend 관련 요청에만 routing protocol이 출력된다.

## 5. 업데이트

marketplace catalog를 갱신한다.

```bash
claude plugin marketplace update backend-claude-plugin
```

plugin을 업데이트한다.

```bash
claude plugin update backend-quality-workflow@backend-claude-plugin
```

`plugin.json`의 `version`이 같으면 Claude Code가 최신 버전으로 판단할 수 있으므로, 배포 변경 시 `version`을 올린다.

## 6. 제거

```bash
claude plugin uninstall backend-quality-workflow@backend-claude-plugin --scope user
```

marketplace까지 제거하려면 다음을 실행한다.

```bash
claude plugin marketplace remove backend-claude-plugin
```

## 주의사항

- 이 plugin은 `PreToolUse` hook으로 위험한 Bash, 민감 파일 read/write, `.env`, private key, credentials 접근을 선택적으로 차단한다.
- 보안 리뷰는 취약점 가능성을 줄이는 workflow이지 무취약성을 보장하지 않는다.
- 외부 scanner나 dependency는 자동 설치하지 않는다. 기존 도구가 있을 때만 검증 명령을 권장한다.
