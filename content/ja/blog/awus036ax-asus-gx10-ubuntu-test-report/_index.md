---
title: "ALFA AWUS036AX 個別実機検証：ASUS GX10 + Ubuntu 24.04 での Wi-Fi 6 Monitor / Injection / AP 機能レポート（Realtek RTL8832BU / rtw89_8852bu）"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX（Wi-Fi 6）を Ubuntu 24.04 ARM64 で実機検証。ドライバのインストールは不要で、Monitor、2.4G インジェクション 96%、5G AP VHT80、WPA3-SAE、エンドツーエンドの handshake（.22000）が通りました。IBSS / mesh には対応していません。プラットフォームは ASUS GX10、RTL8832BU です。"
faq:
  - question: "AWUS036AX は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？lsusb に 0bda:1a2b と表示された場合はどうすればよいですか？"
    answer: "本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8832BU は組み込みの rtw89_8852bu ドライバで、コンパイルも DKMS も要りません。lsusb に 0bda:1a2b（CD-ROM モード）と表示された場合は、sudo usb_modeswitch -v 0bda -p 1a2b -K を実行して WLAN に切り替えてください。"
  - question: "AWUS036AX は monitor mode とパケットインジェクションに対応していますか？"
    answer: "対応しています。2.4 GHz のインジェクションは 29/30（96%）、5 GHz は AP を 1 台ずつ指定して試験すると Injection is working! が返りました。airodump-ng のチャンネルホッピング 60 秒で、14 台の AP と 4 台の client を検出しています。active monitor、IBSS、mesh には対応していません。"
  - question: "AWUS036AX で WPA handshake を取得できますか？MT7921 の AXM / AXML ではどうですか？"
    answer: "AX は取得できます。自前の AP と自前の iPhone 7 Plus で、aireplay-ng -0 により再接続を誘発し、airodump-ng で完全な M1–M4 を取得して、hcxpcapngtool で .22000 に変換しました。MT7921 の AXM / AXML はこのプラットフォームでインジェクションに失敗するため、実現できません。自分が所有する、または許可を得たネットワークに限ります。"
  - question: "AWUS036AX は AP（アクセスポイント）として使えますか？WPA3 には対応していますか？"
    answer: "使えます。hostapd で 2.4G（802.11n）と 5G（VHT 80 MHz）の AP を立て、iPhone 7 Plus が接続すると VHT-NSS2 80 MHz と表示されました。WPA3-SAE（ieee80211w=2、sae_pwe=0）は 2.4 GHz で iPhone 15 Pro が接続し、MFP: yes でした（5 GHz の WPA3 は未実測）。"
  - question: "AWUS036AX と AWUS036AXER の違いは何ですか？どちらを選ぶべきですか？"
    answer: "どちらも RTL8832BU + rtw89_8852bu で、機能マトリクスは同じです。違いはアンテナと受信性能で、AXER は外付けアンテナを備え、同じ検証でチャンネルホッピングにより 63 AP + 12 client を検出しました（AX は 14 AP + 4 client）。デスク据え置きなら AX、長距離や最強の受信が必要なら AXER を選んでください。"
draft: false
---

**要点まとめ（TL;DR）**：Yopitek（ALFA Network 台湾代理店）の実測では、AWUS036AX は ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）でドライバのインストールが不要で、両バンドの monitor が使えます。2.4G のインジェクションは 96%、5G の AP は VHT80 で、エンドツーエンドの .22000 取得も通りました。IBSS / mesh には対応していません。

> 本記事は、Yopitek が**自社設備・自社オフィスの Wi-Fi（SSID `YUPITEK`）・自社のテスト用スマートフォン**上で実施した、製品の互換性と機能の実機検証です。対象は ALFA **AWUS036AX**（Realtek RTL8832BU、Wi-Fi 6 2x2）です。
> 検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。比較用の端末は Apple iPhone 7 Plus（WPA3 と VIF は iPhone 15 Pro でも別途検証）です。
> ⚠️ **合法的な使用について**：Monitor と Injection は、自分が所有する、または許可を得たネットワークでのみ実施してください。AP モードは各地域の電波法規に従ってください。本記事は第三者のネットワークに対する攻撃操作を一切扱いません。

---

## 1. このカードと検証プラットフォーム

