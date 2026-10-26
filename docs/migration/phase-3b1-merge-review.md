# Phase 3B1 merge review

On 2026-10-26 the owner authorized verification and review, then merge if passing and continuation. This supersedes PR #5's earlier draft-only instruction. The migration plan now separates candidate delivery (3B1, PR #5) from remaining acceptance (3B2); phase 4 still depends on full 3B acceptance.

## Independent review

The read-only reviewer inspected the PR changes from base `288561b1feda1cf199f46ae36745ec47df6fb4ba` through `2b3c0d0e0a8abe96baba613cde6410b213c3c821`, the live-source supplement, and subsequent working-tree corrections. It reviewed panel selection, dependency validation, routing, ownership and scope boundaries, portable workflow references and evidence claims. No GitHub review was posted; the independent review is recorded in the current conversation.

One P2 was reproduced: invalid `--node-modules` or `--tool-path` raised before the portable acceptance driver's cleanup boundary, leaving a temporary authentication link. The fix moves initialization inside the boundary and uses nested cleanup so a client-close error cannot skip link removal/environment restoration. A model-free regression uses a fake authentication file and both invalid paths; both subcases failed before the fix and passed after. It checks no model client starts, no auth link survives, environment values are restored, and the original file is unchanged. The duplicated “Then then” in Refactoring was also corrected.

The reviewer reinspected the fix, regression and explicit 3B1/3B2 split and found no remaining 3B1 merge blocker, conditional on current-head checks/CI. The review did not run tests or claim full desktop/live-source/blinding coverage. All 31 partial classifications remain partial.

## Local verification

- Package suite: 34 tests / 57 assertions passed after the fix, including six Python portable-fixture tests inside the wrapper.
- Inherited suite: 69 tests / 247 assertions passed. An initial run through the environment's Node shim hit four timeouts; rerunning with the existing Node 24.22.0 binary directory on the process PATH passed at the unchanged default test timeouts. No inherited code/test changes.
- Strict inherited TypeScript and strict package/inventory-validator TypeScript passed. The first root compiler invocation named the wrong installed type package (`bun`); the corrected invocation used `bun-types`.
- Package validation, 87-unit inventory validation, all 24 principle transformations, Bash syntax and diff checks passed. No inherited skills, agents or automations changed.
- Isolated smoke on Codex CLI `0.164.0-alpha.11.1` passed install, qualified entry, short project entry, implicit exclusion and removal. It used disposable state and a local capture listener; no model or desktop UI ran. The initial sandbox denied loopback binding; the authorized host run passed.
- The optional external skill-creator validator could not import PyYAML in the system Python. The package validator's frontmatter/invocation checks passed; no standalone PyYAML validation is claimed for this increment.

CI must pass for the exact final pushed head before merge; current-head run links and the actual merge result belong in the PR record. A historical CI pass is insufficient. After merge, fetch actual main and create `test/codex-3b-acceptance`; do not start phase 4 or imply that unavailable surfaces passed.
