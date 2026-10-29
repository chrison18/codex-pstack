# Phase 3B2 acceptance closure

Branch `test/codex-3b-acceptance` starts from actual merged main `b9ad7434506b3785b531b66afa85d1ad040b9fbb`. PR #5 merged by squash on 2026-10-26 after independent review, the reproduced/fixed temporary-auth cleanup finding, local checks and both exact-head CI jobs for `75d65c5c8515ac6df6d5884b38dc163e35a12db5`. See [3B1 review](phase-3b1-merge-review.md).

This increment owns acceptance closure, not phase 4. Inventory remains 37 adapted, 31 partial and 19 deferred. A successful bounded probe clears only its named scenario; missing desktop, connector or proof surfaces stay visible.

## Retained work

| Area | Existing evidence | Remaining work |
| --- | --- | --- |
| Interrogate | Concrete two-model defect; native rejected-selection and missing-role boundaries; actual capacity-dropout disclosure and completed empty panel below | Other dropout/recovery modes and desktop coverage |
| Arena / Architect | Artifact synthesis, How grounding, checkpoint and default implementation; invalid Arena pool rejection below | Scrap/reframe/dropout, same-model pools, code-worktree and desktop variants |
| Swarm | Concurrent writers, non-default base, local-process/auth proof, races/conflicts, bounded retry/interruption; tied scores and actual local HTTP rejection below | Actual crash/network recovery and desktop/browser variants |
| Why | Native local history and primary-host GitHub supplement | Actual native connector access and genuine cross-category synthesis; advertised Slack dispatch failed |
| Verification authoring / maintenance | Ordinary-path PTY and bounded-property candidates | Protected installation/native discovery and broader formal-tool evidence |
| UI / visual parity | Host web replay only; native sandbox launch blocked | Applicable native/browser and desktop proof, immutable visual baselines |
| Eval | Bounded artifact comparison and primary reconciliation | Strict path/context blinding, observable child read chain and any claimed family diversity |
| Other partial portable routes | Scoped writing, teaching, quality, refactoring, prototype, plan, measurement and delivery | Reconcile the declared supported scope per inventory row; retain later-phase overlays and unrun scenarios |

Full 3B closure requires updated evidence, capability reconciliation, independent review and current-head checks. Unavailable sources must retain concrete limitations; neither this table nor CI claims they passed. Full phase 4–6 work remains dependent on that closure.

## First increment: Interrogate negative paths

`accept-codex-research.py` adds three explicitly selected native cases:

- `review-empty`: a shipping implementation changes from a conditional expression to an equivalent branch for the declared nonnegative-integer domain. Two default reviewers must preserve the observed parent pair despite conflicting global defaults, keep review read-only, and avoid inventing a defect. Static reasoning must not be presented as executed application checks.
- `review-invalid`: a valid first selection and deliberately unavailable second model test whole-panel rejection before any spawn. The request forbids substitution, preference mutation and primary-only fallback. Capture rejects observed spawn requests or resolved starts, but semantic audit must also find the actual resolver rejection and inspect the final answer.
- `review-missing-role`: the harness deliberately omits project role installation while retaining the explicit entry. A missing registered role may lead only to the disclosed primary read-only fallback, without installing roles, changing configuration or substituting a built-in agent. Capture rejects spawn requests/starts; actual missing-role checks and scoped review still require semantic audit.

All three use disposable projects and isolated homes, local files/history only and a read-only parent. The harness captures entry snapshots plus HEAD/index and removes its temporary auth reference. Raw events stay local. Captured completion does not establish semantic conformance; all results require inspection of real tools, model starts and final claims.

Reproduce after refreshing the native catalog with the selected Codex CLI on PATH:

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /tmp/pstack-3b2-models.json
python3 -B scripts/accept-codex-research.py --case review-empty --case review-invalid --case review-missing-role --codex /absolute/codex --model gpt-6.1-sol --effort low --catalog /tmp/pstack-3b2-models.json
```

Current official OpenAI [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents), fetched 2026-10-26, describes inherited permissions and configurable model precedence. The probes inspect actual local client behavior rather than treating documentation as acceptance evidence.

## Native results — 2026-10-26

Codex CLI `0.164.0-alpha.11.1`, parent Sol/low, macOS. The native catalog was freshly retrieved; the deliberately invalid identifier is absent. Global fixture subagent defaults remain Luna/high so actual Sol/low starts establish explicit parent-pair preservation. Event positions below are zero-based JSONL positions; raw captures remain in task-owned local temporary directories.

### Rejected explicit model — scoped PASS

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-research-live-bviwr67x/review-invalid`. The parent read the runtime/Interrogate requirements, captured refs and ran the exact whole-panel resolver at raw event 170. Its matching tool output at 173 returned exit 1 and `Unavailable model: pstack-unavailable-acceptance-model`. This result is in a raw custom-tool output, not an ordinary command-completed notification; inspection covered both event forms.

There were zero spawn requests and zero resolved child starts. The parent reported a blocked prerequisite, skipped independent reviews and verdict, and did not replace the selection or do a primary-only review. Entry snapshots, HEAD and index stayed unchanged; auth link removed. This passes the rejection boundary, not successful model selection or shipping-code review.

### Empty review with actual capacity dropout — limited PASS; full panel BLOCKED

Initial evidence: `pstack-research-live-bviwr67x/review-empty` under the same temporary parent directory. Whole-panel resolution completed at event 72 with two Sol/low members and `modelDiversity: false`. Native starts were `01a1773e-1b0d-7e50-8d38-358941a1634f` and `01a1773e-38e0-7a82-9c4d-b0969d342026`. Actual server event 285 reports `serverOverloaded`, `willRetry: false` for reviewer 1; this is not inferred from the parent's prose. Reviewer 2 returned no findings at 452. The primary inspected actual code and reported the incomplete panel at 617 rather than presenting two completed reviews.

One bounded rerun used identical model settings: `pstack-research-live-hythvuif/review-empty`. Resolver completed at 84; native starts at 174/191 were `01a17740-8837-7c01-8f90-7d166e248fc2` and `01a17740-9ec8-7fc2-aa47-94bcc47e0367`. Event 274 again reports actual `serverOverloaded`, `willRetry: false` for reviewer 1. Reviewer 2 returned no findings at 415. The primary again retained the capacity gap, same-model label, static-only evidence and unchanged workspace. No third retry or model substitution was attempted.

Both runs support correct same-model resolution, one completed empty review and truthful dropout reporting. Neither passes the full two-completed-reviewer empty-panel scenario. Capture's `artifactChecksPassed: true` is deliberately narrower than that workflow verdict; both results retain an UNREVIEWED warning pending semantic audit. Host-only fixture sanity additionally checked 1,001 nonnegative integers against the actual old/new shipping source, all matching. Native agents did not execute application code; that supplement does not change their static scope.

