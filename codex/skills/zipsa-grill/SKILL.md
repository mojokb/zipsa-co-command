---
name: zipsa-grill
description: Pin a vague request's requirements, scope, constraints, and observable success criteria before planning. Use when material ambiguity remains; stop once it no longer blocks planning. Also gathers authorized reproduction and cause evidence for fix work before planning. Produces requirements and diagnostic evidence, not an implementation.
---

# Zipsa Grill

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Work type and questions

Read the [shared work policy](../zipsa-workflow/references/work-policy.md). Classify fix/feature work from the existing contract. For fixes, gather missing reproduction and causal evidence with existing authorized diagnostics before declaring planning ready; record blockers instead of implementing a speculative fix. Before asking, separate discoverable/observable facts from user-owned decisions. Apply the repeated-premise check when returning from failed fixes.

## Requirements to carry forward

Reuse existing requirement IDs; otherwise assign stable IDs such as R1 to the confirmed requirements and their observable success criteria. Keep IDs stable across revisions. Identify the authoritative requirements file or issue, its revision, and the user-confirmed decisions so later stages can refer to them without copying the entire record.

This is the front of `grill → think → plan → validate → tasks → build → test → review`. Codex leads this stage. No Claude review is needed because the questions go to the user.

1. Read the request, relevant code, documents, issues, and existing decisions before asking. Mark each material claim as observed in code, observed in an execution, or stated in a document. Do not ask for facts the project already answers.
2. Identify only open decisions that could change scope, behavior, acceptance criteria, or the plan. Ask the highest-leverage related questions together. State a reasoned default when useful.
3. After each answer, reflect the decision briefly. Challenge vague answers only when the ambiguity still blocks planning. Follow the repository's confirmation instructions.
4. Stop when scope and success criteria are observable and no material unknown blocks planning; fix work also needs current reproduction and cause evidence. Record lesser unknowns as explicit assumptions.
5. Produce a Markdown requirements document in the user's chosen location, or a suitable project location if authorized. Follow repository worktree and source-change rules before writing into a repository. Include: problem and why, verified context with sources, scope, success criteria, constraints, edge cases, dependencies, assumptions, and user-confirmed decisions. Report its path.

Do not design the implementation or start coding in this skill.
