# Status Model

Use tracker-native fields when available. Prefer a project/status field for lifecycle and labels for classification.

## Canonical lifecycle

```text
Blocked
  ↓
Ready for Agent
  ↓
In Progress
  ↓
In Review
  ↓
Merge Ready
  ↓
Done
```

## Definitions

### Blocked

At least one hard/contract/human prerequisite is unsatisfied.

### Ready for Agent

All start blockers are satisfied and no worker currently owns the issue.

### In Progress

Exactly one worker owns the issue and has an isolated branch/worktree.

### In Review

Implementation is complete enough for review; PR exists.

### Merge Ready

Review/gates required before merge are green. Merge ordering or migration lock may still delay merge.

### Done

Default meaning:

- merged into `main`;
- required CI green;
- issue-specific integration gate green;
- any required migration finalization committed.

If a project requires a post-merge validation before satisfying downstream dependencies, include it in `Done`.

## Claim semantics

Claim atomically when possible:

```text
Ready for Agent
  -> set assignee/worker
  -> set In Progress
  -> record branch/worktree
```

A claimed issue must not be dispatched to another worker.

## Blocker satisfaction

Default:

```text
PR opened       != satisfied
PR approved     != satisfied
code complete   != satisfied
merged only     != satisfied if required gate is red
merged + gates  == satisfied
```

## Failure transitions

If a worker discovers a new blocker:

`In Progress -> Blocked`

Record the newly discovered relationship.

If review requests normal changes:

`In Review -> In Progress`

If an integration gate fails after merge, do not automatically reopen dependent work already started. Freeze new dispatch from the invalidated contract and have the integrator assess affected active issues.
