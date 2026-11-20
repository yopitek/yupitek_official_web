---
title: "ALFA AWUS036EACS 単体実機検証：RTL8821CU（BT + WiFi 複合）を ASUS GX10（ARM64 / Ubuntu 24.04）で試した Monitor・Injection・AP・エンドツーエンド handshake"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS（Bluetooth + Wi-Fi 複合）を Ubuntu 24.04 ARM64 で実機検証。ドライバのインストールは不要で、両帯域のインジェクション 100%、Monitor、AP、WPA3-SAE、エンドツーエンドの handshake（79 ACKs、.22000）が通りました。USB 抜き差し時のリスクも記載しています。プラットフォームは ASUS GX10、RTL8821CU です。"
faq:
  - question: "AWUS036EACS は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？"
    answer: "本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8821CU は組み込みの rtw88_8821cu ドライバで、挿すだけで認識され、コンパイルも DKMS も要りません。インターフェース名は wlx に MAC を付けたもので、抜き差ししても変わりません。"
  - question: "AWUS036EACS の monitor mode とパケットインジェクションの性能はどうですか？"
    answer: "monitor は 2.4G・5G ともに安定しており、ほとんどのチャンネルで 300 frames を取り切りました。aireplay-ng --test は両帯域とも 30/30（100%）です。5G でインジェクションする前に、iw reg set US で TW による TX の制限を解除する必要があります。"
  - question: "AWUS036EACS で WPA handshake を取得できますか？"
    answer: "できます。自前の AP と自前の iPhone 7 Plus でエンドツーエンドに検証しました。deauth は 79 ACKs を受信し、完全な M1–M4 を取得して、hcxpcapngtool --all で .22000（784 bytes、EAPOL pairs 2 組）に変換しています。自分が所有する、または許可を得たネットワークに限ります。"
  - question: "AWUS036EACS を挿すと lsusb には見えるのに、wlx ネットワークインターフェースが出てきません。どうすればよいですか？"
    answer: "BT+Wi-Fi 複合デバイスにおける probe の競合状態です。Bluetooth 側はすでに btusb にバインドされており、Wi-Fi 側の rtw88_8821cu が止まっています。実測では、モジュールの再ロードや手動 bind はほとんど効果がなく、確実な対処法は、カードを抜いて別の USB ポートに挿し直すことです。"
  - question: "AWUS036EACS は mesh、IBSS、hcxdumptool に対応していますか？"
    answer: "対応していません。rtw88 の active-monitor、IBSS、mesh、P2P は -95 を返すか、join が機能しません。hcxdumptool 8.x は 2.4 GHz でのみ arm でき（5 GHz は failed to arm）、airodump-ng + aireplay-ng を使ってください。VHT は 80 MHz のみです。mesh / IBSS が必要な場合は AWUS036ACM / ACHM を選んでください。"
draft: false
---

> 検証担当：Yopitek（ALFA Network 台湾代理店）｜検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜テスト端末：自社の iPhone 7 Plus（WPA3 は iPhone 15 Pro でも別途検証）｜検証対象：自社オフィスの Wi-Fi（SSID YUPITEK、2.4G ch5 / 5G ch36、157）。
>
> 本記事は AWUS036EACS 単体の機能と互換性の実機検証です。Monitor / Injection / handshake の取得はすべて、Yopitek の自社設備・自社オフィスの Wi-Fi・自社のテスト用スマートフォンに対して実施しており、販売代理店によるハードウェアの正当な機能検証です。第三者のネットワークは対象とせず、攻撃の操作手順も提供しません。

**要点まとめ（TL;DR）**：AWUS036EACS は GX10 / Ubuntu 24.04（kernel 6.17）でドライバのインストールが不要です。両帯域のインジェクションが 100% で、エンドツーエンドの .22000 取得も通りました（79 ACKs）。ただし BT+Wi-Fi 複合カードのため、抜き差しには注意が必要です。

## 1. このカードと検証プラットフォーム

