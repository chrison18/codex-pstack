# Codex migration plan

Status: phases 0 through 2 merged in PR #1, PR #2 and PR #3. Phase 3 is split into consecutive increments: 3A on `feat/codex-skill-workflows` (PR #4, inventory/principles/local research) and 3B on `feat/codex-remaining-workflows` (remaining skills and parallel-workflow gates). The owner requested independent review and merge of PR #4 before continuing. This split does not mark phase 3 complete or waive its remaining gates; see the [phase 3 work plan](phase-3-skill-workflows.md). The phase 2 qualified desktop discovery/version-display evidence limit remains assigned to the phase 6 release walkthrough.

## Outcome and scope

Deliver a Codex-only pstack port for desktop and CLI. Preserve its principles, roles, and playbook outcomes while adapting host behavior. Keep `$poteto-mode` explicitly invoked for each new task. Ordinary prompts must not activate the full workflow. Follow-ups within an active task continue that task without repeating the invocation.

Keep persistent repository agreements and configuration separate from the skill's full workflow. Installing the package or adding `AGENTS.md` must not implicitly enable poteto-mode. Once explicitly invoked, its instructions may authorize subagents required by the selected workflow.

Start at `a06537a883278a63132e2518971166002f3de5de`, with pstack 0.15.29 and cursor-team-kit 1.2.0. See [provenance](../../UPSTREAM.md) and [Git rules](../../CONTRIBUTING.md). Preserve the baseline inventory unless a reviewed change explains a removal or replacement.

Core availability requires phases 1 through 4. Full migration requires phases 5 and 6. Unsupported capabilities must be marked. Cursor/Antigravity compatibility, cloud parity, and unrelated upstream upgrades are outside scope.

## Capability mapping

Target mechanisms are proposals until verified against the selected client version. Do not treat a tool visible in one desktop session as a universal Codex API.

| Surface | Inherited dependency | Codex work and proof | Phase |
| --- | --- | --- | --- |
| Distribution | agy manifest/installer | Codex package; clean install, discovery, update, removal | 1, 6 |
| Invocation | Slash commands, frontmatter | Explicit `$poteto-mode`; positive and negative invocation tests | 1 |
| Custom agents | Markdown agents, agy tool lists | Verify distribution/registration for both roles and actual instruction/tool loading | 2 |
| Delegation | `invoke_subagent`, agent messages | Supported spawn, follow-up, wait, result collection; primary ownership | 2, 3 |
| Models | agy tiers and inherit | Detect models; separate model/effort; test configuration precedence | 2 |
| Guidance | Gemini rules, agy-customizations | Minimal `AGENTS.md`, explicit configuration loading, supported skill authoring | 2, 3 |
| Questions/checklists | ask_question, brain task.md | Supported mechanisms or documented fallback; preserve skipped-step reasons | 2 |
| Workspaces | branch/share | Explicit worktree, branch, base ref, one writer; local-state exception | 3 |
| UI/CLI proof | Control skills, agy visuals | Reuse available harnesses; real interactions; report missing dependencies | 3 |
| History/recovery | Gemini JSONL paths | Prefer supported session interfaces; scope file fallbacks; safe recovery/cleanup | 4 |
| Timers/long work | schedule, goal | Separate in-session work, later wakes, recurring jobs; cancellation/completion | 5 |
| External wake | agy agentapi, sidecars, Benny | Supported automation/bot interface; idempotent wake handling | 5 |
| Validation | agy CI | Codex structural checks and client behavior evidence; retain script checks | 1 through 6 |

## Phases and branches

Each listed increment uses one branch and PR from latest merged `main`. Wait for its dependency to merge. Phase 3 is explicitly split below so the verified foundation can land while its remaining capability gates stay visible. Update this plan before any further split; phases 4–6 still depend on completion of phase 3B.

| Phase | Branch | Deliverables | Exit gate |
| --- | --- | --- | --- |
| 0 | `docs/codex-migration-plan` | Plan, Git rules, upstream ledger, baseline | Inventory/ownership documented; checks run; failures and unavailable checks distinguished |
| 1 | `feat/codex-plugin-entry` | Package, invocation policy, minimal setup, structural CI | Clean install/discovery/removal in both clients; explicit invocation works; ordinary prompts do not activate; no developer-machine paths |
| 2 | `feat/codex-core-workflow` | Router, both agents, checklist, model setup; Feature/Bug fix/Investigation | One real task of each kind completes; roles load correct instructions; model/effort rules hold; primary owns workflow |
| 3A | `feat/codex-skill-workflows` | Complete source inventory, full principles, How/Why local research | Source/provenance and explicit invocation guards; representative principles and local research checks; independent review and CI; live-source and remaining-skill gaps explicit |
| 3B | `feat/codex-remaining-workflows` | Remaining core skills, design/review/delegation, expanded playbooks and parallel workflows | Original phase 3 exit gate: every skill classified and structurally checked; changed host mechanisms exercised; isolated writers, base refs and local-state verification work; unavailable live-source coverage explicitly limited |
| 4 | `feat/codex-session-lifecycle` | Recall, pickup, history mining, decision trail, worktree audit | Interrupted task resumes from evidence; scoped history; active/dirty/uncertain worktrees not declared safe |
| 5 | `feat/codex-autonomous-workflows` | Autonomous run, babysit, orchestrate, autopilot, Benny, bot UI | Continuation, wake, cancel, restart, completion, duplicate delivery tested; missing dependencies reported |
| 6 | `chore/codex-release-readiness` | Final docs/CI, client matrix, install/update/remove instructions | Clean walkthrough; all release claims have evidence; supported versions and limits explicit |

