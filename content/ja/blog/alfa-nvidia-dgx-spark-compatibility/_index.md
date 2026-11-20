---
title: "ALFA無線LANアダプターはNVIDIA DGX Spark（GB10）に対応しているか"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "ハードウェアガイド"
description: "ALFA USB無線LAN 9機種のNVIDIA DGX Spark（GB10）対応状況。GX10のkernel 6.17実測で全機種が内蔵ドライバーで動作しDKMS不要、注入はEACS／ACH／ACSが安定、AXM／AXMLは失敗しました。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本記事は2026年11月のGX10実機テストに基づいて更新しました：ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）では、ALFA現行9機種のアダプターがすべてkernel内蔵ドライバーで動作し、挿すだけで使用でき、DKMSは不要です。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。テストはGX10のみで実施しており、他のGB10機種は個別にテストしていません。

## 1. 質問の要約

お客様からの質問：「ALFAシリーズのUSB無線LANアダプターは、NVIDIA DGX Spark（GB10 Grace Blackwell）パーソナルAIスーパーコンピューターで使用できますか？」

簡潔な結論：DGX SparkはNVIDIA DGX OS（Ubuntuベース、kernel 6.x）で動作します。当社は同じGB10プラットフォームのASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）でALFA現行9機種のUSB無線LANアダプターを実機テストし、全機種がkernel内蔵ドライバーで動作し、挿すだけで使用でき、コンパイルやDKMSは不要であることを確認しました。DGX Sparkは同じGB10とNVIDIA kernel系列を使用しているため同じ動作が見込まれますが、テストはGX10のみで、DGX Sparkは個別にテストしていません。機能差：MediaTek MT7921機種（AWUS036AXM / AXML）はstock kernel 6.17上でパケットインジェクションに失敗し、monitor、AP、WPA3は使用可能です。残り7機種はmonitorとインジェクションの両方が実機で動作しました。各アダプターのドライバーがメインラインに入った最低kernelバージョンは異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、コミュニティのDKMSドライバーが必要なのはそれより古いkernelのみです。注意：DGX SparkのUSBポートはすべてUSB Type-Cで、ALFAアダプターはUSB Type-Aのため、USB-C to USB-A変換アダプターまたはケーブルが必要です。

判定対象：ALFA現行9機種のUSB無線LANアダプター（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析対象ハードウェアの仕様構成

### 2.1 NVIDIA DGX Spark ハードウェア仕様

| 項目 | 仕様 |
|---|---|
| 製品名 | NVIDIA DGX Spark |
| コアチップ | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725）、ARMv9.2-A |
| GPU | NVIDIA Blackwell アーキテクチャ、6144 CUDA コア、第5世代 Tensor Core、第4世代 RT Core |
| AI 性能 | 最大 1 PetaFLOP（FP4、Sparse）/ 1000 TOPS |
| システムメモリ | 128GB LPDDR5x 統合メモリ（256-bit、273 GB/s） |
| ストレージ | 最大 4TB NVMe M.2 SSD（自己暗号化） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps）、うち 1 基は PD 入力に対応（180W EPR PD3.1） |
| 映像出力 | 1× HDMI 2.1a |
| 有線ネットワーク | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（200G QSFP） |
| 無線ネットワーク | Wi-Fi 7（内蔵）+ Bluetooth 5.4 |
| オペレーティングシステム | NVIDIA DGX OS（Ubuntu Linux ベース、kernel 6.x） |
| アーキテクチャ | aarch64（ARM64） |
| サイズ | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 約 1.2 kg |
| 電源 | 240W USB-C 電源アダプター |

### 2.2 ソフトウェア環境：NVIDIA DGX OS

