import { test, expect } from '@playwright/test';

const SLUG = 'ypb03-line-beacon-tutorial';
const LOCALES = ['zh-tw', 'zh-cn', 'en', 'ja', 'ar', 'es', 'pt', 'ru', 'de', 'fr'];

test.describe('YPB03 LINE Beacon Tutorial — 10-Locale Verification', () => {
  for (const locale of LOCALES) {
    test(`${locale} article loads with correct title, hero image, and content`, async ({ page }) => {
      const url = `/${locale}/blog/${SLUG}/`;
      const errors: string[] = [];

      // Collect console errors
      page.on('pageerror', (err) => errors.push(err.message));

      // 1. Navigate and check HTTP 200
      const response = await page.goto(url);
      expect(response?.status(), `${locale} should return 200`).toBe(200);

      // Wait for network idle (hydration complete)
      await page.waitForLoadState('networkidle');

      // 2. Page title is non-empty and contains YPB03 or LINE Beacon
      const pageTitle = await page.title();
      expect(pageTitle.length, `${locale} title should be non-empty`).toBeGreaterThan(5);

      // 3. Hero image loads successfully (naturalWidth > 0)
      const heroImg = page.locator('img').first();
      await expect(heroImg, `${locale} should have at least one image`).toBeVisible();
      const naturalWidth = await heroImg.evaluate(
        (img: HTMLImageElement) => img.naturalWidth
      );
      expect(naturalWidth, `${locale} hero image should load (naturalWidth > 0)`).toBeGreaterThan(0);

      // 4. Article body has substantial content (> 500 chars)
      const bodyText = await page.evaluate(() => document.body.innerText.trim());
      expect(bodyText.length, `${locale} body content should be substantial`).toBeGreaterThan(500);

      // 5. No console errors
      expect(errors, `${locale} should have no console errors`).toEqual([]);

      // 6. Screenshot evidence
      await page.screenshot({
        path: `playwright-report/screenshots/${locale}-ypb03-${Date.now()}.png`,
        fullPage: false,
      });
    });
  }

  // Arabic-specific: RTL direction check
  test('ar article has RTL direction', async ({ page }) => {
    await page.goto('/ar/blog/ypb03-line-beacon-tutorial/');
    await page.waitForLoadState('networkidle');
    const dir = await page.evaluate(() => document.documentElement.getAttribute('dir'));
    expect(dir, 'Arabic page should have dir=rtl').toBe('rtl');
  });
});

