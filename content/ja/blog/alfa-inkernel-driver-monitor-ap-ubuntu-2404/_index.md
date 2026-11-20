---
title: "ドライバ不要：Ubuntu 24.04 + kernel 6.17 の in-kernel ドライバで ALFA アダプタの Monitor / AP モードを有効にする（rtw88 / rtw89 / mt76 実測）"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Ubuntu 24.04 / kernel 6.17 でのドライバ不要ガイド。in-kernel の rtw88 / rtw89 / mt76 ドライバで ALFA アダプタの Monitor と AP モードを有効にする手順に加え、WPA3 ホットスポットの互換性設定と Kali ツールチェーンの注意点を解説します。"
faq:
  - question: "Ubuntu 24.04 で ALFA アダプタを monitor mode にするには、どうすればよいですか？"
    answer: "kernel 6.17 以上であれば、インターフェースを NetworkManager の管理から外し、monitor のインターフェースモードに切り替えるだけで済みます。サードパーティ製ドライバのインストールは不要です。本記事でテストした rtw88 / rtw89 / mt76 の 3 つのドライバファミリーで手順は共通です。詳細なコマンドは、本文の各ステップをご覧ください。"
  - question: "Ubuntu では、なぜ ALFA アダプタに別途ドライバをインストールする必要がないのですか？"
    answer: "Realtek の rtw88／rtw89 と MediaTek の mt76 が、これらの USB チップを順次 mainline kernel の in-kernel サポートに加えたためです（最低 kernel は製品ごとに異なり 4.19〜6.17。Ubuntu 24.04 では AX、AXER に kernel 6.17 以上が必要で、例として 24.04.4 の HWE）。kernel 6.17（GX10 で実測）では全 9 製品が内蔵済みで、挿すだけで認識され、ビルドも DKMS も不要です。"
  - question: "ALFA アダプタで WPA3 ホットスポットを立てたところ、旧型の iPhone が接続できません。どうすればよいですか？"
    answer: "実測で、よくある原因が 2 つ見つかりました。1 つ目は、hostapd の sae_pwe を 2 ではなく 0 に設定しないと、旧型の iPhone と互換性がないことです。2 つ目は、802.11n の設定を残していると、旧型の端末が関連付けに失敗することがあることです。互換性を優先する場合は、802.11n を無効にすることを推奨します。"
  - question: "rtw88、rtw89、mt76 のうち、mesh や IBSS に対応しているのはどのドライバファミリーですか？"
    answer: "実測では、mt76 ファミリー（AWUS036ACM / ACHM など）が単体で mesh（802.11s）と IBSS を構築できました。Realtek rtw88 は IBSS の単体 join が可能（ACH の実測に基づく）ですが mesh には非対応で、rtw89 は IBSS の対応すら宣言していません。"
draft: false
---

> 本記事は標準的な Linux ネットワーク設定のガイドです。新しい kernel で**内蔵（in-kernel）ドライバ**を使い、ALFA 無線 LAN アダプタの Monitor（モニタリング）モードと AP（ホットスポット）モードを有効にする方法を示します。
> テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。掲載する数値はすべて、Yupitek が自社の機器と自社オフィスの Wi-Fi（SSID `YUPITEK`）で行った製品互換性の実測からの抜粋です。
> ⚠️ **適法な利用について**：Monitor モードは、自分が所有している、または許可を得たネットワークのモニタリングにのみ使用してください。AP モードは、各地域の電波法令を遵守してください。本記事は、第三者のネットワークに対する攻撃的な操作には一切触れません。

---

## 要点まとめ（TL;DR）

ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）上で Yupitek（ALFA Network 台湾代理店）が実測した ALFA の USB 無線 LAN アダプタ 9 製品はすべて in-kernel ドライバ（`rtw88` / `rtw89` / `mt76`）で動作し、ドライバのインストールなしに共通の手順で Monitor モードと AP モードを有効化でき、2.4G と 5G の AP で iPhone 7 Plus / 15 Pro が正常に接続しました。最低 kernel は製品ごとに 4.19〜6.17 です。

