import { test, expect } from '@playwright/test';

const LOCALES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'de', 'es', 'fr', 'pt', 'ru'];
const ARTICLES = [
  {
    slug: 'mediatek-mt7921au-linux-in-kernel-driver-awus036axml',
    title: 'MediaTek',
  },
  {
    slug: 'macos-acs-acr1252u-m1-web-nfc-apdu-guide',
    title: 'macOS',
  },
  {
    slug: 'jetson-orin-nano-wifi-6e-6ghz-high-bandwidth-streaming',
    title: 'Jetson',
  },
  {
    slug: 'vm-kali-linux-usb-passthrough-troubleshooting-guide',
    title: 'Virtual',
  },
];

const PAGES: string[] = [];
for (const locale of LOCALES) {
  for (const article of ARTICLES) {
    PAGES.push(`/${locale.toLowerCase()}/blog/${article.slug}/`);
  }
}

test.describe('4 ALFA New Blog Articles 10-Locale Quality & Image Audit', () => {
  for (const route of PAGES) {
    test(`Audit ${route}`, async ({ page }) => {
      // Monitor console errors
      const consoleErrors: string[] = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });

      // Navigate to route
      const res = await page.goto(route);
      expect(res?.status()).toBe(200);

      // Wait for network idle
      await page.waitForLoadState('networkidle');

      // Verify no critical console errors
      expect(consoleErrors).toEqual([]);

      // Verify page has a meaningful title
      const title = await page.title();
      expect(title.length).toBeGreaterThan(5);

      // Verify body has meaningful content
      const bodyText = await page.innerText('body');
      expect(bodyText.length).toBeGreaterThan(100);

      // Scroll to bottom to trigger lazy-loaded images
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(500);

      // Check all images on this page load correctly and are not broken
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

      // Check at least 1 image is present
      const imgCount = await page.locator('img').count();
      expect(imgCount).toBeGreaterThanOrEqual(1);

      // Check hreflang alternates exist
      const hreflangCount = await page.locator('link[rel="alternate"][hreflang]').count();
      expect(hreflangCount).toBeGreaterThanOrEqual(5);
    });
  }
});