### Missing role — scoped fallback PASS

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-research-live-8uisq8jn/review-missing-role`. The isolated project has no `.codex` directory/role receipt. The actual resolver call at raw event 201 returned exit 1 at 206 for missing `.codex/pstack-agents.json`. No spawn request or child start occurred. The parent disclosed primary-only fallback, inspected the exact shipping diff and correctly identified the zero-quantity regression as static reasoning. It did not install roles, substitute a built-in reviewer, edit source/configuration or claim a panel agreement map.

Entry snapshots, HEAD and index remained unchanged, `.codex` remained absent, and the auth link was removed. The model additionally reported that its available spawn schema lacked role selection; that tool-schema explanation was not independently established by this audit and is not needed for the missing-receipt result. This proves the documented missing-role fallback in this fixture, not successful role registration or desktop behavior.

## Increment validation and limits

The package suite (34 tests / 57 assertions), package and source-inventory validation, two research-capture regressions and diff checks passed. Native evidence was semantically inspected as described above, including raw tool outputs where normalized command events were absent. All four task-owned auth links were removed; no prior provider session was resumed or modified. The first two empty-panel attempts remain excluded from a full empty-review pass. No product workflow/runtime instruction changed; only acceptance cases and current evidence/status metadata were extended. Interrogate stays partial and full 3B remains incomplete.

## Second increment: Swarm tie and local rejection — scoped PASS

Both probes used Codex CLI `0.164.0-alpha.11.1` on macOS, parent Sol/low and a freshly retrieved native catalog. These are bounded fixtures, not desktop parity or full Swarm completion.

### Tied scores

`accept-codex-swarm-recovery.py --case race-ties` adds rank-all and best-of rounds. The publisher strips optional quality evidence from both arms, leaving valid score 4 reports, and holds a until b publishes. The declared tie-break remains arm ID ascending. Publication order is distinct from agent terminal-message order.

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-swarm-race-ties-368wxs9o`. Actual workers were a `01a17766-e1ce-7e03-9350-0f0d3094cba0` Sol/low and b `01a17767-03ac-7642-b46d-980c1979b19b` Luna/medium. Resolution at raw event 101 preceded explicit registered-role spawn requests at 187/243. Rank-all declaration at 117 preceded fan-out; best-of declaration at 853 preceded follow-up briefs at 949/997. Both agents were reused without nested delegation.

Both rounds published b before a, with one report per arm and both scores 4. Rank-all selected `[a,b]`; best-of selected `[a]`. Terminal answers at 722/819 and 1180/1351 preceded selection writes at 853 and 1448 respectively. The primary inspected reports, validated all four and replayed recorded commands; its final retained the tie without inventing a quality difference. Workspace snapshots, HEAD and index stayed unchanged, and the temporary auth link was removed. A regression also reverses both selections and verifies that the audit rejects them. This proves the declared tie-break for these controlled equal-score submissions, not model quality or speed.

### Rejected local-service capability

`accept-codex-local-denied.py` serves an actual loopback HTTP 403 response in a disposable fixture. A required local-service slice needs a ready response and challenge; the worker may run its checkout's probe once and write evidence. The primary must retain incomplete coverage when that capability is unavailable. Service changes, credential searches, retries, other endpoints and isolated-test substitutes are excluded from the assigned scope.

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-local-denied-zd6cmtr6`. The actual resolver call at raw event 93 preceded the explicit Luna/medium registered-role request at 103; exactly one child started (`01a17768-e185-73b0-ac2e-95f223b27502`). The child ran `python3 -B local_probe.py` in the assigned primary checkout at 389. Tool output 395 returned exit 3 with HTTP 403, `ready:false` and `capability_denied`. Server-side audit independently recorded exactly one `/probe` request, PID 29005.

The worker wrote BLOCKED evidence with the actual base SHA, command and sample count, then finished at 577. The parent read that evidence at 585, wrote `complete:false`, `requiredSlice:local-service`, `status:BLOCKED` at 686, and retained the missing challenge in its final. No second probe or substitute verification occurred. Workspace snapshots, HEAD and index stayed unchanged; auth link removed and server stopped. This passes truthful handling of a real application-level denial, not OS permission isolation, successful authentication, process-crash recovery or desktop access. Capture's UNREVIEWED label requires this separate semantic audit and is not itself a workflow verdict.

Reproduce with a fresh catalog and explicit CLI path:

```sh
python3 -B scripts/accept-codex-swarm-recovery.py --case race-ties --codex /absolute/codex --model gpt-6.1-sol --effort low --catalog /tmp/pstack-3b2-models.json
python3 -B scripts/accept-codex-local-denied.py --codex /absolute/codex --model gpt-6.1-sol --effort low --catalog /tmp/pstack-3b2-models.json
```

The six recovery-instrument regressions and package suite (34 tests / 57 assertions) passed. A model-free service smoke also observed the real 403, exit 3 and exactly one request without changing the probe. No product workflow behavior or inventory status was upgraded: Swarm remains partial, and PR #6 remains an acceptance work in progress.

## Third increment: completed empty review — scoped PASS, 2026-10-28

A later rerun of the unchanged `review-empty` fixture completed both reviewers. This closes the two-completed-reviewer empty-result scenario; it does not change the historical capacity failures above into successes or prove other recovery/desktop variants.

Evidence: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-research-live-xus7oxou/review-empty`. Client remained Codex CLI `0.164.0-alpha.11.1`, parent Sol/low; the native catalog was refreshed for this run. Actual whole-panel resolution at raw event 98 returned before explicit registered-role spawn requests at 110/158. Both used `fork_turns:none` and resolved Sol/low despite conflicting global defaults. Native child IDs were `01a1813f-7635-75a2-8928-ac6240999e23` and `01a1813f-8e06-7f50-b63c-2830291dd394`.

Each reviewer independently read the scoped shipping diff and head artifact (events 183 and 420), then returned no findings at 407 and 515. The primary's final at 658 reconciled both results with its own inspection, explicitly labeled model diversity false and limited its conclusion to static equivalence for nonnegative integers. No application code/tests ran or were claimed to have run. Git emitted sandbox cache warnings but returned the requested artifacts; those warnings are retained in the final evidence limits.

The native capture completed with unchanged snapshots, HEAD and index; the temporary auth link was removed. Manual inspection confirmed exactly two role starts, both final reviews before primary synthesis, no replacement reviewers and no invented findings. This is a same-model independent panel, not cross-model diversity. Interrogate remains partial pending the other retained scenarios; full 3B and phase 4 gates are unchanged.

## Fourth increment: Arena boundaries and Cursor comparison — 2026-10-28

See the [scoped Cursor behavior comparison](cursor-behavior-delta.md) for material goal-carrying, delegation and autonomy differences; the upstream pin is unchanged. Acceptance code started from `612a111bf14106715364b40ed08fa1720b193631` plus the reviewable `accept-codex-design.py` changes adding two opt-in cases. Existing default cases remain unchanged. Native CLI was `0.164.0-alpha.11.1`, macOS; the catalog was refreshed before testing. Raw evidence stays local, not in the public repository.

### Same-model Arena — BLOCKED by actual model capacity

