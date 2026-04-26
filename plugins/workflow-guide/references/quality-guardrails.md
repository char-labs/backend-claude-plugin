# Quality Guardrails Reference

이 문서는 workflow-guide의 skill, rule, template 작성에 자연스럽게 적용되는 실수 방지 원칙이다. 별도 workflow로 호출하기보다 스킬 작성, 룰 정리, 템플릿 설계, 테스트 갱신 안에서 기본 검증 습관으로 사용한다.

## 원칙

- 지시문보다 실행 가능한 검증을 우선한다.
- 변경이 routing, hook, fixture, 문서 정책, cache hygiene에 영향을 주면 관련 회귀 테스트를 함께 갱신한다.
- 자동 gate는 가능한 code-based grading으로 둔다: JSON schema, string match, exit code, fixture assertion.
- LLM judge나 prompt/agent hook은 비용, 지연, 재현성 리스크가 있으므로 기본 차단 gate로 두지 않는다.
- positive, negative, ambiguous, Korean/natural language 케이스를 분리해 회귀 원인을 좁힌다.
- hook은 사용자 권한으로 자동 실행되므로 입력 JSON 검증, shell quoting, path traversal 차단, 민감 파일 보호를 기본값으로 둔다.
- 문서 앞쪽에는 사용자 요청 원문, 날짜, 개인 로컬 절대경로처럼 호출마다 바뀌는 값을 두지 않는다.

## 기본 검증 묶음

```bash
claude plugin validate backend-claude-plugin/plugins/workflow-guide
```

## 적용 지점

| 작업 | 가드레일 |
|---|---|
| Skill/agent 문서 수정 | frontmatter, section 구조, cache hygiene 정책 테스트 |
| Routing 변경 | positive/negative/ambiguous/Korean fixture 추가 |
| Hook 변경 | blocked case와 allowed case를 함께 추가 |
| Review doctrine 변경 | finding template과 focused review skill 영향 확인 |
| Security guard 변경 | false positive와 false negative fixture 모두 추가 |
| Build/test 안내 변경 | repo에 존재하는 명령만 사용하고 자동 설치 금지 |
