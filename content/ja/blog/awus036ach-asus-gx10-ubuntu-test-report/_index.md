---
title: "AWUS036ACH 単体実機検証：Realtek RTL8812AU デュアルアンテナ AC1200 を ASUS GX10（ARM64 / Ubuntu 24.04）で使う場合の Monitor・Injection・AP・WPA3 総合テストレポート"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH（RTL8812AU）は Ubuntu 24.04 / kernel 6.17 で DKMS のインストール不要。デュアルバンドのモニターモードが利用でき、パケットインジェクションは 100%、エンドツーエンドの WPA handshake（.22000）も実証済みです。5G 受信のフリーズなどの制限事項も併記します。"
faq:
  - question: "AWUS036ACH は Kali や Ubuntu でドライバのインストールが必要ですか？"
    answer: "カーネルのバージョンによります。Linux カーネル 6.13 以上（今回の実測は Ubuntu 24.04 / kernel 6.17）では rtw88_8812au ドライバが組み込まれており、挿すだけで認識され、コンパイルも DKMS も不要です。カーネルが 6.13 未満の場合のみ、DKMS で lwfinger/rtw88 を別途インストールする必要があります。Kali では先に uname -r でカーネルバージョンを確認してください。今回は Kali 実機では検証していません。"
  - question: "AWUS036ACH の monitor mode とパケットインジェクションの性能はどうですか？"
    answer: "2.4GHz・5GHz のどちらでも monitor mode に入れます。aireplay-ng による AP ごとの指向性インジェクションは、2.4GHz（4 台の AP に対して）も 5GHz（YUPITEK ch36 に対して）も 30/30 = 100% でした。5GHz のインジェクション前には、規制ドメインを送信が許可される設定にしておく必要があります（例：iw reg set US）。デフォルトの country 00 では 5GHz は送信が禁止されており、インジェクションが送出されません。"
  - question: "AWUS036ACH で WPA handshake をキャプチャできますか？"
    answer: "できます。しかもエンドツーエンドで実証済みです。両バンドともインジェクションは 100% で、2026-11-19 の追加テストでは、自社の iPhone 15 Pro、5GHz ch36 で完全な 4-way ハンドシェイクをキャプチャし、hcxpcapngtool で 47 件の hashcat .22000 hashline に変換しました。自分が所有する、または許可を得たネットワークに限ります。"
  - question: "AWUS036ACH で WPA3 ホットスポットを開くと、iPhone 7 Plus が接続できない場合は？"
    answer: "hostapd で sae_pwe=0 を設定し、ieee80211w=2 と組み合わせると iPhone 7 Plus が接続できます。sae_pwe=2 では接続できません。同じ設定は AWUS036ACHM でも重要です。"
  - question: "AWUS036ACH の 5GHz 受信が突然フリーズする（0 パケットしか取得できない）場合は？"
    answer: "これは rtw88_8812au の既知の現象です。モードの切り替えや規制ドメインの変更を繰り返すと 5GHz 受信がフリーズすることがあり、ソフトウェアでは復旧できず、物理的に抜き挿しするか再起動するしかありません。5GHz のテスト前にカードを挿し直し、5GHz の項目を優先して完了させることをお勧めします。"
draft: false
---

> 検証担当：Yupitek（ALFA Network 台湾代理店）｜検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜テスト機器：自社の Apple iPhone 7 Plus｜テスト対象：自社オフィスの Wi-Fi（SSID `YUPITEK`、2.4G ch5 / 5G ch36、157）｜テスト日：2026-11-18。
>
> 本記事は、代理店による製品の互換性と機能の限界についてのハードウェア検証です。Monitor / Injection / AP / handshake の測定はすべて、Yupitek が所有する機材と自社オフィスの Wi-Fi 上で、自社のテスト用スマートフォンに対して実施したもので、第三者のネットワークは対象とせず、外部ネットワークへの攻撃手順も提供しません。本文中の数値はすべて実機で測定した数字と状態であり、スペックシートからの推測ではありません。

