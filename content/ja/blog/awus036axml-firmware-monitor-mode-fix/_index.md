---
title: "AWUS036AXML モニターモード ファームウェア修正：アクティブモードのクラッシュを解決する"
description: "Kali Linux で AWUS036AXML のモニターモード ファームウェアクラッシュを修正する方法。MT7921AUN ファームウェア更新、カーネルバージョン要件、アクティブ/パッシブモードの回避策、hcxdumptool の代替手段を解説。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
featureimage: "/images/blog/awus036axml-firmware-monitor-mode-fix.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "AWUS036AXMLがアクティブモニターモードでクラッシュするのはなぜですか？"
    answer: "MT7921AUNはファームウェアベースMACアーキテクチャを採用し、現在のLinux mt7921uドライバーとファームウェアの組み合わせがアクティブインジェクションに必要なコマンドパスを完全に実装していないため、aireplay-ng実行後にインターフェースが消滅します。"
  - question: "MT7921AUNのアクティブモードクラッシュをどう修復しますか？"
    answer: "firmware-misc-nonfreeパッケージを最新版に更新、カーネル6.6以上にアップグレード、高パケットレートのdeauthフラッドを回避することで改善できますが、完全にクラッシュを排除できるとは限りません。"
  - question: "hcxdumptoolはパケットインジェクションなしでPMKIDをどうキャプチャしますか？"
    answer: "hcxdumptoolはパッシブモードでアクセスポイントがブロードキャストするビーコンとプローブパケットからPMKIDをキャプチャし、まったくパケットを送信しないためファームウェアクラッシュを引き起こしません。"
  - question: "AWUS036AXMLのパッシブモニタリングにはどんな制限がありますか？"
    answer: "パッシブモニタリングではビーコン、ハンドシェイク、PMKIDを正常にキャプチャできますが、deauth、プローブリクエスト、アソシエーションフラッドなどのアクティブ操作は実行できず、これらはAWUS036ACHで処理する必要があります。"
  - question: "MT7921AUNの安定性を改善できるカーネルバージョンは？"
    answer: "カーネル6.1 LTS以降に複数のmt7921u安定性パッチが含まれ、カーネル6.6以降にはMediaTek USBドライバースタックの追加改善が含まれています。"
---

**ALFA AWUS036AXML** は ALFA Network のフラッグシップ WiFi 6E アダプターで、MediaTek MT7921AUN チップセットを搭載し、トライバンド（2.4 / 5 / 6 GHz）をサポートしています。2026 年時点で、6 GHz 帯でのパッシブモニタリングが可能な数少ない USB アダプターの一つです。サイトサーベイ、パケットキャプチャ、PMKID 収集などのユースケースでは非常に優れたパフォーマンスを発揮します。


{{< tldr >}}
AWUS036AXMLのmt7921uドライバーはアクティブパケットインジェクション時にファームウェアクラッシュを引き起こします。本記事では根本原因、診断手順、ファームウェア更新、カーネルアップグレード、hcxdumptoolによるパッシブキャプチャへの切り替えなどの修復方案を説明します。
{{< /tldr >}}
しかし、ユーザーを困惑させる既知の問題があります：**アクティブモニターモードのコマンドがファームウェアをクラッシュさせる**のです。`aireplay-ng` や `mdk4` などのツールを実行すると、`wlan0mon` インターフェースが完全に消え、アダプターを抜き差しするまで復旧できません。これはハードウェアの欠陥ではなく、現在の Linux `mt7921u` ドライバーとファームウェアの制限です。

本ガイドでは根本原因を説明し、診断手順と具体的な修正・回避策を提供します。

---

## 問題の説明：アクティブモニターモードのクラッシュ

### 症状

モニターモードを有効にして `aireplay-ng --test wlan0mon` などのアクティブコマンドを実行すると、`wlan0mon` インターフェースが `ip link` および `iwconfig` の出力から消えます。アダプターは応答不能となり、物理的に抜き差しするまで復旧できません。場合によっては、クラッシュ直後の `dmesg` にファームウェアエラーまたはリセットイベントが表示されます。

パッシブ操作（`airodump-ng` によるスキャン、生フレームのキャプチャ）は、アクティブインジェクションがトリガーされる前後も正常に動作します。

### 根本原因

**MT7921AUN チップセット**はファームウェアベースの MAC アーキテクチャを採用しています。Linux カーネルの `mt7921u` ドライバーは、モニターモードでのフレームインジェクションを含む一部の低レベル操作を処理するために、チップセットの組み込みファームウェアに依存しています。現在のファームウェアとドライバーの組み合わせは、Linux のモニターモードにおけるアクティブインジェクションに必要なコマンドパスを完全には実装していません。

