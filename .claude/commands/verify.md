---
description: Run the verification harness and explain the results as acceptance criteria
argument-hint: [challenge-id] [--base-url URL]
allowed-tools: Read, Grep, Glob, Bash(python harness/cli.py:*), Bash(pytest harness/:*), Bash(curl:*)
---

Verify a solution against its acceptance criteria.

## Work out the target

Default `--base-url` is `http://localhost:8000`. If `$ARGUMENTS` names a
challenge or a URL, use those. If you do not know where their app is running,
ask — do not guess and report a connection error as a failure.

```
python harness/cli.py --base-url <url> --challenge <id>
```

Omit `--challenge` to run everything.

For the web track the runner is Playwright:

```
cd harness/ui/web && BASE_URL=<their-frontend> npx playwright test
```

## Explain the scorecard

Do not paste the raw output and stop. For each **failing** criterion:

1. Quote the criterion — its ID and its Given/When/Then.
2. State what actually happened.
3. Point at the likely cause, in their code if you can see it.
4. Ask what they think is going on, before giving the fix. Default posture is
   mentoring; see `AGENTS.md`.

For each **skipped** criterion, explain that a skip is not a pass and name the
missing prerequisite:

| Skip | Meaning |
|---|---|
| "Could not register a user" | `backend-02-create-user` is missing |
| "Could not authenticate" | `backend-03-login` is missing |
| "Reference seed data not present" | needs two users matching the fixture |
| "Cannot create statements" | `POST /statement/` is missing |
| "GET /users/me returned 404" | the client cannot learn its own id |

Ignore **uncovered** criteria unless they ask — those are UI or manual-review
items the API harness cannot reach, not something they did wrong.

## Close

One line on where they stand — "6 of 7, and the last one is the scoping rule" —
and what to do next. If everything passes, say so without padding, and point at
`/next`.
