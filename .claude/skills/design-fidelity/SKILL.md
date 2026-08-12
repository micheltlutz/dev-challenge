---
name: design-fidelity
description: Compare an implemented UI against the dev-challenge design tokens and mockups — colours, type scale, spacing, layout and the required testids. Use when someone asks "does this match the design", wants a design review of a screen they built, is working on a web or mobile challenge's visual fidelity, or asks which colour or token to use.
---

# Design fidelity

Check an implementation against the lab's design system, and say specifically
what is off rather than "looks close".

## Sources, in order of authority

1. **Figma** — the canonical design. Node ids per screen are in
   [`specs/design/screens.md`](../../../specs/design/screens.md). Reachable via
   the optional Figma MCP server in [`.mcp.json`](../../../.mcp.json).
2. **[`specs/design/tokens.json`](../../../specs/design/tokens.json)** — sampled
   from the exported mockups. The machine-readable fallback, and good enough for
   every challenge.
3. **[`specs/design/style-guide.md`](../../../specs/design/style-guide.md)** —
   the same thing in prose, with the reasoning.
4. **The mockup PNGs** in `readme_files/images/`.

If a token disagrees with Figma, Figma wins — and the token is a bug worth an
issue.

## How to check

If browser automation is available, screenshot the running UI at the design's
viewport (1440×1024 desktop, 375×812 mobile) and compare against the mockup
side by side. Otherwise read the stylesheet and component source.

Sample computed styles rather than trusting the source — a variable can be
defined correctly and then overridden.

## The checklist

### Colour

| Role | Token | Value |
|---|---|---|
| Primary action | `--color-action-default` | `#19191C` |
| Brand purple | `--color-brand-primary` | `#8E48EC` |
| Deep purple | `--color-brand-primary-deep` | `#4E01B4` |
| Canvas | `--color-surface-canvas` | `#EFEFF0` |
| Credit | `--color-semantic-credit` | `#0CB97B` |
| Debit | `--color-semantic-debit` | `#E02244` |

**The mistake to look for first: a purple primary button.** It is the single
most common fidelity failure. Purple is for brand surfaces — the auth split
panel, the active nav item, the statement table header. Actions are near-black.

**Second: hard-coded hex.** If the stylesheet contains `#8E48EC` rather than
`var(--color-brand-primary)`, say so. The tokens exist to be imported.

### Money semantics

Credit green, debit red — **and never colour alone**. The design pairs it with
`↑`/`↓` and `+`/`-`, and `WEB05-AC3` checks for it. A table that only uses
colour is unreadable to a red-green colour-blind user, which is roughly one in
twelve men.

### Typography

Poppins, falling back to the stack in `tokens.json`. Scale: 12 · 14 · 16 · 20 ·
24 · 32 · 40. Weights 400 body, 500 nav and labels, 600 headings and amounts.

### Spacing and shape

4px base scale. Cards and inputs `--radius-lg` (12px); avatars and pills round.
Inputs and buttons are 48px tall.

### Layout

- Auth screens on web: 50/50 split, purple panel left, form right. On mobile
  the panel is gone.
- App shell: 256px sidebar, 72px top bar, 1184px content max width. On mobile
  the sidebar becomes a drawer.

### Test IDs

Check the `testids:` list in the challenge frontmatter. Every one must be
present. This is not cosmetic — the harness drives the UI through them, so a
missing testid means the criterion cannot be verified at all.

## Deliberate gaps

These appear in the mockups and are **not** backed by the API. Do not report
them as missing features; do check they are inert and documented:

Address · Countries · avatar upload · Preferences and Security tabs ·
Transaction ID · Card · Receipt/Download · Search · Notifications.

See [`ROADMAP.md`](../../../ROADMAP.md).

## Wireframes are not the target

`wireframe-*.png` are an earlier generation, in Portuguese with BRL, while the
hi-fi mockups are English with USD. Build to the hi-fi set.

Two exceptions, because they were only ever drawn in the wireframe and the
specs require them: the **hide-values eye toggle** and the **numbered
pagination control**.

## Reporting

Be specific and quantitative. Not "the spacing is off" but:

> The card padding is 20px; the design uses `--space-5` (24px).

Group findings by severity: broken contract (missing testid, wrong semantic
colour) before visual drift (a few px of padding). Say what is right, too — a
review that is only complaints is hard to act on.
