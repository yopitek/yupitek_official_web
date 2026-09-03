---
title: "ALFA無線ネットワークカードがOpenWrtをサポートしていますか？"
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "ハードウェアガイド"
description: "OpenWrt：ALFA USB WiFi 最適、MT7612U 驅動強力"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題要約

お客様の質問：「ALFAシリーズのUSBワイヤレスネットワークアダプターがOpenWrtルーターで使用できるかどうか？」

簡潔な結論：OpenWrtは、DD-WRT / OpenWrt / Tomatoの三大第三者ルーター固縁体の中で、ALFA USB WiFiネットワークアダプターのサポートが最も良いプラットフォームです。MediaTekチップセット機種（AWUS036ACM / ACHM / AXML / AXM）は、公式のkmod-mt76シリーズパッケージを通じて直接サポートされます；Realtekチップセット機種（AWUS036ACH / ACS / EACS / AX / AXER）は、コミュニティで保守されているout-of-treeドライバーパッケージを使用する必要があり、利用可能性はOpenWrtのバージョンによって異なります。AWUS036ACM（MT7612U）が推奨されます。ドライバが成熟し、安定しており、監視と注入をサポートしています。

判定基準：ALFAの現役9モデルのUSBネットワークアダプター（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 目標ソフトウェアの規格と要求の分析

### 2.1 OpenWrtとは

OpenWrtは、高度にモジュール化されたオープンソースのルーター固件であり、Linuxカーネルとopkgパッケージ管理システムを採用しています。DD-WRTやTomatoとは異なり、OpenWrtのドライバは単独でインストール可能なkernel module（kmod）パッケージ形式で提供されており、ユーザーは必要に応じてUSB WiFiドライバをインストールすることができ、全体の固件を再コンパイルする必要はありません。

### 2.2 OpenWrtのUSB WiFiドライバフレームワーク

OpenWrtの公式パッケージリポジトリには以下のUSB WiFiドライバが含まれています。

| ドライバパッケージ | 源 | 涵蓋チップセット / モデル | メンテナンス状態 |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | 官方 in-kernel | MediaTek MT7612U（AWUS036ACM） | 活発、安定 |
| kmod-mt76-usb + kmod-mt76x0u | 官方 in-kernel | MediaTek MT7610U（AWUS036ACHM） | 活発 |
| kmod-mt7921u | 官方 in-kernel | MediaTek MT7921AUN（AWUS036AXML / AXM） | 23.05+ 版本で利用可能 |
| kmod-rtl8812au-ct | 社群 out-of-tree | Realtek RTL8812AU / RTL8811AU（AWUS036ACH / ACS） | 社群メンテナンス、24.10でkernel crashの報告あり |
| kmod-rtl8821cu | 社群 out-of-tree | Realtek RTL8811CU（AWUS036EACS） | 社群メンテナンス |
| kmod-rtw89 / kmod-rtl8852bu | 開発中 | Realtek RTL8832BU（AWUS036AX / AXER） | rtw89 USBサポートが徐々に統合、新しいカーネルが必要 |

### 2.3 前提条件：USBコアのサポート

WiFiドライバをインストールする前に、OpenWrtがUSBコアのサポートを有効にしていることを確認する必要があります。

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

多くの現代のOpenWrtバージョンでは、kmod-usb-coreがデフォルトで含まれていますが、usbutils（lsusbコマンドを提供）は手動でインストールする必要があります。

## 3. 現在のALFAネットワークカード規格およびチップセットの分析

2026年9月現在、ALFA Networkの現役USB無線ネットワークカード製品ラインは以下の通りです（判定基準：9モデル）：

| 機型 | Wi-Fi レベル | チップセット | インターフェース | OpenWrt 驅動ソフトウェア |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u（23.05+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u（23.05+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89（開発中）/ 自作 rtl8852bu |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct（コミュニティ） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u（公式） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u（公式）⭐ 推奨 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct（包括） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu（コミュニティ） |

## 4. 推薦機型とチップセット

### 4.1 推薦レベル分類

| 推薦レベル | 機型（チップセット） | 説明 |
|---|---|---|
| ⭐ 強烈推薦 | AWUS036ACM（MT7612U） | 公式ドライバが成熟・安定しており、AP / STA / Monitor / Injectionをサポート、OpenWrtにおける最高の選択です |
| ✅ 推薦 | AWUS036ACHM（MT7610U） | 公式ドライバ、双频波長で433Mbps、低消費電力の環境に適しています |
| ✅ 推薦（新バージョン） | AWUS036AXML / AXM（MT7921AUN） | Wi-Fi 6E、公式ドライバ、OpenWrt 23.05+およびkernel 5.15+が必要です |
| ⚠️ 使用可能但注意 | AWUS036ACH（RTL8812AU） | コミュニティドライバ、24.10バージョンでkernel crashの報告があり、23.05を使用することをお勧めします |
| ⚠️ 使用可能但注意 | AWUS036ACS（RTL8811AU） | 上記と同様、8812auドライバでカバーされています |
| ⚠️ 使用可能但注意 | AWUS036EACS（RTL8811CU） | コミュニティドライバ、安定性は中程度です |
| ❌ 不推薦 | AWUS036AX / AXER（RTL8832BU） | Wi-Fi 6、rtw89 USBサポートが開発中、多くのOpenWrtバージョンでは直接使用できません |

