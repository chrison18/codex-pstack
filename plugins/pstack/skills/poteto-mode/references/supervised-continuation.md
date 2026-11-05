# Foreground supervised completion

Use only when the user explicitly asks for supervised continuation/agents to drive one bounded task. Ordinary poteto-mode remains unchanged. Example: `$poteto-mode Complete this task with supervised continuation: …` The user supplies the goal and restrictions, not internal IDs or helper commands. Explain briefly that the original Chat will supervise sequential workers, additional model usage is incurred, and progress needs this coordinator to stay active. Choose and state conservative finite dispatch and elapsed-time limits appropriate to the task; these are not a hard monetary cap. Do not silently override models/settings.

Read [continuation](continuation.md) and the current host's Orca orchestration skill (`orca skills get orchestration`, using that skill's executable-resolution rules). This is a foreground event-driven workflow, not a scheduler. A Run does not wake a stopped coordinator. Do not install automation, periodic prompts or background loops.

## Establish one owner

The primary owns the goal, checklist, verification and final answer; while a worker owns task effects the primary does not edit those files. Initialize the named lifecycle record and enable continuation with ordered verifiable units and a frozen predicate/grant. Require no detached tools or further delegates in this bounded mode; if the selected playbook needs them, stop and reconcile that execution scope rather than silently dropping required review. Retain the applicable installed entry, runtime, playbook and principles in every worker brief. Never read broad provider history.

Create a dedicated Run through `orca orchestration run-create --objective ... --json` and record its returned identity; do not adopt another coordinator's Run. A dispatched worker cannot bind its ancestor Run as coordinator: report that boundary, rather than bypass nesting rules. Then enable the task guard:

```sh
python3 <entry>/scripts/supervision.py enable PROJECT --task-dir TASK --owner OWNER --revision N --run-id RUN --limit MAX_DISPATCHES --seconds MAX_ELAPSED
```

Only one delivery mode can own a task; do not combine this with task-event launches. These identifiers and commands are agent bookkeeping. Cooperative same-user ownership is not isolation against hostile processes or independent user edits.

## Dispatch one unit

1. Inspect status and the first pending operation. Create one Orca Task using documented `task-create --spec ... --json`, retaining its exact returned ID. The self-contained spec includes the operation, workspace, task directory, logical owner, installed entry path, full frozen goal/requirements/authority/scope, verification, and no additional writes/delegation/background work. Tell the worker to read the latest `supervision.py status`, select the unit whose `task_id` matches **its live preamble**, obtain that unit's token/delivery/operation, verify the assignment, and claim before effects. Thus the spec is complete before `start` generates the token; no invented task-update API is needed.
2. Call `supervision.py start PROJECT --task-dir TASK --owner OWNER --revision N --task-id ORCA_TASK`. It persists intent and exact command, then invokes documented `worker-start` in the bound Run/workspace. Only this helper starts the unit. Pass `--model` and `--effort` only for an explicit user selection; otherwise omit and inspect host effective settings. A malformed/lost reply, interruption or duplicate never authorizes another fresh start. Preserve the returned host receipt; `start-returned-not-settled` is not success.
3. The worker uses its live preamble and `orca orchestration worker-show --dispatch EXACT --json` to save actual host proof in the authorized task record directory. It runs `supervision.py claim ... --task-id ORCA_TASK --token TOKEN --input PROOF.json --revision N`. Only `claimed` permits work; duplicate/terminal/deadline results stop. The helper validates the exact Run/Task/Dispatch/workspace. Supplied proof must come from the supported host, not authored JSON.
4. The worker uses `continuation.py next/finish/checkpoint` with `--writer-token TOKEN` and the unit's fixed delivery. It may perform only the assigned operation; it cannot issue the next unit or close the overall task. Verify real effects, finish the operation and send `worker_done` with the live lifecycle IDs and truthful outcome. It then stops. Failure or uncertainty must be reported, never converted into a fabricated completion.

## Advance on accepted settlement

The primary remains in the foreground with documented `check --wait --types worker_done,escalation,question --timeout-ms ...`. Bound waits by remaining elapsed time; process the whole FIFO batch and answer genuine questions. A timeout/empty inbox is not settlement. Validate the expected live Task/Dispatch, obtain fresh `worker-show` output and independently inspect the unit's artifacts/checkpoint and any outstanding resources.

Use `supervision.py settle ... --task-id ORCA_TASK --revision N --input PROOF.json --evidence 'actual artifact and resource reconciliation'`. It requires accepted successful dispatch settlement and the exact completed operation receipt. Missing/failed/unknown/unclaimed state holds. Evidence presence is checked by code; its truth is the primary's responsibility. Accepted settlement is cooperative ownership transfer, not an OS process-exit guarantee. If an old worker was restarted or any background resource is uncertain, do not advance.

Choose supported retention/release for the settled worker before acknowledging the batch. Preserve original and test Chats when retention is required; never substitute terminal close for lifecycle cleanup. The current minimal helper uses a fresh worker for each next unit. After a successful settle, immediately dispatch the next authorized pending unit within the fixed limits—do not ask the user to say continue. Duplicate inbox delivery/settlement cannot reset unit receipts. When no work remains, independently verify the frozen predicate and use continuation `close`; there can be no unsettled worker. Report actual evidence and stop.

## Cancellation, bounds and restart

Cancellation uses continuation `cancel` without a writer token and is terminal. No later start/claim/effect issuance is permitted. A launch already in flight may still create a worker, which must check cancellation; an already-running effect may still settle. Observe it honestly, use only the supported separately authorized host stop/recovery contract, and never classify uncertain work safe. The helper does not kill workers or delete files.

Dispatch-count or elapsed-time exhaustion prevents new starts/effect issuance. It does not pretend to stop an already-running tool or cap its bill. Preserve active ownership and report incomplete work. Unknown start outcomes keep durable intent; a different Task ID cannot evade that hold. For a known host request ID, use documented `request-show` and exact `--retry-request` reconciliation only after inspecting its receipt; the helper never automatically replays. No ID/uncertain effects means HOLD.

After coordinator restart, explicitly `run-use` the recorded own Run, read this task and inspect exact host Task/Dispatch/request receipts before doing anything. A positively identified intended worker may claim using its live preamble; an accepted successful claim/operation/settlement can be reconciled. Never infer settlement from a historical transcript, missing output or a dead parent while descendants are unknown. No automatic coordinator restart, shutdown wake, same-Chat continuity or external exactly-once execution is promised.
