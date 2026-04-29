---
description: Ask a question about the current project's codebase via the antigravity knowledge hub.
allowed-tools: ["mcp__plugin_antigravity_antigravity__ask_project"]
---

Use the `mcp__plugin_antigravity_antigravity__ask_project` MCP tool to answer:

> $ARGUMENTS

If the MCP tool is not available or not connected, tell the user to restart Claude Code once so the Antigravity MCP server loads, then rerun the command. Do not diagnose missing MCP tools as an LLM key problem.

Prefer this tool over manual file search. If the tool returns insufficient detail, follow up with targeted Read/Grep.
