# Style guide

The canonical design lives in Figma. This file exists so that the design is
also readable **without** Figma access — by a challenger on a plane, by CI, and
by a coding agent that cannot open a browser.

- **Figma file:** [Desafio para devs - App / Dashboard | UX/UI](https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?type=design&node-id=1%3A4&mode=design)
- **Machine-readable tokens:** [`tokens.json`](tokens.json) (DTCG) → [`tokens.css`](tokens.css)
- **Screen inventory:** [`screens.md`](screens.md)

Design and UX by [Aline Moraes](https://www.linkedin.com/in/alinegermanodemoraes/).

If a value here disagrees with Figma, Figma wins — open an issue so the tokens
can be corrected.

## Brand

The product is a fictional personal-banking dashboard called **My Statement**.

| Role | Token | Value |
|---|---|---|
| Primary purple | `--color-brand-primary` | `#8E48EC` |
| Deep purple | `--color-brand-primary-deep` | `#4E01B4` |
| Soft purple | `--color-brand-primary-soft` | `#C79BEC` |
| Purple wash | `--color-brand-primary-wash` | `#F7F1FE` |

Purple carries brand presence: the auth split panel, the active navigation
item, the statement table header. It is **not** the button colour.

## Actions

Primary buttons are near-black, full-width inside their container, with white
labels. This is the single most distinctive thing about the design — a purple
button is wrong.

| Role | Token | Value |
|---|---|---|
| Button background | `--color-action-default` | `#19191C` |
| Button hover | `--color-action-hover` | `#2A2A2D` |
| Button label | `--color-action-on-action` | `#FFFFFF` |

Secondary buttons ("Create account" under the login form) are outlined: 1px
border in `--color-surface-border`, transparent background, dark label.

## Surfaces

| Role | Token | Value |
|---|---|---|
| App canvas | `--color-surface-canvas` | `#EFEFF0` |
| Card / panel | `--color-surface-card` | `#FFFFFF` |
| Sunken area | `--color-surface-sunken` | `#F5F5F6` |
| Hairline border | `--color-surface-border` | `#EBEBEB` |

Cards sit on the grey canvas with `--radius-lg` corners and `--shadow-card`.

## Money semantics

This is a banking UI, so colour carries meaning. Get this wrong and the screen
is unreadable.

| Meaning | Token | Value | Where |
|---|---|---|---|
| Credit / money in | `--color-semantic-credit` | `#0CB97B` | `+$750`, upward arrow, Earnings KPI |
| Debit / money out | `--color-semantic-debit` | `#E02244` | `-$2,500`, downward arrow |
| Expenses KPI icon | `--color-semantic-debit-soft` | `#E4482B` | the warmer red on the Expenses card only |

Never use red/green as decoration elsewhere.

Accessibility note: colour alone must not encode the credit/debit distinction.
The mockups pair it with a `↑` / `↓` arrow and a `+` / `-` sign — keep both.

## Typography

Poppins in the mockups; `tokens.json` ships a fallback stack so no webfont is
required.

| Step | Token | Size | Typical use |
|---|---|---|---|
| 3xl | `--font-size-3xl` | 40px | Balance figure |
| 2xl | `--font-size-2xl` | 32px | Page title ("Welcome to My statement") |
| xl | `--font-size-xl` | 24px | Card heading, "Log in" |
| lg | `--font-size-lg` | 20px | KPI value |
| md | `--font-size-md` | 16px | Body, inputs |
| sm | `--font-size-sm` | 14px | Table cells, helper text |
| xs | `--font-size-xs` | 12px | Labels, timestamps |

Weights: 400 body, 500 nav and labels, 600 headings and amounts, 700 sparingly.

## Spacing and shape

4px base scale (`--space-1` … `--space-8`). Cards and inputs use
`--radius-lg` (12px); avatars and pills use `--radius-circle` / `--radius-pill`.

## Layout

| Thing | Token | Value |
|---|---|---|
| Desktop frame | `--layout-breakpoint-desktop` | 1440×1024 |
| Mobile frame | `--layout-breakpoint-mobile` | 375×812 |
| Sidebar / drawer | `--layout-sidebar-width` | 256px |
| Top bar | `--layout-topbar-height` | 72px |
| Content max width | `--layout-content-max-width` | 1184px |
| Input / button height | `--layout-field-height` | 48px |

**Auth screens (web)** are a 50/50 split: purple panel with the wordmark and an
illustration on the left, white form card on the right. On mobile the panel
collapses and only the form remains.

**App shell (web)** is a white sidebar (logo, then Home / Statement / Profile /
Setting / Logout) beside a grey canvas, with a top bar holding search, a gear,
a bell, and the avatar. On mobile the sidebar becomes a drawer
(`menu-mobile.png`) and the top bar keeps only the avatar and search.

## Components you will need

- **Text field** — 48px tall, `--radius-lg`, hairline border, label above, optional
  leading icon (the password field has a lock).
- **Primary / secondary button** — see Actions.
- **KPI card** — white card, coloured circular icon, caption, large value.
  Three across on web; horizontally scrollable on mobile.
- **Transactions table** (web) — purple header row; columns Description,
  Transaction ID, Type, Card, Date, Amount, Receipt.
- **Transactions list** (mobile) — two columns: description block and amount.
- **Nav item** — active state is purple text plus a purple indicator.
- **Avatar** — circular, with a black pencil edit badge on the profile screen.

## Deliberate gaps

The mockups show more than the API supports. Each of these is out of scope
unless a spec says otherwise — mock the data client-side and move on:

Address · Countries · avatar upload · Preferences and Security tabs ·
Transaction ID · Card number · Receipt/Download · global Search · Notifications.

See [`../../ROADMAP.md`](../../ROADMAP.md) for which of these are planned.
