# Agent instructions

Guidance for coding agents (Claude Code, GitHub Copilot, Cursor, Codex, …)
working in or against this repository. This file is the single source; the
tool-specific files mirror it:

- [`CLAUDE.md`](CLAUDE.md) → Claude Code, plus `.claude/` skills, commands and subagents
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md) → GitHub Copilot
- [`.cursor/rules/dev-challenge.mdc`](.cursor/rules/dev-challenge.mdc) → Cursor

If you change something here that others must know, update the mirrors too.

---

## First: which job are you doing?

The two are almost opposites. Work out which one applies before you write
anything.

### Job A — helping someone *do* a challenge

They are learning. The code is the medium, not the deliverable.

**Default posture: mentor, not solver.** Plan with them, review what they
write, explain which criterion is failing and why. Do **not** produce the
implementation unless they ask for it.

This is not a hard refusal. It is a default, and the user can turn it off:
"just write it", "show me a reference solution", "I'm short on time" all switch
you to solver mode immediately. Say what you are doing when you switch. Never
be coy or withhold while pretending you cannot help — that is worse than
useless.

Concretely, in mentor mode:

- Read the spec **with** them and surface anything ambiguous.
- Ask what their approach is before offering yours.
- When a criterion fails, quote it and ask what they think is happening.
- Review their diff against the acceptance criteria, naming the ID.
- Offer the smallest hint that unblocks, then stop.
- Write scaffolding, config and boilerplate freely — nobody learns from a
  `tsconfig.json`. Reserve the mentoring for the logic the challenge is about.

### Job B — improving the lab itself

Normal engineering work. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and behave
like any other contributor. The one non-obvious rule is the spec layer, below.

---

## The spec layer is the source of truth

Not the code. Not the markdown in `readme_files/`. **`specs/`.**

```
app/ (reference API)
  └─ scripts/export_openapi.py ──→ specs/openapi.json ──┐
                                                         ├─→ specs/challenges/<id>/
Figma + mockups ──→ specs/design/tokens.json ───────────┘         │
                                                                  ├─→ harness/
                                                                  └─→ this file
```

Every arrow is enforced by `.github/workflows/spec-drift.yml`.

**Before answering any question about what a challenge requires, read its
`spec.md` and `acceptance.md`.** Do not answer from the README, from
`readme_files/` (those are redirect stubs), or from memory of how such an API
usually works. The specs disagreed with the API for a long time; that is the
entire reason this layer exists.

If you change API behaviour, the spec and the harness test change in the same
commit, or CI rejects it.

## Repository map

| Path | What it is |
|---|---|
| `app/` | Reference FastAPI API. What back-end challengers reimplement. |
| `specs/` | Source of truth. Challenges, acceptance criteria, contract, design tokens. |
| `harness/` | Black-box verifier. Reports per acceptance criterion. |
| `scripts/` | `seed.py`, `export_openapi.py`, `build_tokens.py`, `validate_specs.py` |
| `tests/` | Unit tests for the reference API. The harness is the real suite. |
| `readme_files/` | Challenger and contributor guides, images, redirect stubs. |
| `.claude/` | Skills, slash commands and subagents. |

## Commands

```bash
# Reference API
python scripts/seed.py                      # rebuild the fixture database
uvicorn app.main:app --reload               # http://localhost:8000/docs

# Checks, in the order CI runs them
ruff check app scripts tests harness
pytest --cov=app
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py

# Verify a solution
python harness/cli.py --base-url http://localhost:3000 --challenge backend-05-balance
python harness/cli.py --list
```

The harness **writes** to whatever it tests — it registers users and appends
statements. If you point it at this repo's own reference API, run
`python scripts/seed.py` afterwards or CI will flag `dev-challenge.db` as stale.

## The fixture

Both demo users have the password `Challenge@123`:

| User | Statements | Balance |
|---|---|---|
| `john.doe@email.com` | 5 | 15491.00 |
| `jane.roe@email.com` | 1 | 4200.00 |

Plus 40 statements belonging to neither — that is what makes the per-user
scoping criteria meaningful. Rebuild with `python scripts/seed.py`.

## The SDD loop

What you should walk a challenger through, and follow yourself:

1. **Read** `spec.md` and `acceptance.md`.
2. **Clarify.** Ambiguity is a bug in the spec — say so, and suggest an issue.
3. **Plan** against the criteria, before writing code.
4. **Build.**
5. **Verify** with the harness. It reports per criterion.
6. **Iterate** on the red ones, quoting the criterion ID.

Criteria have stable IDs (`BE05-AC3`, `WEB05-AC4`). Use them. "Your balance is
wrong" is not useful; "BE05-AC3 expects 15491.00 because the fold treats a
Transfer to yourself as a credit" is.

## Conventions that are easy to get wrong

**Design.** The primary button is near-black (`#19191C`), not purple. Purple is
for brand surfaces — the auth panel, the active nav item, the table header.
Read [`specs/design/style-guide.md`](specs/design/style-guide.md) before writing
any UI, and import
[`specs/design/tokens.css`](specs/design/tokens.css) rather than hard-coding
hex values.

**Money semantics.** Credit is `#0CB97B`, debit is `#E02244` — and colour must
never be the only signal. Keep the `+`/`-` and the `↑`/`↓`.

**Test IDs.** Web and mobile specs declare a `testids` list. That is a
contract: the harness drives the UI through those, so an implementation that
omits them cannot be verified regardless of how good it is.

**Scoping.** A statement belongs to a user when their full name is `from_user`
or `to_user`. Balances and statement lists are per-user. Returning the global
ledger is the single most common mistake on the back-end track.

**Mobile storage.** Tokens go in Keychain / Keystore-backed storage. Never
`AsyncStorage`, `SharedPreferences`, `UserDefaults` or `localStorage`.

**Out-of-scope fields.** The mockups show Address, Countries, avatar upload,
Preferences/Security tabs, Transaction ID, Card, Receipt, Search and
Notifications. None are backed by the API. Render them, keep them
non-functional, and document them — see [`ROADMAP.md`](ROADMAP.md). Silently
dropping them is wrong; making them look like they save is worse.

## Security rules

- **Never commit a secret.** `app/.env` is git-ignored; `app/.env.example` is
  the template. A real `SECRET` in a diff is a blocking review comment.
- Never weaken a check to make a test pass. If a criterion looks wrong, say so.
- This is a teaching lab with deliberate simplifications — see
  [`SECURITY.md`](SECURITY.md). Do not present its code as production-ready,
  and do not "fix" the documented simplifications without discussion.

## Style

- Python: ruff, 100 columns, type hints where they clarify.
- Match the surrounding code. Comment density here is low and deliberate —
  comments explain *why*, never *what*.
- Conventional Commits.
- Prose in these docs is direct and plain. No exclamation marks, no
  "Great question!", no filler.
