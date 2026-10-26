# Phase 3B: live source access supplement

## Scope and result

On 2026-10-26, the current Orca primary inspected the Why source-access and confidence requirements against real repository history and live GitHub reads. The inspected head was `2b3c0d0e0a8abe96baba613cde6410b213c3c821`; the worktree and index were clean before and after research, before writing this evidence increment. No remote writes, role installation, model configuration or prior-session resumption occurred.

This is a primary-only host supplement, not a new native `$poteto-mode` invocation, delegated investigator/synthesizer run, desktop acceptance or full Why workflow pass. No new agent ran. Existing native local-history evidence remains in [the research record](phase-3-research-evidence.md). The live GitHub connector worked; advertised Slack search failed. Genuine cross-category synthesis remains NOT RUN, and Why stays partial.

## Question and anchor

Question: why was phase 3 split into 3A and 3B, and did merging 3A waive the remaining phase 3 gates?

The anchor is the phase dependency table in `docs/migration/codex-migration-plan.md` and the increment rule in `CONTRIBUTING.md`. Local `git log --all -- docs/migration/codex-migration-plan.md` led to `d49501f4ed0a18d59fcf3ca587b33431b9600d46`. Reading that commit's actual plan and contribution-rule diff showed the transition from one PR per phase to consecutive 3A/3B increments. `git rev-parse --is-shallow-repository` returned false; this does not imply access to private discussions or pre-import upstream history.

## Actual source calls

All GitHub calls were scoped to `chrison18/codex-pstack`. These are observations of the returned payloads, not inferred from tool discovery. The connector records are retained in the current conversation; private transcripts are not copied into the repository.

| Operation | Arguments / scope | Observed result |
| --- | --- | --- |
| `github_get_pr_info` | PR 4 | Merged; merge SHA `288561b1feda1cf199f46ae36745ec47df6fb4ba`. Description explicitly separates the reviewed 3A increment from remaining 3B gates. |
| `github_fetch_pr_comments` | PR 4 | Successful response with `comments: []`. No review transcript was returned; the description's review narrative is not an independently inspected review. |
| `github_fetch_commit` | `d49501f4ed0a18d59fcf3ca587b33431b9600d46` | Returned the split commit and file patches. The plan/contribution changes agree with local Git. |
| `github_get_pr_info` | PR 5 | `state: open`, `draft: true`, `merged: false`, head `2b3c0d0e0a8abe96baba613cde6410b213c3c821`. The body retains live Why and other limits. |
| `github_search_issues` | `repo:chrison18/codex-pstack is:issue created:2026-10-21..2026-10-26`, topn 20 | Successful response with `issues: []`. Only this repository/date window was searched. |
| `slack_slack_search_public` | Exact keyword `"codex-pstack"`; `after:2026-10-20 before:2026-10-27`; joined public channels only; bots included; no context; limit 20 | `isError: true`, `Unknown tool` (`slack.slack_search_public`). No search coverage established; not a zero-result search. No private-channel search or installation attempted. |

## Findings and confidence

**Direct:** the recorded purpose was to land the verified foundation while retaining outstanding gates. The split commit says the owner requested review and merge of PR 4 before continuing, and explicitly keeps phases 4–6 dependent on 3B. This establishes the recorded rationale, not an independent reconstruction of the owner's original conversation. [Split commit](https://github.com/chrison18/codex-pstack/commit/d49501f4ed0a18d59fcf3ca587b33431b9600d46).

**Direct:** PR 4 describes itself as an incremental merge and explicitly excludes live vendor coverage, cross-source synthesis, desktop parity and concurrent writer isolation from its claims. Its merge is not evidence that those checks passed. [PR 4](https://github.com/chrison18/codex-pstack/pull/4).

**Direct, time-bounded:** PR 5 was still a draft at the time of the read and retained phase 3B limitations. [PR 5](https://github.com/chrison18/codex-pstack/pull/5).

**Unsupported competing hypothesis:** splitting phase 3 waived its remaining acceptance gates. The inspected change and PR description expressly contradict this interpretation. An alternative schedule or commercial motivation is **Unknown**; these reads do not establish one.

The local commit, its GitHub copy, checked-in plan and PR description are related source-control records. Their agreement is useful corroboration, but does not establish independent authorship or genuine cross-category synthesis. The empty comments response cannot verify the review narrative in the PR body. No assertion is made about messages or issues outside the searched scope.

## Seven-category coverage

| Category | Coverage and limit |
| --- | --- |
| Source control | Local history, plan diff and live GitHub commit/PR reads succeeded as listed above. |
| Issue tracker | Repository-scoped GitHub issue search succeeded with zero results for the stated dates. No Linear/Jira search claimed. |
| Long-form documents | Checked-in migration plan inspected as part of the same source-control evidence. No linked external design document identified in inspected records; external document systems not searched. |
| Team chat | Public Slack query failed with Unknown tool. Unavailable, not empty. Private channels and DMs not searched. |
| Infrastructure observability | Not queried: the anchor changes delivery/dependency policy, not a runtime threshold or deployment; inspected records contain no incident/metric lead. No observability acceptance claimed. |
| Error tracking | Not queried: no runtime defect or error identifier motivates the inspected split. No error-service acceptance claimed. |
| Product analytics/warehouse | Not queried: no usage threshold, experiment or analytics lead appears in the inspected split. No warehouse acceptance claimed. |

## Remaining acceptance

- Live GitHub source reads: observed in this primary host session only; native delegate access remains unverified.
- Genuine cross-category synthesis: NOT RUN; no second substantive independent category was retrieved. Do not manufacture one from duplicate Git/PR records.
- Slack: BLOCKED by the advertised tool's actual dispatch failure. Other vendor categories remain unverified.
- Full Why acceptance still requires an eligible real case with substantive sources in multiple categories, actual read access in the intended client, calibrated synthesis and scope checks. Existing local native tests cannot be combined with this host supplement to claim an end-to-end live run.

This research authorizes no merge or phase 4 work. Preserve remaining gate labels, separate source copies from independent evidence, and treat unavailable tools as access gaps. The evidence publication itself changes documentation/metadata only; runtime and inherited source files remain unchanged.

## Checks for this documentation increment

Package validation, local evidence-link resolution and `git diff --check` passed. The package suite initially passed 33 of 34 tests; the portable-fixture test failed because invoking Bun by absolute path did not put Bun on its Python child's PATH. With the existing Bun directory added only to the test process PATH, that exact filtered test passed (1 pass, 5 filtered out). No test or runtime source was changed. This is 33 initial passes plus a corrected-environment pass, not a claim of one clean full-suite run. HEAD and index remain unchanged; the four documentation/metadata files are local working-tree changes. No new CI or independent review is claimed.
