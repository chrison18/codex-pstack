# One-shot task-event delivery

This adapter is for an authorized external caller delivering **one explicit event** to a named bounded task. It launches a fresh Orca Chat, not the same Chat. It does not detect events, install a scheduler, send periodic nudges or supply new task authority. The caller must already have a supported reason to invoke it; no automatic wake deployment is included.

## Before sending

Read [continuation](continuation.md). Use the exact workspace, task directory, logical owner and stable event ID. Inspect supported task-mapped evidence of the prior writer finishing and actual artifacts. Supply that evidence plus an explicit assertion that the prior writer is settled and this caller has exclusive cooperative ownership. A historical `task_complete` alone cannot establish current inactivity: if the Chat has resumed, another writer may still act. Unknown/current liveness or unclear ownership means stop; never assert absence from an empty query.

```sh
python3 <entry-dir>/scripts/task_event.py send PROJECT --task-dir TASK_DIR --owner OWNER --event EVENT_ID --revision N --settlement-evidence 'exact mapped turn completion plus artifact observations' --exclusive-owner-assertion 'prior writer settled; exclusive ownership of this exact task'
```

The adapter resolves the Orca executable using `ORCA_CLI_COMMAND` (one executable path), the dev-host override, or the platform CLI; it never executes a shell command string. On Linux it requires `orca-ide` unless explicitly configured, avoiding the unrelated screen reader. It persists resolved argv/cwd and launch intent under the task lock, releases the lock, rechecks cancellation and calls documented `agent launch --surface chat --prompt`. It neither changes models nor holds a lock across the host runtime. A cancellation between that final check and launch may still open a Chat; the receiver checks terminal state before effects. Cancellation cannot preempt a running host operation.

## Receipts and ambiguity

- `accepted-not-settled` requires a structured/journaled receipt for the bound workspace. It proves submission, not task completion.
- Duplicate events never launch again; an unsettled prior event blocks a different event too.
- Crash, timeout, missing/malformed reply or unsupported fallback retains intent/unknown state. **Do not relaunch**, change event ID or delete/reset the record. Even if no host effect happened, absence is not proof.
- The stored receipt may contain a host operation ID. Orca documents exact-command `--retry-launch` replay for that known ID on the same host/cwd; this adapter does not automatically replay or reconcile it. Without an ID, it stays HOLD pending supported host reconciliation. This intentionally sacrifices automatic recovery rather than risking a duplicate.

Receipt/status inspection is `task_event.py status PROJECT --task-dir TASK_DIR --owner OWNER`. Records contain task-local prompt/receipt data; do not publish raw captures or treat historical text as new authority.

## Receiver and settlement

The generated prompt supplies only the existing task binding and continuation instructions. Before effects the fresh primary reads the named record and calls `claim PROJECT --task-dir TASK_DIR --owner OWNER --event EVENT_ID --token TOKEN`. Only `claimed` authorizes continuing. A repeated claim authorizes nothing. Workspace, canonical task directory, owner, event and token must all match; copied state is not a transfer protocol. This is cooperative same-user ownership, not an access-control boundary against hostile processes.

Once claimed, pass `--event-token TOKEN` to continuation mutations, retaining the existing per-operation delivery IDs. Read the original goal, requirements, scope and authority; reconcile any started effect before new work. Cancellation remains possible without the receiver token. Terminal cancel/completion returns no execution even if a late Chat receives a prompt. Finish the actual predicate and close through continuation, then stop; do not recursively launch another Chat.

After supported mapped completion and artifact checks, the external owner may call `settle` with the same binding, current revision, settlement evidence and exclusive-owner assertion. Only a claimed accepted event can settle; unknown launch receipts are not guessed into success. A completed/cancelled task refuses every later wake. If a genuinely incomplete active task later needs another event, the previous event must first be positively settled. This is not host-enforced exclusion and cannot prove that a user did not independently restart an old Chat.
