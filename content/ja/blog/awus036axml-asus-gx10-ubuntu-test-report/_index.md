---
title: "AWUS036AXML 実測：Wi-Fi 6 + Bluetooth 複合アダプターを ASUS GX10（ARM64 / Ubuntu 24.04）で検証――AP は安定、injection は失敗という正直なレポート"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML（Wi-Fi＋Bluetooth）を ASUS GX10／Ubuntu 24.04 ARM64 で実測：AP、WPA3、monitor は利用可能ですが、injection は失敗し handshake も取得できません。ペネトレーションテストには非推奨です。"
faq:
  - question: "AWUS036AXML でパケットインジェクション（packet injection）はできますか？"
    answer: "当社のテストプラットフォーム（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）ではできません。aireplay-ng --test は No Answer、Found 0 APs と報告し、AP を指定して個別にテストしても No such BSSID available が返るだけでした。通常のスキャンではその AP が見えていても（約 -54 dBm）、インジェクションツールの状況ではその beacon を受信できないため、deauth も handshake の取得（0 件）も利用できません。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションであり、チップが本質的にインジェクション不能というわけではありません。AWUS036AXM も同じ結果です。インジェクションが必要な場合は AWUS036EACS、ACH、ACS をお選びください。"
  - question: "AWUS036AXML の Bluetooth は Ubuntu で使えますか？"
    answer: "本機での実測では Bluetooth は利用可能でした。bluetoothctl／hciconfig で hci コントローラーが UP であることを確認し、BLE とクラシック Bluetooth のデバイスをスキャンでき、Wi-Fi と Bluetooth を同時に使用できます（共存）。Wi-Fi＋Bluetooth の複合デバイスです。なお、再接続時にまれに WiFi probe で止まり、wlx インターフェースが生成されないことがありますが、別の USB ポートに挿し直せば回復します。"
  - question: "AWUS036AXML は Ubuntu 24.04 で別途ドライバのインストールが必要ですか？"
    answer: "不要です。mt7921u ドライバは kernel 6.17 に内蔵されており、挿した後の dmesg で mt7921u がインターフェース名を wlx に MAC を加えた名前へ変更するのが確認できます（USB ID 0e8d:7961）。DKMS もコンパイルも不要です。ドライバは IBSS と mesh モードを提供しません。"
  - question: "AWUS036AXML は AP を開けますか？WPA3 に対応していますか？"
    answer: "開けます。これが最も安定した用途です。2.4 GHz（802.11n、MCS 10）と 5 GHz VHT80（VHT-NSS2）のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は sae_pwe=0 で iPhone 15 Pro が接続でき（MFP: yes。2.4 GHz と 6 GHz で実測、5 GHz は未実測）、STA＋AP の同時動作時の STA 側 ping は約 4.4 ms でした。Wi-Fi 6 チップという位置づけですが、本機では 6 GHz band も利用可能であることを実測しました（6135 MHz の AP を自前で構築し、iPhone 15 Pro が 802.11ax で接続して IP を取得）。"
  - question: "AWUS036AXML と AWUS036AXM の違いは何ですか？どちらを選ぶべきですか？"
    answer: "本プラットフォームでは 2 製品の Wi-Fi の挙動は同じです。どちらも mt7921u を使用し、injection は同様に失敗し、monitor の受信も同様に弱く、AP、WPA3、VIF は同様に利用できます。違いは、AXML には Bluetooth があり（本機で利用可能を実測）、本機で 6 GHz band も利用可能を実測した点です。AXM の Bluetooth と 6 GHz は今回個別に実測していません。純粋な AP や一般的な接続ならどちらを選んでも構いません。injection や handshake が必要なら、どちらも選ばないでください。"
draft: false
---

{{< tldr >}}AWUS036AXML は ASUS GX10／Ubuntu 24.04 ARM64 で AP、WPA3、VIF、受動 monitor が利用でき、Bluetooth と 6 GHz band も本機での実測で利用可能でした。ただし injection は実測で失敗し（No Answer／Found 0 APs）、deauth も handshake の取得もできないため、ペネトレーションテストには推奨しません。位置づけは純粋な AP と一般接続用です。{{< /tldr >}}

