---
name: workflow-guide-bootstrap
description: workflow-guide 플러그인의 rules, templates, skills 구조를 초기화하고 가이드 범위를 정리할 때 사용하는 부트스트랩 스킬.
argument-hint: "[가이드 범위 정리]"
---

# 워크플로우 가이드 부트스트랩

## 설명

이 스킬은 workflow-guide 플러그인의 초기 분리 단계에서 설계 원칙과 스캐폴딩 가이드 범위를 정의할 때 사용한다.

## 실행 절차

1. rules, templates, skills, agents, commands, tests 디렉토리 존재 여부를 확인한다.
2. 기존 references/templates 중 가이드 성격 자산을 선별한다.
3. 적용 우선순위(설계 원칙, 룰 설치, 스캐폴딩)를 정리한다.

## 검증

- `claude plugin validate ./plugins/workflow-guide`

## 주의사항

- 프로젝트 특화 규칙은 템플릿/placeholder로 일반화한다.
