---
title: "WPA3-SAE 時代の無線監査：ALFA 9 製品の handshake キャプチャ能力の実測と、iPhone 接続における sae_pwe 互換性の落とし穴"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "Ubuntu（Kali にも応用可能）における ALFA アダプタの WPA3-SAE handshake キャプチャ能力の実測。9 製品の injection 成功率とエンドツーエンドの .22000 キャプチャ結果、sae_pwe 互換性の落とし穴、選定ガイドを掲載します。"
faq:
  - question: "AWUS036AXM は Ubuntu で WPA handshake をキャプチャできますか？"
    answer: "本プラットフォームではできません。実測では、AWUS036AXM と AWUS036AXML（MT7921 チップ）は injection に失敗して deauth を送出できず、4-way handshake のキャプチャ経路全体が途切れるため、handshake のキャプチャが必要な用途には向きません。"
  - question: "WPA handshake のキャプチャが最も確実な ALFA アダプタはどれですか？"
    answer: "実測では AWUS036EACS が最も確実でした。両バンドの injection がいずれも 100% に達し、deauth の後に 79 個の ACK 応答を受信し、hashcat で使える .22000 ファイルへの変換にも成功しています。今回のラインナップで、エンドツーエンドの検証が最も完全な 1 製品です。"
  - question: "WPA3-SAE のホットスポットに、旧型の iPhone が接続できないのはなぜですか？"
    answer: "鍵は hostapd の sae_pwe パラメータです。2（H2E を強制）にすると iPhone 7 Plus は接続に失敗し、sae_pwe=0（Hunting-and-Pecking）に戻して初めて、4-way handshake を正常に完了して接続できました。"
  - question: "WPA3 環境でも 4-way handshake をキャプチャできますか？"
    answer: "純粋な WPA3-SAE 環境では PMF（ieee80211w=2）が強制的に有効になり、管理フレームを対象とした従来の手法はブロックされます。実務上でも handshake をキャプチャできる場合があるのは、多くの場合、ターゲットが純粋な WPA3 ではなく、WPA2/WPA3 の移行モードで動作しているためです。"
  - question: "ALFA アダプタの 5GHz injection が成功しません。ハードウェアの問題ですか？"
    answer: "必ずしもそうではありません。デフォルトの規制ドメインでは、5GHz の一部の帯域で送信出力が制限され、injection が「送出できない」状態になることがあります。実測では、規制ドメインを送信可能な状態に切り替えたところ、失敗していた 5GHz の injection が使えるようになりました。ハードウェアの制限と判断する前に、まず規制ドメインの設定を確認することを推奨します。"
draft: false
---

> テスト実施：Yopitek（ALFA Network 台湾代理店）｜テストプラットフォーム：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17｜テスト端末：自社の iPhone 7 Plus（WPA3 は iPhone 15 Pro でも別途テスト）｜テスト対象：自社オフィスの Wi-Fi（SSID YUPITEK、2.4G ch5 / 5G ch36、157）。
>
> 本記事は、ALFA 無線 LAN アダプタの能力と互換性の概要です。Monitor / Injection / handshake のキャプチャは、すべて Yopitek 自社の機器と自社オフィスの Wi-Fi 上で、自社のテスト用スマートフォンに対して実施しました。代理店によるハードウェアの正当な能力検証であり、第三者のネットワークを対象とするものではなく、攻撃の操作手順も提供しません。

## 要点まとめ（TL;DR）

ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）で実測した ALFA の 9 製品のうち、ACM、ACHM、ACH、ACS、EACS、AX、AXER の 7 製品が WPA handshake のエンドツーエンドのキャプチャと `.22000` への変換を完了し、AWUS036EACS は両バンドの injection 100%・79 ACKs を記録、MT7921 の AXM / AXML は本プラットフォームで injection に失敗しました。

