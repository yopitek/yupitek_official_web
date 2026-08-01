---
title: "Ubuntu / Debian / Linux Mint で Sierra 4G/5G モジュールをインストールする完全ガイド：EM7455、EM7565、EM919x、MC7455 の設定と GNSS 測位"
description: "Ubuntu/Debian/Linux Mint で Sierra 4G/5G モジュールをインストールするには？本ガイドでは、ModemManager のインストール、qmicli/mbimcli によるダイヤルアップ接続、GNSS 測位の設定までを解説します。EM7455、EM7565、EM919x、MC7455 に対応。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/ja/products/sierra/"
faq:
  - question: "Ubuntu で Sierra 4G/5G モジュールを直接使ってインターネットに接続できますか？"
    answer: "できます。modemmanager、libqmi-utils などのパッケージをインストールし、NetworkManager で APN を入力すれば接続できます。"
  - question: "Linux で Sierra モジュールの GNSS 測位を有効にするにはどうすればよいですか？"
    answer: "ModemManager のコマンドを使用します。まず mmcli -m 0 --location-enable-gps-raw を実行し、次に --location-get で座標を取得します。GNSS アンテナが接続されていることを確認してください。"
---

Ubuntu、Debian、Linux Mint で Sierra Wireless のモジュール（EM7455、EM7565、MC7455、EM919x）をインストールしたいですか？実は、Linux はこれらのデバイスを標準でサポートしています。ModemManager や libqmi-utils など、正しいパッケージをインストールする方法を知っていれば大丈夫です。本記事では、ハードウェアの接続方法、ドライバのインストール、ダイヤルアップでインターネットに接続する手順、そして GNSS 測位機能の有効化までを順を追って解説します。ドローンを開発する場合も、産業用コンピュータを構築する場合も、手順に従えば問題ありません。

{{< tldr >}}
Ubuntu、Debian、Linux Mint で Sierra Wireless のモジュール（EM7455、EM7565、MC7455、EM919x）をインストールしたいですか？実は、Linux はこれらのデバイスを標準でサポートしています。正しいパッケージ（ModemManager と libqmi-utils）をインストールするだけです。ハードウェアの接続からドライバのインストール、ダイヤルアップ接続、GNSS 測位の有効化まで、ドローンにも産業用コンピュータにも対応できる手順です。
{{< /tldr >}}

**一言でまとめると、Linux での Sierra モジュールのインストールはとても簡単です。`apt` で `modemmanager` と関連ツールをインストールすれば、NetworkManager でインターネットに接続でき、GPS 測位まで簡単に読み出せます。**

EM7455、EM7565、EM919x、MC7455 を入手してマザーボードに挿しても、インターネットへの接続設定方法がわからないという方は多いです。実は、これらのモジュールの Linux でのサポートは非常に成熟しています。すべて USB 経由で QMI または MBIM プロトコルを使用して通信します。ここからは、ステップごとに設定方法を説明します。

> 仕様値と技術的な根拠は、すべて Sierra Wireless 公式仕様書に基づいています。本記事は Yupitek（榆閤科技）が編集しました。

---

## 始める前に：お手持ちのハードウェアを確認する

ハードウェアが正しくなければ、ソフトウェアでどんなコマンドを実行しても意味がありません。

| モジュール | フォームファクタ | 速度クラス | Linux の主流通信プロトコル | アンテナ数 |
|---|---|---|---|---|
| **EM7455** | M.2（長さ 42mm） | Cat 6（300/50 Mbps） | QMI | 3 本（Main、GNSS、Aux） |
| **EM7565** | M.2（長さ 42mm） | Cat 12（600/150 Mbps） | QMI / MBIM | 3 本（Main、GNSS、Aux） |
| **EM919x**（5G） | M.2（長さ **52mm**） | 5G NR / LTE Cat 20 | MBPW などのブロードバンドパッケージ | 4 本以上 |
| **MC7455** | mPCIe（旧型スロット） | Cat 6（300/50 Mbps） | QMI | U.FL コネクタ 3 本 |

