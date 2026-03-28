# Agents

This directory holds reusable custom agent definitions and related documentation for the broader AI context repo.

## Recommended Layout

```text
agents/
└── <agent-name>/
    ├── README.md
    └── references/         # optional
```

Add tool-specific entrypoint files only when they are required by the target platform.

## Intended Contents

- reusable custom agents with a clear job
- shared agent-specific references
- setup notes for behavior or tool usage
- examples that help people adopt those agents safely

## Conventions

- use kebab-case directories for concrete agents
- include a `README.md` for humans when an agent gets its own folder
- keep agent assets reusable across projects when possible
- add supporting docs only when they materially improve usage
- update the root `README.md` when a new agent becomes part of the main repo surface
