# Migration Protocol

Apply whenever an issue may change persistent schema, constraints, generated migration artifacts, or persisted data semantics.

## Principle

Parallelize schema implementation when safe. Serialize migration finalization.

Do not make the migration directory itself the unit of parallel work.

## Migration classes

### none

No database impact.

### schema

DDL/schema shape changes only.

Examples:

- table/column/index;
- nullable/default changes;
- enum/check/foreign-key changes.

### data

No structural change required, but persisted rows require transformation or reconciliation.

Examples:

- backfill;
- deduplication;
- status normalization;
- ownership/globalization migration.

### schema+data

Both DDL and data migration/backfill.

Treat as the highest-risk class.

## Exclusive migration lock

Only one owner may finalize migration artifacts at a time.

Lock scope includes generated or hand-authored migration artifacts, including project equivalents of:

- `apps/api/migrations/**`;
- journal files;
- snapshots;
- generated migration metadata.

Agents may edit declarative schema files in their isolated worktree before obtaining the lock.

## Finalization sequence

For a migration-bearing issue:

1. finish implementation and focused tests;
2. ensure upstream blockers are merged;
3. rebase onto current `main`;
4. acquire migration lock;
5. regenerate migration from the consolidated current schema when supported;
6. inspect SQL manually;
7. verify backfill order relative to constraints;
8. run preflight queries for conflicting production-like data;
9. validate empty-database migration path;
10. validate upgrade from current schema;
11. validate the project's expected repeat/second-run behavior;
12. verify migration ledger/history;
13. verify physical schema;
14. verify row counts and domain invariants;
15. run integration tests;
16. merge;
17. release lock.

## Abort conditions

Stop and require a decision if preflight finds ambiguous conflicting data.

Examples:

- multiple candidate global subscriptions;
- duplicate balances that require selecting an owner;
- multiple active carts where only one may survive;
- competing affiliate attribution;
- destructive nullable -> non-null conversion without deterministic fill rule.

Never choose a winner merely to make migration pass.

## Forbidden shortcuts

Unless the project explicitly uses a different policy, never:

- modify already-applied historical migrations;
- use schema push as a substitute for a committed migration;
- settle migration conflicts by selecting one branch's generated snapshot wholesale;
- merge two independently generated migration histories without regeneration/audit;
- apply production migrations merely because local implementation is complete.

## Production hold

A project may allow migrations to be implemented and tested while forbidding production application.

Represent this independently:

```text
migration_implementation = allowed
production_apply = blocked by #X / human gate
```

Do not mark production rollout complete when only migration implementation is complete.
