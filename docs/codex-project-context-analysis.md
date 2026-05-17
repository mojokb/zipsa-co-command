# Codex MCP 프로젝트 Context 활용 분석

## 현재 구조 요약

세 스킬(`zipsa-brainstorm`, `zipsa-plan`, `zipsa-validate`) 모두 동일한 패턴을 따름:

1. 백그라운드 서브에이전트가 `mcp__validate-plans-and-brainstorm-ideas__codex` 호출
2. Claude가 독립적으로 자체 작업 수행 (bias 방지)
3. 두 결과를 비교하여 통합

---

## 특정 프로젝트 Context 기반 동작 가능성

**결론: 가능하다. 단, 현재 구현에 한계가 있음.**

### 가능한 이유

현재 `codex` 도구 호출 시 `cwd` 파라미터를 지정하도록 설계되어 있음:

```
- `cwd`: (use the current working directory)
```

Codex CLI는 지정된 `cwd`에서 파일을 읽을 수 있는 **코딩 에이전트**다. `sandbox: read-only`로 실행되므로 해당 디렉토리의 코드를 탐색하고 이해할 수 있다.

즉, **zipsa-* 스킬을 특정 프로젝트 디렉토리에서 실행하면** Codex는 그 프로젝트의 파일들을 읽고 context로 활용할 수 있다.

---

## 현재 구현의 한계

| 문제 | 내용 |
|---|---|
| **Codex에게 코드 탐색 지시가 없음** | 현재 프롬프트는 Codex에게 "코드베이스를 먼저 파악하라"는 지시가 없어, Codex가 파일을 능동적으로 읽지 않을 수 있음 |
| **cwd가 암묵적** | `(use the current working directory)`는 Claude가 판단하는 것이라 실제 프로젝트 경로가 아닌 잘못된 경로가 넘어갈 수 있음 |
| **context 깊이 불확실** | Codex가 얼마나 깊이 코드베이스를 탐색할지는 Codex 자체 동작에 달려 있음 |

---

## 개선 방향

### 1. Codex 프롬프트에 코드 탐색 지시 추가

각 스킬의 Codex 프롬프트 앞부분에 아래 내용을 추가하면 Codex가 프로젝트 context를 적극 활용하게 만들 수 있음:

```
First, explore the codebase in your working directory to understand the project
structure, key files, and existing patterns. Then proceed with your task.
```

### 2. 명시적 프로젝트 경로 지정

특정 프로젝트를 대상으로 실행할 때 `$ARGUMENTS`로 프로젝트 경로를 받아 `cwd`에 명시적으로 전달하는 방식으로 확장 가능:

```
/zipsa-brainstorm --cwd /path/to/project <topic>
```

---

## 요약

| 항목 | 현재 상태 |
|---|---|
| 프로젝트 파일 접근 | 가능 (`cwd` 파라미터로 전달됨) |
| Codex의 능동적 코드 탐색 | 불확실 (프롬프트에 명시적 지시 없음) |
| 특정 프로젝트 명시 지정 | 불가 (현재는 항상 current working directory) |
| 개선 난이도 | 낮음 (SKILL.md 프롬프트 수정만으로 가능) |

- **현재도 동작 가능**: 스킬을 해당 프로젝트 디렉토리에서 실행하면 Codex는 `cwd`를 통해 프로젝트 파일에 접근 가능
- **단, Codex가 context를 능동적으로 읽도록 프롬프트에 명시적 지시가 없어** 실제로는 주어진 텍스트만으로 판단할 가능성이 높음
- **프롬프트에 "코드베이스를 먼저 탐색하라"는 지시를 추가**하면 특정 프로젝트 context 기반으로 훨씬 더 정확한 결과를 얻을 수 있음
