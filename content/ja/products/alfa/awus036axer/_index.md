---
title: "ALFA AWUS036AXER — Wi-Fi 6 超薄型ナノ USB アダプター"
description: "ALFA AWUS036AXER、Realtek RTL8832BUチップ、Wi-Fi 6デュアルバンド、ナノフォームファクタ（~65×24×10mm）。日常接続向け — Kali Linux・セキュリティ研究には非推奨。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "802.11ax", "超薄型", "USB 3.2", "ポータブル", "ナノ"]
---

## 製品概要

AWUS036AXER は Realtek RTL8832BU チップを搭載し、Wi-Fi 6（802.11ax）デュアルバンド（2.4 GHz + 5 GHz）対応、最大 1800 Mbps（2.4 GHz: 573 Mbps + 5 GHz: 1200 Mbps）。超薄型ナノデザイン（約 65 × 24 × 10 mm、約 10g）で携帯性に優れています。

> ⚠️ **注意：** ナノフォームファクタ — **RP-SMA コネクタなし**、アンテナのアップグレード不可。**Kali Linux またはセキュリティ研究には推奨しません**。

> **macOSについて：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 11 Big Sur 以降および Apple Silicon（M1/M2/M3）は**非対応**です。Intel Mac での最大サポートは macOS 10.15 Catalina です。

## 主な特長

- Wi-Fi 6（802.11ax）デュアルバンド：2.4 GHz + 5 GHz
- Realtek RTL8832BU チップ
- 最大 1800 Mbps
- 超薄型ナノデザイン（~65×24×10mm、~10g）
- USB 3.2 Gen 1 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ RP-SMA コネクタなし、アンテナ一体型

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | Realtek RTL8832BU |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6）|
| 周波数帯 | 2.4 GHz + 5 GHz（6 GHz なし）|
| 最大データレート | 1800 Mbps（2.4G: 573 Mbps + 5G: 1200 Mbps）|
| アンテナ | 内蔵ナノ（RP-SMA なし）|
| USB インターフェース | USB 3.2 Gen 1 Type-A |
| サイズ | ~65 × 24 × 10 mm、~10g |
| 無線セキュリティ | WPA3 / WPA2 / WPA / WEP |

## 対応OS

| OS | 状態 | 備考 |
|----|------|------|
| Windows 10/11 | ✅ 対応 | Alfa ウェブサイトからドライバをダウンロード |
| macOS | ❌ 非対応 | macOS 11+ および Apple Silicon 非対応 |
| Ubuntu | ⚠️ ドライバ必要 | カーネル ≥ 6.14（Ubuntu 24.10+）で内蔵；旧バージョンは手動 DKMS |
| Kali Linux | ⚠️ 限定 | カーネル < 6.12 では Monitor mode 制限；ペンテストには非推奨 |
| NetHunter | ⚠️ 限定 | カーネル依存 |

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|-------------|------|------|
| Raspberry Pi 4/5 | ⚠️ ドライバ必要 | カーネル < 6.14 の Pi OS では手動インストール |
| デスクトップ/ノートPC | ✅ 対応 | 標準 USB-A |

## 高度な機能

| 機能 | 状態 |
|------|------|
| Monitor Mode | ⚠️ 限定 |
| Packet Injection | ⚠️ 限定 |
| Soft AP モード | ✅ あり |
| Bluetooth | ❌ なし |

## 同梱物

- 1× AWUS036AXER ナノアダプター

## リソースとリンク

| リソース | リンク |
|----------|--------|
| 公式ドキュメント | https://docs.alfa.com.tw/ |
| Linux ドライバ（RTL8832BU）| https://github.com/morrownr/rtl8852bu-20240418 |

## 製品仕様書ダウンロード

| ドキュメント | ダウンロード |
|------|------|
| 公式仕様書（PDF） | [📄 AWUS036AXER 仕様書をダウンロード](/docs/alfa/AWUS036AXER_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axer_image_1.png" alt="ALFA AWUS036AXER" />
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
お見積もりやご相談は[こちら](/ja/contact/)からお気軽にどうぞ。
{{< /alert >}}