`arena-same-model` requests two independent Sol/low runners, with the existing Luna/medium judge choice; runner independence must not be labeled model diversity. The Sol/low parent read workflow guidance, then the native server returned `serverOverloaded`, `willRetry:false`, before any runner started (raw events 90/91). Capture status was failed, zero spawn requests/starts, no candidate rationales and no changed paths. The temporary auth link was removed. This is an infrastructure block, not a same-model workflow pass or a dropout test. No unchanged retry or silent selection substitution occurred.

### Invalid Arena pool — scoped PASS

An independent `arena-invalid-pool` case uses the existing available Luna/medium parent and an exact explicit pool containing Luna/medium plus `pstack-unavailable-acceptance-model`, absent from the fresh catalog. On resolution failure it must stop before delegation/artifact writes, without model substitution or primary-only synthesis. This is a different boundary scenario, not a successful rerun of the blocked same-model case.

The parent read the actual entry/runtime/Arena instructions (event 66), then called the real `resolve-panel ... arena-runner` with both exact selections at 86. The tool returned `Unavailable model: pstack-unavailable-acceptance-model` at 92. The final at 227 reported the blocked prerequisite and explicitly skipped judge resolution, candidates, judging, synthesis and verification. There were zero spawn requests/starts, zero changed paths, unchanged HEAD/index and no candidate artifacts; auth link removed. Manual event inspection supports atomic rejection before fan-out, not successful candidate synthesis. Capture retains an UNREVIEWED label because guards alone cannot establish this semantic verdict.

Reproduce with a freshly generated native catalog and the selected CLI:

```sh
python3 -B scripts/accept-codex-design.py --case arena-same-model --codex /absolute/codex --model gpt-6.1-sol --effort low --catalog /tmp/pstack-design-catalog.json
python3 -B scripts/accept-codex-design.py --case arena-invalid-pool --codex /absolute/codex --model gpt-6-luna --effort medium --catalog /tmp/pstack-design-catalog.json
```

The new cases are opt-in so default runs do not silently consume extra model calls. Python parsing, package/inventory validators, the package regression suite (34 tests / 57 assertions), diff and local-link checks passed. No full-3B status is upgraded. Same-model success, design scrap/reframe/dropout, code-worktree variants, actual crash/network recovery, connector synthesis, protected discovery, strict Eval and applicable UI evidence remain open. Next feasible work is a bounded design dropout/reframe probe; goal-carrying guidance differences should be proposed separately with attribution and delegated-brief acceptance. Phases 4 and 5 remain dependent on full 3B closure.

## Fifth increment: controlled missing output and same-model completion — 2026-10-28

Tested source: `79c61dbef6dc50b3c0529f2b56ef7daffaeec0b0` plus the reviewable harness changes in this increment. Native Codex CLI remained `0.164.0-alpha.11.1` on macOS. A fresh native catalog supported the predeclared parent, both runners and judge: `gpt-6-luna/medium`. This is a separate declared scenario from the historical Sol capacity failure, not a substitution within that result. Raw events and fixtures remain local; event positions below are zero-based.

### Controlled missing-output / N−1 handling — scoped PASS

The opt-in case named `arena-dropout` deliberately instructs runner 2 to load its instructions and grounding, then report a simulated missing-input blocker without writing a candidate. It does **not** kill a process or simulate network recovery. Runner 1 must produce its own candidate; the primary may judge/synthesize only that real candidate and must write explicit incomplete coverage. Existing default cases are unchanged.

The parent read entry/runtime/Arena at event 68 and wrote grounding before fan-out at 176. An initial inherited-context spawn failed with `no rollout found`; the parent then used independent `fork_turns:none` starts. Four spawn requests produced exactly three actual starts (two runners and one judge), all at the declared model/effort. Runner entry reads were observed at 431/473. Runner 2 returned BLOCKED at 565 without files; runner 1 wrote only its own app/rationale and completed at 734. The judge started at 822 after both terminal results, read the entry and actual candidate, and returned its reduced-coverage assessment at 1368. The primary wrote synthesis only afterward at 1466 and disclosed one available candidate, no two-candidate comparison and no crash-recovery claim in its final at 1998.

Only candidate 1's two files and four synthesis files changed. Candidate 2 remained empty; production files, HEAD and index stayed unchanged. `coverage.json` records `complete:false`, completed candidate 1, missing candidate 2 and a nonblank reason. The exact synthesized-file contract check passed; temporary auth was removed. The strengthened coverage guard was replayed against these actual artifacts and passed. Negative regression cases reject `complete:true`, incorrect completed/missing lists, absent candidate 1, invented candidate 2, invalid reasons and malformed JSON. These checks validate evidence shape; the semantic verdict comes from the event/artifact audit above.

### Same-model Arena completion — scoped PASS

An initial Luna attempt was BLOCKED by two inherited-context spawn errors (`invalid thread-store request: no rollout found`), with zero child starts and no candidate artifacts. Its honest blocked final is retained. The harness now explicitly requests `fork_turns:none` and self-contained scoped entry/grounding briefs for these two opt-in scenarios. One bounded rerun after that changed launch constraint completed; no unchanged capacity retry was made.

In the completed run, entry/runtime/Arena reads occurred at 74. The parent corrected an initially mistaken runtime-script path and resolved the whole pool before grounding at 289 and two runner spawns at 302/323. Both actual starts were Luna/medium despite isolated global defaults of Luna/high. Each runner independently read the entry (369/454), corrected mistaken principle paths, loaded grounding and wrote only its own app/rationale. Both finals (788/1004) preceded judge spawn 1033. The primary read both complete artifacts at 1021; the judge read the entry, grounding, both full apps and rationales at 1090, ran bounded contract checks, and returned at 1531. Synthesis was written at 1636, then the primary loaded that exact absolute file and verified the contract at 1649. Capture independently returned `design acceptance passed`, exit 0.

The two candidates converged on the same one-pass implementation and rejected the same list-materialization alternative. The judge and primary explicitly reported equivalence, not structural or model diversity; the final at 2240 states `modelDiversity:false` and the judge's matching identity. Seven candidate/synthesis files changed, with no out-of-scope changes, unchanged production files/HEAD/index and removed temporary auth. No extra approval checkpoint was introduced. This proves independent same-model artifact execution and truthful convergence reporting, not Architect structural-alternative quality, code-worktree isolation or Chat parity. The judge's final included mistyped file links; actual tool reads used the correct files, so the links are not used as evidence.

Reproduce each separately with a fresh catalog:

```sh
python3 -B scripts/accept-codex-design.py --case arena-dropout --codex /absolute/codex --model gpt-6-luna --effort medium --catalog /tmp/pstack-design-catalog.json
python3 -B scripts/accept-codex-design.py --case arena-same-model --codex /absolute/codex --model gpt-6-luna --effort medium --catalog /tmp/pstack-design-catalog.json
```

