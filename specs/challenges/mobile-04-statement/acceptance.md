# Acceptance criteria — Statement list, balance and pagination

Challenge: `mobile-04-statement`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

> ⚠️ This challenge has no automated runner. Use these as a self-review checklist.

### MOB04-AC1 — Balance is fetched and shown

Given an authenticated session
When the statement screen opens
Then GET /balance/ is called and the amount is displayed

### MOB04-AC2 — Statements are fetched and listed

Given an authenticated session
When the statement screen opens
Then GET /statements/ is called and one row is rendered per returned item

### MOB04-AC3 — Credits and debits are distinguished

Given rows of both kinds
When the amounts are inspected
Then credits use the credit colour with `+`/`↑` and debits the debit colour with `-`/`↓`

### MOB04-AC4 — Hide-values masks every figure

Given values are visible
When the toggle is activated
Then the balance, KPI values and every row amount are masked

### MOB04-AC5 — The mask preference survives a restart

Given values are hidden
When the app is killed and reopened
Then they are still hidden

### MOB04-AC6 — The next page loads

Given more rows than one page
When the user scrolls to the end
Then GET /statements/ is refetched with an increased `skip` and more rows appear

### MOB04-AC7 — Empty state is shown

Given the API returns an empty list
When the screen renders
Then the empty state is visible and no rows exist

### MOB04-AC8 — Pull-to-refresh resets the list

Given the user has loaded several pages
When they pull to refresh
Then the list resets to the first page