## 要点まとめ（TL;DR）

ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）での実測では、AWUS036ACH は両バンドで monitor モードが使え、AP ごとのパケットインジェクションは両バンドとも 30/30 = 100%、AP ホットスポットも両バンドで構築できます（純 802.11g / 純 802.11a）。

- kernel 6.13 以上では DKMS 不要（今回は Ubuntu 24.04 / kernel 6.17）。rtw88_8812au が組み込まれており、挿すだけで認識されます。
- デュアルバンドのモニターモード（monitor mode）が利用可能。両バンドとも AP ごとのパケットインジェクションは 30/30 = 100% でした。
- エンドツーエンドの WPA handshake を実証済み：2026-11-19 の追加テストで、自社の iPhone 15 Pro、5G ch36 で完全な 4-way をキャプチャし、47 件の .22000 hashline に変換しました。
- 5GHz の受信がフリーズすることがあり、物理的な抜き挿しか再起動でしか復旧できません。
- 単機での IBSS 構築は可能ですが、802.11s mesh、active monitor、Wi-Fi Direct（P2P）には対応していません。

## 1. このカードと検証プラットフォーム

AWUS036ACH は、ALFA Network が「デュアルアンテナ・高ゲイン」と位置づける USB ワイヤレスカードで、Realtek RTL8812AU チップを採用し、スペックは Wi-Fi 5（802.11ac）、2T2R、デュアルバンド AC1200 です。同シリーズのシングルアンテナ機種 AWUS036ACHM（MediaTek MT7610U、AC600）と比べると、ACH は 2 本の外付け高ゲインアンテナによって、より良い受信と、より安定した injection 性能を得ており、お客様から「長距離 monitor」や「両バンドでのインジェクション」について問い合わせがあった際の定番の候補です。

今回の検証プラットフォームと条件は次のとおりです。

- 演算プラットフォーム：ASUS GX10（ARM64 / aarch64）
- OS：Ubuntu 24.04 LTS
- カーネルバージョン：kernel 6.17.0-1014-nvidia
- テスト機器：Apple iPhone 7 Plus（2.4G / 5G / WPA3 はすべてこの機種で実測）
- テスト環境：自社オフィスの Wi-Fi、SSID `YUPITEK`（2.4GHz ch5 / 5GHz ch36、ch157）
- テスト日：2026-11-18 に実機で測定

全体を通じて、操作したのは ALFA カードに対応する `wlx*` インターフェースのみで、GX10 の外部接続用の内蔵ネットワークカードには触れていません。また `airmon-ng check kill` も実行していません（このコマンドは NetworkManager を停止させ、ホストが切断されるため）。

## 2. ハードウェアとドライバ（チップ / USB ID / in-kernel でインストール不要）

| 項目 | スペック |
|---|---|
| 型番 | AWUS036ACH |
| チップ | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| ドライバ | `rtw88_8812au`（kernel 組み込み、mainline ≥ 6.13） |
| ファームウェア | `rtw88/rtw8812a_fw.bin`（システムに同梱） |
| 世代 / ストリーム | Wi-Fi 5（802.11ac）/ 2T2R |
| 帯域幅クラス | デュアルバンド AC1200 |
| アンテナ | デュアルアンテナ・高ゲイン（外付け） |
| USB インターフェース | USB 3.0（実測の列挙は 5000M） |

