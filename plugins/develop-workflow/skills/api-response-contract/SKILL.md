---
name: api-response-contract
description: Spring/Kotlin REST API의 공통 응답 envelope을 설계하거나 생성할 때 사용. ApiResponse, ErrorResponse, ResponseBodyAdvice, RestControllerAdvice, ExceptionHandler, ResponseEntityExceptionHandler, controller 반환 DTO, RestDocs 응답 필드 정책을 함께 다룬다.
argument-hint: "[ApiResponse, ErrorResponse, RestControllerAdvice, 공통 응답 포맷 작업]"
---

# API 응답 Envelope 설계

## 설명

Spring/Kotlin REST API에서 성공/실패 응답 형식을 `ApiResponse` 같은 공통 envelope으로 통일할 때 사용한다. Controller가 직접 wrapper를 반복 생성하는 구조가 아니라, 성공 응답은 `ResponseBodyAdvice`, 실패 응답은 `RestControllerAdvice`/`ExceptionHandler`에서 일관되게 감싸는 구조를 우선한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/api-response-patterns.md`
- `${CLAUDE_PLUGIN_ROOT}/references/api-protocols.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- Spring/Kotlin이면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 기존 프로젝트의 response wrapper, error body, advice, controller 반환 타입, docs/test convention을 먼저 확인한다.
2. 공통 success envelope 필드를 정한다: `success`, `status`, `data`, `timestamp`.
3. 공통 error body를 정한다: framework exception이나 stack trace가 아니라 노출 가능한 error code/class name과 message만 둔다.
4. Controller는 가능한 plain response DTO를 반환하고, status 변경이 필요하면 `@ResponseStatus` 또는 필요한 경우에만 `ResponseEntity`를 사용하게 한다.
5. 성공 응답 wrapping은 `ResponseBodyAdvice`에서 처리한다. 이미 `ApiResponse`, `ErrorResponse`, `String`, null body, 제외 URL은 재감싸지 않는다.
6. 실패 응답 wrapping은 `RestControllerAdvice`에서 처리한다. validation, type mismatch, domain error, authentication error, catch-all exception을 명시적으로 분리한다.
7. API docs나 RestDocs가 있으면 envelope 필드와 실제 `data.*` 필드가 문서화되는지 확인한다.
8. business logic이 없는 단순 wrapper만 추가하면 새 테스트를 강제하지 않는다. advice branch, error mapping, docs shape가 바뀌면 집중 테스트를 제안한다.

## 검증

- Spring/Kotlin이면 영향 모듈의 compile 또는 test task를 우선 제안한다.
- Advice 동작을 바꾸면 success wrapping, already wrapped body, String/null body, error response mapping을 확인한다.
- RestDocs/OpenAPI가 있으면 generated schema 또는 docs test를 확인한다.

## 주의사항

- 실수 방지 가드레일: 공통 응답 포맷 변경은 public API contract 변경이므로 하위 호환성, 클라이언트 영향, 문서 필드, error mapping 테스트 기대치를 함께 남긴다.
- Controller마다 `ApiResponse.success(...)`를 직접 반복 호출하지 않는다. 반복 wrapper 생성은 누락과 불일치를 만든다.
- ErrorResponse에는 stack trace, internal exception message, SQL, token, PII 같은 민감정보를 넣지 않는다.
- `ResponseBodyAdvice`는 actuator, health, prometheus, file/streaming response, `String` converter, already wrapped body를 고려해야 한다.
- catch-all exception은 내부 로그에는 원인을 남기되 외부 응답은 안전한 일반 메시지로 제한한다.
- 테스트는 실 DB와 테스트 `@Transactional` rollback에 의존하지 않는다.

## 출력

응답 envelope 구조, 생성 위치, advice 책임 분리, 예외 mapping, controller 반환 규칙, 필요한 검증 명령을 함께 제시한다.
