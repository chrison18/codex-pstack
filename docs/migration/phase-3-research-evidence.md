# Phase 3: How and Why research workflows

Candidate on `feat/codex-skill-workflows`, based on `a25255330be51548e27c4a2bda4e9ca5af86dfcf`. PR #4 remains draft; no merge is authorized. The preceding principle gate passed on unchanged `f5032db` before this implementation began, recorded by `15f3413`.

## Package and source scope

How and Why are references under the explicitly activated Poteto Investigation entry, not new native skill entries. Ordinary new prompts remain outside that workflow. The inherited `skills/how` and `skills/why` sources remain unchanged at `a06537a883278a63132e2518971166002f3de5de`.

How preserves simple single-explainer and complex 2–4 explorer plus explainer paths, concrete architecture/data-flow explanations and file citations. Why preserves the code anchor, seven evidence categories, source-specific search methods, investigator/synthesizer separation, epistemics, contradiction handling, source gaps and Preserve/Change/Avoid/Risk planning constraints. The package contains both How prompts and all 12 Why reference files; the inventory additionally pins each of these 14 transitive source digests and its package counterpart. CI checks reference coverage, hashes and contained targets. The inventory's 87 top-level unit count is unchanged.

Codex adaptations replace inherited Antigravity tool calls, model-rule paths and Flash/Pro defaults with current tool discovery and native model resolution. All four preference keys (`how-explorer`, `how-explainer`, `why-investigator`, `why-synthesizer`) use the already registered `poteto-agent`; they are not four new native agents. Parent model/effort inheritance, saved role settings and task overrides keep their existing precedence. Role files omit model settings. Research never installs roles or changes model preferences as a side effect.

The primary owns the checklist, inspections and final answer. Role/permission/tool unavailability permits the disclosed primary-only Investigation read path; rejected explicit model selections do not permit substitution or fallback to evade them. Read-only scope is not a new agent sandbox. Native custom agents inherit permissions, provider and MCP configuration from the parent; see [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents), fetched 2026-10-23.

Why does not assume `gh`, a particular vendor, authenticated MCP access or a complete Git history. Example source operations and company table/column names must be mapped to actual schemas. Sources outside the user's scope are explicitly excluded, not searched silently or counted as empty. Sending messages, installing connectors, modifying authentication and production operations remain outside research. No live vendor connector success is claimed by packaging a source playbook.

## Verification method

`accept-codex-research.py` creates disposable Git fixtures with known code flow and two commits. The history records a partner batch limit of five, while timeout eleven has no recorded motivation. The question embeds a performance hypothesis to test confidence separation. All external sources are explicitly excluded for this fixture. The native app-server supplies actual subagent-start model/effort notifications; raw logs remain local.

The fixture parent uses Sol/low and deliberately different global subagent defaults Luna/high. How-simple saves Luna/medium for the explainer. How-complex uses parent inheritance. Why saves Luna/medium for the synthesizer but requests a task override Sol/high. The fallback case installs no project roles and forbids delegation. All cases use a parent read-only sandbox. Temporary authentication references are removed on completion; they are never copied or printed.

Snapshots compare every non-Git workspace entry's type/mode/content/link/directory state; HEAD and staged diff are compared separately. These are artifact checks, not automatic proof of correct citations, coverage or confidence. Inspect actual requests, started agents, reads, source history and replies before marking a case accepted.

## Candidate results

Client: `codex-cli 0.163.0-alpha.11.1` native app-server, 2026-10-23. Evidence directory: `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-research-live-afyjfkqd`. All four parent turns completed, all non-Git entry snapshots matched, HEAD/staged diffs matched, and all temporary authentication references were removed.

