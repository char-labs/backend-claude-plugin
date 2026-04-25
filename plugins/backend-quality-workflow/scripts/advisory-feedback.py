#!/usr/bin/env python3
"""Advisory hook output for backend-quality-workflow."""

from __future__ import annotations

import json
import sys
from pathlib import Path


BACKEND_SUFFIXES = {
    ".java",
    ".kt",
    ".kts",
    ".go",
    ".py",
    ".rb",
    ".rs",
    ".cs",
    ".ts",
    ".js",
    ".sql",
    ".yml",
    ".yaml",
    ".properties",
    ".gradle",
}


def load_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def emit(message: str) -> None:
    print(json.dumps({"systemMessage": message}))


def backendish(path: str) -> bool:
    suffix = Path(path).suffix.lower()
    lowered = path.replace("\\", "/").lower()
    return suffix in BACKEND_SUFFIXES or "/src/main/" in lowered or "/server/" in lowered or "/backend/" in lowered


def post_tool(data: dict) -> None:
    tool_input = data.get("tool_input", {})
    if not isinstance(tool_input, dict):
        return
    path = tool_input.get("file_path") or tool_input.get("path")
    if not isinstance(path, str) or not backendish(path):
        return
    emit(
        "Backend quality 안내: 백엔드 변경이라면 인가/권한, 입력 검증, 트랜잭션 경계, 쿼리 형태, 오류 처리, 민감정보 로깅, 집중 테스트를 확인하세요."
    )


def stop() -> None:
    emit(
        "Backend quality 종료 안내: 백엔드 동작이 바뀌었다면 최종 응답에 수행한 검증과 남은 보안/성능/아키텍처 리스크를 명시하세요."
    )


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "post-tool"
    data = load_input()
    if mode == "stop":
        stop()
    else:
        post_tool(data)


if __name__ == "__main__":
    main()
