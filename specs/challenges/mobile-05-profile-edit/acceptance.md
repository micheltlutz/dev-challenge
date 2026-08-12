# Acceptance criteria — Edit profile

Challenge: `mobile-05-profile-edit`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

> ⚠️ This challenge has no automated runner. Use these as a self-review checklist.

### MOB05-AC1 — Form is prefilled

Given an authenticated user
When the profile screen opens
Then firstname, lastname, email and birthdate show the current values

### MOB05-AC2 — E-mail is not editable

Given the profile form
When the e-mail field is inspected
Then it is read-only or disabled

### MOB05-AC3 — Save is disabled until something changes

Given a freshly loaded form
When nothing has been edited
Then Save is disabled

### MOB05-AC4 — Saving persists the change

Given the fullname has been edited
When Save is tapped
Then a PUT to /users/{id} is issued with the joined fullname

### MOB05-AC5 — Success is confirmed and reflected

Given the API responds 200
When the response is handled
Then a success state is shown and the drawer header shows the updated name

### MOB05-AC6 — The change survives a restart

Given a saved profile change
When the app is killed and reopened
Then the new values are shown

### MOB05-AC7 — Out-of-scope fields do not pretend to save

Given Address, Countries or avatar upload are rendered
When the form is saved
Then they are not sent to the API and the README documents them as unsupported
