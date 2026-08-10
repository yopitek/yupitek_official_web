---
title: "Raspberry Pi と Kali Linux で ALFA WiFi アダプターを使う：セットアップガイド"
description: "Kali Linux ARM64 を動かす Raspberry Pi に ALFA USB WiFi アダプターをインストール。AWUS036ACH RTL8812AU ドライバーのコンパイル、モニターモード、ポータブルペネトレーションテスト環境の構築を解説。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ペネトレーションテストに最も適したRaspberry Piはどれですか？"
    answer: "Raspberry Pi 5（4GBまたは8GB）が最適です。Pi 4（4GB以上）でも正常に動作します。Pi 3B+はリアルタイムパケットキャプチャには速度が不足しています。"
  - question: "AWUS036ACHはRaspberry Piでドライバーをコンパイルする必要がありますか？"
    answer: "必要です。RTL8812AUはメインラインカーネルに含まれていません。まずKali DKMSパッケージrealtek-rtl88xxau-dkmsを試し、失敗した場合はaircrack-ng GitHubから手動でコンパイルしARM64プラットフォームフラグを切り替えてください。"
  - question: "ヘッドレスPiでwlan0をモニターモードに使えますか？"
    answer: "推奨しません。wlan0はPi内蔵WiFiでSSH接続に使用されます。airmon-ng check killを実行するとSSHが切断されるため、wlan1（ALFAアダプター）を使用し、イーサネットまたはtmuxで接続を維持してください。"
  - question: "AWUS036AXMはRaspberry Piでプラグアンドプレイですか？"
    answer: "はい。MT7921AUNドライバーはカーネル5.18以降内蔵で、Kali ARM64イメージのカーネルバージョンはさらに高いです。firmware-misc-nonfreeファームウェアパッケージをインストールするだけです。"
  - question: "Raspberry Pi上のAWUS036ACHにどう給電しますか？"
    answer: "AWUS036ACHは約500mWを消費し、Piに直接挿すとクロックダウンや再起動を引き起こす可能性があります。電源付きUSB 3.0ハブを使用し、3A以上の公式Pi USB-C電源アダプターと組み合わせてください。"
---

Kali Linux を搭載したノートパソコンは標準的なペネトレーションテストワークステーションですが、それが唯一の選択肢ではありません。Raspberry Pi 4 または Pi 5 に ALFA USB WiFi アダプターを組み合わせることで、コンパクトでファンレス、パッシブ冷却のプラットフォームが完成します。ジャケットのポケットに収まり、USB-C モバイルバッテリーで動作し、対象環境に無人で数時間放置できます。Kali Linux ARM64 イメージは Offensive Security が公式提供しており、Pi 4 および Pi 5 でエミュレーションなしにネイティブ動作します。Aircrack-ng、Kismet、Wireshark、Bettercap など Kali の標準ツールセットが完全に使えます。


{{< tldr >}}
Raspberry Pi 4/5にKali Linux ARM64とALFAアダプターを組み合わせればポケットサイズのペネトレーションテストプラットフォームを作れます。AWUS036ACHはRTL8812AUドライバーのコンパイルが必要ですが、AWUS036ACMとAWUS036AXMはカーネル内蔵ドライバーでプラグアンドプレイです。電源付きUSBハブでの給電が必要です。
{{< /tldr >}}
最大の障壁はドライバーです。AWUS036ACH に搭載された RTL8812AU チップセットはメインラインカーネルに含まれていないため、アダプターを差し込んですぐ動作することは期待できません。実行中の ARM64 カーネルに対してドライバーをコンパイルする必要があり、コンパイルフラグは x86-64 と異なります。本ガイドではすべての手順を順を追って説明します。

---

## 推奨ハードウェア

Pi のモデル、アダプター、電源の組み合わせすべてが安定して動作するわけではありません。以下の表は動作確認済みの組み合わせとトレードオフをまとめたものです。

