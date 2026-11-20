---
title: "2026年最も網羅的な実測：ASUS GX10（ARM64 / Ubuntu 24.04）における ALFA 無線 LAN アダプタ 9 製品の Monitor・Injection・AP 全マトリクス"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
bannerimage: "/images/blog/banner/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "ALFA の Wi-Fi USB アダプタ 9 製品について、Ubuntu 24.04 ARM64（GX10）上での Monitor、Injection、AP、WPA3-SAE の実測結果を掲載。Kali 系ツールとの互換性と選定ガイド付き。AWUS036ACH / EACS は injection 成功率 100%。"
faq:
  - question: "AWUS036AXM は Ubuntu で injection できますか？"
    answer: "本プラットフォームではできません。実測では、AWUS036AXM と AWUS036AXML（どちらも MT7921 チップ）は、2.4GHz と 5GHz のどちらでも injection に失敗しました。主因は stock kernel 6.16+ の mac80211 chanctx のリグレッションであり（チップ固有の問題ではありません）、本プラットフォームでは injection や handshake キャプチャが必要な用途にはおすすめしません。"
  - question: "Ubuntu で injection 成功率が最も高い ALFA アダプタはどれですか？"
    answer: "実測では、AWUS036ACH と AWUS036EACS が 2.4GHz と 5GHz の両方で injection 成功率 100% に達しました。今回の 9 製品のうち、最も成績の良い 2 製品です。"
  - question: "9 製品の ALFA アダプタは、Ubuntu 24.04 で別途ドライバをインストールする必要がありますか？"
    answer: "必要ありません。9 製品は kernel 6.17 ですべて kernel 内蔵（in-kernel）ドライバ（rtw88 / rtw89 / mt76 ファミリー）で動作し、挿すだけで認識されます。DKMS モジュールのビルドも不要です。"
  - question: "ALFA アダプタを使って Ubuntu で WPA3-SAE のホットスポットを立てられますか？"
    answer: "できます。9 製品すべてで WPA3-SAE ホットスポットの構築と端末の接続に成功しました（ACS は 5 GHz、それ以外は 2.4 GHz で実測。AXML は 6 GHz でも実測）。ただし AWUS036ACHM だけは、hostapd の sae_pwe を 0 に設定する必要があります。そうしないと、旧型の iPhone 7 Plus が接続に失敗します。"
  - question: "この Ubuntu でのテスト結果は、Kali Linux のユーザーも参考にできますか？"
    answer: "Kali Linux は Debian/Ubuntu 系で、同じ rtw88 / rtw89 / mt76 の in-kernel ドライバを使用します。そのため、本記事のドライバ互換性と能力マトリクスは、原則として Kali ユーザーの参考になります。ただし、本記事の実測プラットフォームは Ubuntu 24.04 であり、Kali では正式な再テストをまだ行っていません。結果は今後の再テストを基準にしてください。"
draft: false
---

## 要点まとめ（TL;DR）

Yopitek（ALFA Network 台湾代理店）が ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）で ALFA の USB 無線 LAN アダプタ 9 製品を実測した結果、9 製品すべてが monitor モードと AP に対応し、AWUS036ACH と AWUS036EACS は両バンドでインジェクション 100% に達し、MT7921 搭載の AWUS036AXM / AWUS036AXML は本プラットフォームでインジェクションに失敗しました。

- **Monitor は全製品で利用可能**：9 製品すべてが monitor mode に入れます。差は受信感度の強弱のみです。
- **Injection が分かれ目**：Realtek `rtw88` の ACH と EACS は両バンドで injection 成功率 100%、ACS がそれに続きます。MT7921 の AXM / AXML は本プラットフォームでは injection に失敗しました。
- **エンドツーエンドの handshake（キャプチャ → `.22000` への変換）を実証できたのは 9 製品中 7 製品**：ACM、ACHM、ACH、ACS、EACS、AX、AXER。
- **AP と WPA3-SAE はほぼ全製品が合格**：AWUS036ACHM のみ、旧型 iPhone との互換性のために `sae_pwe=0` の設定が必要です。
- **ARM64 でもビルド不要**：9 製品すべてが kernel 6.17 の内蔵ドライバで動作し、挿すだけで使えます。DKMS も不要です。

