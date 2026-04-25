#!/usr/bin/env python3
"""PreToolUse guard for backend-quality-workflow.

Blocks high-risk tool calls. The script is intentionally conservative and
dependency-free because plugin hooks run with the user's permissions.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath


SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

SENSITIVE_SUFFIXES = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".jks",
    ".keystore",
    ".crt",
    ".cer",
}

PROD_CONFIG_RE = re.compile(
    r"(^|/)(application|bootstrap|config)[-.](prod|production)\.(yml|yaml|properties|json)$",
    re.IGNORECASE,
)

SECRET_RE = re.compile(
    r"(^|/)(secrets?|credentials?|private[-_]?key|service[-_]?account)(\.|/|$)",
    re.IGNORECASE,
)

DANGEROUS_COMMAND_PATTERNS = [
    (re.compile(r"(^|[;&|]\s*)rm\s+(-[^\s]*r[^\s]*f|-f[^\s]*r|-r[^\s]*f)\s+(/|\*|\.|~)(\s|$)"), "destructive rm command"),
    (re.compile(r"(^|[;&|]\s*)git\s+reset\s+--hard(\s|$)"), "destructive git reset"),
    (re.compile(r"(^|[;&|]\s*)git\s+clean\s+-[^\s]*[fd][^\s]*(\s|$)"), "destructive git clean"),
    (re.compile(r"(^|[;&|]\s*)chmod\s+-R\s+777(\s|$)"), "world-writable recursive chmod"),
    (re.compile(r"(^|[;&|]\s*)sudo(\s|$)"), "sudo command"),
    (re.compile(r"(^|[;&|]\s*)mkfs(\.| \s|$)"), "filesystem formatting command"),
    (re.compile(r"(^|[;&|]\s*)dd\s+.*\bof=/dev/"), "raw device write"),
    (re.compile(r":\s*\(\s*\)\s*\{\s*:\s*\|\s*:"), "shell fork bomb pattern"),
    (re.compile(r"\b(curl|wget)\b[^|;&]*\|\s*(sh|bash|zsh|python|python3|ruby|perl|node)\b"), "remote download piped to interpreter"),
]


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"backend-quality-workflow blocked this action: {reason}",
                }
            }
        )
    )
    sys.exit(0)


def load_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        deny("hook input was not valid JSON")
    if not isinstance(data, dict):
        deny("hook input JSON must be an object")
    return data


def has_path_traversal(path_value: str) -> bool:
    posix_parts = PurePosixPath(path_value.replace("\\", "/")).parts
    windows_parts = PureWindowsPath(path_value).parts
    return ".." in posix_parts or ".." in windows_parts


def normalize_path(path_value: str) -> Path:
    if "\x00" in path_value:
        deny("file path contains a null byte")
    if has_path_traversal(path_value):
        deny(f"path traversal is not allowed: {path_value}")

    project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    candidate = Path(path_value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    resolved = candidate.resolve(strict=False)

    try:
        resolved.relative_to(project_root)
    except ValueError:
        deny(f"write target is outside project root: {path_value}")

    return resolved


def path_is_sensitive(path_value: str) -> bool:
    normalized = path_value.replace("\\", "/")
    name = Path(normalized).name
    lower_name = name.lower()
    lower_path = normalized.lower()

    if lower_name in SENSITIVE_NAMES or lower_name.startswith(".env."):
        return True
    if any(lower_name.endswith(suffix) for suffix in SENSITIVE_SUFFIXES):
        return True
    if PROD_CONFIG_RE.search(lower_path):
        return True
    if SECRET_RE.search(lower_path):
        return True
    if lower_path.startswith(".git/") or "/.git/" in lower_path or lower_path.endswith("/.git"):
        return True
    return False


def check_bash(command: object) -> None:
    if not isinstance(command, str):
        deny("Bash command must be a string")
    command_one_line = " ".join(command.split())
    for pattern, reason in DANGEROUS_COMMAND_PATTERNS:
        if pattern.search(command_one_line):
            deny(reason)


def iter_tool_paths(tool_input: dict) -> list[str]:
    paths: list[str] = []
    for key in ("file_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str):
            paths.append(value)
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict):
                value = edit.get("file_path") or edit.get("path")
                if isinstance(value, str):
                    paths.append(value)
    return paths


def check_read_paths(tool_input: dict) -> None:
    for path_value in iter_tool_paths(tool_input):
        if "\x00" in path_value:
            deny("file path contains a null byte")
        if has_path_traversal(path_value):
            deny(f"path traversal is not allowed: {path_value}")
        if path_is_sensitive(path_value):
            deny(f"sensitive credential/config file read: {path_value}")


def check_write_paths(tool_input: dict) -> None:
    for path_value in iter_tool_paths(tool_input):
        resolved = normalize_path(path_value)
        if path_is_sensitive(path_value) or path_is_sensitive(str(resolved)):
            deny(f"sensitive or production credential/config file write: {path_value}")


def main() -> None:
    data = load_input()
    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input", {})
    if not isinstance(tool_input, dict):
        deny("tool_input must be an object")

    if tool_name == "Bash":
        check_bash(tool_input.get("command"))
    elif tool_name == "Read":
        check_read_paths(tool_input)
    elif tool_name in {"Write", "Edit", "MultiEdit", "NotebookEdit"}:
        check_write_paths(tool_input)


if __name__ == "__main__":
    main()
