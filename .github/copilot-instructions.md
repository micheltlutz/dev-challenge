# GitHub Copilot instructions

Mirror of [`AGENTS.md`](../AGENTS.md). Read that file for the full picture; this
is the short version Copilot loads automatically.

## Which job are you doing?

**Helping someone do a challenge** — they are learning. Default to mentoring:
plan with them, review their code, explain which acceptance criterion fails and
why. Do not write the implementation unless they ask. If they ask, do it
properly and without fuss. Scaffolding, config and boilerplate are always fine
to write outright.

**Improving the lab itself** — normal engineering work. See
[`CONTRIBUTING.md`](../CONTRIBUTING.md).

## The spec layer is the source of truth

`specs/` — not the code, not `readme_files/` (those are redirect stubs).

Before answering what a challenge requires, read
`specs/challenges/<id>/spec.md` and its `acceptance.md`. The old briefs
disagreed with the running API for a long time; this layer exists so that
cannot recur, and CI enforces it.

If you change API behaviour, update the spec and the harness test in the same
commit.

## Layout

- `app/` — reference FastAPI API
- `specs/` — challenges, acceptance criteria, OpenAPI contract, design tokens
- `harness/` — black-box verifier, reports per acceptance criterion
- `scripts/` — `seed.py`, `export_openapi.py`, `build_tokens.py`, `validate_specs.py`

## Commands

```bash
ruff check app scripts tests harness
pytest --cov=app
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py
python harness/cli.py --base-url http://localhost:3000 --challenge backend-05-balance
```

## Fixture

`john.doe@email.com` (5 statements, balance 15491.00) and `jane.roe@email.com`
(1 statement, balance 4200.00). Password `Challenge@123` for both. Plus 40 rows
belonging to neither, which is what makes the scoping criteria bite.

## Easy things to get wrong

- Primary buttons are near-black `#19191C`, not purple. Purple is brand
  surfaces only. Import `specs/design/tokens.css`; do not hard-code hex.
- Credit `#0CB97B`, debit `#E02244`, and colour is never the only signal —
  keep the sign and the arrow.
- Web and mobile specs declare `testids`. The harness drives the UI through
  them; omitting them makes the work unverifiable.
- Balances and statement lists are **per user**. A statement is yours when your
  full name is `from_user` or `to_user`. Returning the global ledger is the
  commonest back-end mistake.
- Mobile tokens go in Keychain/Keystore, never `AsyncStorage` or
  `UserDefaults`.
- Never commit a secret. `app/.env` is git-ignored; use `app/.env.example`.

## Style

Ruff, 100 columns, Conventional Commits. Comments explain *why*, not *what*.
