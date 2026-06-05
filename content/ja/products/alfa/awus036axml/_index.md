---
title: "ALFA AWUS036AXML — Wi-Fi 6E USB-C トリバンド無線アダプター"
description: "ALFA AWUS036AXML、MediaTek MT7921AUNチップ、Wi-Fi 6Eトリバンド（2.4/5/6 GHz）、USB-Cインターフェース、Bluetooth 5.2、Kali Linux Monitor Modeサポート。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "トリバンド", "Bluetooth 5.2", "6GHz", "Kali Linux"]
---

{{< alert "warning" >}}
**合法使用に関する声明**：Monitor Mode および Packet Injection 機能は、認可されたセキュリティテスト、教育目的の研究、および合法的なペネトレーションテストのみを目的としています。対象ネットワークの明示的な許可を得た上でご使用ください。
{{< /alert >}}

## 製品概要

AWUS036AXML は MediaTek MT7921AUN チップを搭載し、Wi-Fi 6E トリバンド（2.4 GHz / 5 GHz / 6 GHz）に対応、最大合計スループット 3000 Mbps と Bluetooth 5.2 を内蔵しています。USB-C インターフェースには 2-in-1 USB-C/USB-A ケーブルとスクリーンクリップマウントが付属します。

> **macOSについて：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 11 Big Sur 以降および Apple Silicon（M1/M2/M3）は**非対応**です。Intel Mac での最大サポートは macOS 10.15 Catalina です。

## 主な特長

- Wi-Fi 6E トリバンド：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN チップ
- 最大 3000 Mbps 合計スループット
- Bluetooth 5.2（コンボチップ）
- USB-C インターフェース（USB 3.2 Gen 1、5 Gbps）
- 2-in-1 USB-C/USB-A ケーブル付属
- 1× RP-SMA 着脱可能アンテナ
- スクリーンクリップマウント付属
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode（カーネル ≥ 5.18）

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | MediaTek MT7921AUN |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 周波数帯 | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| 最大データレート | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · 合計: 3000 Mbps |
| Bluetooth | BT 5.2（コンボチップ）|
| アンテナコネクタ | 1× RP-SMA female（着脱可能）|
| USB インターフェース | USB 3.2 Gen 1 Type-C（5 Gbps）|
| ケーブル | 2-in-1 USB-C/USB-A |
| 無線セキュリティ | WPA3 / WPA2 / WPA / WEP / WPS |
| 原産国 | 台湾 |

## 対応OS

| OS | 状態 | 備考 |
|----|------|------|
| Windows 10 | ✅ 対応 | 2.4 GHz と 5 GHz のみ；6 GHz は Windows 10 非対応 |
| Windows 11 | ✅ 対応 | 6 GHz を含む完全トリバンド |
| macOS | ❌ 非対応 | macOS 11+ および Apple Silicon 非対応 |
| Ubuntu | ✅ 対応 | カーネル内蔵 mt7921u、カーネル ≥ 5.18（Ubuntu 22.10+）|
| Kali Linux | ✅ 対応 | Monitor mode ≥ カーネル 5.18；アクティブ monitor mode ≥ 6.12；パケットインジェクション対応 |
| NetHunter（Android）| ⚠️ 部分対応 | OTG；カーネル依存 |

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|-------------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 対応 | Pi OS更新（カーネル ≥ 5.18）；ファームウェアファイルのコピーが必要な場合あり |
| デスクトップ/ノートPC | ✅ 対応 | USB-Cまたは付属の2-in-1ケーブルでUSB-A |
| Mac Intel | ⚠️ 限定 | macOS 10.15 Catalina 最大 |

## 高度な機能

| 機能 | 状態 |
|------|------|
| Monitor Mode | ✅ あり（カーネル ≥ 5.18；アクティブモード ≥ 6.12）|
| Packet Injection | ✅ あり |
| Soft AP モード | ✅ あり |
| Bluetooth | ✅ BT 5.2 |
| VIF | ✅ あり |

## 同梱物

- 1× AWUS036AXML アダプター
- 1× 着脱可能ダイポールアンテナ
- 1× 2-in-1 USB-C/USB-A ケーブル
- 1× スクリーンクリップマウント

## リソースとリンク

| リソース | リンク |
|----------|--------|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036axml |
| 公式ドキュメント | https://docs.alfa.com.tw/ |
| Linux ドライバ（カーネル内蔵）| mt7921u — Linux カーネル ≥ 5.18 に内蔵 |

## 製品仕様書ダウンロード

| ドキュメント | ダウンロード |
|------|------|
| 公式仕様書（PDF） | [📄 AWUS036AXML 仕様書をダウンロード](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
{{< /gallery >}}

---

## 対応アンテナアクセサリ

すべての ALFA USB アダプターは標準 RP-SMA コネクタを採用。以下の外部アンテナで信号範囲とゲインを向上できます：

| アンテナ | 周波数 | ゲイン | タイプ |
|---------|--------|--------|--------|
| [ALFA APA-M04](/ja/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室内パネル指向性 |
| [ALFA APA-M25](/ja/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | デュアルバンド室内パネル |
| [ALFA APA-M25-6E](/ja/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | トライバンド室内パネル |
| [ARS 25-57A](/ja/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | 屋外無指向性 |
| [ARS NT5B7](/ja/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | 無指向性 |


{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
