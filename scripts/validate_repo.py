#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
SKILLS_ROOT = ROOT / "skills"
JSON_PATHS = [
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r"^([a-zA-Z0-9_-]+):\s*(.+)$", re.MULTILINE)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"Missing required JSON file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON in {path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}"
        )


def discover_skills() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        raise SystemExit("Missing required skills/ directory")

    return [
        child
        for child in sorted(SKILLS_ROOT.iterdir())
        if child.is_dir() and (child / "SKILL.md").exists()
    ]


def parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise SystemExit(f"Missing YAML frontmatter in {skill_path.relative_to(ROOT)}")

    fields = {key: value.strip() for key, value in FIELD_RE.findall(match.group(1))}
    required_fields = {"name", "description"}
    missing = required_fields - fields.keys()
    if missing:
        missing_fields = ", ".join(sorted(missing))
        raise SystemExit(
            f"Missing frontmatter field(s) in {skill_path.relative_to(ROOT)}: {missing_fields}"
        )
    return fields


def validate_readme(skills: list[Path]) -> None:
    readme_text = README_PATH.read_text()
    for skill_dir in skills:
        snippet = f"[{skill_dir.name}](skills/{skill_dir.name}/)"
        if snippet not in readme_text:
            raise SystemExit(
                f"README.md is missing a discoverable link for skill '{skill_dir.name}'"
            )


def validate_plugin_skill_path(manifest: dict, manifest_name: str) -> None:
    skill_path = manifest.get("skills")
    if skill_path != "./skills/":
        raise SystemExit(
            f"{manifest_name} should point to ./skills/, found {skill_path!r}"
        )

    if not SKILLS_ROOT.is_dir():
        raise SystemExit(f"{manifest_name} points to ./skills/, but skills/ is missing")


def main() -> int:
    codex_plugin = load_json(JSON_PATHS[0])
    claude_plugin = load_json(JSON_PATHS[1])
    for path in JSON_PATHS[2:]:
        load_json(path)

    skills = discover_skills()
    if not skills:
        raise SystemExit("No skills were found under skills/")

    for skill_dir in skills:
        fields = parse_frontmatter(skill_dir / "SKILL.md")
        if fields["name"] != skill_dir.name:
            raise SystemExit(
                f"Frontmatter name mismatch in {skill_dir / 'SKILL.md'}: "
                f"expected '{skill_dir.name}', found '{fields['name']}'"
            )

    validate_plugin_skill_path(codex_plugin, ".codex-plugin/plugin.json")
    validate_plugin_skill_path(claude_plugin, ".claude-plugin/plugin.json")
    validate_readme(skills)

    print(
        f"Validated {len(JSON_PATHS)} JSON files, {len(skills)} skills, and README skill links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
