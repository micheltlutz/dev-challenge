import { test, expect, ac } from './support/ac';

// web-03-login / fullstack-02-auth

const USERID = process.env.DC_USERID ?? 'john.doe@email.com';
const PASSWORD = process.env.DC_PASSWORD ?? 'Challenge@123';

test(ac('WEB03-AC1', 'Form renders'), async ({ page }) => {
  await page.goto('/login');

  await expect(page.getByTestId('login-email')).toBeVisible();
  await expect(page.getByTestId('login-password')).toBeVisible();
  await expect(page.getByTestId('login-submit')).toBeVisible();
});

test(ac('WEB03-AC2', 'Valid credentials authenticate'), async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(USERID);
  await page.getByTestId('login-password').fill(PASSWORD);

  const [request] = await Promise.all([
    page.waitForRequest((r) => r.url().includes('/auth') && r.method() === 'POST'),
    page.getByTestId('login-submit').click(),
  ]);

  const body = request.postDataJSON();
  expect(body.userid).toBe(USERID);
  expect(body.password).toBe(PASSWORD);
});

test(ac('WEB03-AC3', 'Token is persisted'), async ({ loggedIn: page }) => {
  const stored = await page.evaluate(() => {
    const buckets = [
      ...Object.values(localStorage),
      ...Object.values(sessionStorage),
    ];
    return buckets.join(' ');
  });
  const cookies = (await page.context().cookies()).map((c) => c.value).join(' ');

  expect(
    /eyJ[\w-]+\.[\w-]+\.[\w-]+/.test(stored + ' ' + cookies),
    'a JWT should be stored in localStorage, sessionStorage or a cookie'
  ).toBe(true);

  await page.reload();
  await expect(
    page.getByTestId('app-shell'),
    'the session should survive a reload'
  ).toBeVisible();
});

test(ac('WEB03-AC4', 'Success navigates to the dashboard'), async ({ loggedIn: page }) => {
  await expect(page.getByTestId('app-shell')).toBeVisible();
});

test(ac('WEB03-AC5', 'Bad credentials show an error'), async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(USERID);
  await page.getByTestId('login-password').fill('definitely-wrong');
  await page.getByTestId('login-submit').click();

  await expect(page.getByTestId('login-error')).toBeVisible();
  await expect(
    page.getByTestId('app-shell'),
    'a failed login must not navigate into the app'
  ).toHaveCount(0);
});

test(ac('WEB03-AC6', 'Protected requests carry the Bearer token'), async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('login-email').fill(USERID);
  await page.getByTestId('login-password').fill(PASSWORD);
  await page.getByTestId('login-submit').click();

  const request = await page.waitForRequest(
    (r) => /\/(balance|statements|users)/.test(r.url()) && r.method() === 'GET',
    { timeout: 15_000 }
  );

  expect(
    request.headers()['authorization'] ?? '',
    'protected requests must send Authorization: Bearer <token>'
  ).toMatch(/^Bearer\s+eyJ/);
});

test(ac('WEB03-AC7', 'Expired or rejected sessions return to login'), async ({
  loggedIn: page,
}) => {
  await page.route('**/{balance,statements,users}**', (route) =>
    route.fulfill({ status: 401, body: JSON.stringify({ detail: 'Not authenticated' }) })
  );

  await page.reload();

  await expect(page.getByTestId('login-submit')).toBeVisible({ timeout: 15_000 });

  const leftovers = await page.evaluate(() =>
    [...Object.values(localStorage), ...Object.values(sessionStorage)].join(' ')
  );
  expect(
    /eyJ[\w-]+\.[\w-]+\.[\w-]+/.test(leftovers),
    'a rejected session must clear the stored token'
  ).toBe(false);
});

// ---------------------------------------------------------------------------
// fullstack-02-auth — the same flow, owned end to end
// ---------------------------------------------------------------------------

test(ac('FS02-AC2', 'The UI satisfies the web criteria against that API'), async ({
  loggedIn: page,
}) => {
  await expect(page.getByTestId('app-shell')).toBeVisible();
});

test(ac('FS02-AC3', 'Register-then-login works end to end'), async ({ page }) => {
  const email = `harness-${Date.now()}@example.com`;
  const password = 'HarnessPw@123';

  await page.goto('/signup');
  await page.getByTestId('signup-firstname').fill('Harness');
  await page.getByTestId('signup-lastname').fill('Runner');
  await page.getByTestId('signup-email').fill(email);
  await page.getByTestId('signup-password').fill(password);
  await page.getByTestId('signup-confirm-password').fill(password);
  await page.getByTestId('signup-birthdate').fill('1990-05-17');
  await page.getByTestId('signup-submit').click();

  await page.goto('/login');
  await page.getByTestId('login-email').fill(email);
  await page.getByTestId('login-password').fill(password);
  await page.getByTestId('login-submit').click();

  await expect(page.getByTestId('app-shell')).toBeVisible({ timeout: 15_000 });
});

test(ac('FS02-AC4', 'Protected routes are guarded'), async ({ page }) => {
  await page.context().clearCookies();
  await page.goto('/login');
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  await page.goto('/statement');

  await expect(
    page.getByTestId('login-submit'),
    'reaching a protected route without a session should land on login'
  ).toBeVisible({ timeout: 15_000 });
});

test(ac('FS02-AC6', 'Logout ends the session for real'), async ({ loggedIn: page }) => {
  await page.getByTestId('logout').click();

  await expect(page.getByTestId('login-submit')).toBeVisible({ timeout: 15_000 });

  const leftovers = await page.evaluate(() =>
    [...Object.values(localStorage), ...Object.values(sessionStorage)].join(' ')
  );
  expect(
    /eyJ[\w-]+\.[\w-]+\.[\w-]+/.test(leftovers),
    'logout must remove the stored token'
  ).toBe(false);

  await page.goto('/statement');
  await expect(page.getByTestId('login-submit')).toBeVisible({ timeout: 15_000 });
});
