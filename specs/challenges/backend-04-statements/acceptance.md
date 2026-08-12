# Acceptance criteria — Statement list with pagination

Challenge: `backend-04-statements`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE04-AC1 — Unauthenticated request is rejected

Given no Authorization header
When GET /statements/
Then status is 401 and the body is `{"detail": "Not authenticated"}`

### BE04-AC2 — Authenticated request returns the documented shape

Given a valid token
When GET /statements/
Then status is 200 and every item has id, description, type, created_at, amount, from_user, to_user, bank_name and authentication

### BE04-AC3 — limit caps the page size

Given John Doe's token
When GET /statements/?skip=0&limit=2
Then exactly 2 items are returned

### BE04-AC4 — skip offsets the page

Given John Doe's token
When GET /statements/?skip=1&limit=10 is compared with skip=0
Then the first item of the skipped page equals the second item of the unskipped page

### BE04-AC5 — Results are scoped to the caller

Given John Doe's token
When GET /statements/?limit=100
Then exactly 5 rows are returned and every one has John Doe as from_user or to_user

### BE04-AC6 — A second user sees only their own rows

Given Jane Roe's token
When GET /statements/?limit=100
Then exactly 1 row is returned and it is not any of John Doe's

### BE04-AC7 — Out-of-range limit is rejected

Given a valid token
When GET /statements/?limit=0
Then status is 422
