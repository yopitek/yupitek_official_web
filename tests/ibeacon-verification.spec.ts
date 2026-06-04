import { test, expect } from '@playwright/test';

const LANGUAGES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'de', 'es', 'fr', 'pt', 'ru'];
const SUB_ROUTES = [
  'products/ibeacon/',
  'products/ibeacon/ypb01/',
  'products/ibeacon/ypb02/',
  'products/ibeacon/ypb03/',
  'products/ibeacon/ypb04/',
  'products/ibeacon/ypb05/'
];

const PAGES: string[] = [];
for (const lang of LANGUAGES) {
  for (const route of SUB_ROUTES) {
    PAGES.push(`/${lang}/${route}`);
  }
}

test.describe('iBeacon Pages Multi-Language Quality Audit', () => {
  for (const route of PAGES) {
    test(`Audit ${route}`, async ({ page }) => {
      // Monitor console errors
      const consoleErrors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });

      // Go to page
      const res = await page.goto(route);
      expect(res?.status()).toBe(200);

      // Wait for network idle
      await page.waitForLoadState('networkidle');

      // Verify no console errors
      expect(consoleErrors).toEqual([]);

      // Verify no Minew branding leakage on the page
      const pageText = await page.innerText('body');
      expect(pageText.toLowerCase()).not.toContain('minew');

      // Verify the simplified sales email CTA is present
      expect(pageText).toContain('sales@yupitek.com');

      // Scroll to bottom to trigger lazy-loaded images
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(1000);

      // Check all image loads on this page
      const brokenImages = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('img'))
          .filter((img: HTMLImageElement) => {
            if (!img.complete) return true;
            if (img.naturalWidth === 0 || img.naturalHeight === 0) return true;
            return false;
          })
          .map((img: HTMLImageElement) => img.src);
      });

      expect(brokenImages, `Broken images on ${route}: ${JSON.stringify(brokenImages)}`).toEqual([]);
    });
  }

  test('Verify dropdown menu item for iBeacon exists on English homepage', async ({ page }) => {
    await page.goto('/en/');
    const link = page.locator('a[href="/en/products/ibeacon/"]').first();
    expect(await link.count()).toBeGreaterThan(0);
  });
});
