"""Reproduce the reviewed source-to-Codex principle adaptation; default is check-only."""

import argparse
from pathlib import Path
import json
import re


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true', help='Regenerate the reviewed package leaves and index')
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent


def emit(path, content):
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    elif not path.is_file() or path.read_text() != content:
        raise SystemExit('Principle adaptation differs: ' + str(path.relative_to(root)))



out = root / 'plugins/pstack/skills/poteto-mode/references/principles'
changes = {
 'principle-never-block-on-the-human': [
 ('The human supervises asynchronously. Agents must stay unblocked.', 'The human supervises asynchronously. Continue authorized work without unnecessary blocking. This principle never expands the user\'s scope or the host\'s permissions.'),
 ('Irreversible actions (force-push, delete production data, send external messages) still require confirmation.', 'Actions such as force-push, production deletion, and sending external messages still require applicable authorization. Existing explicit authorization counts; do not ask again merely because the action is mentioned here.')],
 'principle-sequence-verifiable-units': [('Rebase onto clean trunk first so every check measures against the real baseline.', 'Start from the latest agreed base so every check measures against a known baseline. Respect repository Git rules: do not rewrite a shared branch; merge base updates when required.')],
 'principle-prove-it-works': [
 ('(the **show-me-your-work** skill)', '(an auditable evidence trail; the full **show-me-your-work** lifecycle skill is not yet available in this package)'),
 ('## Script the check when you can', '**Evidence accounting.** Separate static reasoning, planned checks and checks actually executed. A mentally simulated result is not an executed reproduction. Report a check as completed only with an observed command/output or inspected artifact; otherwise label it inferred or not run.\n\n## Script the check when you can')],
 'principle-explain-the-number': [('For a performance number, run the full procedure with the [benchmark-checklist](../benchmark-checklist/SKILL.md) skill.', 'For a performance number, use a repeatable benchmark procedure with comparable work, controlled settings, repeated runs, spread and a measured limiter. The full **benchmark-checklist** skill is not yet available in this package; do not claim it ran.')],
 'principle-type-system-discipline': [('For TypeScript syntax, see the `typescript-best-practices` skill.', 'The dedicated `typescript-best-practices` skill is not yet available in this package; use the project\'s existing TypeScript conventions and authoritative compiler documentation for syntax.')],
 'principle-guard-the-context-window': [('Route bulk to subagents; keep summaries in the main thread, not raw payloads.', 'Use bounded searches and summaries; route bulk to subagents only when delegation is authorized. Keep summaries in the main thread, not raw payloads.')],
 'principle-separate-before-serializing-shared-state': [('Give each actor its own owned file, key, branch, or state directory, and merge only at the read/reporting boundary.', 'Give each actor its own owned file, key, branch, or state directory, and merge only at the read/reporting boundary. Concurrent code writers need separate worktrees and named starting refs; separate branches alone do not isolate a shared checkout. A spawn alone establishes no isolation.')],
}
sources = sorted((root / 'skills').glob('principle-*/SKILL.md'))
if len(sources) != 24:
    raise SystemExit('Reconcile the inherited 24-principle baseline before regeneration')
rows = []
for source in sources:
    text = source.read_text()
    meta, body = text.split('---', 2)[1:]
    description = json.loads(re.search(r'^description: (.+)$', meta, re.M)[1])
    name = source.parent.name
    title, rest = body.strip().split('\n', 1)
    result = title + '\n\nWhen to read: ' + description + '\n' + rest
    for old, new in changes.get(name, []):
        if result.count(old) != 1:
            raise ValueError((name, old))
        result = result.replace(old, new)
    result = re.sub(r'\.\./(principle-[^/]+)/SKILL\.md', r'\1.md', result)
    result += ('\n\nSource: `' + source.relative_to(root).as_posix() +
               '` at inherited baseline `a06537a883278a63132e2518971166002f3de5de`. '
               'Host adaptations are recorded in the phase 3 principles evidence.\n')
    emit(out / (name + '.md'), result)
    rows.append((name, title.removeprefix('# '), description))
index = '''# Applicable principles

These 24 full leaves are adapted from the inherited pstack principles. They are reference material inside the explicitly activated Poteto workflow, not additional native skill entries. Select only the leaves relevant to the current decision and read those leaves in full before applying them. Name a principle only after reading its full leaf and only when it changed a concrete decision. Reading this index does not complete that step. The user\'s scope, host permissions and repository Git rules still govern execution.

| Decision | Read in full |
| --- | --- |
'''
for name, title, desc in rows:
    index += '| ' + desc.replace('|', '\\|') + ' | [' + title + '](principles/' + name + '.md) |\n'
emit(out.parent / 'principles.md', index)
if {path.name for path in out.glob('*.md')} != {name + '.md' for name, _, _ in rows}:
    raise SystemExit('Unexpected principle references; reconcile package inventory')
print('Checked all ' + str(len(rows)) + ' full principle adaptations.')
