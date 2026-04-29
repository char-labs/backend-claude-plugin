#!/usr/bin/env python3
"""Dependency-free develop-workflow hook regression tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADVISORY = ROOT / "scripts" / "advisory-feedback.py"
ROUTER = ROOT / "scripts" / "route-user-prompt.py"


def run(script: Path, payload: dict, *args: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(script), *args],
        input=json.dumps(payload),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=ROOT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def assert_advisory(name: str, payload: dict, mode: str = "post-tool") -> None:
    code, out = run(ADVISORY, payload, mode)
    assert code == 0, name
    data = json.loads(out)
    assert "systemMessage" in data, name


def assert_advisory_contains(name: str, payload: dict, expected: str, mode: str = "post-tool") -> None:
    code, out = run(ADVISORY, payload, mode)
    assert code == 0, name
    data = json.loads(out)
    assert expected in data.get("systemMessage", ""), name


def assert_route(name: str, prompt: str, expected_agent: str, expected_skill: str) -> None:
    code, out = run(ROUTER, {"prompt": prompt, "cwd": str(ROOT)})
    assert code == 0, name
    assert f'Task(subagent_type="{expected_agent}"' in out, name
    assert f"<!-- skill: {expected_skill} -->" in out, name


def assert_no_route(name: str, prompt: str) -> None:
    code, out = run(ROUTER, {"prompt": prompt, "cwd": str(ROOT)})
    assert code == 0, name
    assert out == "", name


def main() -> None:
    assert_advisory(
        "emits backend edit advisory",
        {"tool_name": "Write", "tool_input": {"file_path": "src/main/kotlin/App.kt"}},
    )
    assert_advisory_contains(
        "emits test minimalism advisory",
        {"tool_name": "Write", "tool_input": {"file_path": "src/test/kotlin/AppTest.kt"}},
        "비즈니스 로직",
    )
    assert_advisory_contains(
        "emits controller test confirmation advisory",
        {"tool_name": "Write", "tool_input": {"file_path": "src/test/kotlin/UserControllerTest.kt"}},
        "Controller/Presentation",
    )
    assert_advisory_contains(
        "emits entity relation policy advisory",
        {"tool_name": "Write", "tool_input": {"file_path": "src/main/kotlin/com/example/entity/PostEntity.kt"}},
        "scalar FK",
    )
    assert_advisory_contains(
        "emits repository port adapter advisory",
        {"tool_name": "Write", "tool_input": {"file_path": "src/main/kotlin/com/example/repository/UserCoreRepository.kt"}},
        "*CoreRepository",
    )
    assert_advisory("emits stop advisory", {"hook_event_name": "Stop"}, "stop")
    assert_route(
        "routes query work",
        "UserRepository findByNickname query is slow and may have N+1",
        "persistence-query-specialist",
        "persistence-query-review",
    )
    assert_route(
        "routes repository port adapter work",
        "UserRepository는 인터페이스로 두고 UserCoreRepository가 구현하게 해줘",
        "persistence-query-specialist",
        "persistence-query-review",
    )
    assert_route(
        "routes API contract work",
        "Define GraphQL input and response for profile update",
        "api-contract-designer",
        "api-contract-design",
    )
    assert_route(
        "routes API response envelope work",
        "Create ApiResponse and RestControllerAdvice response envelope for Spring REST API",
        "api-contract-designer",
        "api-response-contract",
    )
    assert_route(
        "routes test work",
        "CallService has a bug and needs regression tests",
        "backend-test-writer",
        "backend-test-strategy",
    )
    assert_no_route("does not route simple git request", "git log recent 5 commits")
    print("hook tests passed")


if __name__ == "__main__":
    main()