Next executable task: a bounded Architect scrap/reframe scenario with a rejected initial design, explicit revised grounding and inspected second-round artifacts. Actual runner/process failure and crash/network recovery, design code-worktree variants, connector synthesis, protected discovery, strict Eval and applicable UI evidence remain open. The Orca Chat input block is unchanged. Full 3B remains incomplete; phases 4/5 and merge gates are unchanged.

Local validation for this increment: package regression suite **35 passed / 59 assertions**, package validator and `git diff --check` passed. No production workflow instruction changed; the new missing-output case and independent-start constraints are acceptance harness controls. Independent review and publication are still pending.

## Sixth increment: package-owned independent starts — 2026-10-28

The fifth increment was reviewed and published as `5d5ca3cb35b28b7610bb15061e3cae36b2d3d4b5` with the verified GitHub-associated author/committer. Remote branch and PR #6 head matched exactly; both [workflow 40652041360](https://github.com/chrison18/codex-pstack/actions/runs/40652041360) and [workflow 40652041309](https://github.com/chrison18/codex-pstack/actions/runs/40652041309) passed for that head. PR #6 remains draft. These CI results apply to the published increment, not the following uncommitted adaptation.

Review found that the fifth increment's successful independent starts were coached by the acceptance prompt, while the package itself lacked that host adapter. The package runtime contract now explains fresh scoped starts with explicit resolved settings when the actual schema supports `fork_turns:none`, and requires self-contained goal, constraints, authority, entry/grounding, ownership and evidence briefs. Arena applies it to each runner and judge. Full-history context is not categorically forbidden; continuing a delegate and other hosts retain their documented capabilities. Missing support or permission denial remains a block, not permission to invent fields, omit model selections or bypass host controls. Registered role templates remain unchanged and still require entry reads. This is a Codex adaptation at the unchanged upstream pin.

The native schema observed in CLI `0.164.0-alpha.11.1` exposes `fork_turns:none/all` and explains that `none` has no surrounding conversation. The current host also constrains full-history model overrides; historical `no rollout found` errors establish a real launch limitation, not a generic prohibition on inheritance. Both opt-in acceptance prompts now omit the `fork_turns`/fresh-start coaching entirely. The declared parent, runners and judge remain Luna/medium with a fresh catalog, against isolated global Luna/high defaults. Native events, not a text-matching test of guidance, are the behavior test.

### Initial uncoached run — launch PASS, complete handoff NOT PASSED

Against published `5d5ca3c` plus the initial runtime/Arena guidance, the same-model run loaded the package at event 81 and used fresh explicit starts at 449/505/1091, with three matching actual starts and no inherited-context launch failures. Candidate entry reads occurred at 504/588; both candidates and the judge completed before synthesis, and exact synthesized-file verification passed. However, grounding was written at 607 **after** runner starts and neither runner read it. This fails complete grounding handoff despite passing artifact guards; it is not a full workflow pass.

The controlled missing-output run also launched three matching fresh delegates. Runner 2 stopped at 437 because its brief lacked the entry path, explicitly without reading grounding; this does not reproduce the intended simulated missing-input scenario. The judge initially stopped for the same omission, then completed after a corrected follow-up. The primary honestly retained missing coverage and verified the single-candidate synthesis, but the artifact guard's success cannot establish the intended scenario. Both raw runs are retained locally; temporary auth links were removed.

The focused correction makes grounding persistence/read-back an explicit pre-spawn condition, supplies a per-delegate brief template including judges, and forbids shortened briefs that assume another runner's context. Entry/grounding omissions must be reported as handoff defects rather than successful negative-path coverage. One bounded rerun uses the unchanged user-level prompts with the corrected package; results follow after event inspection.

### Corrected package, unchanged task prompt — same-model scoped PASS

The rerun read entry/runtime/Arena at event 75, persisted and read back grounding at 360, then spawned independent runners at 371/391. Both actual starts matched Luna/medium with `fork_turns:none`. They read entry, grounding and Arena at 446/515 before their own candidate writes, and completed at 1440/1118 respectively. The primary inspected both complete packages at 1539; judge spawn 1547 followed both finals. The judge independently read entry/grounding at 1615 and both full candidate packages at 1637, verified bounded cases at 1690 and returned at 1800. Synthesis and exact-path verification followed at 1900. The final at 2196 accurately disclosed same-model convergence and matching judge identity.

Each runner wrote only its own `total.py` and `README.md`; both Markdown rationales contain design alternatives/rejections. The existing artifact guard accepts Markdown rationale files without a fixed filename; no guard change was needed. Seven candidate/synthesis files changed, no unexpected changes, unchanged production files/HEAD/index, removed temporary auth and independent exact synthesis verification (`design acceptance passed`, exit 0). There were exactly three spawn requests and three matching actual starts, with no inherited-context retry. This establishes package-driven independent Arena handoff for this fixture without prompt-level launch coaching, not generic reliability or all-route acceptance.

### Controlled missing-output regression — scoped behavior PASS with checklist deviation

The corrected-package run read entry/runtime/Arena at 84, wrote and read back grounding at 354, and launched runners at 366/386. Both actual starts were fresh Luna/medium. Entry and grounding reads are visible at 434/511, before runner 2's intended missing-input BLOCKED result at 647 and runner 1's completion at 942. The primary inspected the sole actual candidate at 958; judge spawn 969 followed both finals. The judge read entry, grounding and actual candidate at 1026, returned a single-candidate assessment at 1346, then primary synthesis/coverage at 1467 and exact-file verification at 1478 completed. The final at 1838 retained missing coverage and no candidate comparison.

Exactly three matching starts, no substitute/retry for runner 2, empty candidate 2, explicit `complete:false` coverage with the observed reason, unchanged production/HEAD/index and removed temporary auth were verified. The actual synthesis and capture verification both passed. Seven files changed, all within candidate 1 and synthesis. A remaining instruction-following deviation is recorded: the primary added `synthesis/checklist.md` despite the fixture asking for a conversational checklist. It stayed within authorized synthesis ownership and does not invalidate the observed launch/context/N−1 behavior, but this is not a claim of perfect prompt compliance or full workflow acceptance. Real process/crash/network recovery remains unproved.

After capture ended, coordinator review narrowed the shared runtime template: grounding is required only by workflows that require it; otherwise it is N/A with full task context and references, never an excuse to create files in a read-only route. Feature, Bug fix and Investigation instructions were inspected for compatibility. Arena's mandatory grounding and start behavior are unchanged by that clarification; the native runs above precede this wording clarification and do not recertify those other routes. Local package tests remain 35 passed / 59 assertions; package validator and diff checks passed. No text-matching test is presented as proof of instruction following.

This new adaptation remains uncommitted for independent review. Next: review the package change and retained limits, then resume bounded Architect scrap/reframe acceptance. The original full-3B, real recovery, code-worktree design, connector, protected discovery, strict Eval and primary Orca Chat gates remain open; no phase 4 work or merge occurred.

### Non-Arena pre-publication regression — 2026-10-28

