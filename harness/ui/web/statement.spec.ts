import { test, expect, ac, toNumber, looksMasked } from './support/ac';

// web-05-statement / fullstack-03-statement

async function gotoStatement(page) {
  await page.getByTestId('nav-statement').click();
  await expect(page.getByTestId('balance-amount')).toBeVisible({ timeout: 15_000 });
}

test(ac('WEB05-AC1', 'Balance is fetched and shown'), async ({ loggedIn: page }) => {
  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/balance') && r.status() === 200),
    gotoStatement(page),
  ]);

  const { amount } = await response.json();
  const shown = toNumber(await page.getByTestId('balance-amount').textContent());

  expect(shown, `the screen shows ${shown} but the API returned ${amount}`).toBeCloseTo(
    amount,
    1
  );
});

test(ac('WEB05-AC2', 'Statements are fetched and listed'), async ({ loggedIn: page }) => {
  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/statements') && r.status() === 200),
    gotoStatement(page),
  ]);

  const rows = await response.json();
  await expect(page.getByTestId('statement-row')).toHaveCount(rows.length);
});

test(ac('WEB05-AC3', 'Credits and debits are distinguished'), async ({ loggedIn: page }) => {
  await gotoStatement(page);

  const amounts = page.getByTestId('statement-amount');
  const count = await amounts.count();
  expect(count, 'need at least one statement row to check').toBeGreaterThan(0);

  const seen = new Set<string>();
  for (let i = 0; i < count; i += 1) {
    const cell = amounts.nth(i);
    const text = (await cell.textContent()) ?? '';
    const colour = await cell.evaluate((el: Element) => getComputedStyle(el).color);

    expect(
      /[+\-−↑↓]/.test(text),
      `"${text.trim()}" carries no sign or arrow. Colour alone must not encode ` +
        'credit vs debit -- the table has to stay readable without colour vision.'
    ).toBe(true);

    seen.add(colour);
  }

  if (count > 1) {
    expect(
      seen.size,
      'every amount renders in the same colour; credits and debits should differ'
    ).toBeGreaterThan(1);
  }
});

test(ac('WEB05-AC4', 'Hide-values masks every figure'), async ({ loggedIn: page }) => {
  await gotoStatement(page);

  const balance = page.getByTestId('balance-amount');
  expect(looksMasked(await balance.textContent()), 'values should start visible').toBe(false);

  await page.getByTestId('balance-toggle').click();

  expect(
    looksMasked(await balance.textContent()),
    'the balance still shows digits after toggling; the mask must remove the value ' +
      'from the DOM, not merely blur it visually'
  ).toBe(true);

  const amounts = page.getByTestId('statement-amount');
  for (let i = 0; i < (await amounts.count()); i += 1) {
    expect(
      looksMasked(await amounts.nth(i).textContent()),
      `statement amount ${i} still shows digits while values are hidden`
    ).toBe(true);
  }
});

test(ac('WEB05-AC5', 'The mask preference persists'), async ({ loggedIn: page }) => {
  await gotoStatement(page);
  await page.getByTestId('balance-toggle').click();

  await page.reload();
  await expect(page.getByTestId('balance-amount')).toBeVisible({ timeout: 15_000 });

  expect(
    looksMasked(await page.getByTestId('balance-amount').textContent()),
    'the hide-values preference should survive a reload'
  ).toBe(true);
});

test(ac('WEB05-AC6', 'Pagination advances the page'), async ({ loggedIn: page }) => {
  await gotoStatement(page);

  const first = await page.getByTestId('statement-row').first().textContent();

  const [request] = await Promise.all([
    page.waitForRequest((r) => r.url().includes('/statements')),
    page.getByTestId('pagination-next').click(),
  ]);

  const skip = new URL(request.url()).searchParams.get('skip');
  expect(Number(skip), 'the next page must request a larger skip').toBeGreaterThan(0);

  await expect(page.getByTestId('statement-row').first()).not.toHaveText(first ?? '');
});

test(ac('WEB05-AC7', 'Previous is disabled on the first page'), async ({
  loggedIn: page,
}) => {
  await gotoStatement(page);

  await expect(page.getByTestId('pagination-prev')).toBeDisabled();
});

test(ac('WEB05-AC8', 'Empty state replaces the table'), async ({ loggedIn: page }) => {
  await page.route('**/statements**', (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: '[]' })
  );

  await gotoStatement(page);

  await expect(page.getByTestId('statement-empty')).toBeVisible();
  await expect(page.getByTestId('statement-row')).toHaveCount(0);
});

test(ac('WEB05-AC9', 'KPI cards are present'), async ({ loggedIn: page }) => {
  await gotoStatement(page);

  for (const id of ['kpi-money', 'kpi-expenses', 'kpi-earnings']) {
    await expect(page.getByTestId(id), `${id} should be visible`).toBeVisible();
  }
});

// ---------------------------------------------------------------------------
// fullstack-03-statement — the same screen, over the candidate's own API
// ---------------------------------------------------------------------------

test(ac('FS03-AC2', 'The UI satisfies the web criteria against that API'), async ({
  loggedIn: page,
}) => {
  await gotoStatement(page);
  await expect(page.getByTestId('statement-table').or(page.getByTestId('statement-empty'))).toBeVisible();
});

test(ac('FS03-AC5', 'Pagination is consistent across the stack'), async ({
  loggedIn: page,
}) => {
  await gotoStatement(page);

  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/statements') && r.status() === 200),
    page.getByTestId('pagination-next').click(),
  ]);

  const rows = await response.json();
  await expect(
    page.getByTestId('statement-row'),
    'the rendered rows must match what the API returned for that page'
  ).toHaveCount(rows.length);
});
