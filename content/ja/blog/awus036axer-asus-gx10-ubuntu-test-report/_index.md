---
title: "AWUS036AXER 実測レポート：ASUS GX10 + Ubuntu 24.04（ARM64）で受信性能が最も高い Wi-Fi 6 アダプター"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER は ASUS GX10／Ubuntu 24.04 ARM64 でドライバ追加不要（rtw89_8852bu）。monitor 60 秒で 63 AP＋12 client を検出、injection は 73%（2.4G）、5G VHT80 AP と WPA3 も合格。"
faq:
  - question: "AWUS036AXER は Ubuntu 24.04 や Kali で別途ドライバのインストールが必要ですか？"
    answer: "Ubuntu 24.04（ARM64、kernel 6.17.0-1014-nvidia）では不要です。内蔵の rtw89_8852bu ドライバが挿すだけで認識され、コンパイルも DKMS も不要です（firmware rtw8852b_fw 0.29.29.5）。本記事のプラットフォームは Kali ではなく Ubuntu のため、Kali 本体は未検証です。Kali でよく使われる airmon-ng、kismet、bettercap、wifite、Wireshark は本プラットフォームで利用できます。kernel が古い場合は内蔵されている保証がないため、先にバージョンを確認してください。"
  - question: "AWUS036AXER は monitor mode に対応していますか？受信性能はどのくらいですか？"
    answer: "対応しており、2.4 GHz でも 5 GHz でも monitor に入れます。自社オフィスで airodump-ng によるチャンネルホッピングスキャンを 60 秒実施したところ、63 個の AP と 12 個の client を検出しました。これは同条件で比較した 9 製品の中で最も高い受信性能です。同じチップの AWUS036AX は別の測定で 14 AP＋4 client でした（2 回の測定は同時実施ではないため、参考値です）。"
  - question: "AWUS036AXER でパケットインジェクション（packet injection）はできますか？"
    answer: "できます。2.4 GHz の aireplay-ng --test の応答率は 73%（22/30）で Injection is working! と表示され、5 GHz の個別 AP セルフテストも合格しました。自社ネットワークと自社デバイスで handshake の取得と .22000 への変換まで完了しています。両バンドとも 100% に近い値を求める場合は、本プラットフォームの実測では AWUS036EACS、ACH、ACS のほうが安定しています。自分が所有または許可を得たネットワークでのみ実施してください。"
  - question: "AWUS036AXER と AWUS036AX の違いは何ですか？"
    answer: "どちらも Realtek RTL8832BU を搭載し、rtw89_8852bu を使用します。本プラットフォームではモード対応も injection の挙動も同じです。違いはアンテナ調整とゲインによる受信性能です（AXER は 60 秒で 63 AP＋12 client、AX は 14 AP＋4 client）。どちらも内蔵アンテナで RP-SMA はありません。アンテナ仕様は製品ページをご確認ください。"
  - question: "AWUS036AXER は AP として使えますか？WPA3 は開けますか？非対応のモードは？"
    answer: "使えます。2.4 GHz 802.11n と 5 GHz VHT80（VHT-NSS2、351 Mbit）のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は sae_pwe=0 で iPhone 15 Pro が接続でき（2.4 GHz で実測。5 GHz の WPA3 は未実測）、STA＋AP の同時動作も可能です。ただし rtw89_8852bu は active monitor、IBSS、mesh に対応していません。"
draft: false
---

{{< tldr >}}AWUS036AXER は ASUS GX10／Ubuntu 24.04 ARM64 で挿すだけで使えます（内蔵の rtw89_8852bu）。monitor 60 秒で 63 AP＋12 client を検出し、2.4 GHz の injection は 73%、AP と WPA3 も合格しました。active monitor、IBSS、mesh には対応していません。{{< /tldr >}}

> 本記事は、Yopitek（ALFA 台湾代理店）が自社設備で実施した、製品の互換性と機能の実測レポートです。
> テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。テスト環境は自社オフィスの Wi-Fi（SSID `YUPITEK`）で、自社のテスト用スマートフォン iPhone 7 Plus（WPA3 のみ iPhone 15 Pro を追加使用）を対象に実施しました。
> ⚠️ **合法的な使用**：Monitor と Injection は、自分が所有している、または許可を得たネットワークとデバイスに限ってください。AP モードは各地域の電波法規に従ってください。本記事はアダプターの機能、互換性、設定、選定に焦点を当てており、第三者のネットワークに対する攻撃操作は一切扱いません。

