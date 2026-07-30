---
title: "Sierra Wireless セルラーモジュール完全選定ガイド：LTE Cat 4 から 5G mmWave まで"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - セルラーモジュール
  - 4g-lte
  - 5g-nr
  - モジュール選定
  - em7455
  - em9190
  - m2-pcie
categories:
  - 製品選定ガイド
series:
  - sierra-wireless-selection
series_order: 1
description: "Yupitek が Sierra Wireless（Semtech）の EM/MC シリーズ全10種類のセルラーモジュールを比較。EM7455、EM9190、MC7455 など、LTE Cat 4 から 5G mmWave までの選定ポイントを解説。"
author: "yupitek"
draft: false
faq:
  - question: "Sierra Wireless にはどのようなモデルがありますか？それぞれの違いは何ですか？"
    answer: "Sierra Wireless には EM シリーズと MC シリーズの 2 シリーズ、合計 10 モデルのセルラーモジュールがあり、LTE Cat 4 / Cat 6 / Cat 12 から 5G Sub-6、mmWave までをカバーしています。最大の違いはパッケージです。EM シリーズは M.2、MC シリーズは mPCIe を採用しています。同じチップセットのモデル（EM7455 と MC7455 など）は性能が同一で、スロット形状のみが異なります。"
  - question: "EM7455 と MC7455 は同じチップセットですか？"
    answer: "はい、同じです。両モデルとも Qualcomm MDM9230 チップセットを採用し、ダウンロード/アップロードのピーク速度はともに 300 / 50 Mbps、2×CA キャリアアグリゲーションに対応しており、スペックは完全に同一です。唯一の違いは、EM7455 が M.2 パッケージ、MC7455 が mPCIe パッケージである点です。"
  - question: "5G モジュールは必ず mmWave（EM9191）を選ぶ必要がありますか？日本でも使用できますか？"
    answer: "必ずしも必要ではありません。日本では現在 Sub-6 が主流であり、mmWave は主に米国市場向け（n260/n261）のエリアで展開されています。一般的な日本での用途であれば EM9190（Sub-6 エントリー 5G）で十分です。mmWave 対応が必要な場合は EM9191 をお選びください。"
  - question: "M.2 と mPCIe のセルラーモジュールはどのように選べばよいですか？"
    answer: "お客様の機器のスロットによって異なります。ノートPCや最新の組み込みマザーボードの多くは M.2 B-Key スロットを採用しており、その場合は EM シリーズを選択します。旧型の産業用ルーターや産業用コンピュータが mPCIe スロットの場合は MC シリーズを選択します。マザーボードが M.2 スロットのみで MC シリーズを使用したい場合は、M.2 to mPCIe 変換アダプタが必要です。"
  - question: "Sierra Wireless は日本でどこで購入できますか？"
    answer: "日本のお客様は Yupitek（榆閤科技）を通じて Sierra Wireless 全シリーズのセルラーモジュールを購入いただけます。Yupitek 公式サイトの製品ページで型番と価格をご確認いただくか、メール（sales@yupitek.com）にてお問い合わせください。"
---

セルラーモジュールの調達で最も怖いのは、「スペック表が読めない、モデルが多すぎて区別がつかない、間違ったパッケージを買って機器に挿さらない」ということです。この記事では、Sierra Wireless の現行モデルとロングセラーモデルを含む全 10 モデルを一度にわかりやすく解説し、LTE Cat 4 から 5G mmWave までの選定をサポートします。

Sierra Wireless は現在 Semtech の一部です。本記事は Yupitek（榆閤科技）が作成し、Sierra Wireless の全 10 モデルのセルラーモジュール（EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455）を網羅しています。EM シリーズは M.2 パッケージ、MC シリーズは mPCIe パッケージです。

本記事の技術資料は Yupitek（榆閤科技）が作成しました。

Sierra Wireless の全 10 モデルは、LTE Cat 4 / 6 / 12 から 5G Sub-6、mmWave までをカバーしています。EM シリーズと MC シリーズの違いはパッケージのみで、EM は M.2、MC は mPCIe となります。

## 10モデル比較一覧表

まずは比較表をご覧ください。数値は公式スペックシートに基づいて記載しています。EM9190/EM9191 の上りピーク値は情報源によって若干の差異があります。実際のご購入前には、最新の公式スペックシートまたはお問い合わせにてご確認ください（詳細は文末の付録リンクをご参照ください）。

