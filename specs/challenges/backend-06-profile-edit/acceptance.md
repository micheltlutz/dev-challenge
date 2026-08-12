# Acceptance criteria — Edit profile route

Challenge: `backend-06-profile-edit`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE06-AC1 — Unauthenticated request is rejected

Given no Authorization header
When PUT /users/{id}
Then status is 401 and the body is `{"detail": "Not authenticated"}`

### BE06-AC2 — Owner can update their profile

Given a user's own token and id
When PUT /users/{id} with a new fullname
Then status is 200 and the response shows the new fullname

### BE06-AC3 — Partial update leaves other fields untouched

Given a user whose birthdate is B
When PUT /users/{id} with only a fullname
Then the response still shows birthdate B

### BE06-AC4 — Response never exposes the password

Given any successful update
When the response body is inspected
Then it contains no `password` or `hashed_password` key

### BE06-AC5 — Changing the password rotates the credential

Given a user changes their password from P to Q
When they authenticate
Then P is rejected with 401 and Q succeeds with 200

### BE06-AC6 — A user cannot edit someone else

Given Jane Roe's token and John Doe's user id
When PUT /users/{john_id}
Then status is 403 and John Doe's profile is unchanged

### BE06-AC7 — Unknown user id is a 404

Given a valid token and a user id that does not exist
When PUT /users/{id}
Then status is 404

### BE06-AC8 — The caller can discover their own profile

Given a valid token
When GET /users/me
Then status is 200 and the body has the caller's id, userid, fullname and birthdate, and no password

