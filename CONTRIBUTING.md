# Contributing

Thanks for helping improve this AI context repository.

The best contributions here are focused, well-documented, and easy for another agent user to pick up without extra context.

Start with [AGENTS.md](AGENTS.md) for the repository structure and packaging rules that all contributions should follow.

## Ways To Contribute

- Add a new skill with a clear, narrow purpose
- Add a reusable custom agent or adjacent context asset
- Improve an existing skill's instructions, references, or examples
- Fix packaging, installation, or validation issues
- Improve documentation, templates, or contributor workflows

## Local Workflow

1. Create a branch for the change.
2. Make the smallest change that fully solves the problem.
3. Update docs and packaging metadata alongside the code when names or install paths change.
4. Run the repository validation script:

```bash
python3 scripts/validate_repo.py
```

5. Open a pull request with a short summary, testing notes, and any follow-up ideas.

## Adding Or Updating A Skill

Before creating a new skill, review the [Claude skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

1. Start from `_template/` when creating a new skill.
2. Use a short, action-led, kebab-case name such as `capture` or `github-actions`.
3. Include YAML frontmatter in `SKILL.md` with:
   - `name`
   - `description`
4. Keep the skill focused on one primary job.
5. Include a human-facing `README.md` alongside `SKILL.md`.
6. Add `references/` only when they meaningfully improve accuracy or execution.
7. Update [README.md](README.md) so the skill is discoverable.
8. Keep all repo skills under `skills/` so the Claude and Codex manifests keep discovering the same set.

## Adding Or Updating A Custom Agent

1. Add reusable agent material under `agents/`.
2. Include a human-facing `README.md` when the agent gets its own directory.
3. Keep the asset reusable and avoid project-specific one-offs unless they are clearly documented.
4. Update [README.md](README.md) if the new agent becomes part of the repo's primary surface.

## Writing Guidelines

- Prefer direct, imperative instructions over abstract advice.
- Optimize for fast execution in real repositories.
- State guardrails clearly when a skill should not activate.
- Keep examples realistic and short.
- Avoid adding supporting files unless they materially improve the skill.

## Pull Request Checklist

- The change is scoped to one clear improvement.
- User-facing docs match the current behavior.
- New or renamed skills are listed in [README.md](README.md).
- Repo-level guidance in [AGENTS.md](AGENTS.md) still matches the current structure.
- `python3 scripts/validate_repo.py` passes locally.
- Packaging manifests and `skills/` stay aligned with the current repo contents.

## Reporting Problems

- Use GitHub issues for bugs, docs gaps, and feature requests.
- Use the issue templates when they fit.
- Read [SECURITY.md](SECURITY.md) before reporting anything security-sensitive.
