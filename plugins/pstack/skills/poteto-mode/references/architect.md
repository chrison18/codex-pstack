# Architect: explore structure before implementation

Use within explicitly active Poteto mode for a requested design or a change whose ownership and interfaces need exploration. The primary owns the checklist: ground → sketch → agree → implement → scrap if necessary. Read [Arena](arena.md) and the [runtime contract](runtime.md).

## Ground

Run [How](how.md) through its applicable route to explain the affected system with file/line evidence, including its explainer delegation when available and authorized. A primary source read alone does not complete that delegated route; any fallback must meet How's stated conditions and be disclosed. When ownership or layering changes, use [Why](why.md) to recover historical constraints and distinguish known reasons from guesses. Skip grounding only for genuinely greenfield work and say why. Pass the user's execution timing, write limits and permitted evidence commands explicitly to the How assignment as well as the design runners and judge. A read-only delegate must not execute application code when the user reserves execution for the primary or a later phase. Share the resulting artifact with each runner, so candidates solve the same actual problem.

## Sketch

Run Arena with the `architect-runner` pool, [runner prompt](architect/runner-prompt.md) and [rationale template](architect/rationale-template.md). Require at least two structurally distinct shapes before synthesis, even if the first appears sufficient. Model diversity and structural diversity are separate claims; two different models do not prove different designs. Ask runners to explore different ownership/data-flow/interface shapes, rather than implementation flavors.

Each candidate is an isolated sketch package: caller usage first, derived types and function signatures, module map, explicit unimplemented bodies/pseudocode, rationale, alternatives and risks. Screen every candidate against the full [design red flags](architect/design-red-flags.md) before synthesis. Judge interface depth: a simple public surface should hide meaningful complexity, not leak transport or storage decisions. Favor code understandable with partial context.

Use Arena's completed-writers → read-only crossjudge → independent primary scoring → coherent graft sequence. Fill the final rationale's Synthesis decision with base, adaptations and rejections. If only one viable structural alternative remains, replace it or stop and disclose the missing comparison; do not relabel two similar sketches as distinct architectures.

## Agree

An explicit request to stop and show the design creates a checkpoint: present the synthesized package and questions, then wait for the user's answer before implementing. Pushback means reground the changed constraints and rerun Sketch. Otherwise continue the already authorized implementation after synthesis. Do not introduce an extra approval gate merely because this is architecture work. Critical unknown scope or permissions still require clarification.

## Implement

Implement against the chosen sketch, replacing unimplemented bodies with working code. The primary owns integration and verification; preserve candidate write ownership until all candidate writers finish. Inspect the final implementation and run relevant checks. Surface meaningful departures from the sketch instead of silently reshaping it. Caller usage, derived types/signatures, module map and completed rationale form the design deliverable; a sketch alone is not a tested implementation.

## Scrap

Watch for repeated structural friction: two independent deviations of the same kind, repeated casts, unexpected shared mutable state, spreading special cases or callers handling leaked internals. A single edge case is not enough to restart the architecture. When a pattern appears, stop extending the failing shape, rerun How using the discovered constraints and return to Arena. Prefer subtracting the source of friction over adding another abstraction. Record the reason and new evidence in the existing checklist.
