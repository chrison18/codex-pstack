# Codex runtime contract

## Roles and installation

The package ships role templates as resources. Codex discovers standalone project roles in `.codex/agents/`; it does not register these resources merely because the plugin is installed. With explicit setup authorization, run `python3 <entry-dir>/scripts/runtime.py install /absolute/project`. This creates only the two role files and an ownership receipt. Project configuration must be trusted by Codex. Restart the session after setup. Do not modify trust automatically.

Native role files deliberately omit model and effort. Those fields can override spawn settings in Codex. Existing user agent files are never overwritten. Repeat setup verifies ownership; removal refuses edited or substituted files. `uninstall` removes only unchanged, receipt-owned roles. Project model choices are retained separately, so removing agents does not erase preferences. The short entry link remains managed by the repository's separate phase 1 helper.

## Model resolution

Run `python3 <entry-dir>/scripts/runtime.py models` to read the native app-server `model/list` catalog. It uses existing authentication without copying credentials or changing providers. Failure to list models is a limitation, not permission to guess a model identifier. If a nested app-server cannot run inside the model sandbox, the host may run `models --output /absolute/scratch/catalog.json` before the task and explicitly supply that file with `--catalog` to configure/resolve. Snapshots expire after one hour. They are host-provided evidence of discovery, not a guarantee of subsequent account access; rejected spawns still stop the step. Never invent or rewrite a snapshot to admit an unavailable model.

Before delegation use `resolve PROJECT ROLE --parent-model MODEL --parent-effort EFFORT`. Supply values actually observed in the current host, not the catalog default guessed as the current parent. If current parent settings are unavailable, ordinary inherited delegation may omit overrides, but exact inheritance is unverified when native agent defaults exist. Report this limitation; do not claim the model gate passed.

The resolver reads only `.codex/pstack-models.json` on explicit activation. Precedence is an explicit task selection (`--model`, optional `--effort`), the role selection in that file, then the observed parent model and effort. `inherit` preserves the parent's exact pair. Selecting a model without an effort uses its advertised default. The result contains explicit `model` and `reasoning_effort` for the native spawn call, including inherited values, so native global subagent defaults do not silently change them. Validate all choices against the current catalog. An unavailable model or incompatible effort stops resolution without substitution.

`configure PROJECT ROLE MODEL [--effort EFFORT]` validates and records a role selection. Use `inherit` without an effort to reset that role. Supported role keys are `feature`, `bug-fix`, `investigation`, and `comment-sicko`. Show the choices before making requested preference changes. A task override is ephemeral and never changes the saved role choice. Native role files edited to contain model settings invalidate this contract; setup verification must pass first.

## Questions, delegation and checklist

Use available native spawn, message/follow-up and wait mechanisms. Inspect the actual tool schema; do not invent Antigravity tool names. Give a delegate its scope, entry path, expected evidence, write ownership and resolved settings. Wait for and inspect the result. The primary reviews the diff and writes the answer. Missing tools or rejected settings produce an actionable limitation; do not silently change the role or model. For Feature and Bug fix, stop the workflow and report the blocked delegation; do not replace mandatory delegation by primary implementation. Investigation may use the documented primary-only read path.

Prefer a native question tool when available; otherwise ask a concise question in conversation. Observe factual answers with tools before asking the user. Existing task authorization does not grant permission to send messages externally, merge, deploy or schedule future work.

Copy the selected playbook's steps into a checklist before work. Use a host checklist tool if available. For persistence, write a Markdown checklist at an explicit task-owned path and update it as work progresses. Retain pending steps, mark completion only after evidence, preserve failed steps as failed and skipped steps with a reason. Investigation uses conversation state or external scratch, never a new file in the target repository. Follow-ups retain the active task checklist; a new task requires explicit activation again. Session recovery is phase 4 work.
