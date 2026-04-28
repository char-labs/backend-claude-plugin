# Backend Claude Plugin

`char-labs/backend-claude-plugin`은 Claude Code에서 백엔드 설계, 구현, 리뷰, Git 안전 워크플로우, 에이전트/스킬 설계 가이드를 일관되게 제공하기 위한 plugin marketplace입니다.

현재 marketplace에는 3개 plugin이 포함됩니다. 백엔드 품질/보안/성능/OOP/Spring-Kotlin 컨텍스트는 `develop-workflow`가 소유합니다.

| Plugin | 상태 | 역할 |
|---|---|---|
| `develop-workflow` | 권장 | 설계, 구현, 리뷰를 통합한 백엔드 개발 워크플로우 |
| `git-utils` | 권장 | 브랜치, 커밋, 푸시, PR 흐름과 위험 명령/민감 파일 guard |
| `workflow-guide` | 권장 | 에이전트 설계 원칙, 스킬 작성, 룰/템플릿 가이드 |

## Quick Start

터미널에서는 `claude plugin ...` CLI 명령을 사용합니다.

```bash
claude plugin marketplace add char-labs/backend-claude-plugin
claude plugin install develop-workflow@backend-claude-plugin --scope user
claude plugin install git-utils@backend-claude-plugin --scope user
claude plugin install workflow-guide@backend-claude-plugin --scope user
```

Claude Code 세션 안에서는 slash command를 사용합니다. 아래 명령은 zsh 터미널이 아니라 Claude Code 입력창에서 실행합니다.

```text
/plugin marketplace add char-labs/backend-claude-plugin
/plugin install develop-workflow@backend-claude-plugin
/plugin install git-utils@backend-claude-plugin
/plugin install workflow-guide@backend-claude-plugin
/reload-plugins
```

자세한 설치, 로컬 개발, 업데이트, 제거 절차는 [INSTALL.md](./INSTALL.md)를 참고하세요.

## 제공 기능

| 영역 | Plugin | 내용 |
|---|---|---|
| 설계 | `develop-workflow` | 서비스 경계, 도메인 모델, 트랜잭션, 인가 책임, 영속성 경계 설계 |
| 구현 | `develop-workflow` | OOP/SOLID, 보안 기본값, 성능을 고려한 데이터 접근, 집중 테스트 |
| 리뷰 | `develop-workflow` | 아키텍처, 보안, 성능, 쿼리, 테스트 가능성 중심의 evidence-based review |
| Spring/Kotlin/Java | `develop-workflow` | Spring Security, JPA/Hibernate, coroutine/concurrency, `@Transactional`, Gradle, nullability, import/static import 규칙 |
| 라우팅 | `develop-workflow` | 사용자 요청을 분석해 적절한 skill/agent 후보를 제안하는 `UserPromptSubmit` hook |
| Git 안전 흐름 | `git-utils` | stage/commit/push/PR 전 검증, 위험 Bash, 민감 파일 read/write 차단 |
| 가이드 작성 | `workflow-guide` | 프로젝트 전용 `SKILL.md`, reference, template, rule 작성 패턴 |

## 주요 Skills

설치 후 `/help`에서 namespaced skill을 확인할 수 있습니다.

### `develop-workflow`

| Skill | 용도 |
|---|---|
| `/develop-workflow:design` | 백엔드 아키텍처, 디자인 패턴, 트랜잭션/인가/영속성 경계 설계 |
| `/develop-workflow:implement` | 백엔드 코드 구현 또는 수정 |
| `/develop-workflow:review` | PR/diff/변경사항 종합 리뷰 |
| `/develop-workflow:security-review` | 인증, 인가, injection, SSRF, secrets, token, CORS/CSRF 리뷰 |
| `/develop-workflow:performance-review` | 응답 시간, 캐시, timeout, retry, memory, lock 병목 리뷰 |
| `/develop-workflow:persistence-query-review` | Repository, SQL/JPQL/QueryDSL, JPA fetch, N+1, index, pagination 리뷰 |
| `/develop-workflow:spring-kotlin-review` | Spring/Kotlin/JPA/Gradle 특화 리뷰 |
| `/develop-workflow:spring-coroutine-concurrency` | Spring Boot + Kotlin coroutine, Dispatchers.IO, blocking IO, structured concurrency 리뷰/설계 |
| `/develop-workflow:backend-test-strategy` | 단위/통합/API contract/인가/failure-mode 테스트 설계 |
| `/develop-workflow:api-contract-design` | GraphQL, gRPC/protobuf, REST/OpenAPI 계약 설계 |
| `/develop-workflow:api-response-contract` | ApiResponse/ErrorResponse 공통 응답 envelope, RestControllerAdvice, ResponseBodyAdvice 설계 |
| `/develop-workflow:build-validation` | Gradle/Maven/CI/compile/test 실패 분석 |

### `git-utils`

| Skill | 용도 |
|---|---|
| `/git-utils:git-safe-workflow` | Git stage/commit/push/PR 작업 전 안전 범위와 검증 확인 |
| `/git-utils:git-utils-bootstrap` | Git 유틸리티 플러그인 구조와 guard 범위 점검 |

### `workflow-guide`

| Skill | 용도 |
|---|---|
| `/workflow-guide:backend-skill-authoring` | 프로젝트 전용 백엔드 `SKILL.md`와 reference 작성 패턴 정리 |
| `/workflow-guide:clarify-requirements` | 모호한 백엔드 요청의 범위, 성공 기준, 검증 기준 명확화 |
| `/workflow-guide:workflow-guide-bootstrap` | 룰, 템플릿, 스킬 구조 초기화/점검 |

## 주요 Agents

`develop-workflow` 설치 후 `/agents`에서 확인할 수 있습니다.

