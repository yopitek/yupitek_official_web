---
title: "YPB02 加速度センサー内蔵 BLE ビーコン"
description: "YPB02 加速度センサー内蔵 BLE ビーコン。低消費電力 Bluetooth BLE 5.0 技術、勤怠管理、位置測位、資産追跡に最適、設定可能。"
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof", "Sensor", "Accelerometer"]
---

## 製品概要

**YPB02** は、高性能な **LIS3DH 3軸加速度センサー** を内蔵したモーション検知型の Bluetooth® Low Energy (BLE 5.0) ビーコンです。YPB01 と同様のコンパクトなコイン型デザイン、交換可能な 1000mAh CR2477 コイン電池、および IP67 防水・防塵筐体を採用しつつ、さらにスマートなモーション検知とセンサー情報の送信に対応しています。

このビーコンはトリガーベースの配信をサポートしており、移動、振動、あるいは落下検知などのイベント発生時のみ、リアルタイムの加速度データ送信や配信間隔の切り替えを行います。これによりバッテリー消費を最小限に抑えつつ、高度な資産活動監視を実現します。

---

## 主な特徴

* **3軸加速度センサー搭載:** LIS3DH センサーを搭載し、X・Y・Z 軸の変位、傾き、動きのデータを測定・送信します。
* **トリガーベース配信:** 特定のトリガー条件（例：移動時のみの配信、落下アラート、移動検知時に配信間隔を 100ms に短縮してリアルタイム追跡など）を設定可能です。
* **高保護筐体:** IP67 防水防塵設計で、屋内や軽度の屋外環境に設置可能です。
* **交換式電池:** 回転式ハウジング設計により、コイン電池 (CR2477, 1000mAh) を簡単に交換できます。

---

## モーション検知とテレメトリ

LIS3DH センサーにより、YPB02 は以下をサポートします：
1. **アクティビティトリガー配信:** 通常時は標準的な iBeacon/Eddystone フレームを送信し、動きを検出したときのみセンサーデータフレーム (HT/ACC) を送信します。
2. **静止・移動モードの併用:** 静止時は休止（スリープ）状態を維持し、動きを検知すると 100ms 間隔でリアルタイム位置情報を送信させることができます。
3. **しきい値調整:** アプリを通じて、加速度のしきい値や検知時間をカスタマイズできます。

---

## 設定ガイド

YPB02 のパラメータ（加速度しきい値、トリガー、UUID、Major、Minor など）は、**BeaconSET+** アプリを使用してワイヤレスで設定します：
1. Google Play または Apple App Store から **BeaconSET+** をダウンロードします。
2. スマートフォンの Bluetooth および位置情報サービスを有効にします。
3. アプリを開き、該当するビーコンの MAC アドレスを選択して接続します。
4. パスワードを入力して、しきい値や配信パラメータを変更します。

## 技術仕様

| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Sensor** | LIS3DH 3-axis accelerometer | X, Y, Z axes telemetry |
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
  <img src="/images/products/ibeacon/ypb02.png" alt="Yupitek YPB02" />
{{< /gallery >}}

---

{{< alert >}}
お見積もりやカスタム統合ソリューションが必要ですか？弊社営業チームまで直接メールでお問い合わせください：**sales@yupitek.com**
{{< /alert >}}
