---
title: "صور المنتجات بالذكاء الاصطناعي: مرجع شامل للأنماط باستخدام baoyu-skills"
description: "كيف نستخدم إضافة baoyu-skills لواجهة سطر أوامر GitHub Copilot لتوليد أغلفة المدونات، والرسوم البيانية، وبطاقات إنستغرام، والكوميكس، وصور المنتجات — مع محوّل ALFA AWUS036ACM كمثال تطبيقي. مرجع عملي لتوليد صور التسويق B2B."
date: 2026-04-02
author: "benny-lai"
lastmod: 2026-07-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "توليد-الصور-بالذكاء-الاصطناعي", "تسويق", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
faq:
  - question: "ما هي baoyu-skills؟"
    answer: "baoyu-skills هي مجموعة إضافات مفتوحة المصدر لواجهة سطر أوامر GitHub Copilot، توفر 19 مهارة تغطي توليد الصور، وإخراج HTML، والترجمة، والنشر الاجتماعي، جميعها قابلة للاستدعاء مباشرةً من الطرفية."
  - question: "أي مهارة baoyu مناسبة لتوليد صورة غلاف مدوّنة؟"
    answer: "baoyu-cover-image مصمَّمة خصيصاً لأغلفة المقالات، تدعم ثلاث نسب: سينمائي عريض 2.35:1، وشاشة عريضة 16:9، ومربع 1:1، مع مجموعة متنوعة من أنماط الألوان والتصيير."
  - question: "كيف أستخدم baoyu-skills في GitHub Copilot CLI؟"
    answer: "بعد تثبيت مجموعة الإضافات، اكتب أوامراً مثل /baoyu-cover-image أو /baoyu-xhs-images في الطرفية، وستوجّهك المهارة عبر أسئلة توضيحية حول النمط والأبعاد والمحتوى قبل التوليد."
  - question: "ما أنواع مخرجات الصور التي تدعمها baoyu-skills؟"
    answer: "تغطي مخرجات الصور من النوع A أغلفة المقالات، والرسوم البيانية، والكوميكس، والشرائح، وتصيير المنتجات، وبطاقات XHS الرأسية؛ بينما يولّد النوع B صفحات HTML منسّقة؛ ويتعامل النوع C مع الترجمة والنشر الاجتماعي."
  - question: "كيف أطبّق baoyu-skills على منتجي الخاص؟"
    answer: "ابحث في هذه المقالة عن المتغير الذي يتطابق مع نبرة علامتك التجارية، انسخ الموجّه، واستبدل اسم المنتج والمواصفات الرئيسية بمنتجك المستهدف، ثم نفّذ المهارة المناسبة في Copilot CLI."
---

في يوبيتك، نوزّع منتجات الأجهزة التقنية — محوّلات WiFi، وأدوات أبحاث الأمان، ووحدات SDR — وقد كان إنشاء مرئيات تسويقية متسقة وعالية الجودة لثماني لغات تحدياً دائماً. توثّق هذه المقالة كيف نستخدم مجموعة إضافات **baoyu-skills** لواجهة سطر أوامر GitHub Copilot لتوليد صور المنتجات عبر تنسيقات وأنماط مختلفة.

{{< tldr >}}
تقدم baoyu-skills 19 مهارة تغطي مخرجات الصور وHTML والنصوص. تستخدم هذه المقالة ALFA AWUS036ACM كمثال لعرض متغيرات الأنماط والموجّهات وسيناريوهات الاستخدام لست مهارات صور رئيسية، كجدول بحث لتوليد صور التسويق.
{{< /tldr >}}

نستخدم محوّل **ALFA AWUS036ACM** USB WiFi كمنتج توضيحي في هذا الدليل. كل موجّه وصورة معروضة هنا جُوِّلت من وصف هذا المحوّل. الهدف هو مرجع عملي للأنماط: عندما تحتاج مستقبلاً إلى صورة غلاف منتج، أو بطاقة إنستغرام، أو رسم بياني تقني، يمكنك البحث عن المهارة والنمط المناسبَيْن.

