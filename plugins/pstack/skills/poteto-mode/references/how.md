# How: architecture and runtime behavior

Use within an explicitly activated Poteto Investigation for “how does X work?”, a code walkthrough, or placement/ownership/layering questions. Explain enough for a senior engineer to form a working mental model. Use [Why](why.md) for historical motivation. These are workflow references, not separate native `$how` or `$why` entries.

Read [the runtime contract](runtime.md). Keep the checklist in conversation or authorized external scratch. Inspect state before and after; do not edit code, create a repository checklist, install roles, configure models, commit or write to remote services during research. A read-only assignment is prose; enforce the permission boundary in the parent sandbox when available.

## Assess and explore

State a reasonable interpretation if the target is ambiguous and continue within that scope.

- **Simple:** a narrow function, utility or single module. Use one explainer, with [the explainer prompt](how/explainer-prompt.md), omitting the explorer-findings block. It explores and explains in one pass. Prefer this path when in doubt.
- **Complex:** multiple files/services, a cross-cutting feature or architectural overview. Divide the question into 2–4 distinct angles. Give each explorer [the explorer prompt](how/explorer-prompt.md), the original question, its bounded angle, the absolute entry path and read-only scope. Dispatch independent reads concurrently where supported. Wait for all findings, then give one explainer every finding, including contradictions and gaps, plus the explainer prompt.

## Delegate using Codex

Use registered `poteto-agent` for both explorer and explainer assignments. Resolve each assignment's model through `runtime.py resolve PROJECT how-explorer` or `how-explainer` with the observed parent model/effort, an explicit task selection if supplied, and the current native catalog or host-provided snapshot. Pass the resolved `model` and `reasoning_effort` to the actual native spawn. Do not translate the inherited Flash/Pro defaults into guessed Codex model names. Default is exact parent inheritance through the resolver.

A resolved workflow role key is a model preference, not a native agent name. Do not spawn an invented `how-explorer` agent. Give delegates this reference, the relevant prompt and the absolute Poteto entry path; they gather evidence, not ownership of the whole workflow. Keep sources read-only and do not delegate again from a delegate.

If no registered role/spawn is available or delegation is not authorized, use the Investigation's primary-only read path with the same evidence and output requirements, and disclose which delegation steps did not run. Do not install/configure anything to unblock it. If resolution rejects a supplied model/effort or native spawn rejects it, report that step blocked without substituting a model or using fallback to evade the explicit selection.

## Present and verify

Use Overview, Key Concepts, How It Works, Where Things Live and Gotchas only where useful. Describe concrete calls and data flow with actual file/line citations. For multiple communicating components, include a small diagram if it clarifies the flow. Do not invent historical intent from current behavior.

Inspect the explainer's cited code and reconcile contradictions before presenting. Light edits for clarity are fine; correct unsupported claims rather than blindly forwarding a delegate's answer. Report unavailable checks and sources. Match named principles and execution claims to the actual tool record as required by Investigation, and recheck workspace state.

Source: `skills/how/SKILL.md` and its two prompt references at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex adaptation preserves simple/complex exploration and synthesis, replaces host-specific tools/model rules, and explicitly retains the read-only fallback and authorization boundaries.