- WPA3-SAE の普及により、監査の焦点は「monitor できるか」から「エンドツーエンドの handshake キャプチャ能力」と「`sae_pwe` のエンドポイント互換性」へ移りました。
- **エンドツーエンドの `.22000` を実証できたのは 9 製品中 7 製品**：ACM、ACHM、ACH、ACS、EACS、AX、AXER。そのうち EACS が最も確実です（両バンドの injection 100%、79 ACKs）。
- **AXM / AXML（MT7921）は本プラットフォームでは injection に失敗**し、deauth を送れず、handshake をキャプチャできません。監査用途では必ず避けてください。
- `sae_pwe` の落とし穴：旧型の iPhone は `sae_pwe=0` でないと接続できません。5G で injection を行う前に、`iw reg set US` で TX を解放してください。
- 純粋な WPA3 では PMF が強制されます（`ieee80211w=2`）。現場で今もキャプチャできるのは、多くの場合、ターゲットが WPA2/WPA3 の移行モードで動作しているためです。

## 1. WPA3-SAE の普及で、無線監査のハードルは大きく上がった

この 10 年、許可された範囲での無線監査（authorized wireless audit）は、ほとんど WPA2-PSK の 4-way handshake を中心に行われてきました。完全なハンドシェイクを 1 回キャプチャすれば、あとはオフラインで照合できたからです。しかし Wi-Fi 6 の認証で WPA3 が必須項目に加わってから、SAE（Simultaneous Authentication of Equals、通称 Dragonfly）が徐々に PSK に置き換わり、「ハンドシェイクをキャプチャしてオフラインで検証する」という従来の道は、だんだん狭まってきています。

代理店や現場のエンジニアにとって、WPA3-SAE は実務上 3 つの変化をもたらします。

1. **PMF（Protected Management Frame）が必須になります。** WPA3-SAE の規格では `ieee80211w=2` が強制され、management frame が保護されます。従来のような「deauth を 1 つ送って端末を簡単に切断する」やり方は、純粋な WPA3 環境では直接ブロックされます。
2. **移行モード（transition mode）では 4-way が残ります。** 実際には、多くの AP が WPA2/WPA3 の混在する移行モードで動作しており、旧型の端末との互換性のために WPA2 の 4-way handshake が残されています。これが、現在でも許可された範囲での監査でハンドシェイクをキャプチャできる主な理由です。ハンドシェイクをキャプチャできるかどうかは、現場のターゲットがどちらのモードで動いているかに大きく左右されます。
3. **エンドポイントの互換性が新たな落とし穴になります。** SAE には password element の導出方法がいくつかあり（`sae_pwe` で制御されます）、AP のパラメータを間違えると、自社の旧型 iPhone すら接続できません。ましてや、監査の現場でクライアント側の接続挙動を再現することはできません。

そのため、お客様から「WPA3 関連の許可された範囲での監査に使える ALFA アダプタはどれですか」と尋ねられたとき、答えはもはや「monitor できるか」だけでは済みません。見るべきことは 2 つあります。**エンドツーエンドの handshake キャプチャ能力**と、**WPA3-SAE のパラメータおよび実機エンドポイントとの互換性**です。本レポートは、ALFA 9 製品を同一の ARM64 プラットフォームで実測し、その能力を整理した対照表です。

## 2. 「エンドツーエンドの handshake キャプチャ能力」とは何か（概念編）

ここでは、能力を 3 つの段階に分けて整理します。あくまで概念の説明であり、第三者のネットワークに対する操作コマンドは含みません。

