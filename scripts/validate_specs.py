#!/usr/bin/env python
"""Validate the spec layer's internal consistency.

This is the guard that keeps `specs/` honest. It checks that:

1. Every challenge's frontmatter validates against `specs/schema/challenge.schema.json`.
2. The `id` matches the directory it lives in, and `(track, order)` is unique.
3. Every endpoint listed exists in `specs/openapi.json`.
4. Every mockup path exists on disk.
5. `depends_on` references real challenges, stays within sensible tracks, and
   forms a DAG.
6. `acceptance.md` exists and its criterion IDs are well-formed and unique
   across the whole repository.
7. Every acceptance criterion is covered by a harness test marked with its ID
   (only enforced once the harness module referenced by `verify:` exists).
8. Every relative link and image in the docs points at something that exists.
   The old briefs shipped broken image links for months; this is the guard.

Exit code is 0 when everything holds, 1 otherwise.

Usage::

    python scripts/validate_specs.py
    python scripts/validate_specs.py --quiet
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - dependency hint
    print(
        "Missing dependency: jsonschema.\n"
        "Install the dev requirements: pip install -r requirements_for_dev.txt"
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS = REPO_ROOT / "specs"
CHALLENGES = SPECS / "challenges"
SCHEMA_PATH = SPECS / "schema" / "challenge.schema.json"
OPENAPI_PATH = SPECS / "openapi.json"

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
AC_HEADING = re.compile(r"^###\s+([A-Z]{2,4}[0-9]{2}-AC[0-9]+)\s+—\s+(.+)$", re.MULTILINE)
# A criterion that no automated runner can check declares so explicitly, so
# "uncovered" always means "we forgot" rather than "we couldn't".
MANUAL_MARKER = "> **Manual review.**"
AC_MARK = re.compile(r"""@pytest\.mark\.ac\(\s*["']([A-Z0-9-]+)["']""")
TS_MARK = re.compile(r"""\bac\(\s*["']([A-Z0-9-]+)["']""")

errors: list[str] = []
warnings: list[str] = []


def error(challenge: str, message: str) -> None:
    errors.append(f"{challenge}: {message}")


def warn(challenge: str, message: str) -> None:
    warnings.append(f"{challenge}: {message}")


def load_frontmatter(spec_path: Path):
    text = spec_path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return None, text
    return yaml.safe_load(match.group(1)), text


def openapi_operations() -> set[str]:
    document = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    operations = set()
    for path, methods in document["paths"].items():
        for method in methods:
            if method.lower() in {"get", "post", "put", "patch", "delete"}:
                operations.add(f"{method.upper()} {path}")
    return operations


def detect_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    """Return one cycle as a path, or None if the graph is acyclic."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(graph, WHITE)
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        colour[node] = GREY
        stack.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in colour:
                continue
            if colour[neighbour] == GREY:
                return stack[stack.index(neighbour):] + [neighbour]
            if colour[neighbour] == WHITE:
                found = visit(neighbour)
                if found:
                    return found
        stack.pop()
        colour[node] = BLACK
        return None

    for node in graph:
        if colour[node] == WHITE:
            found = visit(node)
            if found:
                return found
    return None


def collect_harness_marks() -> set[str]:
    """Every AC id referenced by a harness test, across Python and TS suites."""
    marks: set[str] = set()
    harness = REPO_ROOT / "harness"
    if not harness.is_dir():
        return marks
    for path in harness.rglob("*.py"):
        marks.update(AC_MARK.findall(path.read_text(encoding="utf-8")))
    for pattern in ("*.ts", "*.js", "*.yaml", "*.yml"):
        for path in harness.rglob(pattern):
            marks.update(TS_MARK.findall(path.read_text(encoding="utf-8")))
    return marks


MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

# Docs whose relative links are checked. Anything outside these is not ours.
LINKED_DOCS = ("specs/**/*.md", "readme_files/*.md", "harness/**/*.md", "*.md")


def check_links() -> None:
    for pattern in LINKED_DOCS:
        for document in sorted(REPO_ROOT.glob(pattern)):
            if "venv" in document.parts or "node_modules" in document.parts:
                continue
            label = str(document.relative_to(REPO_ROOT))
            for match in MD_LINK.finditer(document.read_text(encoding="utf-8")):
                target = match.group(1).split()[0].split("#")[0]
                if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                    continue
                if not (document.parent / target).resolve().exists():
                    error(label, f"broken link {target!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="Only print problems.")
    parser.add_argument(
        "--skip-links",
        action="store_true",
        help="Skip the relative-link check (useful mid-refactor).",
    )
    args = parser.parse_args()

    if not OPENAPI_PATH.exists():
        print("specs/openapi.json is missing. Run: python scripts/export_openapi.py")
        sys.exit(1)

    validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    operations = openapi_operations()
    harness_marks = collect_harness_marks()

    directories = sorted(d for d in CHALLENGES.iterdir() if d.is_dir())
    if not directories:
        print("No challenges found under specs/challenges/")
        sys.exit(1)

    frontmatters: dict[str, dict] = {}
    all_ac_ids: dict[str, str] = {}
    seen_order: dict[tuple[str, int], str] = {}
    total_acs = 0

    for directory in directories:
        name = directory.name
        spec_path = directory / "spec.md"
        acceptance_path = directory / "acceptance.md"

        if not spec_path.exists():
            error(name, "missing spec.md")
            continue

        frontmatter, _ = load_frontmatter(spec_path)
        if frontmatter is None:
            error(name, "spec.md has no YAML frontmatter")
            continue

        for problem in sorted(validator.iter_errors(frontmatter), key=lambda e: e.path):
            location = "/".join(str(p) for p in problem.path) or "(root)"
            error(name, f"frontmatter {location}: {problem.message}")

        challenge_id = frontmatter.get("id")
        if challenge_id != name:
            error(name, f"id {challenge_id!r} does not match its directory name")
            continue

        frontmatters[challenge_id] = frontmatter

        track, order = frontmatter.get("track"), frontmatter.get("order")
        if isinstance(order, int):
            key = (track, order)
            if key in seen_order:
                error(name, f"track/order {track}/{order} already used by {seen_order[key]}")
            seen_order[key] = challenge_id

        for endpoint in frontmatter.get("endpoints", []):
            if endpoint not in operations:
                error(name, f"endpoint {endpoint!r} is not in specs/openapi.json")

        for mockup in frontmatter.get("mockups", []) or []:
            if not (REPO_ROOT / mockup).exists():
                error(name, f"mockup {mockup!r} does not exist")

        verify = frontmatter.get("verify")
        if verify and not (REPO_ROOT / verify).exists():
            warn(name, f"verify target {verify!r} does not exist yet")

        # Acceptance criteria
        if not acceptance_path.exists():
            error(name, "missing acceptance.md")
            continue

        acceptance_text = acceptance_path.read_text(encoding="utf-8")
        criteria = AC_HEADING.findall(acceptance_text)

        # Which criteria opted out of automated coverage.
        manual: set[str] = set()
        headings = list(AC_HEADING.finditer(acceptance_text))
        for index, match in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(acceptance_text)
            if MANUAL_MARKER in acceptance_text[match.end():end]:
                manual.add(match.group(1))

        if not criteria:
            error(name, "acceptance.md declares no criteria (expected '### XX00-ACn — title')")
            continue

        total_acs += len(criteria)
        for ac_id, _title in criteria:
            if ac_id in all_ac_ids:
                error(name, f"criterion id {ac_id} is already used by {all_ac_ids[ac_id]}")
            all_ac_ids[ac_id] = challenge_id

        # Only demand harness coverage once the referenced module actually exists.
        if verify and (REPO_ROOT / verify).exists():
            uncovered = [
                ac for ac, _ in criteria if ac not in harness_marks and ac not in manual
            ]
            if uncovered:
                error(
                    name,
                    f"{len(uncovered)} criteria have no harness test: {', '.join(uncovered)}",
                )

    # Dependency graph
    graph = {cid: list(fm.get("depends_on", []) or []) for cid, fm in frontmatters.items()}
    for challenge_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in frontmatters:
                error(challenge_id, f"depends_on unknown challenge {dependency!r}")

    cycle = detect_cycle(graph)
    if cycle:
        errors.append("dependency cycle: " + " -> ".join(cycle))

    if not args.skip_links:
        check_links()

    # Report
    if not args.quiet:
        print(f"Checked {len(frontmatters)} challenges, {total_acs} acceptance criteria.")
        by_track: dict[str, int] = {}
        for frontmatter in frontmatters.values():
            by_track[frontmatter["track"]] = by_track.get(frontmatter["track"], 0) + 1
        for track in ("backend", "web", "mobile", "fullstack"):
            if track in by_track:
                print(f"  {track:<10} {by_track[track]}")
        if harness_marks:
            print(f"  harness covers {len(harness_marks)} criterion ids")

    for message in warnings:
        print(f"WARN  {message}")
    for message in errors:
        print(f"ERROR {message}")

    if errors:
        print(f"\n{len(errors)} problem(s) found.")
        sys.exit(1)

    if not args.quiet:
        print("\nSpec layer is consistent.")


if __name__ == "__main__":
    main()
