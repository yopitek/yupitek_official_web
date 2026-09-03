---
title: "ALFA無線ネットワークカードがTomatoをサポートしていますか？"
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "ハードウェアガイド"
description: "ALFA機型のTomato（含み衍生版）非推奨、USB WiFi非対応、OpenWrt推奨"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題要約

お客様の質問：「ALFAシリーズのUSBワイヤレスネットワークアダプターが、Tomato（FreshTomato / AdvancedTomatoを含む派生バージョンを含む）にアップグレードされたルーターで使用できるか？」

簡潔な結論：現在、ALFA全シリーズの現役モデルは、Tomato（含むFreshTomato / AdvancedTomatoなどの派生バージョン）においてドライバーサポートがなく、使用を全く推奨しません。Tomatoは、三大第三者製ルーターソフトウェアのうち、USB WiFiのサポートが最も弱いプラットフォームであり、開発の中心はBroadcomチップセットの内蔵WiFiに集中しています。ルーターの上でUSB WiFiネットワークアダプターを使用する必要がある場合は、OpenWrtに変更することをお勧めします。

判定対象：ALFAの現役9モデルのUSBネットワークアダプター（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 目標ソフトウェアの規格と要件の分析

### 2.1 Tomatoとは

Tomatoは、歴史のあるオープンソースルーター第三セクターファームウェアで、最初はJonathan Zarateによって開発され、その後多くの派生版が生まれました：

| 派生版 | 维護状況 | 支援プラットフォーム |
|---|---|---|
| 原版Tomato | 维護停止（2010年代初期） | Broadcom MIPSルーター |
| Tomato by Shibby | 维護停止 | Broadcom MIPS / ARM |
| AdvancedTomato | 维護停止 | Broadcom（Shibby派生版のGUI改版） |
| FreshTomato | 活躍維護中 | Broadcom MIPS / ARM（BCM47xx / BCM53xx） |
| Toastman Tomato | 维護停止 | Broadcom MIPS |

### 2.2 TomatoのUSB WiFiサポートフレームワーク

Tomatoの基本的な設計哲学は、「Broadcomルーターのために簡潔で安定した第三セクターファームウェアを提供する」というもので、USB機能は以下のようにサポートされています：

| USB機能種類 | 支援状況 |
|---|---|
| USBストレージデバイス（USBメモリ / ハードディスク） | ✅ 完全サポート（Samba / FTP / DLNA） |
| USBプリンター | ✅ 支援（p910nd / CUPS） |
| USB 3G/4Gデータモデム | ⚠️ 部分サポート |
| USB WiFiネットワークアダプター | ❌ 几乎サポートしていません |

Tomatoのカーネルは、Broadcomルーター内蔵のWiFiの閉源ドライバ（wlモジュール）をデフォルトでインクルードしており、USB WiFiドライバは一切インクルードされていません。また、Tomatoのパッケージ管理システム（ipkg / Optware）もUSB WiFiドライバのパッケージを提供していません。

### 2.3 鍵となる制限

- TomatoはBroadcomチップセットを搭載したルーターのみをサポートしており、BroadcomルーターのUSBポートは通常ストレージ / プリンターに使用されます
- FreshTomatoは維護が続いていますが、開発の焦点はBroadcomプラットフォームのバグ修正であり、USB WiFiドライバの追加は行われていません
- Tomatoのファイルシステムの空間は非常に小さい（通常4-16MB）ため、ドライバを手動で翻訳しようとしてもインストールする空間がありません
- Tomatoにはopkgなどの現代のパッケージ管理システムがなく、OpenWrtのようにkmodドライバを簡単にインストールすることはできません

## 3. 現在のALFAネットワークカード規格およびチップセットの分析

2026年9月現在、ALFA Networkの現役USB無線ネットワークカード製品ラインは以下の通りです（判定基準：9モデル）：

| 機型 | Wi-Fi レベル | チップセット | インターフェース | Tomato 驅動状態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ 無 |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ 無 |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 無 |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ 無 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ 無 |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ 無 |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ 無 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ 無 |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ 無 |

## 4. 対応機種とチップセット

### 4.1 Tomatoで利用可能な非常に古いALFA機種（生産終了）