### 4.2 ルーターのハードウェア要件

| 項目 | 最低要件 | 建議要件 |
|---|---|---|
| USBポート | USB 2.0（AWUS036ACHM / ACS / EACS） | USB 3.0（AWUS036ACH / ACM / AXシリーズ） |
| フラッシュ | 16MB（ドライバおよび依存パッケージのインストール） | 32MB以上 |
| RAM | 128MB | 256MB以上（APモードおよび多ユーザー） |
| OpenWrtバージョン | 21.02以上 | 23.05.x（安定版） |

## 5. 環境要求

### 5.1 ソフトウェア環境

- OpenWrt 稳定版：23.05.x（kernel 5.15）または 24.10.x（kernel 6.6）
- パッケージソース：公式 opkg パッケージリポジトリ（https://downloads.openwrt.org/releases/{version}/packages/{arch}/）
- ネットワーク接続：ドライバのインストール中は、ルーターがインターネットに接続可能である必要があります（WAN ポートを通じて）

### 5.2 ハードウェア環境

- USB 2.0 / 3.0 ポートを備えた OpenWrt 互換ルーター
- 高出力モデル（AWUS036ACH）は、ルーターの USB ポートの電力供給不足を避けるため、USB 3.0 ヒュブを使用することをお勧めします
- AWUS036AXMLはUSB-Cインターフェースであり、ルーターにUSB-Cポートがあるか、USB-C to USB-A コンバータを使用することを確認してください

## 6. 兼容性判定

### ALFA 現役機型 × OpenWrt 兼容性マトリックス

| 機型 | クリスタルセット | 驅動方式 | USB 偵測 | STA 上網 | AP モード | Monitor | 最低バージョン | 総合評価 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ ベスト |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ 限定的 | 21.02+ | ✅ 良好 |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 限定的 | 23.05+ | ✅ 良好 |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ 限定的 | 23.05+ | ✅ 良好 |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ 限定的 | 22.03+（24.10 にクラッシュ） | ⚠️ 利用可能 |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ 利用可能 |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ 利用可能 |
| AWUS036AX | RTL8832BU | rtw89（開発中） | ⚠️ | ❌ | ❌ | ❌ | カスタムコンパイル必要 | ❌ 不推奨 |
| AWUS036AXER | RTL8832BU | rtw89（開発中） | ⚠️ | ❌ | ❌ | ❌ | カスタムコンパイル必要 | ❌ 不推奨 |

判定基準：OpenWrt 公式パッケージリポジトリ（23.05 / 24.10）の kmod パッケージの利用可能性 + OpenWrt フォーラムのユーザーからの報告。Realtek クリスタルのドライバはコミュニティの保守であり、安定性と機能の完全性はMediaTek mt76 シリーズに及ばない。

## 7. 超詳細 Step by Step 設定手順

### 7.1 前置作業：USB 核心支援の有効化

**手順 1：OpenWrt 路由器への SSH 登入**

```bash
ssh root@192.168.1.1
```

**手順 2：パッケージリポジトリの更新および USB 核心支援のインストール**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**手順 3：ALFA 網卡の挿入および USB 動作の確認**

```bash
lsusb
# 預期出力例（AWUS036ACM / MT7612U）：
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 路線 A：MediaTek クロック機型（AWUS036ACM / ACHM / AXML / AXM）

AWUS036ACM（MT7612U）を例にします：

**手順 1：ドライバーパッケージのインストール**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — 別のパッケージを使用
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — 別のパッケージを使用（23.05+ 必要）
# opkg install kmod-mt7921u
```

**手順 2：無線管理ツールのインストール**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**手順 3：ネットワークインターフェースの確認**

```bash
iw dev
# 預期出力例：wlan0 または wlan1 インターフェースが表示されます
```

**手順 4：周辺の WiFi スキャン（機能確認用）**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**手順 5：STA モードとして設定（現存の AP に接続）**

`/etc/config/wireless` を編集します：

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'あなたのWiFi名前'
       option encryption 'psk2'
       option key 'あなたのWiFiパスワード'
