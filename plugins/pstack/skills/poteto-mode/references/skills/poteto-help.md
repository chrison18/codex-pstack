Internal reference within explicitly active Poteto. Follow [runtime](../runtime.md) and use the [workflow index](../workflow-index.md) for dependencies. Reference names are not additional native commands.

# Poteto help

Answer the question and give one usable prompt, with a link to the packaged file you read. A help request does not start implementation, install roles, change preferences or consume a review pool. A request to do work routes through the active entry instead. Infer the need from the conversation; ask a concise choice only when it changes the answer.

Use the [workflow index](../workflow-index.md) to pick a skill or playbook, read that reference, then explain its actual availability using [status](../status.md). Do not advertise inherited commands or unverified capabilities. How explains mechanics, Why investigates motivation, Teach combines them, Interrogate reviews a diff, Blast radius checks effects beyond it, Arena compares alternatives, Architect designs structure and Swarm partitions or races work. A plan is a deliverable and does not authorize execution.

Both native entries require explicit invocation: `$pstack:poteto-mode` and `$pstack:setup-pstack`. `$poteto-mode` requires the separately configured project short link; plugin installation alone does not create it. All other names in this index are internal workflow references, not additional native commands.

For setup, read [the setup entry](../../../setup-pstack/SKILL.md) and [runtime](../runtime.md). Show catalog-supported model/effort choices rather than vendor tiers or an invented cost budget. Missing `.codex/pstack-models.json` means no saved role preference; use the observed parent through resolution, not an assumed default. Setup creates only receipt-owned project roles when requested; no global rule changes. Role registration may require restarting the session. Existing files are preserved.

For proof, first discover an existing project verify skill/harness. If absent, explain Create verification skill; for properties tests rarely reach, explain Create formal verification skill and its bounds. Existing maps/checks are maintained with the corresponding maintenance reference. Setup/help does not automatically generate them.

Named-checkpoint recall, pickup and pause are supported through [task checkpoint and pickup](../session-lifecycle.md); [bounded in-turn continuation](../continuation.md) drives authorized work without routine continuation prompts. Broad provider-history access, destructive worktree cleanup and automatic external wake/recurring autonomy remain unavailable. Explain that gap rather than invoking a guessed tool. Ketchup uses this chat's already available state only; it is not cross-session recall.

For a prompt, state the goal, observable done check, evidence and constraints. Read [prompting](poteto-help/prompting.md) or [recipes](poteto-help/recipes.md) for examples. Adapt the example to the available Codex routes. Read current PR/CI state through available connectors only when needed for the answer; do not infer merge approval or mark drafts ready.

Keep the reply short unless the user asks for the full map. For a public source link use the actual repository/ref supplied by the task, not the inherited fork's main branch.

Source: `skills/poteto-help/SKILL.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex host adaptations and evidence are recorded in the migration ledger.

For a named task with a saved checkpoint, use [task checkpoint and pickup](../session-lifecycle.md). Example: `$poteto-mode Resume the task at <exact task directory> in <workspace>; reconcile uncertain work against its artifacts before continuing within the recorded authority.` The primary reads the named record and continues the appropriate existing route; no global history search or automatic wake is implied.
