---
title: "KI-generierte Produktbilder: Eine vollständige Stilreferenz mit baoyu-skills"
description: "Wie wir das baoyu-skills Plugin für GitHub Copilot CLI nutzen, um Blog-Cover, Infografiken, Instagram-Karten, Comics und Produkt-Renders zu erstellen – mit dem ALFA AWUS036ACM als Praxisbeispiel. Eine praktische Stilreferenz für die B2B-Marketing-Bilderstellung."
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "KI-Bilderzeugung", "Marketing", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

Bei Yopitek vertreiben wir technische Hardware-Produkte – WiFi-Adapter, Sicherheitsforschungs-Tools, SDR-Module – und die Erstellung konsistenter, hochwertiger Marketing-Visuals für 8 Sprachen war schon immer eine Herausforderung. Dieser Artikel dokumentiert, wie wir die **baoyu-skills** Plugin-Sammlung für GitHub Copilot CLI nutzen, um Produktbilder in verschiedenen Formaten und Stilen zu generieren.

Wir verwenden den **ALFA AWUS036ACM** USB-WiFi-Adapter als Beispielprodukt in diesem Leitfaden. Jedes hier gezeigte Prompt und Bild wurde aus einer Beschreibung dieses Adapters generiert. Ziel ist eine praktische Stilreferenz: Wenn Sie in Zukunft ein Produkt-Cover-Bild, eine Instagram-Karte oder eine technische Infografik benötigen, können Sie nachschlagen, welchen Skill und Stil Sie verwenden sollten.

{{< alert "circle-info" >}}
**baoyu-skills** ist eine Open-Source-Plugin-Sammlung für GitHub Copilot CLI von [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). Sie fügt 19 spezialisierte Skills für die Erstellung von Inhalten, Bilderzeugung, Übersetzung und Social Publishing hinzu – alle direkt über Ihr Terminal zugänglich.
{{< /alert >}}

---

## Vollständige Skills-Referenz – Alle 19 baoyu-skills

Die Sammlung umfasst 19 Skills, die in drei Typen unterteilt sind:

- **Typ A — Bild-Ausgabe:** Erzeugung visueller Assets (Cover, Infografiken, Comics, Renders)
- **Typ B — HTML-Ausgabe:** Erzeugung gestalteter Web-Dokumente
- **Typ C — Text / Utility:** Übersetzung, Formatierung, Social Publishing, Komprimierung

| # | Skill | Typ | Zweck | Schlüsselwörter (Trigger) |
|---|-------|------|---------|-----------------|
| 01 | `baoyu-article-illustrator` | Bild | Erzeugt automatisch Illustrationen für jeden Abschnitt eines Artikels | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | Bild | Erstellt Manga/Webtoon/pädagogische Comic-Strips in verschiedenen Kunststilen | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | Utility | Komprimiert Bilder zu WebP/PNG mit 80–99 % Größenreduzierung | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | Bild | Erzeugt Artikel-Cover-Bilder mit 5 Design-Dimensionen (Typ, Palette, Rendering, Text, Stimmung) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | API-Engine | Text- und Bilderzeugung über die Gemini Web API; mehrstufige Konversationen, Vision-Input | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | Text | Konvertiert X (Twitter) Tweets und Artikel in Markdown mit YAML-Frontmatter | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | Text | Formatiert reinen Text in strukturiertes Markdown mit Überschriften, Frontmatter, Codeblöcken | format markdown · beautify article |
| 08 | `baoyu-image-gen` | Bild | Multi-Provider KI-Bilderzeugung (OpenAI, Google, DashScope, Replicate); Parallel-Modus | generate / create / draw images |
| 09 | `baoyu-imagine` | Bild | Freiform KI-Bilderzeugung – fotorealistische Renders, Lifestyle-Szenen, Explosionszeichnungen | imagine · create visual |
| 10 | `baoyu-infographic` | Bild | Professionelle Infografiken: 21 Layout-Typen × 20 visuelle Stile | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Konvertiert Markdown in gestaltetes HTML mit WeChat-Themen, Syntax-Highlighting, Mathe, PlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | Social | Veröffentlicht Artikel und Bild-Text-Inhalte auf dem WeChat Official Account | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | Social | Veröffentlicht auf X (Twitter) mit Bildern/Video; unterstützt X Articles Langform-Format | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | Bild | Erzeugt Slide-Deck-Bilder aus Inhalten mit konsistentem Stil über alle Folien | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | Text | Drei-Modus-Übersetzung: Schnell / Normal (Analyse+Übersetzung) / Verfeinert (Analyse→Übersetzung→Review→Feinschliff) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | Text | Ruft jede URL ab und konvertiert sie mit Chrome CDP in Markdown | save webpage as markdown |
| 17 | `baoyu-xhs-images` | Bild | Vertikale XHS-Karten (Xiaohongshu/Little Red Book): 10 Stile × 8 Layouts, optimiert für Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | Text | Extrahiert YouTube-Transkripte und Untertitel als strukturiertes Markdown | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | Social | Veröffentlicht auf Weibo mit Text, Bildern, Topic-Tags, Handhabung von Zeichenlimits | 发布微博 · post to weibo |

