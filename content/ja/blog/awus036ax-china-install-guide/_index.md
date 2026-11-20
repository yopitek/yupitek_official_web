---
title: "ALFA AWUS036AX ドライバインストールガイド（中国版）：Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "中国国内のミラーサイトを利用して、ALFA AWUS036AXのドライバをインストールする手順をステップバイステップで解説します。RTL8832BUドライバ、WiFi 6 AX1800対応。Kali Linux、Ubuntu 22/24(DKMS)、Debian、Raspberry Piをカバーしています。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/ja/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "AWUS036AXはどのチップを使っていますか？WiFi 6をサポートしていますか？"
    answer: "Realtek RTL8832BUチップを採用し、WiFi 6（802.11ax）高速ネットワークをサポートしています。"
  - question: "AWUS036AXはUbuntu 24.04でドライバーインストールが必要ですか？"
    answer: "カーネルのバージョンによります。Linux カーネル 6.17 以降（例: Ubuntu 24.04 HWE / kernel 6.17）には標準で rtw89_8852bu ドライバが含まれており、挿すだけで認識され、DKMS は不要です。カーネルが 6.17 より古い場合のみ、コミュニティ版 rtl8852bu ドライバ（morrownr/rtl8852bu-20250826）を DKMS で一度ビルドします。まず uname -r でカーネルを確認してください。"
  - question: "AWUS036AXは無線セキュリティリサーチに適していますか？"
    answer: "はい。カーネル 6.17 以降の標準ドライバ rtw89_8852bu では、モニターモードとパケットインジェクションがいずれも実機テストで動作します（Ubuntu 24.04 / kernel 6.17 で 2.4GHz インジェクション 96%、エンドツーエンドの WPA .22000 キャプチャ）。注意：古いカーネルでコミュニティ版 DKMS ドライバを使う場合、モニター対応は制限されることがあります。自分が所有またはテスト許可を得たネットワークに限ります。"
  - question: "中国でAWUS036AXをインストールするのにVPNは必要ですか？"
    answer: "いいえ。検証済みの GitHub リポジトリ（morrownr/rtl8852bu-20250826）からドライバをクローンしてください。GitHub が遅い場合は、信頼できるプロキシまたはミラーを使ってください。ビルドツールは国内ミラーからインストールできます。"
  - question: "AWUS036AXのUSB IDは何ですか？"
    answer: "Realtek RTL8832BUのベンダーIDは0bdaで、プロダクトIDは個体によって8832または885aです。お手元のデバイスはlsusbで確認してください。"
---

AWUS036AXは、ALFAのWiFi 6 AX1800デュアルバンド・アダプターです。その RTL8832BU チップは、**Linux カーネル 6.17 以降**（例: Ubuntu 24.04 HWE / kernel 6.17）では標準の rtw89_8852bu ドライバでサポートされており、挿すだけで使え、ビルドは不要です。**古いカーネル**（6.17 未満）でのみ、コミュニティ版 rtl8852bu ドライバを DKMS で一度ビルドします。本ガイドは両方のケースをカバーします。ドライバのソースは検証済みの GitHub リポジトリからクローンします。GitHub が遅い場合は、信頼できるプロキシまたはミラーを使ってください。


{{< tldr >}}
AWUS036AX は RTL8832BU チップで WiFi 6 に対応します。カーネル 6.17 以降（Ubuntu 24.04 / kernel 6.17 を含む）には標準で rtw89_8852bu ドライバが含まれ、DKMS 不要で、モニターモードとインジェクションも実機テストで動作します。古いカーネルではコミュニティ版 rtl8852bu を DKMS でビルドします。
{{< /tldr >}}
> **セキュリティ研究に関する注意：** **カーネル 6.17 以降の標準ドライバ rtw89_8852bu** では、AWUS036AX のモニターモードとパケットインジェクションが実機テストで動作します（Ubuntu 24.04 / kernel 6.17 で 2.4GHz インジェクション 96%、エンドツーエンドの WPA .22000）。古いカーネルでコミュニティ版 DKMS ドライバを使う場合に限り、モニター対応が制限されることがあります。まず `uname -r` でカーネルを確認してください。自分が所有またはテスト許可を得たネットワークに限ります。