Yopitek は ALFA Network の台湾代理店です。お客様が USB 無線 LAN アダプタを選ぶ際、ほぼ必ず出てくる質問は次の 3 つです。「このアダプタは私の Linux 環境で monitor mode に入れますか？ injection はできますか？ AP は立てられますか？」。スペック表だけで答えるのではなく、現行の ALFA アダプタ 9 製品を自社の検証デスクに持ち込み、**ASUS GX10（ARM64）** と **Ubuntu 24.04 LTS** の環境で 1 枚ずつ実測しました。Monitor、Injection、AP、WPA3-SAE の 4 つの能力を一度に比較し、「このプラットフォームでできないこと」も正直に記載しています。

まず位置づけを明確にしておきます。本記事のすべてのテストは、Yopitek 自社の機器と自社オフィスの Wi-Fi 上で、自社のテスト用スマートフォンを対象に実施しました。これは代理店による製品の互換性と能力の限界に関するハードウェア検証であり、第三者のネットワークに対する攻撃手法の解説ではありません。外部ネットワークに対する操作手順は一切掲載しません。injection や handshake に関する能力は、すべて自社の閉じた環境で、自社の機器に対してのみ測定しています。

本記事は総括表型のハブ記事です。各アダプタの詳細な設定手順と完全な検証結果は、アダプタごとの詳細記事に分けて公開します（記事末尾の関連記事をご覧ください）。

## テストプラットフォームと方法

- **計算プラットフォーム**：ASUS GX10（ARM64 / aarch64）
- **OS**：Ubuntu 24.04 LTS
- **カーネルバージョン**：kernel 6.17.0-1014-nvidia
- **ドライバ方針**：9 製品すべてで kernel 内蔵（in-kernel）ドライバを使用。挿すだけで認識され、サードパーティ製の DKMS モジュールは一切インストールしていません
- **テスト端末**：Apple iPhone 7 Plus（WPA3-SAE の互換性は iPhone 15 Pro でも再テスト）
- **テスト環境**：自社オフィスの Wi-Fi、SSID `YUPITEK`、2.4GHz ch5 / 5GHz ch36、ch157
- **テスト期間**：2026-11-16 から 2026-11-18 まで実機で測定

方法としては、全アダプタに同一の手順を実施しました。まずドライバのロードとインターフェース生成（`wlx*`）を確認し、次に 2.4GHz / 5GHz の monitor、injection、AP、WPA3-SAE 接続を順に検証し、最後に自社のテスト用スマートフォンに対するエンドツーエンドの handshake キャプチャ経路を受け入れ検証しました。各項目の結果は、実際に測定した数値または状態を記録したもので、スペックシートからの推測ではありません。

本記事の表では次の凡例を使用します。

> ✅ 合格 ｜ 🟡 一部対応、または単体でのみ成立 ｜ ⚠️ 制限あり ｜ ❌ 非対応またはテスト失敗 ｜ N/A ドライバがこのモードを持たない ｜ ⬜ 未テスト（2 台目の機器がないため）

## 一、ハードウェアとドライバの対応表

まず、9 製品のハードウェア構成と、kernel 6.17 で実際に読み込まれるドライバを見ていきます。

| # | 型番 | チップ | USB ID | ドライバ（in-kernel） | ファームウェア | 世代 / ストリーム | 備考 |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | morrownr 推奨の Kali 向けアダプタ |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R（AC600） | 単一アンテナ |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R（AC1200） | デュアルアンテナ高ゲイン |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | 軽量・携帯向け |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi コンボ |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | 同一チップ、内蔵アンテナ（Nano） |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

ポイントをいくつか挙げます。

