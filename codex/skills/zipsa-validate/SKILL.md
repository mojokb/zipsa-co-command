---
name: zipsa-validate
description: Critically review an existing implementation plan with an independent Claude review. Use before finalizing a consequential plan. Does not implement.
---

# Zipsa Validate

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and prerequisites

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including its question classification. Check applicable fix reproduction/cause evidence as a planning prerequisite; missing evidence is a material finding, not a valid product-fix plan. Keep this review within existing read-only authority.

## Coverage against requirements

Read the authoritative requirements and the plan revision under review; give both to the peer reviewer. Check every in-scope requirement against a planned change and an observable acceptance check. Report missing coverage and work outside the approved scope with requirement references. Preserve requirement IDs when revising the plan; changed scope, behavior, or acceptance criteria remain proposals until user-confirmed. Identify the revised plan and its approval status rather than treating reviewer agreement as approval.

Input is a plan file or the plan from the current conversation. Codex leads and rules on findings; Claude acts as a read-only staff-engineer reviewer.

1. Read the plan and original request. Identify its concrete acceptance criteria and constraints.
2. Ask Claude to inspect the repository and review the plan for critical flaws, missing edge cases, smaller complete approaches, and mismatches with the original request. Invoke `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Pass the plan path and original request through stdin. Do not interpolate them into shell code. Start with a short yield.
3. Independently review the plan before reading or polling Claude's answer. Record your own objections and simplifications.
4. Verify each material finding in code. Accept and revise the plan, or reject with a reason. Surface any decision that changes user-visible scope or behavior for user confirmation.
5. Return the revised plan and a concise disposition of material findings. Do not implement.

Use `--resume <session_id>` with the same read-only flags for a focused follow-up. If Claude is unavailable, disclose that and complete a single-perspective review.