| コンポーネント | 推奨 | 備考 |
|---|---|---|
| シングルボードコンピューター | Raspberry Pi 5（4 GB または 8 GB） | Pi 4（4 GB+）も良好に動作；Pi 3B+ はリアルタイムキャプチャには非力 |
| 主アダプター | ALFA AWUS036ACH | RTL8812AU チップ；ARM ドライバーサポートが最良；デュアルバンド AC1200 |
| 代替アダプター | ALFA AWUS036ACM | MT7612U チップセット；カーネル内蔵ドライバー (mt76x2u)；Kali ARM64 でプラグアンドプレイ |
| WiFi 6 アダプター | ALFA AWUS036AXM または AXML | MT7921AUN チップ；カーネル 5.18 からネイティブ対応；firmware-misc-nonfree が必要 |
| USB ハブ | 電源付き USB 3.0 ハブ | AWUS036ACH は約 500 mW 消費；ハブなしでは Pi USB ポートが電力不足になる可能性 |
| ストレージ | MicroSD 32 GB 以上（Class 10 / A2） | A2 規格カードはブートと apt 操作が明確に高速 |
| 電源アダプター | 公式 Pi USB-C 電源アダプター（3 A 以上） | サードパーティ製アダプターは安定性問題の一般的な原因 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH は高電流 USB デバイスです。電源付き USB ハブなしで Raspberry Pi 4 または Pi 5 に直接接続すると、負荷時に Pi がスロットリングまたは再起動する可能性があります。他の USB 周辺機器と同時に使用する場合は、必ず電源付きハブを使用してください。
{{< /alert >}}

---

## Raspberry Pi への Kali Linux ARM64 インストール

### ARM イメージのダウンロード

Kali Linux は [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm) で Raspberry Pi 向け公式 ARM64 イメージを提供しています。**Raspberry Pi 4（64 ビット）** または **Raspberry Pi 5（64 ビット）** と表示されたイメージをダウンロードしてください。32 ビットイメージは使用しないでください——本ガイドのドライバーのビルド手順には ARM64 カーネルが必要です。

### MicroSD への書き込み

Raspberry Pi Imager GUI ツールまたはコマンドラインの `dd` で書き込めます：

```bash
# /dev/sdX を実際の SD カードデバイスに置き換える（lsblk で確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Raspberry Pi Imager の場合：**カスタムイメージを使用** → Kali `.img.xz` ファイルを選択 → SD カードを選択 → 書き込み。

### 初回起動と初期設定

SD カードを挿入し、モニターとキーボードを接続（またはまずヘッドレスアクセスを設定）して電源を入れます。デフォルトの認証情報：

- **ユーザー名：** `kali`
- **パスワード：** `kali`

ログイン後、`kali-tweaks` を実行してデフォルト設定を強化します。ドライバーに触れる前にシステムを完全にアップデートしてください：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
SSH 経由で Pi にアクセスする場合は、初回起動前に SD カードの `/boot` パーティションに `ssh` という名前の空ファイルを置くことで SSH を有効にできます。これは標準の Raspberry Pi OS と同じ仕組みです。
{{< /alert >}}

---

## Kali ARM64 への RTL8812AU ドライバーインストール（AWUS036ACH / ACM）

RTL8812AU ドライバーはメインライン Linux カーネルに含まれていません。ARM64 ではソースからコンパイルするか、Kali がパッケージングした DKMS バージョンをインストールする必要があります。両方の方法を説明します——まずパッケージ方式を試し、カーネルバージョンの不一致が発生した場合のみ手動ビルドに切り替えてください。

### 方法 1：Kali パッケージ（推奨の出発点）

Kali Linux は RTL8812AU ドライバーの DKMS パッケージ版を提供しており、カーネル更新時に自動的に再コンパイルされます。

```bash
sudo apt install realtek-rtl88xxau-dkms
```

インストール後に再起動してモジュールが読み込まれていることを確認します：

```bash
sudo modprobe 88XXau
ip link show
```

`wlan1` インターフェース（`wlan0` が Pi の内蔵アダプターと仮定）が表示されれば、ドライバーは正常に動作しています。このパッケージは GitHub ソースより数週間遅れる場合がありますが、最も手軽な出発点です。

{{< alert "circle-info" >}}
Kali パッケージはほとんどの ARM64 環境で十分です。現在のカーネルバージョンに対して DKMS パッケージのコンパイルが失敗した場合のみ、以下の手動ビルドに進んでください（カーネルバージョンは `uname -r` で確認できます）。
{{< /alert >}}

### 方法 2：ソースから手動ビルド（ARM64）

DKMS パッケージが失敗した場合——最も多い原因はパッケージの最終テスト済みバージョンよりカーネルが新しいこと——GitHub の Aircrack-ng フォークから直接ビルドしてください。これが ARM64 サポートの正式なソースです。

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# プラットフォームフラグを x86 から ARM64 に切り替える
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

`sed` コマンドは x86-64 ビルドとの重要な違いです。これらを実行しないと、Makefile がデフォルトで x86 プラットフォームパスを使用し、生成されるモジュールが ARM64 で読み込めません。

ビルド成功後、モジュールを読み込んで確認します：

```bash
sudo modprobe 88XXau
ip link show
```

新しいインターフェース——通常 `wlan1`——が表示されるはずです。`ip link show` にそのインターフェースが表示されれば、ドライバーは正常に動作しています。

---

## Raspberry Pi 上の MT7921AUN（AWUS036AXM / AXML）

AWUS036AXM と AXML に使用されている MediaTek MT7921AUN チップセットはカーネル 5.18 からメインラインカーネルに組み込まれています。Kali Linux ARM64 イメージはそのバージョンをはるかに超えるカーネルを使用しているため、アダプターを差し込むだけでドライバーが自動的に読み込まれます——コンパイル不要です。

必要な追加手順は、MT7921AUN が必要とするクローズドソースのファームウェアをインストールすることだけです：

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

再起動後、アダプターが検出されインターフェースが起動していることを確認します：

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

`lsusb` に MediaTek デバイスが表示され、`ip link show` に新しいワイヤレスインターフェースが一覧表示されれば、アダプターは使用準備完了です。MT7921AUN のモニターモードサポートはカーネル 5.18 以降大幅に改善されましたが、一部のパケットインジェクションテストでは RTL8812AU ベースのアダプターほど安定しない場合があります。旧来のペネトレーションテストワークフローとの最大互換性には、AWUS036ACH が依然として優れた選択肢です。

---

## Raspberry Pi でモニターモードを有効にする

Raspberry Pi には内蔵 WiFi インターフェース（`wlan0`）があります。SSH アクセスを維持するためにネットワークに接続したままにしてください。ALFA アダプター（`wlan1`）はモニターモードとパケットキャプチャ専用にします。ヘッドレス Pi では `wlan0` を絶対にモニターモードにしないでください——SSH 接続が切断されます。

```bash
# モニターモードと競合するプロセスを停止（NetworkManager、wpa_supplicant）
sudo airmon-ng check kill