- **新しい kernel ならドライバ不要**：Realtek `rtw88` / `rtw89` と MediaTek `mt76` が、ALFA のこれらの USB チップを in-kernel でサポートしました。kernel 6.17（GX10 で実測）では 9 製品すべてが内蔵済みで（最低 kernel は製品ごとに異なります）、挿すだけで使え、ビルドも DKMS も不要です。
- **Monitor と AP の手順は 3 ファミリーで共通**：NetworkManager の管理から外し、`iw` で monitor に切り替えるか、`hostapd` で AP を起動します。
- **互換性の落とし穴が 2 つ**：AP を立てるときは 802.11n を無効にし（`ieee80211n=0`）、WPA3-SAE では `sae_pwe=0` を使うことを推奨します。そうしないと旧型の iPhone が接続できません。
- **高度なモードの対応状況**：mesh は `mt76` のみ。IBSS は単体で `mt76` と `rtw88`（ACH）が join 可能で、`rtw89` は未宣言です。
- **プラットフォームの鉄則**：`airmon-ng check kill` は絶対に実行せず（GX10 がネットワークから切断されます）、外付けの `wlx*` インターフェースだけを操作します。

## 1. なぜ「ドライバ不要」がこの世代の要点なのか

これまで Linux で ALFA のような USB 無線 LAN アダプタを使う際、最も多いハードルはドライバでした。RTL8812AU や MT7610U といったチップは、以前は mainline kernel に入っておらず、GitHub から out-of-tree プロジェクト（`morrownr/USB-WiFi`、`aircrack-ng/rtl8812au` など）を取得し、DKMS で現在の kernel バージョンに合わせてビルドする必要がありました。kernel を更新するたびに DKMS で再ビルドが必要になり、ビルドに失敗するとアダプタがそのまま認識されなくなります。安定運用が求められる代理店の検証環境や教育環境にとって、これは長年の悩みの種でした。

近年の mainline kernel で状況が変わりました。Realtek の `rtw88`、`rtw89`、MediaTek の `mt76` という 3 つのドライバファミリーが、これらの USB チップを順次 in-kernel の正式サポートに加えたのです。製品ごとに最低 kernel は異なりますが（下表「最低 kernel」列を参照）、kernel 6.17（GX10 で実測）では本記事でテストした 9 製品すべてが内蔵済みで、**挿すだけで認識され、ビルドも DKMS も不要**です。さらに重要なのは、これまで最も多く使われていた 2 つの out-of-tree プロジェクト（morrownr と aircrack-ng の rtl8812au）が、いずれもこの内蔵ドライバへの誘導に切り替わり、バグ報告の窓口も `lwfinger/rtw88` に一本化されたことです。つまり、新しい kernel ではドライバを手動でビルドする工程を省略できます。

`lwfinger/rtw88` コミュニティは今も活発にメンテナンスされており、修正をアップストリームへ送り続けています。そのため内蔵ドライバの安定性も kernel と一緒に更新され、ユーザーが各自でブランチを維持する必要はなく、アップグレードのたびに DKMS のビルド失敗で止まることもありません。代理店の検証環境や教育環境では、同じ手順を複数のアダプタ、複数回の kernel 更新にわたって繰り返し使えるため、保守コストが明らかに下がります。本記事が「ドライバ不要」に焦点を当てる理由もここにあります。

本記事のテストでカバーしたチップと、対応する内蔵ドライバモジュールは次のとおりです。

| チップファミリー | チップ型番 | 内蔵ドライバモジュール | 最低 kernel | 世代 / ストリーム | 代表アダプタ |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1（+BT） | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> お使いのシステムの kernel が製品ごとの最低バージョン（上表）未満の場合にのみ、従来の方法が必要になります。DKMS で out-of-tree ドライバ（rtw88 系は `lwfinger/rtw88`）をインストールしてください。Ubuntu 24.04 の場合、GA kernel 6.8 には ACM、ACHM、AXM、AXML、EACS のドライバが内蔵済みで、HWE 6.14 で ACH、ACS が加わります。AX、AXER には kernel 6.17 以上（例：24.04.4 の HWE）が必要です。本記事は GX10 の kernel 6.17 を前提としています。

---

## 2. ドライバのロードとバインドを確認する

モードを切り替える前に、アダプタが正しく認識され、ドライバがバインドされ、インターフェース名が生成されていることを確認します。Realtek の AWUS036ACH（`rtw88_8812au`）を例に、4 つの確認ステップを示します。

