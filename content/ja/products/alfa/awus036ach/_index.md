---
title: "ALFA AWUS036ACH — AC1200 デュアルバンド 高出力 USB-C 無線アダプター"
description: "ALFA AWUS036ACH、Realtek RTL8812AU、AC1200 デュアルバンド、USB-C、5 dBi 外部アンテナ×2、Kali Linux セキュリティ研究のゴールドスタンダード、Monitor Mode・Packet Injection 対応。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "デュアルアンテナ", "Monitor Mode", "Kali Linux", "セキュリティ研究"]
---

{{< alert "warning" >}}
**合法使用に関する声明**：Monitor Mode および Packet Injection 機能は、認可されたセキュリティテスト、教育目的の研究、および合法的なペネトレーションテストのみを目的としています。対象ネットワークの明示的な許可を得た上でご使用ください。
{{< /alert >}}

## 製品概要

AWUS036ACH は ALFA Network の最も象徴的なセキュリティ研究用アダプターであり、2017年以来 Kali Linux ペネトレーションテストのゴールドスタンダードとして広く認知されています。実績豊富な Realtek RTL8812AU チップセットを搭載し、確固たる Monitor Mode および Packet Injection サポート、長距離受信のための内蔵パワーアンプ、2本の取り外し可能な 5 dBi アンテナを備えています。世界初の USB Type-C コネクタを採用した WiFi 5 アダプターです。

> **macOSについて：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 11 Big Sur 以降および Apple Silicon（M1/M2/M3）は**非対応**です。Intel Mac での最大サポートは macOS 10.15 Catalina です。

## 主な特長

- Realtek RTL8812AU — WiFi セキュリティ研究で最も広くテストされたチップセット
- WiFi 5（802.11ac）デュアルバンド AC1200 — 5 GHz で 867 Mbps、2.4 GHz で 300 Mbps
- 内蔵パワーアンプ — 一般的なノートPC内蔵カードの最大 3 倍の通信距離
- 2× RP-SMA メスコネクタ + 2× 5 dBi 取り外し可能デュアルバンドアンテナ（高利得アンテナへ換装可）
- 世界初の WiFi 5 USB-C アダプター
- スクリーンクリップマウント付属
- Kali 2017.1 以降で Packet Injection をサポート
- 802.11a/b/g/n 対応

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | Realtek RTL8812AU |
| Wi-Fi 規格 | IEEE 802.11 a/b/g/n/ac（Wi-Fi 5） |
| 周波数帯域 | 2.4 GHz · 5 GHz（デュアルバンド） |
| 最大データレート | 802.11b: 11 Mbps · 802.11a/g: 54 Mbps · 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| 最大合計速度 | AC1200（867 + 300 Mbps） |
| アンテナコネクタ | 2× RP-SMA メス |
| 付属アンテナ | 2× デュアルバンド 全方向性ダイポール、5 dBi |
| USB インターフェース | Type-C SuperSpeed USB（5 Gbps）；USB 2.0 下位互換 |
| パワーアンプ | あり — 通信距離延長 |
| 無線セキュリティ | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| 付属品 | スクリーンクリップマウント · USB ケーブル |
| 原産国 | 台湾 |

## 対応OS

| OS | 状態 | 備考 |
|----|------|------|
| Windows 10 / 11 | ✅ 対応 | Alfa 公式サイトからドライバーをダウンロード；WPA3 対応（2019年10月以降のドライバー） |
| macOS 10.15 Catalina | ⚠️ 限定対応 | 手動インストールが必要；macOS 11+ および Apple Silicon は非対応 |
| Ubuntu | ✅ 対応 | RTL8812AU DKMS を手動インストール；Ubuntu 24.10+（カーネル ≥ 6.14）以降は標準搭載 |
| Kali Linux | ✅ 優秀 | Kali 2017.1 以降；完全な Monitor Mode + Packet Injection；aircrack-ng ドライバーを推奨 |
| NetHunter（Android） | ✅ 対応 | OTG USB；広く動作確認済み |

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|------------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 対応 | morrownr DKMS スクリプトによる手動ドライバーインストール |
| デスクトップ/ノートPC | ✅ 対応 | USB-C または USB-A（付属ケーブル使用） |
| Mac（Intel） | ⚠️ 限定対応 | 最大 macOS 10.15 Catalina |

## 高度な機能

| 機能 | 状態 |
|------|------|
| Monitor Mode | ✅ 優秀（ゴールドスタンダード — 2017年よりコミュニティで実証済み） |
| Packet Injection | ✅ 優秀 |
| Soft AP モード | ✅ 対応 |
| Bluetooth | ❌ なし |
| VIF | ⚠️ 限定（完全な VIF サポートには AWUS036ACM を推奨） |

## 同梱物

- 1× AWUS036ACH アダプター
- 2× 取り外し可能 5 dBi デュアルバンド ダイポールアンテナ
- 1× USB-C to USB-A ケーブル
- 1× スクリーンクリップマウント

## リソースとリンク

| リソース | リンク |
|---------|--------|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036ach_1 |
| 公式ドキュメント | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| ドライバー（aircrack-ng、Kali 推奨） | https://github.com/aircrack-ng/rtl8812au |
| ドライバー（morrownr、一般 Linux 向け） | https://github.com/morrownr/8812au-20210708 |

## 製品仕様書ダウンロード

| 📄 AWUS036ACH 仕様書（PDF） | [ダウンロード](/docs/alfa/AWUS036ACH_spec.pdf) |
|----------------------------|-----------------------------------------------|

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
