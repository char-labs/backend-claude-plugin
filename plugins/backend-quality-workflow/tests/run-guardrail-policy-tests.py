#!/usr/bin/env python3
"""Strict guardrail policy tests for backend-quality-workflow."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]


def fail(message: str) -> None:
    raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_unique_case_ids() -> None:
    cases_path = ROOT / "tests" / "eval" / "routing" / "test-cases.json"
    cases = json.loads(read(cases_path))
    seen: set[str] = set()
    required = {"id", "type", "prompt", "expected_agent", "expected_skill"}
    for case in cases:
        missing = required - case.keys()
        if missing:
            fail(f"routing case missing fields {missing}: {case}")
        case_id = case["id"]
        if case_id in seen:
            fail(f"duplicate routing case id: {case_id}")
        seen.add(case_id)
        agent = case["expected_agent"]
        skill = case["expected_skill"]
        if (agent is None) != (skill is None):
            fail(f"routing case must set both expected_agent and expected_skill together: {case_id}")
        if case["type"] == "negative" and (agent is not None or skill is not None):
            fail(f"negative routing case must not expect a route: {case_id}")
        if case["type"] != "negative" and (agent is None or skill is None):
            fail(f"positive routing case must expect a route: {case_id}")


def assert_hook_policy() -> None:
    hooks_path = ROOT / "hooks" / "hooks.json"
    config = json.loads(read(hooks_path))
    hooks = config.get("hooks")
    if not isinstance(hooks, dict):
        fail("hooks.json must contain a hooks object")
    for event_name, groups in hooks.items():
        if not isinstance(groups, list):
            fail(f"{event_name} groups must be a list")
        for group in groups:
            handlers = group.get("hooks")
            if not isinstance(handlers, list) or not handlers:
                fail(f"{event_name} group must contain hook handlers")
            for handler in handlers:
                if handler.get("type") != "command":
                    fail(f"{event_name} uses non-command hook type: {handler.get('type')}")
                command = handler.get("command")
                if not isinstance(command, str) or "${CLAUDE_PLUGIN_ROOT}" not in command:
                    fail(f"{event_name} command must reference ${{CLAUDE_PLUGIN_ROOT}}: {command}")
                timeout = handler.get("timeout")
                if not isinstance(timeout, int) or timeout < 1 or timeout > 10:
                    fail(f"{event_name} command timeout must be 1..10 seconds: {timeout}")


def assert_skill_docs() -> None:
    forbidden = [
        re.compile(r"/Users/"),
        re.compile(r"Last updated", re.IGNORECASE),
        re.compile(r"Generated at", re.IGNORECASE),
    ]
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = read(path)
        for pattern in forbidden:
            if pattern.search(text):
                fail(f"forbidden dynamic/local marker in skill: {path}")
        if "$ARGUMENTS" in text:
            fail(f"$ARGUMENTS should not appear in skill body: {path}")
        for section in ("## 설명", "## 실행 절차", "## 검증", "## 주의사항", "## 출력"):
            if section not in text:
                fail(f"missing {section} in {path}")
        if "## 상세 자료" in text and "아래 자료는 필요한 경우에만, 나열된 순서로 읽는다." not in text:
            fail(f"missing deterministic reference loading rule in {path}")
        if "실수 방지 가드레일" not in text:
            fail(f"missing mistake-prevention guardrail in {path}")


def assert_agent_docs() -> None:
    for path in sorted((ROOT / "agents").glob("*.md")):
        text = read(path)
        if "/Users/" in text or "$ARGUMENTS" in text:
            fail(f"dynamic/local marker in agent doc: {path}")
        for section in ("## 역할", "## 스킬 활성화", "## 상세 자료", "## 실행 규칙", "## 출력"):
            if section not in text:
                fail(f"missing {section} in {path}")
        if "아래 자료는 필요한 경우에만, 나열된 순서로 읽습니다." not in text:
            fail(f"missing deterministic reference loading rule in {path}")
        if "실수 방지 가드레일" not in text:
            fail(f"missing mistake-prevention guardrail in {path}")


def assert_no_explicit_standalone_guardrail_component() -> None:
    forbidden = ("harness-engineering", "harness-engineer")
    for path in [ROOT / "scripts" / "route-user-prompt.py", ROOT / "tests" / "eval" / "routing" / "test-cases.json"]:
        text = read(path)
        for marker in forbidden:
            if marker in text:
                fail(f"explicit standalone guardrail component marker must not be routed or exposed: {marker} in {path}")
    if (ROOT / "skills" / "harness-engineering").exists():
        fail("harness-engineering must not be exposed as a standalone skill")
    if (ROOT / "agents" / "harness-engineer.md").exists():
        fail("harness-engineer must not be exposed as a standalone agent")


def assert_gitignore_noise_policy() -> None:
    gitignore = REPO / ".gitignore"
    if not gitignore.exists():
        fail("repo must contain .gitignore")
    lines = {line.strip() for line in read(gitignore).splitlines()}
    for pattern in (".DS_Store", "__pycache__/", "*.py[cod]"):
        if pattern not in lines:
            fail(f".gitignore must ignore local/generated noise: {pattern}")


def assert_test_minimalism_policy() -> None:
    required_files = [
        ROOT / "skills" / "backend-test-strategy" / "SKILL.md",
        ROOT / "agents" / "backend-test-writer.md",
        ROOT / "references" / "testing-strategy.md",
        ROOT / "scripts" / "advisory-feedback.py",
    ]
    for path in required_files:
        text = read(path)
        for marker in ("비즈니스 로직", "회귀 위험"):
            if marker not in text:
                fail(f"test minimalism policy must mention {marker}: {path}")
    strategy = read(ROOT / "references" / "testing-strategy.md")
    for marker in ("simple DTOs", "constants", "compile"):
        if marker not in strategy:
            fail(f"testing strategy must document no-test cases: {marker}")


def assert_test_db_and_controller_policy() -> None:
    required_files = [
        ROOT / "skills" / "backend-test-strategy" / "SKILL.md",
        ROOT / "agents" / "backend-test-writer.md",
        ROOT / "references" / "testing-strategy.md",
        ROOT / "references" / "spring-kotlin-backend.md",
        ROOT / "scripts" / "advisory-feedback.py",
    ]
    for path in required_files:
        text = read(path)
        for marker in ("실 DB", "@Transactional"):
            if marker not in text:
                fail(f"test DB/controller policy must mention {marker}: {path}")
        if "Controller/Presentation" not in text and "Presentation/Controller" not in text:
            fail(f"test DB/controller policy must mention Controller/Presentation or Presentation/Controller: {path}")


def main() -> None:
    assert_unique_case_ids()
    assert_hook_policy()
    assert_skill_docs()
    assert_agent_docs()
    assert_no_explicit_standalone_guardrail_component()
    assert_gitignore_noise_policy()
    assert_test_minimalism_policy()
    assert_test_db_and_controller_policy()
    print("guardrail policy tests passed")


if __name__ == "__main__":
    main()
