Internal reference within explicitly active Poteto. Follow [runtime](../runtime.md) and use the [workflow index](../workflow-index.md) for dependencies. Reference names are not additional native commands.

# Author or modify a skill

The primary owns its voice, scope and outcome. Discover the target host's available skill-authoring guide; use Codex skill-creator when available, read it before authoring, and use current official guidance for unresolved schemas. Never invent a foreign built-in. If no guide is available, use the local skill contract: a directory with SKILL.md YAML name/description and only genuinely useful optional references, scripts or assets.

1. Ground real requests and dependencies. Keep only instructions that change a decision. Put conditional detail in linked references. A generated verification skill uses the matching create/maintain reference, not generic prose alone.
2. Preserve the target's invocation policy and user choices. New skills normally use native discovery unless the user requests explicit-only; pstack's two entries remain explicitly enabled by design. Internal pstack references add no native entries.
3. Validate frontmatter, links, scope and any executable helpers using the available validator. Run meaningful structural/behavior checks for workflow or code changes. Subjective prose edits need a careful read, not wording-matching tests.
4. For a complex skill, perform an independent realistic forward test in disposable state when authorized. Give the task and raw inputs, not the expected answer or suspected bug. Inspect actual outputs, side effects and tool evidence. Unsupported tests remain gaps.
5. Use [Opening a PR](opening-a-pr.md) only within delivery authorization. Do not overwrite unrelated skills, global configuration or existing project content.

Reply with the skill's purpose, important decisions, validation, behavioral evidence and remaining gaps. Propose a missing reusable workflow without automatically installing it.

Source: `skills/poteto-mode/playbooks/authoring-a-skill.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex host adaptations and evidence are recorded in the migration ledger.