ALFA AWUS036AXML は、この 9 製品の中で唯一の「MediaTek Wi-Fi 6 + Bluetooth」複合型番です。Bluetooth なしの AWUS036AXM と同じ世代のチップ（MT7921、`mt7921u` ドライバで動作）で、違いは Bluetooth が追加されている点だけです。お客様から最もよく聞かれるのは、やはり次の 3 つです。monitor に入れるか、injection はできるか、AP は構築できるか。本記事では AWUS036AXML を単独で取り上げ、ASUS GX10（ARM64）と Ubuntu 24.04 で項目ごとに実測し、できること・できないことを一度で明らかにします。特に最も重要な制限は、**このプラットフォームでは injection が失敗する**ことです。

まず位置づけをはっきりさせておきます。以下の測定はすべて、Yupitek の自社設備、自社オフィスの Wi-Fi（SSID `YUPITEK`）、自社のテスト用スマートフォン（iPhone 7 Plus、WPA3 は iPhone 15 Pro でも再テスト）で実施しました。これは代理店による製品の互換性と機能の限界に関するハードウェア検証であり、第三者のネットワークに対する操作の解説ではありません。本文中の monitor、AP、injection のセルフテストは、すべて自社の閉じた環境で、自社デバイスを対象に行っています。

## 一、このアダプターとテストプラットフォーム

- **計算プラットフォーム**：ASUS GX10（ARM64 / aarch64）
- **OS**：Ubuntu 24.04 LTS
- **カーネルバージョン**：kernel 6.17.0-1014-nvidia
- **テスト対象アダプター**：ALFA AWUS036AXML（MediaTek MT7921AUN、Wi-Fi 6 / 2x2 / +BT）
- **テストデバイス**：Apple iPhone 7 Plus（WPA3-SAE は iPhone 15 Pro でも再テスト）
- **テスト環境**：自社オフィスの Wi-Fi、SSID `YUPITEK`、2.4GHz ch5 / 5GHz ch36、ch157
- **テスト期間**：2026-11-16 から 2026-11-18 まで実機で測定

すべての結果は、実際に測定した数値や状態を記録したもので、スペックシートからの推測ではありません。MAC アドレスは出力中で `xx` によりマスクしています。

## 二、ハードウェアとドライバ：MT7921AUN、挿すだけで使用可能

| 項目 | 仕様 |
|---|---|
| 型番 | AWUS036AXML |
| チップ | MediaTek MT7921AUN |
| USB ID | `0e8d:7961`（MediaTek Inc. Wireless_Device） |
| in-kernel ドライバ | `mt7921u` |
| 世代 / ストリーム | Wi-Fi 6 / 2x2（2T2R） |
| Bluetooth | あり（BT + WiFi 複合デバイス。本機の実測で hci コントローラーは UP、BLE とクラシック Bluetooth のデバイスをスキャン可能、WiFi+BT は共存） |
| USB 列挙 | USB 3 |
| インターフェース名 | `wlx<MAC>`（例：`wlx00c0cabd65b9`） |

認識の確認は簡単です。挿した後、`lsusb` で MediaTek の USB ID を確認し、`dmesg` で `mt7921u` がマウントされてインターフェース名が変更されることを確認します。

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

ポイントは 2 つあります。1 つ目はコンパイル不要であることです。AWUS036AXML は kernel 6.17 内蔵の `mt7921u` ドライバで動作し、挿すだけで認識されるため、aarch64 上で out-of-tree の DKMS モジュールを扱う必要がなく、ARM64 プラットフォームでは特に手間がかかりません。2 つ目は USB 3 で列挙される点です（旧世代の一部の型番は OTG ケーブルが USB 2.0 のみでした）。転送帯域がボトルネックになることはありません。

