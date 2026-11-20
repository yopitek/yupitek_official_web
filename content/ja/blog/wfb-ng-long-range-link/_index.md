---
title: "ALFA AWUS036ACH で自作する長距離ドローンデジタル映像伝送／テレメトリーリンク：wfb-ng オープンソースガイド（2026）"
description: "ALFA AWUS036ACH 無線LANアダプター＋オープンソースの wfb-ng を使って、低遅延・暗号化対応の長距離ドローンデジタル映像伝送と MAVLink テレメトリーリンクを構築します。完全なハードウェアリスト、Raspberry Pi 設定手順、電源周りのトラブルシューティングまで網羅。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "ドローン映像伝送", "デジタル映像伝送", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "長距離映像伝送", "テレメトリーリンク"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "wfb-ng と通常の WiFi の違いは何ですか？"
    answer: "通常の WiFi は接続（association）と ACK 確認応答が必要なため、長距離では効率が悪くレイテンシが高くなります。wfb-ng は raw パケットインジェクションを使用し、802.11 の接続機構をバイパスして FEC 前方誤り訂正でパケットロスに対処するため、エンドツーエンドの遅延を数十ミリ秒レベルに抑えられます。"
  - question: "なぜ機体側の ALFA 無線LANアダプターに独立した電源が必要ですか？"
    answer: "AWUS036ACH は送信（TX）時に瞬間的に大きな電力を消費します。Raspberry Pi の USB 2.0 ポートに直接接続すると、電力不足によりアダプターのポートがリセットされ、リンク断やパケット破損が発生します。5V BEC で独立給電し、+5V と GND 間に 470µF 低ESR コンデンサを並列接続してフィルタリングすることを推奨します。"
  - question: "接続しても映像もテレメトリーも表示されない場合は？"
    answer: "最も一般的な原因はキーの不一致です。機体側の drone.key と地上局側の gs.key が同じペアであることを確認してください。次に、両端の wifi_channel と link_domain の設定が完全に一致していることを確認します。journalctl -xu wifibroadcast@gs でリアルタイムログを確認してトラブルシューティングできます。"
  - question: "wfb-ng には必ず ALFA AWUS036ACH が必要ですか？"
    answer: "RTL8812AU チップを搭載した無線LANアダプターであれば理論上は使用可能ですが、AWUS036ACH は wfb-ng プロジェクトが公式にテストしたハードウェアであり、ドライバのサポートが最も安定しています。特に高出力・長距離のシナリオでは、ALFA のパワーデザインと着脱可能なアンテナの利点が顕著です。"
---
> 著者：Yopitek（ALFA Network 台湾正規代理店）テクニカルチーム
> 対象読者：ドローン愛好家、Maker、セキュリティ研究者、農業散布／点検ドローンの開発者
> 難易度：★★★☆☆（Linux とフライトコントローラーの基本知識が必要）

{{< tldr >}}
wfb-ng はオープンソースソフトウェアで、<strong>ALFA AWUS036ACH</strong> のような monitor mode に対応した無線LANアダプターをドローン専用の長距離無線機に「変身」させます。運用者は低遅延かつ暗号化された映像伝送と MAVLink テレメトリーリンクを自分で構築できます。
{{< /tldr >}}

---

## 一、なぜ ALFA アダプターでデジタル映像伝送を自作するのか？

従来のアナログ FPV（5.8GHz アナログ映像伝送）を経験したことがあれば、「スノーアンテナ」に悩まされたことはないでしょうか。信号が遮られると画面がノイズだらけになり、遠くに飛ばすと映像が途切れ始めます。さらに<strong>誰でも受信機一台で映像を盗み見できる</strong>——暗号化もなく、テレメトリーの帰還もありません。

私たちのチームはこの1年、農業散布、点検、さらにはセキュリティトレーニングの顧客向けにリンクを構築してきて、非常に実用的なニーズに気づきました：<strong>一般的な ALFA USB 無線LANアダプターとオープンソースソフトウェアを使って、自分たちで「デジタル化、暗号化対応、映像＋テレメトリー同時伝送」の長距離リンクを作れないか？</strong>

