# Acceptance criteria — Balance (amount)

Challenge: `backend-05-balance`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### BE05-AC1 — Unauthenticated request is rejected

Given no Authorization header
When GET /balance/
Then status is 401 and the body is `{"detail": "Not authenticated"}`

### BE05-AC2 — Balance is returned as a number

Given a valid token
When GET /balance/
Then status is 200 and the body has a numeric `amount`

### BE05-AC3 — Seeded balance is exact

Given John Doe's token
When GET /balance/
Then `amount` equals 15491.00 within 0.01

### BE05-AC4 — Balance is scoped per user

Given Jane Roe's token
When GET /balance/
Then `amount` equals 4200.00 within 0.01

### BE05-AC5 — Deposit increases the balance

Given a known balance B
When a Deposit of 100.00 is added to the caller's ledger
Then the balance becomes B + 100.00

### BE05-AC6 — Withdrawal decreases the balance

Given a known balance B
When a Withdrawal of 100.00 is added to the caller's ledger
Then the balance becomes B − 100.00

### BE05-AC7 — Transfer to self increases, to another decreases

Given a known balance B
When a Transfer of 100.00 to the caller's own name is added, then one of 100.00 to another name
Then the balance is B after both, having gone up then down
