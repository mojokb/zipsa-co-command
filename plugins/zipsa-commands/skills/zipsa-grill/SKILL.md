---
name: zipsa-grill
description: Grill the user with sharp, probing questions to pin down requirements, scope, constraints, and success criteria before planning. Use at the front of the workflow when the request is a vague idea. Asks one focused cluster at a time, challenges vague answers, and stops when no material ambiguity remains. Also gathers authorized reproduction and cause evidence for fix work before planning. Outputs requirements and diagnostic evidence, not an implementation.
---

# Zipsa-Grill: Interrogate the Request Into Pinned Requirements

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Work type and questions

Read the [shared work policy](../zipsa-workflow/references/work-policy.md). Classify fix/feature work from the existing contract. For fixes, gather missing reproduction and causal evidence with existing authorized diagnostics before declaring planning ready; record blockers instead of implementing a speculative fix. Before asking, separate discoverable/observable facts from user-owned decisions. Apply the repeated-premise check when returning from failed fixes.

## Requirements to carry forward

Reuse existing requirement IDs; otherwise assign stable IDs such as R1 to the confirmed requirements and their observable success criteria. Keep IDs stable across revisions. Identify the authoritative requirements file or issue, its revision, and the user-confirmed decisions so later stages can refer to them without copying the entire record.

This is the **front** of the zipsa workflow (`grill → think → plan → validate → tasks → build → test → review`). It turns a vague idea into a sharp, written requirements doc that `zipsa-think` / `zipsa-plan` consume. Unlike the other zipsa skills, the interrogation target is **the user**, not Codex.

## Arguments

`$ARGUMENTS` is the rough idea, feature request, or topic to pin down. If not provided, use the user's current request from the conversation.

## Step 1: Gather Context Before Asking Anything

Do NOT open with questions. First explore so your questions are sharp and informed — never ask what the code already answers.

- Read relevant code, docs, and existing patterns in the working directory.
- Verify facts that affect scope against the relevant code, docs, issues, or PRs. Note whether each was run, read in code, or stated in a document; mark what could not be checked.
- Note what is already decided by the codebase (do not ask about these).
- Note what is genuinely undetermined and blocks planning (these become grill targets).

## Step 2: Build a Question Inventory

Privately assemble candidate questions across these dimensions. Keep only the ones whose answer would actually change the plan.

- **Problem & why** — what problem, who feels the pain, why now, cost of doing nothing
- **Users & usage** — who uses it, the primary flow, frequency
- **Scope** — what is explicitly IN vs explicitly OUT (force a boundary)
- **Success criteria** — concrete, observable definition of done ("good" is not an answer)
- **Constraints** — tech, performance, security, compatibility, deadline
- **Edge cases & failure** — what must not break, expected failure behavior
- **Dependencies & unknowns** — external systems, data, things the user has not decided yet

Discard anything derivable from code/context (Step 1) or that does not materially affect the plan. **Over-grilling is a failure mode.**

## Step 3: Grill in Rounds

Interrogate the user one focused cluster at a time — not a wall of questions.

Rules per round:
- Ask the **highest-leverage cluster first** (the answer that unblocks the most downstream decisions).
- Max ~2–4 questions per round, grouped by theme.
- Where you have a view, lead with a recommendation so the user can react: "→ I'd assume X — correct, or different?"
- After each answer:
  - Reflect the pinned fact back in one line so it is confirmed.
  - **Challenge vague answers.** "Make it fast" → "Fast = p95 under what, at what load?" "Handle errors" → "Which errors, and what should the user see?"
  - Detect new ambiguities the answer introduces and queue follow-ups.

Format:
```
**Round N — [theme]**
1. [sharp question] → my assumption: [X]
2. [sharp question]

(Pinned so far: …)
```

## Step 4: Know When To Stop

Stop grilling when ALL of these hold — do not keep asking past this point:
- The scope boundary (in/out) is explicit.
- Success criteria are concrete and observable.
- No remaining unknown blocks planning; fix work also has current reproduction and cause evidence.

If a remaining unknown does NOT block planning, record it as an open question instead of grilling further. Respect the user's time: record deferred nonblocking details as assumptions. A deferred blocking contract decision or missing fix diagnosis remains unresolved; report it without claiming planning readiness.

## Step 5: Output the Requirements Document

Write the result to a markdown file in the working directory (for example `requirements-<short-slug>.md`) so `zipsa-think` / `zipsa-plan` can consume it. Print the path. This skill is **documented only — it does not plan or implement.**

```
## Requirements: [Title]

**Authoritative source / revision:** [file or issue reference and revision]

### Problem & Why
[the problem, who it affects, why now]

### Verified Context
- [fact that affects scope] — [source: file:line or link; how checked]
- [unverified claim, if any] — [what was checked and what remains unknown]

### Scope
**In:** …
**Out:** …

### Success Criteria
- R1: [confirmed requirement and concrete, observable success criterion]

### Constraints
- [tech / perf / security / compat / deadline]

### Edge Cases & Failure Behavior
- …

### Dependencies
- …

### Open Questions / Assumptions
- [unknown that does not block planning] — assumed: […]

### Decisions Pinned
- [user-confirmed decision] — rationale
```

## How To Grill Well

- You are pinning requirements, not solving the problem — resist proposing solutions here (that is `zipsa-think`'s job).
- Sharp and specific beats broad. "What database?" is weak; "this needs transactions across X and Y — does the existing Postgres cover it, or is there a reason to add another store?" is sharp.
- Never accept hand-waving on **scope** or **success criteria** — those are the two things that wreck downstream plans.
- Do not interrogate for its own sake. The moment ambiguity stops being material, stop and write the doc.
