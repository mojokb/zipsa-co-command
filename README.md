# zipsa-co-work

6 collaboration commands for Claude Code that use the [Codex MCP server](https://github.com/openai/codex) as a second opinion — covering the full workflow from brainstorming through implementation.

## Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/zipsa-think` | Bounce ideas off Codex | Want fast alternative ideas, critiques, and perspectives |
| `/zipsa-plan` | Generate a parallel plan via Codex | Want a second opinion on your planning approach |
| `/zipsa-validate` | Get a staff engineer review of your plan | Want critical feedback before finalizing a plan |
| `/zipsa-tasks` | Break a validated plan into implementation tasks | Want a concrete, ordered task list with acceptance criteria |
| `/zipsa-build` | Implement tasks with Codex as approach reviewer | Want to implement incrementally with a second opinion on each approach |
| `/zipsa-review` | Dual-perspective code review via Codex | Want a multi-axis review before merging |

## Installation

See [docs/installation.md](docs/installation.md) for the full installation guide.

## Workflow

The commands form a natural pipeline:

```
/zipsa-think → /zipsa-plan → /zipsa-validate → /zipsa-tasks → /zipsa-build → /zipsa-review
```

Use as many or as few steps as needed — each command is independent.

## Command Details

### `/zipsa-think`

Starts an interactive brainstorming session with Codex. Pass your topic or question as the argument.

```
/zipsa-think how should we structure the authentication system
```

Agent and Codex brainstorm independently, then compare ideas. Supports follow-up conversation to dig deeper.

### `/zipsa-plan`

Generates an alternative plan in the background while you continue your own planning. Pass your task description as the argument.

```
/zipsa-plan add user authentication with OAuth2 support
```

Compare the Codex plan against yours to catch missed approaches, simpler alternatives, or overlooked edge cases.

### `/zipsa-validate`

Sends your plan to Codex for a staff-engineer-style review. Pass the path to your plan file.

```
/zipsa-validate .claude/plans/my-plan.md
```

Agent and Codex each independently review the plan, then findings are compared. Returns critical issues, simplification opportunities, and alternative approaches. Supports back-and-forth discussion.

### `/zipsa-tasks`

Breaks a validated plan into concrete, ordered implementation tasks. Pass the path to your plan file.

```
/zipsa-tasks .claude/plans/my-plan.md
```

Agent and Codex collaborate to surface and resolve every ambiguity in the plan (only escalating unresolvable decisions to the user), then independently produce task breakdowns and merge them into a final ordered list. Each task includes what to build, acceptance criteria, and dependencies.

### `/zipsa-build`

Implements tasks from a task list one by one, with Codex reviewing the approach before each implementation. Pass the path to the tasks file (e.g. from `/zipsa-tasks`).

```
/zipsa-build .claude/plans/my-tasks.md
```

For each task, Agent and Codex independently design the implementation approach, compare, resolve any disagreements, then Agent implements and verifies the acceptance criteria before moving to the next task.

### `/zipsa-review`

Dual-perspective code review. Pass a file path, directory, or leave empty to review the current git diff.

```
/zipsa-review src/api/users.py
/zipsa-review src/handlers/
/zipsa-review                   # reviews current git diff
```

**Agent role:** Junior Backend Engineer — flags anything confusing, hard to follow, or that would slow down a new contributor.

**Codex role:** Senior Engineer — reviews from an architectural, correctness, and production-readiness perspective.

Evaluates code across five axes:

| Axis | What it checks |
|------|----------------|
| SOLID Principles | SRP, OCP, LSP, ISP, DIP violations |
| Clean Code | Naming, function length, duplication, magic values, dead code |
| Lint / Style | Language idioms, error handling, type annotations, import hygiene |
| Google Style Docstrings | Completeness and accuracy of Args, Returns, Raises sections |
| Optimization & Correctness | Algorithmic complexity, allocations, IO batching, resource leaks, correctness bugs |

When REST API code is detected (route decorators, handler signatures, OpenAPI annotations), three additional axes are automatically included:

| Axis | What it checks |
|------|----------------|
| RESTful Compliance | HTTP method semantics, resource URL design, status codes, statelessness, pagination |
| OpenAPI / Schema Compliance | Annotation completeness, parameter declarations, response schema accuracy, error schemas |
| API Comments (Agent-Readability) | Whether another coding agent can call the API correctly based solely on comments and schema |

Each finding is labeled 🔴 Critical / 🟠 Major / 🟡 Minor / 🟢 Suggestion with a prioritized action list at the end.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `npx: command not found` | Install [Node.js](https://nodejs.org/) which includes npm/npx |
| MCP tool not found in session | Verify the server name is exactly `validate-plans-and-brainstorm-ideas` in `~/.claude.json` |
| JSON parse errors in `~/.claude.json` | Validate your JSON (check commas and braces) |
| Commands not appearing after install | Restart Claude Code and verify skill folders exist |

## License

MIT
