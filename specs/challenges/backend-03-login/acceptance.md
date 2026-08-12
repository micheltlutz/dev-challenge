# Acceptance criteria — Login route

Challenge: `backend-03-login`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE03-AC1 — Valid credentials return a token

Given a registered user's correct credentials
When POST /auth/
Then status is 200 and the body has a non-empty `access_token` and `token_type` equal to `bearer`

### BE03-AC2 — Wrong password is rejected

Given a registered userid and a wrong password
When POST /auth/
Then status is 401 and `detail` is `Incorrect username or password`

### BE03-AC3 — Unknown user is rejected identically

Given a userid that does not exist
When POST /auth/
Then status is 401 with the same `detail` as BE03-AC2

### BE03-AC4 — Token is a valid HS256 JWT

Given a token from a successful login
When it is decoded
Then its header algorithm is HS256 and it carries `sub` and an `exp` roughly 30 minutes ahead

### BE03-AC5 — Token opens a protected route

Given a fresh token
When GET /balance/ is called with `Authorization: Bearer <token>`
Then status is 200

### BE03-AC6 — Tampered token is rejected

Given a token with its final character altered
When GET /balance/ is called with it
Then status is 401
