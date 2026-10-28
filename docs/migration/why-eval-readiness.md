# Why / strict Eval readiness — 2026-10-28

Read-only readiness assessment at `1e831cf3d0f2b8ef853c687548761ac18d0be8cf`, Codex CLI `0.164.0-alpha.11.1`. No new native model, investigator, synthesizer or judge ran. No fault injection, source-pin change, product change or gate relaxation occurred. Preparation status: capture feasibility inspected; strict delivered-input blinding is BLOCKED on encrypted child task content, so no new fixture or native run was constructed. Coordinator review accepted this bounded assessment for publication; no native run is authorized by this record.

## Publication checkpoint

The reviewed [fault-interface assessment](native-runner-fault-feasibility.md) is published at the above SHA with the established public author/committer identity. Remote and [draft PR #6](https://github.com/chrison18/codex-pstack/pull/6) match; exact-head workflows [40671279144](https://github.com/chrison18/codex-pstack/actions/runs/40671279144) and [40671279069](https://github.com/chrison18/codex-pstack/actions/runs/40671279069) succeeded. Its closing “uncommitted” sentence is its pre-publication review status, superseded by this checkpoint. No new full-suite rerun is claimed for documentation publication.

## Why: a substantive question, but historical cross-category eligibility not established

Proposed fixed question: **Why did the migration choose explicit activation with `allow_implicit_invocation: false`, and what evidence limits extending that decision to Orca Chat?** This directly concerns convenient startup without silently activating a workflow in unrelated tasks.

| Category / concrete source | Actual evidence available | Limit |
| --- | --- | --- |
| Source control: phase-1 commit `c303a74e4e5e6f7e9f055b5eed49507bc59ddfbd`, plugin `agents/openai.yaml`, `docs/migration/phase-1-entry-evidence.md` | Local `git show` read the false policy and recorded explicit/ordinary-prompt controls, qualified-plugin and project-link behavior | Repository evidence establishes the recorded decision and tested host, not universal client behavior; GitHub copies and PR text are not a second independent category |
| Independently authored long-form documentation: [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), read on this assessment date | Actual primary web read explains explicit versus implicit invocation and the false-policy behavior | Current documentation is an independent source for mechanism, but this read did not establish its contents before/around the phase-1 decision or that it motivated the author; it cannot silently become historical design rationale |
| Issue tracker / team chat | No substantive linked issue or contemporaneous deliberation established in this bounded scope | Not searched across private systems; prior Slack Unknown-tool failure was not retried |
| Infrastructure / error tracking / analytics | No evidence connecting these categories to this activation decision identified in the inspected decision record | Excluded from the proposed bounded case for lack of a relevant linked forcing event; no claim of exhaustive searches or empty databases |

The official document is genuinely independent of this repository, unlike a copied PR. Nevertheless, the packaged Why contract specifically seeks historical motivation and long-form rationale recorded before or around implementation. Therefore **two-source mechanism comparison is source-ready in the primary, but the original native historical cross-category gate remains NOT RUN; qualifying historical second-category evidence is not yet established**. Do not relabel current documentation as a contemporaneous design record. A future eligible Why case needs a dated independent rationale/forcing-function source actually linked to the decision, or explicit review that a narrower mixed historical/current question satisfies the original gate; this report grants neither.

## Tool availability and read-chain boundary

Current primary declarations expose native collaboration spawn/follow-up/wait and shell reads; its nested tool catalog advertises GitHub fetch/file/commit/issue/PR reads, and `web.run` actually returned the official page. These are primary-host observations only. The current directly declared agent-type list does not contain `poteto-agent`; existing native fixture evidence elsewhere used a disposable registered role. An empty nested discovery search would not negate a directly declared role, and no such inference is used here.

The [earlier live-source record](phase-3b-live-source-evidence.md) proved primary GitHub reads, not fresh native delegate connector access. The corrected Investigation fixture proved registered-role local reads, not a web/GitHub connector read. Neither may be composed into a delegated cross-category PASS. No new child was started and no source tool was called on behalf of one; actual fresh-child public-source access is **unverified**, not assumed absent. No unrelated host configuration, private chat store or credential contents were inspected.

If an eligible Why case is subsequently approved, keep it to two investigators and one synthesizer, using the existing isolated research harness and declared resolver-selected catalog pairs. Require actual entry/investigator/epistemics reads, each assigned source read with substantive returned content, terminal completion before synthesis, synthesizer citation spot-checks, primary reconciliation and unchanged source/config/HEAD/index. A missing connector must yield a named gap; no manufactured second category, install, repeated unchanged Unknown-tool attempt or primary-only substitution may pass the delegated gate.

## Eval preparation result: delivered-input audit BLOCKED

The next preparation increment inspected **existing task-owned native captures**, before constructing a formatter fixture. These are the already documented portable Eval run and later Arena worktree run, not private session-store searches or new model calls. `accept-codex-research.py` captures app-server notifications through `Client.receive`; outgoing `Client.send` requests are not themselves a delivered-context receipt. The parent spawn call and returned artifacts alone cannot establish the child's complete actual input.

| Existing capture | Concrete observations (1-based JSONL lines) | Consequence |
| --- | --- | --- |
| Portable Eval | Lines 288/308 declare native **default** writers with `fork_turns: none`; delivered agent messages at 307/335 each have an input-text wrapper plus `encrypted_content` (740 characters). Judge spawn at 521 uses `poteto-agent`; its delivered message at 540 has an input-text wrapper plus encrypted content (1,548 characters). Later messages at 510/807 are also encrypted. | The gap applies to the exact fresh default-writer route proposed for Eval, not merely custom-role writers. Plaintext parent briefs do not prove full delivered writer or judge inputs. |
| Later Arena worktree | Delivered writer messages at 314/407 have encrypted content (3,256 characters each); judge message at 1127 has encrypted content (3,340 characters). Other user/developer messages and actual child commands are visible. | More recent capture confirms partial visibility rather than a missing event stream; visible command/read evidence cannot establish exclusion of a rubric or model mapping inside opaque inputs. |

Capture SHA-256 fingerprints, with raw logs and machine paths kept local:

- Portable Eval: `45f9d5937796800862618f6a3a49a8b20d32db3b4fe9fceffb918e4e7ef20bf8`.
- Arena worktree: `93d625010406068eb8b41c8d8d90f0e0787d62a88d1f08f7577a5c6c4710f5b2`.

The inspected CLI `0.164.0-alpha.11.1` protocol offers `thread/read` with optional history, paginated thread reads and experimental `thread/items/read`. Its persisted item schema explicitly permits `encrypted_content`; the read declarations do not promise decryption or a complete plaintext model-input receipt. No new protocol call was made against historical threads, and no alternate plaintext capability is asserted absent universally. **No supported complete delivered-input audit was established with the available captures/schema.** The existing files are enough to reproduce the concrete blocker; repeatedly running a model cannot repair this evidence boundary.

Accordingly, stop preparation here as requested: **no new formatter fixture, harness, tests, model selection or native run**. Existing limited artifact-comparison PASS remains unchanged; strict blinding/read-chain does not pass. There is no need to invent exact writer/judge inputs for a run whose required observation is currently unavailable.

### Visibility is not filesystem isolation

Neutral assigned trees, no provided peer paths/context, fresh starts and explicit scope are prompt/ownership controls, not proof that the filesystem prevents peer access. Future evidence may establish which reads were observed and which snapshots remained unchanged; it must not claim universal inability to access other trees. Even an observed absence of peer reads does not prove absence of peer/rubric information in encrypted delivered content. No OS isolation claim, privilege probe or workaround is proposed.

### Smallest prerequisite and subsequent one-case boundary

Next actionable review is whether a **supported task-owned plaintext delivered-input export or equivalent documented complete input receipt** is available for fresh default writers and the judge. It must cover initial context and subsequent task messages, with correlation to child/turn and visible read events; a sanitized parent brief alone is insufficient. If not available, retain the strict gate as BLOCKED and ask the coordinator to select the next original finite-queue item, without silently lowering the gate or authorizing implementation.

Only after that prerequisite is demonstrated and reviewed would the single formatter-guide case proceed: identical frozen source and organic briefs in neutral owned directories, four private criteria (input contract, fixed output examples, invalid-input behavior, unsupported performance claims), neutral judge output labels without model mapping, actual child input/read audit, writer completion before judging and primary reconciliation. Exact source, prompts, model/catalog selection and hashes must then be frozen before a run. No model comparison, different-family claim or promotion is implied. Existing task-owned cleanup settlement guards and independent auth finalization would be reused; no fixture/auth/server was created in this preparation, so there is nothing new to terminate or remove.

Historical Why, real crash/network handling, Architect replacement-count FAIL, checklist deviation, remaining Architect worktree coverage and Orca Chat entry/loading retain their existing statuses. Phase 4/5 dependencies and the 31-partial inventory are unchanged. This finding is a bounded environment/evidence limit, not authorization to reorder, merge or waive original gates.

Checks: parsed the two existing task-owned captures, inspected exact fresh-start requests and delivered-content types, read the capture implementation and generated protocol schemas, checked local Markdown links/privacy and `git diff --check`. No native model run or full package rerun was needed for this documentation-only result.
