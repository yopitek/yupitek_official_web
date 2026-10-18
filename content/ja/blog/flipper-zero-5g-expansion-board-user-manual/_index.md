---
title: "Flipper Zero 5G Expansion Board 図解インストール・使用マニュアル (v2.0)"
description: "本ガイドは、Flipper Zero 5G 拡張モジュールのインストールおよび操作ガイド v2.0 です。高解像度のアイソメトリック設計図を用いて、初心者の方向けにアンテナ、スロットの取り付け、および GPIO 設定をわかりやすく解説します。"
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Flipper Zero 5G Expansion Board 図解インストール・使用マニュアル (v2.0)

> **対象読者**：本モジュールを初めて使用されるお客様。  
> **作成方針**：間違いやすい手順やわかりにくい専門用語について、高解像度の設計図を用いてステップごとに詳しく解説します。文章から推測することなく、スムーズにインストールすることができます。

---

## 00. 開封と付属品リスト

Flipper Zero 5G 拡張モジュールをご利用いただき、ありがとうございます。開始する前に、パッケージに以下の付属品がすべて揃っているかご確認ください。

![開封時の付属品一覧](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*図 1：開封時の付属品一覧*

### ⚠️ 付属品リストの説明
*   **標準パッケージに含まれるもの**：
    1.  5G 拡張ボードメインモジュール (5G Expansion Board) x 1
    2.  433MHz ロッドアンテナ (短い黒アンテナ) x 1
    3.  GPS アクティブセラミックアンテナ (正方形アンテナ) x 1
    4.  WiFi デュアルバンドパッチアンテナ (黒のフラットアンテナ) x 1
*   **含まれないもの (ご自身でご用意ください)**：
    *   **Flipper Zero 本体** (本モジュールには本体は付属していません)
    *   **MicroSD カード** (モジュールの動作に必須です。別途ご購入ください)

---

## 01. 5G モジュールの各部名称

アンテナの取り付けや本体への接続を行う前に、モジュールの主要なインターフェースとハードウェアレイアウトを一度ご確認ください。

### 前面インターフェースの説明

![モジュール前面の各部名称](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*図 2：前面ハードウェア配置の説明*

*   **ディスプレイ (LCD Screen)**：現在の接続ステータス、IP アドレス、動作モードを表示します。
*   **トグルスイッチ (Toggle Switch)**：モジュールディスプレイの電源を制御します。上に切り替えるとオンになります。
*   **MicroSD カードスロット (SD Card Slot)**：システムファームウェアの設定やログデータの保存に使用します。
*   **GPIO ソケット**：Flipper Zero 本体の頂部にある GPIO ピンと接続するためのソケットです。
*   **インジケータ (LED Indicators)**：電源と充電ステータスを表示します。

### 側面アンテナポートの説明

![側面アンテナポートの説明](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*図 3：アンテナポートの位置と印字*

*   **433M A**：433MHz ロッドアンテナを接続します。
*   **GPS**：GPS セラミックアンテナを接続します。
*   **2.4G** および **2.4G/5G**：WiFi デュアルバンドパッチアンテナを接続します。

> ⚠️ **出荷ロットによるバージョンに関する重要なお知らせ**：  
> アンテナポートの位置は、生産ロットによって若干調整される場合があります（例：GPS と WiFi 接続ポートの位置が左右逆になるなど）。**必ずお手元のモジュール筐体に印字されている実際のラベルをご確認の上、接続してください。** 破損や信号劣化の原因となりますので、記憶違いなどによる誤接続にご注意ください。

---

## 02. インストール手順 (Step-by-Step)

### Step 1 | MicroSD カードの準備と取り付け

5G モジュールは設定を保存するために MicroSD カードが必要です。

1.  **仕様要件**：容量は **32GB 以下**、フォーマットは **FAT32** である必要があります。
2.  **カードの向き**：金属端子面を下に向けて MicroSD カードスロットに挿入し、カチッと音がするまで軽く押し込みます。

![MicroSD カードスロットの拡大図](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*図 4：MicroSD カードの正しい挿入方向の拡大図*

---

### Step 2 | 3本のアンテナの取り付け

標準付属の 3 本のアンテナを対応する SMA アンテナコネクタにネジで固定します。無理な力を加えすぎず、しっかりと密着するまで回してください。

![アンテナ取り付け接続図](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*図 5：3 種類のアンテナの固定および接続方法のイメージ*

| アンテナタイプ | 対応アンテナポート | 取り付け説明 |
| :--- | :--- | :--- |
| **GPS セラミックアンテナ** | **GPS ポート** | コネクタが正方形のセラミックベースで、長いケーブルが付属しています |
| **WiFi デュアルバンドパッチアンテナ** | **2.4G/5G ポート** | 黒いフラットパッチアンテナです |
| **433MHz ロッドアンテナ** | **433M A ポート** | 黒い短いロッド型のハードアンテナです |

#### ⚠️ GPS アンテナの向きに関する警告
GPS アンテナには指向性があります。取り付ける際は、**セラミック面 (通常は両面テープが貼られている面の裏側、または文字が印刷されていない面) を必ず上 (空に向く方向) に向けてください。** 向きが異なると正常に測位できません。

![GPS アンテナの向き比較図](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*図 6：GPS アンテナの正しい向き (空向き) と誤った向き (地面向き) の比較*

---

### Step 3 | Flipper Zero 本体との接続

5G モジュールを Flipper Zero 頂部の GPIO ピンに挿入します。

1.  ホットプラグによるハードウェアの破損を防ぐため、事前に **Flipper Zero の電源を切ってください。**
2.  Flipper Zero 頂部の GPIO ピンとモジュール底部のソケットの位置を合わせます。

![GPIO 接続のアライメント図](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*図 7：GPIO 接続位置とアライメントライン*

3.  両手で均等に力を加え、モジュールを**一番奥まで軽く押し込みます。**
4.  **密着度の確認**：接続完了後、側面から確認し、モジュールと Flipper Zero の間に**隙間が一切なく、完全に密着していること**をご確認ください。

![GPIO 挿入の密着度確認](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*図 8：完全に挿入され、隙間のない正しい接続状態*

---

### Step 4 | Flipper Zero のソフトウェア設定

接続が完了したら、Flipper Zero の電源を入れ、ソフトウェアの GPIO ピン設定を行います。

ここでは **Momentum ファームウェア** を例に説明します。以下のパスに移動して設定を行ってください。

1.  **ディスプレイの電源を入れる**：モジュールの左手前にあるトグルスイッチを **UP** の位置に切り替えます。
    ![トグルスイッチの拡大図](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *図 9：トグルスイッチを UP の位置に切り替えてディスプレイを表示*

2.  **GPS ピン設定**：
    *   パス：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   設定値：**13** または **14** に変更します (マニュアルまたはハードウェアの出荷仕様に従ってください)。
3.  **ESP32 ピン設定 (WiFi/Bluetooth 機能)**：
    *   パス：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   設定値：**15, 16** に変更します。
4.  **433MHz 送受信モジュール設定**：
    *   `Sub-GHz` ➔ `Advanced Settings` に移動し、Module を **External** に変更します (外部アンテナを有効にします)。

---

### Step 5 | 充電とバッテリー残量の確認

本モジュールには充電式バッテリーが内蔵されています。

![USB-C ポートの比較と警告](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*図 10：上部の充電専用ポート (CHARGE ONLY) と側面の書き込み専用ポート (FLASH ONLY) の比較*

*   **上部の USB-C ポート**：**充電専用です** (CHARGE ONLY と表記)。充電の際はこちらのポートに接続してください。
*   **側面の USB-C ポート**：**ファームウェアの書き込み専用です** (FLASH ONLY と表記)。日常の充電には使用しないでください。バッテリーは充電されません。

#### バッテリー LED インジケータのステータス：
モジュールの前面には、バッテリー残量をパーセンテージで表示する 4 つのインジケータ LED があります。

![バッテリーインジケータの説明](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*図 11：4 つの LED が示すバッテリー残量*

*   1 つ点灯：残量約 25% (速やかに充電してください)
*   2 つ点灯：残量約 50%
*   3 つ点灯：残量約 75%
*   4 つ点灯：残量 100% (満充電)

---

## 03. トラブルシューティングチェックリスト (初心者向け)

モジュールが正常に動作しない場合は、以下の項目を順に確認してください。

*   [ ] **GPIO ピンは奥まで完全に挿入されていますか？** (モジュールと Flipper Zero の間に隙間がないことを確認してください。図 8 参照)
*   [ ] **GPS アンテナの向きは正しいですか？** (セラミック面を必ず空に向けてください。図 6 参照)
*   [ ] **アンテナの接続ポートを間違えていませんか？** (出荷ロットによって位置が異なる場合がありますので、筐体の印字ラベルをご確認ください。図 3 参照)
*   [ ] **MicroSD カードの仕様は合っていますか？** (容量が 32GB 以下で、FAT32 形式でフォーマットされていることを確認してください。図 4 参照)
*   [ ] **ディスプレイのスイッチが UP の位置になっていますか？** (図 9 参照)

---

## 04. ファームウェアのアップグレードと書き込み (アドバンス機能)

公式から新しいファームウェアがリリースされた場合は、側面の USB-C ポートを使用してファームウェアの書き込みを行います。

1.  PC に接続した USB-C ケーブルを用意します。
2.  **重要な手順**：ケーブルをモジュール**側面の USB-C ポート (FLASH ONLY)** に挿入する際、**モジュールの背面/右側にある書き込みボタンを長押し**したままにすることで、チップが Boot 書き込みモードに入ります。

![ファームウェア書き込み手順](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*図 12：書き込みボタンを押しながら USB ケーブルを挿入する手順のイメージ*
