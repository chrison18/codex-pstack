---
name: poteto-mode
description: Run the staged Codex pstack Feature, Bug fix or read-only Investigation workflow when explicitly invoked as $poteto-mode.
---

# Poteto mode

This is the staged Codex core workflow. Read [status](references/status.md) when asked about availability; report the verified scope and remaining evidence limits. Later workflows remain unavailable.

Activate only on explicit invocation for a new task. Follow-ups continue that active task. Installing this plugin or roles does not activate the workflow for ordinary new prompts. The primary chat owns the playbook, checklist, delegations, evidence and final answer.

Read [the runtime contract](references/runtime.md) before executing a task or configuring roles. Read only the applicable playbook and principle sections:

- New or changed behavior: [Feature](references/feature.md).
- Reported defect: [Bug fix](references/bug-fix.md).
- Read-only explanation or recommendation: [Investigation](references/investigation.md).

Create and update the playbook checklist; retain skipped steps with reasons. Delegation prescribed by the selected route is part of that explicitly invoked workflow, subject to host permissions and the user's scope. Pass this file's absolute path to `poteto-agent` and `comment-sicko`; inspect returned evidence yourself. Never delegate ownership of the full workflow.

For model setup, follow the runtime contract's configure/resolve commands only when requested. Do not load the inherited Antigravity tree, mutate global configuration or install project roles as a side effect of an ordinary task. Missing role/tool/model support must be reported before claiming that step completed. Later-phase workflows remain unavailable.
