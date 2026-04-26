---
name: api-contract-design
description: GraphQL, gRPC/protobuf, REST/OpenAPI, DTO, pagination, error shape, 하위 호환성, authorization boundary를 포함한 백엔드 API 입출력 계약을 설계하거나 변경할 때 사용.
argument-hint: "[API 계약 설계 작업]"
---

# API Contract Design

## 설명

사용자 요청의 API 입출력, wire schema, 하위 호환성을 설계한다. GraphQL, gRPC/protobuf, REST/OpenAPI, DTO 경계, 오류 응답, pagination, authorization이 포함된 작업에 사용한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/api-protocols.md`
- `${CLAUDE_PLUGIN_ROOT}/references/security-checklist.md`
- `${CLAUDE_PLUGIN_ROOT}/references/performance-checklist.md`
- Spring/Kotlin API면 `${CLAUDE_PLUGIN_ROOT}/references/spring-kotlin-backend.md`

## 실행 절차

1. 기존 API naming, nullability, pagination, error, authorization 패턴을 확인한다.
2. 요청/응답 shape, validation, authorization, mapping, error translation의 소유 계층을 정한다.
3. GraphQL이면 schema field, input/output type, resolver ownership, DataLoader/batching, N+1 위험을 포함한다.
4. gRPC/protobuf이면 field number 재사용 금지, reserved 처리, additive 변경, error semantics를 확인한다.
5. contract, authorization, invalid input, compatibility 테스트를 정의한다.

## 검증

- Schema/proto generation command가 있으면 먼저 실행한다.
- API contract 또는 resolver/service 테스트를 추가하거나 제안한다.

## 주의사항

- 실수 방지 가드레일: 계약 변경 시 호환성 fixture, authorization test, schema/proto generation 검증을 함께 갱신한다.
- 내부 persistence field, framework exception, stack trace, 민감정보가 API로 새지 않게 한다.
- protected API는 인증과 object-level authorization을 명시한다.

## 출력

스키마 예시, 호환성 메모, 보안 체크, 검증 명령을 포함한 간결한 API 계약 제안을 반환한다.
