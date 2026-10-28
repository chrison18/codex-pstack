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


## Supported initial Chat launch — 2026-10-29

**Scoped PASS: actual Orca structured Chat, literal short-entry skill injection/loading and harmless read-only marker task.** Earlier GUI focus failures remain historical. Visible picker selection, same-Chat follow-up, fresh ordinary control and project role/install/update/remove acceptance are NOT RUN in this increment.

Checkout `16b491cf001a6c5656b77ec1c10df0f52e8487e1`, package `0.2.0-alpha.1`, Orca `1.4.242`, provider CLI `0.164.0-alpha.11.1`. No model override: actual context reports existing `gpt-6-astra/ultra`. Verified retained fixture, README digest/HEAD and project-local entry symlink before executing exactly one documented `orca agent launch --agent codex --surface chat --worktree path:<verified-fixture> --prompt '<literal prompt>' --json`. The single-quoted prompt was exactly:

```text
$poteto-mode Read README.md and report its marker. Read-only: do not modify files, install anything, delegate, or contact external services. Report any missing capability honestly.
```

Receipt returned `outcome.kind: structured` and `prompt.delivery: submit` / `prompt.outcome: journaled`; no fallback, duplicate or retry occurred. Receipt alone did not pass loading. Supported search index status was enabled/current; a fresh Codex search restricted to the exact fixture path returned one hit with structured-session identity matching the launch receipt. Only the precise task-owned provider file returned by that mapping was inspected, not unrelated chats/stores.

Zero-based provider records: 11 contains the submitted prompt; 13 injects the actual named skill/path and maintained SKILL contents; call16/output21 reads entry/runtime; call25/output29 reads Investigation/principles; call35 reads prove-it-works and status; call41/output45 reads README line1 with `ORCA_ENTRY_28` and unchanged Git status; final48 returns the correct marker and truthful read-only/role limits; task_complete51 confirms completion. This is actual injection and tool evidence rather than self-report alone.

Independent before/after snapshots are identical, HEAD/index unchanged; only the pre-existing alias remains untracked. No install, delegate or external-source call occurred. Project roles are absent and delegation was explicitly prohibited; no registered-role or clean-global-policy claim follows. The original user Chat was untouched; this completed test Chat is retained for follow-up.

Completed provider capture SHA-256: `59d176aa7e4766f445afc4a8dda5878931844090e9f63cbc634cffe36a8205df`. Raw paths/identities/receipts/host context remain private. Next: same-task follow-up in the precisely mapped Chat through a supported interface (or minimal owner input), then a separately launched fresh ordinary control and project setup/update/removal evidence. None ran here. Evidence remains uncommitted for coordinator review; no full core/phase4/phase5/merge completion claim. Snapshot, local link/privacy and diff checks passed.


## Fresh ordinary control and remaining core steps — 2026-10-29

**Scoped ordinary-control PASS.** At checkout `a20a06de87bd0a9fb5bcb7532820c9861a37da2b`, launched exactly one fresh structured Codex Chat in the same verified fixture with only `7+5, digits only, no tools` using the documented launch command. No skill mention, evaluation preamble or orchestration instructions were submitted. Receipt confirms structured mode and journaled submission. A fresh exact-path conversation search returned the precise structured-session mapping to its own provider file; only that mapped evidence was inspected.

Zero-based records: user11 is the exact prompt, assistant final16 is exactly `12`, task_complete19 confirms completion. The complete captured turn contains **zero function/custom tool calls and zero skill-injection blocks**; no pstack activation or entry read appears. Actual context remains existing Astra/ultra on CLI `0.164.0-alpha.11.1`. This supports the ordinary prompt control for this client/fixture, not all prompts or a clean global installation claim. Fixture snapshots still exactly match the saved post-positive baseline; HEAD/index and alias are preserved. Capture SHA-256 `f1ad49389911842700f4572a4cc708d6e2ffa189c075e2eb9c1472f1c42bcc92`. Exact test identities/receipts stay private.

**Same-Chat follow-up: NOT RUN, supported send route not established.** The retained positive Chat is identified by its launch/search mapping; a new Chat is not a substitute. Version-matched guide/command schema documents initial Chat launch but no same-structured-Chat selection/send flag; terminal send's contract remains a live terminal, and the historical structured-handle failure is not retried. Advertised runtime send capabilities do not supply a request schema. No guessed RPC, orchestration injection or CUA/getApp was used. Minimal owner action if no supported API emerges: in the positively identified **Read README Marker** test Chat in the disposable project, submit once: `For this same task, repeat the marker and confirm whether any files changed; keep the same read-only limits.` No skill mention. Then inspect that same mapped provider/task for continuity and unchanged files. Title alone is not identity; coordinator retains exact session ID and project path. Both test Chats remain available; original user Chat is untouched.

### Read-only installation lifecycle preparation (not executed here)

Current fixture has the maintained project-local entry alias but no project role install. Read the packaged setup skill/runtime and actual installer/link helper; the supported project-scoped commands are:

```sh
python3 <checkout>/scripts/link-codex-entry.py <project>
python3 <entry>/scripts/runtime.py install <project>
python3 <entry>/scripts/runtime.py verify <project>
python3 <entry>/scripts/runtime.py uninstall <project>
```

The link command is only for an absent alias: it refuses an existing destination, so do not rerun it over this fixture's valid link. Install creates `.codex/agents/poteto-agent.toml`, `.codex/agents/comment-sicko.toml` and `.codex/pstack-agents.json`; it refuses unowned existing files. Repeating install verifies ownership and returns already-installed. Verify checks current-package hashes; uninstall removes only unchanged receipt-owned role files/receipt, retaining model preferences and the separate skill alias. No `update` command exists: same-version install is idempotence, not an upgrade test. For changed role resources, verify/uninstall with the old package before installing the new one; never overwrite edited roles or claim the new verifier can validate an old receipt. Preserve choices and unrelated config in before/after snapshots. The live entry symlink follows its target checkout, so capture actual target/version for discovery after update.

Required surface: an authorized task-owned host installer command capable of writing this project's protected metadata, with actual permission results recorded. Earlier native-agent protected `.agents` denial is evidence for that specific route, not proof that a host installer must fail. Conversely user authorization does not guarantee sandbox access: if the host command requires escalation, use normal approval review, never bypass protections. Trust must not be auto-changed; honor any real client trust requirement and start a fresh test Chat after setup to observe actual role loading. Files/receipt alone do not prove current Chat registration. Removal of the separately owned alias is a distinct guarded unlink (verify symlink target first, never delete the maintained package), followed by fresh-client discovery checks. Global installation is unnecessary.

No install/update/remove or trust action occurred here; this is the precise next lifecycle plan, not a PASS. New evidence remains uncommitted for review. Local link/privacy/diff and independent snapshot checks pass; no product fixes, advanced runs or extra Chat turns were added.
