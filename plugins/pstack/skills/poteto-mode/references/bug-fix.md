# Bug fix

The primary owns reproduction, causal judgment, review and verification.

1. Reproduce the reported defect on the same surface and retain the failing output. If the surface is unavailable, explain the specific missing access; do not count an unobserved reproduction as a pass.
2. Inspect affected call paths and regression history. Form competing hypotheses, eliminate them using execution evidence, and identify the mechanism causing the failure. Remove speculative changes when evidence refutes them.
3. Name the data shape and plan the smallest fix. Read applicable [principles](principles.md). Delegate investigation or implementation to `poteto-agent` with scoped files, the absolute entry path, evidence and success criteria. The primary keeps the playbook and checklist. Only one agent writes in a shared checkout at a time. If the role, model validation or spawn is unavailable, stop and report the blocker; do not implement the fix in the primary as a substitute.
4. Run the same reproduction again after the fix. Retain failing and passing output and focused regression checks. Compilation alone is insufficient. For a cheap local test, commit the failing test before the fix if commits are authorized.
5. Review the actual diff and obtain scoped `comment-sicko` findings. Apply only justified changes. Open a PR within the authorized delivery scope; do not infer merge approval.

Reply with the defect, observed cause, fix, failing-then-passing output and limitations. Timers, autonomous hunts and full upstream design panels remain later-phase work.
