# RepoBrain Troubleshooting

## Normal Claude Code Flow

```bash
/plugin marketplace add study8677/repobrain
/plugin install repobrain@repobrain
/repobrain:rb-setup
/repobrain:rb-refresh
/repobrain:rb-ask "How does this project work?"
```

The first refresh creates the project-local `.repobrain/` knowledge directory automatically.

## CLI Command Not Found

Symptom:

```text
rb-refresh: command not found
```

This means the engine CLI is not installed or its bin directory is not on `PATH`.
Install it manually:

```bash
pipx install "git+https://github.com/study8677/repobrain.git#subdirectory=engine"
```

This is not an API key failure. Do not rerun setup unless `/repobrain:rb-setup` has never completed.

## Missing LLM Configuration

Symptom:

```text
No LLM configured
```

Run `/repobrain:rb-setup` in the project root. It writes `.env` with the provider URL, API key, and model. Do not commit `.env`.

## Project Initialization

`/repobrain:rb-refresh` initializes `.repobrain/` automatically. It is safe to run repeatedly and does not overwrite existing knowledge files just to initialize the directory.

`/repobrain:rb-init` is for scaffolding a new repository from this template; it is not a required step before refresh.

## Optional MCP Diagnostic Log

If you manually register `rb-mcp`, it writes startup and tool errors to:

```text
~/.claude/plugins/data/repobrain-repobrain/rb-mcp.log
```

When Claude Code provides a plugin data directory, the log is written there instead. The log directory is created with `0700` permissions and the log file with `0600`; logged errors are redacted and must not contain API key values.

## Manual Verification Checklist

Use this checklist for behavior that requires a real Claude Code session:

- Fresh session after plugin install: `/repobrain:rb-refresh` runs `rb-refresh` through Bash.
- Ask command: `/repobrain:rb-ask "How does this project work?"` runs `rb-ask` through Bash.
- Missing CLI: `/repobrain:rb-refresh` tells the user to install the engine CLI, not to change API keys.
- First refresh in a clean project: `.repobrain/manifest.json` and knowledge artifacts are created without running `/repobrain:rb-init`.
- Missing LLM config: the tool points to `/repobrain:rb-setup`.
- Optional MCP startup failure: `rb-mcp.log` exists at the diagnostic path and contains no API key values.
