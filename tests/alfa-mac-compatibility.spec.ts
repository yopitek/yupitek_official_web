import { test, expect } from '@playwright/test';

const LANGUAGES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'es', 'pt', 'ru', 'de', 'fr'];
const ARTICLE_SLUG = 'alfa-wireless-card-apple-mac-compatibility';

test.describe('macOS ALFA Wireless Card Compatibility Article', () => {
  for (const lang of LANGUAGES) {
    test(`${lang} version loads successfully and has content`, async ({ page }) => {
      const url = `/${lang}/blog/${ARTICLE_SLUG}/`;
      const response = await page.goto(url);
      
      // Assert HTTP status is 200
      expect(response?.status(), `${lang} article page should return 200`).toBe(200);
      
      // Assert non-empty title
      const title = await page.title();
      expect(title.length).toBeGreaterThan(10);
      
      // Assert page contains core content (e.g. ALFA or Mac)
      const bodyText = await page.innerText('body');
      expect(bodyText.length).toBeGreaterThan(100);
      
      // Specific checks
      if (lang === 'ar') {
        const dir = await page.evaluate(() => document.documentElement.getAttribute('dir'));
        expect(dir).toBe('rtl');
      }
    });
  }
});
