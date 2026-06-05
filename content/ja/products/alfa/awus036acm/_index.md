---
title: "ALFA AWUS036ACM — AC1200 デュアルバンド USB 3.0 アダプター（Linux プラグ＆プレイ最適）"
description: "ALFA AWUS036ACM、MediaTek MT7612U、AC1200 デュアルバンド USB 3.0、Linux カーネル 4.19 からカーネル内蔵ドライバー対応（プラグ＆プレイ、コンパイル不要）。モニターモード、パケットインジェクション、VIF 完全対応。Raspberry Pi 最適の Alfa アダプター。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "デュアルバンド", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**合法使用に関する声明**：Monitor Mode および Packet Injection 機能は、認可されたセキュリティテスト、教育目的の研究、および合法的なペネトレーションテストのみを目的としています。対象ネットワークの明示的な許可を得た上でご使用ください。
{{< /alert >}}

## 製品概要

AWUS036ACM は、Linux ユーザーが設定なしで即座に使えるアダプターとして最初に推奨される製品です。MediaTek MT7612U チップセットは Linux カーネル 4.19 以降からカーネルに内蔵されており、Ubuntu、Kali Linux、Raspberry Pi OS、Arch Linux、そして事実上すべての現代的なディストリビューションで、コードを一行もコンパイルせずにプラグ＆プレイで動作します。物理サイズとアンテナ構成は AWUS036ACH と同一ですが、MediaTek の安定したカーネル内蔵ドライバーを採用しています。モニターモード、パケットインジェクション、VIF（仮想インターフェース）はすべて完全対応しています。

> **macOS に関する注意：** すべての ALFA アダプターは macOS のサポートが限定的です。macOS 11 以降および Apple Silicon（M1/M2/M3）は**非対応**です。AWUS036ACM は macOS 10.12 Sierra が最大対応バージョンです（他のモデルより制限が厳しい）。

## 主な特長

- MediaTek MT7612U チップセット — Linux カーネル 4.19 からカーネル内蔵（プラグ＆プレイ、コンパイル不要）
- WiFi 5（802.11ac）デュアルバンド AC1200 — 5 GHz 最大 867 Mbps、2.4 GHz 最大 300 Mbps
- 2× RP-SMA メスコネクター搭載、2× 5 dBi 着脱式デュアルバンドアンテナ付属 — AWUS036ACH と同一の物理フォーマット
- USB 3.0（USB-A）インターフェース
- モニターモード、パケットインジェクション、AP モード完全対応
- Kali Linux での VIF（仮想インターフェース）対応
- USB 3.0 延長ケーブル付属
- TAA 準拠 — 米国政府調達に適合（GSA 互換）
- Raspberry Pi OS でプラグ＆プレイ — ドライバーインストール不要

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | MediaTek MT7612U |
| WiFi 規格 | IEEE 802.11 a/b/g/n/ac（WiFi 5）|
| 周波数帯域 | 2.4 GHz（2.412–2.472 GHz）· 5 GHz（5.15–5.825 GHz）|
| チャンネル幅 | 20 / 40 / 80 MHz |
| 最大データレート | 5 GHz：最大 867 Mbps · 2.4 GHz：最大 300 Mbps |
| 合計最大速度 | AC1200（867 + 300 Mbps）|
| アンテナコネクター | 2× RP-SMA メス |
| 付属アンテナ | 2× デュアルバンドダイポール、5 dBi ゲイン |
| USB インターフェース | USB 3.0 Type-A（USB 2.0 後方互換）|
| 出力電力 | 802.11a：20 dBm · 802.11b：23 dBm · 802.11g：23 dBm · 802.11n：21 dBm · 802.11ac：20 dBm |
| 受信感度 | 802.11a：−92 dBm · 802.11b：−97 dBm · 802.11g：−90 dBm · 802.11n：−90 dBm |
| 無線セキュリティ | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | あり（電源 + WLAN アクティビティ）|
| アクセサリー | USB 3.0 延長ケーブル |
| 原産国 | 台湾 |

## 対応 OS

| OS | 状態 | 備考 |
|----|------|------|
| Windows XP–11 | ✅ 対応 | Alfa ウェブサイトからドライバーを入手。Windows 10/11 推奨。|
| macOS 10.7–10.12 | ⚠️ 限定対応 | 公式サポートは macOS 10.12 Sierra まで。macOS 11+ および Apple Silicon は非対応。|
| Ubuntu 19.04+ | ✅ プラグ＆プレイ | カーネル内蔵 mt76 ドライバー（カーネル ≥ 4.19）。Ubuntu 20.04 LTS 以降はドライバーインストール不要。|
| Kali Linux 2019.3+ | ✅ プラグ＆プレイ | カーネル内蔵ドライバー。モニターモード確認済み。VIF 対応。5 GHz AP モードは `disable_usb_sg` モジュールパラメーターが必要な場合あり。|
| NetHunter（Android）| ✅ 対応 | OTG USB；カーネル内蔵ドライバーにより RTL アダプターより広い Android 互換性。|

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|------------|------|------|
| Raspberry Pi 3B+/4/5 | ✅ 優秀 | Raspberry Pi OS でプラグ＆プレイ — ドライバーインストール不要。Pi 向け最高の Alfa アダプター。|
| デスクトップ/ノートPC | ✅ 対応 | 標準 USB-A、付属延長ケーブル使用可。|
| Mac（Intel）| ⚠️ 限定対応 | macOS 10.7–10.12 のみ。|

## 高度な機能

| 機能 | 状態 |
|------|------|
| モニターモード | ✅ 対応（カーネル内蔵、現代的なディストリビューションでは追加手順不要）|
| パケットインジェクション | ✅ 対応 |
| Soft AP モード | ✅ 対応（5 GHz AP：最良のパフォーマンスには `disable_usb_sg` モジュールパラメーターを追加）|
| Bluetooth | ❌ 非対応 |
| VIF（仮想インターフェース）| ✅ 対応（Kali での完全 VIF サポート）|

## 同梱物

- 1× AWUS036ACM アダプター
- 2× 着脱式 5 dBi デュアルバンドダイポールアンテナ
- 1× USB 3.0 延長ケーブル
- 1× ドライバー CD（Windows 用）

## リソースとリンク

| リソース | リンク |
|---------|--------|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036acm_1 |
| 公式ドキュメント | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux ドライバー情報（カーネル内蔵）| mt76 ドライバー — Linux カーネル ≥ 4.19 に内蔵、インストール不要 |

## 製品仕様書ダウンロード

| ドキュメント | ダウンロード |
|------------|------------|
| 📄 AWUS036ACM 仕様書（PDF）| [ダウンロード](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
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
