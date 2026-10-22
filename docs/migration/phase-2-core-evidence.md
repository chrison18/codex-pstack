# Phase 2 core candidate evidence

Status: CLI checks, native role probes, independent review, and desktop routed-task observations are recorded. Desktop plugin removal and the complete install/discovery lifecycle still need confirmation. Phase 2 remains unaccepted; keep PR #3 draft and do not merge.

## Candidate and source

Implementation commit: `a306053942f45fd97abc7d7b1fabacf5f2d46a71`; package `0.2.0-alpha.1`. Client: `codex-cli 0.163.0-alpha.11.1`, macOS arm64. Toolchain: Bun 1.4.3, Python 3.9, existing locked TypeScript toolchain. Documentation updates after the implementation do not establish new runtime passes.

The three bounded routes adapt the inherited Feature, Bug fix and Investigation playbooks. The portable principle reference draws from Model the Domain, Prove It Works, Test Behavior Not Implementation, Sequence Verifiable Units, Separate Before Serializing Shared State, and Laziness Protocol. The original source remains outside the distributable package. Full `how`, `why`, `architect`, `arena`, `interrogate` and the remaining leaf skills stay in phase 3; the candidate states these limits and uses direct call-path/history/design work rather than claiming those skills ran.

Native behavior is grounded in the [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) and tested against the installed client. Project `.codex/agents/*.toml` resources require explicit installation and trusted project configuration. Installing a plugin alone does not register those roles. The role files omit model settings because those fields override spawn choices; the resolver supplies explicit settings after inspecting role/task preferences and the observed parent settings.

## Structural and lifecycle checks

| Check | Result | Observation |
| --- | --- | --- |
| Package validation | PASS | Two explicit-only skill entries, two role resources, intact MIT license, references remain inside package |
| Native packaging smoke | PASS | Isolated install, inventory, qualified entry, short project alias, ordinary-prompt exclusion and removal; no model involved |
| Skill Creator validation | PASS | Both entry skills pass frontmatter/name/scaffold validation |
| Candidate regression suite | PASS | 13 Bun tests, including a wrapper running 9 Python lifecycle/model tests |
| Native setup lifecycle | PASS | CLI install/repeat/verify/uninstall preserves unrelated config and agents; occupied paths and edited roles refuse mutation; symlinks preserved |
| Model resolver | PASS, deterministic tests | Parent inheritance, role choice, task choice, reset to inherit, unavailable model, incompatible effort, retained preferences; invalid choices do not replace saved state |
| Catalog transport | PASS | Native app-server model/list returns available identifiers/efforts; an explicitly supplied native snapshot permits sandboxed resolution; wrong-source and expired snapshots rejected |
| TypeScript and inherited checks | PASS | New TS strict check; inherited typecheck, 69 tests and 247 assertions; both Shell syntax checks |

The native model catalog is account/client dependent. No particular identifier is hard-coded into runtime selection. Authenticated probes below select specific advertised models only as test inputs. The catalog snapshot is a bounded transport fallback, not a guarantee of future account access. Its source label is not a cryptographic attestation; the caller supplies a trusted native snapshot, which expires after one hour.

## Real task observations

Three disposable Git projects were isolated from each other. Each had its own temporary CODEX_HOME, explicit fixture-only project trust, installed project role resources and a short-name skill link. Authentication used a temporary reference to the existing login file; credentials were not copied or committed. Test references were removed afterward. No global configuration or user plugin installation changed.

| Route | Observation | Artifact verification |
| --- | --- | --- |
| Feature | Adds multiply(a, b) while preserving add; primary reports scoped implementation and comment review | Original check.py remains byte-identical; multiply positive/negative cases and add pass; only app.py and task.md changed |
| Bug fix | Original average fixture divides by len(values) + 1; failing reproduction is retained before the fix | Same check.py fails before, passes after division changes to len(values); check.py unchanged; only app.py and task.md changed |
| Investigation | Explains total(items) with file/line citations and explicit read-only scope | Before/after file-content snapshots identical, including tracked and untracked files; fixture check passes |

These artifact observations do not independently prove every delegate action in those CLI runs: the CLI JSON output omits some nested activity. Native role/model proof was collected separately below. Checklist files preserve completed, pending and skipped items in the two writing fixtures. Dedicated failure-path and multi-turn observations are described below; they are not inferred from the initial successful task runs.

