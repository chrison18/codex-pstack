Internal reference within explicitly active Poteto. Follow [runtime](../runtime.md) and use the [workflow index](../workflow-index.md) for dependencies. Reference names are not additional native commands.

# Remove AI code slop

Check the diff against main and remove AI-generated slop introduced in the branch.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).


Source: `skills/deslop/SKILL.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex host adaptations and evidence are recorded in the migration ledger.
