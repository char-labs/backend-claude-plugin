# 3-Plugin 구조 정리 체크리스트

이 문서는 현재 repository의 canonical plugin 구조를 유지하기 위한 기준을 정리한다.

## 현재 구조

```text
plugins/
├── develop-workflow/   # 백엔드 설계/구현/리뷰 통합 워크플로우
├── git-utils/          # Git workflow와 위험 명령/민감 파일 guard
└── workflow-guide/     # 스킬/에이전트/템플릿/레퍼런스 작성 가이드
```

## 소유권

| Plugin | 소유 범위 |
|---|---|
| `develop-workflow` | 백엔드 설계, 구현, 리뷰, 테스트 전략, 보안/성능/쿼리/Spring-Kotlin/coroutine 컨텍스트 |
| `git-utils` | Git stage/commit/push/PR workflow, 위험 Bash 차단, 민감 파일 read/write 차단 |
| `workflow-guide` | 프로젝트 전용 skill/agent/reference/template 작성 기준 |

## 중복 방지 규칙

- 백엔드 품질 컨텍스트는 `develop-workflow`에만 둔다.
- Git guard와 Git workflow 컨텍스트는 `git-utils`에만 둔다.
- 스킬/에이전트 작성 패턴과 도메인 스킬 템플릿은 `workflow-guide`에만 둔다.
- 동일한 skill, agent, reference, template을 여러 plugin에 수동 복사해 유지하지 않는다.
- 다른 plugin에서도 필요한 내용은 문서 링크나 README 안내로 연결하고, 배포 산출물 중복이 필요해질 때만 별도 생성 스크립트를 둔다.

## 디렉터리 기준

### `plugins/develop-workflow`

- `.claude-plugin/plugin.json`
- `agents/`
- `hooks/`
- `references/`
- `scripts/`
- `skills/`
- `templates/`
- `tests/`

### `plugins/git-utils`

- `.claude-plugin/plugin.json`
- `hooks/`
- `scripts/`
- `skills/`
- `tests/`

### `plugins/workflow-guide`

- `.claude-plugin/plugin.json`
- `references/`
- `skills/`
- `templates/`

## 검증 명령

```bash
claude plugin validate ./plugins/develop-workflow
claude plugin validate ./plugins/git-utils
claude plugin validate ./plugins/workflow-guide

./plugins/develop-workflow/tests/run-guardrail-policy-tests.py
./plugins/develop-workflow/tests/eval/routing/run-routing-tests.py
./plugins/develop-workflow/tests/run-hook-tests.py
./plugins/git-utils/tests/run-hook-tests.py

python3 -m py_compile \
  plugins/develop-workflow/scripts/route-user-prompt.py \
  plugins/develop-workflow/scripts/advisory-feedback.py \
  plugins/git-utils/scripts/guard-tool-use.py \
  plugins/git-utils/scripts/detect-validation-tools.py
```

## 변경 시 확인

- 새 backend skill/agent/reference는 `develop-workflow`에 추가한다.
- 새 Git guard나 Git workflow는 `git-utils`에 추가한다.
- 새 authoring pattern이나 template은 `workflow-guide`에 추가한다.
- routing fixture, hook test, 문서 정책 테스트가 영향을 받으면 함께 갱신한다.
- marketplace 엔트리는 3개 plugin만 유지한다.

## 완료 정의

- marketplace에 `develop-workflow`, `git-utils`, `workflow-guide`만 노출된다.
- README/INSTALL 설치 예시가 3개 plugin 기준이다.
- 중복 plugin directory가 없다.
- 위 검증 명령이 통과한다.