| 項目 | 説明 |
|---|---|
| ベース | Ubuntu Linux（NVIDIA カスタマイズ） |
| Kernel | Linux 6.x（具体的なバージョンは DGX OS の更新に従う） |
| アーキテクチャ | aarch64（ARM64） |
| プリインストールソフトウェア | NVIDIA AI ソフトウェアスタック（CUDA、cuDNN、TensorRT、PyTorch、Jupyter など） |
| パッケージ管理 | apt（Debian/Ubuntu 系） |
| ドライバーフレームワーク | 標準の Linux kernel driver アーキテクチャ（cfg80211 / mac80211） |

### 2.3 重要な特徴：最新の kernel + ARM64

DGX Spark のソフトウェア環境は、ALFA アダプターの互換性に 2 つの重要な影響を与えます：

- Kernel 6.x（最新）：kernel 6.17（GX10 の実測バージョン）には、本記事の 9 機種すべてのドライバーが内蔵されています。mt76（MT7612U / MT7610U、4.19+）、mt7921u（MT7921AUN、5.18+）、rtw88（RTL8821CU 6.2+、RTL8812AU / RTL8811AU 6.13+）、rtw89（RTL8832BU、6.17+）です。これは Jetson Nano の kernel 4.9 とは対照的です。
- ARM64（aarch64）アーキテクチャ：kernel 内蔵ドライバーを使う場合、ARM64 上で何かをコンパイルする必要はありません。Realtek 機種でコミュニティの DKMS ドライバー（morrownr シリーズなど。Makefile の CONFIG_PLATFORM_ARM64 = y を確認）のコンパイルが必要なのは、kernel がその機種の最低バージョンより古いシステムのみです。

### 2.4 USB Type-C 変換の必要性

DGX Spark の 4 つの USB ポートはすべて Type-C ですが、ALFA の全シリーズのアダプター（USB-C の AXML を除く）は USB Type-A インターフェースです：

| 機種 | インターフェース仕様 | 変換の要否 |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ 変換不要（直挿し可能） |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ USB-C to USB-A が必要 |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ 必要 |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ 必要 |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ 必要 |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ 必要 |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ 必要 |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ 必要 |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ 必要 |

おすすめ：AWUS036ACH / ACM / AX などの USB 3.x 機種がフルスピードで動作するよう、USB 3.2 Gen 2×2（20Gbps）対応の USB-C to USB-A 変換アダプターまたはケーブルを使用してください。

## 3. 現行ALFAアダプターの仕様とチップセットの分析

2026年9月時点で、ALFA Networkの現行USB無線LANアダプターのラインナップは以下のとおりです（判定対象：9機種）：

| 機種 | Wi-Fi 規格 | チップセット | インターフェース | Linux 内蔵ドライバー（最低 kernel バージョン） |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E（6GHz 実機で動作確認） | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ 内蔵（mt7921u、5.18+） |
| AWUS036AXM | Wi-Fi 6E（メーカー公称、6GHz 未テスト） | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ 内蔵（mt7921u、5.18+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 内蔵（rtw89_8852bu、6.17+） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 内蔵（rtw89_8852bu、6.17+） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 内蔵（rtw88_8812au、6.13+） |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ 内蔵（mt76x0u、4.19+） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ 内蔵（mt76x2u、4.19+） |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ 内蔵（rtw88_8821au、6.13+） |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ 内蔵（rtw88_8821cu、6.2+） |

注：GX10 で実測した kernel 6.17 には 9 機種すべてのドライバーが内蔵されています。最低 kernel バージョンは機種ごとに異なります（上表の括弧内）。コミュニティ保守の DKMS ドライバーのインストールが必要なのは、kernel がその機種の最低バージョンより古いシステムのみです。

## 4. 対応機種とチップセット

### 4.1 推奨レベル