**ステップ 1：USB デバイスが列挙されていることを確認します。** `lsusb` で USB ID を探します（Realtek は多くが `0bda:xxxx`、MediaTek は多くが `0e8d:xxxx`）。

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**ステップ 2：ドライバのバインドと USB 速度を確認します。** `lsusb -t` では、バインドされた driver と接続速度を同時に確認できます（`5000M` は USB 3.0 で動作していることを示します）。

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

MediaTek のアダプタでは、`dmesg` でドライバの初期化メッセージを確認し、同時にインターフェース名が変更されたことも確認できます。

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**ステップ 3：インターフェース名を取得します。** Ubuntu は予測可能な命名（predictable naming）を採用しており、ALFA の外付けアダプタは必ず `wlx` に MAC アドレスを付けた名前になります。この名前は MAC で決まるため、**抜き挿ししても変わらず**、スクリプト化に便利です。内蔵の外部接続用アダプタは別の名前（GX10 では `wlP9s9`）なので、必ず区別してください。

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**ステップ 4：チップが宣言しているインターフェースモードを確認します。** このステップで、以降どのモードが使えるかが決まります。

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88（ACH）では `IBSS / managed / AP / AP/VLAN / monitor` が列挙され、mesh と P2P は**ありません**。MediaTek mt76（ACHM）では、さらに `mesh point / P2P-client / P2P-GO` が列挙されます。このリストが、ファミリーごとの能力差を示す一次情報です。詳細は第 5 節をご覧ください。

---

## 3. Monitor モードを有効にする（2.4 GHz / 5 GHz）

Monitor（モニタリング）モードでは、アダプタはどの AP にも関連付けずに、空中の 802.11 フレームを直接受信します。自社ネットワークのパケット診断、周波数帯の点検、電波カバレッジの評価によく使われます。有効化の手順は 3 つのファミリーで共通で、違いは各ファミリーの安定性に関する注意点だけです（第 5、6 節を参照）。

**共通の有効化手順：**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # 自分で管理するため, NetworkManager の介入を避ける
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

`type monitor` と表示されれば、切り替えは成功です。続いて、モニタリングするチャンネルを指定します。**2.4 GHz** では `set channel` を使います。

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

**5 GHz** では、周波数で指定するほうが間違いにくくなります（ch36 = 5180 MHz）。

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**期待される結果（実測の抜粋）：** AWUS036ACH では、ch1 / ch6 / ch11 でそれぞれ 92 / 214 / 71 フレームを取得しました。5 GHz の ch36 / ch149 / ch157 ではそれぞれ 260 / 137 / 127 フレームを取得しており、2.4G と 5G のどちらのモニタリングも正常です。MediaTek の ACHM では、`airodump-ng --band abg` で 120 秒間ホッピングスキャンを行い、ch1/5/6/36/149/157 付近で 19 台の基地局と 14 台のクライアントを検出しました。あるチャンネルで 0 パケットだった場合、たいていはそのチャンネルに AP がないだけで、アダプタの故障ではありません。

monitor モードに切り替えた後は、一般的な標準診断ツールを `wlx*` インターフェース上でそのまま動かせます。`airmon-ng` はアダプタとドライバの状態の一覧表示に、`kismet` はデータソースとしてのリアルタイムキャプチャと `.kismet` ログの生成に、`Wireshark` と `tshark` はキャプチャしたパケットの解析に、`bettercap` はチャンネルの巡回確認に使えます。これらのツールは 3 つのファミリーすべてで動作を確認しており、自社の無線環境におけるチャンネル使用状況や電波カバレッジの棚卸しに適しています。注意点は 1 つだけです。`hcxdumptool` 8.x は本プラットフォームでは 3 つのファミリーすべてで（2.4 GHz の EACS を除き）`failed to arm` となります（内蔵ドライバが active-monitor を提供しないため）。同様の機能が必要な場合は、`airodump-ng` と aircrack-ng スイートを組み合わせて使ってください。

