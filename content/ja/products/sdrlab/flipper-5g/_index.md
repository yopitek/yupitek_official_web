---
title: "SDRLab Flipper Zero 5G 拡張ボード — デュアルバンド Wi-Fi セキュリティ研究モジュール"
description: "Flipper Zero 5G 拡張ボード、RTL8720DN デュアルバンド（2.4+5GHz）Wi-Fi、BLE 5.0、Deauth ファームウェアプリインストール、GPIO 給電、Momentum/Unleashed 互換。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 拡張", "5GHz", "Wi-Fi", "Deauth", "セキュリティ研究"]
---

{{< alert "warning" >}}
**合法利用に関する声明**：この拡張ボードは、授権されたセキュリティ研究および合法的な調査目的のみに使用してください。現地の無線周波数利用に関する法規制を必ず確認してください。
{{< /alert >}}

## 製品特長

![SDRLab Flipper Zero 5G 拡張ボード](/images/products/sdrlab/flipper-5g.png)

- AI Thinker BW16 モジュール（RTL8720DN チップ）ベース、5 GHz Wi-Fi をネイティブサポート
- デュアルバンド対応（2.4 GHz + 5 GHz）、現代のデュアルバンド無線ネットワーク環境を探索可能
- 5G Wi-Fi デオーセンティケーション（Deauth）ファームウェアをプリインストール、プラグアンドプレイ
- Flipper Zero の GPIO から直接給電、追加電源不要
- メッシュネットワークトポロジーの識別と無線環境スキャンに対応
- Momentum および Unleashed ファームウェアフレームワークと互換
- PlatformIO による二次開発とカスタムファームウェアの書き込みに対応
- Cortex-M0 低消費電力コアにより、フィールド作業時間を延長

## 仕様

| 仕様項目 | 値／説明 |
|---------|---------|
| メインチップ | Realtek RTL8720DN（AI Thinker BW16 モジュール） |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n（2.4 GHz + 5 GHz デュアルバンド） |
| Bluetooth | BLE 5.0 |
| フラッシュ | 4 MB |
| 電源 | Flipper Zero GPIO（5 V） |
| 接続インターフェース | Flipper Zero 標準 GPIO ピンヘッダー |
| プリロードファームウェア | 5G Wi-Fi Deauth Firmware |
| ファームウェア互換 | Momentum、Unleashed |
| 二次開発 | PlatformIO 対応 |
| 動作温度 | −40°C 〜 85°C |
| アンテナインターフェース | IPEX（U.FL）または基板アンテナ（バージョンにより異なる） |

## 用途

- 5 GHz Wi-Fi バンドスキャンと環境分析
- 無線ネットワークデオーセンティケーション（Deauth）セキュリティ研究
- 悪意のあるアクセスポイント（Evil Portal）プロトタイプ開発
- ビーコンフラッド（Beacon Flood）テスト
- メッシュネットワークトポロジーの識別
- IoT 無線プロトコルの開発とデバッグ
- 認可された環境における Wi-Fi ペネトレーションテスト教育

---

{{< alert >}}
お見積もりのお問い合わせは[こちら](/ja/contact/)
{{< /alert >}}