| モデル | セルラー規格 | チップセット | 下り/上りピーク速度 | キャリアアグリゲーション | 5G | ミリ波 | パッケージ | GNSS | 備考 |
|---|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/ja/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | エントリー Cat 6（実際の周波数帯構成についてはお問い合わせください） |
| [EM7455](https://yupitek.com/ja/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | コミュニティで最も人気、情報量最多 |
| [EM7511](https://yupitek.com/ja/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 高速アップロード Cat 12 |
| [EM7565](https://yupitek.com/ja/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | CBRS/LAA 対応（実際の認証範囲についてはお問い合わせください）、最多周波数帯、最高アップロード速度 |
| [EM9190](https://yupitek.com/ja/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下り 2.5 Gbps（上りピーク値についてはお問い合わせください） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 エントリー5G |
| [EM9191](https://yupitek.com/ja/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下り最大 4.5 Gbps（ミリ波含む）/ Sub-6 2.5 Gbps（上りピーク値についてはお問い合わせください） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | フラッグシップ5G、ミリ波対応 |
| [MC7304](https://yupitek.com/ja/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | エントリー Cat 4（EOL 間近） |
| [MC7350](https://yupitek.com/ja/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、北米周波数帯 |
| [MC7354](https://yupitek.com/ja/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、グローバル周波数帯 |
| [MC7455](https://yupitek.com/ja/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | mPCIe 版 EM7455 |

> 備考：EM9190 と EM9191 は同一の EM919x/EM7690 仕様書を共有しています。EM9190 は Sub-6 エントリー5G、EM9191 はミリ波対応のフラッグシップモデルです。この公式仕様書は会員ログイン後のダウンロードとなります。当社が現在引用している下りピーク値は公開情報から整理したものであり、上りピーク値などの詳細な数値については、ご注文前に直接お問い合わせいただき、最新版をご確認いただくことをおすすめします。

## EM シリーズ（M.2） vs MC シリーズ（mPCIe） パッケージの違い

これは選定における最初の関門であり、最も多くの方が間違えやすいポイントです。

**EM シリーズ = M.2 B-Key パッケージ**：小型（約 30×42 mm）で、ノートPCの WWAN スロットや組み込み M.2 スロット向けに設計されており、最新の産業用マザーボードやミニPCの多くで採用されています。

**MC シリーズ = Mini PCIe（mPCIe）パッケージ**：一般的な PC 拡張カードと同様の形状で、旧型の産業用ルーターや産業用コンピュータの mPCIe スロットに適しています。マザーボードが M.2 スロットのみの場合は、MC シリーズを使用するために変換アダプタ（M.2 to mPCIe）が必要です。

**共通のハードウェア要件**：どちらも外部 SIM カードスロットとアンテナが必要です。アンテナは主に U.FL コネクタで、標準構成は 2×2 MIMO（メインアンテナ + ダイバーシティアンテナ）に GNSS 測位アンテナを加えたものとなります。

**よく寄せられる質問**：EM7455 と MC7455 は「同じチップセットでパッケージのみが異なります」。両モデルとも Qualcomm MDM9230 を採用し、スペックは完全に同一であり、違いは M.2 と mPCIe のパッケージのみです。したがって、どちらを選ぶかはお客様の機器のスロット形状のみで決まります。

## アプリケーション別の選定推奨

### 無線LANルーター / CPE（OpenWrt / ROOter）

**推奨：[EM7455](https://yupitek.com/ja/products/sierra/em7455/) / [MC7455](https://yupitek.com/ja/products/sierra/mc7455/)**
理由：コミュニティリソースが最も豊富で、ROOter（OpenWrt ベースのセルラー路由ルーター用ファームウェア）のチュートリアルや QMI/MBIM 設定例が最も充実しており、問題発生時にも情報を見つけやすいためです。

### ノートPC WWAN アップグレード

**推奨：[EM7430](https://yupitek.com/ja/products/sierra/em7430/) / [EM7455](https://yupitek.com/ja/products/sierra/em7455/)**
理由：いずれも M.2 パッケージで、Dell、Lenovo などのビジネスノートPCの WWAN スロットに対応します。EM7455 は周波数帯の対応情報が広く知られており、中古価格も手頃で、アップグレードの第一選択肢です（実際の周波数帯とお客様の通信事業者の互換性については、ご注文前にお問い合わせください）。

### 産業用ルーター / ゲートウェイ（広温度範囲、認証、長期供給）

**推奨：EM75 シリーズ（[EM7511](https://yupitek.com/ja/products/sierra/em7511/)、[EM7565](https://yupitek.com/ja/products/sierra/em7565/)）、[EM9190](https://yupitek.com/ja/products/sierra/em9190/)/[EM9191](https://yupitek.com/ja/products/sierra/em9191/)、[MC7455](https://yupitek.com/ja/products/sierra/mc7455/)**
理由：産業用途では、広温度範囲（−40°C 対応オプション）、認証の完全性、長期供給保証が重要です。Cat 12 および 5G モジュールは、より高いアップロード速度と将来の帯域余裕を提供します。実際の温度範囲仕様と認証一覧については公式スペックシートをご確認いただき、正式な選定の際には当社まで最新情報をお問い合わせください。

### コネクテッドカー / 車両テレマティクス（GNSS 測位）

**推奨：[EM7455](https://yupitek.com/ja/products/sierra/em7455/) / [EM7565](https://yupitek.com/ja/products/sierra/em7565/) / [EM9191](https://yupitek.com/ja/products/sierra/em9191/)**
理由：3 モデルとも GNSS を内蔵しており、車両追跡と位置情報の報告に適しています。5G の高速通信が必要な車載アプリケーションには EM9191 をお選びください。

### 5G プライベートネットワーク / CBRS

**推奨：[EM9191](https://yupitek.com/ja/products/sierra/em9191/)（CBRS 対応）、[EM7565](https://yupitek.com/ja/products/sierra/em7565/)（CBRS/LAA 対応）**
理由：CBRS（米国 3.5 GHz 共有周波数帯）と LAA はプライベートネットワークで一般的な要件です。EM9191 と EM7565 はハードウェアで対応周波数帯をサポートしています。実際のプライベートネットワーク導入にあたっては、周波数帯の組み合わせと関連認証について、現地の法規制および通信環境に応じたご確認が必要です。当社までお問い合わせいただき、総合的な技術評価をご依頼ください。

### 映像監視 / デジタルサイネージの高速バックホール

**推奨：[EM9190](https://yupitek.com/ja/products/sierra/em9190/) / [EM9191](https://yupitek.com/ja/products/sierra/em9191/)**
理由：5G の高速通信（下り最大 Sub-6 2.5 Gbps、ミリ波対応時最大 4.5 Gbps）は、マルチチャンネル映像のリアルタイム伝送や 4K サイネージのストリーミングに適しています。

### 既存機器の修理 / 長期保守部品（Cat 4）

**推奨：[MC7304](https://yupitek.com/ja/products/sierra/mc7304/) / [MC7350](https://yupitek.com/ja/products/sierra/mc7350/) / [MC7354](https://yupitek.com/ja/products/sierra/mc7354/)**
理由：mPCIe パッケージの Cat 4 モジュールは、旧型機器の修理部品として最適です。ただし、MC73xx シリーズは EOL（製造終了）が近づいているため、長期の部品調達をお考えの場合は [EM7455](https://yupitek.com/ja/products/sierra/em7455/) または [EM7565](https://yupitek.com/ja/products/sierra/em7565/) への移行をご検討いただくことをおすすめします。これらのモデルの方が長期的な供給保証が期待できます。

## お問い合わせ / ご購入について

選定にお迷いですか？日本のお客様は Yupitek（榆閤科技）を通じて、本記事でご紹介した EM/MC シリーズの Sierra セルラーモジュール全 10 モデルをご購入いただけます。関連アンテナ、SIM 変換アダプタ、評価ボードも取り扱っております。スペック確認、周波数帯比較、数量割引、技術導入サポートを提供しております。

## よくあるご質問

**Q1：Sierra Wireless にはどのようなモデルがありますか？それぞれの違いは何ですか？**
Sierra Wireless には EM シリーズと MC シリーズの 2 シリーズ、合計 10 モデルのセルラーモジュールがあり、LTE Cat 4 / Cat 6 / Cat 12 から 5G Sub-6、mmWave までをカバーしています。最大の違いはパッケージです。EM シリーズは M.2、MC シリーズは mPCIe を採用しています。同じチップセットのモデル（EM7455 と MC7455 など）は性能が同一で、スロット形状のみが異なります。

**Q2：EM7455 と MC7455 は同じチップセットですか？**
はい、同じです。両モデルとも Qualcomm MDM9230 チップセットを採用し、ダウンロード/アップロードのピーク速度はともに 300 / 50 Mbps、2×CA キャリアアグリゲーションに対応しており、スペックは完全に同一です。唯一の違いは、EM7455 が M.2 パッケージ、MC7455 が mPCIe パッケージである点です。

**Q3：5G モジュールは必ず mmWave（EM9191）を選ぶ必要がありますか？日本でも使用できますか？**
必ずしも必要ではありません。日本では現在 Sub-6 が主流であり、mmWave は主に米国市場向け（n260/n261）のエリアで展開されています。一般的な日本での用途であれば EM9190（Sub-6 エントリー 5G）で十分です。mmWave 対応が必要な場合は EM9191 をお選びください。

**Q4：M.2 と mPCIe のセルラーモジュールはどのように選べばよいですか？**
お客様の機器のスロットによって異なります。ノートPCや最新の組み込みマザーボードの多くは M.2 B-Key スロットを採用しており、その場合は EM シリーズを選択します。旧型の産業用ルーターや産業用コンピュータが mPCIe スロットの場合は MC シリーズを選択します。マザーボードが M.2 スロットのみで MC シリーズを使用したい場合は、M.2 to mPCIe 変換アダプタが必要です。

**Q5：Sierra Wireless は日本でどこで購入できますか？**
日本のお客様は Yupitek（榆閤科技）を通じて Sierra Wireless 全シリーズのセルラーモジュールを購入いただけます。Yupitek 公式サイトの製品ページで型番と価格をご確認いただくか、メール（sales@yupitek.com）にてお問い合わせください。

## 付録：10モデル公式スペックシートリンク

以下のリンクは Sierra Wireless 公式テクニカルリソースライブラリ（source.sierrawireless.com）からのものです。一部の文書は会員登録後のログインが必要です。本記事のスペック数値は公開情報から整理したものです。項目ごとに最終的なスペック数値（特に EM9190/EM9191 の上りピーク値）をご確認される場合は、当社まで公式文書をお問い合わせください。

- **EM7430**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