**ハードウェアの注意点は 2 つ：**
1. **EM919x は長い**：52mm の長さなので、42mm のスロットに無理に挿入しないでください。ボードを壊してしまいます。
2. **アンテナなし = 電波なし**：最低でもメインアンテナ（Main）を接続してください。測位を利用する場合は、必ず GPS アンテナを用意して専用の **GNSS コネクタ** に接続しましょう。

---

## ステップ 1：Linux の必須ツールをインストールする

Ubuntu / Debian / Linux Mint では、ドライバを自分で書いてコンパイルする必要はありません。パッケージリポジトリがすべて用意してくれています。

ターミナルを開いて、次の 2 行を実行します：
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
インストール後、サービスが起動していることを確認します：
```bash
systemctl status ModemManager
```
これらのツールがあれば、Linux はこの 4G/5G モデムを認識できるようになります。

---

## ステップ 2：システムがモデムを認識しているか確認する

モデムを挿して起動したら、次の 3 つのコマンドで確認します：

1. **USB ハードウェアの確認：**
   ```bash
   lsusb
   ```
   （Sierra または Qualcomm 関連のデバイスが表示されるはずです）

2. **カーネルドライバの確認：**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   （`cdc-wdm0` と `wwan0` が表示されれば、正常にマウントされています）

3. **ModemManager の状態確認：**
   ```bash
   mmcli -L
   ```
   （モデムの名前と番号の一覧が表示されます。この番号をメモしてください。通常は `0` です）

---

## ステップ 3：超簡単なダイヤルアップ接続（NetworkManager を使用）

デスクトップ版の Ubuntu や Mint を使っている場合は、システム標準のネットワーク管理ツールが最も便利です。

```bash
# 接続を作成する（"internet" を通信事業者の APN に置き換えてください）
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# 接続を開始！
nmcli connection up mobile
```
これだけです！`ip addr show` で `wwan0` に IP が割り当てられたか確認できます。

### （上級者向け）デスクトップ環境のないテキストベースの接続方法
ヘッドレスサーバーや組み込みボードの場合は、`qmicli` で直接コマンドを実行できます：
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## ステップ 4：GPS 測位機能を有効にする！

これらのモジュールには、強力な GNSS 測位システム（GPS、GLONASS などに対応）が内蔵されています。
公式仕様によると：
- EM7455 / EM7565 / MC7455：ホットスタート 1 秒、コールドスタート 32 秒。水平精度は約 2 から 5 メートル。
- 5G の EM919x：コールドスタートがより高速（≤28 秒）で、精度も若干向上（95% で <4m）。

**Linux で座標を取得する最も速い方法：**

1. GPS 機能を有効化：
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. 現在の座標を取得：
```bash
mmcli -m 0 --location-get
```
現在の緯度経度が画面に表示されます！他のプログラムにリアルタイムでストリーミングしたい場合は、`gpsd` と組み合わせて使用できます。

---

## よくある失敗と対処法

1. **`mmcli -L` に何も表示されない**：`ModemManager` が停止しているか、USB の給電がモデムを駆動できない可能性があります。
2. **GPS 測位がいつも失敗する**：GPS アンテナを Main や Aux に挿していませんか？GNSS には専用のコネクタがあります！
3. **EM919x の速度が出ない**：これは 5G モデムで、USB 3.1 Gen 2 や PCIe Gen 3 に対応しています。USB 2.0 ポートに挿した場合、メーカーは性能を保証しません。

## まとめ

Linux での Sierra モジュールの利用は、想像するほど難しくありません。ハードウェアのスロットとアンテナを確認し、`modemmanager` ファミリーのパッケージをインストールして、APN を設定すれば、すぐにインターネットに接続できます。この手順は、エッジコンピューティング（Edge Computing）や産業用 IoT（IIoT）に取り組むエンジニアに最適です。

## 購入情報（Call To Action）

Sierra モジュールを Ubuntu デバイスに統合したいですか？Yupitek（榆閤科技）では、モジュール、アンテナ、変換ボードの完全なソリューションに加え、最前線の技術サポートを提供しています。
ご連絡はこちら：**sales@yupitek.com**
製品情報はこちら：[Sierra Wireless シリーズ](https://yupitek.com/ja/products/sierra/)

{{< faq >}}
