# Add zipsa-review Skill

## Goal

Add a `/zipsa-review` skill that reviews code from a senior engineer's perspective, covering SOLID principles, Clean Code, Lint/Style, and Optimization. The skill follows the same anti-bias pattern as `/zipsa-plan`, `/zipsa-validate`, and `/zipsa-brainstorm`.

## Design

### Review Axes

Base axes (always applied):

| Axis | What it checks |
|---|---|
| SOLID Principles | SRP, OCP, LSP, ISP, DIP violations |
| Clean Code | Naming, function length, duplication, magic values, dead code |
| Lint / Style | Language idioms, error handling, type annotations, import hygiene |
| Optimization | Algorithmic complexity, allocations, IO batching, resource leaks |

REST API axes (applied only when REST API code is detected):

| Axis | What it checks |
|---|---|
| RESTful Compliance | HTTP method semantics, resource URL design, status codes, statelessness, pagination, error consistency |
| OpenAPI / Schema Compliance | Annotation completeness, parameter declarations, response schema accuracy, 4xx/5xx error schemas |
| API Comments (Agent-Readability) | Endpoint descriptions, parameter clarity, field documentation, agent-only-readable completeness, deprecation notices |

### REST API Detection

The skill auto-detects REST API code by looking for:
- Route/path decorators: `@app.get`, `@router.post`, `r.GET`, `r.HandleFunc`, etc.
- Handler function signatures with request/response parameters
- OpenAPI annotations: `swagger:`, `@OperationId`, `openapi`, etc.
- File names containing: `router`, `handler`, `controller`, `api`, `endpoint`

### Severity Labels

| Label | Meaning |
|---|---|
| 🔴 Critical | Correctness bug, security hole, or will break in production |
| 🟠 Major | Significant design flaw or performance problem — fix before merge |
| 🟡 Minor | Style or clarity issue — fix if time permits |
| 🟢 Suggestion | Optional improvement worth considering |

### Input Resolution

`$ARGUMENTS` is a file path, directory, or glob. If omitted:
1. `git diff HEAD` (unstaged + staged changes)
2. `git diff HEAD~1` if working tree is clean

### Anti-Bias Pattern (same as all co-* skills)

```
Step 1: Detect REST API? → select base prompt or base + REST addendum
         Spawn background Codex subagent → Codex reviews independently
         └─ Codex prompt: explore codebase → review across axes → hold result
Step 2: Agent does its own independent review across same axes
         └─ Must NOT check Codex result until own review is done
Step 3: Retrieve Codex result → compare → merge into final report
         └─ Prioritized action list at the end
```

This ensures both reviewers form opinions without influencing each other.

## Codex Prompt Design (Step 1)

The prompt is composed of three parts:

1. **Base prompt** — always included; covers SOLID, Clean Code, Lint, Optimization
2. **REST API addendum** — appended only when REST API code is detected; covers RESTful Compliance, OpenAPI/Schema Compliance, API Comments
3. **Closing** — always appended; severity taxonomy, deferred-reveal gate, code block

Key design choices:

- **Axis-first structure** — grouping by axis (not by file/line) forces a systematic sweep rather than ad-hoc comments
- **Explicit severity taxonomy** — prevents vague "this could be better" feedback; every finding must be labeled
- **Line number citation required** — makes feedback actionable and verifiable
- **Conditional REST axes** — REST-specific checks are only meaningful for API code; including them for all code would generate noise and dilute signal
- **Agent-readability axis** — "would another coding agent call this correctly based only on comments?" is a stricter and more actionable question than "are comments good?" It targets the real failure mode: under-documented parameters and response shapes that force agents to read the implementation
- **"Do NOT share yet" gate** — same deferred-reveal mechanism used by all co-* skills to prevent bias

## Final Report Format

```
## Code Review

### 1. SOLID Principles
### 2. Clean Code
### 3. Lint / Style
### 4. Optimization

<!-- REST API only -->
### 5. RESTful Compliance
### 6. OpenAPI / Schema Compliance
### 7. API Comments (Agent-Readability)

---
### Action List (prioritized)
1. 🔴 ...
2. 🟠 ...
```

## Files Changed

| File | Change |
|---|---|
| `plugins/co-commands/skills/zipsa-review/SKILL.md` | New skill definition |
| `docs/add-zipsa-review.md` | This design record |

## Version

No version bump in this commit — version will be bumped when the skill is finalized and tested.
