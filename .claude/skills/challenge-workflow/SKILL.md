---
name: challenge-workflow
description: Run the spec-driven loop for a dev-challenge exercise — read the spec and its acceptance criteria, clarify ambiguity, plan, build, verify with the harness, iterate on failing criteria. Use whenever someone is working through a challenge from specs/challenges/, mentions a challenge id like backend-05-balance or web-03-login, asks "how do I start this challenge", or asks why a criterion is failing.
---

# Challenge workflow

The spec-driven loop this lab is built around. Follow it yourself, and walk the
learner through it.

## Before anything: posture

Read "First: which job are you doing?" in [`AGENTS.md`](../../../AGENTS.md).

**Default to mentoring.** The person is here to learn; the code is the medium,
not the deliverable. Plan with them, review what they write, name the failing
criterion and explain why — but do not hand over the implementation unless they
ask for it.

They can switch you off this at any time: "just write it", "show me a
solution", `--solve`. When they do, switch cleanly, say you have switched, and
do a proper job. Withholding while pretending you cannot help is worse than
useless.

Scaffolding, config, build setup and boilerplate are always fine to write
outright. Nobody learns from a `tsconfig.json`. Save the mentoring for the
logic the challenge is actually about.

## 1. Read the spec

```bash
cat specs/challenges/<id>/spec.md
cat specs/challenges/<id>/acceptance.md
```

Never answer from `readme_files/` — those are redirect stubs — or from how such
an API usually works. The briefs disagreed with the running API for a long time;
that is why this layer exists.

If it is a web or mobile challenge, also read:

- [`specs/design/style-guide.md`](../../../specs/design/style-guide.md)
- [`specs/design/tokens.css`](../../../specs/design/tokens.css) — import it, do not hard-code hex
- the `mockups:` listed in the frontmatter

Note the `testids:` list. It is a contract: the harness drives the UI through
those values, so an implementation that omits them cannot be verified no matter
how good it looks.

## 2. Clarify

Ambiguity in a spec is a bug in the spec, not something to guess past. Surface
it, state the assumption you would make, and suggest opening an issue. Fixing a
spec is a real contribution and the specs say so.

## 3. Plan

Turn the acceptance criteria into a checklist before writing code. Order it so
that the criteria a failure would cascade from come first — usually
authentication, then scoping, then the feature.

Check `depends_on` in the frontmatter. Starting `web-05-statement` before
`web-04-dashboard` exists means building a screen with nowhere to live.

## 4. Build

Only in solver mode, or for the scaffolding carve-out above.

## 5. Verify

```bash
python harness/cli.py --base-url <their-url> --challenge <id>
```

Web track:

```bash
cd harness/ui/web && npm install && npm run install-browsers
BASE_URL=http://localhost:5173 npx playwright test <name>.spec.ts
```

Mobile track has no automated runner. Walk the `acceptance.md` checklist with
them honestly rather than implying coverage that does not exist.

## 6. Iterate

Quote the criterion ID and its text. Not "your balance is wrong" but:

> `BE05-AC3` expects 15491.00. You are getting 13512.59, which is the total
> over every row in the table — so the fold is running on the whole ledger
> rather than this user's. What decides whether a statement belongs to John Doe?

Then stop and let them answer.

## Reading a skip

A skip is never a pass. It means the harness could not reach the behaviour:

| Skip | Meaning |
|---|---|
| "Could not register a user" | `backend-02-create-user` is missing |
| "Could not authenticate" | `backend-03-login` is missing |
| "Reference seed data not present" | needs two users matching the fixture |
| "Cannot create statements" | `POST /statement/` is missing, so balance arithmetic cannot be exercised |
| "GET /users/me returned 404" | the client has no way to learn its own id |

## The fixture

Both demo users have the password `Challenge@123`:

| User | Statements | Balance |
|---|---|---|
| `john.doe@email.com` | 5 | 15491.00 |
| `jane.roe@email.com` | 1 | 4200.00 |

Plus 40 statements belonging to neither — that is what gives the scoping
criteria teeth. Rebuild with `python scripts/seed.py`.

## Traps worth pre-empting

- **Global ledger.** Balances and statement lists are per user. The commonest
  back-end mistake by a wide margin.
- **Purple buttons.** The primary action is near-black `#19191C`. Purple is for
  brand surfaces — auth panel, active nav, table header.
- **Colour-only semantics.** Credit/debit needs the sign and arrow too.
- **Path-param pagination.** It is `?skip=&limit=`, not `/{limit}/{offset}`.
  Old briefs said otherwise and were wrong.
- **`localStorage` on mobile.** Keychain/Keystore. The old mobile brief copied
  this line from the web brief.
- **Fields the API does not support.** Address, Countries, avatar upload,
  Preferences/Security, Transaction ID, Card, Receipt, Search, Notifications.
  Render them, keep them inert, document them. See
  [`ROADMAP.md`](../../../ROADMAP.md).
