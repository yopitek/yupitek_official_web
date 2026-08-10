---
title: "Kali Linux 2026 モニターモード有効化完全ガイド：WiFi アダプター設定手順"
description: "Kali Linux 2024/2025 で airmon-ng または iw コマンドを使ってモニターモードを有効化する手順を解説。対応 ALFA アダプター一覧、トラブルシューティング、airodump-ng での確認方法付き。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["モニターモード", "Kali-Linux", "airmon-ng", "iw", "WiFiアダプター", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "モニターモードと管理モードの違いは？"
    answer: "モニターモードはアダプターが空中のすべての802.11フレームをキャプチャできるようにし、管理モードのように自身のMACに合致するパケットのみを受信する制限を受けません。無線ペネトレーションテストの基礎です。"
  - question: "airmon-ngとiwコマンドでモニターモードを有効にする違いは？"
    answer: "airmon-ngは干渉プロセスを自動的に処理しwlan0mon仮想インターフェースを作成します。iwは既存のインターフェースを直接変更し、別のインターフェースを作成しないため、きめ細かい制御が必要な場合に適しています。"
  - question: "モニターモード有効化後にインターフェースが自動的に管理モードに戻るのはなぜですか？"
    answer: "wpa_supplicantまたはNetworkManagerがバックグラウンドで再起動したのが原因です。airmon-ng check killを実行してこれらのプロセスを終了すれば解決します。"
  - question: "Kali Linuxで完全にモニターモードをサポートするALFAアダプターは？"
    answer: "AWUS036ACH（RTL8812AU）、AWUS036AXML（MT7921AUN）、AWUS036ACM（MT7612U）の3機種が完全サポートし、その中でACMはプラグアンドプレイです。"
  - question: "airodump-ngでFixed channel wlan0mon: -1エラーが出た場合の解決方法は？"
    answer: "airodump-ngがチャネルを切り替えられないことを示しています。iwconfig wlan0mon channel 1でチャネルを指定し、残留するwpa_supplicantプロセスを終了してください。"
---
モニターモードは、無線 NIC（ネットワークインターフェースカード）の特殊な動作モードで、アダプターが電波上の**すべての** 802.11 フレームをキャプチャできるようにします——自分のデバイス宛てのものだけでなく。通常の「マネージド」モードでは、アダプターは自分の MAC アドレス宛のパケットのみ受信し、それ以外はすべて破棄します。モニターモードはそのフィルターを完全に解除します。

## モニターモードとは？ペネトレーションテストにおける重要性


{{< tldr >}}
モニターモードはアダプターが自身のパケットのみを受信する制限を解除し、無線ペネトレーションテストの基盤です。airmon-ngまたはiwコマンドとALFAアダプターを組み合わせればKali Linuxで安定して有効化できます。
{{< /tldr >}}
無線ペネトレーションテスターにとって、モニターモードは基礎中の基礎です。これなしでは **airodump-ng**、**Wireshark**（無線キャプチャモード）、**Kismet** などのツールでネットワークトラフィックを受動的に傍受することができません。モニターモードが実現できること：

- **パッシブ偵察**——フレームを一切送信せずに周辺のすべての AP とクライアントをスキャン。
- **ハンドシェイクキャプチャ**——クライアント認証時の WPA/WPA2 の 4 ウェイハンドシェイクを待ち受ける。
- **デオーセンティケーション攻撃**——802.11 管理フレームの送信（モニターモードに加えてパケットインジェクションが必要）。
- **不正 AP 検出**——ネットワーク上の未許可アクセスポイントを特定。
- **プロトコル解析**——802.11 の管理・制御・データフレームの詳細な検査。

すべての無線アダプターがモニターモードに対応しているわけではありません。この機能は**チップセット**とカーネルにコンパイルされた**ドライバー**によって決まります。家庭用に販売されている一般的なアダプターはほぼ対応していません。セキュリティ調査向けに販売されている ALFA Network の製品は、モニターモードをクリーンに公開するチップセットとドライバーで構成されています。

---

## 前提条件

モニターモードを有効化する前に、以下を確認してください：

1. 対応カーネルを搭載した **Kali Linux**（2024.1 以降推奨）を実行している。
2. 無線アダプターが接続されている（USB アダプター）または取り付けられている（PCIe/mini-PCIe）。
3. **root または sudo** 権限がある。
4. インターフェース名を確認済み：`ip link` または `iwconfig` を実行し、無線インターフェース（一般的に `wlan0`、`wlan1`、または `wlx...`）を確認。

```bash
ip link show
```

`wlan` で始まる、または `wlx` で始まる長い MAC ベースの名前のエントリを探してください。

---

## 方法 1：airmon-ng でモニターモードを有効化

`airmon-ng` は **aircrack-ng** スイートの一部で、Kali Linux でモニターモードを切り替える最も一般的なツールです。モード切り替えを妨害するプロセスの停止を含む多くのエッジケースを自動的に処理します。

### ステップ 1 — 干渉するプロセスを停止する

NetworkManager、wpa_supplicant、dhclient はモニターモードと競合します。まずこれらを停止します：

```bash
sudo airmon-ng check kill
```

期待される出力：

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **注意：** これにより既存のネットワーク接続が切断されます。テスト中にインターネット接続が必要な場合は、有線接続か、マネージドモードの第 2 無線アダプターを使用してください。

### ステップ 2 — モニターモードを開始する

```bash
sudo airmon-ng start wlan0
```

期待される出力：

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

アダプターがモニターモードになり、新しい仮想インターフェース——通常は **wlan0mon**——が作成されます。

### ステップ 3 — チャンネルを固定する（任意だが推奨）

