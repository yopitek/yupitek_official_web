---
title: "AI 生成产品图片：使用 baoyu-skills 的完整风格参考指南"
description: "我们如何使用 GitHub Copilot CLI 的 baoyu-skills 插件，生成博客封面、信息图表、Instagram 卡片、漫画及产品渲染图——以 ALFA AWUS036ACM 为实际案例。B2B 营销图片生成的实用风格参考。"
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "AI-image-generation", "营销", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

在 Yopitek，我们代理技术硬件产品——WiFi 网卡、安全研究工具、SDR 模块——为 8 种语言持续产出高质量的营销视觉素材一直是一大挑战。本文记录我们如何使用 GitHub Copilot CLI 的 **baoyu-skills** 插件集合，跨不同格式与风格生成产品图片。

我们在本指南中以 **ALFA AWUS036ACM** USB WiFi 网卡作为示例产品。此处展示的每个提示词与图片，均由该网卡的描述生成。目标是建立一份实用的风格参考：当您未来需要产品封面图、Instagram 卡片或技术信息图表时，可以查阅应使用哪种技能与风格。

{{< alert "circle-info" >}}
**baoyu-skills** 是由 [@JimLiu](https://github.com/JimLiu/baoyu-skills.git) 为 GitHub Copilot CLI 开发的开源插件集合。它新增了 19 项专业技能，涵盖内容创作、图片生成、翻译及社交发布——全部可直接从终端访问。
{{< /alert >}}

---

## 完整技能参考——所有 19 个 baoyu-skills

此集合共有 19 项技能，分为三种类型：

- **Type A — Image Output：** 生成视觉素材（封面、信息图表、漫画、渲染图）
- **Type B — HTML Output：** 生成样式化网页文档
- **Type C — Text / Utility：** 翻译、格式化、社交发布、压缩

| # | 技能 | 类型 | 用途 | 触发关键词 |
|---|------|------|------|-----------|
| 01 | `baoyu-article-illustrator` | 图片 | 自动为文章各段落生成插图 | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | 图片 | 以多种画风创作漫画/条漫/教育漫画 | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | 工具 | 将图片压缩为 WebP/PNG，缩小 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | 图片 | 以 5 个设计维度生成文章封面图（类型、色板、渲染、文字、情境） | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | API 引擎 | 通过 Gemini Web API 生成文字与图片；多轮对话、视觉输入 | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | 文字 | 将 X (Twitter) 推文和文章转换为含 YAML front matter 的 Markdown | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | 文字 | 将纯文字格式化为含标题、frontmatter、代码块的结构化 Markdown | format markdown · beautify article |
| 08 | `baoyu-image-gen` | 图片 | 多供应商 AI 图片生成（OpenAI、Google、DashScope、Replicate）；并行模式 | generate / create / draw images |
| 09 | `baoyu-imagine` | 图片 | 自由形式 AI 图片生成——写实渲染、生活场景、爆炸图 | imagine · create visual |
| 10 | `baoyu-infographic` | 图片 | 专业信息图表：21 种版式 × 20 种视觉风格 | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | 将 Markdown 转换为含微信主题、代码高亮、数学、PlantUML 的样式化 HTML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | 社交 | 发布文章与图文内容至微信公众号 | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | 社交 | 发布至 X (Twitter)，支持图片/视频；支持 X Articles 长文格式 | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | 图片 | 从内容生成风格一致的幻灯片图片 | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | 文字 | 三种翻译模式：快速/普通（分析＋翻译）/精翻（分析→翻译→校对→润色） | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | 文字 | 使用 Chrome CDP 抓取任意 URL 并转换为 Markdown | save webpage as markdown |
| 17 | `baoyu-xhs-images` | 图片 | 小红书竖版卡片：10 种风格 × 8 种版式，适用于 Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | 文字 | 将 YouTube 字幕提取为结构化 Markdown | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | 社交 | 发布至微博，支持文字、图片、话题标签、字数限制处理 | 发布微博 · post to weibo |

---

## 第 01 节 — baoyu-cover-image

以三种长宽比生成文章封面图：**电影宽幅 (2.35:1)**、**宽屏 (16:9)** 和 **正方形 (1:1)**。每种比例支持多种配色方案与渲染风格。

**适用场景：** 博客文章主视觉、文章缩略图、网站横幅。

### 风格变体

**变体 1 — 电影宽幅 · 深蓝**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**变体 2 — 电影宽幅 · 橙色**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**变体 3 — 宽屏 · 暗碳**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**变体 4 — 宽屏 · 霓虹赛博朋克**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**变体 5 — 正方形 · 极简**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**变体 6 — 正方形 · 大胆海报**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## 第 02 节 — baoyu-infographic

结合 **21 种版式** 与 **20 种视觉风格** 制作信息图表。版式定义结构（便当格、层级架构、时间轴…）；风格设定视觉语言（大胆图形、技术示意图、折纸…）。

**适用场景：** 产品规格概览、对比表、技术说明帖子、LinkedIn 内容。

### 风格变体

**变体 1 — 便当格 × 大胆图形**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**变体 2 — 便当格 × 技术示意图**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**变体 3 — 层级架构 × 大胆图形**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**变体 4 — 层级架构 × 技术示意图**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**变体 5 — 时间轴 × 折纸**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**变体 6 — 时间轴 × 企业孟菲斯**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## 第 03 节 — baoyu-xhs-images

生成竖版卡片系列（3:4 长宽比），针对小红书（XHS）、Instagram 及其他社交平台优化。10 种视觉风格 × 8 种版式模板。

**适用场景：** Instagram 帖子、XHS 产品卡片、以产品为主的社交媒体内容。

### 风格变体

**变体 1 — Notion · 默认**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**变体 2 — 粗体 · 默认**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**变体 3 — 粉彩 · 默认**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**变体 4 — Notion · 清单版式**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**变体 5 — 粗体 · 对比**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**变体 6 — 粉彩 · 时间轴**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## 第 04 节 — baoyu-comic

以多种风格创作连环漫画：日式漫画、韩式条漫、教育条漫。支持单格与多格叙事。

**适用场景：** 社交媒体互动内容、以视觉方式呈现的产品教程、教育性说明。

### 风格变体

**变体 1 — 漫画 · 科技产品评测**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**变体 2 — 漫画 · 趣味三格漫画**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**变体 3 — 条漫 · 教育性**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**变体 4 — 条漫 · 极简**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## 第 05 节 — baoyu-article-illustrator

分析文章结构，并为每个段落生成符合情境的插图。采用「类型 × 风格」双维度方式。

**适用场景：** 需要内嵌插图来说明概念的技术博客文章。

### 风格变体

**变体 1 — 射频信号图**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**变体 2 — 生活场景**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**变体 3 — 规格图标表**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**变体 4 — 主视觉横幅**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## 第 06 节 — baoyu-imagine

自由形式的 AI 图片生成，具备最大创意自由度。无固定版式或风格限制——描述您所需的任何视觉内容。

**适用场景：** 电商产品渲染图、生活情境摄影替代品、技术爆炸图、自定义场景生成。

### 风格变体

**变体 1 — 写实正面视图**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**变体 2 — 3/4 角度产品渲染**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**变体 3 — 生活场景**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**变体 4 — 技术爆炸图**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## 如何将本文用作风格参考

在需要生成营销图片时，将本文作为查询表使用。决策流程很简单：

**1. 这张图片用于哪个平台？**

| 平台 | 建议技能 | 长宽比 |
|------|---------|--------|
| 博客文章封面 | `baoyu-cover-image` | 电影宽幅 2.35:1 或宽屏 16:9 |
| Instagram / XHS 帖子 | `baoyu-xhs-images` | 3:4 竖版 |
| LinkedIn / Twitter | `baoyu-cover-image`（正方形） | 1:1 |
| 技术文章内嵌图 | `baoyu-article-illustrator` | 视情况而定 |
| 演示幻灯片 | `baoyu-slide-deck` | 16:9 |
| 产品页面渲染图 | `baoyu-imagine` | 自定义 |
| 规格概览帖子 | `baoyu-infographic` | 视情况而定 |
| 社交互动内容 | `baoyu-comic` | 视情况而定 |

**2. 选择您的风格** — 在本文中找到符合您品牌调性的变体，复制提示词，并将产品名称和主要规格替换为您的目标产品。

**3. 在 GitHub Copilot CLI 中运行技能**：

```bash
# 示例 — 生成封面图
/baoyu-cover-image

# 示例 — 生成 Instagram 卡片
/baoyu-xhs-images

# 示例 — 生成产品渲染图
/baoyu-imagine
```

**4. 按照技能的引导提示操作** — 每个技能在生成前，都会询问有关风格、尺寸和内容的澄清问题。

---

## 关于 baoyu-skills

完整的 baoyu-skills 插件集合可在 GitHub 上获取：

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

本文所有图片均使用上述技能生成，以 ALFA AWUS036ACM 作为产品主题。所有图片的完整提示词参考已记录于我们的内部工作流程指南中。

想进一步了解本指南全程使用的示例产品 AWUS036ACM 吗？

{{< button href="/zh-cn/products/alfa/awus036acm/" >}}查看 AWUS036ACM 产品页面{{< /button >}}
