"""Tests for non-blocking ask freshness and health notices."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from repobrain_engine.hub.ask_pipeline import _build_workspace_health_notices


def _write_repobrain(tmp_path: Path, *, sha: str | None = "abc123") -> Path:
    rb_dir = tmp_path / ".repobrain"
    rb_dir.mkdir()
    if sha is not None:
        (rb_dir / ".last_refresh_sha").write_text(sha, encoding="utf-8")
    return rb_dir


def test_ask_fresh_workspace_has_no_notice(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_repobrain(tmp_path)

    def _fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="0\n", stderr="")

    monkeypatch.setattr("subprocess.run", _fake_run)

    assert _build_workspace_health_notices(tmp_path) == []


def test_ask_stale_workspace_reports_commit_lag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_repobrain(tmp_path)

    def _fake_run(*args, **kwargs):
        assert args[0] == ["git", "rev-list", "--count", "abc123..HEAD"]
        return subprocess.CompletedProcess(args[0], 0, stdout="3\n", stderr="")

    monkeypatch.setattr("subprocess.run", _fake_run)

    notices = _build_workspace_health_notices(tmp_path)

    assert notices == [
        "⚠ Knowledge base is 3 commit(s) behind HEAD -- consider running rb-refresh --quick."
    ]


def test_ask_missing_refresh_sha_silently_skips_freshness_check(
    tmp_path: Path,
) -> None:
    _write_repobrain(tmp_path, sha=None)

    assert _build_workspace_health_notices(tmp_path) == []


def test_ask_non_git_workspace_silently_skips_freshness_check(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_repobrain(tmp_path)

    def _fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 128, stdout="", stderr="fatal")

    monkeypatch.setattr("subprocess.run", _fake_run)

    assert _build_workspace_health_notices(tmp_path) == []


def test_ask_partial_status_reports_degraded_modules(tmp_path: Path) -> None:
    rb_dir = _write_repobrain(tmp_path, sha=None)
    (rb_dir / "status.json").write_text(
        json.dumps(
            {
                "refresh_run_id": "run",
                "overall_status": "partial",
                "modules": {
                    "api": "success",
                    "cli": "partial",
                    "worker": "failed",
                },
            }
        ),
        encoding="utf-8",
    )

    notices = _build_workspace_health_notices(tmp_path)

    assert notices == [
        "⚠ Knowledge base has partial/failed module knowledge for: cli, worker."
    ]


@pytest.mark.asyncio
async def test_ask_host_runner_prepends_workspace_health_notice(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("WORKSPACE_PATH", str(tmp_path))
    monkeypatch.setenv("RB_HOST_RUNNER", "codex")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_BASE_URL", raising=False)
    rb_dir = _write_repobrain(tmp_path)
    (rb_dir / "map.md").write_text("api: docs", encoding="utf-8")
    agents_dir = rb_dir / "agents"
    agents_dir.mkdir()
    (agents_dir / "api.md").write_text("agent docs", encoding="utf-8")

    from repobrain_engine.config import reset_settings

    reset_settings()

    async def _fake_host_runner(**kwargs):
        return "host answer"

    def _fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="1\n", stderr="")

    monkeypatch.setattr("repobrain_engine.hub.host_runner.run_host_runner", _fake_host_runner)
    monkeypatch.setattr("subprocess.run", _fake_run)

    from repobrain_engine.hub.ask_pipeline import ask_pipeline

    answer = await ask_pipeline(tmp_path, "What changed?")

    assert answer.startswith(
        "⚠ Knowledge base is 1 commit(s) behind HEAD -- consider running rb-refresh --quick.\n"
    )
    assert answer.endswith("host answer")
