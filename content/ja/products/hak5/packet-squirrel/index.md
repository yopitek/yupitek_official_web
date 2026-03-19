---
title: "Packet Squirrel Mark II"
date: 2025-01-01
draft: false
description: "WireGuard / OpenVPN VPNと5種類のネットワークモードをサポートする、ポケットサイズのEthernet中間者攻撃多機能ツールです。"
featureimage: "/images/products/hak5/packet-squirrel.png"
---

## 製品特長

![Packet Squirrel Mark II](/images/products/hak5/card/packet-squirrel.png)

- **多機能Ethernet MitMツール**：ポケットサイズ。5つのネットワークモードをサポート：NAT、BRIDGE、TRANSPARENT、JAIL、ISOLATE
- **デュアルVPN対応**：WireGuardとOpenVPN接続を同時サポート
- **Web UI + SSHアクセス**：デフォルト管理IP：172.16.32.1:1471
- **4段モード切替**：1ボタンで再起動 / 工場出荷時設定へのリセット
- **USBストレージ拡張**：USB-A 2.0対応、オプションのLUKSフルディスク暗号化をサポート
- **マルチ言語Payload**：Bash / Pythonで記述、DuckyScriptをサポート
- **Cloud C²対応**：リモート管理
- **セキュアワイプ**：SELFDESTRUCTペイロードコマンドをサポート

## 主な仕様

| 仕様項目 | 内容 |
|---------|------|
| インターフェース | デュアルEthernet（TargetポートおよびNetworkポート）、USB-C（電源）、USB-A 2.0（ストレージ） |
| ネットワーク規格 | 802.3 |
| 電源 | USB-C（5V） |
| デフォルト管理IP | 172.16.32.1 |
| OS | Linuxベース |
| LED | マルチカラーステータスLED |

## 適用シナリオ

- 企業ネットワーク中間者攻撃（MitM）によるパケットキャプチャと分析
- 隠蔽VPNトンネルの構築（WireGuard / OpenVPN）
- レッドチームのネットワーク植込みとリモート持続アクセス
- トラフィック操作、DNSスプーフィング（SPOOFDNS）、パケットインジェクション
- Blue Team演習：疑わしいデバイスの隔離（JAIL / ISOLATEモード）
- 企業ネットワーク脆弱性評価の自動化