AWUS036AX は ALFA の今世代の Wi-Fi 6 USB 無線 LAN カードで、チップは Realtek RTL8832BU、2x2 のデュアルスペーシャルストリームに対応し、2.4 GHz と 5 GHz のデュアルバンドで動作します。ALFA の製品ラインでは、外付けアンテナ版の AWUS036AXER とチップもドライバも共通で、違いはアンテナの形式と受信ゲインです。同じ Wi-Fi 6 でも MediaTek 系の AWUS036AXM / AXML とはまったく別のチップ系統で、実測の結論も大きく異なります（第 5 節で説明します）。

今回の検証ではカタログ上の理論速度には触れず、販売や技術の現場が最も気にする 3 点だけに答えます。新しい Linux で導入しやすいか。実際に使える無線機能はどれか。ドライバの仕様上そもそもできず、時間を費やすべきでないものはどれか。結論は再現できなければならないため、すべてのコマンドは 2026-11-18 の当日に GX10 の実機で 1 つずつ実行しており、以下の「実測出力」は本物の抜粋です（MAC アドレスは `xx` で伏せています）。

検証の境界を先に明確にしておきます。すべて自社のオフィス内で、自社の `YUPITEK` ネットワークと自社のスマートフォンに対して実施しました。Monitor は自分の環境のパケットしか受信せず、Injection と handshake は自社の AP と自社の iPhone に対してのみ操作しています。目的は「このカードがこのマシンで何ができるか」を検証することであり、第三者のネットワークへの攻撃を示すことではありません。

---

## 2. ハードウェアとドライバ（Wi-Fi 6、インストール不要）

この世代の最も実際的な利点は、**挿すだけで認識され、コンパイルも DKMS も不要**なことです。RTL8832BU 用の `rtw89_8852bu` ドライバはすでに kernel 6.17 の in-kernel モジュールになっており、GX10 は起動時点でバインド済みです。GitHub から out-of-tree のプロジェクトを持ってきて手動でビルドする必要はありません。

チップ情報と確認手順は次のとおりです。まず `lsusb` で、カードが WLAN モードで列挙されていることを確認します。

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

`ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter` と表示されるはずです。本検証のこのカードは WLAN モードでそのまま現れ、光ディスク（CD-ROM）モードで止まることはありませんでした。お手元のカードに `0bda:1a2b` と表示される場合は、まだ光ディスクモードのままという意味ですので、`sudo usb_modeswitch -v 0bda -p 1a2b -K` で WLAN に切り替えてください。

次に、ドライバとファームウェアのロードを確認します。

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

実機でロードされたのは `rtw89/rtw8852b_fw-1.bin`、firmware version は `0.29.29.5` でした。ドライバもファームウェアも kernel に組み込まれており、別途パッケージを導入する必要はありません。

最後に、このドライバが**どのインターフェースモードを宣言しているか**を確認します。この手順が、後述のどの機能が使えて、どれが N/A になるかを直接決めます。

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

実機の一覧は `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO` でした。一覧には IBSS、mesh point、active-monitor がありません。これは設定を間違えたのではなく、`rtw89_8852bu` がこの 3 つのモードをもともと実装していないためで、第 4 節ではこれを根拠に N/A としています。

---

## 3. 実測した機能：Monitor / Injection / AP / WPA3

まず機能の一覧表を示します。各セルは、下に載せた実測の抜粋に対応しています。

| 機能 | 2.4 GHz | 5 GHz | 実測の抜粋 |
|---|---|---|---|
| **Monitor** | ✅ 強い | ✅ 強い | airodump のチャンネルホッピング 60 秒で **14 AP + 4 client** を検出 |
| **Injection** | ✅ **96%** | ✅ 利用可 | 2.4G の `aireplay-ng --test` は 29/30（96%）、5G は AP を 1 台ずつ指定して `Injection is working!` |
| **AP** | ✅ 802.11n（HT） | ✅ **VHT 80 MHz** | iPhone 7 Plus が接続：2.4G は MCS 12、5G は VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | 未実測 | iPhone 15 Pro が接続、MFP: yes（`sae_pwe=0`）。2.4 GHz のみ実測 |
| **WPA handshake 取得** | ✅ **エンドツーエンド** | — | 自社の iPhone に deauth → 完全な 4-way を取得 → hashcat の `.22000` に変換 |

