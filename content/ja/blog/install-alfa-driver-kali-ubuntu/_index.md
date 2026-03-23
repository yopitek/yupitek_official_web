---
title: "Kali Linux・Ubuntu 24.04 への ALFA USB WiFi ドライバーインストール完全ガイド（2026）"
description: "Kali Linux 2024 と Ubuntu 24.04 に ALFA Network USB WiFi アダプターのドライバーをインストールする完全解説。RTL8812AU・MT7612U・MT7921AU 対応、トラブルシューティング付き。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ドライバーインストール", "Kali-Linux", "Ubuntu", "RTL8812AU", "MT7612U", "MT7921AU", "ALFA-Network"]
---

Linux で USB WiFiアダプターを動かすには、まずドライバーが鍵になります。Windows では製造元がインストーラーを提供してくれますが、Linux ではカーネルモジュール——OSがハードウェアと通信するためにロードするコンパイル済みコード——を使います。この仕組みを理解しておくと、トラブルシューティングが格段に楽になり、ドライバーのインストール作業も迷わず進められます。

このガイドでは、Kali Linux 2024/2025 と Ubuntu 24.04 LTS の両方において、ALFA Network の主要な USB WiFiアダプターチップセット向けのドライバーインストール手順を網羅的に説明します。

---

## Linux における USB WiFiドライバーの仕組み

### カーネルモジュールとは

Linux の WiFiドライバーは**カーネルモジュール**——起動時または必要に応じてカーネルにロードされる `.ko` ファイル——です。USB デバイスを接続すると、カーネルはその USB ベンダー ID とプロダクト ID を読み取り、データベースから対応するモジュールを検索して自動的にロードします。

MediaTek MT7612U のような一般的なチップセットなら、この処理は透過的に行われます——アダプターを挿せばモジュールがロードされ、インターフェースが現れる、それだけです。一方、新しかったり珍しかったりするチップセットには既存のカーネル内モジュールがなく、ソースからコンパイルする必要があります。

### アウトオブツリードライバー

ドライバーがメインラインカーネルに含まれていない場合（「アウトオブツリー」または「外部」ドライバーと呼ばれます）、次の手順が必要です：

1. ドライバーのソースコードをダウンロードする
2. 実行中のカーネルのヘッダーに対してコンパイルする
3. 生成された `.ko` ファイルをカーネルモジュールディレクトリに配置する
4. `modprobe` でロードする

コンパイル手順では、カーネルヘッダーがインストールされており、かつ実行中のカーネルと正確に一致していることが前提となります。ドライバーインストールの失敗原因として最も多いのがこの点です。

### DKMS：ダイナミックカーネルモジュールサポート

単純に `make install` を実行した場合、ドライバーは現在のカーネル向けにのみコンパイルされます。Kali や Ubuntu がカーネルを更新すると——これは定期的に発生します——古いドライバーはロードされなくなり、手動で再コンパイルが必要になります。

**DKMS** はこの問題を解決するために、ドライバーのソースコードをシステムデーモンに登録し、新しいカーネルがインストールされるたびに登録済みモジュールを自動的に再コンパイルします。アウトオブツリードライバーが必要なアダプターには、DKMS の利用を強くおすすめします。

---

## チップセットの確認

必要なドライバーは、アダプターの商品名ではなくチップセットによって決まります。同じ名前のアダプターでも、ハードウェアリビジョンが異なれば別のチップセットを使っている場合があります。

### ALFA モデルとチップセットの対応表