- **第 1 段階：Injection（能動的な注入）。** アダプタが特定の管理フレームを「送出」できて初めて、すでに接続済みの client に再関連付けを促せます。多くのアダプタは受動的な monitor（パケットの受信）しかできず、injection（能動的な送信）はできません。経路全体のなかで、最もつまずきやすい段階です。今回のテストでは、`aireplay-ng --test` で injection の成功率を定量化し、handshake テストでは client から返ってきた ACK の数で、フレームが実際に届いたかを検証しました。
- **第 2 段階：4-way handshake のキャプチャ。** client が再関連付けを行うと、WPA は 4 つの EAPOL メッセージ（M1–M4）を交換します。アダプタは monitor モードで、この 4 フレームをすべて漏れなく受信しなければなりません。1 つでも欠けたら不成立です。
- **第 3 段階：hashcat 用 `.22000` への変換。** キャプチャした pcap を `hcxpcapngtool --all` で hashcat の `.22000` 形式に変換し、バックエンドでのオフライン検証に渡します。

**3 つの段階がすべて実機で通って、初めて「エンドツーエンド」です。** 自社の iPhone 7 Plus に実際に deauth を送り（injection）→ 完全な M1–M4 を受信 → `.22000` に変換してファイル出力する、という流れです。受信しかできない、送信しかできない、4 フレームが揃わない、ファイルに変換できない、のいずれも、エンドツーエンドとは認められません。本記事では、攻撃の手順を示すコマンドは掲載しません。以下の対照表が答えるのは、「この能力の連鎖を最後まで走り切れるアダプタはどれか」という 1 点だけです。

今回最も確実だった EACS を例にすると、成功したエンドツーエンドは次のようなものです。deauth を送ると client から **79 個の ACKs** が返り（フレームがその端末に確実に届いたことの確認）、`aircrack-ng` が YUPITEK に 1 つの handshake があると判定し、EAPOL の M1 / M2 / M3 / M4 の 4 フレームがそれぞれ 1 つずつ受信され、キャプチャした client MAC の先頭は Apple OUI（あの iPhone 7 Plus であることの確認）で、最後に `hcxpcapngtool --all` で約 784 bytes の `.22000` に変換されました。この 4 つの条件のどれか 1 つでも欠けたら、このキャプチャは成立しません。これが、「monitor できる」ことと「エンドツーエンドでキャプチャできる」ことがまったく別物である理由です。

## 3. 9 製品の handshake 能力対照表

| # | 型番 | チップ / 世代 | Injection 2.4G | Injection 5G | WPA handshake キャプチャ能力 |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5・2T2R | 利用可 63–83% | 利用可 76% | **エンドツーエンドの `.22000` を実証済み**（injection 成功率は低め） |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5・1T1R | 利用可 96–100% | ブロードキャストのみ | **エンドツーエンドの `.22000` を実証済み（5 GHz ch36）** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5・2T2R | **100%** | **100%** | **エンドツーエンドの `.22000` を実証済み（2026-11-19 追加テスト）** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5・1x1 | **100%** | 96% | **エンドツーエンドの `.22000` を実証済み** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5・1x1 | **100%** | **100%** | **エンドツーエンドの `.22000` を実証済み（79 ACKs）** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6・2x2 | 96% | 利用可 | **エンドツーエンドの `.22000` を実証済み** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6・2x2 | 73% | 利用可 | **エンドツーエンドの `.22000` を実証済み** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6・2x2 | 失敗 | 失敗 | 非対応：injection 失敗のためキャプチャ不可 |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6・2x2 | 失敗 | 失敗 | 非対応：injection 失敗のためキャプチャ不可 |

**2 つの階層で、ひと目でわかります。**

- **エンドツーエンドを実証済み（キャプチャ → `.22000` のファイル出力、9 製品中 7 製品）**：AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX、AWUS036AXER。そのうち EACS は両バンドの injection がいずれも 100% で、deauth に対して 79 個の ACKs を受信しており、今回のラインナップで handshake 能力が最も確実な 1 枚です。AWUS036ACH（RTL8812AU、デュアルアンテナ高ゲイン）は両バンドの injection が 100% で、2026-11-19 の追加テストで 47 行の hashline を持つ `.22000` に変換できました。EACS と並ぶペネトレーションテストの第一候補です。**エンドツーエンドの handshake キャプチャを完了した型番は 7 製品です：ACM、ACHM、ACH、ACS、EACS、AX、AXER。** ACM は injection 成功率が低め（2.4G 63–83% / 5G 76%）、ACHM は 5 GHz（ch36）で完了しましたが、どちらも `.22000` を出力できました。
- **キャプチャ不可（2 製品）**：AWUS036AXM と AWUS036AXML（MT7921 は本プラットフォームで injection に失敗し、deauth を送れないため、当然 handshake もキャプチャできません）。

