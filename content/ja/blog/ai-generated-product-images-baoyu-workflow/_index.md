---
title: "AI生成プロダクト画像：baoyu-skillsを使った完全スタイルリファレンス"
description: "GitHub Copilot CLIのbaoyu-skillsプラグインを使って、ブログカバー、インフォグラフィック、Instagramカード、漫画、プロダクトレンダリングを生成する方法——ALFA AWUS036ACMを実例として使用。B2Bマーケティング画像生成のための実用的なスタイルリファレンス。"
date: 2026-04-02
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["baoyu-skills", "AI-image-generation", "マーケティング", "ALFA-Network", "GitHub-Copilot"]
featureimage: "/images/blog/baoyu-skills/cover-image-4.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "baoyu-skillsとは何ですか？"
    answer: "baoyu-skillsはGitHub Copilot CLIのオープンソースプラグインコレクションで、画像生成、HTML出力、翻訳、SNS投稿をカバーする19のスキルを提供し、すべてターミナルから直接呼び出せます。"
  - question: "ブログのカバー画像生成に適したbaoyu-skillsはどれですか？"
    answer: "baoyu-cover-imageが記事カバー用に設計されており、シネマワイド2.35:1、ワイドスクリーン16:9、スクエア1:1の3種類の比率に対応し、多彩なカラーとレンダリングスタイルを組み合わせられます。"
  - question: "GitHub Copilot CLIでbaoyu-skillsをどう使いますか？"
    answer: "プラグインコレクションをインストール後、ターミナルで /baoyu-cover-image や /baoyu-xhs-images などのコマンドを入力すると、スキルがスタイル、サイズ、内容に関する確認質問を案内した上で画像を生成します。"
  - question: "baoyu-skillsはどのような画像出力タイプに対応していますか？"
    answer: "Type A画像出力はカバー画像、インフォグラフィック、コミック、スライド、プロダクトレンダリング、小紅書の縦型カードをカバーします。Type Bはスタイル化HTMLを生成し、Type Cは翻訳とSNS投稿を処理します。"
  - question: "baoyu-skillsを自社製品にどう活用しますか？"
    answer: "本記事からブランドのトーンに合うバリアントを見つけ、プロンプトをコピーして製品名と主要スペックを対象製品に置き換え、Copilot CLIで対応スキルを実行するだけです。"
---

Yopitekでは、技術系ハードウェア製品——WiFiアダプター、セキュリティリサーチツール、SDRモジュール——を販売しており、8言語に対応した一貫性の高いマーケティングビジュアルの制作は常に課題となっていました。本記事では、GitHub Copilot CLIの **baoyu-skills** プラグインコレクションを活用して、さまざまなフォーマットとスタイルでプロダクト画像を生成する方法をご紹介します。


{{< tldr >}}
baoyu-skillsは画像、HTML、テキスト出力をカバーする19のスキルを提供します。本記事はALFA AWUS036ACMを例に、6つの主要画像スキルのスタイルバリアント、プロンプト、適用シーンを提示し、マーケティング画像生成のリファレンステーブルとして活用できます。
{{< /tldr >}}
本ガイドでは、**ALFA AWUS036ACM** USB WiFiアダプターをサンプル製品として使用します。ここに掲載されているすべてのプロンプトと画像は、このアダプターの説明から生成されたものです。目的は実用的なスタイルリファレンスの作成です。将来、プロダクトカバー画像、Instagramカード、または技術的なインフォグラフィックが必要になった際に、どのスキルとスタイルを使用すべきかをすぐに参照できます。

