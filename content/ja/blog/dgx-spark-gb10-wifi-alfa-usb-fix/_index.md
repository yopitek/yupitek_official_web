---
title: "DGX SparkのWi-Fiが繋がらない？ALFA USB無線アダプターで10分解決"
description: "NVIDIA DGX Sparkの内蔵Wi-Fi問題を、ドライバー不要のALFA USB無線アダプターで10分で解決する方法を解説します。ASUS GX10で実機検証済みで、他のGB10機種でも同様に使える見込みです。"
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["dgx-spark", "gb10", "ai-server", "wifi", "alfa-network", "tutorial", "asus-ascent-gx10", "msi-edgexpert", "hp-zgx-nano", "altos-brainsphere", "gigabyte-ai-top-atom"]
featureimage: "/images/blog/dgx-spark-gb10-wifi-alfa-usb-fix.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "DGX SparkのWi-Fiがつながらないのはなぜですか？"
    answer: "DGX Spark内蔵のMediaTek MT7925 Wi-Fi 7チップはOOBE段階のwpa_supplicantが過度に簡素化されており、特定ブランドのAP（特にUniFi）と非互換で、WPA2-Enterpriseはほぼ確実に接続できません。"
  - question: "ALFA USBアダプターの解決策はすべてのGB10 AI Serverに適用されますか？"
    answer: "適用されます。NVIDIA GB10 Grace Blackwell Superchipを搭載するすべてのAI Edge Server（ASUS、MSI、HP、ALTOS、GIGABYTE）は同じMT7925 Wi-Fiチップを使用しているため、ALFA AWUS036ACMの解決策はすべてに共通すると見込まれます（実機テストはASUS GX10のみで、他の機種は個別にテストしていません）。"
  - question: "AWUS036ACMはDGX Sparkでドライバーインストールが必要ですか？"
    answer: "不要です。MT7612Uのmt76ドライバーはLinux Kernel 4.19以降カーネルメインラインに内蔵され、DGX OSのKernel 6.17+が自然に完全サポートし、USB挿入で自動的に読み込まれます。"
  - question: "ALFA USBアダプターでWi-Fi問題を修復するのにどのくらいかかりますか？"
    answer: "10分以内です。USB-C→USB-A変換アダプターを介してGX10のUSB-Cポートに接続後、システムが自動的にドライバーを読み込み、nmcliコマンドでスキャンしてWiFiに接続するだけで完了し、ドライバーコンパイルや再起動は不要です。"
  - question: "DGX Sparkで他のALFAアダプターを使えますか？"
    answer: "使えます。ASUS GX10（GB10、Ubuntu 24.04 ARM64、kernel 6.17）でALFA現行9機種を実機テストしたところ、すべてkernel内蔵ドライバーで動作し、挿すだけで使用でき、DKMSは不要でした。AWUS036ACHは内蔵のrtw88_8812auを使用します。ただしAWUS036AXM / AXMLはstock kernel 6.17上でパケットインジェクションに失敗するため、接続とAP用途にのみ適しています。他のGB10機種は個別にテストしていません。"
---

待ちに待った **NVIDIA DGX Spark**（コードネーム Project DIGITS）がついに届いた。

> 📌 本記事は2026年11月のGX10実機テストに基づいて更新しました：ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）では、ALFA現行9機種のアダプターがすべてkernel内蔵ドライバーで動作し、挿すだけで使用でき、DKMSは不要です。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)をご覧ください。テストはGX10のみで実施しており、他のGB10機種は個別にテストしていません。


{{< tldr >}}
NVIDIA DGX SparkおよびすべてのGB10 AI Serverの内蔵MT7925 Wi-Fi 7チップには既知の接続不良があります。解決策はALFA AWUS036ACM USBアダプターを挿入することで、mt76ドライバーはKernel 4.19以降カーネルに内蔵、DGX OS Kernel 6.17+でプラグアンドプレイ、10分で接続完了します。
{{< /tldr >}}
開梱して電源を接続し、OOBE（初回セットアップ画面）が表示される——ここまでは順調だ。Wi-Fiネットワークを選択し、パスワードを入力、画面が30秒ほど回転して…

