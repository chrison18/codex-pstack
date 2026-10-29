# Phase 4: bounded task recovery design and evidence

Base: merged core `7c5307971ffcbfae2d90d93da86d246b98de35a1`. This increment targets A10/A11, not phase 5 wake/timer execution. No inventory status or upstream pin changes.

## Design before implementation

One explicitly selected task directory holds an atomic JSON checkpoint and its task-local decision trail. Required context: goal, requirements, authority, scope, ownership, completed/pending operations, evidence, blockers and next action. A revision check plus local file lock prevents stale concurrent writers. The helper records intents before side effects; a completed operation cannot start again, and a started operation whose completion was not recorded becomes an uncertainty to reconcile, never an automatic retry. This is not exactly-once external execution: the helper cannot transact with arbitrary tools or infer whether a remote mutation happened.

Recovery reads only the named checkpoint/history, validates workspace identity, and returns completed/pending/uncertain work. It does not search private provider stores or other projects. The primary verifies existing artifacts and authority before continuing. Read-only tasks use an authorized scratch checkpoint or a response capsule, not writes in a read-only project.

Worktree audit reads Git status/HEAD against an explicit base and accepts explicit session/PR observations with provenance. Active, dirty, open-PR, missing/uncertain observations or unmerged state cannot become safe. Even an all-clear audit returns review-only, never deletion authorization; no fetch, global history scan or cleanup is performed.

## Evidence plan

Use isolated synthetic Git fixtures and separate Python processes: finish one append operation, begin a second, terminate that owned process after its real side effect but before completion, recover in a new process, refuse duplicate starts, reconcile actual artifact evidence and preserve all context. Test stale revisions, scoped identity/history, corrupt data and symlink rejection. Exercise audit against real dirty Git state plus declared active/open/unknown observations, and prove audit does not change files. Host-helper evidence and native client adoption are separate; no model self-report substitutes for the process/artifact checks.

## Implemented candidate and observed host evidence

`plugins/pstack/skills/poteto-mode/scripts/lifecycle.py` provides explicit init/begin/complete/checkpoint/recover/history and read-only audit. The explicit entry now initializes checkpoints for activated multi-step side-effect work without a separate user pause request; small read-only work uses a response capsule, and forbidden writes remain forbidden. The detailed reference is loaded only for this route. No new discoverable skill or implicit activation was added.

On the merged base plus this uncommitted candidate, `python3 -B scripts/test_codex_lifecycle.py` passes six tests on macOS/Python 3.9. Two tests launch and terminate only their own waiting Python child, then use a fresh CLI process:

| Case | Observed result |
| --- | --- |
| Completed first append; second append executed before interrupted receipt | Recovery returns completed `one`, uncertain `two`; context exactly retained; both begin retries exit nonzero; artifact remains exactly two lines; evidence-backed completion settles `two` without another append. |
| Intent persisted, interrupted before any append | Artifact absent and owned child settled; original record remains byte-identical/uncertain; an explicitly evidence-linked successor performs one missing append, records completion and refuses another start. No reset or broad retry engine. |
| Stale writer/wrong logical owner | Both refused without changing record bytes; a valid checkpoint preserves prior context in history and updates blocker/next action with a reason. |
| Wrong workspace/history boundary and symlink | Other workspace rejected; returned history contains only the selected task; symlink task directory rejected. No provider/global history lookup exists. |
| Malformed context/JSON/schema samples | Nonzero failure, existing state bytes preserved. This is tested fail-closed coverage, not exhaustive validation of every malicious shape. |
| Worktree audit | Real synthetic Git repo with tracked WIP is held; supplied active/open/unknown/mismatched or missing session/PR evidence cannot produce a safe verdict; clean confirmed fixture is only review-only with safe_to_delete false; unresolved base held; WIP preserved. Session/PR values are controlled observations, not live Orca/GitHub discovery proof. |

At the host-only checkpoint, native fresh Codex/Orca Chat adoption was **NOT RUN**, pending coordinator review and a separately scoped client proof. These process fixtures establish helper behavior, not automatic model compliance, exactly-once external mutations or phase 4 closure. Host session/PR evidence must still be obtained through supported task-scoped interfaces; absent observation is a hold. POSIX locking is the implemented host boundary; Windows is not certified. Persistent storage must survive the intended interruption; temporary fixture deletion is not a recovery guarantee.

## Checks and review boundary

Package and 87-unit inventory validators pass; Skill Creator quick validation passes. Root `bun test ./scripts/` passes **39 tests / 67 assertions**, including the six Python lifecycle cases. Initially Bun was absent and PyYAML unavailable; temporary test-only dependencies restored those tools. An intermediate suite run lacked Bun in child PATH and failed one pre-existing portable test; rerunning with the temporary tool directory in PATH passed all 39. No product change was made to mask that environment failure. Shell syntax checks and diff whitespace checks pass. No new model run, Git publication, global setting, source pin or inventory status change occurred.

