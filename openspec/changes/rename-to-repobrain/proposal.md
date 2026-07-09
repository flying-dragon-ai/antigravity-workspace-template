# Change: Rename all functional identifiers from Antigravity to RepoBrain

## Why

The project rebranded to RepoBrain: the GitHub repository is now
`study8677/repobrain` and all README/docs prose uses the new name. Functional
identifiers still carry the old brand (`antigravity_engine`, `ag-*` CLI
commands, `AG_*` env vars, `.antigravity/` knowledge directory, plugin ID
`antigravity`). Keeping two names permanently confuses users and splits SEO,
docs, and support surface. The owner chose a clean break (no compat aliases).

## What Changes

Identifier mapping (clean switch, no backward-compat aliases):

- Python distributions: `antigravity-engine` → `repobrain-engine`,
  `antigravity-cli` → `repobrain-cli`
- Python packages: `antigravity_engine` → `repobrain_engine`,
  `ag_cli` → `rb_cli`
- CLI entry points: `ag` → `rb`, `ag-ask` → `rb-ask`,
  `ag-refresh` → `rb-refresh`, `ag-mcp` → `rb-mcp`
- Environment variables: `AG_*` → `RB_*` (e.g. `AG_HOST_RUNNER` →
  `RB_HOST_RUNNER`, `AG_REFRESH_SCAN_ONLY` → `RB_REFRESH_SCAN_ONLY`)
- Knowledge directory: `.antigravity/` → `.repobrain/`
- Plugin ID and marketplace: `antigravity@antigravity` →
  `repobrain@repobrain`; slash commands `/antigravity:ag-*` → `/repobrain:rb-*`
- Command docs: `commands/ag-*.md` → `commands/rb-*.md`
- MCP example config `docs/examples/antigravity.mcp.json` →
  `docs/examples/repobrain.mcp.json`; suggested server name `antigravity` →
  `repobrain`
- Brand image assets regenerated (logo, social preview, before/after graphic)

Out of scope: the local checkout directory name; historical artifacts under
`artifacts/`; archived OpenSpec changes; third-party names (e.g. "Google
Antigravity" references stay as-is).

## Impact

- BREAKING: users must reinstall the engine/CLI, re-run setup (new `RB_*`
  keys in `.env`), and re-run `rb-refresh` (knowledge dir renamed). Existing
  `.antigravity/` folders are ignored; users can delete or rename them.
- Affected specs: `deployment`, `knowledge-hub`, `developer-workflow`
- Affected code: `engine/` (package rename + all imports + tests),
  `cli/` (package rename, templates), `commands/`, `hooks/`,
  `.claude-plugin/`, `.codex-plugin/`, `.github/workflows/`, `Dockerfile`,
  `scripts/check_repo_contract.py`, `docs/`, README files, image assets.
