---
name: develop-workflow-bootstrap
description: develop-workflow 플러그인 초기 구조와 분리 상태를 점검할 때 사용하는 부트스트랩 스킬.
argument-hint: "[분리 상태 점검 또는 초기 스캐폴드 확인]"
---

# 개발 워크플로우 부트스트랩

## 설명

이 스킬은 develop-workflow 플러그인 초기 분리 단계에서 구조 점검과 다음 이관 대상을 정리할 때 사용한다.

## 실행 절차

1. agents, hooks, skills, scripts, templates, references, tests 디렉토리 존재 여부를 확인한다.
2. 기존 단일 플러그인에서 이관할 skill/agent 목록을 우선순위로 정리한다.
3. validate와 smoke-check(/help, /agents) 계획을 기록한다.

## 검증

- `claude plugin validate ./plugins/develop-workflow`

## 주의사항

- 실수 방지 가드레일: backend 개발 컨텍스트는 `develop-workflow`, Git guard는 `git-utils`, authoring guide는 `workflow-guide`가 소유하도록 중복을 만들지 않는다.

## 출력

현재 구조 점검 결과, 누락된 디렉토리/파일, 필요한 검증 명령을 요약한다.
