---
title: "Images de produits générées par l'IA : Une référence de style complète avec baoyu-skills"
description: "Comment nous utilisons le plugin baoyu-skills pour GitHub Copilot CLI pour générer des couvertures de blog, des infographies, des cartes Instagram, des bandes dessinées et des rendus de produits — avec l'ALFA AWUS036ACM comme exemple concret. Une référence de style pratique pour la génération d'images marketing B2B."
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "génération-images-IA", "marketing", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

Chez Yopitek, nous distribuons des produits matériels techniques — adaptateurs WiFi, outils de recherche en sécurité, modules SDR — et créer des visuels marketing cohérents et de haute qualité pour 8 langues a toujours été un défi. Cet article documente comment nous utilisons la collection de plugins **baoyu-skills** pour GitHub Copilot CLI afin de générer des images de produits dans différents formats et styles.

Nous utilisons l'adaptateur WiFi USB **ALFA AWUS036ACM** comme produit d'exemple tout au long de ce guide. Chaque prompt et image présentés ici ont été générés à partir d'une description de cet adaptateur. L'objectif est de fournir une référence de style pratique : lorsque vous aurez besoin d'une image de couverture de produit, d'une carte Instagram ou d'une infographie technique à l'avenir, vous pourrez consulter quel skill et quel style utiliser.

{{< alert "circle-info" >}}
**baoyu-skills** est une collection de plugins open-source pour GitHub Copilot CLI par [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). Elle ajoute 19 skills spécialisés pour la création de contenu, la génération d'images, la traduction et la publication sur les réseaux sociaux — tous accessibles directement depuis votre terminal.
{{< /alert >}}

---

## Référence complète des skills — Les 19 baoyu-skills

La collection comprend 19 skills, organisés en trois types :

- **Type A — Sortie image :** Générer des actifs visuels (couvertures, infographies, bandes dessinées, rendus)
- **Type B — Sortie HTML :** Générer des documents web stylisés
- **Type C — Texte / Utilitaire :** Traduction, formatage, publication sociale, compression

| # | Skill | Type | Objectif | Mots-clés de déclenchement |
|---|-------|------|---------|-----------------|
| 01 | `baoyu-article-illustrator` | Image | Génère automatiquement des illustrations pour chaque section d'un article | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | Image | Crée des planches de BD de type manga/webtoon/éducatif dans plusieurs styles artistiques | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | Utilitaire | Compresse les images en WebP/PNG avec une réduction de taille de 80 à 99 % | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | Image | Génère des images de couverture d'article avec 5 dimensions de design (type, palette, rendu, texte, ambiance) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | Moteur API | Génération de texte et d'images via l'API Gemini Web ; conversations multi-tours, entrée vision | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | Texte | Convertit les tweets et articles X (Twitter) en Markdown avec frontmatter YAML | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | Texte | Formate le texte brut en Markdown structuré avec titres, frontmatter, blocs de code | format markdown · beautify article |
| 08 | `baoyu-image-gen` | Image | Génération d'images IA multi-fournisseurs (OpenAI, Google, DashScope, Replicate) ; mode parallèle | generate / create / draw images |
| 09 | `baoyu-imagine` | Image | Génération d'images IA de forme libre — rendus photoréalistes, scènes de vie, vues éclatées | imagine · create visual |
| 10 | `baoyu-infographic` | Image | Infographies professionnelles : 21 types de mise en page × 20 styles visuels | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Convertit le Markdown en HTML stylisé avec des thèmes WeChat, coloration syntaxique, maths, PlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | Social | Publie des articles et du contenu image-texte sur un compte officiel WeChat | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | Social | Publie sur X (Twitter) avec images/vidéo ; supporte le format long X Articles | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | Image | Génère des images de diapositives à partir du contenu avec un style cohérent sur toutes les pages | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | Texte | Traduction en trois modes : rapide / normal (analyser+traduire) / raffiné (analyser→traduire→réviser→polir) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | Texte | Récupère n'importe quelle URL et la convertit en Markdown via Chrome CDP | save webpage as markdown |
| 17 | `baoyu-xhs-images` | Image | Cartes verticales XHS (Xiaohongshu) : 10 styles × 8 mises en page, optimisées pour Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | Texte | Extrait les transcriptions et sous-titres YouTube en Markdown structuré | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | Social | Publie sur Weibo avec texte, images, tags de sujet, gestion des limites de caractères | 发布微博 · post to weibo |

---

## Section 01 — baoyu-cover-image

Images de couverture d'article dans trois formats : **cinématique (2.35:1)**, **panoramique (16:9)** et **carré (1:1)**. Chaque format supporte plusieurs palettes de couleurs et styles de rendu.

**Quand l'utiliser :** Images d'en-tête de blog, miniatures d'articles, bannières de sites web.

### Variantes de style

**Variante 1 — Cinématique · Marine**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**Variante 2 — Cinématique · Orange**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**Variante 3 — Panoramique · Carbone Sombre**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**Variante 4 — Panoramique · Néon Cyberpunk**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**Variante 5 — Carré · Minimaliste**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**Variante 6 — Carré · Poster Audacieux**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## Section 02 — baoyu-infographic

Combine **21 types de mise en page** avec **20 styles visuels** pour produire des infographies. La mise en page définit la structure (grille bento, hiérarchie, frise chronologique…) ; le style définit le langage visuel (graphisme audacieux, schéma technique, origami…).

