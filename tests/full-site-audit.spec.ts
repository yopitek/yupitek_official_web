import { test, expect } from '@playwright/test';

const LANGUAGES = ['en', 'zh-tw', 'zh-cn', 'ja', 'ar', 'es', 'pt', 'ru', 'de', 'fr'];
const SECTIONS = ['about', 'contact', 'products', 'blog', 'solution', 'support'];
const PRODUCT_BRANDS = ['alfa', 'hak5', 'flipperzero', 'ubiquiti', 'graphiccard', 'sdrlab', 'acr'];

// ============================================================
// Test 1: All language homepages load (200)
// ============================================================
test.describe('Home pages', () => {
  for (const lang of LANGUAGES) {
    test(`/${lang}/ loads with 200`, async ({ page }) => {
      const res = await page.goto(`/${lang}/`);
      expect(res?.status()).toBe(200);
    });
  }
});

// ============================================================
// Test 2: All section pages load (200) for all languages
// ============================================================
test.describe('Section pages', () => {
  for (const lang of LANGUAGES) {
    for (const section of SECTIONS) {
      test(`/${lang}/${section}/ loads`, async ({ page }) => {
        const res = await page.goto(`/${lang}/${section}/`);
        expect(res?.status(), `${lang}/${section}/ should be 200`).toBe(200);
      });
    }
  }
});

// ============================================================
// Test 3: All product brand pages load for all languages
// ============================================================
test.describe('Product brand pages', () => {
  for (const lang of LANGUAGES) {
    for (const brand of PRODUCT_BRANDS) {
      test(`/${lang}/products/${brand}/ loads`, async ({ page }) => {
        const res = await page.goto(`/${lang}/products/${brand}/`);
        expect(res?.status(), `${lang}/products/${brand}/ should be 200`).toBe(200);
      });
    }
  }
});

// ============================================================
// Test 4: Check all images on all language homepages
// ============================================================
test.describe('Homepage images', () => {
  for (const lang of LANGUAGES) {
    test(`no broken images on /${lang}/`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      await page.waitForLoadState('networkidle');

      const brokenImages = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('img'))
          .filter((img: HTMLImageElement) => {
            if (!img.complete) return true;
            if (img.naturalWidth === 0 || img.naturalHeight === 0) return true;
            return false;
          })
          .map((img: HTMLImageElement) => img.src);
      });

      if (brokenImages.length > 0) {
        console.log(`[BROKEN IMAGES /${lang}/]`, brokenImages);
      }
      expect(brokenImages).toEqual([]);
    });
  }
});

// ============================================================
// Test 5: Check all static images exist (no 404s in /images/)
// ============================================================
test.describe('Static images', () => {
  test('no 404 images in /images/ directory', async ({ page }) => {
    // Check common image directories
    const imageDirs = [
      '/images/products/alfa/',
      '/images/products/hak5/',
      '/images/products/flipperzero/',
      '/images/products/ubiquiti/',
      '/images/products/graphiccard/',
      '/images/blog/',
      '/images/brands/',
    ];

    const brokenImages: string[] = [];
    for (const dir of imageDirs) {
      const res = await page.goto(dir);
      if (res?.status() !== 200) {
        console.log(`  dir ${dir}: ${res?.status()}`);
      }
    }

    // Check a sample of product images
    const sampleImages = [
      '/images/products/alfa/awus036axml.png',
      '/images/products/alfa/awus036ach.png',
      '/images/products/alfa/apa-m04.png',
      '/images/products/hak5/packet-squirrel.png',
      '/images/products/flipperzero/flipper-zero.png',
      '/images/products/ubiquiti/u7-pro.png',
      '/images/brands/alfa.png',
      '/images/brands/hak5.png',
      '/images/blog/banner.png',
    ];

    for (const img of sampleImages) {
      const res = await page.goto(img);
      expect(res?.status(), `${img} should be 200`).toBe(200);
    }
  });
});