ACH は GX10 の 6.17 kernel 上で、文字どおりのプラグアンドプレイです。`lsusb` が `0bda:8812` を認識し、ドライバ `rtw88_8812au` が自動的にバインドされ、ファームウェア `rtw8812a_fw.bin` はシステムに同梱済みで、コンパイルも DKMS も不要です。この点は ARM64 環境では特に重要です。古い out-of-tree の Realtek ドライバの多くは aarch64 ではソースからのコンパイルが必要でしたが、morrownr/USB-WiFi と aircrack-ng/rtl8812au という 2 つの老舗プロジェクトは、現在どちらもこの組み込みドライバへ誘導しており、バグ報告は lwfinger/rtw88 に集約されています。したがって kernel ≥ 6.13（GX10 の 6.17 を含む）のユーザーは、もうサードパーティの DKMS に手を出す必要はありません。DKMS で `lwfinger/rtw88` を別途インストールする必要があるのは、古い kernel（< 6.13）のときだけです。この上流プロジェクトは現在も活発にメンテナンスされており（最新の commit は 2026-10-24、内容には 8812A の Bluetooth 1T1R 修正を含みます）、このチップのメインラインでの対応が継続的に更新されていることを示しています。更新が止まった古いドライバではありません。

ハードウェア接続には 1 つ注意点があります。ACH は USB-A のオスコネクタなので、USB-C→A 変換アダプタを使って GX10 の USB-C ポートに直接挿し、USB 3.0 で動作させてください（列挙では 5000M と表示されます）。キーボード・マウス用の USB 2.0 ハブ経由で接続すると速度が制限され、USB3 での動作を測定できません。

インターフェースモードについては、`iw phy` は IBSS / managed / AP / AP-VLAN / monitor に対応と報告しますが、mesh、P2P、active-monitor はありません。この境界線が、第 4 節の一部の制限を直接決めています。

## 3. 実測した機能：Monitor / Injection / AP / WPA3

| 機能 | 2.4 GHz | 5 GHz | 実測データ |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames；5G ch36/149/157 = 260/137/127 frames |
| Injection（ブロードキャスト探索） | ✅ | ✅ | `aireplay-ng --test` の broadcast probe は両バンドとも Injection is working を返した |
| Injection（AP ごとの指向性） | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G は 4 台の AP（YUPITEK を含む）に対して、5G は YUPITEK ch36 に対して |
| AP ホットスポット（iPhone 7 Plus） | ✅ 純粋な 802.11g | ✅ 純粋な 802.11a（ch36） | 4-way handshake が完了し、初回から接続できた |
| WPA3-SAE AP | ✅（`sae_pwe=0`） | 未実測 | `ieee80211w=2` と組み合わせ、iPhone 7 Plus が接続できた（2.4 GHz のみ実測） |

**Monitor**：2.4GHz では ch1 / ch6 / ch11 でそれぞれ 92 / 214 / 71 フレームを取得し、5GHz では ch36 / ch149 / ch157 で 260 / 137 / 127 フレームを取得しました。両バンドとも monitor は正常で、5GHz の取得量は 2.4GHz より多いほどであり（ch36 で 260 フレーム）、デュアルアンテナ・高ゲインという位置づけと一致します。

**Injection**：ここは ACH の強みです。2.4GHz では `aireplay-ng --test` でまず broadcast probe を行い（Injection is working、Found 4 APs と報告）、続いて AP ごとの指向性テストを行ったところ、YUPITEK を含む 4 台の AP すべてで応答率は 30/30 = 100%、min/avg/max RTT は約 4.9 / 39.2 / 99.0 ms、Power は約 -47 でした。デュアルアンテナの ACH の 2.4G injection は、シングルアンテナの ACHM より明らかに安定しています。実運用では `--ignore-negative-one` を付けるのを忘れないでください。これは lwfinger/rtw88 #453 の既知の現象で、STA インターフェースが開いていると monitor channel が `-1` を報告することがあり、このフラグがないとインジェクション失敗と誤判定されます。また、上流の記録によれば、高負荷のインジェクション時に組み込みドライバで USB reset が起きることがありますが、今回の約 90 秒の測定では観測されませんでした。5GHz で YUPITEK（ch36）に対して AP ごとの指向性テストを行った場合も同様に 30/30 = 100% で、平均 RTT は 13.6 ms、Power は -69.1 でした。これは「カードを挿し直した直後 + regdomain を TX 可能な規制に設定」という前提で測定した結果です（詳細は第 4 節の 5G に関する注意事項を参照）。

