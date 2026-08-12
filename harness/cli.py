#!/usr/bin/env python
"""``dev-challenge-harness`` — verify a solution against the acceptance criteria.

Thin wrapper over pytest so a challenger never has to know it is pytest.

    dev-challenge-harness --base-url http://localhost:3000 --challenge backend-05-balance
    dev-challenge-harness --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HARNESS_DIR))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dev-challenge-harness",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Base URL of the API under test (default: %(default)s).",
    )
    parser.add_argument(
        "--challenge",
        help="Challenge id, e.g. backend-05-balance. Omit to run every suite.",
    )
    parser.add_argument("--list", action="store_true", help="List challenges and exit.")
    parser.add_argument("--report-json", help="Write the scorecard as JSON here.")
    parser.add_argument("--report-markdown", help="Write the scorecard as Markdown here.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Full pytest output.")
    return parser


def list_challenges() -> int:
    from specs_index import load_challenges

    challenges = load_challenges()
    by_track: dict[str, list] = {}
    for challenge in challenges.values():
        by_track.setdefault(challenge.track, []).append(challenge)

    for track in ("backend", "web", "mobile", "fullstack"):
        if track not in by_track:
            continue
        print(f"\n{track}")
        for challenge in sorted(by_track[track], key=lambda c: c.id):
            note = "" if challenge.verifiable else "   (self-review, no automated runner)"
            print(f"  {challenge.id:<32} {len(challenge.criteria):>2} criteria{note}")
    print()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list:
        return list_challenges()

    import pytest

    pytest_args = [
        str(HARNESS_DIR / "suites"),
        "--base-url",
        args.base_url,
        "-p",
        "no:cacheprovider",
        "--no-header",
    ]
    pytest_args += ["-v"] if args.verbose else ["-q", "--tb=no"]

    if args.challenge:
        pytest_args += ["--challenge", args.challenge]
    if args.report_json:
        pytest_args += ["--report-json", args.report_json]
    if args.report_markdown:
        pytest_args += ["--report-markdown", args.report_markdown]

    # conftest.py lives at the harness root, one level above suites/.
    pytest_args += ["--rootdir", str(HARNESS_DIR), "-c", str(HARNESS_DIR / "pytest.ini")]

    return pytest.main(pytest_args)


if __name__ == "__main__":
    raise SystemExit(main())
