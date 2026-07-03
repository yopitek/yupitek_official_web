---

title: "ALFA AWUS036ACH セットアップガイド：Kali Linux モニターモード・パケットインジェクション設定"
description: "ALFA AWUS036ACH を Kali Linux 2024/2025 で使用するための完全セットアップガイド。RTL8812AU ドライバーインストール、airmon-ng によるモニターモード有効化、パケットインジェクション確認手順。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "モニターモード", "パケットインジェクション", "RTL8812AU", "airmon-ng"]
featureimage: "/images/blog/awus036ach-kali-linux-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036ACHはKali Linuxでドライバーの追加インストールが必要ですか？"
    answer: "必要です。RTL8812AUはメインラインカーネルドライバーではなく、aircrack-ng GitHubリポジトリからインストールする必要があります。DKMSの使用を推奨し、カーネル更新後も動作し続けます。"
  - question: "AWUS036ACHがシステムに認識されているかどう確認しますか？"
    answer: "lsusbコマンドを実行し、ID 0bda:8812を探してRealtek RTL8812AUが認識されていることを確認し、lsmodでドライバーモジュールが読み込まれていることを確認します。"
  - question: "モニターモード有効化後にインターフェースが消えたらどうしますか？"
    answer: "通常はNetworkManagerがインターフェースを再取得したことが原因です。airmon-ng check killを実行して干渉プロセスを終了し、再度モニターモードを有効化してください。"
  - question: "パケットインジェクションテストの成功率はどのくらいなら正常ですか？"
    answer: "成功率80%以上で信頼できる動作を示します。50%未満の場合はアンテナ位置、USB給電の充足性、ドライバーの正しいインストールを確認してください。"
  - question: "カーネル更新後にAWUS036ACHドライバーが無効になったらどう対処しますか？"
    answer: "DKMSでインストールしていればドライバーは自動リビルドされます。無効になった場合はdkms autoinstallを実行し、linux-headersパッケージが現在のカーネルバージョンと一致していることを確認してください。"
---
ALFA AWUS036ACH は、Kali Linux を使ったワイヤレスセキュリティ診断において世界中のセキュリティ研究者・ペネトレーションテスターが愛用する USB WiFi アダプターです。RTL8812AU チップセットを搭載し、デュアルバンド（2.4 GHz / 5 GHz）に対応。aircrack-ng コミュニティが長年にわたってメンテナンスしているドライバーにより、安定したモニターモードとパケットインジェクションが実現します。

## はじめに


{{< tldr >}}
AWUS036ACHはRTL8812AUチップを搭載し、aircrack-ngドライバーとDKMSインストールの組み合わせでモニターモードとパケットインジェクションを安定して有効化でき、Kali Linuxペネトレーションテストの標準装備です。
{{< /tldr >}}
本ガイドでは、Kali Linux 2024.x / 2025.x 環境で AWUS036ACH を一から設定し、実際にペネトレーションテストで使える状態にするまでの全手順を解説します。

---

## 前提条件

作業を始める前に、以下の環境・機材が揃っていることを確認してください。

| 項目 | 要件 |
|---|---|
| OS | Kali Linux 2024.1 以降（2025.x 推奨） |
| カーネル | 5.15 以降 |
| USB ポート | USB 3.0（USB 2.0 でも動作するが速度低下あり） |
| アダプター | ALFA AWUS036ACH |
| インターネット接続 | ドライバーのダウンロードに必要 |
| 権限 | sudo 権限を持つアカウント |

> **注意**：仮想マシン（VirtualBox / VMware）で使用する場合は、USB コントローラーの設定を USB 3.0 に変更し、アダプターをゲスト OS へパススルーする設定が別途必要です。

---

## ステップ 1：アダプターの接続と認識確認

AWUS036ACH を PC の USB ポートに接続します。付属のアンテナ2本を本体に取り付けてから接続することを推奨します。

### USB デバイスの確認

```bash
lsusb
```

出力の中に以下のような行が表示されれば、OS がアダプターを認識しています。

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Vendor ID `0bda`、Product ID `8812` が RTL8812AU の識別子です。

### カーネルログの確認

```bash
dmesg | grep -i rtl
```

ドライバーがロードされていれば、チップセット名やファームウェア読み込みに関するメッセージが表示されます。この時点では標準ドライバーがロードされていない場合もありますが、問題ありません。

---

## ステップ 2：RTL8812AU ドライバーのインストール

Kali Linux の標準カーネルには RTL8812AU の完全なモニターモード対応ドライバーが含まれていません。aircrack-ng チームが提供するサードパーティドライバーをインストールします。

### 依存パッケージのインストール

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  dkms \
  git \
  build-essential \
  linux-headers-$(uname -r)
```

`linux-headers-$(uname -r)` は現在実行中のカーネルバージョンに対応するヘッダーファイルをインストールします。カーネルをアップデートした場合は再度このコマンドを実行してください。

### ドライバーソースのクローン

```bash
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
```

### DKMS を使ったインストール

DKMS（Dynamic Kernel Module Support）を使うと、カーネルアップデート時にドライバーが自動的に再ビルドされるため管理が楽になります。

```bash
sudo make dkms_install
```

インストールには数分かかります。完了後、以下のコマンドで DKMS への登録を確認します。

```bash
dkms status
```

`rtl8812au` が `installed` 状態で表示されれば成功です。

### モジュールの手動ロード（再起動なしで確認したい場合）

```bash
sudo modprobe 88XXau
```

---

## ステップ 3：モニターモードの有効化

モニターモードを有効化する方法は2つあります。それぞれの特徴を理解した上で使い分けてください。

### 方法 A：airmon-ng を使う方法（推奨）

airmon-ng は Aircrack-ng スイートに含まれるツールで、モニターモードの管理を簡単に行えます。

#### 干渉プロセスの停止

NetworkManager や wpa_supplicant がアダプターを制御していると、モニターモードへの移行が妨げられます。

```bash
sudo airmon-ng check kill
```

このコマンドは干渉している可能性のあるプロセスを表示し、停止します。出力例：

```
Killing these processes:

  PID Name
  892 NetworkManager
  934 wpa_supplicant
