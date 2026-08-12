#!/usr/bin/env python
"""Generate ``specs/design/tokens.css`` from ``specs/design/tokens.json``.

Flattens the DTCG token tree into CSS custom properties so a front-end can drop
the file in and start using the design system immediately. Front-ends that need
another format (Tailwind config, Swift, Kotlin, Dart) should transform the JSON
rather than hand-copying values.

Usage::

    python scripts/build_tokens.py           # write tokens.css
    python scripts/build_tokens.py --check   # exit 1 if it would change
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "specs" / "design" / "tokens.json"
OUTPUT = REPO_ROOT / "specs" / "design" / "tokens.css"

# Keys that carry metadata rather than tokens.
META_KEYS = {"$type", "$description", "$schema", "$extensions"}


def format_value(value):
    if isinstance(value, list):
        return ", ".join(f'"{v}"' if " " in v else v for v in value)
    if isinstance(value, dict):
        # A shadow token.
        return (
            f"{value['offsetX']} {value['offsetY']} {value['blur']} "
            f"{value.get('spread', '0px')} {value['color']}"
        )
    return str(value)


def flatten(node, prefix=()):
    """Yield ``(css-variable-name, value, description)`` for every leaf token."""
    for key, child in node.items():
        if key in META_KEYS:
            continue
        if not isinstance(child, dict):
            continue
        path = (*prefix, key)
        if "$value" in child:
            yield "-".join(path), format_value(child["$value"]), child.get("$description")
        else:
            yield from flatten(child, path)


def render() -> str:
    tokens = json.loads(SOURCE.read_text(encoding="utf-8"))

    lines = [
        "/* Generated from specs/design/tokens.json by scripts/build_tokens.py.",
        " * Do not edit by hand -- edit the JSON and regenerate.",
        " */",
        ":root {",
    ]

    current_group = None
    for name, value, description in flatten(tokens):
        group = name.split("-", 1)[0]
        if group != current_group:
            lines.append("" if current_group else "")
            lines.append(f"  /* {group} */")
            current_group = group
        comment = f"  /* {description} */" if description else ""
        lines.append(f"  --{name}: {value};{comment}")

    lines.append("}")
    return "\n".join(lines).replace("\n\n\n", "\n\n") + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Exit 1 if tokens.css is stale.")
    args = parser.parse_args()

    css = render()

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != css:
            print("specs/design/tokens.css is out of date. Run: python scripts/build_tokens.py")
            sys.exit(1)
        print("specs/design/tokens.css is up to date.")
        return

    OUTPUT.write_text(css, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
