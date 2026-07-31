---
title: "Sierra Wireless セルラーモジュール選定ガイド：LTE Cat 4 から 5G mmWave まで"
description: "Sierra Wireless（Semtech）の EM/MC シリーズ全10モデルのセルラーモジュールを、LTE Cat 4 から 5G mmWave まで仕様比較と選定アドバイス付きで解説。技術資料は Yupitek（榆閤科技）が提供。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Sierra Wireless にはどのようなモデルがあり、どのように違うのでしょうか？"
    answer: "Sierra Wireless には EM と MC の2つのシリーズ、全10モデルがあり、LTE Cat 4 / Cat 6 / Cat 12 から 5G Sub-6 と mmWave までをカバーしています。最大の違いはパッケージで、EM は M.2、MC は mPCIe です。同じチップセットを搭載するモデル（EM7455 と MC7455 など）は性能が同じで、コネクタ形状のみが異なります。"
  - question: "EM7455 と MC7455 は同じチップなのでしょうか？"
    answer: "はい。どちらも Qualcomm MDM9230 チップセットを採用し、下り/上りピークは同じ 300 / 50 Mbps、2×CA キャリアアグリゲーションにも対応しており、仕様は完全に同じです。唯一の違いは、EM7455 が M.2、MC7455 が mPCIe というパッケージです。"
  - question: "5G プロジェクトには mmWave 対応の EM9191 が必ず必要ですか？日本でも使えますか？"
    answer: "必須ではありません。日本の 5G 通信環境は現在 Sub-6 が中心で、mmWave は主に米国仕様の環境（n260/n261 など）で利用されています。通常の用途であれば EM9190（Sub-6 の低価格 5G）で十分です。米国仕様のミリ波テストの要件がある場合のみ EM9191 が必要です。"
  - question: "M.2 と mPCIe のセルラーモジュールはどちらを選べばよいですか？"
    answer: "お使いのハードウェアのスロットで決まります。ノートPCや最新の組み込みマザーボードは多くが M.2 B-Key なので EM シリーズを、旧型の産業用ルーターやパネルPC が mPCIe スロットの場合は MC シリーズを選びます。M.2 しかないボードで MC を使いたい場合は、M.2 to mPCIe 変換アダプターが必要です。"
  - question: "Sierra Wireless のモジュールはどこで購入できますか？"
    answer: "Yupitek（榆閤科技）にて Sierra Wireless 全シリーズのセルラーモジュールをご購入いただけます。Yupitek 公式サイトの製品ページで型番と価格をご確認いただくか、sales@yupitek.com まで直接お問い合わせください。"
---

# Sierra Wireless セルラーモジュール選定ガイド：LTE Cat 4 から 5G mmWave まで

IoT プロジェクトに取り組む学生の方も、研究室でネットワーク機器を開発しているエンジニアの方も、通信モジュールの購入で最も悩むのは「仕様表を眺めても型番が区別できず、結局フォームファクタを間違えてボードに挿さらない」というケースではないでしょうか。

本記事では、Sierra Wireless（現在は Semtech 傘下）の現行・ロングセラーを含む全10モデルを、エントリー向けの LTE Cat 4 から 5G mmWave まで一通り解説します。EM シリーズはすべて M.2 パッケージ、MC シリーズは mPCIe パッケージです。

技術資料は Yupitek（榆閤科技）が提供しています。

## 全10モデル仕様一覧：データで直接比較

まずは重要な表をご覧ください。数値はすべて公式スペックシートに基づいて整理しています。なお、EM9190/EM9191 の上りピーク値は情報源によって若干異なる場合があります。実際にプロジェクトで購入される場合は、最新の公式スペックシートをご確認いただくか、直接お問い合わせください（記事末の付録にリンクがあります）。

