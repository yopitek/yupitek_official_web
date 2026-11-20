---
title: "AWUS036ACM 個別実機検証：MediaTek MT7612U（mt76x2u）を ASUS GX10 + Ubuntu 24.04（ARM64）で使う場合の Monitor / Injection / AP / mesh 対応レポート"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM（MT7612U）は Ubuntu 24.04 ARM64 でドライバのインストール不要。デュアルバンドのモニターモードと aircrack-ng（Kali で定番）が利用でき、パケットインジェクションは 2.4G で 63–83%、5G で 76%。VIF に対応し、単機での mesh / IBSS 構築も可能です。"
faq:
  - question: "AWUS036ACM は Ubuntu や Kali でドライバのインストールが必要ですか？"
    answer: "不要です。MT7612U は kernel 組み込みの mt76x2u ドライバが処理するため、Ubuntu 24.04（kernel 6.17）では挿すだけで認識され、DKMS も手動のファームウェア導入も要りません。今回の検証プラットフォームは Ubuntu 24.04 ARM64 です。Kali もカーネルが十分に新しければ原則として同様ですが、今回は Kali 実機では検証していません。"
  - question: "AWUS036ACM は monitor mode に入れますか？パケットインジェクションはできますか？成功率はどのくらいですか？"
    answer: "できます。2.4GHz・5GHz のどちらでも monitor mode に入り、正常にキャプチャできます。aireplay-ng によるインジェクションテストでは 2.4GHz が 63–83%、5GHz が 76% で、9 枚のカードの中では中位です。両バンドともインジェクション 100% を求めるなら、Yupitek の実測では AWUS036ACH や AWUS036EACS が適しています。"
  - question: "AWUS036ACM でホットスポットを開きながらインターネットにも接続できますか（VIF）？"
    answer: "できます。STA+AP（上流に接続しつつホットスポットを開く）と AP+monitor（ホットスポットを開きながらモニタリング）のどちらの組み合わせも成立しました。mt76 ドライバのマルチインターフェース同時動作が比較的充実している点です。5GHz ホットスポットは VHT 80 MHz まで開けます。"
  - question: "AWUS036ACM は mesh（802.11s）と IBSS に対応していますか？"
    answer: "単機で構築できます。Ubuntu 24.04 / kernel 6.17 上で、AWUS036ACM は 802.11s mesh と IBSS（Ad-hoc）のインターフェースを作成できます。ただし今回は 2 台目のノードがなく、複数ノード間の接続は検証していないため、「単機で構築可能」としか言えません。"
  - question: "AWUS036ACM で WPA handshake をキャプチャできますか？"
    answer: "できます。自社 AP と自社の iPhone 7 Plus に対してエンドツーエンドの実行に成功しました（deauth、完全な 4-way（M1–M4）のキャプチャ、hcxpcapngtool --all による hashcat .22000 への変換）。自分が所有する、または許可を得たネットワークに限ります。"
draft: false
---

> 本記事は、Yupitek が ALFA AWUS036ACM を新しい Linux プラットフォーム上で検証した、製品の互換性と機能の実測記録です。機種選定の判断材料としてお使いください。
> 検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。すべての数値は、Yupitek が**自社機材・自社オフィスの Wi-Fi**（SSID `YUPITEK`、2.4G ch5 / 5G ch36、ch157）上で、**自社のテスト用スマートフォン**（Apple iPhone 7 Plus。WPA3 のみ iPhone 15 Pro でも再テスト）に対して実測した結果の抜粋です。
> ⚠️ **合法使用と範囲に関する宣言**：Monitor、injection、handshake キャプチャは、自分が所有する、または許可を得たネットワークと機器でのみ実施しています。AP モードは各地域の電波法規に従ってください。本記事はネットワークカード自体の機能・互換性・設定に焦点を当てており、**第三者のネットワークに対するいかなる攻撃操作も扱いません**。

## 要点まとめ（TL;DR）