---

## Abschnitt 01 — baoyu-cover-image

Artikel-Cover-Bilder in drei Seitenverhältnissen: **Cinematic (2,35:1)**, **Widescreen (16:9)** und **Quadratisch (1:1)**. Jedes Verhältnis unterstützt mehrere Farppaletten und Rendering-Stile.

**Wann zu verwenden:** Blog-Post-Hero-Bilder, Artikel-Thumbnails, Website-Banner.

### Stil-Varianten

**Variante 1 — Cinematic · Navy**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**Variante 2 — Cinematic · Orange**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**Variante 3 — Widescreen · Dark Carbon**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**Variante 4 — Widescreen · Neon Cyberpunk**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**Variante 5 — Quadratisch · Minimal**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**Variante 6 — Quadratisch · Bold Poster**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## Abschnitt 02 — baoyu-infographic

Kombiniert **21 Layout-Typen** mit **20 visuellen Stilen**, um Infografiken zu erstellen. Das Layout definiert die Struktur (Bento-Grid, Hierarchie, Zeitachse…); der Stil legt die visuelle Sprache fest (Bold Graphic, technisches Schema, Origami…).

**Wann zu verwenden:** Produkt-Spezifikationsübersichten, Vergleichstabellen, technische Erklärungs-Posts, LinkedIn-Inhalte.

### Stil-Varianten

**Variante 1 — Bento Grid × Bold Graphic**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**Variante 2 — Bento Grid × Technical Schematic**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**Variante 3 — Hierarchical Layers × Bold Graphic**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**Variante 4 — Hierarchical Layers × Technical Schematic**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**Variante 5 — Zeitachse × Origami**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**Variante 6 — Zeitachse × Corporate Memphis**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## Abschnitt 03 — baoyu-xhs-images

Erzeugt vertikale Kartenserien (Seitenverhältnis 3:4), die für Xiaohongshu (XHS), Instagram und andere soziale Plattformen optimiert sind. 10 visuelle Stile × 8 Layout-Vorlagen.

**Wann zu verwenden:** Instagram-Posts, XHS-Produktkarten, produktfokussierte Social-Media-Inhalte.

### Stil-Varianten

**Variante 1 — Notion · Standard**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**Variante 2 — Bold · Standard**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**Variante 3 — Pastel · Standard**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM開箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**Variante 4 — Notion · Listen-Layout**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**Variante 5 — Bold · Vergleich**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**Variante 6 — Pastel · Zeitachse**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## Abschnitt 04 — baoyu-comic

Erzeugt sequenzielle Kunst in mehreren Stilen: Japanischer Manga, Koreanischer Webtoon, pädagogischer Strip. Unterstützt sowohl Einzelpanels als auch mehrstufige Erzählungen.

**Wann zu verwenden:** Social-Media-Inhalte zur Interaktion, visuell erklärte Produkt-Tutorials, pädagogische Erklärungen.

### Stil-Varianten

