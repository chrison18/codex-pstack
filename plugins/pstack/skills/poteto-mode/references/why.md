# Why: evidence of historical motivation

Use within an explicitly activated Poteto Investigation for design rationale, regressions, postmortems, motivating edge cases, tradeoffs or measured thresholds. [How](how.md) explains mechanics; Why investigates the forces behind the code. Read [epistemics](why/epistemics.md) fully. A user's suggested rationale is a hypothesis to test, not a conclusion to confirm.

Read [the runtime contract](runtime.md). This is read-only: keep the checklist in conversation or authorized external scratch; inspect state before/after; do not create files in the target, install roles, change preferences, post messages, mutate remote services or run production interventions. A role's prose does not create a separate read-only sandbox. Use the parent permission boundary.

## Establish the code anchor

Identify the target and question, stating your interpretation when ambiguous. Avoid recency bias: the current design may accumulate many earlier decisions, so trace beyond the most recent change. Gather actual file paths/line ranges, symbols, last-touch commits, history through renames, substantive commit messages, PR numbers and linked ticket IDs. Useful read-only operations include:

```sh
git blame -L START,END -- FILE
git log --follow -p -- FILE
git log --oneline -20 -- FILE
git show --format=fuller COMMIT -- FILE
```

Use actual paths and refs, bounded output, and further reads where the initial view truncates. Fetch substantive PR descriptions, review discussions and linked issues using the available GitHub connector; use an authenticated CLI/API if the connector cannot supply them. Neither `gh` nor remote access is guaranteed. Shallow/missing history, unavailable credentials and denied fetches are explicit gaps. Do not fetch more history or change repository state as an automatic repair.

## Discover sources and map coverage

Inspect the current session's available tools and schemas or native tool discovery; never inspect another host's configuration directory or invent MCP tool names. Discover candidate read capabilities, then verify access within the user's repository/organization scope. Availability of a connector does not establish relevance, authentication or actual search coverage.

Map all seven categories, recording source, queries/time window and outcome for each:

1. **Source control:** implementation-time rationale from history, PRs, comments and tests. Always inspect available local history; missing Git/history must be recorded rather than assumed available.
2. **Issue tracker:** product/business forcing function.
3. **Long-form documents:** design rationale recorded before or around implementation.
4. **Team chat:** deliberation omitted from formal documents.
5. **Infrastructure observability:** runtime conditions that motivated the change.
6. **Error tracking:** concrete failures and trajectories behind defensive code.
7. **Product analytics/warehouse:** usage, experiments and data shaping thresholds or migrations.

Use [the source playbook index](why/source-playbook.md) to choose only the applicable category reference. The vendor examples describe search shapes, not installed tools. For defensive code, also read [incident context](why/sources/incident-postmortem.md).

Default to covering each available, relevant category. Skip only with a written reason: missing capability, failed access, explicit user scope restriction, or demonstrated irrelevance. “Probably irrelevant” is insufficient. Record unavailable or excluded sources as gaps, not zero-result searches. A source may be queried only within existing authorization; no contacting people, installing plugins, requesting broad permissions or writing data is implied.

## Investigate and synthesize

With delegation authorized and registered `poteto-agent` available, assign one investigator per available category with bounded, nonoverlapping source ownership. Give each [the investigator prompt](why/investigator-prompt.md), its category playbook, original question, code anchor, entry path and explicit read-only limits. Dispatch independent categories concurrently where supported. Preserve null results, exact searches, contradictory evidence and cross-category leads; do not let delegates search other categories silently.

Resolve each investigator via `runtime.py resolve PROJECT why-investigator`, using the actual parent pair, task override when supplied, and a current catalog. Use the resolved model/effort in the native spawn. After all results return, resolve `why-synthesizer` and give one `poteto-agent` [the synthesizer prompt](why/synthesizer-prompt.md), all findings, skips, code anchor, question and the full epistemics reference. It must spot-check citations with actual available read tools. Custom agents inherit parent MCP/provider/permissions; do not claim an Antigravity research/self tool distinction or guaranteed access inside a delegate. An inaccessible source is a reported gap.

No role or spawn/delegation authorization: use the documented primary-only read path, keeping the same coverage map and confidence requirements, and disclose that no investigator/synthesizer agent ran. Never install roles or change trust as a research side effect. Invalid explicit model/effort or a rejected native selection blocks that step; do not replace the selection or invoke fallback to evade it. The narrow inline shortcut applies only when all seven categories have been assessed and further available searches are demonstrably redundant; explain that judgment.

## Present

Use The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted and Confidence Summary as applicable. Keep **Direct / Supported / Inferred / Speculative / Unknown** distinct. Direct and Supported claims need precise adjacent citations; inference must expose its evidence chain and uncertainty. Current code is mechanics, not proof of its author's intent. Include one Sources Consulted line per category, including empty, excluded or unavailable ones and the reason. Surface contradictions rather than choosing a tidy narrative. Preserve the synthesizer's calibrated confidence; inspect citations yourself before presenting.

If this investigation precedes a requested change, derive Preserve / Change / Avoid / Risk constraints from the findings; it does not authorize implementation. Before answering, audit named principles and execution claims against actual tool records and recheck state. Report failed inspections honestly.

Source: `skills/why/SKILL.md` and its references at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Codex adaptation removes Antigravity-specific tool/model paths, uses current tool discovery and existing scoped access, adds explicit no-mutation/fallback behavior, and preserves seven-category coverage, source-specific methods and confidence separation.