よく誤解される点を補足します。AWUS036AXML は Wi-Fi 6（6E ではない）チップという位置づけですが、**本機での実測では 6 GHz band が利用可能でした**。6135 MHz の AP を自前で構築し、iPhone 15 Pro が 802.11ax で接続して IP を取得しました。Bluetooth も実測で利用可能でした。`hciconfig`／`bluetoothctl` で hci コントローラーの状態が UP であることを確認し、BLE とクラシック Bluetooth のデバイスをスキャンでき、Wi-Fi と Bluetooth を同時に動作させられます（共存）。

対応するインターフェースモードを確認すると、選定上意味のある細かな点が見えてきます。IBSS も mesh point もないことです。

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

つまり、managed、AP、monitor、P2P はありますが、ad-hoc（IBSS）と 802.11s mesh の 2 つのモードは、`mt7921u` ドライバがそもそも提供していません。mesh / IBSS の実験をしたいお客様は、このアダプターは対象外です（`mt76` の ACM / ACHM を検討してください）。

## 三、実測した機能：Monitor / AP / WPA3、そして injection についての正直な制限

主要機能を一覧にまとめます。

| 機能 | 2.4GHz | 5GHz | 説明 |
|---|---|---|---|
| Monitor | ✅（弱い） | ✅（弱い） | beacon は記録できる。client / data パケットは取りこぼしが多い |
| **Injection** | ❌ **失敗** | ❌ **失敗** | `aireplay-ng` の注入 / deauth は動作しない。根本原因は kernel 6.16+ mac80211 chanctx のリグレッション（チップ本来の制限ではない） |
| AP アクセスポイント | ✅ 802.11n を含む | ✅ VHT80（80MHz） | iPhone 7 Plus が接続、`authorized: yes` |
| WPA3-SAE | ✅ | 未実測 | iPhone 15 Pro が接続、`MFP: yes`（`sae_pwe=0`）。6 GHz（ch37、6135 MHz）でも実測 |

### Monitor：両バンドで入れるが、受信は弱め

