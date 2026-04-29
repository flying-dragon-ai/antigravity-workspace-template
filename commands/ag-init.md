---
description: Scaffold a new multi-agent repository from the Antigravity template (invokes agent-repo-init skill).
---

This command scaffolds a new repository from the Antigravity template. It is not required before `/antigravity:ag-refresh`; refresh initializes the current workspace's `.antigravity/` knowledge directory automatically.

Invoke the `agent-repo-init` skill. Parse $ARGUMENTS for: project name, destination path, mode (`quick` or `full`). If any are missing, ask before running `${CLAUDE_PLUGIN_ROOT}/skills/agent-repo-init/scripts/init_project.py`.
