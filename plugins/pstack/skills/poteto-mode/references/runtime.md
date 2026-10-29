# Codex runtime contract

## Roles and installation

The package ships role templates as resources. Codex discovers standalone project roles in `.codex/agents/`; it does not register these resources merely because the plugin is installed. With explicit setup authorization, run `python3 <entry-dir>/scripts/runtime.py install /absolute/project`. This creates only the two role files and an ownership receipt. Project configuration must be trusted by Codex. Restart the session after setup. Do not modify trust automatically.

Native role files deliberately omit model and effort. Those fields can override spawn settings in Codex. Existing user agent files are never overwritten. Repeat setup verifies ownership; removal refuses edited or substituted files. `uninstall` removes only unchanged, receipt-owned roles. Project model choices are retained separately, so removing agents does not erase preferences. The short entry link remains managed by the repository's separate phase 1 helper.

## Model resolution

Run `python3 <entry-dir>/scripts/runtime.py models` to read the native app-server `model/list` catalog. It uses existing authentication without copying credentials or changing providers. Failure to list models is a limitation, not permission to guess a model identifier. If a nested app-server cannot run inside the model sandbox, the host may run `models --output /absolute/scratch/catalog.json` before the task and explicitly supply that file with `--catalog` to configure/resolve. Snapshots expire after one hour. They are host-provided evidence of discovery, not a guarantee of subsequent account access; rejected spawns still stop the step. Never invent or rewrite a snapshot to admit an unavailable model.

Before delegation use `resolve PROJECT ROLE --parent-model MODEL --parent-effort EFFORT`. Supply values actually observed in the current host, not the catalog default guessed as the current parent. If current parent settings are unavailable, ordinary inherited delegation may omit overrides, but exact inheritance is unverified when native agent defaults exist. Report this limitation; do not claim the model gate passed.

The resolver reads only `.codex/pstack-models.json` on explicit activation. Precedence is an explicit task selection (`--model`, optional `--effort`), the role selection in that file, then the observed parent model and effort. `inherit` preserves the parent's exact pair. Selecting a model without an effort uses its advertised default. The result contains explicit `model` and `reasoning_effort` for the native spawn call, including inherited values, so native global subagent defaults do not silently change them. Validate all choices against the current catalog. An unavailable model or incompatible effort stops resolution without substitution.

`configure PROJECT ROLE MODEL [--effort EFFORT]` validates and records a role selection. Use `inherit` without an effort to reset that role. Supported role keys are `feature`, `bug-fix`, `investigation`, `comment-sicko`, `how-explorer`, `how-explainer`, `why-investigator`, `why-synthesizer`, `interrogate-reviewer`, `arena-runner`, `architect-runner`, `arena-judge`, and `swarm-worker`. These keys select workflow model preferences. Research, panels and generic workers reuse the native `poteto-agent`; comment review retains `comment-sicko`. Preference keys do not install additional agent definitions. Show the choices before making requested preference changes. A task override is ephemeral and never changes the saved role choice. Native role files edited to contain model settings invalidate this contract; setup verification must pass first.

## Questions, delegation and checklist

Use available native spawn, message/follow-up and wait mechanisms. Inspect the actual tool schema; do not invent Antigravity tool names. Give a delegate its scope, entry path, expected evidence, write ownership and resolved settings. Wait for and inspect the result. The primary reviews the diff and writes the answer. Missing tools or rejected settings produce an actionable limitation; do not silently change the role or model. For Feature and Bug fix, stop the workflow and report the blocked delegation; do not replace mandatory delegation by primary implementation. Investigation may use the documented primary-only read path.

### Capability evidence before fallback

Inspect the tools directly declared in the current session, including native collaboration namespaces and the `spawn_agent` schema's available `agent_type` roles. A `functions` orchestration tool's `ALL_TOOLS` list inventories its nested tools, not every directly callable tool. An empty search there does not establish that a directly declared collaboration tool or registered role is missing. Call direct native tools through their declared interface, not as invented `tools.*` members inside an orchestration cell.

Use the actual role schema together with the project installation receipt/verification and resolver result. Successful resolution validates the project settings; it does not alone prove host role loading. Conversely, a role listed by the current native spawn schema is available evidence that must not be discarded because a nested-tool search was empty. When the required role is declared and resolution succeeds, perform the prescribed scoped delegation with the resolved settings. If evidence conflicts, inspect only the relevant declarations and receipt or run the documented local verification; do not probe unrelated privileges or install/change configuration.

