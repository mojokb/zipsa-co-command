# Independent review: overengineering

Every independent peer must assess whether the proposed solution, implementation, tests, and workflow are more complex than the confirmed requirements and demonstrated risks require.

- Identify unnecessary abstractions, options, dependencies, files, artifacts, duplicate tests, fragmented tasks, repeated reviews, and redundant approval requests. Prefer existing code, reuse, and deletion when they fully meet the requirements.
- For complexity worth retaining, name the requirement, observed failure, or concrete constraint that justifies it. Recommend the smallest complete alternative where one exists; do not add speculative hardening to completion criteria.
- Preserve correctness, failure handling, resource ownership, security, and required assertions. Fewer lines or checks alone do not establish a better solution.

Include material simplifications in the existing stage output. The stage owner must adopt them or briefly explain why the extra complexity is necessary. If none are supported, do not invent findings.

Perform this check within the existing peer interaction, including follow-ups. It requires no additional agent, stage, report, or checklist and does not waive actual approval or repository requirements.

## Claude account authorization fallback

If Claude cannot run because of an account authorization HTTP 403 (for example, `oauth_not_allowed_for_organization`), replace that stage's Claude peer with an additional independent Codex reviewer. Do not retry the same denied request or silently reduce the stage to a single perspective. This exception does not apply to unrelated HTTP 403 responses or other CLI failures.

Use a fresh isolated Codex agent/session with no inherited conversation when available. Give it the same authoritative requirements, exact target revision, raw evidence, constraints and review criteria that Claude would receive, including the simplicity check above. Do not supply the primary Codex's conclusions or proposed findings. Restrict it to read-only inspection; it must not edit files, execute tests, post externally, merge or deploy. The primary Codex completes its own analysis before reading the peer result, validates material findings against the sources, resolves disagreements and retains final responsibility. For test design, the peer forms its initial cases from the requirements before reading implementation or existing tests.

Keep the independent Codex result and agent/session identifier with the stage's existing evidence. Report “Claude unavailable: account authorization 403; independent Codex review completed” only after obtaining the result. Identify this as a second Codex perspective, not Claude feedback or evidence of cross-model agreement. If no separate Codex session can run, disclose that independent review remains incomplete and use the stage's existing responsible single-perspective fallback only where permitted; never count the primary agent rereading its own work as independent review. Keep the existing stage scope and approval boundaries.
