---
title: "ALFA AWUS036AXER ドライバインストールガイド（中国版）：Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "中国国内のミラーサイトを利用して、ALFA AWUS036AXERのドライバをインストールする手順をステップバイステップで解説します。RTL8832BUドライバ、WiFi 6 Nanoアダプター対応。Kali Linux、Ubuntu 22/24(DKMS)、Debian、Raspberry Piをカバーしています。GitHubへのアクセスは不要です。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu", "nano"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/ja/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036AXERはどのチップを使っていますか？AWUS036AXと同じですか？"
    answer: "同じくRealtek RTL8832BUチップを採用しWiFi 6をサポートしていますが、より小型で携帯性に優れています。"
  - question: "AWUS036AXERはUbuntu 24.04でドライバーインストールが必要ですか？"
    answer: "必要です。RTL8832BU は Ubuntu 24.04 のカーネルに含まれていません。コミュニティ版 rtl8852bu ドライバ（morrownr/rtl8852bu-20250826）を DKMS で一度ビルドすれば、カーネル更新時も自動で再ビルドされます。"
  - question: "AWUS036AXERは無線セキュリティリサーチに適していますか？"
    answer: "いいえ。コミュニティ版 rtl8852bu ドライバはモニターモードとパケットインジェクションをサポートしていません。代わりに AWUS036ACM などカーネル標準の MediaTek ドライバを持つアダプターをご利用ください。"
  - question: "AWUS036AXERのUSB IDは何ですか？"
    answer: "Realtek RTL8832BUのベンダーIDは0bdaで、プロダクトIDは個体によって8832または885aです。お手元のデバイスはlsusbで確認してください。"
  - question: "中国でAWUS036AXERをインストールするのにVPNは必要ですか？"
    answer: "不要です。Giteeからrtl8852buソースコードをダウンロードし、国内ミラーでコンパイルツールをインストールするだけです。"
---

AWUS036AXERは、ALFAの超小型（Nano）WiFi 6 AX1800デュアルバンド・アダプターです。AWUS036AXER の RTL8832BU チップには Linux カーネル標準のドライバがないため、Ubuntu 24.04 を含むどのディストリビューションでも、コミュニティ版 rtl8852bu ドライバを DKMS で一度ビルドする必要があります。このガイドは Gitee ミラーを使うので GitHub へのアクセスは不要です。このドライバはモニターモードをサポートしていません。


{{< tldr >}}
AWUS036AXER は RTL8832BU チップで WiFi 6 に対応します。ドライバはカーネルに含まれないため、Ubuntu 24.04 を含むすべてのディストリビューションで rtl8852bu を DKMS でビルドする必要があります。モニターモードは非対応です。
{{< /tldr >}}
> **セキュリティ研究に関する注意：** コミュニティ版 rtl8852bu ドライバはモニターモードとパケットインジェクションをサポートしていません。セキュリティ研究にはカーネル標準の MediaTek ドライバを持つ [AWUS036ACM](/ja/blog/awus036acm-china-install-guide/) などをご利用ください。

## 準備するもの

1. **ALFA AWUS036AXER** アダプター本体
2. インターネット接続環境

```bash
lsusb
```

以下のような行を探してください（以下は出力例です。ベンダーIDは常に `0bda`、プロダクトIDは個体によって `8832` または `885a` です）：

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
lsmod | grep 8852bu
iwconfig
```

### ステップ 5: モニターモードを有効にする {#enable-monitor-mode}

> **非対応:** RTL8832BU 向けのコミュニティ版 rtl8852bu ドライバはモニターモードをサポートしていないため、ここで実行するコマンドはありません。モニターモードが必要な場合は、カーネル標準の MediaTek ドライバを持つ [AWUS036ACM](/ja/blog/awus036acm-china-install-guide/) などをご利用ください。

### ステップ 6: パケットインジェクションのテスト {#test-packet-injection}

> **非対応:** パケットインジェクションはモニターモードに依存しますが、このドライバはモニターモードを提供しません。インジェクションのテストには [AWUS036ACM](/ja/blog/awus036acm-china-install-guide/) をご利用ください。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — DKMS が必要

Ubuntu 24.04（カーネル 6.8）には RTL8832BU 用のドライバが含まれていません。国内ミラーに切り替えたうえで、下の Ubuntu 22.04 と同じ手順でドライバをビルドしてください。

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
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

再起動後に `sudo modprobe 8852bu` と `iwconfig` を実行します。モジュールが読み込まれてインターフェースが表示されれば完了です（マネージドモードのみ。モニターモードは非対応）。

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

このドライバはモニターモードをサポートしていません（Kali のステップ 5 を参照）。

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
2. フィルターを追加: **Realtek** (ベンダーID: 0bda、プロダクトID: 8832 または 885a)。
3. VMを起動し、`lsusb` で確認してから、Kaliの手順に従います。

### VMware

1. **仮想マシン → USB と Bluetooth** → **Realtek RTL8832BU** を探し → **接続** をクリック。
2. `lsusb` で確認し、Kaliの手順に従います。

---

## トラブルシューティング

| 問題点 | 考えられる原因 | 解決策 |
|---------|-------------|-----|
| `lsusb` に 0bda:8832 または 0bda:885a が表示されない | アダプターが認識されていない | 別のUSBポートを試してください |
| `install-driver.sh` が失敗する | ヘッダーが不足している | `sudo apt install linux-headers-$(uname -r)` |
| Giteeのクローンが失敗する | ネットワークの問題 | Giteeで `rtl8852bu` を検索してください |
| `modprobe 8852bu` が失敗する | ドライバ未ビルドまたは未ロード | `sudo ./install-driver.sh` を再実行し、`sudo dkms status` を確認して再起動 |
| モニターモード／インジェクションが動作しない | rtl8852bu ドライバは非対応 | ペンテストには AWUS036ACM を使用 |

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


---

{{< faq >}}

---

## 中国向け Alfa アダプターガイド（その他）

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF完全対応
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/) — RTL8811AU、モニターモード
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← 現在のページ
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。

---

## 参考文献

1. [Realtek公式ウェブサイト](https://www.realtek.com/)
2. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
3. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
4. [Gitee rtl8852buミラー](https://gitee.com/mirrors/rtl8852bu)
