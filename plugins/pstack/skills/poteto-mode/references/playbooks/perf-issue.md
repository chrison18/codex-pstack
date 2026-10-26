Internal reference within explicitly active Poteto. Follow [runtime](../runtime.md) and use the [workflow index](../workflow-index.md) for dependencies. Reference names are not additional native commands.

### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement, don't read source instead of measuring.

1. Capture a baseline trace via the matching control skill. Vet the baseline, and each later number, with the **benchmark-checklist** skill.
2. `how` to ground hypotheses. Don't claim a perf ceiling without running it first.
   Try the performance mantras in order, cheapest first:
   1. Don't do it. Stop work whose result nothing uses rather than cheapening it.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   When an earlier mantra meets the target, stop.
3. Plan the fix from the trace. If it crosses a function boundary, `architect` first. Delegate implementation to a subagent using the resolved `swarm-worker` model/effort. Resolve the actual model and effort before native delegation; no vendor tiers or silent substitutions. Review the diff. Capture a post-fix trace.
   Apply the **sequence-verifiable-units** principle skill, verifying each attempt before trying the next.
4. Parse and compare the artifacts (JSON to sqlite, diff). "Inconclusive" or wrong-surface is not a pass. Flag it.
5. Cite the measurement in the PR.
6. Run **Opening a PR**.

For sustained improvement against a metric rather than a one-off fix, use the [Hillclimb](hillclimb.md) playbook.

**Reply:** baseline number, post-fix number, delta, artifact path.


Source: `skills/poteto-mode/playbooks/perf-issue.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex host adaptations and evidence are recorded in the migration ledger.
