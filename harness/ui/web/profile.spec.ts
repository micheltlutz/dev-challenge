import { test, expect, ac } from './support/ac';

// web-06-profile-edit

async function gotoProfile(page) {
  await page.getByTestId('nav-profile').click();
  await expect(page.getByTestId('profile-form')).toBeVisible({ timeout: 15_000 });
}

test(ac('WEB06-AC1', 'Form is prefilled'), async ({ loggedIn: page }) => {
  await gotoProfile(page);

  for (const id of ['profile-firstname', 'profile-lastname', 'profile-email']) {
    await expect(
      page.getByTestId(id),
      `${id} should be prefilled with the current profile`
    ).not.toHaveValue('');
  }
});

test(ac('WEB06-AC2', 'E-mail is not editable'), async ({ loggedIn: page }) => {
  await gotoProfile(page);

  const email = page.getByTestId('profile-email');
  const locked = await email.evaluate(
    (el: Element) =>
      (el as HTMLInputElement).readOnly || (el as HTMLInputElement).disabled
  );

  expect(locked, 'userid cannot be changed, so the e-mail field must be read-only').toBe(
    true
  );
});

test(ac('WEB06-AC3', 'Save is disabled until something changes'), async ({
  loggedIn: page,
}) => {
  await gotoProfile(page);

  await expect(page.getByTestId('profile-save')).toBeDisabled();
});

test(ac('WEB06-AC4', 'Saving persists the change'), async ({ loggedIn: page }) => {
  await gotoProfile(page);
  await page.getByTestId('profile-firstname').fill('Renamed');

  const [request] = await Promise.all([
    page.waitForRequest((r) => /\/users\/\d+/.test(r.url()) && r.method() === 'PUT'),
    page.getByTestId('profile-save').click(),
  ]);

  const body = request.postDataJSON();
  expect(body.fullname, 'fullname should be the joined first and last name').toMatch(
    /^Renamed\s+\S+/
  );
});

test(ac('WEB06-AC5', 'Success is confirmed and reflected'), async ({ loggedIn: page }) => {
  await gotoProfile(page);
  await page.getByTestId('profile-firstname').fill('Confirmed');
  await page.getByTestId('profile-save').click();

  await expect(page.getByTestId('profile-success')).toBeVisible({ timeout: 15_000 });
});

test(ac('WEB06-AC6', 'The change survives a reload'), async ({ loggedIn: page }) => {
  const name = `Persisted${Math.floor(Math.random() * 1e4)}`;

  await gotoProfile(page);
  await page.getByTestId('profile-firstname').fill(name);
  await page.getByTestId('profile-save').click();
  await expect(page.getByTestId('profile-success')).toBeVisible({ timeout: 15_000 });

  await page.reload();
  await expect(page.getByTestId('profile-form')).toBeVisible({ timeout: 15_000 });

  await expect(page.getByTestId('profile-firstname')).toHaveValue(name);
});

test(ac('WEB06-AC7', 'Out-of-scope fields do not pretend to save'), async ({
  loggedIn: page,
}) => {
  await gotoProfile(page);
  await page.getByTestId('profile-firstname').fill('ScopeCheck');

  const [request] = await Promise.all([
    page.waitForRequest((r) => /\/users\/\d+/.test(r.url()) && r.method() === 'PUT'),
    page.getByTestId('profile-save').click(),
  ]);

  const body = request.postDataJSON();
  for (const unsupported of ['address', 'country', 'countries', 'avatar']) {
    expect(
      Object.keys(body).map((k) => k.toLowerCase()),
      `the API does not support "${unsupported}"; sending it pretends it saves`
    ).not.toContain(unsupported);
  }
});
