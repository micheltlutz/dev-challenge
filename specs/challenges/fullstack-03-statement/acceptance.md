# Acceptance criteria — Statement and balance, end to end

Challenge: `fullstack-03-statement`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### FS03-AC1 — The API satisfies the backend criteria

Given the candidate's API is running
When the harness runs the BE04 and BE05 suites against it
Then every criterion passes

### FS03-AC2 — The UI satisfies the web criteria against that API

Given both halves are running
When the harness runs the WEB05 suite
Then every criterion passes

### FS03-AC3 — Seed data reproduces the reference fixture

Given the documented seeding command has been run
When John Doe and Jane Roe are queried
Then their balances are 15491.00 and 4200.00 and their statement counts are 5 and 1

### FS03-AC4 — Ledgers are isolated between users

Given two seeded users
When each lists their statements and balance
Then neither sees any of the other's rows and their balances differ

### FS03-AC5 — Pagination is consistent across the stack

Given more rows than one page
When the UI advances a page
Then the API is called with an increased `skip` and the rendered rows match the response

### FS03-AC6 — The balance the UI shows equals the balance the API computes

Given a logged-in user
When the screen's balance is compared with GET /balance/
Then they are equal
