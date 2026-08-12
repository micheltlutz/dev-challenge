---
id: fullstack-01-contact
title: "Contact, end to end"
track: fullstack
order: 1
difficulty: starter
estimated_hours: 5
depends_on: []
endpoints:
  - "POST /contact/"
figma_node: null
mockups: []
testids:
  - "contact-form"
  - "contact-name"
  - "contact-email"
  - "contact-interest"
  - "contact-message"
  - "contact-submit"
  - "contact-success"
  - "contact-error"
acceptance: acceptance.md
verify: "harness/suites/test_contact.py"
tags:
  - "contract-first"
  - "e2e"
---

# Contact, end to end

**Track:** fullstack · **Difficulty:** starter · **Estimated:** 5h  
**Prerequisites:** none — you can start here.

## Objective

Build **both** ends of the contact feature and prove they agree. You own the
contract now: your API and your UI must satisfy the same acceptance criteria the
separate tracks satisfy individually.

## What you build

1. The API from [`backend-01-contact`](../backend-01-contact/spec.md).
2. The UI from [`web-01-contact-form`](../web-01-contact-form/spec.md), talking
   to **your** API rather than the reference one.

## Why this track exists

On the single-discipline tracks one side of the contract is given to you. Here
nothing is, which is where spec-driven development starts to pay: the
acceptance criteria are the only fixed point, and both halves are written to
satisfy them.

## Requirements

- Your API must pass the `BE01-*` criteria; your UI must pass the `WEB01-*`
  criteria against your API.
- Both halves run together with a single command — `docker compose up` or an
  equivalent documented in your README.
- CORS must be configured so the browser can actually reach your API. Getting
  this wrong is the classic first-day fullstack bug; do not disable it blindly,
  understand what you are allowing.
- Your README documents how to run the stack and how to point the harness at it.

## Verifying

```bash
# your API
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge fullstack-01-contact
```

## Test IDs

Expose these as `data-testid` (web) or the platform accessibility identifier (mobile). They are the contract that lets the harness verify your UI without dictating your framework.

```
contact-form
contact-name
contact-email
contact-interest
contact-message
contact-submit
contact-success
contact-error
```

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 4 criteria (`FS01-AC1`…`FS01-AC4`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge fullstack-01-contact

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge fullstack-01-contact
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
