"""Tests for rb_cli.reader module."""
from pathlib import Path

from rb_cli.reader import append_decision, append_to_memory, read_repobrain_context


def test_read_repobrain_context_empty(tmp_path: Path) -> None:
    """Returns empty dict when .repobrain/ does not exist."""
    assert read_repobrain_context(tmp_path) == {}


def test_read_repobrain_context_reads_md(tmp_path: Path) -> None:
    """Reads .md files from .repobrain/ directory."""
    rb_dir = tmp_path / ".repobrain"
    rb_dir.mkdir()
    (rb_dir / "rules.md").write_text("# Rules\nBe nice.", encoding="utf-8")
    (rb_dir / "conventions.md").write_text("# Conventions", encoding="utf-8")
    (rb_dir / "not-md.txt").write_text("ignored", encoding="utf-8")

    result = read_repobrain_context(tmp_path)
    assert "rules.md" in result
    assert "conventions.md" in result
    assert "not-md.txt" not in result
    assert "Be nice." in result["rules.md"]


def test_append_to_memory_creates_file(tmp_path: Path) -> None:
    """Creates memory file and appends entry."""
    path = append_to_memory(tmp_path, "reports.md", "Found a bug")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Found a bug" in content
    assert "UTC" in content


def test_append_to_memory_appends(tmp_path: Path) -> None:
    """Appends multiple entries to the same file."""
    append_to_memory(tmp_path, "reports.md", "First")
    append_to_memory(tmp_path, "reports.md", "Second")
    content = (tmp_path / ".repobrain" / "memory" / "reports.md").read_text(encoding="utf-8")
    assert "First" in content
    assert "Second" in content


def test_append_decision(tmp_path: Path) -> None:
    """Creates decision log with decision and rationale."""
    path = append_decision(tmp_path, "Use Redis", "Team familiar")
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Use Redis" in content
    assert "Team familiar" in content
    assert "**Decision:**" in content
    assert "**Rationale:**" in content
