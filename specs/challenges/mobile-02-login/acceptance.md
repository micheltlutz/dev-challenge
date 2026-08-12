# Acceptance criteria — Login screen

Challenge: `mobile-02-login`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

> ⚠️ This challenge has no automated runner. Use these as a self-review checklist.

### MOB02-AC1 — Screen renders

Given the login screen is open
When it has loaded
Then the e-mail field, password field and submit button are present

### MOB02-AC2 — Password entry is masked

Given the password field
When text is entered
Then it is obscured

### MOB02-AC3 — Valid credentials authenticate

Given seeded credentials
When submit is tapped
Then a POST to /auth/ is issued and the dashboard is shown

### MOB02-AC4 — Token is kept in secure storage

Given a successful login
When the storage layer is inspected
Then the token is in Keychain/Keystore-backed storage and not in AsyncStorage, SharedPreferences or UserDefaults

### MOB02-AC5 — Session survives an app restart

Given a logged-in user
When the app is killed and reopened within the token lifetime
Then they remain logged in

### MOB02-AC6 — Bad credentials show an error

Given the API responds 401
When the response is handled
Then an error is shown and no navigation happens

### MOB02-AC7 — Rejected sessions return to login

Given a protected request answers 401
When the response is handled
Then the stored token is cleared and the login screen is shown
