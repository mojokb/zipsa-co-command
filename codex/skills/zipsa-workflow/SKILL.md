---
name: zipsa-workflow
description: Advance fix or feature work through the existing zipsa stages, one stage per invocation. Track artifact-backed progress, approval gates, regression routes, and interruption recovery. Use to start, continue, or resume coordinated development; completion ends at implementation, testing, and code review, not merge or deployment.
---

# Zipsa Workflow

## Human-facing reports and HTML

Follow the [shared reporting rules](references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent peer fallback

When a stage encounters Claude account authorization HTTP 403, retain its independent review by using the [shared independent Codex fallback](references/independent-review.md#claude-account-authorization-fallback). Replace the failed stage peer; do not add a controller-level review or treat the stage as single-perspective without attempting the fallback.

## Independent simplicity check

Include the [shared overengineering check](references/independent-review.md) in every stage handoff and its existing peer request; do not add a separate reviewer or review pass for it.

Codex coordinates and loads the installed Codex zipsa stage skills. Each stage owns its Claude peer interaction. Manual callers and future agents use the same checkpoint contract.

## Scope and invocation

Accept a fix/feature request, issue/artifact reference, or existing workflow.md. Follow repository instructions and existing authorization for worktrees, document/source edits, approvals and issue comments. Check real paths and permissions before editing symlinks. Resume in the verified authorized worktree; do not recreate it from a newer base or silently rebase it.

Read the [shared work policy](references/work-policy.md) to classify fix/feature work from its contract, distinguish observable facts from user decisions, and handle repeated failed premises. For fixes, grill owns missing reproduction/cause investigation before planning; valid existing evidence satisfies this gate without a new investigation. For features, grill establishes missing requirements and acceptance criteria. Mixed work retains task-specific types and gates. Pass performance requirements/claims to tasks, test and review under the [conditional performance rules](references/performance.md); unrelated work needs no benchmark. Keep the existing stages; classification creates no new skill or automatic loop.

Each invocation may reconcile evidence, adopt manual work, skip an inapplicable stage with a reason, and execute at most ONE existing stage skill. Run that stage until it completes, needs a user decision/approval, or encounters an unavailable prerequisite; checkpoint and return. Build retains its own task loop; preserve the active task for resumption. A status-only request does not dispatch or imply permission to modify files. This skill authorizes no automatic phase loop, merge, deployment, shared-data reset, or external posting.

## Checkpoint contract

Use one workflow.md beside existing feature artifacts in the authorized worktree/location. Ask if the supplied checkpoint or feature is ambiguous rather than inventing a second record. This is an operational checkpoint, not a separate stage-results report. Link authoritative requirements, plans, tasks, tests and reviews without copying their contents. Verify the checkpoint belongs to the same feature and repository contexts.

Use YAML frontmatter in the Markdown checkpoint with this schema. Replace example values with observations; unknown evidence stays null, never assumed approved/completed.

```yaml
---
schema_version: 1
state_revision: 1
feature_id: "issue-or-feature-id"
request_ref: "authoritative request reference"
work_type: null
repositories:
  - root: "canonical repository path"
    worktree: "authorized worktree path"
    branch: "observed branch"
    base_commit: "feature base SHA"
    target: "head SHA or identifiable working-tree snapshot"
current_stage: "grill"
stage_status: "pending"
active_task: null
attempt: null
sources: {}
approvals: []
stages: {}
blocker: null
next_action: null
presentation: null
---

## Transitions

- Record time, attempt ID, stage/status, evidence references, reason, invalidated records and next action for each transition.
```

Keep state_revision monotonic. sources maps logical artifacts to locations and exact revisions/content fingerprints. approvals records real source references, approved scope and artifact revision. A checkpoint flag or agent claim is not authorization: verify it in the current session or accessible records. Ask only for missing required authorization; preserve still-valid approvals.

work_type is fix, feature, mixed or null pending classification; link its contract/rationale through sources. Existing schema-version-1 checkpoints without this additive field remain readable: infer from current evidence on authorized reconciliation without resetting stages or approvals. Retain feature_id for all work types. Status-only requests can report an unknown type without dispatch or a mandatory migration write.

Each stages entry records status, origin (executed or adopted), input/output references and fingerprints, applicable skill revision, exit-condition evidence and unresolved items. attempt records a unique ID, actor/session, start time and execution handle when available. blocker records kind, cause, evidence and resumption condition; next_action identifies the proposed stage/action and reason. Keep detailed results in existing task records and point active_task to unfinished work. presentation records guide/input paths, current or failed rendering status, explained source-state revision, pending step explanations and any render error. If rendering failed after work completed, repair only the guide and return before dispatching another stage; do not repeat completed child work.

Statuses: pending, running, waiting_approval, blocked, failed, completed, skipped, stale. waiting_approval means a required user decision/authorization is missing; distinguish a question from action approval in blocker. blocked means another prerequisite or ownership is unresolved. failed means executed work violated an exit condition; stale means evidence no longer applies. completed describes a stage, not necessarily the feature.

Fingerprint relevant tracked/untracked code, tests, fixtures, configuration and source artifacts, not just HEAD. Exclude the checkpoint, recorded feature-guide JSON/HTML paths, and transition/presentation-only metadata from product/test snapshots so guide/state updates alone do not invalidate tests. Record test environment identity. Preserve past failures as history.

V0 has one writer per feature and provides no distributed lock. Verify previous ownership/execution before takeover. Before replacing a checkpoint, reread its state_revision and original content fingerprint; stop on concurrent edits. Write a complete temporary file beside it and replace atomically after that check. If state cannot be saved within repository permissions, report the blocker and do not dispatch work whose recovery state cannot be saved.

## One invocation

1. Read repository instructions, checkpoint, source artifacts, Git/worktree state and existing decisions. Verify feature identity, repository contexts and full target range. Reconcile work type and its contract evidence. Re-evaluate next_action rather than treating it as a command. Check applicable skill revisions when revalidating old completion records.
2. Reconcile manual progress and changed inputs against the gates below. Adopt only artifacts with verifiable content, source revision, required approval scope and exit evidence; record manual provenance without claiming the skill ran. Filenames, checkboxes and agent success messages are insufficient. Recognizing verified manually completed work is a read-only assessment plus the authorized checkpoint update: do not require hypothetical source-edit permission when no edit is proposed, unless repository policy explicitly requires historical approval evidence for adoption. An unchanged completed feature returns status without rerunning stages.
3. Select the earliest unmet applicable gate or justified regression route. think is optional when no material alternative remains; record why. Satisfy other stages with equivalent evidence rather than skipping them for convenience. A new/substantively revised plan passes validate before tasks/build. Plan production and approval are separate: read-only validation may precede approval, while edits wait for the repository's required authorization.
4. Verify prerequisites, ownership, input snapshots and action-specific authorization. If missing, save waiting_approval/blocked with the concrete question/prerequisite and return without dispatch. Resolving one blocker does not waive another gate.
5. Save running with attempt, target and input identities BEFORE dispatch. Load the same-host stage SKILL.md and pass work type, contract/reproduction/cause references where applicable, source references/revisions, confirmed decisions, active task, full target, evidence, authority limits and prior failures. Retain the stage's independent peer process and documented fallback; add no controller-level peer. Missing required skill/tool support blocks unless that stage permits a responsible fallback. Request review-only work from review; product fixes belong to a later build phase. In the build handoff, require the child to stop BEFORE implementing a substantive design/contract departure from the validated plan: return the proposed change and affected task, invalidate the old validation, and schedule plan then validate (or validate if a complete revised plan is already produced) before affected implementation resumes. Ordinary implementation details within the validated design do not reopen planning. For plan/validate peer-readiness handoffs, require the session/thread identifier needed by their retrieval steps.
6. Inspect returned artifacts, actual changes, results and outstanding questions against the exit gate. Save completed, waiting_approval, blocked or failed with invalidations and next_action. A regression destination is recorded now and executed only on a later invocation. Save partial progress and exact user questions before yielding.
7. Report checkpoint path, stage outcome, verified/unverified evidence, next action and needed input in chat and the guide. For authorized comment updates, apply the shared relevance check to issue comments without changing the issue title, body or state and preserve only new issue-resolution or future-debugging facts; do not post routine progress or next-stage announcements. Avoid duplicating child-stage comments and never accumulate stage reports in issue bodies.

## Stage gates

Normal order: grill, think when needed, plan, validate, tasks, build, test, review. Use current source revisions and the full feature target. These gates add handoff conditions to each linked skill, not replacement implementations.

| Stage | Entry and exit evidence |
|---|---|
| [grill](../zipsa-grill/SKILL.md) | Request/context in; authoritative requirements with stable IDs, observable success criteria, confirmed scope/constraints and no material ambiguity out; fix work also requires the shared policy’s reproduction and cause evidence before product-fix planning. A deferred blocking decision remains unresolved. |
| [think](../zipsa-think/SKILL.md) | Sufficiently clear requirements in; alternatives, trade-offs and an evidenced choice within confirmed scope out. Material unresolved user choices wait for input. |
| [plan](../zipsa-plan/SKILL.md) | Requirements and necessary choices in; source revisions, requirement-to-change/check mapping, affected files, order, dependencies, risks and approval status out. Draft completion is not approval. |
| [validate](../zipsa-validate/SKILL.md) | Plan and original requirements in; coverage and dispositions for material findings on the final plan revision out. Reassess substantive revisions; peer agreement cannot approve changed user scope/behavior. |
| [tasks](../zipsa-tasks/SKILL.md) | Current plan with valid validation in; ordered requirement-linked tasks, dependencies, acceptance criteria and test cases with inputs, expected results/sources, level selection, fixtures/environment and procedures out. |
| [build](../zipsa-build/SKILL.md) | Current plan/tasks, applicable fix reproduction/cause evidence and approvals required for the proposed actions in; implementation and runnable task/dependency checks evidenced out. Whole-change checks needing remaining planned implementation may stay pending for test; runnable failures cannot be deferred. |
| [test](../zipsa-test/SKILL.md) | Implementation ready for selected checks and designated environment available in; all required criteria/checks passed on the actual target with contract expectations, commands/manual steps, results, environment and evidence locations out. Required blocked/missing/inconclusive checks are incomplete. |
| [review](../zipsa-review/SKILL.md) | Full tested target including later changes in; current test evidence and required findings resolved, or accepted only where repository policy permits with actual authorization, out. Review can diagnose incomplete evidence but cannot complete the feature on it. |

## Regression routes and evidence validity

Route from the observed cause rather than merely the reporting stage. Record cause, destination, invalidated artifacts/approvals/evidence and resumption condition. Regression never means resetting Git, deleting artifacts or rolling back data.

| Cause | Next stage/action |
|---|---|
| Material ambiguity in scope, contract or expectations | grill; reassess affected plan, validation, tasks and implementation. |
| Design choice needs alternatives | think, then plan/validate as affected. |
| Plan cannot satisfy confirmed requirements | plan, then validate and affected tasks. |
| Missing task or wrong dependency under a sound plan | tasks, then affected build work. |
| Product defect in test/review | Authorized build fix, then test, then review. Keep reproducer and previous failure evidence. |
| Faulty assertion/fixture against a clear contract | Authorized correction in test and rerun without weakening expectations; uncertain diagnosis stays unverified. |
| Two fixes sharing a premise fail the same check | Reopen authorized diagnosis in grill; test the shared premise before another fix, then revisit plan/validate only where the evidence changes the design. |
| Environment/dependency outage | blocked at affected stage; restore prerequisites, not product-code workarounds. |
| Required user decision/approval missing | waiting_approval immediately before that action; retain unrelated valid progress. |

Changed requirements invalidate dependent plan coverage/validation, task mappings and approvals/evidence relying on old scope. If new requirements are already clear and confirmed, reassess at plan rather than repeating grill. A substantive plan change invalidates its validation and affected downstream work; reassess required approvals without erasing unchanged authorizations. A task-only correction need not reopen a sound plan.

Code/test/fixture/configuration/relevant environment changes make affected test/review evidence stale. Reconcile whether implementation remains: return to build if needed, otherwise test then review. Changes after review need affected tests/checks and review of the resulting target. Preserve evidence only with an explicit dependency/impact rationale; a "cosmetic" label is insufficient. Changed skill rules require rechecking affected exit conditions, not blindly accepting old completion.

Do not retry an unchanged failure or cycle through stages without new evidence, diagnosed corrective action, changed condition or authorized requirement change. Record attempted remedies and their input identities. If the same cause returns without progress, stop blocked with the concrete decision/input needed; do not rerun just to get a passing label.

## Resume and completion

For interrupted running entries, inspect actual outputs, Git changes, execution handles and external effects before dispatch. Establish prior execution ended through accessible execution evidence or explicit user confirmation after inspection. A timeout/old timestamp does not establish termination. If liveness/ownership is uncertain, stop blocked without takeover or overwriting that checkpoint.

After confirmed termination, adopt verifiably finished output or resume only unfinished work with the original scope/authority and a new linked attempt. Never blindly repeat stateful commands or external comments. Partial files/unverifiable outcomes do not establish completion. Wrong/missing worktrees, ambiguous features or conflicting actors require reconciliation, not silent context switching.

Feature completion requires coverage of all current in-scope requirements, completed build, required whole-change checks passing on the final target/environment, valid dispositions of required review findings, applicable required approvals, and no blocker/unverified required criterion. Record next_action as feature complete: local implementation/testing/code review, not merge/deploy. Changed inputs on reinvocation reopen the earliest affected gate while retaining historical results.

## Changing these skills

When modifying zipsa instructions, use the [behavioral validation procedure](references/skill-validation.md) for affected decisions and recovery gates. This is skill-authoring validation, not an extra stage in product workflows.
