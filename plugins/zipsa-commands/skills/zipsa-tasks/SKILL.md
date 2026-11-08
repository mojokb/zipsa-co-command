---
name: zipsa-tasks
description: Break a validated plan into concrete implementation tasks. Spawns Codex immediately, then collaborates with Codex on technical choices. Escalates user-owned decisions and material information/access gaps after evidence gathering. Once all decisions are made, both independently produce a task breakdown, then compare and merge into a final ordered task list. Pass the path to the plan file as the argument. Results are documented only — does not proceed to implementation.
---

# Zipsa-Tasks: Break Plan Into Implementation Tasks

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Questions and work type

Read the [shared work policy](../zipsa-workflow/references/work-policy.md). Preserve fix/feature classification and its source in task records; carry original fix reproduction/cause evidence into acceptance checks. Resolve observable facts through authorized inspection or execution before escalating a technical disagreement.

## Performance work only

If this task has performance acceptance criteria or measures/reports a speedup or regression, read the [conditional performance rules](../zipsa-workflow/references/performance.md). Apply only the evidence needed for that claim; do not add benchmarks to unrelated work.

## Task traceability

Identify the source requirements and approved plan revision; if approval cannot be established, report it rather than claiming the plan is validated. Preserve requirement IDs in both independent breakdowns and the final list. For each task include its requirement IDs, acceptance criteria, concrete verification method, and dependencies. For each requirement define test scenarios before implementation: inputs and preconditions, expected observable results with a requirement or contract source, unit/integration/E2E level and selection reason, required fixtures and environment, and the command or manual procedure. Cover relevant failure paths and regressions; do not infer expected results from the implementation. Carry these fields into both independent task breakdowns and the final task list. Check that every in-scope requirement is covered and that every task serves the plan; resolve gaps before handing the list to implementation.

## Arguments

`$ARGUMENTS` should be the path to the plan file. If not provided, check if there is a plan file from the current session (for example in `.claude/projects/` or the working directory).

## Step 1: Read the Plan and Spawn Codex Simultaneously

Do both of these at the same time:

**1a. Read the plan.**
Read the plan file at `$ARGUMENTS` and any linked requirements, if available. Identify decisions already confirmed by the user, then every area that is **undecided, ambiguous, or underspecified**:
- Missing technical decisions (e.g. "use a queue" — which queue? what retry policy?)
- Unresolved trade-offs the plan mentions but doesn't resolve
- Implicit assumptions that could go multiple ways
- Scope boundaries that are unclear (what's in, what's out)
- Error handling or edge cases not addressed
- External dependencies with no concrete decision (library, service, protocol)
- Non-functional requirements not specified (performance targets, SLA, scale)

**1b. Spawn a background subagent for Codex.**
Spawn a **background subagent** (Task tool with `run_in_background: true`). The subagent should:

1. Call `mcp__validate-plans-and-brainstorm-ideas__codex` with:
   - `prompt`: construct exactly as shown below
   - `sandbox`: `read-only`
   - `approval-policy`: `never`
   - `cwd`: (use the current working directory)
2. Report back the `threadId` once Codex responds.

### Codex Initial Prompt

```text
First, explore the codebase in your working directory to understand the project structure, key files, and existing patterns.

Then read the following plan and identify every area that is undecided, ambiguous, or underspecified — things that must be decided before the plan can be broken into concrete implementation tasks. Group related ambiguities by theme.

For each ambiguity include:
- A short label
- What is unclear
- Why it matters for task breakdown
- Your recommended resolution (with brief reasoning)

Requirements and plan context:
{include the authoritative requirements with stable IDs and source revision, the plan revision and approval status, and any relevant user-confirmed decisions; mark unavailable records explicitly}

Plan:
<plan>
{paste the full contents of the plan file}
</plan>

Share your ambiguity analysis now.
```

## Step 2: Collaborate with Codex to Resolve Ambiguities

Once Codex shares its ambiguity analysis, compare it against your own list from Step 1a. Merge both lists — add anything Codex found that you missed, and include anything you found that Codex missed.

For each ambiguity, try to reach a decision together. When evaluating options, **actively resist over-engineering**:

- Prefer the simplest solution that satisfies the current requirement — not the most flexible or future-proof one
- If an option adds abstraction, a new dependency, or extra infrastructure that the plan does not explicitly require, default to rejecting it
- "We might need this later" is not a valid reason to add complexity now
- If Codex proposes a more complex approach, challenge it: "What does the simpler version look like, and what concrete requirement does the complexity address?"

