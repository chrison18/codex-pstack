"""Add the explicit poteto-mode entry to an existing project without overwriting skills."""

import argparse
from pathlib import Path
import sys


def link_entry(project):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError("Project must be an existing directory")
    source = Path(__file__).resolve().parent.parent / "plugins/pstack/skills/poteto-mode"
    if not (source / "SKILL.md").is_file():
        raise ValueError("Codex preview source is missing")
    destination = project / ".agents/skills/poteto-mode"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.symlink_to(source, target_is_directory=True)
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Existing project directory")
    arguments = parser.parse_args()
    try:
        print(link_entry(arguments.project))
    except FileExistsError:
        print("An entry already exists at .agents/skills/poteto-mode; no skill was changed.", file=sys.stderr)
        raise SystemExit(1)
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