| 機種 | チップセット | Linuxドライバモジュール | 説明 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 理論的には読み込めるが、Tomatoにはデフォルトで含まれていない；kernel moduleを自分でコンパイルする必要があり、実際の実現可能性は非常に低い |
| AWUS036H | Realtek RTL8187L | rtl8187 | 上記と同様、2.4GHz / 54Mbpsに限られ、生産終了から10年以上経過 |
⚠️ 上記の古い機種であっても、Tomato上ではユーザーが自分で対応するkernelバージョンのドライバモジュールをクロスコンパイルする必要があり、Tomatoのファイルシステムの空間は通常、インストールに十分ではありません。これは「サポート」とは言えず、「非常に高度なハック」となります。

### 4.2 Tomatoで完全に利用できない現行機種

第3節のテーブルに示されるすべての現行ALFA機種は、以下の理由でTomatoで利用できません。

- Realtekチップ（RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU）：Tomatoには対応するドライバがなく、パッケージ管理を通じてインストールすることもできません
- MediaTekチップ（MT7612U / MT7610U / MT7921AUN）：Tomatoにはmt76 / mt7921ドライバが含まれておらず、FreshTomato開発チームもこれを加える計画はありません
- lsusbでデバイスが見える場合（TomatoがUSBコアを有効にしている場合を除き）、USBブリッジレベルでの認識に留まり、ネットワークインターフェースを構築することはできません

## 5. 環境要求

現役のALFAモデルがTomato上で利用不可能であるため、本節では「若客戶が堅持して試みる」必要な極端な条件を以下に示します：

| 項目 | 需求 |
|---|---|
| ルーター機器 | Broadcomチップセットを搭載したUSB 2.0ポートを有するルーター、Flashメモリ32MB以上、RAMメモリ256MB以上 |
| Tomatoバージョン | FreshTomatoの最新版（旧版ではUSBサポートが劣る） |
| 交叉編譯環境 | Broadcomアーキテクチャ（MIPS/ARM）に対応するTomatoの交叉編譯ツールチェーンの構築が必要 |
| 驅動ソースコード | 対応するチップセットのLinuxドライバのソースコードを自ら取得し、Tomatoカーネルバージョンに合わせて修正が必要 |
| 技術能力 | Linuxカーネルモジュール開発、交叉編譯、デバッグの能力が必要 |
| 時間コスト | 数時間から数日かかり、成功確率が低いと予想 |

結論：99.9%のユーザーにとって、Tomato上でALFA USB WiFiアダプターを使用することは不可能です。

## 6. 兼容性判定

### ALFA 現役機型 × Tomato 兼容性マトリックス

| 機型 | クリスタルセット | USB コアサポート | USB デテクション | STA ネットワーク | AP モード | モニターモード | 総合評価 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ USB コアの有効化が必要 | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | 不サポート |

判定基準：Tomato（含 FreshTomato）の公式コアとパッケージリポジトリには、現代の USB WiFi クリスタルセットのドライバが含まれていません。Tomatoの設計目標には、USB WiFi 拡張機能を含むことはありません。

## 7. 超詳細 Step by Step 設定手順

現役のALFAモデルがTomato上で使用できないため、本節では確認手順と代替案を提供します。

### 7.1 チェック：TomatoルーターがUSB WiFiをサポートしているか（デバッグ手順）

**手順 1：Tomato管理インターフェースにログイン**

ブラウザで192.168.1.1（またはルーターのIPアドレス）を入力します。

**手順 2：USBコアが有効か確認**

- USB and NAS > USB Supportに進みます
- Core USB Support、USB 2.0 Support、USB 3.0 Support（もしあれば）が選択されていることを確認します
- USB Wireless Device Support（もしあれば）が選択されていることを確認します—多くのTomatoバージョンにはこの選項がありません

**手順 3：ALFAネットワークカードをルーターのUSBポートに挿入します**

**手順 4：SSH / TelnetでルーターにログインしてUSBの検出を確認**

```bash
# lsusbが存在するか確認（Tomatoではデフォルトで存在しない可能性があります）
which lsusb
# lsusbが存在しない場合、/proc/bus/usbまたはdmesgを確認します
cat /proc/bus/usb/devices
# または
dmesg | grep -i usb
```

**手順 5：ネットワークインターフェースを確認**

```bash
ifconfig -a
# vlan0 / br0 / eth0 / eth1（ルーターの内蔵インターフェース）のみがあり、wlan0 / wlan1がなく、USB WiFiがドライブされていないことを確認します
```

**手順 6：利用可能なkernelモジュールを確認**

