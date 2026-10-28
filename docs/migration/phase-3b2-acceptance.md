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