**Monitor（モニタモード／受信）✅ 強い。** monitor に切り替えると、2.4 GHz も 5 GHz も大量のパケットを受信できました（それぞれ約 100 パケット/6 秒）。`airodump-ng --band abg` でチャンネルホッピングを 60 秒行ったところ、14 台の AP と 4 台の client を検出しました。受信性能は ALFA の Wi-Fi 5 モデルである ACM / ACHM と同等で、MediaTek MT7921 を使った 2 モデル（AXM / AXML は実測で受信が弱め）を大きく上回ります。現場調査やチャンネルの占有状況の棚卸しといった作業には、このカードの受信性能で十分です。

**Injection（パケットインジェクション）✅ 利用可。これが、AX と MediaTek 系の決定的な違いでもあります。** 2.4 GHz（ch6）で `aireplay-ng --test` を実行したところ、実測は `29/30: 96%`、`Injection is working!`、応答率は 96% でした。5 GHz（ch36）では、ブロードキャストでのテストは `Found 0 APs` と返ることがあります（最近の AP はブロードキャストの probe に応答しないため、これは正常です）。しかし AP の BSSID を 1 台ずつ指定して試験すると `Injection is working!` が返り、5 GHz でもインジェクションが使えることを確認しました。これに対し、同じ Wi-Fi 6 の MediaTek AXM / AXML は、このプラットフォームでは**インジェクションが即座に失敗**します（主因は kernel 6.16 以降の mac80211 chanctx のリグレッションで、加えてファームウェアがインジェクションのレートを 1／6 Mbps に固定しており、チップ自体の限界ではありません）。機種選定の際は、この点を必ず区別してください。

**AP ✅ 両帯域で構築可能、5 GHz は VHT80 に対応。** hostapd で AP を立てました。2.4 GHz は 802.11n（`ieee80211n=1`、HT20）で、iPhone 7 Plus が接続すると MCS 12、authorized と表示されました。5 GHz は VHT 80 MHz（`vht_oper_chwidth=1`、`ht_capab=[HT40+]`）で、iPhone 7 Plus が接続すると VHT-NSS2 80 MHz、authorized と表示されました。どちらの帯域でもクライアントを安定して接続でき、80 MHz の帯域幅も実際にネゴシエーションが成立しています。

**WPA3-SAE ✅（2.4 GHz。5 GHz は未実測）。** AP の `wpa_key_mgmt` を `SAE` に、`ieee80211w=2` に変更したところ、iPhone 15 Pro が接続し、MFP（Management Frame Protection）は yes と表示されました。ここには互換性に関する細かい点があります。`sae_pwe` は `0`（Hunting-and-Pecking）に設定する必要があり、そうしないと古い iPhone は接続できません。

**WPA handshake 取得 ✅ エンドツーエンドで成功。** 自社の `YUPITEK` ネットワークで、自社の iPhone 7 Plus を相手に一連の流れを実施しました。そのチャンネルを monitor でキャプチャ → `aireplay-ng -0` で deauth を送り再接続を誘発 → `airodump-ng` で完全な 4-way handshake（M1/M2/M3/M4）を取得 → `hcxpcapngtool` で hashcat の `.22000` 形式に変換、という手順です。このカードはインジェクションが使えるため、チェーン全体が成立しました。インジェクションに失敗するカード（AXM / AXML など）は、deauth の段階で途切れてしまいます。この handshake 取得の流れで使った Kali の定番ツール（aircrack-ng、hcxtools）は、すべて Ubuntu 24.04 ARM64 上でそのまま動作しました。

---

## 4. 高度な機能と制限事項（rtw89 ドライバの N/A 項目）

この節では、「実行できる高度な機能」と「ドライバの仕様上そもそもできないこと」を一度にはっきりさせ、現場で時間を無駄にしないようにします。

| 機能 | 状態 | 説明 |
|---|---|---|
| **VIF（STA + AP 並行）** | ✅ | メインのインターフェースを `YUPITEK` に接続しつつ、AP VIF（ch36 VHT80）を同時に開き、2 つのインターフェースが並行動作。STA 側の ping は 3.2 ms |
| **WPA handshake 取得** | ✅ エンドツーエンド | M1–M4 を取得し、`hcxpcapngtool` で `.22000` に変換 |
| **Active monitor** | **N/A** | `rtw89_8852bu` にはこのモードがない（`iw phy` の supported modes にない） |
| **Ad-hoc（IBSS）** | **N/A** | ドライバが非対応 |
| **Mesh（802.11s）** | **N/A** | ドライバが非対応 |
| **Wi-Fi Direct（P2P）** | ⬜ 未検証 | ドライバは対応を宣言しているが、2 台目の機器が必要なため今回は省略 |