一方、**パッシブモニタリング**（空中にある既存のフレームを受信するだけ）はファームウェアに何も送信させる必要がなく、クラッシュをトリガーしません。問題は送信パス操作に限定されます：デオーセンティケーションフレーム、プローブリクエスト、アソシエーションフラッドなどのアクティブ操作です。

{{< alert "triangle-exclamation" >}}
**既知のファームウェアクラッシュバグ。** これは 2026 年初頭時点の Linux `mt7921u` ドライバーで確認されている問題で、AWUS036AXML および他の MT7921AUN ベースの USB アダプターに影響します。将来のカーネルまたはファームウェアのアップデートで修正される可能性があります——最新状況は[ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/)を参照してください。
{{< /alert >}}

---

## 診断：この問題に該当するか確認する

以下の手順を実行して、MT7921AUN のアクティブモードクラッシュであることを確認してください：

```bash
# アダプターが認識されているか確認
lsusb | grep -i mediatek

# ドライバーがロードされているか確認
lsmod | grep mt7921u

# カーネルバージョンを確認（5.18 以上が必要）
uname -r

# モニターモードを開始
sudo airmon-ng start wlan0

# パッシブキャプチャをテスト（正常動作するはず）
sudo airodump-ng wlan0mon

# アクティブインジェクションをテスト（クラッシュする可能性あり）
sudo aireplay-ng --test wlan0mon
```

`aireplay-ng --test` 後にアダプターが `ip link` から消えた場合、ファームウェアクラッシュバグを確認できました。

カーネルログによる追加検証：

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

aireplay-ng コマンドの直後に `mt7921u: firmware crash`、`mt7921u: chip reset`、または `usb disconnect` などのメッセージが表示されていれば、ファームウェアレベルの障害が確認されます。

{{< alert "circle-info" >}}
**パッシブキャプチャは影響を受けません。** `airodump-ng` は正常動作するが `aireplay-ng` でクラッシュする場合、これはまさに既知の MT7921AUN バグです。以下の修正手順に進んでください。
{{< /alert >}}

---

## 修正方法 1：ファームウェアパッケージを更新する

最も効果的な最初のステップは、最新の MT7921 ファームウェアファイルを確保することです。古いファームウェアバージョンはクラッシュが発生しやすく、更新されたファームウェアは一部のアクティブ操作の安定性を改善します。

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# または linux-firmware リポジトリから最新の mt7921 ファームウェアを手動インストール
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

ファームウェアファイルを更新した後、ドライバーをリロードしてアクティブモードを再テスト：

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

---

## 修正方法 2：最新カーネルを使用する

`mt7921u` ドライバーはアップストリームの Linux カーネルで積極的にメンテナンスされています。5.18 以降、安定性のパッチ、ファームウェアコマンド処理、モニターモードの改善がカーネルアップデートに含まれています。新しいカーネルを実行することが、動作を改善する最も確実な方法の一つです。

現在のカーネルバージョンを確認：

```bash
uname -r
```

Kali Linux で最新のカーネルに更新：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

目標：最も完全な `mt7921u` ドライバーパッチを得るために**カーネル 6.1 LTS 以降**を使用。カーネル 6.6 以降には MediaTek USB ドライバースタックの追加改善が含まれており、ユーザーからの肯定的な報告があります。

{{< alert "circle-info" >}}
**カーネル 6.6+ の改善。** 複数のコミュニティ報告によると、カーネル 6.6 と更新されたファームウェアを組み合わせることで、MT7921AUN のアクティブモードクラッシュが減少（ただし必ずしも完全に解消されるわけではない）することが確認されています。アップグレード後に診断手順を再実行して、お使いの特定の組み合わせを評価してください。
{{< /alert >}}

---

## 回避策：hcxdumptool を使用する（パッシブ PMKID キャプチャ）

ファームウェアレベルの修正でクラッシュが完全に解決しない場合、`hcxdumptool` はフレームインジェクションを一切必要としない効果的な代替ワークフローを提供します。

`hcxdumptool` は**パッシブモード**で動作し、アクセスポイントがブロードキャストするビーコンおよびプローブフレームから直接 PMKID 値をキャプチャします。デオーセンティケーションフレームの送信なし、インジェクションなし、ファームウェアクラッシュなしです。AWUS036AXML はこのワークフローを完璧にこなします。

