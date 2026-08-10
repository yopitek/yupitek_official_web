---
title: 'Flipper Zero × ALFA WiFi アダプター：完全互換性ガイド'
description: 'Flipper Zero で ALFA USB WiFi アダプターのパケットインジェクションが可能か？結論から言うと、できません — その理由を解説します。Flipper One は AWUS036AXML とともにフルモニタモードとインジェクションをサポート。チップセット解析、ドライバ互換性、セットアップ手順付き完全ガイド。'
tags: ['flipper-zero', 'flipper-one', 'alfa-network', 'wifi-adapter', 'monitor-mode', 'packet-injection', 'kali-linux', 'pentesting', 'AWUS036AXML', 'wireless-security']
slug: 'flipper-alfa-compatibility'
categories: ['Technical']
featureimage: '/images/blog/flipper-alfa-compatibility.webp'
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Flipper ZeroはALFA USB無線アダプターに接続できますか？"
    answer: "できません。Flipper ZeroのSTM32WB55マイクロコントローラーはUSB deviceモードのみをサポートし、ハードウェア的にUSB hostとして外付けアダプターを駆動できません。"
  - question: "Flipper OneはどのALFAアダプターモデルをサポートしていますか？"
    answer: "Flipper One創業者はAWUS036AXMLを首选として特別にテストし、AWUS036ACMをベストコスパとしています。両者のドライバーはいずれもmainline Linuxカーネルに内蔵されています。"
  - question: "AWUS036AXMLがFlipper One首选アダプターなのはなぜですか？"
    answer: "AWUS036AXMLはMT7921AUNチップを採用し、mt7921uドライバーはLinux 5.18以降カーネルに内蔵され、完全な2.4/5/6 GHzトリバンドとモニターモードをサポートします。"
  - question: "Flipper Oneはいつ正式発売されますか？"
    answer: "Flipper Oneは現在開発者プレビュー段階で、正式発売時期と価格はクラウドファンディングで発表されます。詳細はflipper.netをフォローしてください。"
  - question: "Flipper ZeroのWiFi Dev BoardはALFAアダプターの代わりになりますか？"
    answer: "なりません。WiFi Dev Boardは2.4 GHzの基本機能のみをサポートし、USB hostがなく、範囲とインジェクションの信頼性は専用ALFAアダプターに遠く及びません。"
---

{{< alert "triangle-exclamation" >}}
**法的注意事項：** モニタモードとパケットインジェクションは、自分が所有するネットワーク、または明示的な書面による認証を受けたネットワークに対してのみ行ってください。無線通信の無許可傍受は、多くの管轄地域で違法です。本ガイドで説明するすべての技術は、**認可されたペネトレーションテスト、自己機器上でのセキュリティ研究、および教育目的** にのみ使用することを意図しています。
{{< /alert >}}


{{< tldr >}}
Flipper ZeroのSTM32WB55はUSB deviceモードのみをサポートし、いかなるALFAアダプターも駆動できません。Flipper OneはRK3576と完全なDebian Linuxを搭載し、AWUS036AXMLでトリバンドモニタリングとインジェクションをサポートします。
{{< /tldr >}}

Flipper Zero を所有している、または購入を検討している方で、ALFA Network の伝説的な USB WiFi アダプターを無線セキュリティテスティングに使ったことがあるなら、こんなことを思ったことはないでしょうか。

## 導入：ペンテスターが必ず抱える疑問

Flipper Zero を所有している、または購入を検討している方で、ALFA Network の伝説的な USB WiFi アダプターを無線セキュリティテスティングに使ったことがあるなら、こんなことを思ったことはないでしょうか。

**「ALFA アダプターを Flipper Zero に差せば、WPA2 ハンドシェイクのキャプチャを始められる？」**

短い答えは「No」です。しかし、もっと深い話があります。

**Flipper Zero はいかなる ALFA USB WiFi アダプターとも接続できません。** これはハードウェアの制限であり、ソフトウェアの問題ではありません。Flipper Zero 内部の STM32WB55 マイクロコントローラーが持つ USB コントローラーは**デバイスモード専用**で、WiFi アダプターのような外部周辺デバイスを駆動するためにホストとして動作することは、物理的に不可能です。

