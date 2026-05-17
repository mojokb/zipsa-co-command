# Installation Guide

## Overview

zipsa-co-work은 두 가지 구성 요소를 설치해야 동작합니다.

```
[스킬 설치]  → Claude Code가 /zipsa-* 커맨드를 인식
[MCP 서버]   → 커맨드 실행 시 Codex와 통신
```

두 단계 모두 완료해야 합니다.

---

## 1단계: 스킬 설치

세 가지 방법 중 하나를 선택합니다.

### 방법 A: Plugin Marketplace (권장)

Claude Code 세션 안에서 실행합니다.

```
/plugin marketplace add mojokb/zipsa-co-work
/plugin install zipsa-commands@zipsa-co-work
```

### 방법 B: Git Clone

```bash
git clone https://github.com/mojokb/zipsa-co-work.git
cp -r zipsa-co-work/plugins/zipsa-commands/skills/* ~/.claude/skills/
```

### 방법 C: 수동 복사

이 저장소의 `plugins/zipsa-commands/skills/` 폴더 안의 내용을 `~/.claude/skills/` 로 복사합니다.

```
~/.claude/skills/
  zipsa-think/SKILL.md
  zipsa-plan/SKILL.md
  zipsa-validate/SKILL.md
  zipsa-tasks/SKILL.md
  zipsa-review/SKILL.md
```

---

## 2단계: MCP 서버 등록

스킬 설치 방법과 무관하게 반드시 완료해야 합니다.

### 방법 A: CLI (권장)

```bash
claude mcp add validate-plans-and-brainstorm-ideas -- npx -y @openai/codex mcp-server
```

### 방법 B: ~/.claude.json 직접 편집

`~/.claude.json`의 `mcpServers` 항목에 아래 내용을 추가합니다.

```json
"validate-plans-and-brainstorm-ideas": {
  "command": "npx",
  "args": ["-y", "@openai/codex", "mcp-server"]
}
```

기존 `mcpServers` 항목이 있다면 덮어쓰지 않고 키를 추가합니다.

```json
{
  "mcpServers": {
    "기존-서버": { ... },
    "validate-plans-and-brainstorm-ideas": {
      "command": "npx",
      "args": ["-y", "@openai/codex", "mcp-server"]
    }
  }
}
```

---

## 3단계: 동작 확인

1. Claude Code를 재시작합니다 (`~/.claude.json`을 직접 편집한 경우).
2. MCP 서버 등록 확인:
   ```bash
   claude mcp list
   ```
   `validate-plans-and-brainstorm-ideas` 가 목록에 있어야 합니다.
3. 스킬 동작 확인:
   ```
   /zipsa-think hello
   ```
   Codex MCP 호출이 트리거되면 정상입니다.

---

## 사전 요구 사항

| 항목 | 비고 |
|------|------|
| [Node.js](https://nodejs.org/) | `npx` 실행에 필요 |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | CLI 또는 IDE 확장 |

---

## 문제 해결

| 증상 | 원인 및 해결 |
|------|-------------|
| `npx: command not found` | Node.js 미설치 → [nodejs.org](https://nodejs.org/) 에서 설치 |
| `/zipsa-*` 커맨드가 보이지 않음 | 스킬 파일이 `~/.claude/skills/` 에 없음 → 1단계 재확인 후 Claude Code 재시작 |
| MCP 도구를 찾을 수 없음 | 서버 이름이 정확히 `validate-plans-and-brainstorm-ideas` 인지 확인 |
| `~/.claude.json` 파싱 오류 | JSON 문법 오류(쉼표, 중괄호) → JSON validator로 검사 |
| Codex가 응답하지 않음 | `claude mcp list` 로 서버 상태 확인, 필요 시 MCP 서버 재등록 |