特に名前を挙げておきたいのが **AXM / AXML** です。どちらも Wi-Fi 6 で、monitor と AP は正常に動作します。ただ本プラットフォームでは injection だけが動作しません。主因は stock kernel 6.16+ の mac80211 chanctx のリグレッションで（チップ固有の問題ではありません）、コミュニティでは同型番に git／パッチ適用済みドライバを使うと動作するものの、ファームウェアがレートをロックします（morrownr/USB-WiFi #387、morrownr/mt76 #18 に対応）。単純なネット接続やホットスポットには問題ありませんが、**injection や handshake のキャプチャが必要な監査用途では、本プラットフォームでは一律に避けてください。**

## 4. WPA3-SAE の互換性の落とし穴：パラメータを間違えると、自社の iPhone すら接続できない

能力以外で、現場で最もつまずきやすいのが、WPA3-SAE のパラメータ互換性です。今回の実測では、2 つの重要な落とし穴に当たりました。

### 4-1. ACHM は `sae_pwe=0` が必須。そうしないと iPhone 7 Plus が接続できない

SAE の password element の導出には複数の方式があり、hostapd では `sae_pwe` で制御します。今回、AWUS036ACHM を純粋な WPA3-SAE（`wpa_key_mgmt=SAE` + PMF 強制の `ieee80211w=2`）で立てたところ、`sae_pwe` を `2` にした途端、**iPhone 7 Plus はまったく接続できませんでした**。`sae_pwe=0`（Hunting-and-Pecking、旧型エンドポイントと互換）に戻して初めて、iPhone 7 Plus（iOS 15）が接続し、4-way を完了できました。

この落とし穴が意味するのは次のことです。旧型 iOS 端末が中心の WPA3 環境を監査の現場で「再現」したい場合、AP 側の `sae_pwe` をエンドポイントの能力に合わせなければなりません。そうしないと、得られるのは本当の互換性に関する結論ではなく、「接続できない」という偽陰性です。EACS と ACS の WPA3-SAE AP テストでも、同じく `sae_pwe=0` + `ieee80211w=2` を使用し、iPhone 7 Plus はいずれも接続できました。`sae_pwe=0` は、今回、旧型 iPhone のエンドポイントに対して検証済みの安全な値です。

### 4-2. 5G の injection の前に、`iw reg set US` で TX を解放する

2 つ目の落とし穴は、規制ドメイン（regulatory domain）に関するものです。デフォルトの `reg=TW` では一部の UNII 帯の TX がロックされ、5 GHz の injection / deauth が「送出できない」状態になります。今回は、5G の injection を行う前に必ず `iw reg set US` で TX を解放し、テスト終了後は直ちに `iw reg set TW` で元に戻しました。ACS の 5G injection は、解放後に失敗から 96% に変わり、EACS と ACH はそのまま 100% に達しました。reg の解放を忘れると、injection 能力が正常なアダプタを「5G は使えない」と誤判定してしまいます。

### 4-3. 補足：WPA3 では PMF が必須

WPA3-SAE の規格では `ieee80211w=2`（Management Frame Protection）が強制されます。つまり、純粋な WPA3 環境では、management frame を対象とした従来の手法は PMF によってブロックされます。現実の監査でも 4-way をキャプチャできるのは、多くの場合、ターゲットが今も WPA2/WPA3 の移行モードで動作しているからです。アダプタを選ぶときにはこの点も考慮に入れておかないと、純粋な WPA3 のターゲットに対して誤った期待を抱くことになります。

