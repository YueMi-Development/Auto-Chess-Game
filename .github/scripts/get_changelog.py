#!/usr/bin/env python3
"""
Extract a changelog section for a given tag from CHANGELOG.md.

Usage:
    python get_changelog.py v1.0.0

The script looks for `## <tag>` in CHANGELOG.md and outputs everything
between that heading and the next `---` or end of file.
"""

import sys
import re
from pathlib import Path


def extract_changelog(tag: str, changelog_path: Path) -> str:
    """
    Extract the changelog body for `tag` from `changelog_path`.

    Returns the content after `## <tag>` up to the next `---` or `## `.
    Returns empty string if tag is not found.
    """
    content = changelog_path.read_text(encoding="utf-8")

    # Match `## <tag>` (case-sensitive, no leading spaces)
    pattern = re.compile(rf"^##\s+{re.escape(tag)}\s*$", re.MULTILINE)
    match = pattern.search(content)

    if not match:
        return ""

    start = match.end()
    # Find next `---` or `## ` after the tag line
    rest = content[start:]
    next_sep = re.search(r"^---$|^\#\# ", rest, re.MULTILINE)

    if next_sep:
        section = rest[: next_sep.start()]
    else:
        section = rest

    # Strip leading/trailing blank lines
    return section.strip()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python get_changelog.py <tag>", file=sys.stderr)
        sys.exit(1)

    tag = sys.argv[1]

    # Resolve relative to this script's directory
    script_dir = Path(__file__).parent.resolve()
    changelog_path = script_dir.parent / "files" / "CHANGELOG.md"

    section = extract_changelog(tag, changelog_path)

    if not section:
        print(f"# {tag}\n\n_No changes recorded._", file=sys.stderr)
        return

    # Output for GitHub Actions — print raw so it can be captured
    print(section)


if __name__ == "__main__":
    main()
