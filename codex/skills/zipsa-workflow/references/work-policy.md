# Work type and investigation

Apply within the invoking stage's authority, including standalone use. These rules add no stage, peer, approval or permission to edit, execute diagnostics, post externally or reset data.

## Classify by the existing contract

- `fix` restores behavior already required by an authoritative contract, confirmed requirement or established supported behavior. Name that source; a bug label alone is insufficient. If sources conflict materially, resolve their authority with existing project decisions or ask about the contract instead of choosing convenient behavior.
- `feature` adds or intentionally changes behavior beyond that contract. Confirm scope and observable acceptance criteria before planning.
- For mixed work, classify the affected requirements/tasks separately and retain both sets of checks. Do not disguise a new behavior as a fix or silently expand a fix's scope.

Record the type and its source in existing requirements/tasks, or the workflow checkpoint. Reuse verified evidence; missing historical classification does not invalidate otherwise current work. If the contract itself is unclear, grill resolves it before selecting a remedy. Think compares material alternatives only after the relevant expectations and, for fixes, the cause are established.

## Fix evidence before product edits

Before planning a product fix, establish the expected behavior and source, reproducible inputs/preconditions, observed failure, affected target/environment and a causal mechanism supported by observations that distinguish it from plausible competing causes. Identify which observation supports the diagnosis; a guess or peer agreement is insufficient. Use existing authorized commands or focused diagnostics on the affected interface. Keep the command/manual steps, observations and source/log references in existing task or requirements evidence. Code inspection alone must not be presented as an executed reproduction.

Grill gathers missing diagnostic evidence without implementing the fix. If existing diagnostics cannot establish it, record what is unverified and the environment, access or proposed diagnostic change needed; do not invent a cause or implement a speculative product fix. Diagnostic code/test edits require their own applicable authorization and must not be smuggled into requirements clarification. Reuse supplied evidence only when its target, environment and inputs still apply, explaining any equivalence; do not rerun it merely for ceremony. A regression test may serve as diagnostic evidence and retained coverage, but creating it still requires applicable test-edit authority.

Standalone build checks the same evidence before product edits. Missing evidence permits authorized investigation, not implementation. Test carries the original reproducer forward, verifies the same affected behavior after the fix and checks relevant regressions; unit success on another interface does not establish that the original symptom is gone.

## Classify questions before asking

Separate facts discoverable from code/documents, facts observable through authorized execution, and user-owned scope, policy, acceptance or preference decisions. Inspect the first category and investigate the second within existing permissions before asking the user. Technical disagreement alone is not a product decision: seek distinguishing evidence and choose the smallest supported approach. Ask only for a remaining material decision or genuinely unavailable information/access. State checked evidence, the surviving uncertainty and a reasoned default when useful. Do not run an unapproved experiment to avoid a required confirmation; preserve repository confirmation gates.

## Repeated fixes with one premise

After two fixes sharing a premise fail the same behavioral check with a materially matching symptom, record that common premise and test an observation that distinguishes it from a competing explanation before a third fix. Keep failed remedies and their target identities in existing evidence. A different edit or another peer's agreement is not new causal evidence. If the premise is contradicted, discard it and revisit diagnosis/plan as needed; remove ineffective changes only within existing edit authority, preserving unrelated user work. If it cannot be tested, stop the affected work with the concrete missing input rather than retrying. This supplements the ban on rerunning unchanged failures.
