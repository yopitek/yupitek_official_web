---
title: "Imagens de Produtos com IA: Uma Referência Completa de Estilos com baoyu-skills"
description: "Como usamos o plugin baoyu-skills para GitHub Copilot CLI para gerar capas de blog, infográficos, cards do Instagram, quadrinhos e renders de produtos — com o ALFA AWUS036ACM como exemplo real. Uma referência prática de estilos para geração de imagens de marketing B2B."
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "geração-de-imagens-IA", "marketing", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "O que é o baoyu-skills?"
    answer: "O baoyu-skills é uma coleção de plugins de código aberto para o GitHub Copilot CLI, oferecendo 19 habilidades que cobrem geração de imagens, saída HTML, tradução e publicação em redes sociais, tudo acessível diretamente do terminal."
  - question: "Qual baoyu-skill  é adequado para gerar imagens de capa de blog?"
    answer: "O baoyu-cover-image  é projetado para capas de artigos, suportando três proporções: cinema 2.35:1, widescreen 16:9 e quadrado 1:1, com múltiplos estilos de cor e renderização."
  - question: "Como usar o baoyu-skills no GitHub Copilot CLI?"
    answer: "Após instalar a coleção de plugins, digite comandos como /baoyu-cover-image ou /baoyu-xhs-images no terminal. A habilidade fará perguntas sobre estilo, dimensões e conteúdo antes de gerar a imagem."
  - question: "Quais tipos de saída de imagem o baoyu-skills suporta?"
    answer: "A saída Tipo A cobre capas, infograficos, quadrinhos, slides, renderizações de produtos e cartões verticais do Xiaohongshu; o Tipo B gera HTML estilizado; o Tipo C lida com tradução e publicação em redes sociais."
  - question: "Como aplicar o baoyu-skills aos seus próprios produtos?"
    answer: "Encontre a variante que corresponde ao tom da sua marca neste artigo, copie o prompt e substitua o nome do produto e especificações principais pelo seu produto alvo, depois execute a habilidade correspondente no Copilot CLI."
---

Na Yopitek, distribuímos produtos de hardware técnico — adaptadores WiFi, ferramentas de pesquisa em segurança, módulos SDR — e criar visuais de marketing consistentes e de alta qualidade para 8 idiomas sempre foi um desafio. Este artigo documenta como usamos a coleção de plugins **baoyu-skills** para GitHub Copilot CLI para gerar imagens de produtos em diferentes formatos e estilos.

Usamos o adaptador USB WiFi **ALFA AWUS036ACM** como produto de exemplo ao longo deste guia. Cada prompt e imagem exibida aqui foi gerada a partir de uma descrição deste adaptador. O objetivo é uma referência prática de estilos: quando você precisar de uma imagem de capa de produto, um card para o Instagram, ou um infográfico técnico no futuro, você pode consultar qual skill e estilo usar.

{{< tldr >}}
O baoyu-skills oferece 19 habilidades cobrindo saida de imagens, HTML e texto. Este artigo usa o ALFA AWUS036ACM como exemplo para demonstrar as variantes de estilo, prompts e casos de uso das 6 principais habilidades de imagem, servindo como tabela de referencia para geracao de imagens de marketing.
{{< /tldr >}}


