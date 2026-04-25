# Review Finding Template

Use this structure for review output.

## Findings

Each finding should use:

```text
[Severity] Title
Evidence: file:line and the exact behavior observed.
Impact: concrete failure, exploit, bottleneck, or maintenance risk.
Fix: specific code-level change.
Tests: scenario or command that should prove the fix.
```

Severity values:

- Critical
- High
- Medium
- Low

If no issues are found:

```text
No blocking findings.
Residual risk: name any area not validated, such as runtime config, production permissions, or load behavior.
Suggested validation: commands or manual checks to run.
```

Rules:

- Lead with findings, ordered by severity.
- Do not list style preferences as findings unless they affect correctness, security, performance, or maintainability.
- Include file and line references when available.
- Keep recommendations concrete enough for another engineer to implement.
