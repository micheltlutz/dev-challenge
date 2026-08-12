# Acceptance criteria — Statement list, balance and pagination

Challenge: `web-05-statement`

Each criterion has a stable ID. The verification harness marks every test with the ID it covers, so a failing test points straight back to the line below that it violates.

### WEB05-AC1 — Balance is fetched and shown

Given an authenticated session
When the statement screen loads
Then GET /balance/ is called and `balance-amount` shows the returned amount

### WEB05-AC2 — Statements are fetched and listed

Given an authenticated session
When the statement screen loads
Then GET /statements/ is called and one `statement-row` is rendered per returned item

### WEB05-AC3 — Credits and debits are distinguished

Given rows of both kinds
When `statement-amount` cells are inspected
Then credits carry the credit colour with a `+`/`↑` and debits the debit colour with a `-`/`↓`

### WEB05-AC4 — Hide-values masks every figure

Given values are visible
When `balance-toggle` is activated
Then `balance-amount`, the KPI values and every `statement-amount` show a mask and the numeric text is absent from the DOM

### WEB05-AC5 — The mask preference persists

Given values are hidden
When the page is reloaded
Then they are still hidden

### WEB05-AC6 — Pagination advances the page

Given more rows than fit one page
When `pagination-next` is activated
Then GET /statements/ is refetched with an increased `skip` and the rows change

### WEB05-AC7 — Previous is disabled on the first page

Given the first page is shown
When `pagination-prev` is inspected
Then it is disabled

### WEB05-AC8 — Empty state replaces the table

Given the API returns an empty list
When the screen renders
Then `statement-empty` is visible and no `statement-row` exists

### WEB05-AC9 — KPI cards are present

Given the statement screen
When it has loaded
Then `kpi-money`, `kpi-expenses` and `kpi-earnings` are visible
