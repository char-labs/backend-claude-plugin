# API 프로토콜 참고 자료

GraphQL, gRPC/protobuf, REST/OpenAPI, DTO boundary를 포함한 백엔드 API contract 작업에서 이 자료를 사용한다.

## 계약 원칙

- 요청이 breaking change를 명시적으로 허용하지 않았다면 compatibility를 보존한다.
- validation, authorization, mapping, error translation, pagination, batching의 ownership을 정의한다.
- repository가 의도적으로 shared model을 쓰는 경우가 아니라면 transport DTO를 domain/persistence model과 분리한다.
- nullability, optionality, default value, error semantic을 명시한다.
- internal persistence field, framework exception, stack trace, security-sensitive data를 노출하지 않는다.

## GraphQL

- query/mutation field, input type, output type, nullability, pagination, authorization을 정의한다.
- collection field에는 bounded list와 cursor/page argument를 우선한다.
- batching, DataLoader, projection, service aggregation으로 N+1 risk를 고려한다.
- resolver는 auth context, argument validation, use-case/service call, response mapping만 담당하게 얇게 유지한다.

## gRPC와 Protobuf

- field number를 재사용하지 않는다. 프로젝트 convention이 지원하면 제거된 field는 reserved로 표시한다.
- 안정적인 package/service naming을 사용한다. compatibility를 위해 additive change를 우선한다.
- status code, error detail, project-specific error envelope을 통해 error를 일관되게 model한다.
- request message에는 caller identity, resource identity, pagination을 명확히 표현한다.

## REST와 OpenAPI

- resource naming, HTTP method, status code, idempotency, error body를 일관되게 사용한다.
- path, query, header, body input은 boundary에서 검증한다.
- public endpoint 또는 expensive endpoint의 cache behavior와 rate limit을 정의한다.

## 보안과 테스트

- 모든 protected API에는 authentication과 object-level authorization이 필요하다.
- interface shape가 바뀌면 contract test 또는 schema/proto generation check를 포함한다.
- unauthorized, invalid input, missing resource, compatibility-relevant default에 대한 negative test를 포함한다.
