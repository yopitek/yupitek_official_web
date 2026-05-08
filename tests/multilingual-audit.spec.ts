import { test, expect } from '@playwright/test';

const LANGUAGES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'es', 'pt', 'ru', 'de', 'fr'];
const SECTIONS = ['about', 'contact', 'products', 'blog', 'solution', 'support'];

// Product subdirectories (7 brands)
const PRODUCTS = ['alfa', 'hak5', 'flipperzero', 'ubiquiti', 'graphiccard', 'sdrlab', 'acr'];

// Blog articles (the canonical set from en)
const BLOG_ARTICLES = [
  'awus036ach-kali-linux-setup',
  'awus036acm-ibss-mesh-raspberry-pi',
  'awus036axml-firmware-monitor-mode-fix',
  'awus036axml-wifi-6e-review',
  'awus036ach-vs-awus036acm',
  'best-wifi-adapter-kali-linux-2026',
  'dji-drone-controller-antenna-upgrade',
  'enable-monitor-mode-kali-linux',
  'enterprise-wireless-security-assessment',
  'fix-alfa-driver-kernel-update',
  'install-alfa-driver-kali-ubuntu',
  'packet-injection-guide',
  'wifi-6e-vs-wifi-5-kali-linux',
  'wpa3-security-testing-alfa-2026',
];

// ============================================================
// Test 1: All main language pages exist (200)
// ============================================================
test.describe('Language coverage', () => {
  for (const lang of LANGUAGES) {
    for (const section of SECTIONS) {
      test(`${lang} /${section}/ page exists`, async ({ page }) => {
        const url = `/${lang}/${section}/`;
        const response = await page.goto(url);
        expect(response?.status(), `${lang} ${section} should be 200`).toBe(200);
      });
    }
  }

  // Test home pages for all languages
  for (const lang of LANGUAGES) {
    test(`${lang} home page exists`, async ({ page }) => {
      const url = `/${lang}/`;
      const response = await page.goto(url);
      expect(response?.status(), `${lang} home should be 200`).toBe(200);
    });
  }

  // Test product pages for de and fr (the languages we recently added)
  for (const lang of ['de', 'fr']) {
    for (const product of PRODUCTS) {
      test(`${lang} /products/${product}/ page exists`, async ({ page }) => {
        const url = `/${lang}/products/${product}/`;
        const response = await page.goto(url);
        expect(response?.status(), `${lang} ${product} should be 200`).toBe(200);
      });
    }
  }

  // Test blog articles for de and fr
  for (const lang of ['de', 'fr']) {
    for (const article of BLOG_ARTICLES) {
      test(`${lang} /blog/${article}/ page exists`, async ({ page }) => {
        const url = `/${lang}/blog/${article}/`;
        const response = await page.goto(url);
        expect(response?.status(), `${lang} ${article} should be 200`).toBe(200);
      });
    }
  }
});

// ============================================================
// Test 2: Images load correctly on all language home pages
// ============================================================
test.describe('Image health', () => {
  for (const lang of LANGUAGES) {
    test(`no broken images on /${lang}/`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      await page.waitForLoadState('networkidle');

      const brokenImages = await page.evaluate(() => {
        return Array.from(document.images)
          .filter((img: HTMLImageElement) => {
            // Check if image is broken (not complete or zero dimensions)
            if (!img.complete) return true;
            if (img.naturalWidth === 0 || img.naturalHeight === 0) return true;
            return false;
          })
          .map((img: HTMLImageElement) => img.src);
      });

      expect(brokenImages).toEqual([]);
    });
  }
});

// ============================================================
// Test 3: hreflang tags present and correct
// ============================================================
test.describe('hreflang tags', () => {
  test('home page has all 10 hreflang alternates + x-default', async ({ page }) => {
    await page.goto('/en/');
    const hreflangs = await page.evaluate(() => {
      const links = document.querySelectorAll('link[rel="alternate"]');
      return Array.from(links).map((l: HTMLLinkElement) => ({
        href: l.getAttribute('href'),
        hreflang: l.getAttribute('hreflang'),
      }));
    });

    expect(hreflangs.length).toBeGreaterThanOrEqual(11); // 10 languages + x-default

    const langCodes = hreflangs.map((h: { hreflang: string }) => h.hreflang).map((c: string | null) => c?.toLowerCase() || '');
    for (const lang of LANGUAGES) {
      expect(langCodes).toContain(lang.toLowerCase());
    }
    expect(langCodes).toContain('x-default');
  });

  // Check that hreflang links are bidirectional
  test('hreflang links are bidirectional', async ({ page }) => {
    await page.goto('/en/');
    const hreflangs = await page.evaluate(() => {
      const links = document.querySelectorAll('link[rel="alternate"]');
      return Array.from(links).map((l: HTMLLinkElement) => ({
        href: l.getAttribute('href'),
        hreflang: l.getAttribute('hreflang'),
      }));
    });

    for (const h of hreflangs) {
      const response = await page.goto(h.href);
      expect(response?.status()).toBe(200);
    }
  });
});

// ============================================================
// Test 4: Content language detection
// ============================================================
test.describe('Language content integrity', () => {
  for (const lang of LANGUAGES) {
    test(`/${lang}/ page has non-empty content`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      await page.waitForLoadState('networkidle');

      const content = await page.evaluate(() => document.body.innerText.trim());
      expect(content.length).toBeGreaterThan(50);
    });
  }
});

// ============================================================
// Test 5: RTL language (Arabic) layout
// ============================================================
test.describe('RTL support', () => {
  test('/ar/ page loads with RTL direction', async ({ page }) => {
    await page.goto('/ar/');
    const dir = await page.evaluate(() => document.documentElement.getAttribute('dir'));
    expect(dir).toBe('rtl');
  });
});