The first run using the user's normal configuration could not discover fixture roles or launch nested model discovery. Feature stopped, but Bug fix performed a primary-only fix after reporting delegation unavailable. That run **FAILS** the delegated workflow gate despite passing its final behavior test. The candidate now explicitly stops Feature/Bug fix when mandatory delegation is unavailable; the isolated test setup uses project trust and a host-provided native catalog. A separate native blocked-delegation recheck then deliberately edited poteto-agent.toml. Both verify and catalog-backed resolve exited 1. The model retained a FAILED/BLOCKED checklist step and subsequent pending steps, and app.py remained byte-identical. No primary implementation or role repair was substituted. That failure-path recheck passes for this observed scenario.

## Native role and model observations

A separate read-only app-server probe used experimental raw event observation in its disposable workspace. The parent selected Sol/low while native global subagent defaults in that isolated home selected Luna/high. No role file had a model or effort override.

| Registered role | Requested model/effort | Observed subAgentActivity start |
| --- | --- | --- |
| poteto-agent | gpt-6.1-sol / low | gpt-6.1-sol / low |
| poteto-agent | gpt-6-luna / medium | gpt-6-luna / medium |
| poteto-agent | gpt-6.1-sol / high | gpt-6.1-sol / high |
| comment-sicko | gpt-6.1-sol / low | gpt-6.1-sol / low |

Raw native spawn calls name the two custom agent types. Host developer-instruction events contain each packaged role's instructions. All four delegates execute successful entry-file reads. Comment-sicko emits its prescribed opening, flags the fixture's redundant comment, and reports no edits. Native model/effort start events match all four requested pairs despite different global defaults. This establishes registration, instruction loading and native explicit-setting handoff; deterministic resolver tests establish preference precedence. A second native matrix generated resolved.json by calling the real resolver: absent-role parent inheritance, a saved feature preference, then an explicit task override. The primary read those resolved settings, spawned the exact registered roles, and native subAgentActivity events matched Sol/low, Luna/medium and Sol/high. This closes the saved-preference-to-spawn chain for those cases. Separate calls using the actual native catalog rejected an unavailable identifier and Sol/none with exit 1, before any spawn; no fallback model was selected.

The probe uses the native app-server backend, not desktop UI automation. Raw account/session/protocol logs remain local and are not committed. No internal database path is treated as a supported product interface.

## Explicit Feature follow-up and new-task control

A separate native session actually loaded `$poteto-mode` for a Feature fixture, delegated implementation and comment review, verified multiply while preserving add, and persisted task.md. The unchanged check.py passed. The next turn in the same thread asked to continue that feature; the primary read the existing checklist, reran the same acceptance command, and appended a follow-up verification entry to the same file. It created no second workflow owner or delegate.

A third turn explicitly started a new ordinary arithmetic task. The native event stream for that root turn contains one user message and one assistant message, with final text `12`; no command, checklist update or subagent activity occurred. This supplements the isolated new-session context-exclusion smoke test. The fixture was not a Git repository, which the model retained as a limitation; Git-based change checks were covered separately by the three-project CLI script.

## Reproduction

```sh
bun scripts/validate-codex-plugin.ts
bun test ./scripts/
python3 -B scripts/smoke-codex-entry.py
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /absolute/scratch/catalog.json
python3 -B scripts/accept-codex-core.py --model MODEL_FROM_CATALOG --effort SUPPORTED_EFFORT --catalog /absolute/scratch/catalog.json
```

The last command uses real model quota, creates three ephemeral sessions with scoped delegates, and prints its local evidence directory. It requires an existing CLI login file (or explicit --auth-file). It checks CLI exit, observable fixture behavior, allowed file changes, unchanged Git HEAD and an unstaged index. It returns nonzero on artifact failure. It deliberately does not call those artifact assertions a full workflow, role, model or desktop pass. Inspect tool activity, the initial failing reproduction and checklist separately.

## Remaining phase 2 gates

