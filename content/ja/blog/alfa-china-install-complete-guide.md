---

title: "完全ガイド：中国でAlfaUSB Wi-FiアダプターをLinuxにインストールする — Kali・Ubuntu・Raspberry Pi対応"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["ドライバーガイド"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "AlfaUSB Wi-FiアダプターをLinuxにインストールするための決定版ガイド。Kali Linux・Ubuntu 22/24・Debian・Raspberry Piに対応。GitHubなし — 国内ミラーのみ使用。"
featureimage: "/images/blog/alfa-china-install-complete-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "中国でAlfa WiFiアダプターをインストールするのにVPNは必要ですか？"
    answer: "不要です。USTC、Alibaba Cloud、清華などの国内ミラーとGiteeソースコードミラーを使用すれば完了までVPNは不要です。"
  - question: "モニターモードとパケットインジェクションに最も適したAlfaアダプターは？"
    answer: "AWUS036ACMはMT7612Uチップを搭載し、ドライバーはカーネル内蔵でVIFを完全サポートするため、最適な選択です。"
  - question: "WiFi 6をサポートするAlfaアダプターは？"
    answer: "AWUS036AXとAWUS036AXERはRTL8832BUチップを採用しWiFi 6をサポート、Ubuntu 24.04ではドライバー不要でプラグアンドプレイです。"
  - question: "WiFi 6EをサポートするAlfaアダプターは？"
    answer: "AWUS036AXMとAWUS036AXMLはMT7921AUNチップを採用し、WiFi 6Eトリバンドをサポートします。"
  - question: "Raspberry PiでAlfaアダプターを使う際の注意点は？"
    answer: "必ず電源付きUSB Hubで給電し、最適なドライバーサポートを得るためKali ARM64バージョンをフラッシュしてください。"
---
このページをご覧になっているということは、Alfa USB Wi-Fiアダプターを購入し、以下のような壁にぶつかっているかもしれません：

## Alfa Linux インストール完全ガイドへようこそ


{{< tldr >}}
中国本土向けAlfa WiFiアダプターLinuxインストールの究極ガイド。Kali、Ubuntu、Debian、Raspberry Piをカバーし、RTL8812AU、MT7612U、RTL8832BUなどのすべてのチップをサポート、全程国内ミラーでVPN不要です。
{{< /tldr >}}
- 中国にいるため GitHub にアクセスできない
- ドライバーのインストール手順が複雑でわからない
- 無線テスト用にモニターモードとパケットインジェクションを有効にしたい
- 自分の Alfa モデルに必要なドライバーがわからない

このガイドは、**これらすべての問題**を解決します。**すべての Alfa USB Wi-Fiアダプター**を**主要な Linux ディストリビューション**にインストールする手順を、**中国国内からアクセスできるミラーのみ**を使って解説します。GitHub 不要、ストレスなし。

---

## このガイドが存在する理由

Alfa USB Wi-Fiアダプターは、ペネトレーションテスター・ネットワークエンジニア・ワイヤレス愛好家の間で広く使われています。モニターモードとパケットインジェクションをサポートしており、これは一般的な Wi-Fi アダプターにはない機能です。

しかし問題があります：**ドライバーインストールの解説記事の多くは、GitHub にアクセスできることを前提としています**。中国にいる場合、それは不可能です。このガイドは中国のユーザー向けに特化しており、中国のインターネット環境で動作するミラーとリソースのみを使用しています。

---

## モデルクイックリファレンス

始める前に、お使いの Alfa アダプターのモデルとチップセットを確認しましょう：

### AX シリーズ（Wi-Fi 6 / 802.11ax）

| モデル | チップセット | ドライバー | 主な用途 |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | 汎用、良好な通信距離 |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | コンパクトデザイン |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | 超コンパクト |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | 強化出力 |

### AC シリーズ（Wi-Fi 5 / 802.11ac）

| モデル | チップセット | ドライバー | 主な用途 |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | 高出力、優れた通信距離 |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **VIF サポート最良**、プラグアンドプレイ |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | コストパフォーマンス重視 |

### お使いのアダプターを確認する

1. アダプター本体のラベルを確認する
2. 箱に記載されているモデル名を確認する
3. オンラインで購入した場合は注文履歴を確認する

モデルがわかったら、該当セクションに直接ジャンプするか、以下の一般的な手順に沿って進めてください。

---

## 開始前の準備

以下のものを用意してから始めてください：

1. **Alfa USB Wi-Fiアダプター** — 用途に合ったモデル
2. **USB ケーブル** — 付属品で問題ありません
3. **電源付き USB ハブ** — Raspberry Pi を使用する場合は必須
4. **有効なインターネット接続** — 中国国内のミラーにアクセスするために必要
5. **sudo 権限** — ドライバーのインストールには管理者権限が必要

まずアダプターを接続し、システムが認識しているか確認します：

```bash
lsusb
```

出力にアダプターのベンダー ID が表示されているか確認します：

- **Alfa アダプター**は `0e8d`（MediaTek）または `0bda`（Realtek）として表示されます
- 例：`Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- 例：`Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

ID が表示されていれば、アダプターは検出されています。以下のドライバーインストールセクションに進んでください。

表示されない場合は、別の USB ポートを試すか、ケーブルを交換してから `lsusb` を再実行してください。

---

## OSを選択する

お使いの OS に合ったセクションに進んでください：

- [Kali Linux](#kali-linux-のインストール)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-のインストール)
- [Debian 12 (Bookworm)](#debian-12-bookworm-のインストール)
- [Raspberry Pi OS（64ビット）](#raspberry-pi-os-のインストール)

すでにドライバーをインストール済みの場合は、応用セクションへ：

- [モニターモードを有効にする](#任意のアダプターでモニターモードを有効にする)
- [パケットインジェクションのテスト](#パケットインジェクションのテスト)
- [仮想インターフェース（VIF）サポート](#仮想インターフェースvifサポート)
- [VM の USB パススルー](#仮想マシンの-usb-パススルー)

---

## 中国でアクセス可能なミラー一覧

このガイドで使用するすべてのリソースは、以下の中国国内ミラーを利用しています：

| リソース | URL | 用途 |
|----------|-----|---------|
| **Alfa 公式ダウンロード** | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバーパッケージ、ファームウェア |
| **Alfa ドキュメント** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル（英語） |
| **清华大学镜像（Tsinghua）** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里云镜像（Aliyun）** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推奨） |
| **中科大镜像（USTC）** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推奨） |
| **华为云镜像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM イメージ（バックアップ） |
| **Gitee（GitHub の代替）** | [gitee.com](https://gitee.com) | ドライバーのソースコード |

---

## Kali Linux のインストール

Kali Linux にはワイヤレスツールがあらかじめインストールされています。Alfa アダプターを動作させるには、いくつかの手順を踏むだけです。

### ステップ 1：中国ミラーに切り替える

ソースリストを開きます：

```bash
sudo nano /etc/apt/sources.list
```

内容をすべて以下に置き換えます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：**Ctrl+O**、Enter、**Ctrl+X**。更新します：

```bash
sudo apt update
```

> **バックアップミラー：** 中科大（USTC）が遅い場合は清华（Tsinghua）を使用：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### ステップ 2：チップセットに合わせてドライバーをインストールする

#### AX シリーズ（RTL8832BU）

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC シリーズ - Realtek（RTL8812AU / RTL8811AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC シリーズ - MediaTek（MT7612U）

MT7612U ドライバーは Kali カーネルに組み込まれています。ロードされているか確認します：

```bash
lsmod | grep mt76
```

`mt76x2u` が表示されれば完了です。表示されない場合：

```bash
sudo modprobe mt76x2u
```

### ステップ 3：ドライバーの読み込みを確認する

`lsusb` を再度実行します。アダプターが表示されるはずです。次にワイヤレスインターフェースを確認します：

```bash
iwconfig
```

`wlan0` または `wlan1` が表示されれば、ドライバーは正常に動作しています。

### ステップ 4：モニターモードを有効にする

干渉するプロセスを停止します：

```bash
sudo airmon-ng check kill
```

モニターモードを開始します：

```bash
sudo airmon-ng start wlan0
```

確認します：

```bash
iwconfig
```

`Mode:Monitor` の `wlan0mon` が表示されれば成功です！

---

## Ubuntu 22.04 / 24.04 のインストール

### ステップ 1：中国ミラーに切り替える

#### Ubuntu 24.04（Noble）

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

以下に置き換えます：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

**Ctrl+O** で保存、**Ctrl+X** で終了します。

#### Ubuntu 22.04（Jammy）

```bash
sudo nano /etc/apt/sources.list
```

以下に置き換えます：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

保存して終了します。

#### パッケージインデックスを更新する

```bash
sudo apt update
```

### ステップ 2：ビルド依存関係をインストールする

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### ステップ 3：ドライバーをインストールする

#### AX シリーズ（RTL8832BU）

Gitee からクローンします：

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC シリーズ - Realtek（RTL8812AU）

Gitee からクローンします：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC シリーズ - MediaTek（MT7612U）

ドライバーは Ubuntu カーネルに組み込まれています。ロードします：

```bash
sudo modprobe mt76x2u
```

### ステップ 4：モニターモードを有効にする

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

`Mode:Monitor` の `wlan0mon` が表示されているか確認します。

---

## Debian 12 (Bookworm) のインストール

### ステップ 1：中国ミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

以下に置き換えます：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

保存して終了します。更新します：

```bash
sudo apt update
```

### ステップ 2：非フリーファームウェアをインストールする

```bash
sudo apt install -y firmware-misc-nonfree
```

### ステップ 3：ビルド依存関係をインストールする

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### ステップ 4：ドライバーをインストールする

#### AX シリーズ（RTL8832BU）

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC シリーズ - Realtek（RTL8812AU）

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC シリーズ - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### ステップ 5：Aircrack-ng をインストールする

```bash
sudo apt install -y aircrack-ng
```

### ステップ 6：モニターモードを有効にする

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

`Mode:Monitor` の `wlan0mon` が表示されているか確認します。

---

## Raspberry Pi OS のインストール

> **重要：** AWUS036ACH は約500mW、AWUS036ACM は約400mW を消費します。高負荷時に Pi がスロットリングやクラッシュを起こさないよう、**必ず電源付き USB ハブを使用してください**。

### ステップ 1：Kali Linux ARM64 イメージをダウンロードする

こちらへアクセス：https://www.kali.org/get-kali/#kali-arm

**Raspberry Pi 4（64ビット）**または**Raspberry Pi 5（64ビット）**を選択してください。32ビット版は使用しないでください — 64ビットが必要です。

> **中国ミラー：** kali.org が遅い場合は华为云を使用：https://repo.huaweicloud.com/kali-images/

### ステップ 2：MicroSD カードに書き込む

SD カードのデバイスパスを確認します：

```bash
lsblk
```

イメージを書き込みます（`/dev/sdX` は実際のカードのパスに置き換えてください）：

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

`sync` が完了するまで待ちます。Pi を起動します。デフォルトの認証情報：**kali / kali**。

### ステップ 3：中国ミラーに切り替える

```bash
sudo nano /etc/apt/sources.list
```

以下に置き換えます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存して適用します：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### ステップ 4：ドライバーをインストールする

#### AX シリーズ（RTL8832BU）

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC シリーズ - Realtek（RTL8812AU）

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC シリーズ - MediaTek（MT7612U）

```bash
sudo modprobe mt76x2u
```

### ステップ 5：モニターモードを有効にする

内蔵 Wi-Fi を搭載した Pi では、Alfa アダプターは `wlan1` として表示されます：

```bash
iwconfig
```

次に：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

`Mode:Monitor` の `wlan1mon` が表示されているか確認します。

---

## 任意のアダプターでモニターモードを有効にする

ドライバーがインストールされていれば、モニターモードの有効化は簡単です：

### ステップ 1：インターフェース名を確認する

```bash
iwconfig
```

`wlan0` または `wlan1` のどちらかをメモしておきます。

### ステップ 2：干渉するプロセスを停止する

```bash
sudo airmon-ng check kill
```

### ステップ 3：モニターモードを開始する

```bash
sudo airmon-ng start wlan0
```

インターフェース名が異なる場合は `wlan0` を実際の名前に置き換えてください。

### ステップ 4：確認する

```bash
iwconfig
```

`Mode:Monitor` の、末尾が `mon`（例：`wlan0mon`）のインターフェースが表示されているか確認します。

---

## パケットインジェクションのテスト

これにより、アダプターが細工したパケットを送信できることを確認します — ワイヤレステストに不可欠な機能です。

```bash
sudo aireplay-ng --test wlan0mon
```

**成功した場合の出力例：**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**失敗した場合：**
- 再起動してから再試行する
- 他のプロセスがインターフェースを保持していないか確認する（`iwconfig`）
- テストのため Wi-Fi AP に近づく
- `wlan0` ではなく `wlan0mon` を使用していることを確認する

---

## 仮想インターフェース（VIF）サポート

VIF（仮想インターフェース機能）を使うと、1つのアダプターで複数のインターフェースを同時に実行できます。例えば：

- **マネージドモード**（`wlan0`）と**モニターモード**（`mon0`）を同時に使用
- ネットワークに接続したまま、トラフィックをキャプチャする

### VIF をサポートするアダプター

| チップセット | VIF サポート | 備考 |
|---------|-------------|-------|
| **MT7612U（AWUS036ACM）** | ✅ フルネイティブサポート | VIF ワークフローに最適 |
| **RTL8812AU（AWUS036ACH）** | ⚠️ 限定的 | マネージド＋モニターの同時使用は不可 |
| **RTL8832BU（AX シリーズ）** | ⚠️ 限定的 | 各モデルのドキュメントを確認 |

### 仮想インターフェースの作成（MT7612U）

AWUS036ACM（MT7612U）をお使いの場合：

```bash
# wlan0 をマネージドモードに保ちながらモニターインターフェースを作成
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

両方のインターフェースがアクティブか確認します：

```bash
iwconfig
```

以下が表示されるはずです：
- `wlan0` — マネージドモード（AP に接続済み）
- `mon0` — モニターモード（全トラフィックをキャプチャ）

### ユースケース

**接続を維持しながらトラフィックをキャプチャ：**

```bash
sudo airodump-ng mon0
```

`wlan0` は通常動作を継続しながら、`mon0` がすべてをキャプチャします。

**フェイク AP ＋ モニター：**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## 仮想マシンの USB パススルー

VM 内で Linux を動かしている場合、USB アダプターをゲストに渡す必要があります。

### VirtualBox

1. VM の電源を切る
2. **設定 → USB** を開く
3. **USB 3.0（xHCI）コントローラー**を有効にする
4. **+** をクリックして USB フィルターを追加する
5. Alfa アダプターを選択する（ID：`0bda:8812` または `0e8d:7612`）
6. VM を起動する

VM 内で `lsusb` を実行して確認し、上記の Kali Linux の手順に従ってください。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. VM を起動する
2. メニュー：**仮想マシン → USB と Bluetooth**
3. Alfa アダプターを見つけて **接続** をクリックする
4. アダプターが VM 内に表示される

`lsusb` で確認してから、ドライバーインストールの手順に進んでください。

---

## トラブルシューティング

| 問題 | 考えられる原因 | 対処方法 |
|---------|-------------|-----|
| `lsusb` にアダプター ID が表示されない | ケーブル不良または電力不足 | 別の USB ポートを試す。Pi では電源付きハブを使用。 |
| `modprobe` が「Module not found」と表示される | カーネルモジュールが不足 | `sudo apt install linux-modules-extra-$(uname -r)` を実行 |
| ドライバーは動作するがモニターモードに切り替えられない | NetworkManager の干渉 | 先に `sudo airmon-ng check kill` を実行 |
| モニターモードは開始するが何もキャプチャされない | インターフェースまたはチャンネルが違う | `iwconfig` を実行。チャンネルを設定：`iwconfig wlan0mon channel 6` |
| インジェクションテストが失敗する | インターフェースが違う | `wlan0` ではなく `wlan0mon` を使用 |
| VIF の作成が失敗する | ドライバーが完全にロードされていない | アダプターを抜き差しするか、モジュールを再ロード |

---

## 付録：Alfa 全モデル一覧

| モデル | チップセット | ドライバー | 中国ミラーソース |
|-------|---------|--------|---------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | カーネル組み込みドライバー |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## まとめ

このガイドでは、**すべての Alfa USB Wi-Fi アダプター**を**主要な Linux ディストリビューション**に、**中国国内からアクセスできるリソースのみ**を使ってインストールする方法を解説しました。これで以下のことができるようになります：

✅ 任意の Alfa アダプターのドライバーをインストール  
✅ Kali・Ubuntu・Debian・Raspberry Pi でモニターモードを有効化  
✅ パケットインジェクションのテスト  
✅ 対応モデルで仮想インターフェース（VIF）を使用  
✅ VM にアダプターをパススルー  

**ご質問や問題がありますか？** シリーズの各モデル別ガイドをご確認いただくか、[yupitek.com](https://yupitek.com/ja/contact/) よりお問い合わせください。

---


---

{{< faq >}}

## 関連ガイド

この記事は **Alfa China インストールガイド**シリーズの一部です：

- [AWUS036ACH 中国インストールガイド](/ja/blog/awus036ach-china-install-guide/) — RTL8812AU、高出力
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、VIF サポート最良
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/) — RTL8811AU、コスパ重視
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/) — Wi-Fi 6、RTL8832BU
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/) — Wi-Fi 6、コンパクトデザイン
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/) — Wi-Fi 6、超コンパクト
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/) — Wi-Fi 6、強化出力
- [AWUS036EAC 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/) — RTL8814AU、高出力

---

*最終更新：2026年4月24日*

---

## 参考文献

1. [aircrack-ng公式ドキュメント](https://www.aircrack-ng.org/)
2. [Linux Kernel mt76ドライバー](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
3. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
4. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
5. [Giteeドライバーソースコードミラー](https://gitee.com/mirrors)
