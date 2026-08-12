# Acceptance criteria — Create user route

Challenge: `backend-02-create-user`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE02-AC1 — User is created

Given a unique userid and a valid body
When POST /users/
Then status is 201 and the body is `{"msg": "success"}`

### BE02-AC2 — Duplicate userid is rejected

Given a userid that already exists
When POST /users/
Then status is 400 and `detail` is `Username already registered`

### BE02-AC3 — Malformed e-mail is rejected

Given `userid` is `not-an-email`
When POST /users/
Then status is 422

### BE02-AC4 — Malformed birthdate is rejected

Given `birthdate` is `13/01/1988`
When POST /users/
Then status is 422

### BE02-AC5 — Password is hashed, not stored in clear text

Given a user created with password P
When they authenticate with P
Then it succeeds, and no API response anywhere exposes P or a `password` field

### BE02-AC6 — Route is public

Given no Authorization header
When POST /users/ with a valid body
Then status is 201, not 401
