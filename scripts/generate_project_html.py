#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# 1. 讀取繁體中文單一真實資料源
with open('static/project/i18n/zh-TW.json', 'r', encoding='utf-8') as f:
    zh_tw = json.load(f)

projects_data = zh_tw['projects']

# 2. 讀取真實多媒體配置 (來自 project_media_map.json)
with open('scripts/project_media_map.json', 'r', encoding='utf-8') as f:
    media_map = json.load(f)

projects_meta = []
for p_id in sorted(projects_data.keys()):
    p_info = projects_data[p_id]
    m_info = media_map.get(p_id, {'video': None, 'images': []})
    projects_meta.append({
        'id': p_id,
        'title': p_info['title'],
        'subtitle': p_info['subtitle'],
        'tags': p_info['tags'],
        'client': p_info['client'],
        'location': p_info['location'],
        'desc': p_info['description'],
        'video': m_info.get('video'),
        'images': m_info.get('images', [])
    })

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
    has_video = bool(p['video'])
    tags_html = '\n'.join([f'          <span class="tag-mecha" data-i18n="projects.{p_id}.tags.{t_i}">{t}</span>' for t_i, t in enumerate(p['tags'])])
    
    thumb_lines = []
    for img_i, img in enumerate(p['images']):
        active_cls = "active" if img_i == 0 else ""
        thumb_lines.append(f'              <button class="thumb-btn {active_cls}" data-img-src="{img}" aria-label="相片 {img_i + 1}"><img src="{img}" alt="{p["title"]} 相片 {img_i + 1}" loading="lazy"></button>')
    thumbs_html = '\n'.join(thumb_lines)

    if has_video:
        hud_tabs_html = f'''          <div class="media-tabs" role="tablist">
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
          </div>'''

        stage_html = f'''        <div class="media-stage-wrapper">
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
        </div>'''
    else:
        # 專案無影片：僅呈現現場相簿
        hud_tabs_html = f'''          <div class="media-tabs" role="tablist">
            <button class="media-tab active" data-tab="gallery" role="tab" aria-selected="true">
              <span class="media-tab__icon">🖼️</span>
              <span class="media-tab__label" data-i18n="labels.tabGallery">現場相簿</span>
              <span class="media-tab__count">{len(p['images'])}</span>
              <span class="media-tab__badge" data-i18n="labels.galleryBadge">現場實景</span>
            </button>
          </div>'''

        stage_html = f'''        <div class="media-stage-wrapper">
          <!-- Gallery Panel (無影片直接啟用現場相簿) -->
          <div class="media-panel media-panel--gallery active">
            <div class="gallery-main-view">
              <img class="gallery-active-img" src="{p['images'][0]}" alt="{p['title']}" data-active-index="0" loading="lazy">
            </div>
            <div class="gallery-filmstrip">
{thumbs_html}
            </div>
          </div>
        </div>'''

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
{hud_tabs_html}
          <button class="media-cinema-btn" title="影院全螢幕模式">
            <span class="cinema-icon">⛶</span>
            <span class="cinema-label" data-i18n="labels.viewFullscreen">影院模式</span>
          </button>
        </div>

{stage_html}
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