| 推奨レベル | 機種（チップセット） | 説明 |
|---|---|---|
| ⭐ ペネトレーションテストに最適 | AWUS036EACS（RTL8821CU）/ AWUS036ACH（RTL8812AU）/ AWUS036ACS（RTL8811AU） | 内蔵ドライバーでインストール不要。インジェクション実測値は EACS、ACH が両バンド 100%、ACS が 2.4GHz 100%・5GHz 96%。WPA handshake をエンドツーエンドで取得可能 |
| ✅ 推奨 | AWUS036ACM（MT7612U） | 内蔵ドライバーでインストール不要。monitor、インジェクション（2.4GHz 63–83%、5GHz 76%）、AP、WPA3 すべて使用可能 |
| ✅ 推奨 | AWUS036ACHM（MT7610U） | 内蔵ドライバーでインストール不要。2.4GHz インジェクション 96–100%、5GHz インジェクションはブロードキャストのみ可能。WPA3 AP には sae_pwe=0 の設定が必要 |
| ✅ 推奨（Wi-Fi 6） | AWUS036AX / AXER（RTL8832BU） | 内蔵ドライバーでインストール不要。monitor の受信感度が高く、インジェクション可能（2.4GHz：AX 96%、AXER 73%）、AP は 80MHz に対応 |
| ⚠️ 接続／AP 用途のみ | AWUS036AXML / AXM（MT7921AUN） | 内蔵ドライバーでインストール不要。monitor、AP、WPA3 は使用可能だが、stock kernel 6.17 ではインジェクションに失敗するため、ペネトレーションテストには不向き。AXML は USB-C で直挿し可能 |

### 4.2 用途別のおすすめ

| 用途 | おすすめ機種 | 説明 |
|---|---|---|
| 一般的な無線インターネット接続（最も簡単） | 9 機種すべて可（例：AWUS036ACM / ACHM） | すべて kernel 内蔵ドライバーで、挿すだけで使用可能 |
| 無線ペネトレーションテスト / 監視 / インジェクション | AWUS036EACS / ACH / ACS | インジェクション実測 96–100%、WPA handshake をエンドツーエンドで取得可能。AXM / AXML は選ばないこと（インジェクション失敗） |
| Wi-Fi 6 + AP ホットスポット | AWUS036AX / AXER | 2x2、80MHz AP が実機で動作 |
| 6GHz 帯 | AWUS036AXML | 6GHz で WPA3 AP を構築できることを実機で確認。AXM は同じチップだが 6GHz は未テスト |
| 手持ちの AWUS036ACH を引き続き使いたい | AWUS036ACH | kernel 6.13 以上は rtw88_8812au を内蔵しており、挿すだけで使用可能。両バンドのインジェクション実測 100% |
| 外付け WiFi が不要な場合（内蔵を使用） | — | DGX Spark は Wi-Fi 7 を内蔵しており、一般的なインターネット接続には外付けの ALFA は不要 |

注意：DGX Spark は Wi-Fi 7 + Bluetooth 5.4 を内蔵しているため、一般的なインターネット接続では外付けの ALFA アダプターは不要です。外付け ALFA が主に必要となるのは、ペネトレーションテスト（監視／インジェクション）、特定チップセットが必要な場合、または内蔵 WiFi では不十分な場合です。

## 5. 環境要件

### 5.1 ハードウェア要件

| 項目 | 要件 |
|---|---|
| USB 変換アダプター | USB-C to USB-A 変換アダプターまたはケーブル（AXML を除く） |
| 電源 | DGX Spark 純正 240W USB-C 電源アダプター（USB ポートへの給電は十分） |
| 冷却 | 純正の冷却で十分（USB WiFi によってシステム負荷が大きく増えることはありません） |

### 5.2 ソフトウェア要件

| 項目 | 要件 |
|---|---|
| DGX OS バージョン | 現行の任意のバージョン（kernel 6.x） |
| Kernel バージョン | kernel 6.17（GX10 実測 6.17.0-1014-nvidia）には 9 機種すべてのドライバーが内蔵されており、コンパイルツールは不要。最低バージョンは機種ごとに異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、それより古い場合のみコミュニティの DKMS ドライバーのインストールが必要 |
| 無線管理ツール | iw、wpa_supplicant、network-manager（DGX OS にデフォルトでインストール済み） |

