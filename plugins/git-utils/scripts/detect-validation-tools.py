#!/usr/bin/env python3
"""Detect existing validation commands without installing dependencies."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path.cwd()


def exists(path: str) -> bool:
    return (ROOT / path).exists()


commands: list[str] = []

if exists("gradlew"):
    commands.extend(["./gradlew test", "./gradlew ktlintCheck"])
    if exists("build.gradle.kts") or exists("settings.gradle.kts"):
        commands.append("./gradlew detekt")
elif exists("pom.xml"):
    commands.append("mvn test")

if exists("package.json"):
    commands.extend(["npm test", "npm run lint"])
if exists("go.mod"):
    commands.extend(["go test ./...", "go vet ./..."])
if exists("pyproject.toml") or exists("requirements.txt"):
    commands.extend(["pytest", "ruff check ."])
if exists("Cargo.toml"):
    commands.extend(["cargo test", "cargo clippy"])

print(json.dumps({"suggested_commands": commands}, indent=2))
