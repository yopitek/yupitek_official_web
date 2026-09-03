---
title: "ALFA無線ネットワークカードがDD-WRTをサポートしているかどうか"
date: 2026-09-03
draft: false
slug: "alfa-ddwrt-router-compatibility"
tags:
  - "ALFA"
  - "DD-WRT"
  - "Router"
  - "Broadcom"
  - "Atheros"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "ハードウェアガイド"
description: "ALFA全シリーズのUSB WiFiカードはDD-WRT非対応、OpenWrt推奨（ALFA無線カードOpenWrt互換確認）"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題要約

お客様の質問：「ALFA シリーズのUSBワイヤレスネットワークアダプターがDD-WRTファームウェアが適用されたルーターで使用できるかどうか？」

簡易結論：現在のALFA全シリーズの現役モデル（AWUS036ACH / ACM / ACHM / ACS / EACS / AX / AXER / AXML / AXM、合計9モデル）は、DD-WRT上で公式ドライバーサポートが提供されていないため、使用を推奨しません。（判定基準：ALFAの現役9モデルのUSBネットワークアダプター）DD-WRTのUSBWiFiサポートは、非常に限られた旧型のAtheros / Ralinkチップセットに限られており、特定のコンパイルバージョンが必要です。ルーターでUSBWiFiネットワークアダプターを使用する必要がある場合は、OpenWrt（[ALFA無線ネットワークアダプターがOpenWrtをサポートするかどうか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)を参照してください）を使用することをお勧めします。

## 2. 目標ソフトウェアの規格と要求の分析

### 2.1 DD-WRTとは

DD-WRTは、オープンソースのルーター用サードパーティー固件で、主にBroadcom / Atheros / Ralink SoCを内蔵したWiFiチップセットを持つルーター向けに設計されています。その核心アーキテクチャはLinuxカーネルですが、デフォルトではドライバは対象のルーターのSoCに対応する無線ドライバのみがインクルードされています。

### 2.2 DD-WRTのUSB WiFiサポートフレームワーク

DD-WRTはipkgパッケージ管理システムを通じて追加ドライバをインストールすることができますが、公式パッケージリポジトリにはUSB WiFiドライバが非常に少ないです：

| ドライバ | DD-WRT状態 | 対応チップセット（ALFAモデル） |
|---|---|---|
| ath9k_htc | 部分バージョン内蔵 | Atheros AR9271（例：TP-Link TL-WN722N v1） |
| rt2800usb | 部分バージョン内蔵 | Ralink RT3070 / RT3370 / RT5370（旧型ALFA AWUS036NHなど） |
| rtl8812au | オフィシャルパッケージ無し | Realtek RTL8812AU（AWUS036ACH） |
| mt76 / mt76x2u | オフィシャルパッケージ無し | MediaTek MT7612U / MT7610U（AWUS036ACM / ACHM） |
| mt7921u | オフィシャルパッケージ無し | MediaTek MT7921AUN（AWUS036AXML / AXM） |
| rtl8852bu / rtw89 | オフィシャルパッケージ無し | Realtek RTL8832BU（AWUS036AX / AXER） |

### 2.3 重要な制限

- DD-WRTの核心はルーターの内蔵WiFiを優先サポートしており、USB WiFiはサブ機能として扱われています
- 異なるルーターモデルのDD-WRTのコンパイルバージョンが異なり、ドライバの利用可能性に大きな差があります
- ソーシャルコミュニティがドライバを自作してリポジトリに追加しても、フラッシュやRAMの不足によりインストールができなくなることがあります
- DD-WRTはUSB WiFiのモニターモード（Monitor Mode）やパケットインジェクション（Packet Injection）をほぼサポートしておりません

## 3. 現在のALFAネットワークカード規格およびチップセットの分析

2026年9月現在、ALFA Networkの現役USB無線ネットワークカード製品ラインは以下の通りです：

| 機型 | Wi-Fi レベル | チップセット | インターフェース | Linux 驅動状態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | Linux in-kernel（mt7921u、kernel 5.12以降が必要） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | Linux in-kernel（mt7921u、kernel 5.12以降が必要） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | Out-of-tree（rtl8852bu / rtw89） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | Out-of-tree（8812au、morrownr 维護） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | Linux in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | Linux in-kernel（mt76x2u） |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | Out-of-tree（8812au 拡張） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | Out-of-tree（8821cu、morrownr 维護） |

## 4. 対応機種およびチップセット

### 4.1 DD-WRT上で利用可能なALFA機種（生産終了 / 興行停止）

| 機種 | チップセット | ドライバ | DD-WRT 状態 |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | 部分のDD-WRTバージョン内蔵、2.4GHz / 150Mbpsのみ |
| AWUS036H | Realtek RTL8187L | rtl8187 | 极めて古い型、部分バージョンでサポート、2.4GHz / 54Mbpsのみ |
| AWUS050NH | Atheros AR9170 | carl9170 / ar9170usb | 极めて古い型、双频、ただし生産終了多年 |