答えは「はい、可能です」——そして想像以上に簡単です。

従来のアナログ映像伝送と比較して、ALFA アダプターでオープンソースの <strong>wfb-ng</strong> を使ってデジタル映像伝送を構築するメリットは圧倒的です：

- <strong>低遅延</strong>：raw WiFi インジェクションモードが通常の 802.11 ACK と接続ハンドシェイクをバイパスし、エンドツーエンドの遅延を数十ミリ秒レベルに抑制。FPV の操作感はアナログに匹敵します。
- <strong>デジタル暗号化</strong>：映像とテレメトリーパケットは libsodium で暗号化され、第三者が受信機で映像やフライトデータを復号することはできません。
- <strong>1つのリンクでマルチタスク</strong>：同じ無線LANアダプター、同じ周波数で<strong>同時に</strong>伝送可能：
  - リアルタイム映像（RTP / RTSP）
  - MAVLink テレメトリー（双方向、フライトコントローラー ↔ 地上局）
  - TCP/IP トンネル（VPN、SSH、ファイル転送に利用可能）
- <strong>TX ダイバーシティ（送信ダイバーシティ）</strong>：複数のアダプターで送信ダイバーシティを構成し、遮蔽に強く、堅牢性を向上。
- <strong>オープンソースでカスタマイズ可能</strong>：ALFA AWUS036ACH とオープンソースの wfb-ng の組み合わせで、市販のデジタル映像伝送（DJI O3 / Walksnail 等）よりはるかに低コスト。<strong>完全オープンソースでカスタマイズ自由</strong>です。

{{< alert "circle-info" >}}
補足：この記事の目的は DJI 純正の映像伝送を「置き換える」ことではありません。<strong>リンクを自分で掌握したい、セカンダリーバックアップを構築したい、カスタムペイロードを開発したい</strong>という愛好家に向けた、実践的なオープンソースの選択肢を提供するものです。
{{< /alert >}}


---

## 二、wfb-ng とは

<strong>wfb-ng</strong>（Wireless Fibre / WiFi Broadcast – next generation）は、オープンソースのデジタル FPV とテレメトリーのためのプロジェクトです。その中核となる発想は非常に賢いものです：

> WiFi を「ネットワーク」として使うのではなく、「無線機」として使う。

通常の 802.11 はローカルエリアネットワークとして動作するため、接続（association）、ACK 確認、再送信を行います。これらの機構は長距離・移動・低信号のシナリオでは速度を低下させ、通信距離を制限します。wfb-ng は <strong>raw WiFi インジェクション（raw WiFi injection）</strong> を採用しています：

- アダプターを <strong>monitor mode（モニターモード）</strong> で動作させ、誰とも「接続」しません。
- 低レベルの WiFi パケットを直接注入し、<strong>ACK も再送信も不要</strong>（パケットロスには FEC 前方誤り訂正で対応）。
- 通常の 802.11 の距離と遅延の制限をバイパスし、伝送距離と安定性をハードウェアの限界まで引き出します。

簡単に言えば、一般的な USB 無線LANアダプターを「デジタル無線機」のペアに変え、その上で RTP 映像、MAVLink テレメトリー、さらには IP トンネルを動作させることができます。

- プロジェクトページ（GitHub）：https://github.com/svpcom/wfb-ng.git
- 現在、PX4 / ArduPilot エコシステムでの自作デジタル映像伝送に広く使用されており、コミュニティは活発です。ウクライナの自作ドローンコミュニティでもよく使われるオープンソースリンク方式です。

---

## 三、主役：ALFA AWUS036ACH

このリンクの「無線機」はまさにこれ——<strong>ALFA AWUS036ACH</strong> です。

