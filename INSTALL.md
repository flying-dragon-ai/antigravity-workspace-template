# Installing the Antigravity plugin

## Claude Code

```
/plugin marketplace add study8677/antigravity-workspace-template
/plugin install antigravity@antigravity
/antigravity:setup
/antigravity:ag-refresh
/antigravity:ag-ask "what does this project do?"
```

1. **Marketplace add** — clones the plugin manifest into Claude Code's cache.
2. **Install** — first session triggers `hooks/install_engine.py`, which auto-installs `ag-mcp` via `pipx` (preferred), `pip --user` fallback, or prints a manual command if both fail. Cross-platform (macOS / Linux / Windows).
3. **Setup** — interactive: choose your LLM provider (OpenAI / DeepSeek / Groq / 阿里灵积 / NVIDIA / Ollama), paste your API key, writes a `.env` to the current project root and ensures it's git-ignored.
4. **Refresh** — builds `.antigravity/` for the current project. The first refresh creates the project knowledge directory automatically.
5. **Ask** — queries the refreshed project knowledge base.

If the current session says the Antigravity MCP tool is not connected, restart Claude Code once and rerun `/antigravity:ag-refresh`. That means the plugin MCP server was not loaded in this session; it is not an API key failure. See [docs/en/TROUBLESHOOTING.md](docs/en/TROUBLESHOOTING.md).

You can also add the marketplace from a local checkout:

```
/plugin marketplace add /absolute/path/to/antigravity-workspace-template
```

## Codex CLI

Codex CLI does not auto-run install hooks (as of April 2026), so install the engine first:

```
pipx install /absolute/path/to/antigravity-workspace-template/engine
ag-mcp --help    # verify
```

Then register and install the plugin:

```
codex plugin marketplace add /absolute/path/to/antigravity-workspace-template
codex plugin install antigravity
```

## Verifying

- **Claude Code**: `/antigravity:ag-ask "what does the engine do?"` should invoke `mcp__plugin_antigravity_antigravity__ask_project`.
- **Codex CLI**: confirm the `antigravity` MCP server appears in your Codex MCP server list.

## Available slash commands (Claude Code)

Slash commands are namespaced by plugin name — type `/antigravity:` to discover them.

| Command | What it does |
|---|---|
| `/antigravity:setup` | **First-time setup** — interactive `.env` writer (LLM provider + key + model) |
| `/antigravity:ag-refresh [quick]` | Rebuild / incrementally update the project knowledge base |
| `/antigravity:ag-ask <question>` | Routed Q&A on the current codebase |
| `/antigravity:ag-init <name>` | Scaffold a new multi-agent repo from this template |

## Bundled MCP tools

After install, the `antigravity` MCP server exposes:

- `ask_project(question)` — routed Q&A with file paths and line numbers
- `refresh_project(quick=False)` — rebuild knowledge base

## Uninstall

```
pipx uninstall antigravity-engine
/plugin uninstall antigravity
```

## Requirements

- Python 3.10+ on PATH (`python3` / `python`)
- `pipx` recommended (`brew install pipx`, `apt install pipx`, or `python3 -m pip install --user pipx`)
- Network access on first launch (for the auto-installer)

## Troubleshooting

**`ag-mcp` not found after install**
The user-pip bin directory may not be on PATH. The installer prints the path; add it to your shell rc file (`~/.zshrc`, `~/.bashrc`, etc.).

**Antigravity MCP tool is not connected**
Restart Claude Code once so plugin-provided MCP servers are loaded. Then rerun `/antigravity:ag-refresh`. Do not rerun setup just for this error unless setup has never been completed.

**Diagnostic log**
`ag-mcp` writes startup and tool errors to `~/.claude/plugins/data/antigravity-antigravity/ag-mcp.log` unless Claude provides a plugin data directory.

**Do I need `/antigravity:ag-init` before refresh?**
No. `/antigravity:ag-refresh` initializes the current project's `.antigravity/` directory automatically. `/antigravity:ag-init` is for scaffolding a new repository from the Antigravity template.

**Hook timed out**
Slow network during first install. Increase the `timeout` in `hooks/hooks.json` or run `pipx install <plugin-root>/engine` manually before restarting.

**Codex CLI marketplace add fails**
Codex's marketplace schema is partially undocumented. If `codex plugin marketplace add <path>` rejects the repo, you can still register the MCP server directly via your local Codex CLI MCP config and load skills from `<path>/skills/` manually.
