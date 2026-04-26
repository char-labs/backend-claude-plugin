---
name: git-utils-bootstrap
description: git-utils 플러그인 초기 구조를 점검하고 안전한 Git 자동화 범위를 정의할 때 사용하는 부트스트랩 스킬.
argument-hint: "[Git 자동화 범위 점검]"
---

# Git Utils Bootstrap

## 설명

이 스킬은 git-utils 플러그인의 초기 분리 단계에서 스크립트 범위와 안전 가드레일을 정리할 때 사용한다.

## 실행 절차

1. commands, scripts, skills, hooks, tests 디렉토리 존재 여부를 확인한다.
2. git-safe-workflow 이관 범위(stage, commit, push, PR)를 확정한다.
3. destructive command 차단과 secret 보호 규칙을 검토한다.

## 검증

- `claude plugin validate ./plugins/git-utils`

## 주의사항

- 사용자 명시 요청 없이 push/PR 자동화를 수행하지 않는다.