<strong>Realtek RTL8812AU</strong> チップを搭載し、<strong>802.11ac（WiFi 5）</strong>、<strong>2.4GHz / 5GHz デュアルバンド</strong>、USB 3.0 Type-C インターフェース、着脱可能アンテナ（RP-SMA）に対応しています。さらに重要なのは：<strong>wfb-ng の公式テストハードウェアは、両端に AWUS036ACH を使用し、5GHz モードで動作することです</strong>。つまり、このアダプターはプロジェクト作者によって検証され、ドライバサポートが最も安定しているモデルです。

選定理由は3つ：

1. <strong>出力が十分</strong>：ALFA の一貫した高出力設計と、外部高ゲインアンテナの組み合わせにより、長距離性能は一般的なノートPC内蔵アダプターをはるかに上回ります。
2. <strong>モニターモード ＋ インジェクション対応</strong>：RTL8812AU はパッチ適用済みドライバ（後述）のもとで、monitor mode と raw パケットインジェクションを安定してサポートします。これは wfb-ng 動作の必須条件です。
3. <strong>汎用性と耐久性</strong>：USB インターフェースで、機体側と地上局側で共通して使用可能。故障時も該当アダプターのみ交換すればよく、メンテナンスが容易です。

{{< alert "triangle-exclamation" >}}
<strong>注意</strong>：wfb-ng には<strong>パッチ適用済みの専用ドライバ</strong>（`rtl88xxau_wfb` など）が必要です。通常の Linux 内蔵ドライバでは wfb-ng が必要とするインジェクションモードに入ることができません。インストール方法は後述の「ソフトウェアリスト」と「Step-by-step 設定」を参照してください。
{{< /alert >}}

---

## 四、ハードウェアリスト（Hardware List）

リンクは<strong>機体側（Drone）</strong>と<strong>地上局（Ground Station）</strong>の2セットに分かれます。

### 機体側（Drone）

| 項目 | 推奨モデル / 説明 |
|---|---|
| 機体側コンピュータ | Raspberry Pi 3B / 3B+ / Zero 2 W / 4（いずれか。1080p を使用する場合は <strong>Pi 4 または Zero 2 W</strong> を推奨） |
| カメラ | Raspberry Pi Camera（CSI インターフェース）または Logitech C920（USB インターフェース） |
| WiFi モジュール | <strong>ALFA AWUS036ACH</strong>（または任意の RTL8812AU チップ搭載アダプター） |
| 電源 | <strong>5V BEC</strong>（アダプターへの独立給電、後述の「トラブル注意点」参照） |
| フィルタコンデンサ | <strong>470µF 低ESR コンデンサ</strong>（アダプターの +5V と GND 間に並列接続） |
| フライトコントローラー | Pixhawk 等（MAVLink プロトコル、UART 経由で機体側コンピュータに接続） |

### 地上局（Ground Station）

| 項目 | 推奨モデル / 説明 |
|---|---|
| コンピュータ | Linux コンピュータ（Ubuntu / Debian x86-64）、または別の Raspberry Pi |
| WiFi モジュール | <strong>ALFA AWUS036ACH</strong> |
| 監視ソフトウェア | <strong>QGroundControl</strong> を実行するマシン（地上局コンピュータと同一で可） |

> 注：<strong>受信専用（RX）</strong> の場合は、monitor mode に対応したアダプターであれば何でも使用可能です。例えば OpenWRT をインストールしたルーターも地上局の受信機として利用できます。ただし、公式テストと本記事の設定は AWUS036ACH を基準としています。

---

## 五、ソフトウェアリスト（Software List）

### オペレーティングシステム

- <strong>Raspberry Pi OS</strong> / <strong>Debian</strong> / <strong>Ubuntu</strong>（Linux kernel >= 4.x）

### コアプロジェクト

- <strong>wfb-ng</strong>（svpcom/wfb-ng）：デジタル映像伝送 / テレメトリー メインプログラム
- <strong>パッチ適用ドライバ</strong>：
  - RTL8812AU -> `svpcom/rtl8812au`（branch <strong>v5.2.20</strong>、dkms でインストール）
  - RTL8812EU -> `svpcom/rtl8812eu`
  - ドライバロード後、アダプター名は `rtl88xxau_wfb`（または `rtl8812eu`）と表示されます

