# Upstream provenance

## Starting point

- Fork: [chrison18/codex-pstack](https://github.com/chrison18/codex-pstack).
- Immediate parent: [pstack-ports/agy-pstack](https://github.com/pstack-ports/agy-pstack).
- Migration base: `a06537a883278a63132e2518971166002f3de5de`.
- Inherited versions: pstack `0.15.29`; bundled cursor-team-kit skills `1.2.0`.
- Base inventory: 59 top-level skills, 2 agents, 23 playbooks, plus 3 Benny skills under `automations/benny/skills`.
- The inherited tree implements Antigravity behavior. Phase 0 documentation does not establish Codex runtime support.

## Original sources

| Source | Attribution | Pin and evidence |
| --- | --- | --- |
| pstack initial import | Lauren Tan (poteto) | [`dbf49813a39c1a5389c5e28cb8e4c1c2379e2454`](https://github.com/cursor/plugins/tree/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454/pstack), imported as a snapshot by `9dbf549c` |
| Latest inherited pstack sync | Lauren Tan (poteto) | [`88d47514b82e7c44f00f2b2a72ff6dd12158038c`](https://github.com/cursor/plugins/tree/88d47514b82e7c44f00f2b2a72ff6dd12158038c/pstack), upstream #729, recorded by `fe51df54` as 0.15.29 |
| cursor-team-kit | Eric Zakariasson | `deslop`, `control-cli`, `control-ui` bundled at 1.2.0 by `a3775da2`; exact source SHA not recorded by that commit |
| Antigravity port | Kaitian Xie and contributors | Parent repository history through the migration base above |

The original pstack history before the snapshot is not present here. The 25 inherited commits describe the port and subsequent synchronization, not Cursor pstack's full history. The sync pin is the inherited recorded pin, not a claim of the latest upstream today.

Preserve the [MIT license](LICENSE) and attribution. An author-only cursor-team-kit change at `2b8ae2ee306f823d54879d3da7f8496b73c31d5d` is mentioned in `fe51df54`; it does not establish the exact revision used to bundle the three skills.

## Inherited commit ledger

IDs resolve in this repository and are listed in ancestry order.

| Commit | Change |
| --- | --- |
| `9dbf549c` | Import pstack 0.15.23 snapshot |
| `c3f5d3c3` | Antigravity support, shared skill paths, porting guide |
| `5b9c9536` | Choose Antigravity-only support |
| `a3775da2` | Bundle three cursor-team-kit skills |
| `a5dd4718` | Rename organization URLs |
| `660c1731` | Fix runtime tools, MCP, bot UI, paths, transcripts, metadata |
| `944c6f7e` | Remove unregistered MCP tool names |
| `f2a1ab07` | Guard absent model rules |
| `d3e5e6c8` | Store checklists in the task artifact |
| `2f04b917` | Correct research tools and read-only commands |
| `a35634b6` | Sync through pstack 0.15.25 |
| `65b9aa7e` | Add plugin and script CI |
| `c8147c70` | Sync #633/#634; normalize agent IDs in CI |
| `a3dcda11` | Sync #700/#704 |
| `791db0e9` | Sync 0.15.27 and formal verification authoring |
| `5810e756` | Sync 0.15.28 and formal verification maintenance |
| `8bb21670` | agy 1.4 tools and model/effort inheritance |
| `fe51df54` | Sync #729 and pstack 0.15.29 |
| `aac68603` | Restore per-task activation guidance |
| `167265db` | Remove leftover cloud-agent wording |
| `503be433` | Restore upstream README with adaptations |
| `ebdd2da7` | Complete agent tool allowlists |
| `a97f19d6` | Restore swarm local-state exception and base ref |
| `80c4faf7` | Correct orchestrate workspace behavior |
| `a06537a8` | Restore editor caret context in why |

## Codex adaptation ledger

| Phase | Adaptation | Status |
| --- | --- | --- |
| 0 | Plan, Git rules, provenance, observed test baseline | Merged in [PR #1](https://github.com/chrison18/codex-pstack/pull/1), `30a666d6fb473caea211fbb750079afbee19d30f` |
| 1 | Isolated Codex package under `plugins/pstack/`, repo marketplace, explicit invocation policy, safe project short-name alias, structural CI | Merged in [PR #2](https://github.com/chrison18/codex-pstack/pull/2), `c303a74e4e5e6f7e9f055b5eed49507bc59ddfbd`; CLI evidence and owner-reported desktop acceptance complete |
| 2 | Router, both agents, model setup, checklist, three bounded playbooks | Merged in [PR #3](https://github.com/chrison18/codex-pstack/pull/3), `a25255330be51548e27c4a2bda4e9ca5af86dfcf`; core-task exit gates met; qualified desktop distribution capture retained for phase 6 |
| 3A / 3B | Full skills and parallel workflows | 3A merged in [PR #4](https://github.com/chrison18/codex-pstack/pull/4), `288561b1feda1cf199f46ae36745ec47df6fb4ba`; [87-unit inventory and guard](docs/migration/phase-3-skill-workflows.md), [24 full principle references](docs/migration/phase-3-principles-evidence.md) with passing representative claim audits, [How/Why candidates](docs/migration/phase-3-research-evidence.md); 3B retains the remaining skills and A7/A8/A9 gates on `feat/codex-remaining-workflows` started from that latest main |
| 4 through 6 | Lifecycle, automation and release | Pending; see the [plan](docs/migration/codex-migration-plan.md) |

The preview package version starts at `0.1.0-alpha.1`. The inherited source pin remains pstack 0.15.29. The package does not include root agy workflows or the bundled cursor-team-kit skills yet. Keeping the package root separate permits incremental migration without exposing unported skills as supported Codex workflows.

## Phase 3B design adaptation

At the same inherited baseline `a06537a883278a63132e2518971166002f3de5de`, PR #5 adopts Arena's six-step comparison/synthesis workflow and Architect's grounding, structural alternatives, caller-first sketches, red-flag screen, opt-in checkpoint, implementation and scrap loop. All three Architect reference hashes are pinned in the [inventory](docs/migration/codex-skill-inventory.json) and independently match that baseline. No upstream pin is advanced and inherited files are unchanged.

Codex adaptation replaces Antigravity task files, tool names, vendor model aliases and global rule paths with scoped checklists, native delegation and project model resolution. Runner/parent ownership is explicit; prose paths are not advertised as separate sandboxes. Both workflows remain internal to explicit Poteto mode. [3B evidence](docs/migration/phase-3b-remaining-workflows.md) distinguishes actual artifact tests from unrun code-worktree, dropout/scrap and desktop paths. The subsequent Swarm increment adopts partition/race selection, exact refs/methods, bounded shared-state access, one evidence retry and consolidated reporting at that same source pin. Foreign workspace/model tooling becomes real worktree preparation plus native worker resolution; [A7/A8/A9 evidence](docs/migration/phase-3b-swarm-evidence.md) separates native fixture passes from desktop variants. The [subsequent race/recovery increment](docs/migration/phase-3b-swarm-recovery-evidence.md) clarifies predeclared selection rules and adds controlled artifact faults, bounded retries, native interruption and actual patch-conflict probes at the same inherited pin. These are scoped fixtures, not process-crash/network/desktop parity. Other remaining units stay pending rather than being silently bundled or removed.

## Future synchronization

1. Open a `sync/<topic>` branch from current `origin/main`.
2. Record exact repository and base/head SHAs independently for each source. Do not infer completeness from version numbers.
3. List adopted, already-present, and skipped changes with reasons. Separate source updates and Codex adaptations in commits.
4. Recheck adapted files against the capability matrix and regression scenarios. Avoid importing another host's generated harness trees.
5. Run applicable checks; record tested head, runtime versions, and resulting PR or merge commit in this ledger.
6. Advance a source pin only after accounting for the claimed range.

## Phase 3B portable sources

At the unchanged inherited pin, the next PR #5 increment classifies the remaining 22 skills and nine playbooks as internal Codex references, including all six transitive source documents. The [dependency index](plugins/pstack/skills/poteto-mode/references/workflow-index.md) and inventory guard keep packaged consumers from relying on missing/deferred execution dependencies or cycles. No new native entry is published.

Host changes preserve substantive quality/writing/verification advice while replacing foreign checklist/log paths, role/model tiers, transcript scraping and built-ins. PR delivery respects explicit drafts, phase branches and unrelated WIP; inherited reset/ready/rewrite defaults are removed. Manual multi-phase planning is explicitly narrower than the phase 5 standing-program template/checker. History, automated wakes and shipping overlays remain deferred. A copied TypeScript duration example now accurately states that a plain number does not prevent negative values; the source remains pinned rather than silently edited.

[Portable native evidence](docs/migration/phase-3b-portable-evidence.md) retains interrupted probes, observed How/brief omissions and instrument faults alongside fresh scoped passes. Protected skill installation, native browser launch, Eval blinding/family coverage and formal/tool/desktop variants are not claimed by scratch candidates or supplementary host replay. Neither zero pending source units nor successful CI completes phase 3B or authorizes phase 4/merge.

## Phase 3B1 review and continuation boundary

On 2026-10-26 the owner authorized PR #5 merge after validation and review. The [migration plan](docs/migration/codex-migration-plan.md) explicitly separates 3B1 candidate delivery from 3B2 acceptance closure; partial capability claims and all original phase 3 gates remain. The [merge review](docs/migration/phase-3b1-merge-review.md) records the independently found/fixed temporary-auth cleanup defect, regression and local checks. The [live-source supplement](docs/migration/phase-3b-live-source-evidence.md) records scoped GitHub reads without claiming native multi-source acceptance. The inherited pin is unchanged.

## Phase 3B2 acceptance start

PR #5 merged as `b9ad7434506b3785b531b66afa85d1ad040b9fbb`; `test/codex-3b-acceptance` starts from that actual main. The [3B2 evidence](docs/migration/phase-3b2-acceptance.md) adds native rejection and missing-role fallback probes, retaining two real capacity failures as partial/dropout evidence rather than full empty-review passes. No inherited source pin or runtime workflow instruction changes; full 3B/phase 4 gates remain open.

## Phase 3B2 independent-start adapter

At the unchanged inherited pin, the package runtime contract and Arena reference now describe the supported Codex fresh-start schema for explicitly modeled independent delegates, complete scoped briefs and existing grounding before Arena fan-out. This is a local host adaptation prompted by observed inherited-context launch errors and missing-context handoffs, not a Cursor source synchronization. The [3B2 evidence](docs/migration/phase-3b2-acceptance.md) separates coached historical runs, initially incomplete uncoached handoffs and the corrected package-driven native run. General Feature/Bug/Investigation behavior and Orca Chat UI are not recertified by the Arena fixture.

The same 3B2 adapter now distinguishes directly declared native collaboration/role schemas from nested tool inventories before missing-role fallback. This responds to a reproduced false-absence inference in Investigation; the retained failed run and corrected role-present/role-absent native probes are in the same evidence record. No upstream source pin or global policy changed.

## Phase 3B2 Architect dependency and comparison clarification

The controlled repeated-friction probe repaired the fixture but failed the full Scrap contract: candidates preceded delegated How completion and equivalent fields/closure designs were counted as distinct. The package now centralizes the grounding dependency and concrete structural-comparison evidence in Architect, with runner/judge references and at most one replacement for unchanged framing. These are workflow instructions, not runtime enforcement or a semantic diversity checker; a subsequent single native controlled-friction run passed the corrected ordering and structural comparison, while the convergence/replacement/stop branch remains NOT RUN. The inherited source pin and ordinary Arena/How/read-only boundaries remain unchanged. See the [acceptance record](docs/migration/phase-3b2-acceptance.md).
