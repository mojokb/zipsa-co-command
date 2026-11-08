---
name: zipsa-test
description: Verify a completed change against requirements with independent test design and executed unit, integration, or E2E checks as needed. Use after build, before code review, or to reverify review fixes. Report defects, blocked checks, and evidence; does not authorize product-code fixes or deployment.
---

# Zipsa Test

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Fix evidence and failed remedies

Read the [shared work policy](../zipsa-workflow/references/work-policy.md). Carry the original fix reproduction and contract expectation into verification on the affected interface. Missing pre-fix evidence stays explicit; never fabricate a historical failure or treat another interface’s passing unit tests as proof. Apply the repeated-premise check before proposing a further product fix and return product changes to build.

## Performance work only

If this task has performance acceptance criteria or measures/reports a speedup or regression, read the [conditional performance rules](../zipsa-workflow/references/performance.md). Apply only the evidence needed for that claim; do not add benchmarks to unrelated work.

## Inputs and authority

Use the task list, linked authoritative requirements and contracts, approved plan when present, and the complete change target. If no task file exists, use the confirmed request and observable acceptance criteria. Resolve missing expectations from authoritative sources or ask about material ambiguity; never invent approval or redefine success to match current behavior. Follow repository worktree, source-edit confirmation, runtime, test-environment, and reporting rules.

Record the tested base/head commits or identifiable working-tree snapshot, including relevant untracked files. Use the requested change range; otherwise state the exact diff being tested and its limits rather than silently treating the last commit as the entire feature.

## 1. Design cases from the contract

Before inspecting implementation or its tests, read the confirmed requirements, contracts, and planned scenarios. Independently write cases with requirement IDs, inputs/preconditions, expected observable results and their sources. Include relevant invalid inputs, boundaries, permissions, duplicate requests, retry behavior, dependency failures, and regressions; select only cases the change can affect. Preserve these expectations when subsequently examining the code. A second agent's agreement is a critique, not proof that the expected behavior is correct.

Use Codex as a read-only test-design peer through a background Task (`run_in_background: true`). The subagent calls `mcp__validate-plans-and-brainstorm-ideas__codex` with `sandbox: read-only`, `approval-policy: never`, and `cwd` set to the target repository. Its prompt must include confirmed requirements and their revisions, API contracts, planned scenarios, change scope, and environment constraints; request contract-derived cases, expected results and sources, test levels, and missing decisions. Tell Codex to form initial cases before reading implementation or existing tests. Return the `threadId` and full response. Finish your own case inventory before reading the subagent's result. Use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` on that thread only for material disagreements, keeping the peer read-only. If the tool is unavailable or fails, disclose single-perspective design and proceed only where expectations and execution can be established responsibly.

## 2. Choose and complete the test scope

After both case inventories are ready, or after completing the disclosed single-perspective fallback, inspect implementation, callers, existing tests, fixtures, and configuration. Compare the independent cases, verify disputed expectations against the contract, and fill meaningful gaps using the existing test framework. Reuse task scenarios and tests without accepting them as sufficient solely because they pass. Record why unit, integration, or E2E levels are selected or omitted; follow required repository checks and coverage targets. Mock-based checks do not establish behavior across the real integration boundary.

Write missing tests and fixtures only within existing authorization and repository confirmation rules; otherwise report the proposed additions and unmet criteria. This stage does not authorize product-code fixes. Return product defects to the authorized build/fix workflow, preserving a reproducing test where permitted.

## 3. Execute and diagnose

Run selected checks in the designated test environment with repository commands and managed runtimes. Confirm service and fixture prerequisites before stateful checks. Do not reset shared data or use production as a substitute for an unavailable test environment without explicit authorization. Keep fixtures isolated and clean up only resources created by this run.

Record commands/manual steps, exit outcomes, observed behavior, evidence locations, environment, and tested revision/snapshot. A missing dependency or environment is not a pass. Separate a contract violation in the product from a faulty assertion or fixture using reproducible evidence; if the cause is uncertain, record that uncertainty and leave the criterion unverified. Fix test defects only when authorized, retaining contract-derived expectations. Do not weaken assertions, remove cases, or lower required coverage merely to obtain a passing run.

For a product fix, demonstrate the reproducer fails on the faulty version where feasible, then passes on the fixed version. Rerun affected regression tests and required repository checks after code, test, fixture, or configuration changes. Retry only after identifying a cause or changing a relevant condition; stop and report an unchanged blocker rather than repeatedly rerunning it. Keep previous failures in the evidence even when a later rerun passes.

## 4. Hand off evidence to review

Update existing task records and the review handoff; do not create a separate stage report unless requested. Use repository issue-comment conventions only where posting is already authorized. Include source requirements/plan revisions, selected scope and omissions, tested target/environment, and for each case:

| Requirement / case | Expected result and source | Check / evidence | Observed result / status |
|---|---|---|---|
| R1 / case name | Contract-derived expectation and reference | Command or manual steps; evidence location | Actual observation; passed, product defect, test defect, environment blocked, not run, or inconclusive |

Summarize verified and unverified acceptance criteria, outstanding defects, and the next action. The stage is incomplete while any required selected check or acceptance criterion remains failing, blocked, not run, or inconclusive. Optional test levels omitted with a reason are scope limits, not executed passes. Handoff to review is allowed with explicit limitations; do not claim full verification. Subsequent review fixes require affected tests and required checks to run against the updated target before the evidence is current again.
