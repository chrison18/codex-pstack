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

## Separate host installer lifecycle — 2026-10-29

**Scoped host lifecycle PASS; fresh-Chat registration/removal discovery and distinct-resource upgrade NOT RUN.** At checkout `e831068dd9cb01491a020d06ab69ae5414a961d7`, ran the model-free [lifecycle harness](../../scripts/accept-codex-install-lifecycle.py) once in a newly created, exclusively owned temporary project, separate from both retained Chat tests. It invokes the actual link helper and packaged runtime CLI, not mocked installer functions. No Chat/model, credentials, trust toggle, global installation or GUI operation was involved. Normal host shell writes succeeded without escalation or a protected-write denial; this does not invalidate the earlier native-agent route denial.

The fixture seeds an unrelated `.codex/config.toml` setting and a valid `pstack-models.json` preference (Luna/medium), plus a README. These are preservation sentinels, not an executed model selection. Actual commands returned installed → verified → already-installed → removed, each exit 0. Full installed snapshots before/after the repeat match. Verification checks both receipt-owned role files against current packaged hashes. Uninstall retains settings/preferences; guarded unlink checks the exact entry symlink target before removing only that link. Task-created empty directories are removed with `rmdir`, with no recursive deletion. Final file/directory/mode/hash snapshot exactly equals the seeded baseline. The temporary baseline and private command/snapshot audit are retained for review; no process or Chat was launched there, and the earlier positive/negative fixture was untouched.

Role hashes: `poteto-agent.toml` = `e3ddf6059eb06f0f0eab7a627191b7c5e4bd58005eafc4625ee2a9dca1531caf`; `comment-sicko.toml` = `d6a57a02c0c928bcead953eb58e2a749fd568a1cf12697507ad582907e157107`. Available all-ref resource history contains original feature commit `a306053942f45fd97abc7d7b1fabacf5f2d46a71` and its published squash `a25255330be51548e27c4a2bda4e9ca5af86dfcf`; both hashes equal current resources. No genuinely distinct prior role-resource revision was found in this history. Same-version repeat proves idempotence only: a meaningful changed-resource upgrade remains untested, with the old-package verify/uninstall then new-package install procedure retained above. No version or changed resource was invented to manufacture an upgrade result.

**Next bounded client step:** after review, reinstall the alias and roles in this same owned baseline, verify them, then launch one fresh mapped Orca Codex Chat through the documented launch interface and inspect actual skill injection, native registered-role declaration and a harmless scoped delegate entry/read chain. Existing Chats cannot prove newly loaded roles. Preserve unrelated preferences; if real client trust is required, report that boundary without toggling it. After settled client evidence, uninstall/guarded unlink and use a new mapped client to check removal discovery. These client steps did not run here and are separate from host PASS. Same-Chat follow-up in the retained positive Chat remains pending; root reports Accessibility/screenshot statuses granted but AX window reads still return permission_denied, so neither an ungranted-permission claim nor safe UI input follows.

New harness/evidence remain uncommitted for coordinator review. Original core acceptance, phase dependencies and advanced support limits are unchanged.

Local checks: `python3 -B scripts/test_codex_runtime.py` (13 passed), `python3 -B scripts/test_codex_acceptance_state.py` (5 passed), harness syntax parse, relative links, new-section private-path check and `git diff --check` passed. These checks do not substitute for pending client registration/discovery.

## Actual Chat role use and removal control — 2026-10-29

**Scoped registered-role use PASS.** At published checkout `6c48884c1cb8751b410266819e75d957d5a0dec5`, a separate disposable Git fixture copied the host lifecycle's synthetic README and configuration/preference sentinels. The original host baseline and original entry/follow-up fixture stayed unchanged. Orca's repository importer rejected the non-Git baseline; a folder import also rejected the supplied project identity. Neither error was treated as successful registration. The separate Git fixture was then registered through the documented repo interface, linked, installed and verified with the actual package helpers. No global trust setting was changed.

One documented structured Chat launch submitted exactly:

```text
$poteto-mode Use the registered poteto-agent to read README.md and report its exact text, and comment-sicko to review that same tiny README wording. Keep all work read-only: no file changes, installation, external access or extra delegates. If either registered role is unavailable or blocked, report the exact limitation and stop rather than substituting a role or claiming success.
```

Supported exact-fixture search mapped the returned structured Chat to its provider capture. Actual calls at zero-based records 52 and 58 requested `poteto-agent` and `comment-sicko`, respectively; successful returns at 55 and 61 established native role dispatch rather than role names in prose. Final delegate reports at 78 and 95 returned the exact README bytes and a concrete wording finding. The primary independently read the README, checked its hash and Git status, returned its final answer at 105, and completed at 108. Child reports say they read the maintained entry and applicable references; their complete delivered instructions are encrypted in this capture, so this evidence does not independently certify every child input or exact inherited model setting. No model override was supplied. Completed parent capture SHA-256: `90af4839051d09b6c4bfdd1caac17447a801082b756087cb763ef3aeaff1897a`.

After both delegates and the parent settled, independent host checks confirmed README, unrelated config and model preferences matched the original sentinels, and the package verifier still passed both installed roles. The owned uninstall succeeded, retained preferences, and the separately owned entry alias was unlinked only after checking its target. Only empty task-created directories were removed.

**Fresh removal control: scoped PASS for observed capability reporting.** A new structured Chat in that same cleaned fixture received a no-tools/no-delegation request to report whether those two agent types and the skill were present in its current declarations. Final record 16 reported all three absent; completion is record 19. Capture SHA-256: `eb2abd77a3a4688087086c174436397f4d4c3bb807d25932f4b354f9e7f892c1`. This combines verified host removal with the fresh client's report, not a direct export of its complete tool schema. Test Chats are retained; the original user Chat is untouched. Same-Chat follow-up and package-transition client discovery remain separate pending checks.

## Published-source package transition — 2026-10-29

**Scoped host source-update PASS.** A separate synthetic fixture used exact Git-exported package/helper files from published old source `a25255330be51548e27c4a2bda4e9ca5af86dfcf` and new source `6c48884c1cb8751b410266819e75d957d5a0dec5`. The actual sequence was old link/install/verify, old-package uninstall and guarded alias unlink, then new link/install/verify. Original README, config and model preferences retained their bytes/modes throughout. Installed snapshots and command results are retained locally. An initial extraction attempt stopped before installation because the local Python tar API lacked the requested filter; the completed attempt exported named Git blobs into a fresh owned directory instead.

Old entry SHA-256 is `cb4805df67ffce42bcef53998997015623cda50f55aedeab10e23b4aef8eb9da`; new entry SHA-256 is `bfc1857cbadaeb6d207bc1abea3329f94b72735d9417a56dec10cb8a273b1aba`. This is a real change of package source and entry content, with installed roles now referencing the new package path. Both sources use the same release version and identical role templates. Therefore this proves the documented source-package replacement path, not a new release-version migration or distinct-template upgrade. No version or template was fabricated to improve the verdict.

**Fresh updated-entry Chat PASS.** The fixture was subsequently initialized as a disposable Git repository and registered with Orca. One fresh structured Chat received `$poteto-mode Read README.md and report its exact text. Also report the resolved path and SHA-256 of the SKILL.md for this invoked skill. Keep this task read-only: no installation, file changes, delegation, or external services.` Supported exact-path search mapped the launch to its own provider capture. Record 13 injected the new exported package path, calls 16 and 36 read/hash that actual entry, final 43 returned the expected README and new entry digest, and completion 46 settled the turn. Capture SHA-256: `5640dbfe067bfa4052a5541a202ee2b9caea1aed7754ff53aa0a336901661e39`. The exported package remains separate from the live checkout, so the result is not inferred merely from a moving source symlink.

Independent post-Chat snapshot equals the saved new-install snapshot. After settlement, new-package uninstall and guarded alias removal restored the original fixture snapshot, excluding the separately introduced Git metadata as the snapshot helper specifies. Model preferences were retained; no global configuration/trust changes occurred. Public evidence contains no raw session paths or transcripts. Same-Chat continuity still requires the retained original positive Chat; these fresh sessions do not replace that check.