**2 つのドライバ系統。** 9 製品は、MediaTek（`mt76x2u` / `mt76x0u` / `mt7921u`）と Realtek（`rtw88_*` / `rtw89_8852bu`）の 2 系統の in-kernel ドライバに分かれます。チップ世代は Wi-Fi 5 が 6 製品、Wi-Fi 6 が 3 製品です（AX と AXER は `rtw89_8852bu`、AXM と AXML は `mt7921u`）。

**ARM64 での最大の実利は「ビルド不要」であること。** この 9 製品は kernel 6.17 ですべて in-kernel ドライバで動作し、挿すだけで認識されるため、aarch64 上で out-of-tree の DKMS モジュールを扱う必要がありません。これは ARM64 では特に効果があります。サードパーティ製の Realtek ドライバの多くは aarch64 向けのビルド済みパッケージがなく、ソースからのビルドとカーネルバージョンの調整が必要になり、つまずく可能性が高いためです。今回のアダプタ群は、この工程が丸ごと不要です。

**同一チップで型番が異なる製品。** AWUS036AX と AWUS036AXER は同じ RTL8832BU チップ、同じ `rtw89_8852bu` ドライバです。違いはアンテナ設計で（AXER は内蔵アンテナの Nano 設計で RP-SMA なし）、これは後述の受信感度と injection の数値に表れます。

**2 製品は BT + WiFi のコンボデバイス。** AWUS036EACS（RTL8821CU）と AWUS036AXML（MT7921AUN）は Bluetooth を同時に搭載しています。この特性は、抜き挿しの際に実務上の副作用があります。後述の「プラットフォームの注意事項」で説明します。

## 二、コア能力マトリクス：Monitor / Injection / AP / WPA3

本記事のメインとなる表であり、選定時に最初に確認すべき表です。

| # | 型番 | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ ブロードキャストのみ | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅（802.11a・20 MHz で実測、VHT80 は未測定） | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅（802.11a・20 MHz で実測、VHT80 は未測定） | ✅ 2.4G |
| 6 | AWUS036AX | ✅ 強 | ✅ 強 | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ 強 | ✅ 強 | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ 弱 | ✅ 弱 | ❌ **失敗** | ❌ **失敗** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ 弱 | ✅ 弱 | ❌ **失敗** | ❌ **失敗** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* AWUS036ACHM の WPA3 には `sae_pwe=0` の設定が必要です。`sae_pwe=2` では iPhone 7 Plus が接続できませんでした。
>
> WPA3-SAE 列：表示したバンドが実際に実測したバンドです（ACS のみ 5G、それ以外は 2.4G。AXML は 6G でも実測）。その他のバンドは未実測です。

項目ごとの読み方は次のとおりです。

**Monitor：9 製品すべてで利用可能。差は受信感度の強弱。** 2.4GHz と 5GHz のどちらでも、9 製品すべてが monitor mode に入れ、例外はありません。違いはスキャンの積極性と受信感度です。Wi-Fi 6 の AX / AXER は受信が最も強く、スキャンも最も積極的です。MT7921 の AXM / AXML は monitor に入れますが、相対的に弱めです。受動的なキャプチャや周波数帯の棚卸しが目的なら、9 製品すべてが使えます。

**Injection：ここから差が開きます。** Realtek `rtw88` 系が最も良好です。ACH と EACS は 2.4GHz / 5GHz の両方で **100%** に達し、ACS も 2.4GHz 100% / 5GHz 96% です。MediaTek `mt76` の ACM は使えるものの、数値は中程度です（2.4GHz 63–83%、5GHz 76%）。ACHM は 5GHz ではブロードキャストのみで、特定のターゲットへの injection はできません。`rtw89` の AX / AXER は injection 可能ですが、AXER の 2.4GHz 成功率（73%）は AX（96%）より一段低くなっています。

