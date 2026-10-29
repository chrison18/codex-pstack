# Bounded continuation

Use for an explicitly activated task the user wants driven to completion without routine “continue” prompts. The primary owns the workflow; helper commands are internal bookkeeping, not commands the user must remember. Execute successive authorized steps in the active turn, checking results and keeping scope. Never infer permission to publish, merge, message others, install globally or schedule recurring work from continuation alone.

## Establish the run

Read [task checkpoint and pickup](session-lifecycle.md). Create one task record with ordered, independently verifiable operation IDs; include the actual goal, requirements, authority, scope and owner. Include verification/review as appropriate to the chosen playbook. Choose a finite operation budget sufficient for that declared work; it is a bound, not a request to stop early for another user nudge. A materially expanded plan requires a reconciled successor, not a silent budget/scope rewrite.

Before effects, enable continuation:

```sh
python3 <entry-dir>/scripts/continuation.py enable PROJECT --task-dir TASK_DIR --owner OWNER --revision N --grant 'actual user continuation authority' --predicate 'observable final done check' --limit COUNT
```

The helper freezes goal/requirements/authority/scope/owner and records the predicate/grant. It refuses unresolved started work on enable; first use the phase 4 evidence-reconciliation path. It never calls a model, shell task or network endpoint on its own. All commands below use this same script and explicit workspace/task/owner.

## Drive the active turn

1. Read `status`. Before each new side effect use `next ... --revision N --delivery STABLE_ID`. Use a unique ID for a genuinely new operation; preserve an external delivery's ID on retry. Only `execute-one` authorizes the returned operation. Persist its intent before touching the artifact. A duplicate response is **not** permission to execute the old receipt again.
2. Perform that scoped operation through the existing playbook/tools, then independently check it. Use `finish ... --revision N --delivery SAME_ID --evidence 'observed result/receipt'`. If a tool fails with an ambiguous effect, retain the started state and inspect actual evidence; don't mint a new ID to get around it.
3. Continue immediately to the next authorized operation while useful work remains. Answer status questions without abandoning the task. Use `checkpoint ... --input CONTEXT.json --reason REASON` to update evidence/blockers/next action while preserving the frozen contract. Missing capability, genuine scope/authority decision or budget exhaustion is a precise incomplete result, never success.
4. Once all operations are complete, independently test the frozen done predicate. Use `close ... --revision N --evidence 'actual final predicate check'`. No pending rows alone is not evidence of success. Completed runs refuse all future work deliveries. Report actual work, verification, remaining limits and the checkpoint location, then stop.

These commands also require `PROJECT --task-dir TASK_DIR --owner OWNER`. Revisions come from the latest successful response/status. The helper validates evidence presence, not its truth; the primary must inspect real artifacts/tool results. Phase 4 mutation commands refuse continuation-owned records so they cannot reset cancellation/completion. Do not edit the JSON manually to bypass these controls.

## Cancel and restart

An explicit cancellation uses `cancel ... --revision N --reason REASON`. Cancellation is terminal. Check run status before further tool effects; already-running external tools may still settle, so cancellation is cooperative, not process preemption. Do not issue later work or claim cancelled in-flight effects complete. Preserve and report the started operation and any actual side effect; inspect it read-only if needed. A later user request needs an explicitly reconciled successor task, never resetting this record.

On restart, first ensure the previous writer is settled through available supported host evidence. Read `status` and the named phase 4 record. Duplicate delivery IDs authorize nothing; a different ID cannot skip a started operation. Reconcile that operation by reading its actual artifact/receipt and use `finish` with its original ID only if the active run's effect is proven. Otherwise keep the blocker or, after proving no effect and settling the prior writer, create an evidence-linked successor as described in phase 4. Never treat missing completion as permission to replay.

## Delivery and host boundary

`next` is a synchronous local delivery receiver, usable from a fresh process with a stable event ID. Its durable deduplication, restart and terminal checks are tested independently of Chat. It does not schedule or launch a session. In-turn persistence is supported by the agent applying this workflow; a separate system must actually wake an idle agent before it can process an external event.

Orca documents `agent launch --surface chat --prompt ...` for a one-shot fresh Chat and `--retry-launch` for an ambiguous operation receipt. That alone is **not** a verified unattended continuation adapter, same-Chat sender or recurring scheduler. No such automatic wake integration is installed or claimed here. When a supported authorized host delivers a task event, the receiving primary must process the stable ID through this receiver; otherwise report the unavailable wake boundary instead of inventing an endpoint or running a background “continue” loop.

Inherited babysit/autopilot/shipping/program/Benny/bot UI workflows have further forge, merge, scheduler, messaging and credential dependencies. Reuse the active task's authorized local work and verification where applicable, but do not claim those integrations from this bounded controller or invoke Antigravity APIs. Shipping still requires its own authorization, and review/CI must describe the actual current head. No external messages, recurring timers or background loops are created by this reference.
