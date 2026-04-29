---
description: First-time setup. Configure the LLM API key Antigravity uses to read and analyze your codebase. Run this once per project before /antigravity:ag-refresh.
---

You are running first-time setup for the Antigravity plugin. The user just installed the plugin and needs an LLM API key configured before `/antigravity:ag-refresh` and `/antigravity:ag-ask` will work. Goal: write a `.env` file at the current workspace root.

## Step 1 — Detect existing config

Read `.env` at the workspace root if it exists. If `OPENAI_API_KEY` is already set, ask the user whether to overwrite. If they say no, confirm "already configured" and stop.

## Step 2 — Ask which LLM provider (use AskUserQuestion)

Present these options:

- **OpenAI** — gpt-4o-mini / gpt-4o
- **DeepSeek** — cheap, strong on code
- **Groq** — fast, free tier
- **阿里灵积 (DashScope)** — qwen 系列
- **NVIDIA NIM** — generous free tier
- **Ollama 本地** — no key needed, runs locally
- **其他 OpenAI 兼容端点** — custom URL

## Step 3 — Collect URL / key / model

Use this table to set the URL and suggest a model based on the provider:

| Provider | `OPENAI_BASE_URL` | Suggested `OPENAI_MODEL` |
|---|---|---|
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` |
| 阿里灵积 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |
| NVIDIA NIM | `https://integrate.api.nvidia.com/v1` | `meta/llama-3.3-70b-instruct` |
| Ollama 本地 | `http://localhost:11434/v1` | `llama3.2` (key can be `ollama`) |
| 其他 | ask the user | ask the user |

For non-Ollama providers ask the user to paste their key. For Ollama use `OPENAI_API_KEY=ollama` (the engine requires the field to be non-empty).

## Step 4 — Write `.env`

Write to `<workspace>/.env`:

```
OPENAI_BASE_URL=<chosen URL>
OPENAI_API_KEY=<the key, or "ollama">
OPENAI_MODEL=<chosen model>
AG_ASK_TIMEOUT_SECONDS=120
```

If `.env` already existed and the user opted to overwrite, replace only the four keys above; preserve any other lines.

## Step 5 — Ensure `.env` is git-ignored

Check `<workspace>/.gitignore`. If `.env` is not listed (and there is no globbing rule that already covers it), append `.env` on a new line. If `.gitignore` doesn't exist, create one with `.env`.

## Step 6 — Tell the user next steps

Print exactly:

```
✅ Antigravity is configured for this project.

Next:
  1. Restart Claude Code (Ctrl+C twice, then re-run claude) so ag-mcp picks up the new .env.
  2. /antigravity:ag-refresh        — build the knowledge base (one-time, a few minutes for small repos)
  3. /antigravity:ag-ask <question> — ask anything about the codebase
```

Do NOT call `mcp__plugin_antigravity_antigravity__refresh_project` from this command — the engine subprocess that's running right now still has the old (empty) env. The user must restart Claude Code first.
