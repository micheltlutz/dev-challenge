# Security Policy

## Scope, and a warning

This repository is a **teaching lab**, not production software. The reference
API deliberately keeps some things simple so the code stays readable:

- SQLite with a committed, seeded database.
- Permissive CORS by default (`CORS_ALLOW_ORIGINS=*`), because challengers run
  front-ends on arbitrary localhost ports.
- Demo accounts with a published password (`Challenge@123`).

**Do not deploy this API as-is with real user data, and do not reuse its code
verbatim in production.** If you host your own instance, at minimum set a
private `SECRET`, pin `CORS_ALLOW_ORIGINS`, and reseed with your own accounts.

## Supported versions

| Version | Supported |
|---|---|
| 2.0.x | ✅ |
| 1.2.x | ❌ |
| < 1.2 | ❌ |

## Reporting a vulnerability

Report privately — please do not open a public issue for anything exploitable.

1. Preferred: open a [private security advisory](https://github.com/micheltlutz/dev-challenge/security/advisories/new).
2. Alternatively, e-mail **michel_lutz@icloud.com** with `[dev-challenge security]`
   in the subject.

Please include what you found, how to reproduce it, and the impact you think it
has. This is a volunteer-maintained project: expect a first response within
about a week. There is no bug bounty.

## Dependencies

`requirements.txt` uses version floors rather than `~=` pins, so security
patches are picked up instead of being locked out. `pip-audit` runs in CI on
every push and weekly on a schedule
([`.github/workflows/audit.yml`](.github/workflows/audit.yml)), and Dependabot
is configured in [`.github/dependabot.yml`](.github/dependabot.yml).

Run it yourself with `pip-audit`.

## Known history

- **JWT signing key exposure (fixed in 2.0.0).** Versions up to 1.2.0 committed
  `app/.env` to the repository, including the `SECRET` used to sign JWTs on the
  public instance. That key has been rotated and `app/.env` is no longer
  tracked. The key remains visible in git history; it is dead and grants no
  access. If you forked or cloned before 2.0.0, set your own `SECRET`.
- **Vulnerable dependencies (fixed in 2.0.0).** Versions up to 1.2.0 pinned
  `PyJWT~=2.8.0`, which carried five advisories including CVE-2026-48526
  (a public-key JWK accepted as an HMAC secret, enabling forged HS256 tokens)
  and CVE-2026-32597 (unknown `crit` header extensions accepted). Two of those
  were reachable, since the API decodes attacker-supplied tokens. 2.0.0 moves to
  `PyJWT>=2.13.0`, drops `python-jose` entirely (7 advisories, one with no fix
  available), and replaces `fastapi[all]` with the packages actually imported.
  The token decoder now also pins a single-algorithm allow-list and requires
  `exp` and `sub`.
- An upstream FastAPI vulnerability affecting 1.1.0 was reported by Marcello via
  huntr and resolved by upgrading the dependency in 1.1.1.
