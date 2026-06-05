---
title: "ALFA AWUS036AXM — Wi-Fi 6E トリバンド デュアルアンテナ USB アダプター"
description: "ALFA AWUS036AXM、MediaTek MT7921AUNチップ、Wi-Fi 6Eトリバンド、USB-A Lエルボーコネクタ、2× 5 dBiアンテナ、Bluetooth 5.2、Kali Linux Monitor Modeサポート。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-A", "802.11ax", "トリバンド", "Bluetooth 5.2", "デュアルアンテナ", "Kali Linux"]
---

{{< alert "warning" >}}
**合法使用に関する声明**：Monitor Mode および Packet Injection 機能は、認可されたセキュリティテスト、教育目的の研究、および合法的なペネトレーションテストのみを目的としています。対象ネットワークの明示的な許可を得た上でご使用ください。
{{< /alert >}}

## 製品概要

AWUS036AXM は MediaTek MT7921AUN チップを搭載し、Wi-Fi 6E トリバンド（2.4 GHz / 5 GHz / 6 GHz）対応、最大 3000 Mbps の合計スループットと Bluetooth 5.2（独立 BT アンテナ内蔵）を提供します。L 型 USB-A コネクタにより隣接ポートをふさぎません。2× 5 dBi RP-SMA アンテナ付属。

> **macOSについて：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 11 Big Sur 以降および Apple Silicon（M1/M2/M3）は**非対応**です。Intel Mac での最大サポートは macOS 10.15 Catalina です。

## 主な特長

- Wi-Fi 6E トリバンド：2.4 / 5 / 6 GHz
- MediaTek MT7921AUN チップ
- 最大 3000 Mbps 合計スループット
- Bluetooth 5.2（独立 BT アンテナ + LED インジケータ）
- USB-A L エルボーコネクタ（USB 3.2 Gen 1、5 Gbps）
- 2× RP-SMA female 着脱可能アンテナ（5 dBi）
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode + Packet Injection 対応

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | MediaTek MT7921AUN |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6E）|
| 周波数帯 | 2.4 GHz · 5 GHz · 6 GHz |
| 最大データレート | 3000 Mbps |
| Bluetooth | BT 5.2（独立アンテナ）|
| アンテナ | 2× RP-SMA female、2× 5 dBi デュアルバンドダイポール（着脱可能）|
| USB インターフェース | USB 3.2 Gen 1 Type-A L エルボー（5 Gbps）|
| 無線セキュリティ | WPA3 / WPA2 / WPA / WEP / WPS |

## 対応OS

| OS | 状態 | 備考 |
|----|------|------|
| Windows 10 | ✅ 対応 | 2.4+5 GHz のみ；6 GHz は Windows 11 が必要 |
| Windows 11 | ✅ 対応 | 6 GHz を含む完全トリバンド |
| macOS | ❌ 非対応 | macOS 11+ および Apple Silicon 非対応 |
| Ubuntu | ✅ 対応 | カーネル内蔵 mt7921u、カーネル ≥ 5.18 |
| Kali Linux | ✅ 対応 | Monitor mode + パケットインジェクション；ファームウェアファイルが必要な場合あり |
| NetHunter | ⚠️ 部分対応 | OTG；カーネル依存 |

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|-------------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 対応 | Pi OS更新（カーネル ≥ 5.18）|
| デスクトップ/ノートPC | ✅ 対応 | L エルボー USB-A コネクタで隣接ポートをふさがない |
| Mac Intel | ⚠️ 限定 | macOS 10.15 Catalina 最大 |

## 高度な機能

| 機能 | 状態 |
|------|------|
| Monitor Mode | ✅ あり |
| Packet Injection | ✅ あり |
| Soft AP モード | ✅ あり |
| Bluetooth | ✅ BT 5.2（独立 BT アンテナ）|
| VIF | ✅ あり |

## 同梱物

- 1× AWUS036AXM アダプター
- 2× 5 dBi アンテナ
- クイックセットアップガイド

## リソースとリンク

| リソース | リンク |
|----------|--------|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036axm |
| 公式ドキュメント | https://docs.alfa.com.tw/ |
| Linux ドライバ | mt7921u — Linux カーネル ≥ 5.18 に内蔵 |

## 製品仕様書ダウンロード

| ドキュメント | ダウンロード |
|------|------|
| 公式仕様書（PDF） | [📄 AWUS036AXM 仕様書をダウンロード](/docs/alfa/AWUS036AXM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axm_image_1.png" alt="ALFA AWUS036AXM" />
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
