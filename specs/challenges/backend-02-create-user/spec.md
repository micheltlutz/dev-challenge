---
id: backend-02-create-user
title: "Create user route"
track: backend
order: 2
difficulty: starter
estimated_hours: 3
depends_on:
  - "backend-01-contact"
endpoints:
  - "POST /users/"
acceptance: acceptance.md
verify: "harness/suites/test_users.py"
tags:
  - "persistence"
  - "hashing"
  - "validation"
---

# Create user route

**Track:** backend · **Difficulty:** starter · **Estimated:** 3h  
**Prerequisites:** [`backend-01-contact`](../backend-01-contact/spec.md)

## Objective

Persist users. This is where the database, the model layer and password hashing
enter the project. Passwords must never be stored or returned in clear text.

## What you build

`POST /users/`

### Request

```json
{
  "userid": "ada@example.com",
  "password": "Challenge@123",
  "fullname": "Ada Lovelace",
  "birthdate": "1815-12-10"
}
```

`userid` is the user's e-mail and is unique. `birthdate` is ISO `YYYY-MM-DD`.

### Response — 201 Created

```json
{ "msg": "success" }
```

### Response — 400 Bad Request

```json
{ "detail": "Username already registered" }
```

### Response — 422 Unprocessable Entity

Invalid e-mail, malformed date, or a missing field.

## Requirements

- Persist to a real database. The reference uses SQLite; use whatever suits
  your stack.
- **Hash the password** with a modern adaptive algorithm (bcrypt, scrypt or
  argon2). A plain or merely-encoded password fails this challenge.
- The stored hash must never appear in any API response.

> **Heads-up:** older briefs documented `POST /create_user` returning
> `{"msg": "User created successfully"}`. The contract above is authoritative.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 6 criteria (`BE02-AC1`…`BE02-AC6`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-02-create-user

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-02-create-user
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