---

## 1. このアダプターとテストプラットフォーム

AWUS036AXER は、ALFA の Wi-Fi 6（802.11ax）2x2 USB アダプターで、Realtek RTL8832BU チップを採用しています（Bluetooth なし）。同社の AWUS036AX とは**同じチップ、同じドライバ**（`rtw89_8852bu`）を使っており、本プラットフォームでのモード対応と挙動は一致します。両者の本当の違いは**アンテナ調整とゲイン**であり、外付けか内蔵かではありません。AXER は**内蔵（Nano）アンテナ設計で RP-SMA はなく**、チップと RF 調整によって受信性能を最大限に引き出しています。この記事の核心となる結論を先にお伝えします。比較した 9 枚の ALFA アダプターの中で、AXER は**最も受信性能が高い 1 枚**でした。

テストプラットフォームは ASUS GX10 で、NVIDIA GB10 スーパーチップと 128GB の統合メモリを搭載し、OS は Ubuntu 24.04 LTS、アーキテクチャは ARM64（aarch64）、kernel は `6.17.0-1014-nvidia` です。すべての結果は 2026-11-18 にこのマシンの実機で取得しました。テストデバイスは自社の iPhone 7 Plus（WPA3 のみ iPhone 15 Pro を追加使用）、テストネットワークは自社オフィスの Wi-Fi です。代理店としての検証において、ARM64 と新しい kernel の組み合わせは比較的厳しい条件です。なぜこの世代のほうがむしろ手間が少ないのかは、次の第 2 節で説明します。

仕様面の補足です。AXER は 2x2（2 空間ストリーム）の Wi-Fi 6 アダプターで、2 本の空間ストリームを同時に送受信できます。これは後述の 5 GHz AP 実測でネゴシエートされた VHT-NSS2 にも対応しています。ただし今回このアダプターが優位に立ったのは、ストリーム数ではなくアンテナ設計と RF 調整によるものです（AX も同じ 2x2 です）。チップ、ドライバ、プラットフォームがすべて同一で、アンテナ調整がほぼ唯一の変数となるため、AXER と AX の受信性能の差は、内蔵アンテナ設計とゲイン調整によるものと明確に切り分けられます。

---

## 2. ハードウェアとドライバ（内蔵アンテナ、ドライバ追加不要）

AWUS036AXER は、Ubuntu 24.04 の 6.17 kernel 上で**挿すだけで認識され、コンパイルも DKMS も不要**です。ドライバ `rtw89_8852bu` はすでに in-kernel モジュールで、firmware は `rtw8852b_fw`（バージョン 0.29.29.5）、起動時に読み込まれます。GitHub から out-of-tree プロジェクトを取得したり、DKMS を設定したりする必要はありません。長期運用し、kernel 更新を何度も経る代理店や教育環境にとって、ドライバのビルド工程がなくなることは、最も多い障害ポイントが 1 つ減ることを意味します。

従来の方法と比べると違いがよく分かります。以前は Realtek のこの種の USB チップの多くが mainline kernel に入っておらず、GitHub から out-of-tree プロジェクト（たとえば `morrownr/USB-WiFi`）を取得し、DKMS で現在の kernel に合わせてビルドする必要がありました。kernel を更新するたびに再ビルドが必要で、ビルドに失敗するとアダプターがそのまま消えてしまいます。rtw89 が in-kernel に正式に取り込まれたことで、6.17 ではこれらの手順をまるごと省略でき、同じ操作を同じドライバの複数のアダプターで使い回せます。

まず、アダプターが正しく認識されているか確認します。

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

通常の WLAN モードの USB ID は `0bda:b832` です。`0bda:1a2b` と表示された場合は、アダプターが「CD-ROM モード」のままであることを示します。`sudo usb_modeswitch -v 0bda -p 1a2b -K` を一度実行して WLAN モードに切り替えてください。今回のテスト機は最初から WLAN モードで列挙され、CD-ROM モードには遭遇しませんでした。

インターフェース名は `wlx` + MAC 形式（例：`wlxAABBCCDDEEFF`）で、どのマシンに挿しても変わらないため、スクリプトでの固定指定に便利です。このアダプターが対応するモードは次のように確認できます。

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

