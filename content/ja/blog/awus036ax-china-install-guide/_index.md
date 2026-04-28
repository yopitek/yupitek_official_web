---
title: "ALFA AWUS036AX ドライバインストールガイド（中国版）：Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "中国国内のミラーサイトを利用して、ALFA AWUS036AXのドライバをインストールする手順をステップバイステップで解説します。RTL8832BUドライバ、WiFi 6 AX1800対応。Kali Linux、Ubuntu 22/24（24.04は標準対応）、Debian、Raspberry Piをカバーしています。GitHubへのアクセスは不要です。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
related_product: "/ja/products/alfa/awus036ax/"
---

AWUS036AXは、ALFAのWiFi 6 AX1800デュアルバンド・アダプターです。搭載されているRTL8832BUチップは、カーネルバージョン6.14未満のLinuxでは標準対応していませんが、Ubuntu 24.04（カーネル6.8）ではネイティブにサポートされています。このガイドでは、古いカーネル向けにはGiteeミラーを、Ubuntu 24.04向けには標準ドライバを使用する方法を解説します。GitHubへのアクセスは不要ですので、安心してくださいね。

> **セキュリティリサーチに関する注意:** RTL8832BUはモニターモードのサポートに制限があります。結果はカーネルやドライバのバージョンによって異なります。Kali Linuxで安定したパケットインジェクションが必要な場合は、[AWUS036ACM](/ja/blog/awus036acm-china-install-guide/) または [AWUS036ACH](/ja/blog/awus036ach-china-install-guide/) をお勧めします。

## 準備するもの

1. **ALFA AWUS036AX** アダプター本体
2. USB-A ケーブル
3. インターネット接続環境

```bash
lsusb
```

以下の行を探してください：

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## オペレーティングシステムの選択

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### ステップ 2: 依存関係のインストール

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### ステップ 3: Giteeからドライバをクローンする

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **注意:** もし上記のGitee URLが読み込めない場合は、Giteeで `rtl8852bu` を検索し、最新のフォークを選んでください。また、[files.alfa.com.tw](https://files.alfa.com.tw) からアーカイブをダウンロードすることも可能です。

### ステップ 4: コンパイルとインストール

```bash
sudo ./install-driver.sh
sudo reboot
```

ドライバが読み込まれているか確認します：

```bash
lsmod | grep 88x2bu
iwconfig
```

### ステップ 5: モニターモードを有効にする {#enable-monitor-mode}

> **注意:** RTL8832BUでのモニターモードのサポートは限定的です。以下のコマンドは多くの環境で動作しますが、結果は異なる場合があります。

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### ステップ 6: パケットインジェクションのテスト {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

インジェクションが不安定な場合は、ペネトレーションテスト作業用として [AWUS036ACM](/ja/blog/awus036acm-china-install-guide/) の使用を検討してください。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — ドライバ標準対応、Gitee不要

Ubuntu 24.04 はカーネル 6.8 を採用しており、RTL8832BU ドライバをネイティブに含んでいます。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

モジュールが読み込まれ、インターフェースが表示されれば完了です。上記のモニターモードの手順に進んでください。

---

### Ubuntu 22.04 (Jammy) — DKMSが必要

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

モニターモードの有効化は、上記の Kali Linux の手順と同じです。

---

## Raspberry Pi 4B / 5

まず中国国内のミラーに切り替えます：

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## 仮想マシンでのUSBパススルー {#virtual-machine-usb-passthrough}

### VirtualBox

1. **設定 → USB** → **USB 3.0 (xHCI) コントローラー**を有効にします。
2. フィルターを追加: **Realtek** (ID: 0bda:885a)。
3. VMを起動し、`lsusb` で確認してから、Kaliの手順に従います。

### VMware

1. **仮想マシン → USB と Bluetooth** → **Realtek RTL8832BU** を探し → **接続** をクリック。
2. `lsusb` で確認し、Kaliの手順に従います。

---

## トラブルシューティング

| 問題点 | 考えられる原因 | 解決策 |
|---------|-------------|-----|
| `lsusb` に 0bda:885a が表示されない | アダプターが認識されていない | 別のUSBポートを試してください |
| `install-driver.sh` が失敗する | ヘッダーが不足している | `sudo apt install linux-headers-$(uname -r)` |
| Giteeのクローンが失敗する | ネットワークの問題 | Giteeで `rtl8852bu` を検索してください |
| Ubuntu 24.04: `modprobe 88x2bu` 失敗 | モジュールが存在しない | `linux-modules-extra-$(uname -r)` をインストール |
| モニターモードが不安定 | RTL8832BUの制限 | ペネトレーションテストには AWUS036ACM を推奨 |

> **VIFに関する注意:** RTL8832BU の標準外ドライバは仮想インターフェース (VIF) をサポートしていません。

## 中国国内ミラーリファレンス

| リソース | URL | 用途 |
|----------|-----|---------|
| Alfa 公式ドライバ | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバパッケージ |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | RTL8832BU ドライバ |
| 清華大学ミラー | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里巴巴ミラー | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中国科学技術大学ミラー | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 華為ミラー | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## 中国向け Alfa アダプターガイド（その他）

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF完全対応
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/) — RTL8811AU、モニターモード
- AWUS036AX ← 現在のページ
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。
