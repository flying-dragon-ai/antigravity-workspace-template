# Tasks: rename-to-repobrain

## 1. Engine package

- [x] 1.1 Rename `engine/antigravity_engine/` → `engine/repobrain_engine/`;
      update all imports, `pyproject.toml` name/packages/scripts
      (`rb-ask`, `rb-refresh`, `rb-mcp`)
- [x] 1.2 Rename `AG_*` settings/env vars → `RB_*` in `config.py` and all
      call sites
- [x] 1.3 Knowledge directory constant `.antigravity` → `.repobrain`
- [x] 1.4 Update engine tests (imports, env var names, path expectations)

## 2. CLI package

- [x] 2.1 Rename `cli/src/ag_cli/` → `cli/src/rb_cli/`; entry point `ag` → `rb`;
      `pyproject.toml` name `repobrain-cli`
- [x] 2.2 Update templates (`AGENTS.md`, `.cursorrules`, etc.) to reference
      `.repobrain/` and `rb-*` commands
- [x] 2.3 Update CLI tests

## 3. Plugin surface

- [x] 3.1 Rename `commands/ag-*.md` → `commands/rb-*.md`; update contents
- [x] 3.2 `.claude-plugin/plugin.json` + `marketplace.json`: plugin ID
      `repobrain`, install `repobrain@repobrain`
- [x] 3.3 `.codex-plugin/`: same rename
- [x] 3.4 `hooks/install_engine.py`: install `repobrain-engine`, verify `rb-*`
- [x] 3.5 `docs/examples/antigravity.mcp.json` → `repobrain.mcp.json`

## 4. Infra and docs

- [x] 4.1 `.github/workflows/test.yml`: verify `rb-ask`/`rb-refresh`/`rb-mcp`;
      Dockerfile entrypoints
- [x] 4.2 `scripts/check_repo_contract.py` + `setup-github-metadata.sh`
- [x] 4.3 READMEs (EN/CN/ES), `INSTALL.md`, `docs/`, `openspec/project.md`:
      command names, env vars, dir name; remove "plugin ID is still
      antigravity" note
- [x] 4.4 Brand images: before/after graphic rebuilt as SVG
      (`docs/assets/before_after.svg`), social preview text updated;
      logo kept (no brand text in it)

## 5. Verification

- [x] 5.1 `pytest engine/tests cli/tests` passes
- [x] 5.2 `python3 scripts/check_repo_contract.py` passes
- [x] 5.3 Reinstall editable packages; `rb-ask --help` / `rb-refresh --help` /
      `rb-mcp --help` work; old `ag-*` entry points gone
- [x] 5.4 Repo-wide grep: no functional `antigravity`/`AG_`/`ag-` identifiers
      remain outside archives/artifacts/third-party references
