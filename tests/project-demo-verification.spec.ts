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
    await page.waitForSelector('html[data-app-ready="true"]');

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

  test('06 - Cinema Lightbox Modal Multi-Media Navigation', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);
    await page.waitForSelector('html[data-app-ready="true"]');

    const lightbox = page.locator('#lightbox');
    await expect(lightbox).not.toHaveClass(/open/);

    // 點擊專案 01 的影院全螢幕模式按鈕
    const cinemaBtn = page.locator('#project-01 .media-cinema-btn');
    await cinemaBtn.click();
    await expect(lightbox).toHaveClass(/open/);

    // 驗證彈窗 HUD 標題與計數器 (1 影片 + 2 相片 = 3 則媒體)
    await expect(page.locator('.lightbox-hud__title')).toBeVisible();
    await expect(page.locator('.lightbox-hud__counter')).toContainText('/ 3');

    // 點擊 Next 切換下一則媒體
    const nextBtn = page.locator('.lightbox-arrow--next');
    if (await nextBtn.isVisible()) {
      await nextBtn.click();
      await expect(page.locator('.lightbox-hud__counter')).toContainText('2 / 3');
    }

    // 點擊關閉按鈕
    await page.click('#lightbox-close');
    await expect(lightbox).not.toHaveClass(/open/);

    // 再次開啟並用 ESC 鍵關閉
    await cinemaBtn.click();
    await expect(lightbox).toHaveClass(/open/);
    await page.keyboard.press('Escape');
    await expect(lightbox).not.toHaveClass(/open/);
  });

  test('07 - Interactive Media Tabs & Filmstrip Switching', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);
    await page.waitForSelector('html[data-app-ready="true"]');

    const card01 = page.locator('#project-01');
    const tabGallery = card01.locator('.media-tab[data-tab="gallery"]');
    const tabVideo = card01.locator('.media-tab[data-tab="video"]');
    const panelGallery = card01.locator('.media-panel--gallery');
    const panelVideo = card01.locator('.media-panel--video');

    // 預設為影片面板 active
    await expect(panelVideo).toHaveClass(/active/);
    await expect(panelGallery).not.toHaveClass(/active/);

    // 切換至相簿面板
    await tabGallery.click();
    await expect(panelGallery).toHaveClass(/active/);
    await expect(panelVideo).not.toHaveClass(/active/);

    // 點擊縮圖 filmstrip 的第二張相片
    const thumb2 = panelGallery.locator('.thumb-btn').nth(1);
    await thumb2.click();
    await expect(thumb2).toHaveClass(/active/);

    // 切換回影片面板
    await tabVideo.click();
    await expect(panelVideo).toHaveClass(/active/);
  });

  test('08 - Mobile Viewport Layout Verification (375px)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 檢查無水平捲動破版
    const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
    const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 2);

    // 語言切換選單依然可視
    await expect(page.locator('.lang-switcher')).toBeVisible();
    await expect(page.locator('.hero__title')).toBeVisible();
  });

  test('09 - CIS Tech-Dark Compliance Verification', async ({ page }) => {
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

  test('10 - Issue 1: Sticky Nav 01-11 placed beside label with zero overlap on lang-switcher', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 往下拉滾動觸發 Sticky
    await page.evaluate(() => window.scrollTo(0, 1000));
    await page.waitForTimeout(300);

    const navLabelBox = await page.locator('.project-nav__label').boundingBox();
    const nav11Box = await page.locator('.project-nav__item[href="#project-11"]').boundingBox();
    const langSwitcherBox = await page.locator('.lang-switcher').boundingBox();

    expect(navLabelBox).not.toBeNull();
    expect(nav11Box).not.toBeNull();
    expect(langSwitcherBox).not.toBeNull();

    // 1. 驗證 01-11 的第一個按鈕緊隨在「專案導覽」標籤旁邊
    const nav01Box = await page.locator('.project-nav__item[href="#project-01"]').boundingBox();
    expect(nav01Box!.x).toBeGreaterThan(navLabelBox!.x);

    // 2. 驗證最後一個數字按鈕 11 的右邊界與右上角五國語言按鈕左邊界之間有充裕間隙（無重疊）
    const gap = langSwitcherBox!.x - (nav11Box!.x + nav11Box!.width);
    expect(gap).toBeGreaterThan(20); // 確保至少有 20px 以上安全距離
  });

  test('11 - Issue 2: Project descriptions match official project_details.md content', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    // 檢查 01 包含生命館主秀與工研院平板花海
    const desc01 = await page.locator('#project-01 .project-card__description').textContent();
    expect(desc01).toContain('Tech World 生命館主秀');
    expect(desc01).toContain('數位花海技術');

    // 檢查 02 包含直立式大型平面 LED 顯示屏與歷史建築
    const desc02 = await page.locator('#project-02 .project-card__description').textContent();
    expect(desc02).toContain('直立式大型平面 LED 顯示屏');
    expect(desc02).toContain('歷史建築改造');

    // 檢查 08 包含起司瀑布與多感官連結
    const desc08 = await page.locator('#project-08 .project-card__description').textContent();
    expect(desc08).toContain('起司瀑布');
    expect(desc08).toContain('多感官連結');
  });

  test('12 - Issue 3: Media stage and preview image dimensions are constrained & screenshot reviewed', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 900 });
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const mediaStage = page.locator('#project-01 .media-stage-wrapper');
    const stageBox = await mediaStage.boundingBox();
    expect(stageBox).not.toBeNull();

    // 驗證主媒體容器寬度已優化收斂，寬度不超過 500px，高度不超過 300px
    expect(stageBox!.width).toBeLessThanOrEqual(500);
    expect(stageBox!.height).toBeLessThanOrEqual(300);

    // 切換到相簿檢查圖片尺寸
    await page.click('#project-01 .media-tab[data-tab="gallery"]');
    const activeImg = page.locator('#project-01 .gallery-active-img');
    const imgBox = await activeImg.boundingBox();
    expect(imgBox).not.toBeNull();
    expect(imgBox!.width).toBeLessThanOrEqual(500);

    // 儲存截圖以利檢視
    await page.screenshot({ path: 'test-results/project-media-size-review.png', fullPage: false });
  });

  test('13 - Project Media Inventory & Asset Integrity Check', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);

    const videoProjects = ['01', '02', '03', '04', '06', '07', '08', '09'];
    const nonVideoProjects = ['05', '10', '11'];

    // 驗證有影片的專案具有 video container 與展示影片 Tab
    for (const id of videoProjects) {
      const card = page.locator(`#project-${id}`);
      await expect(card.locator('.media-tab[data-tab="video"]')).toBeVisible();
      await expect(card.locator('.video-container')).toHaveAttribute('data-video-src', new RegExp(`/project/assets/video/${id}.mp4`));
    }

    // 驗證無影片的專案僅有現場相簿 Tab 且直接為 active
    for (const id of nonVideoProjects) {
      const card = page.locator(`#project-${id}`);
      await expect(card.locator('.media-tab[data-tab="video"]')).toHaveCount(0);
      await expect(card.locator('.media-tab[data-tab="gallery"]')).toHaveClass(/active/);
      await expect(card.locator('.media-panel--gallery')).toHaveClass(/active/);
      await expect(card.locator('.video-container')).toHaveCount(0);
    }

    // 檢查專案展示區所有圖片的 src 均可正常載入 (HTTP 200)
    const imgElements = await page.locator('.projects-container img').all();
    expect(imgElements.length).toBeGreaterThan(20);
    for (const img of imgElements.slice(0, 10)) {
      const src = await img.getAttribute('src');
      expect(src).toBeTruthy();
      const res = await page.request.get(`${BASE_URL}${src}`);
      expect(res.status()).toBe(200);
    }
  });

  test('14 - Non-Video Project Lightbox & Cinema Mode Verification', async ({ page }) => {
    await page.goto(`${BASE_URL}/zh-tw/solution/project/`);
    await page.waitForSelector('html[data-app-ready="true"]');

    const lightbox = page.locator('#lightbox');

    // 測試專案 05 (松菸夜光花園，無影片，2 張相片)
    const cinemaBtn05 = page.locator('#project-05 .media-cinema-btn');
    await cinemaBtn05.click();
    await expect(lightbox).toHaveClass(/open/);

    // 驗證 Lightbox 顯示圖片模式，計數器為 1 / 2
    await expect(page.locator('.lightbox-image')).toBeVisible();
    await expect(page.locator('.lightbox-hud__counter')).toContainText('1 / 2');

    // 點擊 Next 切換下一張相片
    await page.locator('.lightbox-arrow--next').click();
    await expect(page.locator('.lightbox-hud__counter')).toContainText('2 / 2');

    // 關閉 Lightbox
    await page.click('#lightbox-close');
    await expect(lightbox).not.toHaveClass(/open/);

    // 測試專案 10 (2024亞太永續博覽會，無影片，3 張相片)
    const cinemaBtn10 = page.locator('#project-10 .media-cinema-btn');
    await cinemaBtn10.click();
    await expect(lightbox).toHaveClass(/open/);
    await expect(page.locator('.lightbox-hud__counter')).toContainText('1 / 3');
    await page.click('#lightbox-close');
    await expect(lightbox).not.toHaveClass(/open/);
  });
});


