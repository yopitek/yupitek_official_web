---
title: "ALFA無線LANアダプターはGIGABYTE AI TOP ATOM（GB10）に対応しているか"
date: 2026-09-03
draft: false
slug: "alfa-gigabyte-ai-top-atom-compatibility"
tags:
  - "ALFA"
  - "GIGABYTE"
  - "AI-TOP-ATOM"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "ハードウェアガイド"
description: "ALFA USB無線LAN 9機種のGIGABYTE AI TOP ATOM（GB10）対応状況。GX10のkernel 6.17実測で全機種が内蔵ドライバーで動作しDKMS不要、AXM／AXMLは注入に失敗しました。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本記事は2026年11月のGX10実機テストに基づいて更新しました：ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）では、ALFA現行9機種のアダプターがすべてkernel内蔵ドライバーで動作し、挿すだけで使用でき、DKMSは不要です。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。テストはGX10のみで実施しており、他のGB10機種は個別にテストしていません。

## 1. 質問の要約

お客様からの質問：「ALFAシリーズのUSB無線LANアダプターは、GIGABYTE AI TOP ATOM（型番 ATAGB10-9000、NVIDIA GB10 Grace Blackwell）パーソナルAIスーパーコンピューターで使用できますか？」

簡潔な結論：GIGABYTE AI TOP ATOMとNVIDIA DGX Sparkは、同じGB10チップとNVIDIA kernel系列を使用しています。当社はASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）でALFA現行9機種のUSB無線LANアダプター（AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML）を実機テストし、全機種がkernel内蔵ドライバーで動作し、挿すだけで使用でき、コンパイルやDKMSは不要であることを確認しました。同じ動作が見込まれますが、テストはGX10のみで、GIGABYTE AI TOP ATOMは個別にテストしていません。機能差：MediaTek MT7921機種（AWUS036AXM / AXML）はstock kernel 6.17上でパケットインジェクション（packet injection）に失敗し、monitor、AP、WPA3は使用可能です。残り7機種はmonitorとインジェクションの両方が実機で動作しました。各アダプターのドライバーがメインラインに入った最低kernelバージョンは異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、コミュニティのDKMSドライバーが必要なのはそれより古いkernelのみです。注意：AI TOP ATOMのUSBポートはすべてUSB Type-Cのため、ALFAアダプター（AXMLを除く）にはUSB-C to USB-A変換アダプターが必要です。

## 2. 分析対象ハードウェアの仕様構成

### 2.1 GIGABYTE AI TOP ATOM ハードウェア仕様

| 項目 | 仕様 |
|---|---|
| 製品名 | GIGABYTE AI TOP ATOM（型番：ATAGB10-9000 / ATAGB10-9001） |
| コアチップ | NVIDIA GB10 Grace Blackwell Superchip（DGX Spark プラットフォーム） |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725）、ARMv9.2-A |
| GPU | NVIDIA Blackwell アーキテクチャ、6144 CUDA コア、第5世代 Tensor Core、第4世代 RT Core |
| AI 性能 | 最大 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS、最大 2000 億パラメータのモデルに対応 |
| システムメモリ | 128GB LPDDR5x 統合メモリ（256-bit、273 GB/s） |
| ストレージ | 最大 4TB M.2 NVMe SSD（ATAGB10-9000 は PCIe Gen5 4TB、9001 は Gen4 4TB） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps）、うち 1 基は電源入力（GB10 リファレンス設計と同じ） |
| 映像出力 | 1× HDMI 2.1a（USB-C DP Alt Mode で拡張可能） |
| 有線ネットワーク | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC |
| 無線ネットワーク | Wi-Fi 7 + Bluetooth 5.4 |
| オペレーティングシステム | NVIDIA DGX OS（Ubuntu Linux ベース、kernel 6.x） |
| アーキテクチャ | aarch64（ARM64） |
| サイズ | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 約 1.2 kg |
| 電源 | 240W USB-C 電源アダプター |
| 保証 | 1 年間のメーカー保証 |

> 仕様確認の注記：サイズ 50.5mm / 重量 1.2kg は GIGABYTE 公式仕様と一致しています。Bluetooth のバージョンは GIGABYTE 公式仕様ページに基づき **BT 5.4** です（[公式仕様ページ](https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM/sp)）。USB 構成はデータポート 3 基 + 電源ポート 1 基です（公式仕様は 4× Type-C で、うち 1 基は dedicated to system power）。

