---
name: migration-adr
description: DB 스키마 변경, 데이터 backfill, storage 전환, 서비스 분리, 호환성, rollout/rollback, validation, observability를 포함한 백엔드 migration 또는 ADR을 계획할 때 사용.
argument-hint: "[마이그레이션 또는 ADR 작업]"
---

# Migration ADR

## 설명

사용자 요청이 단계적 rollout, 데이터 안전성, 하위 호환성, 아키텍처 의사결정 기록을 필요로 할 때 사용한다.

## 상세 자료

아래 자료는 필요한 경우에만, 나열된 순서로 읽는다.

- `${CLAUDE_PLUGIN_ROOT}/references/migration-playbook.md`
- `${CLAUDE_PLUGIN_ROOT}/references/architecture-principles.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md`
- `${CLAUDE_PLUGIN_ROOT}/templates/task-plan-template.md`

## 실행 절차

1. 현재 상태, 목표 상태, owner, compatibility constraint, 성공 기준을 식별한다.
2. migration strategy를 고른다: expand/contract, dual-write, backfill, replay, blue-green, strangler, big-bang. 선택 이유를 남긴다.
3. rollout phase, validation gate, rollback, 각 단계의 source of truth를 정의한다.
4. metrics, logs, alerts, dashboard, manual check 등 observability를 포함한다.
5. 기술 선택, storage, service boundary, contract, authorization이 바뀌면 ADR을 작성한다.

## 검증

- dry-run, shadow read, sampled reconciliation, count/hash 비교 같은 검증 방식을 정한다.
- rollback 가능 조건과 불가능 조건을 명시한다.
- 운영 지표와 alert threshold를 migration phase별로 둔다.

## 주의사항

- 실수 방지 가드레일: rollout, rollback, reconciliation, alert threshold를 migration plan에 함께 둔다.
- 데이터 삭제/스키마 축소는 contract consumer와 backfill 완료가 확인된 뒤에만 계획한다.
- dual-write나 replay에는 idempotency와 재처리 전략을 포함한다.
- 민감 데이터 이관에는 암호화, 접근권한, audit log를 포함한다.

## 출력

단계별 migration plan 또는 ADR-ready decision record를 반환한다.