**AP ホットスポット**：hostapd で AP を立てました。2.4GHz は純粋な 802.11g（`ieee80211n=0`）、5GHz は純粋な 802.11a（ch36）で、iPhone 7 Plus は両バンドとも初回から接続でき、association の失敗はありませんでした。ログでは authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED の 4 ステップがすべて確認できます。実測上の経験則として、ACH は「802.11n を無効にし、純粋な g / 純粋な a」の設定で最もきれいに接続できます。

**WPA3-SAE**：SAE-only の AP を開く際の重要なパラメータは `sae_pwe=0`（hunting-and-pecking）と `ieee80211w=2` の組み合わせで、これで iPhone 7 Plus が接続できます。`sae_pwe=2` では接続できません。これは同シリーズの ACHM で遭遇したのと同じ互換性の落とし穴です。

## 4. 発展的な機能と handshake：実現可能な範囲と正直な制限

| 発展的な機能 | 結果 | 説明 / 証拠 |
|---|---|---|
| VIF（STA + monitor を同時に） | ✅ 実測で動作 | メインのインターフェース managed と `mon9`（monitor）が同時に up し、monitor VIF は 8 秒で 100 フレームを取得 |
| WPA handshake キャプチャ | ✅ エンドツーエンド（.22000）実証済み | 両バンドのインジェクション 100%。2026-11-19 の追加テストで 5G ch36 の完全な 4-way をキャプチャし、hcxpcapngtool で 47 件の `.22000` hashline に変換 |
| macchanger（MAC の変更） | ✅ | ランダム MAC の設定と復元がどちらも正常（先に `ip link down` が必要） |
| Ad-hoc（IBSS） | 🟡 単機 | 単機で `Joined IBSS` に成功。peer link は 2 台目の機器がないため未テスト |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh（802.11s） | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct（P2P） | ❌ | `Operation not supported (-95)` |

**handshake キャプチャ能力は明確にしておきます**：ACH の両バンドの injection はどちらも 100% で、この injection こそが「自社のテスト用スマートフォンへ deauth → 完全な 4-way（M1–M4）をキャプチャ → hcxpcapngtool で hashcat `.22000` に変換」というエンドツーエンドのワークフローの起点です。2026-11-19 の追加テストで、自社の iPhone 15 Pro、5GHz ch36 で完全な 4-way ハンドシェイクをキャプチャし、hcxpcapngtool で 47 件の `.22000` hashline に変換できたため、ACH のエンドツーエンドの handshake キャプチャは実証済みです。当社の 9 機種の総括表のうち、エンドツーエンド（`.22000`）が実証済みなのは 9 機種中 7 機種で、AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX、AWUS036AXER です。すべてのキャプチャは、自分が所有する、または許可を得たネットワークに限ります。

**VIF**：`iw phy` のフラグには interface combinations are not supported と書かれていますが、実機ではメインの managed インターフェースと、別途開いた monitor インターフェース `mon9` を同時に up にでき、`mon9` は 8 秒で 100 フレームを取得しました。つまり「ネットに接続しながらモニタリング」は ACH で動作します。ただし注意が必要です。この組み合わせは phy が保証しているものではないため、長時間または高負荷の場面では mt76 系（ACM / ACHM）の利用をお勧めします。

**特に明記すべき 3 つの制限：**