### システム依存パッケージ

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### 暗号化

- <strong>libsodium</strong>：`wfb_keygen` で `drone.key`（機体側）と `gs.key`（地上局側）を生成

### 地上局再生

- <strong>QGroundControl</strong>：地上局でフライトコントローラーの状態とテレメトリーを監視
- <strong>GStreamer / RTSP</strong>：機体側からの映像ストリームを受信・再生

---

## 六、GitHub リンクと ALFA AWUS036ACH 仕様カード

### 公式リンク

| 項目 | リンク |
|---|---|
| wfb-ng プロジェクト | https://github.com/svpcom/wfb-ng.git |
| パッチ適用ドライバ（RTL8812AU） | https://github.com/svpcom/rtl8812au |
| パッチ適用ドライバ（RTL8812EU） | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH 製品ページ | https://yupitek.com/ja/products/alfa/awus036ach/ |
| PX4 WFB-ng チュートリアル | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH 仕様カード

| 仕様 | 内容 |
|---|---|
| チップ | Realtek <strong>RTL8812AU</strong> |
| 無線規格 | 802.11a / b / g / n / <strong>ac（WiFi 5）</strong> |
| 周波数帯 | <strong>2.4GHz + 5GHz</strong> デュアルバンド |
| インターフェース | USB 3.0 <strong>Type-C</strong> |
| アンテナ | 2 x 着脱式 <strong>RP-SMA</strong>（2T2R MIMO） |
| モニターモード | monitor mode + パケットインジェクション対応（wfb-ng patch ドライバが必要） |
| wfb-ng ドライバ | `rtl88xxau_wfb`（svpcom/rtl8812au, v5.2.20） |
| 位置づけ | wfb-ng <strong>公式テスト済みアダプター</strong>（両端 5GHz モード） |


---

## 七、Step-by-step 設定（核心章節）

以下の4セクションに分かれます。最も推奨するのは <strong>A（Raspberry Pi クイックスタート）</strong> で、イメージを書き込むだけですぐに使えます。<strong>B</strong> は x86 Linux デスクトップに手動で地上局をインストールしたい方向けです。<strong>C / D</strong> はキーペアと設定ファイルの重要ポイントで、どちらのパスでも必要になります。

### A. Raspberry Pi クイックスタート（最も推奨）

wfb-ng 公式が事前にパッケージ化された Raspberry Pi イメージを提供しています。機体側と地上局側でそれぞれ1枚ずつ書き込めば、起動するだけで使用できます。

<strong>1. イメージのダウンロードと書き込み</strong>

wfb-ng の GitHub <strong>Releases</strong> ページから最新の `*.img.gz` をダウンロードし、解凍して<strong>2枚</strong>の SD カード（機体側、地上局側各1枚）に書き込みます。

```bash
# イメージの解凍 (例, ファイル名は実際の Release に従ってください)
gunzip wfb-ng-*.img.gz
# Raspberry Pi Imager または dd / balenaEtcher で SD カードに書き込み
```

<strong>2. アダプター挿入、起動、SSH ログイン</strong>

両方のカードに ALFA AWUS036ACH を挿し、電源を入れて起動し、SSH でログインします（デフォルト IP と認証情報は以下の通り）：

```bash
ssh pi@192.168.0.111
# パスワード: raspberry
```

<strong>3. 地上局（Ground Station）サービスの有効化</strong>

<strong>地上局側の Pi</strong> で以下を実行：

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

<strong>4. 機体側（Drone）サービスの有効化</strong>

<strong>機体側の Pi</strong> で以下を実行：

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

<strong>5. 地上局でリンク状態を監視</strong>

```bash
wfb-cli gs
```

> 接続、チャンネル、パケットロス率などの情報が表示されればリンクは確立されています。その後 QGroundControl を開けば、テレメトリーと映像が表示されます。

---

### B. Debian / Ubuntu 地上局手動インストール

