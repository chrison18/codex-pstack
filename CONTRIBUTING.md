# Contributing

This fork is migrating to Codex-only support. Read the [migration plan](docs/migration/codex-migration-plan.md) and [upstream ledger](UPSTREAM.md) before changing runtime behavior. The inherited runtime still targets Antigravity until the relevant migration phases pass acceptance.

## Branch and PR workflow

1. Fetch `origin` and start each phase from the latest `origin/main`. Do not develop directly on `main`.
2. Use one branch and one PR per migration phase. Wait for the preceding phase to merge before starting its dependent phase. Split unrelated defects into `fix/<topic>` branches and upstream updates into `sync/<topic>` branches.
3. Use the phase branch names in the migration plan. Other topic branches use `docs/`, `feat/`, `fix/`, `test/`, or `chore/`.
4. Keep commits focused, with subjects prefixed by `docs:`, `feat:`, `fix:`, `test:`, or `chore:`. Separate upstream synchronization from Codex adaptations.
5. Run relevant checks and attach observed results to the PR. A historical passing result is not evidence for the current head.
6. Describe the problem, resulting behavior, scope, verification, and limitations. Link the migration phase and upstream commits where applicable.
7. Merge only after required checks pass, findings are resolved, and the repository owner explicitly approves merging. Use squash merge by default. Opening a PR does not authorize merging it.
8. Fetch merged `main` before creating the next phase branch. Delete merged branches only after their work is retained and no active task uses them.

## Parallel work and history

- Give concurrent writers separate worktrees and branches. Name the starting ref and directory in each brief. A subagent spawn alone does not establish isolation.
- Keep one writer per worktree. Arrange local-state access separately for browsers, credentials, simulators, transcripts, and running processes.
- Do not force-push shared branches or rewrite inherited history. Merge base updates into shared branches; coordinate exceptions with the owner.
- Do not commit credentials, private transcripts, dependency caches, or generated fixtures. Keep validation workspaces disposable.
- Preserve upstream attribution and license notices. Record source SHAs, adopted/skipped changes, and host adaptations in `UPSTREAM.md`.

## Verification

Run from `skills/poteto-mode/scripts`:

```sh
bun install --frozen-lockfile
bun run typecheck
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false bun run test
```

The Git override applies only to test subprocesses, which create disposable commits. It does not change repository or user configuration.

Run from the repository root:

```sh
bash -n skills/poteto-mode/scripts/worktree-audit.sh
bash -n skills/show-me-your-work/scripts/log.sh
git diff --check
```

Runtime changes also require proof in the supported Codex client. Record client version, prompt, expected behavior, actual behavior, and evidence. Mark unavailable checks BLOCKED or NOT RUN with a reason; never count them as passes. The inherited Antigravity CI remains during phase 0 and does not validate Codex behavior.