**VIF ✅。** AP 用の仮想インターフェース（別の MAC、unmanage）を作成し、メインのインターフェースは Wi-Fi に接続したまま、同じチャンネルで AP を開きます。実測では、メインのインターフェースが `YUPITEK` に接続している間に、AP VIF が ch36 で VHT80 として動作し、2 つのインターフェースが並行して稼働しました。STA 側の ping は 3.2 ms です。「一方でインターネットに接続しつつ、もう一方でテスト用のホットスポットを開く」という使い方は可能です。

**Active monitor / IBSS / Mesh は N/A であり、故障ではありません。** この 3 つのモードは、第 2 節の `iw phy info` の supported interface modes に現れておらず、`rtw89_8852bu` ドライバがそもそも実装していないことを意味します。`sudo iw dev $IF set type ibss` のようなコマンドは直接失敗し、解決策もありません。パラメータやファームウェアで救えるものではなく、これら 3 つのモードを使うにはチップ系統を変える必要があります（例えば MediaTek mt76 の ACM / ACHM は、単機で IBSS / mesh を構築できます）。

**まず知っておくべきプラットフォームレベルの制限が 1 つあります。GX10 では hcxdumptool が `failed to arm` になります。** これは AX 固有の問題ではありません。`hcxdumptool 8.x` は active-monitor を必要とし、さらに GX10 は内蔵のトライバンド NIC を持つため、USB カードの列挙時に `-I` が内蔵の phy に誤ってマッピングされやすく、検証したすべての USB カードがこのマシンで arm に失敗します（唯一の例外は 2.4 GHz の AWUS036EACS です）。実務上は**aircrack-ng スイートに切り替え**（airodump-ng + aireplay-ng）てキャプチャを行います。本カードはインジェクションが使えるため、チェーン全体はエンドツーエンドで問題なく完了します（第 3 節を参照）。

**安全上のルール（GX10 プラットフォーム共通）：** `airmon-ng check kill` は絶対に実行しないでください。NetworkManager が停止して GX10 の外部接続が切れます。操作は `wlx*` インターフェースのみにとどめ、内蔵の外部接続用 NIC には触れないでください。

---

## 5. 適した用途と選定（Wi-Fi 6 AP、Hub への接続）

実測の結論を選定のアドバイスに言い換えます。**AWUS036AX の最適な用途は、「Wi-Fi 6 + AP」で、かつインジェクション機能も必要な場面です。**

| 用途 | AWUS036AX の適性 | 説明 |
|---|---|---|
| Wi-Fi 6 AP / エッジアクセス | ★ 第一候補 | 2x2 VHT80 でデュアルバンド構築可、WPA3-SAE も利用可 |
| Injection + handshake 監査 | ★ 対応可能 | 2.4G は 96%、5G は利用可、エンドツーエンドの取得に成功 |
| 最強の受信 / 長距離 monitor | ○ 十分だが第一候補は AXER | 同じチップの AXER は外付けアンテナで受信がより強い |
| mesh / IBSS の実験 | ✗ 不向き | ドライバが N/A。mt76 の ACM / ACHM を選ぶ |

**典型的な導入例：Wi-Fi 6 のホットスポットとして使い、エッジ機器を中央の Hub に接続する。** 実測済みの AP（VHT80）と VIF の機能を使い、GX10 とこのカードで Wi-Fi 6 のアクセスポイントを構成します。テスト用スマートフォンや IoT センサーといったエッジ機器が接続したあと、トラフィックはメインのインターフェースを経由して中央の Hub（gateway）に戻ります。VIF の実測で、「メインのインターフェースで上位ネットワークに接続する」ことと「下流向けに AP を開く」ことが並行できると確認でき、STA 側のレイテンシは 3.2 ms でした。このトポロジーは、本プラットフォームで実現可能であることを検証済みです。エッジのアクセス区間にさらに最新の暗号化が必要なら、WPA3-SAE を追加すれば済みます。