| 型番 | セルラー規格 | チップセット | 下り / 上りピーク | キャリアアグリゲーション | 5G | mmWave | パッケージ | GNSS | 備考 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/ja/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | エントリー向け Cat 6（実周波数帯構成はお問い合わせください） |
| [EM7455](/ja/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | オープンソースコミュニティで最も人気 |
| [EM7511](/ja/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 上りに強い Cat 12 |
| [EM7565](/ja/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | CBRS/LAA バンド対応、対応バンド数・上り速度で最上位 |
| [EM9190](/ja/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下り 2.5 Gbps（上りピークはお問い合わせください） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 低価格 5G のエントリー向け |
| [EM9191](/ja/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下り最大 4.5 Gbps（mmWave 含む）/ Sub-6 2.5 Gbps（上りピークはお問い合わせください） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | フラッグシップ 5G、ミリ波にも対応 |
| [MC7304](/ja/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | エントリー向け Cat 4（EOL 生産終了に近い） |
| [MC7350](/ja/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、北米バンド中心 |
| [MC7354](/ja/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、グローバルバンド中心 |
| [MC7455](/ja/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | 簡単に言えば mPCIe 版の EM7455 |

> 備考：EM9190 と EM9191 は同じ EM919x/EM7690 スペックシートを共有しています。EM9190 は Sub-6 の低価格 5G、EM9191 は mmWave を追加したフラッグシップモデルです。公式スペックシートのダウンロードには会員登録が必要なため、上表の下りピーク値は公開情報から整理しています。上りピークなどの詳細は、発注前に最新版を確認のうえご相談いただくのが安心です。

## 最初の関門：EM シリーズ（M.2）と MC シリーズ（mPCIe）の違い

これは初心者が選定で最もつまずきやすいポイントです。間違えて購入すると挿さらず、大変困ったことになります。

**EM シリーズ = M.2 B-Key パッケージ**：ノートPCに SSD を挿すようなインターフェースをイメージしてください。非常に小型で（約 30×42 mm）、ノートPCの WWAN スロットや組み込み M.2 スロット向けに設計されています。最近の産業用マザーボードやミニPC はほとんどがこのタイプです。

**MC シリーズ = Mini PCIe（mPCIe）パッケージ**：従来の PC 拡張カードのような外観で、旧型の産業用ルーターやパネルPC の mPCIe スロットに向いています。ボードに M.2 スロットしかない場合、MC シリーズを使うには別途変換アダプター（M.2 から mPCIe）が必要です。

**共通点**：どちらも外部 SIM カードホルダーとアンテナが必要です。アンテナコネクタは通常 U.FL で、標準構成は 2×2 MIMO（メインアンテナ 1 本 + ダイバーシティアンテナ 1 本）、さらに GNSS 測位アンテナが 1 本追加されます。

**よくある質問**：EM7455 と MC7455 の違いは？答えは「同じチップで、パッケージだけが違う」です。どちらも Qualcomm MDM9230 を搭載し、仕様はまったく同じなので、選択はお使いのボード次第ということになります。

## プロジェクトや用途に応じたおすすめ選定

### 1. 自前で無線ルーター / CPE を構築（OpenWrt または ROOter）

**おすすめ：[EM7455](/ja/products/sierra/em7455/) / [MC7455](/ja/products/sierra/mc7455/)**
理由は単純で、ネット上のオープンソースコミュニティの情報が最も多いためです。ROOter（OpenWrt ベースのファームウェア）を使えば、チュートリアルや QMI/MBIM の設定例が非常に充実しており、トラブルに陥っても検索で解決できます。

### 2. 旧ノートPC の WWAN カードをアップグレード

**おすすめ：[EM7430](/ja/products/sierra/em7430/) / [EM7455](/ja/products/sierra/em7455/)**
この2モデルはどちらも M.2 パッケージで、Dell や Lenovo などのビジネスノートPC の WWAN スロットに適しています。特に EM7455 は中古価格が手頃なことが多く、アップグレードの第一候補です（ただし実際のバンドがお使いの通信事業者に合うかは、発注前にご確認ください）。

### 3. 産業用ルーター / IoT ゲートウェイ（堅牢性とワイドテンプレート重視）

**おすすめ：EM75 シリーズ（[EM7511](/ja/products/sierra/em7511/)、[EM7565](/ja/products/sierra/em7565/)）、[EM9190](/ja/products/sierra/em9190/)/[EM9191](/ja/products/sierra/em9191/)、[MC7455](/ja/products/sierra/mc7455/)**
産業向けプロジェクトで最も重視されるのは、ワイドテンプレート（例：-40°C ~ +85°C の過酷な環境）、認証の有無、そして長期的に入手できるかどうかです。Cat 12 および 5G モジュールは上り帯域が広く、将来の拡張性にも優れています。実際の温度仕様は公式の最新ドキュメントでご確認ください。

### 4. コネクテッドカー / 車両追跡（GNSS 測位が必要）

**おすすめ：[EM7455](/ja/products/sierra/em7455/) / [EM7565](/ja/products/sierra/em7565/) / [EM9191](/ja/products/sierra/em9191/)**
コネクテッドカーのプロジェクトでは正確な測位が必要になることが多く、この3モデルは GNSS を内蔵しており、通信と測位を1枚で解決できます。5G の大帯域が必要な場合は、EM9191 をお選びください。

### 5. 5G プライベートネットワーク / CBRS 実験

**おすすめ：[EM9191](/ja/products/sierra/em9191/)（CBRS バンド対応）、[EM7565](/ja/products/sierra/em7565/)（CBRS/LAA バンド対応）**
CBRS（米国仕様の 3.5 GHz 共有バンド）や LAA を研究室で検討する場合、この2モデルはハードウェアで対応しています。ただし実際に現地でプライベートネットワークをテストする際は、現地の法規制や通信環境に依存しますので、導入前に技術的な詳細についてご相談ください。

### 6. 映像監視 / 高画質映像のバックホール

**おすすめ：[EM9190](/ja/products/sierra/em9190/) / [EM9191](/ja/products/sierra/em9191/)**
5G の帯域が十分に大きいため（Sub-6 で下り最大 2.5 Gbps、mmWave 込みで最大 4.5 Gbps）、複数系統の映像リアルタイム伝送や 4K ストリーミングに最適です。

### 7. 旧設備の修理 / 実験室の老朽機器の予備部品（Cat 4）

**おすすめ：[MC7304](/ja/products/sierra/mc7304/) / [MC7350](/ja/products/sierra/mc7350/) / [MC7354](/ja/products/sierra/mc7354/)**
mPCIe パッケージの旧機器修理には第一候補です。ただし正直なところ、MC73xx シリーズは EOL（生産終了）に近づいています。長期的なプロジェクトでは、[EM7455](/ja/products/sierra/em7455/) や [EM7565](/ja/products/sierra/em7565/) への移行を検討するのが安心です。

## 選定で迷ったら、お気軽にご相談ください

ご覧になっても選び方が分からない場合は、Yupitek（榆閤科技）にて EM/MC シリーズ全10モデルのセルラーモジュールをご購入いただけます。アンテナ、SIM 変換アダプター、評価ボードまで一式ご用意できます。仕様確認、バンド比較、プロジェクトに必要な見積もりや技術サポートまで、お気軽にお問い合わせください。

## よくある質問（FAQ）

{{< faq >}}

## 付録：全10モデル公式スペックシートへのリンク

以下のリンクは Sierra Wireless 公式の技術リソースライブラリ（source.sierrawireless.com）に接続します。**一部のドキュメントは PDF のダウンロードに会員登録が必要です。** 記事内の数値は公開情報から整理したもので、細かい仕様（例：EM9190/EM9191 の上りピーク）を項目ごとに確認したい場合は、最新の公式ドキュメントを直接ご請求ください。

- **EM7430**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
