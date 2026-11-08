"""Exercise real rendering, input rejection, and output preservation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import render_html as renderer


class PageParser(HTMLParser):
    """Collect elements and text without trusting generated markup."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.text: list[str] = []
        self.attributes: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        self.attributes.extend(attrs)

    def handle_data(self, data: str) -> None:
        self.text.append(data)


def _sample() -> dict[str, object]:
    return {
        "feature_id": "COUNT-1",
        "title": "검증 안내",
        "current_stage": "test",
        "status": "blocked",
        "summary": "환경이 없어 아직 검증하지 못했습니다.",
        "next_action": "환경 복구 후 검사를 실행합니다.",
        "needs_input": [],
        "limits": ["통합 검사 미실행"],
        "sections": [
            {
                "stage": "test",
                "step": "환경 확인",
                "title": "준비 상태",
                "status": "blocked",
                "explanation": "환경부터 확인했습니다.",
                "items": [],
                "evidence": [{"label": "원본", "href": "source note.md"}],
            }
        ],
    }


class GuideTests(unittest.TestCase):
    """Validate user-visible content and safety at the rendering boundary."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "guide.json"
        self.output = self.directory / "guide.html"

    def _load(self, raw: dict[str, object] | None = None) -> renderer.Guide:
        self.source.write_text(
            json.dumps(_sample() if raw is None else raw), encoding="utf-8"
        )
        return renderer.load_guide(self.source)

    def test_blocked_status_remains_visible(self) -> None:
        renderer.write_guide(self._load(), self.output)
        page = PageParser()
        page.feed(self.output.read_text(encoding="utf-8"))
        text = "".join(page.text)
        self.assertIn("진행 차단", text)
        self.assertIn("통합 검사 미실행", text)
        self.assertIn("환경 복구 후 검사를 실행합니다.", text)
        self.assertIn("피처 전체 완료나 수정 승인을 뜻하지 않습니다", text)
        self.assertNotIn("script", page.tags)
        self.assertFalse(
            any(name in ("src", "onload", "onclick") for name, _ in page.attributes)
        )
        self.assertIn('href="source%20note.md"', self.output.read_text())

    def test_supplied_markup_is_text(self) -> None:
        raw = _sample()
        raw["summary"] = '<script>alert("x")</script><img src=x onerror=alert(1)>'
        rendered = renderer.render_guide(self._load(raw))
        page = PageParser()
        page.feed(rendered)
        self.assertIn(raw["summary"], "".join(page.text))
        self.assertNotIn("script", page.tags)
        self.assertNotIn("img", page.tags)

    def test_unsafe_links_are_rejected(self) -> None:
        for href in (
            "javascript:alert(1)",
            "data:text/html,evil",
            "//example.com/a",
            "https://user:secret@example.com/a",
            "https://example.com/\nnext",
        ):
            with self.subTest(href=href), self.assertRaises(ValueError):
                renderer._href(href)

    def test_local_special_characters_are_filename_text(self) -> None:
        self.assertEqual(
            renderer._href("evidence #1?100%.md"), "evidence%20%231%3F100%25.md"
        )
        self.assertEqual(renderer._href("./#notes.md"), "./%23notes.md")
        self.assertEqual(renderer._href("#step-1"), "#step-1")
        self.assertEqual(
            renderer._href("https://example.com/a?q=1#part"),
            "https://example.com/a?q=1#part",
        )

    def test_direct_render_also_rejects_unsafe_evidence(self) -> None:
        section = renderer.Section(
            "test",
            "one",
            "제목",
            "blocked",
            "설명",
            (),
            (renderer.Evidence("source", "javascript:alert(1)"),),
        )
        guide = renderer.Guide(
            "x", "title", "test", "blocked", "summary", "next", (), (), (section,)
        )
        with self.assertRaises(ValueError):
            renderer.render_guide(guide)

    def test_inconsistent_status_is_rejected(self) -> None:
        for status in ("passed-everything", "completed"):
            raw = _sample()
            raw["status"] = status
            with self.subTest(status=status), self.assertRaises(ValueError):
                self._load(raw)

    def test_other_step_sections_are_retained(self) -> None:
        raw = _sample()
        sections = raw["sections"]
        assert isinstance(sections, list)
        sections.append(
            {
                "stage": "plan",
                "step": "review",
                "title": "이전 계획",
                "status": "stale",
                "explanation": "요구사항이 바뀌어 재확인이 필요합니다.",
            }
        )
        rendered = renderer.render_guide(self._load(raw))
        self.assertIn("이전 계획", rendered)
        self.assertIn("다시 확인 필요", rendered)
        sections.append(sections[0])
        with self.assertRaises(ValueError):
            self._load(raw)

    def test_cli_validation_failure_preserves_existing_page(self) -> None:
        self.source.write_text("{}", encoding="utf-8")
        self.output.write_text("existing page", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, renderer.__file__, str(self.source), str(self.output)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.output.read_text(), "existing page")
        self.assertIn("guide_render_failed", result.stderr)

    def test_symlink_requires_verified_real_path(self) -> None:
        real = self.directory / "real.html"
        real.write_text("preserved")
        self.output.symlink_to(real)
        with self.assertRaises(ValueError):
            renderer.write_guide(self._load(), self.output)
        self.assertEqual(real.read_text(), "preserved")


if __name__ == "__main__":
    unittest.main()
