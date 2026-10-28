# Orca Codex Chat entry acceptance — blocked input surface

2026-10-28, Orca **1.4.242**, macOS; package checkout `612a111bf14106715364b40ed08fa1720b193631` with the accepted user-outcome documentation WIP. Primary target is Orca Codex Chat, not standalone desktop or CLI. After this attempt the owner accepted native `$poteto-mode`; a slash alias is no longer required. The original attempts remain recorded below.

## Setup and observations

Created a disposable Git project with a committed harmless README marker and a project-local `.agents/skills/poteto-mode` symlink to the maintained package entry. Package identity is pstack **0.2.0-alpha.1**; implicit invocation remains disabled. No roles, global skills, account configuration or existing project policy changed. `repo add` initially rejected a non-Git directory and succeeded after initializing only the disposable fixture.

`agent launch --agent codex --surface chat --focus` returned a structured Chat launch receipt. No prompt was attached. The returned structured-session handle was rejected by `terminal switch` and `terminal show` with `terminal_handle_stale`; re-listing that exact workspace returned no terminals. This is a control-path limitation for this attempt, not proof that the Chat did not exist. A supported `file open README.md --worktree path:<fixture> --focus` succeeded; its screenshot showed the fixture's README and a **Codex Chat** tab in the same workspace.

Computer-use capabilities allowed screenshots and coordinate clicks, but the accessibility tree exposed only window controls, with no focused element or Chat input. Clicking the observed Chat tab returned `window_not_focused`: the provider reported no focused topmost window and aborted the click. Following the prescribed one-time `get-app-state --restore-window` recovery produced a fresh screenshot; the click again returned `window_not_focused`. No further input attempts or alternate UI automation were used. This was a focus/observation limitation, not an `app_blocked` security denial.

Raw screenshots, session/control receipts and the fixture audit remain local, outside the repository. Screenshots may include unrelated sidebar content and must not be published. Public evidence records the reproducible steps and exact error classes without private paths or runtime IDs.

## Results

| Check | Verdict | Actual observation |
| --- | --- | --- |
| Disposable project and local alias | PASS | Alias resolves to maintained entry; committed README unchanged; only expected untracked `.agents/` exists |
| New Orca Chat shell | PASS, bounded | Structured launch receipt and visible Chat tab; not proof of provider readiness or loaded skill identity |
| Skill picker/discovery | BLOCKED | No accessible input; safe Chat selection failed after prescribed recovery |
| Literal `/poteto-mode` (historical requested spelling) | NOT RUN | Not typed/submitted; no discovery or injection result; no longer a release requirement |
| Native `$poteto-mode` (accepted target) | NOT RUN | Not typed/submitted; historical CLI evidence does not substitute |
| Harmless marker task / instruction loading | NOT RUN | No provider turn/output; actual injection versus prose interpretation cannot be assessed |
| Fresh ordinary-prompt control | NOT RUN | No prompt sent; absence of activity is not a negative-control pass |

No package correction was justified by an attempt that never reached input submission. Static prefix evidence in the [user-outcome contract](user-outcome-acceptance.md) remains separate from end-to-end proof.

## Next step and retained resources

Continue independent 3B2 acceptance and the [Cursor behavior comparison](cursor-behavior-delta.md); no slash adapter is needed. When a supported structured-session control path or safely focused composer is available, rerun native `$poteto-mode` discovery/selection and a read-only request to report the README marker and entry actually loaded, followed by `7+5, digits only, no tools` in a fresh chat. Capture visible submission and actual provider skill-loading evidence; model claims alone do not pass.

The task-owned fixture, symlink and empty Chat are retained locally for the coordinator; their identifiers are in the private fixture audit. No uncertain handle was used to close resources, and the original user chat was untouched. No global changes, runtime implementation, merges or recurring automation occurred. The existing phase gates remain unchanged.

Validation: diff/Markdown link checks and fixture HEAD/status/README checks passed. Runtime tests were not needed for this documentation-only UI record; UI/provider acceptance remains blocked regardless of those local checks.
