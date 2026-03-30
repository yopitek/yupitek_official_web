---
title: "ALFA AWUS036ACM：Raspberry Pi で IBSS アドホックと 802.11s メッシュネットワークを構築する（MT7612U）"
description: "ALFA AWUS036ACM（MT7612U）は、Raspberry Pi 上で IBSS アドホックと 802.11s メッシュネットワークを完全にサポートする唯一の現行 ALFA USB WiFi アダプターです。ドライバーのインストール不要で、すぐに使えます。設定手順を詳しく解説します。"
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "アドホック", "802.11s", "メッシュネットワーク", "Linux", "無線LAN"]
---

# ALFA AWUS036ACM：Raspberry Pi で IBSS アドホックと 802.11s メッシュネットワークを構築する（MT7612U）

ルーターなしで Raspberry Pi ノード間に WiFi ネットワークを構築しようとしたことがある方、あるいは中間ホップを経由して自動的にトラフィックをルーティングする自己修復型のワイヤレスメッシュを作ろうとしたことがある方なら、ほとんどの USB WiFi アダプターではそれができないことをすぐに気づかれたはずです。カーネルドライバーが必要なモードを公開していないのです。

**MediaTek MT7612U** チップセットを搭載した **ALFA AWUS036ACM** は、その例外です。インカーネルの `mt76` ドライバーは Linux mac80211 インターフェースを完全に実装しているため、Raspberry Pi 上で **IBSS（アドホック）** モードと **802.11s メッシュポイント** モードの両方をネイティブにサポートしています。ドライバーのコンパイルは不要で、すぐに使い始められます。

このガイドでは、両モードの動作原理を詳しく説明し、ステップバイステップの設定手順を提供し、それぞれのモードをいつ選択すべきかを解説します。

---

## 目次

