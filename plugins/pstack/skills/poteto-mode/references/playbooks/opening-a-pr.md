Internal reference within explicitly active Poteto. Follow [runtime](../runtime.md) and use the [workflow index](../workflow-index.md) for dependencies. Reference names are not additional native commands.

# Opening or updating a PR

Use at the delivery boundary only within the user's authorization. A playbook ending here is not automatic permission to commit, push, create a PR, mark it ready, merge, deploy or send external messages.

1. Inspect the actual branch, base and working state. Follow repository Git rules. Continue a suitable phase branch or create an authorized topic branch from the named latest base; never develop directly on main. Concurrent writers need distinct actual worktrees. Preserve unrelated WIP. Do not reset hard, discard work, rewrite shared history or rebase without authorization.
2. Inspect the full intended diff. Apply [Deslop](../skills/deslop.md) and [No comments](../skills/no-comments.md) within scope. Preserve protected comments and external constraints according to the reviewer rules; inspect the actual returned diff before accepting it. Fix accepted issues and run appropriate behavior/type/lint checks. Stage named owned files, never unrelated work.
3. Use focused conventional commit titles. Keep independent units reviewable; do not amend or force-push shared history as a cleanup shortcut. Write the title/body with [Technical writing](../skills/technical-writing.md) and [Unslop](../skills/unslop.md).
4. Use a sufficient connected repository tool first. If unavailable or insufficient, use an available forge CLI/API and explain the fallback. Verify repository, branch/base and actual PR identity before mutation. Update an existing task PR instead of creating a duplicate. Attach every created PR to the chat when the host has that capability.
5. Write a one-minute briefing: why, observable behavior, scope, material tradeoffs, blast radius and actual verification. Keep raw logs, exact refs and measurement methodology in linked evidence. Perf claims get one primary number with units and an evidence link. Attach screenshots/video only when they prove the claimed interaction.
6. Preserve the user's readiness preference. A requested draft stays draft; no default-ready conversion. Record the exact tested head and inspect that head's checks. A historical passing check is not proof for new code. Report pending/failed/missing checks accurately.
7. Hand back the PR URL and status. Opening a PR starts no autonomous babysit or merge loop. Separate user merge authorization is required even when CI/review pass. Phase 5 continuation/shipping is not implemented here.

For several dependent PRs, retain explicit bases and dependency order under the repository's rules. Do not silently replace a phase's requested single draft with a new stack.

Source: `skills/poteto-mode/playbooks/opening-a-pr.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex host adaptations and evidence are recorded in the migration ledger.
