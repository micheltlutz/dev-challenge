---
id: backend-06-profile-edit
title: "Edit profile route"
track: backend
order: 6
difficulty: advanced
estimated_hours: 3
depends_on:
  - "backend-03-login"
endpoints:
  - "GET /users/me"
  - "PUT /users/{user_id}"
acceptance: acceptance.md
verify: "harness/suites/test_profile.py"
tags:
  - "auth"
  - "authorization"
  - "partial-update"
---

# Edit profile route

**Track:** backend · **Difficulty:** advanced · **Estimated:** 3h  
**Prerequisites:** [`backend-03-login`](../backend-03-login/spec.md)

## Objective

Let a user update their own profile -- and only their own. This challenge is
about authorization, not just authentication: a valid token is not permission to
edit somebody else.

## What you build

`GET /users/me` — authenticated. Returns the caller's own profile.

```json
{
  "id": 3,
  "userid": "ada@example.com",
  "fullname": "Ada Lovelace",
  "birthdate": "1815-12-10"
}
```

This route exists because the next one needs it: the JWT carries the user's
**e-mail** in `sub`, not their numeric id, so without `/users/me` a client has
no way to discover the `{user_id}` it is supposed to `PUT` to. Returning 401
when unauthenticated.

`PUT /users/{user_id}` — authenticated.

### Request (all fields optional)

```json
{
  "fullname": "Ada L. Byron",
  "birthdate": "1815-12-10",
  "password": "NewPassword@456"
}
```

Only the fields present are applied. Omitted fields keep their current value.

### Response — 200 OK

```json
{
  "id": 3,
  "userid": "ada@example.com",
  "fullname": "Ada L. Byron",
  "birthdate": "1815-12-10"
}
```

The response must **never** include the password or its hash.

### Errors

| Status | When |
|---|---|
| 401 | no or invalid token — `{"detail": "Not authenticated"}` |
| 403 | the token belongs to a different user — `{"detail": "You can only edit your own profile"}` |
| 404 | `user_id` does not exist |
| 422 | malformed `birthdate` |

## Requirements

- A new password must be re-hashed, and the old one must stop working.
- `userid` is not editable through this route.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 7 criteria (`BE06-AC1`…`BE06-AC7`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-06-profile-edit

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-06-profile-edit
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