しかし Flipper Devices が全く新しい製品を発表しました：**Flipper One** です。8 GB RAM 積んだ Rockchip RK3576 上でフル Debian Linux を動作させるこのデバイスは、2 つの USB 3.1 ホストポートを備え、ALFA アダプターを直接接続して完全な無線セキュリティテストを行うことができます — 6 GHz Wi-Fi 6E アナリシスさえ含みます。実際、Flipper One の創設者 Pavel Zhovner 氏は、**ALFA AWUS036AXML** を公式テストアダプターとして製品発表で具体的に名指ししました。

この記事では、完全な互換性の全体像を説明します — 何が動き、何が動かないか、なぜか、そしてどうセットアップするか。

---

## Flipper Zero：なぜ ALFA アダプターを使えないのか

その制限を理解するには、Flipper Zero 内部を知る必要があります。

### ハードウェア仕様

| 項目 | 仕様 |
|------|------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **アーキテクチャ** | ARM Cortex-M4（アプリケーションコア）@ 64 MHz + ARM Cortex-M0+（無線コア）@ 32 MHz |
| **RAM** | 256 KB（両コアで共有） |
| **ストレージ** | 1 MB Flash + MicroSD |
| **OS** | FreeRTOS（リアルタイム OS） |
| **USB** | USB Type-C、USB 2.0 Full Speed（12 Mbps） |
| **USB モード** | **デバイス専用** — ホストまたは OTG 機能なし |

### USB の制限

STM32WB55 の USB コントローラーは**USB Full-Speed Device Controller**です。USB デバイスとして Flipper Zero をコンピューターに提示することは可能ですが（ファイル転送、ファームウェアアップデート、CLI インターフェースのため）、USB ホストとして動作することはできません。チップにホストコントローラーのハードウェアがありません — どのくらいのファームウェア改造をしても、この機能は追加できません。

ALFA USB WiFi アダプターを使用するには、デバイスが以下のものを必要とします：

1. **USB ホストコントローラーのハードウェア** — USB デバイスの列挙と通信のため
2. **WiFi ドライバーサポート付きの Linux カーネル** — `mt7921u`、`mt76`、`rtw88` などのドライバーをロードするため
3. **十分な電力供給** — ALFA アダプターは通常 500 mA から 900 mA（5V）を消費

Flipper Zero はこの 3 つの要件すべてを満たしていません：

- ❌ USB ホストコントローラーなし（ハードウェア）
- ❌ FreeRTOS を動作 — Linux でないため、カーネルドライバーフレームワークが存在しない
- ⚠️ GPIO 5V 出力は全ピン合計で 1.2A に制限され、手動有効化が必要

> **結論：** いかなる ALFA USB WiFi アダプターを Flipper Zero に接続することは**物理的に不可能**です。これはソフトウェア、ファームウェアアップデート、拡張ボードで回避できる制限ではありません — 半導体チップに焼き付けられています。

---

## Flipper Zero + WiFi Dev Board：限定的な代替案

Flipper Devices は公式の **WiFi Dev Board** を販売しています。これは **ESP32-S2** マイクロコントローラーを基盤としており、Flipper Zero の GPIO ヘッダーに差込むことで基本的な 2.4 GHz WiFi 機能を提供します — ただし、USB ホストの状況を**変えるものではありません**。

| 項目 | 対応状況 |
|------|----------|
| **WiFi チップ** | ESP32-S2（Xtensa LX7 シングルコア、240 MHz） |
| **周波数** | 2.4 GHz のみ、802.11 b/g/n |
| **USB ホスト** | ❌ WiFi Dev Board は USB ホストを公開しない — ESP32-S2 は GPIO を介して接続されており、USB ではない |
| **ファームウェア** | ESP32 Marauder（コミュニティ開発） |

**ESP32 Marauder ファームウェア**をインストールすると、WiFi Dev Board は以下のことができます：

- ✅ 認証解除攻撃（2.4 GHz のみ）
- ✅ PMKID キャプチャ（2.4 GHz のみ）
- ✅ アクセスポイントスキャンと SSID 放送
- ✅ 基本的なパケットスニフ（2.4 GHz のみ）

**できないこと：**

