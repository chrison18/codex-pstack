# Foreground supervised continuation

Design on merged PR #10 `089eca8a2cdfac4787eb34c685fd3f2615efafbc`: an explicitly requested supervised task stays in the original Orca Chat, which waits for exact accepted worker settlement and advances the next bounded unit without a user continuation prompt. Ordinary poteto-mode is unchanged. The primary owns goal/review; one worker at a time owns effects. This is opt-in foreground supervision, not shutdown recovery, a recurring service or an installed event source.

## Host contract and durable guards

Orca 1.4.245 version-matched orchestration documentation defines valid `worker_done` as Task/Dispatch settlement, whole-batch FIFO replay/ack, `check --wait`, `worker-show`, `worker-start`, and request-ID reconciliation. The worker-show parser was grounded in actual task-owned live and settled responses, including completed dispatch/succeeded projection, exact Run/Task/Dispatch and workspace. It does not mistake a retained live Chat for an unsettled dispatch, nor claim that cooperative settlement guarantees OS process exit.

The helper stores supervision in the existing atomic checkpoint: exact workspace/task-directory binding, Run, finite dispatch count/deadline, per-unit intent/token/delivery and actual host receipt. It persists launch intent and resolved argv/cwd before the host mutation, releases the lock across that call, and rechecks terminal/deadline before starting. Duplicate IDs, unsettled/unknown starts and terminal runs cannot start another worker. Claim requires exact host proof; continuation requires that writer token and assigned operation/delivery. Old tokens cannot issue later units. Accepted successful host settlement plus completed operation receipt and primary artifact/resource evidence precede a successor. Evidence presence is validated; the primary must establish its truth.

Cancellation is terminal but cooperative; launch or effects already running may settle later. Deadline/count exhaustion prevents new starts/effect issuance, not forced process termination or a hard spending cap. The first bounded mode excludes detached tools and further delegates; uncertainty holds. Coordinator restart reads the named record and own Run, reconciles exact request/dispatch, and never retries blindly. Models inherit host settings unless the user explicitly selects them; actual launch metadata must be inspected.

## Local checks

Eight owned-fixture tests cover two sequential units and immutable frozen context; duplicate settlement/start and completed no-start; lost receipt with fresh-process restart HOLD; cancellation during host launch and before host invocation; exact/copy/old-token/assigned-operation guards; competing process intent reservation; malformed nested proof shapes; late claim/deadline/count and uncertain-effect boundaries. Host replies are captured-shape controlled stubs, not native proof. Existing continuation and task-event tests remain passing.

Repository suite: 42 pass; inherited suite: 69 pass; frozen install/typecheck, package/inventory/portable-source validators, skill validation, shell syntax, diff check and model-free entry smoke pass. The smoke uses a local loopback capture with normal authorized escalation and calls no model.

## Native acceptance plan and status

One approved isolated primary Chat, at most two sequential workers, two alpha/beta operations, ten-minute new-work bound, maintained project-local entry alias, unchanged README/Git, checkpoint-only bookkeeping, no additional delegates/background tools/network/publication. Start from a natural `$poteto-mode` supervised-continuation request with task restrictions, not helper instructions. Required observations: actual entry/route reads; exact accepted lifecycle receipts and model settings; first writer settled and verified before second; original first-unit receipt/history unchanged; final exact bytes, terminal close, retained sessions and no unrelated mutation. Process success or accepted submission alone is not behavioral PASS.

Native result: scoped PASS, as detailed below. Source pin and all 87 inventory classifications remain unchanged. Coordinator review/publication/current-head CI and owner merge remain separate.

## Actual native observations — scoped PASS

One natural task request in a fresh structured Orca Chat on 2026-11-02, Orca **1.4.245**, Codex CLI **0.164.0-alpha.11.1**. Primary and both workers actually used **gpt-6-astra / low**; start receipts requested no model/effort override, and provider turn contexts establish observed settings. The project-local maintained entry was used. The primary created its own Run and two Tasks, not this migration coordinator's Run. No further delegates or extra model attempts occurred.

Exact user prompt:

> $poteto-mode Complete this small task with supervised continuation, without asking me to continue: make steps.txt exactly alpha then beta, each on its own LF-terminated line, in two sequential verifiable units, appending and checking each line once. Use at most two sequential workers and a ten-minute bound for new work. Keep the original Chat as supervisor, retain all task Chats, preserve README.md and Git metadata, and keep bookkeeping only in checkpoint/. No further delegates, detached/background tools, network work, installs, publication or other changes. Verify the final bytes and stop when complete.

Primary capture SHA256 `27fb4690ab29e5ffa3b76f3f55fee0622f701c6c3f9e4e41c92c9fc688102ed1`: records 17/22 load the installed route/runtime/lifecycle/principles; 32 reads version-matched orchestration; 46 creates the Run through normal escalation after a sandbox access denial; 51/56 initialize the goal/checkpoint and finite bounds; 61 creates first Task; 66 calls actual guarded start; 71 onward uses foreground inbox wait. Records 99/104 independently inspect first accepted settlement/artifact, settle and retain/ack; only then 113/118 create/start the second unit. Records 153/158 verify final bytes/baseline and second settlement/retention with no reclaimable worker left; 163 closes at revision 17; 172 is task_complete. No new user prompt occurred between these units.

Alpha worker capture SHA256 `cfe3d0c9df86707a3e94df03ad78dff1ccfbd1d98473f5acc084ef8acce69462`: actual entry/contract reads at 16/27, claim/proof work at 33/39, assigned next at 44, artifact at 49, finish at 59, worker_done at 70, task_complete at 79. Beta capture SHA256 `356488d4e13b25238ba34aecf518176fcb1d85cc89d3e12492c98ba9d747652b`: reads at 16/28, claim at 38/44, assigned next at 54, artifact at 59, finish at 65, worker_done at 71, task_complete at 80. Line numbers are one-based JSONL records. Raw transcripts, paths, tokens and runtime IDs stay local.

Independent worker audit confirmed exactly `616c7068610a626574610a` (**11 bytes**), frozen goal/requirements/authority/scope/owner unchanged, first completed operation/delivery and history prefix unchanged, and a first-start receipt snapshot captured before the second start unchanged afterward. All 25 initial Git file hashes, README and other baseline snapshot entries were preserved; only steps.txt and checkpoint/ changed. Both units settled, both task Chats retained, no new dispatch after verified closure. The original Chat and all fixture sessions remain retained. Coordinator separately audited the bounded native outcome.

**Recorded reporting deviation:** the primary's final prose and close-evidence text incorrectly say “10 bytes”; the actual full-content assertion and independent byte count establish 11. Raw evidence is preserved, not silently corrected. This does not change the exact-artifact or settlement-order verdict, and is not a claim of error-free agent reporting.

Runtime hashes used in this native run: supervision.py `72ab4cb99e1da8204e38b31cf63a10c40a40222e14c8168d8eebea62def1a80d`; continuation.py `5be540ca6169b46c7b266c54aec8347c0ea37d49da024d0a641cb966292222b2`; task_event.py `d99494799575b953dba11d146f8726eb74fae6af1accfad5fdb3ad7ac4fe665b`. No runtime changes followed that run. The final docs/checks do not upgrade source inventory or promise progression while the supervising Chat/app is stopped.
