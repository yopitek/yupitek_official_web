---
title: "Sierra OpenWrt／Raspberry Pi で EM7565 を認識できない？QMI／MBIM トラブルシューティング完全ガイド"
description: "OpenWrt や Raspberry Pi で EM7565 を認識できない、QMI port が消えてしまった。このトラブルシューティングガイドでは、lsusb、dmesg から USB composition、ドライバのロード、EM7565 の設定手順までを解説し、ハードウェアとソフトウェアの接続問題を解決します。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/ja/products/sierra/em7565/"
faq:
  - question: "OpenWrt で EM7565 を認識できない場合、最も多い原因は何ですか？"
    answer: "最も多いのは電源不足（VCC が 3.135 から 4.4V の範囲外）で lsusb に表示されないケース、または USB composition の設定ミスで QMI インターフェースが有効になっていないケースです。"
  - question: "EM7565 が再起動を繰り返して起動しない場合、故障でしょうか？"
    answer: "故障とは限りません。SED 保護メカニズムがあり、異常な再起動が 6 回連続すると保護状態に入りますが、ファームウェアを再ダウンロードすれば復旧できます。"
---

OpenWrt や Raspberry Pi で EM7565 をどうしても認識できない場合、まずモジュールの交換を急がないでください。本記事では、公式仕様書に記載されたトラブルシューティングの流れをまとめています。USB ハードウェアレベルでの接続確認、USB composition の確認、正しい Linux ドライバのロード、システムサービスの干渉排除、そして厄介なファームウェアの SED 状態への対応まで、5 つのステップで問題の原因を素早く特定できます。

{{< tldr >}}
EM7565 を認識できない場合は、次の 5 点を確認してください。1. `lsusb` で USB レベルを確認（給電と変換ボードを点検）。2. QMI/MBIM インターフェースと `/dev/cdc-wdm0` の有無を確認し、`qmi_wwan` / `cdc_mbim` ドライバと USB composition を点検。3. `ModemManager` を停止してシステムサービスの干渉を排除。4. 給電シーケンスを確認（通電後 100ms 以内は信号を駆動せず、リップルは 100mVp-p 以下）。5. ファームウェアの状態を確認：起動失敗が 6 回連続すると SED 保護に入るため、ファームウェアの再ダウンロードが必要です。原則は、ハードウェアを先に、次にソフトウェア、最後にファームウェアです。
{{< /tldr >}}

**EM7565 は Qualcomm MDM9250 を搭載した M.2 WWAN Type 3042-S3-B の 4G LTE-Advanced モジュールです。QMI と MBIM の両方の USB インターフェースに対応しています。** OpenWrt や Raspberry Pi で「認識できない」場合、原因は通常 3 つあります。USB に電源が供給されていない、USB composition が誤った組み合わせのまま停止している、または Linux ドライバが正しくロードされていない、です。まれに、再起動の繰り返しによって保護モードに入ることもあります。本記事では、Sierra Wireless の公式マニュアルに沿って、最もミスの少ない調査手順を整理しました。

