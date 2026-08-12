import { test, expect, ac } from './support/ac';

// web-01-contact-form / fullstack-01-contact

const VALID = {
  name: 'Ada Lovelace',
  email: 'ada@example.com',
  interest: 'Back-end',
  message: 'I would like to know more about the project.',
};

async function fillForm(page, overrides: Partial<typeof VALID> = {}) {
  const data = { ...VALID, ...overrides };
  await page.getByTestId('contact-name').fill(data.name);
  await page.getByTestId('contact-email').fill(data.email);
  await page.getByTestId('contact-interest').fill(data.interest);
  await page.getByTestId('contact-message').fill(data.message);
  return data;
}

test(ac('WEB01-AC1', 'Form renders all fields'), async ({ page }) => {
  await page.goto('/contact');

  for (const id of [
    'contact-name',
    'contact-email',
    'contact-interest',
    'contact-message',
    'contact-submit',
  ]) {
    await expect(page.getByTestId(id), `${id} should be visible`).toBeVisible();
  }
});

test(ac('WEB01-AC2', 'Empty submission is blocked client-side'), async ({ page }) => {
  await page.goto('/contact');

  let requestSent = false;
  page.on('request', (r) => {
    if (r.url().includes('/contact') && r.method() === 'POST') requestSent = true;
  });

  await page.getByTestId('contact-submit').click();
  await page.waitForTimeout(500);

  expect(requestSent, 'an empty form must not reach the API').toBe(false);
});

test(ac('WEB01-AC3', 'Invalid e-mail is flagged'), async ({ page }) => {
  await page.goto('/contact');
  await fillForm(page, { email: 'not-an-email' });

  let requestSent = false;
  page.on('request', (r) => {
    if (r.url().includes('/contact') && r.method() === 'POST') requestSent = true;
  });

  await page.getByTestId('contact-submit').click();
  await page.waitForTimeout(500);

  expect(requestSent, 'a malformed e-mail must not reach the API').toBe(false);
});

test(ac('WEB01-AC4', 'Valid submission calls the API'), async ({ page }) => {
  await page.goto('/contact');
  const data = await fillForm(page);

  const [request] = await Promise.all([
    page.waitForRequest((r) => r.url().includes('/contact') && r.method() === 'POST'),
    page.getByTestId('contact-submit').click(),
  ]);

  const body = request.postDataJSON();
  expect(body.name).toBe(data.name);
  expect(body.email).toBe(data.email);
  expect(body.message).toBe(data.message);
  expect(body.interest).toBe(data.interest);
});

test(ac('WEB01-AC5', 'Success state is shown'), async ({ page }) => {
  await page.goto('/contact');
  await fillForm(page);
  await page.getByTestId('contact-submit').click();

  await expect(page.getByTestId('contact-success')).toBeVisible();
});

test(ac('WEB01-AC6', 'Failure state is shown'), async ({ page }) => {
  await page.route('**/contact*', (route) =>
    route.fulfill({ status: 422, body: JSON.stringify({ detail: 'nope' }) })
  );

  await page.goto('/contact');
  const data = await fillForm(page);
  await page.getByTestId('contact-submit').click();

  await expect(page.getByTestId('contact-error')).toBeVisible();
  await expect(
    page.getByTestId('contact-message'),
    'the entered data must survive a failed submission'
  ).toHaveValue(data.message);
});

// fullstack-01-contact — the same form, over the candidate's own API
test(ac('FS01-AC2', 'The UI satisfies the web criteria against that API'), async ({
  page,
}) => {
  await page.goto('/contact');
  const data = await fillForm(page);

  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/contact') && r.request().method() === 'POST'),
    page.getByTestId('contact-submit').click(),
  ]);

  expect(
    response.status(),
    "the candidate's own API should accept the submission its own UI sends"
  ).toBe(200);
  await expect(page.getByTestId('contact-success')).toBeVisible();
  expect((await response.json()).msg).toContain(data.name);
});

test(ac('WEB01-AC7', 'Double submission is prevented'), async ({ page }) => {
  await page.route('**/contact*', async (route) => {
    await new Promise((r) => setTimeout(r, 1500));
    await route.fulfill({ status: 200, body: JSON.stringify({ msg: 'Thank Ada Lovelace' }) });
  });

  await page.goto('/contact');
  await fillForm(page);

  let requests = 0;
  page.on('request', (r) => {
    if (r.url().includes('/contact') && r.method() === 'POST') requests += 1;
  });

  await page.getByTestId('contact-submit').click();
  await page.getByTestId('contact-submit').click({ force: true });
  await page.waitForTimeout(2000);

  expect(requests, 'the submit control must be disabled while in flight').toBe(1);
});