実測で報告されたモードは managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO でした。IBSS、mesh、active monitor はありません。これは rtw89 ドライバ本来の制限であり、第 4 節で正直に説明します。選定時に見誤らないようにしてください。

アンテナについて：AXER は内蔵（Nano）アンテナ設計で RP-SMA はなく、同じチップの AX との違いはアンテナ調整とゲインにあります。実用上、最も直接的に現れるのが受信感度です。次節の monitor のデータで、この点を明確にします。

---

## 3. 実測した機能

3 つの主要機能（Monitor / Injection / AP）と WPA3 の実測結果をまず表にまとめ、詳細は表の後で項目ごとに説明します。

| 機能 | 2.4 GHz | 5 GHz | 実測のポイント |
|---|---|---|---|
| **Monitor（監視）** | ✅ 強い | ✅ 強い | ホッピングスキャンで **63 AP + 12 client** を検出。9 枚中で受信性能が最高 |
| **Injection（注入）** | ✅ 73% | ✅ 利用可 | 2.4G `22/30 73%`、5G `Injection is working!` |
| **AP（アクセスポイント）** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone が接続。5G は VHT-NSS2、351 Mbit |
| **WPA3-SAE** | ✅ | 未実測 | AP 側で iPhone 15 Pro が接続（`sae_pwe=0`）。2.4 GHz のみ実測 |
| **WPA handshake 取得** | ✅ エンドツーエンド | — | 自社ネットワーク＋自社デバイス、4-way（M1–M4）→ `.22000` |

### 3-1. Monitor（本記事のハイライト：受信性能が最強）

monitor への切り替えは標準的な `iw` の手順です。まずインターフェースの管理を自分に切り替え（`nmcli dev set $IF managed no`）、インターフェースを down にし、monitor type を設定し、up にして、チャンネルを設定します。

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; 2.4 GHz は channel 6 を使用
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

2.4 GHz と 5 GHz のどちらも、6 秒以内に 100 frames を取得できました。本当に差がついたのはホッピングスキャンです。`sudo airodump-ng --band abg $IF` を 60 秒実行し、**63 個の AP と 12 個の client を検出**しました。これは今回の 9 枚の中で最も多くのターゲットを捉えた結果で、内蔵アンテナ設計と RF 調整による受信面での優位性を直接反映しています。現地調査（site survey）、長距離の監視、信号が弱い環境では、この受信性能こそが AXER の最大の価値です。

### 3-2. Injection（注入）

Injection は aireplay-ng のセルフテストモードで検証しました。測定対象はアダプター自体の能力であり、外部への攻撃ではありません。

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

2.4 GHz の応答率は 73%（22/30）で、利用可能と判定しました。5 GHz でも、指定した AP に対する個別セルフテストで `Injection is working!` と報告されました。プラットフォーム共通の注意点を 1 つ補足します。**5 GHz で送信／注入する前に `iw reg set US` で TX 電力の制限を解除し、テスト後は `iw reg set TW` で台湾の規制バンドに戻してください**。

### 3-3. AP（アクセスポイント）（2.4 GHz 802.11n、5 GHz VHT 80 MHz）

AXER は両バンドで hostapd の AP を立ち上げられます。2.4 GHz は `hw_mode=g` + `ieee80211n=1` で 802.11n のアクセスポイントを起動し、iPhone 7 Plus が接続して MCS 15、authorized にネゴシエートされました。5 GHz は `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` で VHT 80 MHz のアクセスポイントを起動し、iPhone 7 Plus の接続は **VHT-NSS2、80 MHz、351 Mbit、authorized** にネゴシエートされました。AP 起動の前提として `sudo nmcli dev set $IF managed no` が必要です。また `wpa_passphrase` は 8 文字以上にしてください。そうでないと hostapd が `invalid WPA passphrase length` を返します。

### 3-4. WPA3-SAE と handshake 取得

WPA3-SAE は AP 側で `wpa_key_mgmt=SAE`、`ieee80211w=2`、`sae_pwe=0` を設定し、実測で iPhone 15 Pro が接続できました。**`sae_pwe` は、ALFA のこのシリーズのアダプターにおける互換性の落とし穴です**。一部のデバイスは `sae_pwe=2`（Hash-to-Element）では接続できず、`sae_pwe=0` にすると古い iPhone とも互換性が保てます。

