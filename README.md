# Skills

A personal collection of [Agent Skills](https://agentskills.io/specification) for Claude Code (and any other agent that reads the open `SKILL.md` format).

Each skill is a self-contained folder whose `SKILL.md` holds the agent-facing instructions and metadata. Skills are invoked with `/<skill-name>` or automatically when a task matches their description.

## Skills

| Skill | Purpose |
|---|---|
| [figma-pixel-perfect](figma-pixel-perfect/) | Make an application page visually identical to a Figma design, starting from just a Figma URL and a page name. Diffs the rendered app against the design, fixes the code, and verifies with screenshots. |
| [orchestrate-issues](orchestrate-issues/) | Orchestrate a backlog of GitHub issues across multiple coding agents. Computes the safe execution frontier from issue dependencies, dispatches one issue per worker, serializes migration finalization, and recalculates after every merge. A scheduler — does not implement the issues itself. |

### Supporting directories

- [figma-pixel-perfect-workspace/](figma-pixel-perfect-workspace/) — benchmark workspace for the `figma-pixel-perfect` skill (fixtures, iterations, and the check script used to evaluate runs). Not a skill.

## Installation

Copy a skill folder into your skills directory:

```bash
# Personal (available in all projects)
cp -r <skill-name> ~/.claude/skills/

# Or project-scoped
cp -r <skill-name> .claude/skills/
```

Then invoke it as `/<skill-name>`, or just describe the task — skills whose description matches will trigger automatically (unless the skill sets `disable-model-invocation: true`, in which case it must be invoked explicitly).

## Conventions

- `SKILL.md` is the skill itself: YAML frontmatter (`name`, `description`) plus the instructions the agent loads. Kept under 500 lines; detail lives in referenced files.
- A per-skill `README.md`, when present, is human-facing documentation (overview, install, usage) and is ignored by agents.
- `references/` holds docs the agent reads on demand; `examples/` worked examples; `evals/` evaluation suites; `assets/` static resources.
- Skills are agent-agnostic where possible — nothing encodes a specific implementing agent.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)
- [anthropics/skills](https://github.com/anthropics/skills) — official skill examples