## 6. 互換性の判定

### ALFA 現行機種 × NVIDIA DGX Spark（GB10）互換性マトリックス

| 機種 | チップセット | ドライバー（kernel 内蔵） | USB 検出 | STA 接続 | AP モード | Monitor | パケットインジェクション | 導入難易度 | 総合評価 |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 両バンド 100% | インストール不要 | ⭐ 最適 |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 両バンド 100% | インストール不要 | ⭐ 最適 |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100%／5G 96% | インストール不要 | ⭐ 最適 |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83%／5G 76% | インストール不要 | ✅ 良好 |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100%／5G ブロードキャストのみ | インストール不要 | ✅ 良好 |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 受信強 | ✅ 2.4G 96%／5G 可 | インストール不要 | ✅ 良好 |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 受信強 | ✅ 2.4G 73%／5G 可 | インストール不要 | ✅ 良好 |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 受信弱 | ❌ 失敗 | インストール不要 | ⚠️ 接続／AP のみ |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 受信弱 | ❌ 失敗 | インストール不要 | ⚠️ 接続／AP のみ |

判定根拠：2026年11月16日～18日に ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）で実機テストを実施し、テスト対象は自社所有の Wi-Fi と自社所有のスマートフォンです。DGX Spark は同じ GB10 と NVIDIA kernel 系列を使用しているため同じ動作が見込まれますが、テストは GX10 のみで、DGX Spark は個別にテストしていません。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。

## 7. 超詳細 Step by Step 設定手順

### 7.1 事前準備

**手順 1：DGX Spark を起動してログイン**（SSH 経由、またはキーボードとモニターを直接接続）

```bash
ssh username@<dgx-spark-ip>
```

**手順 2：システムアーキテクチャと kernel バージョンを確認**

```bash
uname -m
# 期待値: aarch64
uname -r
# 期待値: 6.x.x (DGX OS kernel)
```

**手順 3：kernel バージョンが 6.17 以上かを確認**

kernel 6.17 以上には 9 機種すべてのドライバーが内蔵されているため、コンパイルツールのインストールは不要です。最低バージョンは機種ごとに異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、それより古い場合に限り、Realtek 機種でコミュニティの DKMS ドライバーが必要です（7.3 の最後の段落を参照）。

### 7.2 ルート A：MediaTek チップセット機種（AWUS036ACM / ACHM / AXML / AXM）— 挿すだけで使用可能

**手順 1：アダプターを挿す**

USB-C to USB-A 変換アダプター（AXML は USB-C ポートに直挿し可能）を使い、ALFA アダプターを DGX Spark の USB ポートに挿します。

**手順 2：アダプターが検出されたことを確認**

```bash
lsusb
# 出力例 (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**手順 3：ネットワークインターフェースが自動作成されたことを確認**

```bash
ip link show
# wlx で始まるインターフェースが表示されるはずです (MAC に基づく命名, in-kernel ドライバーが自動ロード)
```

**手順 4：WiFi ネットワークをスキャン**（以下は wlan0 を例にしています。`ip link show` で確認したインターフェース名に置き換えてください）

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**手順 5：WiFi に接続（NetworkManager を使用）**

```bash
nmcli dev wifi list
nmcli dev wifi connect "あなたのWiFi名" password "あなたのWiFiパスワード"
```

**手順 6：（任意）モニターモードを有効化**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 ルート B：Realtek Wi-Fi 5 機種（AWUS036ACH / ACS / EACS）— kernel 6.13+ ならインストール不要（EACS は 6.2+）

**手順 1：アダプターを挿し、ドライバーが自動ロードされたことを確認**

```bash
uname -r          # ACH/ACS は 6.13 以上, EACS は 6.2 以上が必要
lsusb
lsmod | grep rtw88
ip link show
```

各機種で自動ロードされるモジュール：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`（EACS は Bluetooth も搭載しており、実機で動作を確認）。

