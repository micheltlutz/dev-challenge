# Moved — Statement list, balance and pagination

This challenge now lives in the spec layer, where it has a machine-checked API
contract and numbered acceptance criteria:

**➡️ [`specs/challenges/web-05-statement/spec.md`](../specs/challenges/web-05-statement/spec.md)**

- Acceptance criteria: [`acceptance.md`](../specs/challenges/web-05-statement/acceptance.md)
- All challenges: [`specs/README.md`](../specs/README.md)

## Why it moved

The old briefs disagreed with the running API in ways that broke the first
request a challenger made. Specs are now generated against the live contract and
verified in CI, so that cannot happen again. See
[`specs/README.md`](../specs/README.md).

*This stub exists so older links keep working. It will be removed in a future
major version.*
