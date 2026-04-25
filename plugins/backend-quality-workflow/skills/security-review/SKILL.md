---
name: security-review
description: authn/authz, injection, SSRF, path traversal, secrets, sensitive logging, crypto, token handling, CORS/CSRF, rate limiting, dependency risk 등 백엔드 보안을 집중 리뷰할 때 사용.
argument-hint: "[파일, diff, 엔드포인트, 리뷰 범위]"
---

# Backend Security Review

## 설명

`$ARGUMENTS`를 exploit 가능한 보안 위험 관점으로 검토한다. obvious issue가 보이지 않는 것은 제한적 assurance일 뿐 안전 증명이 아니다.

## 상세 자료

- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/review-finding-template.md`
- Spring/Kotlin security behavior면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. trust boundary를 식별한다: caller identity, tenant/account ownership, internal/external network boundary, file boundary, persistence boundary.
2. attacker-controlled input이 database query, shell command, template, redirect, outbound HTTP, file path, log, serialized format으로 흐르는지 추적한다.
3. protected state read/write마다 authentication과 object-level authorization을 확인한다.
4. secret과 sensitive data가 commit, response, log, trace, exception에 포함되지 않는지 확인한다.
5. token, crypto, CORS, CSRF, rate limit, dependency behavior를 관련 범위에서 확인한다.
6. Spring Security에서는 broad `permitAll`, method security 누락, cookie flow에서 CSRF 비활성화, credentials와 wildcard CORS 조합, ownership 없는 role-only check를 확인한다.

## 검증

- authorization boundary와 invalid input은 테스트 기대치를 명시한다.
- existing scanner나 dependency check가 있으면 실행/권장하되 v1에서는 자동 설치하지 않는다.

## 주의사항

- “취약점 없음”이라고 단정하지 않는다.
- PII, token, secret은 예시에도 실제 값을 포함하지 않는다.
- 보안 finding은 exploit path 또는 privilege/정보 노출 impact가 분명해야 한다.

## 출력

Critical/High/Medium/Low severity를 사용한다. 각 finding에는 evidence, impact, fix, test expectation을 포함한다.