## 5. ツールチェーンの概要：ARM64 プラットフォームで実際に動くもの

ハードウェアの能力に加えて、プラットフォームのツールチェーンも監査の効率に影響します。以下は、今回 GX10（ARM64）で整理した、いくつかの実測上の知見です。

- **変換は常に `hcxpcapngtool --all`。** デフォルトのパラメータは厳しめで、「not enough M1」と返されて変換できないことがよくあります。`--all` を付けると、完全な M1–M4 から安定して `.22000` に変換できます。
- **オフィスに同名 AP が複数台ある場合は、`--bssid` で絞らない。** Yopitek のオフィスでは、同じチャンネル上に YUPITEK という同名の AP が複数台あり、iPhone は最も電波の強い 1 台に接続します。キャプチャ時に `--bssid` で単一の BSSID に絞ると、iPhone が実際に接続している AP を除外してしまい、キャプチャ全体が空振りになりかねません。実測の結論は、**BSSID を絞らずにチャンネル全体をキャプチャし**、ファイルのなかから完全なハンドシェイクを選び出すことです。
- **`hcxdumptool` 8.x は本プラットフォームでは、2.4 GHz の EACS（5 GHz は失敗）を除き `failed to arm`。** rtw88 / rtw89 / mt7921u はいずれも active-monitor を提供せず、hcxdumptool 8.x にはそれが必要です。対処法は、従来の aircrack-ng の手順である `airodump-ng` + `aireplay-ng` に切り替えることです。
- **モードを繰り返し切り替えた後に何もスキャンできなくなったら、まずアダプタを抜き挿しする。** rtw88 / rtw89 では、monitor / AP の切り替えを繰り返した後に RX stall（スキャンで 0 パケット）が発生することがあります。USB を再列挙すれば復旧し、インターフェース名は MAC で決まるため抜き挿ししても変わりません。handshake をキャプチャする前に、まずアダプタを一度挿し直すことを推奨します。
- **BT+WiFi コンボデバイス（EACS / AXML）は、抜き挿しの際に競合が起きる。** Bluetooth を含むコンボアダプタは、抜き挿しの際や特定の USB ポートに挿した際に、WiFi 機能の probe が止まって `wlx` インターフェースが生成されないことがあります。対処法は USB ポートを変えて挿し直すことで、`modprobe` や手動の bind はたいてい効果がありません。
- **ARM64 でのツールのインストールのコツ。** aircrack-ng は aarch64 ではビルド済みパッケージがないことが多く、ソースからのビルドが必要です。wifite は git 版を使います（apt 版は自前ビルドの aircrack-ng と依存関係が競合します）。
- **安全上のルール：`airmon-ng check kill` は絶対に実行しない。** GX10 は内蔵アダプタで外部に接続しており、`check kill` は NetworkManager ごと停止させ、ホストをネットワークから切断します。今回は一貫して ALFA アダプタの `wlx*` インターフェースだけを操作し、内蔵の外部接続用の主回線には触れていません。

## 6. 選定のまとめ：WPA3 関連の監査では、どの製品を選ぶべきか

能力、互換性、プラットフォームのツールチェーンを合わせて見ると、「WPA3 関連の許可された範囲での監査」という用途に対する今回の推奨は次のとおりです。

| 要件・状況 | 推奨型番 | 理由 |
|---|---|---|
| 総合的な第一候補（injection + エンドツーエンドの handshake） | **AWUS036EACS** | 両バンドの injection 100%、deauth で 79 ACKs、エンドツーエンドの `.22000` を実証済み。注意点は BT+WiFi コンボデバイスであることだけで、抜き挿しの際に USB ポートを変える必要が時々ある |
| 高ゲイン / 長距離 + 強力な injection | **AWUS036ACH** | RTL8812AU のデュアルアンテナ、両バンドの injection 100%、受信能力が高い |
| 軽量・携帯向け | **AWUS036ACS** | 単一ストリーム、エンドツーエンドの `.22000` を実証済み、5G の injection は 96% |
| Wi-Fi 6 が必要な場合 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80、エンドツーエンドの `.22000` を実証済み。AXER は内蔵アンテナ（Nano）設計とチップのチューニングにより、スキャンの範囲が最も広い |
| **必ず避けるべき製品** | AWUS036AXM / AWUS036AXML | MT7921 は本プラットフォームで injection に失敗し、handshake をキャプチャできない |