{{< alert "circle-info" >}}
**baoyu-skills** は、[@JimLiu](https://github.com/JimLiu/baoyu-skills.git) によるGitHub Copilot CLI向けのオープンソースプラグインコレクションです。コンテンツ制作、画像生成、翻訳、SNS投稿など19の専門スキルが追加され、すべてターミナルから直接利用できます。
{{< /alert >}}

---

## 完全スキルリファレンス——全19のbaoyu-skills

このコレクションには19のスキルが含まれており、3つのタイプに分類されます：

- **Type A — Image Output：** ビジュアルアセットの生成（カバー、インフォグラフィック、漫画、レンダリング）
- **Type B — HTML Output：** スタイル付きWebドキュメントの生成
- **Type C — Text / Utility：** 翻訳、フォーマット、SNS投稿、圧縮

| # | スキル | タイプ | 用途 | トリガーキーワード |
|---|--------|--------|------|-----------------|
| 01 | `baoyu-article-illustrator` | 画像 | 記事の各セクションに挿絵を自動生成 | 为文章配图 · illustrate article · add images |
| 02 | `baoyu-comic` | 画像 | 複数のアートスタイルで漫画/ウェブトゥーン/教育コミックを作成 | 知識漫画 · biography comic · tutorial comic |
| 03 | `baoyu-compress-image` | ユーティリティ | 画像をWebP/PNGに圧縮（80〜99%のサイズ削減） | compress image · optimize image · convert to webp |
| 04 | `baoyu-cover-image` | 画像 | 5つのデザイン次元でカバー画像を生成（タイプ、パレット、レンダリング、テキスト、ムード） | generate cover image · create article cover · make cover |
| 05 | `baoyu-danger-gemini-web` | APIエンジン | Gemini Web APIでテキストと画像を生成；マルチターン会話、ビジョン入力 | generate image with Gemini |
| 06 | `baoyu-danger-x-to-markdown` | テキスト | X (Twitter) のツイートと記事をYAML front matter付きMarkdownに変換 | X to markdown · tweet to markdown |
| 07 | `baoyu-format-markdown` | テキスト | プレーンテキストを見出し、frontmatter、コードブロック付きの構造化Markdownに整形 | format markdown · beautify article |
| 08 | `baoyu-image-gen` | 画像 | マルチプロバイダーAI画像生成（OpenAI、Google、DashScope、Replicate）；並列モード | generate / create / draw images |
| 09 | `baoyu-imagine` | 画像 | 自由形式のAI画像生成——フォトリアルレンダリング、ライフスタイルシーン、分解図 | imagine · create visual |
| 10 | `baoyu-infographic` | 画像 | プロフェッショナルなインフォグラフィック：21レイアウト × 20ビジュアルスタイル | infographic · 信息图 · visual summary |
| 11 | `baoyu-markdown-to-html` | HTML | MarkdownをWeChatテーマ、コードハイライト、数式、PlantUML付きのスタイル化HTMLに変換 | markdown to html · md转html |
| 12 | `baoyu-post-to-wechat` | ソーシャル | WeChat公式アカウントに記事と画像テキストコンテンツを投稿 | 发布公众号 · post to wechat |
| 13 | `baoyu-post-to-x` | ソーシャル | 画像/動画付きでX (Twitter) に投稿；X Articlesの長文形式をサポート | post to X · tweet · publish to Twitter |
| 14 | `baoyu-slide-deck` | 画像 | 一貫したスタイルでコンテンツからスライド画像を生成 | create slides · make a presentation · PPT |
| 15 | `baoyu-translate` | テキスト | 3モード翻訳：クイック / 通常（分析＋翻訳）/ 精密（分析→翻訳→レビュー→ポリッシュ） | translate · 翻译 · 精翻 |
| 16 | `baoyu-url-to-markdown` | テキスト | Chrome CDPを使用して任意のURLを取得しMarkdownに変換 | save webpage as markdown |
| 17 | `baoyu-xhs-images` | 画像 | XHS（小紅書）縦型カード：10スタイル × 8レイアウト、Instagram向けに最適化 | 小红书图片 · XHS images · RedNote |
| 18 | `baoyu-youtube-transcript` | テキスト | YouTubeのトランスクリプトと字幕を構造化Markdownとして抽出 | extract transcript · youtube captions |
| 19 | `baoyu-post-to-weibo` | ソーシャル | 微博にテキスト、画像、トピックタグ付きで投稿（文字数制限に対応） | 发布微博 · post to weibo |

---

## セクション01 — baoyu-cover-image

3つのアスペクト比で記事カバー画像を生成：**シネマティック (2.35:1)**、**ワイドスクリーン (16:9)**、**スクエア (1:1)**。各比率は複数のカラーパレットとレンダリングスタイルに対応しています。

**使用場面：** ブログ記事のヒーロー画像、記事サムネイル、Webサイトバナー。

### スタイルバリアント

**バリアント1 — シネマティック · ネイビー**

![Cover Image 1 — Cinematic Navy](/images/blog/baoyu-skills/cover-image-1.webp)

```
Product hero shot of Alfa AWUS036ACM USB WiFi adapter, cinematic wide angle,
deep navy blue background, dramatic studio lighting, two high-gain RP-SMA
antennas, photorealistic 3D render, 2.35:1 aspect
```

---

**バリアント2 — シネマティック · オレンジ**

![Cover Image 2 — Cinematic Orange](/images/blog/baoyu-skills/cover-image-2.webp)

```
Alfa AWUS036ACM WiFi adapter, cinematic composition, burnt orange and black
backdrop, rim-lit product photography, antennas extended, professional tech
product shot, 2.35:1 aspect
```

---

**バリアント3 — ワイドスクリーン · ダークカーボン**

![Cover Image 3 — Widescreen Dark](/images/blog/baoyu-skills/cover-image-3.webp)

```
Alfa AWUS036ACM on dark carbon fiber surface, widescreen editorial tech
photography, neon blue accent light, AC1200 label visible, dual antennas,
16:9 aspect
```

---

**バリアント4 — ワイドスクリーン · ネオンサイバーパンク**

![Cover Image 4 — Widescreen Neon](/images/blog/baoyu-skills/cover-image-4.webp)

```
AWUS036ACM USB WiFi adapter, cyberpunk neon lighting, purple and cyan glow,
dark background, 16:9 widescreen, product floats above reflective surface
```

---

**バリアント5 — スクエア · ミニマル**

![Cover Image 5 — Square Minimal](/images/blog/baoyu-skills/cover-image-5.webp)

```
Alfa AWUS036ACM minimal product shot, white background, soft shadows, clean
tech branding, square 1:1 format, e-commerce style
```

---

**バリアント6 — スクエア · ボールドポスター**

![Cover Image 6 — Square Bold](/images/blog/baoyu-skills/cover-image-6.webp)

```
AWUS036ACM bold graphic poster, black background, high contrast, large
typography: AC1200 DUAL BAND, red accent color, 1:1 square format
```

---

## セクション02 — baoyu-infographic

**21種類のレイアウト**と**20種類のビジュアルスタイル**を組み合わせてインフォグラフィックを制作します。レイアウトが構造を定義し（ベントグリッド、階層、タイムライン…）、スタイルがビジュアル言語を設定します（ボールドグラフィック、テクニカル設計図、折り紙…）。

**使用場面：** 製品仕様の概要、比較シート、技術解説投稿、LinkedInコンテンツ。

### スタイルバリアント

**バリアント1 — ベントグリッド × ボールドグラフィック**

![Infographic 1](/images/blog/baoyu-skills/infographic-1.webp)

```
Infographic: Alfa AWUS036ACM specs, bento-grid layout, bold-graphic comic
style with halftone. Sections: chipset MT7612U, AC1200 speed, dual-band
2.4+5GHz, USB 3.0, OS compatibility Linux/Windows
```

---

**バリアント2 — ベントグリッド × テクニカル設計図**

![Infographic 2](/images/blog/baoyu-skills/infographic-2.webp)

```
Technical schematic infographic of AWUS036ACM, blueprint engineering style,
bento-grid layout, shows RF signal path, antenna specs, USB interface,
chipset architecture
```

---

**バリアント3 — 階層レイヤー × ボールドグラフィック**

![Infographic 3](/images/blog/baoyu-skills/infographic-3.webp)

```
AWUS036ACM feature hierarchy infographic, layered architecture diagram, bold
graphic style, vibrant colors, shows: Hardware → Driver → OS layers → Use
cases (Kali/Ubuntu/RPi)
```

---

**バリアント4 — 階層レイヤー × テクニカル設計図**

![Infographic 4](/images/blog/baoyu-skills/infographic-4.webp)

```
AWUS036ACM technical hierarchy: MT7612U chipset layers, driver stack (Linux
in-kernel), protocol stack 802.11ac, schematic blueprint style, monochrome
with blue accents
```

---

**バリアント5 — タイムライン × 折り紙**

![Infographic 5](/images/blog/baoyu-skills/infographic-5.webp)

```
Linux kernel support timeline for MediaTek MT7612U (AWUS036ACM), origami
folded-paper style, milestones: kernel 4.19 mainline, 5.x improvements,
monitor mode support
```

---

**バリアント6 — タイムライン × コーポレートメンフィス**

![Infographic 6](/images/blog/baoyu-skills/infographic-6.webp)

```
AWUS036ACM product evolution timeline, corporate memphis flat vector style,
vibrant colors, showing WiFi adapter generations from 802.11n to ac to ax
```

---

## セクション03 — baoyu-xhs-images

小紅書（XHS）、Instagram、その他のSNSプラットフォーム向けに最適化された縦型カードシリーズ（3:4アスペクト比）を生成します。10種類のビジュアルスタイル × 8種類のレイアウトテンプレート。

**使用場面：** Instagram投稿、XHS製品カード、製品に特化したSNSコンテンツ。

### スタイルバリアント

**バリアント1 — Notion · デフォルト**

![XHS 1](/images/blog/baoyu-skills/xhs-1.webp)

```
小红书风格产品种草卡片, notion简约风格, 介绍Alfa AWUS036ACM WiFi网卡, 白色背景,
简洁排版, 重点标注: MT7612U芯片/AC1200双频/Linux免驱
```

---

**バリアント2 — ボールド · デフォルト**

![XHS 2](/images/blog/baoyu-skills/xhs-2.webp)

```
小红书爆款封面, 粗体大字bold风格, AWUS036ACM渗透测试神器推荐, 高对比度配色, 红黑白,
强烈视觉冲击, 关键词: Kali Linux必备
```

---

**バリアント3 — パステル · デフォルト**

![XHS 3](/images/blog/baoyu-skills/xhs-3.webp)

```
小红书粉彩风格种草图, pastel柔和色调, Alfa AWUS036ACM开箱分享, 奶油色背景,
可爱贴纸元素, 标注: 双天线/USB3.0/即插即用
```

---

**バリアント4 — Notion · リストレイアウト**

![XHS 4](/images/blog/baoyu-skills/xhs-4.webp)

```
小红书notion风格清单卡片, AWUS036ACM选购指南, 横向list布局, 列出5个购买理由,
简洁checklist样式, 适合技术宅
```

---

**バリアント5 — ボールド · 比較**

![XHS 5](/images/blog/baoyu-skills/xhs-5.webp)

```
小红书对比信息卡, bold风格, AWUS036ACM vs 普通WiFi网卡对比表, 左右对比布局,
突出MT7612U优势, 醒目配色
```

---

**バリアント6 — パステル · タイムライン**

![XHS 6](/images/blog/baoyu-skills/xhs-6.webp)

```
小红书pastel时间线卡片, AWUS036ACM从开箱到使用的步骤图, 纵向timeline布局,
温柔色调, 步骤: 开箱→插入USB→Linux免驱识别→开始使用
```

---

## セクション04 — baoyu-comic

複数のスタイルで連続アートを作成します：日本の漫画、韓国のウェブトゥーン、教育コミック。単一パネルと複数パネルのナラティブの両方をサポートします。

**使用場面：** SNSエンゲージメントコンテンツ、視覚的な製品チュートリアル、教育的な解説。

### スタイルバリアント

**バリアント1 — 漫画 · 技術製品レビュー**

![Comic 1](/images/blog/baoyu-skills/comic-1.webp)

```
Manga-style comic panel, tech reviewer character unboxing Alfa AWUS036ACM,
excited expression, speech bubble: "MT7612U in-kernel support?!", black and
white with screen tones, Japanese manga style
```

---

**バリアント2 — 漫画 · 楽しい3コマ漫画**

![Comic 2](/images/blog/baoyu-skills/comic-2.webp)

```
Fun manga comic strip 3-panels: panel1=struggling with WiFi drivers,
panel2=discovers AWUS036ACM, panel3=celebrating with Kali Linux working
perfectly. Chibi style characters
```

---

**バリアント3 — ウェブトゥーン · 教育的**

![Comic 3](/images/blog/baoyu-skills/comic-3.webp)

```
Webtoon vertical comic, educational explainer about how MediaTek MT7612U
driver works in Linux kernel, clean digital art style, character explains with
diagrams, colorful webtoon aesthetic
```

---

**バリアント4 — ウェブトゥーン · ミニマル**

![Comic 4](/images/blog/baoyu-skills/comic-4.webp)

```
Minimal webtoon style, 2-panel: hacker character with AWUS036ACM + Raspberry
Pi, clean lines, flat colors, caption: "Plug and play on any Linux distro
since kernel 4.19"
```

---

## セクション05 — baoyu-article-illustrator

記事の構造を分析し、各セクションに適切なイラストを生成します。「タイプ × スタイル」の二次元アプローチを使用します。

**使用場面：** コンセプトを説明するインライン挿絵が必要な技術ブログ記事。

### スタイルバリアント

**バリアント1 — RF信号ダイアグラム**

![Illustrator 1](/images/blog/baoyu-skills/illustrator-1.webp)

```
Technical RF signal diagram for AWUS036ACM, shows 2.4GHz and 5GHz signal
paths from MT7612U chip to dual RP-SMA antennas, clean engineering
illustration, blue on white
```

---

**バリアント2 — ライフスタイルシーン**

![Illustrator 2](/images/blog/baoyu-skills/illustrator-2.webp)

```
Lifestyle scene illustration: AWUS036ACM connected to laptop, person doing
WiFi security research, Kali Linux terminal visible on screen, cozy home
office setting, digital art style
```

---

**バリアント3 — スペックアイコンシート**

![Illustrator 3](/images/blog/baoyu-skills/illustrator-3.webp)

```
Icon sheet illustration: 8 icons representing AWUS036ACM features — dual
antenna, AC1200 badge, USB 3.0 connector, Linux penguin, monitor mode symbol,
packet injection, RPi logo, security shield. Flat design
```

---

**バリアント4 — ヒーローバナー**

![Illustrator 4](/images/blog/baoyu-skills/illustrator-4.webp)

```
Hero banner illustration for AWUS036ACM product page, wide format, adapter
floating center with WiFi signal waves, specs text panels on sides, tech
gradient background
```

---

## セクション06 — baoyu-imagine

最大限の創造的自由度を持つ自由形式のAI画像生成。固定されたレイアウトやスタイルの制約はありません——必要なビジュアルを自由に記述してください。

**使用場面：** EC向け製品レンダリング、ライフスタイル写真の代替、技術的な分解図、カスタムシーン生成。

### スタイルバリアント

**バリアント1 — フォトリアル正面ビュー**

![Imagine 1](/images/blog/baoyu-skills/imagine-1.webp)

```
Photorealistic product render of Alfa AWUS036ACM WiFi USB adapter, front view,
black housing, two adjustable RP-SMA antennas, USB 3.0 connector visible,
white background, studio lighting
```

---

**バリアント2 — 3/4アングル製品レンダリング**

![Imagine 2](/images/blog/baoyu-skills/imagine-2.webp)

```
Alfa AWUS036ACM 3/4 angle product render, showing side profile, antenna
adjustment, LED indicator, clean white background, soft shadows, commercial
photography style
```

---

**バリアント3 — ライフスタイルシーン**

![Imagine 3](/images/blog/baoyu-skills/imagine-3.webp)

```
Lifestyle product photo: AWUS036ACM plugged into a laptop USB port, Kali Linux
desktop visible on screen with WiFi scanning tool, dark desk setup, blue LED
glow
```

---

**バリアント4 — 技術的分解図**

![Imagine 4](/images/blog/baoyu-skills/imagine-4.webp)

```
Technical exploded view illustration of AWUS036ACM internals: PCB with
MT7612U chip, USB 3.0 connector, antenna connectors, RF shielding can, labels
for each component
```

---

## スタイルリファレンスとしての使い方

マーケティング画像を生成する際は、本記事をルックアップテーブルとしてご活用ください。判断の流れはシンプルです：

**1. この画像はどのプラットフォーム向けですか？**

| プラットフォーム | 推奨スキル | アスペクト比 |
|----------------|-----------|------------|
| ブログ記事カバー | `baoyu-cover-image` | シネマティック 2.35:1 またはワイドスクリーン 16:9 |
| Instagram / XHS投稿 | `baoyu-xhs-images` | 3:4 縦型 |
| LinkedIn / Twitter | `baoyu-cover-image`（スクエア） | 1:1 |
| 技術記事インライン | `baoyu-article-illustrator` | 状況による |
| プレゼンテーションスライド | `baoyu-slide-deck` | 16:9 |
| 製品ページレンダリング | `baoyu-imagine` | カスタム |
| スペック概要投稿 | `baoyu-infographic` | 状況による |
| SNSエンゲージメントコンテンツ | `baoyu-comic` | 状況による |

**2. スタイルを選択する** — 本記事でブランドトーンに合ったバリアントを見つけ、プロンプトをコピーして、製品名と主要スペックをターゲット製品のものに置き換えてください。

**3. GitHub Copilot CLIでスキルを実行する**：

```bash
# 例 — カバー画像を生成
/baoyu-cover-image

# 例 — Instagramカードを生成
/baoyu-xhs-images

# 例 — 製品レンダリングを生成
/baoyu-imagine
```

**4. スキルのガイドプロンプトに従う** — 各スキルは生成前に、スタイル、サイズ、コンテンツについて確認の質問をします。

---


---

{{< faq >}}

## baoyu-skillsについて

baoyu-skillsプラグインコレクションの全容はGitHubでご覧いただけます：

➜ [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills.git)

本記事のすべての画像は、ALFA AWUS036ACMを製品サンプルとして上記のスキルを使用して生成されました。すべての画像の完全なプロンプトリファレンスは、社内ワークフローガイドに記録されています。

本ガイド全体を通じてサンプルとして使用したAWUS036ACMについて、詳しく知りたい方はこちら：

{{< button href="/ja/products/alfa/awus036acm/" >}}AWUS036ACM製品ページを見る{{< /button >}}

---

## 参考文献

1. [baoyu-skills GitHubリポジトリ](https://github.com/JimLiu/baoyu-skills.git)
2. [GitHub Copilot CLI公式ドキュメント](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
3. [ALFA Network AWUS036ACM製品仕様](https://www.alfa.com.tw/)
4. [MediaTek MT7612Uチップセット情報](https://www.mediatek.com/products/networking-and-connectivity)
5. [OpenAI画像生成APIドキュメント](https://platform.openai.com/docs/guides/images)