**最も重要な正直な制限：MT7921（AXM / AXML）の injection は本プラットフォームで失敗しました。** これはパラメータ調整の問題ではなく、チップが本質的に injection できないわけでもありません。主因は kernel 6.16+ の mac80211 chanctx のリグレッションです。コミュニティでは、同型番に git／パッチ適用済みドライバを使うと動作するものの、ファームウェアがレートをロックします（morrownr/USB-WiFi #387、morrownr/mt76 #18 に対応）。本プラットフォームでは injection が失敗するため、この 2 製品は deauth を送れず、handshake キャプチャの経路を完走できません。injection が必要な用途では、本プラットフォームではこの 2 製品を選択肢から外してください。

**AP と WPA3：ほぼ全製品が合格。** 9 製品すべてが AP として動作し、多くは 5GHz の VHT80（80MHz）に対応します。WPA3-SAE 接続も、実測したバンドでは全製品で成立しました（表の下の注記を参照）。注意が必要なのは AWUS036ACHM だけで、WPA3 では hostapd の `sae_pwe` を 0 に設定しないと、旧型の iPhone 7 Plus が接続できません（iPhone 15 Pro で再テストしたところ接続できたため、互換性設定の違いによるものです）。

## 三、高度な機能と handshake 能力のまとめ

範囲をもう一段広げて、handshake のエンドツーエンド、仮想インターフェース（VIF）、active monitor、mesh / IBSS を見ていきます。

| # | 型番 | WPA handshake キャプチャ | VIF | Active monitor | Ad-hoc（IBSS） | Mesh（802.11s） |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **エンドツーエンド**（.22000） | ✅ STA+AP / AP+mon | 🟡 設定可能、ACK は未検証 | 🟡 単体 | 🟡 単体 |
| 2 | AWUS036ACHM | ✅ **エンドツーエンド**（.22000、5 GHz ch36） | ✅ | 🟡 | 🟡 単体 | 🟡 単体 |
| 3 | AWUS036ACH | ✅ **エンドツーエンド**（.22000） | ✅ STA+mon | ❌ -95 | 🟡 単体 | ❌ -95 |
| 4 | AWUS036ACS | ✅ **エンドツーエンド**（.22000） | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **エンドツーエンド**（.22000、79 ACKs） | 🟡 パッシブ monitor + 同一チャンネルの managed（ソフトウェア monitor）。独立した 2 つの VIF は非対応 | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **エンドツーエンド**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **エンドツーエンド**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ injection 失敗 | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ injection 失敗 | ✅ | 🟡 | N/A | N/A |

ここでの「エンドツーエンド」には明確な定義があります。そのアダプタで **Yopitek 自社の iPhone 7 Plus**（自社の `YUPITEK` SSID に接続中）に対して injection を実行し、完全な 4-way handshake（M1–M4）をキャプチャし、`hcxpcapngtool --all` で hashcat 用の `.22000` 形式に変換するところまでを指します。この経路全体が通るかどうかが、「ペネトレーションテスト能力」の受け入れ基準であり、「monitor に入れる」だけでは合格とはしません。

- **エンドツーエンド合格（9 製品中 7 製品）**：ACM、ACHM、ACH、ACS、EACS、AX、AXER が `.22000` を出力できました。そのうち EACS は 79 個の ACK を受信しており、信号の返りが最も確実です。ACH は両バンドで injection 100% を達成し、2026-11-19 の追加テストで 47 行の hashline を持つ `.22000` への変換に成功しました。ACHM は 5GHz（ch36）で完走し、ACM は injection 成功率が低めでも完走しました。
- **エンドツーエンドが途切れる製品**：AXM / AXML は injection が失敗するため、handshake の経路全体が途切れます。MT7921 は本プラットフォームではペネトレーションテスト用途に向かないことが、ここでも裏付けられました。
- **VIF（仮想インターフェースの併用）**：9 製品すべてが何らかの形で複数インターフェースの併用に対応します。Realtek rtw89 は STA + AP を同時に動作させられますが、EACS はパッシブ monitor と同一チャンネルの managed の併用（ソフトウェア monitor）のみで、独立した 2 つの VIF には対応しません。
- **Active monitor（ACK 報告付き）**：`rtw88` の ACH / ACS / EACS は -95（非対応）を返します。`rtw89` の AX / AXER はドライバがこのモードを持ちません（N/A）。`mt76` / `mt7921u` は一部対応（🟡）です。
- **Mesh（802.11s）**：単体で構築できるのは `mt76` の ACM / ACHM のみです（🟡、完全な相互接続の検証には 2 枚目のアダプタが必要）。Realtek `rtw88` は -95 で非対応、`rtw89` と `mt7921u` はドライバがこのモードを持ちません。mesh の実験を行うなら、このラインナップで選択肢になるのは MediaTek `mt76` だけです。
- **IBSS（Ad-hoc）**：`mt76` の ACM / ACHM と `rtw88` の ACH は、単体で join できます（🟡）。EACS は iftype が列挙されるものの、実測では join が機能しませんでした。`rtw89` の AX / AXER は IBSS の iftype 自体がありません（N/A）。

