---
id: backend-05-balance
title: "Balance (amount)"
track: backend
order: 5
difficulty: intermediate
estimated_hours: 3
depends_on:
  - "backend-04-statements"
endpoints:
  - "GET /balance/"
acceptance: acceptance.md
verify: "harness/suites/test_balance.py"
tags:
  - "auth"
  - "business-rules"
  - "scoping"
---

# Balance (amount)

**Track:** backend · **Difficulty:** intermediate · **Estimated:** 3h  
**Prerequisites:** [`backend-04-statements`](../backend-04-statements/spec.md)

## Objective

Compute the authenticated user's balance from their statements. This is the
first challenge with real business logic -- the rules below are the whole point.

## What you build

`GET /balance/` — authenticated.

### Response — 200 OK

```json
{ "amount": 15491.00 }
```

### Response — 401 Unauthorized

```json
{ "detail": "Not authenticated" }
```

## Business rules

Fold over **the caller's own statements only** (same scoping rule as
`backend-04-statements`):

| Type | Condition | Effect |
|---|---|---|
| `Deposit` | any | **add** the amount |
| `Withdrawal` | any | **subtract** the amount |
| `Transfer` | `to_user == from_user` | **add** the amount |
| `Transfer` | `to_user != from_user` | **subtract** the amount |

> Earlier versions of this brief listed two separate Deposit rules with
> identical outcomes. They have been consolidated into the single row above.

## Worked example

The seeded ledger for `john.doe@email.com`:

| Type | Amount | from → to | Effect |
|---|---|---|---|
| Deposit | 15000.00 | John Doe → John Doe | +15000.00 |
| Withdrawal | 250.00 | John Doe → John Doe | −250.00 |
| Transfer | 1200.50 | John Doe → John Doe | +1200.50 |
| Transfer | 800.25 | John Doe → Marie Curie | −800.25 |
| Deposit | 340.75 | Grace Hopper → John Doe | +340.75 |
| | | **Total** | **15491.00** |

`jane.roe@email.com` has a single 4200.00 deposit, so her balance is
**4200.00**. If both users see the same number, your scoping is wrong.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 7 criteria (`BE05-AC1`…`BE05-AC7`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-05-balance

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-05-balance
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
