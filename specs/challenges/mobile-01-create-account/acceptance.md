# Acceptance criteria — Create account screen

Challenge: `mobile-01-create-account`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

> ⚠️ This challenge has no automated runner. Use these as a self-review checklist.

### MOB01-AC1 — Screen renders every designed field

Given the create-account screen is open
When it has loaded
Then firstname, lastname, email, password, confirm-password, birthdate and submit are all present

### MOB01-AC2 — Password confirmation is enforced

Given password and confirm-password differ
When submit is tapped
Then no request is sent and a mismatch message appears

### MOB01-AC3 — Valid submission registers the user

Given valid input
When submit is tapped
Then a POST to /users/ is issued with the joined fullname and an ISO birthdate

### MOB01-AC4 — Duplicate e-mail is surfaced

Given the API responds 400
When the response is handled
Then an error is shown against the e-mail field

### MOB01-AC5 — Keyboard does not obscure the focused field

Given the keyboard is open on the last field
When the screen is inspected
Then the focused field and the submit button remain reachable

### MOB01-AC6 — Native date input is used

Given the birthdate field
When it is activated
Then the platform date picker appears rather than a free-text field
