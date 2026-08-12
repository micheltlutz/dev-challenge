# Screen inventory

Every designed screen, with its mockup, its Figma node, and the challenges that
build it. `scripts/validate_specs.py` checks that the mockup paths here and in
the challenge frontmatter actually exist.

Figma file base URL:

```
https://www.figma.com/file/Q44nlEVrODE7W6iBFRVPZL/Desafio-para-devs---App-%2F-Dashboard-%7C-UX%2FUI?node-id=
```

## Hi-fi screens

| Screen | Mockup | Figma node | Challenges |
|---|---|---|---|
| Create account (web) | [`create-account-web.png`](../../readme_files/images/create-account-web.png) | `1-655` | `web-02-create-account` |
| Create account (mobile) | [`create-account-mobile.png`](../../readme_files/images/create-account-mobile.png) | `1-655` | `mobile-01-create-account` |
| Log in (web) | [`login-web.png`](../../readme_files/images/login-web.png) | `1-655` | `web-03-login` |
| Log in (mobile) | [`login-mobile.png`](../../readme_files/images/login-mobile.png) | `1-731` | `mobile-02-login` |
| Home / dashboard (web) | [`home-web.png`](../../readme_files/images/home-web.png) | `13-3891` | `web-04-dashboard` |
| Home / dashboard (mobile) | [`home-mobile.png`](../../readme_files/images/home-mobile.png) | `13-4267` | `mobile-03-dashboard` |
| Navigation drawer (mobile) | [`menu-mobile.png`](../../readme_files/images/menu-mobile.png) | `13-4267` | `mobile-03-dashboard` |
| Statement (web) | [`statement-web.png`](../../readme_files/images/statement-web.png) | `13-5855` | `web-05-statement`, `fullstack-03-statement` |
| Statement (mobile) | [`statement-mobile.png`](../../readme_files/images/statement-mobile.png) | `19-1283` | `mobile-04-statement` |
| Edit profile (web) | [`profile-web.png`](../../readme_files/images/profile-web.png) | `19-3597` | `web-06-profile-edit` |
| Edit profile (mobile) | [`profile-mobile.png`](../../readme_files/images/profile-mobile.png) | `19-4040` | `mobile-05-profile-edit` |

There is no designed screen for the contact form (`web-01-contact-form`,
`backend-01-contact`, `fullstack-01-contact`). That is intentional: the first
challenge on each track is deliberately open-ended so you can design it
yourself.

## Wireframes (historical)

These predate the hi-fi mockups and are **not** the target. They are kept
because two requirements were only ever drawn here, and the specs that need
those requirements point at them explicitly.

| Wireframe | Mockup | Why it still matters |
|---|---|---|
| Statement (lo-fi) | [`wireframe-statement.png`](../../readme_files/images/wireframe-statement.png) | The only drawing of the **hide-values eye toggle** and the **numbered pagination control**. Both are required by `web-05-statement` / `mobile-04-statement`. |
| Home (lo-fi) | [`wireframe-home.png`](../../readme_files/images/wireframe-home.png) | Earlier dashboard layout. Superseded by `home-web.png`. |
| User details (lo-fi) | [`wireframe-user-details.png`](../../readme_files/images/wireframe-user-details.png) | Earlier profile form with a password eye toggle. Superseded by `profile-web.png`. |

⚠️ The wireframes are in **Portuguese with BRL** (PIX, boleto, `R$`) while the
hi-fi mockups are in **English with USD**. The hi-fi set is canonical: build in
English with `$`. Take only the *interaction* ideas from the wireframes, never
the copy or currency.

## Swagger reference

Screenshots used by the challenger guide, not designs to build:

- [`swagger-auth-padlock.png`](../../readme_files/images/swagger-auth-padlock.png) — authenticated routes carry a padlock.
- [`swagger-schema-contact.png`](../../readme_files/images/swagger-schema-contact.png) — how to read a schema panel.
