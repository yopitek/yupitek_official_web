---
title: "AWUS036AXM 単体実測：MediaTek MT7921AU（Wi-Fi 6 2x2）の ASUS GX10 + Ubuntu 24.04（ARM64）における Monitor・AP・WPA3 の対応状況と Injection の制限"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM（mt7921u）を ASUS GX10／Ubuntu 24.04 ARM64 で実測：monitor、AP、WPA3 は利用可能ですが、packet injection は失敗。ペネトレーションテストには非推奨で、純粋な AP と一般接続向けです。"
faq:
  - question: "AWUS036AXM でパケットインジェクション（packet injection）はできますか？"
    answer: "当社のテストプラットフォーム（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）ではできません。aireplay-ng --test は 2.4 GHz でも 5 GHz でも No Answer、Found 0 APs と報告し、deauth も WPA handshake の取得もできません。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションであり、チップが本質的にインジェクション不能というわけではありません。同シリーズの AWUS036AXML も同じ結果でした。インジェクションが必要な場合は、実測で利用可能だった AWUS036EACS、ACH、ACS をお選びください。"
  - question: "AWUS036AXM はペネトレーションテストや Kali での利用に向いていますか？"
    answer: "推奨しません。monitor は使えますが受信が弱く、client や data パケットの取りこぼしが多い上、本プラットフォームでは injection が失敗するため、deauth も handshake の取得もできません。本記事のプラットフォームは Ubuntu 24.04 であり、Kali ディストリビューション自体では検証していません。純粋な AP、一般的な接続、WPA3 アクセスポイントには適しています。ペネトレーションテストには AWUS036EACS、ACH、ACS をお選びください。"
  - question: "AWUS036AXM は Ubuntu 24.04 で別途ドライバのインストールが必要ですか？"
    answer: "不要です。mt7921u ドライバは kernel 6.17 に内蔵されており、挿すだけで認識されます（USB ID 0e8d:7961）。DKMS もコンパイルも不要です。ドライバは IBSS（Ad-hoc）と mesh モードを提供しません。これは設定の問題ではなく制限です。"
  - question: "AWUS036AXM は AP としてアクセスポイントを開けますか？WPA3 に対応していますか？"
    answer: "開けます。これが最も得意な用途です。2.4 GHz（802.11n）と 5 GHz VHT80 のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は 2.4 GHz で利用可能で（MFP: yes。5 GHz の WPA3 は未実測）、古い iPhone では sae_pwe=0 の設定が必要です。STA＋AP の同時動作（VIF）も可能です。今回のテストは 2.4 GHz と 5 GHz のみで、6 GHz と Bluetooth は個別に実測していません。"
  - question: "AWUS036AXM の monitor mode は使いやすいですか？"
    answer: "monitor に入ることはでき、2.4 GHz と 5 GHz のどちらでも beacon を受信できますが、受信が弱く、client と data パケットの量は少なめです。ホッピングではなく単一チャンネルに固定することをお勧めします。広範囲または長距離の監視が必要な場合は、当社のテストでは AWUS036AXER と ACH のほうが明らかに高性能でした。"
draft: false
---

{{< tldr >}}AWUS036AXM は ASUS GX10／Ubuntu 24.04 ARM64 で monitor、AP、WPA3、VIF が利用できますが、packet injection は実測で失敗しました（No Answer／Found 0 APs）。deauth も WPA handshake の取得もできないため、ペネトレーションテストには推奨しません。位置づけは純粋な AP と一般接続用です。{{< /tldr >}}

Yupitek は ALFA Network の台湾代理店です。本記事は AWUS036AXM を 1 枚ずつ実測したレポートで、目的はシンプルです。この Wi-Fi 6 アダプターが **ASUS GX10（ARM64）+ Ubuntu 24.04** で「何ができて、何ができないか」を明確に測定し、購入を検討するお客様がスペック表から推測しなくて済むようにすることです。

まず位置づけをはっきりさせておきます。以下のテストはすべて、Yupitek の自社設備と自社オフィスの Wi-Fi で、自社のテスト用スマートフォンを対象に実施しました。これは代理店による製品の互換性と機能の限界に関するハードウェア検証であり、第三者のネットワークに対する攻撃手法の解説ではありません。本文には外部ネットワークに対する操作手順は一切記載しません。monitor と injection に関する測定は、すべて自社の閉じた環境で、自社デバイスを対象に行っています。

