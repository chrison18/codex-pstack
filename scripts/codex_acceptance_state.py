"""Capture fixture entries without following symlinks; Git metadata is checked separately."""

import hashlib
import os
from pathlib import Path
import stat


def snapshot(workspace):
    workspace = Path(workspace)
    entries = {}
    for path in [workspace, *workspace.rglob('*')]:
        relative = path.relative_to(workspace)
        if relative.parts and relative.parts[0] == '.git':
            continue
        mode = path.lstat().st_mode
        entry = {'mode': stat.S_IMODE(mode)}
        if stat.S_ISLNK(mode):
            entry.update(kind='symlink', target=os.readlink(path))
        elif stat.S_ISREG(mode):
            entry.update(kind='file', sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        elif stat.S_ISDIR(mode):
            entry.update(kind='directory')
        else:
            entry.update(kind='special', fileType=stat.S_IFMT(mode))
        entries[str(relative)] = entry
    return entries