- ❌ 外部 ALFA USB アダプターの使用（USB ホストなし）
- ❌ 5 GHz または 6 GHz 帯での動作
- ❌ 専用 ALFA アダプターの範囲やインジェクション信頼性に追いつくこと
- ❌ aircrack-ng、Kismet、Wireshark などの Linux ベースツールの実行

> **Flipper Zero しか持っておらず、基本的な 2.4 GHz テスティングが必要であれば**、ESP32 Marauder 付きの WiFi Dev Board は機能する — しかし深刻に制限された — 回避策です。それ以上のことを求める場合は、別のハードウェアが必要です。

---

## Flipper One：ALFA が待っていたプラットフォーム

**2026 年 5 月 21 日**、Flipper Devices 創設者 Pavel Zhovner 氏は *"Flipper One — We Need Your Help"* というタイトルのブログ記事を公開し、全く新しい製品を発表しました。Flipper One は Flipper Zero のアップグレードではありません — プロトコルスタックの異なるレイヤーのために設計された、全く異なるクラスのデバイスです。

> *"Flipper Zero はレイヤー 0 — オフラインポイントツーポイントのアクセス制御：NFC、RFID、Sub-GHz、赤外線。Flipper One はレイヤー 1 — IP 接続：Wi-Fi、Ethernet、5G、衛星。お互いを置き換えるものではありません。"*
> — Pavel Zhovner、flipper.net