**手順 2：接続方法は 7.2 の手順 5 と同じ（nmcli を使用）**

**手順 3：（任意）モニターモードとインジェクション**

⚠️ 監視とインジェクションのテストは、自分が所有する、または許可を得たネットワークでのみ行ってください。

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # ip link で確認したインターフェース名に置き換える
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- `airmon-ng check kill` は実行しないでください：NetworkManager が停止し、ホストの外部接続が切断されます。
- AWUS036AXM / AXML は stock kernel 6.17 上で `aireplay-ng --test` が失敗し（Found 0 APs）、deauth や handshake の取得はできません。
- hcxdumptool 8.x は 2.4 GHz の EACS を除く全機種で `failed to arm`（ドライバーが active monitor 非対応）となるため、airodump-ng + aireplay-ng を使用してください。

**古い kernel（ACH／ACS は 6.13 未満、EACS は 6.2 未満）でのみ必要な手順**：`build-essential git bc dkms` をインストールした後、コミュニティのドライバーをコンパイルします。例えば RTL8812AU なら morrownr/8812au-20210820 を使用します（Makefile の `CONFIG_PLATFORM_ARM64 = y` を確認）。バージョンが足りていれば内蔵ドライバーをそのまま使用してください。

### 7.4 ルート C：Wi-Fi 6 機種（AWUS036AX / AXER、RTL8832BU）— kernel 6.17+ ならインストール不要

```bash
lsusb                      # 0bda:b832 が表示されるはず
lsmod | grep rtw89_8852bu
ip link show
```

GX10 での実測：kernel 内蔵の `rtw89_8852bu` が自動ロードされ、monitor の受信感度が高く、インジェクション可能（2.4GHz：AX 96%、AXER 73%）、AP は 80MHz に対応しました。rtw89_8852bu は kernel 6.17 で初めてメインラインに入ったため、kernel 6.16 以下のシステムではコミュニティの DKMS ドライバー（morrownr/rtl8852bu-20250826）が必要です。

## 8. よくあるエラーと対処法

| 症状 | 考えられる原因 | 対処法 |
|---|---|---|
| lsusb で ALFA アダプターが表示されない | USB-C 変換アダプターの不良 / 接触不良 | USB-C to USB-A 変換アダプターを交換。変換アダプターがデータ転送に対応しているか（充電専用でないか）を確認。別の USB-C ポートを試す |
| MediaTek チップを挿しても wlan インターフェースが出ない | kernel module が自動ロードされない / ファームウェアの欠落 | 手動ロード：`sudo modprobe mt76x2u`；`dmesg \| grep mt76` を確認；ファームウェアのインストール：`sudo apt install linux-firmware` |
| Realtek アダプターを挿しても wlan インターフェースが出ない | kernel がその機種の最低バージョン（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）より古く、対応ドライバーが内蔵されていない | `uname -r` でバージョンを確認。kernel をアップグレードするか、古い kernel ではコミュニティの DKMS ドライバーをインストール |
| 古い kernel で DKMS ドライバーをインストールした後、modprobe で Operation not permitted が出る | Secure Boot / モジュール署名 | モジュールに署名するか Secure Boot を無効化（内蔵ドライバーを使う場合は発生しません） |
| monitor／AP を繰り返し切り替えた後、何も受信できない | RX 停止（RX stall） | アダプターを抜き差しして USB を再列挙させる |
| EACS／AXML を挿し直した後に wlx インターフェースが出ない | Bluetooth＋Wi-Fi 複合デバイスの probe が停止 | 別の USB ポートに挿し直す |
| WiFi 接続が不安定 / 速度が遅い | USB-C 変換アダプターが USB 2.0 のみ対応 | USB 3.2 Gen 2×2 対応の変換アダプターに交換。変換アダプターの表示が「Charge Only」ではなく「Data」であることを確認 |
| 内蔵 Wi-Fi 7 と外付け ALFA が競合する | 2 つの無線インターフェースのルーティング競合 | 内蔵 WiFi を無効化：`sudo nmcli radio wifi off`、または BIOS/UEFI で無効化。あるいはルーティングの優先順位を設定 |
| 6GHz（Wi-Fi 6E）が使えない | Regulatory Domain の制限 | 規制地域を設定：`sudo iw reg set US`（米国は 6GHz を開放）。AXML は 6GHz での動作を実機で確認済み、AXM は未テスト |
| AP モードの起動に失敗する | NetworkManager と hostapd の競合 | Yopitek の ALFA Soft AP ガイドを参照。そのインターフェースを NetworkManager の管理対象から外し、hostapd を手動で設定 |
| スリープ復帰後にアダプターが消える | USB の自動サスペンド | USB 自動サスペンドを無効化：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 既知の制限