Yupitek（ALFA Network 台湾代理店）が ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）で実測した結果、AWUS036ACM は両バンドで monitor モードが使え、パケットインジェクションは 2.4G で 63–83%、5G で 76%、AP ホットスポットも両バンドで構築できます（5G は VHT 80 MHz で動作）。

- Ubuntu 24.04（ARM64）ではドライバのインストール不要：MT7612U は kernel 6.17 組み込みの mt76x2u が処理し、挿すだけで認識されます。DKMS は不要です。
- デュアルバンドのモニターモード（monitor mode）が利用可能。パケットインジェクションは 2.4G で 63–83%、5G で 76% で、9 枚のカードの中では中位です。
- 単機で 802.11s mesh と IBSS を構築でき、VIF（STA+AP、AP+monitor）にも対応します。
- WPA handshake キャプチャはエンドツーエンド（完全な 4-way、hashcat `.22000` に変換）まで成功しました。9 枚中 7 枚が完了したうちの 1 枚です。
- 両バンドともインジェクション 100% を求めるなら、AWUS036ACH または AWUS036EACS をお勧めします。

---

## 1. このカードと検証プラットフォーム

AWUS036ACM は ALFA の製品ラインナップにおける MediaTek 製デュアルバンドカードで、チップは MT7612U、Wi-Fi 5（802.11ac）、2T2R の 2 空間ストリーム、2.4GHz / 5GHz のデュアルバンドです。morrownr のリストで Kali 向けの推奨カードとして長く挙げられてきましたが、その理由はスループットではなく、`mt76` 系ドライバが Linux における Monitor、injection、マルチインターフェース同時動作（VIF）に比較的しっかり対応している点にあります。802.11s mesh のような実験的なモードも、本プラットフォームで起動できるのは mt76 陣営だけです（Realtek 製カードは単機の IBSS までしか構築できず、mesh は起動できません）。したがって、このカードを評価するうえで重要なのは速度ではなく、機能面が揃っているか、mt76 の特長が実際に活かせるか、そしてどの項目を正直に「限界」と記すべきか、という点です。

今回も同じ運用シナリオを踏襲しました。GX10 の内蔵ネットワークカード（`wlP9s9`）が外部接続を担当し、AWUS036ACM は USB 外付けでテスト専用とします。Monitor や AP に切り替えても、ホスト自身のネットワークには影響しません。操作したのは ALFA カードに対応する `wlx*` インターフェースのみで、外部接続用の内蔵カードには一切触れていません。

| 項目 | 内容 |
|---|---|
| 型番 | AWUS036ACM |
| チップ | MediaTek MT7612U（Wi-Fi 5 / 802.11ac、2T2R 2 ストリーム） |
| ドライバ | `mt76x2u`（in-kernel、kernel 6.17 組み込み） |
| 世代 / ストリーム | Wi-Fi 5 / 2T2R |
| 備考 | morrownr 推奨の Kali 向けカード |
| プラットフォーム | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| テスト機器 | Apple iPhone 7 Plus（WPA3 のみ iPhone 15 Pro でも測定） |
| テスト環境 | 自社オフィスの Wi-Fi、SSID `YUPITEK`、2.4G ch5 / 5G ch36、ch157 |

> 今回の総括表には AWUS036ACM の USB ID とファームウェアバージョンの欄が登録されていない（「—」）ため、本記事ではこの 2 項目の値を推測で記載しません。以下の機能に関する数値はすべて、総括表の ACM の各行に基づきます。

---

## 2. ハードウェアとドライバ（インストール不要）

このカードは GX10 に挿すだけで認識され、コンパイルも DKMS も不要です。MT7612U は mainline kernel 組み込みの `mt76x2u` ドライバが直接処理するため、out-of-tree のプロジェクトを追加する必要も、ファームウェア blob を手動で導入する必要もありません。ARM64 においては、これが mt76 の最も実用的な利点です。多くのサードパーティ製 Realtek ドライバは aarch64 向けの prebuilt がなく、カーネルバージョンに合わせて自分でコンパイルする必要があります。mt76 は in-kernel なので、kernel をアップグレードしてもドライバの依存関係で行き詰まることがありません。

