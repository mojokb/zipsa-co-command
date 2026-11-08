---
name: zipsa-review
description: "Review a code path or diff from two perspectives: Codex checks maintainability and clarity, and read-only Claude checks architecture, correctness, and production risks. Return ranked findings with source lines."
---

# Zipsa Review

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Performance work only

If this task has performance acceptance criteria or measures/reports a speedup or regression, read the [conditional performance rules](../zipsa-workflow/references/performance.md). Apply only the evidence needed for that claim; do not add benchmarks to unrelated work.

## Compare the change with the approved plan

Read the linked authoritative requirements, approved plan revision, task list, and verification evidence when available; supply these references to the peer reviewer along with the exact review target. Independently compare the actual changes against each in-scope requirement and the approved plan. Report omitted requirements, changes outside the plan, and whether departures have a recorded reason and required approval. A later plan edit alone is not evidence of approval.

Check that verification evidence applies to the reviewed commit or working tree; report material changes after the checks as unverified. Cite requirement IDs, plan sections, and code lines in findings where applicable. If the requirements, approved baseline, or evidence cannot be found, state the resulting review limitation without inventing a record or blocking a standalone code review. Keep this disposition in the existing review output rather than a separate report.

Review the test scenarios and assertions against authoritative requirements and API contracts, not just the implementation. Check relevant failure paths, integration boundaries, and whether mocks or missing environments leave required behavior unverified. Agent agreement and coverage percentages alone do not prove correctness. After review fixes change code, tests, fixtures, or configuration, rerun the affected tests and required repository checks against the updated target; keep earlier results as history, not current proof. A standalone review may report missing evidence without executing tests, but must not claim the change is fully verified.

Input is a path, directory, or change range. Without an explicit target, use the complete tested range/snapshot from the zipsa-test handoff, including later changes; report missing snapshots or unresolvable revisions as scope limitations. Only for a standalone review without a handoff, use `git diff HEAD` or, if empty, `git diff HEAD~1`, and identify that target. State any difference between the requested and tested scopes. Codex owns the final review. Claude provides an independent senior-engineer perspective.

1. Read the target and connected code. Detect REST API code from handlers, routes, or OpenAPI annotations. Supply the target path or diff, relevant request, and review criteria to Claude on stdin. Run `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Ask for specific findings with file and line, severity, impact, and evidence, including assertion validity against requirements, failure paths, integration boundaries, and evidence freshness. Do not interpolate source text into shell code. Use a short initial yield.
2. Independently review as the developer who must maintain the code. Check behavior, edge cases, naming, readability, duplication, function limits (Python 40 lines excluding docstrings; Go 60), idioms, type hints, error handling, resource use, and tests. For public APIs, check that documentation explains arguments, returns, errors, and units; apply Google docstrings in Python and adjacent Go doc comments. For REST code also check method and status semantics, OpenAPI request/response contracts, and Go response `binding:"required"` versus nullable or omitted fields.
3. Finish your findings before reading or polling Claude's result. Validate each Claude-only finding against code. Merge duplicates; give your ruling on disagreements. Do not list speculative or unsupported concerns.
4. Return findings ordered by severity: Critical, Major, Minor, Suggestion. Each finding names the file and line, states what fails and why, and gives the smallest corrective action. Add a prioritized action list. If no findings, say so and state what was checked. Do not edit unless the user also requested fixes.
5. A focused follow-up may use `claude -p --resume <session_id>` with the same read-only flags. If Claude fails, disclose that this is a Codex-only review.

When the user later asks to apply review findings, report each fix with its verification and a plain-language explanation, as the original Claude skill requires.
