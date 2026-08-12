# Acceptance criteria — Contact, end to end

Challenge: `fullstack-01-contact`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### FS01-AC1 — The API satisfies the backend criteria

Given the candidate's API is running
When the harness runs the BE01 suite against it
Then every BE01 criterion passes

### FS01-AC2 — The UI satisfies the web criteria against that API

Given both halves are running
When the harness runs the WEB01 suite against the UI
Then every WEB01 criterion passes

### FS01-AC3 — The stack starts with one command

Given a clean checkout of the candidate's repo
When the documented start command is run
Then both the API and the UI become reachable
> **Manual review.** The harness cannot run an arbitrary project's start command safely. A reviewer follows the candidate's README on a clean checkout.

### FS01-AC4 — Cross-origin requests work

Given the UI is served from a different origin than the API
When the form is submitted
Then the request succeeds without a CORS error
