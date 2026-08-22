# Dependency Model

Use this reference to build a deterministic execution graph.

## Canonical direction

`A -> B` means A must be satisfied before B starts.

Store only direct hard dependencies in the canonical graph. Compute transitive blockers from them.

If:

- A -> B
- B -> C

then C has:

- direct blocker: B
- transitive blockers: A, B

Do not redundantly add A -> C unless there is an independent direct reason.

## Relationship types

### hard

B cannot be implemented correctly before A is merged.

Examples:

- endpoint requires a table introduced by A;
- consumer requires a domain model introduced by A;
- B's acceptance criteria explicitly require A.

Scheduling effect: blocks start.

### contract

A establishes a contract B consumes.

Examples:

- normalized payment events;
- balance states;
- global membership/tier semantics;
- shared API response shape.

Treat as hard unless B can genuinely implement against an already stable pre-existing contract.

Scheduling effect: normally blocks start.

### migration

Two issues can implement declarative schema independently but generated migration artifacts cannot be finalized concurrently.

Scheduling effect: does not necessarily block implementation; requires exclusive migration lock before finalization/merge.

### collision

Likely overlap in files/modules but no semantic prerequisite.

Scheduling effect: parallel implementation allowed when useful; merge is ordered. Later PR rebases after earlier merge.

Escalate collision to hard dependency only if one branch would otherwise code against an invalid contract.

### gate

A validation or integration checkpoint.

Examples:

- marketplace E2E;
- financial reversal suite;
- release readiness;
- migration rehearsal.

Scheduling effect: blocks whatever explicitly depends on gate success.

### human

Manual action such as backup/restore validation, approval, credential provisioning, or production rollout.

Scheduling effect: not assigned to implementation workers.

## Frontier algorithm

For each open in-scope agent issue:

```text
ready =
  not claimed
  AND all hard blockers satisfied
  AND all contract blockers satisfied
  AND required human prerequisites satisfied
  AND no exclusive-start lock conflict
```

The frontier is all issues where `ready = true`.

After every state transition that may alter readiness, recompute the frontier from source-of-truth state. Do not incrementally assume the old frontier is still valid.

## Cycles

A hard/contract dependency graph must be acyclic.

If:

A -> B -> C -> A

do not guess an ordering. Report:

- cycle members;
- edges that created the cycle;
- which edge appears weakest, if inferable;
- what decision is needed.

Collision and migration relationships do not participate in hard-DAG cycle detection unless explicitly escalated.

## Critical path bias

When multiple READY issues exist, prefer an issue that unlocks more blocked work.

Useful tie-breakers:

1. transitive dependents count;
2. foundational contract;
3. schema prerequisite;
4. integration critical path;
5. low collision risk.

Do not sacrifice safety for maximum worker utilization.
