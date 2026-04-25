# Design Decision Template

Use this structure when planning backend architecture or implementation.

```text
Goal:
Success criteria:
Constraints:

Proposed design:
- Boundary:
- Data flow:
- Transaction model:
- Authorization model:
- Error model:
- Performance considerations:
- Observability:

Alternatives considered:
- Option:
- Tradeoff:

Validation:
- Unit tests:
- Integration tests:
- Security checks:
- Performance checks:
```

Rules:

- Make dependency direction explicit.
- Name the owning layer for validation, authorization, transaction control, persistence, and external calls.
- Prefer the smallest design that satisfies the success criteria.
