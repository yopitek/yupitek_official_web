---
title: "ALFA AWUS036ACH × Raspberry Pi：標準 Remote ID ドローン検出キット完全ガイド（2026）"
description: "ALFA AWUS036ACH ＋ Raspberry Pi で構築する合法的なパッシブ Remote ID ドローン検出キット。ASTM F3411 規格の解説、ハードウェアリスト、Step-by-Step 設定、DJI OcuSync との技術的区別まで網羅。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "ドローン検出", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "なぜ AWUS036ACH が推奨されるのですか？新しい Wi-Fi 6/6E アダプターではない理由は？"
    answer: "Remote ID のキャプチャには安定したモニターモードと raw パケットインジェクションが必要です。現在、コミュニティドライバが最も成熟しているのは Realtek rtl88xxau ブランチ（RTL8812AU / RTL8814AU）です。Wi-Fi 6/6E（MediaTek MT7921AUN、Realtek RTL8832BU）には、主流のペネトレーションテスト／キャプチャツールチェーンに対応するインジェクションドライバがまだありません。AWUS036ACH はコミュニティと本キットの両方で検証済みの選択肢です。"
  - question: "nRF52840 は必須ですか？"
    answer: "Wi-Fi Remote ID（NAN / Beacon）のみの場合は不要で、AWUS036ACH だけで十分です。Bluetooth 5 Long Range ブロードキャストも同時にキャプチャする場合は、nRF52840（sniffer ファームウェア書き込み済み）が必要です。完全なカバレッジのためには本モジュールを含めることを推奨します。"
  - question: "このキットで DJI ドローンをデコードできますか？"
    answer: "DJI の標準 Wi-Fi / BT Remote ID ブロードキャストは処理できます。ただし、DJI 独自の OcuSync DroneID は標準プロトコルに含まれておらず、ALFA アダプターではデコードできません。別途 SDR（ANTSDR / HackRF）＋ Kismet プラグインが必要です。両者は併用可能です。"
  - question: "Raspberry Pi はどの世代を使うべきですか？"
    answer: "Raspberry Pi 4（2 GB+）が最もバランスが良いです。Pi 3B は unix_rid_capture の原作者がテストで検証済みです。Pi 5 も使用可能ですが、放熱と電源に注意してください。Pi 内蔵 WiFi は安定してモニターモードに入れないため、必ず外付けの AWUS036ACH が必要です。"
  - question: "パッシブ受信は合法ですか？"
    answer: "ドローンが公開ブロードキャストする Remote ID を受信することは合法的な受信行為であり、公開情報の読み取りに相当します。ただし、能動的な妨害（jamming）は厳しく規制されており、本キットの範囲外です。"
---
> Yupitek テクニカルチーム｜ALFA Network 台湾正規代理店

{{< tldr >}}
Remote ID 検出キットは **ALFA AWUS036ACH** アダプターのモニターモードを利用して、ドローンが法令に従ってブロードキャストする身分情報と位置情報（ドローンの「中空ナンバープレート」）を受動的に受信します。施設のセキュリティ管理者にとって、合法的かつ低コストな状況認識手段です。
{{< /tldr >}}

---

## 1. Remote ID 検出キットが必要な理由

各国のドローン規制は「ブロードキャスト型身分識別」の時代に入っています。規格に従い、ドローンは空中で継続的に自身の情報をブロードキャストしなければなりません：

| ブロードキャストフィールド | 説明 |
|---|---|
| UAS / 操作者 ID | シリアル番号または登録コード |
| リアルタイム位置（緯度経度、高度） | WGS-84 / 気圧高度 |
| 速度、方位 | 水平 / 垂直速度 |
| 操作者位置 | 離着陸地点またはリアルタイム位置 |

ブロードキャストは2種類の無線キャリアを通じて行われます：

- **Bluetooth**：BT4 Legacy Advertising、BT5 Long Range（Extended Advertising）
- **Wi-Fi**：NAN（Wi-Fi Aware、2.4 / 5 GHz）、Beacon（2.4 / 5 GHz）