> **5 GHz の注意：** デフォルトの regdomain（`country 00`）では、多くの 5 GHz チャンネルが passive/no-IR となり、モニタリングはできても能動的な送信は制限されます。その後、許可された範囲で 5 GHz のテストを行う場合は、先に `sudo iw reg set US` で制限を解除し、テスト後に `sudo iw reg set TW` で元に戻してください。Realtek の `rtw88_8812au` には、既知の 5G RX-stuck 現象（モードの切り替えを繰り返した後に 5G でパケットを受信できなくなる）もあります。発生した場合は、アダプタを物理的に一度抜き挿しし、5G のテストを優先して行ってください。

---

## 4. AP / ホットスポットモードを有効にする（2.4 GHz / 5 GHz）

AP（ホットスポット）モードでは、`hostapd` を使ってアダプタを Wi-Fi の基地局にします。手順は 3 つのファミリーで同じです。まずインターフェースを NetworkManager の管理から外し、次に `hostapd` の設定ファイルで起動します。以下は共通の最小構成です。

**4-1. 2.4 GHz（純粋な 802.11g）**

設定ファイル `/tmp/ap24.conf` を作成します。

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<8 文字以上のパスワード>
```

起動します。

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

クライアントが接続すると、`hostapd` は `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED` の順に出力します。最後の行が表示されれば、4-way handshake が完了し、接続に成功したことを意味します。

**4-2. 5 GHz（純粋な 802.11a、ch36）**

上記の設定を 5 GHz に変更します。

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2 のアダプタ（rtw89 の AX/AXER、mt76 の ACM/AXM など）では、VHT80 の設定を追加して 80 MHz 帯域幅に広げることもできます。単一アンテナの場合や互換性を優先する場合は、20 MHz の純粋な a のままにしてください。

**4-3. 重要な互換性設定 2 点**

1. **AP を立てるときは 802.11n を無効にすることを推奨します**（`ieee80211n=0`、純粋な g / 純粋な a で動作）。実測では、旧型のクライアント（iPhone 7 Plus）は `ieee80211n=1` のままだと関連付けに失敗し、画面には「パスワードが違います」と誤って表示されました。実際には `handle_assoc_cb: STA not found` です。802.11n を外したところ、1 回目から接続できました。
2. **WPA3-SAE では `sae_pwe=0` を使用してください**（hunting-and-pecking）。`sae_pwe=2`（H2E を強制）にすると、旧型の端末では鍵交換に失敗します。WPA3 セクションの例は次のとおりです。

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

この 2 つの落とし穴は Realtek と MediaTek のアダプタで同じように発生するため、ドライバの違いではなく、クライアント側の互換性の問題です。本記事でテストした 9 製品は、2.4G と 5G のどちらの AP でも、iPhone 7 Plus / 15 Pro が正常に接続できました。

**4-4. インターネット接続とホットスポットの併用（STA + AP）**

mt76 ファミリーは、1 枚のアダプタで既存の Wi-Fi に接続しながら、別に AP VIF を作って中継ホットスポットにすることに対応しています。実測では、ACHM がメインインターフェースで YUPITEK に接続したまま 5 GHz のホットスポットを立て、iPhone を接続させた状態で、ダウンロード 198 Mbit/s、ping 平均 3.2 ms を維持しました。この構成には 3 つの条件があります。AP VIF には別の MAC を使うこと、インターフェース名を `wlx` 形式のままにすること、すべての VIF が同じチャンネルにあることです。Realtek のアダプタでは、この組み合わせは phy によって保証されていません（rtw88 の managed + monitor は使えますが、STA + AP は安定しません）。中継ホットスポットを作るなら、mt76 ファミリーを優先して選ぶことを推奨します。

---

## 5. 3 つのチップファミリーの違いと制限

基本となる managed / monitor / AP の 3 モードは、3 つのファミリーすべてが対応しており、挙動も一致しています。違いは**高度なインターフェースモード**（mesh、IBSS、active monitor、P2P）にあります。これは完全にドライバの宣言で決まり、アダプタのアンテナ数とは無関係です。以下は実測の集計です。

| 高度なモード | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor（2.4G/5G） | ✅ | ✅ | ✅ |
| AP（hostapd） | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS（単体） | 🟡 単体で構築可能 | 🟡 単体で構築可能 | ❌ ドライバが未宣言 |
| Mesh（802.11s、単体） | 🟡 単体で構築可能 | ❌ `-95` 非対応 | ❌ ドライバが未宣言 |
| Active monitor | 🟡 設定可能 | ❌ `-95` 非対応 | N/A |
| Wi-Fi Direct（P2P） | 2 台目の機器が必要 | ❌ `-95` 非対応 | N/A |

**MediaTek mt76（ACM / ACHM / AXM / AXML）** は、高度なモードが最も充実したファミリーです。`iw phy info` が `mesh point`、`IBSS`、`P2P-client/GO` を宣言しています。実測では、単体で `Joined IBSS`、`type mesh point` となり、対応する beacon も送出されました（2 台目の機器がないため、2 台目との peer link は未検証です）。mesh や IBSS の単体実験が目的なら、mt76 ファミリーが第一候補です。特に注意が必要なのは、Wi-Fi 6 の MT7921（AXM/AXML）です。モードは一通り揃っていて AP も安定していますが、本プラットフォームでは frame injection ができません（主因は stock kernel 6.16+ の mac80211 chanctx のリグレッションで、チップ固有の問題ではありません。コミュニティでは同型番に git／パッチ適用済みドライバを使うと動作するもののファームウェアがレートをロックします。morrownr/USB-WiFi #387、morrownr/mt76 #18 に対応）。そのため、injection が必要な高度なテストには向きません。

**Realtek rtw88（ACH / ACS / EACS）** は `IBSS / managed / AP / AP/VLAN / monitor` に対応します。IBSS は単体で構築できます（`Joined IBSS`。ACH の実測に基づく。EACS は iftype が列挙されるものの、実測では join が機能しませんでした）。しかし、**mesh（802.11s）、active monitor、Wi-Fi Direct の 3 つは、実測ですべて `Operation not supported (-95)` を返しました**。rtw88 に固有のもう 1 つの特性が VIF です。`iw phy` のフラグには「interface combinations are not supported」とありますが、ACH の実測では managed + monitor の 2 つのインターフェースを同時に up にでき、monitor VIF で 100 フレームを取得できたため、「ネット接続しながらキャプチャ」は可能です。ただし phy がこの組み合わせを保証しているわけではないため、高負荷での長時間運用には、引き続き mt76 ファミリーを推奨します。

**Realtek rtw89（AX / AXER）** は、本記事で最も新しい Wi-Fi 6 ファミリーで、monitor と AP（VHT80 を含む）はいずれも良好で、受信感度も強力です。ただし、高度なモードについては、active monitor / mesh / IBSS / P2P がドライバレベルで未宣言（N/A）です。これらの単体実験には、mt76 のアダプタを使ってください。rtw89 の位置づけは、安定した Wi-Fi 6 のモニタリングとホットスポットであり、高度なインターフェースモードの実験プラットフォームではありません。

> ひとことでまとめた選定：**mesh / IBSS を単体で → mt76（ACM / ACHM）、Wi-Fi 6 ホットスポットと強力な受信 → rtw89（AX / AXER）、デュアルバンドの汎用用途と VIF → rtw88（ACH）。**

---

## 6. プラットフォームの安全上の注意（GX10 + Ubuntu ARM64）

GX10 のように「内蔵アダプタで外部に接続し、外付けの ALFA アダプタでテストする」マシンでは、以下の点が運用の鉄則です。守らないと、自分でネットワークを切断してしまいます。

1. **`airmon-ng check kill` は絶対に実行しないでください。** このコマンドは NetworkManager を停止させ、GX10 の外部接続も切断します。本記事では一貫して `iw` と `nmcli dev set <インターフェース> managed no` だけを使い、`check kill` には触れません。
2. **操作は `wlx*` だけにし、内蔵の `wlP9s9` には絶対に触れないでください。** `wlP9s9` は GX10 が外部に接続するための主回線です。down やモード変更などの操作は、ALFA の `wlx*` インターフェースにだけ行い、コマンドを打つ前に必ず `echo $IF` で対象を確認してください。
3. **RX stall は抜き挿しで復旧します。** monitor / AP の切り替えを繰り返した後に何もスキャンできなくなった場合は、多くがドライバの受信ハングです（Realtek の 5G で特に多い）。ソフトウェアでは復旧できないことが多いため、**物理的にアダプタを一度抜き挿し**してください。USB が再列挙され、インターフェース名は MAC が変わらないため同じままです。
4. **BT+WiFi コンボアダプタは USB ポートを変えます。** EACS や AXML のような Bluetooth + Wi-Fi のコンボデバイスは、抜き挿しの際に Wi-Fi の probe が止まって `wlx` インターフェースが生成されないことが時々あります。USB ポートを変えれば、たいてい正常になります。
5. **5 GHz で送信する前に regdomain を設定してください。** デフォルトの `country 00` では、5 GHz の多くが no-IR となり、能動的な送信が禁止されます。許可された範囲でテストする前に `sudo iw reg set US` で制限を解除し、テスト後に `sudo iw reg set TW` で元に戻してください。
6. **ARM64 でのパッケージの注意。** GX10 は aarch64 のため、`aircrack-ng` はビルド済みの wheel/package がないことが多く、ソースからのビルドが必要です。`wifite` は apt の依存関係の競合を避けるため、GitHub 版を推奨します。また、`hcxdumptool` 8.x は本プラットフォームでは 3 つのファミリーすべてで（2.4 GHz の EACS を除き）`failed to arm` となります（内蔵ドライバが active-monitor に対応していないため）。モニタリングのキャプチャには、`airodump-ng` と aircrack-ng スイートを組み合わせて使ってください。

**テスト終了後に通常モードへ戻す：**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # 期待値 type managed
```

