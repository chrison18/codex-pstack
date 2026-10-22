# Phase 2 core workflow

Status: candidate implementation committed; CLI artifact and native role observations are recorded in [the evidence report](phase-2-core-evidence.md). Acceptance remains incomplete. Branch `feat/codex-core-workflow` starts at phase 1 squash merge `c303a74e4e5e6f7e9f055b5eed49507bc59ddfbd`. The branch packages a 0.2.0-alpha.1 development candidate; main remains the accepted phase 1 entry preview until phase 2 passes its gates.

## Source mapping

Use the inherited files at this branch's base as the migration source. Their upstream lineage remains the pstack 0.15.29 pin recorded in [UPSTREAM.md](../../UPSTREAM.md). Keep substantive workflow advice and adapt host mechanisms explicitly.

| Source | Behavior to retain | Codex adaptation to implement and prove |
| --- | --- | --- |
| `skills/poteto-mode/SKILL.md` | Explicit per-task activation; primary owns routing, checklist, delegation, review and final answer | Package a router for Feature, Bug fix and Investigation; follow-ups continue the active task; ordinary new tasks remain inactive |
| `agents/poteto-agent.md` | Scoped delegate reads the exact parent-supplied entry and applicable principles | Verify native role registration and actual instruction loading; require explicit installed paths; report missing registration instead of silently using an unrelated role |
| `agents/comment-sicko.md` | Scoped comment review, evidence for exceptions, exact refactor targets, no application-code edits | Resolve packaged resources without Gemini paths; make review output distinct from any authorized edit pass; distinguish instructions from enforced tool restrictions |
| `skills/setup-pstack/SKILL.md` | Inspect current choices, show resolved role settings, validate before writing | Inspect available model identifiers and supported efforts; model and effort are separate; default to inheritance; no Gemini tiers or always-applied rule assumption |
| `skills/poteto-mode/playbooks/feature.md` | Data shape before logic; throughput checkpoint; delegated implementation with primary review; actual-surface verification | Define scoped writer handoff and result collection using capabilities available in the tested client |
| `skills/poteto-mode/playbooks/bug-fix.md` | Reproduce first; evidence-based cause; fix; same reproduction passes | Capture failing and passing output in a disposable fixture; retain failing-test-first history where appropriate |
| `skills/poteto-mode/playbooks/investigation.md` | Cited explanation or recommendation; read-only; no PR | Keep checklist outside the investigated repository when persistence is needed; snapshot tracked and untracked state before and after |

The original router depends on `how`, `architect`, principles and other leaf skills assigned to phase 3. Classify every dependency before packaging. Bring in a required portable dependency with a recorded reason, or explicitly limit that route until its dependency is migrated. Do not retain a mandatory instruction that points to an absent skill, silently skip it, or advertise the entire inherited catalog as supported.

## Implementation order

- [x] Probe native custom-role registration, loading and available model discovery in isolated Codex state. Record CLI version, desktop scope and actual errors. Plugin discovery alone does not establish role discovery.
- [x] Define one explicit runtime capability contract for routing, delegation, questions, persistent checklists and model resolution. Name unsupported mechanisms and their allowed fallback before changing the preview response.
- [x] Implement the three routed playbooks and their required portable dependencies. Keep implicit invocation disabled for the main entry and any setup entry.
- [x] Port both agent roles. Scope every delegate to named files, read/write responsibilities, success criteria and the primary's resource paths. Preserve one writer per worktree.
- [x] Implement setup without modifying unrelated settings. Keep task override, role override and inheritance distinct; validate the selected model and effort together; surface unsupported selections without silently substituting another model.
- [x] Add structural and regression checks for the expanded package, referenced resources, role/config parsing and safe setup/removal.
- [x] Run actual CLI/model tasks for each route and model-resolution case. Record resulting artifacts and tool activity with the tested implementation SHA.
- [x] Record owner-operated desktop Feature, follow-up, Bug fix, Investigation, ordinary-chat control and plugin removal; keep qualified UI discovery/version-display capture as an explicit phase 6 evidence limit.
- [x] Obtain independent review and green CI; the snapshot correction was independently verified. The owner now authorizes PR #3 merge conditional on one final review and green CI at the merge head.

## Acceptance contract

These are required observations, not recorded passes. Use PASS, FAIL, BLOCKED or NOT RUN in the eventual evidence report. A model saying that it loaded an agent is insufficient evidence.

| Gate | Test | Required evidence |
| --- | --- | --- |
| Activation | Ordinary task, explicit task through both entry names, then follow-up | Captured host loading and actual responses; new ordinary task excludes workflow; active follow-up retains the primary's checklist |
| Feature | Add a small behavior in a disposable repository | Correct route, named data shape, complete checklist, scoped delegation, reviewed diff and a passing behavior check |
| Bug fix | Repair a seeded defect | Same reproduction fails before the change and passes afterward; recorded cause matches execution evidence |
| Investigation | Explain a fixture subsystem and make a recommendation | Cited file/line findings; tracked and untracked repository state unchanged; no remote mutation |
| Roles | Spawn each registered role with scoped input | Actual role/instruction loading and relevant file reads; the delegate reports to the primary, which evaluates the result |
| Checklist | Complete, skip and fail individual steps | Completed and pending steps persist; skipped steps retain reasons; failure does not become completion |
| Models | Inherit, role override, task override, unavailable identifier, incompatible effort | Resolved model and effort observed in host events/configuration; precedence demonstrated; invalid choices produce an actionable limitation |
| Setup lifecycle | Configure twice, encounter occupied paths, remove setup artifacts | Repeatable behavior; existing user files survive; only owned artifacts are removed |
| Package | Clean install, discover, invoke and remove | Expanded inventory is intentional and self-contained; no machine-specific source path is shipped |

Inherited script checks and phase 1 negative activation checks remain required. CLI and desktop results are reported separately. When desktop automation is unavailable, owner-reported manual evidence is labeled as such, following the phase 1 record.

## Boundaries

Phase 2 does not claim parallel design panels, all 59 skills, session recovery, timers, recurring automation, autonomous runs or full release readiness. Those remain assigned to later phases. A task requiring an unavailable workflow receives a specific limitation; installation alone never enables the full workflow.

The candidate adds an explicit-only setup-pstack entry. Six portable principle summaries required by the bounded routes are included as one reference. Full routed skills remain phase 3 work, explicitly limited in the candidate. See the evidence report for failed first-run observations and gates that remain open.
