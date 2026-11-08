# Independent review: overengineering

Every independent peer must assess whether the proposed solution, implementation, tests, and workflow are more complex than the confirmed requirements and demonstrated risks require.

- Identify unnecessary abstractions, options, dependencies, files, artifacts, duplicate tests, fragmented tasks, repeated reviews, and redundant approval requests. Prefer existing code, reuse, and deletion when they fully meet the requirements.
- For complexity worth retaining, name the requirement, observed failure, or concrete constraint that justifies it. Recommend the smallest complete alternative where one exists; do not add speculative hardening to completion criteria.
- Preserve correctness, failure handling, resource ownership, security, and required assertions. Fewer lines or checks alone do not establish a better solution.

Include material simplifications in the existing stage output. The stage owner must adopt them or briefly explain why the extra complexity is necessary. If none are supported, do not invent findings.

Perform this check within the existing peer interaction, including follow-ups. It requires no additional agent, stage, report, or checklist and does not waive actual approval or repository requirements.
