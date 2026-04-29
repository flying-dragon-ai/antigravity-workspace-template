"""Antigravity Knowledge Hub — MCP Server.

Exposes `ask_project` and `refresh_project` as MCP tools so that
Claude Code (and any MCP-compatible AI IDE) can query the project
knowledge base without doing its own grep/file search.

Usage (stdio transport):
    python -m antigravity_engine.hub.mcp_server --workspace /path/to/project

Or via the installed entry-point:
    ag-mcp --workspace /path/to/project

Then configure in Claude Code's MCP settings (~/.claude/mcp.json):
    {
      "mcpServers": {
        "antigravity": {
          "command": "ag-mcp",
          "args": ["--workspace", "/path/to/your/project"]
        }
      }
    }
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path


def _resolve_workspace(workspace: str | None) -> Path:
    """Resolve workspace path from argument, env, or upward-scan from cwd.

    Resolution order:
      1. --workspace argument (if usable)
      2. WORKSPACE_PATH env var (if usable)
      3. Walk up from cwd looking for a `.env` or `.git` marker — the
         common signature of a project root. This rescues cases where an
         MCP host doesn't substitute variables and spawns the server from
         a non-project cwd (cache dir, /, etc.).
      4. cwd as last resort.

    Treats values containing un-expanded `${...}` placeholders as missing.
    """
    def _usable(v: str | None) -> bool:
        return bool(v) and "${" not in v

    if _usable(workspace):
        resolved = Path(workspace).resolve()
        print(f"[ag-mcp] workspace from --arg: {resolved}", file=sys.stderr)
        return resolved
    env = os.environ.get("WORKSPACE_PATH", "")
    if _usable(env):
        resolved = Path(env).resolve()
        print(f"[ag-mcp] workspace from WORKSPACE_PATH env: {resolved}", file=sys.stderr)
        return resolved

    cwd = Path.cwd().resolve()
    for d in [cwd, *cwd.parents]:
        if (d / ".env").is_file() or (d / ".git").exists():
            print(
                f"[ag-mcp] workspace auto-detected by scanning up from cwd ({cwd}): {d}",
                file=sys.stderr,
            )
            return d
    print(f"[ag-mcp] workspace fallback to cwd (no .env/.git found upward): {cwd}", file=sys.stderr)
    return cwd


# Active workspace is module-level so MCP roots can upgrade it on the first
# tool call after the protocol handshake completes. Initialized by serve().
_active_workspace: Path | None = None
_roots_attempted = False


def _root_uri_to_path(uri: str) -> Path | None:
    """Convert an MCP file:// root URI to a filesystem Path."""
    from urllib.parse import unquote, urlparse

    parsed = urlparse(uri)
    if parsed.scheme != "file":
        return None
    raw = unquote(parsed.path or "")
    if not raw:
        return None
    return Path(raw).resolve()


async def _maybe_upgrade_via_roots(ctx) -> None:
    """If the MCP client supports the `roots` protocol, prefer its root.

    MCP clients (Claude Code, Cursor, etc.) typically advertise the open
    project as a workspace root. Asking the client directly is the most
    reliable workspace source — better than args (host may not substitute
    variables), better than env (same), better than cwd-scan (may pick a
    nested git repo or miss entirely).

    Idempotent: only attempts once per process. On success, updates
    `_active_workspace`, sets WORKSPACE_PATH env var, and resets the
    cached Settings so the new project's `.env` is read on next access.
    """
    global _active_workspace, _roots_attempted
    if _roots_attempted:
        return
    _roots_attempted = True

    try:
        result = await ctx.request_context.session.list_roots()
    except Exception as exc:  # noqa: BLE001 — client may not support roots
        print(f"[ag-mcp] MCP roots/list unavailable ({exc.__class__.__name__}): keeping workspace = {_active_workspace}", file=sys.stderr)
        return

    if not result.roots:
        print(f"[ag-mcp] MCP roots/list returned empty list: keeping workspace = {_active_workspace}", file=sys.stderr)
        return

    new_workspace = _root_uri_to_path(str(result.roots[0].uri))
    if new_workspace is None or not new_workspace.exists():
        print(f"[ag-mcp] MCP roots/list returned unusable URI {result.roots[0].uri!r}: keeping workspace = {_active_workspace}", file=sys.stderr)
        return

    if new_workspace == _active_workspace:
        print(f"[ag-mcp] MCP roots confirmed workspace = {_active_workspace}", file=sys.stderr)
        return

    print(f"[ag-mcp] upgrading workspace via MCP roots: {_active_workspace} → {new_workspace}", file=sys.stderr)
    _active_workspace = new_workspace
    os.environ["WORKSPACE_PATH"] = str(new_workspace)
    try:
        from antigravity_engine.config import reset_settings

        reset_settings()
    except Exception:  # noqa: BLE001
        pass


