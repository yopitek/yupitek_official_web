---
title: "ALFA AWUS036AX — Wi-Fi 6 デュアルバンド USB アダプター"
description: "ALFA AWUS036AX、Realtek RTL8832BUチップ、Wi-Fi 6（802.11ax）デュアルバンド 2.4+5 GHz、最大 1200 Mbps、USB 3.0。注意：Wi-Fi 6のみ — 6 GHz帯なし。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6", "USB 3.0", "802.11ax", "デュアルバンド", "OFDMA", "MU-MIMO"]
---

## 製品概要

AWUS036AX は Realtek RTL8832BU チップを搭載し、Wi-Fi 6（802.11ax）デュアルバンド（2.4 GHz + 5 GHz）対応、最大 1200 Mbps の合計スループット、MU-MIMO 2×2 と OFDMA 技術をサポートします。アンテナは一体型（着脱不可）です。

> ⚠️ **重要：** このモデルは **Wi-Fi 6** であり、Wi-Fi 6E ではありません — **6 GHz 帯なし**。6 GHz が必要な場合は AWUS036AXML または AWUS036AXM をご検討ください。カーネル < 6.12 では Monitor mode が制限されます。**Linux セキュリティ研究には推奨しません**。

> **macOSについて：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 11 Big Sur 以降および Apple Silicon（M1/M2/M3）は**非対応**です。Intel Mac での最大サポートは macOS 10.15 Catalina です。

## 主な特長

- Wi-Fi 6（802.11ax）デュアルバンド：2.4 GHz + 5 GHz
- Realtek RTL8832BU チップ
- 最大 1200 Mbps
- MU-MIMO 2×2
- OFDMA テクノロジー
- USB 3.0 Type-A
- WPA3/WPA2/WPA/WEP
- ⚠️ 6 GHz 帯なし

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | Realtek RTL8832BU |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n/ac/ax（Wi-Fi 6）|
| 周波数帯 | 2.4 GHz + 5 GHz（6 GHz なし）|
| 最大データレート | 1200 Mbps |
| MIMO | MU-MIMO 2×2 |
| アンテナ | 一体型（着脱不可）|
| USB インターフェース | USB 3.0 Type-A |
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
| Raspberry Pi 4/5 | ⚠️ ドライバ必要 | カーネル < 6.14 の Pi OS では手動インストール必要 |
| デスクトップ/ノートPC | ✅ 対応 | 標準 USB-A |

## 高度な機能

| 機能 | 状態 |
|------|------|
| Monitor Mode | ⚠️ 限定（カーネル ≥ 6.12 推奨）|
| Packet Injection | ⚠️ 限定 |
| Soft AP モード | ✅ あり |
| Bluetooth | ❌ なし |

## 同梱物

- 1× AWUS036AX アダプター

## リソースとリンク

| リソース | リンク |
|----------|--------|
| 公式ドキュメント | https://docs.alfa.com.tw/ |
| Linux ドライバ（RTL8832BU）| https://github.com/morrownr/rtl8852bu-20240418 |

## 製品仕様書ダウンロード

| ドキュメント | ダウンロード |
|------|------|
| 公式仕様書（PDF） | [📄 AWUS036AX 仕様書をダウンロード](/docs/alfa/AWUS036AX_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ax_image_1.png" alt="ALFA AWUS036AX" />
{{< /gallery >}}

---

{{< alert >}}
お見積もりやご相談は[こちら](/ja/contact/)からお気軽にどうぞ。
{{< /alert >}}