AWUS036EACS は ALFA の軽量・携帯向け Wi-Fi 5（802.11ac）USB 無線 LAN カードです。チップは Realtek RTL8821CU で、1x1 シングルストリーム、2.4GHz と 5GHz のデュアルバンドに対応し、さらに Bluetooth も内蔵した BT + WiFi 複合デバイスです。本記事ではこのカードを単独で Yopitek の検証台に載せ、ASUS GX10（ARM64）と Ubuntu 24.04 の環境で項目ごとに検収し、お客様が最も気にされる点に答えます。ARM64 でドライバが認識されるか、どのモードに入れるか、性能はどこまで出るか、の 3 点です。

まず位置づけをはっきりさせておきます。これは販売代理店が自社取り扱い製品の互換性と機能の限界を検証したものであり、攻撃の手ほどきではありません。本文中の injection や handshake に関する機能測定は、すべて自社の閉じた環境で自社の機器に対して行ったもので、外部のネットワークに対する操作手順は一切提供しません。

検証プラットフォームと方法は、このシリーズの他の単体記事に準じています。

- 計算プラットフォーム：ASUS GX10（ARM64 / aarch64）
- OS：Ubuntu 24.04 LTS、kernel 6.17.0-1014-nvidia
- ドライバ方針：kernel 組み込み（in-kernel）ドライバを使用。挿すだけで認識され、サードパーティの DKMS モジュールは一切導入しない
- テスト端末：Apple iPhone 7 Plus（WPA3-SAE は iPhone 15 Pro でも再検証）
- 検証環境：自社オフィスの Wi-Fi、SSID YUPITEK、2.4GHz ch5 / 5GHz ch36、ch157
- 安全上のルール：操作は常に `wlx*` インターフェースのみとし、内蔵の外部接続用ラインには触れない。`airmon-ng check kill` は絶対に実行しない（NetworkManager が停止し、GX10 の外部接続が切れるため）

## 2. ハードウェアとドライバ：BT + WiFi 複合デバイスの実態

まず素性を確認します。次の表は、AWUS036EACS が kernel 6.17 上で実際にマウントされた状態です。

| 項目 | 内容 |
|---|---|
| チップ | Realtek RTL8821CU（1x1 シングルストリーム） |
| 世代 | Wi-Fi 5（802.11ac）、2.4 + 5GHz |
| 複合機能 | BT + WiFi 複合デバイス（Bluetooth 内蔵） |
| USB ID | `0bda:c820` |
| ドライバ | `rtw88_8821cu`（in-kernel、USB は kernel 6.2 以降で対応） |
| ファームウェア | 24.11.0（H2C version 12、dmesg で実測） |
| VHT 帯域幅 | 80MHz のみ（160 / 80+80 なし） |

`iw phy` で調べたところ、対応する interface mode は `managed` / `AP` / `AP/VLAN` / `monitor` です（`IBSS` は一覧にあるものの、実測では join が機能しませんでした）。対応帯域は 2.4GHz の ch1–13 と 5GHz の ch36–165（このうち ch52–144 は DFS 帯域）で、cipher には CCMP-256、GCMP-128 / GCMP-256、CMAC が含まれ、AP 側で WPA3 を動かす条件は揃っています。

ドライバについては懸念はありません。RTL8821CU の USB 対応は kernel 6.2 で mainline の `rtw88` に取り込まれ、GX10 の kernel 6.17 には `rtw88_8821cu` がすでに入っているため、挿すだけでロードされ、コンパイルも DKMS も不要です。初期の in-kernel 版では AP mode にバグがありましたが、macid patch（linux-next-20240911 以降）で修正済みで、今回の kernel 6.17 では AP の 3 モードすべてが正常に終了することを確認しました。確認方法は次のとおりです。

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Wi-Fi インターフェースはロード後、`wlan0` ではなく `wlx` + MAC の名前（例：`wlx00c0cab3a52e`）になります。抜き差ししても名前は変わらないため、スクリプトから安定して参照できます。

本当に注意が必要なのは「複合デバイス」である点です。`lsusb -t` で見ると、同じ RTL8821CU の下に複数の USB interface がぶら下がっています。Bluetooth 機能は `btusb` に、Wi-Fi 機能は別に `rtw88_8821cu` にバインドされます。

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