handshake 取得は、**自社オフィスの Wi-Fi（YUPITEK）＋自社のテストデバイス**でエンドツーエンドの検証を行いました。完全な 4-way（M1/M2/M3/M4）を取得し、`hcxpcapngtool` で hashcat が読み込める `.22000` に変換しています。ここで GX10 プラットフォーム共通の現象を指摘しておきます。**`hcxdumptool` は本プラットフォームで、2.4 GHz の AWUS036EACS を除くすべての USB アダプターで `failed to arm` になります**（GX10 内蔵の 3 バンドアダプターとの列挙競合に加え、ドライバに active monitor がないため）。そのため handshake の取得は aircrack-ng スイート（airodump-ng + aireplay-ng）で行います。AXER の injection 性能は、この手順に対して十分です。

---

## 4. 高度な機能と正直な制限事項

**VIF（STA + AP の同時動作）✅**：AXER は、station として上位の Wi-Fi に接続しながら、AP の VIF も立ち上げられます。実測では、メインインターフェースを YUPITEK に接続し、AP VIF を ch36 VHT80 で同時に動作させ、STA 側の ping は 3.5 ms でした。「ネットに接続しながらアクセスポイントも開く」用途に適しています。

**Wi-Fi Direct（P2P）は未検証（⬜）**：ドライバは P2P-client / P2P-GO を宣言していますが、完全に検証するには相手側の 2 台目のデバイスが必要なため、今回は見送りました。したがって検証済みの機能には含めていません。このような「ドライバが対応を宣言しているが実機では試していない」項目は、水増しして合格扱いにせず、一貫して未検証と明記しています。

**非対応の 3 モード（N/A）**：`rtw89_8852bu` ドライバは **active monitor、Ad-hoc（IBSS）、Mesh（802.11s）を提供しません**。`iw dev $IF set type ibss` や `mp` は即座に失敗します。これはドライバ層の制限で、設定で回避することはできません。mesh や IBSS の実験が目的の場合は、MediaTek の mt76 シリーズ（AWUS036ACM / ACHM など）を検討してください。

**プラットフォーム共通の注意事項：**

- `airmon-ng check kill` は絶対に実行しないでください。NetworkManager が停止し、GX10 が外部と切断されます。操作対象は `wlx*` インターフェースのみとし、内蔵の外部接続用アダプターには触れないでください。
- monitor / AP の切り替えを繰り返した後に突然何もスキャンできなくなった場合（RX stall）は、アダプターを**抜き差し**すれば復旧します（USB が再列挙され、インターフェース名は MAC で決まるため変わりません）。
- ARM64 プラットフォームでは、aircrack-ng はソースからのビルドが必要です。wifite は git 版を使用すると、apt の依存関係の競合を回避できます。

**Kali ツールとの互換性**：airmon-ng、kismet 2026.10、bettercap 2.32、wifite（git）、Wireshark / tshark 4.2 のいずれも、AXER をデータソースや管理インターフェースとして問題なく使用できます。

---

## 5. 適した用途と選定の目安

ひとことで位置づけるなら、**AXER は「受信重視」の Wi-Fi 6 アダプター**です。AX と同じチップで機能も一致しており、違いはアンテナ調整とゲインによる受信面の優位性です。そのため選定の考え方は明快です。

| 用途 | AXER は第一候補か | 説明 |
|---|---|---|
| 最強の受信 / 長距離 monitor / 現地調査 | ✅ **第一候補** | ホッピングスキャンで 63 AP + 12 client、9 枚中で最強。AWUS036ACH（デュアルアンテナ高ゲイン）と組み合わせて補完可能 |
| Wi-Fi 6 + AP（アクセスポイント） | ✅ 適している | 2x2、5G VHT80。AWUS036AX と同等 |
| Injection + エンドツーエンドの handshake | 🟡 利用可 | 2.4G 73% で利用可能。両バンドとも 100% に近い値が必要なら AWUS036EACS / ACH / ACS のほうが安定 |
| mesh / IBSS の実験 | ❌ 不向き | rtw89 は非対応のため、AWUS036ACM / ACHM（mt76）を使用 |

典型的な導入シーンは、AXER を**リモート無線監視ノード**として、電波が弱い場所や遠い地点に設置することです。内蔵アンテナの受信面での優位性を活かして現場の AP / client をできるだけ多く収集し、スキャン結果を中央のホストに集約して確認します。内蔵（Nano）アンテナで RP-SMA はないためアンテナは交換できません。より高いゲインや強い指向性が必要な場合は、デュアルアンテナ高ゲインの AWUS036ACH を組み合わせて補完してください。