```bash
lsmod
# wl（Broadcom内蔵WiFiドライブ）、et（エーテルネットワークドライブ）などが期待されます
# mt76 / rtl8812 / cfg80211 / mac80211などのUSB WiFiドライブは存在しません
```

**手順 7：追加のパッケージをインストールできるか確認**

```bash
# Tomatoではipkgを使用しますが、パッケージリポジトリの内容は非常に少ないです
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 期待される結果は空です
```

### 7.2 推奨代替案

#### 方案一：OpenWrtに変更（強く推奨）

あなたのルーターのモデルがOpenWrtをサポートしている場合、Tomatoから韌体をOpenWrtに変更することをお勧めします。OpenWrtにはUSB WiFiの完全なドライバパッケージリポジトリがあり、多くのALFAモデルをサポートします。

- あなたのルーターのモデルがOpenWrtのサポートリストにあるか確認します
- サポートしている場合、[ALFA無線ネットワークカードがOpenWrtをサポートしているか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)のインストール手順を参照してください

#### 方案二：ルーターの内蔵WiFiを使用

TomatoはBroadcomルーターの内蔵WiFiを完全にサポートしており、一般的なインターネット使用やAPホットスポットの場合、ルーターの内蔵WiFiを使用することでALFAネットワークカードを外接する必要はありません。

#### 方案三：ハードウェアを交換

特定のUSB WiFi機能（例えば、高電力出力、監視モード、パケット注入）が必要な場合、Tomatoプラットフォームではその要件を満たすことができません。以下の選択肢をお勧めします：

- OpenWrtをサポートするルーター + ALFAネットワークカードを使用
- x86小規模サーバーにOpenWrt / pfSenseをインストールしてALFAネットワークカードを使用
- Kali Linux / UbuntuコンピュータにALFAネットワークカードを使用

## 8. 常見なエラーとその解決策

| 症狀 | 可能な原因 | 解決方法 |
|---|---|---|
| Tomato 管理インターフェースには「USB Wireless Device Support」オプションがありません | その Tomato バージョンでは USB WiFi サポートが翻訳されていません | これは通常のことです；Tomatoのほとんどのバージョンにはこの機能がありません |
| ALFA ネットワークカードを接続した後、dmesgにはUSBの検出がありますが、ネットワークインターフェースがありません | 驅動が不足しています | 解決できません；Tomatoには対応するドライバがありません |
| ipkg パッケージを手動でインストールしたいが、WiFi ドライバが見つかりません | Tomatoのパッケージリポジトリには USB WiFi ドライバがありません | これは通常のことです；OpenWrtを使用することをお勧めします |
| 古い ALFA（RT3070）は Tomato で検出できますが、接続できません | ドライバが不完全または firmware が欠けています | 旧型のチップセットでも保証されません；OpenWrtを使用することをお勧めします |
| Tomato にブートした後、USB ポートはUSBメモリカードのみ読み取れる | TomatoのUSB機能はストレージやプリンターに限定されています | これは期待通りの行為です；TomatoはUSB WiFiをサポートしていません |

## 9. 知られている制約

- **完全にUSB WiFiドライバがない**：Tomato（含FreshTomato）の公式コアには、現代のUSB WiFiチップセットのドライバが含まれていないため、これは最も基本的な制約です。
- **Broadcomのクローズドソースドライバのバインド**：TomatoはBroadcomのクローズドソースのwlドライバに依存しており、mac80211 / cfg80211アーキテクチャのUSB WiFiドライバと共存することができません。
- **パッケージ管理のエコシステムがない**：Tomatoのipkgパッケージライブラリの内容は非常に少なく、OpenWrtのように数千のインストール可能なパッケージがない。
- **フラッシュ/RAMの空間不足**：多くのTomatoルーターは4-16MBのフラッシュしか持ち合わせておらず、ドライバをコンパイルしてもインストールする空間がありません。
- **開発方向が異なる**：FreshTomatoの開発チームの優先事項は、Broadcomプラットフォームの安定性を修復することであり、USB WiFiのサポートを追加するためのリソースを投資することはありません。
- **監視/注入が完全にサポートされていない**：TomatoのWiFiアーキテクチャ（Broadcom wlドライバ）自体が、パイプラインテスト機能をサポートしておらず、外部のUSB WiFiもこれを変更することはできません。
- **APモードの拡張がサポートされていない**：古いチップセットがドライバをロードできる場合でも、Tomatoのネットワーク設定インターフェースはUSB WiFiのAPモードを設定することをサポートしていません。

