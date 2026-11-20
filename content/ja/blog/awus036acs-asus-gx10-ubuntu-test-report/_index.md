---
title: "AWUS036ACS 個別実機検証：RTL8811AU 搭載の軽量ポータブルカードを ASUS GX10 + Ubuntu 24.04（ARM64）で試した互換性・機能レポート"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS を Ubuntu 24.04 ARM64 で実機検証。ドライバのインストールは不要で、Monitor、インジェクション（2.4G 100%、5G 96%）、AP、WPA3-SAE、エンドツーエンドの handshake（.22000）がすべて通りました。プラットフォームは ASUS GX10、kernel 6.17、RTL8811AU です。"
faq:
  - question: "AWUS036ACS は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？"
    answer: "本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8811AU は組み込みの rtw88_8821au ドライバで、挿すだけで認識され、コンパイルも DKMS も要りません。kernel が古い場合は、まず modinfo rtw88_8821au でモジュールが存在するか確認してください。"
  - question: "AWUS036ACS は monitor mode と packet injection に対応していますか？"
    answer: "対応しています。2.4 GHz・5 GHz のどちらでも monitor できます。aireplay-ng --test によるインジェクションは 2.4G が 100%（30/30）、5G が 96%（29/30、事前に iw reg set US で TW の制限を解除する必要あり）でした。active monitor には対応していません。"
  - question: "AWUS036ACS で WPA handshake を取得し、hashcat 用の .22000 に変換できますか？"
    answer: "できます。自前の AP と自前の iPhone 7 Plus でエンドツーエンドに検証しました。指向性 deauth で再接続を誘発し、完全な 4-way（M1–M4）を取得して、hcxpcapngtool --all で .22000 に変換しています。自分が所有する、または許可を得たネットワークに限ります。"
  - question: "AWUS036ACS は AP（アクセスポイント）として使えますか？WPA3 には対応していますか？"
    answer: "使えます。hostapd で 2.4G と 5G のアクセスポイントを立て（5G は 802.11a・20 MHz で実測し、VHT80 は未測定）、iPhone 7 Plus が接続して 4-way を完了しました。5G の WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）でも接続に成功しています（2.4G の WPA3 は未実測）。"
  - question: "AWUS036ACS が対応していないモードは？hcxdumptool は使えますか？"
    answer: "active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）には対応していません。hcxdumptool 8.x は failed to arm interface となるため、airodump-ng + aireplay-ng を使ってください。mesh / IBSS が必要な場合は AWUS036ACM / ACHM を選んでください。"
draft: false
---

**要点まとめ（TL;DR）**：Yopitek（ALFA Network 台湾代理店）の実測では、AWUS036ACS は ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）でドライバのインストールが不要で、両バンドの monitor と AP（5G の AP は使用可：802.11a・20 MHz で実測、VHT80 は未測定）が使えます。インジェクションは 2.4G が 100%、5G が 96% で、エンドツーエンドの .22000 取得も通りました。一方、mesh / IBSS には対応していません。

> 本記事は、ALFA AWUS036ACS を新しい Linux プラットフォーム上で検証した、製品の互換性と機能の実測記録です。機種選定の判断材料としてお使いください。
> 検証プラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。掲載データはすべて、Yopitek が**自社設備・自社オフィスの Wi-Fi**（SSID `YUPITEK`、2.4G ch5 / 5G ch36）上で**自社のテスト用スマートフォン**（Apple iPhone 7 Plus）を相手に実測したものの抜粋で、MAC アドレスは一部伏せています。
> ⚠️ **合法性と範囲に関する宣言**：Monitor、Injection、handshake の取得は、自分が所有する、または許可を得たネットワークと機器でのみ実施しています。AP モードは各地域の電波法規に従ってください。本記事はカード自体の機能・互換性・設定に焦点を当てており、**第三者のネットワークに対する攻撃操作は一切扱いません**。

---

## 1. このカードと検証プラットフォーム

