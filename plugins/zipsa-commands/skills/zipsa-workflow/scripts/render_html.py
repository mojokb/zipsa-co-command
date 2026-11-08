"""Render an offline feature guide from validated stage explanations."""

from __future__ import annotations

import argparse
import json
import logging
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from urllib.parse import quote, urlsplit

LOGGER = logging.getLogger(__name__)

STAGES = {
    "workflow": "진행 관리",
    "grill": "요구사항 정리",
    "think": "대안 검토",
    "plan": "구현 계획",
    "validate": "계획 검증",
    "tasks": "작업 나누기",
    "build": "구현",
    "test": "테스트",
    "review": "코드 리뷰",
}
STATUSES = {
    "pending": "아직 시작하지 않음",
    "running": "진행 중",
    "waiting_approval": "사용자 답변·승인 필요",
    "blocked": "진행 차단",
    "failed": "문제 발견",
    "completed": "해당 단계 완료",
    "skipped": "사유를 기록하고 생략",
    "stale": "다시 확인 필요",
    "inconclusive": "판단 근거 부족",
}
CSS = """
:root{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#172b4d;background:#f3f6fa;line-height:1.65}
*{box-sizing:border-box}body{margin:0}main{max-width:1040px;margin:auto;padding:32px 22px 64px}
a{color:#1559b7;overflow-wrap:anywhere}h1{font-size:2rem;line-height:1.3;margin:8px 0 16px}h2{font-size:1.25rem;margin:0 0 12px}h3{font-size:1rem;margin:16px 0 6px}
.meta{font-size:.85rem;color:#52657e}.card{background:white;border:1px solid #dbe3ee;border-radius:14px;padding:24px;margin:18px 0;overflow-wrap:anywhere}
.status{display:inline-block;border-radius:7px;background:#e7edf5;color:#263b55;padding:4px 10px;font-size:.9rem;font-weight:650}
.status-completed{background:#dff2e7;color:#135333}.status-failed,.status-blocked{background:#fde7e7;color:#832329}
.status-waiting_approval,.status-stale,.status-inconclusive{background:#fff0cb;color:#71500c}
.next{border-left:5px solid #2563a5}.attention{border-left:5px solid #bb7b00}.label{font-size:.8rem;letter-spacing:.04em;color:#52657e}
nav ul{display:flex;flex-wrap:wrap;gap:8px 20px;padding-left:20px}p{margin:10px 0}li{margin:5px 0}details{border-top:1px solid #e1e7ef;margin-top:18px;padding-top:12px}summary{cursor:pointer;font-weight:600}
footer{font-size:.85rem;color:#52657e;margin-top:28px}@media(max-width:600px){main{padding:20px 14px}.card{padding:18px}h1{font-size:1.55rem}}
@media print{body{background:white}main{max-width:none}.card{break-inside:avoid}details{display:block}nav{display:none}}
"""


@dataclass(frozen=True)
class Evidence:
    """A readable label and a checked original-source link."""

    label: str
    href: str


@dataclass(frozen=True)
class Section:
    """One stage step's explanation, observed status and supporting evidence."""

    stage: str
    step: str
    title: str
    status: str
    explanation: str
    items: tuple[str, ...]
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class Guide:
    """Derived presentation data; this does not grant approval or execution authority."""

    feature_id: str
    title: str
    current_stage: str
    status: str
    summary: str
    next_action: str
    needs_input: tuple[str, ...]
    limits: tuple[str, ...]
    sections: tuple[Section, ...]


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(k, str) for k in value):
        raise ValueError("Expected a JSON object with string keys")
    return value


