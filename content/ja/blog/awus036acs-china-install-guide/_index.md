---

title: "ALFA AWUS036ACS ドライバインストールガイド（中国版）：Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "中国国内のミラーサイトを利用して、ALFA AWUS036ACSのドライバをインストールする手順をステップバイステップで解説します。RTL8811AU DKMSドライバ、モニターモード、パケットインジェクションに対応。Kali Linux、Ubuntu 22/24、Debian、Raspberry Piをカバーしています。GitHubへのアクセスは不要です。"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 3
related_product: "/ja/products/alfa/awus036acs/"
featureimage: "/images/blog/awus036acs-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACSはどのチップを使っていますか？AWUS036ACHと同じですか？"
    answer: "Realtek RTL8811AUチップを採用し、RTL8812AUと同じドライバーパッケージを共有しています。"
  - question: "AWUS036ACSはモニターモードをサポートしていますか？"
    answer: "サポートしています。RTL8811AUはモニターモードとパケットインジェクションを完全にサポートし、セキュリティリサーチに経済的な選択肢です。"
  - question: "中国でAWUS036ACSをインストールするのにVPNは必要ですか？"
    answer: "不要です。KaliではaptでDKMSドライバーをインストールし、Ubuntu/DebianではGiteeからソースコードをダウンロードしてコンパイルするだけです。"
  - question: "AWUS036ACSのUSB IDは何ですか？"
    answer: "Realtek RTL8811AUのUSB IDは0bda:0811で、lsusbで確認できます。"
  - question: "Kali LinuxでAWUS036ACSドライバーをインストールするコマンドは？"
    answer: "Kaliではsudo apt install realtek-rtl88xxau-dkmsを直接実行してドライバーをインストールできます。"
---

AWUS036ACSは、ALFAのコンパクトなデュアルバンド・セキュリティリサーチ用アダプターです。搭載されているRTL8811AUチップは、Kali Linuxでモニターモードやパケットインジェクションをフルサポートしていますが、ドライバがカーネルに含まれていないため、ソースからコンパイルする必要があります。中国ではGitHubへのアクセスが制限されていることが多いため、このガイドでは国内のGiteeミラーのみを使用します。GitHubへのアクセスは一切不要ですので、安心してくださいね。


{{< tldr >}}
AWUS036ACSはRTL8811AUチップを採用し、KaliではaptでDKMSドライバーをインストール、Ubuntu/DebianではGiteeからコンパイル、モニターモードとパケットインジェクションをサポートします。
{{< /tldr >}}

始める前に、以下のものが手元にあるか確認しましょう：

## 準備するもの

始める前に、以下のものが手元にあるか確認しましょう：

1. **ALFA AWUS036ACS** アダプター本体
2. USBケーブル（製品に付属しているUSB-A 2.0のもので大丈夫です）
3. 国内ミラーサイトにアクセスできるインターネット環境

アダプターを接続したら、システムが認識しているか確認してみましょう：

```bash
lsusb
```

出力の中に以下のような行があればOKです：

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

`0bda:0811` が表示されていれば、アダプターは認識されています。お使いのOSのセクションに進んでください。

## オペレーティングシステムの選択

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

インストールが済んでいる方は、こちらから：

