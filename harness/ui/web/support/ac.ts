/**
 * Ties a Playwright test to the acceptance criterion it verifies.
 *
 * The ID is the same one the spec declares in `acceptance.md`, so a failure
 * points straight at the line of specification it violates -- and
 * `scripts/validate_specs.py` can prove that every criterion has a test.
 */
import { test as base, expect, Page } from '@playwright/test';

export { expect };

/** Wrap a test title with its criterion id: `ac('WEB03-AC1')` */
export function ac(id: string, title: string): string {
  return `${id} — ${title}`;
}

export const test = base.extend<{
  /** Log in through the UI and land on an authenticated page. */
  loggedIn: Page;
}>({
  loggedIn: async ({ page, baseURL }, use) => {
    const userid = process.env.DC_USERID ?? 'john.doe@email.com';
    const password = process.env.DC_PASSWORD ?? 'Challenge@123';

    await page.goto(`${baseURL}/login`);
    await page.getByTestId('login-email').fill(userid);
    await page.getByTestId('login-password').fill(password);
    await page.getByTestId('login-submit').click();

    await expect(
      page.getByTestId('app-shell'),
      'after a successful login the authenticated shell should be visible'
    ).toBeVisible({ timeout: 15_000 });

    await use(page);
  },
});

/** The API the UI under test talks to, for seeding and cross-checking. */
export const apiBase = process.env.DC_API_URL ?? 'http://localhost:8000';

/** Strip everything but digits, a sign and a decimal point. */
export function toNumber(text: string | null): number {
  if (!text) return NaN;
  const cleaned = text.replace(/[^0-9.,\-+]/g, '').replace(/,/g, '');
  return parseFloat(cleaned);
}

/** True when the text looks masked rather than numeric. */
export function looksMasked(text: string | null): boolean {
  if (!text) return false;
  return !/\d/.test(text);
}
