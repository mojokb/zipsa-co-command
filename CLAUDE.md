# Repository guidance

## Purpose and layout

This repository distributes nine zipsa skills for both Claude Code and Codex.

- Claude skills: `plugins/zipsa-commands/skills/`.
- Claude manifest: `plugins/zipsa-commands/.claude-plugin/plugin.json`.
- Marketplace: `.claude-plugin/marketplace.json`.
- Codex skills: `codex/skills/`.
- Shared policy, HTML renderer and renderer tests live inside each host's `zipsa-workflow/`.

The Claude plugin uses the default `skills/` discovery directory. There is no glob-based
manifest override. Keep host-neutral reference files and renderer resources aligned across
both distributions. Keep host-specific lead/peer roles, tool calls and failure behavior distinct.
Do not copy Claude peer instructions over the Codex distribution or vice versa.

## Workflow contracts

The lead agent implements; the independent peer is read-only. Each invocation coordinates
at most one stage. Preserve repository approval boundaries, fix diagnosis before product
edits, requirement traceability, evidence freshness and safe interruption recovery.
The HTML guide does not grant approval or replace canonical artifacts.

## Versioning

Bump and synchronize these three fields for a release:

1. `.claude-plugin/marketplace.json`: `metadata.version`.
2. `.claude-plugin/marketplace.json`: `plugins[0].version`.
3. `plugins/zipsa-commands/.claude-plugin/plugin.json`: `version`.

Keep `pyproject.toml`'s tooling project version consistent as well.
The former `plugins/zipsa-commands/plugin.json` has moved to the standard manifest location.
Maintain the existing marketplace/plugin names for installed users.

## Validation

Use asdf runtimes from `.tool-versions` and uv; do not add global runtimes or use pip.
The renderer and tests use the Python standard library and require Python 3.11 or later.

```sh
uv sync --locked --python "$(asdf which python3)"
uv run python -m unittest discover -s tests -v
uv run python -m unittest discover -s plugins/zipsa-commands/skills/zipsa-workflow/tests -v
uv run python -m unittest discover -s codex/skills/zipsa-workflow/tests -v
claude plugin validate --strict plugins/zipsa-commands
claude plugin validate --strict .claude-plugin/marketplace.json
```

For behavioral instruction changes, use the distribution's
`zipsa-workflow/references/skill-validation.md` in an isolated workspace. Do not treat
static checks, test counts or peer agreement as proof of model behavior. Keep unexecuted
native model checks explicit, including account/tool failures. Never run production checks
or post externally merely because a skill was updated.
