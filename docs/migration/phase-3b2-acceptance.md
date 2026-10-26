# Phase 3B2 acceptance closure

Branch `test/codex-3b-acceptance` starts from actual merged main `b9ad7434506b3785b531b66afa85d1ad040b9fbb`. PR #5 merged by squash on 2026-10-26 after independent review, the reproduced/fixed temporary-auth cleanup finding, local checks and both exact-head CI jobs for `75d65c5c8515ac6df6d5884b38dc163e35a12db5`. See [3B1 review](phase-3b1-merge-review.md).

This increment owns acceptance closure, not phase 4. Inventory remains 37 adapted, 31 partial and 19 deferred. A successful bounded probe clears only its named scenario; missing desktop, connector or proof surfaces stay visible.

## Retained work

| Area | Existing evidence | Remaining work |
| --- | --- | --- |
| Interrogate | Concrete two-model defect; native rejected-selection and missing-role boundaries; actual capacity-dropout disclosure below | Full two-completed-reviewer empty review, other dropout/recovery modes and desktop coverage |
| Arena / Architect | Artifact synthesis, How grounding, checkpoint and default implementation | Scrap/reframe/dropout, same-model pools, code-worktree and desktop variants |
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
