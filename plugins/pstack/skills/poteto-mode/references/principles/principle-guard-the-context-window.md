# Guard the Context Window

When to read: Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Use bounded searches and summaries; route bulk to subagents only when delegation is authorized. Keep summaries in the main thread, not raw payloads.

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.

Source: `skills/principle-guard-the-context-window/SKILL.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Host adaptations are recorded in the phase 3 principles evidence.
