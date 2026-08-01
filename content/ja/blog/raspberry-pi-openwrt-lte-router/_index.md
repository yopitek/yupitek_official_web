---
title: "Raspberry Pi + OpenWrt で作る 4G/5G ルーター：Sierra モジュール対応マトリクスと実装ガイド"
description: "Raspberry Pi と Sierra Wireless 4G/5G モジュール（EM7455、EM7565、EM7511、EM919x、MC7455）で OpenWrt ルーターを自作するための完全対応マトリクス、QMI/MBIM 設定、wwan0 での接続手順、電源とアンテナの注意点を解説します。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/ja/products/sierra/"
faq:
  - question: "Raspberry Pi で OpenWrt ルーターを作る場合、Sierra モジュールはどれを選べばよいですか？"
    answer: "初心者は情報の多い EM7455 を推奨します。アップロード速度を重視する場合は EM7565/EM7511、5G が必要な場合は EM919x、旧型の mPCIe スロットには MC7455 を選んでください。"
  - question: "QMI と MBIM の違いは何ですか？"
    answer: "QMI は Qualcomm 独自のプロトコル、MBIM は後発の標準化されたプロトコルです。OpenWrt ではどちらも利用できますが、ネット上のガイドは QMI が中心です。"
  - question: "Raspberry Pi がモジュールを認識しない場合はどうすればよいですか？"
    answer: "多くの場合、Raspberry Pi の USB 電源が不足しています（突入電流は最大 2.5A に達することがあります）。アダプターボードの給電とケーブルを確認し、デバイスが起動を完了するまで 10 秒ほど待ってください。"
---

Raspberry Pi に Sierra Wireless の 4G/5G モジュールを接続して OpenWrt ルーターを構築できるのか。答えは「できます」です。EM7455、EM7565、EM7511、EM919x などの M.2 モジュールは、Linux 上でネイティブに動作します。`kmod-usb-net-qmi-wwan` または `kmod-usb-net-cdc-mbim` をインストールし、`wwan0` を設定するだけでインターネットに接続できます。本記事では、モジュール対応マトリクス、設定手順、電源とアンテナの注意点までを整理して解説します。

{{< tldr >}}
Raspberry Pi に Sierra 4G/5G モジュールを接続すれば、OpenWrt ルーターとして十分に機能します。多くの M.2 モジュール（EM7455、EM7565、EM7511）は USB 接続で、EM919x は PCIe Gen3 レーンを追加、MC7455 は EM7455 の mPCIe 版です。OpenWrt では QMI プロトコルと `wwan0` の組み合わせが推奨です。`kmod-usb-net-qmi-wwan`、`uqmi`、`luci-proto-qmi` をインストールし、`/etc/config/network` で APN を設定してネットワークを再起動すれば接続できます。速度面では、EM7455 / MC7455 は LTE Cat 6（300/50 Mbps）、EM7565 / EM7511 は Cat 12（600/150 Mbps）、EM919x シリーズは 5G Sub-6（EM9190 は mmWave 対応）です。
{{< /tldr >}}

## OpenWrt における Sierra モジュール完全対応マトリクス

作業を始める前に、お手元のモジュールの仕様を確認しましょう。

| 型番 | 速度クラス | ベースバンドチップ | フォームファクタ | Linux データパス | GNSS 測位 |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM（Linux 両対応） | QZSS 対応 |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | QZSS 対応 |
| **EM919x** (9190/9191/7690) | 5G Sub-6（9190 は mmWave 対応） | SDX55 | M.2（長さ 52mm） | Windows/Linux 両対応 | L1 + L5（オプション） |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50.95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### 型番の選び方

- **初心者のメーカー向け**：**EM7455** を選択してください。情報が多く、トラブル時の解決策が見つかりやすくなります。
- **アップロード速度を重視する場合（ライブ配信、監視）**：**EM7565** または **EM7511** で、最大 150 Mbps のアップロードが可能です。
- **5G を利用する場合**：**EM9190** で 5G の速度を体験できます。
- **旧型の mPCIe スロットのみの場合**：**MC7455** をご検討ください。

## ハードウェアの接続方法：3 つのパターン

### A. Raspberry Pi 5 + M.2 HAT（PCIe 経由）

