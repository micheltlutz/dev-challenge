# Acceptance criteria — Edit profile

Challenge: `web-06-profile-edit`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB06-AC1 — Form is prefilled

Given an authenticated user
When the profile screen loads
Then firstname, lastname, email and birthdate show the current values

### WEB06-AC2 — E-mail is not editable

Given the profile form
When `profile-email` is inspected
Then it is read-only or disabled

### WEB06-AC3 — Save is disabled until something changes

Given a freshly loaded form
When nothing has been edited
Then `profile-save` is disabled

### WEB06-AC4 — Saving persists the change

Given the fullname has been edited
When `profile-save` is activated
Then a PUT to /users/{id} is issued with the joined fullname

### WEB06-AC5 — Success is confirmed and reflected

Given the API responds 200
When the response is handled
Then `profile-success` is visible and the shell shows the updated name

### WEB06-AC6 — The change survives a reload

Given a saved profile change
When the page is reloaded
Then the new values are shown

### WEB06-AC7 — Out-of-scope fields do not pretend to save

Given Address, Countries or avatar upload are rendered
When the form is saved
Then they are not sent to the API and the README documents them as unsupported