- USB Type-C 変換が必要：AXML 以外のすべての ALFA アダプターに USB-C to USB-A 変換アダプターが必要で、変換アダプターの品質が性能と安定性に影響します
- MT7921 機種のインジェクション失敗：AWUS036AXM / AXML は stock kernel 6.17 上でパケットインジェクションに失敗し、deauth や handshake の取得ができません。monitor、AP、WPA3 は使用可能です。主な原因は kernel 6.16 以降の mac80211 chanctx のリグレッションで、コミュニティのパッチ版ドライバーにもまだレート制限があります
- テスト範囲：ASUS GX10（kernel 6.17.0-1014-nvidia）でのみ実機テストしており、DGX Spark は個別にテストしていません（同じ動作が見込まれます）
- hcxdumptool は使用不可：2.4 GHz の EACS を除く全機種で `failed to arm` となるため、airodump-ng + aireplay-ng を使用してください
- 内蔵 Wi-Fi 7 と外付けが競合する可能性：DGX Spark は Wi-Fi 7 を内蔵しており、内蔵と外付けの WiFi を同時に使うとルーティングやリソースの競合が起きる場合があります
- AP モードは手動設定が必要：DGX OS はデフォルトで開発環境として構成されており、AP ホットスポットモードには hostapd / dnsmasq の手動インストールと設定が必要です
- 6GHz の法規制限：Wi-Fi 6E の 6GHz 帯の利用可否は規制地域の設定によって異なります。台湾での 6GHz の開放状況は最新の法規を確認してください
- 古い kernel：Realtek 機種でコミュニティの DKMS ドライバー（morrownr）が必要なのは kernel がその機種の最低バージョン（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）より古いシステムのみで、その場合は kernel 更新のたびに再コンパイルが必要です
- ペネトレーションテスト機能の差：GX10 の実測ではインジェクション成功率は Realtek rtw88 機種が最も高く（EACS、ACH は両バンド 100%）、MediaTek mt76 機種（ACM / ACHM）は使用可能、MT7921（AXM / AXML）は失敗しました
- Bluetooth 機能：AWUS036AXML と AWUS036EACS の Bluetooth は GX10 上で動作を確認しました。AWUS036AXM の Bluetooth は個別に検証していません（DGX Spark は BT 5.4 を内蔵）
- RTL8832BU（AWUS036AX / AXER）：ドライバーのメンテナーである morrownr は、rtl8852/32au シリーズの out-of-tree ドライバーを避けるよう公に推奨したことがあります（出典は第10節）。今回の GX10 実機テストでは kernel 内蔵の `rtw89_8852bu` を使用し、monitor、インジェクション、AP、WPA3 すべてが使用可能でした。この結論は kernel 6.17 以上の内蔵ドライバーにのみ当てはまります
- RTL8812AU（AWUS036ACH）：mac80211 標準の in-kernel ドライバー `rtw88_8812au` は kernel 6.13 でメインラインに統合され、6.14 以降で品質が成熟しました（morrownr の告知）。GX10 では kernel 6.17 で挿すだけで動作し、両バンドのインジェクションは 100% でした。サポート対応の前に、お客様に `uname -r` を報告してもらい、6.13 以上かどうかを確認するとよいでしょう