```

**手順 6：無線サービスの再起動**

```bash
/etc/init.d/network restart
```

**手順 7：AP モードとして設定（ネットワークを共有）**

`/etc/config/wireless` を編集し、mode を ap に変更します：

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'あなたのホットスポットパスワード'
```

**手順 8：リスニングモードの設定（渗透テスト用）**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# 验証
iw dev wlan0 info
# type は monitor に表示されるべきです
```

### 7.3 路線 B：Realtek クロック機型（AWUS036ACH / ACS / EACS）

AWUS036ACH（RTL8812AU）を例にします：

**手順 1：コミュニティドライバのインストール**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — 別のパッケージを使用
# opkg install kmod-rtl8821cu
```

**手順 2：無線管理ツールのインストール**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**手順 3：インターフェースの確認**

```bash
iw dev
# 注意：rtl8812au-ct ドライバのインターフェース名は wlan0 または wlan1 になる可能性があります
```

設定方法は 7.2 の手順 5-7（STA / AP モード設定）と同じです。

**手順 4：リスニングモード**

```bash
# rtl8812au-ct ドライバはリスニングモードをサポートしています
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# パケット注入機能は限られています、渗透テストには mt76 クロックを使用することをお勧めします
```

**手順 5：kernel crash（24.10 版本の既知問題）が発生した場合**

