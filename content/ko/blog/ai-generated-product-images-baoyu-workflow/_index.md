---
title: "AI 생성 제품 이미지: baoyu-skills를 활용한 완전한 스타일 레퍼런스"
description: "GitHub Copilot CLI용 baoyu-skills 플러그인으로 블로그 커버, 인포그래픽, Instagram 카드, 만화, 제품 렌더링을 생성하는 방법을 ALFA AWUS036ACM 실제 사례와 함께 소개합니다. B2B 마케팅 이미지 생성을 위한 실용적인 스타일 레퍼런스입니다."
date: 2026-04-02
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "baoyu-skills란 무엇입니까?"
    answer: "baoyu-skills는 GitHub Copilot CLI용 오픈소스 플러그인 모음으로, 이미지 생성, HTML 출력, 번역, 소셜 미디어 게시를 아우르는 19개의 스킬을 제공하며 모두 터미널에서 호출할 수 있습니다."
  - question: "블로그 커버 이미지를 생성하기에 가장 적합한 baoyu-skill은 무엇입니까?"
    answer: "baoyu-cover-image는 글 커버용으로 설계되었습니다. 시네마틱 2.35:1, 와이드스크린 16:9, 정사각형 1:1 비율을 지원하며 다양한 색상 및 렌더링 스타일을 제공합니다."
  - question: "GitHub Copilot CLI에서 baoyu-skills는 어떻게 사용합니까?"
    answer: "플러그인 모음을 설치한 뒤 터미널에서 /baoyu-cover-image 또는 /baoyu-xhs-images와 같은 명령을 입력합니다. 스킬이 이미지를 생성하기 전에 스타일, 크기, 콘텐츠에 관한 질문을 차례로 안내합니다."
  - question: "baoyu-skills는 어떤 이미지 출력 유형을 지원합니까?"
    answer: "유형 A는 커버 이미지, 인포그래픽, 만화, 슬라이드, 제품 렌더링, 샤오홍슈 세로 카드를 다룹니다. 유형 B는 스타일이 적용된 HTML을 생성합니다. 유형 C는 번역과 소셜 게시를 처리합니다."
  - question: "baoyu-skills를 자사 제품에 맞게 적용하려면 어떻게 해야 합니까?"
    answer: "브랜드 톤에 맞는 변형을 찾아 프롬프트를 복사한 뒤, 제품명과 주요 사양을 바꾸고 Copilot CLI에서 해당 스킬을 실행하면 됩니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "AI-image-generation", "marketing", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

Yopitek은 WiFi 어댑터, 보안 연구 도구, SDR 모듈 등 기술 하드웨어 제품을 유통하고 있으며, 8개 언어에 걸쳐 일관되고 품질 높은 마케팅 비주얼을 제작하는 일은 늘 과제였습니다. 이 글에서는 GitHub Copilot CLI용 **baoyu-skills** 플러그인 모음을 사용하여 다양한 형식과 스타일의 제품 이미지를 생성하는 방법을 기록합니다.

{{< tldr >}}
baoyu-skills는 이미지, HTML, 텍스트 출력을 아우르는 19개의 스킬을 제공합니다. 이 글은 ALFA AWUS036ACM을 예시로 6개 주요 이미지 스킬의 스타일 변형, 프롬프트, 활용 사례를 보여 주며, 마케팅 이미지 생성을 위한 조회용 표로 활용할 수 있습니다.
{{< /tldr >}}





이 가이드 전체에서 예시 제품으로 **ALFA AWUS036ACM** USB WiFi 어댑터를 사용합니다. 여기에 실린 모든 프롬프트와 이미지는 이 어댑터에 대한 설명으로 생성되었습니다. 목표는 실용적인 스타일 레퍼런스입니다. 나중에 제품 커버 이미지, Instagram 카드, 기술 인포그래픽이 필요할 때 어떤 스킬과 스타일을 사용할지 찾아볼 수 있습니다.