## 準備するもの

1. **ALFA AWUS036AX** アダプター本体
2. USB-A ケーブル
3. インターネット接続環境

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

### ステップ 3: GitHubからドライバをクローンする

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **注意:** メンテナンスされている上流ドライバは [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) です。GitHub が遅い場合は、信頼できるプロキシまたはミラーを使ってください。[files.alfa.com.tw](https://files.alfa.com.tw) からアーカイブをダウンロードすることもできます。

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

> **カーネル 6.17 以降で動作:** 標準の rtw89_8852bu ドライバでは、モニターモードが実機テストで動作します:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> **古いカーネル**でコミュニティ版 DKMS ドライバを使う場合は、モニター対応が制限されることがあります——その場合はカーネル標準の MediaTek ドライバを持つアダプター（例: [AWUS036ACM](/ja/blog/awus036acm-china-install-guide/)）に切り替えてください。

### ステップ 6: パケットインジェクションのテスト {#test-packet-injection}

> **カーネル 6.17 以降で動作:** モニターモードに入ったら、aireplay-ng でインジェクションをテストします（実機テストで 2.4GHz 96%）:
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> 自分が所有またはテスト許可を得たネットワークに限ります。古いカーネルでコミュニティ版 DKMS ドライバがモニターを提供しない場合、インジェクションも利用できません。

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

Ubuntu 24.04 では、**カーネル 6.17 以降の HWE**（例：24.04.4 の HWE）にのみ標準の rtw89_8852bu ドライバが含まれており、挿すだけで使え、ビルドは不要です。**GA カーネル 6.8** や **HWE カーネル 6.14**（どちらもこのドライバを含みません）の場合は、国内ミラーに切り替えて下の Ubuntu 22.04 と同じ手順でコミュニティ版ドライバをビルドするか、6.17 以降の HWE カーネルにアップグレードして標準ドライバを入手してください。

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

再起動後に `sudo modprobe 8852bu` と `iwconfig` を実行します。モジュールが読み込まれてインターフェースが表示されれば完了です（これは古いカーネル向けのコミュニティ版 DKMS ドライバの経路で、モニター対応は制限されることがあります。カーネル 6.17 以降では標準の rtw89_8852bu を使い、モニターとインジェクションが実機テストで動作します）。

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

古いカーネルのコミュニティ版 DKMS ドライバではモニター対応が制限されることがあります。カーネル 6.17 以降では標準の rtw89_8852bu でモニターが動作します（Kali のステップ 5 を参照）。

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
| GitHub のクローンが失敗する／遅い | ネットワークの問題 | 信頼できるプロキシまたはミラーを使う |
| `modprobe 8852bu` が失敗する | ドライバ未ビルドまたは未ロード | `sudo ./install-driver.sh` を再実行し、`sudo dkms status` を確認して再起動 |
| モニターモード／インジェクションが動作しない | カーネルが 6.17 未満でコミュニティ版 rtl8852bu DKMS ドライバを使用（モニター対応は制限されることがあります） | `uname -r` で確認し、カーネル 6.17 以降（標準の rtw89_8852bu）を使用。古いカーネルでは AWUS036ACM を使用 |

> **VIFに関する注意:** RTL8832BU の標準外ドライバは仮想インターフェース (VIF) をサポートしていません。

## 中国国内ミラーリファレンス

| リソース | URL | 用途 |
|----------|-----|---------|
| Alfa 公式ドライバ | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバパッケージ |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU ドライバ |
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
- AWUS036AX ← 現在のページ
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。

---

## 参考文献

1. [Realtek公式ウェブサイト](https://www.realtek.com/)
2. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
3. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
