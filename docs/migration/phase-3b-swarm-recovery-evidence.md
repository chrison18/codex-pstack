# Swarm race and recovery evidence

This increment continues draft PR #5 from `c66844afb38c57f65bf5eeaa07ab4e2d7dd29f19`. The inherited source pin remains `a06537a883278a63132e2518971166002f3de5de`; inherited files are unchanged. Swarm remains an internal reference under explicitly invoked Poteto. Its reference now distinguishes earliest eligible completion from fastest self-reported PASS, all-result ranking and single-winner best-of, with a rubric and tie-break fixed before submissions.

## Instrument and scope

`scripts/accept-codex-swarm-recovery.py` runs three independently disposable native cases: `race`, `recovery`, `conflict`. Each uses real native `poteto-agent` starts with explicit resolved settings, temporary project roles/auth references, entry snapshots, HEAD/index comparisons and local event capture. The parent is Sol/low; arm a/healthy uses Sol/low and other arms Luna/medium. Deliberately different global agent defaults are Luna/high. No service or desktop automation is used. Client: codex-cli `0.163.0-alpha.11.1`, macOS, Python 3.9, 2026-10-23. Raw transcripts/generated fixtures remain local; event indices below are zero-based JSONL positions.

For report cases, models execute a one-batch four-case check of a read-only quotation function, calculate the actual input total and author JSON proposals containing exact base refs, results, commands and sample definition/order. The publisher supplies no answers. It physically corrupts/truncates selected published artifacts; only those immutable artifacts are eligible evidence. Optional extra examples distinguish quality, without claiming model performance or a benchmark. The primary must inspect published reports rather than filling gaps from a proposal or worker prose. Artifact checks require additional semantic event audit before a run is counted as a workflow pass.

Five model-free instrument tests cover wrong-total eligibility, missing command evidence/placeholders, quality differences, non-report rejection, actual report truncation and retry limits, late rule declaration, matching a running dropout interruption, and real overlapping Git patches. These are CI regressions for the instrument, separate from real model evidence. The shared app-server client adds an optional timeout parameter; existing callers retain the 900-second default, and these multi-stage probes use 1,800 seconds.

## Three race rules — PASS within fixture scope

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-race-2pdtcbvt`; base `84eba69c1924064a6961437ae6efb9907ea4dab1`.

Two actual agents were reused across three rounds: a `01a1680d-737c-79b2-aa9f-221524b0d2a3` Sol/low; b `01a1680d-9430-7783-8a6d-c6711d07069f` Luna/medium. Native starts (213/269) followed model resolution. Before each round, the primary declared the selection rule, four mandatory eligibility cases, optional two-point quality rubric and arm-id tie-break. Both arms received the same task. Each published exactly once per round.

| Rule | Actual fault / evidence | Result |
| --- | --- | --- |
| first-pass | a published first but its total was corrupted to 12; correct total is 11. b publication was held until a submitted. | a rejected; b selected as earliest eligible result. |
| rank-all | a's optional examples removed, leaving eligible score 4; b eligible score 6. | Ordered set b, a. |
| best-of | b's optional examples removed, leaving eligible score 4; a eligible score 6. | Single winner a. |

Child final events were 752/912, 1257/1458 and 1850/1978; primary selection writes occurred at 934, 1477 and 2089. Both workers were drained in every round. The final report excluded invalid evidence, retained the declared rules and did not restore stripped optional points from proposal files. The unchanged repository, HEAD and index passed independent snapshot checks. Regrading all six artifacts with the stricter command-evidence guard added during recovery work retains these results. All race artifact checks passed. This is controlled artifact quality variation, not evidence that one model is generally better/faster; tied-score behavior is declared but not separately exercised here.

## Conflicting code integration — PASS within fixture scope

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-conflict-u4bz3k8r`; base `1b4e4e117d51cf0c76e620f658270f119e50e187`.

Separate real Git worktrees/branches start from the same two-line `total(values)` implementation. Writer a `01a1680d-9953-7e70-aac4-cd032282a2f6` Sol/low added negative-value rejection with one-shot iterable support. Writer b `01a1680d-ba0b-74f2-9cd3-1aa70f6401ed` Luna/medium independently added optional `fee`, retaining keyword calls. Native spawns were 127/184; final results 982/673. Neither writer read the other's implementation.

After both completed, the primary inspected actual diffs. Applying a's actual patch succeeded at 1011. `git apply --check` of b's actual patch failed at 1013 with exit 1 and `patch does not apply`; the check left the integration source unchanged. After reading that evidence, the primary manually reconciled both requirements in the integration worktree. Combined verification at 1121/1134 and independent harness replay passed empty input, fee, generator, keyword and negative rejection cases. Only each assigned `calc.py` changed; the primary repository, all HEADs and indexes stayed unchanged. No worker commit or cleanup was performed. Worktrees were prepared by the harness, not falsely attributed to native spawn behavior.