{{< alert "circle-info" >}}
**baoyu-skills**는 [@JimLiu](https://github.com/JimLiu/baoyu-skills.git)가 만든 GitHub Copilot CLI용 오픈소스 플러그인 모음입니다. 콘텐츠 제작, 이미지 생성, 번역, 소셜 게시를 위한 19개의 전문 스킬을 추가하며, 모두 터미널에서 직접 사용할 수 있습니다.
{{< /alert >}}

---

## 전체 스킬 레퍼런스 - baoyu-skills 19종

이 모음에는 19개의 스킬이 있으며 세 가지 유형으로 구분됩니다.

- **유형 A - 이미지 출력:** 시각 자산(커버, 인포그래픽, 만화, 렌더링)을 생성합니다
- **유형 B - HTML 출력:** 스타일이 적용된 웹 문서를 생성합니다
- **유형 C - 텍스트 / 유틸리티:** 번역, 서식 지정, 소셜 게시, 압축

트리거 키워드 열에는 스킬이 입력된 그대로 반응하기 때문에 원래의 중국어 간체 문구를 그대로 두었으며, 영어 표현을 함께 나열했습니다.

| # | 스킬 | 유형 | 용도 | 트리거 키워드 |
|---|-------|------|---------|-----------------|
| 01 | `baoyu-article-illustrator` | 이미지 | 글의 각 섹션에 맞는 삽화를 자동 생성합니다 | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | 이미지 | 다양한 화풍으로 만화/웹툰/교육용 만화를 제작합니다 | 知识漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | 유틸리티 | 이미지를 WebP/PNG로 압축하여 용량을 80~99% 줄입니다 | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | 이미지 | 5가지 디자인 차원(유형, 팔레트, 렌더링, 텍스트, 분위기)으로 글 커버 이미지를 생성합니다 | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | API 엔진 | Gemini Web API를 통한 텍스트 및 이미지 생성, 멀티턴 대화, 비전 입력을 지원합니다 | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | 텍스트 | X(Twitter) 트윗과 글을 YAML 프런트 매터가 포함된 Markdown으로 변환합니다 | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | 텍스트 | 일반 텍스트를 제목, 프런트 매터, 코드 블록이 있는 구조화된 Markdown으로 서식화합니다 | format markdown · beautify article |
| 08 | `baoyu-image-gen` | 이미지 | 멀티 공급자 AI 이미지 생성(OpenAI, Google, DashScope, Replicate), 병렬 모드를 지원합니다 | generate / create / draw images |
| 09 | `baoyu-imagine` | 이미지 | 자유 형식 AI 이미지 생성 - 사실적인 렌더링, 라이프스타일 장면, 분해도 | imagine · create visual |
| 10 | `baoyu-infographic` | 이미지 | 전문적인 인포그래픽: 21가지 레이아웃 유형 × 20가지 비주얼 스타일 | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | Markdown을 WeChat 테마, 코드 하이라이팅, 수식, PlantUML이 적용된 HTML로 변환합니다 | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | 소셜 | WeChat 공식 계정에 글과 이미지-텍스트 콘텐츠를 게시합니다 | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | 소셜 | 이미지/영상과 함께 X(Twitter)에 게시하며, X Articles 장문 형식을 지원합니다 | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | 이미지 | 콘텐츠로부터 슬라이드 전반에 일관된 스타일의 슬라이드 덱 이미지를 생성합니다 | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | 텍스트 | 세 가지 번역 모드: 빠른 번역 / 일반(분석+번역) / 정밀(분석→번역→검토→다듬기) | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | 텍스트 | 임의의 URL을 가져와 Chrome CDP로 Markdown으로 변환합니다 | save webpage as markdown |
| 17 | `baoyu-xhs-images` | 이미지 | XHS(샤오홍슈/Little Red Book) 세로 카드: 10가지 스타일 × 8가지 레이아웃, Instagram에 최적화되어 있습니다 | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | 텍스트 | YouTube 대본과 자막을 구조화된 Markdown으로 추출합니다 | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | 소셜 | 텍스트, 이미지, 주제 태그, 글자 수 제한 처리와 함께 Weibo에 게시합니다 | 发布微博 · post to weibo |

---

## 섹션 01 - baoyu-cover-image

세 가지 화면 비율의 글 커버 이미지: **시네마틱(2.35:1)**, **와이드스크린(16:9)**, **정사각형(1:1)**. 각 비율은 다양한 색상 팔레트와 렌더링 스타일을 지원합니다.

**사용 시기:** 블로그 글 히어로 이미지, 글 썸네일, 웹사이트 배너.

### 스타일 변형

**변형 1 - 시네마틱 · 네이비**

![커버 이미지 1 - 시네마틱 네이비](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**변형 2 - 시네마틱 · 오렌지**

![커버 이미지 2 - 시네마틱 오렌지](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**변형 3 - 와이드스크린 · 다크 카본**

![커버 이미지 3 - 와이드스크린 다크](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**변형 4 - 와이드스크린 · 네온 사이버펑크**

![커버 이미지 4 - 와이드스크린 네온](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**변형 5 - 정사각형 · 미니멀**

![커버 이미지 5 - 정사각형 미니멀](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**변형 6 - 정사각형 · 볼드 포스터**

![커버 이미지 6 - 정사각형 볼드](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## 섹션 02 - baoyu-infographic

**21가지 레이아웃 유형**과 **20가지 비주얼 스타일**을 조합하여 인포그래픽을 만듭니다. 레이아웃은 구조(벤토 그리드, 계층, 타임라인 등)를 정의하고, 스타일은 시각 언어(볼드 그래픽, 기술 도식, 오리가미 등)를 정합니다.

**사용 시기:** 제품 사양 개요, 비교표, 기술 해설 글, LinkedIn 콘텐츠.

### 스타일 변형

**변형 1 - 벤토 그리드 × 볼드 그래픽**

![인포그래픽 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**변형 2 - 벤토 그리드 × 기술 도식**

![인포그래픽 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**변형 3 - 계층 구조 × 볼드 그래픽**

![인포그래픽 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**변형 4 - 계층 구조 × 기술 도식**

![인포그래픽 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**변형 5 - 타임라인 × 오리가미**

![인포그래픽 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**변형 6 - 타임라인 × 코퍼레이트 멤피스**

![인포그래픽 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## 섹션 03 - baoyu-xhs-images

샤오홍슈(XHS), Instagram 및 기타 소셜 플랫폼에 최적화된 세로 카드 시리즈(3:4 비율)를 생성합니다. 10가지 비주얼 스타일 × 8가지 레이아웃 템플릿.

**사용 시기:** Instagram 게시물, XHS 제품 카드, 제품 중심의 소셜 미디어 콘텐츠.

### 스타일 변형

아래 XHS 프롬프트는 표시된 카드를 생성하는 데 실제로 사용한 프롬프트이므로 원래의 중국어 간체 그대로 두었습니다. 각 프롬프트는 카드 스타일(Notion, 볼드, 파스텔), AWUS036ACM 주제, 레이아웃, 표시할 핵심 라벨을 설명합니다.

**변형 1 - Notion · 기본**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**변형 2 - 볼드 · 기본**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**변형 3 - 파스텔 · 기본**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**변형 4 - Notion · 리스트 레이아웃**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**변형 5 - 볼드 · 비교**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**변형 6 - 파스텔 · 타임라인**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## 섹션 04 - baoyu-comic

일본 만화, 한국 웹툰, 교육용 컷 만화 등 다양한 스타일로 연속 이미지를 만듭니다. 단일 컷과 여러 컷의 서사를 모두 지원합니다.

**사용 시기:** 소셜 미디어 참여 유도 콘텐츠, 시각적으로 설명하는 제품 튜토리얼, 교육용 해설.

### 스타일 변형

**변형 1 - 만화 · 기술 제품 리뷰**

![만화 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**변형 2 - 만화 · 재미있는 3컷 만화**

![만화 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**변형 3 - 웹툰 · 교육용**

![만화 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**변형 4 - 웹툰 · 미니멀**

![만화 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## 섹션 05 - baoyu-article-illustrator

글의 구조를 분석하여 각 섹션에 맞는 삽화를 생성합니다. 유형 × 스타일의 2차원 접근 방식을 사용합니다.

**사용 시기:** 개념을 설명하기 위해 본문 중간에 삽화가 필요한 기술 블로그 글.

### 스타일 변형

**변형 1 - RF 신호 다이어그램**

![삽화 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**변형 2 - 라이프스타일 장면**

![삽화 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**변형 3 - 사양 아이콘 시트**

![삽화 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**변형 4 - 히어로 배너**

![삽화 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## 섹션 06 - baoyu-imagine

창의적 자유도가 최대인 자유 형식 AI 이미지 생성입니다. 고정된 레이아웃이나 스타일 제약이 없으므로 필요한 비주얼을 무엇이든 설명하면 됩니다.

**사용 시기:** 이커머스용 제품 렌더링, 라이프스타일 사진 대체, 기술 분해도, 맞춤형 장면 생성.

### 스타일 변형

**변형 1 - 사실적인 정면 뷰**

![이미지 생성 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**변형 2 - 3/4 각도 제품 렌더링**

![이미지 생성 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**변형 3 - 라이프스타일 장면**

![이미지 생성 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**변형 4 - 기술 분해도**

![이미지 생성 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## 스타일 레퍼런스로 활용하는 방법

마케팅 이미지를 생성해야 할 때마다 이 글을 조회용 표로 사용하십시오. 결정 흐름은 간단합니다.

**1. 이 이미지는 어떤 플랫폼용입니까?**

| 플랫폼 | 권장 스킬 | 화면 비율 |
|----------|-------------------|--------------|
| 블로그 글 커버 | `baoyu-cover-image` | 시네마틱 2.35:1 또는 와이드스크린 16:9 |
| Instagram / XHS 게시물 | `baoyu-xhs-images` | 3:4 세로 |
| LinkedIn / Twitter | `baoyu-cover-image` (정사각형) | 1:1 |
| 기술 글 본문 삽화 | `baoyu-article-illustrator` | 다양함 |
| 프레젠테이션 슬라이드 | `baoyu-slide-deck` | 16:9 |
| 제품 페이지 렌더링 | `baoyu-imagine` | 사용자 지정 |
| 사양 개요 게시물 | `baoyu-infographic` | 다양함 |
| 소셜 참여 유도 콘텐츠 | `baoyu-comic` | 다양함 |

**2. 스타일을 선택합니다** - 이 글에서 브랜드 톤에 맞는 변형을 찾아 프롬프트를 복사하고, 제품명과 주요 사양을 대상 제품에 맞게 바꿉니다.

**3. GitHub Copilot CLI에서 스킬을 실행합니다**:

```bash
# Example — generate a cover image
/baoyu-cover-image

# Example — generate an Instagram card
/baoyu-xhs-images

# Example — generate a product render
/baoyu-imagine
```

**4. 스킬의 안내 프롬프트를 따릅니다** - 각 스킬은 이미지를 생성하기 전에 스타일, 크기, 콘텐츠에 관한 확인 질문을 합니다.

---

{{< faq >}}

## baoyu-skills 소개

baoyu-skills 플러그인 전체 모음은 GitHub에서 확인하실 수 있습니다.

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

이 글의 모든 이미지는 위의 스킬을 사용하여 ALFA AWUS036ACM을 제품 피사체로 생성했습니다. 모든 이미지의 전체 프롬프트 레퍼런스는 내부 워크플로 가이드에 문서화되어 있습니다.

이 가이드 전체에서 예시로 사용한 제품인 AWUS036ACM에 대해 더 알고 싶으십니까?

{{< button href="/ko/products/alfa/awus036acm/" >}}AWUS036ACM 제품 페이지 보기{{< /button >}}

## 참고 자료

1. [baoyu-skills GitHub 저장소](https://github.com/JimLiu/baoyu-skills.git)
2. [GitHub Copilot CLI 문서](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
3. [ALFA Network AWUS036ACM 제품 사양](https://www.alfa.com.tw/)
4. [MediaTek MT7612U 칩셋 정보](https://www.mediatek.com/products/networking-and-connectivity)
5. [OpenAI 이미지 생성 API 문서](https://platform.openai.com/docs/guides/images)