- [モニターモードを有効にする](#enable-monitor-mode)
- [パケットインジェクションのテスト](#test-packet-injection)
- [VMでのUSBパススルー](#virtual-machine-usb-passthrough)

---

## Kali Linux

### ステップ 1: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

既存の内容を削除して、以下を貼り付けてください：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

**Ctrl+O**、Enter、**Ctrl+X** の順に押して保存・終了します。その後、リポジトリを更新します：

```bash
sudo apt update
```

> **バックアップ用ミラー:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### ステップ 2: 依存関係のインストール

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### ステップ 3: Giteeからドライバをクローンする

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **注意:** もし上記のGitee URLが読み込めない場合は、Giteeで `8821au` を検索し、最新のフォークを選んでください。また、[files.alfa.com.tw](https://files.alfa.com.tw) からドライバのアーカイブを直接ダウンロードすることも可能です。

---

### ステップ 4: コンパイルとインストール

```bash
sudo ./install-driver.sh
sudo reboot
```

再起動後、ドライバが読み込まれているか確認します。

```bash
lsmod | grep 88XXau
```

`88XXau` モジュールが表示されれば成功です。次に、インターフェースが表示されるか確認しましょう。

```bash
iwconfig
```

`wlan0` や `wlan1` を探してください。

---

### ステップ 5: モニターモードを有効にする {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig` で確認し、`wlan1mon` が `Mode:Monitor` になっていれば準備完了です。

---

### ステップ 6: パケットインジェクションのテスト {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### ステップ 1: 中国国内のミラーに切り替える

#### Ubuntu 24.04 (Noble)

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

#### Ubuntu 22.04 (Jammy)

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

---

### ステップ 2: 依存関係のインストール

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### ステップ 3: Giteeからドライバをクローンしてインストール

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### ステップ 4: モニターモードを有効にする

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### ステップ 5: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1mon
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

### ステップ 2: 依存関係のインストール

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### ステップ 3: クローンとインストール

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### ステップ 4: モニターモードを有効にする

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig` で `wlan1mon` が `Mode:Monitor` になっているか確認します。

### ステップ 5: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### ステップ 1: Kali ARM64をダウンロードして書き込む

公式サイト: https://www.kali.org/get-kali/#kali-arm — Raspberry Pi 4/5 64-bit を選択。

中国国内ミラー: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

デフォルトのログイン情報: **kali / kali**

### ステップ 2: 中国国内のミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### ステップ 3: 依存関係のインストール

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### ステップ 4: ドライバのクローンとインストール

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### ステップ 5: モニターモードを有効にする

Wi-Fi内蔵のPiでは、AWUS036ACSは通常 `wlan1` として表示されます。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### ステップ 6: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1mon
```

---

## 仮想マシンでのUSBパススルー {#virtual-machine-usb-passthrough}

### VirtualBox

1. VMを終了します → **設定 → USB** → **USB 2.0 コントローラー**を有効にします。
2. **+** アイコンをクリック → **Realtek** (ID: 0bda:0811) を選択します。
3. VMを起動し、`lsusb` で `0bda:0811` が表示されることを確認してから、上記のKali Linuxの手順に従ってください。

### VMware Fusion / Workstation

1. **仮想マシン → USB と Bluetooth** → **Realtek 8811AU** を探し → **接続** をクリックします。
2. `lsusb` で認識を確認し、上記のKali Linuxの手順に従ってください。

---

## トラブルシューティング

| 問題点 | 考えられる原因 | 解決策 |
|---------|-------------|-----|
| `lsusb` に 0bda:0811 が表示されない | 電源不足またはケーブルの不具合 | 別のUSBポートを試してください |
| `install-driver.sh` が失敗する | カーネルヘッダーが不足している | `sudo apt install linux-headers-$(uname -r)` を実行してください |
| Giteeからのクローンが失敗する | ネットワークの問題 | Giteeで `8821au` を検索し、別のリポジトリを試してください |
| `airmon-ng start` が失敗する | NetworkManagerが干渉している | 最初に `sudo airmon-ng check kill` を実行してください |
| モニターモードでトラフィックが見えない | チャンネルが間違っている | チャンネルを設定します: `iwconfig wlan1mon channel 6` |
| インジェクションテストで "No Answer" | アクセスポイントが遠すぎる | もっと近づいてください。`wlan1` ではなく `wlan1mon` を使用しているか確認してください。 |

> **VIFに関する注意:** RTL8811AU ドライバは仮想インターフェース (VIF) をサポートしていません。モニターモードとマネージドモードの同時使用はできません。

## 中国国内ミラーリファレンス

| リソース | URL | 用途 |
|----------|-----|---------|
| Alfa 公式ドライバ | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバパッケージ |
| Alfa ドキュメント | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル |
| 8821au ドライバ (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | RTL8811AU ドライバ |
| 清華大学ミラー | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里巴巴（アリババ）ミラー | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (推奨) |
| 中国科学技術大学ミラー | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (推奨) |
| 華為（ファーウェイ）ミラー | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM イメージ |


---

{{< faq >}}

---

## 中国向け Alfa アダプターガイド（その他）

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF完全対応
- AWUS036ACS ← 現在のページ
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — MT7921AUN, L型
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

ご不明な点がありますか？下のコメント欄に記入するか、[yupitek.com](https://yupitek.com/ja/contact/) までお問い合わせください。

---

## 参考文献

1. [aircrack-ng公式ドキュメント](https://www.aircrack-ng.org/)
2. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
3. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
4. [Gitee rtl8812auミラー](https://gitee.com/mirrors/rtl8812au)