def serve(workspace: Path) -> None:
    """Start the MCP server on stdio.

    Args:
        workspace: Initial workspace guess from CLI/env/cwd-scan. Will be
            upgraded to the MCP client's reported root on the first tool call
            if the client supports the `roots` protocol.
    """
    global _active_workspace
    _active_workspace = workspace

    from mcp.server.fastmcp import Context, FastMCP

    mcp = FastMCP(
        "Antigravity Knowledge Hub",
        instructions=(
            "Use ask_project to answer any question about the codebase — "
            "where code lives, why decisions were made, how things work. "
            "Use refresh_project to rebuild the project knowledge base after "
            "significant changes. Prefer ask_project over manual file search."
        ),
    )

    @mcp.tool()
    async def ask_project(question: str, ctx: Context) -> str:
        """Answer a question about the project using the knowledge hub.

        Searches the codebase, reads actual source files, checks git history,
        and synthesizes a grounded answer with file paths and line numbers.
        Use this instead of manual grep or file reading.

        Args:
            question: Natural language question about the project, e.g.
                "Where is the authentication logic?",
                "Why was the JWT migration done?",
                "What does the Scanner class do?"

        Returns:
            Grounded answer with file paths, line numbers, and context.
        """
        await _maybe_upgrade_via_roots(ctx)
        from antigravity_engine.hub.pipeline import ask_pipeline

        try:
            return await ask_pipeline(_active_workspace, question)
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    @mcp.tool()
    async def refresh_project(quick: bool = False, ctx: Context = None) -> str:
        """Rebuild the project knowledge base (.antigravity/conventions.md and structure.md).

        Run this after significant code changes to keep the knowledge base
        up to date. Use quick=True to only scan files changed since the
        last refresh.

        Args:
            quick: If True, only scan files changed since the last refresh.
                   Faster but may miss some changes.

        Returns:
            Confirmation message with updated file paths.
        """
        if ctx is not None:
            await _maybe_upgrade_via_roots(ctx)
        from antigravity_engine.hub.pipeline import refresh_pipeline

        try:
            await refresh_pipeline(_active_workspace, quick=quick)
            ag_dir = _active_workspace / ".antigravity"
            return (
                f"Knowledge base updated:\n"
                f"  {ag_dir / 'conventions.md'}\n"
                f"  {ag_dir / 'structure.md'}"
            )
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"

    mcp.run(transport="stdio")


def main() -> None:
    """Entry point for ag-mcp CLI command."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="ag-mcp",
        description="Antigravity Knowledge Hub MCP server (stdio transport)",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Project root directory (default: WORKSPACE_PATH env or cwd)",
    )
    args = parser.parse_args()

    workspace = _resolve_workspace(args.workspace)

    if not workspace.exists():
        print(f"Error: workspace does not exist: {workspace}", file=sys.stderr)
        sys.exit(1)

    # Set env so pipeline picks up the workspace
    os.environ["WORKSPACE_PATH"] = str(workspace)

    serve(workspace)


if __name__ == "__main__":
    main()
