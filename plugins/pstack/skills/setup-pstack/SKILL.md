---
name: setup-pstack
description: Configure project-scoped pstack agents and role model choices when explicitly invoked as $setup-pstack.
---

# Setup pstack for Codex

Read the [runtime contract](../poteto-mode/references/runtime.md). Resolve the sibling poteto-mode directory relative to this file; its script is `../poteto-mode/scripts/runtime.py`.

Inspect current project state and the available native model catalog. Show the two project roles, current saved choices and proposed changes. Default every role to inheritance of the parent model and effort. Do not map Gemini tiers to guessed Codex models. Treat model identifier and reasoning effort separately.

For requested setup, use the runtime script's `install` command at the named project. It refuses existing or modified role files. Trust and restart requirements are reported to the user; do not change global settings or trust automatically. For requested model changes, use `configure` with the chosen role and validated model/effort. Do not change unrelated roles. Re-running setup must preserve existing choices. The script's `verify` command checks role integrity and `resolve` reports the chosen spawn settings without changing preferences.

Explain removal via `uninstall`: it removes only unchanged owned roles, retains saved model choices, and does not remove a separately installed short-name skill link. Do not claim that setup activates poteto-mode, registers roles in the current already-running chat, or proves desktop runtime acceptance. Do not begin a feature or bug workflow merely because setup completed.
