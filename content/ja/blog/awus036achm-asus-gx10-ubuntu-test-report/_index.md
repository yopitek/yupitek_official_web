---
title: "AWUS036ACHM 個別実機検証：MediaTek MT7610U シングルアンテナ AC600 を ASUS GX10（ARM64 / Ubuntu 24.04）で使う場合の Monitor・Injection・AP・WPA3 対応状況"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM（MT7610U）は Ubuntu 24.04 でドライバのインストール不要。デュアルバンドのモニターモードが利用でき、2.4G のパケットインジェクションは 96–100%。AP を開くには 802.11n を無効にする必要があり、WPA3 は sae_pwe=0 に設定しないと古い iPhone が接続できません。"
faq:
  - question: "AWUS036ACHM は Ubuntu 24.04 でドライバのインストールが必要ですか？"
    answer: "不要です。MT7610U は kernel 組み込みの mt76x0u ドライバが処理するため、Ubuntu 24.04（kernel 6.17）では挿すだけで認識され、DKMS も追加ファームウェアも要りません。lsusb で USB ID 0e8d:7610 を確認できます。"
  - question: "AWUS036ACHM は monitor mode に入れますか？AP はいくつ見つかりますか？"
    answer: "入れます。2.4GHz・5GHz のどちらでも monitor mode に入れます。airodump-ng でホッピングしながら全バンドを 120 秒スキャンしたところ、実測で 19 台の AP と 14 台のクライアントを検出し、分布は ch1、2、5、6、36、149、157 でした。"
  - question: "AWUS036ACHM のパケットインジェクション成功率はどのくらいですか？5GHz でも使えますか？"
    answer: "2.4GHz のチャンネル 6 では、AP ごとのインジェクション応答率が 96–100% でした（aireplay-ng --test、4 台の AP を検出）。5GHz（ch36、ch149）ではブロードキャストのインジェクションが動作することしか確認できず、AP ごとのテストは Found 0 APs と報告されました。今回はパーセンテージを取得できておらず、原因は調査中です。"
  - question: "AWUS036ACHM で AP を開くと iPhone に「ネットワークに接続できません」や「パスワードが違います」と表示される場合は？"
    answer: "まず 802.11n を無効にしてください。hostapd の設定ファイルに ieee80211n=1 と ht_capab を入れず、2.4GHz は純粋な hw_mode=g、5GHz は純粋な hw_mode=a（20 MHz）を使います。そうしないと hostapd に handle_assoc_cb: STA not found が繰り返し出力され、画面上はパスワード間違いのように見えますが、実際は 802.11n のアソシエーション失敗です。"
  - question: "AWUS036ACHM の WPA3-SAE で、古い iPhone が接続できないのはなぜですか？"
    answer: "多くの場合は hostapd の sae_pwe 設定が原因です。実測では sae_pwe=0 のとき iPhone 7 Plus も iPhone 15 Pro も接続できました。sae_pwe=2 のときは、iPhone 7 Plus はアソシエーションには成功するものの 4-way ハンドシェイクに失敗して切断され、パスワード間違いのように見えます。ieee80211w=2 と組み合わせ、設定変更後は iPhone でいったんそのネットワークを削除してから再接続してください。"
draft: false
---

