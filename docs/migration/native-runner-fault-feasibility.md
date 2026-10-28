# Native runner fault feasibility — 2026-10-28

**Result: no safe supported per-native-runner crash/network injection interface established in the inspected host.** Fault injection is NOT RUN; deterministic injection is currently BLOCKED on that missing mechanism. This is a bounded read-only assessment, not proof that native failures cannot occur or that every future host lacks such an interface. Do not convert existing interruption, missing-output or HTTP-403 evidence into a crash-recovery pass.

## Publication checkpoint

The reviewed seven-file Arena worktree increment is published as `9d8c4853142dca12274cbaafe470a2b83e958780` on `test/codex-3b-acceptance`. Author and committer are the verified public GitHub identity; remote and [draft PR #6](https://github.com/chrison18/codex-pstack/pull/6) match. Exact-head CI passed [40670673584](https://github.com/chrison18/codex-pstack/actions/runs/40670673584) and [40670673251](https://github.com/chrison18/codex-pstack/actions/runs/40670673251).

Worker local validation was 38 package tests / 65 assertions plus package/syntax/link/diff checks. Coordinator independently reran two cleanup tests and audited actual source-B copy/integration evidence; its root shell lacked Bun on PATH, so no coordinator full-suite rerun is claimed. The [Arena checklist-location deviation](arena-code-worktree-evidence.md) and [Architect replacement-count FAIL](architect-convergence-evidence.md) remain explicit. Ordinary Arena does not establish Architect worktree support, phase 4 recovery or phase 5 autonomy.

## Inspected interfaces and evidence

Local CLI `0.164.0-alpha.11.1` successfully generated its experimental protocol schema without starting an app-server or model:

```sh
codex --version
codex app-server --help
codex app-server generate-json-schema --help
codex app-server generate-json-schema --experimental --out <task-owned-schema-directory>
```

Read the generated ClientRequest methods and relevant parameter/notification definitions, current directly exposed collaboration tools, and `accept-codex-swarm-recovery.py`'s existing interruption scenario. No mutating protocol call, process termination, network change, auth change or GUI action was made. The CLI emitted a PATH-alias permission warning but returned the schema successfully; this is not a tested runtime permission failure.

| Observed interface | What it actually targets or observes | Why it does not close the original actual-runner-failure gate |
| --- | --- | --- |
| Native `interrupt_agent` and protocol `turn/interrupt` | Agent/turn interruption; protocol accepts threadId and turnId | Deliberate cancellation/interruption, already covered by the earlier live Swarm probe; not a crash or transport failure |
| `process/kill` | A `process/spawn` session identified by client-supplied, connection-scoped processHandle | A child command process, not a native collaboration-agent worker; no mapping from agent thread to its own killable process is exposed |
| `command/exec/terminate` | A running command/exec session by connection-scoped processId | Killing a tool command can yield a tool failure while the agent remains healthy; not agent failure |
| `thread/backgroundTerminals/terminate` | Background terminal processId within a thread | Terminal lifetime differs from agent/model lifetime |
| `thread/sample/cancel` | A pending sample requestId | Cancellation, not a network-outage primitive |
| `thread/archive`, `thread/delete`, `thread/unsubscribe` | Thread lifecycle requests with threadId | No inspected contract promises an isolated crash or a failed child terminal result; not safe to infer fault semantics from names |
| `turn/completed` | Separate status values `completed`, `interrupted`, `failed`, `inProgress`; optional TurnError | Sufficient vocabulary to distinguish outcomes if they occur, not an injection control or a guarantee of parent notification/cleanup |
| `error` notification | threadId, turnId, TurnError and willRetry | Retryable errors are not terminal failures; require the eventual child failed terminal and actual parent handling |
| Error variants | HTTP connection/stream connection/disconnection/retry-exhaustion variants plus other error categories | Support observing an actual transport error; no observed per-child endpoint/proxy switch or fault API guarantees creating it safely |

The generated ClientRequest contains 175 distinct request methods. Inspection found the process/command termination and turn interruption APIs above, but no declared per-collaboration-agent crash or transport-fault injection method. The current collaboration schema offers spawn/follow-up/message/list/wait/interrupt, not an isolated worker PID or process handle. Native children in existing captures are identified by thread IDs; that alone does not establish separate OS processes. The harness's own app-server process is shared by parent and children: terminating it would destroy the observer/parent as well and test a different recovery boundary.

Reproduction fingerprints (local generated schema; raw bundle not committed):

| File | SHA-256 |
| --- | --- |
| ClientRequest.json | `503d09a12ae36fca152e044877d22e93b0094c2d08c3a53ed731f3c8cf33b9ce` |
| v2/TurnCompletedNotification.json | `963c4b492eecd8975a3134200b9a2b834f82841243736283c9c18d88d60106a8` |
| v2/ErrorNotification.json | `63518d8faae38b8eb73518d59b113f77603d238dd0cf36260b4232f381f43f8c` |

These are version-specific local schema observations, not a universal product claim. No new fault behavior was observed. Existing Sol-capacity failures remain real failures within their recorded scopes; deliberately repeating an unavailable model or invalid selection would not establish crash/network recovery.

## Smallest conditional test, not authorized/executed here

A genuine native-runner test becomes feasible only if the host exposes a documented task-owned child fault handle or a child-specific test transport that leaves parent and healthy child unaffected. First prove the handle-to-child mapping and supported failure semantics without guessing PIDs, changing global network/auth or suppressing security. No such mapping was established in this assessment.

If that prerequisite becomes available, use one ordinary Arena case: one healthy candidate and one identified failing child in separate disposable worktrees, one declared model pair, and one failure trigger after an observed start. Predeclare that the failed child's incomplete artifact cannot be counted as a completed candidate. The parent must read the actual failure, disclose missing coverage, and either stop or use N−1 only where Arena's task permits it; no false two-candidate comparison or full-coverage claim. Record one actual child `failed` terminal with the relevant error after any bounded transport retry, healthy-child terminal, parent handling, unchanged refs/config and final snapshots. `interrupted`, a tool exit error, synthetic missing output, provider stream warning with willRetry=true, or parent-server disappearance does not satisfy that failed-child predicate.

Safe cleanup is a separate condition: preserve worktrees whenever terminal/activity state is unknown. The current worktree harness accepts only completed child turns for removal; a future failed-terminal cleanup policy needs its own reviewed proof that failure implies no remaining writer/tool activity. Do not silently treat failed as completed or relax the guard during a run. Archive only task-owned evidence before any explicitly safe removal, remove temporary auth independently, and never touch the original Chat or user worktrees.

A smaller **tool-process failure** probe could safely target only a newly created connection-scoped process and observe its failed command result, but would test tool-error handling, not the requested runner crash/network gate. It is not proposed as a substitute PASS, and no such process was started here.

## Return to the finite original queue

Retain actual runner crash/network coverage as BLOCKED/NOT RUN with the above interface limit. The next original shared gate is **native live Why and genuine cross-category synthesis**: first identify one eligible question with two substantive independent source categories and verify read-only source availability in the intended native delegate host. Existing primary GitHub access plus duplicate Git/PR records is insufficient; the recorded Slack Unknown-tool failure and no eligible second category remain constraints until changed evidence exists. A bounded source-readiness assessment is useful work without fault injection or new product changes.

If no eligible sources are available, report that concrete boundary and proceed only under the existing reviewed queue to strict Eval blinding/read-chain feasibility, rather than inventing a second category. Applicable Orca Chat entry/loading, protected installation and native browser limits remain separate. Neither this recommendation nor environment unavailability changes the original phase/merge gates, authorizes a scope reduction, or starts phase 4/5. No convergence rerun or product fix is bundled.

This new assessment is uncommitted for coordinator review. Checks: generated schema parsing and method enumeration succeeded; evidence links and `git diff --check` checked locally. No native fault run or new full package test rerun was needed for this documentation-only assessment.