{{< alert "circle-info" >}}
**baoyu-skills** هي مجموعة إضافات مفتوحة المصدر لواجهة سطر أوامر GitHub Copilot بقلم [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). تضيف 19 مهارة متخصصة لإنشاء المحتوى، وتوليد الصور، والترجمة، والنشر الاجتماعي — كلها متاحة مباشرةً من طرفيّتك.
{{< /alert >}}

---

## المرجع الشامل للمهارات — جميع مهارات baoyu-skills التسعة عشر

يضم المجموعة 19 مهارة، منظّمة في ثلاثة أنواع:

- **النوع A — مخرجات مرئية:** توليد الأصول البصرية (الأغلفة، الرسوم البيانية، الكوميكس، صور التصيير)
- **النوع B — مخرجات HTML:** توليد مستندات ويب منسّقة
- **النوع C — نصوص / أدوات مساعدة:** الترجمة، التنسيق، النشر الاجتماعي، الضغط

| # | المهارة | النوع | الغرض | الكلمات المفتاحية |
|---|---------|-------|--------|-------------------|
| 01 | `baoyu-article-illustrator` | مرئي | يولّد تلقائياً رسومات توضيحية لكل قسم من المقالة | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | مرئي | ينشئ شرائط كوميكس مانغا/ويبتون/تعليمية بأساليب فنية متعددة | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | أداة مساعدة | يضغط الصور إلى WebP/PNG بتخفيض الحجم 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | مرئي | يولّد صور أغلفة المقالات بخمسة أبعاد تصميمية (النوع، اللوحة، التصيير، النص، المزاج) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | محرك API | توليد النصوص والصور عبر Gemini Web API؛ محادثات متعددة الأدوار، إدخال الرؤية | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | نص | يحوّل تغريدات وقصاصات X (تويتر) إلى Markdown مع مقدمة YAML | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | نص | ينسّق النص العادي إلى Markdown منظّم مع عناوين ومقدمة وكتل كود | format markdown · beautify article |
| 08 | `baoyu-image-gen` | مرئي | توليد صور AI متعدد المزوّدين (OpenAI, Google, DashScope, Replicate)؛ الوضع المتوازي | generate / create / draw images |
| 09 | `baoyu-imagine` | مرئي | توليد صور AI مفتوح النمط — تصييرات فوتوواقعية، مشاهد أسلوب حياة، مناظر مُفكَّكة | imagine · create visual |
| 10 | `baoyu-infographic` | مرئي | رسوم بيانية احترافية: 21 نوع تخطيط × 20 نمط مرئي | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | يحوّل Markdown إلى HTML منسّق مع سمات WeChat، وإبراز الكود، والرياضيات، وPlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | اجتماعي | ينشر المقالات والمحتوى النصي-المرئي إلى الحساب الرسمي على WeChat | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | اجتماعي | ينشر على X (تويتر) مع الصور/الفيديو؛ يدعم تنسيق المقالات المطوّلة X Articles | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | مرئي | يولّد صور شرائح من المحتوى بنمط متسق عبر الشرائح | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | نص | ترجمة ثلاثية الأوضاع: سريعة / عادية (تحليل+ترجمة) / مُحسَّنة (تحليل→ترجمة→مراجعة→صقل) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | نص | يجلب أي URL ويحوّله إلى Markdown باستخدام Chrome CDP | save webpage as markdown |
| 17 | `baoyu-xhs-images` | مرئي | بطاقات رأسية لـ XHS (شياوهونغشو/ليتل ريد بوك): 10 أنماط × 8 تخطيطات، محسَّنة لإنستغرام | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | نص | يستخرج نصوص YouTube والتعليقات كـ Markdown منظّم | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | اجتماعي | ينشر على Weibo مع النص والصور وعلامات الموضوع وإدارة حدود الأحرف | 发布微博 · post to weibo |