### Kali / aircrack 系ツールの互換性（プラットフォーム共通）

以下のツールは、9 製品すべてに共通するプラットフォームレベルの挙動であり、個々のアダプタとは無関係です。

| ツール | 状態 | 説明 |
|---|---|---|
| airmon-ng | ✅ | 全アダプタで検出 / 管理が可能。**`check kill` は厳禁**（NetworkManager が停止して GX10 がネットワークから切断されます） |
| kismet | ✅ | 各アダプタをデータソースとして起動でき、`.kismet` ログを出力 |
| bettercap | ✅ | `wifi.recon` とチャンネルホッパーは正常動作 |
| wifite（git 3.0.0） | ✅ | スキャンしてターゲット一覧を作成可能（git 版が必須。apt 版は自前ビルドの aircrack-ng と競合） |
| Wireshark / tshark | ✅ | monitor でのキャプチャと解析は正常 |
| **hcxdumptool 8.x** | ⚠️ | **2.4 GHz の EACS を除く全アダプタで failed to arm（EACS も 5 GHz は失敗）**：active-monitor が必要ですが、`rtw88` / `rtw89` / `mt7921u` はいずれも非対応 → `airodump-ng` + `aireplay-ng` を使用 |

ARM64 の補足：`aircrack-ng` はソースからのビルドが必要です。`wifite` は git 3.0.0 版を推奨します。apt パッケージと自前ビルド版の間の依存関係の競合を回避できます。

## 四、用途別の選定ガイド

上の 3 つの表を、「用途からそのまま選べる」形にまとめます。

| 用途 | 第一候補 | 説明 |
|---|---|---|
| **ペネトレーションテスト（injection + handshake）** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | 両バンドの injection が最良（EACS、ACH は 100%）。エンドツーエンドの `.22000` は EACS、ACS、ACH で実証（ACH は 2026-11-19 に追加テスト） |
| **最強の受信 / 長距離 monitor** | **AWUS036AXER** / AWUS036ACH | AXER はチャンネルホッピングで一度に 63 個の AP と 12 個の client を検出。ACH はデュアルアンテナ高ゲイン |
| **Wi-Fi 6 + AP ホットスポット** | AWUS036AX / AWUS036AXER | 2x2 VHT80 で AP が安定しており、injection も利用可能 |
| **純粋な AP / 通常接続（injection 不要）** | AWUS036AXM / AWUS036AXML | MediaTek は接続が安定していますが、**injection は失敗**するためペネトレーション用途には不向き |
| **mesh / IBSS の実験** | AWUS036ACM / AWUS036ACHM | `mt76` ドライバは単体で mesh と IBSS を構築可能（`rtw88` の ACH は IBSS の単体 join のみで mesh は非対応。`rtw89` はどちらも未宣言） |

ひとことでまとめると次のとおりです。

