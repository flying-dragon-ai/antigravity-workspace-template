---
description: Rebuild the antigravity project knowledge base after significant changes.
allowed-tools: ["mcp__plugin_antigravity_antigravity__refresh_project"]
---

Call `mcp__plugin_antigravity_antigravity__refresh_project` for the current workspace.

If $ARGUMENTS contains "quick" → pass `quick=true`. Otherwise pass `quick=false`.

If the MCP tool is not available or not connected, do not diagnose this as an LLM key problem. Tell the user to restart Claude Code once so the Antigravity MCP server loads, then rerun `/antigravity:ag-refresh`. Point them to `docs/en/TROUBLESHOOTING.md` for the diagnostic log path.

Report progress concisely; full refresh can take several minutes.
