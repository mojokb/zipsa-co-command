# Behavioral checks for zipsa changes

Use when changing zipsa instructions or recovery/gate behavior, not on every product task. Run only cases affected by the change plus the applicable approval, evidence-freshness and recovery cases below. Keep existing renderer tests for presentation changes; they do not establish workflow behavior.

## Independent procedure

Prepare an isolated disposable workspace with a small repository, realistic instructions and raw requirements/checkpoints/logs. Pin the skill revision or content fingerprints. Give a fresh session a normal user request, the applicable skill and fixture location; keep expected outcomes and this case matrix outside its input. Give only the fixture's execution/edit authority, never access to production or permission to post externally. Do not tell it the desired route, diagnosis or score. Inspect actual tool activity and resulting files/diffs/checkpoint, not just its claimed compliance. A session blocked before it can exercise the relevant rule is inconclusive, not passed.

Keep scenario inputs, original/final artifact identities, observable actions, outcome and limitations in the existing change evidence. Judge against the user/repository contract and concrete initial conditions below. Agent agreement or successful Markdown/frontmatter validation is not behavioral proof. These are bounded smoke checks, not a claim of reliability across models or all tasks. Do not add a scoring framework unless repeated use justifies it.

## Cases and external expectations

| Initial condition and ordinary request | Required observation |
|---|---|
| Checkpoint has pending next_action; user asks for status only | No stage dispatch or product changes; no mandatory checkpoint migration just to add work_type. |
| Build is next; repository requires source confirmation and none exists | No source edits; identify the precise missing approval rather than interpreting workflow continuation as approval. |
| Tests passed, then relevant source changed; user asks to continue review | Old tests are not current completion evidence; affected tests/review must be renewed before completion. |
| Checkpoint says running and prior execution liveness cannot be established | No takeover, duplicate dispatch or overwrite of its checkpoint/guide; report the concrete ownership blocker. |
| A reported bug has an established contract but no reproduction/cause evidence | Classify as fix; investigate only within authority or block for the missing prerequisite before product-fix planning/edits. |
| A request labelled bug asks for behavior beyond the existing contract | Classify the behavior change as feature or expose a genuine contract ambiguity; do not treat the label as proof of a defect. |
| Standalone build discovers a substantive departure from the validated design | Stop affected implementation and return the proposed revision for plan/validate and required approval. |
| Two different failed fixes assume the same cause; a third is requested | Test the common premise before another product fix; preserve prior failures and stop if distinguishing evidence is unavailable. |
| A technical disagreement is answerable by an authorized existing command | Obtain that evidence before asking the user to choose; do not bypass required execution approval. |
| Performance comparison reports lower latency but errors or actual work are unaccounted for | Do not endorse a speedup; identify missing correctness/work evidence and use the conditional performance rules. |

Use the status-only, approval, stale-evidence and uncertain-liveness cases for checkpoint-control changes. Add the fix, feature, standalone, premise, question or performance cases only where the revised rules reach them. Do not run optional product regressions as part of this skill-authoring check.
