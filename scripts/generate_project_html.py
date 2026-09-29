#!/usr/bin/env python3
# -*- coding: utf-8 -*-

projects_meta = [
    {
        'id': '01',
        'title': '2026台灣燈會 TechWorld',
        'subtitle': 'Tech World Pavilion — Architectural & Indoor Cylinder Projection',
        'tags': ['大型戶外結構光雕', '圓柱沉浸裝置', '主題館系統整合'],
        'client': 'Tech World',
        'location': '嘉義',
        'desc': 'Tech World 生命館案例是榆閤科技跨場域整合能力的完整展現，同時承接戶外大型結構投影與室內沉浸裝置兩大主要場景。',
        'video': '/project/assets/video/01.mp4',
        'images': ['/project/assets/img/01/main.webp', '/project/assets/img/01/02.webp']
    },
    {
        'id': '02',
        'title': '臺灣當代文化實驗場 C-LAB',
        'subtitle': 'FUTURE VISION LAB — Multi-Projector Dome Edge-Blending',
        'tags': ['穹頂球形展演', '邊緣融合技術', '數位藝術校準'],
        'client': '臺灣當代文化實驗場',
        'location': '台北',
        'desc': '臺灣當代文化實驗場（C-LAB）是台灣重要的藝術科技實驗基地，致力於探索科技媒體與視覺藝術的創新極限。',
        'video': '/project/assets/video/02.mp4',
        'images': ['/project/assets/img/02/main.webp', '/project/assets/img/02/02.webp', '/project/assets/img/02/03.webp']
    },
    {
        'id': '03',
        'title': '東港王船博物館',
        'subtitle': "King's Boat Museum — Panoramic Immersive Projection Wall",
        'tags': ['文化遺產數位化', '環形曲面投影', '博物館常設展'],
        'client': '屏東縣東港王船文化館',
        'location': '屏東',
        'desc': '屏東東港王船祭是台灣最具代表性的無形文化遺產之一，被列為國家重要民俗。',
        'video': '/project/assets/video/03.mp4',
        'images': ['/project/assets/img/03/main.jpg', '/project/assets/img/03/02.webp']
    },
    {
        'id': '04',
        'title': '2026台灣花卉科技展',
        'subtitle': 'Houbi Orchid Exhibition — 64m Ultra-Wide Curved Panoramic Projection',
        'tags': ['64公尺超寬弧形幕', '高亮度融合校準', '國際花卉博覽會'],
        'client': '台南市政府',
        'location': '台南後壁',
        'desc': '後壁蘭花展為台灣重要的國際花卉展覽活動。本次榆閤科技承接主展覽館核心沉浸場景的超大型曲面投影製作任務。',
        'video': '/project/assets/video/04.mp4',
        'images': ['/project/assets/img/04/main.webp', '/project/assets/img/04/02.webp']
    },
    {
        'id': '05',
        'title': '松菸夜光花園',
        'subtitle': 'The LUMINOUS GARDEN — Baroque Garden Heritage Projection Mapping',
        'tags': ['百年古蹟立面光雕', '夜間常態劇場', '文創園區活化'],
        'client': '松山文創園區',
        'location': '台北',
        'desc': '松山文創園區「松菸夜光花園（The LUMINOUS GARDEN）」是園區極具指標性的常態夜間光影展演。',
        'video': '/project/assets/video/05.mp4',
        'images': ['/project/assets/img/05/main.webp', '/project/assets/img/05/02.webp']
    },
    {
        'id': '06',
        'title': 'PALLADIUM 全境轉運站',
        'subtitle': 'PALLADIUM Terminal — 360° Sensory Immersive Experience',
        'tags': ['360度環景投影', '品牌潮流快閃', '實景雨霧五感整合'],
        'client': 'PALLADIUM Taiwan',
        'location': '台北心中山',
        'desc': 'PALLADIUM 是來自法國的百年機能鞋履品牌，以探索城市地貌與戶外場域為核心品牌精神。',
        'video': '/project/assets/video/06.mp4',
        'images': ['/project/assets/img/06/main.webp', '/project/assets/img/06/02.webp']
    },
    {
        'id': '07',
        'title': '板橋放送所',
        'subtitle': 'Banqiao Broadcasting Station — 360° Full Immersive Projection Space',
        'tags': ['360度全沉浸常設展', '地空全覆蓋投影', '表演藝術互動融合'],
        'client': '新北市文化場館',
        'location': '新北板橋',
        'desc': '板橋放送所為榆閤科技最具代表性的旗艦常設展案例，同時也是台灣極少數完整實現 360° 全沉浸式投影空間的文化場館。',
        'video': '/project/assets/video/07.mp4',
        'images': ['/project/assets/img/07/main.webp', '/project/assets/img/07/02.webp']
    },
    {
        'id': '08',
        'title': '樂事：風味光影展',
        'subtitle': "Lay's Cheese Waterfall — Real-time Fluid Interactive Projection",
        'tags': ['即時體感互動', '流體分流演算法', '現象級品牌沉浸展'],
        'client': '台灣百事食品 / 樂事',
        'location': '台北華山1914',
        'desc': '樂事（Lay\'s）風味光影展是台灣零食界首創的沉浸式品牌體驗展覽，於台北華山 1914 文化創意產業園區盛大展出。',
        'video': '/project/assets/video/08.mp4',
        'images': ['/project/assets/img/08/main.webp', '/project/assets/img/08/02.webp']
    },
    {
        'id': '09',
        'title': '台北市政府光雕投影',
        'subtitle': 'Color Taipei — City Hall Dynamic Facade Projection Mapping',
        'tags': ['地標建築立面光雕', '幾何結構對位', '城市節慶公共藝術'],
        'client': '台北市政府觀傳局',
        'location': '台北信義區',
        'desc': '本案以台北市政府整棟建築立面作為投影畫布，配合 2021 年「Color Taipei」彩虹節慶活動。',
        'video': '/project/assets/video/09.mp4',
        'images': ['/project/assets/img/09/main.webp', '/project/assets/img/09/02.webp']
    },
    {
        'id': '10',
        'title': '2024亞太永續博覽會',
        'subtitle': 'Rong Cheng Paper Industry — 4-Wall Panoramic Eco Exhibition',
        'tags': ['企業永續形象展', '四面沉浸環繞', '快速展場融合佈設'],
        'client': '榮成紙業股份有限公司',
        'location': '台北世貿一館',
        'desc': '本案於台北世貿展覽中心內打造多面牆環繞式沉浸投影展間，專為榮成紙業年度環保形象展而量身設計。',
        'video': '/project/assets/video/10.mp4',
        'images': ['/project/assets/img/10/main.webp', '/project/assets/img/10/02.webp']
    },
    {
        'id': '11',
        'title': '蕭敬騰展',
        'subtitle': 'Jam Hsiao Art Exhibition — Multi-Screen Framed Window Projection',
        'tags': ['個人藝術特展', '多幕窗景擬真', '音樂與光影美學交融'],
        'client': '蕭敬騰個人藝術工作室',
        'location': '台北',
        'desc': '本案為知名音樂人蕭敬騰量身打造的沉浸式個人藝術展覽空間，以音樂旅程、詩詞意境與北歐自然景觀為核心設計主題。',
        'video': '/project/assets/video/11.mp4',
        'images': ['/project/assets/img/11/main.webp', '/project/assets/img/11/02.webp']
    }
]