空港、産業団地、刑務所、大規模イベントなどの施設管理者にとって、**これらの公開ブロードキャストを受動的に受信する**ことは（ドローンの「機体番号」を確認することに相当）、法令に適合した低コストな状況認識手段であり、能動的な妨害は必要ありません。

{{< alert "triangle-exclamation" >}}
**合法性に関する注意**：本記事の手法はすべて**公開ブロードキャストのパッシブ受信**です。能動的な妨害（jamming）は各国で厳しく規制されており、本キットの範囲外であり、導入も推奨しません。
{{< /alert >}}

---

## 2. 製品の位置づけ：技術リスクが最も低いオープンソースパス

複数の技術パスを評価した結果、**ALFA AWUS036ACH** を中核とする組み合わせを選定しました：

- ALFA AWUS036ACH は **Realtek RTL8812AU** を搭載、デュアルバンド 2.4 + 5 GHz（802.11ac）、2×2 MIMO、2本の着脱可能 5 dBi 高ゲインアンテナ（RP-SMA）、USB 3.0 帯域幅十分。
- コミュニティ保守の `rtl88xxau` ドライバにより、安定した**モニターモード（Monitor Mode）**と**raw パケットインジェクション**をサポート——これが Wi-Fi RID Beacon / NAN フレームをキャプチャする前提条件です。
- 最も重要な点：`sxjack/unix_rid_capture` の README に **「Tested using an rtl8812au based WiFi dongle, an nRF52840 dongle and a Raspberry Pi 3B」** と明記されており、コミュニティがハードウェア検証を完了しています。このアーキテクチャをそのまま製品化することで、技術リスクを最小限に抑えられます。


---

## 3. ハードウェアリスト

| 項目 | 型番 / 仕様 | 役割 | 必要性 |
|---|---|---|---|
| **コアアダプター** | ALFA **AWUS036ACH**（RTL8812AU、デュアルバンド 2.4/5 GHz、USB 3.0、デュアル 5 dBi RP-SMA アンテナ） | Wi-Fi Remote ID キャプチャ（モニターモード） | **必須** |
| シングルボードコンピュータ | Raspberry Pi 4（2 GB+ 推奨；3B / 5 も可） | 演算ホスト | **必須** |
| ストレージ | microSD 16 GB+（Samsung / SanDisk Endurance 推奨） | システムディスク | **必須** |
| Bluetooth 5 キャプチャ | **nRF52840** USB Dongle（sniffer ファームウェア書き込み済み、Nordic Sniffer 等） | BT5 Long Range Remote ID キャプチャ | 推奨（オプション） |
| 電源 | 5 V / 3 A USB-C（公式 Pi PSU） | 供电 | **必須** |
| ネットワーク | イーサネットケーブル または WiFi 認証情報 | アップロード / 管理 | **必須** |
| アンテナアップグレード | ALFA **APA-M25** 指向性パネルアンテナ | 受信距離の延伸、環境ノイズの抑制 | オプション |

> 注：コミュニティプロジェクト `DroneAware` のオリジナルリストは **AWUS036N（Ralink RT3070、2.4 GHz シングルバンド）** を指定していました。本キットは **AWUS036ACH（デュアルバンド）** にアップグレードしており、2.4 / 5 GHz の **NAN と Beacon** の両方の Wi-Fi RID 伝送方式をカバーし、より完全で将来の拡張性に優れています。

---

## 4. ソフトウェアリスト

| ソフトウェア / パッケージ | 用途 | ソース |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | オペレーティングシステム（headless） | raspberrypi.com |
| **rtl88xxau ドライバ** | RTL8812AU モニター / インジェクションドライバ | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`、`libbluetooth-dev`、`libncurses-dev` | `unix_rid_capture` コンパイル依存 | APT |
| **opendroneid-core-c** | Open Drone ID メッセージエンコード/デコード C ライブラリ（ASTM F3411 / EN 4709-002） | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Linux Wi-Fi / BT RID キャプチャプログラム（JSON 出力） | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node（オプション） | ワンクリックでコミュニティリアルタイムマップに接続 | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR プラグイン（DJI パス） | DJI OcuSync DroneID デコード（SDR ハードウェア必要） | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) ＋ [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub プロジェクトリンク

```text
# コアデコードライブラリ（ASTM F3411 / EN 4709-002 メッセージエンコード/デコード）
https://github.com/opendroneid/opendroneid-core-c

