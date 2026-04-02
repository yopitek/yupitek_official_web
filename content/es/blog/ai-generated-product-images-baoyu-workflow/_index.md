---
title: "Imágenes de Productos con IA: Una Referencia Completa de Estilos con baoyu-skills"
description: "Cómo usamos el plugin baoyu-skills para GitHub Copilot CLI para generar portadas de blog, infografías, tarjetas de Instagram, cómics y renders de productos — con el ALFA AWUS036ACM como ejemplo real. Una referencia práctica de estilos para la generación de imágenes de marketing B2B."
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "generación-de-imágenes-IA", "marketing", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
---

En Yopitek, distribuimos productos de hardware técnico — adaptadores WiFi, herramientas de investigación en seguridad, módulos SDR — y crear visuales de marketing consistentes y de alta calidad para 8 idiomas siempre ha sido un desafío. Este artículo documenta cómo usamos la colección de plugins **baoyu-skills** para GitHub Copilot CLI para generar imágenes de productos en diferentes formatos y estilos.

Usamos el adaptador USB WiFi **ALFA AWUS036ACM** como producto de ejemplo a lo largo de esta guía. Cada prompt e imagen mostrada aquí fue generada a partir de una descripción de este adaptador. El objetivo es una referencia práctica de estilos: cuando necesites una imagen de portada de producto, una tarjeta de Instagram, o una infografía técnica en el futuro, puedes consultar qué skill y estilo usar.

{{< alert "circle-info" >}}
**baoyu-skills** es una colección de plugins de código abierto para GitHub Copilot CLI creada por [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). Agrega 19 skills especializadas para creación de contenido, generación de imágenes, traducción y publicación en redes sociales — todas accesibles directamente desde tu terminal.
{{< /alert >}}

---

## Referencia Completa de Skills — Las 19 baoyu-skills

La colección tiene 19 skills, organizadas en tres tipos:

- **Tipo A — Salida de Imágenes:** Genera activos visuales (portadas, infografías, cómics, renders)
- **Tipo B — Salida HTML:** Genera documentos web con estilo
- **Tipo C — Texto / Utilidad:** Traducción, formateo, publicación social, compresión

| # | Skill | Tipo | Propósito | Palabras Clave |
|---|-------|------|-----------|----------------|
| 01 | `baoyu-article-illustrator` | Imagen | Genera automáticamente ilustraciones para cada sección de un artículo | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | Imagen | Crea tiras cómicas manga/webtoon/educativas en múltiples estilos artísticos | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | Utilidad | Comprime imágenes a WebP/PNG con una reducción de tamaño del 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | Imagen | Genera imágenes de portada con 5 dimensiones de diseño (tipo, paleta, renderizado, texto, mood) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | Motor API | Generación de texto e imágenes vía Gemini Web API; conversaciones multi-turno, entrada de visión | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | Texto | Convierte tweets y artículos de X (Twitter) a Markdown con front matter YAML | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | Texto | Formatea texto plano en Markdown estructurado con encabezados, frontmatter, bloques de código | format markdown · beautify article |
| 08 | `baoyu-image-gen` | Imagen | Generación de imágenes IA multi-proveedor (OpenAI, Google, DashScope, Replicate); modo paralelo | generate / create / draw images |
| 09 | `baoyu-imagine` | Imagen | Generación libre de imágenes IA — renders fotorrealistas, escenas de lifestyle, vistas explosionadas | imagine · create visual |
| 10 | `baoyu-infographic` | Imagen | Infografías profesionales: 21 tipos de diseño × 20 estilos visuales | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Convierte Markdown a HTML con estilo con temas WeChat, resaltado de código, matemáticas, PlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | Social | Publica artículos y contenido imagen-texto en la Cuenta Oficial de WeChat | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | Social | Publica en X (Twitter) con imágenes/video; soporta el formato X Articles de formato largo | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | Imagen | Genera imágenes de diapositivas desde contenido con estilo consistente | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | Texto | Traducción en tres modos: rápida / normal (análisis+traducción) / refinada (análisis→traducción→revisión→pulido) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | Texto | Obtiene cualquier URL y la convierte a Markdown usando Chrome CDP | save webpage as markdown |
| 17 | `baoyu-xhs-images` | Imagen | Tarjetas verticales XHS (Xiaohongshu/Little Red Book): 10 estilos × 8 layouts, optimizadas para Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | Texto | Extrae transcripciones y subtítulos de YouTube como Markdown estructurado | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | Social | Publica en Weibo con texto, imágenes, etiquetas de tema y manejo del límite de caracteres | 发布微博 · post to weibo |

---

## Sección 01 — baoyu-cover-image

Imágenes de portada de artículos en tres relaciones de aspecto: **cinemático (2.35:1)**, **pantalla ancha (16:9)**, y **cuadrado (1:1)**. Cada relación admite múltiples paletas de colores y estilos de renderizado.

**Cuándo usar:** Imágenes hero de publicaciones de blog, miniaturas de artículos, banners de sitios web.

### Variantes de Estilo

**Variante 1 — Cinemático · Azul Marino**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**Variante 2 — Cinemático · Naranja**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**Variante 3 — Pantalla Ancha · Carbono Oscuro**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**Variante 4 — Pantalla Ancha · Neon Cyberpunk**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**Variante 5 — Cuadrado · Minimalista**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**Variante 6 — Cuadrado · Póster Impactante**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## Sección 02 — baoyu-infographic

