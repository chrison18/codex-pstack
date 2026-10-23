# Laziness Protocol

When to read: Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem.

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.

Source: `skills/principle-laziness-protocol/SKILL.md` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. Host adaptations are recorded in the phase 3 principles evidence.