# ALFA アダプターインターフェースでモニターモードを有効化
sudo airmon-ng start wlan1

# モニターモードが有効であることを確認
sudo iwconfig wlan1mon

# 全チャンネルでキャプチャを開始
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` は `wlan1mon` という新しいインターフェースを作成します。後続のツールは `wlan1` ではなく必ず `wlan1mon` に対して実行してください。インターフェース名は `iwconfig` または `ip link show` で確認できます。
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
`airmon-ng check kill` を実行すると NetworkManager と wpa_supplicant が停止します。`wlan0` を通じて SSH 接続している場合、SSH セッションも切断されます。ヘッドレスセットアップでは、これらのコマンドを実行する前にイーサネットまたは第 2 の有線インターフェースで接続するか、`tmux` を使用して切断後もセッションを維持してください。
{{< /alert >}}

モニターモードを無効にしてマネージドモードに戻すには：

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## ポータブルペネトレーションテストのセットアップのヒント

ハードウェアを動作させることは作業の半分にすぎません。以下の実践的なアドバイスが、安定したフィールドキットと問題だらけのケーブルの山との違いを生みます。

**ネットワーク構成：** `wlan0`（Pi 内蔵 WiFi）を管理接続の維持に使用——同一 LAN またはホットスポット上のノートパソコンから Pi に SSH 接続します。`wlan1`（ALFA アダプター）はペネトレーションテスト活動専用にします。2 つの役割を絶対に混在させないでください。

**ヘッドレス運用：** フィールドではキーボード、マウス、モニターの接続を避けてください。初回起動時に SSH を設定し、ノートパソコンのターミナルエミュレーターからすべてにアクセスします。`tmux` セッションは再接続後も維持され、ネットワーク状態が不安定な場合に非常に役立ちます。

**電源：** 最低 3 A の公式 Raspberry Pi USB-C 電源アダプターを使用します。AWUS036ACH には 2.5 A 以上の電源付き USB ハブを追加してください。高品質な USB-C モバイルバッテリー（65 W 以上）は Pi、ハブ、アダプターを同時に負荷に応じて 4～6 時間供電できます。

**ストレージ：** Kismet のログやキャプチャファイルは MicroSD カードではなく USB SSD に書き込んでください。MicroSD カードは書き込み回数に制限があり、継続的なロギングワークロードで急速に劣化します。電源付きハブに接続した USB 3.0 SSD はより高速で耐久性があります。

**ケース：** 電源付きハブを収容できる開放 USB ポートまたは切り欠きのある Pi ケースを選んでください。パッシブヒートシンクフィン付きのアルミニウムケースは、継続的なキャプチャ中の熱管理に役立ちます。

---

## Raspberry Pi で Kismet を実行する

Kismet はパッシブ WiFi スキャナーで、バックグラウンドサーバーとして動作し、ブラウザベースの Web UI を提供します。ヘッドレス Pi の展開に非常に適しています：Pi を動かしたままにして、同一ネットワーク上のデバイスから Web インターフェースを確認します。

```bash
sudo apt install kismet

