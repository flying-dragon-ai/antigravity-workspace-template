"""Tests for engine CLI entrypoint dispatch."""

from __future__ import annotations

import pytest


def test_engine_main_dispatches_ask(monkeypatch: pytest.MonkeyPatch) -> None:
    """engine_main dispatches ask subcommands to ask_main."""
    from repobrain_engine import _cli_entry

    calls: list[list[str]] = []

    monkeypatch.setattr(
        _cli_entry,
        "ask_main",
        lambda argv=None: calls.append(list(argv or [])),
    )

    _cli_entry.engine_main(["ask", "Where is auth?"])

    assert calls == [["Where is auth?"]]


def test_engine_main_dispatches_mcp(monkeypatch: pytest.MonkeyPatch) -> None:
    """engine_main dispatches mcp subcommands to mcp_main."""
    from repobrain_engine import _cli_entry

    calls: list[list[str]] = []

    monkeypatch.setattr(
        _cli_entry,
        "mcp_main",
        lambda argv=None: calls.append(list(argv or [])),
    )

    _cli_entry.engine_main(["mcp", "--workspace", "/tmp/project"])

    assert calls == [["--workspace", "/tmp/project"]]


def test_hub_main_dispatches_refresh(monkeypatch: pytest.MonkeyPatch) -> None:
    """hub_main dispatches refresh subcommands to refresh_main."""
    from repobrain_engine import _cli_entry

    calls: list[list[str]] = []

    monkeypatch.setattr(
        _cli_entry,
        "refresh_main",
        lambda argv=None: calls.append(list(argv or [])),
    )

    _cli_entry.hub_main(["refresh", "--quick"])

    assert calls == [["--quick"]]


def test_engine_main_rejects_unknown_subcommand() -> None:
    """engine_main exits with argparse usage on unknown subcommands."""
    from repobrain_engine import _cli_entry

    with pytest.raises(SystemExit) as exc_info:
        _cli_entry.engine_main(["unknown-command"])

    assert exc_info.value.code == 2


def test_ask_main_wraps_unexpected_exception_without_traceback(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Unexpected ask failures print one actionable line by default."""
    from repobrain_engine import _cli_entry

    monkeypatch.delenv("DEBUG_MODE", raising=False)
    monkeypatch.setattr(
        _cli_entry,
        "_diagnostic_log_path",
        lambda: "/tmp/rb-mcp.log",
    )
    monkeypatch.setattr(
        _cli_entry,
        "_run_ask_pipeline",
        lambda workspace, question: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    with pytest.raises(SystemExit) as exc_info:
        _cli_entry.ask_main(["Where is auth?", "--workspace", "."])

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "Error: RuntimeError: boom." in err
    assert "Run rb doctor" in err
    assert "Diagnostic log: /tmp/rb-mcp.log" in err
    assert "Traceback" not in err


def test_refresh_main_debug_mode_prints_traceback(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """DEBUG_MODE=1 preserves a full traceback for unexpected refresh errors."""
    from repobrain_engine import _cli_entry

    monkeypatch.setenv("DEBUG_MODE", "1")
    monkeypatch.setattr(
        _cli_entry,
        "_diagnostic_log_path",
        lambda: "/tmp/rb-mcp.log",
    )

    def fail_refresh(workspace, *, quick: bool, failed_only: bool):
        raise RuntimeError("refresh failed")

    monkeypatch.setattr(_cli_entry, "_run_refresh_pipeline", fail_refresh)

    with pytest.raises(SystemExit) as exc_info:
        _cli_entry.refresh_main(["--workspace", "."])

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "Error: RuntimeError: refresh failed." in err
    assert "Diagnostic log: /tmp/rb-mcp.log" in err
    assert "Traceback" in err
    assert "RuntimeError: refresh failed" in err


def test_ask_main_keyboard_interrupt_exits_130(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """KeyboardInterrupt exits 130 and does not print a traceback."""
    from repobrain_engine import _cli_entry

    monkeypatch.setattr(
        _cli_entry,
        "_run_ask_pipeline",
        lambda workspace, question: (_ for _ in ()).throw(KeyboardInterrupt()),
    )

    with pytest.raises(SystemExit) as exc_info:
        _cli_entry.ask_main(["Where is auth?", "--workspace", "."])

    assert exc_info.value.code == 130
    err = capsys.readouterr().err
    assert "Traceback" not in err
