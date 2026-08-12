# CLAUDE.md

@AGENTS.md

Everything above applies. What follows is Claude Code specific.

## The one rule to internalise

Read `specs/challenges/<id>/spec.md` and `acceptance.md` before answering
anything about what a challenge requires. Never answer from `readme_files/`
(redirect stubs) or from how such an API usually works.

And decide which job you are doing — **mentoring a learner** or **improving the
lab**. The default when someone is working through a challenge is to coach, not
to hand over the implementation. See "First: which job are you doing?" in
[`AGENTS.md`](AGENTS.md).

## Slash commands

| Command | What it does |
|---|---|
| `/challenge <id>` | Load a challenge's spec, criteria and design tokens, and start work on it |
| `/verify [id]` | Run the harness and explain failures in terms of the criteria |
| `/next` | Suggest what to do next from the dependency graph and what currently passes |

`/challenge <id> --solve` switches to solver mode explicitly.

## Subagents

| Agent | Use it for |
|---|---|
| `challenge-mentor` | Reviewing a learner's work without solving it for them |
| `spec-auditor` | Checking a spec change against the contract before a PR |

## Skills

| Skill | Loads when |
|---|---|
| `challenge-workflow` | Someone is working through a challenge |
| `design-fidelity` | Comparing an implemented UI against the tokens and mockups |
| `spec-authoring` | Adding or editing a challenge in `specs/` |

## MCP

[`.mcp.json`](.mcp.json) declares an optional Figma Dev Mode server. With it,
you can pull real node specs instead of inferring layout from a PNG. It needs
the user's own Figma token and is inert without one — the sampled tokens in
`specs/design/tokens.json` are the fallback, and they are good enough for every
challenge.

## Working in this repo

- The venv is at `./venv`. Use `./venv/bin/python`, or activate it.
- Before saying you are done, run what CI runs (see Commands in `AGENTS.md`).
- `dev-challenge.db` is generated. Change `scripts/seed.py` and regenerate; do
  not hand-edit it.
- `specs/openapi.json` and `specs/design/tokens.css` are generated. Same rule.
