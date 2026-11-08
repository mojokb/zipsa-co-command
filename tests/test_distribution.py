"""Exercise clean installs, bundled resources and offline rendering for both hosts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
HOST_SOURCES = {
    "claude": REPOSITORY / "plugins/zipsa-commands/skills",
    "codex": REPOSITORY / "codex/skills",
}
SKILL_NAMES = {
    "zipsa-workflow",
    "zipsa-grill",
    "zipsa-think",
    "zipsa-plan",
    "zipsa-validate",
    "zipsa-tasks",
    "zipsa-build",
    "zipsa-test",
    "zipsa-review",
}
EVIDENCE_FILENAME = "source note.md"
BLOCKED_GUIDE = {
    "feature_id": "R1",
    "title": "Installed workflow",
    "current_stage": "test",
    "status": "blocked",
    "summary": "The required environment is unavailable.",
    "next_action": "Restore the designated test environment.",
    "limits": ["Integration behavior is unverified."],
    "sections": [
        {
            "stage": "test",
            "step": "prerequisites",
            "title": "Blocked check",
            "status": "blocked",
            "explanation": "No integration pass is claimed.",
            "evidence": [{"label": "Original observation", "href": EVIDENCE_FILENAME}],
        }
    ],
}


class DistributionTests(unittest.TestCase):
    """Check the files that installed workflows and plugin discovery actually consume."""

    def test_marketplace_resolves_versioned_plugin(self) -> None:
        marketplace = json.loads(
            (REPOSITORY / ".claude-plugin/marketplace.json").read_text()
        )
        entry = marketplace["plugins"][0]
        plugin_root = REPOSITORY / entry["source"]
        manifest = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(entry["name"], manifest["name"])
        self.assertEqual(marketplace["metadata"]["version"], entry["version"])
        self.assertEqual(entry["version"], manifest["version"])
        for filename in ("pyproject.toml", "uv.lock"):
            data = tomllib.loads((REPOSITORY / filename).read_text())
            version = (
                data["project"]["version"]
                if filename.endswith("toml")
                else data["package"][0]["version"]
            )
            self.assertEqual(version, manifest["version"])
        self.assertEqual(
            {p.name for p in (plugin_root / "skills").iterdir() if p.is_dir()},
            SKILL_NAMES,
        )

    def test_clean_copies_keep_resources_and_existing_unrelated_skills(self) -> None:
        for host, source in HOST_SOURCES.items():
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                installed = Path(directory) / ".skills"
                installed.mkdir()
                sentinel = installed / "unrelated-skill"
                sentinel.mkdir()
                (sentinel / "SKILL.md").write_text("preserved", encoding="utf-8")
                subprocess.run(
                    [
                        "cp",
                        "-R",
                        *map(str, sorted(source.glob("zipsa-*"))),
                        str(installed),
                    ],
                    check=True,
                )
                self.assertEqual((sentinel / "SKILL.md").read_text(), "preserved")
                self._check_installed_references(installed)
                self._check_installed_renderer(installed)

    def _check_installed_references(self, installed: Path) -> None:
        actual = {p.name for p in installed.glob("zipsa-*") if p.is_dir()}
        self.assertEqual(actual, SKILL_NAMES)
        for folder in installed.glob("zipsa-*"):
            skill = folder / "SKILL.md"
            header = skill.read_text().split("---", 2)[1]
            match = re.search(r"^name:\s*(\S+)\s*$", header, re.MULTILINE)
            self.assertIsNotNone(match, str(skill))
            assert match is not None
            self.assertEqual(match.group(1), folder.name)
            for document in [skill, *folder.glob("references/*.md")]:
                for href in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                    if "://" in href or href.startswith("#"):
                        continue
                    target = (document.parent / href.split("#", 1)[0]).resolve()
                    self.assertTrue(
                        target.is_relative_to(installed.resolve()), str(target)
                    )
                    self.assertTrue(target.is_file(), f"{document}: {href}")

    def _check_installed_renderer(self, installed: Path) -> None:
        renderer = installed / "zipsa-workflow/scripts/render_html.py"
        self.assertTrue(renderer.is_file())
        self.assertTrue((renderer.parents[1] / "tests/test_render_html.py").is_file())
        evidence = installed / EVIDENCE_FILENAME
        evidence.write_text("Required integration environment is unavailable.")
        source = installed / "guide.json"
        source.write_text(json.dumps(BLOCKED_GUIDE))
        output = installed / "guide.html"
        result = subprocess.run(
            [sys.executable, str(renderer), str(source), str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        page = output.read_text()
        self.assertIn("Integration behavior is unverified.", page)
        self.assertIn('href="source%20note.md"', page)
        self.assertNotIn("<script", page)


if __name__ == "__main__":
    unittest.main()
