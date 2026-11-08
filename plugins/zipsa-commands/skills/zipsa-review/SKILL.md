---
name: zipsa-review
description: Dual-perspective code review — Agent as Junior BE developer, Codex as Senior developer. Reviews code against SOLID, Clean Code, linting, readability, Python 40-line function limit excluding docstrings and Go 60-line limit, Google style docstring compliance. If REST API code is detected, also reviews RESTful compliance, OpenAPI spec, and agent-readability. Pass a path or change range; otherwise review the tested scope when available, falling back to the current git diff for standalone reviews.
---

# Zipsa-Review: Dual-Perspective Code Review

## Human-facing reports and HTML

Follow the [shared reporting rules](../zipsa-workflow/references/reporting.md) for issue comments and HTML wording.

Follow the [shared HTML guide contract](../zipsa-workflow/references/html-guide.md) on entry, after each meaningful internal step, and before yielding or completing, including standalone invocation. Update the feature's integrated HTML with plain explanations, observed results, uncertainty, original evidence and next actions; preserve other steps and return its path. This presentation does not replace canonical artifacts or grant execution/approval authority.

## Independent simplicity check

Include the [shared overengineering check](../zipsa-workflow/references/independent-review.md) in every independent peer prompt, including follow-ups, and apply its findings in the existing stage comparison.

## Performance work only

If this task has performance acceptance criteria or measures/reports a speedup or regression, read the [conditional performance rules](../zipsa-workflow/references/performance.md). Apply only the evidence needed for that claim; do not add benchmarks to unrelated work.

## Compare the change with the approved plan

Read the linked authoritative requirements, approved plan revision, task list, and verification evidence when available; supply these references to the peer reviewer along with the exact review target. Independently compare the actual changes against each in-scope requirement and the approved plan. Report omitted requirements, changes outside the plan, and whether departures have a recorded reason and required approval. A later plan edit alone is not evidence of approval.

Check that verification evidence applies to the reviewed commit or working tree; report material changes after the checks as unverified. Cite requirement IDs, plan sections, and code lines in findings where applicable. If the requirements, approved baseline, or evidence cannot be found, state the resulting review limitation without inventing a record or blocking a standalone code review. Keep this disposition in the existing review output rather than a separate report.

Review the test scenarios and assertions against authoritative requirements and API contracts, not just the implementation. Check relevant failure paths, integration boundaries, and whether mocks or missing environments leave required behavior unverified. Agent agreement and coverage percentages alone do not prove correctness. After review fixes change code, tests, fixtures, or configuration, rerun the affected tests and required repository checks against the updated target; keep earlier results as history, not current proof. A standalone review may report missing evidence without executing tests, but must not claim the change is fully verified.

**Agent role:** Junior Backend Engineer — reads the code as someone who must understand, maintain, and extend it. Flags anything confusing, hard to follow, or that would slow down a new contributor.

**Codex role:** Senior Engineer — reviews from an architectural, correctness, and production-readiness perspective. Catches design flaws, edge cases, and systemic issues.

## Arguments

`$ARGUMENTS` should identify the path or change range to review. Without an explicit target, use the complete tested range/snapshot from the zipsa-test handoff, including later changes. For a standalone review without that handoff, default to `git diff HEAD`; if clean, fall back to `git diff HEAD~1`. State any difference between the requested and tested scopes.

## Step 1: Collect the Target Code and Spawn Codex Simultaneously

Do both at the same time:

**1a. Resolve the review target:**
- If `$ARGUMENTS` is provided: resolve and read the specified paths or change range.
- Otherwise, use the complete range/snapshot identified by the zipsa-test handoff and include later changes; report missing snapshots or unresolvable revisions as scope limitations.
- Only without a handoff, run `git diff HEAD`; fall back to `git diff HEAD~1` if empty, and identify this standalone scope.

Detect whether the code is REST API code. Signals: route/path decorators (`@app.get`, `@router.post`, `r.GET`, etc.), handler functions with request/response parameters, OpenAPI annotations (`swagger`, `openapi`, `@OperationId`, etc.), or files named `router`, `handler`, `controller`, `api`, `endpoint`.

**1b. Spawn a background subagent for Codex** (Task tool with `run_in_background: true`). The subagent should:

1. Call `mcp__validate-plans-and-brainstorm-ideas__codex` with:
   - `prompt`: construct exactly as shown below
   - `sandbox`: `read-only`
   - `approval-policy`: `never`
   - `cwd`: (use the current working directory)
2. If Codex asks clarifying questions, answer using codebase context and wait for it to finish.
3. Once Codex says "My review is complete and I'm ready to present", report back the `threadId` and that Codex is ready — but do NOT retrieve the review yet.

### Codex Prompt (Senior Engineer perspective)

The prompt has a **base** (always included) and a **REST API addendum** (append only when REST API code is detected).

#### Base prompt