| ALFA モデル | チップセット | USB ID | ドライバー |
|---|---|---|---|
| [AWUS036ACH](/ja/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACHM](/ja/products/alfa/awus036achm/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/ja/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u（カーネル内蔵） |
| [AWUS036ACX](/ja/products/alfa/awus036acx/) | MT7612U | 0e8d:7612 | mt76x2u（カーネル内蔵） |
| [AWUS036AX](/ja/products/alfa/awus036ax/) | MT7921AU | 0e8d:7961 | mt7921u（カーネル 5.18+） |
| [AWUS036AXML](/ja/products/alfa/awus036axml/) | MT7921AU | 0e8d:7961 | mt7921u（カーネル 5.18+） |
| [AWUS1900](/ja/products/alfa/awus1900/) | RTL8814AU | 0bda:8813 | morrownr/8814au |

### lsusb でアダプターを確認する

アダプターを接続して、次のコマンドを実行します：

```bash
lsusb
```

出力例：

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
Bus 003 Device 004: ID 0bda:8813 Realtek Semiconductor Corp. RTL8814AU 802.11a/b/g/n/ac
```

`ID xx:xx` の値を上の対応表と照合して、チップセットを確定させてください。

---

## システムの準備

チップセットを問わず、まず共通のビルド前提パッケージをインストールします。

**Kali Linux の場合：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04 の場合：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

実行中のカーネルに対してヘッダーが正しくインストールされているか確認します：

```bash
uname -r
# 例: 6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# このパスが存在すれば OK。存在しない場合はヘッダーが入っていません
```

---

## RTL8812AU ドライバー（AWUS036ACH・AWUS036ACHM）

RTL8812AU はアウトオブツリードライバーが必要です。コミュニティが管理する 2 つのフォークがあり、OS によって使い分けます。

### オプション A：aircrack-ng/rtl8812au（Kali Linux 推奨）

このフォークは Aircrack-ng チームが管理しており、Kali との明示的な互換性とパケットインジェクション最適化が施されています：

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

インターフェースが現れたか確認します：

```bash
ip link show | grep wlan
# wlan0 などが表示されれば成功
```

### オプション B：morrownr/8812au-20210708（Ubuntu 24.04 推奨）

morrownr フォークは Ubuntu 向けに最適化されており、DKMS 統合を含む便利なインストールスクリプトが付属しています：

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

インストールスクリプトが DKMS 登録を自動的に処理します。実行後：

```bash
# 新しいモジュールをロードするために再起動
sudo reboot

# 再起動後に確認
lsmod | grep 8812au
```

### DKMS への手動登録（どちらのフォークでも利用可）

手動で制御したい場合：

```bash
# ドライバーをクローン（どちらのフォークでも可）
git clone https://github.com/aircrack-ng/rtl8812au

# Makefile からバージョンを確認
grep "^MODULE_VERSION" rtl8812au/Makefile
# バージョンを確認、例：v5.6.4.2 → 5.6.4.2 として使用

# ソースを DKMS ディレクトリにコピー
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# 登録・ビルド・インストール
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# 確認
dkms status
# 期待される出力: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### インストール成功後の lsusb・lsmod 出力

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## MT7612U ドライバー（AWUS036ACM・AWUS036ACX）

MT7612U チップセットは、ドライバーがバージョン **4.19** からメインラインカーネルに組み込まれているため、4 つのチップセットの中で最も簡単に使えます。Kali Linux 2022+ や Ubuntu 20.04+ では、ドライバーのインストール自体が不要です。

### カーネルバージョンの確認

```bash
uname -r
```

4.19 以上であれば（最新の Kali・Ubuntu では必ずそうなります）、`mt76x2u` モジュールが利用できます。

### モジュールのロード

```bash
sudo modprobe mt76x2u
```

ロードを確認します：

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

すぐにワイヤレスインターフェースが現れるはずです：

```bash
ip link show
# wlan0: ...
```

### 起動時にモジュールを自動ロードする設定

多くのシステムではアダプターを検出すると自動的にロードされますが、明示的に設定しておきたい場合：

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### コンパイル不要

これが MT7612U チップセットの大きな利点です——コンパイル作業なし、ドライバーソース不要、カーネルヘッダーへの依存もありません。対応ディストリビューションではそのまま動きます。ドライバー管理の手間を省きたい方には、[AWUS036ACM](/ja/products/alfa/awus036acm/) が最もプラグアンドプレイに近いペネトレーションテスト用アダプターです。

---

## MT7921AU ドライバー（AWUS036AX・AWUS036AXML — Wi-Fi 6E）

MT7921AU は MediaTek の Wi-Fi 6E チップセットです。Linux ドライバー `mt7921u` はカーネル **バージョン 5.18** からメインラインにマージされています。

### カーネルバージョンの確認

```bash
uname -r
```

**Kali Linux 2022.2 以降**はカーネル 5.18 以上を搭載しており、サポートされます。
**Ubuntu 22.04 LTS** はカーネル 5.15 を搭載しており、カーネルのアップグレードなしでは**サポートされません**。
**Ubuntu 24.04 LTS** はカーネル 6.8 を搭載しており、完全にサポートされます。

### モジュールのロード（カーネル 5.18+）

```bash
sudo modprobe mt7921u
```

確認：

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04：カーネルアップグレードの方法

カーネル 5.15 の Ubuntu 22.04 をお使いの場合、2 つの選択肢があります：

**オプション A：HWE カーネル**（推奨）

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

Ubuntu 22.04 の HWE（ハードウェアイネーブルメント）カーネルはバージョン 6.2 以上で、mt7921u をサポートします。

**オプション B：Ubuntu 24.04 へのアップグレード**

Ubuntu 24.04 LTS はカーネル 6.8 と mt7921u の完全サポートを提供します。長期的に見て最もクリーンな解決策です。

### Wi-Fi 6E とモニターモードの現状

2026 年時点で、mt7921u ドライバーは 2.4 GHz・5 GHz・6 GHz のすべてのバンドでマネージドモード（ネットワーク接続）を安定してサポートしています。2.4 GHz と 5 GHz でのモニターモードは動作しています。**6 GHz のモニターモード**はまだ成熟途上です——6 GHz アセスメントで利用する前に、`mt76` カーネルドライバーのイシュートラッカーで最新状況を確認してください。

---

## RTL8814AU ドライバー（AWUS1900）

RTL8814AU は [AWUS1900](/ja/products/alfa/awus1900/) に搭載されており、4 本のアンテナと AC1900 の性能を誇る ALFA の最高出力アダプターです。`morrownr/8814au` リポジトリのアウトオブツリードライバーが必要です。

### インストール

```bash
git clone https://github.com/morrownr/8814au
cd 8814au
sudo ./install-driver.sh
```

インストールスクリプトは DKMS 統合を含みます。インストール後、再起動します：

```bash
sudo reboot
```

再起動後の確認：

```bash
lsmod | grep 8814au
# 8814au    3825664  0

ip link show | grep wlan
# wlan0: ...
```

### 手動ビルド（install-driver.sh を使わない場合）

```bash
make
sudo make install
sudo modprobe 88XXau_btcoex
```

注意：RTL8814AU のモジュール名は `88XXau_btcoex`（またはフォークのバージョンによっては `8814au`）です。インストール後に `lsmod | grep 88` で正しい名前を確認してください。

---

## DKMS：カーネル更新後もドライバーを維持する

Kali Linux と Ubuntu はどちらも定期的にカーネルを更新します。DKMS なしでは、カーネル更新のたびにアウトオブツリードライバー（RTL8812AU・RTL8814AU）が動かなくなり、手動での再コンパイルが必要になります。

DKMS を正しく設定しておけば、`apt upgrade` の際に再コンパイルが自動的に行われます。

### DKMS がドライバーを管理しているか確認する

```bash
dkms status
```

正しく管理されている場合の出力例：

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### カーネル更新時の動作

```
apt upgrade
→ 新しいカーネルパッケージがダウンロードされる
→ DKMS フックが起動
→ rtl8812au ソースが新カーネル向けに再コンパイルされる
→ 新しい .ko がインストールされる
→ システムが新カーネルで再起動
→ ドライバーが自動的にロード
```

アップグレード中に DKMS が失敗した場合（`dkms status` で "built" だが "installed" になっていない場合）、手動で再インストールします：

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## トラブルシューティング

| 症状 | 考えられる原因 | 対処法 |
|---|---|---|
| 接続後に wlan インターフェースが現れない | ドライバーがロードされていない | `sudo modprobe 88XXau` または `sudo modprobe mt76x2u` を実行 |
| `modprobe: FATAL: Module not found` | 現在のカーネル向けにドライバーがコンパイルされていない | ドライバーを再コンパイルするか `sudo dkms install` を実行 |
| インターフェースが現れてすぐ消える | 電源管理の干渉 | `sudo iwconfig wlan0 power off` を実行 |
| `make` が "linux/module.h not found" で失敗 | カーネルヘッダーが未インストール | `sudo apt install linux-headers-$(uname -r)` を実行 |
| `make` がバージョン不一致で失敗 | ヘッダーが実行中カーネルと一致していない | `uname -r` と `ls /lib/modules` を比較し、一致するヘッダーを再インストール |
| lsusb にはデバイスが表示されるがインターフェースが現れない | モジュールはロードされたがインターフェースが作成されていない | `dmesg \| tail -30` でエラーを確認 |
| モニターモードが失敗：「Operation not supported」 | ドライバーのバージョンがモニターモードに未対応 | ディストリビューション提供のドライバーではなく aircrack-ng フォークを使用 |
| aireplay-ng インジェクションテスト：0% | インターフェースがモニターモードになっていない | `iwconfig` で確認し、`airmon-ng start` を再実行 |
| ドライバーは動くが再起動後に消える | モジュールが initramfs に追加されていない | `sudo update-initramfs -u` を実行するか DKMS を使用 |
| カーネル更新後に DKMS ビルドが失敗 | 新カーネル用のヘッダーが不足 | `sudo apt install linux-headers-$(uname -r)` を実行 |

### 詳細な診断コマンド

```bash
# ロード済みのワイヤレスモジュールをすべて確認
lsmod | grep -E "8812|8814|mt76|mt79"

# USB とワイヤレスイベントのカーネルメッセージを確認
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# すべてのワイヤレスインターフェースを一覧表示
iw dev

# 特定のインターフェースが使用するドライバーを確認
ethtool -i wlan0 | grep driver

# USB デバイスの詳細を確認
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# 登録済みモジュールの DKMS ステータスを確認
dkms status
```

---

## クイックリファレンス：アダプター別推奨ドライバー

| 手持ちのアダプター | チップセット | Kali Linux | Ubuntu 24.04 |
|---|---|---|---|
| [AWUS036ACH](/ja/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` | `morrownr/8812au-20210708` |
| [AWUS036ACM](/ja/products/alfa/awus036acm/) | MT7612U | 内蔵（`mt76x2u`） | 内蔵（`mt76x2u`） |
| [AWUS036AX](/ja/products/alfa/awus036ax/) | MT7921AU | 内蔵（`mt7921u`、カーネル 5.18+） | 内蔵（`mt7921u`、カーネル 6.8） |
| [AWUS036AXML](/ja/products/alfa/awus036axml/) | MT7921AU | 内蔵（`mt7921u`、カーネル 5.18+） | 内蔵（`mt7921u`、カーネル 6.8） |
| [AWUS1900](/ja/products/alfa/awus1900/) | RTL8814AU | `morrownr/8814au` | `morrownr/8814au` |

---

## 正規品であることを確認する

ドライバーの問題の中には、USB ID を偽装したり、記載のモデルと異なる低品質チップセットを使った模造品のアダプターが原因であるケースもあります。正規代理店から購入した本物の ALFA Network アダプターは、ドキュメント通りに動作します。

Yopitek は ALFA Network の正規代理店です。正規品の保証と予測通りのドライバー互換性のために、[ALFA Network 製品ラインナップ](/ja/products/alfa/)からお求めください。

---

## まとめ

Linux の WiFiドライバーインストールは、シンプルな判断フローで進められます：

1. `lsusb` と上の対応表で**チップセットを確認する**
2. **MT7612U または MT7921AU（カーネル 5.18+）?** → `modprobe` を実行するだけで完了
3. **RTL8812AU または RTL8814AU?** → 対応リポジトリをクローンし、`make && sudo make install` を実行。DKMS で永続化
4. **うまくいかない場合?** → トラブルシューティング表を確認し、ヘッダーとカーネルが一致しているか確認し、`dmesg` をチェック

ALFA Network アダプターの魅力は、4 つの主要チップセットすべてについて、よくドキュメント化されアクティブにメンテナンスされたドライバーソリューションが存在する点です。サポートされない状況に陥ることはありません。