このアダプターについて最初に知っておくべきことが 1 つあります。**本プラットフォームでは injection（注入）が失敗する**ということです。injection や handshake の取得を使う用途の場合は、第四、第五節の選定結論へ直接お進みください。安定した接続や AP の構築が目的であれば、AWUS036AXM は十分に役立つアダプターです。

## 一、アダプターとテストプラットフォーム

AWUS036AXM は MediaTek **MT7921AU** チップを採用し、kernel 内蔵の **mt7921u** ドライバで動作します。仕様は **Wi-Fi 6（802.11ax）、2x2** のデュアル空間ストリームです。同じチップの **AWUS036AXML**（MT7921AUN、Bluetooth 付き）は、本プラットフォームでの Wi-Fi の monitor／AP／injection の挙動がまったく同じで、2 製品は相互に参照できます。違いは、AXML には Bluetooth があり、本機での実測で 6 GHz band も利用できたのに対し、AXM の 6 GHz と Bluetooth は今回個別に実測していない点です。

- **計算プラットフォーム**：ASUS GX10（ARM64 / aarch64）
- **OS**：Ubuntu 24.04 LTS
- **カーネルバージョン**：kernel 6.17.0-1014-nvidia
- **テストデバイス**：Apple iPhone 7 Plus（WPA3-SAE と VIF は iPhone 15 Pro でも再テスト）
- **テスト環境**：自社オフィスの Wi-Fi、SSID `YUPITEK`、2.4GHz ch5 / 5GHz ch36
- **テスト期間**：2026-11-16 から 2026-11-18 まで実機で測定

## 二、ハードウェアとドライバ（挿すだけで使用可能）

mt7921u ドライバはすでに kernel 6.17 に内蔵されており、AWUS036AXM は GX10 に挿すだけで認識されます。DKMS も、サードパーティ製ドライバの自前コンパイルも不要です。これは、この世代の MediaTek アダプターが ARM64 で最も手間がかからない点です。

| 項目 | 内容 |
|---|---|
| 型番 | AWUS036AXM |
| チップ | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| ドライバ（in-kernel） | `mt7921u` |
| 世代 / ストリーム | Wi-Fi 6（802.11ax）/ 2x2 |
| インターフェースモード | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| 非対応モード | IBSS（Ad-hoc）、Mesh（802.11s） |

アダプターが認識されているか確認します。

```bash
lsusb | grep 0e8d:7961
```

想定される出力は `ID 0e8d:7961 MediaTek Inc. Wireless_Device` です。なお、`iw phy info` が列挙するインターフェースモードに IBSS と mesh point は含まれません。これは mt7921u 本来の制限であり、設定の問題ではありません。mesh / IBSS を使うシーンでは、`mt76` の AWUS036ACM / ACHM を使用してください。

## 三、実測した機能：Monitor / AP / WPA3、そして Injection 失敗についての正直な説明

まず主要機能のマトリクスを示し、その後で項目ごとに説明します。

| 機能 | 2.4 GHz | 5 GHz | 実測メモ |
|---|---|---|---|
| Monitor（監視） | ✅ 利用可（受信は弱め） | ✅ 利用可（受信は弱め） | beacon は受信できるが、client / data frame の量は少ない |
| **Injection（注入）** | ❌ **本プラットフォームで失敗** | ❌ **本プラットフォームで失敗** | 根本原因は kernel 6.16+ mac80211 chanctx のリグレッション（チップ本来の制限ではない） |
| AP（アクセスポイント） | ✅ 802.11n（HT20）を含む | ✅ VHT 80 MHz | iPhone 7 Plus が実機で接続、authorized |
| WPA3-SAE | ✅ | 未実測 | MFP: yes、`sae_pwe=0` で古い iPhone と互換。2.4 GHz のみ実測 |
| VIF（STA + AP） | ✅ | ✅ | 1 枚で 2 役、STA 側の ping 17 ms |

### Monitor（監視）✅ 利用可、ただし受信は弱め

2.4GHz と 5GHz のどちらでも monitor モードに入れ、beacon も受信できます。ただし正直に言うと、AWUS036AXM の受信は、同じプラットフォームの AWUS036ACM / ACHM と比べて明らかに弱く、実測の frame 数が少なく、client や data パケットの取得量も多くありません。実用上は、ホッピングせずに**単一チャンネルに固定**して記録することをお勧めします。そのほうが取得結果が安定します。