逆に、純粋な AP や一般的な接続が目的で injection がまったく不要なら、MediaTek の AWUS036AXM / AXML も使えます。ただし、**injection や handshake が関わるなら AXM / AXML は選ばないでください**。これらは本プラットフォームで injection が失敗します（主因は kernel 6.16 以降の mac80211 chanctx のリグレッションで、加えてファームウェアがインジェクションのレートを 1／6 Mbps に固定しており、チップ自体の限界ではありません）。AXER はその逆で、injection が使えて、しかも受信性能が最強です。

9 製品の完全なマトリクスと相互比較をまとめて確認したい場合は、総合評価ページに戻ってください → [`/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

---

## よくある質問（FAQ）

**Q1. AWUS036AXER は Ubuntu 24.04 や Kali で別途ドライバのインストールが必要ですか？**
Ubuntu 24.04（ARM64、kernel 6.17.0-1014-nvidia）では不要です。内蔵の `rtw89_8852bu` ドライバが挿すだけで認識され、コンパイルも DKMS も不要です（firmware `rtw8852b_fw` 0.29.29.5）。本記事のプラットフォームは Kali ではなく Ubuntu のため、Kali 本体は未検証です。Kali でよく使われる airmon-ng、kismet、bettercap、wifite、Wireshark は本プラットフォームで利用できます。kernel が古い場合は内蔵されている保証がないため、先にバージョンを確認してください。

**Q2. AWUS036AXER は monitor mode に対応していますか？受信性能はどのくらいですか？**
対応しており、2.4 GHz でも 5 GHz でも monitor に入れます。自社オフィスで airodump-ng によるチャンネルホッピングスキャンを 60 秒実施したところ、63 個の AP と 12 個の client を検出しました。これは同条件で比較した 9 製品の中で最も高い受信性能です。同じチップの AWUS036AX は別の測定で 14 AP＋4 client でした（2 回の測定は同時実施ではないため、参考値です）。

**Q3. AWUS036AXER でパケットインジェクション（packet injection）はできますか？**
できます。2.4 GHz の `aireplay-ng --test` の応答率は 73%（22/30）で `Injection is working!` と表示され、5 GHz の個別 AP セルフテストも合格しました。自社ネットワークと自社デバイスで handshake の取得と `.22000` への変換まで完了しています。両バンドとも 100% に近い値を求める場合は、本プラットフォームの実測では AWUS036EACS、ACH、ACS のほうが安定しています。自分が所有または許可を得たネットワークでのみ実施してください。

**Q4. AWUS036AXER と AWUS036AX の違いは何ですか？**
どちらも Realtek RTL8832BU を搭載し、`rtw89_8852bu` を使用します。本プラットフォームではモード対応も injection の挙動も同じです。違いはアンテナ調整とゲインによる受信性能です（AXER は 60 秒で 63 AP＋12 client、AX は 14 AP＋4 client）。どちらも内蔵アンテナで RP-SMA はありません。アンテナ仕様は製品ページをご確認ください。

**Q5. AWUS036AXER は AP として使えますか？WPA3 は開けますか？非対応のモードは？**
使えます。2.4 GHz 802.11n と 5 GHz VHT80（VHT-NSS2、351 Mbit）のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は `sae_pwe=0` で iPhone 15 Pro が接続でき（2.4 GHz で実測。5 GHz の WPA3 は未実測）、STA＋AP の同時動作も可能です。ただし `rtw89_8852bu` は active monitor、IBSS、mesh に対応していません。

---

## 6. 関連記事

- 9 種類の ALFA アダプター総合マトリクスと選定一覧表（Monitor・Injection・AP の全比較）→ `/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- 同じチップの AWUS036AX 実測（アンテナ調整が異なる） → `/ja/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- ドライバ不要：in-kernel ドライバで Monitor と AP モードを有効にする → `/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- WPA3-SAE 時代の handshake 取得能力と `sae_pwe` の互換性 → `/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- 関連記事の内部リンクは、確定後に正式な hreflang 対応 URL へ差し替える予定です。上記は zh-TW slug を基にしたプレースホルダーです。 -->

---

*テスト実施：Yopitek（ALFA 代理店）— https://www.yupitek.com ｜ テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ テストデバイス：Apple iPhone 7 Plus（WPA3 のみ iPhone 15 Pro を追加使用）*
