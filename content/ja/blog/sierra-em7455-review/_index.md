---
title: "Sierra EM7455 完全レビュー：Maker と研究室で人気の Sierra カードの理由"
description: "EM7455 の完全レビュー：仕様、EM7430 との違い、OpenWrt/Linux 設定、Dell/Lenovo との互換性。技術資料は Yupitek（榆閤科技）が提供。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "EM7455 は 5G に対応していますか？"
    answer: "対応していません。EM7455 は LTE-A Cat 6 のモジュールで、最大速度は 300 Mbps です。5G が必要な場合は EM9190 または EM9191 をご検討ください。"
  - question: "EM7455 は日本でも使えますか？"
    answer: "対応バンドを持つ通信事業者の SIM カードであれば利用可能です。ただし実際の電波強度やキャリアアグリゲーションの効果は基地局のカバレッジに依存しますので、購入前にご相談ください。"
  - question: "EM7455 と MC7455 の違いは何ですか？"
    answer: "どちらも Qualcomm MDM9230 チップセットを搭載し、仕様は完全に同じです。唯一の違いはパッケージで、EM7455 が M.2、MC7455 が mPCIe です。お使いのスロットに合わせて選んでください。"
  - question: "EM7455 と EM7430 の違いは何ですか？"
    answer: "同じ MDM9230 チップセットで、コア仕様は同じです。主な違いは対応バンドで、EM7455 は米州と EMEA バンド、EM7430 はアジア太平洋バンドをカバーしています。"
  - question: "Dell DW5811e は EM7455 と同じですか？"
    answer: "はい。DW5811e は Dell のリブランド版 EM7455 で、コアは同じ Qualcomm MDM9230 チップセットです。"
---

# Sierra EM7455 完全レビュー：Maker と研究室で人気の Sierra カードの理由

Raspberry Pi に OpenWrt を組み合わせて使っている方、あるいは研究室の機器に 4G 通信を追加したい方は、Sierra EM7455 という名カードをご存じでしょう。Sierra Wireless が提供する LTE-A Cat 6 の M.2 セルラーモジュールで、Qualcomm MDM9230 チップセットを搭載し、下り最大 300 Mbps、上り最大 50 Mbps を実現します。さらに GNSS 測位機能を内蔵し、動作温度は -40°C から +85°C の過酷な環境にも耐えます。

本記事は Yupitek（榆閤科技）が整理し、この M.2 B-Key パッケージの 4G LTE-Advanced Cat 6 モジュールがなぜこれほど人気なのか、そして Linux システムでのドライバと設定の方法について解説します。

> 製品ページ：[EM7455 — Yupitek](/ja/products/sierra/em7455/) | 公式スペックシート：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完全スペック表：詳細データを一覧で

以下の数値は Sierra Wireless 公式スペックシートから整理したものです。実際にプロジェクトで発注する場合は、特にバンドやファームウェアバージョンなど更新される可能性のある項目について、最新版の公式ドキュメントを先にご確認いただくことをおすすめします。

| 項目 | 仕様 |
|---|---|
| **型番** | AirPrime EM7455 |
| **セルラー規格** | LTE-A Cat 6 |
| **チップセット** | Qualcomm MDM9230（Snapdragon X7 LTE） |
| **下りピーク** | 300 Mbps（LTE-A、2×CA） |
| **上りピーク** | 50 Mbps（LTE-A） |
| **キャリアアグリゲーション** | 2×CA（複数の組み合わせに対応、詳細は公式 AT コマンドリファレンス参照） |
| **パッケージ** | PCI Express M.2 B-Key（52-pin） |
| **サイズ** | 42 × 30 × 2.3 mm |
| **動作温度** | -40°C ~ +85°C（産業グレード） |
| **GNSS** | GPS、GLONASS、BeiDou、Galileo |
| **ホストインターフェース** | USB 3.0 / USB 2.0 High Speed |
| **LTE バンド** | 米州と EMEA（欧州/中東/アフリカ）の主要バンドをカバー。詳細なバンドリストは最新の公式スペックシートでご確認ください |
| **3G WCDMA バンド** | 最新の公式スペックシートをご確認ください |
| **汎用 VID:PID** | `1199:9079`（EM7455、一般バージョン） |
| **Dell DW5811e VID:PID** | `413c:81b6`（ブランドバージョン、実機の `lsusb` 結果を確認してください） |
| **Linux ドライバ** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主要ディストリビューションに標準搭載） |
| **汎用ファームウェア** | 公式 source.sierrawireless.com の最新バージョンをご利用ください |
| **キャリア認証** | 地域によって異なります（例：AT&T、Verizon、Vodafone など）。最新リストはお問い合わせください |

---

## EM7455 はどんなプロジェクトに適しているか？

