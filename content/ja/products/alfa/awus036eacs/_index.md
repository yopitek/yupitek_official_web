---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 Nano USB アダプター"
description: "ALFA AWUS036EACS、Realtek RTL8821CU、AC600 デュアルバンド、USB 2.0 Nano フォームファクター、Bluetooth 4.2 搭載。カーネル 6.2 以降は mainline の rtw88_8821cu ドライバーを搭載し、GX10 で両バンドの Monitor mode とインジェクションを確認済み。"
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "ホーム", "Windows"]
---

## 製品概要

AWUS036EACS は、家庭およびオフィスユーザー向けに設計された Alfa の超小型 WiFi + Bluetooth 複合 USB アダプターです。Realtek RTL8821CU チップセットを搭載し、AC600 デュアルバンド WiFi と Bluetooth 4.2 を Nano フォームファクターに統合。Windows では内蔵ドライバーによりプラグアンドプレイで動作します。Soft AP モードによりインターネット共有も可能です。Linux ではカーネル 6.2 以降、mainline の rtw88_8821cu ドライバーが組み込まれています。GX10（Ubuntu 24.04、カーネル 6.17）でのテストでは、Monitor mode とパケットインジェクションが 2.4 GHz・5 GHz の両方で 100% に達し、エンドツーエンドの WPA ハンドシェイク取得に成功、Bluetooth と Wi-Fi も同時に使用できました。

> ⚠️ **注意：** AWUS036EACS は Windows ホームユーザー向けですが、mainline の rtw88_8821cu ドライバー（カーネル 6.2 以降）で Linux でも動作します。RP-SMA ポートなし、アンテナ交換不可。

## 主な特長

- 802.11ac AC600 デュアルバンド WiFi + Bluetooth 4.2 を単一の Nano USB アダプターに統合
- Windows でプラグアンドプレイ — 内蔵ドライバーが自動インストール
- Soft AP モード — アダプターから直接 WiFi ホットスポットを作成可能
- 超コンパクト設計 — USB ポートに挿したまま忘れるほど小さい
- デュアルバンド：2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）
- 内蔵 2 dBi アンテナ — 外部 RP-SMA コネクターなし
- WiFi と Bluetooth の両方が必要なデスクトップ・組み込みシステム・家庭用 PC に最適
- Bluetooth 4.2 でオーディオストリーミング、キーボード、マウスなどの周辺機器に対応

## 技術仕様

| 項目 | 仕様 |
|------|------|
| チップセット | Realtek RTL8821CU |
| WiFi 規格 | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| Bluetooth | BT 4.2（2.4 GHz） |
| 周波数帯域 | WiFi：2.4 GHz / 5 GHz・BT：2.4 GHz |
| 最大データレート | 802.11b：11 Mbps · 802.11g：54 Mbps · 802.11n：150 Mbps · 802.11ac：433 Mbps |
| 最大複合速度 | AC600（150 + 433 Mbps） |
| アンテナ | 内蔵 2 dBi（取外不可、RP-SMA なし） |
| USB インターフェース | USB 2.0 |
| 出力電力 | 典型値 17 dBm |
| 受信感度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 無線セキュリティ | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| 動作温度 | −10°C ～ 60°C |
| フォームファクター | Nano / 低プロファイル |
| 製造国 | 台湾 |

## 対応 OS

| OS | 対応状況 | 備考 |
|----|---------|------|
| Windows XP–10 | ✅ 対応 | 内蔵ドライバー、プラグアンドプレイ。Windows 11 の互換性は Alfa ドライバーページを確認。 |
| macOS | ⚠️ 限定的 | 対応バージョン範囲は未確認。Apple Silicon 非対応。 |
| Ubuntu / Linux | ✅ カーネル 6.2 以降 | mainline の rtw88_8821cu ドライバーが組み込み済みでインストール不要（GX10、Ubuntu 24.04、カーネル 6.17 で実測）。 |
| Kali Linux | ✅ 対応 | GX10（Ubuntu 24.04、カーネル 6.17）で Monitor mode とパケットインジェクションが両バンドで 100%、エンドツーエンドの WPA ハンドシェイク取得に成功。実機の Kali は未検証。 |
| NetHunter (Android) | ❌ 非推奨 | RTL8821CU の NetHunter 対応は未確認。 |

## 対応ハードウェア

| ハードウェア | 対応状況 | 備考 |
|------------|---------|------|
| Raspberry Pi | ⚠️ 未検証 | 未検証；カーネル 6.2 以降は mainline の rtw88_8821cu ドライバーを搭載。 |
| デスクトップ / ノートPC | ✅ 対応 | Windows のみ推奨。 |
| 組み込み / IoT（Windows） | ⚠️ Windows のみ | コンパクト設計が Windows 組み込みシステムに適合。 |

## 高度な機能

| 機能 | 対応状況 |
|------|---------|
| モニターモード | ✅ 対応（GX10 テスト：両バンドで 100%） |
| パケットインジェクション | ✅ 対応（GX10 テスト：両バンドで 100%） |
| Soft AP モード | ✅ 対応 |
| Bluetooth | ✅ BT 4.2（Wi-Fi と同時使用可） |
| VIF | 🟡 部分対応（パッシブ monitor + 同一チャンネルの managed。独立した 2 つの VIF は非対応） |

## 同梱物

- 1× AWUS036EACS Nano アダプター

## リソースとリンク

| リソース | リンク |
|---------|-------|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036eacs_1 |
| 公式ドキュメント | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## 製品仕様書ダウンロード

仕様書は近日公開予定です。

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## 対応アンテナアクセサリ

すべての ALFA USB アダプターは標準 RP-SMA コネクタを採用。以下の外部アンテナで信号範囲とゲインを向上できます：

| アンテナ | 周波数 | ゲイン | タイプ |
|---------|--------|--------|--------|
| [ALFA APA-M04](/ja/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | 室内パネル指向性 |
| [ALFA APA-M25](/ja/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | デュアルバンド室内パネル |
| [ALFA APA-M25-6E](/ja/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | トライバンド室内パネル |
| [ARS 25-57A](/ja/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | 屋外無指向性 |
| [ARS NT5B7](/ja/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | 無指向性 |


{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
