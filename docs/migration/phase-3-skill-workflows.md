# Phase 3 skills and parallel workflows

## Increment boundaries

PR #4 is phase **3A**: source inventory, full principle references and local How/Why research. Its merge gate is independent review of the exact head, passing CI and the recorded scoped acceptance; it does not claim completion of all phase 3 skills or A7/A8/A9. The owner requested review and merge of this increment before continuing.

Phase **3A** merged in PR #4 as `288561b1feda1cf199f46ae36745ec47df6fb4ba` after independent review of `7469194` and exact-head CI. Phase **3B** has now started on `feat/codex-remaining-workflows` from that latest `main`; see [3B work and evidence](phase-3b-remaining-workflows.md). It owns the unchecked work below: live Why coverage where available, design/review/delegation, remaining core skills, expanded playbooks and actual A7/A8/A9 checks. Phase 4 remains dependent on those gates. The inventory keeps integer phase ownership `3` across both increments, and the split itself does not clear pending/partial work; current counts are below.


History: 3A started on `feat/codex-skill-workflows` from phase 2 squash merge `a25255330be51548e27c4a2bda4e9ca5af86dfcf`. PR #3 has merged. The first unit established an executable inventory and provenance guard. The second unit replaces six principle summaries with all 24 full principle references; How/Why references and model roles are now ported; four local native research cases and two integrated principle regressions passed. Live Why connector coverage remains unverified. Remaining design and parallel workflows are pending.

## Inventory contract

The [machine-readable inventory](codex-skill-inventory.json) accounts for all inherited units, not only files currently shipped by the Codex plugin:

| Kind | Count |
| --- | --- |
| Top-level skills | 59 |
| Agent definitions | 2 |
| Playbooks | 23 |
| Benny skills | 3 |
| Total | 87 |

Each row records its source path and SHA256 at the inherited migration baseline, responsible runtime phase, adaptation status, package target and evidence reference when applicable. The phase 3 starting ref is also recorded. The initial classifications describe delivery ownership and known availability; pending source units still require content/dependency review before porting.

| Status | Current count | Meaning |
| --- | --- | --- |
| adapted | 27 | Two native agents, 24 full principles and How; see scoped native evidence for representative checks |
| partial | 10 | Two bounded entries, three initial playbooks, Why, Interrogate, Arena, Architect and Swarm candidates; local Why checks passed, live source access remains unverified |
| pending | 31 | Phase 3 source units need review and adaptation; no package target or runtime pass is claimed |
| deferred | 19 | Full lifecycle/history or autonomous/Benny runtime belongs to phase 4 or 5 |

Full lifecycle ownership of automate-me/reflect remains phase 4. Phase 3 must review any portable content needed by an earlier dependency and record its narrower scope rather than claiming the whole unit is supported. The same boundary applies to phase 5 automation overlays.

The validator compares the catalog with actual source discovery and pinned content. It rejects missing/new units, source drift, duplicate identities, invalid phases/statuses, unsupported package claims, absent evidence, escaping paths and distributed skill entries without matching inventory targets. How/Why pin and validate all 14 transitive reference sources and package targets; Interrogate adds four and Architect adds three, with complete mappings required for each port. The package's existing structural checker remains responsible for manifest, role and invocation-policy validation. An evidence reference makes a claim reviewable; neither a file path nor a green structural check proves runtime behavior.

## Implementation sequence

- [x] Account for all 87 inherited source units, distinguish bounded phase 2 adaptations and later-phase runtime ownership, and wire inventory validation into CI.
- [x] Review and port all 24 full principle leaves, replacing the six bounded summaries with an applicable-leaf index. Preserve applicability metadata, provenance and explicit host adaptations. See [principles evidence](phase-3-principles-evidence.md) for representative behavior checks and their limits.
- [x] Pass the final principle evidence-claim audit in the real client. Both f5032db cases passed on 2026-10-23; actual full-leaf reads, Python replay, final claims and unchanged snapshots were inspected. Earlier failures remain in the evidence record.
- [x] Port How/Why as explicit-workflow references with all 14 prompt/source references. Add four research model preference keys while retaining task overrides and exact parent model/effort inheritance.
- [x] Record local How/Why native acceptance: simple and complex exploration, synthesis, role/parent/task model choices, seven-category source exclusions, confidence separation and primary-only fallback. Integrated principle regressions also passed. See [research evidence](phase-3-research-evidence.md).
- [ ] Verify live Why connector access and cross-source synthesis where available; preserve explicit source gaps for unavailable services. Why remains partial.
- [ ] Port the remaining design/review/delegation workflows.
- [ ] Port remaining phase 3 code-quality, prose, verification/control and authoring skills. Check all transitive references and mark unavailable host capabilities explicitly.
- [ ] Expand the bounded playbooks to consume the migrated skills without claiming that later-phase lifecycle or automation works.
- [x] Exercise bounded native parallel writers in separate worktrees, a pushed non-default starting ref, integration and local-process/auth access. See [Swarm evidence](phase-3b-swarm-evidence.md); desktop/browser variants remain NOT RUN. A spawn alone is not proof.
- [ ] Complete the per-unit support/evidence classification, real client checks, independent review and phase 3 CI before requesting merge approval.

These units ship no new native skill entry and change no project/global model settings. Poteto-mode remains explicitly activated per task. The inherited Antigravity source is retained for comparison; it is not automatically loaded by the Codex package.

## Validation

```sh
bun scripts/validate-codex-plugin.ts
bun scripts/validate-codex-inventory.ts
python3 -B scripts/sync-codex-principles.py
bun test ./scripts/
```

The inventory is source control metadata. Intentional upstream changes require reconciling the pinned source, ownership and provenance together; do not regenerate hashes merely to hide unexplained changes. A new package claim needs a real artifact and a cited evidence file, followed by behavior checks appropriate to that capability.

Initial-unit observations: Bun 1.4.3 passed 23 tests with 35 assertions, including 9 inventory regressions; strict TypeScript checks passed. All 87 recorded source digests were independently compared with git show at the inherited baseline and matched. Both package and inventory validators passed. No new phase 3 client-runtime behavior is claimed by this source-accounting unit.

Swarm now has bounded native [A7/A8/A9 evidence](phase-3b-swarm-evidence.md): real concurrent worktrees, a pushed non-default base and an authenticated local process probe. Desktop/browser variants and the remaining source units are not covered by those fixture passes.