> 検証担当：Yopitek（ALFA Network 台湾代理店）｜検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`|テスト機器：自社の iPhone 7 Plus（WPA3 のみ iPhone 15 Pro でも測定）|テスト対象：自社オフィスの Wi-Fi（SSID `YUPITEK`、2.4G ch5 / 5G ch36、157）。
>
> 本記事は、代理店による製品の互換性と機能の限界についてのハードウェア検証です。Monitor / Injection / AP / WPA3 のテストはすべて、Yopitek が所有する機材と自社オフィスの Wi-Fi 上で、自社のテスト用スマートフォンに対して実施した正当な機能検証であり、第三者のネットワークは対象とせず、攻撃手順も提供しません。本文中の injection は probe request を送って機能を自己テストしただけで、攻撃用パケットは送信していません。

## 要点まとめ（TL;DR）

ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）での実測では、AWUS036ACHM は両バンドで monitor モードが使え、2.4G のパケットインジェクションは 96–100%（5G はブロードキャストインジェクションのみ確認）、AP ホットスポットも両バンドで構築できます（802.11n の無効化が必要）。

- Ubuntu 24.04 ではドライバのインストール不要：MT7610U は kernel 6.17 組み込みの mt76x0u が処理し、挿すだけで認識されます。DKMS も追加ファームウェアも不要です。
- デュアルバンドのモニターモード（monitor mode）が利用可能。2.4G のパケットインジェクションは 96–100%。
- 5GHz ではブロードキャストのインジェクションしか確認できておらず、AP ごとの応答率は今回取得できていません（原因は調査中）。
- AP を開くには 802.11n を無効にする必要があります。WPA3 は `sae_pwe=0` に設定しないと、古い iPhone が接続できません。
- シングルアンテナの 1T1R（AC600）で、スループットと位置づけは 2T2R の ACM / ACH とは別クラスです。

## 1. このカードとこのプラットフォーム

AWUS036ACHM は ALFA のシングルアンテナ AC600 カードで、チップは MediaTek MT7610U、Linux 組み込みドライバ `mt76x0u` に対応します。AWUS036ACM（MT7612U、2T2R）のシングルストリーム版の姉妹機種で、スペック上は 1T1R（AC600）と空間ストリームが 1 本少ない代わりに、より小型で、コミュニティで定評のある長距離受信を備えています。morrownr/USB-WiFi コミュニティは、これを Kali 推奨リストおよび「The Short List」に入れており、VIF、Active monitor、WPA3 はいずれも Yes、Very Long range、シングルストリーム、in-kernel と注記しています。

これを ASUS GX10（NVIDIA GB10、128GB UMA、ARM64）に挿し、Ubuntu 24.04 LTS、kernel 6.17 上で Monitor、Injection、AP、WPA3-SAE を項目ごとに測定しました。先に結論を述べると、このカードは本プラットフォームで使え、2.4GHz の機能もかなり揃っています。ただし、知っておくべき互換性の落とし穴が 2 つあります。AP を開くには 802.11n を無効にする必要があること、WPA3 は `sae_pwe=0` にする必要があることです。また、5GHz の AP ごとの injection は今回ブロードキャストまでしか確認できていません。次の表が全体の概要です。

| 機能項目 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（モニタリング） | ✅ | ✅ |
| Injection（インジェクション） | ✅ 96–100% | ⚠️ ブロードキャストのみ動作、AP ごとの応答率は未取得 |
| AP ホットスポット | ✅（純粋な 802.11g が必要） | ✅（純粋な 802.11a、20 MHz が必要） |
| WPA3-SAE | ✅（`sae_pwe=0` が必要） | 未実測 |

> 凡例：✅ 実測で合格 ｜ 🟡 部分的、または単機でのみ成立 ｜ ⚠️ 制限あり ｜ ❌ 非対応または失敗。

## 2. ハードウェアとドライバ（インストール不要）

ACHM を GX10 に挿すと、kernel 6.17 組み込みの `mt76x0u` が直接認識し、DKMS も追加ファームウェアも不要で、GitHub から out-of-tree ドライバをビルドする必要もありません。カードを確認する 3 つのコマンドは次のとおりです。

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

インターフェース名は MAC に基づく名前（`wlx<MAC>`）で、カードを挿し直しても変わらないため、スクリプトを書くときはそのままバインドできます。`iw phy info` が対応を宣言しているインターフェースモードには `managed`、`AP`、`monitor`、`mesh point`、`IBSS`、`P2P-client`、`P2P-GO` が含まれ、本記事でテストするすべてのシナリオをカバーしています。

プラットフォーム共通の安全上の注意 2 点は、ACHM でも同様に適用されます。1 つ目は、`airmon-ng check kill` を絶対に実行しないこと。NetworkManager が停止し、GX10 が外部ネットワークから切断されます。2 つ目は、操作するのは `wlx*` インターフェースのみとし、内蔵の `wlP9s9`（GX10 の外部接続の主回線）には触れないこと。monitor／AP に入る場合は、必ず `iw` と `nmcli dev set $IF managed no` を組み合わせ、システムのメインのネットワークカードには手を付けません。

## 3. 実測した機能：Monitor / Injection / AP / WPA3

### 3-1. Monitor（2.4 + 5 GHz）✅

両バンドとも、モニタリングは正常でした。2.4GHz のチャンネル 6 では、8 秒でキャプチャ上限の 300 パケットに達しました。5GHz は周波数ごとのアクティビティによって異なり、ch36（5180）は 8 秒で 300 に達し、5745 は 254、5785 は 54 でした（あるチャンネルでパケットが少ないのは、通常そのチャンネルに当時アクティブな AP がないことを意味し、ネットワークカードの問題ではありません）。

ホッピングによる全バンドスキャンは、シングルアンテナカードの受信性能が最もよく表れます。

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

実測で 120 秒間に 19 台の基地局と 14 台のクライアントを検出し、分布は ch1/2/5/6/36/149/157 でした。シングルストリームの AC600 カードとして、この検出範囲は安定したモニタリングソースとして十分であり、コミュニティによる「Very Long range」という評価とも一致します。

### 3-2. Injection（2.4 + 5 GHz）

ここは ACHM で 2 つのバンドの差が最もはっきり出る部分であり、機種選定の際に特に注意すべき項目です。

2.4GHz のチャンネル 6 で `aireplay-ng --test` による機能の自己テストを行ったところ、結果は良好でした。

```text
Injection is working!
Found 4 APs
30/30: 100%
```

4 台の基地局の応答率は 96–100% で、インジェクション機能は完全に動作しています。

しかし 5GHz に切り替えると（ch36 と ch149 の両方を試しました）状況が変わります。

```text
Injection is working!
Found 0 APs
```

つまり、5GHz のブロードキャストインジェクションは動作しています（ドライバが `Injection is working!` と報告）が、`aireplay-ng --test` による AP ごとの応答率は、2 つの 5G チャンネルのどちらでも `Found 0 APs` であり、今回はパーセンテージを取得できていません。これは ACHM というシングルアンテナカードを本プラットフォームで測定した際の実測上の現象で、原因は今後調査します。測定できていない数字を補って書くことはしません。正直に言えば、安定した 5GHz の AP ごとのインジェクションが必要な用途では、ACHM は今回 2.4GHz でしか完全なインジェクション成功率を確認できていません。

### 3-3. AP ホットスポット（2.4 + 5 GHz）✅ — ただし 802.11n の無効化が必須

ACHM の 1 つ目の互換性の落とし穴はここです。AP を開くとき、hostapd の設定ファイルに `ieee80211n=1` と `ht_capab` を入れないでください。2.4GHz は純粋な `hw_mode=g`、5GHz は純粋な `hw_mode=a`（20 MHz）にします。動作する最小限の 2.4GHz 設定は次のようになります。

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 純粋な 802.11g. ieee80211n=1 や ht_capab は追加しない
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=ご自身のパスワード (8 文字以上) に変更してください
```

