#!/usr/bin/env python3
"""Run route-user-prompt.py against routing fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ROUTER = ROOT / "scripts" / "route-user-prompt.py"
CASES = Path(__file__).with_name("test-cases.json")


def main() -> None:
    failures: list[str] = []
    cases = json.loads(CASES.read_text())
    for case in cases:
        payload = {"prompt": case["prompt"], "cwd": str(ROOT)}
        result = subprocess.run(
            [sys.executable, str(ROUTER)],
            input=json.dumps(payload),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
            check=False,
        )
        out = result.stdout
        expected_agent = case["expected_agent"]
        expected_skill = case["expected_skill"]
        if expected_agent is None:
            if out.strip():
                failures.append(f"{case['id']}: expected no route, got output")
            continue
        if f'Task(subagent_type="{expected_agent}"' not in out:
            failures.append(f"{case['id']}: missing agent {expected_agent}")
        if f"<!-- skill: {expected_skill} -->" not in out:
            failures.append(f"{case['id']}: missing skill hint {expected_skill}")

    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"routing tests passed ({len(cases)} cases)")


if __name__ == "__main__":
    main()
