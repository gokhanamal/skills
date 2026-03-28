#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"
SKILLS_ROOT = ROOT / "skills"
AGENTS_ROOT = ROOT / "agents"
JSON_PATHS = [
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
]
REQUIRED_ROOT_DOCS = [
    ROOT / "README.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
]
REQUIRED_TEMPLATE_FILES = [
    ROOT / "_template" / "SKILL.md",
    ROOT / "_template" / "README.md",
]
CONSISTENT_PLUGIN_FIELDS = [
    "name",
    "version",
    "description",
    "homepage",
    "repository",
    "license",
    "skills",
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


def discover_agents() -> list[Path]:
    if not AGENTS_ROOT.is_dir():
        raise SystemExit("Missing required agents/ directory")

    return [
        child
        for child in sorted(AGENTS_ROOT.iterdir())
        if child.is_dir() and not child.name.startswith(".")
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


def validate_required_files(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"Missing required file: {path.relative_to(ROOT)}")


def validate_skill_docs(skills: list[Path]) -> None:
    for skill_dir in skills:
        readme_path = skill_dir / "README.md"
        if not readme_path.is_file():
            raise SystemExit(
                f"Skill '{skill_dir.name}' is missing README.md at "
                f"{readme_path.relative_to(ROOT)}"
            )


def validate_agent_docs(agent_dirs: list[Path]) -> None:
    for agent_dir in agent_dirs:
        readme_path = agent_dir / "README.md"
        if not readme_path.is_file():
            raise SystemExit(
                f"Agent directory '{agent_dir.name}' is missing README.md at "
                f"{readme_path.relative_to(ROOT)}"
            )


def validate_plugin_skill_path(manifest: dict, manifest_name: str) -> None:
    skill_path = manifest.get("skills")
    if skill_path != "./skills/":
        raise SystemExit(
            f"{manifest_name} should point to ./skills/, found {skill_path!r}"
        )

    if not SKILLS_ROOT.is_dir():
        raise SystemExit(f"{manifest_name} points to ./skills/, but skills/ is missing")


def validate_manifest_consistency(codex_plugin: dict, claude_plugin: dict) -> None:
    for field in CONSISTENT_PLUGIN_FIELDS:
        if codex_plugin.get(field) != claude_plugin.get(field):
            raise SystemExit(
                f"Plugin manifest mismatch for '{field}': "
                f".codex-plugin/plugin.json has {codex_plugin.get(field)!r}, "
                f".claude-plugin/plugin.json has {claude_plugin.get(field)!r}"
            )

    if codex_plugin.get("author") != claude_plugin.get("author"):
        raise SystemExit("Plugin manifest mismatch for 'author' between Codex and Claude manifests")


def validate_marketplace(claude_plugin: dict, marketplace: dict) -> None:
    metadata = marketplace.get("metadata", {})
    if metadata.get("version") != claude_plugin.get("version"):
        raise SystemExit(
            ".claude-plugin/marketplace.json metadata.version must match "
            ".claude-plugin/plugin.json version"
        )

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        raise SystemExit(".claude-plugin/marketplace.json must include at least one plugin entry")

    root_plugin = next((plugin for plugin in plugins if plugin.get("source") == "./"), None)
    if root_plugin is None:
        raise SystemExit(
            ".claude-plugin/marketplace.json must include a root plugin entry with source './'"
        )

    for field in ("name", "homepage", "repository", "license"):
        if root_plugin.get(field) != claude_plugin.get(field):
            raise SystemExit(
                f"Marketplace root plugin field '{field}' must match .claude-plugin/plugin.json"
            )


def main() -> int:
    validate_required_files(REQUIRED_ROOT_DOCS + REQUIRED_TEMPLATE_FILES)

    codex_plugin = load_json(JSON_PATHS[0])
    claude_plugin = load_json(JSON_PATHS[1])
    marketplace = load_json(JSON_PATHS[2])

    skills = discover_skills()
    agents = discover_agents()
    if not skills:
        raise SystemExit("No skills were found under skills/")

    for skill_dir in skills:
        fields = parse_frontmatter(skill_dir / "SKILL.md")
        if fields["name"] != skill_dir.name:
            raise SystemExit(
                f"Frontmatter name mismatch in {skill_dir / 'SKILL.md'}: "
                f"expected '{skill_dir.name}', found '{fields['name']}'"
            )

    validate_skill_docs(skills)
    validate_agent_docs(agents)
    validate_plugin_skill_path(codex_plugin, ".codex-plugin/plugin.json")
    validate_plugin_skill_path(claude_plugin, ".claude-plugin/plugin.json")
    validate_manifest_consistency(codex_plugin, claude_plugin)
    validate_marketplace(claude_plugin, marketplace)
    validate_readme(skills)

    print(
        f"Validated {len(JSON_PATHS)} JSON files, {len(skills)} skills, "
        f"{len(agents)} agent directories, and README/documentation rules."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
