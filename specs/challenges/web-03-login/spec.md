---
id: web-03-login
title: "Login form"
track: web
order: 3
difficulty: intermediate
estimated_hours: 4
depends_on:
  - "web-02-create-account"
endpoints:
  - "POST /auth/"
figma_node: "1-655"
mockups:
  - "readme_files/images/login-web.png"
testids:
  - "login-form"
  - "login-email"
  - "login-password"
  - "login-submit"
  - "login-error"
  - "link-signup"
acceptance: acceptance.md
verify: "harness/ui/web/login.spec.ts"
tags:
  - "auth"
  - "forms"
  - "session"
---

# Login form

**Track:** web · **Difficulty:** intermediate · **Estimated:** 4h  
**Prerequisites:** [`web-02-create-account`](../web-02-create-account/spec.md)

## Objective

Build the login screen and establish a session. Everything after this challenge
depends on the token you store here.

## Design

[Open this screen in Figma](https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?node-id=1-655)

![Login Web](../../../readme_files/images/login-web.png)

Design system: [`../../design/style-guide.md`](../../design/style-guide.md) · tokens: [`../../design/tokens.json`](../../design/tokens.json)

## What you build

The **Log in** screen: same split layout as create-account, with the heading
"Log in" and the subtitle "Welcome to My Statement, please fill in the fields
below to log into your account."

Fields: **E-mail**, **Password** (with the lock icon). Primary button **Log
in**, then an `or` divider and an outlined **Create account** button.

### On submit

```http
POST /auth/
Content-Type: application/json

{ "userid": "<e-mail>", "password": "<password>" }
```

| Response | What to do |
|---|---|
| 200 | store the token, navigate to the dashboard |
| 401 | show `Incorrect username or password` near the form |

## Session handling

Store `access_token` and send it on every protected request as:

```
Authorization: Bearer <access_token>
```

`localStorage` is acceptable for this lab. Understand the trade-off: it is
readable by any script on the page, so a single XSS bug leaks the session. In
production you would prefer an httpOnly cookie. Write down your choice and your
reasoning in your README — that reasoning is part of the challenge.

The token expires after 30 minutes. Handle a 401 on any protected route by
clearing the session and returning the user to this screen.

## Test IDs

Expose these as `data-testid` (web) or the platform accessibility identifier (mobile). They are the contract that lets the harness verify your UI without dictating your framework.

```
login-form
login-email
login-password
login-submit
login-error
link-signup
```

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 7 criteria (`WEB03-AC1`…`WEB03-AC7`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge web-03-login

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge web-03-login
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