```text
First, explore the codebase in your working directory to understand the project structure, language conventions, and existing patterns.

You are acting as a **Senior Engineer**. Review the following code from an architectural, correctness, and production-readiness perspective. Evaluate across these axes — be specific, cite line numbers or code snippets where relevant:

1. **SOLID Principles**
   - Single Responsibility: does each class/function own exactly one concern?
   - Open/Closed: is behavior extended via new types rather than editing existing code?
   - Liskov Substitution: do subtypes honor the contract of their parent?
   - Interface Segregation: are interfaces small and focused, not bloated?
   - Dependency Inversion: does the code depend on abstractions, not concrete implementations?

2. **Clean Code**
   - Are names (variables, functions, types) intention-revealing and unambiguous?
   - Does any code require a comment to understand what it does? (Hard-to-read logic, non-obvious control flow, clever one-liners — flag these)
   - Are functions within the length limit? (≤40 lines for Python, excluding docstring lines; ≤60 lines for Go) Flag any function that exceeds this limit.
   - Is there duplication that should be extracted?
   - Are there magic numbers, unclear booleans, or tangled conditional logic?
   - Does the code have dead code, commented-out blocks, or stale TODOs?

3. **Lint / Style**
   - Are there violations of language idioms (PEP 8 for Python, gofmt/golangci-lint for Go)?
   - Are error values handled correctly (no bare `except`, no ignored `err` in Go)?
   - Are there missing type hints (Python) or improper use of `any`/`interface{}` (Go)?
   - Are imports organized and unused imports removed?

4. **Google Style Docstrings**
   - Does every public function, method, class, **and exported type** have a docstring? A **missing docstring on any public API is a 🟠 Major finding** (not Minor).
   - **If a docstring exists, it MUST follow Google docstring format.** A docstring that exists but is not Google style (missing `Args:`/`Returns:`/`Raises:` sections where applicable, or freeform prose for a function with arguments/returns) is a 🟠 Major finding — "present but wrong format" is treated as seriously as "missing".
   - **The docstring must be agent-readable**: a coding agent that has NOT seen the implementation must be able to understand what the symbol does, what each argument means (meaning, unit, format, valid range), what is returned, and what errors/edge cases occur — from the docstring alone. Vague or implementation-restating docstrings that fail this bar are 🟠 Major.
   - Does the docstring describe what the function does (not how)?
   - Are all arguments documented under `Args:` with name, type, and description?
   - Are return values documented under `Returns:` with type and description?
   - Are raised exceptions documented under `Raises:`?
   - Are docstrings accurate — do they match the actual behavior of the code?
   - Note on Go: Go uses `// Symbol ...` doc comments rather than `Args:/Returns:` sections; apply the same bar — every exported symbol documented, accurate, and agent-readable; missing or inaccurate exported-symbol docs are 🟠 Major.

5. **Optimization & Correctness**
   - Are there obvious algorithmic inefficiencies (e.g., O(n²) where O(n) is possible)?
   - Are there unnecessary allocations, redundant computations, or blocking calls in hot paths?
   - Are database/IO calls batched where possible?
   - Are there resource leaks (unclosed connections, files, goroutines)?
   - Are there correctness bugs, off-by-one errors, or unhandled edge cases?
```

#### REST API addendum (append when REST API code is detected)

```text
6. **RESTful Compliance**
   - Are HTTP methods used semantically correctly? (GET = read/idempotent, POST = create, PUT = full replace, PATCH = partial update, DELETE = remove)
   - Are resource URLs noun-based and hierarchical? (e.g., `/users/{id}/orders`, not `/getUser`)
   - Are HTTP status codes semantically accurate? (200, 201, 204, 400, 401, 403, 404, 409, 422, 500)
   - Is the API stateless?
   - Are collection endpoints paginated where the result set could be large?
   - Are error responses consistent in structure across all endpoints?

7. **OpenAPI / Schema Compliance**
   - Does every endpoint have a complete OpenAPI annotation: `operationId`, `summary`, `description`, request body schema, all response schemas including errors?
   - Are all path parameters, query parameters, and headers declared?
   - Do actual response payloads match the declared schema?
   - Are enum values and constraints (min/max, pattern, format) declared?
   - Are 4xx and 5xx error schemas defined and consistent?
   - **Response struct `required` field contract (Go/swaggo):** For each response struct, verify that fields always present in the JSON output are marked `binding:"required"` (swaggo uses this to emit `required` in the OpenAPI schema), and that nullable or conditionally-omitted fields (pointer types, `omitempty`) do NOT have `binding:"required"`. Also check that `binding:"required"` is not applied to request-parsing structs used as response types — that is a misuse that causes silent contract drift.

8. **API Comments (Agent-Readability)**
   - Does each endpoint description explain: what it does, what triggers each error, and any non-obvious side effects or preconditions?
   - Are parameter descriptions unambiguous enough that a coding agent can call the API correctly without reading the implementation?
   - Are request/response field descriptions accurate with meaning, unit, format, and valid range?
   - Are deprecated fields or endpoints marked with `deprecated: true` and a migration note?
```

#### Closing (always append)

```text
For each finding, assign a severity:
- 🔴 **Critical** — correctness bug, security hole, or will break in production
- 🟠 **Major** — significant design flaw; spec mismatch that blocks integration; or any public-API docstring defect: missing, not in Google docstring format, inaccurate, or not agent-readable
- 🟡 **Minor** — style or clarity issue; fix if time permits
- 🟢 **Suggestion** — optional improvement worth considering

