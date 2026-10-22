# Phase 2 desktop acceptance

Run against the 0.2.0-alpha.1 development candidate on `feat/codex-core-workflow`. This is separate from the accepted 0.1.0-alpha.1 UI test. Record desktop version and the tested Git commit. Do not merge on the strength of CLI evidence alone.

Use three disposable project directories named feature, bug and investigation. Each starts as a Git repository with app.py, an unchanged check.py acceptance test, project role resources installed by runtime.py, and an optional native short-entry link. The investigator fixture must retain its full before/after state. Do not use a production project.

## Preparation

The plugin directory should show the candidate version after removing the old preview and reinstalling from this checkout's marketplace. The plugin exposes `$pstack:poteto-mode` and `$pstack:setup-pstack`. The separate native project link exposes `$poteto-mode`.

Codex must trust the fixture's project configuration and the chat must start with that fixture as its working directory after role setup. Do not change global trust or unrelated settings just to make a test pass. Choose and record a parent model/effort that the native catalog advertises. A resolved role's settings must match the actual selected parent; do not guess them from catalog defaults.

If nested app-server discovery cannot run from the desktop model sandbox, export a fresh catalog from the terminal first and explicitly give its path in the prompt:

```sh
python3 -B plugins/pstack/skills/poteto-mode/scripts/runtime.py models --output /absolute/scratch/catalog.json
```

A snapshot expires after one hour. The host must create it from native discovery; do not manufacture a catalog to avoid validation.

## Tasks

Include the observed parent model/effort and the catalog path when applicable. All work is confined to its fixture, with no commits, PRs or external messages.

| Fixture | Prompt | Expected observation |
| --- | --- | --- |
| feature | `$pstack:poteto-mode` Add multiply(a,b) to app.py, preserve add, verify with python3 -B check.py. Persist checklist in task.md. Only app.py and task.md may change. | Feature route; scoped poteto-agent implementation; primary checks the diff and behavior; comment-sicko review; test passes, check.py unchanged |
| feature follow-up | Continue the same task: rerun acceptance and update the existing checklist. | Same primary and checklist, no new independent workflow owner |
| bug | `$poteto-mode` Fix average([2,4,6]) returning 3 instead of 4 in app.py. Reproduce with python3 -B check.py first. Persist checklist in task.md. Only app.py and task.md may change. | Bug fix route; original test fails before the fix and passes after; delegation and parent review observed; check.py unchanged |
| investigation | `$poteto-mode` Explain total(items) in app.py with file/line citations. Do not change files, install anything or perform remote writes. | Investigation route; cited explanation; tracked and untracked file snapshots unchanged |
| new ordinary chat | `7+5，只输出数字` | Exactly 12; no workflow setup, checklist or delegation |

## Evidence and cleanup

Record each result as PASS, FAIL, BLOCKED or NOT RUN with the actual observations, not just the model saying it succeeded. Inspect tool activity and changed files. A missing role/model/tool is a limitation, not a passing delegate step. Owner-reported evidence is labeled as such; screenshots and app-version details are optional evidence rather than something the agent claims to have seen.

Remove the candidate plugin after testing if it was installed temporarily. Before deleting fixtures, remove their native skill links and unchanged owned roles with the documented uninstall command; do not remove unrelated files. Retain the local evidence needed to assess the result without committing private session transcripts.
