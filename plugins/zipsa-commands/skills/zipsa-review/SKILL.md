---
name: zipsa-review
description: Dual-perspective code review — Agent as Junior BE developer, Codex as Senior developer. Reviews code against SOLID, Clean Code, linting, readability, 80-line function limit, Google style docstring compliance. If REST API code is detected, also reviews RESTful compliance, OpenAPI spec, and agent-readability. Pass a file path, directory, or leave empty to review current git diff.
---

# Zipsa-Review: Dual-Perspective Code Review

**Agent role:** Junior Backend Engineer — reads the code as someone who must understand, maintain, and extend it. Flags anything confusing, hard to follow, or that would slow down a new contributor.

**Codex role:** Senior Engineer — reviews from an architectural, correctness, and production-readiness perspective. Catches design flaws, edge cases, and systemic issues.

## Arguments

`$ARGUMENTS` should be a file path, directory path, or glob pattern to review. If not provided, default to `git diff HEAD`. If the working tree is clean, fall back to `git diff HEAD~1`.

## Step 1: Collect the Target Code and Spawn Codex Simultaneously

Do both at the same time:

**1a. Resolve the review target:**
- If `$ARGUMENTS` is provided: read the file(s) at the given path.
- If not provided: run `git diff HEAD`; fall back to `git diff HEAD~1` if empty.

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
   - Are functions within the length limit? (≤40 lines for Python, ≤60 lines for Go) Flag any function that exceeds this limit.
   - Is there duplication that should be extracted?
   - Are there magic numbers, unclear booleans, or tangled conditional logic?
   - Does the code have dead code, commented-out blocks, or stale TODOs?

3. **Lint / Style**
   - Are there violations of language idioms (PEP 8 for Python, gofmt/golangci-lint for Go)?
   - Are error values handled correctly (no bare `except`, no ignored `err` in Go)?
   - Are there missing type hints (Python) or improper use of `any`/`interface{}` (Go)?
   - Are imports organized and unused imports removed?

4. **Google Style Docstrings**
   - Does every public function, method, and class have a Google style docstring?
   - Does the docstring describe what the function does (not how)?
   - Are all arguments documented under `Args:` with name, type, and description?
   - Are return values documented under `Returns:` with type and description?
   - Are raised exceptions documented under `Raises:`?
   - Are docstrings accurate — do they match the actual behavior of the code?

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
- 🟠 **Major** — significant design flaw, missing docstring on public API, or spec mismatch that blocks integration
- 🟡 **Minor** — style or clarity issue; fix if time permits
- 🟢 **Suggestion** — optional improvement worth considering

Do NOT share your review yet. When your review is fully formed, respond with exactly: "My review is complete and I'm ready to present" and nothing else.

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
   - Flag any function exceeding the limit (≤40 lines for Python, ≤60 lines for Go)
   - Are names clear enough without needing to trace the implementation?
3. **Lint / Style** — language idioms, error handling, type annotations, imports
4. **Google Style Docstrings**
   - Is every public function/method/class documented?
   - Do `Args:`, `Returns:`, `Raises:` sections exist and match the actual code?
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