反論条件：もしFreshTomatoの将来のバージョンが公式のrelease notesで明確にUSB WiFiドライバのサポートを追加すると述べ、またはコミュニティで広く検証されたFreshTomatoのmt76 / rtl8812auモジュール移植プロジェクトが登場した場合、本文の第6節「サポートしない」の判定は再評価される必要があります。また、もしFreshTomatoがオープンソースのmac80211アーキテクチャのコアに移行した場合、制約の説明も更新する必要があります。

| 条件 | 説明 |
| --- | --- |
| 完全にUSB WiFiドライバがない | Tomato（含FreshTomato）の公式コアには、現代のUSB WiFiチップセットのドライバが含まれていないため、これは最も基本的な制約です。 |
| Broadcomのクローズドソースドライバのバインド | TomatoはBroadcomのクローズドソースのwlドライバに依存しており、mac80211 / cfg80211アーキテクチャのUSB WiFiドライバと共存することができません。 |
| パッケージ管理のエコシステムがない | Tomatoのipkgパッケージライブラリの内容は非常に少なく、OpenWrtのように数千のインストール可能なパッケージがない。 |
| フラッシュ/RAMの空間不足 | 多くのTomatoルーターは4-16MBのフラッシュしか持ち合わせておらず、ドライバをコンパイルしてもインストールする空間がありません。 |
| 開発方向が異なる | FreshTomatoの開発チームの優先事項は、Broadcomプラットフォームの安定性を修復することであり、USB WiFiのサポートを追加するためのリソースを投資することはありません。 |
| 監視/注入が完全にサポートされていない | TomatoのWiFiアーキテクチャ（Broadcom wlドライバ）自体が、パイプラインテスト機能をサポートしておらず、外部のUSB WiFiもこれを変更することはできません。 |
| APモードの拡張がサポートされていない | 古いチップセットがドライバをロードできる場合でも、Tomatoのネットワーク設定インターフェースはUSB WiFiのAPモードを設定することをサポートしていません。 |

**反論条件**：
- FreshTomatoの将来のバージョンが公式のrelease notesで明確にUSB WiFiドライバのサポートを追加すると述べ、またはコミュニティで広く検証されたFreshTomatoのmt76 / rtl8812auモジュール移植プロジェクトが登場した場合、本文の第6節「サポートしない」の判定は再評価される必要があります。
- FreshTomatoがオープンソースのmac80211アーキテクチャのコアに移行した場合、制約の説明も更新する必要があります。

[https://www.example.com](https://www.example.com)

## 10. 参考情報 URL

| 情報源 | 説明 | URL | 検証状態 | 検証日 |
|---|---|---|---|---|
| FreshTomato 公式ウェブサイト | FreshTomato 最新バージョンおよびサポートデバイスリスト | https://freshtomato.org/ | ✅ 検証済み | 2026-09-03 |
| OpenWrt 公式文書 | USB WiFi ドライバおよび無線設定（比較参考） | https://openwrt.org/docs/start | ✅ 検証済み | 2026-09-03 |
| OpenWrt 公式フォーラム | USB WiFi ドライバディスカッション（比較参考） | https://forum.openwrt.org/ | ✅ 検証済み | 2026-09-03 |
| ALFA Network 製品一覧（Yupitek） | ALFA 現行製品スペック | https://yupitek.com/zh-tw/products/alfa/ | ✅ 検証済み | 2026-09-03 |

関連記事：[ALFA 无線ネットワークカードが DD-WRT に対応しているか](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[ALFA 无線ネットワークカードが OpenWrt に対応しているか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 无線ネットワークカードが NVIDIA DGX Spark に対応しているか](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无線ネットワークカードが NVIDIA Jetson Nano に対応しているか](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責事項：本記事の互換性判定は、Tomato / FreshTomato 公式コアおよびパッケージリポジトリに基づいています。非常に少数の高度なユーザーが特定の旧型チップセットで基本機能を実現するために自己交叉コンパイルを行うことがありますが、これは公式サポート範囲外であり、一般ユーザーによる試行は推奨されません。USB WiFiを使用するルーター上での使用シーンにおいて、OpenWrtは唯一実際に実行可能な第三者製ファームウェア選択となります。
