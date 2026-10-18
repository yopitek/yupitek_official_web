const { chromium } = require('playwright');
const fs = require('fs');

const LOCALES = ['zh-tw', 'zh-cn', 'en', 'ja', 'ar', 'es', 'pt', 'ru', 'de', 'fr'];
const SLUGS = ['flipper-zero-beginners-guide-setup-tutorial', 'awus036axml-wifi6e-kali-linux-setup'];

(async () => {
  const browser = await chromium.launch({ args: ['--disable-blink-features=AutomationControlled'] });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  let success = true;

  for (const slug of SLUGS) {
    for (const locale of LOCALES) {
      const url = `https://yupitek.com/${locale}/blog/${slug}/?v=1`;
      console.log(`Checking ${url}...`);
      
      const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(e => null);
      if (!response || !response.ok()) {
        console.error(`❌ Failed to load ${url}: ${response ? response.status() : 'timeout'}`);
        success = false;
        continue;
      }
      
      const title = await page.title();
      if (!title || title.length < 5) {
        console.error(`❌ Bad title on ${url}: "${title}"`);
        success = false;
      }
      
      const hreflangs = await page.locator('link[rel="alternate"][hreflang]').count();
      if (hreflangs < 9) {
        console.error(`❌ Missing hreflangs on ${url}: found ${hreflangs}`);
        success = false;
      }
      
      console.log(`✅ Passed ${locale} ${slug} (hreflangs: ${hreflangs})`);
    }
  }

  await browser.close();
  if (success) {
    console.log("ALL VERIFICATIONS PASSED.");
    process.exit(0);
  } else {
    process.exit(1);
  }
})();
