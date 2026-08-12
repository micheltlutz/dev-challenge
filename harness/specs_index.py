"""Read the spec layer so the harness can report in the specification's terms.

The harness never hard-codes a criterion's text. It parses
``specs/challenges/*/acceptance.md`` at run time, so a scorecard always quotes
the spec as it exists in the checkout being tested -- and a criterion that is
renamed or removed shows up immediately instead of silently drifting.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

AC_HEADING = re.compile(r"^###\s+([A-Z]{2,4}[0-9]{2}-AC[0-9]+)\s+—\s+(.+)$", re.MULTILINE)
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SIMPLE_FIELD = re.compile(r"^(\w+):\s*(.*)$")


@dataclass
class Criterion:
    id: str
    title: str
    challenge: str
    body: str = ""


@dataclass
class Challenge:
    id: str
    title: str
    track: str
    verifiable: bool = True
    criteria: list[Criterion] = field(default_factory=list)


def specs_root() -> Path:
    """Locate ``specs/``.

    Honours ``DEV_CHALLENGE_SPECS`` so the Docker image can point at the copy
    baked into it; otherwise walks up from this file looking for the directory.
    """
    override = os.environ.get("DEV_CHALLENGE_SPECS")
    if override:
        return Path(override)
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "specs" / "challenges"
        if candidate.is_dir():
            return parent / "specs"
    raise RuntimeError(
        "Could not locate specs/. Set DEV_CHALLENGE_SPECS to its path."
    )


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    parsed: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith(" ") or line.startswith("-"):
            continue
        field_match = SIMPLE_FIELD.match(line)
        if field_match:
            parsed[field_match.group(1)] = field_match.group(2).strip().strip('"')
    return parsed


@lru_cache(maxsize=1)
def load_challenges() -> dict[str, Challenge]:
    challenges: dict[str, Challenge] = {}
    root = specs_root() / "challenges"

    for directory in sorted(root.iterdir()):
        spec_file = directory / "spec.md"
        acceptance_file = directory / "acceptance.md"
        if not spec_file.exists() or not acceptance_file.exists():
            continue

        frontmatter = _parse_frontmatter(spec_file.read_text(encoding="utf-8"))
        challenge = Challenge(
            id=frontmatter.get("id", directory.name),
            title=frontmatter.get("title", directory.name),
            track=frontmatter.get("track", "unknown"),
            verifiable=frontmatter.get("verifiable", "true") != "false",
        )

        acceptance_text = acceptance_file.read_text(encoding="utf-8")
        matches = list(AC_HEADING.finditer(acceptance_text))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(acceptance_text)
            body = acceptance_text[match.end():end].strip()
            challenge.criteria.append(
                Criterion(
                    id=match.group(1),
                    title=match.group(2).strip(),
                    challenge=challenge.id,
                    body=body,
                )
            )

        challenges[challenge.id] = challenge

    return challenges


@lru_cache(maxsize=1)
def criteria_by_id() -> dict[str, Criterion]:
    return {
        criterion.id: criterion
        for challenge in load_challenges().values()
        for criterion in challenge.criteria
    }


def criteria_for_challenge(challenge_id: str) -> list[str]:
    """AC ids belonging to a challenge.

    Fullstack challenges reuse the backend and web criteria by design, so their
    own `FSxx-*` ids are returned alongside whatever the harness has marked.
    """
    challenges = load_challenges()
    if challenge_id not in challenges:
        known = ", ".join(sorted(challenges))
        raise SystemExit(f"Unknown challenge {challenge_id!r}.\nKnown challenges: {known}")
    return [criterion.id for criterion in challenges[challenge_id].criteria]
