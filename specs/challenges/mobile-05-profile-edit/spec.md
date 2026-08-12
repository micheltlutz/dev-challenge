---
id: mobile-05-profile-edit
title: "Edit profile"
track: mobile
order: 5
difficulty: advanced
estimated_hours: 4
depends_on:
  - "mobile-03-dashboard"
endpoints:
  - "GET /users/me"
  - "PUT /users/{user_id}"
figma_node: "19-4040"
mockups:
  - "readme_files/images/profile-mobile.png"
testids:
  - "profile-tabs"
  - "profile-form"
  - "profile-avatar"
  - "profile-firstname"
  - "profile-lastname"
  - "profile-email"
  - "profile-birthdate"
  - "profile-save"
  - "profile-success"
  - "profile-error"
acceptance: acceptance.md
verify: null
verifiable: false
tags:
  - "forms"
  - "partial-update"
  - "scope-boundaries"
---

# Edit profile

**Track:** mobile · **Difficulty:** advanced · **Estimated:** 4h  
**Prerequisites:** [`mobile-03-dashboard`](../mobile-03-dashboard/spec.md)

## Objective

Build the mobile profile screen and persist changes. As on web, several fields
in the mockup are not backed by the API — how you handle that is the challenge.

## Design

[Open this screen in Figma](https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?node-id=19-4040)

![Profile Mobile](../../../readme_files/images/profile-mobile.png)

Design system: [`../../design/style-guide.md`](../../design/style-guide.md) · tokens: [`../../design/tokens.json`](../../design/tokens.json)

## What you build

The **Edit Profile** screen from the mobile design: the three tabs (Edit
Profile, Preferences, Security) with the first active, a centred avatar with the
pencil badge, then stacked fields and a full-width **Save**.

### Finding your own user id

`PUT /users/{user_id}` needs a numeric id, and the token only carries your
e-mail. Fetch it first:

```http
GET /users/me
Authorization: Bearer <access_token>
```

```json
{ "id": 3, "userid": "ada@example.com", "fullname": "Ada Lovelace", "birthdate": "1815-12-10" }
```

Use the same response to prefill the form.

### Backed by the API

| Field | Notes |
|---|---|
| Last Name / First name | joined into `fullname` on save |
| Date of birth | native picker, sent as ISO `YYYY-MM-DD` |
| E-mail | **read-only** |

### Not backed by the API

Address · Countries · avatar upload · the Preferences and Security tabs. Render
them, keep them non-functional, and list them under "Known limitations" in your
README.

### On save

```http
PUT /users/{user_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{ "fullname": "First Last", "birthdate": "YYYY-MM-DD" }
```

## Requirements

- Prefill from the current profile.
- Disable **Save** until something changes.
- Keyboard avoidance, as in `mobile-01-create-account`.
- A 401 clears secure storage and returns to login.

## Test IDs

Expose these as `data-testid` (web) or the platform accessibility identifier (mobile). They are the contract that lets the harness verify your UI without dictating your framework.

```
profile-tabs
profile-form
profile-avatar
profile-firstname
profile-lastname
profile-email
profile-birthdate
profile-save
profile-success
profile-error
```

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 7 criteria (`MOB05-AC1`…`MOB05-AC7`).

## Verifying your work

⚠️ **This challenge is not automatically verified.** Native mobile UI cannot be checked the way an HTTP API or a browser page can, so the criteria in `acceptance.md` are a self-review checklist. Optional [Maestro](https://maestro.mobile.dev/) flows live in `harness/ui/mobile/` if you want to automate part of it.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