- **ペネトレーションテストや handshake のキャプチャを行う場合**：エンドツーエンドの `.22000` をファイル出力まで実証できたのは 9 製品中 7 製品です。**AWUS036EACS**（最も確実、79 ACKs）、**AWUS036ACS**、Wi-Fi 6 の AWUS036AX / AWUS036AXER、**AWUS036ACM**、**AWUS036ACHM**（5 GHz）、そして **AWUS036ACH**（両バンドの injection 100%、2026-11-19 の追加テストで 47 行の hashline を持つ `.22000` への変換に成功）です。
- **最も遠い受信距離と最も広いキャプチャが必要な場合**：AWUS036AXER（Wi-Fi 6、内蔵アンテナの Nano 設計とチップのチューニングにより、ホッピングスキャンが最も積極的）、またはデュアルアンテナ高ゲインの AWUS036ACH。
- **Wi-Fi 6 のホットスポットを立てる場合**：AWUS036AX / AWUS036AXER。2x2 VHT80 で、injection にも同時に対応します。
- **安定した接続 / 単純な AP だけで足りる場合**：AWUS036AXM / AWUS036AXML。MediaTek 方式は接続が安定しており、日常利用では問題ありません。
- **mesh を試したい場合**：このラインナップでは `mt76` の AWUS036ACM / AWUS036ACHM だけが対応しています（IBSS の単体 join は `rtw88` の AWUS036ACH でも可能です）。

**避けるべき製品（最も重要な注意点）**：用途が **injection や handshake** であれば、**AWUS036AXM / AWUS036AXML は選ばないでください**。MT7921 は、ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）というこのプラットフォームでは injection に失敗します。主因は kernel 6.16+ の mac80211 chanctx のリグレッションであり（チップ固有の問題ではありません）、設定の問題でもありません。コミュニティでは同型番に git／パッチ適用済みドライバを使うと動作するものの、ファームウェアがレートをロックします。本プラットフォームの stock kernel では、依然として injection はできません。この 2 製品は「純粋な接続 / 純粋な AP」の用途に限定してください。

## 五、プラットフォームの注意事項（GX10 ARM64 の実運用）

ASUS GX10 + Ubuntu 24.04（ARM64）でこれらのアダプタを操作する際に、9 製品に共通する実務上の要点を挙げます。

1. **自分のネットワークを切断しないこと**：`airmon-ng check kill` は絶対に実行しないでください。NetworkManager が停止し、GX10 全体がネットワークから切断されます。操作対象は外付けの `wlx*` インターフェースだけにし、外部接続に使っている内蔵の主回線には触れないでください。
2. **RX stall の解消**：monitor / AP の切り替えを繰り返した後に、突然何もスキャンできなくなった場合は、たいてい RX stall です。アダプタを一度抜き挿しすれば復旧します（USB が再列挙され、インターフェース名は MAC ベースのため変わりません）。
3. **BT + WiFi コンボデバイス**：EACS と AXML は Bluetooth を同時に搭載しており、抜き挿しの際に WiFi の probe で止まって `wlx` インターフェースが生成されないことが時々あります。USB ポートを変えれば、たいてい解決します。
4. **5GHz の TX 解放**：自社環境で 5GHz の injection を行う前に、正しい規制ドメイン（regulatory domain）を設定して TX 出力を解放する必要があります。テスト終了後は、地域のドメインに戻してください。これは 5GHz が正常に送信できるための前提条件です。
5. **handshake キャプチャのコツ**：オフィス内には同名の AP が複数台あることが多いため、実務上は単一の BSSID に絞らず、チャンネル全体をキャプチャするほうが安定します。変換時は `hcxpcapngtool --all` を使用します。
6. **hcxdumptool はプラットフォーム全体で failed to arm（例外は 2.4 GHz の EACS）**：トライバンドの内蔵アダプタと上記のドライバはいずれも active-monitor に非対応のため、aircrack-ng スイート（`airodump-ng` + `aireplay-ng`）に切り替えてください。
7. **ARM64 でのビルドの細部**：`aircrack-ng` はソースからのビルドが必要です。`wifite` は git 版を使い、apt の依存関係の競合を回避します。

改めて位置づけを強調します。上記の injection / deauth / handshake の能力は、すべて Yopitek 自社の閉じた環境で、自社のテスト機器に対して測定したものであり、製品の能力と互換性の限界を検証することが目的です。本記事は、第三者のネットワークに対して上記の操作を行うことを提供も推奨もしていません。

