---
id: web-05-statement
title: "Statement list, balance and pagination"
track: web
order: 5
difficulty: advanced
estimated_hours: 6
depends_on:
  - "web-04-dashboard"
endpoints:
  - "GET /balance/"
  - "GET /statements/"
figma_node: "13-5855"
mockups:
  - "readme_files/images/statement-web.png"
  - "readme_files/images/wireframe-statement.png"
testids:
  - "balance-amount"
  - "balance-toggle"
  - "kpi-money"
  - "kpi-expenses"
  - "kpi-earnings"
  - "statement-table"
  - "statement-row"
  - "statement-amount"
  - "statement-empty"
  - "pagination"
  - "pagination-prev"
  - "pagination-next"
  - "pagination-page"
acceptance: acceptance.md
verify: "harness/ui/web/statement.spec.ts"
tags:
  - "data-fetching"
  - "pagination"
  - "money-semantics"
  - "a11y"
---

# Statement list, balance and pagination

**Track:** web · **Difficulty:** advanced · **Estimated:** 6h  
**Prerequisites:** [`web-04-dashboard`](../web-04-dashboard/spec.md)

## Objective

The most substantial screen in the track: the user's balance, three KPI cards, a
paginated transactions table, and a control that hides monetary values.

## Design

[Open this screen in Figma](https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?node-id=13-5855)

![Statement Web](../../../readme_files/images/statement-web.png)
![Wireframe Statement](../../../readme_files/images/wireframe-statement.png)

Design system: [`../../design/style-guide.md`](../../design/style-guide.md) · tokens: [`../../design/tokens.json`](../../design/tokens.json)

## What you build

The **Statement** screen from the design, inside the shell from
`web-04-dashboard`.

### Balance and KPI cards

Fetch `GET /balance/` and show `amount` as the headline figure.

Three cards across (horizontally scrollable on mobile): **Money** (purple wallet
icon), **Expenses** (red icon), **Earnings** (green icon). Only Money is backed
by the API — derive Expenses and Earnings from the fetched statements by summing
debits and credits, and note in your README that the mockup's fixed figures are
not API-backed.

### Hide values

A toggle (`balance-toggle`) masks every monetary value on the screen — the
balance, the KPI values and the amount column — replacing them with a mask such
as `••••••`. This is drawn in
[`wireframe-statement.png`](../../../readme_files/images/wireframe-statement.png)
as the crossed-out eye, and it is a **required** behaviour even though the hi-fi
mockup omits it. The setting persists across a page reload.

### Transactions table

Fetch `GET /statements/?skip=<n>&limit=<size>`.

Columns from the design: Description · Transaction ID · Type · Card · Date ·
Amount · Receipt.

- **Amount** is `--color-semantic-credit` with a `+` and `↑` for Deposit and
  self-Transfer, `--color-semantic-debit` with a `-` and `↓` otherwise.
- **Transaction ID**, **Card** and **Receipt** are not in the API. Render them
  from the `authentication` field, a placeholder, and a non-functional Download
  button respectively — and say so in your README.

### Pagination

Numbered control (`< 1 2 … 9 10 >`), as drawn in the wireframe. Changing page
refetches with a new `skip`. Disable `pagination-prev` on the first page.

When there are no rows, show `statement-empty` instead of an empty table.

## Requirements

- Colour must not be the only signal for credit vs debit — keep the arrow and
  the sign, so the table is readable without colour vision.
- The mask must hide the values in the DOM, not merely blur them visually.

## Test IDs

Expose these as `data-testid` (web) or the platform accessibility identifier (mobile). They are the contract that lets the harness verify your UI without dictating your framework.

```
balance-amount
balance-toggle
kpi-money
kpi-expenses
kpi-earnings
statement-table
statement-row
statement-amount
statement-empty
pagination
pagination-prev
pagination-next
pagination-page
```

## Acceptance criteria

See [`acceptance.md`](acceptance.md) — 9 criteria (`WEB05-AC1`…`WEB05-AC9`).

## Verifying your work

```bash
# Linux
docker run --rm --network host ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://localhost:8000 --challenge web-05-statement

# macOS / Windows
docker run --rm ghcr.io/micheltlutz/dev-challenge-harness \
  --base-url http://host.docker.internal:8000 --challenge web-05-statement
```

See [`../../../harness/README.md`](../../../harness/README.md) for the UI runner and other options.

## Final considerations

- Write a README that says how to run your project, what you chose and why.
- Handle the error paths, not just the happy one.
- Tests are not required, but they are the clearest signal you can send.
- If something in this spec is ambiguous or wrong, [open an issue](https://github.com/micheltlutz/dev-challenge/issues/new/choose) — fixing the spec is a real contribution.