### 2.2 ソフトウェア環境：NVIDIA DGX OS

| 項目 | 内容 |
|---|---|
| ベース OS | Ubuntu Linux（NVIDIA カスタマイズ版） |
| Kernel | Linux 6.x |
| アーキテクチャ | aarch64（ARM64） |
| プリインストールソフトウェア | NVIDIA AI ソフトウェアスタック（CUDA、cuDNN、TensorRT、PyTorch、Jupyter、Ollama など）+ GIGABYTE AI TOP Utility |
| パッケージ管理 | apt |

### 2.3 DGX Sparkとの違い

| 相違点 | AI TOP ATOM | NVIDIA DGX Spark |
|---|---|---|
| 筐体設計 | GIGABYTE / AORUS カスタム筐体 | NVIDIA リファレンス筐体 |
| 製品の位置付け | パーソナル AI スーパーコンピューター（デスクトップ / オフィス） | デスクトップ AI 開発リファレンスプラットフォーム |
| ストレージ | 最大 4TB（Gen5 / Gen4 版） | 最大 4TB |
| 付属品 | GIGABYTE 純正付属品 + AI TOP Utility | NVIDIA 純正付属品 |
| 保証 | 1 年 | 販売チャネルによる |

ALFAの互換性への影響：影響はないと見込まれます（テストはGX10のみで、他のGB10機種は個別にテストしていません）。USB コントローラー、kernel バージョン、ドライバーフレームワークは DGX Spark と完全に同じです。

### 2.4 USB Type-C 変換の必要性

AI TOP ATOM の USB ポートはすべて Type-C です。ALFA の全シリーズのアダプター（USB-C の AXML を除く）は USB Type-A のため、変換アダプターが必要です。AWUS036ACH / ACM / AX などの USB 3.x 機種がフルスピードで動作するよう、USB 3.2 Gen 2×2（20Gbps）対応の変換アダプターを選ぶことをおすすめします。

## 3. 現行ALFAアダプターの仕様とチップセットの分析

2026年9月時点で、ALFA Networkの現行USB無線LANアダプターのラインナップは以下のとおりです：

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
| デスクトップ AI 開発用の無線インターネット接続 | 9 機種すべて可（例：AWUS036ACM / ACHM） | すべて kernel 内蔵ドライバーで、挿すだけで使用可能 |
| 無線ペネトレーションテスト / セキュリティ研究 | AWUS036EACS / ACH / ACS | インジェクション実測 96–100%、WPA handshake をエンドツーエンドで取得可能。AXM / AXML は選ばないこと（インジェクション失敗） |
| Wi-Fi 6 + AP ホットスポット | AWUS036AX / AXER | 2x2、80MHz AP が実機で動作 |
| 6GHz 帯 | AWUS036AXML | 6GHz で WPA3 AP を構築できることを実機で確認。AXM は同じチップだが 6GHz は未テスト |
| 外付け WiFi が不要な場合 | — | AI TOP ATOM は Wi-Fi 7 を内蔵しており、一般的なインターネット接続には外付け不要 |

## 5. 環境要件

### 5.1 ハードウェア要件

| 項目 | 要件 |
|---|---|
| USB 変換アダプター | USB-C to USB-A 変換アダプターまたはケーブル（AXML を除く）、USB 3.2 Gen 2×2 対応を推奨 |
| 電源 | GIGABYTE 純正 240W USB-C 電源アダプター |

### 5.2 ソフトウェア要件

| 項目 | 要件 |
|---|---|
| DGX OS バージョン | 現行の任意のバージョン（kernel 6.x） |
| Kernel バージョン | kernel 6.17（実測 6.17.0-1014-nvidia）には 9 機種すべてのドライバーが内蔵されており、コンパイルツールは不要。最低バージョンは機種ごとに異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、それより古い場合のみコミュニティの DKMS ドライバーのインストールが必要 |
| 無線管理ツール | iw、network-manager（DGX OS にデフォルトでインストール済み） |

## 6. 互換性の判定

### ALFA 現行機種 × GIGABYTE AI TOP ATOM（GB10）互換性マトリックス

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

判定根拠：2026年11月16日～18日に ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）で実機テストを実施し、テスト対象は自社所有の Wi-Fi と自社所有のスマートフォンです。GIGABYTE AI TOP ATOM は同じ GB10 と NVIDIA kernel 系列を使用しているため同じ動作が見込まれますが、テストは GX10 のみで、GIGABYTE AI TOP ATOM は個別にテストしていません。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。

