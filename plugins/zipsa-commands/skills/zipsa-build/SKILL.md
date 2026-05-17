---
name: zipsa-build
description: Implement tasks incrementally with Codex as an approach reviewer. For each task, Agent and Codex independently design the implementation approach, compare, then Agent implements. Use after zipsa-tasks produces a task list. Pass the path to the tasks file or a single task description as the argument.
---

# Zipsa-Build: Implement Tasks with Codex Approach Review

## Arguments

`$ARGUMENTS` should be the path to the tasks file (e.g. from `zipsa-tasks` output), or a single task description. If a tasks file is provided, tasks are processed one by one in dependency order.

---

## Per-Task Loop

Repeat Steps 1–4 for each task. Complete each task fully before moving to the next.

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
- **Unresolvable disagreement or missing decision** → escalate to the user before proceeding

State the confirmed approach in one short paragraph before implementing.

---

## Step 4: Implement and Verify

**4a. Implement.**

Write the code according to the confirmed approach. Follow project conventions:
- Max function length: 40 lines (Python), 60 lines (Go)
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

### Tasks Implemented
1. [Task title] — ✅ verified
2. [Task title] — ✅ verified
...

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
