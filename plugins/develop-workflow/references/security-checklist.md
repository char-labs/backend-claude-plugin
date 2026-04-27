# 백엔드 보안 체크리스트

인증, 인가, 입력, 저장소, 네트워크, 비밀값, logging, dependency를 다루는 보안 리뷰와 구현 작업에서 이 자료를 사용한다.

## 심각도 기준

- Critical: 원격 코드 실행 가능성, authentication bypass, 권한 상승, 민감 secret 노출, 파괴적 data access, 악용 가능한 injection.
- High: unauthorized data access 가능성, object-level authorization 누락, 민감 network로의 SSRF, 심각한 crypto misuse, unsafe deserialization.
- Medium: security control이 불완전하거나 일관되지 않거나 현실적인 조건에서 우회 가능함.
- Low: 직접 악용 가능성은 낮지만 hardening, defense-in-depth, maintainability에 영향을 주는 문제.

## 인증과 인가

- 보호된 endpoint와 background command에 authentication이 필요한지 확인한다.
- role check만 보지 말고 object-level authorization을 확인한다. 유효한 session을 가진 사용자가 다른 tenant, account, order, coupon, admin object에 접근하면 안 된다.
- admin path, batch job, internal API에 명시적 trust boundary가 있는지 확인한다.
- 독립적으로 인가되지 않았다면 client-controlled user ID, tenant ID, role, price, balance, state transition을 거부한다.

## 입력과 Injection

- SQL, JPQL, native query, LDAP, shell, template, expression-language 입력은 parameter binding 또는 safe API를 사용해야 한다.
- dynamic `ORDER BY`, table name, field name, filter에는 allowlist가 필요하다.
- request body, path, query, header, file metadata는 boundary에서 검증한다.
- XML, YAML, archive, serialized object parsing은 high risk로 다룬다.

## SSRF, 파일, 네트워크 안전성

- user-controlled URL에는 scheme, host, port, redirect, DNS rebinding, private network 제한이 필요하다.
- file path는 traversal, absolute path escape, symlink escape, 위험한 extension을 거부해야 한다.
- upload에는 size limit, type validation, storage isolation, 도메인상 필요한 경우 malware scanning이 필요하다.

## 비밀값과 민감 데이터

- secret, token, API key, cookie, authorization header, private key, 민감 payload 전체를 log에 남기지 않는다.
- `.env`, private key, certificate, keystore, production config, generated credential을 commit하지 않는다.
- password와 token에는 one-way hashing 또는 secure storage가 필요하다. 나중에 복구할 목적으로 password를 encrypt하지 않는다.
- log, metric, trace, error message, audit event에서 PII와 규제 대상 데이터를 redact한다.

## 암호화와 Token

- 검증된 library와 platform primitive를 사용한다. custom crypto를 직접 구현하지 않는다.
- JWT validation은 signature, algorithm, issuer, audience, expiration, not-before, key rotation behavior를 검증해야 한다.
- random token에는 cryptographically secure randomness와 충분한 entropy가 필요하다.
- password hashing은 bcrypt, scrypt, Argon2 또는 프로젝트가 승인한 equivalent를 configured cost와 함께 사용한다.

## Web/API 통제

- CORS는 명시적이고 environment-aware해야 한다. credential과 함께 wildcard origin을 쓰지 않는다.
- cookie-authenticated browser flow에는 다른 강한 통제가 없다면 CSRF protection이 필요하다.
- login, signup, password reset, OTP, payment, search, expensive endpoint에는 rate limit과 abuse control이 필요하다.
- error response는 stack trace, SQL detail, internal URL, secret을 노출하면 안 된다.

## 공급망

- review 중 dependency를 자동 설치하지 않는다. 기존 tool을 감지하고 command를 추천한다.
- 새 dependency는 maintenance status, license 적합성, 최소 scope, repo와 호환되는 version pinning을 확인해야 한다.
- build script는 검증 없이 remote script를 실행하지 않아야 한다.