---

## よくある質問（FAQ）

**Q：Ubuntu 24.04 で ALFA アダプタを monitor mode にするには、どうすればよいですか？**
A：kernel 6.17 以上であれば、インターフェースを NetworkManager の管理から外し、monitor のインターフェースモードに切り替えるだけで済みます。サードパーティ製ドライバのインストールは不要です。本記事でテストした rtw88 / rtw89 / mt76 の 3 つのドライバファミリーで手順は共通です。詳細なコマンドは、本文の各ステップをご覧ください。

**Q：Ubuntu では、なぜ ALFA アダプタに別途ドライバをインストールする必要がないのですか？**
A：Realtek の `rtw88`／`rtw89` と MediaTek の `mt76` が、これらの USB チップを順次 mainline kernel の in-kernel サポートに加えたためです（最低 kernel は製品ごとに異なり 4.19〜6.17。Ubuntu 24.04 では AX、AXER に kernel 6.17 以上が必要で、例として 24.04.4 の HWE）。kernel 6.17（GX10 で実測）では全 9 製品が内蔵済みで、挿すだけで認識され、ビルドも DKMS も不要です。

**Q：ALFA アダプタで WPA3 ホットスポットを立てたところ、旧型の iPhone が接続できません。どうすればよいですか？**
A：実測で、よくある原因が 2 つ見つかりました。1 つ目は、hostapd の `sae_pwe` を 2 ではなく 0 に設定しないと、旧型の iPhone と互換性がないことです。2 つ目は、802.11n の設定を残していると、旧型の端末が関連付けに失敗することがあることです。互換性を優先する場合は、802.11n を無効にすることを推奨します。

**Q：`rtw88`、`rtw89`、`mt76` のうち、mesh や IBSS に対応しているのはどのドライバファミリーですか？**
A：実測では、`mt76` ファミリー（AWUS036ACM / ACHM など）が単体で mesh（802.11s）と IBSS を構築できました。Realtek `rtw88` は IBSS の単体 join が可能（ACH の実測に基づく）ですが mesh には非対応で、`rtw89` は IBSS の対応すら宣言していません。

## 7. 関連記事

- 9 枚の ALFA アダプタの能力比較と選定の総評 → [ALFA 無線 LAN アダプタ総評ハブ（総括表）](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Realtek rtw88 の代表アダプタのステップガイド → [AWUS036ACH 単体実測](/ja/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- MediaTek mt76 の代表アダプタのステップガイド → [AWUS036ACHM 単体実測](/ja/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*テスト実施：Yupitek（ALFA Network 台湾代理店）— https://www.yupitek.com ｜ テスト環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ テスト端末：Apple iPhone 7 Plus（WPA3 は iPhone 15 Pro でも別途テスト）*