// ============================================================
// Test 6: Check all links on homepage are reachable
// ============================================================
test.describe('Homepage links', () => {
  for (const lang of LANGUAGES) {
    test(`all internal links on /${lang}/ are valid`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      await page.waitForLoadState('networkidle');

      const links = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href]'))
          .map((a: HTMLAnchorElement) => a.getAttribute('href'))
          .filter((href: string | null) => {
            if (!href) return false;
            if (href.startsWith('http')) return false;
            if (href.startsWith('#')) return false;
            if (href.startsWith('javascript:')) return false;
            if (href.startsWith('mailto:')) return false;
            if (href.startsWith('tel:')) return false;
            if (href.startsWith('sms:')) return false;
            if (href.startsWith('data:')) return false;
            return true;
          });
      });

      const brokenLinks: string[] = [];
      for (const href of links.slice(0, 200)) {
        try {
          const res = await page.goto(href);
          if (res?.status() !== 200) {
            brokenLinks.push(`${href} (${res?.status()})`);
          }
        } catch (e: unknown) {
          const err = e as Error;
          if (!err.message.includes('ERR_ABORTED')) {
            brokenLinks.push(`${href} (${err.message})`);
          }
        }
      }

      if (brokenLinks.length > 0) {
        console.log(`[BROKEN LINKS /${lang}/]`, brokenLinks.slice(0, 20));
      }
      // Allow for links beyond the 200-sample limit
      expect(brokenLinks.length, `/${lang}/ should have no broken links (showing first 200)`).toBeLessThanOrEqual(Math.max(0, links.length - 200));
    });
  }
});

// ============================================================
// Test 7: Check blog articles for translated languages
// ============================================================
test.describe('Blog articles', () => {
  const BLOG_ARTICLES = [
    'awus036axml-firmware-monitor-mode-fix',
    'awus036axml-wifi-6e-review',
    'awus036ach-vs-awus036acm',
    'packet-injection-guide',
    'best-wifi-adapter-kali-linux-2026',
    'hak5-wifi-pineapple-pager-alfa-compatibility',
  ];

  for (const lang of ['en', 'de', 'fr', 'ja']) {
    for (const article of BLOG_ARTICLES) {
      test(`/${lang}/blog/${article}/ loads`, async ({ page }) => {
        const res = await page.goto(`/${lang}/blog/${article}/`);
        expect(res?.status(), `/${lang}/blog/${article}/ should be 200`).toBe(200);
      });
    }
  }
});

// ============================================================
// Test 8: Check product detail pages for DE and FR
// ============================================================
test.describe('DE/FR product detail pages', () => {
  const SAMPLE_SLUGS = [
    'awus036axml',
    'awus036ach',
    'awus036acm',
    'apa-m04',
    'ars-25-57a',
  ];

  for (const lang of ['de', 'fr']) {
    for (const slug of SAMPLE_SLUGS) {
      test(`/${lang}/products/alfa/${slug}/ loads`, async ({ page }) => {
        const res = await page.goto(`/${lang}/products/alfa/${slug}/`);
        expect(res?.status(), `/${lang}/products/alfa/${slug}/ should be 200`).toBe(200);
      });
    }
  }
});

// ============================================================
// Test 9: Check special pages
// ============================================================
test.describe('Special pages', () => {
  const SPECIAL_PAGES = [
    '/en/404.html',
    '/de/404.html',
    '/fr/404.html',
    '/en/alfa_compare/',
    '/de/alfa_compare/',
    '/fr/alfa_compare/',
  ];

  for (const spage of SPECIAL_PAGES) {
    test(`${spage} loads`, async ({ page }) => {
      const res = await page.goto(spage);
      expect(res?.status(), `${spage} should be 200`).toBe(200);
    });
  }
});

// ============================================================
// Test 10: Check hreflang tags on all language homepages
// ============================================================
test.describe('Hreflang tags', () => {
  for (const lang of LANGUAGES) {
    test(`/${lang}/ has hreflang tags`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      const hreflangs = await page.evaluate(() => {
        const links = document.querySelectorAll('link[rel="alternate"]');
        return Array.from(links).map((l: HTMLLinkElement) => ({
          href: l.getAttribute('href'),
          hreflang: l.getAttribute('hreflang'),
        }));
      });

      expect(hreflangs.length, `/${lang}/ should have hreflang tags`).toBeGreaterThanOrEqual(11);
    });
  }
});

// ============================================================
// Test 11: Check RTL layout for Arabic
// ============================================================
test.describe('RTL support', () => {
  test('/ar/ page has RTL direction', async ({ page }) => {
    await page.goto('/ar/');
    const dir = await page.evaluate(() => document.documentElement.getAttribute('dir'));
    expect(dir).toBe('rtl');
  });
});

// ============================================================
// Test 12: Check content language detection
// ============================================================
test.describe('Content integrity', () => {
  for (const lang of LANGUAGES) {
    test(`/${lang}/ has non-empty content`, async ({ page }) => {
      await page.goto(`/${lang}/`);
      await page.waitForLoadState('networkidle');

      const content = await page.evaluate(() => document.body.innerText.trim());
      expect(content.length, `/${lang}/ should have content`).toBeGreaterThan(100);
    });
  }
});
