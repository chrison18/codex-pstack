# Phase 3 skills and parallel workflows

Status: started on `feat/codex-skill-workflows` from phase 2 squash merge `a25255330be51548e27c4a2bda4e9ca5af86dfcf`. PR #3 has merged. The first unit established an executable inventory and provenance guard. The second unit replaces six principle summaries with all 24 full principle references; how/why and parallel workflows remain pending.

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
| adapted | 2 | Both native agent resources were adapted and exercised in phase 2 |
| partial | 29 | Two bounded entries, three playbooks and 24 full principle references; principle content is ported, but final evidence-claim behavior is not accepted yet |
| pending | 37 | Phase 3 source units need review and adaptation; no package target or runtime pass is claimed |
| deferred | 19 | Full lifecycle/history or autonomous/Benny runtime belongs to phase 4 or 5 |

Full lifecycle ownership of automate-me/reflect remains phase 4. Phase 3 must review any portable content needed by an earlier dependency and record its narrower scope rather than claiming the whole unit is supported. The same boundary applies to phase 5 automation overlays.

The validator compares the catalog with actual source discovery and pinned content. It rejects missing/new units, source drift, duplicate identities, invalid phases/statuses, unsupported package claims, absent evidence, escaping paths and distributed skill entries without matching inventory targets. The package's existing structural checker remains responsible for manifest, role and invocation-policy validation. An evidence reference makes a claim reviewable; neither a file path nor a green structural check proves runtime behavior.

## Implementation sequence

- [x] Account for all 87 inherited source units, distinguish bounded phase 2 adaptations and later-phase runtime ownership, and wire inventory validation into CI.
- [x] Review and port all 24 full principle leaves, replacing the six bounded summaries with an applicable-leaf index. Preserve applicability metadata, provenance and explicit host adaptations. See [principles evidence](phase-3-principles-evidence.md) for representative behavior checks and their limits.
- [ ] Pass the final principle evidence-claim audit in the real client. Earlier replies overclaimed execution or leaf reads; the final correction could not be evaluated because workspace routing failed. These 24 units remain partial.
- [ ] Port how/why and the design/review/delegation workflows. Extend role model resolution deliberately; retain task overrides and exact parent model/effort inheritance.
- [ ] Port remaining phase 3 code-quality, prose, verification/control and authoring skills. Check all transitive references and mark unavailable host capabilities explicitly.
- [ ] Expand the bounded playbooks to consume the migrated skills without claiming that later-phase lifecycle or automation works.
- [ ] Exercise parallel writers in separate worktrees, an explicit non-default starting ref, result integration and local-process/browser/auth access. Record gaps; a spawn alone is not proof of isolation or local-state access.
- [ ] Complete the per-unit support/evidence classification, real client checks, independent review and phase 3 CI before requesting merge approval.

These units ship no new native skill entry and changes no project/global model settings. Poteto-mode remains explicitly activated per task. The inherited Antigravity source is retained for comparison; it is not automatically loaded by the Codex package.

## Validation

```sh
bun scripts/validate-codex-plugin.ts
bun scripts/validate-codex-inventory.ts
python3 -B scripts/sync-codex-principles.py
bun test ./scripts/
```

The inventory is source control metadata. Intentional upstream changes require reconciling the pinned source, ownership and provenance together; do not regenerate hashes merely to hide unexplained changes. A new package claim needs a real artifact and a cited evidence file, followed by behavior checks appropriate to that capability.

Initial-unit observations: Bun 1.4.3 passed 23 tests with 35 assertions, including 9 inventory regressions; strict TypeScript checks passed. All 87 recorded source digests were independently compared with git show at the inherited baseline and matched. Both package and inventory validators passed. No new phase 3 client-runtime behavior is claimed by this source-accounting unit.
