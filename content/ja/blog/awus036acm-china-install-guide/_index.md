---
title: "ALFA AWUS036ACM ドライバーインストールガイド（中国向け）: Kali Linux、Ubuntu、Debian & ラズベリーパイ"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
description: "中国国内ミラーを使ってALFA AWUS036ACMドライバーをインストールするステップバイステップガイド。MT7612Uカーネル内蔵ドライバー、完全VIFサポート。Kali Linux、Ubuntu 22/24、Debian、ラズベリーパイ対応。GitHubは不要です。"
related_product: "/ja/products/alfa/awus036acm/"
---

AWUS036ACMは、LinuxでセットアップしやすいAlfaアダプターのひとつです。MT7612Uチップは`mt76x2u`ドライバーを使用しており、このドライバーはLinuxカーネルバージョン4.19以降に標準搭載されています。最新のシステムであれば、2〜3つのコマンドだけでアダプターが動作します。本ガイドでは、国内ミラーのみを使用して、ドライバーの確認・モニターモード・パケットインジェクション・VIFの完全なセットアップ手順を説明します。GitHubは不要です。

## はじめる前に

以下をご用意ください：

1. **ALFA AWUS036ACM** アダプター
2. USBケーブル（同梱のものを使用できます）
3. 給電付きUSBハブ — ラズベリーパイの場合は必須
4. 国内ミラーにアクセスできるインターネット接続

アダプターを接続し、システムが認識しているか確認します：

```bash
lsusb
```

出力から以下を探します：

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

`0e8d:7612`が表示されれば、アダプターは検出されています。下記のOSセクションに進んでください。

表示されない場合は、別のUSBポートを試すかケーブルを交換して、再度`lsusb`を実行してください。

## 使用OSを選択してください

お使いのOSの該当セクションに進んでください：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

すでにインストール済みの場合はこちらへ：