Tested the same reviewed adapter WIP over `5d5ca3cb35b28b7610bb15061e3cae36b2d3d4b5`, now including the conditional-grounding wording. Native CLI `0.164.0-alpha.11.1`, parent and resolved delegates Luna/medium, fresh catalog; neither prompt specified `fork_turns` or an expected start mechanism. Reused the existing core Feature (`multiply` alongside unchanged `add`) and read-only Investigation (`total` explanation) fixtures. The first `accept-codex-core.py --case feature --case investigation` run passed both artifact checks, but its ephemeral CLI event stream omitted direct spawn arguments and child reads. A local capture-only supplement reused those exact fixture bodies/prompts and the existing research `Client`/`summarize_events`, replacing the subprocess execution with raw app-server capture; no new fixture framework or runtime behavior was introduced. The original CLI results remain artifact evidence, not independent proof of child instruction loading.

**Feature — scoped PASS.** In the raw supplement the primary read runtime/Feature at event 76, resolved both roles at 168 after correcting a mistaken script path, and spawned `poteto-agent` at 190 with `fork_turns:none` and explicit Luna/medium. The actual child read the entry/Feature at 250 and source/acceptance contract at 278, changed only `app.py` at 292 and returned at 442. The primary inspected the actual diff and ran `python3 -B check.py` at 443 (`feature acceptance passed`), then spawned read-only `comment-sicko` at 462 with the same explicit settings. That child read the entry at 503 and exact diff/source at 548 before returning no findings at 813. Primary checklist reconciliation and scope inspection at 829 preceded final 1017. Exactly two matching actual role starts occurred; only `app.py` and authorized `task.md` changed, no grounding file was created, `check.py`/configuration/HEAD/index stayed unchanged and auth was removed. The host-side independent check also passed.

**Investigation — read-only preservation PASS; delegation regression FAIL.** The primary read entry/runtime/Investigation/How at 73, searched the nested `ALL_TOOLS` list for spawn/role names at 218, corrected a mistaken resolver path and successfully resolved Luna/medium at 240. Its final at 472 nevertheless asserted that no registered `poteto-agent` was available and used primary-only fallback. The actual native `collaboration.spawn_agent` schema in that capture explicitly lists `poteto-agent` and `comment-sicko`; direct collaboration tools are not established absent by searching the nested orchestration tool list. There were zero spawn requests and zero child starts, no host rejection and no evidence of unavailable model or permissions. This is a false capability inference, not an environment block or successful delegated Investigation. Source citations and primary inspection were present, snapshots/HEAD/index remained unchanged, no grounding or other file was created, and auth was removed. The separate host-side fixture check does not count as a native application test or delegate proof.

Publication of the adapter is therefore **held** under the coordinator's regression gate. No new commit, push or PR update was made in this regression task; the previous published head and its CI remain unchanged. The likely next focused correction is capability discovery: inspect direct native collaboration declarations and role schema before claiming absence; `ALL_TOOLS` only inventories nested tools. That correction is not silently bundled here. Local checks passed: 35 package tests / 59 assertions, package validator, Python parsing and diff checks. These do not override the observed semantic failure or recertify other routes. The existing Arena checklist deviation and all original phase/UI/recovery gates remain recorded.

### Capability-discovery correction — scoped positive and negative PASS

The preceding false-role-absence result remains a failure. The new runtime guidance distinguishes directly declared native collaboration tools and their `agent_type` schema from the nested tool inventory exposed through `functions.ALL_TOOLS`. An empty nested search cannot negate a directly declared role. Capability decisions combine actual schema, installation verification/receipt, resolver results and concrete tool rejection; resolution alone does not prove host loading. Investigation now explicitly follows this check before fallback. Legitimate read-only fallback, mandatory Feature/Bug delegation, explicit model settings and permission boundaries remain unchanged.

Tested over published `5d5ca3c` plus the reviewable adapter and this correction, with CLI `0.164.0-alpha.11.1`, a fresh catalog and Luna/medium parent. Reused the same core Investigation task and raw-capture supplement described above, with no prompt-level `fork_turns` instruction or capability-discovery coaching. The task remained a read-only explanation of the two-line `total` function, with all repository changes prohibited.

**Role present:** the primary read runtime/Investigation/How at event 67, corrected initially mistaken package reference paths, inspected the actual registration receipt and role at 260, then resolved `how-explainer` at 282. One `poteto-agent` spawn at 295 used `fork_turns:none` and explicit Luna/medium; one matching actual native start followed. The child read the absolute entry, runtime, Investigation, How and explainer instructions at 459, then inspected the actual source with line numbers at 467 before returning at 668. The primary independently read the same source at 413, checked final status/diff at 684 and reconciled the explanation at 895, accurately stating no application tests were run. There were zero snapshot changes, no grounding/checklist files, unchanged HEAD/index, and removed temporary auth. The separate host-side fixture check passed but is not attributed to the native agent. This closes the reproduced false-absence path for this scoped fixture, not all Investigation variants or perfect path discovery.

**Role genuinely absent:** ran the existing `review-missing-role` fixture separately with the same parent pair and catalog, omitting role installation as before. Its actual native spawn schema lacked an `agent_type` selector; the project had no `.codex` directory or ownership receipt. After entry/runtime/Interrogate/Investigation reads at 74, the primary called `resolve-panel` at 192; output at 198 reports the missing `.codex/pstack-agents.json`. Zero spawn requests and zero child starts occurred. The final at 598 disclosed primary-only static fallback and both concrete limitations, found the fixture's zero-quantity shipping defect, and did not claim a panel ran. No installation, configuration, application execution or repository mutation occurred; snapshots/HEAD/index were unchanged and auth removed. Sandbox cache warnings were retained, not used to invent a missing-role reason.

Local checks: 35 package tests / 59 assertions, package validator, Python parsing, relative-link checks and `git diff --check` passed. No further native retry or broad route rerun was needed. The change is ready for independent review; publication remains pending that review, with no commit/push in this correction task. Prior full-3B, actual recovery, design worktree, strict Eval, connector, protected discovery and Orca Chat gates remain unchanged.

## Seventh increment: actual Architect checkpoint and user rejection — 2026-10-28

The reviewed delegation fixes were published as `5c2782d90232d86b200638eab1927775e785ccb2` with the verified GitHub-associated author/committer; remote and draft PR #6 head matched. Both current-head workflows passed: [40655717590](https://github.com/chrison18/codex-pstack/actions/runs/40655717590) and [40655717587](https://github.com/chrison18/codex-pstack/actions/runs/40655717587). The PR now describes actual runtime/Arena/Investigation behavior changes rather than claiming instructions are unchanged. No merge occurred.

The new `accept-codex-architect-reframe.py` reuses the research native Client and snapshot helper. One real thread receives two sequential user turns; it does not restart a new task and label it continuation. CLI `0.164.0-alpha.11.1`, fresh catalog, parent and all declared How/design/judge selections Luna/medium, against isolated Luna/high defaults. Tested package source was `5c2782d` plus this new harness; no product instruction changed for this scenario. Eight actual delegates matched the declared pair and used fresh scoped starts without prompt-level `fork_turns` coaching.

