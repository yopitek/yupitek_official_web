---
title: "EM7455 完全レビュー：Maker とエンジニアに愛される Sierra Wireless モジュール"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - 製品レビュー
series:
  - sierra-wireless-selection
series_order: 2
description: "EM7455 完全レビュー：仕様、EM7430 との違い、OpenWrt/Linux 設定、Dell/Lenovo 互換性。本記事は Yupitek（ユピテック）が技術資料をまとめたものです。"
author: "yupitek"
draft: false
faq:
  - question: "EM7455 は 5G に対応していますか？"
    answer: "対応していません。EM7455 は LTE-A Cat 6 モジュールで、最大 300 Mbps です。5G（Sub-6 または mmWave）が必要な場合は、EM9190（Sub-6）または EM9191（Sub-6 + mmWave）をご検討ください。"
  - question: "EM7455 は台湾で使用できますか？"
    answer: "一般的には台湾の主要キャリアの SIM カードでご利用いただけます。実際の信号品質や利用可能な周波数帯は、基地局の位置、キャリアのネットワーク計画、キャリアアグリゲーションの対応状況によって異なります。ご注文前に、お客様の地域とキャリアの互換性についてお問い合わせください。"
  - question: "EM7455 と MC7455 の違いは何ですか？"
    answer: "コアチップは同じ Qualcomm MDM9230 で、仕様は同一です。唯一の違いはパッケージ形式です：EM7455 は M.2、MC7455 は mPCIe です。お持ちのスロットに応じてお選びください。"
  - question: "EM7455 と EM7430 の違いは何ですか？"
    answer: "同じ MDM9230 チップを採用しており、コア仕様は同一です。主な違いは対応周波数帯の構成です：EM7455 はアメリカ大陸と EMEA 向け、EM7430 はアジア太平洋向けの周波数帯をカバーしています。詳細な周波数帯リストについては、最新の公式仕様書をご確認ください。"
  - question: "Dell DW5811e は EM7455 と同じものですか？"
    answer: "はい、DW5811e は Dell ブランド版の EM7455 で、コアは同じ Qualcomm MDM9230 です。多くの Dell ノートパソコンでは BIOS ホワイトリストの制限がないとコミュニティで報告されていますが、実際の状況はお使いの機種に依存します。"
---

EM7455 は、Sierra Wireless の LTE-A Cat 6 M.2 セルラーモジュールです。Qualcomm MDM9230 チップを搭載し、最大 300 Mbps のダウンロード、50 Mbps のアップロードに対応。GNSS 測位を内蔵し、動作温度範囲は -40°C 〜 +85°C です。本記事は Yupitek（ユピテック）が仕様の解説と設定の参考情報をまとめたものです。

Sierra Wireless EM7455 は M.2 B-Key パッケージの 4G LTE-Advanced Cat 6 モジュールで、OpenWrt ルーター、Raspberry Pi モバイル基地局、産業用ゲートウェイ、商用ノートパソコンの WWAN として幅広く利用されています。以下の設定手順はコミュニティおよび公式ドキュメントの一般的な流れをまとめたものです。実際のコマンドはお使いの OS バージョン、ファームウェアバージョンに応じてご確認の上、実行前に既存の設定をバックアップすることをおすすめします。

