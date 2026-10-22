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
| 2 | Router, both agents, model setup, checklist, three initial playbooks | Started on `feat/codex-core-workflow`; [source mapping and gates](docs/migration/phase-2-core-workflow.md); runtime acceptance NOT RUN |
| 3 through 6 | Remaining skills, lifecycle, automation, release | Pending; see the [plan](docs/migration/codex-migration-plan.md) |

The preview package version starts at `0.1.0-alpha.1`. The inherited source pin remains pstack 0.15.29. The package does not include root agy workflows or the bundled cursor-team-kit skills yet. Keeping the package root separate permits incremental migration without exposing unported skills as supported Codex workflows.

## Future synchronization

1. Open a `sync/<topic>` branch from current `origin/main`.
2. Record exact repository and base/head SHAs independently for each source. Do not infer completeness from version numbers.
3. List adopted, already-present, and skipped changes with reasons. Separate source updates and Codex adaptations in commits.
4. Recheck adapted files against the capability matrix and regression scenarios. Avoid importing another host's generated harness trees.
5. Run applicable checks; record tested head, runtime versions, and resulting PR or merge commit in this ledger.
6. Advance a source pin only after accounting for the claimed range.
