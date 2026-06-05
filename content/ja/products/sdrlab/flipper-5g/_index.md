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

- **デュアルバンドカバレッジ** — 2.4 GHz + 5 GHz（IEEE 802.11 a/b/g/n）；旧来の 2.4 GHz 専用アドオンでは届かなかった現代の 5 GHz ネットワークにアクセス可能
- **Realtek RTL8720DN（AI Thinker BW16 モジュール）** — FCC/CE 認証取得済みモジュール採用、業界標準のデュアルバンド SoC
- **デュアルコア CPU** — ARM Cortex-M4 @ 200 MHz がアクティブなプロトコル処理を担当；Cortex-M0 @ 20 MHz が省電力バックグラウンドタスクを実行
- **Marauder 5G ファームウェアプリインストール** — スキャン、Deauth、ビーコンフラッド、スニッフィング（EAPOL/PMKID）、Evil Portal モードを搭載；プラグアンドプレイ
- **BLE 5.0** — Wi-Fi 研究と並行して BLE 5.0 デバイスの列挙とビーコン解析が可能
- **GPIO 給電** — Flipper Zero の GPIO ヘッダーから直接 5 V を取得；外部電源不要
- **アンテナ拡張パス** — 対応リビジョンは IPEX（U.FL）コネクター装備、高ゲイン外部アンテナ取り付け可能
- **ファームウェアエコシステム対応** — Momentum および Unleashed カスタムファームウェアフレームワークと互換
- **PlatformIO 開発対応** — Arduino 互換の Ameba D フレームワークによるカスタムファームウェア開発をフルサポート
- **堅牢な動作範囲** — −40°C 〜 85°C、あらゆる気候環境のフィールド使用に対応

## 仕様

| 仕様項目 | 値／説明 |
|---------|---------|
| メインチップ | Realtek RTL8720DN（AI Thinker BW16 モジュール） |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n（2.4 GHz + 5 GHz デュアルバンド） |
| Wi-Fi 送信電力 | ~17 dBm（地域規制による） |
| Bluetooth | BLE 5.0 |
| フラッシュ | 4 MB |
| 電源 | Flipper Zero GPIO（5 V） |
| 典型的な電流消費 | 150–250 mA（アクティブスキャン時） |
| 接続インターフェース | Flipper Zero 標準 GPIO ピンヘッダー（2×8 ピン） |
| プリロードファームウェア | Marauder 5G（スキャン、Deauth、Beacon、スニッフィング、Evil Portal） |
| ファームウェア互換 | Momentum、Unleashed |
| 二次開発 | PlatformIO（Ameba D / RTL8720DN フレームワーク） |
| 動作温度 | −40°C 〜 85°C |
| アンテナインターフェース | IPEX（U.FL）または基板アンテナ（バージョンにより異なる） |
| フォームファクター | Flipper Zero GPIO 拡張ボード |

## 用途

- **デュアルバンド Wi-Fi スキャン** — 2.4 GHz と 5 GHz のネットワークを受動的に列挙；SSID、BSSID、チャネル、RSSI、暗号化タイプおよび接続クライアントを取得
- **Wi-Fi Deauth セキュリティ研究** — 802.11 Deauth フレームを送信してネットワーク耐障害性をテスト、および認可ネットワーク上の 802.11w/PMF（保護管理フレーム）の有効性を評価
- **WPA ハンドシェイクキャプチャ** — 認可ネットワークのセキュリティ監査のため EAPOL/PMKID ハンドシェイクをスニッフィング
- **Evil Portal 開発** — 認可環境でのフィッシング意識テスト用に不正 AP キャプティブポータルをプロトタイピング
- **ビーコンフラッドテスト** — カスタム SSID をブロードキャストして RF 輻輳の影響とクライアント挙動を調査
- **BLE デバイス列挙** — Wi-Fi 研究と並行して近くの BLE 5.0 周辺機器をスキャンして特定
- **メッシュネットワークトポロジーマッピング** — メッシュ AP の関係、バックホールチャネル、隠し SSID 構成を特定
- **IoT 無線プロトコル研究** — 管理された実験室環境で両 Wi-Fi バンドにおける IoT デバイスの挙動を分析
- **認可された侵入テスト教育** — 認可環境での Wi-Fi セキュリティ基礎の実践的学習プラットフォーム

---

{{< alert "warning" >}}
**このボードを初めてお使いですか？** 前提条件、ファームウェアのセットアップ、初めての 5G スキャン、すべての主要機能をカバーしたステップバイステップの初心者ガイドをご覧ください。
[📖 オンラインユーザーマニュアルを開く](/ja/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