{{< alert "circle-info" >}}
**baoyu-skills** é uma coleção de plugins de código aberto para GitHub Copilot CLI criada por [@JimLiu](https://github.com/JimLiu/baoyu-skills.git). Adiciona 19 skills especializadas para criação de conteúdo, geração de imagens, tradução e publicação em redes sociais — todas acessíveis diretamente do seu terminal.
{{< /alert >}}

---

## Referência Completa de Skills — Todas as 19 baoyu-skills

A coleção tem 19 skills, organizadas em três tipos:

- **Tipo A — Saída de Imagens:** Gera ativos visuais (capas, infográficos, quadrinhos, renders)
- **Tipo B — Saída HTML:** Gera documentos web estilizados
- **Tipo C — Texto / Utilitário:** Tradução, formatação, publicação social, compressão

| # | Skill | Tipo | Propósito | Palavras-chave |
|---|-------|------|-----------|----------------|
| 01 | `baoyu-article-illustrator` | Imagem | Gera automaticamente ilustrações para cada seção de um artigo | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | Imagem | Cria tirinhas de manga/webtoon/educacional em múltiplos estilos artísticos | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | Utilitário | Comprime imagens para WebP/PNG com redução de tamanho de 80–99% | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | Imagem | Gera imagens de capa com 5 dimensões de design (tipo, paleta, renderização, texto, mood) | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | Motor API | Geração de texto e imagens via Gemini Web API; conversas multi-turno, entrada de visão | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | Texto | Converte tweets e artigos de X (Twitter) para Markdown com front matter YAML | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | Texto | Formata texto simples em Markdown estruturado com títulos, frontmatter, blocos de código | format markdown · beautify article |
| 08 | `baoyu-image-gen` | Imagem | Geração de imagens IA multi-provedor (OpenAI, Google, DashScope, Replicate); modo paralelo | generate / create / draw images |
| 09 | `baoyu-imagine` | Imagem | Geração livre de imagens IA — renders fotorrealistas, cenas de lifestyle, vistas explodidas | imagine · create visual |
| 10 | `baoyu-infographic` | Imagem | Infográficos profissionais: 21 tipos de layout × 20 estilos visuais | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Converte Markdown para HTML estilizado com temas WeChat, destaque de código, matemática, PlantUML | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | Social | Publica artigos e conteúdo de imagem-texto na Conta Oficial do WeChat | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | Social | Publica no X (Twitter) com imagens/vídeo; suporta o formato X Articles de formato longo | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | Imagem | Gera imagens de slides a partir de conteúdo com estilo consistente entre os slides | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | Texto | Tradução em três modos: rápida / normal (análise+tradução) / refinada (análise→tradução→revisão→polimento) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | Texto | Busca qualquer URL e converte para Markdown usando Chrome CDP | save webpage as markdown |
| 17 | `baoyu-xhs-images` | Imagem | Cards verticais XHS (Xiaohongshu/Little Red Book): 10 estilos × 8 layouts, otimizados para Instagram | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | Texto | Extrai transcrições e legendas do YouTube como Markdown estruturado | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | Social | Publica no Weibo com texto, imagens, tags de tópico e tratamento de limite de caracteres | 发布微博 · post to weibo |

---

## Seção 01 — baoyu-cover-image

Imagens de capa de artigos em três proporções: **cinemático (2.35:1)**, **widescreen (16:9)**, e **quadrado (1:1)**. Cada proporção suporta múltiplas paletas de cores e estilos de renderização.

**Quando usar:** Imagens hero de publicações de blog, miniaturas de artigos, banners de sites.

### Variantes de Estilo

**Variante 1 — Cinemático · Azul Marinho**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**Variante 2 — Cinemático · Laranja**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**Variante 3 — Widescreen · Carbono Escuro**

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

**Variante 5 — Quadrado · Minimalista**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**Variante 6 — Quadrado · Pôster Impactante**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## Seção 02 — baoyu-infographic

Combina **21 tipos de layout** com **20 estilos visuais** para produzir infográficos. O layout define a estrutura (grade bento, hierarquia, linha do tempo…); o estilo define a linguagem visual (gráfico em negrito, esquema técnico, origami…).

**Quando usar:** Visões gerais de especificações de produtos, planilhas de comparação, posts de explicação técnica, conteúdo do LinkedIn.

### Variantes de Estilo

**Variante 1 — Grade Bento × Gráfico Impactante**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**Variante 2 — Grade Bento × Esquema Técnico**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**Variante 3 — Camadas Hierárquicas × Gráfico Impactante**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**Variante 4 — Camadas Hierárquicas × Esquema Técnico**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**Variante 5 — Linha do Tempo × Origami**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**Variante 6 — Linha do Tempo × Corporate Memphis**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## Seção 03 — baoyu-xhs-images

Gera séries de cards verticais (proporção 3:4) otimizados para Xiaohongshu (XHS), Instagram e outras plataformas sociais. 10 estilos visuais × 8 templates de layout.

**Quando usar:** Posts do Instagram, cards de produtos XHS, conteúdo de mídia social focado em produtos.

### Variantes de Estilo

**Variante 1 — Notion · Padrão**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**Variante 2 — Negrito · Padrão**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**Variante 3 — Pastel · Padrão**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**Variante 4 — Notion · Layout de Lista**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**Variante 5 — Negrito · Comparação**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**Variante 6 — Pastel · Linha do Tempo**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## Seção 04 — baoyu-comic

Cria arte sequencial em múltiplos estilos: manga japonês, webtoon coreano, tirinha educacional. Suporta tanto painéis únicos quanto narrativas de múltiplos painéis.

**Quando usar:** Conteúdo de engajamento em redes sociais, tutoriais de produtos explicados visualmente, conteúdo educacional.

### Variantes de Estilo

**Variante 1 — Manga · Review de Produto Tech**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**Variante 2 — Manga · Tirinha Divertida de 3 Painéis**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**Variante 3 — Webtoon · Educacional**

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

## Seção 05 — baoyu-article-illustrator

Analisa a estrutura de um artigo e gera ilustrações apropriadas ao contexto para cada seção. Usa uma abordagem bidimensional de Tipo × Estilo.

**Quando usar:** Artigos de blog técnicos que precisam de ilustrações inline para explicar conceitos.

### Variantes de Estilo

**Variante 1 — Diagrama de Sinal RF**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**Variante 2 — Cena de Lifestyle**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**Variante 3 — Folha de Ícones de Especificações**

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

## Seção 06 — baoyu-imagine

Geração livre de imagens IA com máxima liberdade criativa. Sem restrições fixas de layout ou estilo — descreva qualquer visual que você precisar.

**Quando usar:** Renders de produtos para e-commerce, substituições de fotografia de lifestyle, vistas técnicas explodidas, geração de cenas personalizadas.

### Variantes de Estilo

**Variante 1 — Render Fotorrealista Frontal**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**Variante 2 — Render de Produto em Ângulo 3/4**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**Variante 3 — Cena de Lifestyle**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**Variante 4 — Vista Técnica Explodida**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## Como Usar Isso como Referência de Estilos

Use este artigo como tabela de consulta sempre que precisar gerar uma imagem de marketing. O fluxo de decisão é simples:

**1. Para qual plataforma é esta imagem?**

| Plataforma | Skill Recomendada | Proporção |
|------------|-------------------|-----------|
| Capa de artigo de blog | `baoyu-cover-image` | Cinemático 2.35:1 ou Widescreen 16:9 |
| Post do Instagram / XHS | `baoyu-xhs-images` | Vertical 3:4 |
| LinkedIn / Twitter | `baoyu-cover-image` (quadrado) | 1:1 |
| Artigo técnico inline | `baoyu-article-illustrator` | Variável |
| Slide de apresentação | `baoyu-slide-deck` | 16:9 |
| Render de página de produto | `baoyu-imagine` | Personalizado |
| Post de visão geral de especificações | `baoyu-infographic` | Variável |
| Conteúdo de engajamento social | `baoyu-comic` | Variável |

**2. Escolha seu estilo** — encontre a variante neste artigo que corresponde ao tom da sua marca, copie o prompt e substitua o nome do produto e as especificações principais pelo seu produto alvo.

**3. Execute a skill** no GitHub Copilot CLI:

```bash
# Exemplo — gerar uma imagem de capa
/baoyu-cover-image

# Exemplo — gerar um card do Instagram
/baoyu-xhs-images

# Exemplo — gerar um render de produto
/baoyu-imagine
```

**4. Siga os prompts guiados da skill** — cada skill fará perguntas de esclarecimento sobre estilo, dimensões e conteúdo antes de gerar.

---

{{< faq >}}

## Sobre baoyu-skills

A coleção completa de plugins baoyu-skills está disponível no GitHub:

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

Todas as imagens neste artigo foram geradas usando as skills acima, com o ALFA AWUS036ACM como produto de referência. A referência completa de prompts para todas as imagens está documentada em nosso guia de fluxo de trabalho interno.

Quer saber mais sobre o AWUS036ACM — o produto usado como exemplo ao longo deste guia?

{{< button href="/pt/products/alfa/awus036acm/" >}}Ver Página do Produto AWUS036ACM{{< /button >}}

## Referências

1. [Repositorio GitHub do baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)
2. [Documentacao oficial do GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
3. [Especificacoes do produto ALFA Network AWUS036ACM](https://www.alfa.com.tw/)
4. [Dados do chipset MediaTek MT7612U](https://www.mediatek.com/products/networking-and-connectivity)
5. [Documentacao da API de geracao de imagens da OpenAI](https://platform.openai.com/docs/guides/images)
