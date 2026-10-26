# Phase 3B Swarm and A7/A8/A9 evidence

This increment continues `feat/codex-remaining-workflows` from `c94bfaba0095f692fc1c3f61f656aa7c724f6731` in draft PR #5. It ports the inherited `skills/swarm/SKILL.md` at baseline `a06537a883278a63132e2518971166002f3de5de` without changing inherited files or advancing the upstream pin. Swarm remains an internal reference under explicitly invoked Poteto, with no new native entry or implicit activation.

## Adaptation and instrument

The reference retains frame/fan-out/aggregate/report, partition/race/mixed shapes, declared race rules, exact verification refs, measurement method, PASS/ISSUES/BLOCKED reports, one retry for missing evidence and honest coverage gaps. Native `poteto-agent` replaces foreign agent/workspace tools. `swarm-worker` uses singular model resolution, so one-worker tasks are allowed; each assignment retains task > saved role > observed parent precedence. All choices resolve before spawning. Scope and execution limits travel with each brief.

Code writers require distinct real Git worktrees/branches at named refs. A verifier requiring local machine state instead receives a bounded read-only assignment in the primary context, with permitted probe commands and no credential copies. The primary owns integration only after writers finish, combined verification and the consolidated report. Directory ownership is not separate OS sandbox enforcement.

`scripts/accept-codex-swarm.py` creates a disposable repository and local bare remote. `fixture-base` is actually pushed; the remote default is `main`, with unrelated changes including a different function name and a main-only sentinel. Two worker branches and one integration branch are prepared from `origin/fixture-base`, not the default branch. Preparation happens before the model run; workers verify their actual cwd, branch, HEAD and feature-only/main-only contents before writes. This is actual Git ref/worktree behavior, not GitHub network or browser evidence.

Each model authors `proposal.py` in its own worktree. Its own tool process invokes the publisher with that worktree as cwd. The publisher checks branch/base, waits at a barrier until both independent writer processes enter, then writes the supplied source to the assigned tracked module. It supplies no implementation. A separate observer confirms both PIDs are alive and releases the barrier. Shared Unix-epoch nanosecond receipts verify enter/release/write/finish order and overlapping writer intervals; Git directories and indexes must differ. The primary integrates only accepted module bytes after workers finish. Independent checks compare proposal, worker module and integrated bytes, exercise both APIs and verify all four HEADs/indexes and the path allowlists.

A loopback server requires a temporary fixture token held only in the primary's untracked `.local-state`. `local_probe.py` requires the primary cwd and reads that state to authenticate; neither token nor local state is copied to worker worktrees. The isolated-worktree control rejects the required cwd and records absent worker state. This is context rejection, not a failed-authentication exchange. The verifier must run one shared-context probe; the primary independently repeats it. The server records authenticated requests and client PIDs without recording credentials. The disposable host configuration enables network access for this test; only loopback is permitted by the task and observed. It is not a network isolation guarantee.

## First probe — A7 instrument FAIL, retained

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-live-_qyvxhvr`. All three native slices returned, integration and local-state checks passed, and no unexpected path changed. However, the initial instrument compared different processes' monotonic clocks: observed entered/finished values near 0–32 seconds were not comparable with the observer's release at 132 seconds in this environment. It also incorrectly demanded exact one-line proof text even though workers were allowed to enrich their own reports. `result.json` correctly remains `artifactChecksPassed: false`; this run is not counted as the final A7 pass.

The instrument now uses a shared epoch, actual PID-liveness observation and receipt/branch/path identity rather than a fixed report text format. Two model-free instrument tests exercise real publisher subprocesses: wrong-base rejection before any publish; barrier hold before the second writer, live distinct PIDs, shared-clock ordering, richer report acceptance and rejection of fabricated non-overlap. These validate the measuring instrument; they do not replace the fresh real-model rerun below.

## Fresh native rerun — scoped A7/A8/A9 PASS

Client: codex-cli `0.163.0-alpha.11.1`, macOS, system Python 3.9, Sol/low parent, 2026-10-23. Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-live-2fnps4jd`. Raw events and generated fixtures remain local. Event positions below are zero-based JSONL indices.

| Assignment | Observed native start | Model / effort | Required context |
| --- | --- | --- | --- |
| Writer a | `01a167da-3582-7af2-9ee3-aa2e5927a24e` | Sol / low | `fixture-worker-a`, own worktree |
| Writer b | `01a167da-5ea9-7f12-be83-19364c4c55d5` | Luna / medium | `fixture-worker-b`, own worktree |
| Verifier | `01a167da-8806-74b3-9385-dc950eec4f30` | Luna / medium | Read-only primary local-state probe |

The initial guessed runtime path was absent; the primary found the actual entry script without changing configuration. All three resolutions succeeded at events 136/139/142 before spawns 146/200/272. Global agent defaults deliberately differ (Luna/high); actual starts match explicit resolved pairs. Writers verify real branches/refs before proposing code; no inherited vendor alias or silent model fallback was used.

### A7: isolated concurrent writers and integration

