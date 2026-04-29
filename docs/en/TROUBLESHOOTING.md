# Antigravity Troubleshooting

## Normal Claude Code Flow

```bash
/plugin marketplace add study8677/antigravity-workspace-template
/plugin install antigravity@antigravity
/antigravity:setup
/antigravity:ag-refresh
/antigravity:ag-ask "How does this project work?"
```

The first refresh creates the project-local `.antigravity/` knowledge directory automatically.

## MCP Tool Not Connected

Symptom:

```text
The mcp__...refresh_project tool isn't connected in this session
```

This means Claude Code has not loaded the plugin MCP server in the current session. Restart Claude Code once, reopen the same project directory, then rerun `/antigravity:ag-refresh`.

This is not an API key failure. Do not rerun setup unless `/antigravity:setup` has never completed.

## Missing LLM Configuration

Symptom:

```text
No LLM configured
```

Run `/antigravity:setup` in the project root. It writes `.env` with the provider URL, API key, and model. Do not commit `.env`.

## Project Initialization

`/antigravity:ag-refresh` initializes `.antigravity/` automatically. It is safe to run repeatedly and does not overwrite existing knowledge files just to initialize the directory.

`/antigravity:ag-init` is for scaffolding a new repository from this template; it is not a required step before refresh.

## Diagnostic Log

`ag-mcp` writes startup and tool errors to:

```text
~/.claude/plugins/data/antigravity-antigravity/ag-mcp.log
```

When Claude Code provides a plugin data directory, the log is written there instead. The log directory is created with `0700` permissions and the log file with `0600`; logged errors are redacted and must not contain API key values.

## Manual Verification Checklist

Use this checklist for behavior that requires a real Claude Code session:

- Fresh session after plugin install: `/mcp` shows the Antigravity plugin MCP server.
- Tool naming: slash commands call `mcp__plugin_antigravity_antigravity__refresh_project` and `mcp__plugin_antigravity_antigravity__ask_project`.
- Missing tool session: `/antigravity:ag-refresh` tells the user to restart Claude Code once, not to change API keys.
- First refresh in a clean project: `.antigravity/manifest.json` and knowledge artifacts are created without running `/antigravity:ag-init`.
- Missing LLM config: the tool points to `/antigravity:setup`.
- Startup failure: `ag-mcp.log` exists at the diagnostic path and contains no API key values.
