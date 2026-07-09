# Tasks: improve-freshness-and-first-run

## 1. Freshness-aware ask (Tier 1)

- [x] 1.1 `rb-ask` compares `.repobrain/.last_refresh_sha` to git HEAD; if
      behind, prepend staleness notice with commit distance and
      `rb-refresh --quick` suggestion (never block the answer)
- [x] 1.2 `rb-ask` reads `status.json`; on partial/failed modules prepend a
      degradation notice naming the affected modules
- [x] 1.3 Tests: fresh, stale, missing-sha, partial-status, non-git workspace

## 2. True incremental quick refresh (Tier 1)

- [x] 2.1 Map quick-scan changed files to affected module groups
- [x] 2.2 Re-run agents only for affected groups; reuse `agents/*.md` for
      untouched groups; regenerate map only when any group changed
- [x] 2.3 Update `.last_refresh_sha` and status only for what actually ran
- [x] 2.4 Tests: no-change quick refresh runs zero module agents; single-file
      change re-runs only its group

## 3. Resumable refresh (Tier 1)

- [x] 3.1 Persist per-group completion into `status.json` as groups finish
- [x] 3.2 Re-run after interruption skips groups completed at the same HEAD
- [x] 3.3 Tests: simulated interruption resumes without re-running done groups

## 4. rb doctor + error handling (Tier 2)

- [x] 4.1 `rb doctor`: engine install, `.env` completeness, provider
      reachability, knowledge dir existence/freshness/health, log locations;
      non-zero exit on blocking problems
- [x] 4.2 Wrap CLI entry points: unexpected exceptions → one-line actionable
      error + log path; full traceback only under `DEBUG_MODE=1`
- [x] 4.3 Tests: doctor happy path, missing .env, stale knowledge; error
      wrapper behavior with and without DEBUG_MODE

## 5. README demo (Tier 2)

- [x] 5.1 Render `docs/assets/demo.tape` with VHS to gif; embed in first
      screen of README / README_CN / README_ES

## 6. Verification

- [x] 6.1 Full test suite green; contract check passes
- [x] 6.2 Manual: stale-repo ask shows notice; quick refresh on one-file
      change is visibly cheaper; `rb doctor` output is actionable
