---
title: "AI 生成產品圖片：使用 baoyu-skills 的完整風格參考指南"
description: "我們如何使用 GitHub Copilot CLI 的 baoyu-skills 外掛，生成部落格封面、資訊圖表、Instagram 卡片、漫畫及產品渲染圖——以 ALFA AWUS036ACM 為實際範例。B2B 行銷圖片生成的實用風格參考。"
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "AI-image-generation", "行銷", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

在 Yopitek，我們代理技術硬體產品——WiFi 網路卡、安全研究工具、SDR 模組——為 8 種語言持續產出高品質的行銷視覺素材一直是一大挑戰。本文記錄我們如何使用 GitHub Copilot CLI 的 **baoyu-skills** 外掛集合，跨不同格式與風格生成產品圖片。

我們在本指南中以 **ALFA AWUS036ACM** USB WiFi 網路卡作為範例產品。此處展示的每個提示詞與圖片，均由這款網路卡的描述所生成。目標是建立一份實用的風格參考：當您未來需要產品封面圖、Instagram 卡片或技術資訊圖表時，可以查閱應使用哪種技能與風格。

{{< alert "circle-info" >}}
**baoyu-skills** 是由 [@JimLiu](https://github.com/JimLiu/baoyu-skills.git) 為 GitHub Copilot CLI 開發的開源外掛集合。它新增了 19 項專業技能，涵蓋內容創作、圖片生成、翻譯及社群發布——全部可直接從終端機存取。
{{< /alert >}}

---

## 完整技能參考——所有 19 個 baoyu-skills

此集合共有 19 項技能，分為三種類型：

- **Type A — Image Output：** 生成視覺素材（封面、資訊圖表、漫畫、渲染圖）
- **Type B — HTML Output：** 生成樣式化網頁文件
- **Type C — Text / Utility：** 翻譯、格式化、社群發布、壓縮

| # | 技能 | 類型 | 用途 | 觸發關鍵字 |
|---|------|------|------|-----------|
| 01 | `baoyu-article-illustrator` | 圖片 | 自動為文章各段落生成插圖 | 為文章配圖 · illustrate article · add images |
| 02 | `baoyu-comic` | 圖片 | 以多種畫風創作漫畫／條漫／教育漫畫 | 知識漫畫 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | 工具 | 將圖片壓縮為 WebP/PNG，縮小 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | 圖片 | 以 5 個設計維度生成文章封面圖（類型、色盤、渲染、文字、情境） | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | API 引擎 | 透過 Gemini Web API 生成文字與圖片；多輪對話、視覺輸入 | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | 文字 | 將 X (Twitter) 推文和文章轉換為含 YAML front matter 的 Markdown | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | 文字 | 將純文字格式化為含標題、frontmatter、程式碼區塊的結構化 Markdown | format markdown · beautify article |
| 08 | `baoyu-image-gen` | 圖片 | 多供應商 AI 圖片生成（OpenAI、Google、DashScope、Replicate）；平行模式 | generate / create / draw images |
| 09 | `baoyu-imagine` | 圖片 | 自由形式 AI 圖片生成——寫實渲染、生活場景、爆炸圖 | imagine · create visual |
| 10 | `baoyu-infographic` | 圖片 | 專業資訊圖表：21 種版型 × 20 種視覺風格 | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | 將 Markdown 轉換為含微信主題、程式碼高亮、數學、PlantUML 的樣式化 HTML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | 社群 | 發布文章與圖文內容至微信公眾號 | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | 社群 | 發布至 X (Twitter)，支援圖片／影片；支援 X Articles 長文格式 | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | 圖片 | 從內容生成風格一致的投影片圖片 | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | 文字 | 三種翻譯模式：快速／一般（分析＋翻譯）／精翻（分析→翻譯→校閱→潤稿） | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | 文字 | 使用 Chrome CDP 擷取任何 URL 並轉換為 Markdown | save webpage as markdown |
| 17 | `baoyu-xhs-images` | 圖片 | 小紅書垂直卡片：10 種風格 × 8 種版型，適用於 Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | 文字 | 將 YouTube 字幕提取為結構化 Markdown | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | 社群 | 發布至微博，支援文字、圖片、話題標籤、字數限制處理 | 发布微博 · post to weibo |

---

## 第 01 節 — baoyu-cover-image

以三種長寬比生成文章封面圖：**電影寬幅 (2.35:1)**、**寬螢幕 (16:9)** 和 **正方形 (1:1)**。每種比例支援多種色彩搭配與渲染風格。

**適用時機：** 部落格文章主視覺、文章縮圖、網站橫幅。

### 風格變體

**變體 1 — 電影寬幅 · 深藍**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**變體 2 — 電影寬幅 · 橙色**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**變體 3 — 寬螢幕 · 暗碳**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**變體 4 — 寬螢幕 · 霓虹賽博龐克**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**變體 5 — 正方形 · 極簡**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**變體 6 — 正方形 · 大膽海報**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## 第 02 節 — baoyu-infographic

結合 **21 種版型** 與 **20 種視覺風格** 製作資訊圖表。版型定義結構（便當格、層次架構、時間軸…）；風格設定視覺語言（大膽圖形、技術示意圖、折紙…）。

**適用時機：** 產品規格概覽、比較表、技術說明貼文、LinkedIn 內容。

### 風格變體

**變體 1 — 便當格 × 大膽圖形**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**變體 2 — 便當格 × 技術示意圖**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**變體 3 — 層次架構 × 大膽圖形**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**變體 4 — 層次架構 × 技術示意圖**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**變體 5 — 時間軸 × 折紙**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**變體 6 — 時間軸 × 企業孟菲斯**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## 第 03 節 — baoyu-xhs-images

生成垂直卡片系列（3:4 長寬比），針對小紅書（XHS）、Instagram 及其他社群平台優化。10 種視覺風格 × 8 種版型範本。

**適用時機：** Instagram 貼文、XHS 產品卡片、以產品為主的社群媒體內容。

### 風格變體

**變體 1 — Notion · 預設**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**變體 2 — 粗體 · 預設**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**變體 3 — 粉彩 · 預設**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**變體 4 — Notion · 清單版型**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**變體 5 — 粗體 · 比較**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**變體 6 — 粉彩 · 時間軸**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## 第 04 節 — baoyu-comic

以多種風格創作連環圖：日式漫畫、韓式條漫、教育條漫。支援單格與多格敘事。

**適用時機：** 社群媒體互動內容、以視覺方式說明的產品教學、教育性說明。

### 風格變體

**變體 1 — 漫畫 · 科技產品評測**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**變體 2 — 漫畫 · 趣味三格漫畫**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**變體 3 — 條漫 · 教育性**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**變體 4 — 條漫 · 極簡**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## 第 05 節 — baoyu-article-illustrator

分析文章結構，並為每個段落生成符合情境的插圖。採用「類型 × 風格」雙維度方式。

**適用時機：** 需要內嵌插圖來說明概念的技術部落格文章。

### 風格變體

**變體 1 — 射頻訊號圖**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**變體 2 — 生活場景**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**變體 3 — 規格圖示表**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**變體 4 — 主視覺橫幅**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## 第 06 節 — baoyu-imagine

自由形式的 AI 圖片生成，具備最大創意自由度。無固定版型或風格限制——描述您所需的任何視覺內容。

**適用時機：** 電商產品渲染圖、生活情境攝影替代品、技術爆炸圖、自訂場景生成。

### 風格變體

**變體 1 — 寫實正面視圖**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**變體 2 — 3/4 角度產品渲染**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**變體 3 — 生活場景**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**變體 4 — 技術爆炸圖**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## 如何將本文用作風格參考

在需要生成行銷圖片時，將本文作為查詢表使用。決策流程很簡單：

**1. 這張圖片用於哪個平台？**

| 平台 | 建議技能 | 長寬比 |
|------|---------|--------|
| 部落格文章封面 | `baoyu-cover-image` | 電影寬幅 2.35:1 或寬螢幕 16:9 |
| Instagram / XHS 貼文 | `baoyu-xhs-images` | 3:4 垂直 |
| LinkedIn / Twitter | `baoyu-cover-image`（正方形） | 1:1 |
| 技術文章內嵌圖 | `baoyu-article-illustrator` | 視情況而定 |
| 簡報投影片 | `baoyu-slide-deck` | 16:9 |
| 產品頁面渲染圖 | `baoyu-imagine` | 自訂 |
| 規格概覽貼文 | `baoyu-infographic` | 視情況而定 |
| 社群互動內容 | `baoyu-comic` | 視情況而定 |

**2. 選擇您的風格** — 在本文中找到符合您品牌調性的變體，複製提示詞，並將產品名稱和主要規格替換為您的目標產品。

**3. 在 GitHub Copilot CLI 中執行技能**：

```bash
# 範例 — 生成封面圖
/baoyu-cover-image

# 範例 — 生成 Instagram 卡片
/baoyu-xhs-images

# 範例 — 生成產品渲染圖
/baoyu-imagine
```

**4. 依照技能的引導提示操作** — 每個技能在生成前，都會詢問有關風格、尺寸和內容的澄清問題。

---

## 關於 baoyu-skills

完整的 baoyu-skills 外掛集合可在 GitHub 上取得：

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

本文所有圖片均使用上述技能生成，以 ALFA AWUS036ACM 作為產品主題。所有圖片的完整提示詞參考已記錄於我們的內部工作流程指南中。

想進一步了解本指南全程使用的範例產品 AWUS036ACM 嗎？

{{< button href="/zh-tw/products/alfa/awus036acm/" >}}查看 AWUS036ACM 產品頁面{{< /button >}}