1. [IBSS と 802.11s メッシュとは何か、そしてなぜ重要なのか？](#1-what-are-ibss-and-80211s-mesh)
2. [ALFA AWUS036ACM ハードウェア仕様](#2-alfa-awus036acm-hardware-specifications)
3. [Raspberry Pi 上の MT7612U ドライバー](#3-the-mt7612u-driver-on-raspberry-pi)
4. [モード 1：IBSS アドホックネットワーク](#4-mode-1-ibss-ad-hoc-networking)
5. [モード 2：802.11s メッシュポイントネットワーク](#5-mode-2-80211s-mesh-point-networking)
6. [実際の使用例](#6-real-world-use-cases)
7. [AWUS036ACM がこの用途で唯一の ALFA の選択肢である理由](#7-why-the-awus036acm-is-the-only-alfa-choice-for-this)
8. [よくある質問とトラブルシューティング](#8-faq-and-troubleshooting)
9. [購入先](#9-where-to-buy)

---

## 1. IBSS と 802.11s メッシュとは何か？

### IBSS — Independent Basic Service Set（アドホックモード）

ラップトップをご自宅の WiFi ルーターに接続する場合、アダプターは **マネージド（ステーション）** モードで動作しています。つまり、1 つの中央アクセスポイントと通信しています。IBSS はその逆です。**中央インフラを持たないピアツーピアの無線ネットワーク**を定義した IEEE 802.11 の仕様です。

IBSS モードでは：

- デバイスは AP やルーターを介さずに**直接**通信します
- 同じ SSID とチャンネルに設定された任意の 2 台のデバイスがデータを交換できます
- ネットワークは自己完結型であり、インターネット接続は不要です
- IP アドレスは静的に割り当てます（または自身で実行するシンプルな DHCP デーモンを使用します）
- 最初に IBSS に「参加」したデバイスが BSSID（セル識別子）の起点になります

少数の Pi ノード間に即席のプライベート無線 LAN を構築するイメージです。2 ノードのパイプライン、3 ノードのセンサークラスター、あるいは現場に展開するポータブル通信キットなどに活用できます。

**IBSS の制限事項：**
- すべてのノードが互いの直接無線到達範囲内にいる必要があります。自動的なマルチホップ転送はありません
- IBSS モードでは標準の WPA2 暗号化は利用できません（WEP は技術的には可能ですが推奨しません。ほとんどの展開ではアプリケーション層のセキュリティを使用します）
- 実用的なノード数は 3〜5 台が上限で、それを超えるとパフォーマンスが低下します

### 802.11s メッシュポイント — スケーラブルな代替手段

802.11s は、**真のワイヤレスメッシュネットワーク**を定義する独立した IEEE 修正仕様です。IBSS とは異なり、802.11s メッシュは：

- 隣接するノードを自動的に発見し、ルーティングテーブルを構築します
- 直接到達範囲外のノードに届かせるため、中間ホップを経由してトラフィックを転送します
- ノードが消えた場合に自己修復します。他のパスが自動的に使用されます
- デフォルトでパス選択に **Hybrid Wireless Mesh Protocol（HWMP）** を使用します

```
例：4 ノードメッシュ

  [Pi A] ──── [Pi B] ──── [Pi C]
                │
              [Pi D]

Pi A は Pi B を経由して Pi C に自動的に到達できます。
Pi A は Pi B を経由して Pi D に自動的に到達できます。
Pi B が故障した場合、メッシュは代替ルートを探します。
```

ノードが 3〜4 台以上ある場合、ノードが広いエリアに分散している場合、あるいは手動管理なしにネットワークを冗長化したい場合には 802.11s が適切な選択肢です。

### 動作するアダプターを見つけるのが難しい理由

上記の 2 つのモードは、WiFi ドライバーが Linux の **mac80211** ソフトウェア MAC 層——カーネルの公式 802.11 スタック——の上に構築されている必要があります。mac80211 準拠のドライバーだけが、IBSS とメッシュポイントを使用可能なインターフェース型として公開します。

人気のある USB WiFi アダプターの多くは、**アウトオブカーネルドライバー**を使用しており、独自の簡易無線スタックを実装して IBSS とメッシュのサポートを意図的に省略しています。新しいチップセット向けのインカーネルドライバーでさえ、これらのモードを公開していないものがあります。

MT7612U は、両方について明確で疑いようのない **YES** が得られる数少ないチップセットの 1 つです。

---

## 2. ALFA AWUS036ACM ハードウェア仕様

AWUS036ACM は ALFA Network の AC1200 デュアルバンド USB 3.0 アダプターで、Linux パワーユーザーと組み込み開発者向けに設計されています。

![ALFA AWUS036ACM](/images/products/alfa/awus036acm.png)

### 主要仕様

| パラメーター | 値 |
|---|---|
| **チップセット** | MediaTek MT7612U |
| **WiFi 規格** | IEEE 802.11 a/b/g/n/ac（WiFi 5） |
| **周波数帯域** | 2.4 GHz（2.412〜2.472 GHz）+ 5 GHz（5.15〜5.825 GHz） |
| **チャンネル幅** | 20 / 40 / 80 MHz |
| **最大速度（5 GHz）** | 867 Mbps（802.11ac） |
| **最大速度（2.4 GHz）** | 300 Mbps（802.11n） |
| **合計速度** | AC1200（867 + 300 Mbps） |
| **USB インターフェース** | USB 3.0 Type-A（USB 2.0 との後方互換性あり） |
| **アンテナ** | RP-SMA メスコネクター × 2、5 dBi デュアルバンド ダイポール（着脱式）× 2 |
| **USB VID/PID** | 0e8d:7612 |
| **LED インジケーター** | 電源 + WLAN アクティビティ |
| **付属品** | USB 3.0 延長ケーブル、ドライバー CD（Windows 用） |
| **寸法** | 62 × 85.3 × 24 mm |
| **重量** | 60 g |
| **原産国** | 台湾（Alfa Network Inc.） |

### 送信電力

| 規格 | TX 電力 |
|---|---|
| 802.11a | 20 dBm |
| 802.11b | 23 dBm |
| 802.11g | 23 dBm |
| 802.11n | 21 dBm |
| 802.11ac | 20 dBm |

### 受信感度

| 規格 | 感度 |
|---|---|
| 802.11a | −92 dBm |
| 802.11b | −97 dBm |
| 802.11g | −90 dBm |
| 802.11n | −90 dBm |
| 802.11ac | −86 dBm |

### サポートされているインターフェースモード（全一覧）

これが重要な機能表です。MT7612U / mt76x2u ドライバーは、主要な mac80211 インターフェースモードをすべてサポートしています：

| モード | サポート | 説明 |
|---|---|---|
| **IBSS** | ✅ 対応 | AP 不要のアドホックピアツーピア |
| **マネージド（ステーション）** | ✅ 対応 | 標準クライアントモード |
| **AP** | ✅ 対応 | ソフトウェアアクセスポイント（hostapd） |
| **AP/VLAN** | ✅ 対応 | AP 上の仮想 LAN |
| **モニター** | ✅ 対応 | パッシブキャプチャ + パケットインジェクション |
| **メッシュポイント** | ✅ 対応 | 802.11s マルチホップメッシュネットワーク |
| **P2P-クライアント** | ✅ 対応 | Wi-Fi ダイレクトクライアント |
| **P2P-GO** | ✅ 対応 | Wi-Fi ダイレクトグループオーナー |

### 無線セキュリティ
WPA2 / WPA / WEP / WPA-PSK / 802.1X / 64〜128 ビット WEP

### 対応オペレーティングシステム

| OS | 状態 | 備考 |
|---|---|---|
| Raspberry Pi OS（2020 年以降） | ✅ プラグ＆プレイ | ドライバーインストール不要 |
| Ubuntu 20.04 LTS 以降 | ✅ プラグ＆プレイ | インカーネル mt76 ドライバー |
| Kali Linux 2019.3 以降 | ✅ プラグ＆プレイ | モニター + インジェクション + VIF フル対応 |
| Debian 11 以降 | ✅ 動作確認済み | firmware-misc-nonfree が必要な場合あり |
| Arch Linux | ✅ プラグ＆プレイ | 4.19 以降でインカーネル対応 |
| Windows 10/11 | ✅ 対応 | Alfa 公式サイトの公式ドライバー |
| Android NetHunter | ✅ 対応 | OTG USB |
| macOS 11 以降 / Apple Silicon | ❌ 非対応 | macOS 10.7〜10.12 のみ |

---

## 3. Raspberry Pi 上の MT7612U ドライバー

### ドライバー：mt76x2u（mt76 ファミリーの一部）

MediaTek MT7612U は `mt76x2u` ドライバーによって処理されます。このドライバーは、MediaTek が管理し Linux カーネルメインラインに統合された広範な **mt76** ドライバープロジェクトの一部です。

**重要な数字：**
- インカーネル化されたバージョン：**Linux カーネル 4.19**（2018 年 10 月リリース）
- Raspberry Pi OS のカーネルバージョン：**5.15 以降**（Pi 4/5）および **5.10 以降**（Pi 3B+）——いずれも 4.19 を大幅に上回っています
- **最新の Raspberry Pi OS ではインストール手順は一切不要です**

### ドライバーの読み込みを確認する方法

AWUS036ACM を接続した後、次のコマンドを実行します：

```bash
lsusb
```

次のエントリを探します：
```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

次に、ドライバーがアクティブであることを確認します：

```bash
dmesg | grep mt76
```

期待される出力（要約）：
```
mt76x2u 1-1.4:1.0: ASIC revision: 76120044
mt76x2u 1-1.4:1.0: Firmware Version: 0.1
mt76x2u 1-1.4:1.0: loaded firmware from mediatek/mt7662u_rom_patch.bin
```

新しいインターフェースを一覧表示します：
```bash
iw dev
```

新しいインターフェース（Pi の内蔵 WiFi が `wlan0` の場合、通常 `wlan1`）が表示されるはずです：
```
phy#1
    Interface wlan1
        ifindex 4
        wdev 0x100000001
        addr xx:xx:xx:xx:xx:xx
        type managed
        channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
```

アダプターの機能一覧全体を確認します：
```bash
iw phy phy1 info | grep -A 20 "Supported interface modes"
```

次のように表示されます：
```
Supported interface modes:
     * IBSS
     * managed
     * AP
     * AP/VLAN
     * monitor
     * mesh point
     * P2P-client
     * P2P-GO
```

### ドライバーアーキテクチャが重要な理由

AWUS036ACM のドライバースタックは次のようになっています：

```
Your Application (ping, iperf3, batman-adv...)
        ↓
nl80211 / cfg80211  ← kernel WiFi configuration API
        ↓
mac80211            ← IEEE 802.11 software MAC layer
        ↓
mt76x2u             ← MT7612U USB hardware driver
        ↓
MediaTek MT7612U    ← Physical chip (2×2 MIMO, USB 3.0)
```

**mac80211** は、完全な 802.11 ステートマシンの Linux カーネル実装です。ビーコン管理、フレーム構築、省電力、IBSS ピア探索、メッシュパスルーティングを処理します。mac80211 の上に構築されたドライバーは、これらの機能をすべて自動的に継承します。

mac80211 をバイパスするドライバー（たとえば Realtek のアウトオブカーネルドライバー）は、自社が公開することを選択したモードのみを実装します。IBSS とメッシュポイントはほぼ常に省略されています。

---

## 4. モード 1：IBSS アドホックネットワーク

### IBSS の動作原理

IBSS モードでは、各アダプターが独自の 802.11 フレームを管理します。2 つのアダプターが同じ SSID とチャンネルに設定されると：

1. 最初のデバイスがランダムな **BSSID**（IBSS セル ID）を生成します
2. 選択したチャンネルでビーコンをブロードキャストします
3. 2 台目のデバイスがスキャンし、ビーコンを見つけて、セルに**参加**します
4. 両デバイスは AP を介さずに直接データフレームを交換できるようになります

OS の観点から見ると、IBSS インターフェースは通常の Ethernet インターフェースと同様に動作します。IP を割り当て、通常通り TCP/IP を使用します。

### IBSS とマネージドモードの比較

| 機能 | IBSS（アドホック） | マネージド（ステーション） |
|---|---|---|
| 中央 AP が必要か？ | ❌ 不要 | ✅ 必要 |
| インターネットが必要か？ | ❌ 不要 | 通常は必要 |
| 設定の複雑さ | 低い | 非常に低い |
| 実用的な最大ノード数 | 3〜5 台 | 無制限（AP 経由） |
| WPA2 サポート | ❌ なし | ✅ あり |
| 最適な用途 | 孤立した Pi クラスター、現場キット | 家庭/オフィスネットワーク |

### ステップバイステップ：2 台の Raspberry Pi による IBSS ネットワーク

この例では、2 台の Raspberry Pi 間に 5 GHz の直接リンクを作成します。デプロイ環境に合わせて IP アドレスと SSID を変更してください。

**両方のノードで — 正しいインターフェースを特定します：**

```bash
iw dev
```

AWUS036ACM は通常（Pi の内蔵 WiFi が `wlan0` の場合）`wlan1` として表示されます。`lsusb` と照合して MAC アドレスで確認してください。以下のすべてのコマンドで、`wlan1` を実際のインターフェース名に置き換えてください。

---

#### ノード 1（Pi #1 — IP: 192.168.88.1）

**ステップ 1 — NetworkManager / wpa_supplicant の干渉を停止します：**

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```

**ステップ 2 — インターフェースをダウンさせます：**

```bash
sudo ip link set wlan1 down
```

**ステップ 3 — インターフェースを IBSS モードに設定します：**

```bash
sudo iw dev wlan1 set type ibss
```

**ステップ 4 — インターフェースを再度アップします：**

```bash
sudo ip link set wlan1 up
```

**ステップ 5 — 5 GHz チャンネル 36 で IBSS セルに参加（または作成）します：**

```bash
sudo iw dev wlan1 ibss join RaspberryMesh 5180
```

> **周波数の参照：**
> - 5180 MHz = 5 GHz チャンネル 36（一般的な屋内チャンネル、良好なスループット）
> - 5200 MHz = 5 GHz チャンネル 40
> - 2412 MHz = 2.4 GHz チャンネル 1（より広い範囲、低速）
> - 2437 MHz = 2.4 GHz チャンネル 6

**ステップ 6 — 静的 IP アドレスを割り当てます：**

```bash
sudo ip addr add 192.168.88.1/24 dev wlan1
```

---

#### ノード 2（Pi #2 — IP: 192.168.88.2）

IP アドレスのみを変更して、同じコマンドを実行します：

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
sudo ip link set wlan1 down
sudo iw dev wlan1 set type ibss
sudo ip link set wlan1 up
sudo iw dev wlan1 ibss join RaspberryMesh 5180
sudo ip addr add 192.168.88.2/24 dev wlan1
```

---

#### リンクを確認する

ノード 1 で：
```bash
iw dev wlan1 link
```

期待される出力（ノード 2 が参加した後）：
```
Connected to xx:xx:xx:xx:xx:xx (on wlan1)
    IBSS cell ID/AP: xx:xx:xx:xx:xx:xx
    SSID: RaspberryMesh
    freq: 5180
    RX: 1204 bytes (12 packets)
    TX: 852 bytes (8 packets)
    signal: -48 dBm
    tx bitrate: 300.0 MBit/s MCS 15 40MHz
```

接続性をテストします：
```bash
ping -c 4 192.168.88.2
```

```
PING 192.168.88.2 (192.168.88.2) 56(84) bytes of data.
64 bytes from 192.168.88.2: icmp_seq=1 ttl=64 time=1.84 ms
64 bytes from 192.168.88.2: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 192.168.88.2: icmp_seq=3 ttl=64 time=2.01 ms
64 bytes from 192.168.88.2: icmp_seq=4 ttl=64 time=1.88 ms
```

iperf3 でスループットをテストします：
```bash
# ノード 2（サーバー）で：
iperf3 -s

# ノード 1（クライアント）で：
iperf3 -c 192.168.88.2 -t 10
```

### 再起動後も IBSS を持続させる

各ノードに `/etc/systemd/system/ibss-mesh.service` を作成します：

```ini
[Unit]
Description=IBSS Ad Hoc Mesh Network
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  ip link set wlan1 down && \
  iw dev wlan1 set type ibss && \
  ip link set wlan1 up && \
  iw dev wlan1 ibss join RaspberryMesh 5180 && \
  ip addr add 192.168.88.1/24 dev wlan1'
ExecStop=/bin/bash -c '\
  iw dev wlan1 ibss leave && \
  ip link set wlan1 down'

[Install]
WantedBy=multi-user.target
```

有効化します：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ibss-mesh.service
sudo systemctl start ibss-mesh.service
```

> **注意：** 各ノードのサービスファイルで IP アドレスを変更してください（`.1`、`.2`、`.3` など）

### 3 台目のノードを追加する

ノード 3 には、IP `192.168.88.3` で同じ手順を使用します。3 台のノードはすべて互いの直接無線到達範囲内にいる必要があります。ノード 2 を経由してノード 1 とノード 3 の間でトラフィックをルーティングするには、ノード 2 で IP フォワーディングを有効にします：

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## 5. モード 2：802.11s メッシュポイントネットワーク

### 802.11s の動作原理

802.11s 修正仕様は、**メッシュ調整レイヤー**を 802.11 MAC に直接追加します。すべてのノードが中央 AP に話しかける代わりに、各ノードは：

1. 選択したチャンネルと `mesh_id` で **メッシュビーコン**フレームをブロードキャストして、隣接するメッシュノードを発見します
2. **HWMP（Hybrid Wireless Mesh Protocol）** を実行して、各宛先への最適なパスを計算します
3. 宛先が直接到達範囲外の場合、送信元と宛先の MAC アドレスおよびメッシュシーケンス番号を含む**メッシュヘッダー**でデータフレームをカプセル化します
4. 中間ホップを経由してフレームを自動的に転送します

Linux カーネルはこれを `iw` の `mp`（メッシュポイント）インターフェース型を通じて公開しており、カーネル自身の 80211s 実装がピアリングとパス管理をすべて処理します。

### 802.11s と IBSS の比較

| 機能 | IBSS（アドホック） | 802.11s メッシュポイント |
|---|---|---|
| IEEE 規格 | 802.11 IBSS | 802.11s |
| マルチホップルーティング | ❌ 手動のみ | ✅ 自動（HWMP） |
| ノード範囲 | すべてが直接範囲内 | シングルホップを超えて拡張 |
| スケーラビリティ | 実用 3〜5 ノード | batman-adv で 10 ノード以上 |
| 設定の複雑さ | 低い | 中程度 |
| 自己修復 | ❌ なし | ✅ あり |
| 最適な用途 | シンプルな 2〜3 ノード構成 | 大規模な分散システム |

### ステップバイステップ：マルチノード 802.11s メッシュ

この例では、5 GHz チャンネル 36 上に 3 ノードのメッシュを構築します。各ノードは他のノードを自動的に発見し、パスを確立します。

---

#### すべてのノードで — メッシュインターフェースを作成する

**ステップ 1 — 物理デバイス（phy）名を特定します：**

```bash
iw dev
```

AWUS036ACM に関連付けられた phy を探します（通常 `phy1`）：
```
phy#1
    Interface wlan1
        ...
```

**ステップ 2 — `mesh0` という名前の新しいメッシュポイントインターフェースを追加します：**

```bash
sudo iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh
```

> これにより、`wlan1` と同じ物理ラジオ上に新しい仮想インターフェース `mesh0` が作成されます。元の `wlan1` はマネージドモードのままでインターネットアクセスに使い続けることができます。これが VIF（仮想インターフェース）の活用です。

**ステップ 3 — 動作チャンネルを設定します（5 GHz チャンネル 36）：**

```bash
sudo iw dev mesh0 set channel 36
```

**ステップ 4 — メッシュインターフェースをアップします：**

```bash
sudo ip link set mesh0 up
```

**ステップ 5 — 各ノードに固有の IP アドレスを割り当てます：**

```bash
# ノード 1：
sudo ip addr add 10.88.0.1/24 dev mesh0

# ノード 2：
sudo ip addr add 10.88.0.2/24 dev mesh0

# ノード 3：
sudo ip addr add 10.88.0.3/24 dev mesh0
```

---

#### メッシュの形成を確認する

**ピアが発見されていることを確認します：**

```bash
iw dev mesh0 station dump
```

出力例（ノード 1 がノード 2 とノード 3 を認識している場合）：
```
Station xx:xx:xx:xx:xx:02 (on mesh0)
    inactive time:  120 ms
    rx bytes:       4820
    tx bytes:       3560
    signal:         -52 dBm
    tx bitrate:     300.0 MBit/s MCS 15 40MHz
    mesh plink:     ESTAB
    mesh local PS mode: ACTIVE

Station xx:xx:xx:xx:xx:03 (on mesh0)
    mesh plink:     ESTAB
```

**メッシュルーティングパスを確認します：**

```bash
iw dev mesh0 mpath dump
```

```
DEST ADDR         NEXT HOP          IFACE   SN      METRIC  QLEN    EXPTIME         DTIM    DRET    FLAGS
xx:xx:xx:xx:xx:02 xx:xx:xx:xx:xx:02 mesh0   32      1158    0       0       100     0       0x4
xx:xx:xx:xx:xx:03 xx:xx:xx:xx:xx:02 mesh0   18      2316    0       0       100     0       0x14
```

> ノード 3 のネクストホップはノード 2 であり、ノード 1 がノード 2 を経由して自動的にノード 3 に到達することを意味します。

**メッシュ越しに ping を実行します：**

```bash
# ノード 1 から：
ping -c 4 10.88.0.3
```

### 応用：レイヤー 2 メッシュルーティングに batman-adv を追加する

本番環境での展開では、カーネル組み込みの HWMP を **batman-adv** に置き換えることで、より高度なルーティング、モビリティ下でのパフォーマンス向上、および高レベルなネットワークツールとの互換性が得られます。

**batman-adv をインストールします：**

```bash
sudo apt install batctl
```

**モジュールをロードします：**

```bash
sudo modprobe batman-adv
```

**メッシュインターフェースを batman-adv のスレーブとして設定します：**

```bash
# まず IP なしで mesh0 をアップします
sudo ip link set mesh0 up
sudo batctl if add mesh0

# batman インターフェースをアップします
sudo ip link set bat0 up

# IP を batman インターフェースに割り当てます（mesh0 ではありません）
sudo ip addr add 10.88.0.1/24 dev bat0
```

**batman ルーティングテーブルを確認します：**

```bash
sudo batctl n    # 近隣ノード
sudo batctl o    # オリジネーターテーブル（すべての既知ノード）
sudo batctl tg   # トランスレーションテーブル（MAC → IP マッピング）
```

### 802.11s メッシュを永続化する

`/etc/systemd/system/mesh-point.service` を作成します：

```ini
[Unit]
Description=802.11s Mesh Point Network
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh && \
  iw dev mesh0 set channel 36 && \
  ip link set mesh0 up && \
  ip addr add 10.88.0.1/24 dev mesh0'
ExecStop=/bin/bash -c '\
  ip link set mesh0 down && \
  iw dev mesh0 del'

[Install]
WantedBy=multi-user.target
```

有効化します：
```bash
sudo systemctl daemon-reload
sudo systemctl enable mesh-point.service
sudo systemctl start mesh-point.service
```

---

## 6. 実際の使用例

### 使用例 1 — オフグリッドセンサーネットワーク（スマート農業 / 環境モニタリング）

**シナリオ：** 3 台の Raspberry Pi を畑に展開し、それぞれに土壌水分、温度、湿度センサーを接続しています。携帯電話や WiFi インフラは利用できません。

**設定：** 最大レンジのため 2.4 GHz チャンネル 1（2412 MHz）で IBSS を使用します。各ノードはセンサーデータを収集し、30 秒ごとに中央ロガーノード（ノード 1）に送信します。

**AWUS036ACM を選ぶ理由：** 5 dBi アンテナと 2.4 GHz での 23 dBm の TX 電力により、畑の畝間距離をカバーするのに有用な、平均以上の到達範囲が得られます。オプションの RP-SMA アンテナ（指向性 Yagi など）に換装することで、到達範囲をさらに大幅に延長できます。

**サンプルデータパイプライン：**
```
[Sensor Pi A] ──IBSS──> [Edge Pi B (logger)]
[Sensor Pi C] ──IBSS──> [Edge Pi B (logger)]
```

---

### 使用例 2 — ドローン / ロボットクラスターの通信

**シナリオ：** 2〜3 台の Raspberry Pi ベースのドローンまたは地上ロボットが、地上局を経由せずにテレメトリデータを共有し、動作を調整する必要があります。

**設定：** 低遅延と高スループットのため 5 GHz チャンネル 36（5180 MHz）で IBSS を使用します。各ユニットは約 5 Mbps で 1080p H.264 ビデオをストリーミングし、100 Kbps 未満のテレメトリを送信します。

**5 GHz を選ぶ理由：** AC1200 速度（5 GHz で 867 Mbps）により、AWUS036ACM は複数の同時ビデオストリームに十分すぎるほどのヘッドルームを持っています。また、5 GHz 帯は都市部でよく見られる混雑した 2.4 GHz の干渉を避けられます。

**トポロジー：**
```
[Drone 1 / 192.168.88.1] ──5GHz IBSS──> [Drone 2 / 192.168.88.2]
```

---

### 使用例 3 — 災害対応 / 緊急通信キット

**シナリオ：** 迅速展開チームがインフラのない場所に到着します。各チームメンバーは Raspberry Pi Zero 2W + AWUS036ACM + バッテリーパックを携帯しています。60 秒以内に、テキスト通信、ファイル共有、調整のための多ノードメッシュが稼動します。

**設定：** 建物や障害物を越えた最大レンジのため 2.4 GHz で 802.11s メッシュを使用します。batman-adv がルーティングを処理するため、チームは IP を手動で管理する必要がありません。

**802.11s / batman-adv を選ぶ理由：** チームメンバーが移動するとメッシュトポロジーが変化します。batman-adv はパスを自動的に更新します。単一障害点はありません。

---

### 使用例 4 — Raspberry Pi コンピュートクラスターのバックボーン

**シナリオ：** 開発者が 4〜6 台の Raspberry Pi 4 を使用して Beowulf スタイルのコンピュートクラスターを運用しています。メインの Ethernet ネットワークとは別に、専用の低遅延インターコネクトが必要です。

**設定：** mesh_id `ClusterBackbone` を使用して 5 GHz 上で 802.11s メッシュを構築します。各ノードはプロセス間メッセージング（MPI、Redis pub/sub、ZeroMQ）のためにメッシュ経由で通信します。

**専用メッシュを使う理由：** クラスタートラフィックをメインネットワークから分離することで、共有 Ethernet スイッチの飽和を防ぎ、メインネットワークが利用できない場合でもクラスターネットワークを維持できます。

---

### 使用例 5 — セキュリティ研究ラボ / 隔離テスト環境

**シナリオ：** ペネトレーションテスターまたはセキュリティ研究者が、アドホック固有の脆弱性のテストや検出ツールの検証のために、プライベートな 802.11 IBSS ネットワークをシミュレートしたいと考えています。

**設定：** クリアなチャンネルで IBSS を使用し、本番 WiFi から隔離します。AWUS036ACM のモニターモードを VIF 経由で同時に使用します。1 つのインターフェースが IBSS に参加し、もう 1 つのインターフェースがすべてのフレームを Wireshark 分析用にキャプチャします。

```bash
# IBSS と並行してモニターインターフェースを作成する
sudo iw phy phy1 interface add mon0 type monitor
sudo ip link set mon0 up
# キャプチャ：
sudo tcpdump -i mon0 -w capture.pcap
```

---

## 7. AWUS036ACM がこの用途で唯一の ALFA の選択肢である理由

### 決定的な要因：mac80211 準拠

USB WiFi アダプターが Linux で IBSS と 802.11s メッシュをサポートするかどうかは、完全にドライバーアーキテクチャに依存します。**mac80211 ベースのインカーネルドライバー**だけがこれらのモードを公開します。独自の WiFi スタックを実装しているドライバー（ほとんどのアウトオブカーネル Realtek ドライバー）は、IBSS やメッシュ機能を単純に含んでいません。

### 他のすべての現行 ALFA アダプターの状況

| モデル | チップセット | ドライバー | IBSS | 802.11s メッシュ | 備考 |
|---|---|---|---|---|---|
| **AWUS036ACM** | MT7612U | mt76x2u（インカーネル ≥ 4.19） | ✅ | ✅ | **唯一の選択肢** |
| AWUS036ACH | RTL8812AU | rtw88（インカーネル ≥ 6.14） | ✅（カーネル ≥ 6.14 のみ） | ❌ | 新しいインカーネルドライバー、メッシュポイントなし |
| AWUS036ACS | RTL8811AU | rtl8812au-dkms（OOK） | ❌ | ❌ | アウトオブカーネルドライバー、IBSS/メッシュなし |
| AWUS036AX | RTL8832BU | rtw88（インカーネル） | ❌ | ❌ | Raspberry Pi サポートなし |
| AWUS036AXER | RTL8832BU | rtw88（インカーネル） | ❌ | ❌ | Raspberry Pi サポートなし |
| AWUS036AXM | MT7921AUN | mt7921u（インカーネル ≥ 5.18） | ❌ | ❌ | mt7921u は IBSS を公開しない |
| AWUS036AXML | MT7921AUN | mt7921u（インカーネル ≥ 5.18） | ❌ | ❌ | mt7921u は IBSS を公開しない |
| ~~AWUS036ACHM~~ | ~~MT7610U~~ | ~~mt76x0u~~ | ~~✅~~ | ~~✅~~ | **製造終了 — 廃番** |
| ~~AWUS1900~~ | ~~RTL8814AU~~ | ~~OOK~~ | ~~Limited~~ | ~~❌~~ | **製造終了 — 廃番** |

### これがユーザーにとって意味すること

AWUS036ACHM（MT7610U）はこれらのモードをサポートしていた以前の ALFA アダプターでしたが、現在は廃番です。Raspberry Pi 上でクリーンなプラグ＆プレイの IBSS と 802.11s メッシュを提供する、現在製造中の他の ALFA USB アダプターは存在しません。

**AWUS036ACM は単に最良の選択肢というだけでなく、このユースケースにおける ALFA の現行ラインナップで唯一の選択肢です。**

さらに、AWUS036ACM は以下も提供しています：
- **AC1200 デュアルバンド** — 2.4 GHz（レンジ重視）または 5 GHz（スループット重視）のどちらでも IBSS/メッシュをサポート
- **USB 3.0** — Pi 4/5 の USB 3.0 ポートで帯域幅を最大限活用
- **着脱式 RP-SMA アンテナ × 2** — 高ゲイン指向性アンテナに換装して、付属の 5 dBi ダイポールをはるかに超えるメッシュ範囲を実現
- **VIF サポート** — メッシュバックボーンと AP モードを 1 台のアダプターで同時に実行
- **Raspberry Pi 3B+、4、5 で動作** — すべての Pi 世代にわたって一貫したサポート

---

## 8. よくある質問とトラブルシューティング

**Q: Pi に `wlan0` しか表示されません。`wlan1` はどこにありますか？**

AWUS036ACM のインターフェースはアダプターを接続した後に表示されます。接続後に `iw dev` を実行してください。10 秒以内に表示されない場合は、`dmesg | grep -i mt76` でエラーメッセージを確認してください。Raspberry Pi OS Lite では、パッケージがまだインストールされていない場合は `sudo apt install iw` が必要な場合があります。

---

**Q: `iw dev wlan1 set type ibss` が「Device or resource busy」を返します**

NetworkManager または `wpa_supplicant` がインターフェースを占有しています。これらを停止してください：
```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```
その後、再試行してください。デスクトップ版の Raspberry Pi OS では、`dhcpcd` もインターフェースを占有している場合があります。`/etc/dhcpcd.conf` に `denyinterfaces wlan1` を追加して、`dhcpcd` を再起動してください。

---

**Q: `iw phy phy1 interface add mesh0 type mp` が「Operation not supported」を返します**

アダプターの phy 名が `phy1` ではない可能性があります。`iw dev` を実行して AWUS036ACM がどの phy にあるかを確認し、正しい phy 名に置き換えてください。

---

**Q: IBSS は設定されましたが、ノード間の ping が失敗します**

確認してください：
1. 両方のノードが**まったく同じ周波数**を使用しているか（例：両方が `5180`、一方が `5180` でもう一方が `5200` ということがないか）
2. 両方のノードが同じサブネット内に**異なる IP アドレス**を持っているか
3. ICMP をブロックするファイアウォールがないか — `sudo iptables -L` を確認してください
4. `iw dev wlan1 link` を実行して、両ノードで IBSS セル ID（BSSID）が一致していることを確認してください

---

**Q: 再起動後に mesh0 インターフェースが消えてしまいます**

`iw` で作成した仮想インターフェースは再起動後に維持されません。[セクション 5](#making-80211s-mesh-persistent) に示した systemd サービスを使用して、自動的に再作成されるようにしてください。

---

**Q: IBSS 上で WPA2 暗号化を使用できますか？**

標準の WPA2-Personal（PSK）は、Linux カーネルの IBSS モードではサポートされていません。IBSS を保護するには、アプリケーション層の暗号化（WireGuard、OpenVPN、または SSH トンネル）を使用できます。802.11s メッシュでは、`wpa_supplicant` を使用した SAE（WPA3 スタイル認証）がサポートされています。

---

**Q: AWUS036ACM を IBSS とマネージドモードで同時に使用できますか？**

はい — これが VIF（仮想インターフェース）の目的です。`wlan1` をマネージドモードのままホームルーターのインターネットアクセスに使いながら、Pi 間ネットワーク用の IBSS またはメッシュモードで 2 番目の仮想インターフェースを追加できます：

```bash
# wlan1 はマネージドのまま（インターネット用）
# IBSS 用に 2 番目のインターフェースを追加
sudo iw phy phy1 interface add adhoc0 type ibss
sudo ip link set adhoc0 up
sudo iw dev adhoc0 ibss join LocalNet 5180
sudo ip addr add 192.168.88.1/24 dev adhoc0
```

---

**Q: 到達できる最大範囲はどれくらいですか？**

付属の 5 dBi アンテナを使用した場合、5 GHz での屋外開放空間で 20〜50 m、2.4 GHz で 50〜100 m 程度を期待できます。アンテナを高ゲイン RP-SMA 指向性アンテナ（別売）に換装することで、見通し条件下で数百メートルまで範囲を延長できます。AWUS036ACM の RP-SMA コネクターは標準サイズで、幅広いサードパーティ製アンテナと互換性があります。

---

**Q: Raspberry Pi Zero 2W でも動作しますか？**

はい — Raspberry Pi Zero 2W にはフルサイズ USB-A ポート（OTG アダプター経由）があり、カーネルバージョンが 4.19 を大幅に上回る Raspberry Pi OS が動作しています。AWUS036ACM はそこでも動作しますが、Zero 2W の USB ポートは USB 2.0 のみであることに注意してください。そのため、実際の帯域幅は約 300〜400 Mbps に制限されます。IBSS/メッシュの制御トラフィックとセンサーデータには十分すぎる速度です。

---

## 9. 購入先

ALFA AWUS036ACM は、ALFA Network の公式リセラーである [yupitek.com](https://yupitek.com) から購入できます。正規リセラーからの購入により、Alfa Network Inc. の標準保証付きの正規品を確実に入手できます。

**製品ページ：** [Yupitek の ALFA AWUS036ACM](https://yupitek.com)

同梱物：
- AWUS036ACM アダプター × 1
- 着脱式 5 dBi デュアルバンドダイポールアンテナ（RP-SMA）× 2
- USB 3.0 延長ケーブル × 1
- ドライバー CD（Windows 用）× 1

---

## まとめ

| 機能 | AWUS036ACM |
|---|---|
| チップセット | MediaTek MT7612U |
| WiFi | AC1200（867 + 300 Mbps）、デュアルバンド |
| IBSS アドホック | ✅ 2020 年以降のすべての Raspberry Pi OS バージョン |
| 802.11s メッシュ | ✅ プラグ＆プレイ |
| インカーネルドライバー | ✅ mt76x2u（カーネル 4.19 以降） |
| Pi でのプラグ＆プレイ | ✅ インストール不要 |
| 着脱式アンテナ | ✅ 5 dBi RP-SMA × 2 |
| IBSS + メッシュ対応の唯一の現行 ALFA モデル | ✅ はい |

Raspberry Pi ノード間にワイヤレスネットワークを構築する必要がある場合——2 デバイスの直接リンクであれ、マルチホップの自己修復型メッシュであれ——ALFA AWUS036ACM はそれを実現するアダプターです。

---

*記事：Yupitek テクニカルチーム · [yupitek.com](https://yupitek.com)*

*参考資料：[Alfa Network 公式ドキュメント](https://docs.alfa.com.tw/Product/AWUS036ACM/) · [Linux Wireless Wiki — インターフェース型](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) · [MediaTek mt76 Linux ドライバー](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) · [morrownr USB-WiFi インカーネル一覧](https://github.com/morrownr/USB-WiFi)*