### Checkpoint → rejection → revised implementation — scoped PASS

First turn: preserve tuple inputs and numeric return, reject negative quantities with `ValueError`, and stop at the synthesized design without implementation or application execution. How spawn 217 read the entry at 318 and returned static source/caller grounding at 788. The primary wrote/read back grounding at 804/817 before candidate starts 832/901. Candidate 1 proposed streaming validation/accumulation; candidate 2 retained the input snapshot for validation before reduction. These are small alternative data flows with different buffering and validation timing, not different model families or a claim of large-system architectural diversity. Both include caller usage, signatures/types, module maps, pseudocode and rationale/rejections. Their finals at 1647/1476 preceded judge spawn 1749. Judge entry/grounding/candidate reads at 1807 preceded its return at 1903 and primary synthesis. Primary final 2477 explicitly requested the checkpoint answer and waited. The captured checkpoint changed only five round-1 design/grounding files; production `app.py` and historical `check.py` were byte-identical.

The harness then submitted the explicit rejection in a second `turn/start` on the same thread (follow-up begins after event offset 2484): exceptions and numeric return were rejected; the new goal was a two-key dictionary containing the total of accepted rows and ordered zero-based indexes for rejected negative-quantity rows, including one-pass iterable support. Implementation of only `app.py` was now authorized after revised synthesis. Round-1 artifacts had to remain unchanged.

Second How spawn 2615 read entry/context at 2669 and returned static evidence at 2771. Revised grounding was written/read back at 2864/2877 and explicitly identified the old numeric assertions as superseded. New candidates started at 2889/2962: a streaming summary fold versus classification into product/index lists followed by reduction. Entry and revised grounding reads appear at 2976/3137 before their own writes; finals 3645/3627 preceded judge spawn 3770. Judge read the entry, grounding, red flags and full candidates at 3798/3838, then returned at 4491; primary synthesis at 4599, read-back at 4612, and the first production edit at 4689 followed. Only the primary executed application checks, at 4702: empty/ordinary inputs, multiple rejected positions in order, exact dictionary keys and a generator all passed. Final 5054 described the revised contract, superseded old check and preserved rejected artifacts. Independent harness verification returned `revised contract passed`, exit 0.

Final snapshot checks confirm the complete round-1 tree stayed unchanged, only `app.py` plus round-owned artifact files changed, `check.py`/configuration/HEAD/index stayed unchanged, and temporary auth was removed. No first-round design was silently implemented before rejection or retained as the old public contract afterward. The second-round synthesis recorded why streaming was selected and buffering rejected; the parent inspected both full sketches in addition to the judge. This proves explicit user-driven reframe and authorized continuation across a design checkpoint. It does **not** prove the separate automatic Scrap trigger for repeated implementation friction, crash/context recovery, code-worktree variants, autonomous continuation or Orca Chat parity.

### Read audit, recovered errors and harness review

The run was not error-free: initial runtime path lookup failed at 165, singular `resolve` incorrectly received `--selections` at 187, then corrected path/flags resolved before delegation. Some candidate principle paths and one copied absolute grounding path were wrong; the actual workspace-relative grounding read succeeded before candidate output. These were bounded command corrections, not model substitution or permission bypass.

Read evidence was checked against matching raw call outputs, not only successful aggregate command status. First-round candidate 1 entry call 914/output 941 succeeded while other operands failed; its grounding read was recovered separately at 1227. Candidate 2 call 1087/output 1090 contains the actual entry body even though a later `&&` principle read failed; grounding was read at 1114. Second-round candidate 1 call 2976/output 2979 contains both entry and revised grounding bodies despite a different failed `cat` operand. Candidate 2 call 3137/output 3157 contains both. An overall nonzero exit neither proves all operands failed nor licenses claiming unread references succeeded. How and judge entry/grounding reads above were also inspected. Delegates used static-only source/artifact inspection; application execution was reserved for the second-turn primary after synthesis.

Coordinator review caught a cleanup exception hazard in the new harness. After the native capture ended, `finalize_capture` was changed to guarantee an auth unlink attempt even when client shutdown throws, persist both shutdown and unlink failures in `result.json`, and return failure when cleanup errors exist. Two credential-free negative tests exercise close failure with a real dummy symlink (target retained, link removed) and unlink denial (error recorded). The native run preceded this cleanup-only change and its actual auth removal was independently verified; no additional model run is represented as testing the changed cleanup path.

Reproduce with a fresh catalog:

```sh
python3 -B scripts/accept-codex-architect-reframe.py --codex /absolute/codex --model gpt-6-luna --effort medium --catalog /tmp/pstack-reframe-catalog.json
```

Raw events, prompts, snapshots and full artifacts remain local. New harness/evidence changes remain uncommitted for review. Next feasible design gate is a separately bounded Scrap scenario driven by repeated structural friction, not another identical user-rejection run; all other retained 3B/UI/recovery gates stay open.

Local validation after the cleanup correction: **36 package tests / 61 assertions passed**, including both cleanup fault cases; package validator, Python parsing, relative-link and diff checks passed. These local checks do not extend the native run's behavioral scope.

## Eighth increment: controlled repeated structural friction — 2026-10-28

The reviewed checkpoint/reframe increment was published as `368c016cddc5510be161faf48b1a9a50bc738db3`, with verified author/committer and exact remote/PR #6 head. Current-head CI passed [40658003756](https://github.com/chrison18/codex-pstack/actions/runs/40658003756) and [40658003796](https://github.com/chrison18/codex-pstack/actions/runs/40658003796); PR remains draft and unmerged. The following new fixture and evidence are uncommitted for review.

### Predeclared fixture and proof boundary

Read the actual Architect Scrap rule: repeated same-kind structural deviations require stopping extension of the failing shape, rerunning How on discovered constraints and returning to Arena; a single edge case is insufficient. Before the model run, coordinator review accepted the following bounded fixture and verdict criteria. The seed `DESIGN.md` explicitly identifies itself as a manually prepared acceptance handoff, not a design previously chosen by this live agent.

Fixed contract: `prepare(customer, rows)` materializes rows and returns a receipt handle; `render(before_render=None)` returns exactly customer/total, with independent retained handles and reentrant callback support. Callers cannot coordinate storage reset/restore. The seeded implementation instead puts all receipt state in one module-level current-receipt dictionary. Two unchanged consumers independently expose that same ownership failure:

- Retain Ada and Bob handles, then render Ada: the seed returns Bob's result.
- Render Ada while its callback prepares/renders an Audit receipt: the seed returns Audit's result for Ada.

A simple single-receipt/empty-input control passes. Host preflight ran each negative separately (each failed) and the full unittest suite (three tests, two failures), so one assertion cannot hide the second deviation. A host-only reference implementation proved all fixed tests satisfiable with per-receipt state; it was not placed in the live fixture or prompt. The native prompt asks only to continue Architect implementation, inspect the design/code, run fixed checks and deliver under explicit ownership/model boundaries. It does not mention Scrap, a repeated-failure count, the shared-state cause or a replacement shape.

