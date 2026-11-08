---
name: zipsa-build
description: Implement an ordered task list one task at a time, comparing each nontrivial approach with an independent read-only Claude review before editing. Verify each task's acceptance criteria.
---

# Zipsa Build

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and diagnosis

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including standalone use. Identify fix/feature work against its contract; require fix reproduction and cause evidence before product edits and apply the repeated-premise check to failed remedies. Reuse current evidence and investigate missing facts only within existing authority. A missing diagnostic prerequisite blocks the affected implementation, not unrelated authorized tasks.

## Verification evidence and plan changes

Read the linked requirements and approved plan as well as the task list; include their references in the approach review. If the project requires plan approval and the relevant revision is pending or its approval cannot be established, obtain confirmation before implementation. For a standalone task without a separate plan, use the confirmed task and acceptance criteria as the baseline; do not invent a plan artifact. Preserve requirement IDs in task results. For each acceptance criterion record the check or manual procedure, observed result, evidence location, and tested commit or identifiable working-tree snapshot when uncommitted changes exist. Mark checks not run or inconclusive as unverified with the reason; do not mark a task fully verified while a required criterion remains unverified. Write or update meaningful unit tests with implementation as required by the repository. Preserve the planned scenarios and evidence for the subsequent zipsa-test stage; task-level checks do not replace verification of the complete change. Checks that require remaining planned implementation may stay explicitly pending for zipsa-test; do not defer runnable failing task-level checks or dependency checks needed by the next task.

Before implementing a substantive design/contract departure from the validated plan, stop the affected task and return the proposed revision and reason. Invalidate the affected validation and obtain plan/validate reassessment plus required confirmation before resuming, including standalone invocation. For a standalone task without a plan, stop for confirmation if the proposed change departs from its confirmed scope/contract; do not invent a plan merely for this gate. Ordinary implementation details within the validated design need no new planning cycle. Update the existing plan for authorized departures and preserve the approved baseline reference; a retrospective plan edit is not approval.

Use the existing task records for execution evidence and stage progress. For authorized issue-comment updates, follow the shared reporting rules: preserve only new facts needed for issue resolution or later debugging; stage completion alone does not warrant a comment. Keep requirements and completion criteria in the issue body. Do not create a separate stage report or post externally without authorization.

Codex is the implementer and final decision maker. Claude reviews the approach, not the code it will write. Input is a task file or one concrete task with acceptance criteria.

For each task, in dependency order:

1. Read the task, affected code, callers, tests, fixtures, config, exports, and repository instructions. Confirm source-edit authorization required by the repository before modifying source. Start a Claude review in parallel: `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Supply the complete task and acceptance criteria on stdin. Ask for affected files, implementation order, edge cases, and simpler options. Do not interpolate task text into shell code. Use a short initial yield.
2. Independently design the smallest complete change before reading or polling Claude's response. For a plainly mechanical task, you may skip Claude and record the reason.
3. Compare the approaches. Verify any Claude claim that changes the direction. Adopt a simpler complete design or a substantiated risk; reject extra complexity. State the chosen direction briefly.
4. Implement the task, including affected callers and meaningful checks. Preserve existing error handling and validation. Run the checks that establish the task's acceptance criteria. Diagnose and fix failures before moving to the next task. Re-consult Claude only if a failure reveals a fundamental design flaw, using `--resume <session_id>` and the same read-only flags.
5. After all tasks, report completed tasks, evidence, material approach decisions, skips, and remaining risks.

Follow higher-priority user and repository instructions for worktrees, confirmation, PRs, and deployment. Claude must not edit files. If the CLI fails, disclose the missing peer review and continue only when the task can be completed responsibly without it.