Phase 1 proves discovery and activation before runtime migration. Do not advertise an executable core workflow until phase 2 passes. During staged migration expose only verified workflows as supported and identify pending ones; packaging must not imply pending workflows are fully supported.

Phase 1 uses `plugins/pstack/` as the Codex package root and retains inherited source outside that package. Codex CLI 0.163.0-alpha.10.2 exposes the plugin entry as `$pstack:poteto-mode`; a native project skill link supplies the agreed `$poteto-mode` short entry. Both paths have implicit invocation disabled. Installation does not create that project link automatically. See the [entry evidence](phase-1-entry-evidence.md) for the verified scope, including owner-reported desktop acceptance.

## Inventory ownership

Baseline inventory is 59 top-level skills, 2 agent definitions, 23 playbooks, plus 3 Benny skills. Phase 1 owns package/invocation metadata across the inventory. Phase 2 owns both agents, setup-pstack, poteto-mode, and its three initial playbooks. Phase 3 (3A plus 3B; inventory `ownerPhase: 3` remains unchanged) owns all remaining top-level skills' portable content and host dependencies, with these runtime overlays assigned later:

- Phase 4 owns recall, history-reading portions of automate-me/reflect, show-me-your-work, session-pickup, pause-safely, trace/runtime forensics, and worktree-cleanup.
- Phase 5 owns autonomous-run, babysit, orchestrate, autopilot-full/stack, shipping continuation, make-bot-ui, and `automations/benny/`.
- Phase 6 reconciles all entries, help pages, examples, and support claims. Each entry must be supported with evidence, explicitly limited, or removed with an approved reason.

Keep portable principles and scripts aligned with upstream. Adapt host assumptions rather than rewriting substantive workflow advice.

## Acceptance scenarios

Run applicable scenarios in desktop and CLI separately. Unsupported results block claiming parity or full support for that capability.

| ID | Scenario | Required observation |
| --- | --- | --- |
| A1 | Ordinary feature/bug prompt | poteto-mode instructions are not automatically loaded; full workflow does not activate |
| A2 | Explicit feature and follow-up | Correct playbook, checklist, implementation, verification, report; follow-up retains task ownership |
| A3 | Bug fix | Reproduction fails before fix; same behavior passes afterward |
| A4 | Read-only investigation | Cited findings; no tracked/untracked repository or remote mutation |
| A5 | Both agent roles | Correct instructions/skills actually read; tool access demonstrated; primary checks work |
| A6 | Models | Observe inheritance, role override, explicit override, unavailable model, compatible effort and resolved settings |
| A7 | Concurrent writers | Separate worktrees/branches; results integrate without shared-file interference |
| A8 | Non-default base | Worker starts at named ref without unrelated default-branch changes |
| A9 | Local-state proof | Verifier can access required local process/browser/auth; spawn alone is not isolation proof |
| A10 | Interrupt/recover and history | Restore completed/pending work without duplicate operations; unrelated projects remain outside scope |
| A11 | Worktree audit | Active session, tracked WIP, open PR, or uncertain session state prevent automatic safe classification |
| A12 | Autonomous task/timer | Wake, cancellation, restart, duplicate delivery, completion work; completed task stops |
| A13 | Missing dependency | Actionable limitation; no invented tool, model, path, or successful result |
| A14 | Install/update/remove | Disposable-config walkthrough; correct inventory/version; unrelated user configuration survives |

## Evidence and checks

Each PR records tested Git SHA, platform, client/runtime versions, commands/prompts, expected/observed behavior, and evidence. Use PASS, FAIL, BLOCKED, or NOT RUN. Static validation and model self-report alone cannot pass behavior scenarios. Capture tool activity, actual files/diffs, assertions, or UI proof as applicable without committing private transcripts.

Run [script checks](../../CONTRIBUTING.md#verification) for affected code/dependencies. Keep manifest/frontmatter parsing, reference resolution, principle/playbook inventory checks in CI. Add tests for meaningful changed behavior. The existing multi-phase-plan checker validates a different autonomous-program artifact contract; do not apply it to this migration document.

Inherited Antigravity CI stays unchanged in phase 0. Phase 1 adds Codex packaging checks; phase 6 removes obsolete host checks. Authenticated checks unavailable in CI require explicit local evidence and must never appear as a CI pass.

See the [initial baseline](baseline-2026-10-21.md). Review and owner approval are required before merge. This plan does not authorize deployment, automatic merging, or activation of recurring jobs.
