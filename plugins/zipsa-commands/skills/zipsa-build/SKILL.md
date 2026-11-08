---
name: zipsa-build
description: Implement tasks incrementally with Codex as an approach reviewer. For each task, Agent and Codex independently design the implementation approach, compare, then Agent implements. Use after zipsa-tasks produces a task list. Pass the path to the tasks file or a single task description as the argument.
---

# Zipsa-Build: Implement Tasks with Codex Approach Review

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and diagnosis

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including standalone use. Identify fix/feature work against its contract; require fix reproduction and cause evidence before product edits and apply the repeated-premise check to failed remedies. Reuse current evidence and investigate missing facts only within existing authority. A missing diagnostic prerequisite blocks the affected implementation, not unrelated authorized tasks.

## Verification evidence and plan changes

Read the linked requirements and approved plan as well as the task list; include their references in the approach review. If the project requires plan approval and the relevant revision is pending or its approval cannot be established, obtain confirmation before implementation. For a standalone task without a separate plan, use the confirmed task and acceptance criteria as the baseline; do not invent a plan artifact. Preserve requirement IDs in task results. For each acceptance criterion record the check or manual procedure, observed result, evidence location, and tested commit or identifiable working-tree snapshot when uncommitted changes exist. Mark checks not run or inconclusive as unverified with the reason; do not mark a task fully verified while a required criterion remains unverified. Write or update meaningful unit tests with implementation as required by the repository. Preserve the planned scenarios and evidence for the subsequent zipsa-test stage; task-level checks do not replace verification of the complete change. Checks that require remaining planned implementation may stay explicitly pending for zipsa-test; do not defer runnable failing task-level checks or dependency checks needed by the next task.

Before implementing a substantive design/contract departure from the validated plan, stop the affected task and return the proposed revision and reason. Invalidate the affected validation and obtain plan/validate reassessment plus required confirmation before resuming, including standalone invocation. For a standalone task without a plan, stop for confirmation if the proposed change departs from its confirmed scope/contract; do not invent a plan merely for this gate. Ordinary implementation details within the validated design need no new planning cycle. Update the existing plan for authorized departures and preserve the approved baseline reference; a retrospective plan edit is not approval.

Use the existing task records for execution evidence and stage progress. For authorized issue-comment updates, follow the shared reporting rules: preserve only new facts needed for issue resolution or later debugging; stage completion alone does not warrant a comment. Keep requirements and completion criteria in the issue body. Do not create a separate stage report or post externally without authorization.

## Arguments

`$ARGUMENTS` should be the path to the tasks file (e.g. from `zipsa-tasks` output), or a single task description. If a tasks file is provided, tasks are processed one by one in dependency order.

---

## Per-Task Loop

Repeat Steps 1–4 for each task. Complete implementation and applicable task-level checks before moving to the next; carry explicitly pending whole-change checks to zipsa-test without marking them verified.

---

## Step 1: Read the Task and Spawn Codex Simultaneously

Do both at the same time:

**1a. Read the task.**

Extract from the task:
- What to build (concrete scope)
- Acceptance criteria (how to verify it's done)
- Dependencies (which prior tasks this builds on)

Identify files likely involved by reading relevant parts of the codebase. Do not implement yet.

**1b. Spawn a background subagent for Codex** (Task tool with `run_in_background: true`). The subagent should:

1. Call `mcp__validate-plans-and-brainstorm-ideas__codex` with:
   - `prompt`: construct exactly as shown below
   - `sandbox`: `read-only`
   - `approval-policy`: `never`
   - `cwd`: (use the current working directory)
2. If Codex asks clarifying questions, answer using codebase context and wait for it to finish.
3. Once Codex responds, report back the `threadId` and the full response.

### Codex Prompt

```text
First, explore the codebase in your working directory to understand the project structure, key files, and existing patterns.

You are acting as a **Senior Engineer reviewing an implementation approach** — not writing code. For the following task, describe how you would implement it:

- Which files and functions would you modify or create?
- In what order would you make the changes?
- What edge cases or conflicts with existing code should be watched for?
- Is there a simpler alternative approach worth considering?

Do NOT write code. Describe the approach only. Be concise and specific.

Requirements and plan context:
{include the authoritative requirements with stable IDs and source revision, the plan revision and approval status, and any relevant user-confirmed decisions; mark unavailable records explicitly}

Task:
<task>
{paste the full task description and acceptance criteria}
</task>
```

**Skip Codex (Step 1b) when:**
- The task is clearly mechanical (e.g. adding a config value, renaming a field, copy-paste CRUD pattern identical to an adjacent task already implemented this session). State the reason explicitly before skipping.

---

## Step 2: Design Your Own Approach

While Codex works in the background, independently design your implementation approach:

- Which files and functions to modify or create
- Order of changes
- Edge cases and potential conflicts with existing code
- Any simpler alternatives

**Do NOT read the Codex response until your own approach is fully formed.**

---

## Step 3: Compare Approaches and Confirm Direction

Read the Codex response. Compare it against your own approach:

- **Agreement** → proceed with your approach (no change needed)
- **Codex suggests simpler alternative** → adopt if it satisfies the acceptance criteria with less code or fewer dependencies
- **Codex identifies a risk or conflict you missed** → incorporate into your approach
- **Codex proposes more complex approach** → challenge it: "What concrete requirement does this complexity address?" Default to the simpler approach unless Codex's reason is compelling.
- **Technical disagreement** → first seek distinguishing evidence within existing authority and apply the shared question policy; escalate only a remaining user-owned decision or unavailable information/access.

State the confirmed approach in one short paragraph before implementing.

---

## Step 4: Implement and Verify

**4a. Implement.**

Write the code according to the confirmed approach. Follow project conventions:
- Max function length: 40 lines (Python, excluding docstring lines), 60 lines (Go)
- Max file length: 300 lines — split if exceeded
- No magic numbers, no commented-out code, no TODO left behind
- No features beyond what the task requires

**4b. Verify acceptance criteria.**

Check each acceptance criterion from the task:
- Run relevant tests
- Confirm behavior matches what was specified
- If a criterion cannot be verified automatically, state how you verified it manually

**4c. On failure:**

If verification fails:
- Diagnose root cause by reading the error and the code
- Fix and re-verify
- Do NOT re-consult Codex unless the failure reveals a fundamental flaw in the confirmed approach — in that case, use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` to share the failure and ask for a revised approach

**4d. On success:** proceed to the next task.

---

## Step 5: Final Summary (after all tasks complete)

```
## Build Complete

### Task Results
- [Task title / requirement IDs]: [verified, failed, or unverified]
  - [acceptance criterion]: [check or procedure; observed result; evidence location; tested commit or working-tree snapshot]

### Plan Conformance
- [approved baseline; departures and reasons; confirmation references or pending decisions]

### Approach Decisions
- [Task title]: chose [approach] over [Codex alternative] because [reason]
- [Task title]: adopted Codex suggestion to [simplification] — reduced [X] lines
...

### What Was Skipped and Why
- [Task title]: skipped Codex review — [reason]

### Remaining Work
- [anything explicitly out of scope or deferred]
```

---

## How To Treat Codex Responses

- Codex reviews the approach, not the implementation — its job is to catch bad directions before you invest in code.
- Never assume Codex suggestions are correct; validate against the codebase yourself.
- You are the lead engineer and have final say.
- Prefer the simpler approach unless there is a concrete, specific reason to choose complexity.
