---
description: Start work on a dev-challenge exercise — loads its spec, criteria and design tokens
argument-hint: <challenge-id> [--solve]
allowed-tools: Read, Grep, Glob, Bash(python harness/cli.py:*), Bash(python scripts/validate_specs.py:*)
---

Start work on challenge `$1`.

## Load the context

1. Read `specs/challenges/$1/spec.md`. If the directory does not exist, run
   `python harness/cli.py --list` and suggest the closest match.
2. Read `specs/challenges/$1/acceptance.md`.
3. If the frontmatter has `mockups:` or `figma_node:`, also read
   `specs/design/style-guide.md` and note the `testids:` list.
4. Check `depends_on:` — if a prerequisite has not been done, say so before
   starting.

## Then

Give the person a short orientation, not a wall of text:

- What they are building, in two or three sentences.
- The contract: endpoints, request and response shapes, status codes.
- The acceptance criteria as a numbered checklist, with IDs.
- Anything the spec leaves genuinely ambiguous.
- The one trap most people hit on this specific challenge.

Then ask what their approach is, and work from there.

## Posture

**Default: mentor.** Plan with them, review what they write, explain failing
criteria. Do not write the implementation. Scaffolding, config and boilerplate
are fine to write outright — nobody learns from a `tsconfig.json`.

**If `$ARGUMENTS` contains `--solve`**, or they ask directly, switch to solver
mode: say you have switched, then implement it properly and walk them through
the reasoning as you go.

See the `challenge-workflow` skill for the full loop.

## Verifying

```
python harness/cli.py --base-url <their-url> --challenge $1
```

Mobile challenges have no automated runner — say so plainly rather than
implying coverage that does not exist.
