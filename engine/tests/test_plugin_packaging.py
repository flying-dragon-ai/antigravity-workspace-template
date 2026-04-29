"""Regression tests for Claude/Codex plugin packaging files."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_MCP_TOOL_PREFIX = "mcp__plugin_antigravity_antigravity__"
PLUGIN_VERSION = "0.2.1"


def test_plugin_versions_are_in_sync() -> None:
    """Claude, Codex, marketplace, and engine package versions stay aligned."""
    manifest = json.loads(
        (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    codex_manifest = json.loads(
        (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    engine_pyproject = (REPO_ROOT / "engine" / "pyproject.toml").read_text(
        encoding="utf-8"
    )
    engine_init = (
        REPO_ROOT / "engine" / "antigravity_engine" / "__init__.py"
    ).read_text(encoding="utf-8")

    assert manifest["version"] == PLUGIN_VERSION
    assert codex_manifest["version"] == PLUGIN_VERSION
    assert marketplace["plugins"][0]["version"] == PLUGIN_VERSION
    assert f'version = "{PLUGIN_VERSION}"' in engine_pyproject
    assert f'__version__ = "{PLUGIN_VERSION}"' in engine_init


def test_claude_manifest_uses_dedicated_mcp_config() -> None:
    manifest = json.loads(
        (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )

    assert manifest["mcpServers"] == "./.mcp.json"


def test_mcp_config_passes_workspace_to_ag_mcp() -> None:
    config = json.loads((REPO_ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["antigravity"]

    assert server["command"] == "ag-mcp"
    assert server["args"] == ["--workspace", "${CLAUDE_PROJECT_DIR}"]
    assert server["env"]["WORKSPACE_PATH"] == "${CLAUDE_PROJECT_DIR}"


def test_slash_commands_allow_plugin_prefixed_mcp_tools() -> None:
    ask_command = (REPO_ROOT / "commands" / "ag-ask.md").read_text(encoding="utf-8")
    refresh_command = (REPO_ROOT / "commands" / "ag-refresh.md").read_text(
        encoding="utf-8"
    )

    assert f"{PLUGIN_MCP_TOOL_PREFIX}ask_project" in ask_command
    assert f"{PLUGIN_MCP_TOOL_PREFIX}refresh_project" in refresh_command
    assert "mcp__antigravity__ask_project" not in ask_command
    assert "mcp__antigravity__refresh_project" not in refresh_command


def test_legacy_unprefixed_mcp_tool_names_do_not_reappear() -> None:
    """Repo text should not route users back to the non-plugin MCP names."""
    legacy_names = (
        "mcp__antigravity__ask_project",
        "mcp__antigravity__refresh_project",
    )
    skipped_parts = {
        ".git",
        ".pytest_cache",
        "__pycache__",
        "venv",
        ".venv",
        "antigravity_workspace_template_venv",
    }
    searchable_suffixes = {".md", ".json", ".py", ".toml"}
    this_file = Path(__file__).resolve()
    hits: list[str] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.resolve() == this_file:
            continue
        if any(part in skipped_parts for part in path.parts):
            continue
        if path.suffix not in searchable_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for legacy_name in legacy_names:
            if legacy_name in text:
                hits.append(f"{path.relative_to(REPO_ROOT)}: {legacy_name}")

    assert hits == []
