# Backend Claude Plugin

`char-labs/backend-claude-plugin`은 Claude Code에서 백엔드 설계, 구현, 리뷰 품질을 일관되게 높이기 위한 plugin marketplace입니다.

현재 포함된 plugin은 `backend-quality-workflow` 하나이며, 백엔드 아키텍처, OOP/SOLID, 보안, 쿼리 병목, 애플리케이션 성능, Spring/Kotlin 검증 흐름을 한글 중심으로 지원합니다.

## Quick Start

Claude Code 안에서 marketplace를 추가하고 plugin을 설치합니다.

```text
/plugin marketplace add char-labs/backend-claude-plugin
/plugin install backend-quality-workflow@backend-claude-plugin
```

설치 후 현재 세션에 바로 반영하려면 reload합니다.

```text
/reload-plugins
```

CLI로 설치할 수도 있습니다.

```bash
claude plugin marketplace add char-labs/backend-claude-plugin
claude plugin install backend-quality-workflow@backend-claude-plugin --scope user
```

자세한 설치, 로컬 개발, 업데이트, 제거 절차는 [INSTALL.md](./INSTALL.md)를 참고하세요.

## 제공 기능

| 영역 | 내용 |
|---|---|
| 설계 | 서비스 경계, 도메인 모델, 트랜잭션, 인가 책임, 영속성 경계 설계 |
| 구현 | OOP/SOLID, 보안 기본값, 성능을 고려한 데이터 접근, 집중 테스트 |
| 리뷰 | 아키텍처, 보안, 성능, 쿼리, 테스트 가능성 중심의 evidence-based review |
| Spring/Kotlin | Spring Security, JPA/Hibernate, `@Transactional`, Gradle, Kotlin nullability/import style |
| 라우팅 | 사용자 요청을 분석해 적절한 skill/agent 후보를 제안하는 `UserPromptSubmit` hook |
| 보안 가드 | 위험한 shell, 민감 파일 read/write, `.env`, private key, credentials 접근 차단 |

## 주요 Skills

설치 후 `/help`에서 namespaced skill을 확인할 수 있습니다.

| Skill | 용도 |
|---|---|
| `/backend-quality-workflow:design` | 백엔드 아키텍처와 트랜잭션/인가/영속성 경계 설계 |
| `/backend-quality-workflow:implement` | 백엔드 코드 구현 또는 수정 |
| `/backend-quality-workflow:review` | PR/diff/변경사항 종합 리뷰 |
| `/backend-quality-workflow:security-review` | 인증, 인가, injection, SSRF, secrets, token, CORS/CSRF 리뷰 |
| `/backend-quality-workflow:performance-review` | 응답 시간, 캐시, timeout, retry, memory, lock 병목 리뷰 |
| `/backend-quality-workflow:persistence-query-review` | Repository, SQL/JPQL/QueryDSL, JPA fetch, N+1, index, pagination 리뷰 |
| `/backend-quality-workflow:spring-kotlin-review` | Spring/Kotlin/JPA/Gradle 특화 리뷰 |
| `/backend-quality-workflow:backend-test-strategy` | 단위/통합/API contract/인가/failure-mode 테스트 설계 |
| `/backend-quality-workflow:backend-skill-authoring` | 프로젝트 전용 백엔드 `SKILL.md` 작성 패턴 정리 |

## 주요 Agents

설치 후 `/agents`에서 확인할 수 있습니다.

| Agent | 용도 |
|---|---|
| `backend-architect` | 설계, 경계 설정, 모호한 백엔드 요청 정리 |
| `backend-coder` | 범용 백엔드 구현 |
| `backend-reviewer` | 종합 백엔드 리뷰 |
| `security-reviewer` | 읽기 전용 보안 리뷰 |
| `performance-reviewer` | 읽기 전용 성능 리뷰 |
| `persistence-query-specialist` | Repository/SQL/JPA/QueryDSL/N+1 전문 작업 |
| `api-contract-designer` | GraphQL, gRPC/protobuf, REST/OpenAPI 계약 설계 |
| `backend-test-writer` | 테스트 작성/보강 |
| `migration-planner` | 마이그레이션, rollout/rollback, ADR 계획 |
| `build-validation-specialist` | Gradle/Maven/CI/compile/test 실패 분석 |

## 사용 예시

자연어로 요청해도 routing hook이 backend 관련 요청을 분류합니다.

```text
UserRepository 쿼리가 느려. N+1이 있는지 리뷰해줘.
```

```text
신규 주문 API의 GraphQL input/output과 에러 응답을 설계해줘.
```

```text
이 PR을 보안, 성능, OOP 관점에서 리뷰해줘.
```

```text
Spring Security 설정에서 permitAll 범위가 안전한지 확인해줘.
```

## 로컬 개발

로컬에서 plugin 구조를 검증합니다.

```bash
claude plugin validate ./plugins/backend-quality-workflow
```

개발 중인 plugin directory를 현재 세션에만 로드합니다.

```bash
claude --plugin-dir ./plugins/backend-quality-workflow --debug
```

로컬 marketplace로 설치 테스트를 할 수도 있습니다.

```text
/plugin marketplace add .
/plugin install backend-quality-workflow@backend-claude-plugin
```

## Repository Structure

```text
backend-claude-plugin/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── backend-quality-workflow/
│       ├── .claude-plugin/plugin.json
│       ├── agents/
│       ├── hooks/
│       ├── references/
│       ├── scripts/
│       ├── skills/
│       ├── templates/
│       └── tests/
├── INSTALL.md
└── README.md
```

## Security Model

이 plugin은 보안 위험을 줄이기 위한 workflow와 hook guard를 제공합니다. 다만 AI workflow나 hook만으로 무취약성을 보장할 수는 없습니다.

기본 정책:

- 위험한 shell pattern과 destructive command를 선택적으로 차단합니다.
- `.env`, private key, credentials, production config 같은 민감 파일 read/write를 차단합니다.
- 외부 scanner나 dependency는 자동 설치하지 않습니다.
- security review 결과는 evidence, impact, fix, test expectation 중심으로 작성합니다.

## Requirements

- Claude Code plugin 지원 버전
- GitHub marketplace 설치 시 `char-labs/backend-claude-plugin` 접근 권한
- Hook script 실행을 위한 Python 3

## Author

Maintained by `char-yb` for `char-labs`.
