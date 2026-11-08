---
name: zipsa-plan
description: Generate a parallel plan via Codex. Use when you want an additional planning perspective to compare against your own plan. Runs in the background so you can continue working in parallel. Results are documented only — does not proceed to implementation.
---

# Co-Plan: Generate a Parallel Plan via Codex

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Work type and prerequisites

Read the [shared work policy](../zipsa-workflow/references/work-policy.md), including its question classification. Before product-fix planning, require current reproduction/cause evidence; return missing diagnosis to grill. Feature planning uses confirmed scope and observable acceptance criteria. This grants no diagnostic execution or product-edit authority.

## Requirements and plan references

Read the authoritative requirements and identify their source and revision in the final plan. Preserve existing requirement IDs; if absent, use stable labels in the plan and state their source without inventing approval. Map each in-scope requirement to the planned change and its acceptance check. Identify the approved plan revision, or explicitly mark approval as pending. Include these references and mapping in the peer review input.

## Step 1: Spawn a Background Subagent for Codex

You MUST immediately spawn a **background subagent** (using the Task tool with `run_in_background: true`) to handle all communication with Codex. The subagent should:

1. Call `mcp__validate-plans-and-brainstorm-ideas__codex` with:
   - `prompt`: `First, explore the codebase in your working directory to understand the project structure, key files, and existing patterns. Then create a detailed implementation plan for the following task. Think deeply about architecture, steps, edge cases, and trade-offs — but do NOT share the plan yet. If you need to ask clarifying questions about the task before planning, ask them now. Otherwise, when your plan is fully formed and ready, respond with exactly: "My plan is ready to present" and nothing else. Wait for my next message before sharing the plan.\n\nTask: $ARGUMENTS\n\nRequirements context: {include the authoritative requirements, their stable IDs and source revision, and relevant confirmed decisions}. Map each in-scope requirement to planned changes and acceptance checks.`
   - `sandbox`: `read-only`
   - `approval-policy`: `never`
   - `cwd`: (use the current working directory)

2. If Codex asks clarifying questions instead of saying it's ready, the subagent should answer them using its own judgment and the codebase context, then wait for Codex to finish and respond with "My plan is ready to present".

3. Once Codex says "My plan is ready to present", the subagent should report back that Codex is ready (but NOT request the plan yet — that happens in Step 3).

The subagent handles the back-and-forth so the main agent is free to do its own work.

## Step 2: Create Your Own Plan

While the subagent communicates with Codex in the background, create your own independent plan. **Do NOT check the Codex result until you have finished your own plan.** The entire point is to produce two independent plans and then compare them — reading Codex's plan early defeats this purpose and introduces bias.

## Step 3: Retrieve and Compare

Only after your own plan is finalized, confirm the background subagent has reported that Codex is ready. Then use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

- `threadId`: the thread ID from the Codex session
- `prompt`: `Go ahead, send the plan.`

Once the plan arrives:

1. Read the Codex plan output.
2. Compare it against your own plan and look for:
   - Approaches you missed
   - Simpler alternatives
   - Risks or edge cases you overlooked
3. Integrate useful ideas into your plan and discard the rest.

## Continuing The Conversation

If you want to discuss the plan further, use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

- `threadId`: the thread ID from the previous response
- `prompt`: your follow-up question or counterpoint

## How To Treat Responses

Treat Codex responses as coming from a junior developer:

- Never assume suggestions are correct; validate each one yourself.
- You are the lead engineer and have final say.
- Use responses as a starting point, not authoritative answers.
