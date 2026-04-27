# 마이그레이션 플레이북

schema, data, storage, service, contract migration에서 이 자료를 사용한다.

## 계획 구조

- 현재 상태: data model, traffic, writer/reader, owner, dependency, known risk.
- 목표 상태: 원하는 model, compatibility contract, operational requirement, acceptance criteria.
- 전략: expand/contract, dual-write, backfill, replay, blue-green, strangler, big-bang 중 하나를 선택하고 명시적 근거를 둔다.
- rollout: stage, feature flag, traffic slice, validation gate, rollback point.
- 관측성: metric, log, alert, dashboard, manual check.

## 데이터 안전성

- 각 phase의 source of truth를 정의한다.
- backfill은 idempotent하고 resumable하게 만든다.
- duplicate write, lost update, partial replay, out-of-order event를 방지한다.
- count, checksum, constraint, business invariant를 검증한다.

## 호환성

- breaking change가 승인되지 않았다면 API/protobuf/schema compatibility를 보존한다.
- 필요하면 전환 중 old/new reader와 writer를 함께 지원한다.
- additive compatibility만으로 부족할 때만 message, column, event, endpoint에 version을 둔다.

## ADR 작성 트리거

- 새로운 storage technology, 새로운 service boundary, 큰 schema redesign, auth model 변경, consistency model 변경, external provider 교체.