Report a missing capability only with concrete evidence: absent required role in the actual native schema, failed registration verification/resolution, or an actual tool rejection. Distinguish absence from a rejected model, permission denial or transient launch failure; do not relabel one as another. Preserve each workflow's existing fallback policy: read-only Investigation can use its documented primary path when the required role truly cannot run, while mandatory Feature/Bug delegation remains blocked. Never infer permission to mutate from fallback.

### Independent starts on the supported Codex host

For a new independent, explicitly modeled delegate, inspect `spawn_agent` first. When its schema exposes `fork_turns` with `none`/`all`, use `fork_turns: "none"` together with the resolved `model` and `reasoning_effort`. On the tested host, full-history forks do not accept model overrides and may fail to locate a parent rollout. A fresh start avoids that dependency; it does not change permissions or establish file isolation. This rule applies to scoped independent work, not a blanket ban on context inheritance or continuing an existing delegate.

A fresh delegate has no parent conversation. Supply a self-contained brief: the user's goal, required behavior and constraints, authorized actions and prohibitions, absolute project/base and owned output paths, absolute entry and relevant reference paths, plus existing grounding when the selected workflow requires it, expected evidence and done predicate. Require entry and any workflow-required grounding reads before work; retain workflow/checklist ownership in the primary. For independent candidates, give the common task and grounding without other candidates' outputs; give the read-only judge the rubric and completed artifacts only after writers finish. Do not rely on a model name or role file to convey this context.

Before calling spawn, fill and check this compact brief for **each** new delegate (including judges); placeholders are not usable values:

```text
Goal and done predicate: <user outcome and required evidence>
Task and constraints: <complete scoped assignment, allowed actions and prohibitions>
Project and base: <absolute working directory and actual ref when applicable>
Read first: <absolute poteto-mode/SKILL.md>; <existing absolute grounding path when required by the selected workflow, otherwise N/A>; <relevant references>
Ownership: <absolute writable paths, or read-only>; no other writes or nested delegation unless authorized
Return: entry and applicable grounding/reference reads, changed files, commands/results, limitations and skipped work
```

Grounding is mandatory for Arena/Architect, not a new artifact requirement for every route. For Feature, Bug fix or read-only Investigation without a grounding artifact requirement, mark grounding N/A and pass the complete task context and relevant references. Never create files merely to fill this template or violate a read-only assignment.

If the actual schema lacks this fresh-start mechanism, use only its documented equivalent when it supports the required model and scoped context. Otherwise report the capability block; do not invent fields, drop explicit selections, silently inherit settings or retry a permission denial. Follow-up to an existing delegate may preserve its state when the task requires it, subject to the same ownership and authority boundaries.

Prefer a native question tool when available; otherwise ask a concise question in conversation. Observe factual answers with tools before asking the user. Existing task authorization does not grant permission to send messages externally, merge, deploy or schedule future work.

Copy the selected playbook's steps into a checklist before work. Use a host checklist tool if available. For persistence, write a Markdown checklist at an explicit task-owned path and update it as work progresses. Retain pending steps, mark completion only after evidence, preserve failed steps as failed and skipped steps with a reason. Investigation uses conversation state or external scratch, never a new file in the target repository. Follow-ups retain the active task checklist; a new task requires explicit activation again. Session recovery is phase 4 work.

## Read-only review panels

`resolve-panel PROJECT interrogate-reviewer --parent-model MODEL --parent-effort EFFORT [--selections JSON] [--catalog PATH]` returns the full validated `reviewers` array, `distinctModels` and `modelDiversity`. Task selections are ephemeral and contain only `model` and optional `effort`; `{}` uses the saved role or parent. At least two are required. Without selections, two reviewers use that same saved/parent pair. No panel is spawned or preference written by this command; the primary starts delegates only after the whole call succeeds. Model diversity counts distinct model IDs, not differing efforts.

## Design pools

`resolve-panel` also accepts `arena-runner` and `architect-runner`, with the same atomic validation, precedence and `reviewers` result field as review panels. `arena-judge` uses singular `resolve`. Pools do not spawn agents or establish write isolation. Follow [Arena](arena.md) for candidate ownership, completed-writer ordering and primary synthesis, and [Architect](architect.md) for structural diversity and optional checkpoints.

## Swarm slices

`swarm-worker` uses singular `resolve` for each worker, allowing any positive worker count and distinct task choices per race arm. Resolve the full set before spawning. Follow [Swarm](swarm.md) for explicit base refs, one writer per actual worktree, bounded shared local-state verification and combined integration proof. The resolver does not create worktrees, grant machine-state access or execute workers.
