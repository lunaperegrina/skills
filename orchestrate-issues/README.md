# Orchestrate Issues

Coordinate a backlog of GitHub issues across multiple coding agents without letting parallelism violate dependency, migration, or integration constraints.

This is a **scheduler and integrator**, not an implementer. It computes what can safely run right now, dispatches one issue per worker, serializes migration finalization, and recalculates the plan after every merge. The implementation itself is delegated to your implementation skills of choice (`/implement`, `/tdd`, Codex, or any other agent).

## When to use

Reach for this skill when several issues may run in parallel but involve:

- direct or transitive blockers between issues;
- shared-file collisions;
- database schema changes or migrations;
- integration gates or ordered merges;
- human-only tasks mixed into the backlog.

Not worth it for a single issue or a handful of fully independent ones.

## How it works

1. **Build the issue graph** — reads open issues, `blocked by` / `blocking` relationships, and dependencies stated in issue bodies. Detects cycles.
2. **Classify relationships** — not everything is a hard dependency:
   | Class | Meaning |
   |---|---|
   | `hard` | Downstream must not start before upstream is satisfied |
   | `contract` | Downstream consumes an API/schema/domain contract from upstream |
   | `migration` | Parallel implementation is fine; finalization is serialized |
   | `collision` | Parallel work with ordered merge/rebase (overlapping files) |
   | `gate` | Completion depends on an integrated validation |
   | `human` | Requires a human; never consumes an agent worker |
3. **Compute the frontier** — an issue is `READY` only when every `hard`/`contract` blocker is satisfied by **merge + required gates green**. An open or approved PR does not count.
4. **Dispatch workers** — one issue per worker, each in its own worktree and branch (`issue/<number>-<slug>`), invoking your implementation skill of choice in a fresh context. Defaults to 3 implementation workers + 1 integrator.
5. **Serialize migrations** — schema work happens in parallel, but only the holder of the migration lock may create or modify migration SQL, journals, or snapshots, and only during finalization after rebasing onto `main`.
6. **Integrate and recalculate** — rebase, run gates, merge, release locks, and immediately recompute the frontier. Workers are never idle waiting for a "wave" if another safe issue exists.

Every run reports the current frontier, active workers, a Mermaid dependency graph, locks and gates, and what becomes eligible after each next merge. See [examples/example-orchestration.md](examples/example-orchestration.md) for a full worked example.

## Usage

Invoke manually (the skill does not auto-trigger):

```
/orchestrate-issues
```

Typical flow:

```
/to-tickets -> /orchestrate-issues -> /implement (per worker) -> /code-review -> PR -> integrate -> recalculate frontier
```

Tune the run by telling it the issues in scope, exclusions, and desired worker concurrency — it defaults to 3 workers and never asks for information already present in the repo or issue tracker.

## Installation

Copy this folder into your skills directory:

```bash
# Personal (all projects)
cp -r orchestrate-issues ~/.claude/skills/

# Or project-scoped
cp -r orchestrate-issues .claude/skills/
```

Requires `gh` (GitHub CLI) authenticated against the target repository, and git worktree support in the environment.

## Repository layout

```
orchestrate-issues/
├── SKILL.md                          # Agent-facing instructions (the skill itself)
├── README.md                         # This file (human-facing)
├── references/
│   ├── dependency-model.md           # Read before planning non-trivial graphs
│   ├── migrations.md                 # Migration lock protocol (read when schema is at risk)
│   └── status-model.md               # Issue state transitions
├── examples/
│   └── example-orchestration.md      # Full worked example
├── assets/
│   └── icon.svg
└── agents/
    └── openai.yaml                   # OpenAI-specific agent metadata (ignored by Claude)
```

The orchestrator is agent-agnostic: workers can be Claude Code subagents, Codex, or any other executor. Branch names never encode the implementing agent.

## Design invariants

The full list lives in [SKILL.md](SKILL.md). The ones that matter most:

- One issue = one implementation context = one worktree/branch = one PR.
- A blocker is satisfied only by `MERGED + REQUIRED CI/GATE GREEN`.
- Never assign a blocked issue because its blocker has code in an unmerged branch.
- Never edit historical migrations or pick data-conflict winners automatically.
- Correctness first; do not parallelize merely to keep workers busy.