---

## القسم 01 — baoyu-cover-image

صور أغلفة المقالات بثلاثة نسب عرض: **سينمائي (2.35:1)**، **شاشة عريضة (16:9)**، و**مربع (1:1)**. كل نسبة تدعم لوحات ألوان وأنماط تصيير متعددة.

**متى تستخدمه:** صور بطولية للمدونات، صور مصغّرة للمقالات، لافتات المواقع.

### متغيرات الأنماط

**المتغير 1 — سينمائي · أزرق داكن**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**المتغير 2 — سينمائي · برتقالي**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**المتغير 3 — شاشة عريضة · كربون داكن**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**المتغير 4 — شاشة عريضة · نيون سايبربنك**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**المتغير 5 — مربع · بسيط**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**المتغير 6 — مربع · ملصق جريء**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## القسم 02 — baoyu-infographic

يجمع بين **21 نوع تخطيط** و**20 نمط مرئي** لإنتاج الرسوم البيانية. يحدد التخطيط البنية (شبكة بينتو، هرمية، جدول زمني…)؛ ويضبط النمط اللغة البصرية (جرافيك جريء، مخطط تقني، أوريغامي…).

**متى تستخدمه:** نظرات عامة على مواصفات المنتج، صفحات المقارنة، منشورات الشرح التقني، محتوى LinkedIn.

### متغيرات الأنماط

**المتغير 1 — شبكة بينتو × جرافيك جريء**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**المتغير 2 — شبكة بينتو × مخطط تقني**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**المتغير 3 — طبقات هرمية × جرافيك جريء**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**المتغير 4 — طبقات هرمية × مخطط تقني**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**المتغير 5 — جدول زمني × أوريغامي**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**المتغير 6 — جدول زمني × ممفيس المؤسسي**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## القسم 03 — baoyu-xhs-images

يولّد سلاسل بطاقات رأسية (نسبة 3:4) محسَّنة لـ Xiaohongshu (XHS)، وإنستغرام، ومنصات التواصل الاجتماعي الأخرى. 10 أنماط مرئية × 8 قوالب تخطيط.

**متى تستخدمه:** منشورات إنستغرام، بطاقات منتجات XHS، محتوى وسائل التواصل الاجتماعي المرتكز على المنتجات.

### متغيرات الأنماط

**المتغير 1 — Notion · افتراضي**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**المتغير 2 — جريء · افتراضي**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**المتغير 3 — باستيل · افتراضي**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**المتغير 4 — Notion · تخطيط قائمة**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**المتغير 5 — جريء · مقارنة**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**المتغير 6 — باستيل · جدول زمني**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## القسم 04 — baoyu-comic

ينشئ فن تسلسلي بأساليب متعددة: مانغا يابانية، ويبتون كوري، شريط تعليمي. يدعم اللوحات المفردة والسرديات متعددة اللوحات.

**متى تستخدمه:** محتوى التفاعل على وسائل التواصل الاجتماعي، دروس المنتجات المشروحة بصرياً، الشروح التعليمية.

### متغيرات الأنماط

**المتغير 1 — مانغا · مراجعة منتج تقني**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**المتغير 2 — مانغا · شريط 3 لوحات مرح**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**المتغير 3 — ويبتون · تعليمي**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**المتغير 4 — ويبتون · بسيط**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## القسم 05 — baoyu-article-illustrator

يحلّل بنية المقالة ويولّد رسومات توضيحية مناسبة للسياق لكل قسم. يستخدم نهجاً ثنائي الأبعاد من النوع × النمط.

**متى تستخدمه:** مقالات المدوّنات التقنية التي تحتاج إلى رسومات مدمجة لشرح المفاهيم.

### متغيرات الأنماط

