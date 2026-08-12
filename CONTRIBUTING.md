# Contributing

Thanks for helping out. This project is a volunteer-run learning lab, so the
bar is "clear and correct", not "enterprise grade".

There are two very different ways to participate — pick the one that matches
what you want to do.

## I want to *do* the challenges

You do not contribute here. Work in **your own repository** and verify your
solution with the portable harness:

```bash
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:3000 --challenge backend-05
```

Start at [the challenger guide](readme_files/challenged.md). When you are done,
open a [Submit your solution](https://github.com/micheltlutz/dev-challenge/issues/new/choose)
issue and we will link it from `SOLUTIONS.md`.

## I want to improve the project

That is what the rest of this file covers.

### Good first contributions

- A new challenge (see the `spec-authoring` skill in `.claude/skills/`).
- Harness coverage for an acceptance criterion that has none.
- Fixing drift between a spec and the reference API.
- Translations, typo fixes, clearer wording.

### Setup

Follow [readme_files/contributors.md](readme_files/contributors.md).

### Branches

`<type>/<short-description>`, e.g. `fix/statement-pagination`,
`feat/fullstack-track`, `docs/spec-layer`.

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

### Commits

[Conventional Commits](https://www.conventionalcommits.org/):

```
feat(specs): add fullstack track
fix(balance): scope statements to the authenticated user
docs(readme): document the harness quickstart
```

Reference an issue when there is one (`Closes #42`).

### The spec layer is the source of truth

This is the one rule that is easy to get wrong.

`specs/` — not the code, and not the markdown briefs — defines what a challenge
requires. If you change API behaviour, you must update the spec **and** the
harness test in the same PR. CI enforces this:

- `specs/openapi.json` is regenerated and diffed against the code.
- Every `endpoints:` entry in a spec must exist in the OpenAPI document.
- Every acceptance-criterion ID must have a harness test with a matching mark.

### Before you open a PR

```bash
ruff check app scripts tests harness
pytest --cov=app
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py
pip-audit
pytest harness/ --base-url http://localhost:8000
```

### Review checklist

- [ ] Specs, code, and harness agree.
- [ ] New behaviour has an acceptance criterion and a test for it.
- [ ] No secrets, no `.env`, no personal data in fixtures.
- [ ] `pip-audit` is clean.
- [ ] Docs updated if the challenger-facing flow changed.
- [ ] Commits follow Conventional Commits.

### Dependencies

Use floors (`>=`), not `~=`. A compatible-release pin blocks security patches
outside the pinned minor, which is exactly how this project shipped a PyJWT
with five open advisories. Cap only where a major version is known to break us,
and keep the runtime list minimal — every extra package is attack surface for a
project that imports eight things.

Dependabot is configured in [`.github/dependabot.yml`](.github/dependabot.yml)
and `.github/workflows/audit.yml` runs `pip-audit` on every push and weekly.

### Reporting bugs and asking for features

Open an issue using the templates. For anything security-sensitive, follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## Code of Conduct

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