# モニターモードで ALFA アダプターを使用して Kismet を起動
kismet -c wlan1
```

{{< alert "circle-info" >}}
インターフェース名を直接渡すと、Kismet は自らインターフェースをモニターモードに設定します。Kismet を起動する前に `airmon-ng start` を実行する必要はありません。Kismet はインターフェースのライフサイクルを内部で管理します。
{{< /alert >}}

起動後、ネットワーク上の任意のブラウザから Kismet Web UI にアクセスします：

```
http://raspberrypi.local:2501
```

初回起動時、Kismet は管理者ユーザー名とパスワードの作成を求めます。ログイン後、検出されたネットワーク、関連クライアント、シグナル強度の履歴、GPS ドングルが接続されている場合は GPS データを確認できます。

Kismet はデフォルトですべてを `~/.kismet/` の `.kismet` データベースファイルに記録します。これらは後で分析や WiGLE へのアップロードのためにエクスポートできます。

---

## ユースケース：ウォードライビングセットアップ

Kismet を実行し、ALFA アダプターと GPS ドングルを組み合わせた Raspberry Pi は、完全な自給自足型ウォードライビングキットです——専用のウォードライビング機器よりも小型で安価です。

**必要なコンポーネント：**
- Raspberry Pi 4 または Pi 5
- ALFA AWUS036ACH
- USB GPS ドングル（u-blox チップセットは Kismet との相性が良好）
- 電源付き USB ハブ
- USB-C モバイルバッテリー（65 W 以上、パススルー充電対応）

**セットアップ手順：**

1. Kismet と GPS パッケージをインストール：

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. GPS ドングルを読み取るよう `gpsd` を設定：

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. GPS サポート付きで Kismet を起動：

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Pi、ハブ、アダプター、モバイルバッテリーをバッグまたはケースに入れて車内に設置します。Pi と同じ WiFi ネットワークに接続したスマートフォンのホットスポットまたはタブレットから Kismet Web UI にアクセスします。

Kismet のログは検出されたすべてのネットワークの GPS 座標を記録します。`kismetdb_to_wigle`（Kismet に同梱）を使用して `.kismet` データベースを WiGLE CSV フォーマットにエクスポートし、WiGLE にアップロードしてマッピングします。

{{< alert "triangle-exclamation" >}}
ネットワークスキャン活動を行う前に、必ず現地の法律を遵守してください。多くの法域では、パッシブスキャンのみのウォードライビングは合法ですが、許可なくネットワークへのアクティブなプローブや接続は違法です。お住まいの地域の規制を確認してください。
{{< /alert >}}

---


---

{{< faq >}}

## 関連記事

デスクトップ版 Kali Linux と Ubuntu での RTL8812AU ドライバーの完全インストールガイドは、[Kali Linux と Ubuntu への ALFA ドライバーのインストール](/ja/blog/install-alfa-driver-kali-ubuntu/)をご覧ください。どのアダプターを購入するか検討中の場合は、[ALFA WiFi アダプター購入ガイド 2026](/ja/blog/alfa-wifi-adapter-buyer-guide-2026/) でチップセットの詳細と用途別の推奨情報をすべての現行モデルについて確認できます。

---

## 参考文献

1. [Kali Linux ARM公式ダウンロード](https://www.kali.org/get-kali/#kali-arm)
2. [aircrack-ng rtl8812auドライバープロジェクト](https://github.com/aircrack-ng/rtl8812au)
3. [Raspberry Pi公式ウェブサイト](https://www.raspberrypi.com/)
4. [Linux Kernel mt76ドライバードキュメント](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
