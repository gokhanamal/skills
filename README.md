[![Validate](https://github.com/gokhanamal/ai-context/actions/workflows/validate.yml/badge.svg)](https://github.com/gokhanamal/ai-context/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# AI Context

Reusable AI context and installable skills for coding agents.

This repository started as a skills collection and now serves as a broader home for reusable agent context: skills today, with room for custom agents, workflows, references, and supporting documentation as the project grows.

## Why This Repo Exists

- Broad skill distribution via [skills.sh](https://skills.sh/) and the `skills` CLI
- First-class packaging for Claude Code and OpenAI Codex
- Reusable skills for common coding workflows
- A shared home for custom agents and other AI context assets
- Human-readable Markdown files that stay easy to audit and extend

## Current Contents

### Skills

| Skill | What it helps with |
|-------|---------------------|
| [github-actions](skills/github-actions/) | Create, review, debug, and harden GitHub Actions workflows and custom actions |
| [capture](skills/capture/) | Decide whether reusable knowledge belongs in a skill, lesson, solution doc, or nowhere at all |
| [ios-simulator](skills/ios-simulator/) | Manually drive an iOS Simulator: discover the app, launch it, inspect screens, interact with UI, and capture screenshots or logs |

`ios-simulator` is intentionally a manual skill because it can open apps and perform real UI actions inside the simulator.

### Agents

[agents/](agents/) is the home for reusable custom agents and related documentation. Each concrete agent should live in its own `agents/<agent-name>/` directory with a human-facing `README.md`.

## Repository Guidance

- [AGENTS.md](AGENTS.md) defines the repository rules for skills, agents, packaging, and validation.
- [CLAUDE.md](CLAUDE.md) forwards Claude-compatible tooling to the same guidance so repo instructions stay in one place.
- [CONTRIBUTING.md](CONTRIBUTING.md) covers the contribution workflow and authoring checklist.
- [CHANGELOG.md](CHANGELOG.md) tracks notable packaged changes over time.

## Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| skills.sh / `skills` CLI | Yes | Install individual skills from this repo into compatible agents |
| Claude Code | Yes | Includes `.claude-plugin/` manifest and marketplace catalog |
| OpenAI Codex | Yes | Includes `.codex-plugin/` manifest |
| Manual clone/install | Yes | Clone the repo and copy or symlink skills into user-scope or project-scope skill directories |

## Quick Start

### skills.sh

Use [skills.sh](https://skills.sh/) and the `skills` CLI to install individual skills from this repo:

```bash
npx skills add https://github.com/gokhanamal/ai-context --skill github-actions
npx skills add https://github.com/gokhanamal/ai-context --skill capture
```

Replace the skill name with any directory under `skills/`, such as `ios-simulator`.

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

### Manual Clone Install

Clone the repository, then move or link the skills you want into your agent's user-scope or project-scope skills directory:

```bash
git clone https://github.com/gokhanamal/ai-context.git
cd ai-context
mkdir -p "$HOME/.agents/skills"
cp -R skills/github-actions "$HOME/.agents/skills/"
```

Project-scoped installs work the same way when your agent supports a repo-local skills directory, for example:

```bash
mkdir -p .agents/skills
cp -R /path/to/ai-context/skills/capture .agents/skills/
```

You can also symlink skill directories instead of copying them if you want local edits in this repo to stay live in your agent setup.

## Adding A New Skill

Before creating a new skill, review the [Claude skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

1. Copy `_template/` to `skills/my-new-skill/`.
2. Update `SKILL.md` frontmatter with the final `name` and `description`.
3. Add `references/` or `agents/` content only when it genuinely helps the skill.
4. Add the new skill to the table in this README.
5. Keep repo skills under `skills/` so shared install surfaces, including the Claude and Codex manifests, discover them consistently.
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
├── docs/                   # Brainstorms, plans, and supporting repo docs
├── skills/                 # Reusable skills used by both plugin manifests
│   └── <skill-name>/
│       ├── README.md
│       ├── SKILL.md
│       ├── agents/         # Optional skill-specific helpers
│       └── references/     # Optional supporting docs
├── scripts/                # Local validation helpers
├── AGENTS.md               # Repo rules for contributors and coding agents
├── CLAUDE.md               # Claude-compatible pointer to AGENTS.md
├── CHANGELOG.md
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
