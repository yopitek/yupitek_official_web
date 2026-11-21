---
title: "ALFA Network USB Wi-Fi アダプター 比較表"
description: "ALFA Network の USB Wi-Fi アダプター 9 製品の仕様比較：チップセット、Linux ドライバー、Monitor／Injection／AP 対応状況、ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17）での実測結果を掲載。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

下表は ALFA Network の USB Wi-Fi アダプター 9 製品の仕様一覧です。Monitor、Injection、AP、エンドツーエンド handshake の各列は、Yopitek が ASUS GX10（Ubuntu 24.04 LTS / ARM64 / kernel 6.17）上で、自社の機材と自社オフィスの Wi-Fi を使って測定した実測結果であり、データシートの値を転記したものではありません。

## 仕様の詳細比較

モバイルでは表を横にスクロールしてください。型番をタップすると製品ページへ移動します。

| 型番 | Wi-Fi 世代 | チップセット | 対応バンド | 最大速度 | USB インターフェース | アンテナ | MIMO | モニターモード | パケットインジェクション | エンドツーエンド handshake（GX10 実測） | Linux ドライバー | ドライバー種別 | AP モード | 最大消費電力 | Bluetooth | 主な用途 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/ja/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 対応 | ❌ 標準 6.17 カーネルでは失敗 | ❌ 非対応（インジェクション失敗） | カーネル内蔵 ≥5.18 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.6W | BT 5.2 | Wi-Fi 6E＋Linux＋USB-C |
| [AWUS036AXM](/ja/products/alfa/awus036axm/) | WiFi 6E | MT7921AU | 2.4 + 5 + 6 GHz（6 GHz 未検証） | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 対応 | ❌ 標準 6.17 カーネルでは失敗 | ❌ 非対応（インジェクション失敗） | カーネル内蔵 ≥5.18 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.6W | BT 5.2 | Wi-Fi 6E＋デュアルアンテナ |
| [AWUS036AX](/ja/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.0 | 内蔵 | 2×2 MIMO | ✅ 対応 | ✅ 対応 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥6.17 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.6W | — | Wi-Fi 6＋AP ホットスポット |
| [AWUS036AXER](/ja/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | 内蔵（nano） | 2×2 MIMO | ✅ 対応 | ✅ 対応 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥6.17 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.0W | — | コンパクトな携帯用アダプター |
| [AWUS036ACH](/ja/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ 最適 | ✅✅ 最適 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥6.13 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.6W | — | Kali Linux の定番 |
| [AWUS036ACM](/ja/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 対応 | ✅ 対応 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥4.19 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | 3.0W | — | Linux プラグアンドプレイ |
| [AWUS036ACHM](/ja/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ 対応 | ✅ 2.4 GHz／⚠️ 5 GHz はビーコン送信のみ | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥4.19 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応 | — | — | 小型 AC600、Linux プラグアンドプレイ |
| [AWUS036ACS](/ja/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ 対応 | ✅ 対応 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥6.13 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応（5 GHz は 802.11a 20 MHz で試験、VHT80 は未試験） | 2.5W | — | 低価格セキュリティテスト |
| [AWUS036EACS](/ja/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | 内蔵 2dBi | 1×1 SISO | ✅ 対応 | ✅✅ 最適 | ✅ エンドツーエンド（.22000） | カーネル内蔵 ≥6.2 | カーネル内蔵（プラグアンドプレイ） | ✅ ネイティブ対応（5 GHz は 802.11a 20 MHz で試験、VHT80 は未試験） | 2.5W | BT 4.2 | Windows 家庭用 Wi-Fi＋Bluetooth |

## 用途別クイック購入ガイド

**🔴 Kali Linux / ペネトレーションテスト** — おすすめ: AWUS036ACH

RTL8812AU — Kali 上でのモニターモードとパケットインジェクションの実績が最も豊富。GX10（kernel 6.17）では両バンドでインジェクション成功率 100%。カーネル内蔵の rtw88_8812au ドライバーは 6.13 以降で利用可能。ヒント：古いカーネルでは、安定版 commit 63cf0b4 に固定した aircrack-ng の DKMS ドライバーを使用してください。

**🔵 WiFi 6E（トライバンド）ヘビーユーザー** — おすすめ: AWUS036AXML or AWUS036AXM

MT7921AUN — Linux カーネル内蔵ドライバーは 5.18 以降で利用可能。6 GHz 帯に対応（AXML で確認済み、AXM は未試験）、Bluetooth 5.2。注意：標準 kernel 6.17 ではパケットインジェクションが失敗します（6.16 以降の mac80211 のリグレッション）。そのためペネトレーションテストには適しません。形状の違い：AXML は着脱式 USB-C コネクターで、単一アンテナ筐体に 2 系統の出力を備えます。AXM は L 字型の USB-A 一体型です。

**🌐 Soft-AP / ホットスポットエミュレーション** — おすすめ: AWUS036ACM

MT7612U — Linux カーネル標準の hostapd でプラグアンドプレイの AP モードに対応。独自ビルドの hostapd が必要で不具合の出やすい Realtek 製アダプターと異なり、MediaTek はスムーズで安定しており、Rogue AP / Evil Twin のシミュレーションに適しています。

**🟢 Linux 日常利用（プラグアンドプレイ）** — おすすめ: AWUS036ACM

MT7612U — カーネル 4.19 以降で内蔵。Ubuntu / Debian / Fedora ではドライバーの設定は不要で、最も手間のかからない Linux 環境です。

**🟣 Raspberry Pi / 組み込み** — おすすめ: AWUS036ACM

低消費電力とカーネル内蔵ドライバーの組み合わせは Raspberry Pi に最適です。注意：高出力モデル（ACH、AXML）は最大 3.6W を消費するため、Pi での電圧低下や接続リセットを防ぐにはセルフパワーの USB ハブが必要です。

**🟡 低価格 / セキュリティ入門** — おすすめ: AWUS036ACS

RTL8811AU — モニターモードとパケットインジェクションに対応した手頃な入門モデル。シングルアンテナのコンパクト設計です。

**⚡ コンパクトな携帯用アダプター** — おすすめ: AWUS036AXER

厚さを抑えたナノサイズで重量はわずか 10.5g。WiFi 6（1800 Mbps）、USB-A。出張に適しており、Windows 利用向けです。

**🏠 Windows 家庭向け＋Bluetooth** — おすすめ: AWUS036EACS

RTL8821CU — WiFi 5 と Bluetooth 4.2 のデュアルモード一体型。ナノサイズ。PCIe スロットがなく、手軽に無線と Bluetooth を追加したいデスクトップ PC に適しています。

**🍎 macOS 互換性** — おすすめ: AWUS036ACH or AWUS036AXML

ACH はサードパーティ製ドライバーにより macOS で良好に動作します。AXML の MT7921AUN にはコミュニティ版の macOS 対応があります。必ず macOS バージョンとの互換性をご確認ください。Intel Mac は M シリーズよりも過去のドライバー資産が充実しています。

## プラットフォーム／OS 別クイック購入ガイド

| プラットフォーム／OS | 第一候補 | 第二候補 | 備考 |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = モニターモードで最良、ACM = カーネル対応が最も容易。仮想マシンで使う場合：接続断を防ぐため、VM の USB コントローラーを USB 3.0（xHCI）に設定してください。 |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U はカーネル 4.19 以降、MT7921AUN は 5.18 以降で内蔵 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | 低消費電力でカーネル内蔵ドライバーのため、手動ビルドは不要です。高出力カードにはリセット防止のためセルフパワーの USB ハブを推奨します。 |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | WiFi 6 の性能。EACS は Bluetooth 一体型 |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | サードパーティ製ドライバーがありますが、macOS バージョンをご確認ください。Intel Mac には従来のドライバーがあり、Apple Silicon（M1/M2/M3）は限定的な実験的対応にとどまります。 |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU と RTL8811AU は NetHunter に対応。OTG アダプターとカスタムカーネルのビルドが必要です。 |

---

測定環境：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia（2026-11）。各アダプターの詳細レポートは[ブログ](/ja/blog/)をご覧ください。
