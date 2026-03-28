# AI Context Repository Guide

This repository packages reusable AI context for coding agents. Keep it small, auditable, and easy to install across supported tools.

## Repository Surfaces

- `skills/` holds reusable skills shared by the plugin manifests.
- `agents/` holds reusable custom agent definitions and related docs.
- `_template/` is the starter layout for new skills.
- `docs/` holds supporting brainstorms, plans, and other working notes when they add value.
- `.claude-plugin/` and `.codex-plugin/` hold packaging metadata and must stay aligned with the repo structure.

## Skill Rules

- Add each skill under `skills/<skill-name>/`.
- Keep skill names short, action-led, and kebab-case.
- Every skill directory must include both `SKILL.md` and `README.md`.
- `SKILL.md` must include `name` and `description` frontmatter, and the `name` must match the directory name.
- Add `references/` or other support files only when they materially improve accuracy or execution.
- Update the root `README.md` whenever a skill is added, removed, or renamed.

## Agent Rules

- Add each reusable agent under `agents/<agent-name>/`.
- Include a human-facing `README.md` in every concrete agent directory.
- Keep agents reusable across projects; avoid one-off repo-specific helpers unless clearly documented.
- Update the root `README.md` when an agent becomes part of the repo's main surface area.

## Packaging Rules

- Keep shared installable assets under the existing top-level surfaces instead of creating duplicate plugin copies elsewhere in the repo.
- When names, install paths, or packaging metadata change, update `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, and `README.md` together.
- Prefer structural improvements that fit this repo cleanly over copying larger plugin layouts wholesale.

## Validation

Run these checks before opening or updating a pull request:

```bash
python3 scripts/validate_repo.py
git diff --check
```