> 製品リンク：[EM7455 — Yupitek 製品ページ](https://yupitek.com/zh-tw/products/sierra/em7455/) | 公式仕様書：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完全仕様表

以下の仕様数値は Sierra Wireless 公式仕様書および公開情報をもとにまとめています。実際にご注文される際は、弊社より最新の公式ドキュメントをお取り寄せいただき、特に周波数帯やファームウェアバージョンなど随時更新される項目を逐一ご確認ください。

| 項目 | 仕様 |
|---|---|
| **型番** | AirPrime EM7455 |
| **セルラー規格** | LTE-A Cat 6 |
| **チップセット** | Qualcomm MDM9230（Snapdragon X7 LTE） |
| **ダウンロード最大** | 300 Mbps（LTE-A、2×CA） |
| **アップロード最大** | 50 Mbps（LTE-A） |
| **キャリアアグリゲーション** | 2×CA（複数の組み合わせに対応。詳細は公式 AT コマンドリファレンスをご参照ください） |
| **パッケージ** | PCI Express M.2 B-Key（52-pin） |
| **サイズ** | 42 × 30 × 2.3 mm |
| **動作温度** | -40°C ~ +85°C（産業用グレード） |
| **GNSS** | GPS、GLONASS、BeiDou、Galileo |
| **通信インターフェース** | USB 3.0 / USB 2.0 High Speed |
| **LTE 周波数帯** | アメリカ大陸および EMEA（欧州/中東/アフリカ）の主要周波数帯をカバー。詳細な周波数帯リストはお問い合わせください |
| **3G WCDMA 周波数帯** | お問い合わせください |
| **汎用 VID:PID** | `1199:9079`（EM7455、一般バージョン） |
| **Dell DW5811e VID:PID** | `413c:81b6`（ブランドバージョン。実機の `lsusb` 結果をご確認ください） |
| **Linux ドライバー** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主要ディストリビューションに標準搭載。最低 kernel バージョンはお使いのディストリビューションの説明をご確認ください） |
| **汎用ファームウェア** | 公式 source.sierrawireless.com の最新バージョンを参照してください。本記事では特定のバージョン番号を記載せず、情報の陳腐化を防止します |
| **キャリア認証** | キャリアや地域によって変動します（AT&T、Verizon、T-Mobile、Bell、Rogers、Telus、Vodafone 等）。お客様の地域の最新認証リストについてはお問い合わせください |

---

## EM7455 の用途

**EM7455 は以下の 3 つの用途に最適です。（1）4G LTE ルーターの自作（OpenWrt / ROOter）、（2）ノートパソコンの WWAN アップグレード（Dell / Lenovo）、（3）産業用 IoT ゲートウェイおよびコネクテッドカーのテレマティクス。** 主な強みは、Linux ドライバーの成熟度の高さ、コミュニティリソースの豊富さ、そしてアメリカ大陸/EMEA の広範な周波数帯カバレッジです。

### Maker / ホビイスト向け

| アプリケーション | 構成 | 理由 |
|---|---|---|
| Raspberry Pi 4G ルーター | Raspberry Pi 4/5 + M.2→USB 変換基板 + OpenWrt / ROOter | OpenWrt コミュニティでの互換性が安定、uqmi パッケージが成熟 |
| GL.iNet ルーターのアップグレード | GL-MT1300 / GL-AR750S + USB 変換 | ROOter フックや `create_connect.sh` に関するコミュニティでの議論あり |
| ポータブル LTE ホットスポット | バッテリー駆動 + USB 変換 + 小型ルーター | 発熱が少なく放熱性に優れ、野外での使用に適しています |

### 企業 / 産業向け

| アプリケーション | 構成 | 理由 |
|---|---|---|
| 産業用ルーター | M.2 スロット産業用ゲートウェイ（Advantech、Cincoze 等） | 広い動作温度 -40~85°C、幅広い周波数帯カバレッジ |
| コネクテッドカーテレマティクス | 車載ゲートウェイ + GNSS アンテナ | GPS/GLONASS/BeiDou/Galileo 内蔵、単一モジュールで通信＋測位を実現 |
| ノート PC WWAN アップグレード | Dell Latitude / Precision、Lenovo ThinkPad | M.2 B-Key に直接装着可能、Linux ドライバーのサポートが充実 |
| WAN バックアップ | OpenWrt / pfSense デュアル WAN バックアップ | QMI/MBIM デュアルモード対応。ただし pfSense のサポートは限定的なため、OpenWrt を推奨 |

---

## EM7455 と EM7430 の違い

**EM7455 と EM7430 は同じ Qualcomm MDM9230 チップを採用しており、コア仕様は同一です（Cat 6、300/50 Mbps、2×CA、GNSS）。主な違いは対応周波数帯の構成です。EM7455 はアメリカ大陸と EMEA 向け、EM7430 はアジア太平洋（APAC）向けの周波数帯をカバーしています。**

| 項目 | EM7455 | EM7430 |
|---|---|---|
| **チップセット** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **セルラー規格** | LTE-A Cat 6 | LTE-A Cat 6 |
| **ダウンロード最大** | 300 Mbps | 300 Mbps |
| **アップロード最大** | 50 Mbps | 50 Mbps |
| **キャリアアグリゲーション** | 2×CA | 2×CA |
| **パッケージ** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **対象地域** | アメリカ大陸、EMEA（欧州/中東/アフリカ） | APAC（アジア太平洋） |
| **詳細周波数帯リスト** | お問い合わせください | お問い合わせください |

> 両モジュールの正確な周波数帯別の詳細は、最新の公式 Spec Sheet をご参照ください。本記事では周波数帯番号の一覧を掲載せず、公式ドキュメントの更新による情報の不正確化を防止しています。お客様のキャリアと必要な周波数帯がすでにわかっている場合は、お気軽に弊社までお問い合わせください。

**選定の指針**：お使いの SIM キャリアが主に北米または欧州の場合は **EM7455** を、アジア太平洋地域のキャリア（台湾、日本、オーストラリア等）をご利用の場合は **EM7430** を優先的にご検討ください。

---

## EM7455 vs MC7455：同じチップ、異なるパッケージ

EM7455（M.2）と MC7455（mPCIe）は同じ Qualcomm MDM9230 チップセットを採用しており、コアとなる電気的仕様は同一です。主な違いは**パッケージインターフェース**です：

| 項目 | EM7455 | MC7455 |
|---|---|---|
| **パッケージ** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **サイズ** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **適した機器** | ノート PC の WWAN スロット、最新の M.2 マザーボード | 旧型産業用ルーターの mPCIe スロット |
| **汎用 VID:PID** | `1199:9079` | `1199:9071` |

**どちらを選ぶかは、お持ちの機器のスロット次第です。** マザーボードが M.2 の場合は EM7455 を、mPCIe の場合は MC7455 をお選びください。パッケージを間違えた場合は、変換基板（M.2→mPCIe または mPCIe→M.2）で対応できます。

---

## Linux 設定（Ubuntu / Debian / Linux Mint）

EM7455 は主要な Linux ディストリビューションでのドライバーサポートが充実しています。以下はコミュニティで一般的な基本的な設定手順です。実際の環境（ディストリビューションのバージョン、カーネルバージョン、ファームウェアバージョン）によって詳細は異なる場合がありますので、本番環境に導入する前にテスト環境で検証することをおすすめします。

### 手順 1：ハードウェア検出

```bash
lsusb | grep -i sierra
# 想定される出力：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 手順 2：ツールパッケージのインストール

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 手順 3：USB コンポジションモードを QMI に切り替え

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# コンポジションモードの確認
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 想定される結果：USB composition 6: DM, NMEA, AT, QMI
```

> MBIM モードのみが必要な場合（一部のキャリアで要求されます）は、`AT!USBCOMP` 関連の設定を確認し、代わりに `mbimcli` をご使用ください。実際の数値は公式 AT コマンドリファレンスをご確認ください。

### 手順 4：FCC Auth ロック解除

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# ModemManager の内蔵自動化機能を使用する場合：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 手順 5：NetworkManager で接続

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'あなたのAPN'
sudo nmcli connection up 'EM7455 LTE'
```

### 手順 6：手動 QMI 接続（上級者向け / トラブルシューティング）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='あなたのAPN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## OpenWrt QMI 設定

EM7455 は OpenWrt コミュニティで互換性の高いモデルの一つです。以下は QMI モードの基本的な設定例です。

### パッケージのインストール

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### ネットワーク設定ファイルの編集

`/etc/config/network` を編集し、以下のインターフェース設定を追加します：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'あなたのAPN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### ネットワークの再起動

```bash
/etc/init.d/network restart
```

LUCI Web インターフェースを使用する場合：ネットワーク → インターフェース → 新しいインターフェースを追加 → プロトコルで「QMI」を選択、デバイスを `/dev/cdc-wdm0` に設定し、APN を入力してください。

> ROOter（OpenWrt ベースのセルラールーティングファームウェア）は Sierra QMI モジュールをサポートしており、`create_connect.sh` 関連のフックが内蔵されています。Raspberry Pi ユーザーの方は、ROOter ファームウェアの直接使用をご検討ください。正式なサポート範囲については ROOter 公式の発表をご確認ください。

---

## ブランド PC 互換性：Dell / Lenovo ノートパソコン

### Dell ノートパソコン（DW5811e は EM7455 プラットフォーム相当）

Dell DW5811e は Dell ブランド版の EM7455（VID `413c`、PID `81b6`）で、コアチップは同じ Qualcomm MDM9230 です。主要な Linux ディストリビューションの `qmi_wwan` ドライバーは一般的なブランド版 ID を収録済みです。実際に追加設定が必要かどうかは、実機でご確認ください：

```bash
lsusb | grep 413c
# 想定される出力：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Dell の主要機種（Latitude、Precision、XPS）は、コミュニティの報告によると BIOS ホワイトリストの制限がなく、DW5811e を直接インストールして使用できる場合がほとんどです。ただし、実際の状況は機種や BIOS バージョンによって異なりますので、お手持ちの実機でご確認ください。

### Lenovo ノートパソコン（EM7455 FRU）

Lenovo ThinkPad には BIOS ホワイトリストの制限があるというコミュニティでの報告があります。一部の機種は Lenovo FRU バージョンのモジュールのみを認識します。以下はコミュニティでこの制限を回避するために試行された AT コマンドの例です：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **このコマンド群については、弊社で個別に元の出典や正確性を確認しておりません。また、これらはモジュールの低レベルファームウェアの動作を変更する操作であり、実行を誤るとモジュールが使用不能になる（いわゆる「文鎮化」）リスクがあります。** これらは公開コミュニティの議論からまとめた例であり、Yupitek が検証済みの標準的な手順ではありません。試行される場合は、以下の点を強くおすすめします：現在のファームウェアバージョンを確認してバックアップする、重要でないテスト環境でのみ操作する、操作リスクはすべてご自身で負うものとします。不明な点がある場合は、実際のご要件と実現可能な方法について弊社までお気軽にご相談ください。

### ThinkPad 機種（コミュニティでこの種の設定が報告されている機種）

以下のリストはコミュニティでの議論をもとにまとめたものです。実際の適用可否や BIOS/ファームウェアの更新の要否については、お持ちの機種の公式仕様と BIOS バージョンをご確認ください。購入前に弊社または Lenovo 公式チャネルでご確認いただくことをおすすめします：

- 60 シリーズ：T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- 70 シリーズ：T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## プラットフォーム互換性一覧

| プラットフォーム | サポート | 接続方法 | 備考 |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ コミュニティ事例多数 | QMI / MBIM | M.2→USB 変換基板が必要 |
| Raspberry Pi + ROOter | ✅✅ | QMI（コミュニティ報告による内蔵フック） | Raspberry Pi ユーザーは優先的に検討 |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | 主要ディストリビューションでドライバーサポート充実 |
| DD-WRT | ⚠️ サポート限定的 | QMI / PPP | 新しい BETA ビルドが必要、コミュニティ事例は限定的 |
| pfSense / FreeBSD | ⚠️ サポート限定的 | QMI / PPP（主に AT コマンド経由） | FreeBSD ネイティブのセルラードライバーは限定的、個別評価が必要 |
| Dell ノート PC（DW5811e） | ✅ | QMI / MBIM | 主要ディストリビューションで認識可能、個別機種は実機確認推奨 |
| Lenovo ノート PC | ⚠️ 追加設定が必要 | QMI | 一部機種に BIOS ホワイトリスト制限あり、対応方法のリスクは上記参照 |

---

## コミュニティリソース

以下は EM7455 に関連する公開コミュニティおよび公式リソースです。さらなる調査の参考にしてください：

- **danielewood/sierra-wireless-modems**：EM7455/MC7455 関連の設定スクリプトとコミュニティ議論：[GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)**：Linux 設定に関するコミュニティ情報（カーネルオプション、ファームウェア更新、トラブルシューティング含む）：[Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE Wiki**：公式 LTE モデムサポートリストと設定：[OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen**：エンジニアリングモード関連ツール、PRI と周波数帯設定に関連する可能性あり：[GitHub](https://github.com/bkerler/SierraWirelessGen)

> 上記のサードパーティリソースのリンク先は弊社が管理するものではありません。実際にご利用になる際は、その正確性と最新性を各自でご判断ください。

---

## よくある質問（FAQ）

**Q1：EM7455 は 5G に対応していますか？**
対応していません。EM7455 は LTE-A Cat 6 モジュールで、最大 300 Mbps です。5G（Sub-6 または mmWave）が必要な場合は、EM9190（Sub-6）または EM9191（Sub-6 + mmWave）をご検討ください。

**Q2：EM7455 は台湾で使用できますか？**
一般的には台湾の主要キャリアの SIM カードでご利用いただけます。実際の信号品質や利用可能な周波数帯は、基地局の位置、キャリアのネットワーク計画、キャリアアグリゲーションの対応状況によって異なります。ご注文前に、お客様の地域とキャリアの互換性についてお問い合わせください。

**Q3：EM7455 と MC7455 の違いは何ですか？**
コアチップは同じ Qualcomm MDM9230 で、仕様は同一です。唯一の違いはパッケージ形式です：EM7455 は M.2、MC7455 は mPCIe です。お持ちのスロットに応じてお選びください。

**Q4：EM7455 が Ubuntu で認識されない場合はどうすればよいですか？**
まず `lsusb` で `1199:9079` が表示されるか確認してください。表示されない場合は、USB 2.0 ポートをお試しください（一部のケースでは USB 3.0 が干渉する可能性があります）。次に `qcserial` と `qmi_wwan` がロードされているか `lsmod | grep qmi` で確認します。ModemManager を停止（`systemctl stop ModemManager`）して、手動で `qmicli` を実行しトラブルシューティングすることもできます。解決しない場合は、弊社までお問い合わせください。

**Q5：Dell DW5811e は EM7455 と同じものですか？**
はい、DW5811e は Dell ブランド版の EM7455 で、コアは同じ Qualcomm MDM9230 チップです。Dell 版は中古市場での流通量が多く、入手コストも比較的低く、多くの Dell ノートパソコンでは BIOS ホワイトリストの制限がないと報告されていますが、実際の状況はお使いの機種に依存します。

---

## 購入に関するお問い合わせ

以上、EM7455 の仕様と設定情報は Yupitek（ユピテック）がまとめたものです。EM7455、EM7430、MC7455 または Sierra Wireless 全シリーズのセルラーモジュールのご購入については、製品ページでお問い合わせいただくか、技術チームまでご連絡ください。

- **製品ページ**：[https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **全シリーズ製品**：[https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **Email**：sales@yupitek.com
