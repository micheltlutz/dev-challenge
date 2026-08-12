# Instructions for contributors

How to run the reference API locally and work on the project itself. If you
came here to *do* the challenges, you want
[the challenger guide](challenged.md) instead.

## Requirements

- Python 3.11+
- Docker (optional, for the container path)

## Create the environment

```bash
python -m venv venv
```

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```powershell
.\venv\Scripts\activate.bat
# or
.\venv\Scripts\activate.ps1
```

## Install dependencies

Contributors need the dev extras (pytest, coverage, ruff):

```bash
pip install -r requirements_for_dev.txt
```

## Configure

Every setting has a working default, so this step is optional:

```bash
cp app/.env.example app/.env
```

`app/.env` is git-ignored. **Never commit a real `SECRET`.** Generate your own
with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Seed the database

`dev-challenge.db` ships with the repo, but you can rebuild it deterministically
at any time:

```bash
python scripts/seed.py
```

This creates two demo users, both with the password `Challenge@123`:

| User | Statements | Balance |
|---|---|---|
| `john.doe@email.com` | 5 | 15491.00 |
| `jane.roe@email.com` | 1 | 4200.00 |

## Run the server

```bash
uvicorn app.main:app --reload
```

Then open <http://localhost:8000/docs>.

## Run the checks

Everything CI runs, in order:

```bash
ruff check app scripts tests harness    # lint
pytest --cov=app                        # unit tests
python scripts/export_openapi.py --check   # contract matches the code
python scripts/build_tokens.py --check     # tokens.css matches tokens.json
python scripts/validate_specs.py           # spec layer integrity
pip-audit                                  # dependency advisories
```

Note that running the harness against your local reference API **writes** to
`dev-challenge.db` — it registers users by design. Run `python scripts/seed.py`
afterwards, or CI will report the committed fixture as stale.

## About the dependency pins

`requirements.txt` uses floors (`>=`), not compatible-release pins (`~=`). That
is deliberate: `PyJWT~=2.8.0` looks careful but blocks every patch outside
2.8.x, which is how the project ended up shipping a PyJWT with five open
advisories. Cap only where a major version is known to break us.

Keep the list minimal, too. `fastapi[all]` used to pull in `ujson`, `orjson`,
`jinja2` and more that nothing here imports.

## Deactivate the environment

```bash
deactivate
```

## Before opening a PR

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the branch naming, commit
convention, and review checklist.