**簡単に言えば、EM7455 は次の3つの用途の救世主です：（1）オープンソースで 4G LTE ルーターを構築（OpenWrt や ROOter など）、（2）Dell や Lenovo のノートPC の WWAN カードをアップグレード、（3）工場の研究室での IoT ゲートウェイや車両追跡。**

最大の強みは、Linux ドライバが非常に成熟していること、コミュニティにチュートリアルが豊富なこと、そして対応バンドが広いことです。

### Maker や学生のプロジェクト向け

| 用途 | 構成例 | 選ばれる理由 |
|---|---|---|
| Raspberry Pi 4G ルーター | Pi 4/5 + M.2 から USB 変換ボード + OpenWrt / ROOter | OpenWrt コミュニティでの互換性が非常に安定、uqmi パッケージも使いやすい |
| GL.iNet ルーターのアップグレード | GL-MT1300 / GL-AR750S + USB 変換 | ROOter の `create_connect.sh` 設定に関するコミュニティの議論が豊富で参考になる |
| 屋外用ポータブル LTE ホットスポット | バッテリー電源 + USB 変換 + 小型ルーター | 発熱が少なく放熱性が良好、屋外での物体追跡に適している |

### エンタープライズや産業用途

| 用途 | 構成例 | 選ばれる理由 |
|---|---|---|
| 産業用ルーター | M.2 スロット搭載の産業用ゲートウェイ（例：Advantech） | 堅牢で、-40~85°C のワイドテンプレート仕様が安心、バンドも豊富 |
| 車両テレマティクス | 車載ゲートウェイ + GNSS アンテナ | GPS/GLONASS などの測位機能を内蔵、通信と測位を1枚で解決 |
| ノートPC の WWAN アップグレード | Dell Latitude / Lenovo ThinkPad シリーズ | M.2 B-Key にそのまま挿せて、Linux でもプラグアンドプレイの可能性が高い |
| WAN フェイルオーバー | OpenWrt / pfSense のデュアル WAN | QMI/MBIM のデュアルモードに対応（pfSense のサポートは不確実なため、OpenWrt を推奨） |

---

## EM7455 と EM7430 の違いは？

よくある質問です。実は **EM7455 と EM7430 はまったく同じ Qualcomm MDM9230 チップセットを採用しており、コア仕様（Cat 6、300/50 Mbps、2×CA、GNSS）は同じです。大きな違いは「対象とする市場のバンド」だけ**です。EM7455 は主に米州と欧州/中東/アフリカ（EMEA）向け、EM7430 は主にアジア太平洋（APAC）地域向けです。

| 項目 | EM7455 | EM7430 |
|---|---|---|
| **チップセット** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **セルラー規格** | LTE-A Cat 6 | LTE-A Cat 6 |
| **下りピーク** | 300 Mbps | 300 Mbps |
| **上りピーク** | 50 Mbps | 50 Mbps |
| **キャリアアグリゲーション** | 2×CA | 2×CA |
| **パッケージ** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **対象地域** | 米州、EMEA | アジア太平洋（APAC） |

**選定のヒント**：お使いの SIM カードが北米や欧州中心であれば **EM7455** を、アジア太平洋地域（日本、オーストラリアなど）であれば理論上 **EM7430** が適しています。ただし通信事業者のバンド構成は地域ごとに特殊な場合がありますので、発注前にどちらのカードが最適かご相談ください。

---

## EM7455 vs MC7455：チップは同じ、異なるのはピン形状だけ

前述のとおり、EM7455（M.2）と MC7455（mPCIe）は同じ Qualcomm MDM9230 を採用し、電気仕様も完全に同じです。唯一の違いは「外皮」、つまりパッケージです：

| 項目 | EM7455 | MC7455 |
|---|---|---|
| **パッケージ** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **サイズ** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **適した機器** | ノートPC の WWAN スロット、最新の開発ボード | 旧型のパネルPC の mPCIe スロット |
| **汎用 VID:PID** | `1199:9079` | `1199:9071` |

**これは簡単です。お使いのデバイスのスロット形状に合わせて選んでください。** 万一間違えても、変換アダプター（M.2 から mPCIe、またはその逆）で補えます。

---

## Linux での設定方法（Ubuntu / Debian / Linux Mint）

EM7455 は一般的な Linux システムでのサポートが非常に良好です。以下はコミュニティで一般的な基本設定手順です。ただし OS バージョンやカーネルはマシンごとに異なりますので、まずテスト機で試してから本番環境に適用してください。

### ステップ 1：ハードウェアの認識を確認

```bash
lsusb | grep -i sierra
# 以下のような出力が表示されます：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### ステップ 2：必要なツールをインストール

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### ステップ 3：USB モードを QMI に切り替え

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# モード切り替えが成功したか確認
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 出力：USB composition 6: DM, NMEA, AT, QMI
```

