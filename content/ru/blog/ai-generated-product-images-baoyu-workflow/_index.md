---
title: "Изображения продуктов с помощью ИИ: Полный справочник стилей с baoyu-skills"
description: "Как мы используем плагин baoyu-skills для GitHub Copilot CLI для создания обложек блога, инфографики, карточек Instagram, комиксов и рендеров продуктов — на примере ALFA AWUS036ACM. Практический справочник стилей для генерации маркетинговых изображений B2B."
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "ИИ-генерация-изображений", "маркетинг", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

В Yopitek мы дистрибутируем технические аппаратные продукты — WiFi-адаптеры, инструменты для исследований в области безопасности, SDR-модули — и создание последовательных высококачественных маркетинговых материалов для 8 языков всегда было серьёзной задачей. В этой статье мы документируем, как используем коллекцию плагинов **baoyu-skills** для GitHub Copilot CLI для генерации изображений продуктов в различных форматах и стилях.

В качестве примера продукта на протяжении всего руководства мы используем USB WiFi-адаптер **ALFA AWUS036ACM**. Каждый промпт и изображение, показанные здесь, были сгенерированы на основе описания этого адаптера. Цель — практический справочник стилей: когда вам понадобится обложка для продукта, карточка для Instagram или техническая инфографика, вы сможете найти нужный навык и стиль.

{{< alert "circle-info" >}}
**baoyu-skills** — это коллекция плагинов с открытым исходным кодом для GitHub Copilot CLI от [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). Добавляет 19 специализированных навыков для создания контента, генерации изображений, перевода и публикации в социальных сетях — всё доступно прямо из терминала.
{{< /alert >}}

---

## Полный справочник навыков — Все 19 baoyu-skills

В коллекции 19 навыков, разделённых на три типа:

- **Тип A — Графический вывод:** Создание визуальных материалов (обложки, инфографика, комиксы, рендеры)
- **Тип B — HTML-вывод:** Создание стилизованных веб-документов
- **Тип C — Текст / Утилиты:** Перевод, форматирование, публикация в соцсетях, сжатие

| # | Навык | Тип | Назначение | Ключевые слова |
|---|-------|-----|------------|----------------|
| 01 | `baoyu-article-illustrator` | Изображение | Автоматически генерирует иллюстрации для каждого раздела статьи | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | Изображение | Создаёт комиксы в стиле манга/вебтун/образовательные в нескольких художественных стилях | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | Утилита | Сжимает изображения до WebP/PNG с уменьшением размера на 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | Изображение | Генерирует обложки статей по 5 дизайн-измерениям (тип, палитра, рендеринг, текст, настроение) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | API-движок | Генерация текста и изображений через Gemini Web API; многоходовые диалоги, визуальный ввод | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | Текст | Конвертирует твиты и статьи X (Twitter) в Markdown с YAML front matter | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | Текст | Форматирует обычный текст в структурированный Markdown с заголовками, frontmatter, блоками кода | format markdown · beautify article |
| 08 | `baoyu-image-gen` | Изображение | Мультипровайдерная ИИ-генерация изображений (OpenAI, Google, DashScope, Replicate); параллельный режим | generate / create / draw images |
| 09 | `baoyu-imagine` | Изображение | Свободная ИИ-генерация изображений — фотореалистичные рендеры, lifestyle-сцены, взрыв-схемы | imagine · create visual |
| 10 | `baoyu-infographic` | Изображение | Профессиональная инфографика: 21 тип макета × 20 визуальных стилей | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Конвертирует Markdown в стилизованный HTML с темами WeChat, подсветкой кода, математикой, PlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | Социальные | Публикует статьи и контент «изображение+текст» в официальный аккаунт WeChat | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | Социальные | Публикует в X (Twitter) с изображениями/видео; поддерживает длинный формат X Articles | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | Изображение | Генерирует слайды из контента с единым стилем по всей презентации | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | Текст | Перевод в трёх режимах: быстрый / стандартный (анализ+перевод) / улучшенный (анализ→перевод→проверка→шлифовка) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | Текст | Получает любой URL и конвертирует в Markdown с помощью Chrome CDP | save webpage as markdown |
| 17 | `baoyu-xhs-images` | Изображение | Вертикальные карточки XHS (Xiaohongshu/Little Red Book): 10 стилей × 8 макетов, оптимизированы для Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | Текст | Извлекает транскрипты и субтитры YouTube в виде структурированного Markdown | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | Социальные | Публикует на Weibo с текстом, изображениями, тематическими тегами и учётом лимита символов | 发布微博 · post to weibo |

---

## Раздел 01 — baoyu-cover-image

Обложки статей в трёх форматах: **кинематографический (2.35:1)**, **широкоэкранный (16:9)** и **квадратный (1:1)**. Каждый формат поддерживает несколько цветовых палитр и стилей рендеринга.

**Когда использовать:** Главные изображения публикаций блога, миниатюры статей, баннеры сайта.

### Варианты стилей

**Вариант 1 — Кинематографический · Тёмно-синий**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**Вариант 2 — Кинематографический · Оранжевый**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**Вариант 3 — Широкоэкранный · Тёмный карбон**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**Вариант 4 — Широкоэкранный · Неоновый киберпанк**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**Вариант 5 — Квадратный · Минимализм**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**Вариант 6 — Квадратный · Яркий постер**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## Раздел 02 — baoyu-infographic