Coordinator's independent first review requested normal activated-task checkpointing and the before-effect interruption case; both are included above. The settled candidate remains uncommitted for final independent review; fresh-client recovery evidence and eventual phase acceptance remain separate.

Inherited script checks also passed: frozen-lockfile install (no changes), strict TypeScript check, and 69 tests / 247 assertions with only the test-subprocess Git signing override. The additional audit identity mismatch assertion passes in the six-test lifecycle suite.

Model-free CLI entry smoke passed on `codex-cli 0.164.0-alpha.11.1`: install, package inventory, qualified invocation, implicit exclusion, short project alias and removal. Initial sandbox loopback bind was denied; normal escalated execution succeeded. This captures host context injection only, not a model response or recovery behavior. At that checkpoint, coordinator independently reran the six lifecycle tests and diff check and reviewed activation/successor limits without a remaining blocker; the subsequent client result is recorded below.

## Actual fresh Orca Chat pickup — 2026-10-29

**Scoped PASS: named-task pickup and evidence reconciliation in a fresh structured Orca Codex Chat.** This supersedes the earlier native NOT RUN checkpoint, without rewriting the host-test history. Tested candidate is based on merged `7c5307971ffcbfae2d90d93da86d246b98de35a1`; helper SHA-256 `19162d4269ba6bb6519fb7210df17a055efee191d96c38fa2af2e268bd50e306`. Provider CLI `0.164.0-alpha.11.1` recorded `gpt-6-astra` / `ultra`. The structured/journaled launch was mapped by supported exact-project search to its task-owned provider capture; no unrelated histories were read.

The host seeded a disposable task at revision 3: operation `one` completed, `two` started with its side effect already present, and `three` pending. Initial file bytes were `one\ntwo\n`. This is deliberately controlled prior state, **not an interrupted live Chat**. The fresh Chat was asked to resume that exact named task within its recorded authority and reconcile uncertain work before continuing. Separate tests above terminate real owned Python processes on both sides of the effect boundary; they are complementary evidence, not a relabeling of this seed as a Chat crash.

Zero-based capture records 16/21/29 read the entry/runtime/lifecycle/principles and task state/artifacts; 39 executed actual `recover` at revision 3. Record 51 completed `two` from existing artifact evidence without replay, began/appended only `three`, and verified the result; 58 checkpointed final context and recovered it; 64 returned the final report; 67 completed the task. Capture SHA-256: `2e4c59396ef207030d75ec8315fd5bd43c0416dab7366effffc4623190c388e9`.

The independent host audit confirmed exact final bytes `one\ntwo\nthree\n`, unchanged original goal/requirements/authority/scope/owner, unchanged prior history and operation-one receipt, and exactly four new history entries: complete-two, begin-three, complete-three, checkpoint. Final revision is 7 with no pending/uncertain operations. README, HEAD and all 46 baselined non-record paths were unchanged. The documentation reviewer independently checked these retained context/history invariants and the matching helper/capture digests. Raw paths, session IDs and private captures stay local. The original user Chat is retained.

## Phase 4 exit review

**Decision: the bounded phase 4 implementation is ready for final independent review and publication/CI, with no additional mandatory model matrix identified.** This is not a merge or full migration claim.

| Gate | Evidence and supported boundary |
| --- | --- |
| A10 retained context and no duplicate work after interruption/restart | Six host tests include real process termination before/after effects; actual fresh Chat reconciles seeded uncertain work, inherits completed evidence and completes only pending work. Local helper history is task/workspace-bound; wrong-workspace reads are rejected. No live Chat crash-control or automatic provider-history reconstruction claim. |
| A11 active/dirty/open/uncertain worktrees are not called safe | Actual Git fixture plus controlled session/PR observations prove hold behavior and identity checks; all-clear remains review-only with safe_to_delete false. The adapter never deletes, and cannot authenticate supplied host observations. Missing supported liveness/PR evidence remains a hold rather than a pass. |
| Usable primary workflow | Explicitly activated multi-step work establishes checkpoints before effects; read-only/no-write fallback remains explicit. Named pickup routes through maintained entry/reference/helper, without global activation or separate copied policy. |
| Review and release boundary | Coordinator reviewed helper and independently reran six tests; prior required package/inherited checks pass. This documentation reconciliation and eventual publication-head CI still need final review. Owner merge authorization is separate. |

Task-scoped checkpoint recall, pickup, decision trail and conservative audit are the implemented phase 4 path. Broader automate-me/reflect mining, provider forensics and safe automatic cleanup are not advertised; inherited named overlays are not silently promoted in the inventory. No extra fixture is required merely to cover every historical host mechanism. If a future support claim needs those integrations, it needs its own evidence. Phase 5 wake/cancel/restart/duplicate-delivery/completion scheduling remains unimplemented and depends on accepted/merged phase 4; external exactly-once, hostile-process isolation and unattended continuation are not proved by this result.
