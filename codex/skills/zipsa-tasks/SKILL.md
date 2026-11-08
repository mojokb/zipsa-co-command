---
name: zipsa-tasks
description: Turn a validated plan into ordered implementation tasks after resolving material ambiguities with an independent Claude analysis. Produces tasks only, not code.
---

# Zipsa Tasks

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Questions and work type

Read the [shared work policy](../zipsa-workflow/references/work-policy.md). Preserve fix/feature classification and its source in task records; carry original fix reproduction/cause evidence into acceptance checks. Resolve observable facts through authorized inspection or execution before escalating a technical disagreement.

## Performance work only

If this task has performance acceptance criteria or measures/reports a speedup or regression, read the [conditional performance rules](../zipsa-workflow/references/performance.md). Apply only the evidence needed for that claim; do not add benchmarks to unrelated work.

## Task traceability

Identify the source requirements and approved plan revision; if approval cannot be established, report it rather than claiming the plan is validated. Preserve requirement IDs in both independent breakdowns and the final list. For each task include its requirement IDs, acceptance criteria, concrete verification method, and dependencies. For each requirement define test scenarios before implementation: inputs and preconditions, expected observable results with a requirement or contract source, unit/integration/E2E level and selection reason, required fixtures and environment, and the command or manual procedure. Cover relevant failure paths and regressions; do not infer expected results from the implementation. Carry these fields into both independent task breakdowns and the final task list. Check that every in-scope requirement is covered and that every task serves the plan; resolve gaps before handing the list to implementation.

Input is a validated plan file. Codex owns decisions and the final task list; Claude is a read-only technical peer.

1. Read the plan, linked requirements, and confirmed user decisions. List missing choices that would change a task: API behavior, data shape, error handling, external dependency, scope, or acceptance checks.
2. Ask Claude to inspect the repository and independently identify ambiguities, their impact, and a minimal recommended resolution. Call `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Supply the plan path and instructions on stdin; do not interpolate plan text into shell code. Start with a short yield, then finish your own ambiguity inventory before reading Claude's response.
3. Compare inventories. Resolve ordinary implementation choices with evidence and the smallest complete approach. Ask the user only for decisions that change scope, user-visible behavior, acceptance criteria, or ownership, or for missing information/access after evidence gathering leaves a material blocker. Preserve the repository's confirmation requirements. Do not continue until material blockers are resolved.
4. Independently write ordered tasks. For each, state what to build, observable acceptance criteria, and dependencies. Then ask Claude for its task breakdown using `--resume <session_id>` and the same read-only flags, including the resolved decisions. Finish your breakdown before reading Claude's.
5. Merge valid Claude-only tasks, remove unsupported extras, and order by dependency. Output one Markdown task list with decisions applied, tasks, acceptance checks, and dependencies. Save it only where authorized. Do not implement.

If Claude cannot run, disclose the missing peer review and continue with your own evidence-based breakdown. Never fabricate agreement.
