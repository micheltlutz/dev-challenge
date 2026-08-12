# Acceptance criteria — Contact route

Challenge: `backend-01-contact`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE01-AC1 — Valid submission is accepted

Given a body with name, email, message and interest
When POST /contact/
Then status is 200 and the JSON body has a `msg` key containing the submitted name

### BE01-AC2 — Missing field is rejected

Given a body without `message`
When POST /contact/
Then status is 422

### BE01-AC3 — Malformed e-mail is rejected

Given `email` is `not-an-email`
When POST /contact/
Then status is 422

### BE01-AC4 — Route is public

Given no Authorization header
When POST /contact/ with a valid body
Then status is 200, not 401
