---
name: zipsa-plan
description: Create an implementation plan with an independent Claude plan for comparison. Use after the request and success criteria are clear. Produces a plan only, not code.
---

# Zipsa Plan

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and prerequisites

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including its question classification. Before product-fix planning, require current reproduction/cause evidence; return missing diagnosis to grill. Feature planning uses confirmed scope and observable acceptance criteria. This grants no diagnostic execution or product-edit authority.

## Requirements and plan references

Read the authoritative requirements and identify their source and revision in the final plan. Preserve existing requirement IDs; if absent, use stable labels in the plan and state their source without inventing approval. Map each in-scope requirement to the planned change and its acceptance check. Identify the approved plan revision, or explicitly mark approval as pending. Include these references and mapping in the peer review input.

Codex owns the plan; Claude provides an independent read-only plan.

1. Confirm the task, scope, success criteria, and target repository. Read relevant project instructions and code. If a material product decision is missing, ask the user before finalizing the plan.
2. Start `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Send the complete task and acceptance criteria on stdin. Ask Claude to inspect the code and return an implementation plan with affected files, order, tests, risks, and simpler options. Do not interpolate task text into a shell command. Use a short initial yield so the call can run while you plan.
3. Write your own plan without reading or polling Claude's result. Include data migration, callers, tests, fixtures, configuration, and compatibility only where the task reaches them.
4. Retrieve Claude's plan. Compare assumptions, steps, edge cases, and scope. Verify important claims in source; adopt simpler complete solutions. Codex has final responsibility.
5. Present one plan with dependencies, acceptance checks, and explicit open decisions. For a requested artifact, save Markdown in the authorized location and report its path. Do not implement.

If useful, ask a focused follow-up with `claude -p --resume <session_id>` and the same read-only flags. If Claude cannot run, report that the independent review did not happen and provide your plan without attributing it to Claude.