> 製品リンク：[Yupitek Sierra Wireless シリーズ](https://yupitek.com/ja/products/sierra/)

## クイック結論：EM7565 を認識できないときは、この 5 ステップで調査

トラブルシューティングで最も多い失敗は、いきなりファームウェアを書き込もうとすることです。**まずハードウェアを確認し、次にソフトウェア、最後にファームウェアを扱います。**

1. **USB レベルを確認**：`lsusb` でモジュールの有無を確認します。表示されない場合は、給電（VCC は 3.135 から 4.4V が必須）、変換ボード、USB ケーブルを点検してください。
2. **QMI／MBIM インターフェースを確認**：`lsusb` では表示されるのに `/dev/cdc-wdm0` が存在しない場合は、`qmi_wwan` / `cdc_mbim` ドライバのロード状況と、USB composition が診断モードのみになっていないかを確認します。
3. **システムサービスを確認**：システムの `ModemManager` がモジュールを占有している場合があります。
4. **給電シーケンスを確認**：通電後は少なくとも 100ms 以内に信号を駆動せず、電源リップルは 100mVp-p 以下に抑えます。電圧が不安定だと USB が切断と再接続を繰り返します。
5. **ファームウェアの状態を確認**：起動失敗後のリセットが 6 回連続すると、SED（Smart Error Detection）保護状態に入ります。この場合はファームウェアの再ダウンロードが必要です。

## EM7565 とは：どのようなモジュールか

トラブルシューティングの前に、EM7565 の概要を確認しましょう。本モジュールは 3 本の外部アンテナ（Main、GNSS、Aux）を必要とします。アンテナは付属していません。

| 項目 | 公式仕様（Doc# 41110788、Rev 8） |
|---|---|
| **チップ** | Qualcomm MDM9250 |
| **フォームファクタ** | M.2 (3042-S3-B) / 42 × 30 mm、厚さ最大 1.50mm、重量 6.5g |
| **ダウンロード最大** | Cat 12 (3CA, 256QAM) 最大 600 Mbps |
| **アップロード最大** | Cat 13 (2CA, 64QAM) 最大 150 Mbps |
| **LTE バンド** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66（注：B42/B43/B48 は法規制承認待ちのため disabled と記載） |
| **通信インターフェース** | USB 2.0 と USB 3.0；QMI / MBIM / AT コマンド |
| **供給電圧** | VCC 3.135V(min) / 3.3V(typ) / 4.4V(max)、リップル ≤ 100mVp-p |
| **動作温度** | 内部温度は 90°C 未満（できれば 80°C 未満）を推奨 |

## ステップ 1：USB レベルから調査

このホストはハードウェアを「認識」しているでしょうか。

```bash
lsusb
```

Sierra Wireless または 1199 で始まるデバイスが表示されれば、ハードウェアの接続は成功しています。表示されない場合は、次の点を確認してください。

- 電源を確認：EM7565 の起動時突入電流は 2.2A から 2.5A に達することがあります（最大動作電流は 1.5A）。多くの Raspberry Pi 用 USB 変換ケースでは対応できません。
- 時間を置く：挿入後は 10 秒ほど待って、USB の認識プロセスが完了するのを待ちましょう。

続いてカーネルログを確認します。

```bash
dmesg | tail -50
```

`qmi_wwan` が `/dev/cdc-wdm0` を作成していれば、接続の準備ができています。

## ステップ 2：USB composition を確認

`lsusb` ではモジュールが表示されるのに `/dev/cdc-wdm0` が生成されない場合、モジュールが QMI/MBIM チャネルを無効にしている可能性があります。モジュール内には USB composition という設定があり、公開するチャネルを決定します。

この場合は `AT!USBCOMP?` コマンドで確認します。むやみに切り替えるとチャネルをすべて失う恐れがあるため、切り替え前には必ず元のパラメータを記録し、公式の AT コマンドマニュアル（Doc#41111748）を参照してください。

## ステップ 3：ModemManager の干渉を排除

デスクトップ版 Linux や Raspberry Pi では、`ModemManager` という組み込みサービスが 4G モジュールを占有してしまうことがあります。制御権を奪われると、自分で入力する `qmicli` コマンドが止まってしまいます。

手動でトラブルシューティングする場合は、まずこれを停止してください。

```bash
sudo systemctl stop ModemManager
```

モジュールに問題がないことを確認したら、手動でダイヤルするか、ModemManager に制御を戻すかを判断します。

## ステップ 4：ファームウェアはロックされていませんか（SED 保護メカニズム）

起動後にモジュールが無限に再起動を繰り返す場合、**SED（Smart Error Detection）** 状態に入っている可能性があります。

公式仕様書には明確に記載されています。起動直後にリセットが 6 回連続すると、モジュールは bootloader 内で待機状態になり、ファームウェアの再書き込みを待ちます。これは通常、電源が不安定（電圧の急激な低下）なために発生します。

モジュールの故障と決めつけず、より安定した電源に交換し、公式ツールでファームウェアを再書き込みすれば復旧できます。

## QMI でのダイヤルアップ方法（OpenWrt の例）

上記の問題を解決し、`/dev/cdc-wdm0` が出現すれば、OpenWrt でのダイヤルアップは非常に簡単です。

1. 必要なパッケージをインストールします。

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. `/etc/config/network` で APN を設定します（通信事業者の値を使用）。

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. ネットワークを再起動します。

```bash
/etc/init.d/network restart
```

これで `wwan0` インターフェースが出現し、インターネットに接続できます。

## まとめ

OpenWrt や Raspberry Pi で EM7565 を認識できない問題は、パソコンの修理と同じで、手順が正しければ素早く解決できます。

1. **ハードウェアを確認**：`lsusb` の結果と電圧の安定性。
2. **インターフェースを確認**：USB composition が正しいか。
3. **ソフトウェアを確認**：ドライバがインストールされているか、ModemManager と競合していないか。
4. **ファームウェアを確認**：再起動の繰り返しでロックされていないか。

ファームウェアをむやみに書き込まなければ、ほとんどの問題は 10 分以内に原因を特定できます。

## 購入情報（Call To Action）

お手持ちの変換ボードやアンテナが EM7565 に対応するか不明ですか？Yupitek（榆閤科技）では、Sierra Wireless 全シリーズの製品と、完全なハードウェア統合ソリューションを提供しています。

お問い合わせ：**sales@yupitek.com**

製品ページをご覧ください：[EM7565 製品ページ](https://yupitek.com/ja/products/sierra/em7565/)