## まとめ

ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）というこのプラットフォームでの ALFA 9 製品の総評は、3 文に集約できます。**Monitor は全製品で利用可能、AP と WPA3 はほぼ全製品が合格、分かれ目は Injection です。** injection と handshake が必要な専門用途には、Realtek `rtw88` の EACS / ACH / ACS が最も安定した選択です。受信感度と Wi-Fi 6 が必要なら AXER / AX を選び、MT7921 の AXM / AXML は純粋な接続用途にとどめてください。全製品がビルド不要で、挿すだけで使えることが、ARM64 におけるこのラインナップ最大の共通の利点です。

## よくある質問（FAQ）

**Q：AWUS036AXM は Ubuntu で injection できますか？**
A：本プラットフォームではできません。実測では、AWUS036AXM と AWUS036AXML（どちらも MT7921 チップ）は、2.4GHz と 5GHz のどちらでも injection に失敗しました。主因は stock kernel 6.16+ の mac80211 chanctx のリグレッションであり（チップ固有の問題ではありません）、本プラットフォームでは injection や handshake キャプチャが必要な用途にはおすすめしません。

**Q：Ubuntu で injection 成功率が最も高い ALFA アダプタはどれですか？**
A：実測では、AWUS036ACH と AWUS036EACS が 2.4GHz と 5GHz の両方で injection 成功率 100% に達しました。今回の 9 製品のうち、最も成績の良い 2 製品です。

**Q：9 製品の ALFA アダプタは、Ubuntu 24.04 で別途ドライバをインストールする必要がありますか？**
A：必要ありません。9 製品は kernel 6.17 ですべて kernel 内蔵（in-kernel）ドライバ（rtw88 / rtw89 / mt76 ファミリー）で動作し、挿すだけで認識されます。DKMS モジュールのビルドも不要です。

**Q：ALFA アダプタを使って Ubuntu で WPA3-SAE のホットスポットを立てられますか？**
A：できます。9 製品すべてで WPA3-SAE ホットスポットの構築と端末の接続に成功しました（ACS は 5 GHz、それ以外は 2.4 GHz で実測。AXML は 6 GHz でも実測）。ただし AWUS036ACHM だけは、hostapd の `sae_pwe` を 0 に設定する必要があります。そうしないと、旧型の iPhone 7 Plus が接続に失敗します。

**Q：この Ubuntu でのテスト結果は、Kali Linux のユーザーも参考にできますか？**
A：Kali Linux は Debian/Ubuntu 系で、同じ rtw88 / rtw89 / mt76 の in-kernel ドライバを使用します。そのため、本記事のドライバ互換性と能力マトリクスは、原則として Kali ユーザーの参考になります。ただし、本記事の実測プラットフォームは Ubuntu 24.04 であり、Kali では正式な再テストをまだ行っていません。結果は今後の再テストを基準にしてください。

## 関連記事

本記事は総括表のハブ記事です。以下の詳細記事とアダプタごとの実測記事を順次公開します（リンクは準備中です）。

- 『ドライバ不要：Ubuntu（ARM64）で Monitor モードと AP モードを有効にする』 → [`/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 『WPA3-SAE handshake キャプチャの実務（自社環境での検証）』 → [`/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)

アダプタごとの詳細実測記事 9 本：

- [AWUS036ACM 単体実測](/ja/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM 単体実測](/ja/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH 単体実測](/ja/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS 単体実測](/ja/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS 単体実測](/ja/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX 単体実測](/ja/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER 単体実測](/ja/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM 単体実測](/ja/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML 単体実測](/ja/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*テスト実施：Yopitek（ALFA Network 台湾代理店）｜ テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ テスト端末：Apple iPhone 7 Plus（WPA3 は iPhone 15 Pro でも別途テスト）｜ テスト環境：自社オフィスの Wi-Fi。本記事は製品の互換性と能力の検証であり、第三者のネットワークに対する操作手順の解説ではありません。*