Separate implementation choices from user decisions. Agent agreement may resolve technical choices within confirmed requirements. Changes to scope, user-visible behavior, acceptance criteria, or ownership need the user's decision even if you and Codex agree; present those changes as proposals until confirmed.

Decision rules:
1. If you and Codex agree on a technical resolution within confirmed requirements → **record the decision and move on.**
2. If you and Codex disagree or neither has a clear answer, first seek distinguishing evidence through authorized inspection or execution. Escalate only a material user-owned decision or unavailable information/access, stating what was checked and why it remains blocked.

### Escalating to the User

When escalating, group related open questions and present them clearly:

```
We need your input on a few decisions before we can continue:

**1. [Topic]**
[What is unclear and why it matters]
→ My recommendation: [option A — brief reason]
→ Codex recommends: [option B — brief reason]
Which do you prefer, or do you have another direction?

**2. [Topic]**
[What is unclear]
→ Both of us are unsure. Options: (a) ... (b) ... (c) ...
```

After the user answers, acknowledge each decision, check if the answer introduces new ambiguities, and either ask follow-ups or confirm all questions are resolved.

**Do not proceed to Step 3 while material ambiguity blocks the tasks.** Record nonblocking details as assumptions; do not continue peer dialogue or user questions merely to eliminate every minor uncertainty.

### Continuing the Codex Dialogue

Use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` to exchange messages with Codex:
- Share user decisions so Codex stays in sync
- Ask Codex to re-examine remaining ambiguities after each user answer
- Use `threadId` from the initial Codex session throughout

## Step 3: Independent Task Breakdowns — In Parallel

Once all ambiguities are resolved, do both of these simultaneously:

**3a. Your own task breakdown.**
Independently produce a task breakdown applying all resolved decisions. For each task include:
- A short title
- What to build (concrete, not vague)
- Requirement IDs from the source plan
- Acceptance criteria and test scenarios: inputs/preconditions, expected results and their requirement/contract source, test level and selection reason, fixtures/environment, and verification command or procedure
- Dependencies on other tasks (by title)

Order tasks so dependencies come first.

**3b. Request Codex's task breakdown.**
Use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

```text
All ambiguities are now resolved. Here are the final decisions:
<decisions>
{list all resolved decisions}
</decisions>

Now produce your task breakdown. Keep tasks minimal — only what the plan explicitly requires. Do not add tasks for abstractions, extensibility, or "nice to have" infrastructure unless it was explicitly decided above.

Each task must preserve the source requirement IDs. Include the source requirements and plan revision in the breakdown. Each task must include:
- A short title
- What to build (concrete, not vague)
- Requirement IDs from the source plan
- Acceptance criteria and test scenarios: inputs/preconditions, expected results and their requirement/contract source, test level and selection reason, fixtures/environment, and verification command or procedure
- Dependencies on other tasks (by title)

Order tasks so dependencies come first.
```

**Do not look at Codex's breakdown before finishing your own.**

## Step 4: Compare, Negotiate, and Output Final Task List

Once both breakdowns are complete, compare them:

- **Tasks in both** → include; merge detail differences, keep the clearer version
- **Codex-only tasks** → validate independently; include if legitimate, discard if not
- **Your-only tasks** → keep if you are confident
- **Ordering conflicts** → resolve by dependency analysis; if genuinely ambiguous, prefer the safer order

Produce the final merged task list.

## Output Format

```
## Implementation Tasks

**Sources:** [requirements reference / revision; plan reference / revision; approval status]

### Decisions Applied
- [decision 1]
- [decision 2]
...

---

### Task 1: [Title]
**Requirements:** [R1, ...]
**Build:** [what to build]
**Acceptance criteria:** [observable outcome]
**Test scenarios:** [inputs / preconditions; expected results and requirement or contract source]
**Test scope:** [unit / integration / E2E and selection reason; fixtures / environment]
**Verification:** [command or manual procedure]
**Depends on:** —

### Task 2: [Title]
**Requirements:** [R2, ...]
**Build:** [what to build]
**Acceptance criteria:** [observable outcome]
**Test scenarios:** [inputs / preconditions; expected results and requirement or contract source]
**Test scope:** [unit / integration / E2E and selection reason; fixtures / environment]
**Verification:** [command or manual procedure]
**Depends on:** Task 1

...
```

## How To Treat Codex Responses

Treat Codex responses as coming from a junior developer:

- Never assume suggestions are correct; validate each one yourself.
- You are the lead engineer and have final say.
- Use responses as a starting point, not authoritative answers.
