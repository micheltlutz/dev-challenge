import { defineConfig, devices } from '@playwright/test';

/**
 * Points at the *candidate's* front-end, not at anything in this repository.
 *
 *   BASE_URL=http://localhost:5173 npx playwright test
 *
 * DC_API_URL should point at the API that front-end talks to, so the harness
 * can cross-check what the screen renders against what the API returned.
 */
export default defineConfig({
  testDir: '.',
  testMatch: '*.spec.ts',
  timeout: 30_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  retries: process.env.CI ? 1 : 0,
  reporter: [
    ['list'],
    ['json', { outputFile: '../../../.harness-ui-report.json' }],
  ],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 1024 } } },
  ],
});