def _text(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected nonempty text")
    return value


def _list(value: object) -> list[object]:
    if not isinstance(value, list):
        raise TypeError("Expected a JSON list")
    return value


def _choice(value: object, choices: dict[str, str]) -> str:
    text = _text(value)
    if text not in choices:
        raise ValueError(f"Unknown stage or status: {text}")
    return text


def _href(value: object) -> str:
    text = _text(value)
    parts = urlsplit(text)
    if parts.scheme not in ("", "http", "https") or text.startswith("//"):
        raise ValueError("Evidence links must be local paths or HTTP(S)")
    if parts.username or parts.password or any(ord(c) < 32 for c in text):
        raise ValueError(
            "Evidence links cannot contain credentials or control characters"
        )
    if parts.scheme and not parts.netloc:
        raise ValueError("HTTP(S) evidence links need a host")
    if parts.scheme:
        return quote(text, safe="/:#?&=%@+~,;")
    if text.startswith("#"):
        return "#" + quote(text[1:], safe="")
    return quote(text, safe="/")


def _section(value: object) -> Section:
    row = _mapping(value)
    evidence = []
    for item in _list(row.get("evidence", [])):
        link = _mapping(item)
        href = _text(link.get("href"))
        _href(href)
        evidence.append(Evidence(_text(link.get("label")), href))
    return Section(
        _choice(row.get("stage"), STAGES),
        _text(row.get("step")),
        _text(row.get("title")),
        _choice(row.get("status"), STATUSES),
        _text(row.get("explanation")),
        tuple(_text(v) for v in _list(row.get("items", []))),
        tuple(evidence),
    )


def load_guide(path: Path) -> Guide:
    """Load validated presentation input.

    Args:
        path: UTF-8 JSON file containing the derived feature explanation.

    Returns:
        A guide with checked stage/status values and evidence links.

    Raises:
        OSError: The input cannot be read.
        ValueError: JSON, required fields, statuses, or links are invalid.
        TypeError: A JSON list field has the wrong type.
    """
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    row = _mapping(raw)
    sections = tuple(_section(v) for v in _list(row.get("sections")))
    if not sections or len({(s.stage, s.step) for s in sections}) != len(sections):
        raise ValueError("Provide at least one step and unique (stage, step) keys")
    stage = _choice(row.get("current_stage"), STAGES)
    status = _choice(row.get("status"), STATUSES)
    if not any(s.stage == stage and s.status == status for s in sections):
        raise ValueError("Current stage/status must match an actual step section")
    return Guide(
        _text(row.get("feature_id")),
        _text(row.get("title")),
        stage,
        status,
        _text(row.get("summary")),
        _text(row.get("next_action")),
        tuple(_text(v) for v in _list(row.get("needs_input", []))),
        tuple(_text(v) for v in _list(row.get("limits", []))),
        sections,
    )


def _bullets(items: tuple[str, ...]) -> str:
    return "<ul>" + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def _badge(status: str) -> str:
    return f'<span class="status status-{status}">{escape(STATUSES[status])}</span>'


def _render_section(section: Section, index: int) -> str:
    links = "".join(
        f'<li><a href="{escape(_href(e.href), quote=True)}">{escape(e.label)}</a></li>'
        for e in section.evidence
    )
    sources = (
        f"<details><summary>원본 근거 확인</summary><ul>{links}</ul></details>"
        if links
        else ""
    )
    return f"""<section class="card" id="step-{index}">
<div class="label">{escape(STAGES[section.stage])} · {escape(section.step)}</div>
<h2>{escape(section.title)}</h2>{_badge(section.status)}
<p>{escape(section.explanation)}</p>{_bullets(section.items)}{sources}</section>"""


def _panel(title: str, items: tuple[str, ...], css: str) -> str:
    if not items:
        return ""
    return f'<aside class="card {escape(css)}"><h2>{escape(title)}</h2>{_bullets(items)}</aside>'


def render_guide(guide: Guide) -> str:
    """Render an offline guide with escaped caller text.

    Args:
        guide: Validated explanation data; each section describes one stage step.

    Returns:
        A UTF-8-compatible HTML string with no script or external asset imports.

    Raises:
        ValueError: A supplied evidence URL is unsafe.
    """
    nav = "".join(
        f'<li><a href="#step-{i}">{escape(s.title)}</a></li>'
        for i, s in enumerate(guide.sections, 1)
    )
    sections = "".join(_render_section(s, i) for i, s in enumerate(guide.sections, 1))
    attention = _panel("내 확인이 필요한 내용", guide.needs_input, "attention")
    limits = _panel("아직 확인하지 못한 범위", guide.limits, "")
    updated = datetime.now(UTC).isoformat(timespec="seconds")
    return (
        f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(guide.title)}</title><style>{CSS}</style></head><body><main>"
        f'<header><div class="meta">{escape(guide.feature_id)} · 생성 {updated}</div>'
        f"<h1>{escape(guide.title)}</h1><div>현재 단계: {escape(STAGES[guide.current_stage])} "
        f"{_badge(guide.status)}</div><p>{escape(guide.summary)}</p></header>"
        f'{attention}<aside class="card next"><h2>다음 행동</h2>'
        f'<p>{escape(guide.next_action)}</p></aside><nav aria-label="단계별 설명">'
        f"<ul>{nav}</ul></nav>{sections}{limits}<footer>"
        "이 문서는 원본 산출물과 실행 근거를 쉽게 설명하는 보기입니다. "
        "표시된 완료는 해당 단계의 상태이며, 피처 전체 완료나 수정 승인을 뜻하지 않습니다."
        "</footer></main></body></html>"
    )


def write_guide(guide: Guide, output: Path) -> None:
    """Replace an HTML output in an existing authorized directory.

    Args:
        guide: Validated explanation data to render.
        output: Local output path whose parent directory already exists.

    Raises:
        OSError: The temporary or output file cannot be written.
        ValueError: Output is a symlink or an evidence URL is unsafe.
    """
    if output.is_symlink():
        raise ValueError("Verify the real output path before writing through a symlink")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=output.parent, suffix=".html", delete=False
        ) as handle:
            temporary = Path(handle.name)
            handle.write(render_guide(guide))
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    """Run the command-line renderer.

    Returns:
        Zero on success, or one after logging a validation or filesystem error.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        write_guide(load_guide(args.input), args.output)
    except (OSError, TypeError, ValueError) as error:
        LOGGER.error("guide_render_failed: %s", error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