# Linux キャプチャプログラム（本キットのメインプログラム、rtl8812au + nRF52840 + RPi 検証済み）
https://github.com/sxjack/unix_rid_capture

# コミュニティリアルタイムマップネットワーク（ワンクリックインストール、droneaware.io に自動アップロード）
https://github.com/fduflyer/DroneAware-Node-Releases

# 無線検出フレームワーク（DJI OcuSync パスは SDR プラグインと併用）
https://github.com/kismetwireless/kismet

# RTL8812AU モニター / インジェクションドライバ（AWUS036ACH に必須）
https://github.com/morrownr/8812au-20210629
```

---

## 6. Step-by-Step 設定

### ステップ 1 — システムの書き込み

**Raspberry Pi Imager** を使用して **Raspberry Pi OS Lite (64-bit)** を書き込みます。歯車アイコン（詳細設定）をクリック：

- ホスト名：`droneid-kit`
- SSH を有効化し、ユーザー名とパスワードを設定
- WiFi 認証情報を入力（後でイーサネットを接続しないため）

### ステップ 2 — 接続とハードウェア検証

AWUS036ACH を Pi の **USB 3.0** ポート（青色 / `SS` 表示）に直接挿入し、デュアルアンテナが確実に締まっていることを確認します。起動後 SSH で接続：

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

以下の表示を確認：

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### ステップ 3 — rtl88xxau モニタードライバのインストール

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### ステップ 4 — モニターモードの検証

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

出力に **`Mode:Monitor`** と表示されることを確認。

### ステップ 5 — コンパイル依存関係のインストール

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### ステップ 6 — opendroneid-core-c のコンパイル

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# libopendroneid/libopendroneid.so と test/odidtest が生成されます
```

### ステップ 7 — unix_rid_capture のコンパイル

`unix_rid_capture` は `opendroneid.c` / `opendroneid.h` を必要とします。前のステップからコピーします：

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### ステップ 8 — キャプチャの実行

root 権限または `cap_net_raw` が必要：

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # キャプチャして JSON として保存
```

リアルタイム UDP 出力（別のターミナルを開く）：

```bash
nc -lu 32001
```

### ステップ 9 — 軌跡の可視化（GPX → Google Earth）

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # .gpx を生成
```

Google Earth で開くとドローンの飛行経路が表示されます。典型的な検出 JSON の例：

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### ステップ 10 —（オプション）DroneAware コミュニティリアルタイムマップへの接続

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**セキュリティ注意**：`curl ... | sudo bash` 形式のサードパーティスクリプトは、事前にダウンロードして内容を確認してから実行することを推奨します：`curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`。インストーラは USB アダプターを自動検出し、ノード名を入力するよう促し、droneaware.io への登録をガイドします。検出結果はリアルタイムで live map に表示されます。
{{< /alert >}}


---

## 7. 重要な技術的区別：標準 RID vs DJI OcuSync

これはプロフェッショナルな価値が最も高い部分です。お客様に明確に説明してください：

| パス | 対象 | ハードウェア | ALFA AWUS036ACH は使用可能か |
|---|---|---|---|
| **標準 Remote ID** | ASTM F3411 Wi-Fi / BT ブロードキャスト | AWUS036ACH + nRF52840 | ✅ 可能（本記事の主体） |
| **DJI OcuSync DroneID** | DJI 独自プロトコル（非標準 Wi-Fi） | フル SDR（ANTSDR / HackRF / USRP）＋ Kismet `kismet_cap_antsdr_droneid` プラグイン | ❌ 不可 |