もう 1 つ見誤りやすい点があります。monitor モードでは `txpower` が 3 dBm と報告されますが、これは報告上の見かけの値です（ハードウェアの実際の TX は約 20 dBm で、`txpower_sku` により確認済み）。送信が本当にそこまで抑えられているわけではありません。AWUS036AXM はそもそも広範囲の記録を想定した設計ではありません。広く、遠くまでスキャンしたい場合は、アンテナ調整がより優れホッピングも積極的な AWUS036AXER、またはデュアルアンテナ高ゲインの AWUS036ACH をご検討ください。この 2 製品は同じプラットフォームで monitor の受信が明らかに強力です。

### AP（アクセスポイント）✅ AXM が最も得意とする用途

2.4GHz で AP を開く場合、802.11n（HT20）を同時に有効にでき、iPhone 7 Plus の接続は MCS 7、authorized にネゴシエートされました。5GHz は **VHT 80 MHz** まで設定でき、iPhone の接続は VHT-NSS2、authorized でした。2.4G でも 5G でも、AWUS036AXM のアクセスポイントとしての動作は安定しており、本プラットフォームで最も価値のある機能です。

### WPA3-SAE ✅

AP 側で WPA3-SAE を有効にし、iPhone 7 Plus が接続できました。MFP（Management Frame Protection）は `yes` と表示されます。実用上の注意点として、`sae_pwe=0` に設定すると iPhone 7 Plus のような古めのデバイスと互換性が保てます。`sae_pwe=2` にすると、古い iPhone は接続できない場合があります。

### VIF（STA + AP の 1 枚 2 役）✅

AWUS036AXM は、STA として既存の Wi-Fi に接続しながら、AP の仮想インターフェース（VIF）も開けます。実測では、iPhone 15 Pro が AP VIF に接続している間、STA 側から `YUPITEK` への ping は約 17 ms で、接続は正常でした。「1 枚のアダプターでネットに接続しつつ、アクセスポイントも共有する」という用途には利用可能です。

### Injection（注入）❌ 本プラットフォームで失敗 —— 選定の分かれ目

これは AWUS036AXM について最も重要で、正直に伝えなければならない項目です。実測した `aireplay-ng --test` の出力は次のとおりです。

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

2.4GHz でも 5GHz でも同様に失敗しました。よくある誤解を先に整理しておきます。monitor モードで `iw` が報告する txpower が 3 dBm しかないのは**報告上の見かけの値**で、ハードウェアの実際の TX は約 20–23 dBm です（`txpower_sku` により確認済み）。送信電力が抑えられているわけではなく、これが失敗の主因ではありません。真の根本原因は**ソフトウェア層**にあります。kernel 6.16 以降、mac80211 の channel context（chanctx）にリグレッションが発生し、stock ドライバが active monitor／injection の状況でターゲットの beacon を受信できなくなります。その結果、`aireplay-ng` は `No Answer` と判定します。これは **kernel 側のリグレッションであり、MT7921 チップが本質的に injection できないわけではありません**。この現象は morrownr/USB-WiFi の issue #387 に記録されており、根本原因の分析は morrownr/mt76 の issue #18 にあります。

補足すると、コミュニティの実測では、同じ型番で git／パッチ適用済みのドライバを使うと、active monitor と injection が実際に動作するとのことです。ただしその場合でも、MT7921 の firmware は injection を **1 Mbps／6 Mbps の基本レートに固定**しており、HT／VHT レートでの injection はできません。つまり、kernel のリグレッションを回避したとしても、このアダプターの injection 機能には制約が残ります。同じ aircrack-ng、同じ GX10 プラットフォームで injection が使える Realtek の rtw89 アダプター（AWUS036AX／AXER など）と比べると、MT7921 の経路は **stock kernel 6.17** では通りません。

もう一度強調しますが、これは個体の故障でも設定ミスでもありません。同じチップの AWUS036AXML もまったく同じ挙動で、stock kernel 6.17 ではパラメータの変更、チャンネルの変更、regulatory domain の変更のいずれでも解決しません。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションに、firmware による injection レート固定が加わったものであり、チップのハードウェア欠陥ではありません。直接的な結果として、AWUS036AXM は本プラットフォームで **deauth も、能動的な WPA handshake の取得もできません**。これらの機能が必要な場合は、次節の Realtek / mt76x 系のアダプターを使用してください。