デフォルトではアダプターはチャンネルをホッピングします。特定のターゲットをキャプチャするためにチャンネルを固定します：

```bash
sudo iwconfig wlan0mon channel 6
```

---

## 方法 2：iw コマンドでモニターモードを有効化

`iw` コマンドは最新の低レベル無線設定ユーティリティです。この方法はより直接的な制御が可能で、`airmon-ng` が利用できない場合や動作が不安定な場合に役立ちます。

```bash
# インターフェースをダウンにする
sudo ip link set wlan0 down

# モニターモードに設定
sudo iw dev wlan0 set type monitor

# インターフェースを再度アップにする
sudo ip link set wlan0 up
```

3 コマンドをまとめて実行：

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

この方法は `wlan0mon` という新しいインターフェースを作成するのではなく、既存の `wlan0` インターフェース自体を変更します。変更が適用されたか確認します：

```bash
iw dev wlan0 info
```

出力に `type monitor` が表示されていれば成功です。

---

## モニターモードの確認

### iwconfig を使う

```bash
iwconfig
```

モニターモードのインターフェースは次のように表示されます：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

重要なのは **Mode:Monitor** という表示です。

### iw dev を使う

```bash
iw dev
```

インターフェースのエントリの下に `type monitor` があるか確認します。`type managed` と表示された場合、モニターモードは正しく適用されていません。

---

## airodump-ng でテストする

モニターモードが有効になったら、`airodump-ng` でエンドツーエンドのテストを行います：

```bash
sudo airodump-ng wlan0mon
```

周辺のアクセスポイントのリストが画面にスクロール表示されるはずです——BSSID、チャンネル、電波強度（PWR）、暗号化タイプ、ESSID が表示されます。画面が空白またはエラーが表示される場合は、後述のトラブルシューティングを参照してください。

5 GHz 帯のみをスキャンするには：

```bash
sudo airodump-ng --band a wlan0mon
```

特定のネットワークをキャプチャして後で分析するために保存するには：

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## ALFA アダプター対応表

[ALFA Network](/ja/products/alfa/) アダプターは Kali Linux 無線テストの業界標準です。次のモデルはモニターモードを完全にサポートしています：

| モデル | チップセット | バンド | モニターモード | インジェクション | 備考 |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | ペネトレーションテストで最も人気 |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E、カーネル 5.18+ が必要 |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | 優れた Linux ドライバーサポート |

上記のすべてのモデルは Kali Linux 2024.x および 2025.x でのドライバーサポートが確認されています。RTL8812AU などのチップセットでは、カーネルバージョンが非常に新しい場合、Aircrack-ng の GitHub リポジトリからドライバーをインストールする必要があるかもしれません。

---

## トラブルシューティング

### 「モニターモードを有効化できない」またはインターフェースが消える

NetworkManager がインターフェースを再取得する際によく起こります。`airmon-ng check kill` を再度実行してからリトライしてください。問題が続く場合は、NetworkManager を手動で停止します：

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### モニターモードがマネージドモードに戻る

一部のドライバーは数秒後に自動的にマネージドモードにリセットされます。これは通常、wpa_supplicant がバックグラウンドで再起動したことを意味します。実行中のプロセスを確認します：

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

見つかったプロセスを PID で停止し、モニターモードを再有効化します。

### airmon-ng 後にインターフェース名が変わる

システムによっては、新しいインターフェースが `wlan0mon`、`mon0`、または別の名前になることがあります。airodump-ng で使用する前に、`airmon-ng start` の実行後に必ず `iwconfig` または `iw dev` で実際のインターフェース名を確認してください。

### airodump-ng で「Fixed channel wlan0mon: -1」エラー

airodump-ng がチャンネルを変更できないことを意味します。試してみてください：

```bash
sudo iwconfig wlan0mon channel 1
```

それでも失敗する場合は、残っている wpa_supplicant プロセスを停止してリトライしてください。

### 新しいカーネルでの RTL8812AU ドライバーの問題

最新のカーネルのカーネル内蔵 RTL8812AU ドライバーは、モニターモードのサポートが不完全な場合があります。コミュニティドライバーをインストールしてください：

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

インストール後に再起動します。

---

## テスト終了後にモニターモードを無効化する

テストが終わったら、必ずアダプターをマネージドモードに戻してください。モニターモードのままでは通常のネットワーク接続ができません。

### airmon-ng を使う場合：

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### iw を使う場合：

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

`iwconfig` でインターフェースがマネージドモードに戻ったことを確認し、ネットワークに再接続します。

---


---

{{< faq >}}

## まとめ

Kali Linux でモニターモードを有効化するのは 2 ステップです：干渉するサービスを停止し、`airmon-ng` または `iw` のどちらかを使ってインターフェースモードを切り替える。成功の鍵は対応チップセットを持つアダプターを使うことです。RTL8812AU、MT7921AUN、MT7612U のチップセットを持つ ALFA Network アダプターは、Kali Linux で最も信頼できるすぐに使える体験を提供します。

Yopitek（台湾の ALFA Network 正規代理店）の [ALFA Network 無線アダプター製品ラインナップ](/ja/products/alfa/)で、ワイヤレスセキュリティ調査に最適なアダプターをお探しください。

---

## 参考文献

1. [aircrack-ng公式ドキュメント](https://www.aircrack-ng.org/documentation.html)
2. [Kali Linux公式ドキュメント](https://www.kali.org/docs/)
3. [Linux Wireless mac80211サブシステム](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
4. [iwコマンド使用説明](https://wireless.wiki.kernel.org/en/users/Documentation/iw)