1. **Active monitor、Mesh（802.11s）、Wi-Fi Direct（P2P）には非対応**：3 つとも実測ではすべて `Operation not supported (-95)` が返りました。これら 3 つの機能が必要な場合は、mt76 系のカード（ACM / ACHM の phy は mesh / P2P / active-monitor を宣言しています）を使ってください。
2. **5G RX のフリーズ（`rtw88_8812au` の既知の現象）**：カードを挿した直後は 5G の monitor / injection は正常ですが、モードの切り替えや regdomain の変更を繰り返すと、5G 受信がフリーズすることがあり（0 パケットしか取得できない）、ソフトウェアでは復旧できず、物理的に抜き挿しするか再起動するしかありません。5G のテストの前に一度抜き挿しし、5G の項目を優先して完了させることをお勧めします。ここで、5G の injection を送出できる前提も補足します。デフォルトの `country 00` では 5G はすべて passive / no-IR（TX 禁止）であり、指向性インジェクションはそもそも送出できません。TX 可能な規制に設定する必要があり（`iw reg set US` で ch36 / ch149 が解除され、`TW` は ch149 以上のみ許可で ch36 は含まれません）、テスト後は `TW` に戻します。また「カードを挿し直した直後」とは、USB が再列挙されるまで物理的に抜き挿しすることを指します。`dmesg` で `USB disconnect` と `renamed from wlan0` が確認でき、bus 番号が変わって初めて有効です。5G がすでにフリーズしている場合、aireplay は `No such BSSID available` を返します。
3. **hcxdumptool は本プラットフォームで、2.4 GHz の AWUS036EACS を除く全カードで `failed to arm`**：active-monitor が必要なのに、rtw88 / rtw89 / mt7921u のいずれも対応していないためです。handshake をキャプチャするには airodump-ng + aireplay-ng の経路を使ってください。

### ツールチェーンの互換性（Kali）

Kali でよく使われるツールについて、ACH で一通りの簡易確認を行いました（環境のターゲットは自社の `YUPITEK`）。結果は次のとおりです。

| ツール | 状態 | 説明 |
|---|---|---|
| airmon-ng | ✅ | `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` を正しく列挙 |
| Wireshark / tshark | ✅ | `tshark -i $IF` で beacon（YUPITEK を含む）を取得、20 packets captured |
| kismet | ✅ インストール済み | `/usr/bin/kismet`、data source として起動可能 |
| bettercap | ✅ インストール済み | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | インストール済みだが、本プラットフォームでは `failed to arm`（active-monitor が必要、上記参照） |
| macchanger | ✅ | GNU 1.7.0；`-r` でランダム、`-p` で復元、実測で正常 |
| wifite | ❌ 未インストール | 本機にコマンドがなく、別途インストールが必要（自前ビルドの aircrack-ng との apt 依存関係の衝突を避けるため、git 版を推奨） |

結論は単純です。airmon-ng は ACH を正しく認識して管理でき、通常の monitor とキャプチャの流れは aircrack-ng パッケージ（airodump-ng + aireplay-ng）を使うのが最も安定しています。active-monitor を必要とする hcxdumptool は本プラットフォームでは arm できないため、そこで足止めされないようにしてください。

## 5. 適した利用シーンと機種選定の提案（総括表 Hub へ）

ACH を製品ライン全体の中に置いて見ると、その位置づけははっきりしています。デュアルアンテナ・高ゲイン、両バンドの injection 100%、エンドツーエンドの WPA handshake（.22000）も実証済みで、「安定したインジェクションと、より強い受信の両方がほしい」お客様にとって現実的な選択肢です。

- **ペネトレーションテスト（injection + handshake）**：第一候補は AWUS036EACS / AWUS036ACH / AWUS036ACS で、3 機種とも両バンドのインジェクション性能は上位です。
- **最強の受信 / 長距離 monitor**：AWUS036AXER と AWUS036ACH で、ACH はデュアルアンテナ・高ゲインが持ち味です。
- **802.11s mesh / active-monitor / P2P が必要な場合**：ACH（Realtek rtw88）では実現できません（実測で `-95` が返りました）。mt76 ドライバの AWUS036ACM / AWUS036ACHM をご利用ください。ACH の IBSS は単機でしか構築できず、peer-link は未テストです。
- **純粋な AP や通常の接続のみで、インジェクションはしない場合**：MediaTek の AWUS036AXM / AXML のほうが安定しますが、これらは本プラットフォームで injection が失敗するため、ペネトレーションテスト用途には向きません。