Combina **21 tipos de diseño** con **20 estilos visuales** para producir infografías. El diseño define la estructura (cuadrícula bento, jerarquía, línea de tiempo…); el estilo establece el lenguaje visual (gráfico en negrita, esquema técnico, origami…).

**Cuándo usar:** Resúmenes de especificaciones de productos, hojas de comparación, publicaciones de explicación técnica, contenido de LinkedIn.

### Variantes de Estilo

**Variante 1 — Cuadrícula Bento × Gráfico Impactante**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**Variante 2 — Cuadrícula Bento × Esquema Técnico**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**Variante 3 — Capas Jerárquicas × Gráfico Impactante**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**Variante 4 — Capas Jerárquicas × Esquema Técnico**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**Variante 5 — Línea de Tiempo × Origami**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**Variante 6 — Línea de Tiempo × Corporate Memphis**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## Sección 03 — baoyu-xhs-images

Genera series de tarjetas verticales (relación de aspecto 3:4) optimizadas para Xiaohongshu (XHS), Instagram y otras plataformas sociales. 10 estilos visuales × 8 plantillas de diseño.

**Cuándo usar:** Publicaciones de Instagram, tarjetas de productos XHS, contenido de redes sociales enfocado en productos.

### Variantes de Estilo

**Variante 1 — Notion · Predeterminado**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**Variante 2 — Negrita · Predeterminado**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**Variante 3 — Pastel · Predeterminado**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**Variante 4 — Notion · Diseño de Lista**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**Variante 5 — Negrita · Comparación**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**Variante 6 — Pastel · Línea de Tiempo**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## Sección 04 — baoyu-comic

Crea arte secuencial en múltiples estilos: manga japonés, webtoon coreano, tira educativa. Admite tanto paneles únicos como narrativas de múltiples paneles.

**Cuándo usar:** Contenido de participación en redes sociales, tutoriales de productos explicados visualmente, explicadores educativos.

### Variantes de Estilo

**Variante 1 — Manga · Reseña de Producto Tech**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**Variante 2 — Manga · Tira Cómica Divertida de 3 Paneles**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**Variante 3 — Webtoon · Educativo**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**Variante 4 — Webtoon · Minimalista**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## Sección 05 — baoyu-article-illustrator

Analiza la estructura de un artículo y genera ilustraciones apropiadas al contexto para cada sección. Utiliza un enfoque bidimensional de Tipo × Estilo.

**Cuándo usar:** Artículos de blog técnicos que necesitan ilustraciones en línea para explicar conceptos.

### Variantes de Estilo

**Variante 1 — Diagrama de Señal RF**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**Variante 2 — Escena de Lifestyle**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**Variante 3 — Hoja de Iconos de Especificaciones**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**Variante 4 — Banner Hero**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## Sección 06 — baoyu-imagine

Generación libre de imágenes IA con máxima libertad creativa. Sin restricciones fijas de diseño o estilo — describe cualquier visual que necesites.

**Cuándo usar:** Renders de productos para e-commerce, reemplazos de fotografía de lifestyle, vistas técnicas explosionadas, generación de escenas personalizadas.

### Variantes de Estilo

**Variante 1 — Render Fotorrealista Frontal**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**Variante 2 — Render de Producto en Ángulo 3/4**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**Variante 3 — Escena de Lifestyle**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**Variante 4 — Vista Técnica Explosionada**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## Cómo Usar Esto como Referencia de Estilos

Usa este artículo como tabla de consulta cada vez que necesites generar una imagen de marketing. El flujo de decisión es simple:

**1. ¿Para qué plataforma es esta imagen?**

| Plataforma | Skill Recomendada | Relación de Aspecto |
|------------|-------------------|---------------------|
| Portada de artículo de blog | `baoyu-cover-image` | Cinemático 2.35:1 o Pantalla ancha 16:9 |
| Publicación de Instagram / XHS | `baoyu-xhs-images` | Vertical 3:4 |
| LinkedIn / Twitter | `baoyu-cover-image` (cuadrado) | 1:1 |
| Artículo técnico en línea | `baoyu-article-illustrator` | Variable |
| Diapositiva de presentación | `baoyu-slide-deck` | 16:9 |
| Render de página de producto | `baoyu-imagine` | Personalizado |
| Publicación de resumen de especificaciones | `baoyu-infographic` | Variable |
| Contenido de participación social | `baoyu-comic` | Variable |

**2. Elige tu estilo** — encuentra la variante en este artículo que coincida con el tono de tu marca, copia el prompt, y reemplaza el nombre del producto y las especificaciones clave con tu producto objetivo.

**3. Ejecuta la skill** en GitHub Copilot CLI:

```bash
# Ejemplo — generar una imagen de portada
/baoyu-cover-image

# Ejemplo — generar una tarjeta de Instagram
/baoyu-xhs-images

# Ejemplo — generar un render de producto
/baoyu-imagine
```

**4. Sigue los prompts guiados de la skill** — cada skill hará preguntas de aclaración sobre estilo, dimensiones y contenido antes de generar.

---

## Acerca de baoyu-skills

La colección completa de plugins baoyu-skills está disponible en GitHub:

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

Todas las imágenes de este artículo fueron generadas usando las skills anteriores, con el ALFA AWUS036ACM como producto sujeto. La referencia completa de prompts para todas las imágenes está documentada en nuestra guía de flujo de trabajo interno.

¿Quieres saber más sobre el AWUS036ACM — el producto usado como ejemplo en esta guía?

{{< button href="/es/products/alfa/awus036acm/" >}}Ver Página de Producto AWUS036ACM{{< /button >}}
