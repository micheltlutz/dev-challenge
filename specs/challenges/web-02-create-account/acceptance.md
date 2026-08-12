# Acceptance criteria — Create account form

Challenge: `web-02-create-account`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB02-AC1 — Form renders every designed field

Given the create-account page is open
When it has loaded
Then firstname, lastname, email, password, confirm-password, birthdate and submit are all visible

### WEB02-AC2 — Password confirmation is enforced

Given password and confirm-password differ
When `signup-submit` is activated
Then no request is sent and a mismatch message appears

### WEB02-AC3 — Valid submission registers the user

Given a valid, unused e-mail and matching passwords
When `signup-submit` is activated
Then a POST to /users/ is issued whose fullname is `<First name> <Last Name>` and whose birthdate is ISO formatted

### WEB02-AC4 — Success routes the user onward

Given the API responds 201
When the response is handled
Then `signup-success` appears or the app navigates to the login screen

### WEB02-AC5 — Duplicate e-mail is surfaced

Given the API responds 400 `Username already registered`
When the response is handled
Then `signup-error` is visible and names the e-mail field

### WEB02-AC6 — Design tokens are respected

Given the rendered page
When the submit button's background is sampled
Then it matches `--color-action-default` (#19191C), not the brand purple

### WEB02-AC7 — There is a route to the login screen

Given the create-account page
When `link-login` is activated
Then the login screen is shown
