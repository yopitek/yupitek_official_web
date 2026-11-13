---
title: "USB Rubber Ducky"
date: 2025-01-01
draft: false
description: "普通のUSBフラッシュドライブと外観が全く同一のキーストロークインジェクション攻撃ツールです。DuckyScript™ 3.0による条件ロジックとOS検出に対応しています。"
featureimage: "/images/products/hak5/usb-rubber-ducky.png"
---

{{< alert "warning" >}}
**法的使用に関する免責事項**: USB Rubber Duckyは専門的なHIDインジェクション研究ツールです。許可されたセキュリティテストおよび研究目的でのみ使用してください。有効な書面による許可を得たセキュリティ専門家、セキュリティ教育機関、CTF競技会のみを対象としています。第三者のデバイスに対する無許可のHIDインジェクションは違法です。
{{< /alert >}}

## 製品特長

![USB Rubber Ducky](/images/products/hak5/card/usb-rubber-ducky.png)

- **キーストロークインジェクションの始祖**：2010年にキーストロークインジェクション攻撃を発明。2022年に全面刷新
- **完璧な偽装**：普通のUSBフラッシュドライブと外観が完全に同一。PCが自動的に信頼済みHIDキーボードとして認識
- **DuckyScript™ 3.0**：変数、フロー制御、ロジック判断、OS検出、関数をサポート
- **OS検出**：OS_DETECT拡張機能でターゲットOS（Windows、macOS、Linux、ChromeOS、Android、iOS）を識別
- **Keystroke Reflection**：ターゲットマシンの状態を読み返す
- **ダイナミック攻撃モード**：HID + ストレージ攻撃モードを動的切替（ATTACKMODE）
- **デバイスなりすまし**：任意のUSBデバイスのVID / PID / ベンダー / シリアル番号をなりすまし
- **コミュニティPayload**：PayloadHubコミュニティの数百の既製Payloadと互換

## 主な仕様

| 仕様項目 | 内容 |
|---------|------|
| USB | ハイスピードUSB 2.0 |
| インターフェース | USB-A + USB-Cデュアルヘッド（Mark II版） |
| ストレージ | MicroSDカード付属（ペイロード保存用） |
| スクリプト言語 | DuckyScript™ 3.0 |

## 適用シナリオ

- 物理アクセス攻撃：認証情報の窃取、バックドア植込み、DNSポイズニング
- レッドチームによる自動化ソーシャルエンジニアリングシミュレーション
- 複雑なITタスクの自動化（正当な用途）
- セキュリティトレーニングとペネトレーションテストコース

## 公式ドキュメント & ダウンロード

| リソース | リンク |
|----------|--------|
| �� 公式ドキュメント | [オンラインで見る](https://documentation.hak5.org/hak5-usb-rubber-ducky/master) |
| ⬇️ ファームウェア & ツール | [Hak5 ダウンロード](https://downloads.hak5.org/ducky) |

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