- Confirm the candidate plugin install/discovery/removal lifecycle. The three desktop routed tasks, Feature follow-up and ordinary-chat control now have manual observations below; phase 1 UI evidence still applies only to 0.1.0-alpha.1.
- Preserve independent review and green CI when making later changes. The review of `81ca134` found no remaining blockers; both [inherited checks](https://github.com/chrison18/codex-pstack/actions/runs/39735424733/job/119679858492) and [Codex checks](https://github.com/chrison18/codex-pstack/actions/runs/39735424742/job/119679858383) passed at that head.

Desktop automation was denied for the Codex app during phase 1. The restriction has not been bypassed. Desktop acceptance needs separately labeled owner/manual evidence unless an allowed control surface becomes available. See the [desktop acceptance procedure](phase-2-desktop-acceptance.md).

The catalog helper starts a native app-server with its own effective configuration; it does not replay arbitrary command-line provider overrides from a different parent process. Use a snapshot from the same provider/configuration as the task. Cross-provider parity is not established by these account-backed tests.

On October 22 the owner initially deferred desktop acceptance, then provided the routed-task screenshots described below. PR #3 remains a draft; no phase 2 merge is authorized or performed.

## PR #3 independent review correction

The reviewer reproduced a P2 false-positive in the artifact snapshot: it ignored symlinks and empty directories, so a read-only task could change a link without appearing in the changed-path set. The corrected snapshot records lstat types and modes, regular-file digests, link targets without following them, and directories. Root Git metadata stays outside the content snapshot and is checked separately by the harness's HEAD/index assertions; this is not a promise to audit every internal Git metadata write.

Five Python regression cases cover link creation/deletion/retargeting, file-to-link replacement, empty directories, mode changes, and non-traversal of links. The suite now has 14 Bun tests, including 9 runtime and 5 snapshot Python cases. A --case selector allows rerunning only the affected real-model fixture. The earlier Investigation result established regular-file content stability; the corrected snapshot is required for the stronger entry/type/mode claim.

With the corrected snapshot, the authenticated Investigation-only recheck completed with CLI exit 0, unchanged entry/type/mode state, and a passing fixture check. This is a new observed result, not a relabeling of the earlier content-only observation.

The independent reviewer rechecked the fix at `81ca134`, independently ran the tests, verified the native distribution inventory, and confirmed the corrected Investigation before/after snapshots contain the same 11 entries. No further blocking findings remained. The PR stays draft/open and unmerged by the owner's instruction.

## Owner-operated desktop observations, 2026-10-22

Installed desktop application version: **26.1016.61520**, build **21421**, production channel. The app update tool reported those values; the installed application's Info.plist independently matched them. This is the desktop version, distinct from the CLI protocol version above.

The owner manually operated the application and supplied screenshots. No automated UI control was used. The tested short entry was the project-linked poteto-mode candidate from this checkout; the checked project roles and source remain 0.2.0-alpha.1. The owner moved the prepared fixtures from temporary storage into a project directory. Artifact inspection therefore used the actual project paths, without assuming the original temporary copy changed.

| Desktop scenario | Result | Evidence |
| --- | --- | --- |
| Explicit Feature | PASS | Screenshot shows implementation and comment-review delegates; primary checks diff and runs check.py. Independent artifact inspection confirms multiply was added, add retained, check.py unchanged and acceptance exit 0. The fixture's preexisting Finder metadata and installed role/link resources were not counted as implementation changes. |
| Same-task follow-up | PASS | Screenshot and task.md show the existing checklist read and appended; the same check passes again, without a new implementation or delegate. |
| Expired model catalog | PASS for stopping behavior | Bug reproduction fails first; catalog-backed model resolution then refuses the expired snapshot. The application is left unchanged and pending work is retained. The host refreshes the same snapshot path, without changing model preferences. |
| Bug fix after refresh | PASS | Original chat resumes, delegates the denominator correction, and primary reruns the same test. Screenshot retains exit 1 before and exit 0 after; artifact inspection confirms only the intended denominator fix, unchanged check.py and a passing check. |
| Read-only Investigation | PASS | Screenshot explains total(items) with file/line citations. The independently captured before/after snapshots have the same 12 entries, with no content, type, mode, directory or link changes. No task file is created. |
| New ordinary chat | PASS for visible response | Screenshot shows exactly 12 for the digits-only arithmetic prompt, with no visible tool, checklist or delegation activity. This manual observation supplements the earlier native event/context negative controls. |
| Candidate install/discovery lifecycle | NOT FULLY RECORDED | Task screenshots prove short project-entry operation; candidate version display and qualified plugin entry discovery were not independently captured. |
| Candidate plugin removal | PENDING | The owner said they were going to uninstall pstack. Intent is not recorded as completed removal. |

Private screenshots and full conversations are not committed. The desktop test results above are explicitly separated into owner-operated UI observations and agent-inspected local artifacts. Final lifecycle confirmation and owner merge authorization remain separate requirements.