> 一部の通信事業者で MBIM モードが要求される場合は、`AT!USBCOMP` コマンドを調べて `mbimcli` で接続してください。

### ステップ 4：FCC 認証の解除

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# ModemManager で完全自動化したい場合：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### ステップ 5：NetworkManager で接続

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'YOUR_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### ステップ 6：手動 QMI 接続（より高度なトラブルシューティング用）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='YOUR_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## OpenWrt での QMI 設定

EM7455 は OpenWrt コミュニティでも評価が高いです。OpenWrt を導入したルーターをお持ちの場合は、以下の QMI 設定をご参考ください。

### 必要なパッケージのインストール

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### ネットワーク設定ファイルの編集

`/etc/config/network` を開き、以下のインターフェース設定を追加します：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'YOUR_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### ネットワークの再起動

```bash
/etc/init.d/network restart
```

GUI（LuCI Web インターフェース）をお好みの場合は、Network から Interfaces を開き、新しいインターフェースを追加して、プロトコルに QMI、デバイスに `/dev/cdc-wdm0` を選択し、APN を入力するだけです。

> ヒント：Raspberry Pi をお使いの方は、OpenWrt ベースで 4G/5G ルーティングに特化したファームウェア ROOter を強くおすすめします。便利な設定フックが多数内蔵されています。

---

## ブランドノートPC との互換性：Dell と Lenovo

### Dell ノートPC（DW5811e というカードがそれです）

オンラインでよく見かける Dell DW5811e は、実は Dell のリブランド版 EM7455 です（VID が `413c`、PID が `81b6` に変更）。内部のチップは同じ MDM9230 で、ほとんどの Linux `qmi_wwan` ドライバはすでに認識しています。

```bash
lsusb | grep 413c
# 出力例：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

良いニュースとして、Dell のノートPC（Latitude、Precision など）の多くは、コミュニティの報告によると BIOS ホワイトリストによる制限がなく、そのまま挿して使用できることが多いです。

### Lenovo ノートPC（厄介なホワイトリスト）

Lenovo ThinkPad をお使いの場合は注意が必要です。Lenovo は BIOS にホワイトリストを設定し、Lenovo 純正 FRU バージョンのカードのみを許可する場合があります。フォーラムで制限を回避する AT コマンドを共有している上級者もいます。挑戦意欲のある方はご参考ください：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **警告：これらのコマンドはフォーラムから収集したものです。誤って実行するとカードが文鎮化する可能性があります。** ハードウェアの分解やリスクを受け入れる上級ユーザーでない限り、発注前に安全な代替案についてお問い合わせください。

---

## 対応プラットフォーム一覧

| プラットフォーム | サポート度 | 接続方式 | 備考 |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ 非常に安定、チュートリアル豊富 | QMI / MBIM | M.2 から USB への変換ボードが必要 |
| Raspberry Pi + ROOter | ✅✅ | QMI | Pi ユーザーに強くおすすめ |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | プラグアンドプレイの可能性が非常に高い |
| DD-WRT | ⚠️ 運次第 | QMI / PPP | コミュニティの議論が少なく、初心者には不向き |
| pfSense | ⚠️ 不安定 | QMI / PPP | 手間を避けるなら OpenWrt への切り替えを検討 |
| Dell ノートPC | ✅ | QMI / MBIM | 基本的に Linux で認識される |
| Lenovo ノートPC | ⚠️ 回避策が必要な場合あり | QMI | BIOS ホワイトリストに注意、乱暴なコマンド実行は文鎮化のリスク |

---

## さらに詳しい情報はどこで探せるか？

プロジェクトで行き詰まったら、以下のオープンソースコミュニティをご活用ください：

- **danielewood の GitHub**：EM7455/MC7455 のスクリプトとディスカッションが充実。
- **Gentoo Wiki**：Linux の上級者が詳細なトラブルシューティングをまとめています。
- **OpenWrt LTE Wiki**：公式ドキュメント。ネットワーク設定前に必ず確認してください。

## よくある質問（FAQ）

{{< faq >}}

---

## 研究室での調達は、ぜひお問い合わせください

本記事は Yupitek（榆閤科技）のエンジニアチームが整理しました。大学のプロジェクト、実験室の計画、あるいは EM7455 やその他の Sierra モジュールの法人向け大量調達まで、お気軽にご相談ください！

- **このカードを見る**：[https://yupitek.com/ja/products/sierra/em7455/](/ja/products/sierra/em7455/)
- **全 Sierra 型番を見る**：[https://yupitek.com/ja/products/sierra/](/ja/products/sierra/)
- **メールでお問い合わせ**：sales@yupitek.com
