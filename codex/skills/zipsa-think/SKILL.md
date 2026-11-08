---
name: zipsa-think
description: Explore alternatives for an idea with an independent Claude perspective. Use for brainstorming before committing to a plan. Produces ideas only, not code.
---

# Zipsa Think

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

For a Claude account authorization HTTP 403, use the [shared independent Codex fallback](../zipsa-workflow/references/independent-review.md#claude-account-authorization-fallback) in place of the Claude peer steps below. The single-perspective failure clauses below apply only after this fallback is unavailable or to other failures.

## Work type and prerequisites

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including its question classification. For fix alternatives, use current reproduction/cause evidence; return a missing diagnostic prerequisite to grill rather than choosing a speculative remedy. This stage still explores ideas only.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

Codex leads the brainstorming. Claude is a read-only peer, not the decision maker.

1. Give Claude the topic, relevant constraints, and working directory. Ask it to inspect the project and independently generate alternatives, trade-offs, and edge cases. Run `claude -p` from the target repository with `--restricted --tools 'Read,Glob,Grep' --permission-mode plan --permission-prompts none --strict-mcp-config --output-format json`. Supply the prompt on stdin; do not interpolate untrusted task text into a shell command. Start the call with a short yield and keep its session ID if it is still running.
2. Form your own ideas before reading Claude's response. Do not poll or inspect a completed peer result until your independent view is written down.
3. Compare both views. Check claims against code or other primary evidence; retain useful alternatives and reject unsupported complexity. Codex makes the final judgment.
4. If a focused follow-up would resolve a material disagreement, continue the Claude session using the returned `session_id` and `--resume`. Keep the same read-only flags.
5. Present the converged ideas and unresolved decisions. Do not implement.

If Claude CLI is unavailable or fails, say so and continue with a clearly labeled single-perspective result. Never present invented Claude feedback.