Predeclared full success required actual native recognition of the common structural cause, no patching of that shape before regrounding, completed How before renewed Arena, two meaningfully different ownership/data-flow/interface alternatives, judge/primary synthesis and verified implementation. A direct functional repair or two packaging variants is insufficient. This is a controlled existing-design probe, not production autonomous discovery, a new requirement, user rejection or interruption recovery.

### Native result — functional repair PASS; full Scrap FAIL

One native run only, tested package `368c016` plus the new harness, CLI `0.164.0-alpha.11.1`, fresh catalog and declared Luna/medium parent/roles. Raw events remain local. The primary read the entry and workflow at 70/82 and executed the actual baseline suite at 175. At 315 it identified both failing contract cases as the shared latest-receipt cause. Thus the controlled common-cause recognition is observed, not inferred solely from final code.

The primary wrote grounding from its own source inspection at 344 and read it back at 357. It then spawned candidate writers at 369/445 **before** How spawn 821 and its completion at 1507. The primary's initial file read/grounding does not substitute for Architect's required delegated How route. The candidate finals were already at 1111/1427; no renewed candidate round followed the How evidence. This fails the predeclared reground-before-Arena order even though How later confirmed the same source mechanics and the final grounding was updated at 5198.

Both candidates read the entry and initial grounding (entry reads at 437/522; grounding/reference calls at 536/693) and wrote within their assigned directories. However, candidate 1 stores `(customer, tuple(rows))` in receipt fields, while candidate 2 closes over that same per-handle snapshot and reduces it at render time. State ownership, retained data and main computation are the same; the difference is object fields versus closure encapsulation. The judge at 3710 acknowledged the closure added indirection without a distinct caller capability, but neither it nor the primary required a genuinely different second structural shape or stopped for the missing comparison. The final still called these “two structurally distinct sketches”. That claim is not accepted under the existing Architect standard; no gate is relaxed to make the run pass.

There was no production patch before the judge and synthesis. Primary implementation at 5269/5282 removed module-shared state; actual checks at 5295 and independent host verification passed all three tests. Only `app.py` and owned artifact files changed; fixed `DESIGN.md`, consumers, tests, configuration, HEAD and index were preserved. Auth cleanup succeeded with no recorded errors. Functional correctness and scope preservation therefore pass within this fixture, while complete Scrap remains failed.

Additional retained observations:

- Early role-availability uncertainty did not block actual `poteto-agent` starts; the accepted starts are the capability evidence, not the initial commentary about a summarized role list.
- Seven spawn requests produced six actual starts. The first Why source-control request at 886 was rejected at 889 with `agent thread limit reached`; one later request at 1435 succeeded at 1444 after completed work freed capacity. This is a concrete concurrency limit with a bounded retry, not model substitution or evidence of two investigators.
- The Why investigator and synthesizer found only the manual seed commit and did not invent historical motivation. External sources were out of scope; this does not establish connector coverage.
- Candidate 1 also wrote `CHECKLIST.md` within its owned directory despite the conversational-checklist instruction. This is a bounded instruction-following deviation, not an out-of-directory write, and is retained rather than silently ignored.

### Review boundary and next fix

The new `accept-codex-architect-scrap.py` reuses the native Client, snapshot helper and reviewed cleanup finalizer. `test_codex_architect_scrap.py` proves the separate failures, normal control, full-suite coverage and host-only satisfying witness; functional exit zero is explicitly labeled UNREVIEWED for workflow semantics. No product instructions were changed after this failed run, and no repeat was made to obtain a green result.

Next smallest correction to review: make completed delegated How plus primary reconciliation an explicit pre-fan-out dependency, and require a concrete ownership/data-flow/interface difference before accepting a second Architect candidate. If candidates converge to the same snapshot structure, replace one with a genuinely different viable shape or stop and disclose the missing comparison, as the existing rule already requires. These are package-level workflow enforcement gaps, not a reason to modify Lingentic policy or advance phases 4/5. Keep this failed capture and validate a future correction separately.

Local checks: **37 package tests / 63 assertions passed**, package validator, Python parsing, relative links and diff checks passed. Full Scrap and the other original 3B/UI/recovery gates remain open.

### Post-probe workflow clarification — pending native verification

