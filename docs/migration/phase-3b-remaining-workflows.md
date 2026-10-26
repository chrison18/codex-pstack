# Phase 3B: remaining skills and parallel workflows

Branch: `feat/codex-remaining-workflows`, created from latest main `288561b1feda1cf199f46ae36745ec47df6fb4ba` after PR #4 squash merge. The preceding head `74691947a83376563cccfb936a35e06aadab4bd3` was independently reviewed, its reference-map gap fixed, and both exact-head CI jobs passed before merge. This increment retains all original phase 3 remaining gates; phase 4 has not started.

## Work sequence

- [x] Start the branch from merged main and retain source/inventory/evidence ownership.
- [x] Port the read-only Interrogate reference and four prompt/quality/judgment references; remove foreign host paths/tool assumptions and retain no-auto-fix semantics.
- [x] Add whole-panel model validation, explicit task choices, saved reviewer role and exact parent inheritance. Reject any bad member before returning a usable panel. Distinguish independent same-model review from model diversity.
- [x] Inspect native Interrogate acceptance: actual independent starts, calibrated lead verdict, concrete evidence and unchanged workspace/HEAD/index.
- [x] Port Arena/Architect with full alternatives and explicit checkpoint choices; bounded native synthesis/checkpoint/default-implementation probes passed, with remaining negative/desktop/worktree gaps retained below.
- [x] Port Swarm with write ownership, explicit base refs, integration and local-state access boundaries; see [native evidence](phase-3b-swarm-evidence.md) and [race/recovery evidence](phase-3b-swarm-recovery-evidence.md), with desktop limits retained.
- [x] Port all remaining quality/prose/verification/control/authoring candidates and expand bounded playbooks; see [portable evidence](phase-3b-portable-evidence.md) for dependency order, native results and precise partial limits.
- [ ] Complete available live Why source checks and genuine cross-source synthesis; preserve unavailable-source gaps.
- [x] Run actual bounded native A7 concurrent-writer, A8 pushed non-default-base and A9 local-process/auth checks; inspect live-PID/clock receipts, real worktree metadata, combined verification and authenticated requests. Desktop/browser variants remain NOT RUN; see [evidence](phase-3b-swarm-evidence.md).
- [ ] Reconcile every phase 3 inventory entry, complete applicable desktop/native evidence, independent review and CI before phase 3B merge.

## First candidate: read-only adversarial review

The installed package still exposes only Poteto and setup as explicit native entries. Interrogate is a scoped reference inside active Poteto mode. It gathers a named immutable diff/context, runs independent reviewers and has the primary inspect and bucket findings as Act on / Consider / Noted / Dismissed. Empty reviews are valid. Quality-lens examples are proposals, not authorization to refactor. No review automatically edits files or posts GitHub feedback.

`runtime.py resolve-panel PROJECT interrogate-reviewer` takes observed parent model/effort, a native catalog and optional `--selections` JSON array. Each member uses existing task > saved role > parent precedence. At least two selections are required. Defaults yield two independent reviewers on the same resolved pair; that is explicitly not multi-model review. Actual distinct model IDs determine diversity. The function validates the full list before any caller starts delegates, writes no preferences and returns no partially usable result for an invalid member. Existing role templates and ownership receipts are unchanged.

All four inherited Interrogate references are hashed and mapped in the inventory; their complete mapping is required even while runtime support is partial. Source remains `a06537a883278a63132e2518971166002f3de5de`. One local native two-model review passed as recorded below. Empty-review, delegate-dropout, missing-role and invalid-explicit-model client paths remain unverified; the unit stays partial. No UI parity or complete 3B pass is claimed.

The native fixture uses a shipping fee change that incorrectly charges quantity zero. It asks two explicitly selected models for independent read-only review and expects the primary to verify a concrete counterexample without applying a fix. The fixture's code/history, non-Git state, HEAD and index are captured separately. External business data is excluded. Auth references are temporary and removed after the run. Raw logs remain local.

## Local native acceptance — first review unit