実測では iPhone 7 Plus が両バンドで接続できました。2.4GHz では `AP-STA-CONNECTED` に続いて `EAPOL-4WAY-HS-COMPLETED` が確認でき、5GHz（ch36、20 MHz）では -71 dBm、rx 54 Mbit、`authorized: yes` を計測しました。

逆に、設定ファイルに `ieee80211n=1` を残したままだと、hostapd は `handle_assoc_cb: STA not found` を繰り返し出力し、iPhone の画面には「ネットワークに接続できません」や「パスワードが違います」と表示されますが、実際には 802.11n のアソシエーション失敗であり、パスワードの問題ではありません。802.11n を外せば解決します。ACHM はシングルアンテナカードのため、5GHz の AP は今回 20 MHz とし、VHT80 は試していません。

### 3-4. WPA3-SAE ✅ — ただし `sae_pwe=0` が必須（最も踏みやすい互換性の落とし穴）

ACHM の 2 つ目、そして単独で取り上げる価値のある互換性の落とし穴です。WPA3-SAE の hostapd では、`sae_pwe` でパスワード要素（password element）の導出方法を制御します。`0` は従来の Hunting-and-Pecking のみ、`1` は Hash-to-Element（H2E）のみ、`2` は両者の併用（Hunting-and-Pecking と H2E の両方に対応）です。この違いが、古い iPhone が接続できるかどうかを直接左右します。

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 では PMF が必須
ieee80211w=2
# 重要: iPhone 7 Plus のような古い端末との互換性のため
sae_pwe=0
sae_password=ご自身のパスワードに変更してください
```

実測での比較は次のとおりです。

- `sae_pwe=0`：iPhone 15 Pro と iPhone 7 Plus の**どちらも接続できました**（`authorized: yes`、`MFP: yes`）。
- `sae_pwe=2`：iPhone 7 Plus は**アソシエーションには成功するものの 4-way 鍵交換に失敗して切断され**、表面的にはやはり「パスワード間違い」のように見えます。iPhone 15 Pro は接続できます。

結論は明快です。古い iPhone（iPhone 7 Plus のような 2016 年の機種を含む）との互換性が必要なら、hostapd には必ず `sae_pwe=0` を設定してください。設定変更後は、iPhone でいったん「このネットワーク設定を削除」してから再接続し、残ったアソシエーション状態による見かけ上の失敗を避けてください。この点は、9 機種の総括表でも ACHM の WPA3 欄に「✅*」と星印を付けて特記しています。

## 4. 発展的な機能と制限

まず表で、今回の ACHM の検証範囲と状態の全体をまとめ、そのあと要点ごとに掘り下げます。

| 機能 | 状態 | 今回の実測の要点 |
|---|---|---|
| Monitor（2.4 + 5 GHz） | ✅ | ホッピング 120 秒で 19 AP + 14 client を検出 |
| Injection 2.4 GHz | ✅ | 応答率 96–100% |
| Injection 5 GHz | ⚠️ | ブロードキャストは動作、AP ごとの応答率は未取得 |
| AP（2.4 + 5 GHz） | ✅ | iPhone が両バンドで接続、802.11n の無効化が必要 |
| WPA3-SAE | ✅* | 2.4 GHz で実測（5 GHz は未実測）。新旧どちらの iPhone も接続、`sae_pwe=0` が必要 |
| VIF（STA+AP、AP+monitor） | ✅ | 接続しながらホットスポットとして動作、ダウンロード 198 Mbit/s |
| WPA handshake キャプチャ | ✅ エンドツーエンド（.22000、5 GHz ch36） | 自社の iPhone に deauth、完全な 4-way M1–M4 をキャプチャし、hashcat `.22000` に変換 |
| Active monitor | 🟡 | モニタリングの設定は可能、ACK は未検証 |
| Ad-hoc（IBSS） | 🟡 | 単機で構築可能、2 台目との相互接続は未実施 |
| Mesh（802.11s） | 🟡 | 単機で参加可能、peer link は未確立 |
| Wi-Fi Direct（P2P） | ⬜ | 2 台目の機器が必要なため省略 |

> ✅* ＝ WPA3-SAE は利用可能だが `sae_pwe=0` が必要。詳しくは第 3-4 節を参照。

**VIF（仮想インターフェース、同一チャンネル、最大 2 インターフェース）。** ACHM は 1 枚のカードから複数のインターフェースを切り出して同時に動作させられます。前提は、各 VIF が異なる MAC を使うこと、AP の VIF を NetworkManager の管理下に置かないこと、すべての VIF が同一チャンネルであることで、ACHM ではさらに AP の 802.11n 無効化が必要です。2 種類の組み合わせを実測しました。

- **STA + AP（インターネットに接続しながらホットスポットとしても動作）**：iPhone 7 Plus が AP に接続している間（-66 dBm、authorized）、メインのインターフェースは YUPITEK に接続され、ping は 30/30、avg 3.2 ms、ダウンロードは 198 Mbit/s でした。
- **AP + Monitor**：AP を開いたままモニタリングし、8 秒で 300 フレームをキャプチャしました。そのうち 46 個は自社 AP の beacon でした。

**handshake キャプチャ。** ACHM は 5GHz（ch36）でエンドツーエンドの流れを完了しました。自社の iPhone に deauth を送り、完全な 4-way（M1–M4）をキャプチャして hashcat `.22000` に変換しています。エンドツーエンドを完了した 9 枚中 7 枚（ACM、ACHM、ACH、ACS、EACS、AX、AXER）のうちの 1 枚です。なお 5GHz の AP ごとのインジェクション応答率（`aireplay-ng --test`）は引き続き取得できていません。

**mesh / IBSS（単機で構築可能）。** これは mt76 ファミリーが Realtek の rtw88/rtw89 と異なる点です。IBSS（Ad-hoc）は約 9 秒で `Joined IBSS` となり、beacon を送出できました。Mesh（802.11s）は `type mesh point` に入り、mesh beacon を送出できました。どちらも今回は単機での成立にとどまり、2 台目との相互接続は行っていません（2 台目の機器がなく省略）。そのため 🟡 と表記しています。Realtek の rtw88/rtw89 カード（AWUS036ACH など）は、本プラットフォームで単機の IBSS は構築できますが、802.11s mesh には対応していません。したがって 802.11s mesh の実験をするなら、ACM と ACHM の 2 枚の mt76 カードは数少ない選択肢になります。

**Active monitor 🟡。** 設定でき、モニタリングも正常ですが、ACK 応答の動作は 2 台目の機器がないと検証できず、今回は未検証です。

**Kali ツール（プラットフォームレベルで、他のカードと共通）。** `airmon-ng`、`kismet`、`bettercap`、`wifite`（git 版）、Wireshark/tshark は、いずれも ACHM をソースとして利用できます。`hcxdumptool` だけは、本プラットフォームで `failed to arm interface` となります（2.4 GHz の AWUS036EACS を除く。内蔵ドライバが active-monitor に対応していないため）。キャプチャには `airodump-ng` と aircrack-ng パッケージを組み合わせて使ってください。ARM64 ではさらに、`aircrack-ng` は prebuilt パッケージがないことが多くソースからのコンパイルが必要になる点、`wifite` は apt の依存関係の衝突を避けるため GitHub 版の利用を推奨する点にご注意ください。

## 5. 適した利用シーンと機種選定（Hub への導線）

ACHM を 9 機種の選定の文脈に戻すと、その位置づけは明確です。

**向いている用途**

- **mesh（802.11s）実験**：mt76 ドライバは単機で 802.11s mesh（および IBSS）を構築できます。Realtek 製カードは単機の IBSS は構築できますが、802.11s mesh は実現できません。
- **長距離のシングルストリーム monitor によるモニタリング**：ホッピング 120 秒で 19 AP + 14 client を検出し、コミュニティでは Very Long range と評価されています。
- **2.4GHz の injection、および AP / WPA3 ホットスポット**：2.4G のインジェクションは 96–100%、WPA3 は `sae_pwe=0` を正しく設定すれば新旧の iPhone が接続できます。

**留意点（正直な制限事項）**

- 5GHz の AP ごとの injection は今回ブロードキャストまでしか確認できておらず、パーセンテージはありません。
- AP を開くときは 802.11n の無効化、WPA3 では `sae_pwe=0` が必要です。どちらの設定を誤っても、古い iPhone では「パスワード間違いのように見える」状態になります。
- シングルアンテナの 1T1R で、スループットと位置づけは 2T2R の ACM／ACH とは別クラスです。

**機種選定の指針**：中心となる要件が、両バンドでの安定したインジェクションとエンドツーエンドの handshake であれば、9 機種の中では AWUS036EACS / AWUS036ACH / AWUS036ACS がより適しています。Wi-Fi 6 + AP ホットスポットが必要なら AWUS036AX / AWUS036AXER を、mesh / IBSS の単機実験や長距離モニタリングが主目的なら、ACHM（またはその 2T2R の姉妹機種 ACM）が適切なツールです。最後に避けるべき点として、injection / handshake の用途では AWUS036AXM / AXML を選ばないでください。この 2 枚の MT7921 のインジェクションは、本プラットフォームでは失敗しました。

9 機種のハードウェア、ドライバ、Monitor / Injection / AP / WPA3 の全マトリクスと、用途別の機種選定の総評は、Hub 総括表をご覧ください：[9 種の ALFA ワイヤレスカード ARM64 / GX10 実測総合マトリクス](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## よくある質問（FAQ）

**Q：AWUS036ACHM は Ubuntu 24.04 でドライバのインストールが必要ですか？**
不要です。MT7610U は kernel 組み込みの mt76x0u ドライバが処理するため、Ubuntu 24.04（kernel 6.17）では挿すだけで認識され、DKMS も追加ファームウェアも要りません。lsusb で USB ID 0e8d:7610 を確認できます。

**Q：AWUS036ACHM は monitor mode に入れますか？AP はいくつ見つかりますか？**
入れます。2.4GHz・5GHz のどちらでも monitor mode に入れます。airodump-ng でホッピングしながら全バンドを 120 秒スキャンしたところ、実測で 19 台の AP と 14 台のクライアントを検出し、分布は ch1、2、5、6、36、149、157 でした。

**Q：AWUS036ACHM のパケットインジェクション成功率はどのくらいですか？5GHz でも使えますか？**
2.4GHz のチャンネル 6 では、AP ごとのインジェクション応答率が 96–100% でした（aireplay-ng --test、4 台の AP を検出）。5GHz（ch36、ch149）ではブロードキャストのインジェクションが動作することしか確認できず、AP ごとのテストは Found 0 APs と報告されました。今回はパーセンテージを取得できておらず、原因は調査中です。

**Q：AWUS036ACHM で AP を開くと iPhone に「ネットワークに接続できません」や「パスワードが違います」と表示される場合は？**
まず 802.11n を無効にしてください。hostapd の設定ファイルに ieee80211n=1 と ht_capab を入れず、2.4GHz は純粋な hw_mode=g、5GHz は純粋な hw_mode=a（20 MHz）を使います。そうしないと hostapd に handle_assoc_cb: STA not found が繰り返し出力され、画面上はパスワード間違いのように見えますが、実際は 802.11n のアソシエーション失敗です。

**Q：AWUS036ACHM の WPA3-SAE で、古い iPhone が接続できないのはなぜですか？**
多くの場合は hostapd の sae_pwe 設定が原因です。実測では sae_pwe=0 のとき iPhone 7 Plus も iPhone 15 Pro も接続できました。sae_pwe=2 のときは、iPhone 7 Plus はアソシエーションには成功するものの 4-way ハンドシェイクに失敗して切断され、パスワード間違いのように見えます。ieee80211w=2 と組み合わせ、設定変更後は iPhone でいったんそのネットワークを削除してから再接続してください。

## 6. 関連記事

- 〔Hub 総括表〕9 種の ALFA ワイヤレスカードを ASUS GX10（ARM64 / Ubuntu 24.04）で使う場合の Monitor・Injection・AP 全マトリクスと機種選定の総評 → [/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 〔姉妹機種〕AWUS036ACM（MT7612U / 2T2R）個別実機検証 — 内部リンク準備中（placeholder）
- 〔プラットフォーム解説〕ドライバ不要：Ubuntu 24.04 + kernel 6.17 の in-kernel ドライバで ALFA ワイヤレスカードの Monitor と AP を有効化 — 内部リンク準備中（placeholder）
- 〔特集〕WPA3-SAE 時代の handshake キャプチャ対応と `sae_pwe` 互換性の落とし穴 — 内部リンク準備中（placeholder）

---

*検証担当：Yopitek（ALFA Network 台湾代理店）— https://www.yupitek.com ｜ 検証環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ テスト機器：Apple iPhone 7 Plus（WPA3 のみ iPhone 15 Pro でも測定）。数値は 2026-11-16～11-18 の実機テストレポートからの引用であり、第三者のネットワークを対象とせず、攻撃手順も提供しません。*