The reviewed six-file fixture/evidence increment was published as `e9cb808c6ea90ed6a138af4ffad6c42c7e3b3ba5`; remote head matched and both workflows passed ([40660287288](https://github.com/chrison18/codex-pstack/actions/runs/40660287288), [40660287259](https://github.com/chrison18/codex-pstack/actions/runs/40660287259)). Author and committer use the repository owner's verified public noreply identity.

The subsequent uncommitted package clarification makes delegated How completion and primary source reconciliation a prerequisite to freezing Architect grounding and launching candidates. Architect now defines concrete ownership/lifetime, data-flow/computation and interface-responsibility evidence for runners, judge and primary; equivalent encapsulations cannot establish structural diversity. One replacement is permitted for unchanged framing, followed by explicit incomplete stop if comparison still fails. Arena and runner instructions reference that central contract; ordinary Arena convergence, legitimate How fallback, greenfield exceptions and read-only boundaries remain intact.

These are workflow constraints, not executable scheduling or semantic guarantees. No new native model run was started in this increment; the previous full Scrap FAIL remains unchanged. Next targeted verification: rerun the predeclared controlled fixture after review, inspect actual How completion/reconciliation before every candidate start, and inspect concrete candidate differences plus judge/primary comparison before implementation. If candidates converge, inspect the bounded replacement or honest stop instead of demanding a passing implementation. Full 3B, UI and recovery gates remain open.

Post-change local checks: package validator, 37 package tests / 63 assertions, 34 relative Markdown link targets and `git diff --check` passed. These structural checks do not prove native ordering or semantic diversity.

## Ninth increment: package-driven controlled Scrap verification — 2026-10-28

**Verdict: scoped controlled Scrap repair PASS; convergence/replacement/stop branch NOT RUN.** This is one new run after review of the package clarification, not a retry of the unchanged failed package. The eighth increment remains FAIL. The manually seeded design and two independent fixed consumer failures remain controlled fixture evidence, not a claim of production-discovered friction or lifecycle recovery.

Source was published `e9cb808c6ea90ed6a138af4ffad6c42c7e3b3ba5` plus the reviewed uncommitted Architect/Arena/runner guidance. Runtime was Codex CLI `0.164.0-alpha.11.1`; a fresh native catalog validated the predeclared parent, design and research/judge pool `gpt-6-luna/medium`, against isolated global Luna/high defaults. The unchanged committed `accept-codex-architect-scrap.py` supplied the same seed, fixed requirements, tests and user prompt; no prompt-level How-order, diversity or Scrap answer hints were added. Tested package SHA-256 identities:

| Reference | SHA-256 |
| --- | --- |
| `architect.md` | `bf16f459a2814c0fb93a6095d3fc4c6cbedb4eee1dac7695a8c6ac5eadcb8636` |
| `arena.md` | `e5a0df79c86f394edc225da32bcaa077f6c981f76d0649a34171a36f14c9412b` |
| `architect/runner-prompt.md` | `8a084e45ee587f7e9c53360ace6e4b80faf06d3c73b15a1c1271bc553a2b210d` |

### Actual sequence and delegated context

Zero-based positions in the locally retained native event stream:

- Primary read package entry/runtime/Architect at 84, then Arena/How at 97. Actual baseline execution at 111 reproduced two failures and one passing control. It identified their shared-state cause at 172, read the fixed contract and sources at 181/477, and deferred implementation pending research/design. No production patch occurred until 4111.
- How spawned at 515, read entry and source context at 589, and completed at 1718. Why history and synthesis completed at 1858/2811, retaining unknown historical intent. The primary reconciled the How/history findings against its inspected sources at 1987, wrote the resulting shared grounding at 2831 and read it back at 2841. Both candidate spawns, 2853/2875, were later. No candidate raced its prerequisite How.
- Candidate 1 actually read entry, Architect references and frozen grounding at 3084. Candidate 2's raw call/output at 3044/3068 contains those same required reads; later principle-path recovery did not erase the successful entry/grounding reads. Both wrote only their separate candidate directories and finished at 3582/3369 before judge spawn 3692.
- The primary read every candidate file at 3673. Judge read entry at 3754, Architect/Arena comparison instructions at 3776, grounding at 3793 and candidate files at 3805/3871. Its observed comparison at 3866 and final at 3955 distinguish render-time retained rows from prepare-time result snapshots; this was not inferred only from the primary's final claim.
- Seven requests produced seven actual native starts: six `poteto-agent` assignments (How, Why investigator/synthesizer, two candidates, judge) and one `comment-sicko` review. Every observed start resolved Luna/medium with independent-start requests. The comment reviewer read entry at 4210 and the diff/input evidence at 4228/4279/4291. Research/review used existing source context; no new grounding was required from those delegates. All delegate commands were static reads or authorized candidate artifact writes; no delegate imported/executed the app or tests.

### Structural comparison and implementation

Candidate 1 retains materialized rows for each receipt's lifetime and sums during every render. Candidate 2 materializes and aggregates inside `prepare`, drops the row collection and retains only customer/total. Actual types, pseudocode and rationale show a different retained-data lifetime and computation boundary: repeated O(rows) rendering and row storage versus one-time aggregation and constant-sized retained result. Public caller signatures agree; a mere wrapper distinction is not the accepted difference.

Judge and primary agreed these were viable distinct shapes, but disagreed on the preferred base. Judge preferred candidate 1's direct shape and compatibility; primary's synthesis at 3991/4005 records independent scoring, arithmetic-timing/type risks, and chooses candidate 2's data lifecycle while removing its extra snapshot wrapper and narrowed type aliases. The implemented `app.py` at 4111 actually materializes/sums in `prepare` and retains customer/total fields; it does not silently revert to candidate 1. Tests at 4128 and independent host verification both passed all three cases; diff checks passed.

Only seven paths changed: `app.py`, four candidate documents and two synthesis documents. Snapshot comparison found no changes to fixed `DESIGN.md`, `consumers.py`, `check.py`, role/configuration files or other paths. HEAD/index were preserved; temporary auth was removed and cleanup errors were empty. No checklist file was created. The final's phrase that candidates “remained read-only” is imprecise: they wrote authorized design artifacts, while remaining static-only with respect to the application; the actual record takes precedence.

### Retained limits and next gate

Early resolver calls used wrong paths and an unsupported singular `--selections` argument; the agent recovered through local discovery/help before any spawn. Principle leaf paths also needed local correction. Preserve these failures as execution friction, not a reason to rerun until flawless. No capability or model substitution was observed.

No convergence occurred, so the one-replacement limit, constrained replacement ownership and honest incomplete-stop behavior remain **NOT RUN**. The next bounded native gate is a separately predeclared convergence scenario to inspect that branch without coaching its decision or widening directory authority. The new workflow guidance remains prose, not runtime scheduling/semantic enforcement. The original automatic-discovery, actual dropout/crash/network, code-worktree and Orca Chat/UI limits and full phase 3B dependencies remain; no phase 4/5 advance or publication occurred here.

Local package validator and all **37 tests / 63 assertions** passed. Existing fixture proof/cleanup tests are included; no new framework or acceptance harness change was needed. Raw logs, fixture paths and incidental runtime identifiers remain local. Package changes and this evidence await coordinator review before publication.

## Tenth increment: controlled existing-artifact convergence — 2026-10-28

The [single reviewed convergence probe](architect-convergence-evidence.md) correctly recognized two manually seeded fields/closure proposals as structurally equivalent, with actual initial judge reads and primary reconciliation. It then started **two** replacement candidate writers while describing them as one round, violating the package's one-candidate-once limit. Overall bounded regression **FAIL**; three functional tests pass but do not override that verdict. Originals/config/HEAD/index and cleanup were preserved; all seven actual delegates used Luna/medium. The stop branch was not taken. No rerun or product fix followed; keep this point open while returning to the original design worktree/actual-failure queue, as the finite closeout review requires.

## Eleventh increment: ordinary Arena in real code worktrees — 2026-10-28

The [single code-worktree run](arena-code-worktree-evidence.md) passed its scoped route: two actual full-contract candidates wrote disjoint Git worktrees at a declared non-default base, a static judge followed both terminal events, and primary selected B with explicit provenance into a separate integration worktree before real verification. All three actual delegates used Luna/medium; 72 host assertions passed for each candidate and integration. Identity/scope/base checks and archive-before-cleanup passed. A primary checklist file inside its owned artifacts violated the conversation-only instruction and remains recorded; this is not a flawless-compliance claim. The harness now conservatively preserves worktrees on unknown activity rather than inferring settlement from server close. Actual failure/crash/network handling remains next; the Architect replacement-limit failure is unchanged.


## Twelfth increment: global replacement count and incomplete stop — 2026-10-28

One unchanged controlled-convergence fixture run after the reviewed central count clarification produced six actual Luna/medium delegates and exactly one replacement writer/package. Initial judge and primary recognized original equivalence; the replacement finished before final judge/primary comparison, then the primary truthfully stopped with incomplete comparison and unchanged app. [Detailed evidence and interpretation limits](architect-convergence-evidence.md#reviewed-count-clarification-single-native-verification--2026-10-28) record scoped count/stop **PASS**, with implementation **NOT PERFORMED** and the unchanged seed still failing two of three host checks. Conservative row-retention interpretation and an early corrected two-sketch checklist remain limitations; the earlier actual two-replacement FAIL is preserved. No runtime enforcement, zero-replacement stop, viable-replacement implementation, UI/recovery or full 3B claim follows. Product/evidence remain uncommitted for review; no further native run occurred.