反証条件：DGX OS の更新で kernel バージョンや USB コントローラードライバーが変わり動作が異なる場合、または DGX Spark の実機で GX10 と異なる結果が得られた場合は、本記事第6節の互換性マトリックスを見直す必要があります。将来の kernel で mt7921u のインジェクション問題が修正された場合、AWUS036AXM / AXML の評価は「接続／AP のみ」から引き上げられる可能性があります。

## 10. 参考情報 URL

| 情報源 | 説明 | URL | 確認状態 | 確認日 |
|---|---|---|---|---|
| NVIDIA DGX Spark 公式ページ | DGX Spark の仕様とプラットフォーム情報 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 確認済み | 2026-09-03 |
| NVIDIA DGX ドキュメント | DGX OS のシステム構成と kernel バージョン | https://docs.nvidia.com/dgx/dgx-spark | ✅ 確認済み | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux ドライバー（ARM64 対応） | https://github.com/morrownr/8812au-20210820 | ✅ 確認済み | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux ドライバー（古い kernel 用） | https://github.com/morrownr/8821cu-20210916 | ✅ 確認済み | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux ドライバー | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 確認済み | 2026-09-03 |
| Linux kernel mt76 ドライバードキュメント | MediaTek mt76 / mt7921 メインラインドライバーの説明（各チップの対応開始 kernel バージョンを含む） | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 確認済み | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yopitek） | Linux での ALFA AP モード設定ガイド | /ja/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 確認済み | 2026-09-03 |
| ALFA 9機種 ARM64 実機テスト総まとめ（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 実機テスト | https://yupitek.com/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 実機テスト | 2026-11-18 |
| ALFA Network 製品一覧（Yopitek） | ALFA 現行製品仕様 | /ja/products/alfa/ | ✅ 確認済み | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | ドライバーメンテナーによる公式声明：rtl8852/32au（RTL8832BU）チップは避けることを推奨 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 確認済み | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU ドライバーの最新状況（kernel 6.13 でメインライン統合、6.14 で品質成熟） | https://github.com/morrownr/8812au-20210820 | ✅ 確認済み | 2026-09-03 |

関連記事：[ALFA無線LANアダプターはMSI EdgeXpertに対応しているか](/ja/blog/alfa-msi-edgexpert-compatibility/)｜[ALFA無線LANアダプターはASUS Ascent GX10に対応しているか](/ja/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA無線LANアダプターはALTOS BrainSphere GB10 F1に対応しているか](/ja/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA無線LANアダプターはGIGABYTE AI TOP ATOMに対応しているか](/ja/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA無線LANアダプターはNVIDIA Jetson Nanoに対応しているか](/ja/blog/alfa-nvidia-jetson-nano-compatibility/)

免責事項：本記事の互換性判定は、2026年11月に ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）で行った実機テストを基準としています。DGX Spark は GX10 と同じ GB10 と NVIDIA kernel 系列を使用しているため同じ動作が見込まれますが、個別にはテストしていません。GX10 で実測した kernel 6.17 には ALFA 9 機種のドライバーがすべて内蔵されており（最低バージョンは機種ごとに異なる）、コミュニティの DKMS ドライバー（morrownr）が必要なのは kernel がその機種の最低バージョンより古い場合のみです。DGX Spark は Wi-Fi 7 を内蔵しており、外付けの ALFA アダプターは主にペネトレーションテストや特定チップセットが必要な用途に使われます。USB-C 変換アダプターの品質は使い勝手に直接影響するため、USB 3.2 Gen 2×2 の表示があるブランド品を選ぶことをおすすめします。監視とインジェクションは、自分が所有する、または許可を得たネットワークでのみ行ってください。