AWUS036ACS は ALFA の製品ラインのなかでも軽量・携帯向けの無線 LAN カードで、チップは Realtek RTL8811AU、Wi-Fi 5（802.11ac）世代の 1x1 シングルストリームです。位置づけははっきりしています。小型・低消費電力・シングルアンテナで、現場での棚卸しに持ち出すためのカードであり、最高スループットや最長距離を狙う重装備のカードではありません。そのため評価のポイントは「どれだけ速いか」ではなく、「これだけ軽い仕様で、実務上の機能がどこまで揃っているか」になります。

今回の検証では、典型的な運用シナリオにこのカードを置きました。GX10 の内蔵 NIC（`wlP9s9`）を外部接続用とし、AWUS036ACS は USB 外付けでテスト専用にします。こうしておけば、Monitor や AP に切り替えてもホスト自身のネットワークには影響しません。操作したのは ALFA カードに対応する `wlx*` インターフェースだけで、内蔵の外部接続用 NIC には触れていません。

| 項目 | 内容 |
|---|---|
| 型番 | AWUS036ACS |
| チップ | Realtek RTL8811AU（Wi-Fi 5 / 802.11ac、1x1 シングルストリーム） |
| USB ID | `0bda:0811` |
| ドライバ | `rtw88_8821au`（in-kernel、kernel 6.17 に組み込み済み） |
| ファームウェア | 42.4.0（dmesg で実測） |
| プラットフォーム | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| テスト端末 | Apple iPhone 7 Plus |

---

## 2. ハードウェアとドライバ（インストール不要）

このカードは GX10 に挿すだけで認識され、コンパイルも DKMS も不要です。RTL8811AU / RTL8821AU は mainline kernel 6.13 から、Realtek の in-kernel `rtw88` ドライバ群に正式に取り込まれました。GX10 に載っている 6.17 には `rtw88_8821au` モジュールがすでに入っているため、GitHub から out-of-tree のプロジェクトを持ってくる必要はありません。（旧版のインストールガイドとは異なります。以前のサイト記事は `morrownr` の out-of-tree ドライバや古い kernel を前提に、DKMS での自前コンパイルが必要と書いていましたが、kernel 6.17 の in-kernel ドライバではその手順はもう不要です。）以前よく使われていた `morrownr/8821au-20210708` は現在 legacy 扱いで、6.13 未満のカーネルでのみ推奨されます。しかも導入すると組み込みドライバが blacklist されてしまうため、新しい kernel でこの古い道をたどる理由はありません。運用面での利点はさらに実際的です。in-kernel ドライバは kernel と一緒に更新されるので、利用者が各自でブランチを保守する必要がなく、アップグレードのたびに DKMS のビルド失敗で詰まることもありません。同じ手順が、複数回の kernel 更新をまたいでそのまま使えます。ファームウェアは `linux-firmware` がシステムとともに提供し、本機での実測は 42.4.0 です。こちらも手作業は要りません。

カードが認識され、ドライバがバインドされ、インターフェースが生成されたことを確認します。

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

ファームウェアのバージョンは `dmesg` で確認できます（実測は 42.4.0）。

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

宣言されているインターフェースモード（この一覧が、後述のどの機能が使えるかを決めます）。

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

この一覧には `IBSS / managed / AP / AP/VLAN / monitor` が挙がっています。ここで特に注意してほしい点があります。一覧に IBSS が載っているにもかかわらず、実測では `ibss join` のあとに `iw link` が Not connected と表示され、接続できませんでした。mesh、active-monitor、P2P は一覧にそもそも存在しません（詳細は第 4 節の制限事項を参照）。これは RTL8811AU のハードウェアとドライバの現状であり、アンテナ数とは関係ありません。

対応帯域は、2.4 GHz が ch1–13（ch14 は disabled）、5 GHz が ch36–165（このうち ch52–144 は radar / DFS 指定）です。デフォルトの regdomain は `TW` で、TX 出力は 2.4 GHz が 30 dBm、5 GHz の UNII-1/2 が 23 dBm、UNII-3 が 30 dBm でした。

---

## 3. 実測した機能：Monitor / Injection / AP / WPA3

まず主要機能の一覧表を示し、そのあと項目ごとに詳しく見ていきます。すべての項目は、自社の YUPITEK AP と自社の iPhone 7 Plus を使って確認しました。