Client: codex-cli `0.163.0-alpha.11.1` native app-server, Sol/low parent, parent read-only sandbox, 2026-10-23. Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-research-live-b8vsq5wu/review`. The reviewer task used explicit Sol/low and Luna/medium choices from a freshly queried native catalog.

The full `resolve-panel` command completed at event 119 before either spawn (events 263 and 287). Native starts confirmed `01a16791-99b4-7e22-897e-dd2d035eac3f` at Sol/low and `01a16791-d5ab-7ed0-953b-3713aeba705d` at Luna/medium. Both independently inspected the immutable parent-to-target diff and found the zero-quantity fee regression. The primary inspected the same source, agreed on Act on, rejected unsupported impact claims because the function had no local caller, and kept unrelated batching changes separate from the fee requirement. The reply explicitly labeled counterexamples static deductions rather than executed tests; no fix was applied.

Harness result: completed; two spawn requests and two resolved starts; `changed: []`; workspace entry snapshots, HEAD and staged diff unchanged; temporary auth reference removed. This is native backend evidence, not desktop UI evidence, runtime execution of the shipping fixture, or proof of write-worktree isolation.

Unit checks: 12 Python runtime tests passed, including inherited/role/task pair resolution, accurate one-model diversity reporting, bad panel members, no preference mutation, and a bad later member producing an error with no partial stdout. The package suite passed 29 tests / 44 assertions before the additional CLI negative case; the final rerun includes it inside the runtime wrapper. Package/source validation, complete reference-map checks, 24-principle transformation, strict inventory TypeScript, isolated install/qualified+short invocation/ordinary-chat exclusion/removal smoke and diff checks passed.

## Arena / Architect candidate

Arena and Architect are internal references under the same explicit Poteto entry, with no new native entry or implicit activation. Arena retains frame, independent candidates, completed-writer crossjudging, independent primary scoring, base/graft decisions and verification of the synthesized artifact. Architect adds How/Why grounding, caller-first sketches, at least two structural alternatives, all three hashed source references, red-flag screening and the implementation/scrap loop. An explicitly requested design checkpoint pauses; default behavior continues the already authorized implementation.

The runtime adds `arena-runner` and `architect-runner` panel roles and singular `arena-judge`, sharing existing precedence and whole-pool rejection. The legacy `reviewers` result field is retained for panels of runners as well as reviewers. Defaults permit independent same-model runners and do not claim model diversity. A model ID or effort does not prove structural diversity. Source vendor aliases and global rule paths are removed; the inherited source tree and baseline hashes remain untouched. Architect reference maps cannot be omitted from CI, including while the unit remains partial.

Artifact candidates use separate owned scratch directories; repository code candidates require separate worktrees and explicit base refs. Directory assignments do not establish independent host sandboxes. The native acceptance below exercises artifact ownership under a workspace-write parent, not concurrent code-worktree isolation. Those design probes did not clear A7/A8/A9; the subsequent [Swarm increment](phase-3b-swarm-evidence.md) supplies bounded native evidence.

### Arena native result

Client: codex-cli `0.163.0-alpha.11.1`, Sol/low parent, 2026-10-23. Evidence root: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-design-live-nu7bvc32/arena`. The fixture has a pre-existing tuple-based `total(items)` API; candidates must retain its callers while rejecting negative quantities, then produce a separately verified synthesis. Auth is referenced temporarily and removed after each run. Raw logs stay local.

The pool and judge resolved successfully at event 108 before spawning. Actual native starts confirmed candidate 1 Sol/low (`01a167a9-b140-72f0-942b-dfe077f7312f`), candidate 2 Luna/medium (`01a167a9-dc59-7893-9037-1690f5f344da`) and judge Luna/medium (`01a167aa-e208-7d21-b8e2-a28818a41efb`), overriding deliberately different global agent defaults. Candidate finals were events 618 and 795; judge spawn was event 813. The primary's full candidate read completed at event 839, before its decision. Judge completion preceded integration.

The candidates produced a validating generator retaining built-in `sum`, and a direct accumulator. Both primary and judge recommended the generator to preserve existing summation behavior, despite the accumulator's simplicity advantage. The decision records the scores, rejected accumulator and convergence on validation; no artificial code graft was claimed. The primary verified the absolute synthesized module against unchanged `check.py` and additional checks; an independent harness run of that exact file also exited 0 with `design acceptance passed`. The change snapshot contains only candidate/synthesis artifact paths. Production files, configuration, HEAD and index remained unchanged; zero dropouts and three observed delegate starts. This is native backend evidence, not desktop UI evidence.

