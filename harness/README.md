# Verification harness

Checks a solution against the acceptance criteria in
[`../specs/`](../specs/README.md) and reports **per criterion**, not per stack
trace.

```
  Balance (amount)  (backend-05-balance)
  --------------------------------------------------------------------
  PASS  BE05-AC1  Unauthenticated request is rejected
  PASS  BE05-AC2  Balance is returned as a number
  FAIL  BE05-AC3  Seeded balance is exact
        └─ john.doe@email.com should have a balance of 15491.00, got 13512.59.
  SKIP  BE05-AC5  Deposit increases the balance
        └─ Cannot create statements (POST /statement/ returned 404).

  2/7 criteria passed   (1 failed, 4 skipped, 0 uncovered)
```

It is **black-box**: it speaks HTTP to whatever you point it at and knows
nothing about your language, framework or database.

## API and fullstack tracks

### Docker (nothing to install)

**Linux** — `--network host` lets the container see your `localhost`:

```bash
docker run --rm --network host \
  ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:3000 \
  --challenge backend-05-balance
```

**macOS and Windows** — `--network host` does not bridge to the host there.
Use `host.docker.internal` instead:

```bash
docker run --rm \
  ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:3000 \
  --challenge backend-05-balance
```

If you see *"Cannot reach ... Connection refused"* from inside the container,
this is almost always why.

Published for `linux/amd64` and `linux/arm64` by
[`.github/workflows/publish-images.yml`](../.github/workflows/publish-images.yml)
on every release, alongside `ghcr.io/micheltlutz/dev-challenge` (the reference
API). Tags: `latest`, `2`, `2.0`, `2.0.0`.

To build it yourself, do so from the repository root — not from `harness/`,
because the image needs `specs/` too:

```bash
docker build -f harness/Dockerfile -t dev-challenge-harness .
```

### Python

```bash
pip install -r requirements_for_dev.txt
python harness/cli.py --base-url http://localhost:3000 --challenge backend-05-balance
```

Or drive pytest directly, which is all the CLI does:

```bash
pytest harness/ --base-url http://localhost:3000
```

### Options

| Flag | Meaning |
|---|---|
| `--base-url` | The API under test. Default `http://localhost:8000`. |
| `--challenge` | Run one challenge's criteria. Omit to run everything. |
| `--list` | List every challenge and its criterion count. |
| `--report-json PATH` | Machine-readable scorecard. |
| `--report-markdown PATH` | Scorecard you can paste into a PR. |
| `-v` | Full pytest output instead of the summary. |

`BASE_URL` and `CHALLENGE` work as environment variables too.

## Web track

Playwright, driven by the `testids` each spec declares. Expose those as
`data-testid` and the harness can drive your UI whatever you built it with.

```bash
cd harness/ui/web
npm install
npm run install-browsers

BASE_URL=http://localhost:5173 \
DC_API_URL=http://localhost:8000 \
npx playwright test statement.spec.ts
```

| Variable | Meaning |
|---|---|
| `BASE_URL` | Your front-end. Default `http://localhost:3000`. |
| `DC_API_URL` | The API it talks to, for cross-checking. |
| `DC_USERID` / `DC_PASSWORD` | Login used by the `loggedIn` fixture. Defaults to the seeded `john.doe@email.com` / `Challenge@123`. |

The suite assumes conventional routes — `/contact`, `/login`, `/signup`, `/home`,
`/statement`, `/profile`. If yours differ, adjust `playwright.config.ts` or the
`goto` calls; that is expected, not cheating.

## Mobile track

**Not automatically verified.** Native UI cannot be checked the way an HTTP API
or a browser page can, and pretending otherwise would be worse than saying so.
The criteria in each mobile `acceptance.md` are a self-review checklist.

[Maestro](https://maestro.mobile.dev/) flows cover part of it:

```bash
maestro test harness/ui/mobile/login.yaml -e APP_ID=com.example.mystatement
```

## The harness writes to the database it tests

It registers users and appends statements — that is how a black-box verifier
checks behaviour it cannot see. Two consequences:

- **Do not point it at anything you care about.** It is for your own dev
  instance.
- **Running it against this repo's reference API mutates `dev-challenge.db`.**
  Reseed afterwards, or CI will tell you the committed fixture is stale:

  ```bash
  python scripts/seed.py
  ```

## What "skipped" means

A skip is never a pass. It means the harness could not reach the behaviour —
almost always because a prerequisite is missing:

| Skip | What to do |
|---|---|
| "Could not register a user" | Implement `backend-02-create-user`. |
| "Could not authenticate" | Implement `backend-03-login`. |
| "Reference seed data not present" | Seed two users matching the fixture — see the spec. |
| "Cannot create statements" | Implement `POST /statement/` so balance arithmetic can be exercised. |

## The fixture

Criteria that quote exact numbers rely on the reference seed. Both users have
the password `Challenge@123`:

| User | Statements | Balance |
|---|---|---|
| `john.doe@email.com` | 5 | 15491.00 |
| `jane.roe@email.com` | 1 | 4200.00 |

Plus 40 statements belonging to neither, which is how the scoping criteria have
teeth. Rebuild with `python scripts/seed.py`.

## How a test is tied to a criterion

```python
@pytest.mark.ac("BE05-AC3")
def test_seeded_balance_is_exact(seeded, balance_of):
    ...
```

```ts
test(ac('WEB05-AC4', 'Hide-values masks every figure'), async ({ loggedIn: page }) => {
```

`scripts/validate_specs.py` reads these marks and fails CI if any criterion has
no test — so "uncovered" always means someone forgot, never that it could not be
done. Criteria that genuinely cannot be automated say so with a
**Manual review** note in their `acceptance.md`.

A test may carry several marks: the fullstack track reuses the backend and web
criteria by design.

## Contributing a test

1. Add or edit the criterion in `specs/challenges/<id>/acceptance.md`.
2. Write the test, marked with the criterion's ID.
3. `python scripts/validate_specs.py`
4. `pytest harness/ --base-url http://localhost:8000` against the reference API.

Both halves land in the same pull request — see
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).
