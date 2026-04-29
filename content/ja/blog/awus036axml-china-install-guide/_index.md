---
title: "ALFA AWUS036AXML ドライバインストールガイド（中国版）：Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "中国国内のミラーサイトを利用して、ALFA AWUS036AXMLのドライバをインストールする手順をステップバイステップで解説します。MT7921AUN WiFi 6E インカーネルドライバ、モニターモード、VIFをサポート。Kali Linux、Ubuntu 22/24、Debian、Raspberry Piをカバーしています。GitHubへのアクセスは不要です。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 7
related_product: "/ja/products/alfa/awus036axml/"
---

AWUS036AXMLは、ALFAのWiFi 6Eフラッグシップモデルです。2.4 GHz、5 GHzに加えて、混雑の少ない6 GHz帯をカバーするUSB-Cアダプターです。搭載されているMT7921AUNチップは、Linuxカーネルバージョン5.18以降で `mt7921u` ドライバが標準組み込みされています。Ubuntu 24.04やKali 2025では、国内ミラーからファームウェアパッケージをインストールするだけで、プラグアンドプレイで使用可能です。このガイドでは、GitHubに触れることなく、ファームウェアの設定、ドライバの確認、モニターモード、パケットインジェクション、VIFの設定までを完全にカバーします。

## 準備するもの

1. **ALFA AWUS036AXML** アダプター本体と USB-C ケーブル
2. 電源付きUSBハブ（Raspberry Piを使用する場合は必須です）
3. 国内ミラーサイトにアクセスできるインターネット環境

アダプターを接続し、システムが認識しているか確認します：

```bash
lsusb
```

出力の中に以下の行を探してください：

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

`0e8d:7961` が表示されていればOKです。お使いのOSのセクションに進んでください。

表示されない場合は、別のUSB-Cポートやケーブルを試して、再度 `lsusb` を実行してください。

## オペレーティングシステムの選択

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

インストールが済んでいる方は、こちらから：