（Bus／Port の番号は抜き差しのたびに変わります。重要なのは、interface 0/1 が `btusb`、interface 2 が Wi-Fi 用の `rtw88_8821cu` という点です。）

**BT + WiFi 複合デバイスの抜き差しリスク（導入前に必読）。** Bluetooth と Wi-Fi が同じ USB デバイスを共有しているため、特定の USB ポートや素早い抜き差しの際に、Bluetooth はすでに `btusb` にバインドされているのに Wi-Fi 側の interface の probe が止まり、`lsusb` には `0bda:c820` が見えるのに `wlx` インターフェースが生成されない、という競合状態が起こることがあります。実測では、`modprobe -r` のあとの再ロードや手動の `bind` はほとんど効果がありませんでした（`bind` は `Operation already in progress` を返します）。確実な対処法は 1 つだけで、カードを抜いて別の USB ポートに挿し直すことです。ポートを変えると列挙がきれいに行われ、`wlx` インターフェースが正常に現れました。これは、非複合の AWUS036ACS（RTL8811AU）と比べてこのカードに追加で必要な運用上の注意点です。あらかじめ知っておけば、カードの故障と誤判断せずに済みます。

## 3. 実測した機能：Monitor / Injection / AP / WPA3

次の表は AWUS036EACS の主要機能の実測まとめで、各項目はいずれも 2026-11-18 に GX10 の実機で実行したものです。

| 機能項目 | 2.4GHz | 5GHz | 実測のポイント |
|---|---|---|---|
| Monitor | ✅ 強い | ✅ 強い | ほとんどのチャンネルで 300 frames を取り切り。コミュニティの #453「ch1 で固まる」は再現せず |
| Injection | ✅ 100%（30/30） | ✅ 100%（30/30） | Power は 2.4G -38.27 / 5G -76.10。このシリーズの ac カードで最強のインジェクション |
| AP | ✅ きれいに終了 | ✅ 802.11a・20 MHz（VHT80 は未測定） | `hostapd` で構築し、iPhone 7 Plus が接続して 4-way を完了 |
| WPA3-SAE（AP 側） | ✅ iPhone が接続 | 未実測 | SAE-only + PMF 必須（`ieee80211w=2`、`sae_pwe=0`） |
| WPA handshake 取得 | — | ✅ エンドツーエンド | M1–M4 が完全、deauth は 79 ACKs、`.22000` に変換 |

Monitor（モニタモード）は 2.4GHz も 5GHz も安定しています。6 つのチャンネルを順にキャプチャしたところ、ほとんどで上限の 300 frames を取り切りました。8821cu については、非常に重要な好材料もあります。rtw88 コミュニティが長く追跡している GitHub #453「8821cu で kernel 6.9 以降かつ STA が up のとき、monitor が ch1 で固まる」は、この GX10 環境では再現せず、5GHz の ch36、ch149、ch157 も 300 フレームを安定して取り切りました。2.4 / 5GHz をまたぐ電波調査やパケット解析をする場合でも、このカードの monitor は安心して使えます。

Injection（パケットインジェクション）の結果は最も目覚ましいものでした。`aireplay-ng --test` で測定すると、2.4GHz も 5GHz も 30/30、100% で、このシリーズの ac カードのなかで最強のインジェクションです（同じ 1x1 の AWUS036ACS は 5G で 96% にとどまります）。台湾ならではの細かい点もあります。regulatory domain が TW のままだと 5GHz の TX はロックされるため、測定前に `iw reg set US` で解除し、測定後に `iw reg set TW` で元に戻してください。

AP については、`hostapd` で 2.4GHz（WPA2）、5GHz（802.11a・20 MHz、VHT80 は未測定）、WPA3-SAE の 3 種類をそれぞれ構築し、いずれも iPhone 7 Plus が接続して 4-way handshake を完了しました。停止時もきれいに終了しています（`AP-DISABLED` / `TERMINATING`）。一部のカードで見られる beacon re-key の問題は出ておらず、2.4G の点では姉妹カードの ACS より安定しています。WPA3 は SAE-only に PMF 必須（`ieee80211w=2`、`sae_pwe=0`）を組み合わせ、iPhone 15 Pro が接続に成功しました。RTL8821CU の AP 側で WPA3-SAE が利用できることを確認しています。

