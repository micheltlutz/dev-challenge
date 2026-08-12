#!/usr/bin/env python
"""Export the reference API's OpenAPI document to ``specs/openapi.json``.

The committed document is the machine-readable contract that challenge specs
and the verification harness are checked against. CI regenerates it and fails
if the result differs from what is committed, which is what stops the specs
from drifting away from the code.

Usage::

    python scripts/export_openapi.py           # write specs/openapi.json
    python scripts/export_openapi.py --check   # exit 1 if it would change
"""

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

OUTPUT = REPO_ROOT / "specs" / "openapi.json"

# Pin the values that leak into the document so the output is reproducible on
# any machine, regardless of the developer's local .env.
os.environ.setdefault("DATABASE_URL", "sqlite:///./dev-challenge.db")
os.environ.setdefault("SECRET", "openapi-export-placeholder")


def render() -> str:
    from app.main import app

    return json.dumps(app.openapi(), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit non-zero if the committed file is stale.",
    )
    args = parser.parse_args()

    document = render()

    if args.check:
        if not OUTPUT.exists():
            print(
                f"{OUTPUT.relative_to(REPO_ROOT)} is missing. "
                "Run: python scripts/export_openapi.py"
            )
            sys.exit(1)
        if OUTPUT.read_text(encoding="utf-8") != document:
            print(
                f"{OUTPUT.relative_to(REPO_ROOT)} is out of date.\n"
                "The API changed but the committed contract did not.\n"
                "Run: python scripts/export_openapi.py"
            )
            sys.exit(1)
        print(f"{OUTPUT.relative_to(REPO_ROOT)} is up to date.")
        return

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(document, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
