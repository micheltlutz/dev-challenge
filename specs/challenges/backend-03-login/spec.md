---
id: backend-03-login
title: "Login route"
track: backend
order: 3
difficulty: intermediate
estimated_hours: 3
depends_on:
  - "backend-02-create-user"
endpoints:
  - "POST /auth/"
acceptance: acceptance.md
verify: "harness/suites/test_auth.py"
tags:
  - "auth"
  - "jwt"
---

# Login route

**Track:** backend · **Difficulty:** intermediate · **Estimated:** 3h  
**Prerequisites:** [`backend-02-create-user`](../backend-02-create-user/spec.md)

## Objective

Exchange credentials for a JWT. Everything after this challenge is protected by
the token you issue here.

## What you build

`POST /auth/`

### Request

```json
{ "userid": "john.doe@email.com", "password": "Challenge@123" }
```

### Response — 200 OK

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Response — 401 Unauthorized

```json
{ "detail": "Incorrect username or password" }
```

Return the **same** message for an unknown user and for a wrong password. A
different message for each tells an attacker which e-mails are registered.

## Token requirements

- Signed with **HS256** using a secret read from the environment — never
  hard-coded, never committed.
- Expires in **30 minutes**.
- Carries the user's identity in the `sub` claim.
- Sent by clients as `Authorization: Bearer <access_token>`.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 6 criteria (`BE03-AC1`…`BE03-AC6`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-03-login

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-03-login
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