**Quand l'utiliser :** Aperçus des spécifications produits, fiches comparatives, articles explicatifs techniques, contenu LinkedIn.

### Variantes de style

**Variante 1 — Grille Bento × Graphisme Audacieux**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**Variante 2 — Grille Bento × Schéma Technique**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**Variante 3 — Couches Hiérarchiques × Graphisme Audacieux**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**Variante 4 — Couches Hiérarchiques × Schéma Technique**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**Variante 5 — Frise Chronologique × Origami**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**Variante 6 — Frise Chronologique × Corporate Memphis**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## Section 03 — baoyu-xhs-images

Génère des séries de cartes verticales (format 3:4) optimisées pour Xiaohongshu (XHS), Instagram et d'autres plateformes sociales. 10 styles visuels × 8 modèles de mise en page.

**Quand l'utiliser :** Posts Instagram, cartes produit XHS, contenu réseaux sociaux axé sur le produit.

### Variantes de style

**Variante 1 — Notion · Par défaut**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**Variante 2 — Audacieux · Par défaut**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**Variante 3 — Pastel · Par défaut**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**Variante 4 — Notion · Mise en page Liste**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**Variante 5 — Audacieux · Comparaison**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**Variante 6 — Pastel · Frise Chronologique**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## Section 04 — baoyu-comic

Crée des arts séquentiels dans plusieurs styles : manga japonais, webtoon coréen, bande dessinée éducative. Supporte à la fois les cases uniques et les récits multi-cases.

**Quand l'utiliser :** Contenu d'engagement pour les réseaux sociaux, tutoriels produits expliqués visuellement, explications éducatives.

### Variantes de style

**Variante 1 — Manga · Revue de produit technique**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**Variante 2 — Manga · Bande dessinée amusante en 3 cases**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**Variante 3 — Webtoon · Éducatif**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**Variante 4 — Webtoon · Minimaliste**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## Section 05 — baoyu-article-illustrator

Analyse la structure d'un article et génère des illustrations contextuelles appropriées pour chaque section. Utilise une approche bidimensionnelle Type × Style.

**Quand l'utiliser :** Articles de blog techniques nécessitant des illustrations intégrées pour expliquer des concepts.

### Variantes de style

**Variante 1 — Schéma de signal RF**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**Variante 2 — Scène de vie**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**Variante 3 — Planche d'icônes de spécifications**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**Variante 4 — Bannière Hero**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## Section 06 — baoyu-imagine

Génération d'images IA de forme libre avec une liberté créative maximale. Aucune contrainte de mise en page ou de style fixe — décrivez tout visuel dont vous avez besoin.

**Quand l'utiliser :** Rendus de produits pour le e-commerce, remplacements de photographies de mode de vie, vues éclatées techniques, génération de scènes personnalisées.

### Variantes de style

**Variante 1 — Vue de face photoréaliste**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**Variante 2 — Rendu de produit sous un angle de 3/4**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**Variante 3 — Scène de vie**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**Variante 4 — Vue éclatée technique**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## Comment utiliser ceci comme référence de style

Utilisez cet article comme un tableau de consultation chaque fois que vous devez générer une image marketing. Le flux de décision est simple :

**1. Pour quelle plateforme cette image est-elle destinée ?**

| Plateforme | Skill recommandé | Format |
|----------|-------------------|--------------|
| Couverture d'article de blog | `baoyu-cover-image` | Cinématique 2.35:1 ou Panoramique 16:9 |
| Post Instagram / XHS | `baoyu-xhs-images` | 3:4 vertical |
| LinkedIn / Twitter | `baoyu-cover-image` (carré) | 1:1 |
| Article technique intégré | `baoyu-article-illustrator` | Varie |
| Diapositive de présentation | `baoyu-slide-deck` | 16:9 |
| Rendu de page produit | `baoyu-imagine` | Personnalisé |
| Post d'aperçu des spécifications | `baoyu-infographic` | Varie |
| Contenu d'engagement social | `baoyu-comic` | Varie |

**2. Choisissez votre style** — trouvez la variante dans cet article qui correspond au ton de votre marque, copiez le prompt et remplacez le nom du produit et les spécifications clés par votre produit cible.

**3. Lancez le skill** dans GitHub Copilot CLI :

```bash
# Exemple — générer une image de couverture
/baoyu-cover-image

# Exemple — générer une carte Instagram
/baoyu-xhs-images

# Exemple — générer un rendu de produit
/baoyu-imagine
```

**4. Suivez les instructions guidées du skill** — chaque skill posera des questions de clarification sur le style, les dimensions et le contenu avant de générer.

---

## À propos de baoyu-skills

La collection complète de plugins baoyu-skills est disponible sur GitHub :

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

Toutes les images de cet article ont été générées à l'aide des skills ci-dessus, avec l'ALFA AWUS036ACM comme sujet du produit. La référence complète des prompts pour toutes les images est documentée dans notre guide de workflow interne.

Vous voulez en savoir plus sur l'AWUS036ACM — le produit utilisé comme exemple tout au long de ce guide ?

{{< button href="/fr/products/alfa/awus036acm/" >}}Voir la page produit AWUS036ACM{{< /button >}}
