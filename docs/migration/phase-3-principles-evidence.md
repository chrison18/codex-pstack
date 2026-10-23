# Phase 3: full principle references

This unit replaces six phase 2 summaries with all 24 inherited principle leaves. It does not add native skill entries, enable implicit invocation, or complete phase 3. Source baseline: `a06537a883278a63132e2518971166002f3de5de`; phase branch base: `a25255330be51548e27c4a2bda4e9ca5af86dfcf`.

## Content and host adaptations

The inventory maps each principle to its own packaged Markdown reference. The index includes each applicability description, and each leaf retains both that description and its full substantive body. Several upstream leaves put most of their guidance in the description; copying the body alone would lose that guidance. Internal principle links resolve inside the installed package. Source skill frontmatter is converted to readable applicability text; these references are not independently discoverable native skills.

`python3 -B scripts/sync-codex-principles.py` checks all 24 reviewed transformations without writing. `--write` deliberately regenerates them. CI runs the check after source inventory validation. The transformation records the following host changes explicitly:

| Source principle | Adaptation |
| --- | --- |
| Never Block on the Human | Reversible work stays within existing user scope and host permissions; applicable prior authorization counts without repeated confirmation |
| Sequence Verifiable Units | Use the agreed base and repository Git rules instead of blindly rebasing a shared branch |
| Separate Before Serializing Shared State | Concurrent code writers need separate worktrees and named starting refs; branches or spawns alone do not isolate a checkout |
| Guard the Context Window | Bulk delegation requires authorization; bounded searches and summaries remain available |
| Prove It Works | Distinguish observed execution from static reasoning/planned checks; retain the evidence-trail advice while marking the full show-me-your-work lifecycle unavailable |
| Explain the Number | Retain repeatable measurement, repeated runs, spread and limiter criteria; the full benchmark-checklist remains pending |
| Type System Discipline | Keep the type-design advice and links to migrated principle leaves; the dedicated typescript-best-practices skill remains pending |

The inherited source files and hashes remain unchanged. Both package entries still have `allow_implicit_invocation: false`. The primary selects applicable leaves and reads them fully before applying them; neither an index read nor familiarity with the advice is proof that a leaf loaded. Investigation adds a final audit of named principle and execution claims against actual tool records.

## Real-client method and observed failures

Client: `codex-cli 0.163.0-alpha.11.1`, explicitly selected `gpt-6.1-sol` / `low`, 2026-10-23. The harness uses an isolated temporary Codex home, a task-owned fixture and project entry link, a parent read-only sandbox, and only a temporary reference to existing authentication. It removes that reference in `finally`. No project roles are installed. Delegation and external service searches are forbidden for these fixtures; the documented primary-only investigation fallback is expected. This is CLI evidence, not desktop UI evidence.

Reproduce with:

```sh
python3 -B scripts/accept-codex-principles.py \
  --codex /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex \
  --model gpt-6.1-sol --effort low
```

The harness records commands, replies and before/after file-kind/mode/content/link/directory snapshots outside the investigated workspace. It also checks that the fixture does not acquire Git metadata. It checks named principle titles against full content actually returned by successful inspection commands. That last check is conservative and does not judge whether the principle was correctly applied; inspect reasoning and execution claims manually. Raw transcripts and authentication references are not committed.

The first network-restricted attempt failed workspace routing. Network-enabled attempts also intermittently failed routing/TLS before producing a reply; those are NOT RUN behavior checks, not passes. No endpoint, certificate, provider or authentication configuration was weakened to work around them.

The first completed premise response found the correct key collision, but claimed to have independently replayed it without a corresponding execution command. It also named Model the Domain without reading that leaf. Behavior result: FAIL despite unchanged fixture state. Adding execution accounting to Prove It Works produced a real Python replay on the next completed run, but the reply still overclaimed which leaves it had read. That run also remains FAIL for claim accuracy. The investigation's final audit and the harness's full-content claim check were added before the final rerun.

## Final candidate results

| Case / observation | Result |
| --- | --- |
| All 24 full-content transformations, package links and 87 pinned source digests | PASS |
| First completed premise run: correct diagnosis but unexecuted replay claimed and unread leaf named | FAIL |
| Second completed premise run: actual replay, but unread leaf still named | FAIL |
| Completed isolation response before the final audit change | PASS for that earlier revision only; proposed checks clearly separated from executed proof |
| First final-candidate rerun after the audit change | NOT RUN: both exited 1 with `workspace routing discovery failed`, with no model reply |
| 2026-10-23 retry of unchanged f5032db: premise and isolation | PASS: both exit 0, unchanged snapshots, no named-but-unread principle leaves; actual commands and final claims manually matched |
| Representative final-candidate behavior acceptance | PASS on f5032db after routing recovered; earlier failures are retained above |

Local final-attempt evidence directory: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-principles-live-gj7suvm9`. Earlier completed premise evidence: `pstack-principles-live-2yegqnff` and `pstack-principles-live-q84yk_v9` under the same temporary root. Earlier completed isolation evidence: `pstack-principles-live-aljsvfqm`. These disposable raw files may expire; the summarized failures above are retained in Git.

Static/regression results on the final candidate: 23 Bun tests with 35 assertions; 69 inherited tests with 247 assertions; strict TypeScript checks for the package/inventory tooling and inherited typecheck; source inventory and all 24 transformation checks; CLI context-injection installation/qualified invocation/implicit exclusion/short alias/removal smoke; shell syntax and `git diff --check`. Static checks are separate from the real-client behavior audit.

The earlier completed isolation response did read the shared-state and verification leaves, reject branch-only isolation, and propose either one serialized writer or separate worktrees with named bases. It explicitly labeled the worktree checks as proposed rather than executed. The workspace snapshot was unchanged. This is evidence of reasoning about isolation, not execution of phase 3 A7/A8/A9.

## Scope and remaining work

These 24 inventory units are now `adapted`: their full portable advice is packaged with reviewed host adaptations and traceable source mappings, and the two representative claim-audit cases passed. These checks do not establish that every principle works in every context. Source completeness is established separately by the transformation check and all 87 pinned source digests.

How/why, design panels, remaining quality/prose/control/authoring skills, expanded playbooks, real parallel writers, non-default base refs and local-state access remain phase 3 work. No phase 3 merge or desktop acceptance is claimed here.

## Successful retry on unchanged f5032db

Evidence directory: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-principles-live-brudjm2i`. Both harness results: `exit: 0`, `changed: []`, `namedButUnreadLeaves: []`, `leafClaimChecksPassed: true`, `artifactChecksPassed: true`. The temporary authentication reference was removed. Client/model/effort and prompts were unchanged.

Premise inspection: tool item 4 returned the attack/root-cause/measurement/laziness/proof/lever leaves; item 6 returned shared-state/domain/foundational leaves. Item 7 actually executed the original `store` function with both write orders and 1, 3, 10 repetitions. The output retained only the last regional value for each customer. The reply correctly identified key collision, proposed a composite `(customer, region)` key without implementing it, and marked reader compatibility unverified. Every named applied principle had an observed full-leaf read.

Isolation inspection: the shared-state/proof and other selected leaves were read in full. The answer rejected branch-only isolation, recommended separate worktrees with recorded starting refs or one writer for the entire edit/test/stage/commit cycle, and explicitly called the proposed worktree checks unexecuted. Actual `shasum -a 256 jobs.py` output matched before and after. Git status failed because this deliberately minimal fixture is not a Git repository; the reply reported that limitation instead of counting it as passed. Harness snapshots independently matched all workspace entries. This remains reasoning evidence, not A7/A8/A9 execution evidence.