カードを挿すと、インターフェースは `wlx` + MAC で命名されます（例：`wlxXXXXXXXXXXXX`）。名前は MAC に紐づいていて再挿入しても変わらないため、スクリプトで固定指定するのに便利です。ドライバのバインドとインターフェースの生成は、次の汎用的な確認方法で見られます（マシンによってインターフェース名や phy 番号は異なります）。

```bash
# ALFA カードのインターフェース名を探す (wlx で始まるものだけを選び, 内蔵の wlP9s9 には触れない)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# バインドされているドライバが mt76x2u であることを確認
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# その phy が対応を宣言しているインターフェースモードを一覧表示 (後続でどの機能が使えるかが決まる)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

今回の実測では、`mt76x2u` で利用できるインターフェースモードは Realtek `rtw88` より充実していました。managed / AP / monitor に加えて、IBSS と mesh point も単機で構築できます（第 4 節を参照）。これが、ACM が単機で mesh / IBSS を動かせる土台です。同じプラットフォームの Realtek 製カード（AWUS036ACH など）も単機で IBSS は構築できますが、802.11s mesh と active monitor は本プラットフォームでは起動できません。

---

## 3. 実測した機能：Monitor / Injection / AP / WPA3

まず中核となる機能の総括表（9 カード総括表の第 1 行より）を示し、そのあと項目ごとに掘り下げます。すべての項目を、自社の `YUPITEK` AP と自社の iPhone 7 Plus で実施しました。

| 機能 | 2.4 GHz | 5 GHz | 説明 |
|---|---|---|---|
| Monitor（モニタリング受信） | ✅ | ✅ | 両バンドとも monitor に入れ、正常にキャプチャ可能 |
| Injection（パケットインジェクション） | ✅ 63–83% | ✅ 76% | 標準の injection test によるインジェクション成功率 |
| AP ホットスポット（hostapd） | ✅ | ✅ 80MHz | 5G は VHT 80 MHz まで開設可能 |
| WPA3-SAE（AP 側） | ✅ | 未実測 | WPA3-SAE は 2.4 GHz のみ実測。5 GHz は未実測 |

### 3-1. Monitor（2.4 GHz + 5 GHz）✅

2.4 GHz と 5 GHz のどちらでも正常に monitor に入ってパケットをキャプチャでき、このカードで最も議論の余地がない機能です。2T2R の 2 アンテナカードとして、両バンドの受信モニタリングは安定しており、現場でのチャンネル調査やパケット診断を支えるには十分です。

### 3-2. Injection（パケットインジェクション）✅（中位レベル）

標準の injection test でパケットインジェクションの信頼性を測定したところ、AWUS036ACM は 2.4 GHz で 63–83%、5 GHz で 76% でした。9 枚のカードの中では中位で、Realtek RTL8812AU（AWUS036ACH、両バンド 100%）や RTL8821CU（AWUS036EACS、両バンド 100%）には明らかに及びませんが、機能は一通り揃っており、実用上は十分です。ACM はインジェクションできますが、安定度はクラス最高ではありません。「インジェクション成功率が最優先」というお客様には、第一候補にはなりません（第 5 節の機種選定を参照）。

5 GHz のインジェクション前に、設定上の注意点が 1 つあります。デフォルトの規制ドメインでは一部の UNII バンドでの能動的な送信が制限されるため、テスト前に regulatory domain を送信が許可される設定へ切り替え、テスト後に現地のドメインへ戻す必要があります（`iw reg set US` → テスト → `iw reg set TW`）。これは 5 GHz で正常に送信できるための前提であり、カード本来の性能とは無関係です。

### 3-3. AP ホットスポットと WPA3-SAE ✅

AWUS036ACM は AP として動作し、2.4 GHz と 5 GHz のどちらでも可能で、5 GHz では 80 MHz 帯域幅（VHT80）まで開設できます。AP 側で WPA3-SAE を有効にした場合（2.4 GHz）も、自社のテスト用スマートフォンは正常に接続できました（5 GHz の WPA3 は未実測）。

ここで、同じ mt76 のシングルアンテナ機種 AWUS036ACHM と比較しておく価値があります。ACHM の WPA3 では、hostapd の `sae_pwe` を特別に 0 に設定しないと iPhone 7 Plus が接続できません。AWUS036ACM は今回この制限に遭遇せず、WPA3-SAE はそのまま利用できました。

---

## 4. 発展的な機能：VIF / mesh / IBSS の単機動作と制限

もう一段掘り下げて、handshake、仮想インターフェース（VIF）、active monitor、そして mesh / IBSS を見ていきます。この節は、AWUS036ACM と Realtek 製カードとで差が開くところでもあります。

| 発展項目 | ACM の結果 | 説明 |
|---|---|---|
| WPA handshake キャプチャ | ✅ エンドツーエンド（.22000） | 自社の iPhone 7 Plus に deauth、完全な 4-way M1–M4 をキャプチャし、hashcat `.22000` に変換 |
| VIF（マルチインターフェース同時動作） | ✅ STA+AP / AP+mon | STA+AP または AP+monitor を同時に実行可能 |
| Active monitor | 🟡 設定可能、ACK 未検証 | モードは構築できるが、ACK 応答の動作は未検証 |
| Ad-hoc（IBSS） | 🟡 単機 | 単機でインターフェースを構築可能。相互接続には 2 台目が必要 |
| Mesh（802.11s） | 🟡 単機 | 単機でインターフェースを構築可能。相互接続には 2 台目が必要 |
| Wi-Fi Direct（P2P） | ⬜ 2 台目が必要 | 今回は未テスト |

### 4-1. VIF（仮想インターフェースの同時動作）— ACM の強み ✅

このカードは 2 つの仮想インターフェースを同時に動かせます。今回の実測では、STA+AP（上流に接続しつつホットスポットを開く）と AP+monitor（ホットスポットを開きつつモニタリングする）の両方の組み合わせが成立しました。「接続しながら観測する」「1 枚のカードでクライアントと基地局を兼ねる」といった場面に向いています。これは `mt76` ドライバのマルチインターフェース同時動作が比較的充実している点です。

### 4-2. mesh / IBSS は「単機で可」— mt76 の決定的な違い 🟡

AWUS036ACM は単機で 802.11s mesh と ad-hoc（IBSS）のインターフェースを構築できます。Realtek `rtw88` / `rtw89`（AWUS036ACH、AWUS036AX など）も単機で IBSS は構築できますが、本プラットフォームでは 802.11s mesh に対応していません。したがって 802.11s mesh の実験をするなら、mt76 のカード（ACM / ACHM）には Realtek 製カードにはない出発点があります。

限界は明確にしておきます。今回確認できたのは「単機でインターフェースを構築できる」ことまでです。複数ノード間の完全な相互接続には 2 枚目のカード / 2 台目のノードが必要ですが、まだ実施していません。そのため、ここは ✅ ではなく 🟡（単機）と表記しています。

### 4-3. 正直な機能の限界

- **handshake**：ACM は、インジェクション成功率（2.4G 63–83% / 5G 76%）が Realtek 製カードより低いものの、完全なエンドツーエンドの流れ（自社機器への deauth → 完全な 4-way M1–M4 のキャプチャ → `hcxpcapngtool --all` で hashcat `.22000` に変換）を完了しました。
- **active monitor**：モードは設定できますが、ACK 応答の動作は今回未検証です（🟡 と表記）。関連事項として、プラットフォームレベルでは `hcxdumptool` 8.x が、2.4 GHz の AWUS036EACS を除くすべてのカードで `failed to arm` となりました（active-monitor が必要ですが、本プラットフォームのトライバンド内蔵カードと現行ドライバが対応していません）。そのため ACM の handshake の流れは `airodump-ng` + `aireplay-ng` を使います。
- **Wi-Fi Direct（P2P）**：今回は未テストで、2 台目の機器が必要です。

### 4-4. プラットフォーム運用上の注意（GX10 ARM64、ACM 関連）

1. **自分のネットワークを切断しない**：`airmon-ng check kill` は絶対に実行しないでください（NetworkManager が停止して GX10 がネットワークから切断されます）。操作するのは `wlx*` のみで、外部接続用の内蔵 `wlP9s9` には触れません。
2. **RX stall の解消**：monitor / AP を繰り返し切り替えたあと、突然何もスキャンできなくなった場合は、カードを**一度抜き挿し**すれば復旧します（USB の再列挙。インターフェース名は MAC で決まるため変わりません）。
3. **5 GHz TX のロック解除**：5 GHz の injection を行う前に、正しい規制ドメインを設定して TX 出力のロックを解除し、テスト後は現地のドメインに戻してください。
4. **handshake キャプチャのコツ**：オフィスには同名の AP が複数あることが多いため、実務では単一の `--bssid` に固定せず、チャンネル全体をキャプチャするほうが安定します。変換には `hcxpcapngtool --all` を使います。
5. **ARM64 のツールチェーン**：`aircrack-ng` はソースからのコンパイルが必要です。`wifite` は git の 3.0.0 版を使用します（apt の依存関係の衝突を回避するため）。

プラットフォームレベルの Kali ツール（`airmon-ng`、`kismet`、`bettercap`、`wifite` の git 版、Wireshark / tshark）は、いずれも ACM をデータソースとして問題なく利用できます。唯一の例外は、前述の active-monitor を必要とする `hcxdumptool` です。

---

## 5. 適した利用シーンと機種選定（Hub への導線）

上記の機能を製品の位置づけに当てはめると、AWUS036ACM の役割はかなり明確です。機能のバランスが良く、ドライバのインストールが不要で、mt76 ならではの mesh / IBSS / VIF の強みを持つ Wi-Fi 5 2T2R カードです。では、どのような場面で使うべきでしょうか。

- **mesh（802.11s）実験の第一候補**：この 9 枚のカードの中で、単機で 802.11s mesh インターフェースを構築できるのは mt76 の ACM / ACHM だけです。Realtek `rtw88` / `rtw89` は単機の IBSS は構築できますが、802.11s mesh には対応していません。mesh の実験をするなら、ACM が適切な出発点です。
- **VIF の同時動作が必要な場合**：STA+AP、AP+monitor のどちらも成立するため、1 枚のカードでクライアントと AP を兼ねたり、接続しながらモニタリングしたりする用途に向きます。
- **ドライバ不要の運用を重視する場合**：in-kernel の `mt76x2u` なので、kernel をアップグレードしてもドライバで詰まらず、ARM64 で out-of-tree モジュールをコンパイルする手間も省けます。
- **最適解ではない場面**：中心となる要件が「最高のインジェクション成功率」である場合、ACM のインジェクション（2.4G 63–83% / 5G 76%）はクラス最高ではないため、Realtek の AWUS036EACS / ACH / ACS をお勧めします。最強の受信性能・長距離 monitor を求めるなら、AWUS036AXER / ACH をご検討ください。

同ファミリーの他機種との位置づけの違いは次のとおりです。

| 要件 | 推奨カード | 理由 |
|---|---|---|
| mesh（802.11s）の単機実験 | **AWUS036ACM** / AWUS036ACHM | `mt76` ドライバは単機で 802.11s mesh を構築可能（Realtek は単機 IBSS のみで mesh 非対応） |
| VIF 同時動作（STA+AP / AP+mon） | **AWUS036ACM** | マルチインターフェースの同時動作が成立 |
| 両バンドともインジェクション 100% / エンドツーエンドの handshake | AWUS036EACS、AWUS036ACH、AWUS036ACS | 両バンドのインジェクションが最良で、`.22000` のエンドツーエンドも裏付け済み |
| 最強の受信 / 長距離 monitor | AWUS036AXER、AWUS036ACH | ホッピングでより多くのターゲットをスキャン / デュアルアンテナの高ゲイン |

一言でまとめると、mesh / IBSS を試したい、VIF の同時動作が必要、しかもドライバ不要で運用したいなら、AWUS036ACM はこの中で最も適した mt76 カードです。両バンドともインジェクション 100% を求めるなら、EACS / ACH を選んでください。9 枚のカードの完全な横断比較と機種選定の判断は、[ALFA ワイヤレスカード総合評価 Hub（9 カード総括表）](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。

---

## よくある質問（FAQ）

**Q：AWUS036ACM は Ubuntu や Kali でドライバのインストールが必要ですか？**
不要です。MT7612U は kernel 組み込みの mt76x2u ドライバが処理するため、Ubuntu 24.04（kernel 6.17）では挿すだけで認識され、DKMS も手動のファームウェア導入も要りません。今回の検証プラットフォームは Ubuntu 24.04 ARM64 です。Kali もカーネルが十分に新しければ原則として同様ですが、今回は Kali 実機では検証していません。

**Q：AWUS036ACM は monitor mode に入れますか？パケットインジェクションはできますか？成功率はどのくらいですか？**
できます。2.4GHz・5GHz のどちらでも monitor mode に入り、正常にキャプチャできます。aireplay-ng によるインジェクションテストでは 2.4GHz が 63–83%、5GHz が 76% で、9 枚のカードの中では中位です。両バンドともインジェクション 100% を求めるなら、Yupitek の実測では AWUS036ACH や AWUS036EACS が適しています。

**Q：AWUS036ACM でホットスポットを開きながらインターネットにも接続できますか（VIF）？**
できます。STA+AP（上流に接続しつつホットスポットを開く）と AP+monitor（ホットスポットを開きながらモニタリング）のどちらの組み合わせも成立しました。mt76 ドライバのマルチインターフェース同時動作が比較的充実している点です。5GHz ホットスポットは VHT 80 MHz まで開けます。

**Q：AWUS036ACM は mesh（802.11s）と IBSS に対応していますか？**
単機で構築できます。Ubuntu 24.04 / kernel 6.17 上で、AWUS036ACM は 802.11s mesh と IBSS（Ad-hoc）のインターフェースを作成できます。ただし今回は 2 台目のノードがなく、複数ノード間の接続は検証していないため、「単機で構築可能」としか言えません。

**Q：AWUS036ACM で WPA handshake をキャプチャできますか？**
できます。自社 AP と自社の iPhone 7 Plus に対してエンドツーエンドの実行に成功しました（deauth、完全な 4-way（M1–M4）のキャプチャ、hcxpcapngtool --all による hashcat .22000 への変換）。自分が所有する、または許可を得たネットワークに限ります。

---

## 6. 関連記事

- 9 枚の ALFA カードの完全な機能比較と機種選定の総評 → [ALFA ワイヤレスカード総合評価 Hub（9 カード総括表）](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- ドライバ不要：Ubuntu 24.04 + kernel 6.17 で Monitor / AP を有効化（rtw88 / rtw89 / mt76 実測）（placeholder、リンク準備中）
- WPA3-SAE とエンドツーエンドの handshake キャプチャのステップバイステップ解説（placeholder、リンク準備中）
- 同じ mt76 のシングルアンテナ機種 → AWUS036ACHM 個別実機検証（placeholder、リンク準備中）

---

*検証担当：Yupitek（ALFA Network 台湾代理店）— https://www.yupitek.com ｜ 検証環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ テスト機器：Apple iPhone 7 Plus（WPA3 のみ iPhone 15 Pro でも測定）*