| Agent | 용도 |
|---|---|
| `backend-architect` | 설계, 경계 설정, 모호한 백엔드 요청 정리 |
| `backend-coder` | 범용 백엔드 구현 |
| `backend-reviewer` | 종합 백엔드 리뷰 |
| `security-reviewer` | 읽기 전용 보안 리뷰 |
| `performance-reviewer` | 읽기 전용 성능 리뷰 |
| `coroutine-concurrency-specialist` | Spring Boot + Kotlin coroutine/concurrency 설계, 구현, 리뷰 |
| `persistence-query-specialist` | Repository/SQL/JPA/QueryDSL/N+1 전문 작업 |
| `api-contract-designer` | GraphQL, gRPC/protobuf, REST/OpenAPI 계약 설계 |
| `backend-test-writer` | 테스트 작성/보강 |
| `migration-planner` | 마이그레이션, rollout/rollback, ADR 계획 |
| `build-validation-specialist` | Gradle/Maven/CI/compile/test 실패 분석 |
| `oop-solid-reviewer` | OOP/SOLID, 디자인 패턴, 응집도, 결합도, 계층 의존성 리뷰 |

## 사용 예시

자연어로 요청해도 `develop-workflow`의 routing hook이 backend 관련 요청을 분류합니다.

```text
UserRepository 쿼리가 느려. N+1이 있는지 리뷰해줘.
```

```text
신규 주문 API의 GraphQL input/output과 에러 응답을 설계해줘.
```

```text
Spring Kotlin API에 ApiResponse 공통 응답 래퍼와 RestControllerAdvice를 만들어줘.
```

```text
이 PR을 보안, 성능, OOP 관점에서 리뷰해줘.
```

```text
Spring Security 설정에서 permitAll 범위가 안전한지 확인해줘.
```

```text
Spring Kotlin coroutineScope로 외부 API 두 개를 병렬 호출해도 되는지 Dispatchers.IO와 blocking 관점에서 리뷰해줘.
```

```text
전략 패턴과 템플릿 메서드 패턴을 활용해서 객체지향 백엔드 설계해줘.
```

## 로컬 개발

로컬에서 plugin manifest를 검증합니다.

```bash
claude plugin validate ./plugins/develop-workflow
claude plugin validate ./plugins/git-utils
claude plugin validate ./plugins/workflow-guide
```

스크립트 문법과 hook JSON을 빠르게 확인합니다.

```bash
python3 -m py_compile \
  plugins/develop-workflow/scripts/route-user-prompt.py \
  plugins/develop-workflow/scripts/advisory-feedback.py \
  plugins/git-utils/scripts/guard-tool-use.py \
  plugins/git-utils/scripts/detect-validation-tools.py

python3 -m json.tool plugins/develop-workflow/hooks/hooks.json
python3 -m json.tool plugins/git-utils/hooks/hooks.json
```

플러그인 회귀 테스트를 실행합니다.

```bash
./plugins/develop-workflow/tests/run-guardrail-policy-tests.py
./plugins/develop-workflow/tests/eval/routing/run-routing-tests.py
./plugins/develop-workflow/tests/run-hook-tests.py
./plugins/git-utils/tests/run-hook-tests.py
```

로컬 marketplace로 설치 테스트를 할 수도 있습니다.

```bash
claude plugin marketplace add .
claude plugin install develop-workflow@backend-claude-plugin --scope user
claude plugin install git-utils@backend-claude-plugin --scope user
claude plugin install workflow-guide@backend-claude-plugin --scope user
```

## Repository Structure

```text
backend-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── develop-workflow/           # 설계/구현/리뷰 통합 워크플로우
│   ├── git-utils/                  # Git workflow와 안전 guard
│   └── workflow-guide/             # 스킬/에이전트/룰 작성 가이드
├── INSTALL.md
├── PLUGIN_SPLIT_CHECKLIST.md
└── README.md
```

## Security Model

이 marketplace는 보안 위험을 줄이기 위한 workflow와 hook guard를 제공합니다. 다만 AI workflow나 hook만으로 무취약성을 보장할 수는 없습니다.

기본 정책:

- 위험한 shell pattern과 destructive command를 선택적으로 차단합니다.
- `.env`, private key, credentials, production config 같은 민감 파일 read/write를 차단합니다.
- 외부 scanner나 dependency는 자동 설치하지 않습니다.
- security review 결과는 evidence, impact, fix, test expectation 중심으로 작성합니다.
- Kotlin/Java 코드는 본문/하단 영역의 inline FQCN을 금지하고 파일 상단 import를 우선합니다. Java static member는 `import static`을 사용합니다.

## Context Cache Hygiene

이 repository의 Markdown 문서는 Claude prompt caching이 정적 prefix를 재사용하기 쉽도록 작성합니다.

- skill/agent 문서 앞쪽에는 사용자 요청 원문, 날짜, timestamp, 개인 로컬 절대경로를 넣지 않습니다.
- 요청 대상을 가리킬 때는 `사용자 요청`, `대상 코드`처럼 정적인 표현을 사용합니다.
- 상세 reference는 필요한 경우에만, 문서에 적힌 순서대로 읽도록 안내합니다.
- 긴 예시와 프로젝트별 세부 규칙은 `references/`와 `templates/`로 분리합니다.
- 배포 변경 시 `plugin.json`의 `version`을 올려 캐시와 설치 업데이트 경계를 명확히 합니다.

## Requirements

- Claude Code plugin 지원 버전
- GitHub marketplace 설치 시 `char-labs/backend-claude-plugin` 접근 권한
- Hook script 실행을 위한 Python 3

## Author

Maintained by `char-yb` for `char-labs`.
