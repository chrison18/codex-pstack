# Core principles for phase 2

These portable principles are adapted from the inherited pstack leaf skills. Read the relevant section before applying it. Name a principle only when it changed a concrete decision.

- **Model the Domain.** Choose the data shape before logic. Encode state and valid transitions in a state machine, typed model or registry rather than scattered flags. Prefer boring local code when a new abstraction removes no complexity.
- **Prove It Works.** Inspect the real artifact and execute the behavior on the relevant surface. A delegate's self-report, compilation or passing proxy does not establish the outcome. Record unavailable checks honestly.
- **Test Behavior, Not Implementation.** Drive observable behavior. A test must fail when the promised outcome breaks and survive internal restructuring that preserves it.
- **Sequence Work into Verifiable Units.** Build, verify and commit a small unit before the next. For a bug with a cheap reproduction, retain the failing test before the fix.
- **Separate Before Serializing Shared State.** Give concurrent writers separate worktrees and named base refs. In a shared checkout, use one writer and serialize writing. A subagent spawn alone establishes no isolation.
- **Laziness Protocol.** Choose the smallest change that solves the observed problem. Delete dead weight before adding layers. Review separation still matters for small changes.

The remaining upstream principles and routed skills are assigned to phase 3. This reference is the bounded core used by the three phase 2 playbooks, not a claim that the complete upstream style has been ported.
