---
title: "ALFA AWUS036ACH ドライバーインストールガイド（中国向け）: Kali Linux、Ubuntu、Debian & ラズベリーパイ"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
description: "国内ミラーを使ってALFA AWUS036ACHドライバーを中国でインストールするステップバイステップガイド。Kali Linux、Ubuntu 22/24、Debian、ラズベリーパイ対応。GitHubなし。"
related_product: "/ja/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACHはどのチップを使っていますか？ドライバーの追加インストールは必要ですか？"
    answer: "AWUS036ACHはRealtek RTL8812AUチップを採用し、ドライバーはLinuxカーネルに内蔵されていないため手動インストールが必要です。"
  - question: "中国でAWUS036ACHドライバーをインストールするのにVPNは必要ですか？"
    answer: "不要です。USTC、Alibaba Cloudなどの国内ミラーとGiteeソースコードミラーを使用すればインストール完了までVPNは不要です。"
  - question: "AWUS036ACHはモニターモードとパケットインジェクションをサポートしていますか？"
    answer: "サポートしています。RTL8812AUドライバーインストール後、airmon-ngでモニターモードを有効化し、aireplay-ngでパケットインジェクションをテストできます。"
  - question: "AWUS036ACHはRaspberry Piで使えますか？"
    answer: "使えます。電源付きUSB Hubを組み合わせ、Kali ARM64バージョンをフラッシュして使用することを推奨します。"
  - question: "Kali LinuxでAWUS036ACHドライバーをインストールするコマンドは？"
    answer: "Kaliではsudo apt install realtek-rtl88xxau-dkmsを直接実行してプレビルドドライバーをインストールできます。"
---

AWUS036ACHを入手したのに、Linuxがデバイスを認識しない。よくある話です。このチップにはRTL8812AUドライバーが必要で、最初からは動きません。このガイドでは、国内ミラーだけを使って約30分でセットアップを完了させます。GitHubへのアクセスは不要です。


{{< tldr >}}
AWUS036ACHはRTL8812AUチップを採用し、KaliではaptでDKMSドライバーをインストール、Ubuntu/DebianではGiteeからコンパイル、30分でモニターモードとパケットインジェクションを利用できます。
{{< /tldr >}}

以下を用意してください：

## 準備するもの

以下を用意してください：

1. **ALFA AWUS036ACH** アダプター
2. USBケーブル（付属品で問題ありません）
3. セルフパワーUSBハブ — ラズベリーパイ使用時は必須
4. 国内ミラーに接続できるインターネット環境

アダプターを接続したら、システムが認識しているか確認します：

```bash
lsusb
```

出力の中に以下の行があるか探してください：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

`0bda:8812` が表示されれば、アダプターは認識されています。下のOSセクションへ進んでください。

表示されない場合は、別のUSBポートに差し替えるかケーブルを交換して、再度 `lsusb` を実行してください。

## OSを選択する