一言で避けるべき点を言えば、お客様の要件が明確にインジェクションと handshake であるなら、AWUS036AXM / AXML は選ばないでください（MT7921 チップのインジェクションは本プラットフォームの実測で失敗し、deauth も handshake のキャプチャもできません）。そうした要件には、ACH のほうがむしろ堅実な候補です。機種選定では、帯域幅の数字だけを見ないでください。デュアルアンテナ・高ゲインがもたらす受信の安定性は、実際のモニタリング距離において、紙面のスペックよりも差を実感しやすいものです。機種選定の判断とプラットフォーム共通の落とし穴は、総括表 Hub をご覧ください：[9 種の ALFA ワイヤレスカードを ASUS GX10（ARM64）で使う場合の Monitor・Injection・AP 全マトリクス](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## よくある質問（FAQ）

**Q：AWUS036ACH は Kali や Ubuntu でドライバのインストールが必要ですか？**
カーネルのバージョンによります。Linux カーネル 6.13 以上（今回の実測は Ubuntu 24.04 / kernel 6.17）では rtw88_8812au ドライバが組み込まれており、挿すだけで認識され、コンパイルも DKMS も不要です。カーネルが 6.13 未満の場合のみ、DKMS で lwfinger/rtw88 を別途インストールする必要があります。Kali では先に uname -r でカーネルバージョンを確認してください。今回は Kali 実機では検証していません。

**Q：AWUS036ACH の monitor mode とパケットインジェクションの性能はどうですか？**
2.4GHz・5GHz のどちらでも monitor mode に入れます。aireplay-ng による AP ごとの指向性インジェクションは、2.4GHz（4 台の AP に対して）も 5GHz（YUPITEK ch36 に対して）も 30/30 = 100% でした。5GHz のインジェクション前には、規制ドメインを送信が許可される設定にしておく必要があります（例：iw reg set US）。デフォルトの country 00 では 5GHz は送信が禁止されており、インジェクションが送出されません。

**Q：AWUS036ACH で WPA handshake をキャプチャできますか？**
できます。しかもエンドツーエンドで実証済みです。両バンドともインジェクションは 100% で、2026-11-19 の追加テストでは、自社の iPhone 15 Pro、5GHz ch36 で完全な 4-way ハンドシェイクをキャプチャし、hcxpcapngtool で 47 件の hashcat .22000 hashline に変換しました。自分が所有する、または許可を得たネットワークに限ります。

**Q：AWUS036ACH で WPA3 ホットスポットを開くと、iPhone 7 Plus が接続できない場合は？**
hostapd で sae_pwe=0 を設定し、ieee80211w=2 と組み合わせると iPhone 7 Plus が接続できます。sae_pwe=2 では接続できません。同じ設定は AWUS036ACHM でも重要です。

**Q：AWUS036ACH の 5GHz 受信が突然フリーズする（0 パケットしか取得できない）場合は？**
これは rtw88_8812au の既知の現象です。モードの切り替えや規制ドメインの変更を繰り返すと 5GHz 受信がフリーズすることがあり、ソフトウェアでは復旧できず、物理的に抜き挿しするか再起動するしかありません。5GHz のテスト前にカードを挿し直し、5GHz の項目を優先して完了させることをお勧めします。

## 6. 関連記事

- 総括表 Hub：[9 種の ALFA ワイヤレスカード ARM64 全マトリクス](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- ドライバ不要で Ubuntu（ARM64）の Monitor と AP を有効化：[placeholder](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE の handshake キャプチャと `sae_pwe` の互換性：[placeholder](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 姉妹カードとの比較：AWUS036ACHM（シングルアンテナ AC600）単体実機検証 [placeholder]
- 本機種の完全な証拠パス（内部）：`AWUS036ACH_evidence/`（p0 列挙、p1_gx10 動作、retest 切り分け）

<!-- hreflang：zh-TW が原稿。ja 版は L2 ローカライズ。 -->