Do NOT share your review yet. When your review is fully formed, respond with exactly: "My review is complete and I'm ready to present" and nothing else.

Requirements and plan context:
{include the authoritative requirements with stable IDs and source revision, the plan revision and approval status, the task-list reference and revision, and any relevant user-confirmed decisions; mark unavailable records explicitly}

Verification evidence:
{include the zipsa-test results when available: scenarios, expected-result sources, selected test levels and limitations, checks, results, evidence locations, and tested commit or working-tree snapshot}. Review assertion validity, failure paths, integration boundaries, and evidence freshness against the supplied requirements and contracts.

Code to review:
<code>
{paste the full file contents or git diff here}
</code>
```

## Step 2: Do Your Own Review (Junior BE Perspective)

While Codex works in the background, do your own independent review **as a Junior Backend Engineer** — someone who must read, understand, and maintain this code. Ask yourself: "Would I understand this six months from now without asking anyone?"

Review across these axes:

1. **SOLID Principles** — identify violations by principle name
2. **Clean Code**
   - Is every piece of logic easy to follow on first read?
   - Flag any code that made you pause and re-read to understand
   - Flag any function exceeding the limit (≤40 lines for Python, excluding docstring lines; ≤60 lines for Go)
   - Are names clear enough without needing to trace the implementation?
3. **Lint / Style** — language idioms, error handling, type annotations, imports
4. **Google Style Docstrings** (every defect here is 🟠 Major)
   - Is every public function/method/class/exported type documented? Missing → 🟠 Major.
   - If a docstring exists, is it in Google docstring format? Present-but-not-Google-style → 🟠 Major (as serious as missing).
   - Is it agent-readable — could an agent that never saw the implementation call/use this symbol correctly from the docstring alone (arg meaning/unit/range, return, errors)? If not → 🟠 Major.
   - Do `Args:`, `Returns:`, `Raises:` sections exist and match the actual code? (Go: `// Symbol ...` doc comments held to the same bar.)
5. **Optimization & Correctness** — obvious inefficiencies, edge cases, resource leaks

If REST API code was detected, also review:

6. **RESTful Compliance**
7. **OpenAPI / Schema Compliance** — including the response struct `required` field contract: always-present fields have `binding:"required"`, nullable/omitempty fields do not
8. **API Comments (Agent-Readability)**

For each finding assign severity: 🔴 Critical / 🟠 Major / 🟡 Minor / 🟢 Suggestion.

**Do NOT check the Codex result until your own review is complete.**

## Step 3: Retrieve Codex Review and Merge

Once your review is done, use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` with:

- `threadId`: thread ID from Step 1b
- `prompt`: `Go ahead, share your review. Be direct and specific. Cite line numbers. Use severity labels. Do not repeat the code.`

Then merge both reviews:

- **Agreed findings** → include once, note both perspectives agree
- **Codex-only findings** → validate independently before including; note source as Senior perspective
- **Your-only findings** → keep if confident; note source as Junior/readability perspective
- **Conflicting assessments** → state both and give your ruling

## Output Format

```
## Code Review

> Agent: Junior BE perspective | Codex: Senior perspective

### 1. SOLID Principles
[findings with severity and source]

### 2. Clean Code
[findings with severity and source]

### 3. Lint / Style
[findings with severity and source]

### 4. Google Style Docstrings
[findings with severity and source]

### 5. Optimization & Correctness
[findings with severity and source]

<!-- Include sections 6–8 only when REST API code was detected -->
### 6. RESTful Compliance
[findings with severity and source]

### 7. OpenAPI / Schema Compliance
[findings with severity and source]

### 8. API Comments (Agent-Readability)
[findings with severity and source]

### Plan Conformance and Verification
[requirements / plan revisions; omitted requirements; changes outside the plan and their approval; assertion validity and test gaps; evidence applicable to the review target; required reruns or unverified criteria]

---
### Action List (prioritized)
1. 🔴 [critical fix]
2. 🟠 [major fix]
...
```

## Continuing The Conversation

Use `mcp__validate-plans-and-brainstorm-ideas__codex-reply` to follow up — ask for elaboration, push back on a finding, or request a concrete refactor example.

## How To Treat Codex Responses

- Codex is the Senior voice, but Senior engineers can still be wrong — validate findings before accepting.
- You are the lead engineer and have final say.
- Junior perspective findings (readability, clarity) are equally valid — do not discard them just because Codex didn't raise them.

## Reporting After Fixes Are Applied

When the user asks you to apply the review's Action List and you report the result, the report has two parts, in this order:

1. **반영 요약 (technical)** — one bullet per Action List item: what changed, where, and how it was verified (test name, mutation check, command).
2. **쉬운 설명 (plain language)** — the same items again for a reader who has not read the code. Each bullet says what could go wrong before, what the fix does now, and how we know it works. No identifiers beyond one per bullet; describe the rest in words. State plainly what did NOT change (e.g. "설정 자체는 바뀌지 않았다. 검사만 강화했다").

Both parts are mandatory. Do not merge them into one list.