高度な機能は次のとおりです。

| 高度な機能 | 状態 | 説明 |
|---|---|---|
| WPA handshake 取得 | ❌ | injection の失敗により利用不可。ACM / ACHM / ACH / ACS / EACS を使用 |
| VIF（STA + AP） | ✅ | 1 枚 2 役が可能 |
| Active monitor | 🟡 | `set monitor active` は受理されるが、ACK は未検証 |
| Ad-hoc（IBSS） | N/A | mt7921u は非対応 |
| Mesh（802.11s） | N/A | mt7921u は非対応 |
| Wi-Fi Direct（P2P） | ⬜ | ドライバは対応を宣言しているが、2 台目のデバイスがなく未検証 |

### 操作上の安全性と実用上の注意

GX10 でこのアダプターを操作する際の実用上のポイントです。先に知っておくと失敗を避けられます。

- **自分のネットワークを切断しない**：`airmon-ng check kill` は絶対に実行しないでください。NetworkManager が停止し、GX10 全体がネットワークから切断されます。操作対象は外付けの `wlx*` インターフェースのみとし、GX10 内蔵の外部接続用メイン回線には触れないでください。
- **AP のパスワードは 8 文字以上**：そうでないと hostapd が `invalid WPA passphrase length` を返して起動しません。
- **スマートフォンから SSID が見えないとき**：アダプターを一度抜き差ししてリセットするか、スマートフォンを近づければ解消します（monitor モードで報告される 3 dBm は見かけの値で実際の電力ではなく、主因ではありません）。
- **RX stall の対処**：monitor / AP を繰り返し切り替えた後に突然何もスキャンできなくなった場合は、多くの場合 RX stall です。アダプターを一度抜き差しすれば復旧します（インターフェース名は MAC で決まるため変わりません）。

## 四、適した用途と適さない用途

ここまでの測定結果をひとことにまとめると、AWUS036AXM は優れた「接続 / AP」用アダプターですが、「injection / 攻防」用アダプターではありません。

**適した用途**

- 安定した日常の接続（Wi-Fi 6、2x2）
- 2.4GHz / 5GHz の AP アクセスポイントの構築（802.11n と VHT80 を含む）
- WPA3-SAE の互換性検証と展開テスト
- STA + AP の 1 枚 2 役（VIF）
- beacon を受動的に記録する軽量な monitor 用途

**適さない用途（避けるべき用途）**

- injection / deauth
- WPA handshake の取得、能動的な攻防演習
- IBSS（Ad-hoc）や Mesh が必要な実験
- 長距離で高感度な、広範囲の monitor 記録が必要な用途

**最も重要な注意点**：用途が **injection または handshake** の場合、**AWUS036AXM（または同じチップの AWUS036AXML）は選ばないでください**。MT7921 は ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）というこのプラットフォームで injection に失敗します。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションであり、チップが本質的に injection できないわけではありません。ただし 2026-11-18 時点の stock 環境ではパラメータ調整では解決できないため、「純粋な接続 / 純粋な AP」のシーン専用としてお使いください。

## 五、選定の目安（純粋な AP／接続向け）

| 用途 | おすすめ | 理由 |
|---|---|---|
| 純粋な AP / 安定した接続（injection 不要） | **AWUS036AXM** / AWUS036AXML | MediaTek は接続が安定しており、AP と WPA3 の動作が良好 |
| ペネトレーションテスト（injection + handshake） | AWUS036EACS / AWUS036ACH / AWUS036ACS | 両バンドで injection が利用可能で、エンドツーエンドの handshake が動作する |
| 最強の受信 / 長距離 monitor | AWUS036AXER / AWUS036ACH | AXER はホッピングスキャンが積極的、ACH はデュアルアンテナ高ゲイン |
| Wi-Fi 6 + AP で injection も必要 | AWUS036AX / AWUS036AXER | 2x2 VHT80、AP が安定し injection も利用可能 |
| mesh / IBSS の実験 | AWUS036ACM / AWUS036ACHM | `mt76` ドライバで単体構築が可能 |