```bash
# 23.05 稳定版に戻すか、カスタムコンパイルのドライバを使用
# crash ログを確認
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 路線 C：Wi-Fi 6 モデル（AWUS036AX / AXER、RTL8832BU）

⚠️ この路線は一般ユーザーには適していません、OpenWrt をカスタムコンパイルする必要があります。

**手順 1：OpenWrt 版本が rtw89 USB 支援を含むか確認**

```bash
opkg list | grep rtw89
# 結果が無い場合、そのバージョンには含まれていません
```

**手順 2：使用する場合は、OpenWrt イメージファイルを自作**

`kmod-rtw89` と対応の firmware を追加します。

**代替案**：OpenWrt ルーター上で Wi-Fi 6 USB ネットワークカードを使用する必要がある場合、AWUS036AXML（MT7921AUN）を使用することをお勧めします。

## 8. 常見なエラーとその解決策

| 症狀 | 可能な原因 | 解決方法 |
|---|---|---|
| lsusb で ALFA ネットワークカードが見られない | USB コアがインストールされていない / 供給不足 | kmod-usb-core、kmod-usb2、kmod-usb3がインストールされていることを確認；電源付きのUSB Hubを使用 |
| lsusb で見えるがiw devでインターフェースが見られない | 驅動がインストールされていない / 驅動が互換性がない | 对応するkmodパッケージをインストール；dmesgでfirmwareの欠失エラーがないか確認 |
| opkg install kmod-mt76x2uで「kernel version mismatch」が表示される | OpenWrtのバージョンとパッケージリポジトリのバージョンが一致していない | opkg updateを実行してから再試行；ハードウェアバージョンとパッケージリポジトリのアーキテクチャが一致していることを確認 |
| APモードが起動しない（hostapdエラー） | 驅動がAPモードをサポートしていない / チャンネル設定が間違っている | クリップセットがAPモードをサポートしていることを確認；チャンネルを固定（例えば6または149）に試み；Regulatory Domainを確認 |
| 監視モードでパケット注入ができない | 驅動が注入をサポートしていない / チャンネルが衝突している | MediaTek mt76シリーズが最適；Realtek 8812au-ctの注入機能は限られている；airmon-ng check killを確認 |
| AWUS036ACHの高電力モードで切断 | USBの供給不足 | 電源付きのUSB 3.0 Hubを使用；/etc/config/wirelessでoption txpower '20'を設定してパワーを低減 |
| 24.10でrtl8812au-ctをインストールした後でkernel panic | 已知なドライバの互換性問題 | 23.05.xの安定版に戻す；GitHub issueを追跡して修復を待つ |
| MT7921（AXML/AXM）で6GHzを使用できない | Regulatory Domainの制限 / kernelのバージョン | kernel 5.19以上が必要でWi-Fi 6Eの規制地域を正しく設定；OpenWrt 23.05の6GHzのサポートはまだテスト中 |

## 9. 知られている制限

- Realtek クリスタルチップドライバのコミュニティ保守：kmod-rtl8812au-ct、kmod-rtl8821cu は OpenWrt 公式保守されておらず、安定性と更新スケジュールが保証されません
- 24.10 版の rtl8812au-ct には kernel crash の報告があります：Realtek クリスタルチップユーザーは 23.05.x に維持することをお勧めします
- Wi-Fi 6（RTL8832BU）のサポート不足：rtw89 USB ドライバは開発中であり、多くの OpenWrt 版本では AWUS036AX / AXER を直接使用することができません
- AP モードの性能制限：USB WiFi で AP を行う場合、スループットはルーター内蔵 WiFi（USB ブリッジの帯域幅 + ドライバオーバーヘッド）より低くなります
- 監視 / 注入機能の差異：MediaTek mt76 シリーズが最も完全にサポートされています；Realtek クリスタルチップの注入機能は限られており、プロフェッショナルなパイプラインテストには適していません
- ルーターのハードウェアリソース：低価格のルーター（16MB Flash / 128MB RAM）にドライバをインストールすると、他の機能に影響を与える可能性がある空間不足が発生します
- USB 3.0の干渉：USB 3.0 デバイスは 2.4GHz WiFi に干渉を与えるため、USB 2.0 ポートまたは良好に隔離された USB Hub を使用することをお勧めします
- 多数のネットワークカードの同時使用：ルーター内蔵 WiFi + USB WiFi を同時に使用する場合、チャネル衝突やリソース競合が発生する可能性があります
- ⚠️ **RTL8832BU（AWUS036AX/AXER）ドライバ保守者は公開で使用を避けることを推奨しています**：本文の第 4.1 節で「❌ 不推奨」とされていますが、原因は rtw89 USB が開発中であるだけでなく、ドライバ保守者 morrownr が公開で该晶片シリーズ「ドライバは非常に悪く、クリスタルチップ自体に問題があると疑います」と述べており、Linux ユーザーは現時点で避けることを推奨しています（詳細は第 10 節を参照してください）
- **kernel バージョンのバリアー用語を明確にする必要があります**：第 4.1 節の「MT7921AUN は OpenWrt 23.05+ で kernel 5.15+ 必要」との記述は誤解を招きやすいです——mt7921u ドライバ自体はデスクトップ Linux 上で実際に存在するためには **kernel 5.19+** が必要です（ドライバ保守者の原話を参照してください），しかし OpenWrt 公式パッケージは backport メカニズムを通じて事前に収録することが多く、したがって OpenWrt 23.05（kernel 5.15をベースにしていますが）でも kmod-mt7921u のインストールが成功するユーザーの報告があります。**判定は、実際のクライアントバージョンの `opkg list` 実際の検索結果に基づいてください、kernel バージョンを逆推定しないでください**

反論条件：OpenWrt 後续パッケージの更新で 24.10 の rtl8812au-ct kernel crash 問題が修復された場合、第 4.1 節と第 6 節の AWUS036ACH の推奨は「維持 23.05」にアップグレードされる可能性があります；rtw89 USB サポートが OpenWrt 公式パッケージに正式に追加された場合、AWUS036AX / AXER の「不推奨」の判定が再評価される必要があります；MT7921の 6GHz 完全サポートの公式声明が発表された場合、AXML / AXM の制限説明を更新する必要があります。

## 10. 参考情報 URL

| 情報源 | 説明 | URL | 検証状態 | 検証日 |
|---|---|---|---|---|
| OpenWrt 公式文書 | OpenWrt 公式ファイルエントリ（ワイヤレス設定 / パッケージ管理） | https://openwrt.org/docs/start | ✅ 検証済み | 2026-09-03 |
| OpenWrt 公式フォーラム | USB WiFi ドライバ討論エントリ | https://forum.openwrt.org/ | ✅ 検証済み | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux ドライバのアップストリーム | https://github.com/morrownr/8812au-20210820 | ✅ 検証済み | 2026-09-03 |
| ALFA Network 製品一覧（Yupitek） | ALFA 現行製品仕様 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 検証済み | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | ドライバ保守者公式声明：rtl8852/32au（RTL8832BU）チップセットを避ける推奨 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 検証済み | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko は kernel 5.19+ でのみコアに表示される（ドライバ保守者原話） | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ 検証済み | 2026-09-03 |
| OpenWrt 公式フォーラム — Best USB WiFi dongle for Raspberry Pi 4B | 使用者からの報告：OpenWrt 23.05.0 で kmod-mt7921u が成功してインストール | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ 検証済み | 2026-09-03 |

関連記事：[ALFA 无線ネットワークカードが DD-WRT に対応していますか](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[ALFA 无線ネットワークカードが Tomato に対応していますか](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA 无線ネットワークカードが NVIDIA DGX Spark に対応していますか](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 无線ネットワークカードが NVIDIA Jetson Nano に対応していますか](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責事項：本記事の互換性判定は OpenWrt 23.05.x / 24.10.x 公式パッケージリポジトリに基づいています。異なるルーターアーキテクチャ（ath79 / ramips / mvebu / x86 など）のパッケージの利用可能性は異なります。Realtek チップセットのドライバはコミュニティで保守されていますが、実際の安定性はバージョンによって異なる可能性があります。OpenWrt USB WiFi の優先選択として MediaTek チップセット機型（AWUS036ACM が推奨）をご検討ください。