x86-64 の Linux デスクトップ / ノート PC を地上局として使用する場合は、手動インストールが可能です。

<strong>1. dkms とパッチ適用ドライバのインストール</strong>

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

<strong>2. アダプターが wfb-ng ドライバに制御されていることを確認</strong>

```bash
# wlan0 が表示され, MTU が 2312 であることを確認
ifconfig

# ドライバ名が rtl88xxau_wfb (RTL8812AU) または rtl8812eu (RTL8812EU) と表示されることを確認
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
`ethtool -i wlan0` が通常の `rtl8812au` と表示され、`rtl88xxau_wfb` でない場合、パッチドライバが正しくインストールされていません。wfb-ng はインジェクションモードに入れなくなります。dkms インストール時のエラーを確認してください。
{{< /alert >}}

<strong>3. 公式自動インストールスクリプトの実行</strong>

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

<strong>4. リンクの監視</strong>

```bash
wfb-cli gs
```

---

### C. キーとペアリング

wfb-ng の映像とテレメトリーは暗号化されています。機体側と地上局側で<strong>対応するキー</strong>を使用する必要があります。

```bash
# キーの生成 (機体側で生成し, 配布)
wfb_keygen

# drone.key を機体側に配置
# gs.key    を地上局側に配置
# 両端で対応している必要があります. そうしないと復号できず, リンクは"接続済みだがデータなし"と表示されます
```

> <strong>B セクションの自動インストールスクリプト（install_gs.sh）</strong> を使用する場合、スクリプトが自動的にキーを生成・設定するため、手動ペアリングは不要です。手動インストールの場合は、必ず `drone.key` と `gs.key` が同じペアであることを確認してください。

---

### D. 設定ファイルの重点：/etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` は wfb-ng の中核設定ファイルです。以下は最も頻繁に調整が必要なパラメータです：

```ini
[common]
# チャンネル 165 = 5825 MHz (5.8GHz 帯)
wifi_channel = 165

# 国コードを 'BO'(ボリビア) に設定すると最大送信電力が解放される
wifi_region = 'BO'

[drone]
# 機体側と地上局の link_domain は"完全に一致"している必要があります
link_domain = "my_wfb_link_01"

[drone_mavlink]
# フライトコントローラーの UART から MAVLink を受信 (フライトコントローラー側の UART を 1500000 baud に設定)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# 同上, 両端で一致
link_domain = "my_wfb_link_01"
```

<strong>最も間違いやすい3つのポイント：</strong>

1. <strong>`wifi_channel` を両端で一致させる</strong>：本記事では 165（5825 MHz, 5.8GHz）を使用。機体側と地上局側で同じチャンネルを設定してください。
2. <strong>`link_domain` を両端で一致させる</strong>：これがリンクの「識別子」です。一致しないと接続できません。
3. <strong>フライトコントローラーの UART ボーレートを 1500000 に設定</strong>：`peer = 'serial:ttyS0:1500000'` は、フライトコントローラー側の UART も 1500000 baud に設定されていることを前提としています。

{{< alert "triangle-exclamation" >}}
<strong>注意</strong>：`wifi_region = 'BO'` は送信電力の上限を解放するためのものです。<strong>これはお住まいの地域で合法的に使用できることを意味するものではありません</strong>。後述の「法規に関する注意」を必ず参照してください。
{{< /alert >}}

---

## 八、実装上の注意事項／トラブルポイント

このセクションは私たちが実際に遭遇したトラブルです。必ずお読みください。

### トラブル 1：アダプターの電力不足によるポートリセットとパケットロス

AWUS036ACH は<strong>送信（TX）時に瞬間的に大きな電力を消費します</strong>。Raspberry Pi の通常の USB2 ポートに直接接続すると、Pi の USB 給電が瞬間的な電流に耐えられず、<strong>アダプターポートのリセット、リンク断、パケット破損、画面フリーズ</strong>が発生します。

解決策（機体側では必ず実施）：

