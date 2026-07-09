# Change: Freshness-aware ask, true incremental refresh, and first-run self-diagnosis

## Why

Post-rename audits (deep-research-report.md, artifacts/_codex_take.md, Codex
code audit 2026-07-09, GitHub issues #54/#47/#19) converge on the same gaps:

1. `rb-ask` answers from stale knowledge silently — it only checks that
   `.repobrain/map.md` exists, never compares `.last_refresh_sha` with git
   HEAD or reads `status.json` health.
2. `rb-refresh --quick` is not truly incremental — scan is incremental but
   module agents still re-run broadly, hurting cost/latency on large repos.
3. An interrupted refresh cannot resume — progress is only persisted at the
   end of the pipeline, so `--failed-only` cannot help after a crash.
4. First-run failures are opaque — the CLI formats only `ValueError`, other
   exceptions surface as raw tracebacks, and there is no self-diagnosis
   command (issue #54 "failed with no reason" is the canonical report).

## What Changes

- `rb-ask`: before answering, compare `.repobrain/.last_refresh_sha` with
  current git HEAD; if behind, prepend a staleness notice (N commits behind,
  suggest `rb-refresh --quick`). Read `status.json`; on `partial`/`failed`
  module states, prepend a degradation notice. Never block the answer.
- `rb-refresh --quick`: map changed files (from quick scan git diff) to
  affected module groups; only re-run agents for affected groups, reusing
  existing `agents/*.md` for untouched groups. Map index is regenerated only
  when any group changed.
- Refresh resume: persist per-group completion to `status.json` incrementally
  as groups finish; `--failed-only` (and plain re-runs) skip groups already
  completed for the same HEAD SHA.
- New `rb doctor` CLI command (engine): checks engine install, `.env`
  presence and key completeness, provider reachability (cheap models/list or
  equivalent), knowledge dir existence/freshness/health, and prints log
  locations. Exit non-zero when a blocking problem is found.
- CLI error handling: wrap `rb-ask`/`rb-refresh`/`rb doctor` entry points so
  unexpected exceptions print a one-line actionable error plus the diagnostic
  log path instead of a raw traceback (keep traceback under `DEBUG_MODE=1`,
  wiring the existing unused setting).
- README demo: render `docs/assets/demo.tape` (VHS) to a gif/webp and embed
  in the three READMEs' first screen.

## Impact

- Affected specs: `knowledge-hub`, `developer-workflow`
- Affected code: `engine/repobrain_engine/hub/ask_pipeline.py`,
  `engine/repobrain_engine/hub/refresh_pipeline.py`,
  `engine/repobrain_engine/hub/scanner.py` (changed-file plumbing),
  `engine/repobrain_engine/_cli_entry.py`, `engine/repobrain_engine/config.py`
  (DEBUG_MODE wiring), `engine/pyproject.toml` (rb-doctor entry if separate),
  engine tests, README files, `docs/assets/`.
- Backward compatible: no identifier or artifact-format breaking changes;
  `status.json` gains fields (additive).