**Variante 1 — Manga · Tech-Produkt-Review**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**Variante 2 — Manga · Lustiger 3-Panel-Strip**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**Variante 3 — Webtoon · Pädagogisch**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**Variante 4 — Webtoon · Minimalistisch**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## Abschnitt 05 — baoyu-article-illustrator

Analysiert die Struktur eines Artikels und erzeugt kontextgerechte Illustrationen für jeden Abschnitt. Verwendet einen Typ-×-Stil-zweidimensionalen Ansatz.

**Wann zu verwenden:** Technische Blog-Artikel, die Inline-Illustrationen benötigen, um Konzepte zu erklären.

### Stil-Varianten

**Variante 1 — RF-Signaldiagramm**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**Variante 2 — Lifestyle-Szene**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**Variante 3 — Spezifikations-Icon-Sheet**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**Variante 4 — Hero-Banner**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## Abschnitt 06 — baoyu-imagine

Freiform KI-Bilderzeugung mit maximaler kreativer Freiheit. Keine festen Layout- oder Stilbeschränkungen – beschreiben Sie jedes Bild, das Sie benötigen.

**Wann zu verwenden:** Produkt-Renders für den E-Commerce, Ersatz für Lifestyle-Fotografie, technische Explosionszeichnungen, benutzerdefinierte Szenenerzeugung.

### Stil-Varianten

**Variante 1 — Fotorealistische Frontansicht**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**Variante 2 — 3/4-Winkel Produkt-Render**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**Variante 3 — Lifestyle-Szene**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**Variante 4 — Technische Explosionszeichnung**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## Verwendung als Stilreferenz

Nutzen Sie diesen Artikel als Nachschlagetabelle, wann immer Sie ein Marketing-Bild erstellen müssen. Der Entscheidungsfluss ist einfach:

**1. Für welche Plattform ist dieses Bild bestimmt?**

| Plattform | Empfohlener Skill | Seitenverhältnis |
|----------|-------------------|--------------|
| Blog-Artikel-Cover | `baoyu-cover-image` | Cinematic 2,35:1 oder Widescreen 16:9 |
| Instagram / XHS Post | `baoyu-xhs-images` | 3:4 vertikal |
| LinkedIn / Twitter | `baoyu-cover-image` (quadratisch) | 1:1 |
| In technischem Artikel | `baoyu-article-illustrator` | Variiert |
| Präsentationsfolie | `baoyu-slide-deck` | 16:9 |
| Produktseiten-Render | `baoyu-imagine` | Benutzerdefiniert |
| Spezifikationsübersicht | `baoyu-infographic` | Variiert |
| Social-Media-Interaktion | `baoyu-comic` | Variiert |

**2. Wählen Sie Ihren Stil** — finden Sie die Variante in diesem Artikel, die zu Ihrem Marken-Ton passt, kopieren Sie das Prompt und ersetzen Sie den Produktnamen und die wichtigsten Spezifikationen durch Ihr Zielprodukt.

**3. Führen Sie den Skill aus** in GitHub Copilot CLI:

```bash
# Beispiel — erzeugen Sie ein Cover-Bild
/baoyu-cover-image

# Beispiel — erzeugen Sie eine Instagram-Karte
/baoyu-xhs-images

# Beispiel — erzeugen Sie einen Produkt-Render
/baoyu-imagine
```

**4. Folgen Sie den geführten Prompts des Skills** — jeder Skill stellt klärende Fragen zu Stil, Abmessungen und Inhalt vor der Erzeugung.

---

## Über baoyu-skills

Die vollständige baoyu-skills Plugin-Sammlung ist auf GitHub verfügbar:

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

Alle Bilder in diesem Artikel wurden mit den oben genannten Skills generiert, wobei der ALFA AWUS036ACM das Produktsubjekt war. Die vollständige Prompt-Referenz für alle Bilder ist in unserem internen Workflow-Leitfaden dokumentiert.

Möchten Sie mehr über den AWUS036ACM erfahren – das Produkt, das in diesem Leitfaden als Beispiel verwendet wurde?

{{< button href="/de/products/alfa/awus036acm/" >}}AWUS036ACM Produktseite anzeigen{{< /button >}}