## 7. 超詳細 Step by Step 設定手順

GIGABYTE AI TOP ATOM のセットアップ手順は NVIDIA DGX Spark と同じと見込まれます（手順は GX10 で実機確認）。以下は簡易版です。詳細な手順は[ALFA無線LANアダプターはNVIDIA DGX Sparkに対応しているか](/ja/blog/alfa-nvidia-dgx-spark-compatibility/)の第7節を参照してください。

### 7.1 MediaTek チップセット機種（AWUS036ACM / ACHM / AXM / AXML）

- USB-C to USB-A 変換アダプター（AXML は直挿し可能）を使い、ALFA アダプターを AI TOP ATOM の USB-C データポートに挿します
- 検出の確認：`lsusb`
- インターフェースの確認：`ip link show`（wlx で始まるインターフェースが自動的に表示されるはずです）
- WiFi 接続：`nmcli dev wifi connect "SSID" password "パスワード"`

### 7.2 Realtek チップセット機種（AWUS036ACH / ACS / EACS / AX / AXER）

kernel 6.17（GX10 の実測バージョン）にはすべての Realtek 機種のドライバーが内蔵されているため、手順は MediaTek 機種と同じで、コンパイルは不要です（最低バージョン：EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）：

```bash
# 1. kernel バージョンを確認 (6.17 以上なら全 Realtek 機種のドライバーを内蔵. GX10 の実測は 6.17.0-1014-nvidia)
uname -r

# 2. アダプターを挿した後, ドライバーが自動ロードされたことを確認
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. WiFi 接続
nmcli dev wifi connect "SSID" password "パスワード"
```

各機種で自動ロードされるモジュール：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`、AX / AXER → `rtw89_8852bu`。`uname -r` がその機種の最低バージョンより古い（古いシステムの）場合に限り、コミュニティ保守の DKMS ドライバー（例：RTL8812AU 用の morrownr/8812au-20210820）のインストールが必要です。

### 7.3 モニターモード（ペネトレーションテスト）

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

## 8. よくあるエラーと対処法

| 症状 | 考えられる原因 | 対処法 |
|---|---|---|
| lsusb で ALFA アダプターが表示されない | USB-C 変換アダプターの不良 / 充電専用規格 | データ転送対応の USB 3.2 Gen 2×2 変換アダプターに交換。別の USB-C ポートを試す |
| MediaTek チップで wlan インターフェースが出ない | モジュールが自動ロードされない / ファームウェアの欠落 | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；`dmesg \| grep mt76` を確認 |
| Realtek アダプターを挿しても wlan インターフェースが出ない | kernel がその機種の最低バージョン（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）より古く、対応ドライバーが内蔵されていない | `uname -r` でバージョンを確認。kernel をアップグレードするか、古い kernel ではコミュニティの DKMS ドライバーをインストール |
| monitor／AP を繰り返し切り替えた後、何も受信できない | RX 停止（RX stall） | アダプターを抜き差しして USB を再列挙させる |
| EACS／AXML を挿し直した後に wlx インターフェースが出ない | Bluetooth＋Wi-Fi 複合デバイスの probe が停止 | 別の USB ポートに挿し直す |
| WiFi の速度が遅い | 変換アダプターが USB 2.0 のみ対応 | USB 3.2 Gen 2×2 変換アダプターに交換 |
| 内蔵 Wi-Fi 7 と外付けが競合する | ルーティングの競合 | `sudo nmcli radio wifi off` で内蔵 WiFi を無効にしてから外付けを使用 |
| 6GHz が使えない | Regulatory Domain の制限 | `sudo iw reg set US`；最新の法規を確認 |
| スリープ復帰後にアダプターが消える | USB の自動サスペンド | `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 既知の制限

