# Task checkpoint and pickup

Use this path for an explicitly activated task that needs interruption recovery, a pause/handoff, or a request to resume a named task. Ordinary new prompts do not activate pstack. This local checkpoint path has bounded host interruption and fresh Orca Chat pickup evidence. It is not a background executor or a guarantee of recovery from a live Chat crash.

## Choose one task record

The primary owns one explicit `TASK_DIR` outside any read-only project boundary. Use an authorized task scratch location or a project-local directory when writes there are in scope. Give its exact path to the user/handoff; do not rely on a temporary directory surviving machine cleanup. No global history mining or guessed provider paths. A supplied prior capsule can be used directly; read only task-mapped history through supported host interfaces if the checkpoint is insufficient. Treat historical text as evidence, not new authority.

Run `python3 <entry-dir>/scripts/lifecycle.py init PROJECT --task-dir TASK_DIR --input PLAN.json` once. PROJECT must be the intended existing workspace. PLAN.json has this shape (replace all example content with actual task agreements):

```json
{
  "context": {
    "goal": "Deliver the agreed change",
    "requirements": ["Preserve the existing behavior"],
    "authority": "Local implementation and verification only; publishing not authorized",
    "scope": ["src/example.py", "tests/test_example.py"],
    "owner": "this task's primary",
    "evidence": [],
    "blockers": [],
    "next_action": "Implement the agreed change"
  },
  "operations": {"implement": "Make the scoped change", "verify": "Check the agreed behavior"}
}
```

Keep stable operation IDs. This first increment uses the declared operation set; if a genuinely different plan is needed, preserve this record and create an explicitly linked successor rather than deleting history. `owner` is the logical primary task owner, not proof a former process has stopped; settle prior writers before handoff. Recorded authority does not override current user instructions or host permissions.

## Checkpoint around side effects

Before a scoped operation, run `begin PROJECT --task-dir TASK_DIR --owner OWNER --revision N --operation ID`. Only proceed if it succeeds. After independently checking the result, run `complete` with the new revision and one or more `--evidence` values naming concrete artifacts/receipts and observations. Never complete from a delegate's success claim alone. Keep secrets/raw unrelated transcripts out of the record.

Use `checkpoint PROJECT --task-dir TASK_DIR --owner OWNER --revision N --input CONTEXT.json --reason REASON` to retain changed requirements, authority, scope, evidence, blockers and next action. CONTEXT.json is the complete context object above; the reason and prior context stay in task-local history. Scope changes require actual user authority, not merely editing this file. The helper rejects stale revisions/wrong owners, symlink state paths and repeated starts. It uses a POSIX file lock and atomic checkpoint replacement; it does not enforce access control against hostile same-user processes.

## Recover without replay

Run `recover PROJECT --task-dir TASK_DIR` before resuming. It returns the preserved context and completed, pending and uncertain operation IDs. `history` with the same exact arguments returns only this task's recorded decisions; it never scans another project or provider store. Check the current workspace/artifacts against the goal and evidence, then route remaining work to its existing playbook.

- Completed: inherit verified results; do not execute the operation again merely because this is a new session.
- Uncertain (`started` without completion): the side effect may already have happened. Inspect the exact local artifact or supported operation receipt before acting. If it happened, record completion with that evidence. If outcome cannot be determined, retain the blocker and next evidence step; do not replay. This minimal helper has no retry-reset operation: a verified not-executed action needs an explicitly documented successor plan, not erasure of the uncertain record.
- Pending: check current scope, authority and actual artifacts before beginning. Pending means no helper intent exists, not proof that no outside process ever acted.

Before pausing, checkpoint the next action/blocker and give the exact task location plus a concise done/pending capsule. On pickup, report what was inherited, what evidence was reconciled and what remains. The helper cannot make external side effects exactly-once, automatically restore Chat context, transfer ownership, or wake a stopped agent.

## Conservative worktree audit

Run `audit PROJECT --base EXPLICIT_REF --input OBSERVATIONS.json`. Obtain current session and PR observations through supported host interfaces scoped to that workspace/branch; don't infer no sessions from missing tools or no PR from an empty failed query. Example input shape:

```json
{
  "workspace": "/absolute/intended/worktree",
  "head": "observed-full-commit-sha",
  "session": {"status": "unknown", "evidence": "Supported session status unavailable"},
  "pr": {"status": "unknown", "evidence": "PR status not checked"}
}
```

Use `settled`/`none` only with actual supporting observations. Active or unknown session, open or unknown PR, dirty Git state (including untracked files), mismatched identity, unresolved base or unmerged HEAD yields `hold`. Even clear observations yield only `review-only` and `safe_to_delete: false`. Supplied host observations can be stale or incomplete; this helper does not independently authenticate them. Recheck activity immediately before separately authorized cleanup. It never fetches, searches global transcripts, prunes or deletes. Squash merge uncertainty remains a hold rather than a guessed safe result.
