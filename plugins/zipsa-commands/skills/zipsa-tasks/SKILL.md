---
name: zipsa-tasks
description: Break a validated plan into concrete implementation tasks. Spawns Codex immediately, then collaborates with Codex to identify and resolve undecided areas — only escalating to the user when both cannot agree. Once all decisions are made, both independently produce a task breakdown, then compare and merge into a final ordered task list. Pass the path to the plan file as the argument. Results are documented only — does not proceed to implementation.
---

# Zipsa-Tasks: Break Plan Into Implementation Tasks

## Scope

**This skill produces documentation only.** Do NOT write, edit, or modify any source code files. All output must be saved as a Markdown (`.md`) file.

## Arguments

`$ARGUMENTS` should be the path to the plan file. If not provided, check if there is a plan file from the current session (for example in `.claude/projects/` or the working directory).

## Step 1: Read the Plan and Spawn Codex Simultaneously

Do both of these at the same time:

**1a. Read the plan.**
Read the plan file at `$ARGUMENTS`. Identify every area that is **undecided, ambiguous, or underspecified**:
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

Decision rules:
1. If you and Codex agree on a resolution → **record the decision and move on.**
2. If you and Codex disagree or neither has a clear answer → **escalate to the user.**

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

**Do not proceed to Step 3 until every ambiguity is resolved.** Keep the Codex dialogue and user Q&A going until there are no open questions.

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
- Acceptance criteria — how to verify it is done
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

Each task must include:
- A short title
- What to build (concrete, not vague)
- Acceptance criteria — how to verify it is done
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

Save the final task list as a Markdown file in the current working directory. Use a descriptive filename based on the plan (e.g., `tasks-[plan-slug].md`).

```
## Implementation Tasks

### Decisions Applied
- [decision 1]
- [decision 2]
...

---

### Task 1: [Title]
**Build:** [what to build]
**Acceptance criteria:** [how to verify]
**Depends on:** —

### Task 2: [Title]
**Build:** [what to build]
**Acceptance criteria:** [how to verify]
**Depends on:** Task 1

...
```

## How To Treat Codex Responses

Treat Codex responses as coming from a junior developer:

- Never assume suggestions are correct; validate each one yourself.
- You are the lead engineer and have final say.
- Use responses as a starting point, not authoritative answers.