```bash
sudo apt install hcxdumptool hcxtools

# パッシブキャプチャ — デオーセンティケーション不要、ファームウェアクラッシュなし
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# hashcat 形式に変換
hcxpcapngtool -o hash.hc22000 capture.pcapng

# hashcat でクラック
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

このワークフローはビーコンフレームから PMKID をキャプチャし、何も送信しません——無線メディアの観点から完全にパッシブです。

{{< alert "circle-info" >}}
**PMKID キャプチャはすべての現代の WPA2/WPA3 ネットワークで有効です。** アクセスポイントはクライアントが関連付けられているかどうかに関わらず、ビーコンフレームで PMKID をブロードキャストします。AP の範囲内にいるだけでよく、クライアントは不要です。デオーセンティケーションが選択肢にない場合に最適です。
{{< /alert >}}

---

## 回避策：アクティブインジェクションには AWUS036ACH を使用する

アクティブフレームインジェクションが本当に必要なタスク（強制 WPA ハンドシェイクキャプチャ、WPS 列挙など）には、**AWUS036ACH**（RTL8812AU チップセット）が Kali Linux で成熟した、十分にテスト済みのドライバーサポートを持つ確立されたソリューションです。

推奨のデュアルアダプター プロフェッショナルセットアップ：

- **AWUS036AXML** → 5 GHz / 6 GHz のパッシブスキャンとキャプチャ
- **AWUS036ACH** → 2.4 GHz / 5 GHz のアクティブインジェクション

この組み合わせにより、インジェクションは長年安定している RTL8812AU が担い、AWUS036AXML は 6 GHz 探索と高品質なパッシブキャプチャを担当します。

[AWUS036AXML レビュー](/ja/blog/awus036axml-wifi-6e-review/)と[パケットインジェクションガイド](/ja/blog/packet-injection-guide/)で両アダプターの設定詳細を参照してください。

---

## アクティブモードが機能する場合

MT7921AUN のアクティブモードで安定した、または安定に近い動作が報告されている条件があります：

- **カーネル 6.6 以降** と firmware-misc-nonfree 20240610 以降の組み合わせ
- `aireplay-ng --deauth` のバーストモード使用を避ける（高パケットレートのデオーセンティケーションフラッドは単一フレーム操作よりもクラッシュを引き起こしやすい）
- 継続的なデオーセンティケーションストリームではなく `--deauth 1` または `--deauth 3` を使用
- アダプターを USB 3.0 ポートに接続する（USB 2.0 の帯域幅制限はファームウェアコマンドパイプラインに負担をかける）
- 5 GHz よりも 2.4 GHz でインジェクション操作を実行する（一部のドライバーバージョンでは低周波帯の方が安定しているように見える）

{{< alert "triangle-exclamation" >}}
**本番エンゲージメント前にテストしてください。** アクティブモードが正常に見えても、MT7921AUN ファームウェアは負荷時に操作中にクラッシュする可能性があります。アクティブ操作に AWUS036AXML を使用する場合は、常に回復計画（バックアップアダプターまたはパッシブオンリーワークフロー）を用意してください。
{{< /alert >}}

---

## ファームウェアが更新されているか確認する

```bash
# 現在のファームウェアファイルの日付を確認
ls -la /lib/firmware/mediatek/mt7921*

# ドライバーバージョンを確認
modinfo mt7921u | grep -E "version|filename"

# カーネルメッセージでファームウェアのロード状況を確認
sudo dmesg | grep mt7921
```

ファームウェアの正常ロード時、`dmesg` 出力には以下のような内容が表示されるはずです：

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

---

## まとめ：AWUS036AXML の最適なユースケース

- ✅ **パッシブ WiFi 6E スキャンと PCAP キャプチャ** — 完璧に動作
- ✅ **hcxdumptool PMKID キャプチャ** — インジェクション不要、ファームウェアクラッシュなし
- ✅ **6 GHz ネットワーク探索** — airodump-ng による 6 GHz 帯パッシブスキャン
- ✅ **WiFi 6E サイトサーベイと干渉分析** — トライバンドパッシブモニタリング
- ✅ **ベースライン WPA2 ハンドシェイクキャプチャ** — 既存トラフィックからのパッシブキャプチャ
- ⚠️ **アクティブフレームインジェクション** — ファームウェアが成熟するまで AWUS036ACH を使用
- ⚠️ **デオーセンティケーションフラッド** — クラッシュリスクあり；カーネル 6.6+ で慎重にテスト
- ⭐ **最適ワークフロー：AWUS036AXML + AWUS036ACH の両方を携帯**して全バンド全機能をカバー

---


---

{{< faq >}}

## 関連ガイド

- [AWUS036AXML 完全レビュー](/ja/blog/awus036axml-wifi-6e-review/)
- [パケットインジェクションガイド](/ja/blog/packet-injection-guide/)
- [ドライバーインストールガイド](/ja/blog/install-alfa-driver-kali-ubuntu/)

---

## 参考文献

1. [Linux firmwareリポジトリ（kernel.org）](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git)
2. [Linuxカーネルmt76ドライバー](https://wireless.wiki.kernel.org/en/users/drivers/mediatek)
3. [aircrack-ngツールスイート](https://www.aircrack-ng.org/)
4. [hcxdumptool GitHubプロジェクト](https://github.com/ZerBea/hcxdumptool)
5. [ALFA Network公式サポート](https://www.alfa.com.tw/)
