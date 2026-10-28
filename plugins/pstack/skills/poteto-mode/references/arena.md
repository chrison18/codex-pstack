# Arena: independent candidates and synthesis

Within explicitly active Poteto mode, use Arena when requested or when the selected design workflow calls for it. The primary owns this checklist: frame → fan out → crossjudge → pick → graft → verify. Read the [runtime contract](runtime.md), applicable [principles](principles.md), and inspect the available native delegation schema.

## Frame

Give every runner the same task, constraints and grounding artifact. Define 3–6 gradeable criteria before fan-out; retain the picker rubric in the primary, rather than coaching runners to that rubric. Record the base commit and target before any writes. Persist and read back the shared grounding artifact before spawning any runner; a path to a file that will be written later is not grounding. When invoked by Architect, complete its [Ground dependency](architect.md#ground) before freezing this artifact or starting runners. Keep the picker rubric in the primary, separate from the common task grounding. Do not turn a request for alternatives into authorization to implement production code.

Resolve the entire pool with `python3 <entry-dir>/scripts/runtime.py resolve-panel PROJECT arena-runner --parent-model MODEL --parent-effort EFFORT [--selections JSON] [--catalog PATH]`. For Architect use `architect-runner` instead. The returned `reviewers` array contains runner settings (the shared panel field name is retained for compatibility). At least two independent runners are required. Explicit task pairs override the saved role, which overrides the observed parent pair. Without choices, two runners inherit the same resolved pair; report model diversity accurately. Do not translate inherited vendor aliases into guessed Codex models.

Resolve `arena-judge` with the singular `resolve` command before spawning. Prefer a different available model from the parent when the user's choices permit it; an explicit choice wins. Validate the pool and judge before starting any runner. Rejected model/role/tool support blocks this route; report it rather than silently replacing mandatory delegation.

## Fan out

Assign each runner a disjoint absolute output path and the shared grounding path, entry path, resolved model/effort, task and expected rationale including concrete alternatives and rejections. Use `poteto-agent` and the runtime contract's independent-start adapter: on the supported schema, `fork_turns: "none"` with resolved model/effort and a self-contained scoped brief. The delegate owns one candidate, never this entire workflow or recursive fan-out.

For repository code candidates, use separate Git worktrees with explicit base refs and one writer each. For non-code artifacts or design sketches, separate task-owned scratch directories are sufficient. A path in prose does not enforce a separate OS sandbox: inspect actual changes. Do not let candidates write shared files, parent checkout, configuration or each other's output. If required isolation cannot be established, stop before writes. The primary does not write a candidate's files while that runner is active.

Before each spawn, complete the runtime contract's brief fields with concrete absolute paths; do not send a shortened second-runner brief that assumes the first runner's context. Each runner must read the entry and existing grounding before creating candidate files, and report those reads. If a runner reports missing entry/grounding, treat that as a handoff defect, not successful execution of an intended negative-path scenario.

Start independent runners, then wait for every writer to finish before judging or integration. A runner without inspectable output is a dropout, not a vote. Record the dropout and proceed with N−1 only if that still satisfies the task; Architect requires at least two structurally distinct designs and must replace a dropout or stop when fewer remain. Never claim unreturned output as completed.

## Crossjudge and pick

After all writers finish, start one read-only judge using the same complete independent-start brief, including the absolute entry and grounding paths, plus the rubric and every completed candidate path. Require those reads before judging. It must not edit candidates, synthesize, implement or delegate. While it reads, the primary independently reads every candidate end to end and scores against the same criteria. Compare the judge recommendation to the primary assessment; resolve disagreement by inspecting the artifacts and rationale. For Architect, give the judge the [structural comparison contract](architect.md#structural-comparison); both judge and primary must apply it to actual candidate artifacts, including its bounded replacement/stop rule, before synthesis. Prefer a shape maintainers can extend through simple boundaries when scores tie.

## Graft and verify

Choose a base and adapt the best one or two compatible parts of other candidates into one coherent artifact. Record each graft's source and each meaningful rejection. Do not force a graft when candidates converge; explain convergence. Wildly incompatible candidates may indicate an underspecified task: reframe and rerun instead of averaging incompatible designs.

Only the primary integrates after writers and judge complete. Preserve candidates as evidence. Verify the synthesized artifact itself with the task's relevant checks; candidate tests or judge assurances do not prove the synthesis. If verification finds a problem, revisit Frame when the contract was wrong or Graft when a candidate already covered it; do not patch around the missing design reasoning. Inspect final diff, scope and checklist. Report the delivered artifact, base and reason, judge agreement/disagreement, grafts/rejections, diversity/dropouts and actual verification. Keep implementation, configuration, commits and external writes within the user's authorization.
