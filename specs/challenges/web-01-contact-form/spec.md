---
id: web-01-contact-form
title: "Contact form"
track: web
order: 1
difficulty: starter
estimated_hours: 3
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
verify: "harness/ui/web/contact.spec.ts"
tags:
  - "forms"
  - "validation"
  - "free-design"
---

# Contact form

**Track:** web · **Difficulty:** starter · **Estimated:** 3h  
**Prerequisites:** none — you can start here.

## Objective

Build a contact form in the framework of your choice and wire it to the API.
There is **no Figma for this one on purpose** -- design it yourself. It is the
warm-up that gets your project, routing, form state and error handling in place.

## What you build

A single page with a form that posts to `POST /contact/`.

Fields: **Name**, **E-mail**, **Interest**, **Message** — all required.

### On submit

```http
POST /contact/
Content-Type: application/json

{ "name": "...", "email": "...", "message": "...", "interest": "..." }
```

- **200** — show the returned `msg` as a success state and clear the form.
- **422** — show which fields are invalid.
- **network error** — show a retryable error state.

## Requirements

- Validate before sending: no empty fields, and a plausible e-mail.
- Disable the submit button while the request is in flight so a double-click
  cannot send twice.
- The form must be usable with the keyboard alone, and every input must have a
  real `<label>`.

Design is yours, but read [`../../design/style-guide.md`](../../design/style-guide.md)
first — matching the lab's look makes the later challenges feel continuous.

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

See [`acceptance.md`](acceptance.md) — 7 criteria (`WEB01-AC1`…`WEB01-AC7`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge web-01-contact-form

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge web-01-contact-form
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