```

#### モニターモードの開始

```bash
sudo airmon-ng start wlan0
```

`wlan0` の部分はご自身の環境のインターフェース名に合わせてください（`wlan1` など）。正常に完了すると `wlan0mon` という新しいインターフェースが作成されます。

### 方法 B：iw コマンドを使う方法

iw はより低レベルなネットワーク設定コマンドです。

```bash
# インターフェースをダウン
sudo ip link set wlan0 down

# モードをモニターに変更
sudo iw wlan0 set monitor control

# インターフェースをアップ
sudo ip link set wlan0 up
```

iw を使う場合、インターフェース名は `wlan0mon` ではなく `wlan0` のままです。

---

## ステップ 4：動作確認（iwconfig）

```bash
iwconfig
```

出力例：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

`Mode:Monitor` が表示されていればモニターモードは正常に有効化されています。`Power Management:off` になっていることも確認してください。オンのままだとパケットキャプチャが不安定になる場合があります。

### 特定の周波数帯でモニターモードを有効化する

5 GHz 帯のみを対象としたい場合は、チャンネルを指定します。

```bash
# 5 GHz 帯のチャンネル 36（5180 MHz）に設定
sudo airmon-ng start wlan0 36
```

---

## ステップ 5：パケットインジェクションテスト

パケットインジェクションが正常に機能するかどうかを確認します。

```bash
sudo aireplay-ng --test wlan0mon
```

成功した場合の出力例：

```
21:03:18  Trying broadcast probe requests...
21:03:18  Injection is working!
21:03:19  Found 3 APs

21:03:19  Trying directed probe requests...
21:03:19  XX:XX:XX:XX:XX:XX - channel: 6 - 'HomeNetwork'
21:03:20  30/30: 100%

21:03:21  Injection is working!
```

`Injection is working!` が2回表示されれば、ブロードキャストおよびユニキャスト両方のインジェクションが正常に動作しています。

### 5 GHz 帯でのインジェクションテスト

```bash
# まず 5 GHz チャンネルに合わせる
sudo iwconfig wlan0mon channel 36

# テスト実行
sudo aireplay-ng --test wlan0mon
```

---

## 作業後：通常モードへの復帰

ペネトレーションテスト終了後は、アダプターを通常のマネージドモードに戻します。

```bash
# モニターモードの停止
sudo airmon-ng stop wlan0mon

# NetworkManager の再起動
sudo systemctl start NetworkManager
```

---

## トラブルシューティング

### アダプターが認識されない

`lsusb` に表示されない場合は、別の USB ポートを試してください。USB ハブ経由での接続は電力不足になる可能性があります。可能であれば PC 本体のポートに直接接続してください。

### ドライバーのビルドに失敗する

```
ERROR: Kernel configuration is invalid.
```

このエラーが出た場合は、カーネルヘッダーが正しくインストールされているか確認します。

```bash
ls /usr/src/linux-headers-$(uname -r)
```

ディレクトリが存在しない場合は再インストールしてください。

```bash
sudo apt install --reinstall linux-headers-$(uname -r)
```

### モニターモードに移行できない

`airmon-ng check` で干渉プロセスをすべて停止した後、再試行してください。それでも失敗する場合は `rfkill` によるソフトブロックを確認します。

```bash
rfkill list
sudo rfkill unblock wifi
```

### パケットインジェクションが失敗する

テスト対象の AP が存在するチャンネルにアダプターが合っていない場合、インジェクションが失敗することがあります。`airodump-ng` で対象チャンネルを確認してから再テストしてください。

```bash
sudo airodump-ng wlan0mon
```

### カーネルアップデート後にドライバーが動かない

DKMS でインストールした場合は通常自動的に再ビルドされますが、手動でトリガーすることもできます。

```bash
sudo dkms autoinstall
```

---


---

{{< faq >}}

## まとめ

本ガイドの手順に従うことで、ALFA AWUS036ACH を Kali Linux 上でモニターモード・パケットインジェクション対応の状態で使用できるようになります。

設定の流れをまとめると：

1. `lsusb` でアダプターの認識を確認
2. aircrack-ng 版 RTL8812AU ドライバーを DKMS でインストール
3. `airmon-ng check kill` で干渉プロセスを停止
4. `airmon-ng start wlan0` でモニターモードを有効化
5. `iwconfig` で `Mode:Monitor` を確認
6. `aireplay-ng --test wlan0mon` でインジェクション動作を確認

AWUS036ACH の製品詳細・仕様・購入については、[ALFA AWUS036ACH 製品ページ](/ja/products/alfa/awus036ach/) をご覧ください。

---

## 参考文献

1. [aircrack-ng公式rtl8812auドライバーリポジトリ](https://github.com/aircrack-ng/rtl8812au)
2. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
3. [Realtek RTL8812AU仕様説明](https://www.realtek.com/)
4. [Linux Wireless公式ドキュメント](https://wireless.wiki.kernel.org/)
