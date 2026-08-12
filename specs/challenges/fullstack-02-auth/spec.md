---
id: fullstack-02-auth
title: "Authentication, end to end"
track: fullstack
order: 2
difficulty: intermediate
estimated_hours: 8
depends_on:
  - "fullstack-01-contact"
endpoints:
  - "POST /users/"
  - "POST /auth/"
figma_node: "1-655"
mockups:
  - "readme_files/images/create-account-web.png"
  - "readme_files/images/login-web.png"
testids:
  - "signup-form"
  - "signup-submit"
  - "login-form"
  - "login-email"
  - "login-password"
  - "login-submit"
  - "login-error"
  - "app-shell"
  - "logout"
acceptance: acceptance.md
verify: "harness/suites/test_auth.py"
tags:
  - "auth"
  - "jwt"
  - "contract-first"
  - "e2e"
---

# Authentication, end to end

**Track:** fullstack · **Difficulty:** intermediate · **Estimated:** 8h  
**Prerequisites:** [`fullstack-01-contact`](../fullstack-01-contact/spec.md)

## Objective

Own the whole authentication story: registration, password hashing, token
issuance, session storage, route guarding and logout.

## Design

[Open this screen in Figma](https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?node-id=1-655)

![Create Account Web](../../../readme_files/images/create-account-web.png)
![Login Web](../../../readme_files/images/login-web.png)

Design system: [`../../design/style-guide.md`](../../design/style-guide.md) · tokens: [`../../design/tokens.json`](../../design/tokens.json)

## What you build

| Half | From |
|---|---|
| API | [`backend-02-create-user`](../backend-02-create-user/spec.md) + [`backend-03-login`](../backend-03-login/spec.md) |
| UI | [`web-02-create-account`](../web-02-create-account/spec.md) + [`web-03-login`](../web-03-login/spec.md) + the guarded shell from [`web-04-dashboard`](../web-04-dashboard/spec.md) |

## The end-to-end flow

1. A visitor registers. The password is hashed with bcrypt, scrypt or argon2.
2. They log in. Your API issues an HS256 JWT carrying `sub`, expiring in 30
   minutes, signed with a secret from the environment.
3. The UI stores the token and sends it as `Authorization: Bearer <token>`.
4. Protected routes are unreachable without it.
5. Logout clears the session; an expired token returns the user to login.

## Requirements

- The signing secret comes from the environment. Never hard-coded, never
  committed — your repository must not contain a real secret.
- Registration and login errors are distinguishable to the user but never leak
  whether an e-mail is registered.
- Document your token-storage choice and its trade-off in your README.

## Test IDs

Expose these as `data-testid` (web) or the platform accessibility identifier (mobile). They are the contract that lets the harness verify your UI without dictating your framework.

```
signup-form
signup-submit
login-form
login-email
login-password
login-submit
login-error
app-shell
logout
```

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 6 criteria (`FS02-AC1`…`FS02-AC6`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge fullstack-02-auth

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge fullstack-02-auth
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
