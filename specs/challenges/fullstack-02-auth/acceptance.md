# Acceptance criteria — Authentication, end to end

Challenge: `fullstack-02-auth`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### FS02-AC1 — The API satisfies the backend criteria

Given the candidate's API is running
When the harness runs the BE02 and BE03 suites against it
Then every criterion passes

### FS02-AC2 — The UI satisfies the web criteria against that API

Given both halves are running
When the harness runs the WEB02 and WEB03 suites
Then every criterion passes

### FS02-AC3 — Register-then-login works end to end

Given a fresh e-mail
When a user registers through the UI and then logs in
Then they reach the authenticated shell

### FS02-AC4 — Protected routes are guarded

Given no session
When a protected route is opened directly
Then the user is sent to login

### FS02-AC5 — The signing secret is not in the repository

Given the candidate's repository
When it is searched for the signing secret
Then the secret is supplied by the environment and no real value is committed
> **Manual review.** This is a property of the candidate's repository, not of a running service. A reviewer greps the history and the working tree.

### FS02-AC6 — Logout ends the session for real

Given a logged-in user
When they log out
Then the token is gone from storage and protected routes are unreachable