Kali のツールチェーン（プラットフォーム層）も、このカードですべて動作しました。`airmon-ng` は EACS（`rtw88_8821cu`）を検出できますが、やはり `check kill` は使わないでください。`kismet` は本カードをデータソースにして起動に成功し、約 733 KB の `.kismet` ログが出力されました。`bettercap` 2.32 の `wifi.recon on` は正常に動作します（txpower の警告は無視して構いません）。`wifite`（git 3.0.0）は自社の YUPITEK（ch5、PWR 84）を含む 10 台以上の AP を検出しました。この版には `--band` フラグがないため、`-c 1,6,11,36,149,157` でチャンネルを指定する必要があります。`Wireshark` / `tshark` 4.x は monitor の ch6 で実際にキャプチャし、325 frames を解析できました。`macchanger` によるランダム MAC への偽装も使えます。ツール層についてはこのシリーズの他のカードと同じで、差が出るのは前述の injection と monitor のハードウェア性能です。

## 4. エンドツーエンドの handshake：見どころと正直な制限事項

このカードの見どころは、injection と capture をつなげて、一連の使えるチェーンにできる点です。自社の YUPITEK AP と自社の iPhone 7 Plus の間で、チェーン全体を実機で動かしました。自社の iPhone に deauth を送り（injection。実測で 79 個の ACKs を受信し、注入したパケットがクライアントに確かに届いたことを確認）、iPhone が再接続する際に完全な 4-way handshake（M1、M2、M3、M4 が各 1）を取得し、`hcxpcapngtool --all` で hashcat 形式の `.22000`（784 bytes、EAPOL pairs 2 組、RC checked）に変換しました。この流れ全体はカードの機能を検証するためだけのもので、対象は一貫して自社の AP と自社のスマートフォンであり、第三者のネットワークは一切関係ありません。

実務上、記録しておくべき重要な点が 2 つあります。オフィスの ch36 には同名の YUPITEK AP が複数台あるため、キャプチャ時は `--bssid` で絞らず、チャンネル全体を取得してください。そうしないと、iPhone が実際に接続している AP が除外されてしまいます。もう 1 つは、`hcxpcapngtool` がデフォルトでは厳しめなので、`--all` を付けないと `.22000` に変換できないことです。

制限事項もまとめてはっきり述べておきます。

- **active-monitor / IBSS（Ad-hoc）/ Mesh（802.11s）/ Wi-Fi Direct（P2P）には対応していません。** これらのモードは `rtw88` では `-95`（Operation not supported）を返すか、一覧には出ても join が機能しません。ドライバ層の制限であり、回避策はありません。mesh / IBSS の実験が必要なお客様は、MediaTek 系の AWUS036ACM / ACHM に切り替えてください。
- **`hcxdumptool` 8.x は制限があります。** active-monitor が必要で、このカードでは 2.4 GHz でのみ arm でき、5 GHz では `failed to arm interface` になります（シリーズ内の他のカードはすべて `failed to arm interface`）。`airodump-ng` + `aireplay-ng` を使えば問題なく、本カードはインジェクションが 100% のため影響を受けません。
- **VHT は 80MHz のみです。** シングルストリームで 160MHz も 80+80 もなく、位置づけはあくまで軽量・携帯向けのカードであり、スループットを追う役ではありません。
- **VIF は部分対応です。** パッシブ monitor インターフェースを、同一チャンネルの managed インターフェースと並行して動かすこと（ソフトウェア monitor）のみ可能です（実測 100 frames）。独立した 2 つの VIF には対応していません。

## 5. 適した用途と選定

実測を総合すると、AWUS036EACS の位置づけは明快です。デュアルバンドでの Monitor + Injection + エンドツーエンドの handshake 検証が必要で、かつ軽量で Bluetooth 内蔵の携帯向けカードが欲しいなら、これが適した選択肢です。両帯域のインジェクション 100% と、きれいな AP / WPA3 の挙動により、許可された範囲内での無線監査やセキュリティ教育の用途で、AWUS036ACH、AWUS036ACS と並ぶ第一候補グループに入ります。

