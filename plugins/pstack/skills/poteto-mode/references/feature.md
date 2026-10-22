# Feature

The primary owns the design, checklist, every delegation, verification and final reply.

1. Map the affected subsystem by reading its actual call paths. State the requested outcome and acceptance check. Choose the data shape before writing logic; read the relevant [principles](principles.md).
2. Compare plausible design choices and choose the smallest justified shape. Full `how`, `architect`, `arena` and `interrogate` panels are phase 3 work. Do not claim those skills ran. If the task requires them, report the limitation before promising coverage.
3. Write the throughput checkpoint as four checklist entries: blocking first steps, independent workstreams, shared mutable state, and smallest safe decomposition. Retain an inapplicable item with `skip: <reason>`.
4. Delegate implementation to registered `poteto-agent` with the absolute entry path, named files, chosen data shape, success criteria and resolved model/effort. The primary owns the workflow. Use one writer per checkout; do not edit concurrently with the worker. Review the returned diff yourself. A missing role or rejected spawn blocks the delegated step; stop the workflow and report it without substituting another role or primary implementation.
5. Verify actual behavior on the relevant UI or CLI surface. Run focused checks and inspect the final diff. Record failures, limitations and skipped steps; a failure is not completion.
6. Obtain scoped comment review from `comment-sicko`, giving it the same entry path and exact diff. Evaluate its findings before changing code. Keep commits focused if commits are authorized. Open a PR only when requested or part of the authorized delivery; merge authorization is separate.

Reply with the resulting behavior, design choice, verification and material limits. Include the throughput checkpoint and the actual PR link when one was created.
