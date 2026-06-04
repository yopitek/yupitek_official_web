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

      // Model-specific software & protocol checks
      if (route.includes('/ypb01/')) {
        // YPB01 should use BeaconSET
        expect(pageText).toContain('BeaconSET');
        // YPB01 should NOT use BeaconSET+ in its operational/config guidance text
        // (We check the config guidance section specifically)
        const configText = await page.locator('body').innerText();
        // Ensure no BeaconSET+ in configuration section
        const configIndex = configText.indexOf('BeaconSET');
        if (configIndex !== -1) {
          const sectionText = configText.slice(configIndex, configIndex + 500);
          expect(sectionText).not.toContain('BeaconSET+');
        }
      } else if (route.includes('/ypb02/') || route.includes('/ypb04/') || route.includes('/ypb05/')) {
        // YPB02, YPB04, YPB05 should use BeaconSET+
        expect(pageText).toContain('BeaconSET+');
      } else if (route.includes('/ypb03/')) {
        // YPB03 should be a LINE Beacon and mention FE6F
        expect(pageText).toContain('LINE Beacon');
        expect(pageText).toContain('0xFE6F');
      }

      // Check localization: non-English pages should have translated content and not fall back to English body paragraphs
      if (!route.startsWith('/en/')) {
        // Check that common English body text strings do not leak
        expect(pageText).not.toContain('Simultaneous Broadcasts');
        expect(pageText).not.toContain('How to Turn the Beacon ON');
        expect(pageText).not.toContain('Key Features');
        expect(pageText).not.toContain('Operational Guide');
        expect(pageText).not.toContain('Configuration Guidance');
      }

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
    // Wait for the link to be attached in the document using robust assertion
    const link = page.locator('a[href="/en/products/ibeacon/"]').first();
    await expect(link).toBeAttached();
  });
});
