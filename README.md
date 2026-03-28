[![Validate](https://github.com/gokhanamal/ai-context/actions/workflows/validate.yml/badge.svg)](https://github.com/gokhanamal/ai-context/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# AI Context

Reusable AI context for coding agents.

This repository started as a skills collection and now serves as a broader home for reusable agent context: skills today, with room for custom agents, workflows, references, and supporting documentation as the project grows.

## Why This Repo Exists

- Cross-platform packaging for Claude Code and Codex
- Reusable skills for common coding workflows
- A shared home for custom agents and other AI context assets
- Human-readable Markdown files that stay easy to audit and extend

## Current Contents

### Skills

| Skill | What it helps with |
|-------|---------------------|
| [github-actions](skills/github-actions/) | Create, review, debug, and harden GitHub Actions workflows and custom actions |
| [capture](skills/capture/) | Decide whether reusable knowledge belongs in a skill, lesson, solution doc, or nowhere at all |

### Agents

The repository now reserves [agents/](agents/) for reusable custom agent definitions and related documentation as that part of the project expands.

## Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| Claude Code | Yes | Includes `.claude-plugin/` manifest and marketplace catalog |
| OpenAI Codex | Yes | Includes `.codex-plugin/` manifest |
| Manual install | Yes | Copy any skill directory directly into your agent's skills directory |

## Quick Start

### Claude Code

Install directly from GitHub:

```bash
claude plugin install --source github gokhanamal/ai-context
```

Add this repository as a marketplace:

```text
/plugin marketplace add gokhanamal/ai-context
/plugin install gokhanamal-ai-context@gokhanamal-context
```

Test the marketplace locally from the repo root:

```text
/plugin marketplace add .
/plugin install gokhanamal-ai-context@gokhanamal-context
```

Load the plugin directory directly from the repo root:

```bash
claude --plugin-dir .
```

### OpenAI Codex

Pick the workflow that fits how you like to install context from this repository:

1. Copy one or more directories from `skills/` into `$HOME/.agents/skills/`.
2. Or use this repository as a local plugin through `.codex-plugin/plugin.json`.

### Manual Install

Copy any skill directory from `skills/`, such as `skills/github-actions/` or `skills/capture/`, into your agent's skills folder.

## Adding A New Skill

1. Copy `_template/` to `skills/my-new-skill/`.
2. Update `SKILL.md` frontmatter with the final `name` and `description`.
3. Add `references/` or `agents/` content only when it genuinely helps the skill.
4. Add the new skill to the table in this README.
5. Keep repo skills under `skills/` so both plugin manifests discover them consistently.
6. Run the repository validation script before opening a pull request:

```bash
python3 scripts/validate_repo.py
```

## Repository Layout

```text
repo-root/
├── .claude-plugin/         # Claude Code plugin manifest and marketplace catalog
├── .codex-plugin/          # Codex plugin manifest
├── .github/                # Issue templates, PR template, and CI validation
├── _template/              # Starter template for new skills
├── agents/                 # Reusable custom agent definitions and docs
├── skills/                 # Reusable skills used by both plugin manifests
│   └── <skill-name>/
│       ├── README.md
│       ├── SKILL.md
│       ├── agents/         # Optional skill-specific helpers
│       └── references/     # Optional supporting docs
├── scripts/                # Local validation helpers
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── README.md
└── LICENSE
```

## Contributing

Contributions are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow, authoring checklist, and validation steps. By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

Please review [SECURITY.md](SECURITY.md) before reporting a vulnerability publicly.

## License

[MIT](LICENSE)