Объединяет **21 тип макета** с **20 визуальными стилями** для создания инфографики. Макет определяет структуру (сетка бенто, иерархия, временная шкала…); стиль задаёт визуальный язык (жирный графический, технический схемный, оригами…).

**Когда использовать:** Обзоры технических характеристик продукта, сравнительные таблицы, технические объяснительные посты, контент для LinkedIn.

### Варианты стилей

**Вариант 1 — Сетка бенто × Жирный графический**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**Вариант 2 — Сетка бенто × Технический схемный**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**Вариант 3 — Иерархические слои × Жирный графический**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**Вариант 4 — Иерархические слои × Технический схемный**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**Вариант 5 — Временная шкала × Оригами**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**Вариант 6 — Временная шкала × Corporate Memphis**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## Раздел 03 — baoyu-xhs-images

Создаёт серии вертикальных карточек (соотношение сторон 3:4), оптимизированных для Xiaohongshu (XHS), Instagram и других социальных платформ. 10 визуальных стилей × 8 шаблонов макетов.

**Когда использовать:** Посты в Instagram, карточки продуктов XHS, контент для соцсетей, ориентированный на продукты.

### Варианты стилей

**Вариант 1 — Notion · По умолчанию**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**Вариант 2 — Жирный · По умолчанию**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**Вариант 3 — Пастель · По умолчанию**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**Вариант 4 — Notion · Макет списка**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**Вариант 5 — Жирный · Сравнение**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**Вариант 6 — Пастель · Временная шкала**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## Раздел 04 — baoyu-comic

Создаёт последовательное искусство в нескольких стилях: японская манга, корейский вебтун, образовательный стрип. Поддерживает как одиночные панели, так и многопанельные нарративы.

**Когда использовать:** Вовлекающий контент для соцсетей, визуально объяснённые инструкции по продуктам, образовательные разборы.

### Варианты стилей

**Вариант 1 — Манга · Технический обзор продукта**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**Вариант 2 — Манга · Весёлый трёхпанельный стрип**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**Вариант 3 — Вебтун · Образовательный**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**Вариант 4 — Вебтун · Минимализм**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## Раздел 05 — baoyu-article-illustrator

Анализирует структуру статьи и генерирует контекстно-подходящие иллюстрации для каждого раздела. Использует двумерный подход Тип × Стиль.

**Когда использовать:** Технические статьи блога, которым нужны встроенные иллюстрации для объяснения концепций.

### Варианты стилей

**Вариант 1 — Схема радиочастотного сигнала**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**Вариант 2 — Lifestyle-сцена**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**Вариант 3 — Лист иконок характеристик**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**Вариант 4 — Главный баннер**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## Раздел 06 — baoyu-imagine

Свободная ИИ-генерация изображений с максимальной творческой свободой. Никаких фиксированных ограничений по макету или стилю — опишите любой нужный вам визуал.

**Когда использовать:** Рендеры продуктов для e-commerce, замена lifestyle-фотографии, технические взрыв-схемы, генерация кастомных сцен.

### Варианты стилей

**Вариант 1 — Фотореалистичный рендер спереди**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**Вариант 2 — Рендер продукта под углом 3/4**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**Вариант 3 — Lifestyle-сцена**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**Вариант 4 — Техническая взрыв-схема**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## Как использовать это как справочник стилей

Используйте эту статью как таблицу поиска каждый раз, когда нужно сгенерировать маркетинговое изображение. Логика выбора проста:

**1. Для какой платформы предназначено это изображение?**

| Платформа | Рекомендуемый навык | Соотношение сторон |
|-----------|--------------------|--------------------|
| Обложка статьи блога | `baoyu-cover-image` | Кинематографический 2.35:1 или Широкоэкранный 16:9 |
| Пост Instagram / XHS | `baoyu-xhs-images` | Вертикальный 3:4 |
| LinkedIn / Twitter | `baoyu-cover-image` (квадрат) | 1:1 |
| Встроенная иллюстрация в статье | `baoyu-article-illustrator` | Варьируется |
| Слайд презентации | `baoyu-slide-deck` | 16:9 |
| Рендер страницы продукта | `baoyu-imagine` | Произвольный |
| Пост с обзором характеристик | `baoyu-infographic` | Варьируется |
| Вовлекающий контент для соцсетей | `baoyu-comic` | Варьируется |

**2. Выберите стиль** — найдите вариант в этой статье, соответствующий тональности вашего бренда, скопируйте промпт и замените название продукта и ключевые характеристики на данные вашего продукта.

**3. Запустите навык** в GitHub Copilot CLI:

```bash
# Пример — создать обложку
/baoyu-cover-image

# Пример — создать карточку для Instagram
/baoyu-xhs-images

# Пример — создать рендер продукта
/baoyu-imagine
```

**4. Следуйте подсказкам навыка** — каждый навык задаст уточняющие вопросы о стиле, размерах и содержании перед началом генерации.

---

## О baoyu-skills

Полная коллекция плагинов baoyu-skills доступна на GitHub:

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

Все изображения в этой статье были сгенерированы с использованием перечисленных выше навыков, при этом ALFA AWUS036ACM использовался в качестве продукта-субъекта. Полный справочник промптов для всех изображений задокументирован в нашем внутреннем руководстве по рабочему процессу.

Хотите узнать больше об AWUS036ACM — продукте, использованном в качестве примера на протяжении всего руководства?

{{< button href="/ru/products/alfa/awus036acm/" >}}Перейти на страницу продукта AWUS036ACM{{< /button >}}
