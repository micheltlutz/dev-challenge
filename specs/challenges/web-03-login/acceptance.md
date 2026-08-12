# Acceptance criteria — Login form

Challenge: `web-03-login`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB03-AC1 — Form renders

Given the login page is open
When it has loaded
Then `login-email`, `login-password` and `login-submit` are visible

### WEB03-AC2 — Valid credentials authenticate

Given seeded credentials
When `login-submit` is activated
Then a POST to /auth/ is issued with userid and password

### WEB03-AC3 — Token is persisted

Given the API responds 200 with a token
When the response is handled
Then the token is stored and survives a page reload

### WEB03-AC4 — Success navigates to the dashboard

Given a successful login
When navigation settles
Then the dashboard shell is displayed

### WEB03-AC5 — Bad credentials show an error

Given the API responds 401
When the response is handled
Then `login-error` is visible and no navigation happens

### WEB03-AC6 — Protected requests carry the Bearer token

Given an authenticated session
When a protected endpoint is called
Then the request carries `Authorization: Bearer <token>`

### WEB03-AC7 — Expired or rejected sessions return to login

Given a protected request answers 401
When the response is handled
Then the stored token is cleared and the login screen is shown
