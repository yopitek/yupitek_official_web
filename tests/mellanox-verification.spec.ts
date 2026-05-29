import { test, expect } from '@playwright/test';

const PAGES = [
  '/en/products/mellanox/',
  '/en/products/mellanox/nic/',
  '/en/products/mellanox/dpu/',
  '/en/products/mellanox/transceiver/',
  '/en/products/mellanox/cable-dac/',
  '/en/products/mellanox/cable-aoc/',
  '/en/products/mellanox/cable-fiber/',
  '/en/products/mellanox/switch/'
];

test.describe('Mellanox Pages Quality Audit', () => {
  for (const route of PAGES) {
    test(`Audit ${route}`, async ({ page }) => {
      // Monitor console errors and network requests
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

      // Verify no literal ":::carousel" text is visible on the page
      const pageText = await page.innerText('body');
      expect(pageText).not.toContain(':::carousel');
      expect(pageText).not.toContain('<!-- slide -->');

      // Verify Mellanox selector widget is completely removed
      const selectorElement = await page.$('#mellanox-selector-root');
      expect(selectorElement).toBeNull();

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

  test('Verify homepage brand table links are correct', async ({ page }) => {
    await page.goto('/en/');
    const link = await page.locator('a[href="/en/products/mellanox/"]');
    await expect(link).toBeVisible();
  });
});
