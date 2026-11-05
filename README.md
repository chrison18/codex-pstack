# pstack for Codex

An explicitly invoked engineering workflow for **Orca Codex Chat**: start with `$poteto-mode`, describe the work, and keep following up in the same task. The primary and its delegates use one maintained package. Bounded tasks can retain checkpoints, recover named work and continue within an active turn without routine “continue” prompts.

This is a **source-checkout preview**, package `0.2.0-alpha.1`, not a tagged release or full migration. Core workflows, recovery and bounded continuation have scoped evidence. Automatic wake, recurring jobs and several advanced integrations are unsupported. See the [client/evidence matrix and all 87 capability dispositions](docs/migration/release-readiness.md).

## Set up a project once

Keep a checkout of this repository at a stable location. From its root, run these commands with your existing project path (Python 3.11+ on the tested POSIX host):

```sh
python3 scripts/link-codex-entry.py /absolute/path/to/project
python3 plugins/pstack/skills/poteto-mode/scripts/runtime.py install /absolute/path/to/project
python3 plugins/pstack/skills/poteto-mode/scripts/runtime.py verify /absolute/path/to/project
```

The first command adds the project skill link; the others install and verify `poteto-agent` and `comment-sicko`. Existing skills or edited roles are not overwritten. Unrelated project configuration and saved model choices are preserved. Nothing installs globally or changes `AGENTS.md`, trust or model preferences. If the host denies a protected write, stop and use its normal permission flow; do not bypass trust. Open the project in Orca and start a **new Codex Chat** so it can discover the entry and roles. An already-open Chat may retain old declarations.

## Use it

Type this in Orca Codex Chat:

```text
$poteto-mode Fix the failing test in this project, verify the fix, and report what changed.
```

Or start read-only: `$poteto-mode Read README.md and explain this project; do not modify files.` Follow up in the same Chat without repeating the entry. A fresh ordinary prompt does not activate pstack. Native `$` spelling is the supported entry; `/poteto-mode` and visible picker automation are not promised.

For sustained work, ask: `$poteto-mode Complete this bounded task, verify the result, and preserve a checkpoint so it can be resumed: …` Include the goal and any scope restrictions. The agent manages checkpoint commands. Keep the reported checkpoint location; after a restart, invoke `$poteto-mode` and ask it to resume that exact named checkpoint. It checks completed and uncertain effects before continuing. Cancellation is cooperative: it prevents later work but cannot undo or forcibly stop a tool already running. A stopped Chat does not wake itself.

For sequential agents under the original Chat, ask: `$poteto-mode Complete this task with supervised continuation: …` The Chat chooses and states finite worker/time limits, supervises one writer at a time, verifies each result and advances without asking you to continue. Additional workers consume model usage; the supervising Chat must remain active. Cancellation stops later work, but cannot preempt a running tool. This opt-in mode does not install a recurring job or resume after app shutdown. See the [bounded evidence and limitations](docs/migration/supervised-continuation-evidence.md).

Role models inherit the parent by default; no model change is required for setup. To request explicit choices, use the optional setup entry described below. Unsupported roles/tools must be reported rather than replaced by a claimed successful fallback.

## Update safely

A project link follows its source checkout. Do not change that checkout while a task is using it. Keep the old checkout until its roles have been removed with **its own** installer; this matters if role templates change.

1. Finish or pause active tasks and retain checkpoints. Obtain the reviewed new checkout separately and record its Git SHA.
2. From the old checkout, run `runtime.py verify PROJECT` then `runtime.py uninstall PROJECT` using the full script path shown above. Modified or unowned files cause refusal: inspect them instead of deleting them.
3. Remove only the link that points to that old checkout, using the guarded command below.
4. From the new checkout, repeat the three setup commands and start a new Codex Chat.

This is a **source update**. Re-running `install` on identical owned roles is idempotence, not an upgrade. The preview version has not been bumped to imply a new release; record source SHAs for reproducibility. Saved `.codex/pstack-models.json` remains yours.

## Remove project setup

First run the owning checkout's `runtime.py verify PROJECT` and `runtime.py uninstall PROJECT`. Then, from that same checkout, remove only its exact project link:

```sh
python3 - /absolute/path/to/project <<'PY'
from pathlib import Path
import sys
alias = Path(sys.argv[1]).resolve(strict=True) / '.agents/skills/poteto-mode'
expected = (Path.cwd() / 'plugins/pstack/skills/poteto-mode').resolve(strict=True)
if not alias.is_symlink() or alias.resolve(strict=True) != expected:
    raise SystemExit('Not this checkout’s skill link; nothing removed')
alias.unlink()
PY
```

Do not delete the package target or unrelated skills. Model preferences are retained intentionally. Start a new Chat to observe removal; existing Chats may retain loaded instructions. Keep checkpoints needed for later recovery.

## Optional plugin distribution

The project-local path above is enough for Orca usage. On clients supporting the tested marketplace interface, from this checkout you may instead/additionally install the packaged entries:

```sh
codex plugin marketplace add .
codex plugin add pstack@codex-pstack
codex plugin list --json
```

Plugin entries are `$pstack:poteto-mode` and `$pstack:setup-pstack`; the latter can configure a named project's roles/models on explicit request. The separate project link supplies `$poteto-mode`. Plugin removal uses `codex plugin remove pstack@codex-pstack` and `codex plugin marketplace remove codex-pstack`; remove owned project roles/links first. Plugin installation alone neither installs the project roles nor activates the workflow. Qualified desktop discovery/version display is not fully certified; consult the dated matrix.

## Development and attribution

Read [CONTRIBUTING](CONTRIBUTING.md), the [migration plan](docs/migration/codex-migration-plan.md) and [UPSTREAM](UPSTREAM.md). CI validates the Codex package and retained source integrity plus portable script tests; native client behavior is separately evidenced, not inferred from CI.

Adapted from Lauren Tan (poteto)'s [pstack](https://github.com/cursor/plugins/tree/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack), with Eric Zakariasson's cursor-team-kit and the Antigravity port by Kaitian Xie and contributors. Preserve the [MIT license](LICENSE). The inherited `skills/`, `agents/`, `automations/` and root manifests remain provenance/source, **not the Codex installation**. The [original inherited README at the pinned baseline](https://github.com/chrison18/codex-pstack/blob/a06537a883278a63132e2518971166002f3de5de/README.md) retains its original relative-link context and attribution; its host instructions are historical.
