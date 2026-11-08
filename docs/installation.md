# Installation

## 배포본 선택

| 실행 주체 | 설치할 경로 | 독립 검토 상대 |
|---|---|---|
| Claude Code | `plugins/zipsa-commands/skills/` | 읽기 전용 Codex MCP |
| Codex | `codex/skills/` | 읽기 전용 Claude CLI |

두 배포본은 역할과 도구 호출이 다릅니다. 같은 실행 주체의 스킬 디렉터리에 두 배포본을 섞지 않습니다.
공통 참조 문서와 렌더러를 포함해야 하므로 `SKILL.md`만 복사하지 않고 9개 디렉터리를 통째로 설치합니다.

## 사전 요구사항

- Claude 실행: Claude Code와 인증된 Codex MCP 환경, MCP 실행에 필요한 Node.js/npm.
- Codex 실행: Codex와 인증된 Claude CLI. 독립 검토의 실패·대체 규칙은 해당 단계가 결정합니다.
- 두 배포본의 HTML 안내 생성: Python 3.11 이상, asdf, uv. 렌더러 자체는 Python 표준 라이브러리만 사용합니다.
- 이 저장소의 개발·검증 Python은 `.tool-versions`의 3.12.6입니다. 런타임은 asdf로 관리합니다.
- 대상 프로젝트가 지정한 실행 환경, 승인 절차와 테스트 명령이 우선합니다. 렌더링만을 위해 프로젝트 런타임 설정을 바꾸지 않습니다.

인증되지 않은 상대 모델을 호출한 경우 독립 검토가 완료됐다고 표시하지 않습니다.
Codex에서 Claude 계정 인증 403이 발생하면 별도 독립 Codex 세션으로 대체하는 공통 규칙을 따릅니다.

## Claude Code: Marketplace

기존 marketplace 이름 `zipsa-co-work`와 plugin 이름 `zipsa-commands`는 유지합니다.
등록할 GitHub 저장소 이름은 `mojokb/zipsa-co-command`입니다.

```text
/plugin marketplace add mojokb/zipsa-co-command
/plugin install zipsa-commands@zipsa-co-work
```

설치 후 사용 예:

```text
/zipsa-commands:zipsa-workflow 요구사항 또는 workflow.md 경로
```

### Codex MCP 등록

이미 등록했다면 기존 구성을 보존합니다. 새 구성이 필요한 경우:

```sh
claude mcp add validate-plans-and-brainstorm-ideas -- npx -y @openai/codex mcp-server
claude mcp list
```

해당 이름의 MCP 도구를 사용할 수 있고 Codex 인증이 되어 있어야 합니다.
프로젝트 지침은 읽기 전용 검토에도 적용됩니다.

## 직접 설치: Claude 또는 Codex

먼저 배포 저장소를 받습니다. 이미 clone했다면 기존 checkout의 변경사항을 확인하고 업데이트합니다.

```sh
git clone https://github.com/mojokb/zipsa-co-command.git
cd zipsa-co-command
```

릴리스에 고정하려면 게시된 릴리스 태그를 checkout한 뒤 설치합니다.
두 명령 묶음 중 사용할 실행 주체에 해당하는 것을 선택합니다.

### Claude

```sh
mkdir -p "$HOME/.claude/skills"
cp -R plugins/zipsa-commands/skills/zipsa-* "$HOME/.claude/skills/"
```

직접 설치한 스킬은 `/zipsa-workflow`처럼 호출합니다.
Marketplace와 직접 설치를 동시에 사용하면 이름이 겹칠 수 있으므로 활성 스킬의 실제 경로를 확인합니다.

### Codex

```sh
mkdir -p "$HOME/.agents/skills"
cp -R codex/skills/zipsa-* "$HOME/.agents/skills/"
```

`$zipsa-workflow`로 호출합니다. 이 경로를 별도 계정 디렉터리로 복제하는 실행 환경에서는
그 환경의 동기화 절차로 같은 버전을 반영합니다.

복사는 기존 zipsa 파일을 갱신합니다. 개인적으로 수정한 스킬은 먼저 보존합니다.
다른 이름의 스킬은 삭제하지 않습니다.

## 설치 확인

1. 9개 스킬 중 `zipsa-workflow`가 선택 목록에 있는지 확인합니다.
2. 설치된 `zipsa-workflow/references/work-policy.md`와 `scripts/render_html.py`가 존재하는지 확인합니다.
3. 스킬이 읽는 경로가 선택한 배포본인지 확인합니다. 프로젝트에 같은 이름의 스킬이 있으면 함께 확인합니다.
4. 상태만 알려달라는 요청으로 시작하여 작업 실행이나 소스 변경이 발생하지 않는지 확인합니다.
5. 독립 검토가 필요한 작업에서는 실제 상대 모델 호출 결과를 확인합니다. 파일 검증 성공은 인증·모델 실행 검증을 대신하지 않습니다.

## 업데이트

Marketplace 설치는 marketplace 목록을 갱신한 뒤 플러그인을 업데이트합니다.

```text
/plugin marketplace update zipsa-co-work
/plugin update zipsa-commands@zipsa-co-work
```

직접 설치는 업데이트한 checkout에서 해당 실행 주체의 복사 명령을 다시 실행합니다.
새 버전이 보이지 않으면 실행 도구를 재시작합니다. 이미 스킬을 읽은 세션에는 최신
`SKILL.md`와 필요한 참조 문서를 다시 읽도록 요청하고, 기존 승인·체크포인트·진행 상태는 유지합니다.

기존 schema-version-1 checkpoint에 `work_type`이 없어도 사용할 수 있습니다.
허용된 상태 정리 시 근거로 분류하며, 상태 조회만을 위해 checkpoint를 강제로 바꾸지 않습니다.

## 문제 해결

| 증상 | 확인할 내용 |
|---|---|
| 스킬이 안 보임 | 설치한 실행 주체·디렉터리·plugin 활성 상태와 이름 충돌 |
| 공통 문서를 찾지 못함 | 9개 디렉터리를 참조 문서·스크립트와 함께 복사했는지 |
| 독립 검토 실패 | 상대 도구 이름·설치·인증, 해당 단계의 대체 규칙 |
| HTML 생성 실패 | asdf의 Python 3.11 이상과 uv, 출력 경로 권한 |
| 이전 동작이 계속됨 | 세션이 최신 지침을 다시 읽었는지와 실행 환경의 사본 동기화 |

HTML 생성 실패로 이미 완료한 구현·테스트를 다시 실행하지 않습니다.
생성 실패를 기록하고 안내 문서만 복구하는 절차는 workflow와 HTML guide 계약을 따릅니다.