| Case | Actual native behavior and inspection | Result |
| --- | --- | --- |
| How-simple | One native `poteto-agent` explainer started as Luna/medium from the saved `how-explainer` preference, despite Luna/high global defaults. Primary inspected the cited source. Correct price × quantity sum and normalization caveats; static inference explicitly separated from execution. | PASS, local native |
| How-complex | Two explorer starts preceded their completion, followed by one explainer. All three resolved to Sol/low from the parent, overriding global Luna/high. Actual source reads traced API → normalization → sum and identified unused limits. The reply labeled its example unexecuted and inspected references in the primary. | PASS, local native |
| Why | Git investigator started Sol/low; synthesizer started Sol/high from the task override despite saved Luna/medium. Actual history reads and independent citation checks found the explicit partner limit in the change commit; timeout eleven remained Unknown. The performance hypothesis was not rubber-stamped. All seven coverage categories were accounted for; six external categories were explicitly outside local-only scope rather than claimed searched. | PASS for local Git/history and exclusions |
| Primary-only fallback | No installed project roles, no spawn requests and no resolved-agent starts. Primary read and cited source, reported that no custom role ran, and did not install/configure anything. An unnecessary resolution attempt failed on the missing receipt and was reported blocked, not passed; the answer still followed the allowed primary-only read route. | PASS, local fallback; no model-resolution pass claimed |

Native agent IDs and resolved pairs:

- How-simple: `01a16751-b524-70e1-a297-71ba1d5de884`, Luna/medium.
- How-complex: `01a16752-d2e0-7b72-85cd-8a090602625e`, `01a16753-0be3-78f3-afe3-3fc030cdc6cb`, `01a16754-35f0-7751-a669-25c44196dae4`, all Sol/low.
- Why investigator: `01a16756-8710-7422-8149-f820b6ccea01`, Sol/low; synthesizer: `01a16757-f965-79d2-b67c-3a2243fc1986`, Sol/high.

The local Why fixture's motivation commit is `46573770d6f03b13423219c1c2a5f30fe2f236a2` (“Limit batches to five because the partner endpoint rejects larger batches”), changing 3 → 5. The initialization commit `41a97273f459974f361b56290545682b0dbd81f0` introduced timeout eleven without rationale. The reply did not infer production enforcement or measured speed from these unused constants.

The first capture counter expected legacy `collabAgentToolCall` items and printed zero even while resolved-start notifications showed actual agents. It was corrected to parse the actual `rawResponseItem/completed` spawn requests and deduplicate `subAgentActivity` starts. Existing raw events were reprocessed: 1 / 3 / 2 / 0 requests and starts. Regression checks preserve the distinction between requested and resolved models and exclude child answers/commentary from the primary final-answer capture. This collector correction did not substitute an agent self-report for start evidence.

How is classified adapted for this local supported scope. Why remains partial: live MCP access and genuine multi-source synthesis were not tested. Desktop UI and phase 3 A7/A8/A9 are outside these local read-only fixture checks. No vendor-source queries were issued in the fixture tool records, and packaging a source playbook does not prove that connector is installed or reachable.

## Integrated regressions and static checks

After routing Investigation through How/Why, the original premise and isolation cases were rerun against the integrated candidate at `/private/var/folders/47/vjdx7cgs6kgd9bxf146wm1ph0000gn/T/pstack-principles-live-t7tvlhqm`. Both completed with unchanged snapshots, no named-but-unread leaves and passing harness checks. Manual inspection matched the premise's actual Python replay and isolation's explicitly proposed, unexecuted checks to the replies.

Final local checks: 28 Bun tests / 41 assertions (including 10 Python runtime tests, 5 snapshot tests and 2 capture tests inside the wrappers); 69 inherited tests / 247 assertions; strict TypeScript tooling/inherited checks; package/inventory/24-principle transformation checks; skill quick validation; isolated install/invocation/ordinary-chat exclusion/removal smoke; shell syntax and `git diff --check`.

An earlier parallel run hit Bun's 5-second per-test limit in the subprocess-based runtime test and three inherited Git fixture tests. The new role test was reduced to the necessary CLI boundary calls, while direct precedence/immutability checks remain for all four keys. Its subprocess wrapper now has a bounded 30-second timeout. With suites run separately, all 28 and all 69 passed at the normal CLI test settings; inherited tests and assertions were unchanged.

To repeat native checks, refresh a real host catalog and run `python3 -B scripts/accept-codex-research.py --codex /absolute/codex --model gpt-6.1-sol --effort low --catalog /absolute/fresh-catalog.json`. Use `--case` to scope a rerun. The harness's artifact result is intentionally narrower than this manual behavior assessment.