html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="{{ .Language.Locale }}" data-scheme="tech-dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ .Title }} | {{ .Site.Title }}</title>
  <meta name="description" content="{{ .Description }}">

  <!-- hreflang 多語系 SEO -->
  {{ range .AllTranslations }}
  <link rel="alternate" hreflang="{{ .Language.Locale }}" href="{{ .Permalink }}">
  {{ end }}
  <link rel="canonical" href="{{ .Permalink }}">

  <!-- Google Fonts Preconnect -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Outfit:wght@400;600;700&display=swap">

  <!-- 樣式表 (獨立於 Blowfish 主題，避免樣式衝突) -->
  <link rel="stylesheet" href="/project/css/tokens.css">
  <link rel="stylesheet" href="/project/css/fonts.css">
  <link rel="stylesheet" href="/project/css/project.css">
</head>
<body class="tech-dark-body">

  <!-- 置頂左上：返回首頁 -->
  <a href="/{{ .Language.Lang }}/" class="back-home" title="返回首頁">←<span class="back-label" data-i18n="nav.back"> 返回首頁</span></a>

  <!-- 置頂右上：五語系即時切換器 -->
  <nav class="lang-switcher" aria-label="Language Selector">
    <button class="lang-btn" data-lang="zh-TW">繁中</button>
    <button class="lang-btn" data-lang="zh-CN">简中</button>
    <button class="lang-btn" data-lang="en">EN</button>
    <button class="lang-btn" data-lang="ja">日本語</button>
    <button class="lang-btn" data-lang="ko">한국어</button>
  </nav>

  <!-- Hero Section -->
  <section class="hero">
    <canvas id="hero-canvas" class="hero__canvas"></canvas>
    <div class="hero__content">
      <div class="hero__eyebrow" data-i18n="hero.eyebrow">IMMERSIVE VISUAL EXPERIENCE</div>
      <h1 class="hero__title" data-i18n-html="hero.titleHtml">
        以光雕與動態影像<br>重塑<span class="highlight">空間與感知邊界</span>
      </h1>
      <p class="hero__subtitle" data-i18n="hero.subtitle">
        精選 11 個代表性沉浸式投影專案。從歷史古蹟立面光雕到 360° 穹頂全沉浸展演，結合邊緣融合校準與即時體感互動技術。
      </p>
      <div class="hero__actions">
        <a href="#projects-container" class="btn-mecha btn-mecha--primary" data-i18n="hero.ctaExplore">探索精選專案 ↓</a>
        <a href="/{{ .Language.Lang }}/contact/" class="btn-mecha btn-mecha--ghost" data-i18n="hero.ctaContact">洽詢合作方案 →</a>
      </div>
    </div>
  </section>

  <!-- Sticky 專案切換導航列 -->
  <div class="project-nav-wrapper">
    <nav class="project-nav" aria-label="Projects Quick Navigation">
      <span class="project-nav__label" data-i18n="nav.projects">專案導覽</span>
      <ul class="project-nav__list">
        <li><a href="#project-01" class="project-nav__item active">01</a></li>
        <li><a href="#project-02" class="project-nav__item">02</a></li>
        <li><a href="#project-03" class="project-nav__item">03</a></li>
        <li><a href="#project-04" class="project-nav__item">04</a></li>
        <li><a href="#project-05" class="project-nav__item">05</a></li>
        <li><a href="#project-06" class="project-nav__item">06</a></li>
        <li><a href="#project-07" class="project-nav__item">07</a></li>
        <li><a href="#project-08" class="project-nav__item">08</a></li>
        <li><a href="#project-09" class="project-nav__item">09</a></li>
        <li><a href="#project-10" class="project-nav__item">10</a></li>
        <li><a href="#project-11" class="project-nav__item">11</a></li>
      </ul>
    </nav>
  </div>

  <!-- 11 個專案展示區塊 -->
  <main id="projects-container" class="projects-container">''')

for idx, p in enumerate(projects_meta):
    p_id = p['id']
    tags_html = '\n'.join([f'          <span class="tag-mecha" data-i18n="projects.{p_id}.tags.{t_i}">{t}</span>' for t_i, t in enumerate(p['tags'])])
    
    thumb_lines = []
    for img_i, img in enumerate(p['images']):
        active_cls = "active" if img_i == 0 else ""
        thumb_lines.append(f'              <button class="thumb-btn {active_cls}" data-img-src="{img}" aria-label="相片 {img_i + 1}"><img src="{img}" alt="{p["title"]} 相片 {img_i + 1}" loading="lazy"></button>')
    thumbs_html = '\n'.join(thumb_lines)

    card_html = f'''    <!-- {p_id} {p['title']} -->
    <article id="project-{p_id}" class="project-card">
      <div class="project-card__info">
        <div class="project-card__header">
          <div class="project-card__index" data-i18n="projects.{p_id}.index">{p_id} / 11</div>
          <h2 class="project-card__title" data-i18n="projects.{p_id}.title">{p['title']}</h2>
          <div class="project-card__subtitle" data-i18n="projects.{p_id}.subtitle">{p['subtitle']}</div>
        </div>
        <div class="project-card__tags">
{tags_html}
        </div>
        <div class="project-card__meta">
          <div class="meta-item"><span data-i18n="labels.client">委託單位</span><strong data-i18n="projects.{p_id}.client">{p['client']}</strong></div>
          <div class="meta-item"><span data-i18n="labels.location">專案地點</span><strong data-i18n="projects.{p_id}.location">{p['location']}</strong></div>
        </div>
        <p class="project-card__description" data-i18n="projects.{p_id}.description">
          {p['desc']}
        </p>
      </div>
      <div class="project-card__media">
        <!-- Media HUD Switcher -->
        <div class="media-hud-bar">
          <div class="media-tabs" role="tablist">
            <button class="media-tab active" data-tab="video" role="tab" aria-selected="true">
              <span class="media-tab__icon">🎥</span>
              <span class="media-tab__label" data-i18n="labels.tabVideo">展示影片</span>
              <span class="media-tab__badge" data-i18n="labels.videoBadge">動態巡禮</span>
            </button>
            <button class="media-tab" data-tab="gallery" role="tab" aria-selected="false">
              <span class="media-tab__icon">🖼️</span>
              <span class="media-tab__label" data-i18n="labels.tabGallery">現場相簿</span>
              <span class="media-tab__count">{len(p['images'])}</span>
            </button>
          </div>
          <button class="media-cinema-btn" title="影院全螢幕模式">
            <span class="cinema-icon">⛶</span>
            <span class="cinema-label" data-i18n="labels.viewFullscreen">影院模式</span>
          </button>
        </div>

        <!-- Stage Container -->
        <div class="media-stage-wrapper">
          <!-- Video Panel -->
          <div class="media-panel media-panel--video active">
            <div class="video-container" data-video-src="{p['video']}">
              <img class="video-poster" src="{p['images'][0]}" alt="{p['title']}" loading="lazy">
              <div class="video-play-btn" role="button" aria-label="Play video">
                <span class="play-icon">▶</span>
                <span class="play-text" data-i18n="labels.playVideo">播放影片</span>
              </div>
            </div>
          </div>

          <!-- Gallery Panel -->
          <div class="media-panel media-panel--gallery">
            <div class="gallery-main-view">
              <img class="gallery-active-img" src="{p['images'][0]}" alt="{p['title']}" data-active-index="0" loading="lazy">
            </div>
            <div class="gallery-filmstrip">
{thumbs_html}
            </div>
          </div>
        </div>
      </div>
    </article>'''

    html_parts.append(card_html)
    if idx < len(projects_meta) - 1:
        html_parts.append('    <div class="brand-divider"></div>\n')

html_parts.append('''  </main>

  <!-- CTA Section -->
  <section class="cta-section">
    <div class="cta-section__inner">
      <h2 class="cta-section__title" data-i18n="cta.title">開始規劃您的沉浸式投影專案</h2>
      <p class="cta-section__desc" data-i18n="cta.subtitle">
        無論是歷史古蹟光雕、360° 沉浸空間、大型商業博覽會或互動感測展演，榆閤科技提供從光學規劃、硬體融合到現場校準的一站式整合服務。
      </p>
      <a href="/{{ .Language.Lang }}/contact/" class="btn-mecha btn-mecha--primary" data-i18n="cta.btn">立即預約技術諮詢 →</a>
    </div>
  </section>

  <!-- Lightbox 影院全螢幕彈窗容器 -->
  <div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Media Preview">
    <button id="lightbox-close" class="lightbox__close" aria-label="Close modal">&times;</button>
    <div id="lightbox-content" class="lightbox__content"></div>
  </div>

  <!-- GSAP CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>

  <!-- Application Entry Point -->
  <script type="module" src="/project/js/project-core.js"></script>
</body>
</html>
''')

output_path = 'layouts/_default/project.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f'Successfully generated {output_path} with {len(projects_meta)} projects!')