### Architect grounding correction

The initial checkpoint probe in `pstack-design-live-nu7bvc32/architect-checkpoint` grounded the two-line API through primary static reading and explicitly skipped How explainer delegation to limit itself to runners/judge. Available roles and scope did not require that skip. Artifact/checkpoint success alone therefore does not establish full Architect conformance. The Ground reference now explicitly carries How's prescribed delegation and fallback conditions. A fresh checkpoint run checks that correction; the failure is retained rather than relabeled as a full pass. Event indices in this increment are zero-based JSONL positions.

### Reproduce native design probes

With a trusted, authenticated Codex CLI on PATH, refresh the catalog immediately before testing:

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /tmp/pstack-design-catalog.json
python3 -B scripts/accept-codex-design.py --model gpt-6.1-sol --effort low --catalog /tmp/pstack-design-catalog.json
```

Pass `--codex /absolute/path/to/codex` when it is not on PATH (as on the owner's Terminal); add `--case arena`, `--case architect-checkpoint`, or `--case architect-implement` to select a probe. Use catalog-supported selections; the fixture deliberately requests Sol/low and Luna/medium and must fail rather than substitute when unavailable. Each case has isolated project/configuration state and temporary auth references, no remote, unchanged HEAD/index and captured entry snapshots. Artifact checks are necessary checks, not a semantic pass: inspect actual model starts, completed-writer ordering, full candidate reads, structural alternatives, red-flag decisions and final behavior before recording conformance. A checkpoint probe must not execute or implement the application; the implementation probe must exercise the unchanged check against the implemented API.

### Architect checkpoint rerun — PASS within static scope

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-design-live-b8cvz078/architect-checkpoint`. Native starts confirmed How explainer Sol/low (`01a167af-5e12-78e0-a6ed-1941a7438c79`), candidate 1 Sol/low (`01a167b0-8cf4-7f81-a204-f4bed9e19343`), candidate 2 Luna/medium (`01a167b0-b932-7ce0-acbf-a61dcb6b6550`) and judge Luna/medium (`01a167b2-a3d8-7871-a4f0-e35b2bbc6766`). How completed at event 600 before either runner spawn (622/678). Candidate finals were 1161/1456; judge spawn was 1470. The primary read all candidate files at 1526; the judge completed at 2746; the final checkpoint reply was 3017.

Actual alternatives were private validated immutable records with a trusted reducer versus a direct functional validation/aggregation boundary. Both packages include caller usage, signatures/pseudocode, module ownership and rationale. Primary and judge screened all eight red flags, agreed on the functional base and explicitly discussed differing scores. The primary rejected a candidate's unsupported claim that private records necessarily leak to callers and clarified ordinary addition versus augmented assignment. It adapted trace/consumption wording without pretending a forced structural hybrid was needed. This demonstrates artifact inspection and reconciliation rather than forwarding the judge's verdict.

The final package retains unimplemented pseudocode, labels contract traces as static, presents the design and waits for approval. All application/configuration hashes, HEAD and index were unchanged; no application execution/import was observed, no unexpected path changed, and the temporary auth reference was removed. This passes the requested checkpoint path; it does not prove implementation, scrap/reframe/dropout recovery, desktop UI, or independent sandbox enforcement.

### Default implementation scope correction — initial probe FAIL

In `pstack-design-live-nu7bvc32/architect-implement`, the How explainer executed `python3 -B check.py` at event 255 before synthesis, while the fixture reserved execution for the primary after synthesis. It correctly reproduced the baseline failure and made no file changes, but that does not satisfy the assignment boundary. The probe was stopped; the server and auth reference were cleaned up, tracked diff remained empty, and `scope-failure.json` records the reason locally. This is not counted as a default-path pass.

Architect Ground now explicitly propagates the user's execution timing and permitted evidence commands to How, runners and judge. The fixture also states static-only delegate work unambiguously. A fresh default-path run checks both scope propagation and implementation; interrupted future harness runs retain result/snapshot evidence and clean auth in `finally`.

