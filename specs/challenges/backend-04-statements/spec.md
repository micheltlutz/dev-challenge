---
id: backend-04-statements
title: "Statement list with pagination"
track: backend
order: 4
difficulty: intermediate
estimated_hours: 4
depends_on:
  - "backend-03-login"
endpoints:
  - "GET /statements/"
acceptance: acceptance.md
verify: "harness/suites/test_statements.py"
tags:
  - "auth"
  - "pagination"
  - "scoping"
---

# Statement list with pagination

**Track:** backend · **Difficulty:** intermediate · **Estimated:** 4h  
**Prerequisites:** [`backend-03-login`](../backend-03-login/spec.md)

## Objective

Return the authenticated user's bank transactions, paginated. The important
word is *their* -- a user must never see anyone else's rows.

## What you build

`GET /statements/?skip=0&limit=10`

| Parameter | Type | Default | Rules |
|---|---|---|---|
| `skip` | integer | `0` | how many rows to skip; must be >= 0 |
| `limit` | integer | `10` | how many rows to return; 1..100 |

Authenticated. Send `Authorization: Bearer <access_token>`.

### Response — 200 OK

```json
[
  {
    "id": 1,
    "description": "Payment from Freela",
    "type": "Deposit",
    "created_at": "2023-09-21T18:46:45",
    "amount": "15000.00",
    "from_user": "John Doe",
    "to_user": "John Doe",
    "bank_name": "Adams LLC",
    "authentication": "8f9a...c21e"
  }
]
```

`type` is one of `Deposit`, `Withdrawal`, `Transfer`.

### Response — 401 Unauthorized

```json
{ "detail": "Not authenticated" }
```

### Response — 422 Unprocessable Entity

`limit` outside 1..100, or a negative `skip`.

## Scoping rule

A statement belongs to a user when their **full name** appears as either
`from_user` or `to_user`. Return only those rows.

Seeded fixture: `john.doe@email.com` has exactly 5 statements;
`jane.roe@email.com` has exactly 1. The database also holds 40 rows belonging to
neither — if those leak into either response, the scoping is wrong.

> **Heads-up:** older briefs documented `GET /statements/{limit}/{offset}` as
> path parameters. The real contract is query parameters named `skip` and
> `limit`.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 7 criteria (`BE04-AC1`…`BE04-AC7`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-04-statements

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-04-statements
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
