# Acceptance criteria — Dashboard and navigation drawer

Challenge: `mobile-03-dashboard`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

> ⚠️ This challenge has no automated runner. Use these as a self-review checklist.

### MOB03-AC1 — Shell renders for an authenticated user

Given a logged-in session
When the app opens
Then the top bar and the home content are shown

### MOB03-AC2 — Drawer opens and lists the destinations

Given the home screen
When the drawer is opened
Then Home, Statement, Profile and Logout are present

### MOB03-AC3 — The active item is marked

Given the user is on Home
When the drawer is open
Then the Home item carries an active state distinct from the others

### MOB03-AC4 — Navigation moves between destinations

Given the drawer is open
When Statement is tapped
Then the statement screen is shown and the drawer closes

### MOB03-AC5 — Unauthenticated launch goes to login

Given no stored token
When the app launches
Then the login screen is shown

### MOB03-AC6 — Logout resets the stack

Given a logged-in session
When Logout is tapped
Then secure storage is cleared and the back gesture cannot reach an authenticated screen
