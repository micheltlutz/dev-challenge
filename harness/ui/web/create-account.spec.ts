import { test, expect, ac } from './support/ac';

// web-02-create-account

const PASSWORD = 'HarnessPw@123';

function freshEmail() {
  return `harness-${Date.now()}-${Math.floor(Math.random() * 1e4)}@example.com`;
}

async function fillForm(page, overrides: Record<string, string> = {}) {
  const data = {
    firstname: 'Ada',
    lastname: 'Lovelace',
    email: freshEmail(),
    password: PASSWORD,
    confirm: PASSWORD,
    birthdate: '1815-12-10',
    ...overrides,
  };
  await page.getByTestId('signup-firstname').fill(data.firstname);
  await page.getByTestId('signup-lastname').fill(data.lastname);
  await page.getByTestId('signup-email').fill(data.email);
  await page.getByTestId('signup-password').fill(data.password);
  await page.getByTestId('signup-confirm-password').fill(data.confirm);
  await page.getByTestId('signup-birthdate').fill(data.birthdate);
  return data;
}

test(ac('WEB02-AC1', 'Form renders every designed field'), async ({ page }) => {
  await page.goto('/signup');

  for (const id of [
    'signup-firstname',
    'signup-lastname',
    'signup-email',
    'signup-password',
    'signup-confirm-password',
    'signup-birthdate',
    'signup-submit',
  ]) {
    await expect(page.getByTestId(id), `${id} should be visible`).toBeVisible();
  }
});

test(ac('WEB02-AC2', 'Password confirmation is enforced'), async ({ page }) => {
  await page.goto('/signup');
  await fillForm(page, { confirm: 'something-else' });

  let requestSent = false;
  page.on('request', (r) => {
    if (r.url().includes('/users') && r.method() === 'POST') requestSent = true;
  });

  await page.getByTestId('signup-submit').click();
  await page.waitForTimeout(500);

  expect(requestSent, 'mismatched passwords must not reach the API').toBe(false);
});

test(ac('WEB02-AC3', 'Valid submission registers the user'), async ({ page }) => {
  await page.goto('/signup');
  const data = await fillForm(page);

  const [request] = await Promise.all([
    page.waitForRequest((r) => r.url().includes('/users') && r.method() === 'POST'),
    page.getByTestId('signup-submit').click(),
  ]);

  const body = request.postDataJSON();
  expect(body.userid).toBe(data.email);
  expect(body.fullname, 'fullname should be "<First name> <Last Name>"').toBe(
    `${data.firstname} ${data.lastname}`
  );
  expect(body.birthdate, 'birthdate must be ISO YYYY-MM-DD').toMatch(/^\d{4}-\d{2}-\d{2}$/);
});

test(ac('WEB02-AC4', 'Success routes the user onward'), async ({ page }) => {
  await page.goto('/signup');
  await fillForm(page);
  await page.getByTestId('signup-submit').click();

  const success = page.getByTestId('signup-success');
  const login = page.getByTestId('login-submit');
  await expect(
    success.or(login),
    'after a 201 the app should confirm success or navigate to login'
  ).toBeVisible({ timeout: 15_000 });
});

test(ac('WEB02-AC5', 'Duplicate e-mail is surfaced'), async ({ page }) => {
  await page.route('**/users**', (route) =>
    route.request().method() === 'POST'
      ? route.fulfill({
          status: 400,
          contentType: 'application/json',
          body: JSON.stringify({ detail: 'Username already registered' }),
        })
      : route.continue()
  );

  await page.goto('/signup');
  await fillForm(page);
  await page.getByTestId('signup-submit').click();

  await expect(page.getByTestId('signup-error')).toBeVisible();
});

test(ac('WEB02-AC6', 'Design tokens are respected'), async ({ page }) => {
  await page.goto('/signup');

  const background = await page
    .getByTestId('signup-submit')
    .evaluate((el) => getComputedStyle(el as Element).backgroundColor);

  const match = background.match(/\d+/g)?.map(Number) ?? [];
  expect(match.length, `could not read a colour from ${background}`).toBeGreaterThanOrEqual(3);

  const [r, g, b] = match;
  // --color-action-default is #19191C. Allow a wide tolerance for hover states
  // and slight palette adjustments, but reject anything that is not near-black.
  const isNearBlack = r < 70 && g < 70 && b < 80;
  expect(
    isNearBlack,
    `the primary button should use --color-action-default (#19191C), got rgb(${r}, ${g}, ${b}). ` +
      'A purple button is the most common mistake here -- purple is for brand surfaces, not actions.'
  ).toBe(true);
});

test(ac('WEB02-AC7', 'There is a route to the login screen'), async ({ page }) => {
  await page.goto('/signup');
  await page.getByTestId('link-login').click();

  await expect(page.getByTestId('login-submit')).toBeVisible({ timeout: 15_000 });
});