**المتغير 1 — مخطط إشارة RF**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**المتغير 2 — مشهد أسلوب حياة**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**المتغير 3 — ورقة أيقونات المواصفات**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**المتغير 4 — لافتة بطولية**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## القسم 06 — baoyu-imagine

توليد صور AI مفتوح النمط بأقصى قدر من الحرية الإبداعية. لا قيود ثابتة على التخطيط أو النمط — صِف أي مشهد بصري تحتاجه.

**متى تستخدمه:** صور المنتجات للتجارة الإلكترونية، بدائل التصوير الفوتوغرافي لأسلوب الحياة، المناظر التقنية المُفكَّكة، توليد المشاهد المخصصة.

### متغيرات الأنماط

**المتغير 1 — تصيير واقعي من المقدمة**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**المتغير 2 — تصيير المنتج بزاوية 3/4**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**المتغير 3 — مشهد أسلوب حياة**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**المتغير 4 — منظر تقني مُفكَّك**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## كيفية استخدام هذا كمرجع للأنماط

استخدم هذه المقالة كجدول بحث في كل مرة تحتاج فيها إلى توليد صورة تسويقية. تدفق القرار بسيط:

**1. لأي منصة هذه الصورة؟**

| المنصة | المهارة الموصى بها | نسبة العرض |
|--------|-------------------|-------------|
| غلاف مقالة مدوّنة | `baoyu-cover-image` | سينمائي 2.35:1 أو شاشة عريضة 16:9 |
| منشور إنستغرام / XHS | `baoyu-xhs-images` | رأسي 3:4 |
| LinkedIn / Twitter | `baoyu-cover-image` (مربع) | 1:1 |
| مضمّن في مقالة تقنية | `baoyu-article-illustrator` | متغير |
| شريحة عرض تقديمي | `baoyu-slide-deck` | 16:9 |
| تصيير صفحة منتج | `baoyu-imagine` | مخصص |
| منشور نظرة عامة على المواصفات | `baoyu-infographic` | متغير |
| محتوى تفاعل اجتماعي | `baoyu-comic` | متغير |

**2. اختر نمطك** — ابحث عن المتغير في هذه المقالة الذي يتطابق مع نبرة علامتك التجارية، انسخ الموجّه، واستبدل اسم المنتج والمواصفات الرئيسية بمنتجك المستهدف.

**3. شغّل المهارة** في GitHub Copilot CLI:

```bash
# مثال — توليد صورة غلاف
/baoyu-cover-image

# مثال — توليد بطاقة إنستغرام
/baoyu-xhs-images

# مثال — توليد تصيير منتج
/baoyu-imagine
```

**4. اتبع الموجّهات الإرشادية للمهارة** — ستطرح كل مهارة أسئلة توضيحية حول النمط والأبعاد والمحتوى قبل التوليد.

---

{{< faq >}}

## حول baoyu-skills

مجموعة إضافات baoyu-skills الكاملة متاحة على GitHub:

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

جميع الصور في هذه المقالة جُوِّلت باستخدام المهارات أعلاه، مع ALFA AWUS036ACM كموضوع المنتج. يوثّق دليل سير العمل الداخلي لدينا المرجع الكامل للموجّهات لجميع الصور.

هل تريد معرفة المزيد عن AWUS036ACM — المنتج المستخدم كمثالنا في هذا الدليل؟

{{< button href="/ar/products/alfa/awus036acm/" >}}عرض صفحة منتج AWUS036ACM{{< /button >}}

## المراجع

1. [مستودع baoyu-skills على GitHub](https://github.com/JimLiu/baoyu-skills.git)
2. [وثائق GitHub Copilot CLI الرسمية](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
3. [مواصفات منتج ALFA Network AWUS036ACM](https://www.alfa.com.tw/)
4. [بيانات شريحة MediaTek MT7612U](https://www.mediatek.com/products/networking-and-connectivity)
5. [وثائق OpenAI لتوليد الصور API](https://platform.openai.com/docs/guides/images)
