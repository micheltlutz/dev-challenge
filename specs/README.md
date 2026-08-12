# The spec layer

`specs/` is the source of truth for this lab. Not the code, not the markdown in
`readme_files/` — this directory.

If you are here to *do* a challenge, jump to
[the challenge index](#challenge-index). If you are here to *change* something,
read [How it stays honest](#how-it-stays-honest) first.

## Why it exists

The challenges used to live as prose in `readme_files/`, and the prose drifted
from the API it described. Briefs documented `POST /create_contact` with a field
called `nome` while the running API served `POST /contact/` with `name` — so the
very first request a challenger made returned a 422 for reasons the
documentation could not explain.

Prose cannot be checked. This layer can:

```
app/ (reference API)
  └─ scripts/export_openapi.py ──→ specs/openapi.json ──┐
                                                         ├─→ specs/challenges/<id>/
Figma + mockups ──→ specs/design/tokens.json ───────────┘         │
                                                                  ├─→ harness/  (verification)
                                                                  └─→ AGENTS.md (coding agents)
```

Every arrow is enforced by CI.

## What is in here

| Path | What it is |
|---|---|
| [`openapi.json`](openapi.json) | The API contract. **Generated** — never edit by hand. |
| [`schema/challenge.schema.json`](schema/challenge.schema.json) | JSON Schema for challenge frontmatter. |
| `challenges/<id>/spec.md` | One challenge: frontmatter, objective, contract, requirements. |
| `challenges/<id>/acceptance.md` | Its acceptance criteria, each with a stable ID. |
| [`design/tokens.json`](design/tokens.json) | Design tokens in W3C DTCG format. |
| [`design/tokens.css`](design/tokens.css) | **Generated** from the JSON. |
| [`design/style-guide.md`](design/style-guide.md) | The design, readable without Figma. |
| [`design/screens.md`](design/screens.md) | Screen → mockup → Figma node → challenge. |

## The SDD loop

Spec-driven development, as this lab practises it:

1. **Read the spec.** `spec.md` for the contract, `acceptance.md` for what
   "done" means.
2. **Clarify.** Anything ambiguous is a bug in the spec — open an issue rather
   than guessing.
3. **Plan.** Decide your approach against the criteria, before writing code.
4. **Build.**
5. **Verify.** Run the harness. It reports per criterion, not per stack trace.
6. **Iterate** on the red ones.

The criteria are the contract. They are deliberately written before any
implementation exists, which is what makes them a specification rather than a
description of whatever got built.

## Anatomy of a challenge

```yaml
---
id: backend-05-balance          # must match the directory name
title: "Balance (amount)"
track: backend                  # backend | web | mobile | fullstack
order: 5                        # position within the track
difficulty: intermediate        # starter | intermediate | advanced
estimated_hours: 3
depends_on: ["backend-04-statements"]
endpoints: ["GET /balance/"]    # must exist in openapi.json
acceptance: acceptance.md
verify: "harness/suites/test_balance.py"
tags: ["auth", "business-rules", "scoping"]
---
```

Web and mobile challenges additionally carry `figma_node`, `mockups` and
`testids`. **`testids` is the contract that makes a UI verifiable** without
dictating a framework: expose those values as `data-testid` (web) or the
platform accessibility identifier (mobile), and the harness can drive your
interface whatever you built it with.

Acceptance criteria look like this, and the ID is load-bearing:

```markdown
### BE05-AC3 — Seeded balance is exact
Given John Doe's token
When GET /balance/
Then `amount` equals 15491.00 within 0.01
```

The harness marks each test with the ID it covers
(`@pytest.mark.ac("BE05-AC3")`), so a failure points straight back at the line
of specification it violates.

## How it stays honest

`.github/workflows/spec-drift.yml` fails the build when:

- `specs/openapi.json` no longer matches the reference API.
- `specs/design/tokens.css` no longer matches `tokens.json`.
- A spec lists an endpoint that does not exist in the contract.
- A spec references a mockup that is not on disk.
- `depends_on` points at a missing challenge, or the graph has a cycle.
- Two criteria share an ID.
- A criterion has no harness test covering it.
- `scripts/seed.py` is non-deterministic, or `dev-challenge.db` is stale.

Run the same checks locally:

```bash
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py
```

## Challenge index

### Back-end — reimplement the API in your language

| # | Challenge | Difficulty | ~h |
|---|---|---|---|
| 1 | [Contact route](challenges/backend-01-contact/spec.md) | starter | 1.5 |
| 2 | [Create user route](challenges/backend-02-create-user/spec.md) | starter | 3 |
| 3 | [Login route](challenges/backend-03-login/spec.md) | intermediate | 3 |
| 4 | [Statement list with pagination](challenges/backend-04-statements/spec.md) | intermediate | 4 |
| 5 | [Balance (amount)](challenges/backend-05-balance/spec.md) | intermediate | 3 |
| 6 | [Edit profile route](challenges/backend-06-profile-edit/spec.md) | advanced | 3 |

### Web — build the interface against the provided API

| # | Challenge | Difficulty | ~h |
|---|---|---|---|
| 1 | [Contact form](challenges/web-01-contact-form/spec.md) | starter | 3 |
| 2 | [Create account form](challenges/web-02-create-account/spec.md) | starter | 4 |
| 3 | [Login form](challenges/web-03-login/spec.md) | intermediate | 4 |
| 4 | [Dashboard shell](challenges/web-04-dashboard/spec.md) | intermediate | 5 |
| 5 | [Statement, balance and pagination](challenges/web-05-statement/spec.md) | advanced | 6 |
| 6 | [Edit profile](challenges/web-06-profile-edit/spec.md) | advanced | 4 |

### Mobile — build the native app against the provided API

| # | Challenge | Difficulty | ~h |
|---|---|---|---|
| 1 | [Create account screen](challenges/mobile-01-create-account/spec.md) | starter | 4 |
| 2 | [Login screen](challenges/mobile-02-login/spec.md) | intermediate | 4 |
| 3 | [Dashboard and drawer](challenges/mobile-03-dashboard/spec.md) | intermediate | 5 |
| 4 | [Statement, balance and pagination](challenges/mobile-04-statement/spec.md) | advanced | 6 |
| 5 | [Edit profile](challenges/mobile-05-profile-edit/spec.md) | advanced | 4 |

Mobile challenges are **not automatically verified** — see each spec.

### Fullstack — own both ends of the contract

| # | Challenge | Difficulty | ~h |
|---|---|---|---|
| 1 | [Contact, end to end](challenges/fullstack-01-contact/spec.md) | starter | 5 |
| 2 | [Authentication, end to end](challenges/fullstack-02-auth/spec.md) | intermediate | 8 |
| 3 | [Statement and balance, end to end](challenges/fullstack-03-statement/spec.md) | advanced | 10 |

## Fixture data

Both demo users have the password `Challenge@123`:

| User | Statements | Balance |
|---|---|---|
| `john.doe@email.com` | 5 | 15491.00 |
| `jane.roe@email.com` | 1 | 4200.00 |

The database also contains 40 statements belonging to neither. If those appear
in either user's results, per-user scoping is broken. Rebuild the fixture at any
time with `python scripts/seed.py`.

## Adding or changing a challenge

See the `spec-authoring` skill in [`../.claude/skills/`](../.claude/skills/), or
[`../CONTRIBUTING.md`](../CONTRIBUTING.md). The short version: a spec change and
its harness test land in the same pull request, or CI rejects it.
