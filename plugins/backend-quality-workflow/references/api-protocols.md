# API Protocols Reference

Use this reference for backend API contract work across GraphQL, gRPC/protobuf, REST/OpenAPI, and DTO boundaries.

## Contract Principles

- Preserve compatibility unless the request explicitly allows a breaking change.
- Define ownership for validation, authorization, mapping, error translation, pagination, and batching.
- Keep transport DTOs separate from domain and persistence models unless the repository already uses a deliberate shared model.
- Make nullability, optionality, default values, and error semantics explicit.
- Avoid leaking internal persistence fields, framework exceptions, stack traces, or security-sensitive data.

## GraphQL

- Define query/mutation fields, input types, output types, nullability, pagination, and authorization.
- Prefer bounded lists and cursor/page arguments for collection fields.
- Account for N+1 risks through batching, DataLoader, projections, or service aggregation.
- Keep resolvers thin: auth context, argument validation, use-case/service call, response mapping.

## gRPC And Protobuf

- Do not reuse field numbers. Mark removed fields as reserved when the project convention supports it.
- Use stable package and service naming. Prefer additive changes for compatibility.
- Model errors consistently through status codes, error details, or project-specific error envelopes.
- Keep request messages explicit about caller identity, resource identity, and pagination.

## REST And OpenAPI

- Use consistent resource naming, HTTP methods, status codes, idempotency, and error bodies.
- Validate path, query, header, and body inputs at the boundary.
- Define cache behavior and rate limits for public or expensive endpoints.

## Security And Tests

- Every protected API needs authentication and object-level authorization.
- Include contract tests or schema/proto generation checks when interface shape changes.
- Include negative tests for unauthorized, invalid input, missing resource, and compatibility-relevant defaults.