{{< alert "circle-info" >}}
**利用状況のお知らせ：** Flipper One は現在**開発者プレビュー**中です。一般提供日、価格、地域配布はクラウドファンディング経由で発表される予定です。[flipper.net](https://flipper.net) と [Flipper One Developer Portal](https://docs.flipper.net/one) をフォローしてアップデートを受け取ってください。
{{< /alert >}}

### ハードウェア仕様

| 項目 | 仕様 |
|------|------|
| **CPU** | Rockchip RK3576：4× Cortex-A72 + 4× Cortex-A53、最大 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3（OpenGL ES 3.2、Vulkan 1.2） |
| **NPU** | INT8 で 6 TOPS（ローカル LLM を実行可能） |
| **コプロセッサー** | Raspberry Pi RP2350B（デュアル M33 + デュアル RISC-V、表示/ボタン/電源用） |
| **RAM** | 8 GB LPDDR5 |
| **ストレージ** | 64 GB UFS 2.2 + MicroSD |
| **OS** | Debian 13 (Trixie) — Flipper Devices はメインライン Linux カーネル 7.0 をターゲットし、out-of-tree パッチ依存なしで提供すると述べている |
| **USB ホスト** | USB-C2 + USB-A、両方 USB 3.1（5 Gbps）、両方ホスト対応 |
| **内蔵 WiFi** | MT7921AUN 経由の Wi-Fi 6E（2.4/5/6 GHz、2×2 MIMO） |
| **Ethernet** | 2× RJ45 Gigabit（inline/MitM スニフ対応） |
| **M.2 拡張** | Key-B：PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM |

### Flipper One が ALFA アダプターで動作する理由

Flipper Zero とは異なり、Flipper One は 3 つの要件すべてを満たしています：

1. ✅ **USB 3.1 ホストコントローラー**：外部デバイスを列挙・給電できるホスト対応 USB ポート ×2
2. ✅ **フル Debian Linux**：`mt7921u`、`mt76`、`rtw88` のインカーネルドライバーサポート付き標準 Linux カーネル
3. ✅ **十分な電力**：USB ポートは標準バス電力を供給可能；GPIO は 5V @ 2A および 3.3V @ 2A と eFuse 保護付き

USB 3.1 の帯域幅（5 Gbps）は十分 — どんなに最速の ALFA アダプター（AWUS036AXML、AXE3000）でも USB 3.0 の実 throughput の約 1.2 Gbps に制限されます。

### ソフトウェア環境

Flipper One は標準的な Debian 環境を動作するため、`apt` で直接無線セキュリティツールをインストールできます：

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

Flipper One では **Flipper OS Profiles** も導入されました — スナップショットベースのシステムで、クリーンで分離された環境を作成できます。すべての無線ツールを専用「Pentest」プロフィールに格納し、通常使用時はクリーンプロフィールに戻すことができます。

---

## Flipper One 向け推奨 ALFA アダプター

すべての ALFA アダプターが無線セキュリティテスティングで同じように動作するわけではありません。重要な要素は**チップセット**、**ドライバーの成熟度**、**インカーネルサポート**（DKMS コンパイル不要）です。

### ⭐⭐⭐⭐⭐ トップピック：AWUS036AXML（Wi-Fi 6E）

| 仕様 | 詳細 |
|------|------|
| **チップセット** | MediaTek MT7921AUN |
| **帯域** | 2.4 / 5 / 6 GHz（Wi-Fi 6E） |
| **最大速度** | AXE3000（理論値）、約 1.2 Gbps（実測） |
| **ドライバー** | `mt7921u` — Linux 5.18 からインカーネル |
| **DKMS 必要** | ❌ なし |
| **アンテナ** | デュアル RP-SMA（交換可能）+ Bluetooth 5.2 |

> **なぜ最高の選択か：** Flipper One の創設者が特別にテストしたアダプターです。`mt7921u` ドライバーはメインラインカーネルにあり、ベンダーパッチ不要です。3 つの WiFi 帯域（2.4/5/6 GHz）すべてをサポートするため、Wi-Fi 6E セキュリティ評価で将来に対応可能です。モニタモードとパケットインジェクションは安定して動作し、十分にテストされています。

### ⭐⭐⭐⭐⭐ ベストバリュー：AWUS036ACM（Wi-Fi 5 AC1200）

| 仕様 | 詳細 |
|------|------|
| **チップセット** | MediaTek MT7612U |
| **帯域** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速度** | AC1200（300 + 867 Mbps） |
| **ドライバー** | `mt76` — Linux 4.19 からインカーネル |
| **DKMS 必要** | ❌ なし |
| **アンテナ** | デュアル 5 dBi RP-SMA（交換可能） |

> **なぜベストバリューか：** MT7612U チップセットはペンテスタコミュニティでテスト済みです。`mt76` ドライバーはカーネルに何年も存在し、特に安定しています。モニタモードとインジェクションはカーネル 6.5 以上で完璧に動作します。ACM より低価格で、2.4/5 GHz テスティングにおいて最高の価格対性能比を提供します。

### ⭐⭐⭐⭐ 軽量ピック：AWUS036ACHM（Wi-Fi 5 AC433）

| 仕様 | 詳細 |
|------|------|
| **チップセット** | MediaTek MT7610U |
| **帯域** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速度** | AC433（理論値） |
| **ドライバー** | `mt76` — Linux 4.19 からインカーネル |
| **DKMS 必要** | ❌ なし |
| **アンテナ** | シングル高出力 RP-SMA（交換可能） |

> **なぜ軽量か：** 最もポータブルなオプション — USB 2.0、シングルアンテナ、最小電力消費。ACM と同じ `mt76` ドライバーファミリーを使用。フィールドワークでサイズと電力効率が raw スループットより重要場合に最適。**注意：** ARM64 プラットフォーム（RK3576 を含む）では、`airodump-ng` と `aireplay-ng` を同時に実行すると既知のインターフェースドロップバグ（morrownr issue #379）が発生する可能性があります。注意して使用してください。

### ⭐⭐⭐ オプション：AWUS036ACH（Wi-Fi 5 AC1200、RTL8812AU）

| 仕様 | 詳細 |
|------|------|
| **チップセット** | Realtek RTL8812AU |
| **帯域** | 2.4 / 5 GHz（Wi-Fi 5） |
| **最大速度** | AC1200（300 + 867 Mbps） |
| **ドライバー** | `rtw88` — Flipper One の予定カーネルでインカーネル；古いシステムでは DKMS 必要 |
| **DKMS 必要** | ❌ Flipper One では不要 / ⚠️ 古いカーネルでは [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS 必要 |
| **アンテナ** | デュアル 6 dBi RP-SMA（高出力） |

> **なぜオプションか：** RTL8812AU チップセットにはペンテスタでの長い歴史があります。Flipper One の予定カーネルで DKMS モジュール追加なしでサポートされる予定。古いシステムでは aircrack-ng DKMS ドライバーが利用可能。高出力 6 dBi アンテナは優れた範囲を提供しますが、MediaTek 搭載アダプターの方がより成熟したインカーネルドライバーサポートを提供するため、一般的に推奨されます。

### ⚠️ ペンテスティングに非推奨

以下の ALFA モデルは Realtek チップセットを使用し、モニタモードとパケットインジェクションに未成熟または不安定な Linux ドライバーを備えています。**Flipper One の無線セキュリティ作業には避けてください：**

| モデル | チップセット | 問題点 |
|--------|-------------|--------|
| AWUS036AX | RTL8832BU | Wi-Fi 6 チップセット、2026 年現在でもドライバーサポートが進展中 |
| AWUS036AXER | RTL8832BU | AWUS036AX と同じチップセットの問題 |
| AWUS036ACS | RTL8811AU | モニタモードが制限され、インジェクションが不安定 |
| AWUS036EACS | RTL8811CU | モニタモードが制限され、インジェクションが不安定 |

---

## セットアップガイド：Flipper One + ALFA AWUS036AXML

このガイドでは、アダプターが USB ホストポートに物理的に接続された Debian Linux を実行する Flipper One を前提としています。

### ステップ 1：アダプターが認識されているか確認

```bash
# USB デバイスの列挙を確認
lsusb
# 期待される出力（例）：
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# 無線インターフェースをリスト
iw dev
# 期待される出力：wlan0（内蔵 WiFi が wlan0 を占有する場合は wlan1）

# 代替チェック
ip link show
```

### ステップ 2：ドライバーがロードされているか確認

```bash
# AWUS036AXML / AWUS036AXM（MT7921AUN）の場合：
lsmod | grep mt7921u

# AWUS036ACM / AWUS036ACHM（MT7612U / MT7610U）の場合：
lsmod | grep mt76

# AWUS036ACH（RTL8812AU）の場合：
lsmod | grep rtw88

# カーネルバージョンを確認（MT7921AUN の最適なサポートには 6.12+）：
uname -r
```

ドライバーモジュールがリストされる場合は、ロード済みで準備完了です。追加インストールは不要 — これらすべてインカーネルドライバーです。

### ステップ 3：モニタモードを有効化

```bash
# 競合プロセスを殺す（NetworkManager、wpa_supplicant など）
# 注意：これにより Flipper One の内蔵 WiFi も切断されます。
# 通常のネットワーク接続を disruption しないよう、
# ペンテスティングには専用 Flipper OS Profile を使用してください。
sudo airmon-ng check kill

# アダプターでモニタモードを開始
sudo airmon-ng start wlan0
# インターフェース名が wlan0mon に変更される

# モニタモードがアクティブか確認
iw dev wlan0mon info
# type monitor と表示されるはず
```

手動メソッド（airmon-ng を使わない場合）：

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### ステップ 4：パケットインジェクションをテスト

```bash
# インジェクション能力をテスト
sudo aireplay-ng --test wlan0mon
# "Injection is working!" を確認

# 基本的なスキャンを実行
sudo airodump-ng wlan0mon

# 全対応帯域をスキャン（AWUS036AXML のみ）
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz（aircrack-ng 1.7+）

# 特定のチャネルを対象に
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### ステップ 5：WPA2 ハンドシェイクをキャプチャ

```bash
# ターミナル 1：対象チャネルでキャプチャ開始
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# ターミナル 2：再接続を強制するために認証解除を送信
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# ターミナル 1 でハンドシェイクキャプチャを確認：
# "WPA handshake: AA:BB:CC:DD:EE:FF" が表示される
```

### ステップ 6：通常操作に戻る

```bash
# モニタモードを停止し、マネージドモードを復元
sudo airmon-ng stop wlan0mon

# ネットワークサービス再起動
sudo systemctl restart NetworkManager
```

### アーキテクチャ概要

以下のダイアグラムは、Flipper One と ALFA アダプターを用いた完全な無線ペンテストアーキテクチャを示しています：

![Flipper One + ALFA WiFi アダプター ペンテストアーキテクチャ](diagram/flipper-alfa-topology.svg)

*トポロジー：Flipper One プラットフォーム → ALFA USB アダプター → ペンテストツールチェーン → 無線能力*

---

## Flipper Zero vs. Flipper One：並列比較

| 機能 | Flipper Zero | Flipper One |
|------|:-----------:|:----------:|
| **OS** | FreeRTOS | Debian 13 (Trixie) |
| **CPU** | STM32WB55（Cortex-M4、64 MHz） | RK3576（8 コア ARM、2.2 GHz） |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **ストレージ** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB ホスト** | ❌ デバイス専用 | ✅ USB-C2 + USB-A（USB 3.1） |
| **ALFA アダプター対応** | ❌ | ✅ |
| **内蔵 WiFi** | ❌（BLE のみ） | ✅ Wi-Fi 6E（MT7921AUN） |
| **5 GHz / 6 GHz WiFi** | ❌ | ✅ |
| **Gigabit Ethernet** | ❌ | ✅ 2× RJ45 |
| **モニタモード** | ❌（ネイティブ） | ✅ |
| **パケットインジェクション** | ❌（ネイティブ） | ✅ |
| **M.2 拡張** | ❌ | ✅ Key-B（PCIe / USB 3.1 / SATA） |
| **価格** | 約 $169 USD（量産中） | 開発者プレビュー（クラウドファンディング価格未定） |

---


---

{{< faq >}}

## 結論：正しいツールを正しい目的に

ALFA WiFi アダプターを無線セキュリティテスティングに使いたいなら、**Flipper Zero は間違ったプラットフォーム**です — それは Flipper Zero のせいかではありません。Flipper Zero は異なる目的のために設計されました：オフラインのアクセスコントロールテスト（NFC、RFID、Sub-GHz、赤外線）です。それらのタスクでは非常に優秀ですが、USB ホスト機能はその設計には含まれていません。

**ALFA アダプターを用いた Monitor Mode と Packet Injection** という特定のユースケースには、2 つの道があります：

| パス | プラットフォーム | ALFA アダプター | 能力 |
|------|-----------------|----------------|------|
| **最適** | Flipper One | AWUS036AXML（MT7921AUN） | 完全な 2.4/5/6 GHz、インカーネルドライバー、公式サポート |
| **ベストバリュー** | Flipper One | AWUS036ACM（MT7612U） | 完全な 2.4/5 GHz、インカーネルドライバー、実績ある安定性 |
| **回避策** | Flipper Zero + WiFi Dev Board | なし（ESP32-S2 内蔵） | 2.4 GHz のみ、範囲が限定、基本的な能力 |

**Flipper One は飛躍的な進歩**を表しています — USB 3.1 ホスト能力を持つ Debian Linux 環境のフルパワーを、ポータブルで目的特化のハードウェアプラットフォームにもたらします。ALFA AWUS036AXML（Flipper One の創設者が特別にテストしたアダプター）と組み合わせると、ポケットに入る完全な無線セキュリティ評価ツールキットが得られます。

---

### 購入先

推奨されるすべての ALFA アダプターは Yupitek で購入可能です — 公式 ALFA Network 販売店です。全カタログを見るかモデルを比較：

- [ALFA USB WiFi アダプター — 全カタログ](https://yupitek.com/ja/products/alfa/) — 全モデルの仕様と価格
- [ALFA 製品比較](/ja/alfa_compare/) — チップセット、帯域、ドライバの並列比較

### さらなる読み物

- [Flipper One 公式ブログ記事](https://blog.flipper.net/flipper-one-we-need-your-help/) — Pavel Zhovner、2026 年 5 月
- [Flipper One Developer Portal](https://docs.flipper.net/one) — 技術仕様とドキュメント
- [パケットインジェクションとは？](/ja/blog/packet-injection-guide/) — パケットインジェクション入門ガイド
- [AWUS036AXML WiFi 6E レビュー](/ja/blog/awus036axml-wifi-6e-review/) — 主力アダプターの詳細レビュー
- [ALFA 製品比較](/ja/alfa_compare/) — すべての ALFA モデルの並列仕様

---

*Flipper One と ALFA アダプターの互換性に関する販売前の質問は、Yupitek サポート support@yupitek.com または +886-2-87325338 までお問い合わせください。*

---

## 参考文献

1. [Flipper One公式ブログ — Pavel Zhovner製品アナウンス](https://blog.flipper.net/flipper-one-we-need-your-help/)
2. [Flipper One Developer Portal — 技術仕様とドキュメント](https://docs.flipper.net/one)
3. [Flipper Zero公式ウェブサイト](https://flipperzero.one/)
4. [aircrack-ng — 無線セキュリティツールスイート公式ウェブサイト](https://www.aircrack-ng.org/)
5. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
