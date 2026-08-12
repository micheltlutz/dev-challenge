# Acceptance criteria — Dashboard shell

Challenge: `web-04-dashboard`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB04-AC1 — Shell renders for an authenticated user

Given a logged-in session
When the dashboard loads
Then `app-shell`, `sidebar` and `topbar` are visible

### WEB04-AC2 — Navigation exposes the three real destinations

Given the sidebar is visible
When its items are inspected
Then `nav-home`, `nav-statement` and `nav-profile` are present

### WEB04-AC3 — The active item is marked

Given the user is on Home
When `nav-home` is inspected
Then it carries an active state distinct from the other items

### WEB04-AC4 — Navigation moves between routes

Given the dashboard
When `nav-statement` is activated
Then the URL changes to the statement route and the shell stays mounted

### WEB04-AC5 — Unauthenticated access is blocked

Given no stored token
When the dashboard route is opened directly
Then the app redirects to login

### WEB04-AC6 — Logout ends the session

Given a logged-in session
When `logout` is activated
Then the stored token is cleared and the login screen is shown

### WEB04-AC7 — Welcome content matches the design

Given the home route
When it has loaded
Then `welcome-heading` is visible and reads `Welcome to My statement`
