import { test, expect } from '@playwright/test';

const LOCALES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'de', 'es', 'fr', 'pt', 'ru'];
const ARTICLES = [
  {
    slug: 'wfb-ng-long-range-link',
    title: 'wfb-ng', // partial title match
  },
  {
    slug: 'remote-id-detection-kit',
    title: 'Remote ID', // partial title match
  },
];

const PAGES: string[] = [];
for (const locale of LOCALES) {
  for (const article of ARTICLES) {
    PAGES.push(`/${locale.toLowerCase()}/blog/${article.slug}/`);
  }
}

test.describe('New Blog Articles Multi-Language Quality Audit', () => {
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

      // Verify page has a meaningful title
      const title = await page.title();
      expect(title.length).toBeGreaterThan(5);

      // Verify body has meaningful content
      const bodyText = await page.innerText('body');
      expect(bodyText.length).toBeGreaterThan(100);

      // Check locale-specific content
      const locale = route.split('/')[1];

      // zh-tw articles should contain 延伸閱讀 (cross-reference kept)
      if (locale === 'zh-tw') {
        expect(bodyText).toContain('延伸閱讀');
      } else if (locale === 'zh-cn') {
        // zh-cn (overseas simplified) should NOT have 延伸閱讀
        // But might have some translated reference section
        expect(bodyText).not.toContain('延伸閱讀');
      } else if (locale === 'en') {
        // English should have a "Further Reading" or similar section
        expect(bodyText).not.toContain('延伸閱讀');
      } else if (locale === 'ja') {
        // Japanese should NOT have 延伸閱讀
        expect(bodyText).not.toContain('延伸閱讀');
      }

      // Scroll to bottom to trigger lazy-loaded images
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(1000);

      // Check all images on this page load correctly
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

      // Check hreflang alternates exist (blog pages should have them)
      const hreflangCount = await page.locator('link[rel="alternate"][hreflang]').count();
      // Should have at least some hreflang entries
      expect(hreflangCount).toBeGreaterThanOrEqual(5);
    });
  }
});
