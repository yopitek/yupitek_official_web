---
title: "ALFA AWUS036ACS — AC600 デュアルバンド USB アダプター（入門セキュリティ研究）"
description: "ALFA AWUS036ACS、Realtek RTL8811AU、AC600 デュアルバンド USB 2.0、1× 2 dBi RP-SMA 取り外し可能アンテナ、Monitor Mode とパケットインジェクション対応、入門セキュリティ研究に最適。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "入門"]
---

{{< alert "warning" >}}
**法的免責事項**：Monitor Mode およびパケットインジェクション機能は、授権されたセキュリティテスト、教育研究、および合法的なペネトレーションテストのみを目的としています。使用前に対象ネットワークの所有者から明示的な許可を取得してください。
{{< /alert >}}

## 製品概要

AWUS036ACS は、Monitor Mode とパケットインジェクションをサポートする Alfa デュアルバンド 802.11ac ラインナップの中で最も手頃な入門機です。Realtek RTL8811AU チップセットを搭載し、コンパクトで軽量。取り外し可能な RP-SMA アンテナを備え、高ゲインや指向性アンテナへのアップグレードも可能です。ACH や ACM ほどのパフォーマンスはありませんが、無線セキュリティ研究の初心者や、外部アンテナ対応の手頃な 5 GHz アダプターを必要とするユーザーに最適な選択肢です。

> **macOS に関する注意：** すべての ALFA アダプターは macOS サポートが限定的です。macOS 10.15 Catalina 以降および Apple Silicon（M1/M2/M3）は**非対応**です。AWUS036ACS は macOS 10.14 Mojave（Intel Mac のみ）まで対応しています。

## 主な特長

- Realtek RTL8811AU チップセット — Monitor Mode とパケットインジェクション対応
- WiFi 5（802.11ac）デュアルバンド — 2.4 GHz（150 Mbps）+ 5 GHz（433 Mbps）= AC600
- 1× RP-SMA メスコネクター、1× 2 dBi ミニ取り外し可能アンテナ付き — パネルや高ゲインアンテナへのアップグレード可能
- コンパクトなフォームファクター — 携帯性に優れる
- USB 2.0（USB-A）インターフェース — 任意の USB ポートと互換
- Alfa APA-M25 デュアルバンドパネルアンテナに対応、指向性受信が可能
- Kali Linux on Raspberry Pi（KaliPi）対応 — DKMS によるドライバーインストール

## 技術仕様

| パラメータ | 仕様 |
|---|---|
| チップセット | Realtek RTL8811AU |
| 無線規格 | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| 周波数帯域 | 2.4 GHz（150 Mbps）· 5 GHz（433 Mbps） |
| 最大合計速度 | AC600（150 + 433 Mbps） |
| アンテナコネクター | 1× RP-SMA メス |
| 付属アンテナ | 1× デュアルバンド ダイポール ミニ、2 dBi |
| USB インターフェース | USB 2.0 Type-A |
| 受信感度 | 802.11b：−85 dBm · 802.11g：−69 dBm · 802.11n：−68 dBm · 802.11ac：−59 dBm |
| 無線セキュリティ | WPA2 / WPA / WEP / 802.1X |
| 原産国 | 台湾 |

> ⚠️ **注意：** USB 2.0 のみ対応 — 最大バス速度 480 Mbps。スループットは 433 Mbps に制限されます。最大速度が必要な場合は、USB 3.0 対応の AWUS036ACM または AWUS036ACH をご使用ください。

## 対応 OS

| OS | 状態 | 備考 |
|---|---|---|
| Windows XP–11 | ✅ 対応 | Alfa 公式サイトからドライバーをダウンロード |
| macOS 10.5–10.14 | ⚠️ 限定対応 | macOS 10.15+ および Apple Silicon は非対応 |
| Ubuntu | ✅ 対応 | DKMS ドライバーの手動インストールが必要（morrownr/8821au）。カーネル組み込みサポートなし。 |
| Kali Linux | ✅ 対応 | Monitor Mode + パケットインジェクション対応。morrownr GitHub のコミュニティドライバーを使用。 |
| NetHunter（Android） | ✅ 対応 | OTG USB 接続；RTL8811AU は NetHunter 互換性確認済み |

## 対応ハードウェア

| ハードウェア | 状態 | 備考 |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ 対応 | morrownr DKMS 経由で KaliPi 専用インストール可能 |
| デスクトップ/ノートPC | ✅ 対応 | 標準 USB-A |
| Mac（Intel） | ⚠️ 限定対応 | macOS 10.5–10.14 のみ |

## 高度な機能

| 機能 | 状態 |
|---|---|
| Monitor Mode | ✅ 対応 |
| パケットインジェクション | ✅ 対応 |
| Soft AP モード | ✅ 対応 |
| Bluetooth | ❌ 非対応 |
| VIF | ⚠️ 限定対応 |

## 同梱物

- 1× AWUS036ACS アダプター
- 1× 取り外し可能 2 dBi デュアルバンド ミニ ダイポールアンテナ

## リソースとリンク

| リソース | リンク |
|---|---|
| 公式製品ページ | https://www.alfa.com.tw/products/awus036acs_1 |
| 公式ドキュメント | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux ドライバー（RTL8811AU） | https://github.com/morrownr/8821au-20210708 |

## 製品仕様書ダウンロード

| 📄 AWUS036ACS 仕様書（PDF） | [ダウンロード](/docs/alfa/AWUS036ACS_spec.pdf) |
|---|---|

## ギャラリー

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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


{{< alert "info" >}}
見積もりや購入に関するご相談は[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
