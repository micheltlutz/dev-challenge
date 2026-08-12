---
id: backend-01-contact
title: "Contact route"
track: backend
order: 1
difficulty: starter
estimated_hours: 1.5
depends_on: []
endpoints:
  - "POST /contact/"
acceptance: acceptance.md
verify: "harness/suites/test_contact.py"
tags:
  - "public"
  - "validation"
---

# Contact route

**Track:** backend · **Difficulty:** starter · **Estimated:** 1.5h  
**Prerequisites:** none — you can start here.

## Objective

Build a public endpoint that accepts a contact submission and answers with a
thank-you message. No database, no authentication -- this is the warm-up that
gets your project skeleton, routing, validation and error handling in place.

## What you build

`POST /contact/`

### Request

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "message": "I would like to know more about the project.",
  "interest": "Back-end"
}
```

All four fields are required. `email` must be a valid e-mail address.

### Response — 200 OK

```json
{
  "msg": "Thank Ada Lovelace, for getting in touch and sharing your interests,\n    look forward to hearing from you soon."
}
```

The exact wording is yours; the harness only checks that the response is a JSON
object with a `msg` key whose value contains the submitted `name`.

### Response — 422 Unprocessable Entity

Returned when a field is missing or `email` is not a valid address. The body
shape is up to your framework.

> **Heads-up:** earlier versions of this challenge documented `POST
> /create_contact` with a field called `nome`. That was wrong and never matched
> the reference API. The contract above is authoritative.

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 4 criteria (`BE01-AC1`…`BE01-AC4`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge backend-01-contact

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge backend-01-contact
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
