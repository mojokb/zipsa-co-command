# Reader-facing reporting

Apply these rules to issue comments and the feature's HTML guide. They govern presentation, not execution authority or evidence. Keep the repository's posting, confirmation and reporting conventions. Do not edit past comments or rewrite existing guides merely because these rules changed.

## Issue comments

The reporting target is the issue comments, not the issue itself. Put investigation, correction and verification evidence in relevant comments. Leave the issue title, body, requirements, completion criteria and state unchanged unless the user separately requests those changes. For an authorized comment update, preserve valid evidence and update the relevant existing comment rather than duplicating it; add a comment only when distinct new evidence has no appropriate existing comment.

Issue comments preserve facts needed to resolve the issue and debug it later. Before posting, check whether the new information helps reproduce, explain, fix, or verify the issue, or investigate a later failure. If it does not, do not post. Completing a workflow stage alone is not a reason to update the issue.

When posting is already authorized, lead with a plain-language summary for the project owner: what happened, what the result means, what remains uncertain, and what decision or next action is needed. Make it understandable without opening technical evidence. Keep failures, material limitations and required decisions visible in this summary; do not hide them only inside a collapsed section. Distinguish observations from hypotheses and untested conditions.

Use subject-based hierarchy in both the summary and the detailed evidence: top-level bullets name the subjects, and nested bullets contain their related facts. Keep unrelated subjects in separate bullets. Choose subjects that fit the comment rather than forcing a fixed inventory.

Put agent-facing details needed for reproduction, verification or continuation in a default-collapsed `<details>` block with a descriptive `<summary>`, such as `에이전트용 상세 근거 — 재현 조건·측정값·미확인 항목`. Preserve applicable inputs, environment and revision identities, measurement windows and units, commands, source lines, logs, evidence links and unchecked conditions there. Include details only when they help resolve or later debug the issue; do not invent metadata or create an empty toggle. Keep a blank line after `</summary>` and before `</details>` so the nested Markdown renders. Do not add the `open` attribute. An agent label does not grant execution or posting authority.

Keep routine progress, phase completion, reviewer/tool execution status, and next-stage announcements in chat, the workflow checkpoint or the HTML guide. Omit repeated explanations, superseded tool errors and validation that does not change the issue judgment. Mention an unexecuted check only when its missing evidence matters to resolving or verifying this issue; state the unchecked condition rather than a task queue. Do not post merely to report that another stage is next.

For example, using only the facts actually established for the issue:

- **확인 결과**

  - 한계값을 바꿀 때 저장된 후보를 현재 한계로 다시 판정하도록 수정했습니다.
  - 같은 후보에 서로 다른 한계를 적용한 검사에서 현재 한계에 맞는 결과를 확인했습니다.

- **확인 한계**

  - 여러 요청이 동시에 들어오는 조건은 아직 확인하지 않았습니다.

<details>
<summary>에이전트용 상세 근거 — 재현 조건·검증 범위</summary>

- **재현 조건과 수정 근거**

  - 수정 전에는 한계값만 바꾸면 저장된 후보를 다시 판정하지 않아 이전 결과가 반환됐습니다.
  - 후보는 재사용하고 적합 여부는 현재 한계로 다시 판정합니다.

- **검증 범위**

  - 같은 후보에 서로 다른 한계를 적용해 각 결과가 현재 한계를 따르는지 확인했습니다.
  - 동시 요청이 겹치는 조건은 미확인입니다.

</details>

Omit skill names, invocation commands and stage-completion labels from issue comments. These rules do not authorize posting, changing an issue body, or editing historical comments. Keep requirements and completion criteria in the issue body; preserve implementation and test evidence in their existing artifacts.

## HTML explanations

Write for the project owner who has not read the chat or the implementation. At the end of a stage, refresh the opening summary and next action so the reader can answer: what was requested, what changed or was learned, what that means for using or finishing the feature, what remains unresolved, and who does what next. Keep earlier evidence as history, but make the latest conclusion easy to find.

Lead each stage explanation with the task's purpose and outcome. Connect the work to its effect: explain what now works, what still cannot be relied on, or which decision is needed. Do not narrate the agent's commands or simply list files and tests. Explain necessary technical terms at first use with familiar language; use full, naturally spaced Korean sentences rather than compressed fragments or internal status labels.

Keep code paths, commit hashes, commands, detailed logs and implementation inventories in evidence links or expandable technical details, outside the summary, next action, titles, explanations and items. If no evidence link is available, omit incidental metadata rather than inventing links. The visible explanation must stand on its own without opening those links. Preserve precise technical details when they change the user's decision, and explain why they matter.

Report observations separately from assumptions and plans. Say what the tests cover and what important condition remains unchecked. Distinguish a finished stage from a finished feature; a passing test count must not hide an unresolved result or imply an unexecuted check passed. If a decision is needed, name the decision and its consequence; otherwise give the concrete next action and responsible person or agent.

For example, a completed implementation with unfinished integration checks can say:

> 한계값을 바꿀 때 후보를 다시 탐색하지 않고 저장된 후보로 화면을 갱신하도록 구현했습니다. 관련 자동 검사 50건은 통과했습니다. 다만 개발환경에서 여러 요청을 함께 보낼 때도 결과가 유지되는지는 아직 확인하지 않았습니다. 구현은 끝났지만 전체 검증은 남아 있습니다. 다음에는 에이전트가 개발환경에서 동시 요청을 확인합니다.

The example illustrates wording only; use the actual task, counts, environment, uncertainty and authority. Before finishing, read the summary and latest stage without their evidence links: the reader should understand the result and next step without earlier conversation. Formatting or shorter text alone does not satisfy this check.
