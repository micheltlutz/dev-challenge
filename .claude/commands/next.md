---
description: Suggest which dev-challenge exercise to do next
argument-hint: [track]
allowed-tools: Read, Grep, Glob, Bash(python harness/cli.py:*)
---

Suggest what to work on next.

## Gather

1. `python harness/cli.py --list` — every challenge and its criterion count.
2. Read the `depends_on`, `difficulty` and `estimated_hours` frontmatter across
   `specs/challenges/*/spec.md`.
3. If you know where their app runs, run the harness to see what already
   passes. If not, ask what they have finished rather than assuming.
4. If `$ARGUMENTS` names a track, restrict to it.

## Choose

- Never suggest a challenge whose `depends_on` is unmet — say what to do first.
- Prefer the lowest `order` among the unblocked ones; the tracks are built to
  be climbed.
- If they have just finished something hard, a `starter` on another track is a
  reasonable change of pace. Offer it, do not insist.
- Someone who has finished a backend and a web challenge on the same feature is
  ready for the fullstack track — that is where SDD actually pays off, because
  neither side of the contract is given to them.

## Say

- The recommendation, and why it follows from what they have done.
- What it builds on, and what it unlocks.
- Difficulty and rough hours.
- One alternative, if there is a sensible one.

Keep it to a few lines. Then offer to run `/challenge <id>`.

If everything in a track is done, say so and point at another track or at
[`ROADMAP.md`](../../ROADMAP.md) — contributing a challenge is the natural next
step for someone who has finished one.
