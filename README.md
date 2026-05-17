# zipsa-co-work

4 collaboration commands for Claude Code that use the [Codex MCP server](https://github.com/openai/codex) to generate parallel plans, validate plans, brainstorm ideas, and review code.

## Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| `/zipsa-brainstorm` | Bounce ideas off Codex | Want fast alternative ideas, critiques, and perspectives |
| `/zipsa-plan` | Generate a parallel plan via Codex | Want a second opinion on your planning approach |
| `/zipsa-validate` | Get a staff engineer review of your plan | Want critical feedback before finalizing a plan |
| `/zipsa-review` | Senior engineer code review via Codex | Want a multi-axis review before merging |

## Installation

See [docs/installation.md](docs/installation.md) for the full installation guide.

## Command Details

### `/zipsa-brainstorm`

Starts an interactive brainstorming session with Codex. Pass your topic or question as the argument.

```
/zipsa-brainstorm how should we structure the authentication system
```

Supports follow-up conversation to dig deeper into ideas.

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

Returns critical issues, simplification opportunities, and alternative approaches. Supports back-and-forth discussion.

### `/zipsa-review`

Reviews code from a senior engineer's perspective. Pass a file path, directory, or leave empty to review the current git diff.

```
/zipsa-review src/api/users.py
/zipsa-review src/handlers/
/zipsa-review                   # reviews current git diff
```

Evaluates code across four axes:

| Axis | What it checks |
|------|----------------|
| SOLID Principles | SRP, OCP, LSP, ISP, DIP violations |
| Clean Code | Naming, function length, duplication, magic values, dead code |
| Lint / Style | Language idioms, error handling, type annotations, import hygiene |
| Optimization | Algorithmic complexity, allocations, IO batching, resource leaks |

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
# zipsa-co-command