ひとことでまとめると、**WPA3 関連の監査を行うなら、まず EACS、次に ACH / ACS。Wi-Fi 6 が必要なら AX / AXER。AXM / AXML は必ず避けてください。** エンドツーエンドの handshake キャプチャを完了した 7 製品のうち、Realtek（rtw88 / rtw89）は全製品が injection 可能で、MediaTek の ACM と ACHM（mt76）も完走しましたが、MT7921 の AXM / AXML は使えません。選定にあたっては、型番名よりチップで判断するほうが確実です。

## よくある質問（FAQ）

**Q：AWUS036AXM は Ubuntu で WPA handshake をキャプチャできますか？**
A：本プラットフォームではできません。実測では、AWUS036AXM と AWUS036AXML（MT7921 チップ）は injection に失敗して deauth を送出できず、4-way handshake のキャプチャ経路全体が途切れるため、handshake のキャプチャが必要な用途には向きません。

**Q：WPA handshake のキャプチャが最も確実な ALFA アダプタはどれですか？**
A：実測では AWUS036EACS が最も確実でした。両バンドの injection がいずれも 100% に達し、deauth の後に 79 個の ACK 応答を受信し、hashcat で使える `.22000` ファイルへの変換にも成功しています。今回のラインナップで、エンドツーエンドの検証が最も完全な 1 製品です。

**Q：WPA3-SAE のホットスポットに、旧型の iPhone が接続できないのはなぜですか？**
A：鍵は hostapd の `sae_pwe` パラメータです。2（H2E を強制）にすると iPhone 7 Plus は接続に失敗し、`sae_pwe=0`（Hunting-and-Pecking）に戻して初めて、4-way handshake を正常に完了して接続できました。

**Q：WPA3 環境でも 4-way handshake をキャプチャできますか？**
A：純粋な WPA3-SAE 環境では PMF（`ieee80211w=2`）が強制的に有効になり、管理フレームを対象とした従来の手法はブロックされます。実務上でも handshake をキャプチャできる場合があるのは、多くの場合、ターゲットが純粋な WPA3 ではなく、WPA2/WPA3 の移行モードで動作しているためです。

**Q：ALFA アダプタの 5GHz injection が成功しません。ハードウェアの問題ですか？**
A：必ずしもそうではありません。デフォルトの規制ドメインでは、5GHz の一部の帯域で送信出力が制限され、injection が「送出できない」状態になることがあります。実測では、規制ドメインを送信可能な状態に切り替えたところ、失敗していた 5GHz の injection が使えるようになりました。ハードウェアの制限と判断する前に、まず規制ドメインの設定を確認することを推奨します。

## 7. 関連記事

- [ALFA 無線 LAN アダプタ 9 製品の ARM64 実測総括表と選定の総評](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 型番ごとの単体実測：[AWUS036EACS 単体実測](/ja/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 単体実測](/ja/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*本記事のすべてのテストは、Yopitek 自社オフィスの Wi-Fi（SSID YUPITEK）で、自社の iPhone 7 Plus に対して実施したもので、代理店による ALFA 無線 LAN アダプタの正当な能力検証です。数値は 2026-11-16～11-18 の実機テストレポートから引用しており、第三者のネットワークを対象とするものではなく、攻撃の操作手順も提供しません。テスト実施：Yopitek（ALFA Network 台湾代理店）— https://www.yupitek.com*
