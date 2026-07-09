# RepoBrain Mission

**Objective:** Make any repository queryable by AI development tools through a
portable, evidence-grounded knowledge layer.

## Description
RepoBrain centers on the `rb-refresh` + `rb-ask` workflow:
1. `rb-refresh` scans a repository and builds `.repobrain/` knowledge artifacts.
2. `rb-ask` routes codebase questions to the relevant module context.
3. Native plugins, CLI entrypoints, and MCP tools expose the same knowledge layer
   to different AI IDEs without changing the core product.

## Success Criteria
- Answers cite concrete source files and line-level evidence where available.
- Claude Code and Codex CLI have native slash-command flows.
- Other IDEs can use the shared context files, raw CLI commands, or `rb-mcp`.
- Documentation, version metadata, and CI checks describe the same product
  contract.
