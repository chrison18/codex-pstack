# Swarm: parallel work and one accountable report

Use within explicitly active Poteto mode for partitioned coverage, races or mixed parallel work. The primary owns the checklist: frame → fan out → aggregate → report. Read the [runtime contract](runtime.md) and applicable [principles](principles.md). A delegate owns one slice, never this workflow or recursive fan-out.

## Frame

State the done predicate, required slices and delivered artifact/report. Choose partitioned coverage, identical-brief race or a mixed shape. For any race, declare `first pass`, `rank all` or `best-of` before spawning. Define how a passing result will be checked and the scoring/tie-break policy before seeing results. `first pass` selects the earliest completed eligible result after independent validation, not the earliest self-reported PASS; drain later workers without changing that winner. `rank all` waits for all results and returns an ordered eligible set. `best-of` waits for all results and selects one against the declared rubric. Keep invalid arms and ties visible.

Resolve every worker with `python3 <entry-dir>/scripts/runtime.py resolve PROJECT swarm-worker --parent-model MODEL --parent-effort EFFORT [--model MODEL --effort EFFORT] [--catalog PATH]`. Validate all settings before spawning. Each race arm may have a different explicit pair. Task choices override saved `swarm-worker`, then the actual observed parent pair. Do not guess foreign vendor aliases or silently replace rejected settings. Swarm can have one or more workers; a review panel's minimum-two constraint does not apply.

For each writing worker, prepare a distinct Git worktree and branch from the explicitly named starting ref. Resolve and record the exact base SHA before any writes. When a non-default pushed branch is requested, fetch/resolve it and prepare each worktree at that ref, then have each worker verify its branch, HEAD and required base contents before editing. If preparation/check-out is not permitted, stop that slice before writes. A spawn or a directory name alone does not create a worktree. Do not let workers reset a shared checkout, reuse an occupied worktree or fall back to the remote default branch.

Every brief stands alone: goal, scope/slice or race arm, entry path, absolute worktree/output path, branch/base SHA, exact verification SHAs, permitted commands/execution timing, write owner, local-state requirements, resolved settings and required evidence. A measurement brief additionally fixes sample count, sample definition and execution order; the result must record both refs and method. Do not allow delegate execution that the user reserves for the primary or a later phase.

## Fan out

Use registered `poteto-agent` with the resolved model and reasoning effort through the actual native schema. Start independent workers without waiting for each prior result, then drain all started workers. Keep one writer per worktree. The primary does not edit a live worker's files, and workers do not write the parent checkout, Git metadata/configuration, another worker's output, or shared integration files. Separate artifact directories suffice for non-code outputs; repository code writes require real worktrees. These ownership instructions do not establish separate OS sandboxes.

For a verifier needing the user's own checkout or machine state (local service, browser session, credential or simulator), explicitly assign the minimum required shared access instead of pretending an isolated worktree contains it. Prefer read-only access, exact paths/processes and permitted probe commands. Do not copy credentials/session data into worker worktrees, commit them, or broaden access silently. First prove the required dependency is reachable in that context; otherwise report BLOCKED. An unrelated isolated test or spawn is not proof of local-state access. A shared verifier must not become a concurrent shared-checkout writer.

Workers report `PASS`, `ISSUES` or `BLOCKED`, with branch/base/verified SHAs, commands and observed outputs, changed paths and remaining limits. A proved defect is ISSUES; include every proved issue rather than stopping the report at the first. No output or unsupported success claims are gaps, not passes. Preserve a dropped-out worker in the checklist.

## Aggregate

Inspect every terminal result and its actual evidence. If a result omits named SHAs, the specified measurement method or reproducible command evidence (including unresolved placeholders), discard it and ask that worker once to repeat the missing evidence; after a second miss, record a gap. Do not fill missing evidence from the primary's knowledge or an unpublished proposal. Coverage requires a valid result for every required slice. N−1 may be useful progress but does not satisfy missing required coverage. Apply the predeclared rule for races; never equate fastest response with a verified pass.

After every writer finishes, inspect actual per-worktree diffs against the named base and integrate the accepted changes into the designated integration checkout under one primary writer. Keep unrelated default-branch or user-local changes out. Resolve conflicts deliberately and rerun the combined verification there; individually passing slices do not prove integration. Drain remaining race workers before cleanup. Do not remove dirty/active/uncertain worktrees or rewrite history as a side effect; cleanup authorization and lifecycle evidence remain separate.

## Report

Return one consolidated in-chat table of slices/arms, refs, status and verification, with issue one-liners, integration result, gaps/dropouts and the declared race rule where applicable. Distinguish isolated code results from shared local-state observations. Do not paste raw worker dumps or claim browser/UI/auth parity from a fixture that only exercised a local process. Report missing capabilities before declaring completion; commits, external messages, PRs and merges still require their own task authorization.
