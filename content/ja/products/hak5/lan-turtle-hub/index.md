---
title: "LAN Turtle Hub"
date: 2026-11-12
draft: false
featureimage: "/images/products/hak5/lan-turtle-hub.jpg"
showBreadcrumbs: true
brands: ["hak5"]
tags: ["Network Audit", "USB-C Ethernet", "Penetration Testing", "WiFi"]
description: "3ポートUSB 3ハブを内蔵したUSB-C Ethernetアダプター。帯域外WiFi、USBインターセプト、DuckyScriptペイロードに対応しています。"
---

{{< alert "warning" >}}
**法的使用に関する免責事項**: LAN Turtle Hubは専門的なセキュリティ研究ツールです。許可されたセキュリティテストおよび研究目的でのみ使用してください。有効な書面による許可を得たセキュリティ専門家のみを対象としています。
{{< /alert >}}

Hak5 LAN Turtle Hubは、3ポートUSB 3ハブを内蔵したUSB-C Ethernetアダプターです。帯域外WiFi、USBインターセプト用の切り替え可能なUSBポート、DuckyScriptペイロード、ブラウザベースのWebインターフェースを備え、認可されたネットワーク評価に使用できます。

## 製品特長

![LAN Turtle Hub](/images/products/hak5/lan-turtle-hub.jpg)

- **日常的な外観**：USB-C Ethernetアダプターと3ポートUSB 3ハブとして動作
- **リモートアクセス**：WireGuard、OpenVPN、SSHトンネル、Cloud C²で接続
- **帯域外WiFi**：WPA保護の管理用APまたは近隣ネットワークへのクライアント接続による独立した管理チャネル
- **USBインターセプト**：切り替え可能なUSB-Aポートが、ターゲットへのパススルーと内部Linuxへの接続を切り替え
- **DuckyScriptペイロード**：root権限でBashとDuckyScriptを利用、Webインターフェースまたは Payload Studioで開発・テスト
- **Webインターフェース**：ブラウザからペイロード展開、VPN設定、SSHトンネル管理、収集データの閲覧

## 主な仕様

| 仕様項目 | 内容 |
|---|---|
| USB-C Ethernet | ターゲットネットワークへのブリッジ接続を提供するUSB Ethernetアダプター |
| Ethernetポート | RJ45、標準Cat5e/6ケーブル |
| USBハブ | USB-A 3.1ポート × 3、最大5 Gbps（ハブポート2、切り替えポート1） |
| ワイヤレス | 帯域外WiFi：WPA保護の管理用APまたはクライアントモード |
| 電源 | USB-Cケーブル経由 |
| ステータスLED | RGB、スクリプトで制御または無効化可能 |
| 既定の管理方法 | Web UI http://172.16.84.1:1471、SSHは172.16.84.1 |
| リモートアクセス | WireGuard、OpenVPN、SSHトンネル、Cloud C² |
| ターゲット接続 | USB-C（旧型ホストにはUSB-C → USB-Aアダプター） |

## 適用シナリオ

- 企業ITネットワークからホームラボまでの認可されたリモートアクセスと持続性のテスト
- ホストとネットワーク間の中間者攻撃・トラフィック評価
- 切り替え可能なUSBポートによるUSBメモリのインターセプトとファイル処理テスト
- 信頼できないネットワーク上でノートPCの通信を暗号化トンネル経由にするハードウェアVPN

## 公式ドキュメント

| リソース | リンク |
|---|---|
| 📖 公式ドキュメント | [オンラインで見る](https://documentation.hak5.org/lan-turtle-hub/getting-started/lan-turtle-hub-basics) |
| 🛒 Hak5 ショップ製品ページ | [製品を見る](https://shop.hak5.org/products/lan-turtle-hub) |

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