- [モニターモードを有効にする](#enable-monitor-mode)
- [パケットインジェクションのテスト](#test-packet-injection)
- [仮想インターフェース (VIF)](#virtual-interface-vif)
- [VMでのUSBパススルー](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7921AUNドライバは既にKaliのカーネルに含まれています。必要なのはMediaTekのファームウェアパッケージだけで、これは国内ミラーから入手可能です。

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

以下の一行を貼り付けます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

**Ctrl+O**、Enter、**Ctrl+X** で保存して終了します。リポジトリを更新します：

```bash
sudo apt update
```

> **バックアップ用ミラー:** 中科大 (USTC) が遅い場合は、清華大学 (Tsinghua) を使用してください：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### ステップ 2: ファームウェアのインストール

MT7921AUNには、`firmware-misc-nonfree` と `linux-firmware` からのファームウェアが必要です。これらがないと、ドライバは読み込まれてもアダプターの初期化に失敗します。

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### ステップ 3: ドライバの確認

再起動後、アダプターを接続して確認します。

```bash
lsmod | grep mt7921
```

出力に `mt7921u` が表示されれば成功です。次に無線インターフェースが表示されるか確認します。

```bash
iwconfig
```

`wlan0` や `wlan1` を探してください。

---

### ステップ 4: モニターモードを有効にする {#enable-monitor-mode}

まず、インターフェース名を確認します。

```bash
iwconfig
```

表示された名前（例：`wlan1`）を使用します。干渉するプロセスを終了させてから、モニターモードに切り替えます。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

確認します：

```bash
iwconfig
```

`Mode:Monitor` になっていればOKです。

---

### ステップ 5: パケットインジェクションのテスト {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

成功した場合の出力例：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

失敗した場合は、再起動してもう一度試してください。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — カーネル 6.8、プラグアンドプレイ対応

Ubuntu 24.04 はカーネル 6.8 を採用しており、MT7921AUN ドライバをネイティブに含んでいます。

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

すべて削除して以下を貼り付けます：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
```

### ステップ 2: ファームウェアのインストール

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### ステップ 3: 確認とモニターモードの有効化

再起動後、`lsmod | grep mt7921` を実行してドライバが読み込まれていることを確認し、上記の Kali Linux のモニターモードの手順（ステップ 4）に従ってください。

---

### Ubuntu 22.04 (Jammy) — HWEカーネルが必要

Ubuntu 22.04 の標準カーネルは 5.15 ですが、MT7921AUN ドライバにはカーネル 5.18 以上が必要です。まず HWE カーネルをインストールしてください。

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

すべての行を以下に置き換えます：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

### ステップ 2: HWEカーネルのインストール

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

再起動後、カーネルバージョンを確認します：

```bash
uname -r
```

5.19以上が表示されればOKです。その後、ファームウェアのインストールとモニターモードの有効化を行います。

### ステップ 3: ファームウェアのインストール

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

貼り付け（Debian 12 Bookwormの場合）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### ステップ 2: ファームウェアのインストール

Debian 12 Bookworm はカーネル 6.1 を採用しており、MT7921AUN と互換性があります。

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### ステップ 3: 確認とモニターモードの有効化

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### ステップ 4: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1
```

`Injection is working!` と表示されれば、アダプターは完全に動作しています。

---

## Raspberry Pi 4B / 5

> AWUS036AXML は負荷時に最大 2.7W の電力を消費します。Raspberry Pi では必ず電源付きの USB ハブを使用してください。

### ステップ 1: Kali Linux ARM64 イメージをダウンロード

公式サイト: https://www.kali.org/get-kali/#kali-arm

**Raspberry Pi 4 (64-bit)** または **Raspberry Pi 5 (64-bit)** を選択（64-bit 必須）。

> **中国国内ミラー:** https://repo.huaweicloud.com/kali-images/ — 最新リリースのフォルダから ARM64 イメージをダウンロードしてください。

### ステップ 2: MicroSD への書き込み

```bash
lsblk
# /dev/sdX を実際の SD カードのパスに置き換えてください
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

デフォルトのログイン情報: **kali / kali**

### ステップ 3: 中国国内のミラーに切り替えてファームウェアをインストール

```bash
sudo nano /etc/apt/sources.list
```

以下に置き換えます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

その後：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### ステップ 4: ドライバの確認

```bash
lsmod | grep mt7921
```

`mt7921u` が表示されればOKです。

### ステップ 5: モニターモードを有効にする

Wi-Fi内蔵のPiでは、AWUS036AXML は `wlan1` として表示されます。

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### ステップ 6: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1
```

---

## 仮想マシンでのUSBパススルー {#virtual-machine-usb-passthrough}

### VirtualBox

1. VMを終了し、**設定 → USB** を開きます。
2. **USB 3.0 (xHCI) コントローラー** を有効にします。
3. **+** をクリックして USB フィルターを追加します。
4. **MediaTek Inc.** (ID: 0e8d:7961) を選択します。
5. VMを起動すると、Kali の中でアダプターが認識されます。

VM内で `lsusb` を実行して `0e8d:7961` を確認し、上記の Kali の手順に従ってください。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VMを起動します。
2. メニュー: **仮想マシン → USB と Bluetooth**。
3. **MediaTek MT7921AUN** を探し、**接続** をクリックします。
4. VM内で `lsusb` を確認し、上記の Kali の手順に従ってください。

---

## 仮想インターフェース (VIF) {#virtual-interface-vif}

MT7921AUN は、カーネルネイティブの完全な VIF サポートを備えています。パッチを当てることなく、同じアダプター上でモニターインターフェースとマネージドインターフェースを同時に実行できます。

### マネージドモードと並行してモニターインターフェースを作成する

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

`wlan0`（マネージド）と `mon0`（モニター）の両方が同時にアクティブになっていることが確認できます。

### 接続を維持したままモニターする

```bash
sudo airodump-ng mon0
```

`wlan0` は関連付けられたまま、`mon0` は範囲内のすべての通信をキャプチャします。

### Fake AP + モニター

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **hostapd に関する注意:** 完全な AP 動作には `hostapd` の設定が必要です。上記の手順はアダプターがインターフェースを作成できることを確認するためのもので、実際の AP 設定は別のトピックとなります。

---

## トラブルシューティング

| 問題点 | 考えられる原因 | 解決策 |
|---------|-------------|-----|
| `lsusb` に 0e8d:7961 が表示されない | 電源不足またはケーブル不具合 | 別の USB-C ポートやケーブルを試してください。Raspberry Pi では電源付きハブを使用してください。 |
| `lsmod` に mt7921u が表示されない | ファームウェア未インストールまたはカーネルが古い | `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` を実行 |
| Ubuntu 22.04 でドライバが読み込まれない | カーネル 5.15 は古すぎます | HWE をインストール: `sudo apt install linux-generic-hwe-22.04` |
| インターフェースは見えるが関連付けられない | ファームウェアの blob が不足している | `sudo apt install firmware-misc-nonfree` を実行して再起動 |
| モニターモードへの切り替えが失敗する | インターフェースがまだ UP 状態 | `iw dev` コマンドの前に `sudo ip link set wlan1 down` を実行 |
| インジェクションテストが "No Answer" | AP が遠すぎるかインターフェース間違い | もっと近づいてください。`iwconfig` で `Mode:Monitor` を確認 |
| VIF インターフェース作成が失敗する | ドライバが完全にロードされていない | 一度抜き、次を実行: `sudo rmmod mt7921u && sudo modprobe mt7921u` |

## 中国国内ミラーリファレンス

| リソース | URL | 用途 |
|----------|-----|---------|
| Alfa 公式ドライバ | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバパッケージ、ファームウェア |
| Alfa ドキュメント | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル |
| 清華大学ミラー | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里巴巴ミラー | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (推奨) |
| 中国科学技術大学ミラー | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (推奨) |
| 華為ミラー | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM イメージ (バックアップ) |

## 中国向け Alfa アダプターガイド（その他）

このページは **Alfa China Install Guide** シリーズの一部です：

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF完全対応
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/) — RTL8811AU、モニターモード
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型USB-A
- AWUS036AXML ← 現在のページ
- [AWUS036EACS 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。