お使いのOSに合わせてセクションに移動してください：

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [ラズベリーパイ 4B / 5](#ラズベリーパイ-4b--5)

インストール済みの場合はこちらへ：

- [モニターモードの有効化](#モニターモードの有効化)
- [パケットインジェクションのテスト](#パケットインジェクションのテスト)
- [VM USBパススルー](#仮想マシンusbパススルー)

---

## Kali Linux

Kaliには強力なワイヤレスツールが標準で含まれています。AWUS036ACHドライバーを動かすには4つのステップで完了します。まず高速な国内ミラーに切り替えて、ダウンロードを快適にしましょう。

### ステップ1：中国ミラーに切り替える

ターミナルでソースリストを開きます。

```bash
sudo nano /etc/apt/sources.list
```

既存の内容を全て削除して、以下の1行を貼り付けます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存は **Ctrl+O**、Enterキー、そして Ctrl+X で終了します。パッケージインデックスを更新します。

```bash
sudo apt update
```

> **バックアップミラー：** 中科大（USTC）が遅い場合は、清華大学（Tsinghua）を使ってください：
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### ステップ2：ドライバーをインストールする

KaliのパッケージリポジトリにはDKMSドライバーが含まれています。1つのコマンドでインストールできます。

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMSはカーネルがアップデートされるたびに自動的にドライバーを再コンパイルするので、アップグレード後に手動で再インストールする必要はありません。

ドライバーが正しく読み込まれているか確認します。

```bash
modinfo 88XXau | grep -E "filename|version"
```

`filename` が `.ko` で終わる行と、`5.6.4.2` のようなバージョン文字列が表示されれば、ドライバーは準備完了です。

---

### ステップ2（代替）：ソースからの手動コンパイル

上記の `apt install` が失敗した場合のみ、このセクションを実行してください。まずビルド依存関係をインストールします。

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Giteeからドライバーのソースコードをダウンロードします。

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **注意：** そのURLが開かない場合は、Giteeで `rtl8812au` を検索して、最近更新されたフォークを選んでください。[files.alfa.com.tw](https://files.alfa.com.tw) からソースアーカイブを直接ダウンロードすることもできます。

クローンしたディレクトリに移動して、コンパイルとインストールを実行します。

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

実行中のカーネルにドライバーを読み込みます。

```bash
sudo modprobe 88XXau
```

---

### ステップ3：モニターモードを有効にする {#モニターモードの有効化}

アダプターをモニターモードに切り替える前に、システムが割り当てたインターフェース名を確認します。

```bash
iwconfig
```

`wlan0` または `wlan1` のエントリを探してください。以下のコマンドではその名前を使用します。

NetworkManagerとwpa_supplicantを停止します。両方ともアダプターを占有してモニターモードをブロックします。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

切り替えが成功したか確認します。

```bash
iwconfig
```

`Mode:Monitor` と表示された `wlan0mon` のエントリがあれば、アダプターはパケットキャプチャの準備ができています。

---

### ステップ4：パケットインジェクションをテストする {#パケットインジェクションのテスト}

モニターインターフェースに対してインジェクションテストを実行します。

```bash
sudo aireplay-ng --test wlan0mon
```

成功すると以下のように表示されます：

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

テストが失敗した場合は、マシンを再起動してもう一度テストしてください。再起動後も失敗する場合は、他のプロセスがインターフェースを保持していないか確認してください。`iwconfig` を実行して `wlan0mon` だけが表示されているか、別のプロセスがアダプターを使用していないことを確認してください。

---

## Ubuntu 22.04 / 24.04

Ubuntuはバージョンによってパッケージファイル形式が異なる2つのブランチがあります。以下の手順は両方に対応しています。ミラーには**阿里云（Aliyun）**を使います。高速で信頼性が高く、Alibabaが管理しています。

### ステップ1：中国ミラーに切り替える

Ubuntuのバージョンに合わせて、該当する手順だけを実行してください。

#### Ubuntu 24.04 (Noble)

新しいDEB822形式のソースファイルを開きます：

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

ファイルの内容を全て削除して、以下を正確に貼り付けます：

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

`Ctrl+O` で保存し、`Ctrl+X` で終了します。

#### Ubuntu 22.04 (Jammy)

代わりに従来のソースファイルを開きます：

```bash
sudo nano /etc/apt/sources.list
```

既存の行を全て以下に置き換えます：

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

同様に保存して終了します（`Ctrl+O`、`Ctrl+X`）。

#### パッケージインデックスを更新する

ソースファイルを編集した後、どちらのバージョンでも実行してください：

```bash
sudo apt update
```

---

### ステップ2：ビルド依存関係をインストールする

ドライバーはソースからコンパイルするため、カーネルヘッダーとビルドツールが必要です：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

これによりgcc、make、そして実行中のカーネルに合ったヘッダーが取得されます。`$(uname -r)` の部分がカーネルバージョンを自動検出するので、手動で入力する必要はありません。

---

### ステップ3：ドライバーソースをダウンロードする（中国ミラー）

中国国内でアクセス可能なGiteeからドライバーリポジトリをクローンします：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

クローンしたフォルダに移動します：

```bash
cd rtl8812au
```

> **注意：** URLがタイムアウトするか404が返る場合は、[gitee.com](https://gitee.com) で `rtl8812au` を検索して、最新のコミット日付があるフォークを選んでください。

---

### ステップ4：コンパイルとインストール

ソースからカーネルモジュールをビルドします：

```bash
make
```

システムにインストールします：

```bash
sudo make install
```

カーネルアップグレード後も動作するようDKMSに登録します：

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

実行中のカーネルにモジュールを読み込みます：

```bash
sudo modprobe 88XXau
```

モジュールが正しく読み込まれているか確認します：

```bash
modinfo 88XXau | grep filename
```

`88XXau.ko` で終わるパスが表示されれば、ドライバーは有効です。

---

### ステップ5：モニターモードを有効にする

ワイヤレスインターフェースに干渉するプロセスを終了します：

```bash
sudo airmon-ng check kill
```

アダプターをモニターモードに切り替えます：

```bash
sudo airmon-ng start wlan0
```

> **注意：** インターフェース名が `wlan0` ではなく `wlan1` の場合があります。`iwconfig` を実行してワイヤレスインターフェースの一覧を確認し、上のコマンドで正しい名前に置き換えてください。

---

### ステップ6：パケットインジェクションをテストする

アダプターがモニターモードになったら、インジェクションテストを実行します：

```bash
sudo aireplay-ng --test wlan0mon
```

成功すると `Injection is working!` のような行が表示されます。インターフェースに関するエラーが出た場合は、`iwconfig wlan0mon` でモニターモードが有効か確認してください。

---

## Debian

Debianのパッケージマネージャーはデフォルトで海外サーバーを指しています。清華大学（Tsinghua University）ミラーに切り替えることで、ダウンロード速度が劇的に改善されます。

### ステップ1：中国ミラーに切り替える

ソースリストを開きます：

```bash
sudo nano /etc/apt/sources.list
```

中身を全て削除して、以下の3行を貼り付けます（Debian 12 Bookworm）：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

`Ctrl+O` で保存し、`Ctrl+X` で終了します。パッケージインデックスを更新します：

```bash
sudo apt update
```

### ステップ2：ビルド依存関係をインストールする

AWUS036ACHドライバーはソースからコンパイルするため、カーネルヘッダーとビルドツールが必要です：

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

このコマンドは実行中のカーネルバージョンに合ったヘッダーパッケージを自動的にインストールします。

### ステップ3：ドライバーソースをダウンロードする（中国ミラー）

Giteeからドライバーリポジトリをクローンします：

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

プロジェクトフォルダに移動します：

```bash
cd rtl8812au
```

> **URLにアクセスできない場合？** Giteeで `rtl8812au` を検索して、最近更新されたフォークを選んでください。

### ステップ4：コンパイルとインストール

`rtl8812au` フォルダ内で以下のコマンドを順番に実行します：

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` がドライバーを登録するので、カーネルアップデート後も自動的に機能し続けます。

### ステップ5：モニターモードを有効にする

モードを切り替える前に**干渉するプロセスを終了**します：

```bash
sudo airmon-ng check kill
```

アダプターでモニターモードを開始します：

```bash
sudo airmon-ng start wlan0
```

`airmon-ng` がない場合は先にインストールします：

```bash
sudo apt install -y aircrack-ng
```

インターフェースが起動したか確認します：

```bash
iwconfig
```

出力に `wlan0mon` という名前のインターフェースがあるか確認してください。

### ステップ6：パケットインジェクションをテストする

```bash
sudo aireplay-ng --test wlan0mon
```

インジェクションテスト結果が連続して表示されれば、アダプターは正常に動作しています。準備完了です。

---

## ラズベリーパイ 4B / 5

> AWUS036ACHは約500mWの電力を消費します。ラズベリーパイのUSBポートに直接接続すると、負荷時にPiが制限をかけたり再起動したりすることがあります。**必ずセルフパワーUSBハブを使用してください。**

---

### ステップ1：Kali Linux ARM64イメージをダウンロードする

公式のKali ARMダウンロードページにアクセスします：
https://www.kali.org/get-kali/#kali-arm

お使いのボードに合わせて **Raspberry Pi 4 (64-bit)** または **Raspberry Pi 5 (64-bit)** を選択してください。32ビットイメージはダウンロードしないでください。ドライバーのビルドには64ビットカーネルが必要です。

> **中国ミラー：** kali.orgの読み込みが遅い場合は、华为云を代わりに使ってください：
> https://repo.huaweicloud.com/kali-images/
> 最新リリースフォルダを参照して、同じARM64イメージをダウンロードしてください。

---

### ステップ2：microSDにフラッシュする

microSDカードを挿入して、書き込む前にデバイスパスを確認します。

```bash
lsblk
```

リストからカードを見つけます。`sdb` または `mmcblk0` のような形式で表示されます。次に `/dev/sdX` を実際のパスに置き換えてイメージを書き込みます。

```bash
# /dev/sdX を実際のSDカードに置き換えてください（lsblkで確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

カードを抜く前に `sync` が完了するまで待ってください。SDカードからPiを起動します。起動後のデフォルト認証情報：**kali / kali**。

---

### ステップ3：中国ミラーに切り替える

初回起動後、パッケージソースファイルを開きます。

```bash
sudo nano /etc/apt/sources.list
```

ファイルの内容を全て削除して、以下の1行に置き換えます：

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

保存：**Ctrl+O**、Enter、Ctrl+X。ミラーを適用してシステムをアップグレードします。

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

再起動でドライバーインストール前のカーネルアップデートを適用します。

---

### ステップ4：ドライバーをインストールする（ARM64）

DKMSパッケージはARM64でもx86と全く同じように動作します。特別な手順は必要ありません。

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

そのコマンドでパッケージが見つからないというエラーが返った場合は、代わりにソースからドライバーをコンパイルします。

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### ステップ5：モニターモードを有効にする

アダプターを操作する前に、Piが割り当てたインターフェース名を確認します。

```bash
iwconfig
```

内蔵Wi-Fiチップを持つPiでは、AWUS036ACHは `wlan1` として表示されます。内蔵ラジオが `wlan0` を占有しています。`iwconfig` で報告された名前を使用してください。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

再度 `iwconfig` を実行して、`Mode:Monitor` と表示された `mon` で終わるエントリ（通常のPiでは `wlan1mon`）があるか確認してください。これでアダプターが正常に切り替わったことが確認できます。

---

### ステップ6：パケットインジェクションをテストする

```bash
sudo aireplay-ng --test wlan1mon
```

`wlan1mon` はステップ5で表示されたモニターインターフェース名に置き換えてください。正常なアダプターは `Injection is working!` と表示します。テストが失敗した場合は再起動してもう一度試してください。Pi上での最も一般的な原因は、非セルフパワーハブを経由した悪いUSB接続です。セルフパワーハブを使用していることを再確認してください。

---

## 仮想マシンUSBパススルー

macOSまたはWindowsのVM上でKali Linuxを実行していますか？USBアダプターをゲストOSにパススルーする必要があります。

### VirtualBox

1. VMの電源をオフにして、**設定 → USB** に移動します。
2. **USB 3.0 (xHCI) コントローラー** を有効にします。
3. **+** アイコンをクリックしてUSBフィルターを追加します。
4. **Realtek 802.11ac NIC [...]**（ID: 0bda:8812）を選択します。
5. VMを起動すると、アダプターがKali内に表示されます。

VM内で `lsusb` を実行して `0bda:8812` が表示されることを確認し、上記のKali Linuxの手順に従ってください。

### VMware Fusion（macOS）/ VMware Workstation（Windows）

1. VMを起動します。
2. メニューから：**仮想マシン → USB & Bluetooth** を選択します。
3. **Realtek 802.11ac NIC** を見つけて **接続** をクリックします。
4. アダプターがホストから切断され、VM内に表示されます。

VM内で `lsusb` を実行して確認し、上記のKali Linuxの手順に従ってください。

### VIF（仮想インターフェース）について

AWUS036ACHに搭載されたRTL8812AUチップは、Linux上でのVIFサポートが限定的です。同じアダプター上でマネージドモードとモニターモード（またはAPモード）を同時に信頼性高く実行することはできません。

ワークフローでVIFが必要な場合（例：偽APを実行しながら同時にモニタリングする場合）、AWUS036ACHは適切なツールではありません。代わりに [AWUS036ACM インストールガイド](/ja/blog/awus036acm-china-install-guide/) をご確認ください。そのアダプターはMT7612Uチップを使用しており、完全なカーネルネイティブVIFサポートを持ち、パッチなしで同時仮想インターフェースを処理できます。

---

## トラブルシューティング

| 問題 | 考えられる原因 | 解決方法 |
|------|--------------|---------|
| `lsusb` に 0bda:8812 が表示されない | アダプターが給電されていない、またはケーブルが不良 | 別のUSBポートを試してください。ラズベリーパイではセルフパワーハブを使用してください。 |
| `make` がヘッダーエラーで失敗する | カーネルヘッダーが見つからないかバージョンが一致しない | `sudo apt install linux-headers-$(uname -r)` を実行してください |
| `modprobe 88XXau` が失敗する | Secure Bootが未署名モジュールをブロックしている | BIOSでSecure Bootを無効にするか、モジュールに署名してください |
| カーネルアップデート後にドライバーが消える | ドライバーがDKMSに登録されていない | ソースディレクトリから `sudo dkms install rtl8812au/$(cat VERSION)` を再実行してください |
| `airmon-ng start wlan0` が失敗する | NetworkManagerがまだ実行中 | 先に `sudo airmon-ng check kill` を実行してください |
| モニターモードが開始されるがトラフィックをキャプチャしない | チャンネルまたはインターフェース名が違う | `iwconfig` でインターフェースを確認し、チャンネルを設定：`iwconfig wlan0mon channel 6` |
| インジェクションテストで "No Answer" と表示される | APが遠すぎるか、インターフェース名が間違っている | APに近づいてください。`wlan0` ではなく `wlan0mon` を使用してください |

## 中国ミラーリファレンス

このガイドで使用するリソース一覧。GitHubは一切不要です：

| リソース | URL | 用途 |
|---------|-----|------|
| Alfa公式ドライバー | [files.alfa.com.tw](https://files.alfa.com.tw) | ドライバーパッケージ、ファームウェア |
| Alfaドキュメント | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | 製品マニュアル |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu（推奨） |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali（推奨） |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARMイメージ（バックアップ） |
| RTL8812AUドライバー（Gitee） | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | 手動コンパイルの代替 |


---

{{< faq >}}

---

## 中国向けAlfaアダプターガイド

このガイドは **Alfa中国インストールガイド** シリーズの一部です。各記事は1つのアダプターモデルをカバーしています：

- AWUS036ACH ← 現在のページ
- [AWUS036ACM 中国インストールガイド](/ja/blog/awus036acm-china-install-guide/) — MT7612U、最良のVIFサポート
- [AWUS036ACS 中国インストールガイド](/ja/blog/awus036acs-china-install-guide/)
- [AWUS036AX 中国インストールガイド](/ja/blog/awus036ax-china-install-guide/)
- [AWUS036AXER 中国インストールガイド](/ja/blog/awus036axer-china-install-guide/)
- [AWUS036AXM 中国インストールガイド](/ja/blog/awus036axm-china-install-guide/)
- [AWUS036AXML 中国インストールガイド](/ja/blog/awus036axml-china-install-guide/)
- [AWUS036EAC 中国インストールガイド](/ja/blog/awus036eacs-china-install-guide/)

ご質問はコメント欄か [yupitek.com](https://yupitek.com/ja/contact/) よりお気軽にどうぞ。

---

## 参考文献

1. [aircrack-ng公式ドキュメント](https://www.aircrack-ng.org/)
2. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
3. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
4. [Gitee rtl8812auミラー](https://gitee.com/mirrors/rtl8812au)
5. [Realtek RTL8812AUドライバー](https://www.realtek.com/)
