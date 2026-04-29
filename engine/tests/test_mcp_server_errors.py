"""Tests for user-actionable ag-mcp error formatting."""

from __future__ import annotations

from pathlib import Path


def test_redact_secrets_covers_common_token_patterns() -> None:
    """Diagnostics should not persist common API key or auth token shapes."""
    from antigravity_engine.hub.mcp_server import _redact_secrets

    raw = (
        "OPENAI_API_KEY=sk-test-123456789 "
        "GOOGLE_API_KEY=AIzaSyTestSecret123456789 "
        "ANTHROPIC_API_KEY=anthropic-secret "
        "CUSTOM_API_KEY=custom-secret "
        "Authorization: Bearer auth-token-123 "
        "Bearer standalone-token-456 "
        "sk-live-abcdef123456789"
    )

    redacted = _redact_secrets(raw)

    assert "sk-test-123456789" not in redacted
    assert "AIzaSyTestSecret123456789" not in redacted
    assert "anthropic-secret" not in redacted
    assert "custom-secret" not in redacted
    assert "auth-token-123" not in redacted
    assert "standalone-token-456" not in redacted
    assert "sk-live-abcdef123456789" not in redacted
    assert "OPENAI_API_KEY=<redacted>" in redacted
    assert "GOOGLE_API_KEY=<redacted>" in redacted
    assert "ANTHROPIC_API_KEY=<redacted>" in redacted
    assert "CUSTOM_API_KEY=<redacted>" in redacted
    assert "Authorization: <redacted>" in redacted
    assert "Bearer <redacted>" in redacted


def test_mcp_log_permissions_are_private(tmp_path: Path, monkeypatch) -> None:
    """The diagnostic directory and log file should not be world-readable."""
    from antigravity_engine.hub.mcp_server import _log_mcp_event

    monkeypatch.setenv("CLAUDE_PLUGIN_DATA_DIR", str(tmp_path))

    log_path = _log_mcp_event("startup failed with OPENAI_API_KEY=sk-test-123456789")

    assert (tmp_path.stat().st_mode & 0o777) == 0o700
    assert (log_path.stat().st_mode & 0o777) == 0o600
    assert "sk-test-123456789" not in log_path.read_text(encoding="utf-8")


def test_format_tool_error_redacts_secrets_in_response_and_log(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """The full tool-error path must redact both user response and log."""
    from antigravity_engine.hub.mcp_server import _format_tool_error

    monkeypatch.setenv("CLAUDE_PLUGIN_DATA_DIR", str(tmp_path))
    raw_tokens = (
        "OPENAI_API_KEY=sk-test123fake",
        "Authorization: Bearer test456fake",
        "Bearer xyzfaketoken",
        "sk-fake789",
        "AIzafake000",
    )
    response = _format_tool_error(
        "refresh_project",
        RuntimeError("provider failed: " + " ".join(raw_tokens)),
    )
    log_text = (tmp_path / "ag-mcp.log").read_text(encoding="utf-8")

    assert "Diagnostic log:" in response
    for raw_token in raw_tokens:
        assert raw_token not in response
        assert raw_token not in log_text


def test_no_llm_error_points_to_setup_and_restart(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Missing LLM config should not look like an MCP registration failure."""
    from antigravity_engine.hub.mcp_server import _format_tool_error

    monkeypatch.setenv("CLAUDE_PLUGIN_DATA_DIR", str(tmp_path))

    text = _format_tool_error(
        "refresh_project",
        ValueError(
            "No LLM configured. Set GOOGLE_API_KEY, OPENAI_API_KEY, "
            "or OPENAI_BASE_URL in .env"
        ),
    )

    assert "/antigravity:setup" in text
    assert "restart Claude Code" in text
    assert (tmp_path / "ag-mcp.log").exists()


def test_generic_tool_error_includes_log_path(tmp_path: Path, monkeypatch) -> None:
    """Unexpected tool failures should expose the diagnostic log location."""
    from antigravity_engine.hub.mcp_server import _format_tool_error

    monkeypatch.setenv("CLAUDE_PLUGIN_DATA_DIR", str(tmp_path))

    text = _format_tool_error("refresh_project", RuntimeError("boom"))

    assert "Diagnostic log:" in text
    assert str(tmp_path / "ag-mcp.log") in text
