import { test, expect } from '@playwright/test';

test.describe('Yupitek Online Project Demo Showcase', () => {
  const BASE_URL = process.env.BASE_URL || 'http://localhost:1314';

  test('01 - Page Loads & Multilingual Metadata Check', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);
    
    // 檢查 Title
    await expect(page).toHaveTitle(/線上專案展示/);

    // 檢查 hreflang 標記存在且齊備
    const hreflangs = await page.$$eval('link[rel="alternate"][hreflang]', els => 
      els.map(el => ({ lang: el.getAttribute('hreflang'), href: el.getAttribute('href') }))
    );
    
    const langs = hreflangs.map(h => h.lang);
    expect(langs).toContain('zh-TW');
    expect(langs).toContain('zh-CN');
    expect(langs).toContain('en');
    expect(langs).toContain('ja');
    expect(langs).toContain('ko');

    // 檢查 canonical
    const canonical = await page.$eval('link[rel="canonical"]', el => el.getAttribute('href'));
    expect(canonical).toContain('/zh-tw/solution/project/');
  });

  test('02 - Hero Section & Canvas Particle Background', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const hero = page.locator('.hero');
    await expect(hero).toBeVisible();

    const canvas = page.locator('#hero-canvas');
    await expect(canvas).toBeVisible();

    const title = page.locator('.hero__title');
    await expect(title).toBeVisible();
    await expect(title).toContainText('光雕與動態影像');

    const primaryBtn = page.locator('.hero .btn-mecha--primary');
    await expect(primaryBtn).toBeVisible();
    await expect(primaryBtn).toHaveAttribute('href', '#projects-container');
  });

  test('03 - Verify Exactly 11 Projects Rendered Sequentially', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const projectCards = page.locator('.project-card');
    await expect(projectCards).toHaveCount(11);

    const expectedProjects = [
      { id: 'project-01', index: '01 / 11', titleKeyword: 'TechWorld' },
      { id: 'project-02', index: '02 / 11', titleKeyword: 'C-LAB' },
      { id: 'project-03', index: '03 / 11', titleKeyword: '王船' },
      { id: 'project-04', index: '04 / 11', titleKeyword: '花卉' },
      { id: 'project-05', index: '05 / 11', titleKeyword: '松菸' },
      { id: 'project-06', index: '06 / 11', titleKeyword: 'PALLADIUM' },
      { id: 'project-07', index: '07 / 11', titleKeyword: '板橋放送所' },
      { id: 'project-08', index: '08 / 11', titleKeyword: '樂事' },
      { id: 'project-09', index: '09 / 11', titleKeyword: '台北市政府' },
      { id: 'project-10', index: '10 / 11', titleKeyword: '永續' },
      { id: 'project-11', index: '11 / 11', titleKeyword: '蕭敬騰' }
    ];

    for (let i = 0; i < expectedProjects.length; i++) {
      const p = expectedProjects[i];
      const card = page.locator(`#${p.id}`);
      await expect(card).toBeVisible();
      await expect(card.locator('.project-card__index')).toContainText(p.index);
      await expect(card.locator('.project-card__title')).toContainText(p.titleKeyword);
      await expect(card.locator('.project-card__description')).not.toBeEmpty();
    }
  });

  test('04 - Dynamic 5-Language Switching Functionality', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 1. 切換至 EN
    await page.click('.lang-btn[data-lang="en"]');
    await expect(page.locator('.hero__eyebrow')).toHaveText('IMMERSIVE VISUAL EXPERIENCE');
    await expect(page.locator('#project-01 .project-card__title')).toContainText('2026 Taiwan Lantern Festival');
    await expect(page.locator('.hero .btn-mecha--primary')).toContainText('Explore Projects');

    // 2. 切換至 日本語
    await page.click('.lang-btn[data-lang="ja"]');
    await expect(page.locator('#project-01 .project-card__title')).toContainText('台湾ランタンフェス');
    await expect(page.locator('.hero .btn-mecha--primary')).toContainText('プロジェクトを見る');

    // 3. 切換至 한국어
    await page.click('.lang-btn[data-lang="ko"]');
    await expect(page.locator('#project-01 .project-card__title')).toContainText('대만 등불축제');
    await expect(page.locator('.hero .btn-mecha--primary')).toContainText('프로젝트 탐색');

    // 4. 切換至 简中
    await page.click('.lang-btn[data-lang="zh-CN"]');
    await expect(page.locator('#project-01 .project-card__title')).toContainText('2026台湾灯会');

    // 5. 切換回 繁中
    await page.click('.lang-btn[data-lang="zh-TW"]');
    await expect(page.locator('#project-01 .project-card__title')).toContainText('2026台灣燈會');
  });

  test('05 - Sticky Navigation Links', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const navItems = page.locator('.project-nav__item');
    await expect(navItems).toHaveCount(11);

    // 點擊專案 05 跳轉按鈕
    const nav05 = page.locator('.project-nav__item[href="#project-05"]');
    await nav05.click();
    await page.waitForTimeout(500);

    const project05 = page.locator('#project-05');
    await expect(project05).toBeInViewport();
  });

  test('06 - Lightbox Modal Open and Close', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const lightbox = page.locator('#lightbox');
    await expect(lightbox).not.toHaveClass(/open/);

    // 點擊專案 01 的媒體觸發 Lightbox
    const mediaItem = page.locator('#project-01 [data-lightbox]').first();
    await mediaItem.click();
    await expect(lightbox).toHaveClass(/open/);

    // 驗證彈窗內容載入
    const content = page.locator('#lightbox-content');
    await expect(content.locator('video, img')).toBeVisible();

    // 點擊關閉按鈕
    await page.click('#lightbox-close');
    await expect(lightbox).not.toHaveClass(/open/);

    // 再次開啟並用 ESC 關閉
    await mediaItem.click();
    await expect(lightbox).toHaveClass(/open/);
    await page.keyboard.press('Escape');
    await expect(lightbox).not.toHaveClass(/open/);
  });

  test('07 - Mobile Viewport Layout Verification (375px)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 檢查無水平捲動破版
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2); // 容許 1-2px 次像素微差

    // 語言切換選單依然可視
    await expect(page.locator('.lang-switcher')).toBeVisible();
    await expect(page.locator('.hero__title')).toBeVisible();
  });

  test('08 - CIS Tech-Dark Compliance Verification', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 背景色檢查
    const bgColor = await page.evaluate(() => {
      return window.getComputedStyle(document.body).backgroundColor;
    });
    // rgb(11, 14, 17) corresponds to #0B0E11
    expect(bgColor).toBe('rgb(11, 14, 17)');

    // 檢查 html tag 的 data-scheme
    const scheme = await page.getAttribute('html', 'data-scheme');
    expect(scheme).toBe('tech-dark');
  });
});
