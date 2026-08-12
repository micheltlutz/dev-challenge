import { test, expect, ac } from './support/ac';

// web-04-dashboard

test(ac('WEB04-AC1', 'Shell renders for an authenticated user'), async ({
  loggedIn: page,
}) => {
  await expect(page.getByTestId('app-shell')).toBeVisible();
  await expect(page.getByTestId('sidebar')).toBeVisible();
  await expect(page.getByTestId('topbar')).toBeVisible();
});

test(ac('WEB04-AC2', 'Navigation exposes the three real destinations'), async ({
  loggedIn: page,
}) => {
  for (const id of ['nav-home', 'nav-statement', 'nav-profile']) {
    await expect(page.getByTestId(id), `${id} should be present`).toBeVisible();
  }
});

test(ac('WEB04-AC3', 'The active item is marked'), async ({ loggedIn: page }) => {
  const home = page.getByTestId('nav-home');
  const profile = page.getByTestId('nav-profile');

  const signature = async (locator) =>
    locator.evaluate((el: Element) => {
      const style = getComputedStyle(el);
      return [el.className, el.getAttribute('aria-current'), style.color, style.backgroundColor].join('|');
    });

  expect(
    await signature(home),
    'the active nav item must be visually distinguishable from an inactive one'
  ).not.toBe(await signature(profile));
});

test(ac('WEB04-AC4', 'Navigation moves between routes'), async ({ loggedIn: page }) => {
  const before = page.url();
  await page.getByTestId('nav-statement').click();

  await expect(page).not.toHaveURL(before);
  await expect(
    page.getByTestId('app-shell'),
    'the shell should persist across navigation'
  ).toBeVisible();
});

test(ac('WEB04-AC5', 'Unauthenticated access is blocked'), async ({ page }) => {
  await page.goto('/login');
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
  await page.context().clearCookies();

  await page.goto('/home');

  await expect(
    page.getByTestId('login-submit'),
    'the dashboard must redirect to login without a session'
  ).toBeVisible({ timeout: 15_000 });
});

test(ac('WEB04-AC6', 'Logout ends the session'), async ({ loggedIn: page }) => {
  await page.getByTestId('logout').click();

  await expect(page.getByTestId('login-submit')).toBeVisible({ timeout: 15_000 });

  const leftovers = await page.evaluate(() =>
    [...Object.values(localStorage), ...Object.values(sessionStorage)].join(' ')
  );
  expect(/eyJ[\w-]+\.[\w-]+\.[\w-]+/.test(leftovers)).toBe(false);
});

test(ac('WEB04-AC7', 'Welcome content matches the design'), async ({ loggedIn: page }) => {
  await expect(page.getByTestId('welcome-heading')).toBeVisible();
  await expect(page.getByTestId('welcome-heading')).toHaveText(/welcome to my statement/i);
});