**選定上の注意：注入 / handshake 用途なら、AWUS036AXM / AXML は選ばないでください。** この 2 モデルは同じ Wi-Fi 6 2x2 で AP も立てられますが、MediaTek MT7921 は本プラットフォームで**インジェクションに失敗**するため、deauth ができず、handshake も取得できません。お客様が単純な Wi-Fi 6 の AP / 一般接続用カードだけを求めていて、インジェクションをまったく使わないのであれば、MediaTek 系でも安定しているため問題ありません。ただし、用途が少しでも無線監査に関わるなら、Realtek の AX（または外付けアンテナの AXER）を選ぶべきです。

**同じチップの AXER とはどう使い分けるか？** 両者はチップ、ドライバ、機能マトリクスが同じです。AXER は外付けアンテナ版で、受信と長距離 monitor がより強力です（同じ検証で AXER はチャンネルホッピングにより 63 AP + 12 client を検出しました）。デスクに据え置きでアンテナの要求が高くなければ AX を、距離を伸ばしたい、あるいは最強の受信が欲しいなら AXER を選んでください。

---

## よくある質問（FAQ）

**Q：AWUS036AX は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？lsusb に 0bda:1a2b と表示された場合はどうすればよいですか？**
本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8832BU は組み込みの rtw89_8852bu ドライバで、コンパイルも DKMS も要りません。lsusb に `0bda:1a2b`（CD-ROM モード）と表示された場合は、`sudo usb_modeswitch -v 0bda -p 1a2b -K` を実行して WLAN に切り替えてください。

**Q：AWUS036AX は monitor mode（モニタモード）とパケットインジェクションに対応していますか？**
対応しています。2.4 GHz のインジェクションは 29/30（96%）、5 GHz は AP を 1 台ずつ指定して試験すると `Injection is working!` が返りました。airodump-ng のチャンネルホッピング 60 秒で、14 台の AP と 4 台の client を検出しています。active monitor、IBSS、mesh には対応していません。

**Q：AWUS036AX で WPA handshake（ハンドシェイクパケット）を取得できますか？MT7921 の AXM / AXML ではどうですか？**
AX は取得できます。自前の AP と自前の iPhone 7 Plus で、`aireplay-ng -0` により再接続を誘発し、`airodump-ng` で完全な M1–M4 を取得して、`hcxpcapngtool` で .22000 に変換しました。MT7921 の AXM / AXML はこのプラットフォームでインジェクションに失敗するため、実現できません。自分が所有する、または許可を得たネットワークに限ります。

**Q：AWUS036AX は AP（アクセスポイント）として使えますか？WPA3 には対応していますか？**
使えます。`hostapd` で 2.4G（802.11n）と 5G（VHT 80 MHz）の AP を立て、iPhone 7 Plus が接続すると VHT-NSS2 80 MHz と表示されました。WPA3-SAE（ieee80211w=2、sae_pwe=0）は 2.4 GHz で iPhone 15 Pro が接続し、MFP: yes でした（5 GHz の WPA3 は未実測）。

**Q：AWUS036AX と AWUS036AXER の違いは何ですか？どちらを選ぶべきですか？**
どちらも RTL8832BU + rtw89_8852bu で、機能マトリクスは同じです。違いはアンテナと受信性能で、AXER は外付けアンテナを備え、同じ検証でチャンネルホッピングにより 63 AP + 12 client を検出しました（AX は 14 AP + 4 client）。デスク据え置きなら AX、長距離や最強の受信が必要なら AXER を選んでください。

---

## 6. 関連記事

- 〈ALFA 無線 LAN カード 9 モデル ASUS GX10 + Ubuntu ARM64 機能総合表〉—— 全モデルの Monitor / Injection / AP / handshake を一度に比較 → [総合表 Hub](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [ドライバのインストール不要：Ubuntu 24.04 + kernel 6.17 で in-kernel ドライバを使い Monitor と AP を有効にする](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)——rtw88 / rtw89 / mt76 共通の設定手順
- [AWUS036AXER 個別実機検証](/ja/blog/awus036axer-asus-gx10-ubuntu-test-report/)——同じチップの外付けアンテナ版。受信と長距離 monitor の比較
- [WPA3-SAE handshake 取得機能の実機検証と sae_pwe の互換性](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)——iPhone 接続時の `sae_pwe` の落とし穴

---

*検証担当：Yopitek（ALFA 代理店）— https://www.yupitek.com ｜ 検証環境：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 ｜ 比較用端末：Apple iPhone 7 Plus（WPA3 / VIF は iPhone 15 Pro でも別途検証）*
