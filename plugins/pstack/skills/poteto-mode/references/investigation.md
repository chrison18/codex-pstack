# Investigation

This route produces a cited answer or recommendation. It does not authorize code, configuration, repository or remote mutations.

1. Inspect relevant call paths and, for motivation questions, relevant history. State `throughput checkpoint: n/a, read-only investigation`.
2. Keep the checklist in the conversation or an explicitly provided external scratch file. Do not create a checklist or install roles inside the investigated repository. Inspect tracked and untracked state before and after without changing it. For stronger enforcement, use a parent read-only sandbox; a role's prose is not a separate permission boundary.
3. A registered `poteto-agent` may gather scoped evidence under an explicit read-only assignment when delegation is authorized. Never install a missing role as a side effect of an investigation. Without it, gather evidence in the primary and disclose that no custom role ran.
4. Write Overview, Key Concepts, How It Works, Where Things Live and Gotchas, or a recommendation with a tradeoffs table. Cite actual files and lines or fetched sources. Distinguish observation, inference and uncertainty. No PR or code change follows automatically; a later requested change routes as a new Feature or Bug fix task.

Full `how`, `why` and prose skills remain phase 3 dependencies. This route uses direct evidence gathering rather than claiming those skills loaded.
