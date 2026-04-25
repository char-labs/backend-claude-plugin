# Backend Security Checklist

Use this reference for security reviews and for implementation work that touches authentication, authorization, inputs, storage, networking, secrets, logging, or dependencies.

## Severity Calibration

- Critical: likely remote code execution, authentication bypass, privilege escalation, sensitive secret exposure, destructive data access, or exploitable injection.
- High: likely unauthorized data access, missing object-level authorization, SSRF to sensitive networks, serious crypto misuse, or unsafe deserialization.
- Medium: security control is incomplete, inconsistent, or bypassable under plausible conditions.
- Low: hardening, defense-in-depth, or maintainability issue with limited direct exploitability.

## Authentication And Authorization

- Verify authentication is required for protected endpoints and background commands.
- Check object-level authorization, not only role checks. A user with a valid session must not access another tenant, account, order, coupon, or admin object.
- Confirm admin paths, batch jobs, and internal APIs have explicit trust boundaries.
- Reject client-controlled user IDs, tenant IDs, roles, prices, balances, or state transitions unless independently authorized.

## Input And Injection

- SQL, JPQL, native queries, LDAP, shell, template, and expression-language inputs must use parameter binding or safe APIs.
- Dynamic `ORDER BY`, table names, field names, and filters need allowlists.
- Validate request body, path, query, headers, and file metadata at the boundary.
- Treat parsing of XML, YAML, archives, and serialized objects as high risk.

## SSRF, File, And Network Safety

- User-controlled URLs need scheme, host, port, redirect, DNS rebinding, and private network restrictions.
- File paths must reject traversal, absolute path escape, symlink escape, and dangerous extensions where relevant.
- Uploads need size limits, type validation, storage isolation, and malware scanning where the domain requires it.

## Secrets And Sensitive Data

- Never log secrets, tokens, API keys, cookies, authorization headers, private keys, or full sensitive payloads.
- Do not commit `.env`, private keys, certificates, keystores, production configs, or generated credentials.
- Passwords and tokens require one-way hashing or secure storage. Never encrypt passwords for later recovery.
- Redact PII and regulated data in logs, metrics, traces, error messages, and audit events.

## Crypto And Tokens

- Use established libraries and platform primitives. Do not implement custom crypto.
- JWT validation must verify signature, algorithm, issuer, audience, expiration, not-before, and key rotation behavior.
- Random tokens need cryptographically secure randomness and sufficient entropy.
- Password hashing should use bcrypt, scrypt, Argon2, or a project-approved equivalent with configured cost.

## Web And API Controls

- CORS must be explicit and environment-aware. Avoid wildcard origins with credentials.
- CSRF protection is required for cookie-authenticated browser flows unless another strong control applies.
- Rate limits and abuse controls are required for login, signup, password reset, OTP, payment, search, and expensive endpoints.
- Error responses must not reveal stack traces, SQL details, internal URLs, or secrets.

## Supply Chain

- Do not auto-install dependencies during review. Detect existing tools and recommend commands.
- New dependencies need maintenance status, license fit, minimal scope, and version pinning compatible with the repo.
- Build scripts must avoid executing remote scripts without verification.
