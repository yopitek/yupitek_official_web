---
title: "YPB01 BLE 5.0 ビーコン"
description: "YPB01 BLE 5.0 ビーコン。低消費電力 Bluetooth BLE 5.0 技術、勤怠管理、位置測位、資産追跡に最適、設定可能。"
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof"]
---

## 製品概要

**YPB01** は、屋内位置測位、活動監視、および資産追跡用に設計された、コンパクトで頑丈な Bluetooth® Low Energy (BLE 5.0) コイン型ビーコンです。超低消費電力の nRF52 シリーズ チップセットをベースに、iBeacon および Eddystone (UID、URL、TLM) フレームを同時にブロードキャストします。

回転開閉式の筐体構造により、コイン型電池の交換が容易でありながら、IP67 の防水・防塵性能を達成。湿気の多い環境や過酷な環境への設置に最適です。

---

## 主な特徴

* **高保護筐体:** IP67 防水防塵仕様で、屋内および一時的な屋外設置に対応。
* **交換式電池:** 回転式開閉機構により、長寿命の CR2477 電池 (1000mAh) を簡単に交換可能。
* **同時配信:** iBeacon と Eddystone 双方のプロトコルをカバーする、最大 6 個の独立した広告スロットの同時配信に対応。
* **電源ボタン:** 輸送や保管時のバッテリー消耗を防ぐため、内部に電源オン/オフ用の物理ボタンを搭載。

---

## 操作ガイド

### ビーコンの電源を入れる方法
1. 回転式の筐体を時計回りに回して開きます。
2. 内部の「プッシュボタン」を **3秒間** 長押しします。
3. 青色の LED インジケーターが **5秒間** 点灯した後に消灯します。これで YPB01 が起動し、配信が開始されます。

### ビーコンの電源を切る方法
1. 内部のプッシュボタンを **3秒間** 長押しします。
2. 青色の LED インジケーターが **5秒間** 点滅した後に消灯します。これでビーコンの電源が切れます。

---

## 設定ガイド

YPB01 のパラメータ（UUID、Major、Minor、送信出力、およびアドバタイジング間隔）は、**BeaconSET** アプリケーションを使用してワイヤレスで設定します：
1. Google Play または Apple App Store から **BeaconSET** をダウンロードします。
2. スマートフォンの Bluetooth および位置情報サービスが有効になっていることを確認します。
3. アプリを開き、ビーコンの MAC アドレスをスキャンして接続します。
4. デフォルトのセキュリティパスワードを入力してロックを解除し、パラメータを編集します。

## 技術仕様

| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## 製品ギャラリー

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb01.png" alt="Yupitek YPB01" />
{{< /gallery >}}

---

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