Pi 5 には PCIe が搭載されているため、M.2 HAT+ 拡張ボードに M.2 WWAN モジュールを直接挿入できます（B-Key であることを必ず確認してください）。

### B. Raspberry Pi 4B 以前 + USB WWAN 変換ケース

EM シリーズのモジュールは USB 2.0/3.0 にも対応しています。M.2 から USB への変換ケース（通常 SIM カードスロット内蔵）を Raspberry Pi の USB ポートに接続するだけでよい、最も手軽な方法です。

### C. MC7455（mPCIe）変換

MC7455 は旧型の mPCIe インターフェースのため、mPCIe から USB、または mPCIe から M.2 への変換ボードが必要です。

> ⚠️ **電源は最大の落とし穴**：モジュールは 3.135 から 4.4 V（通常 3.3V）で動作します。「モジュールを認識できない」原因は、多くの場合 Raspberry Pi の USB 電源不足です。突入電流は最大 2.5A に達するため、電源には十分な余裕を持たせてください。

## QMI と MBIM プロトコルについて

どちらも 4G/5G モジュールの通信を制御するプロトコルです。

- **QMI**：Qualcomm 独自のプロトコルで、Linux/OpenWrt のガイドでは最も多く使われています（インターフェース名は `wwan0`）。
- **MBIM**：後発の標準化されたプロトコルで、Windows と Linux の両方で利用できます（インターフェース名はこちらも `wwan0`）。

**どちらを選ぶか**：基本的には QMI で問題ありません。ファームウェアが MBIM を要求する場合のみ、MBIM に切り替えてください。

## 実践 Part 1：OpenWrt で QMI を設定して接続する

4 つのステップだけで、コンパイルは一切不要です。

### 1. パッケージのインストール

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Raspberry Pi がモジュールを認識していることを確認

```bash
lsusb                                  # Sierra デバイスの有無を確認
ls /dev/cdc-wdm*                       # QMI の制御チャネルを確認
dmesg | grep qmi_wwan                  # ドライバのロードを確認
ip link show wwan0                     # インターフェースの出現を確認
```

### 3. ネットワーク設定ファイルの編集（`/etc/config/network`）

QMI の設定を追加し、APN をご利用の通信事業者のものに変更してください。

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. ネットワークの再起動

```bash
/etc/init.d/network restart
ifup wwan
```

以上で完了です。`wwan0` が IP アドレスを取得すれば、インターネットに接続できます。

## アンテナと SIM カード：見落とし厳禁

モジュールには**内蔵アンテナはありません**。アンテナの品質が通信速度を左右します。

- **メインアンテナ（Main）**：必ず接続してください。
- **補助アンテナ（Aux）**：MIMO の高速通信に必要です。未接続だと速度が低下します。
- **GNSS アンテナ**：測位を利用する場合のみ接続します。メインアンテナと混同しないように注意してください。

## よくあるトラブル一覧（初心者必読）

1. **`lsusb` で何も表示されない**：99% は電源不足、変換ボードの接触不良、またはケーブルの故障です。
2. **焦りすぎ**：モジュールは起動に時間がかかります。挿入後は 10 秒ほど待ってからコマンドを実行してください。
3. **5G モジュール（EM919x）の発熱**：5G モジュールは 100°C 前後になることも珍しくありません（上限 115°C）。冷却対策を行ってください。
4. **ModemManager との競合**：通常の Linux 環境で手動操作する場合、まず `ModemManager` を停止してください（`systemctl stop ModemManager`）。制御権を奪われるのを防ぎます。

## まとめ

Raspberry Pi と OpenWrt で Sierra モジュールを駆動する手順は、チェックリストに沿って進めるだけです。まずハードウェアの仕様（フォームファクタ、電圧、アンテナ）を確認し、次に QMI/MBIM 関連ドライバをインストールし、最後に APN を設定します。本記事がプロジェクトの回り道を減らし、Raspberry Pi で 4G/5G の速度を実現する一助となれば幸いです。

## 購入情報（Call To Action）

EM7455、EM7565、EM7511 などのモジュールや、対応する M.2 変換ボード・アンテナをお求めの場合は、Yupitek（榆閤科技）がハードウェアソリューションと技術相談を提供しています。

お問い合わせ：**sales@yupitek.com**

製品ページ：[Yupitek Sierra Wireless シリーズ](https://yupitek.com/ja/products/sierra/)