- ALFA AWUS036ACH は **Wi-Fi 帯域（2.4 / 5 / 6 GHz）受信機**であり、標準 RID を完全に処理できます。
- DJI 独自の **OcuSync** DroneID は標準 Wi-Fi プロトコルを使用しないため、**ALFA アダプターではデコードできません**。2.4 / 5.8 GHz をカバーする SDR（ANTSDR E200 等）と `alphafox02/antsdr_dji_droneid` + Kismet プラグインが必要です。
- ⚠️ 注意：**RTL-SDR の帯域幅上限は約 1.7 GHz** であり、2.4 / 5.8 GHz の OcuSync を受信できません。高周波対応の SDR を選択する必要があります。
- 2つのパスは**補完関係**です：ALFA アダプターで標準 RID ブロードキャストを検出し、SDR で DJI 独自プロトコルをデコードすることで、完全な Counter-UAV / RF 状況認識フロントエンドを構成します。

---

{{< faq >}}

---

## 付録：初心者向け用語集（キーワードをやさしく解説）

ドローン規制 / 対ドローン（Counter-UAV）技術に初めて触れる方のために、本記事で頻出する用語をわかりやすく説明します：

| 用語 | わかりやすい説明 |
|---|---|
| **Remote ID（リモートID）** | ドローンの「中空ナンバープレート」。法令により、ドローンは飛行中、自身の身分や位置などの情報を常にブロードキャストすることが義務付けられています。地上の人（特に規制当局）が「誰のドローンがどこへ飛んでいるか」を知ることができます。 |
| **ASTM F3411 / EN 4709-002** | それぞれ米国とEUが策定した Remote ID ブロードキャスト規格。ブロードキャストの内容と形式を規定し、異なるメーカーのドローンと検出機器間の相互運用性を確保します。 |
| **パッシブ検出（Passive Detection）** | ブロードキャストされた公開情報を「受信する」だけであり、ドローンに干渉したり攻撃するために能動的に信号を発信することはありません。合法性は能動的妨害（jamming）とは全く異なります。 |
| **monitor mode（モニターモード）** | WiFi アダプターがルーターに接続せず、空中の無線パケットを「純粋に受信」するモード。Remote ID ブロードキャストをキャプチャするための前提条件です。 |
| **NAN（Wi-Fi Aware）／ Beacon** | ドローンが Remote ID をブロードキャストするための2種類の Wi-Fi フレーム形式。本キットは両方の解析を試みます。 |
| **Bluetooth 5 Long Range** | Wi-Fi に加えて、一部のドローンは Bluetooth でも Remote ID をブロードキャストします。キャプチャには別途 nRF52840 が必要です。 |
| **DJI OcuSync / DroneID** | DJI 独自の映像 / テレメトリー伝送プロトコル。**標準 Wi-Fi ではない**ため、本記事では対応できません。別途 SDR ハードウェアとプラグインが必要です。詳細は第7節を参照。 |
| **SDR（Software Defined Radio、ソフトウェア無線）** | ソフトウェアで受信周波数範囲と復調方式を調整できる汎用無線ハードウェア。ANTSDR、HackRF などがあり、ALFA アダプターでは受信できない帯域（DJI OcuSync 等）をカバーできます。 |
| **RTL8812AU** | ALFA AWUS036ACH アダプターに使用されている Realtek のチップ型番。このチップがモニターモードをサポートするかどうかを決定します。 |
| **GPX ファイル** | GPS 座標の軌跡を記録する汎用フォーマット。Google Earth 等のソフトウェアで直接開き、ドローンの飛行経路を描画できます。 |

> 一言でまとめると：本記事は ALFA アダプターを「ドローン身分情報スキャナー」に変える方法を解説します。上空のドローンが法令に従ってブロードキャストする公開情報を受動的に受信するもので、施設セキュリティ管理の合法的な手段です。

---

## 参考ソース

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture（rtl8812au + nRF52840 + RPi 検証済み）](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — コミュニティ Remote ID 検出ネットワーク](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — 無線検出フレームワーク](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR デコード](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux モニター / インジェクションドライバ](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH 製品ページ（Yupitek）](https://yupitek.com/ja/products/alfa/awus036ach/)
8. [Yupitek お問い合わせ](https://www.yupitek.com/ja/contact/)

---

*本記事は Yupitek テクニカルチームが作成しました。AWUS036ACH および関連ハードウェアは Yupitek より正規代理店ルートでご購入いただけます。*