別のカードをお勧めするのは、次のような場合です。

- **現場で頻繁に抜き差しする、または筐体の USB ポートの品質にばらつきがある場合** → 複合デバイスの probe 競合が悩みの種になりやすいため、非複合の AWUS036ACS（RTL8811AU、同じ 1x1 ac で、Bluetooth という変数がない）を検討してください。
- **mesh / IBSS の実験をしたい場合** → `rtw88` は非対応なので、MediaTek の AWUS036ACM / ACHM に切り替えてください。
- **最強の受信や長距離の monitor を求める場合** → デュアルアンテナの AWUS036ACH、または Wi-Fi 6 の AWUS036AXER が適しています。
- **避けるべきケース**：injection / handshake 用途なら、MT7921 の AWUS036AXM / AXML は選ばないでください。このプラットフォームではインジェクションが失敗します。

ALFA カード 9 モデルの Monitor / Injection / AP / WPA3 を横並びで比較し、完全な選定マトリクスを一度に確認したい方は、総合表に戻ってください：[2026 年最も包括的な実機検証：ASUS GX10 における ALFA 無線 LAN カード 9 モデルの全マトリクス](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## よくある質問（FAQ）

**Q：AWUS036EACS は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？**
本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8821CU は組み込みの rtw88_8821cu ドライバで、挿すだけで認識され、コンパイルも DKMS も要りません。インターフェース名は wlx に MAC を付けたもので、抜き差ししても変わりません。

**Q：AWUS036EACS の monitor mode（モニタモード）とパケットインジェクションの性能はどうですか？**
monitor は 2.4G・5G ともに安定しており、ほとんどのチャンネルで 300 frames を取り切りました。`aireplay-ng --test` は両帯域とも 30/30（100%）です。5G でインジェクションする前に、`iw reg set US` で TW による TX の制限を解除する必要があります。

**Q：AWUS036EACS で WPA handshake（ハンドシェイクパケット）を取得できますか？**
できます。自前の AP と自前の iPhone 7 Plus でエンドツーエンドに検証しました。deauth は 79 ACKs を受信し、完全な M1–M4 を取得して、`hcxpcapngtool --all` で .22000（784 bytes、EAPOL pairs 2 組）に変換しています。自分が所有する、または許可を得たネットワークに限ります。

**Q：AWUS036EACS を挿すと lsusb には見えるのに、wlx ネットワークインターフェースが出てきません。どうすればよいですか？**
BT+Wi-Fi 複合デバイスにおける probe の競合状態です。Bluetooth 側はすでに btusb にバインドされており、Wi-Fi 側の rtw88_8821cu が止まっています。実測では、モジュールの再ロードや手動 bind はほとんど効果がなく、確実な対処法は、カードを抜いて別の USB ポートに挿し直すことです。

**Q：AWUS036EACS は mesh、IBSS、hcxdumptool に対応していますか？**
対応していません。rtw88 の active-monitor、IBSS、mesh、P2P は -95 を返すか、join が機能しません。hcxdumptool 8.x は 2.4 GHz でのみ arm でき（5 GHz は failed to arm）、airodump-ng + aireplay-ng を使ってください。VHT は 80 MHz のみです。mesh / IBSS が必要な場合は AWUS036ACM / ACHM を選んでください。

---

## 6. 関連記事

- [2026 年最も包括的な実機検証：ASUS GX10（ARM64 / Ubuntu 24.04）における ALFA 無線 LAN カード 9 モデルの Monitor・Injection・AP 全マトリクス](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)（Hub 総合表）
- [WPA3-SAE 時代の無線監査：ALFA カード 9 モデルの handshake 取得機能の実機検証](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [ドライバのインストール不要：Ubuntu 24.04 + kernel 6.17 で in-kernel ドライバを使い ALFA 無線 LAN カードの Monitor と AP モードを有効にする](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 同じ rtw88 USB ac カード → [AWUS036ACS 単体実機検証レポート（RTL8811AU）](/ja/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*検証担当：Yopitek（ALFA Network 台湾代理店）— https://www.yupitek.com*