- アダプターは<strong>5V BEC から直接給電</strong>（Pi の USB から取らないでください）。BEC 出力をアダプターに接続します。
- アダプターの <strong>+5V と GND 間に 470µF 低ESR コンデンサを並列接続</strong>してフィルタリングし、TX 時の電流スパイクを吸収します。
- 地上局側で<strong>ノートPCの USB3 ポート、純正 USB3 ケーブル</strong>を使用する場合は、通常は直接給電可能で、追加の BEC は不要です。

> この手順が「安定するかどうか」の鍵です。パケットロスで悩んでいる多くのケースは、結局給電の問題でした。

### トラブル 2：暗号化エラー／接続できない

`wfb-cli gs` で接続済みと表示されるが<strong>映像もテレメトリーも表示されない</strong>場合、原因は以下の2つであることがほとんどです：

- <strong>キーの不一致</strong>：機体の `drone.key` と地上局の `gs.key` が同じペアか確認してください。
- <strong>チャンネルまたは link_domain の不一致</strong>：両端の `wifi_channel` と `link_domain` が完全に同一である必要があります。

トラブルシューティングコマンド：

```bash
# 地上局サービスのリアルタイムログを確認し, 暗号化/接続関連のエラーを探す
journalctl -xu wifibroadcast@gs
```

### トラブル 3：法規に関する注意（非常に重要）

このリンクは能動的に電波を発射するため、無線設備の使用に関する行為に該当します。

- <strong>使用前に、お住まいの地域でこのような WiFi 用途の送信電力と周波数帯が許可されていることを確認してください。</strong>
- 日本、欧米では 5.8GHz ISM 帯の送信電力、利用可能チャンネル、および「非接続型送信」に関する規制がそれぞれ異なります。
- 本記事の `wifi_region = 'BO'` はハードウェアの出力上限を解放するためのものですが、<strong>日本を含む各地域で合法的であることを意味するものではありません</strong>。お住まいの国・地域の電波法規に従ってチャンネルと出力を調整し、必要に応じて送信電力を下げるか、合法チャンネルに変更してください。
- 合法的なエリア（私有農地、クローズドテスト環境、教育訓練など）でのみ使用し、他者の通信を妨害しないでください。

---

## 九、まとめ

振り返ってみると、私たちは1枚の ALFA AWUS036ACH とオープンソースの wfb-ng を使って、以下の特長を持つシステムを構築できました：

- <strong>コスト優位性</strong>：自作リンクの材料費は市販のデジタル映像伝送ソリューションをはるかに下回ります。
- <strong>オープンソース</strong>：すべてのコード、ドライバ、設定が公開されており、確認可能です。
- <strong>カスタマイズ可能</strong>：チャンネル、出力、キー、MAVLink の公開方法をすべて自分で制御できます。
- <strong>長距離</strong>：デジタル映像伝送とテレメトリーを一体化。5GHz での実測距離はアナログをはるかに超え、遮蔽に強く、暗号化も可能です。

農業散布、点検、セキュリティトレーニング、あるいは純粋に「デジタル映像伝送の背後にある原理」を理解したい愛好家にとって、これは非常に価値のある実践的な道です。

私たちのチームは引き続きブログで ALFA アダプターを使ったドローンリンクの実装ノートを発信していきます。構築中に問題が発生した場合は、ぜひコメントでお知らせください——<strong>実際に手を動かすことが、最も速い学習方法です</strong>。


---

{{< faq >}}

---

## 付録：初心者向け用語集（キーワードをやさしく解説）

この種の技術に初めて触れる方のために、本記事で頻出する用語をわかりやすく説明します：

