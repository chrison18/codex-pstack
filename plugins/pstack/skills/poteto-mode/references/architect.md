# Architect: explore structure before implementation

Use within explicitly active Poteto mode for a requested design or a change whose ownership and interfaces need exploration. The primary owns the checklist: ground → sketch → agree → implement → scrap if necessary. Read [Arena](arena.md) and the [runtime contract](runtime.md).

## Ground

Run [How](how.md) through its applicable route to explain the affected system with file/line evidence, including its explainer delegation when available and authorized. A primary source read alone does not complete that delegated route; any fallback must meet How's stated conditions and be disclosed. When ownership or layering changes, use [Why](why.md) to recover historical constraints and distinguish known reasons from guesses. Skip grounding only for genuinely greenfield work and say why. Pass the user's execution timing, write limits and permitted evidence commands explicitly to the How assignment as well as the design runners and judge. A read-only delegate must not execute application code when the user reserves execution for the primary or a later phase. Complete the selected How route and inspect its cited sources, reconcile contradictions and record unresolved limits before freezing the shared grounding artifact. If How is delegated, wait for its actual result and primary reconciliation; an initial primary draft is not completion of that dependency. Only then persist and read back the frozen artifact and start candidates. Do not run candidates concurrently with the How work they depend on. Share the same frozen artifact with every runner. A later material grounding change requires a new Sketch round rather than retroactively treating earlier candidates as grounded. These steps also apply when returning from Scrap; genuinely greenfield work and How's disclosed legitimate fallback retain their stated boundaries.

## Sketch

Run Arena with the `architect-runner` pool, [runner prompt](architect/runner-prompt.md) and [rationale template](architect/rationale-template.md). Require at least two structurally distinct shapes before synthesis, even if the first appears sufficient. Model diversity and structural diversity are separate claims; two different models do not prove different designs. Ask runners to explore different ownership/data-flow/interface shapes, rather than implementation flavors.

Each candidate is an isolated sketch package: caller usage first, derived types and function signatures, module map, explicit unimplemented bodies/pseudocode, rationale, alternatives and risks. Screen every candidate against the full [design red flags](architect/design-red-flags.md) before synthesis. Judge interface depth: a simple public surface should hide meaningful complexity, not leak transport or storage decisions. Favor code understandable with partial context.

Use Arena's completed-writers → read-only crossjudge → independent primary scoring → coherent graft sequence. Fill the final rationale's Synthesis decision with base, adaptations and rejections. Apply the structural comparison below before choosing or implementing a synthesis.

### Structural comparison

Each runner describes its own concrete shape in its rationale: who owns state and its lifetime, how inputs move and when derived values are computed, and what responsibilities cross each interface. Cite the proposed types, signatures and call sites; a label or claimed benefit is not evidence. Independent runners need not see other candidates.

After writers finish, both the read-only judge and the primary independently compare those same three axes across the actual artifacts. Identify at least one task-relevant structural difference and its consequences for the required caller behavior or constraints. Different syntax, names, fields versus closures, or wrapper placement do not establish distinct structures when ownership, data flow and interface responsibilities are equivalent. Record convergence honestly, even when both candidates fix the defect or use different models.

If fewer than two viable, structurally distinct candidates remain, either stop with the comparison incomplete or replace one candidate once for this unchanged framing. Preserve prior artifacts, assign the replacement a fresh owned directory and an explicitly different structural hypothesis, and wait for its completion before repeating judge and primary comparison. If it still converges, fails or drops out, stop before synthesis/implementation and report the unresolved comparison; do not keep generating candidates or claim diversity. A materially revised user goal requires a newly grounded round, not a way to evade this bound. This is an Architect requirement; ordinary Arena may report convergence without forcing diversity.

## Agree

An explicit request to stop and show the design creates a checkpoint: present the synthesized package and questions, then wait for the user's answer before implementing. Pushback means reground the changed constraints and rerun Sketch. Otherwise continue the already authorized implementation after synthesis. Do not introduce an extra approval gate merely because this is architecture work. Critical unknown scope or permissions still require clarification.

## Implement

Implement against the chosen sketch, replacing unimplemented bodies with working code. The primary owns integration and verification; preserve candidate write ownership until all candidate writers finish. Inspect the final implementation and run relevant checks. Surface meaningful departures from the sketch instead of silently reshaping it. Caller usage, derived types/signatures, module map and completed rationale form the design deliverable; a sketch alone is not a tested implementation.

## Scrap

Watch for repeated structural friction: two independent deviations of the same kind, repeated casts, unexpected shared mutable state, spreading special cases or callers handling leaked internals. A single edge case is not enough to restart the architecture. When a pattern appears, stop extending the failing shape, rerun How using the discovered constraints and return to Arena. Prefer subtracting the source of friction over adding another abstraction. Record the reason and new evidence in the existing checklist.