AWUS036AXML は、2.4GHz（ch1 / 6 / 11）と 5GHz（ch36 / 149 / 157）のどちらでも monitor mode に入れ、beacon の記録には問題ありません。設定手順は標準的な `iw dev` の 4 ステップです。

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # 2.4GHz は set channel 6 を使用
```

正直に言うと、このアダプターの monitor の受信は、同じ検証セットの MT7612U（ACM）や Wi-Fi 6 の AXER と比べて明らかに弱いです。beacon は取得できますが、client / data パケットは取りこぼしが多く、`airodump-ng` でホッピングスキャンを行うと一部の AP を見逃しやすくなります。実用上は、ホッピングではなく単一チャンネル（`-c <ch>`）に固定することをお勧めします。そのほうが取得結果が安定します。また、monitor モードでは `iw info` が txpower を 3 dBm と報告しますが、これは**報告上の見かけの値**です（ハードウェアの実際の TX は約 20–23 dBm で、`txpower_sku` により確認済み）。電力が本当に 3 dBm まで抑えられているわけではありません。この点は後の「注意事項」でもあわせて触れます。

### AP アクセスポイント：2.4GHz は HT を維持、5GHz は VHT80 まで可能

AP は AWUS036AXML が最も安定している領域です。2.4GHz では 802.11n（HT）をそのまま維持でき、シングルアンテナの ACHM のように HT を無効にする必要はありません。5GHz では VHT 80MHz まで設定できます。どちらのバンドでも iPhone 7 Plus が接続し、`authorized: yes` となることを実測しました。

5GHz VHT80 の hostapd の主要な設定は次のとおりです。

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

実測では、接続後は VHT-NSS2、80MHz でした。2.4GHz 版は `hw_mode` を `g`、`channel=6` に変更し、`ieee80211n=1` と `ht_capab=[HT20]` を残せば、iPhone の接続は MCS 10（802.11n）になります。

### WPA3-SAE：利用可能、sae_pwe=0 を忘れずに

AP の `wpa_key_mgmt` を `SAE` に変更し、`ieee80211w=2` と `sae_pwe=0` を加えれば、WPA3-SAE を有効にできます。実測では iPhone 15 Pro が 2.4 GHz（および 6 GHz。5 GHz は未実測）で接続でき、`authorized: yes`、`MFP: yes` でした。`sae_pwe=0` は古い iPhone との互換性のためで、この点は ACHM の落とし穴と同じです。`sae_pwe=2` では古い端末が接続できないことがよくあります。

### VIF：ネットに接続しながらアクセスポイントも開ける、可能

AWUS036AXML は複数インターフェースの同時動作に対応しています。AP VIF（別の MAC、unmanage）を作成し、メインインターフェースを Wi-Fi に接続して、同じチャンネルで AP を開いたところ、iPhone 7 Plus が AP VIF に接続している間、STA から `YUPITEK` への ping は 4.4 ms でした。「1 枚のアダプターでネットに接続しつつアクセスポイントも共有する」という用途は成立します。

### 正直な制限：本プラットフォームでは injection が失敗する

これは AWUS036AXML（および Bluetooth なしの双子である AXM）について、最も明確に伝えるべき項目です。ASUS GX10 + kernel 6.17 で、自社のテスト環境に対して injection のセルフテストを行った結果は、失敗でした。

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

自社 AP の BSSID を指定して個別にテストしても、返ってくるのは `No such BSSID available` だけでした。肝心な点は、通常のスキャンではその AP が確かに見えている（信号 -54 dBm）にもかかわらず、injection ツールの状況に入ると、このアダプターはターゲットの beacon を「聞き取れなく」なり、deauth を送信できず、4-way handshake の取得数は 0 になることです。

これはパラメータの調整不足でも、個体の故障でもありません。真の根本原因は**ソフトウェア層**にあります。kernel 6.16 以降、mac80211 の channel context（chanctx）にリグレッションが発生し、stock ドライバが injection の状況でターゲットの beacon を受信できなくなります。そのため `aireplay-ng` は `No Answer` と判定します。**MT7921 チップが本質的に injection できないわけではありません**。この現象は morrownr/USB-WiFi の issue #387 に記録されており、根本原因の分析は morrownr/mt76 の issue #18 にあります。コミュニティの実測では、同じ型番で git／パッチ適用済みのドライバを使うと active monitor と injection が動作するとのことですが、MT7921 の firmware は injection を 1 Mbps／6 Mbps の基本レートに固定しており、HT／VHT での injection はできません。AXM と AXML の 2 製品は、**stock kernel 6.17** では同様にこの問題に当たり、2026-11-18 時点ではパラメータ調整では解決できません。

したがって、deauth、WPA handshake の取得、injection を前提としたペネトレーションテストなど、injection が関わる機能は、AWUS036AXML では本プラットフォーム上で実行できません。このような用途には、実測で injection が利用可能だった型番を使用してください（下記の選定を参照）。

### その他の高度なモード一覧

| 高度な機能 | 状態 | 説明 |
|---|---|---|
| VIF（STA + AP の同時動作） | ✅ | 同じチャンネル ch36。iPhone 接続時の STA ping は 4.4 ms |
| WPA handshake 取得 | ❌ | injection の失敗 → deauth を送信できず、handshake は 0 |
| Active monitor | 🟡 | `set monitor active` は受理されるが、ACK は未検証 |
| Ad-hoc（IBSS） | N/A | `mt7921u` ドライバにこのモードはない |
| Mesh（802.11s） | N/A | `mt7921u` ドライバにこのモードはない |
| Wi-Fi Direct（P2P） | ⬜ | ドライバは対応を宣言しているが、2 台目のデバイスが必要なため見送り |

## 四、Bluetooth 複合に関する注意事項と、適した用途／適さない用途

### BT + WiFi 複合アダプターの実用上の副作用

AWUS036AXML には Bluetooth が内蔵されており、この検証セットでは 2 つある複合デバイスの 1 つです（もう 1 つは Realtek の EACS）。Bluetooth は本機で利用可能を実測済み（hci コントローラー UP、BLE とクラシック Bluetooth のデバイスをスキャン可能、Wi-Fi と共存。前述のとおり）です。ここでは複合デバイスの実用上の副作用を 1 つ補足します。再接続時にまれに WiFi probe で止まり、`wlx` インターフェースが生成されないことがあります。症状は、抜き差し後に `ls /sys/class/net` でアダプターがいつまでも現れないというものです。対処法は単純で、**別の USB ポート**に挿し直せば、通常は正常に列挙されます。

もう 1 つ覚えておきたい小さな操作があります。AP モードでスマートフォンから SSID が突然見えなくなった場合は、アダプターを**一度抜き差し**してリセットすれば解消します。設定を変更する必要はありません。（注意：前述の monitor で報告される 3 dBm は見かけの値で実際の電力ではなく、SSID が消える主因ではありません。）

### プラットフォームの安全上のルール

- `airmon-ng check kill` は絶対に実行しないでください。NetworkManager が停止し、GX10 全体がネットワークから切断されます。操作対象は外付けの `wlx*` インターフェースのみとし、内蔵の外部接続用メイン回線には触れないでください。
- `hcxdumptool 8.x` はこのマシンで（2.4 GHz の AWUS036EACS を除き）`failed to arm` になります（GX10 内蔵の 3 バンドアダプターとの列挙競合 + ドライバに active-monitor がないため）。これはプラットフォーム全体に共通する問題で、AXML とは無関係です。同様の機能が必要な場合は、`airodump-ng` とその他の aircrack-ng ツールを組み合わせて使用してください。
- ARM64 の補足：`aircrack-ng` はソースからのビルドが必要です。`wifite` は git 版を使うと、apt の依存関係の競合を回避できます。

### 適した用途 / 適さない用途の一覧

| 適した用途 | 適さない用途 |
|---|---|
| 純粋な AP / アクセスポイント（2.4G は HT を含む、5G は VHT80） | injection / deauth |
| WPA3-SAE アクセスポイント | WPA handshake の取得 |
| 一般的な managed 接続 | injection を前提としたペネトレーションテストの主力アダプター |
| 受動 monitor / 周波数スペクトルの棚卸し（単一チャンネルに固定） | mesh / IBSS の実験 |
| STA + AP の同時動作（VIF、ネットに接続しながら共有） | 強い受信が必要な長距離の記録 |

## 五、選定の目安（総合ページへ）

AWUS036AXML を 9 製品の全体像の中に置いてみると、位置づけは明確です。MediaTek らしく接続が安定し、コンパイル不要で、両バンドの AP で VHT80 まで設定できる、「純粋な接続 / 純粋な AP」用として十分に役立つアダプターです。injection が絡む用途は、このアダプターの出番ではありません。

| 用途 | おすすめ型番 |
|---|---|
| 純粋な AP / 一般接続（injection 不要） | **AWUS036AXML / AWUS036AXM**（本アダプターが該当） |
| injection + handshake（ペネトレーションテスト） | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS の実験 | AWUS036ACM / AWUS036ACHM |
| 最強の受信 / 長距離 monitor | AWUS036AXER / AWUS036ACH |

9 製品の中で取捨選択をしている場合は、Monitor / Injection / AP / WPA3 の完全なマトリクスと用途別の選定を総合ページでご確認ください。

- [2026 年最も詳細な実測：9 種類の ALFA ワイヤレスアダプターを ASUS GX10 で全マトリクス比較](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

ひとことで注意点をまとめると、**injection や handshake が必要なら、AWUS036AXML / AWUS036AXM は選ばないでください**。純粋な接続やアクセスポイントの構築であれば、とても使いやすいアダプターです。

## よくある質問（FAQ）

**Q1. AWUS036AXML でパケットインジェクション（packet injection）はできますか？**
当社のテストプラットフォーム（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）ではできません。`aireplay-ng --test` は `No Answer`、`Found 0 APs` と報告し、AP を指定して個別にテストしても `No such BSSID available` が返るだけでした。通常のスキャンではその AP が見えていても（約 -54 dBm）、インジェクションツールの状況ではその beacon を受信できないため、deauth も handshake の取得（0 件）も利用できません。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションであり、チップが本質的にインジェクション不能というわけではありません。AWUS036AXM も同じ結果です。インジェクションが必要な場合は AWUS036EACS、ACH、ACS をお選びください。

**Q2. AWUS036AXML の Bluetooth は Ubuntu で使えますか？**
本機での実測では Bluetooth は利用可能でした。`bluetoothctl`／`hciconfig` で hci コントローラーが UP であることを確認し、BLE とクラシック Bluetooth のデバイスをスキャンでき、Wi-Fi と Bluetooth を同時に使用できます（共存）。Wi-Fi＋Bluetooth の複合デバイスです。なお、再接続時にまれに WiFi probe で止まり、`wlx` インターフェースが生成されないことがありますが、別の USB ポートに挿し直せば回復します。

**Q3. AWUS036AXML は Ubuntu 24.04 で別途ドライバのインストールが必要ですか？**
不要です。mt7921u ドライバは kernel 6.17 に内蔵されており、挿した後の dmesg で mt7921u がインターフェース名を `wlx` に MAC を加えた名前へ変更するのが確認できます（USB ID `0e8d:7961`）。DKMS もコンパイルも不要です。ドライバは IBSS と mesh モードを提供しません。

**Q4. AWUS036AXML は AP を開けますか？WPA3 に対応していますか？**
開けます。これが最も安定した用途です。2.4 GHz（802.11n、MCS 10）と 5 GHz VHT80（VHT-NSS2）のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は `sae_pwe=0` で iPhone 15 Pro が接続でき（`MFP: yes`。2.4 GHz と 6 GHz で実測、5 GHz は未実測）、STA＋AP の同時動作時の STA 側 ping は約 4.4 ms でした。Wi-Fi 6 チップという位置づけですが、本機では 6 GHz band も利用可能であることを実測しました（6135 MHz の AP を自前で構築し、iPhone 15 Pro が 802.11ax で接続して IP を取得）。

**Q5. AWUS036AXML と AWUS036AXM の違いは何ですか？どちらを選ぶべきですか？**
本プラットフォームでは 2 製品の Wi-Fi の挙動は同じです。どちらも mt7921u を使用し、injection は同様に失敗し、monitor の受信も同様に弱く、AP、WPA3、VIF は同様に利用できます。違いは、AXML には Bluetooth があり（本機で利用可能を実測）、本機で 6 GHz band も利用可能を実測した点です。AXM の Bluetooth と 6 GHz は今回個別に実測していません。純粋な AP や一般的な接続ならどちらを選んでも構いません。injection や handshake が必要なら、どちらも選ばないでください。

## 関連記事

（リンクは順次公開予定です。準備中）

- 同じチップの Bluetooth なし版：[AWUS036AXM 単体実測](/ja/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- injection が利用可能な代替品：[AWUS036EACS 単体実測](/ja/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACH 単体実測](/ja/blog/awus036ach-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 単体実測](/ja/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- テーマ記事：[ドライバ不要：Ubuntu（ARM64）で Monitor と AP モードを有効にする](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- テーマ記事：[WPA3-SAE 接続と handshake の実務（自社環境で検証）](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 総合ハブ：[9 種類の ALFA アダプターを ASUS GX10 で全マトリクス比較](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*テスト実施：Yupitek（ALFA Network 台湾代理店）｜ テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ テストデバイス：Apple iPhone 7 Plus（WPA3 は iPhone 15 Pro でも測定）｜ テスト環境：自社オフィスの Wi-Fi（SSID YUPITEK）。本記事は製品の互換性と機能の検証であり、第三者のネットワークに対する操作の解説ではありません。*
