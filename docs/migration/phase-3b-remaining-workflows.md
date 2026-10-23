# Phase 3B: remaining skills and parallel workflows

Branch: `feat/codex-remaining-workflows`, created from latest main `288561b1feda1cf199f46ae36745ec47df6fb4ba` after PR #4 squash merge. The preceding head `74691947a83376563cccfb936a35e06aadab4bd3` was independently reviewed, its reference-map gap fixed, and both exact-head CI jobs passed before merge. This increment retains all original phase 3 remaining gates; phase 4 has not started.

## Work sequence

- [x] Start the branch from merged main and retain source/inventory/evidence ownership.
- [x] Port the read-only Interrogate reference and four prompt/quality/judgment references; remove foreign host paths/tool assumptions and retain no-auto-fix semantics.
- [x] Add whole-panel model validation, explicit task choices, saved reviewer role and exact parent inheritance. Reject any bad member before returning a usable panel. Distinguish independent same-model review from model diversity.
- [x] Inspect native Interrogate acceptance: actual independent starts, calibrated lead verdict, concrete evidence and unchanged workspace/HEAD/index.
- [ ] Port Arena/Architect, comparing full design alternatives and retaining explicit user checkpoint choices.
- [ ] Port Swarm with write ownership, explicit base refs, integration and local-state access boundaries.
- [ ] Port remaining quality/prose/verification/control/authoring skills and expand the bounded playbooks.
- [ ] Complete available live Why source checks and genuine cross-source synthesis; preserve unavailable-source gaps.
- [ ] Run actual A7 concurrent-writer, A8 non-default-base and A9 local-state checks; spawn alone is not isolation proof.
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