### Architect default implementation rerun — PASS within fixture scope

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-design-live-dmyn1bph/architect-implement`. Actual native starts: How Sol/low (`01a167b6-57b5-7861-a5cb-f37c403c8050`), candidate 1 Sol/low (`01a167b7-02db-7422-a630-62881f486415`), candidate 2 Luna/medium (`01a167b7-24d3-7581-9f60-8672392151f1`) and judge Luna/medium (`01a167b8-b7db-7dd3-8c38-666d7494f9a0`). How completed at 504 with only static commands; candidate spawns were 526/579. Candidate finals were 1029/1314, judge spawn 1329, full primary candidate reads 1056/1351, and judge final 1733. No delegate executed/imported the application in this rerun.

The primary scored both shapes and reconciled the read-only judge's findings. In particular, the functional candidate proposed a positional-only marker that would break `total(items=...)`, plus unnecessary integer annotations. The synthesis retained the original unannotated keyword-compatible signature and adapted the record candidate's validate-before-multiply and operand-preservation rationale while rejecting the record/class allocation. All red flags and accepted tradeoffs are recorded. The user requested default implementation, so no extra approval checkpoint was introduced.

Only after synthesis and judge completion did the primary change `app.py` (1829), run unchanged `check.py` (1833), refine augmented addition to ordinary addition during diff review (1849) and rerun the same check successfully (1853). Independent harness verification of the final application also exited 0 with `design acceptance passed`. A separate supplemental run passed keyword calls, one-shot iterables, Decimal operands, unchanged negative-price behavior and late negative rejection; it is recorded locally in `supplemental-verification.json`. These are bounded Python 3.9 fixture checks, not exhaustive equivalence across numeric types or Python versions.

Changes were limited to `app.py` and candidate/synthesis artifact paths. `check.py`, configuration, HEAD and index were unchanged; temporary auth references were removed. No structural-friction pattern arose, so Scrap was not exercised. Dropout/reframe recovery, same-model native design pools, code-worktree writing, non-default base/local-state verification and desktop design flows remain NOT RUN. Arena and Architect remain partial inventory units rather than full parity claims.

### Checks for this design increment

PASS: 13 Python runtime tests; 29 package Bun tests / 45 assertions; 69 inherited Bun tests / 247 assertions; strict inventory TypeScript and inherited typecheck; package/inventory validation; all 24 principle transformations; all three Architect transitive-source hashes independently compared with the inherited Git baseline; skill validation; Bash syntax and diff checks. Isolated CLI smoke passed installation, both explicit entry forms, ordinary-prompt exclusion and removal. The smoke does not call a model; native model evidence is recorded separately above. Native probe failures are retained and excluded from the final three passing behavior cases. PR #5 remains draft; those design checks did not complete phase 3B or A7/A8/A9. Subsequent native Swarm results are recorded below.

## Swarm increment

[Swarm and A7/A8/A9 evidence](phase-3b-swarm-evidence.md) records the initial instrument failure, two instrument regressions, fresh native pass and remaining limits. Current validation includes 30 package Bun tests / 47 assertions and 13 runtime tests (including singular Swarm selection), separate from the two new publisher-instrument tests. These passes do not complete the remaining 3B work or change PR #5 from draft.

### Swarm race/recovery increment

[Native race/recovery evidence](phase-3b-swarm-recovery-evidence.md) records three selection rules, actual overlapping patch integration, controlled incomplete reports and native interruption, including an excluded first recovery probe. The instrument has five regression tests, invoked in CI through the package suite. Swarm remains partial, remaining 3B gates remain pending and PR #5 stays draft.

## Portable skills and playbooks increment

[Portable evidence](phase-3b-portable-evidence.md) records 22 additional skill references, nine playbooks, six pinned transitive references, dependency guards and native forward tests. Pending source units are now zero; adapted/partial/deferred counts are 37/31/19. This does not clear native installation restrictions, desktop coverage, strict Eval blinding, full formal-tool coverage, live Why or later-phase overlays. PR #5 remains draft and phase 4 remains blocked on the remaining 3B gates.