**「このネットワークに接続できません。」**

もう一度試す。再起動。リセット。それでも失敗。

あなただけではない。[NVIDIA Developer Forums](https://forums.developer.nvidia.com) には、DGX SparkのWi-Fi故障を訴える**数十のスレッド**が立ち上がっている。

これは設定ミスではない。DGX Sparkの既知の設計上の欠陥だ。

---

## 根本原因：DGX SparkのWi-Fiが信頼できない理由

DGX Spark（および **NVIDIA GB10 Grace Blackwell Superchip** を搭載するすべてのAIサーバー）は、**MediaTek MT7925 Wi-Fi 7チップ**を内蔵している。仕様上は最高クラスのハードウェアだ。

問題はソフトウェア層にある。

### 3つの致命的な欠陥

**① OOBEのWi-Fi supplicantが過度に簡略化されている**

DGX Sparkの初回セットアップでは、最小限の `wpa_supplicant` が使用される。このバージョンでは多くのエンタープライズ認証機能が削除されており、特定ブランドのAP（特にUbiquiti UniFi）とのassociationが完全に失敗する。

NVIDIAは **DGX Spark Release Notes（2026年4月更新）** でこの問題を正式に認めているが、本稿執筆時点では未修正のままだ。

**② WPA2-Enterpriseに非互換**

オフィスやラボがWPA2-Enterprise（企業環境で一般的）を使用している場合、DGX Sparkの内蔵Wi-Fiはほぼ確実に接続できない。これは設定ファイルで解決できる問題ではない——ドライバ層とsupplicantの二重の制限だ。

**③ ランダムな「No Wi-Fi Adapter Found」エラー**

NVIDIAフォーラム（スレッド #356183）では、DGX Sparkが通常使用中に突然「ワイヤレスアダプターが見つかりません」と表示され、完全な再起動が必要になると複数のユーザーが報告している。さらに悪いことに、**切断後もシステムは自動再接続しない**——手動で `nmcli` コマンドを実行する必要がある。

| 問題 | 影響 |
|------|------|
| OOBEがエンタープライズAPに接続不可 | UniFi / WPA2-Enterpriseは全滅 |
| ランダムな「No Wi-Fi Adapter Found」 | 再起動必須、開発ワークフロー中断 |
| 切断後の自動再接続なし | リモート管理が不可能に |
| Release Notesが問題を認めている | NVIDIA公式確認、個別事象ではない |

> 💡 **朗報：これらのソフトウェア問題は短期間では完全解決しないが、ハードウェアによる簡単・安定・完全互換の解決策がある。**

---

## DGX Sparkだけじゃない——すべてのGB10 AI Edge Serverが同じWi-Fiチップを共有

DGX Sparkが注目を集めているのは、単にNVIDIA自社ブランドで最初に出荷されたからだ。しかし実際には、**NVIDIA GB10 Grace Blackwell Superchipを搭載するすべてのAI Edge Server**が、まったく同じ**MediaTek MT7925 Wi-Fi 7チップ**を使用している——同じドライバスタック、同じ`wpa_supplicant`の制限、同じ互換性問題だ。

現在市場で入手可能なGB10 AI Edge Serverは6機種ある：

### GB10 AI Edge Server 全機種スペック比較

全機種が以下のコアスペックを共有する：

| コンポーネント | 仕様 |
|----------|------|
| Superchip | **NVIDIA GB10 Grace Blackwell** |
| CPU | **20-core Arm**（10× Cortex-X925 + 10× Cortex-A725） |
| GPU | **NVIDIA Blackwell GPU**、第5世代Tensor Cores / 第4世代RT Cores |
| AI性能 | **1 PFLOP FP4**（1000 TOPS AI） |
| システムメモリ | **128 GB LPDDR5x** ユニファイド、256-bit、273 GB/s帯域幅 |
| メモリ相互接続 | **NVLink-C2C**（PCIe 5.0の5倍の帯域幅） |
| NIC | **NVIDIA ConnectX-7** SmartNIC（200G × 2 QSFP） |
| イーサネット | **1× 10GbE RJ-45** |
| Wi-Fiチップ | **MediaTek MT7925** Wi-Fi 7（2×2） |
| ディスプレイ出力 | **1× HDMI 2.1a** |
| OS | **NVIDIA DGX OS**（Ubuntu Linuxベース） |
| 電源 | **240W** USB-C外部アダプター |
| 2台スタッキング | 対応（最大405Bパラメータモデル） |

各ブランドの差異は以下の通り：

| 項目 | **ASUS ASCENT GX10** | **MSI EdgeXpert** | **NVIDIA DGX Spark** | **HP ZGX Nano G1n** | **ALTOS BrainSphere GB10 F1** | **GIGABYTE AI TOP ATOM** |
|------|----------------------|-------------------|----------------------|---------------------|------------------------------|--------------------------|
| ストレージ | 1TB / 2TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 4TB NVMe | 1TB / 2TB / 4TB NVMe | 4TB NVMe | 1TB / 4TB NVMe（Gen5最大） |
| Wi-Fiモジュール | AW-EM637（Wi-Fi 7） | Wi-Fi 7 | Wi-Fi 7 | MT7925（Wi-Fi 7） | Wi-Fi 7 | Wi-Fi 7 |
| Bluetooth | BT 5.4 | BT 5.3 | BT 5.4 | BT 5.4 | BT 5.4 LE | BT 5.4 |
| USB | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Type-C | 4× USB Type-C | 4× USB Type-C | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Gen 2×2 Type-C |
| 寸法 | 150×150×51mm | 151×151×52mm | 150×150×50.5mm | 150×150×51mm | 150×150×50mm | 150×150×50.5mm |
| 重量 | 1.48 kg | 1.2 kg | 1.2 kg | 1.25 kg | < 1.5 kg | 1.2 kg |
| 付属ソフトウェア | — | — | — | HP ZGX Toolkit | Altos aiGeniプラットフォーム | — |

> ⚠️ **結論**：どのGB10 AI Edge Serverを購入しても、内蔵Wi-Fiは同じMediaTek MT7925チップであり、すべてが同じ接続問題に遭遇する可能性がある。以下のALFA USBアダプターによる解決策は、**6機種すべてで有効と見込まれる**（実機テストはASUS GX10のみで、他の機種は個別にテストしていない）。

---

## 解決策：USB無線アダプター1枚、10分で完了

NVIDIAが公式テストしているのはDGX OS（Ubuntu 24.04ベース）のみ。**すべてのGB10プラットフォームはARM64（aarch64）アーキテクチャ**で、Kernelは**バージョン6.17以上**。

つまり、必要なUSB無線アダプターは以下の3条件を満たす必要がある：

1. ✅ **Linux Kernel組み込みドライバ**——コンパイル不要、DKMS不要
2. ✅ **ARM64 (aarch64) 完全サポート**——GB10でプラグアンドプレイ
3. ✅ **実績のある安定性**——コミュニティで広く検証済み

ALFA現行9機種のUSBアダプターは、GX10で実測したkernel 6.17上ですべてこの3条件を満たす（GX10で実機テスト済み。記事末尾の「その他のALFAアダプター」を参照）。本記事では、管理用ネットワークに最も適したAWUS036ACMを例に説明する。

### 🥇 推奨：ALFA AWUS036ACM

| 項目 | 詳細 |
|------|------|
| チップセット | **MediaTek MT7612U** |
| ドライバ | **Linux Kernel組み込み mt76**（Kernel 4.19以降） |
| バンド | デュアルバンド 2.4GHz + 5GHz（AC1200） |
| アンテナ | 2× RP-SMA 着脱式 5dBi（高利得アンテナに交換可能） |
| インターフェース | USB 3.0 Type-A |
| モニターモード | ✅ 完全サポート |
| APモード | ✅ 対応 |
| TAA準拠 | ✅ 米国政府調達基準に適合 |

#### なぜこれなのか？6つの理由

**1. ドライバ不要・プラグアンドプレイ**

mt76ドライバはLinux Kernel 4.19以降メインラインに組み込まれている。DGX SparkのKernel 6.17はこれをネイティブにサポート。USBに挿せば、システムが**自動的にドライバをロード**する——インストールは一切不要。

**2. ARM64で実機検証済み**

MT7612Uは、Raspberry Pi OS（aarch64）、Ubuntu Server（ARM64）など、複数のARMプラットフォームで何年も実戦テストされてきた。GB10プラットフォームのASUS GX10（kernel 6.17）でも実機テストを行い、挿すだけで `mt76x2u` が自動ロードされ、パッチは一切不要だった。

**3. ゼロコンパイル・ゼロ設定**

mt76ドライバは長年メインラインに含まれているため、DGX OSのKernelを更新しても、ACMはそのまますぐ使える。（Realtek機種もkernel 6.17上ではコンパイル不要。最低バージョンは機種ごとに異なり、それより古い場合にのみDKMSが必要。）

**4. モニターモードとパケットインジェクションに対応**

DGX Spark上でKali Linux VMを動かしてセキュリティリサーチを行う場合、ACMはモニターモード、パケットインジェクション、仮想インターフェース（VIF）に対応している。GX10での実測インジェクション成功率は2.4GHz 63–83%、5GHz 76%。インジェクションが主な用途なら、AWUS036EACS、ACH（両バンド100%）のほうが性能は上だ。

**5. アンテナ交換が可能**

2本のRP-SMA着脱式アンテナ。標準で5dBiが付属し、7dBiや9dBiの高利得アンテナに交換可能——サーバールームや工場などWi-Fi電波の弱いエッジ展開に最適。

**6. TAA準拠**

組織が政府調達要件を持つ場合、ALFA AWUS036ACMは**TAA準拠**を取得した数少ない外付けUSB無線アダプターの一つ。

---

## 実践：10分で「無線なし」から「デュアルネットワーク」へ

DGX SparkでALFA AWUS036ACMを使用する完全な手順：

### ステップ1：USBアダプターを接続

DGX SparkのUSBポートはすべてUSB-Cなので、USB-C to USB-A変換アダプター（データ転送対応）を介してAWUS036ACMを挿入する。

ターミナルを開き、以下を実行：

```bash
dmesg | tail -20
```

以下のような出力が表示されるはず：

以下は AWUS036ACM を ASUS GX10（kernel 6.17.0-1014-nvidia）で実測した dmesg 出力です（MAC アドレスはマスク済み）：

```
usb 5-1: new high-speed USB device number 2 using xhci-hcd
usb 5-1: New USB device found, idVendor=0e8d, idProduct=7612, bcdDevice= 1.00
mt76x2u 5-1:1.0: ASIC revision: 76120044
mt76x2u 5-1:1.0: ROM patch build: 20141115060606a
mt76x2u 5-1:1.0: Firmware Version: 0.0.00
usbcore: registered new interface driver mt76x2u
mt76x2u 5-1:1.0 wlxXXXXXXXXXXXX: renamed from wlan0
```

**これがドライバが自動ロードされた合図だ。** 一切のインストールは行っていない。

### ステップ2：アダプターが認識されているか確認

```bash
nmcli device status
```

`wlan1`（または `wlx...`）が `disconnected` ステータスでリストに表示されるはず。

### ステップ3：Wi-Fiに接続

```bash
# 利用可能なネットワークをスキャン
nmcli device wifi list

# SSIDに接続 ("MyLabWiFi"を実際のものに置き換え)
sudo nmcli device wifi connect "MyLabWiFi" password "your-password"

# 接続状態を確認
nmcli connection show --active
```

### ステップ4：起動時の自動接続を有効化

前のステップが成功していれば、`nmcli` が自動的に接続プロファイルを保存する。以降の起動時に自動接続される。

プロファイルが保存されたか確認：

```bash
nmcli connection show
```

SSIDがリストに表示されれば——完了。USBを挿してから安定したWi-Fi接続まで、**合計10分もかからない**。

---

## これこそ真のAIサーバーネットワークアーキテクチャ

AWUS036ACMを導入すれば、DGX Sparkのネットワーク設定はプロ仕様の**デュアルネットワークアーキテクチャ**に格上げされる：

{{< mermaid >}}
%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#2d1f4e","primaryTextColor":"#e2d9f3","primaryBorderColor":"#7c3aed","lineColor":"#9d6dff","secondaryColor":"#1a1030","tertiaryColor":"#0e0818","background":"#0e0818","mainBkg":"#1e1040","nodeBorder":"#7c3aed","clusterBkg":"#150d2a","titleColor":"#c4b5fd","edgeLabelBackground":"#1a1030","attributeBackgroundColorEven":"#1e1040","attributeBackgroundColorOdd":"#150d2a"}}}%%
flowchart TD
    subgraph sub1["🌐 ネットワーク層"]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>モデルトレーニング · 大規模データ転送"]
        B["📡 ALFA AWUS036ACM<br/>SSH管理 · Jupyter · システム更新"]
    end

    C["🖥️ DGX Spark / GB10<br/>ARM64 | 128GB | 20コアCPU"]

    subgraph sub2["🎯 ユースケース"]
        D["🤖 AI開発者<br/>推論 + SSH 並行実行"]
        E["🔐 セキュリティラボ<br/>LLMトレーニング + 侵入テスト"]
        F["🚀 エッジ展開<br/>本番ネットワーク + 管理分離"]
    end

    A -->|高速データ| C
    B -->|管理リンク| C
    C --> D
    C --> E
    C --> F
{{< /mermaid >}}

**なぜトラフィックを分離するのか？**

AIモデルのトレーニングは膨大なネットワークトラフィックを生成する——事前学習済み重みのダウンロード、データセットの同期、分散トレーニング通信。これらをSSH管理と同じ回線に混在させると：

- SSHセッションが遅延またはタイムアウト
- 10GbEの広帯域が管理トラフィックに浪費される
- メイン接続が切断された場合（例：モデルダウンロードのハング）、リモート修正すらできない

分離すれば、**管理接続はモデルのワークロードに関係なく常に安定**する。

---

## 3つのシナリオ、1枚のアダプター

### シナリオA：AI開発者
```
10GbE → モデル推論, データ転送
ALFA ACM → SSH, Jupyter Notebook, システム更新
```

### シナリオB：セキュリティリサーチラボ（自分が所有する、または許可を得たネットワークに限る）
```
GB10 → LLMファインチューニング実行
Kali Linux VM → USBパススルー ALFA ACM → 無線侵入テスト
```

### シナリオC：エッジ展開（工場／倉庫）
```
10GbE → 本番ネットワーク
ALFA ACM + 高利得アンテナ → オフィス管理Wi-Fi
```

---

## よくある質問

**Q：AWUS036ACMのMT7612UとGB10内蔵のMT7925は同じMediaTekではないのか？**

A：同じメーカーだが、ドライバアーキテクチャはまったく異なる。MT7925は `mt7925e` ドライバを使用し、新しいPCIeインターフェースのドライバでまだ改良中。MT7612Uは `mt76` USBドライバを使用し、Kernel 4.19から成熟を重ねており非常に安定している。

**Q：このアダプターはDGX OS以外でも使えるか？**

A：もちろん。MT7612UドライバはLinux Kernelメインラインの一部であり、Ubuntu、Debian、Raspberry Pi OS、Kali Linux、Fedora、Arch Linux——Kernel 4.19以上ならすべてプラグアンドプレイ対応。

---

## その他のALFAアダプター：GX10での実機テスト結果

ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）でALFA現行9機種のアダプターを実機テストしたところ、すべてkernel内蔵ドライバーで動作し、挿すだけで使用でき、DKMSは不要だった。他のGB10機種（DGX Spark、MSI EdgeXpert、GIGABYTE AI TOP ATOM、ALTOS BrainSphere、HP ZGX Nano）は同じGB10とNVIDIA kernel系列を使用しているため同じ動作が見込まれるが、個別にはテストしていない。

| 機種 | チップ | 内蔵ドライバー | パケットインジェクション（GX10実測） | 適した用途 |
|------|------|----------|----------------------|----------|
| AWUS036ACM | MediaTek MT7612U | mt76x2u | ✅ 2.4G 63–83%／5G 76% | 管理用ネットワーク、AP、ペネトレーションテスト |
| AWUS036ACHM | MediaTek MT7610U | mt76x0u | ⚠️ 2.4G 96–100%／5G ブロードキャストのみ | 管理用ネットワーク、AP |
| AWUS036ACH | Realtek RTL8812AU | rtw88_8812au | ✅ 両バンド 100% | ペネトレーションテスト、長距離受信 |
| AWUS036ACS | Realtek RTL8811AU | rtw88_8821au | ✅ 2.4G 100%／5G 96% | ペネトレーションテスト、持ち運び |
| AWUS036EACS | Realtek RTL8821CU（Bluetooth搭載） | rtw88_8821cu | ✅ 両バンド 100% | ペネトレーションテスト |
| AWUS036AX | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 96% | Wi-Fi 6接続、AP |
| AWUS036AXER | Realtek RTL8832BU | rtw89_8852bu | ✅ 2.4G 73% | Wi-Fi 6接続、AP、監視時の受信 |
| AWUS036AXM | MediaTek MT7921AUN | mt7921u | ❌ 失敗 | 接続、APのみ |
| AWUS036AXML | MediaTek MT7921AUN | mt7921u | ❌ 失敗 | 接続、APのみ（6GHzは実機で動作確認） |

AWUS036AXM / AXMLはstock kernel 6.17上でパケットインジェクションに失敗する（monitor、AP、WPA3は使用可能）ため、ペネトレーションテストには適さない。各機種のドライバーがメインラインに入った最低kernelバージョンは異なり（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）、それより古い場合にのみコミュニティのDKMSドライバーが必要だ。詳細データは[ALFA 9機種 ARM64 実機テスト総まとめ](/ja/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)を参照。

---


---

{{< faq >}}

## まとめ：どのGB10でも、10分でオンラインに

NVIDIA DGX Spark、ASUS ASCENT GX10、MSI EdgeXpert、HP ZGX Nano、ALTOS BrainSphere GB10 F1、GIGABYTE AI TOP ATOM——どのGB10 AI Edge Serverを購入しても、これらは驚異的なAI開発マシンだ：128GBユニファイドメモリ、20コアARM CPU、ConnectX-7 200GbEネットワーク。しかし、すべてが同じMediaTek MT7925 Wi-Fiチップを共有しており、すべてが最初のステップでつまずく可能性がある。

ALFA AWUS036ACMの解決策は、ほとんど馬鹿げているほどシンプルだ：**USBに挿すだけ。**

しかし、その「シンプルさ」こそが真のエンジニアリング生産性だ——Wi-Fiドライバのデバッグに時間を費やすべきではない。モデルのトレーニングに時間を使うべきだ。

他のアプローチと比較すると、その優位性は明らかだ：

| アプローチ | 時間 | 信頼性 | メンテナンス |
|------|------|--------|---------|
| NVIDIAのWi-Fiドライバ修正を待つ | 不明（数ヶ月？） | 不確実 | 低 |
| Wi-Fiブリッジを購入 | 30分設定 | 中 | 中 |
| **ALFA AWUS036ACM** | **10分未満** | **最高** | **ゼロ** |

10分、USBアダプター1枚で、あなたのAIサーバーは本当の意味でオンラインになる。

---

> 📌 **ALFA AWUS036ACM 在庫あり** → [Yopitek製品ページ](/ja/products/alfa/awus036acm/)
>
> Yopitek Ltd は ALFA Network の台湾正規販売代理店です
> ご注文・技術的なお問い合わせ：sales@yupitek.com

---

*参考資料：NVIDIA DGX Spark Release Notes、NVIDIA Developer Forums、morrownr/USB-WiFi GitHub、ALFA Network Docs、Linux Kernel Wireless Documentation*

---

## 参考文献

1. [NVIDIA DGX Spark公式ドキュメント](https://developer.nvidia.com/dgx-spark)
2. [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFi GitHubプロジェクト](https://github.com/morrownr/USB-WiFi)
4. [Linux Kernel Wireless Documentation](https://wireless.wiki.kernel.org/)
5. [ALFA Network公式ウェブサイト](https://www.alfa.com.tw/)