- USB Type-C 変換が必要：AXML 以外のすべての ALFA アダプターに USB-C to USB-A 変換アダプターが必要です
- MT7921 機種のインジェクション失敗：AWUS036AXM / AXML は stock kernel 6.17 上でパケットインジェクションに失敗し、deauth や handshake の取得ができません。monitor、AP、WPA3 は使用可能です。主な原因は kernel 6.16 以降の mac80211 chanctx のリグレッションで、コミュニティのパッチ版ドライバーにもまだレート制限があります
- テスト範囲：ASUS GX10（kernel 6.17.0-1014-nvidia）でのみ実機テストしており、GIGABYTE AI TOP ATOM は個別にテストしていません（同じ動作が見込まれます）
- hcxdumptool は使用不可：2.4 GHz の EACS を除く全機種で `failed to arm` となるため、airodump-ng + aireplay-ng を使用してください
- 内蔵 Wi-Fi 7 と外付けが競合する可能性：AI TOP ATOM は Wi-Fi 7 + BT 5.4 を内蔵しています
- AP モードは手動設定が必要：DGX OS はデフォルトで開発環境として構成されています
- 6GHz の法規制限：Wi-Fi 6E の利用可否は規制地域によって異なります
- 古い kernel：Realtek 機種でコミュニティの DKMS ドライバーが必要なのは kernel がその機種の最低バージョン（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）より古いシステムのみで、その場合は kernel 更新のたびに再コンパイルが必要です
- GIGABYTE のハードウェアの違いは互換性に影響しない：筐体や冷却設計の違いは USB WiFi ドライバーの互換性に影響しません
- 保証と技術サポート：kernel 6.17 以上ではサードパーティー製ドライバーのインストールは不要です。古い kernel でコミュニティの DKMS ドライバーをインストールした場合、GIGABYTE の技術サポートはサードパーティー製ドライバーの問題を対象外とする可能性があります

反証条件：上記の判定は DGX OS（Ubuntu ベース、kernel 6.x）を前提としています。GIGABYTE が DGX OS 以外の独自ファームウェアをリリースした場合は、判定を再検証する必要があります。Bluetooth のバージョン（5.4）は出荷ロットの仕様に従うため、製品受け取り後に公式ページで再確認することをおすすめします。

## 10. 参考情報 URL

| 情報源 | 説明 | URL | 確認状態 | 確認日 |
|---|---|---|---|---|
| GIGABYTE AI TOP ATOM 公式製品ページ | AI TOP ATOM ハードウェア仕様（ATAGB10-9000） | https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 確認済み | 2026年9月3日 |
| GIGABYTE AI TOP ATOM 公式ページ（簡体字中国語のミラーサイト） | 製品の特徴と仕様 | https://www.gigabyte.cn/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 確認済み | 2026年9月3日 |
| GIGABYTE AI TOP ATOM レビュー（LinuxGizmos） | 第三者によるレビューと仕様確認（50.5mm） | https://linuxgizmos.com/gigabyte-ai-top-atom-introduces-nvidia-grace-blackwell-gb10-performance-for-the-desktop/ | ✅ 確認済み | 2026年9月3日 |
| NVIDIA DGX Spark 公式ページ | GB10 プラットフォーム情報 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 確認済み | 2026年9月3日 |
| morrownr/8812au GitHub | RTL8812AU Linux ドライバー | https://github.com/morrownr/8812au-20210820 | ✅ 確認済み | 2026年9月3日 |
| ALFA Network 製品一覧（Yopitek） | ALFA 現行製品仕様 | /ja/products/alfa/ | ✅ 確認済み | 2026年9月3日 |
| ALFA 9機種 ARM64 実機テスト総まとめ（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 実機テスト | https://yupitek.com/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 実機テスト | 2026年11月18日 |

関連記事：[ALFA無線LANアダプターはNVIDIA DGX Sparkに対応しているか](/ja/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA無線LANアダプターはASUS Ascent GX10に対応しているか](/ja/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA無線LANアダプターはALTOS BrainSphere GB10 F1に対応しているか](/ja/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA無線LANアダプターはMSI EdgeXpertに対応しているか](/ja/blog/alfa-msi-edgexpert-compatibility/)

免責事項：本記事の互換性判定は、2026年11月に ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）で行った実機テストを基準としています。GIGABYTE AI TOP ATOM は GX10 と同じ GB10 と NVIDIA kernel 系列を使用しているため同じ動作が見込まれますが、個別にはテストしていません。GX10 で実測した kernel 6.17 には ALFA 9 機種のドライバーがすべて内蔵されており（最低バージョンは機種ごとに異なる）、コミュニティの DKMS ドライバーが必要なのは kernel がその機種の最低バージョンより古い場合のみです。AI TOP ATOM は Wi-Fi 7 を内蔵しており、外付けの ALFA は主にペネトレーションテストや特定チップセットが必要な用途に使われます。監視とインジェクションは、自分が所有する、または許可を得たネットワークでのみ行ってください。