| 機能 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（モニタ受信） | ✅ 強い | ✅ 強い |
| Injection（パケットインジェクション） | ✅ **100%**（30/30） | ✅ **96%**（29/30、事前に reg の解除が必要） |
| AP（hostapd） | ✅ iPhone が接続 + handshake 完了 | ✅ **安定**（802.11a・20 MHz で実測、VHT80 は未測定） |
| AP の WPA3-SAE | 未実測 | ✅ iPhone が接続（SAE-only + PMF） |

### 3-1. Monitor（モニタモード、2.4 GHz + 5 GHz）✅

monitor に切り替えたあと、6 つのチャンネルで一定時間ずつキャプチャしたところ、いずれも受信は正常でした。混雑しているチャンネルでは、6 秒以内に上限の 300 フレームに達しました。

| チャンネル | キャプチャした frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

2.4 GHz も 5 GHz も安定して受信できています。シングルアンテナの携帯カードとしては、現場でのチャンネル棚卸しやパケット診断に十分な受信性能です。ch11、ch149、ch157 のフレーム数が少ないのは、それらのチャンネルでその時点の電波上のトラフィックがもともと少なかったためで、カードが受信できていないわけではありません。混雑している ch1、ch6、ch36 は 6 秒で上限の 300 フレームに達しており、受信がボトルネックでないことは明らかです。

### 3-2. Injection（パケットインジェクション）✅

自社の YUPITEK AP に対し、`aireplay-ng --test` で指向性インジェクションを試験しました。2.4 GHz は 100%（30/30、`Injection is working!`）、5 GHz は 96%（29/30）でした。5 GHz には設定上の注意点があります。デフォルトの `reg=TW` では一部の UNII 帯域で能動送信がロックされるため、テスト前に `sudo iw reg set US` で解除し、テスト後に `sudo iw reg set TW` で戻してください。