### 4.2 DD-WRT上で利用不可能な現行機種

すべての現行ALFA機種（第3節のテーブルを参照）は、以下の理由でDD-WRT公式サポートされていません。

- Realtekチップ（RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU）：DD-WRTには対応するout-of-treeドライバパッケージがありません
- MediaTekチップ（MT7612U / MT7610U / MT7921AUN）：DD-WRTにはmt76 / mt7921ドライバが編入されていません
- もしルーターにUSBポートがある場合でも、ハードウェアレベルでデバイスが認識できる（lsusbでVID/PIDが見える）にもかかわらず、ドライバがないためネットワークインターフェースを構築することができません

## 5. 環境要求

若客戶がDD-WRT上でALFAネットワークカードを使用を試みたい場合は、以下の条件を満たす必要があります：

| 項目 | 需要条件 |
|---|---|
| ルーター機器 | USB 2.0 / 3.0 ポートが必須で、DD-WRTがUSBコアサポートを有効にしています（Services > USB） |
| DD-WRTバージョン | そのルーターのサポートする最新のBrainSlayer / Kongバージョンが必要で、旧バージョンのドライバはサポートが少ない |
| フラッシュ空間 | 少なくとも16MBのフラッシュが必要です（多くのエントリーレベルルーターは4-8MBしかないため、追加のドライバをインストールすることができません） |
| RAM | 少なくとも128MBのRAMが必要です（USB WiFiドライバとhostapdはメモリを占有します） |
| 供給 | USBポートが十分な電流を提供する必要があります（AWUS036ACHの高電力出力時は800mA以上、電源USBHubを使用することをお勧めします） |

## 6. 兼容性判定

### ALFA 現役機型 × DD-WRT 兼容性マトリックス

| 機型 | クリスタルセット | USB ポートスキャン | ドライバのインストール | STA ネットワーク | AP モード | モニターモード | 総合判定 |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ✅（lsusb） | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036AXM | MT7921AUN | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036AX | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036AXER | RTL8832BU | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036ACH | RTL8812AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036ACHM | MT7610U | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036ACM | MT7612U | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036ACS | RTL8811AU | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |
| AWUS036EACS | RTL8811CU | ✅ | ❌ | ❌ | ❌ | ❌ | 不対応 |

判定基準：DD-WRT 公式パッケージとコアのデフォルトのコンパイルには、上記のクリスタルセットが含まれていない USB WiFi ドライバが含まれていません。lsusb でデバイスが見えることは、USB ポートレベルの認識を示すだけで、ネットワーク機能が利用可能であることを示しません。

## 7. 超詳細 Step by Step 設定手順

現役のALFAモデルがDD-WRT上で使用できないため、以下の2つの代替経路を提供します：

### 経路 A：DD-WRTルーターが実際にサポートしていないか確認する（デバッグ手順）

**手順 1：DD-WRT管理インターフェースにログイン**

ブラウザに `192.168.1.1`（またはルーターのIPアドレス）を入力します。

**手順 2：USBサポートを有効にする**

- Services > USB に進みます
- Core USB Support、USB 2.0 Support、USB 3.0 Support（もしあれば）をチェックします
- USB Wireless Device Support（もしあれば）をチェックします
- Save > Apply Settings をクリックします

**手順 3：ALFAネットワークカードをルーターのUSBポートに挿入します**

**手順 4：SSHでルーターにログインして確認する**

```bash
# USBデバイスが検出されているか確認
lsusb
# 期待される出力はALFAネットワークカードのVID/PIDを含むべきです、例えば：
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter

# ネットワークインターフェースが作成されているか確認
ip link show
# wlan0 / wlan1などの新しいインターフェースがなければ、ドライバが読み込まれていないことを意味します

# カーネルログを確認
dmesg | tail -30
# "no driver"やUSBリスト表示のみが表示されている場合、ドライバが欠けていることを確認してください
```

**手順 5：利用可能なWiFiドライバモジュールを確認する**

```bash
# 読み込まれた無線ドライバをリストアップ
lsmod | grep -E "ath|rt2|rtl|mt76|mac80211|cfg80211"
# ルーターの内蔵WiFiのドライバ（wl / b43 / ath9kなど）のみがあれば、USB WiFiドライバがありません
```

**手順 6：コミュニティドライバのインストールを試みる（もしあれば**）

```bash
ipkg update
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# 検索結果が空の場合、そのDD-WRTバージョンには利用可能なドライバがありません
```

### 経路 B：代替案 — OpenWrtへの変更

