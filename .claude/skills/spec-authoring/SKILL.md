---
name: spec-authoring
description: Add or change a challenge in the dev-challenge spec layer — frontmatter, acceptance criteria with stable IDs, the matching harness test, and the validation that keeps them in sync. Use when someone wants to add a new challenge or track, edit an existing spec or acceptance criterion, change API behaviour that a spec describes, or asks why validate_specs.py or the spec-drift workflow is failing.
---

# Authoring a spec

For contributors extending the lab. The rule that governs everything here: **a
spec change and its harness test land in the same pull request**, or CI rejects
it.

## Anatomy

```
specs/challenges/<track>-<nn>-<slug>/
  spec.md          frontmatter + objective + contract + requirements
  acceptance.md    criteria, each with a stable ID
```

The directory name, the `id:` in the frontmatter, and the criterion prefix all
have to agree.

## Frontmatter

Validated against
[`specs/schema/challenge.schema.json`](../../../specs/schema/challenge.schema.json).

```yaml
---
id: backend-05-balance          # must equal the directory name
title: "Balance (amount)"
track: backend                  # backend | web | mobile | fullstack
order: 5                        # unique within the track
difficulty: intermediate        # starter | intermediate | advanced
estimated_hours: 3
depends_on: ["backend-04-statements"]   # must exist, must stay acyclic
endpoints: ["GET /balance/"]            # must exist in specs/openapi.json
acceptance: acceptance.md
verify: "harness/suites/test_balance.py"
tags: ["auth", "business-rules"]
---
```

Web and mobile additionally require:

```yaml
figma_node: "13-5855"           # or null
mockups: ["readme_files/images/statement-web.png"]
testids: ["balance-amount", "balance-toggle"]   # non-empty
```

`testids` is the contract that makes a UI verifiable without dictating a
framework. Choose names that describe the *role*, not the implementation:
`balance-toggle`, not `eye-icon-button`.

Set `verifiable: false` and `verify: null` when no automated runner can check
the challenge — the whole mobile track is in that position, and saying so
plainly is better than implying coverage that does not exist.

## Writing criteria

```markdown
### BE05-AC3 — Seeded balance is exact

Given John Doe's token
When GET /balance/
Then `amount` equals 15491.00 within 0.01
```

- **IDs are stable and globally unique.** `<PREFIX><nn>-AC<n>`: `BE` back-end,
  `WEB` web, `MOB` mobile, `FS` fullstack. Never renumber an existing criterion
  — append.
- **One observable behaviour per criterion.** If you need "and" in the Then,
  you probably have two.
- **Testable from outside.** The harness is black-box. "The code is well
  structured" is not a criterion; "the response contains no password field" is.
- **Say the number.** `15491.00`, not "the correct balance".

For a criterion no runner can check, add a manual marker — this is what keeps
"uncovered" meaning "we forgot" rather than "we couldn't":

```markdown
> **Manual review.** Why no automated check is possible.
```

## The harness test

Mark it with the criterion ID:

```python
@pytest.mark.ac("BE05-AC3")
def test_seeded_balance_is_exact(seeded, balance_of):
    spec, header = seeded("john")
    amount = balance_of(header)
    assert abs(amount - spec["balance"]) < 0.01, (
        f"expected {spec['balance']:.2f}, got {amount:.2f}.\n"
        "Check the fold: Deposit adds, Withdrawal subtracts, Transfer to self "
        "adds, Transfer to another subtracts -- over this user's rows only."
    )
```

```ts
test(ac('WEB05-AC4', 'Hide-values masks every figure'), async ({ loggedIn: page }) => {
```

A test may carry several `ac` marks — the fullstack track reuses the backend
and web criteria by design.

**Failure messages are documentation.** A challenger reads them at their most
stuck. Say what was expected, what happened, and where to look. Never just
`assert x == y`.

Available fixtures are in [`harness/conftest.py`](../../../harness/conftest.py):
`api`, `base_url`, `new_user`, `token_for`, `authed_user`, `seeded`,
`add_statement`, `balance_of`.

Prefer fixtures that build their own data — those work against any
implementation. Use `seeded` only when the criterion genuinely quotes fixture
numbers; it skips cleanly when the seed is absent.

## Changing API behaviour

1. Change `app/`.
2. `python scripts/export_openapi.py` — regenerate the contract.
3. Update every affected `spec.md` and `acceptance.md`.
4. Update the harness tests.
5. Update `scripts/seed.py` if the fixture numbers move, and regenerate
   `dev-challenge.db`.
6. Run the checks below.

Skipping step 3 is exactly the drift this layer was built to prevent, and CI
will catch it.

## Validate

```bash
python scripts/export_openapi.py --check
python scripts/build_tokens.py --check
python scripts/validate_specs.py
pytest harness/ --base-url http://localhost:8000    # against the reference API
```

`validate_specs.py` checks frontmatter, id/directory agreement, endpoints
against the contract, mockup paths, the `depends_on` DAG, globally unique
criterion IDs, harness coverage, and every relative link.

## Common failures

| Error | Cause |
|---|---|
| `endpoint 'X' is not in specs/openapi.json` | you renamed a route without regenerating, or typoed it |
| `N criteria have no harness test` | you added a criterion without its test, or the mark's ID is misspelt |
| `criterion id X is already used by Y` | IDs are globally unique |
| `specs/openapi.json is out of date` | run `python scripts/export_openapi.py` |
| `dev-challenge.db is stale` | run `python scripts/seed.py` |
| `broken link 'X'` | a relative path in a doc does not exist |

## Adding a whole track

Pick a prefix nobody uses, add every challenge under it in one PR, and give
`depends_on` edges to the existing tracks where a prerequisite genuinely
exists. Update the index tables in
[`specs/README.md`](../../../specs/README.md) and the entry points in
[`readme_files/challenged.md`](../../../readme_files/challenged.md).