| 用語 | わかりやすい説明 |
|---|---|
| <strong>FPV</strong>（First Person View） | 「一人称視点」。ドローンの「操縦席」に座って飛んでいるかのように、機体カメラからの映像がリアルタイムで画面やゴーグルに表示されます。 |
| <strong>デジタル映像伝送 vs アナログ映像伝送</strong> | アナログは旧式テレビ信号のように、信号が弱くなるとノイズが発生し、誰でも受信可能。デジタルは映像をデジタルパケットに変換して伝送するため、暗号化が可能でノイズ耐性に優れますが、ハードウェアと設定は複雑です。 |
| <strong>monitor mode（モニターモード）</strong> | 通常の WiFi アダプターはルーターに「接続」してデータを送受信します。monitor mode ではアダプターが「何にも接続せず、空中の無線信号を直接傍受・送信」するようになります。本記事の技術的基盤です。 |
| <strong>packet injection（パケットインジェクション）</strong> | monitor mode で、カスタム無線パケットを通常の WiFi 接続プロセスを介さずに直接空中に「射出」します。wfb-ng はこの仕組みを利用して映像とテレメトリーを伝送します。 |
| <strong>wfb-ng</strong> | WiFi アダプターを通常のネットワーク機器ではなく、ドローン専用の無線機として「生まれ変わらせる」オープンソースソフトウェア。本記事の中核ソフトウェアです。 |
| <strong>FEC（前方誤り訂正、Forward Error Correction）</strong> | 送信時にあらかじめ「バックアップ情報」を追加で送っておき、一部のパケットが空中で失われても、受信側がそのバックアップ情報を使って元の映像を復元できる仕組み。再送信（長距離・高速移動シーンでは速度低下の原因に）を不要にします。 |
| <strong>MAVLink</strong> | ドローンのフライトコントローラー（Pixhawk 等）と地上局が通信するための「共通言語」プロトコル。飛行状態の送信や飛行指令の伝達など、テレメトリーデータのやり取りに使用されます。 |
| <strong>RTP / RTSP</strong> | インターネット上でリアルタイム映像を伝送するための一般的なプロトコル。スマートフォンのIPカメラや監視カメラの多くも同様のプロトコルで映像を配信しています。 |
| <strong>libsodium 暗号化</strong> | 本記事で映像とテレメトリーデータの暗号化に使用するオープンソース暗号化ライブラリ。正しくペア設定されたキーを持つ機体側と地上局のみが映像を復号できます。 |
| <strong>TX ダイバーシティ（送信ダイバーシティ）</strong> | 複数のアダプターで同一データを同時送信します。1つのアダプターの信号が遮蔽されても、別のアダプターが補完する「二重の保険」のような仕組みです。 |
| <strong>BEC（Battery Eliminator Circuit）</strong> | ドローンバッテリーの電圧をアダプターが必要とする 5V に降圧する安定化電源モジュール。アダプターの瞬間的な大電流需要にも対応し、給電不安定によるリンク断を防止します。 |
| <strong>RTL8812AU</strong> | ALFA AWUS036ACH アダプターに使用されている Realtek のチップ型番。このチップが monitor mode とパケットインジェクションに対応しているかどうかを決定します。 |

> 一言でまとめると：wfb-ng は ALFA アダプターをドローン専用の無線局に「変身」させ、映像とフライトデータをオープンソース・暗号化・長距離で伝送できるようにします。これは運用者が自ら構築する「自分だけの専用チャンネル」です。

---

## 参考リソース

- <strong>wfb-ng プロジェクト（svpcom/wfb-ng）</strong>：https://github.com/svpcom/wfb-ng.git
- <strong>ALFA AWUS036ACH 製品ページ</strong>：https://yupitek.com/ja/products/alfa/awus036ach/
- <strong>パッチ適用ドライバ（RTL8812AU）</strong>：https://github.com/svpcom/rtl8812au
- <strong>パッチ適用ドライバ（RTL8812EU）</strong>：https://github.com/svpcom/rtl8812eu
- <strong>PX4 WFB-ng チュートリアルドキュメント</strong>：https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*本記事は Yopitek（ALFA Network 台湾正規代理店）テクニカルチームが、wfb-ng 公式ドキュメントと実装経験に基づいて作成しました。実装前には、必ずお住まいの地域の電波法規を確認し、規定に従って送信電力と周波数を調整してください。*
