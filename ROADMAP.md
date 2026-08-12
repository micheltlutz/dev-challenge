# Roadmap

What the lab does not do yet, tracked honestly so the specs can point at it
instead of quietly going silent.

## API gaps the designs already show

The hi-fi mockups depict features the reference API does not support. Today
every affected spec tells the challenger to render them and document them as
unsupported. Building them out would make several challenges richer.

| Gap | Screens affected | Notes |
|---|---|---|
| Avatar upload | Profile (web + mobile) | Needs file upload and static serving. The pencil badge is drawn but does nothing. |
| Address and Countries fields | Profile | Straightforward columns on the user model. |
| Preferences and Security tabs | Profile | Undesigned beyond the tab bar; needs UX before API. |
| Transaction ID and Card | Statement table | The table renders `authentication` as a stand-in today. |
| Receipt / Download | Statement table | Would need generated PDFs or a receipt endpoint. |
| Global search | Top bar | Search across statements. Decorative today. |
| Notifications | Top bar, mobile drawer | No backing model. Decorative today. |
| `POST /statement/` in the specs | — | The route exists and is authenticated, but no challenge uses it. Either give it a challenge or document it as an internal helper. |

## Lab infrastructure

- **Mobile verification.** The mobile track is self-reviewed. Maestro flows
  exist as a starting point, but there is no hosted runner. Native UI
  verification will never match the API suite; the goal is useful, not equal.
- **Design token extraction from Figma.** Tokens were sampled from the exported
  PNGs. A Figma API export would make them authoritative and let CI catch a
  design change the same way it catches an API change.
- **Solution gallery automation.** `SOLUTIONS.md` is maintained by hand from
  submission issues.
- **More languages in the harness docs.** The contract suite is language
  agnostic already; worked examples only cover a few stacks.

## Non-goals

- Grading, scoring or ranking submissions. The harness reports which criteria
  pass; it does not judge people.
- Hosting challengers' solutions. Solutions live in their own repositories.
- Becoming production-grade software. See [SECURITY.md](SECURITY.md) — this is
  a teaching lab and some simplifications are deliberate.

## Contributing to any of this

Pick an item, open an issue to claim it, and read
[CONTRIBUTING.md](CONTRIBUTING.md). Items in the first table are the most
valuable: each one unlocks part of a design that is currently drawn but dead.