- [モニターモードを有効にする](#enable-monitor-mode)
- [パケットインジェクションのテスト](#test-packet-injection)
- [仮想インターフェース（VIF）](#virtual-interface-vif)
- [仮想マシン USBパススルー](#virtual-machine-usb-passthrough)

---

## Kali Linux

MT7612UドライバーはすでにKaliのカーネルに含まれています。ほとんどの場合、アダプターを接続した瞬間から動作します。以下の手順でドライバーの読み込みを確認し、モニターモードへの切り替えを行います。

### ステップ 1: 中国ミラーへ切り替える

ターミナルでソースリストを開きます。

```bash
sudo nano /etc/apt/sources.list
```

既存の内容を削除し、以下の行を貼り付けます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：**Ctrl+O** を押してからEnter、その後 Ctrl+X で終了します。パッケージインデックスを更新します。

```bash
sudo apt update
```

> **バックアップミラー:** 中科大（USTC）が遅い場合は、清華大学（Tsinghua）を代わりに使用してください：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### ステップ 2: ドライバーを確認する

アダプターを接続したときにモジュールが自動的に読み込まれたか確認します。

```bash
lsmod | grep mt76
```

`mt76x2u`を含む出力が表示されるはずです。何も表示されない場合は、手動で読み込みます。

```bash
sudo modprobe mt76x2u
```

再度`lsmod | grep mt76`を実行して確認します。その後、アダプターが起動しているか確認します。

```bash
iwconfig
```

無線インターフェース（通常は`wlan0`または`wlan1`）を探します。ESSIDや`unassociated`とともにインターフェースが表示されれば、ドライバーは動作しています。

---

### ステップ 2（代替）: カーネル追加モジュールのインストール

`modprobe mt76x2u`で「Module not found」エラーが出た場合、カーネルビルドにMT76モジュールが含まれていない可能性があります。中国ミラーからインストールします。

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

インストール後、再度モジュールを読み込みます。

```bash
sudo modprobe mt76x2u
```

お使いのカーネルバージョン用のパッケージが利用できない場合は、ソースからドライバーをコンパイルしてください。

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **注意:** そのGitee URLが開かない場合は、Giteeで`mt76`を検索し、最近更新されたフォークを選んでください。[files.alfa.com.tw](https://files.alfa.com.tw) からドライバーアーカイブを直接ダウンロードすることもできます。

---

### ステップ 3: モニターモードを有効にする {#enable-monitor-mode}

モニターモードに切り替える前に、システムがアダプターに割り当てたインターフェース名を確認します。

```bash
iwconfig
```

`wlan0`または`wlan1`を探します。以下のコマンドでその名前を使用します。

NetworkManagerとwpa_supplicantを停止して干渉を防ぎます。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

切り替えを確認します。

```bash
iwconfig
```

`Mode:Monitor`の`wlan0mon`のようなエントリーを探します。表示されれば、アダプターはパケットキャプチャの準備ができています。

---

### ステップ 4: パケットインジェクションのテスト {#test-packet-injection}

モニターインターフェースに対してインジェクションテストを実行します。

```bash
sudo aireplay-ng --test wlan0mon
```

成功した場合の出力は以下のようになります：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

テストが失敗した場合は、再起動して再度実行してください。それでも失敗する場合は、`iwconfig`で他のプロセスがインターフェースを使用していないか確認します。

---

## Ubuntu 22.04 / 24.04

MT7612UドライバーはUbuntuのカーネルにも含まれていますが、ベースカーネルイメージではなく`linux-modules-extra`パッケージに含まれている場合があります。以下の手順で両方の場合に対応します。

### ステップ 1: 中国ミラーへ切り替える

#### Ubuntu 24.04 (Noble)

DEB822形式のソースファイルを開きます：

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

`Ctrl+O`で保存し、`Ctrl+X`で終了します。

#### Ubuntu 22.04 (Jammy)

従来のソースファイルを開きます：

```bash
sudo nano /etc/apt/sources.list
```

すべての行を以下に置き換えます：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存して終了します（`Ctrl+O`、その後`Ctrl+X`）。

#### パッケージインデックスを更新する

```bash
sudo apt update
```

---

### ステップ 2: ドライバーを読み込む

まずモジュールを直接読み込んでみます。

```bash
sudo modprobe mt76x2u
```

「Module not found」エラーが出た場合は、追加モジュールパッケージをインストールします。

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

アダプターが認識されているか確認します。

```bash
iwconfig
```

出力に`wlan0`や`wlan1`などのインターフェースが表示されれば、ドライバーはアクティブです。

---

### ステップ 3: 無線ツールのインストール

モニターモードとインジェクションテスト用にaircrack-ngをインストールします。

```bash
sudo apt install -y aircrack-ng
```

---

### ステップ 4: モニターモードを有効にする

干渉するプロセスを停止し、モニターモードを開始します。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **注意:** 別の無線カードが存在する場合、インターフェースが`wlan1`になることがあります。最初に`iwconfig`で確認してください。

---

### ステップ 5: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan0mon
```

成功した場合は`Injection is working!`が表示されます。インターフェースエラーが出た場合は、`iwconfig wlan0mon`でモニターモードがアクティブか確認します。

---

## Debian

MT7612UドライバーはDebianカーネルに含まれていますが、完全に初期化するために`firmware-misc-nonfree`パッケージが必要な場合があります。

### ステップ 1: 中国ミラーへ切り替える

ソースリストを開きます：

```bash
sudo nano /etc/apt/sources.list
```

すべて削除し、以下の3行を貼り付けます（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

`Ctrl+O`で保存し、`Ctrl+X`で終了します。更新します：

```bash
sudo apt update
```

### ステップ 2: Non-Freeファームウェアのインストール

MT7612Uは`firmware-misc-nonfree`パッケージのファームウェアファイルを必要とします。これがないと、アダプターは初期化されますが、アソシエートやモニターモードへの切り替えができない場合があります。

```bash
sudo apt install -y firmware-misc-nonfree
```

### ステップ 3: ドライバーを読み込む

```bash
sudo modprobe mt76x2u
```

モジュールが見つからない場合は、先にカーネル追加モジュールをインストールします。

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

インターフェースが表示されたか確認します。

```bash
iwconfig
```

### ステップ 4: モニターモードを有効にする

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

`iwconfig`でモニターモードを確認します — `Mode:Monitor`の`wlan0mon`を探します。

### ステップ 5: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!`と表示されれば、アダプターは完全に動作しています。

---

## Raspberry Pi 4B / 5

> AWUS036ACMは負荷時に約400mWを消費します。Piのスロットリングを防ぐため、給電付きUSBハブを使用してください。

---

### ステップ 1: Kali Linux ARM64イメージをダウンロードする

Kali ARM公式ダウンロードページにアクセスします：
https://www.kali.org/get-kali/#kali-arm

**Raspberry Pi 4 (64-bit)** または **Raspberry Pi 5 (64-bit)** を選択します。32ビットイメージは使用しないでください — 64ビットが必要です。

> **中国ミラー:** kali.orgが遅い場合は、华为云を使用してください：
> https://repo.huaweicloud.com/kali-images/
> 最新リリースフォルダーに移動し、ARM64イメージをダウンロードします。

---

### ステップ 2: MicroSDにフラッシュする

まずカードのデバイスパスを確認します。

```bash
lsblk
```

次に、`/dev/sdX`を実際のカードパスに置き換えてフラッシュします。

```bash
# /dev/sdX を実際のSDカードに置き換えてください（lsblkで確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync`が完了するまで待ってから起動します。デフォルト認証情報：**kali / kali**。

---

### ステップ 3: 中国ミラーへ切り替える

```bash
sudo nano /etc/apt/sources.list
```

内容を以下に置き換えます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存して適用します。

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### ステップ 4: ドライバーを確認する

再起動後、アダプターを接続して確認します。

```bash
lsmod | grep mt76
```

`mt76x2u`が表示されれば完了です。表示されない場合：

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### ステップ 5: モニターモードを有効にする

内蔵Wi-Fiを搭載したPiでは、AWUS036ACMは`wlan1`として表示されます — 内蔵ラジオが`wlan0`を占有しています。

```bash
iwconfig
```

インターフェース名を確認し、そのインターフェースでモニターモードを開始します。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

`iwconfig`で確認します — `Mode:Monitor`の`wlan1mon`を探します。

---

### ステップ 6: パケットインジェクションのテスト

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!`と表示されれば完全に動作しています。失敗する場合は、給電付きハブを使用しているか再確認してください。

---

## 仮想マシン USBパススルー

### VirtualBox

1. VMの電源を切ります。**設定 → USB** に移動します。
2. **USB 3.0 (xHCI) コントローラー**を有効にします。
3. **+** をクリックしてUSBフィルターを追加します。
4. **MediaTek Inc. MT7612U**（ID: 0e8d:7612）を選択します。
5. VMを起動すると、Kali内でアダプターが表示されます。

VMで`lsusb`を実行して`0e8d:7612`を確認し、上記のKali手順に従ってください。

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. VMを起動します。
2. メニュー：**仮想マシン → USB & Bluetooth**。
3. **MediaTek MT7612U**を見つけて**接続**をクリックします。
4. VMで`lsusb`を実行して確認し、上記のKali手順に従ってください。

---

## 仮想インターフェース（VIF）

これがAWUS036ACMがACHより優れている点です。MT7612Uチップはカーネルネイティブの完全VIFサポートを持っています。パッチやハックなしに、同じアダプターでモニターインターフェースとマネージドまたはAPインターフェースを同時に実行できます。

### 2つ目の仮想インターフェースを作成する

アダプターが`wlan0`としてマネージドモードで動作している状態で、その横にモニターインターフェースを追加します。

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

両方のインターフェースがアクティブか確認します。

```bash
iwconfig
```

`wlan0`（アソシエート済み、マネージドモード）と`mon0`（モニターモード）の両方が表示されるはずです。アダプターは同時に両方を実行しています。

### ユースケース：接続を維持しながらモニタリング

`wlan0`がネットワークに接続したままの状態で、`mon0`でトラフィックをキャプチャできます — 相関分析に便利です。

```bash
sudo airodump-ng mon0
```

`wlan0`は通常のアソシエーションを続けながら、`mon0`が範囲内のすべてをキャプチャします。

### ユースケース：フェイクAP + モニター

APインターフェースとモニターインターフェースを一緒に作成します。

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

`iwconfig`を実行して、3つのインターフェース（`wlan0`、`ap0`、`mon0`）がすべてアクティブか確認します。

> **hostapdについての注意:** 完全なAP動作にはhostapdの設定が必要です。それはこのガイドの範囲外です。上記の手順はアダプターがインターフェースを作成できることを確認するものです — 実際のAP設定は別のトピックです。

---

## トラブルシューティング

| 問題 | 考えられる原因 | 解決策 |
|------|--------------|--------|
| `lsusb`に0e8d:7612が表示されない | アダプターに電源が供給されていないか、ケーブルが不良 | 別のUSBポートを試す。ラズベリーパイでは給電付きハブを使用する。 |
| `modprobe mt76x2u`で「Module not found」と表示される | カーネルに追加モジュールがない | `sudo apt install linux-modules-extra-$(uname -r)`を実行する |
| インターフェースは表示されるがアソシエートできない | ファームウェアファイルが欠落している | `sudo apt install firmware-misc-nonfree`を実行する（Debian） |
| `airmon-ng start wlan0`が失敗する | NetworkManagerがまだ実行中 | 先に`sudo airmon-ng check kill`を実行する |
| モニターモードは起動するがトラフィックがキャプチャされない | チャンネルまたはインターフェース名が間違っている | チャンネルを設定する：`iwconfig wlan0mon channel 6` |
| インジェクションテストで「No Answer」と表示される | APが遠すぎるかインターフェースが間違っている | APに近づく。`wlan0`ではなく`wlan0mon`を使用する。 |
| VIFインターフェースの作成に失敗する | ドライバーが完全に読み込まれていない | アダプターを抜いてモジュールを再読み込みする：`sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## 中国ミラーリファレンス

このガイドで使用するすべてのリソース — GitHubは不要：

| リソース | URL | 用途 |
|---------|-----|-----|
| Alfa公式ドライバー | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバーパッケージ、ファームウェア |
| Alfaドキュメント | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル |
| 清華大学ミラー | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| アリクラウドミラー | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推奨） |
| 中科大ミラー | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推奨） |
| 华为云ミラー | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARMイメージ（バックアップ） |
| MT76ドライバー（Gitee） | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | 手動コンパイルの代替 |

## 中国向けAlfaアダプターガイド一覧

これは**Alfa China Install Guide**シリーズの一部です。各記事で1つのアダプターモデルを取り上げています：

- [AWUS036ACH 中国向けインストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- AWUS036ACM ← 現在のページ
- [AWUS036ACS 中国向けインストールガイド](/ja/blog/awus036acs-china-install-guide/)
- [AWUS036AX 中国向けインストールガイド](/ja/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 中国向けインストールガイド](/ja/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 中国向けインストールガイド](/ja/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 中国向けインストールガイド](/ja/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 中国向けインストールガイド](/ja/blog/awus036eacs-china-install-guide/)

ご質問はコメント欄またはこちらからどうぞ：[yupitek.com/ja/contact/](https://yupitek.com/ja/contact/)