Writer publisher PIDs were `95163` and `95193`, with separate Git directories under `.git/worktrees/worker-a` and `worker-b`, separate index files, distinct branches and explicit assigned cwd paths. The observer confirmed both PIDs alive before release. The common epoch receipts establish:

- Both entered before release `1792743751964125000` ns.
- Both wrote only after release, at `1792743752034158000` and `1792743752062688000` ns.
- Both finished after both writes. The writer intervals overlap by approximately 157 ms.

The writer models independently supplied `return a + b` and `return a * b`, with positional/keyword/negative/zero checks. The primary read actual diffs and receipts at events 1711/1713 after terminal results 1380/1689. Writer a supplied exact command evidence on one read-only followup: its compound command's final filename search had exited 1, while the preceding Python assertions passed. The primary distinguished the subcommand results, obtained the missing detail once and closed the gap before integration at 2934. The followup made no changes.

Only `alpha.py` and `beta.py` entered the integration worktree. Its 48 combined API assertions passed, including positional, reordered keyword, mixed invocation, zero and negative inputs. The independently authored harness verification also exited 0 with `swarm integration acceptance passed`. Source/proposal/integrated bytes matched; no shared-file interference or unexpected path change was observed. No worker, primary or integration commit was created; HEADs/indexes remained unchanged.

### A8: pushed non-default base

The local remote's `refs/heads/fixture-base` is `9a55a3bb169e2f86d8f2e6801ff19045dddbcf07`; its default `main` and primary HEAD are `2469223e755dcdb93a55b5e73b60244b9f78e084`. Both writers and integration retained the feature SHA and feature-only sentinel, with the main-only sentinel absent. `origin_kind.KIND == "feature"` passed in independent integration verification. The primary remained on main with its unrelated source unchanged. Precreated/fetched refs were verified rather than falsely claiming the native spawn created the worktrees or fetched GitHub.

### A9: required local process/auth state

The verifier ran `python3 -B local_probe.py` exactly once from the primary context and returned requestId 1; the primary repeated it after the verifier returned, at event 1481, and obtained requestId 2 with the same fresh server challenge. Independent server records show two authenticated requests from distinct client PIDs `95210` and `95258`. This proves access to the required running fixture process and primary-held authentication state, not merely a successful spawn or a copied Git worktree.

No native primary path change or worker credential copy was observed. After the native turn, the harness shut down the service and removed the temporary fixture token and Codex auth symlink. The documented token cleanup is excluded from path comparisons; snapshots otherwise preserve primary entries, file types/modes and symlinks. This passes a bounded local process/auth scenario, not desktop browser/session access, real third-party credential parity or independent per-agent OS sandboxing.

## Results, reproduction and remaining work

Final `result.json`: completed, all nine checks true, three requested/resolved native starts, two authenticated probes, no unexpected paths and independent integration exit 0. The primary consolidated refs, methods, statuses and limitations in `reports/consolidated.md`, rather than forwarding worker dumps. Generated code and private raw event logs are not committed.

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /tmp/pstack-swarm-catalog.json
python3 -B scripts/accept-codex-swarm.py --model gpt-6.1-sol --effort low --catalog /tmp/pstack-swarm-catalog.json
```

Use `--codex /absolute/path/to/codex` when the CLI is not on PATH. The fixture requires those model pairs to exist in the fresh native catalog, Git worktrees, loopback binding and the explicitly configured disposable host access. Missing support must fail/report a gap rather than substitute a model or count an isolated check as local-state proof. Inspect native events in addition to artifact checks.

Subsequent [race and recovery evidence](phase-3b-swarm-recovery-evidence.md) records first-pass/rank-all/best-of and conflict integration, recovery probes and their retained failures. Swarm remains partial; genuine missing/rejected capability and desktop/browser variants remain NOT RUN. The A7/A8/A9 native fixture passes do not complete all phase 3B skills/playbooks/live-source work or authorize phase 4. PR #5 stays draft and must not merge.

## Local regression checks

PASS: 30 package Bun tests / 47 assertions; 13 role/runtime tests (now including Swarm saved/task/parent resolution without changing other choices); two separate publisher-instrument tests; strict root TypeScript and inherited typecheck; package/inventory validation; all 24 principle transformations; skill validation; Bash syntax and diff checks. Isolated CLI smoke passed install, qualified/short entry invocation, ordinary-prompt exclusion and removal; it makes no model request and is separate from the native proof above.

The first inherited-suite attempt while native/smoke probes were active finished 67 pass / 2 timeout failures at its existing 5-second limits, with follow-on errors from killed Git test subprocesses. An isolated rerun using the original limits passed all 69 tests / 247 assertions in 3.60 seconds. No inherited test/runtime code or timeout was changed. The failed attempt is not presented as a pass.

For catalog discovery, the CLI directory must be on PATH; the acceptance script's `--codex` option sets its backend binary but does not change that preceding discovery command. On hosts without the required sandbox/network/local-process capabilities, record the missing access rather than claiming these fixture results apply unchanged.
