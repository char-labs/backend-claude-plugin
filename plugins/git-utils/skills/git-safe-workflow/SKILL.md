---
name: git-safe-workflow
description: 백엔드 변경 후 branch, commit, push, PR을 안전하게 준비할 때 사용하는 수동 전용 Git workflow. 사용자가 명시적으로 commit, push, PR, branch 작업을 요청한 경우에만 사용.
argument-hint: "[커밋, 푸시, PR, 브랜치 작업]"
disable-model-invocation: true
---

# Git Safe Workflow

## 설명

사용자 요청을 안전한 Git 작업으로 처리한다. 이 skill은 자동 호출을 막고, 사용자가 명시적으로 Git 작업을 요청한 경우에만 사용한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/scripts/detect-validation-tools.py`

## 실행 절차

1. `git status --short`로 현재 변경 상태를 먼저 확인한다.
2. 사용자 변경과 이번 작업 변경을 분리한다. 관련 없는 사용자 변경을 되돌리지 않는다.
3. diff를 확인한 뒤 요청 범위에 속한 파일만 stage한다.
4. 가능하면 관련 validation을 실행한다. `${CLAUDE_PLUGIN_ROOT}/scripts/detect-validation-tools.py`로 기존 명령을 확인하되 도구를 자동 설치하지 않는다.
5. commit message는 구현 세부보다 변경된 동작을 짧게 표현한다.
6. push 또는 PR 생성은 사용자가 명시적으로 요청한 경우에만 수행한다.

## 검증

- stage 전후 `git status --short`를 확인한다.
- commit 전 가능하면 관련 compile/test/lint를 실행한다.
- 검증을 실행하지 못한 경우 이유와 residual risk를 남긴다.

## 주의사항

- 실수 방지 가드레일: stage 전후 상태와 diff 범위를 확인하고, 관련 없는 사용자 변경을 커밋에 섞지 않는다.
- Do not run destructive commands such as `git reset --hard`, `git clean -fd`, or broad restore commands unless the user explicitly requests them.
- Do not include secrets, `.env`, private keys, production credentials, or local config in commits.
- If validation cannot run, state why and include residual risk.

## 출력

stage/commit/push/PR 여부, 포함된 파일 범위, 실행한 검증, 남은 위험을 요약한다.