```bash
# 2.4 GHz (YUPITEK は実際には ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

シングルアンテナのカードで 2.4 GHz が 100%、5 GHz が 96% というのは十分に信頼できるインジェクション性能で、これが後述のエンドツーエンドの handshake 取得を成立させる土台にもなっています。

### 3-3. AP（2.4 GHz / 5 GHz）✅

`hostapd` でカードを基地局にし、3 種類の設定すべてで iPhone 7 Plus が接続して 4-way handshake（`EAPOL-4WAY-HS-COMPLETED`）を完了しました。

- **5 GHz（802.11a・20 MHz で実測、VHT80 は未測定）**：最も安定した設定です。iPhone が接続し、handshake が完了し、`AP-DISABLED` できれいに終了しました。
- **2.4 GHz（WPA2-PSK）**：iPhone が接続し、handshake が完了し、切断後もきれいに終了しました。ここで正直に記しておくべき事象があります。前回の同じ設定では、STA の切断後に `key not allowed / Failed to set beacon parameters` が出て中断したことがありました。しかし再テストでは再現できず、rtw88_8821au で偶発的に起こる beacon re-key であり、恒常的な欠陥ではないと判断しています。ただし、長時間・高頻度の再接続を伴う用途では注意するか、いっそ 5 GHz の AP に切り替えることをお勧めします。
- **WPA3-SAE（5 GHz、PMF 必須。2.4 GHz は未実測）**：鍵となる設定は `wpa_key_mgmt=SAE`（WPA3 のみで WPA2 へのフォールバックなし）、`ieee80211w=2`（Management Frame Protection を必須化）、`sae_pwe=0`（古いクライアントとの互換性確保）です。iPhone 7 Plus（iOS 15）が SAE で接続できました。AP 側は SAE のみで WPA2 の逃げ道がないため、アソシエーションが完了したということは、SAE の認証ハンドシェイクが成立したことを意味します。RTL8811AU + rtw88_8821au は、AP 側の WPA3-SAE が利用可能です。

---

## 4. エンドツーエンドの handshake 機能と制限事項

### 4-1. エンドツーエンドの handshake 取得 ✅

これは、インジェクションとキャプチャが本当に「つながる」かを検証する総合テストで、すべて自社の YUPITEK AP と自社の iPhone 7 Plus を使い、許可を得た前提で実施しました。流れは次のとおりです。対象チャンネルに monitor を合わせる → 自社端末へ指向性 deauth を送って再接続を誘発する → 完全な 4-way（M1–M4）を取得する → `hcxpcapngtool --all` で hashcat が読める `.22000` に変換する。

実測結果は次のとおりです。`aircrack-ng` は YUPITEK で 1 件の handshake を取得したと判定し、EAPOL の 4 メッセージ M1–M4 がすべて揃い、クライアントは Apple OUI（`b8:53:ac`、iPhone 7 Plus であることを確認）でした。変換した `.22000` はそのまま hashcat に渡せます。これは、AWUS036ACS がエンドツーエンドの handshake 取得機能を備えていることを示しています。

実測で得られた要点が 2 つあります（詳細な手順は別記事を参照してください）。

1. **オフィスの同一チャンネルに同名の AP が複数台ある場合は、`--bssid` で 1 台に絞らず**、チャンネル全体をキャプチャしてください。そうしないと、別の AP につながっている端末を取りこぼします。
2. `hcxpcapngtool` はデフォルトでは厳しめで、「not enough M1」と返すことがあります。`--all` を付ければ、完全な M1–M4 から `.22000` を変換できます。

この handshake 取得の流れで使った Kali の定番ツール（aircrack-ng、hcxtools）は、Ubuntu 24.04 ARM64 上でそのまま動作し、airodump-ng、aireplay-ng、hcxpcapngtool はいずれも正常に動きました。

### 4-2. VIF（仮想インターフェース）✅

`iw dev $IF interface add mon9 type monitor` で monitor VIF を作成し、100 frames をキャプチャできました。さらにスクリプトで「メインのインターフェースを STA として YUPITEK に接続 + AP VIF を 1 つ」という構成も作成でき、単一チップで STA と AP を同時に担えます。

### 4-3. 正直な制限事項（実測報告）

| 高度なモード / ツール | 状態 | 実測 |
|---|---|---|
| Active monitor | ❌ 非対応 | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc（IBSS） | ❌ 非対応 | モードは一覧にあるが、`ibss join` 後に `iw link` = Not connected |
| Mesh（802.11s） | ❌ 非対応 | `set type mp` → `-95` |
| Wi-Fi Direct（P2P） | ❌ 非対応 | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ arm できない | `failed to arm interface`：rtw88_8821au は active-monitor を提供しない。airodump-ng + aireplay-ng を使う |

運用面で知っておくべき制限がさらに 2 つあります。1x1 のシングルストリームが理論上限（HT Max RX 150 Mbps、VHT80 で約 433 Mbps）を決めており、スループットはもともとこのカードの得意分野ではありません。また、monitor / AP を何度も切り替えると、RX が一時的に degraded 状態になる（何も検出できなくなる）ことがあります。その場合はカードを物理的に抜き差しすれば復旧します。インターフェース名は MAC から決まるため、抜き差ししても変わりません。

---

## 5. 適した用途と選定（軽量・携帯向け、Hub への接続）

ここまでの機能を製品の位置づけに当てはめると、AWUS036ACS の役割は明確です。機能は一通り揃っているが、軽さを売りにした携帯向けカードです。では、どんな用途に向くのでしょうか。

- **現場での簡易棚卸し / 携帯診断**：シングルアンテナ・小型・低消費電力で、チャンネルの棚卸し、電波強度の巡回確認、パケット診断に持ち出す用途に向いています。GX10 のような中央プラットフォームと組み合わせ、携帯カードが現場でキャプチャし、そのデータを Hub に戻して集中分析するという分担が明快です。
- **教育と検証**：Monitor / Injection / AP / WPA3-SAE / エンドツーエンドの handshake という主要な流れをすべて通せるため、デモや、許可された範囲内での検証用カードに向いています。
- **向かない用途**：最高のスループットや最長の距離が必要な場合、あるいは mesh / IBSS / P2P / active-monitor が必要な場合、このカードは適切な選択ではありません。

軽量だからといって機能が削られているわけではありません。主要な機能は何一つ欠けておらず、取捨されたのはスループットの上限と高度なインターフェースモードです。したがって、選ぶかどうかは「持ち歩きたいか」「性能を出し切りたいか」で決まります。

同ファミリーの他モデルと比べた位置づけは次のとおりです。

| 要件 | 推奨カード | 理由 |
|---|---|---|
| 軽量・携帯向け + 主要機能が一通り揃う | **AWUS036ACS** | 2.4G インジェクション 100%、5G 96%、エンドツーエンドの handshake 利用可、シングルアンテナで軽量 |
| 両帯域ともインジェクション 100% / より安定した検証 | AWUS036EACS、AWUS036ACH | 両帯域でインジェクション 100%、EACS は BT も内蔵 |
| 最強の受信 / 長距離の monitor | AWUS036AXER、AWUS036ACH | チャネルホッピングでより多くの対象を検出 / デュアルアンテナ高ゲイン |
| mesh / IBSS の単機実験 | AWUS036ACM、AWUS036ACHM | mt76 ドライバなら単機で構築可能（Realtek rtw88 は非対応） |

一言でまとめると、軽量でありながら主要機能も揃えたいなら AWUS036ACS は携帯向けとして適した選択です。両帯域でインジェクション 100% が必要な場合や、より本格的な検証をしたい場合は、EACS / ACH を選んでください。

---

## よくある質問（FAQ）

**Q：AWUS036ACS は Ubuntu 24.04 ARM64 でドライバのインストールが必要ですか？**
本記事で検証した kernel 6.17（ASUS GX10）では不要です。RTL8811AU は組み込みの rtw88_8821au ドライバで、挿すだけで認識され、コンパイルも DKMS も要りません。kernel が古い場合は、まず `modinfo rtw88_8821au` でモジュールが存在するか確認してください。

**Q：AWUS036ACS は monitor mode（モニタモード）と packet injection（パケットインジェクション）に対応していますか？**
対応しています。2.4 GHz・5 GHz のどちらでも monitor できます。`aireplay-ng --test` によるインジェクションは 2.4G が 100%（30/30）、5G が 96%（29/30、事前に `iw reg set US` で TW の制限を解除する必要あり）でした。active monitor には対応していません。

**Q：AWUS036ACS で WPA handshake（ハンドシェイクパケット）を取得し、hashcat 用の .22000 に変換できますか？**
できます。自前の AP と自前の iPhone 7 Plus でエンドツーエンドに検証しました。指向性 deauth で再接続を誘発し、完全な 4-way（M1–M4）を取得して、`hcxpcapngtool --all` で .22000 に変換しています。自分が所有する、または許可を得たネットワークに限ります。

**Q：AWUS036ACS は AP（アクセスポイント）として使えますか？WPA3 には対応していますか？**
使えます。`hostapd` で 2.4G と 5G のアクセスポイントを立て（5G は 802.11a・20 MHz で実測し、VHT80 は未測定）、iPhone 7 Plus が接続して 4-way を完了しました。5G の WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）でも接続に成功しています（2.4G の WPA3 は未実測）。

**Q：AWUS036ACS が対応していないモードは？hcxdumptool は使えますか？**
active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）には対応していません。hcxdumptool 8.x は failed to arm interface となるため、airodump-ng + aireplay-ng を使ってください。mesh / IBSS が必要な場合は AWUS036ACM / ACHM を選んでください。

---

## 6. 関連記事

- ALFA 無線 LAN カード 9 モデルの機能比較と選定の総括 → [ALFA 無線 LAN カード総括 Hub（総合表）](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [ドライバのインストール不要：Ubuntu 24.04 + kernel 6.17 で Monitor / AP を有効にする（rtw88 / rtw89 / mt76 実機検証）](/ja/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [WPA3-SAE とエンドツーエンドの handshake 取得のステップバイステップ解説](/ja/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 同ファミリーの BT+WiFi 複合カード → [AWUS036EACS 個別実機検証](/ja/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*検証担当：Yopitek（ALFA Network 台湾代理店）— https://www.yupitek.com ｜ 検証環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ テスト端末：Apple iPhone 7 Plus*