## Recovery first probe — excluded from conformance pass

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-recovery-x18hvzy5`. The original loose artifact checks returned true, but semantic audit found a healthy report with an unresolved `COMMAND` placeholder. Its numeric results were correct, but its recorded command was not reproducible. That run is not counted as a complete recovery pass. The first interruption also targeted an already-completed dropout turn; a later interruption returned `previous_status: running`. A duplicate spawn request hit the native thread limit without creating another worker. These observations remain retained, rather than being presented as a clean four-worker probe.

The instrument now rejects absent/placeholder commands and verifies a matching native interrupt result for the named dropout with previous status `running`. Task instructions require a separate executed evidence command, keep yielded hold sessions active, start dropout last and interrupt it immediately. A fresh case verifies those corrections; the original result file is historical and is superseded by this semantic audit.

## Fresh recovery rerun — PASS for expected incomplete coverage

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-recovery-_5efr_kw`; base `1f752da7a950d3bdd0ac97b047520be452845f9c`. All four model choices resolved before fan-out. Actual starts: healthy `01a16816-fb53-7650-b221-f271aaff3127` Sol/low; once `01a16817-1dc1-71d0-91f0-715b3c3913fc`, twice `01a16817-3ce9-75c3-a031-5949eb607491`, dropout `01a16817-d1e9-7a70-8e8c-1e6271547cd9`, all Luna/medium. The first dropout spawn request hit the native concurrency limit without creating a worker; the same required slice started successfully after healthy completed. Thus there are five requests but exactly four actual starts, not four simultaneously running workers or a hidden replacement slice.

| Slice | Published evidence / action | Final result |
| --- | --- | --- |
| healthy | One complete report, actual runnable evaluation command, correct refs/method/results. | PASS |
| once | First report physically lost SHA and also contained string-typed numeric results. One same-worker followup corrected types and republished verified evidence. | PASS after one retry |
| twice | `method` physically absent on both publications, despite a complete proposal. One same-worker followup; no third request/publication. | GAP |
| dropout | Held helper wrote ready marker; native interrupt at 1296 returned `previous_status: running` at 1306. Primary released it; same worker drained its session at exit 98 without a report. | GAP |

Healthy finalized at 976; once at 1445/1923; dropout at 1674 after release and drain; twice at 2182/2613; primary finalized at 2854. Actual retry calls targeted once/twice at 1480/2191. The primary independently reran the accepted healthy/once evaluation commands and obtained exit 0 with matching results. Published-artifact grades are healthy valid, once invalid then valid, twice invalid then invalid. It did not fill the missing method from the proposal or worker prose. A sandbox-denied process-list check was not counted as proof; actual native running-status interruption and held-session exit provide the bounded evidence.

Final `summary.json` correctly records `complete: false`, PASS for healthy/once and GAP for twice/dropout, with exactly one retry each for once/twice. All seven artifact checks passed; source/configuration entry snapshots, HEAD and index stayed unchanged. Primary release existed before harness cleanup; no dropout report was created and the auth reference was removed. Passing this negative scenario means handling failure honestly, not claiming the required workload completed. The Swarm reference also explicitly treats placeholder commands as missing evidence under the same one-retry rule.

## Local regression checks

PASS: 31 package Bun tests / 49 assertions, including five fault-instrument tests; 13 runtime tests and two earlier publisher-instrument tests remain covered. All 69 inherited tests / 247 assertions passed in an isolated run, with original timeouts. Strict root TypeScript, inherited typecheck, package/inventory validation, all 24 principle transformations, skill validation, Bash syntax and diff checks passed. Isolated CLI smoke passed install, qualified and short invocation, ordinary-prompt exclusion and removal; it calls no model and supplies no desktop UI proof. CI does not run authenticated native model probes.

## Reproduction and remaining limits

Place the CLI directory on PATH for catalog discovery, or use its absolute path. Refresh the catalog before running authenticated model probes:

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /tmp/pstack-swarm-recovery-catalog.json
python3 -B scripts/accept-codex-swarm-recovery.py --case race --model gpt-6.1-sol --effort low --catalog /tmp/pstack-swarm-recovery-catalog.json
python3 -B scripts/accept-codex-swarm-recovery.py --case recovery --model gpt-6.1-sol --effort low --catalog /tmp/pstack-swarm-recovery-catalog.json
python3 -B scripts/accept-codex-swarm-recovery.py --case conflict --model gpt-6.1-sol --effort low --catalog /tmp/pstack-swarm-recovery-catalog.json
```

Use `--codex /absolute/path/to/codex` for probes when needed. Missing catalog/model/role/native tool support must remain a reported failure or gap. Controlled missing artifacts and native interruption do not establish recovery from an actual process crash, network outage or rejected capability. Desktop/browser variants, tie-specific runs and other phase 3B skills/playbooks/live-source gates remain unverified. Swarm stays partial; phase 4 has not started. PR #5 stays draft and must not merge.

## Later acceptance supplement

PR #5 subsequently merged as phase 3B1. The [3B2 evidence](phase-3b2-acceptance.md#second-increment-swarm-tie-and-local-rejection--scoped-pass) records separate native tied-score and local HTTP rejection probes on 2026-10-26. The historical scope and limitations above describe the original runs; full 3B remains incomplete.