クライアントがルーターでALFA USB WiFiネットワークカードを使用する必要がある場合、DD-WRTからルーターのファームウェアをOpenWrtに変更することを強く推奨します。OpenWrtには活発なUSB WiFiドライバパッケージライブラリがあり、MT7612U / MT7610U / RTL8812AUなどのチップセットをサポートしています。詳細な手順は、[ALFA無線ネットワークカードがOpenWrtでサポートされているか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)を参照してください。

## 8. 常見なエラーとその解決策

| 症狀 | 可能な原因 | 解決方法 |
|---|---|---|
| lsusb で ALFA ネットワークカードが見られない | USBの電力不足 / 接触不良 / DD-WRTのUSBコアが未启動 | Services > USBが有効に設定されているか確認；USBポートを変更するか、電源付きのUSBホブを利用する |
| lsusb で見えるがip linkでwlanインターフェースが見られない | 必要なチップセットのドライバが不足 | DD-WRTのバージョンがそのドライバをサポートしているか確認；多くの場合、解決策は見つからず、OpenWrtに変更することをお勧めします |
| wlanインターフェースがあるがAPをスキャンできない | ドライバが完全にサポートしていない / 監視モードの競合 | dmesgでfirmwareの読み込みエラーがないか確認；Regulatory Domainの設定を確認 |
| ルーターが再起動した後設定が消失 | DD-WRTのNVRAM空間不足 | 低階ルータに追加のドライバをインストールしないように；ハードウェアをアップグレードするか、OpenWrtに変更することを検討 |
| AWUS036ACHの高電力出力時の切断 | USBポートの電力不足 | 電源付きのUSB 3.0ホブを使用する；TX Powerの設定を低減 |

## 9. 既存の制約

- 驅動の欠如：DD-WRTの公式では、ALFAの現役モデルのUSB WiFiのドライバを提供していないため、これは最も基本的な制約となります。
- �硬体資源：多くのDD-WRT対応ルーターのFlash（4-16MB）とRAM（32-128MB）は限られており、ドライバが提供されていてもインストールできない可能性があります。
- 監視/注入のサポートが無い：DD-WRTのUSB WiFiアーキテクチャは、渗透テストに必要なMonitor ModeとPacket Injectionをサポートしていません。
- APモードの不安定：古いRalinkチップセットが動作する場合でも、USB WiFiのAPモードはDD-WRT上で常時切断や性能問題が発生します。
- バージョンが分裂している：異なるルーターモデルのDD-WRTのコンパイルバージョンが大きく異なり、あるバージョンのドライバが別のバージョンでも使用できることを保証できません。
- 維護が停止している：DD-WRTの開発ペースが遅れ、USB WiFiのドライバが追加される可能性は低いです。
- 追加：DD-WRT自体の制約を除いても、AWUS036AX / AXER（RTL8832BU）のこれらのモデルのドライバの維護者であるmorrownrは、Linuxユーザーに対してこのチップセットシリーズを避けることを公に勧告しています（[ALFA無線ネットワークカードがOpenWrtでサポートされているかどうか](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) 第9節を参照してください）。これはDD-WRTプラットフォームの問題に限られていません。
- 反論条件：クライアントがBrainSlayer / Kongなどの追加ドライバを含むコミュニティ編集バージョンを使用している場合、実際のサポート状況は異なる可能性があります。この判定は公式リリースバージョンに基づいています。

## 10. 参考来源 URL

| 来源 | 説明 | URL | 検核状態 | 検核日期 |
|---|---|---|---|---|
| DD-WRT 公式 Wiki | インストール / サポート / FAQ 全体入口 | https://wiki.dd-wrt.com/wiki/Main_Page | ✅ 検核済み | 2026年9月3日 |
| DD-WRT 公式 Wiki — インストール | インストール説明（USB サポート含む） | https://wiki.dd-wrt.com/wiki/Installation | ✅ メインページリンクで確認済み | 2026年9月3日 |
| OpenWrt 公式文書 | USB WiFi 比較参考 | https://openwrt.org/docs/start | ✅ 検核済み | 2026年9月3日 |
| morrownr/8812au GitHub | RTL8812AU Linux ドライバ（DD-WRT 未統合） | https://github.com/morrownr/8812au-20210820 | ✅ 検核済み | 2026年9月3日 |
| ALFA Network 產品一覧（Yupitek） | ALFA 現役製品仕様 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 検核済み | 2026年9月3日 |

関連記事：[ALFA 无線网卡是否支持 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 无線网卡是否支持 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)

免責事項：本文の相容性判定は、チップセットのドライバ状態と DD-WRT 公式パッケージリポジトリに基づいています。DD-WRT コミュニティには大量のカスタム翻訳バージョンがありますが、お客様が非公式バージョンを使用する場合、実際の結果は異なる可能性があります。お客様には、OpenWrt をルーター USB WiFi の優先選択としてお勧めします。