ひとことで言うと、安定した接続や AP が目的なら AWUS036AXM は十分に役立ちます。injection や handshake が関わるなら、Realtek の EACS / ACH / ACS に切り替えてください。ARM64 でのこのシリーズの完全な比較と、9 製品の Monitor / Injection / AP / WPA3 の全マトリクスは、総合ハブページをご覧ください。

- [2026 年最も詳細な実測：9 種類の ALFA ワイヤレスアダプターを ASUS GX10（ARM64 / Ubuntu 24.04）で全マトリクス比較](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

改めて位置づけを強調します。本記事の monitor / injection に関する測定はすべて、Yupitek の自社の閉じた環境で、自社のテストデバイスを対象に行いました。目的は製品の機能と互換性の限界を検証することであり、第三者のネットワークに対して上記の操作を行うことは、提供も推奨もしていません。

## よくある質問（FAQ）

**Q1. AWUS036AXM でパケットインジェクション（packet injection）はできますか？**
当社のテストプラットフォーム（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）ではできません。`aireplay-ng --test` は 2.4 GHz でも 5 GHz でも `No Answer`、`Found 0 APs` と報告し、deauth も WPA handshake の取得もできません。根本原因は kernel 6.16+ の mac80211 chanctx のリグレッションであり、チップが本質的にインジェクション不能というわけではありません。同シリーズの AWUS036AXML も同じ結果でした。インジェクションが必要な場合は、実測で利用可能だった AWUS036EACS、ACH、ACS をお選びください。

**Q2. AWUS036AXM はペネトレーションテストや Kali での利用に向いていますか？**
推奨しません。monitor は使えますが受信が弱く、client や data パケットの取りこぼしが多い上、本プラットフォームでは injection が失敗するため、deauth も handshake の取得もできません。本記事のプラットフォームは Ubuntu 24.04 であり、Kali ディストリビューション自体では検証していません。純粋な AP、一般的な接続、WPA3 アクセスポイントには適しています。ペネトレーションテストには AWUS036EACS、ACH、ACS をお選びください。

**Q3. AWUS036AXM は Ubuntu 24.04 で別途ドライバのインストールが必要ですか？**
不要です。mt7921u ドライバは kernel 6.17 に内蔵されており、挿すだけで認識されます（USB ID `0e8d:7961`）。DKMS もコンパイルも不要です。ドライバは IBSS（Ad-hoc）と mesh モードを提供しません。これは設定の問題ではなく制限です。

**Q4. AWUS036AXM は AP としてアクセスポイントを開けますか？WPA3 に対応していますか？**
開けます。これが最も得意な用途です。2.4 GHz（802.11n）と 5 GHz VHT80 のどちらでも iPhone が接続して authorized になりました。WPA3-SAE は 2.4 GHz で利用可能で（`MFP: yes`。5 GHz の WPA3 は未実測）、古い iPhone では `sae_pwe=0` の設定が必要です。STA＋AP の同時動作（VIF）も可能です。今回のテストは 2.4 GHz と 5 GHz のみで、6 GHz と Bluetooth は個別に実測していません。

**Q5. AWUS036AXM の monitor mode は使いやすいですか？**
monitor に入ることはでき、2.4 GHz と 5 GHz のどちらでも beacon を受信できますが、受信が弱く、client と data パケットの量は少なめです。ホッピングではなく単一チャンネルに固定することをお勧めします。広範囲または長距離の監視が必要な場合は、当社のテストでは AWUS036AXER と ACH のほうが明らかに高性能でした。

## 六、関連記事

以下の関連記事は順次公開予定です（リンクは準備中）。

- 《ドライバ不要：Ubuntu（ARM64）で Monitor と AP モードを有効にする》 → [`/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE の対応状況と handshake の実務（自社環境で検証）》 → [`/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 《AWUS036AXML 単体実測（同じ MT7921 チップ + BT）》 →（準備中）
- 《なぜ mt7921u は kernel 6.16 以降で injection できないのか：chanctx リグレッションとファームウェアのレート固定の解説》 →（準備中）

---

*テスト実施：Yupitek（ALFA 代理店）｜ プラットフォーム：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ テストデバイス：Apple iPhone 7 Plus（WPA3 / VIF は iPhone 15 Pro でも測定）*
