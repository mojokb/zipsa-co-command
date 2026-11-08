---
name: zipsa-validate
description: Get a staff engineer review of your plan via Codex. Use when you want critical review feedback on a plan before finalizing it. Pass the path to the plan file as the argument.
---

# Co-Validate: Get a Staff Engineer Review of Your Plan

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and prerequisites

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including its question classification. Check applicable fix reproduction/cause evidence as a planning prerequisite; missing evidence is a material finding, not a valid product-fix plan. Keep this review within existing read-only authority.

## Coverage against requirements

Read the authoritative requirements and the plan revision under review; give both to the peer reviewer. Check every in-scope requirement against a planned change and an observable acceptance check. Report missing coverage and work outside the approved scope with requirement references. Preserve requirement IDs when revising the plan; changed scope, behavior, or acceptance criteria remain proposals until user-confirmed. Identify the revised plan and its approval status rather than treating reviewer agreement as approval.

## Arguments

`$ARGUMENTS` should be the path to the plan file. If not provided, check if there is a plan file from the current session (for example in `.claude/projects/` or the working directory).

## Step 1: Read the Plan and Spawn a Background Subagent for Codex

1. Read the plan file at the path provided in `$ARGUMENTS`.
2. Find the original user prompt that triggered the plan by checking the conversation history.
3. Spawn a background subagent to handle the Codex review.

You MUST spawn a **background subagent** (using the Task tool with `run_in_background: true`) to handle all communication with Codex. The subagent should:

1. Call `mcp__validate-plans-and-brainstorm-ideas__codex` with:
   - `prompt`: construct exactly as shown below
   - `sandbox`: `read-only`
   - `approval-policy`: `never`
   - `cwd`: (use the current working directory)

2. If Codex asks clarifying questions instead of saying it's ready, the subagent should answer them using its own judgment and the codebase context, then wait for Codex to finish and respond with "My review is complete and I'm ready to present".

3. Once Codex says "My review is complete and I'm ready to present", the subagent should report back that Codex is ready (but NOT request the review yet — that happens in Step 3).

### Prompt Format

```text
First, explore the codebase in your working directory to understand the project structure, key files, and existing patterns. Then, as a staff engineer, review this plan. Analyze it for critical issues, big simplifications, or a completely different better approach — but do NOT share your review yet. If you need to ask clarifying questions about the plan or original request before reviewing, ask them now. Otherwise, when your review is complete and fully formed, respond with exactly: "My review is complete and I'm ready to present" and nothing else. Wait for my next message before sharing your review.

Requirements and plan context:
{include the authoritative requirements with stable IDs and source revision, the plan revision and approval status, and any relevant user-confirmed decisions; mark unavailable records explicitly}

Original request from the user:
<original_request>
{paste the user's original prompt/request that triggered the plan}
</original_request>

Plan:
{paste the full contents of the plan file}
```

The subagent handles the back-and-forth so the main agent is free to do its own work.

## Step 2: Do Your Own Review

While the subagent communicates with Codex in the background, do your own independent review of the plan. Look for:

- Critical issues or flaws in the approach
- Opportunities for simplification
- Missing edge cases or risks
- Whether a completely different approach would be better

Write down your own assessment. **Do NOT check the Codex result until you have finished your own review.** The entire point is to produce two independent reviews and then compare them — reading Codex's review early defeats this purpose and introduces bias.

## Step 3: Retrieve and Compare

Only after your own review is complete, confirm the background subagent has reported that Codex is ready. Then use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

- `threadId`: the thread ID from the Codex session
- `prompt`: `Go ahead, share your review. Be direct and concise. Do not repeat the plan back. Focus only on critical issues, big simplifications, or a completely different better approach.`

Once the review arrives:

1. Read the Codex review output.
2. Compare it against your own review, including requirement coverage and work outside the confirmed scope.
3. For each issue raised (by either review), either:
   - Accept it and update the plan accordingly
   - Override it with an explanation of why the current approach is better

Return the revised plan with requirement coverage, source revisions, approval status, and a disposition of material findings.

## Continuing The Conversation

Use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

- `threadId`: the thread ID from the previous response
- `prompt`: your response addressing points, explaining overrides, and asking for clarification when needed

If you override points, explain why so they can push back if needed.

## How To Treat Responses

Treat Codex responses as coming from a junior developer:

- Never assume suggestions are correct; validate each one yourself.
- You are the lead engineer and have final say.
- Use responses as a starting point, not authoritative answers.
