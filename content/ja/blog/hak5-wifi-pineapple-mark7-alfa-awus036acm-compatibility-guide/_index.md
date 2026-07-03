---

title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM：5GHz 完全セットアップガイド（2026）"
description: "HAK5 WiFi Pineapple MK7 と ALFA AWUS036ACM (MT7612U) の完全互換性ガイド — プラグアンドプレイの 5GHz モニターモード、パケットインジェクション、PineAP 拡張。検証済みコマンド付きのステップバイステップ設定手順。ドライバーのコンパイル不要。"
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "WiFi Pineapple Mark VIIに外付けアダプターは必要ですか？"
    answer: "必要です。MK7内蔵無線は2.4 GHzのみをサポートし、2026年のほとんどのネットワークは5 GHzに移行済みで、外付けAWUS036ACMで5 GHzモニタリングとインジェクション機能を追加できます。"
  - question: "AWUS036ACMがMK7でプラグアンドプレイなのはなぜですか？"
    answer: "MK7 Firmware 2.xにkmod-mt76x2uドライバーがプリロードされており、MT7612UチップセットはLinux 4.19以降カーネルに内蔵されているため、コンパイルやインストールが不要です。"
  - question: "MK7のUSB 2.0はAWUS036ACMのパフォーマンスを制限しますか？"
    answer: "USB 2.0はスループットを150〜250 Mbpsに制限しますが、パケットキャプチャやハンドシェイク収集などのペネトレーションテストワークロードには影響せず、高スループットのブリッジングのみ制限されます。"
  - question: "MK7でMonitor Modeをどう有効にしますか？"
    answer: "SSHでログイン後、airmon-ng start wlan3コマンドを実行するとインターフェースがwlan3monにリネームされ、iwconfigでモードを確認します。"
  - question: "MK7と互換性のないALFAアダプターは？"
    answer: "AWUS036AXとAWUS036AXERはRTL8832BUチップを使用し、AWUS036EACSはRTL8811CUを使用し、ドライバーがモニターモードやインジェクションをサポートしないため互換性がありません。"
---

HAK5 WiFi Pineapple Mark VII は、ポータブルワイヤレスセキュリティ監査のゴールドスタンダードです。しかし初期状態では重大な制限があります：内蔵無線は **2.4 GHz** のみに対応しています。2026 年現在、ほとんどの企業および家庭用ネットワークは 5 GHz に移行しており、より優れたパフォーマンスと混雑の少なさを実現しています。


{{< tldr >}}
AWUS036ACMはMT7612Uチップセットを採用し、MK7 Firmware 2.xにドライバーがプリロード、挿入後wlan3インターフェースとして認識され、5 GHzモニターモード、パケットインジェクション、PineAP拡張をサポート、10分でセットアップ完了します。
{{< /tldr >}}
ここで **ALFA AWUS036ACM** の出番です。Hak5 が[公式に互換性を確認](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)した数少ない 802.11ac アダプターの一つであり、MK7 Firmware 2.x にプリロードされた `mt76x2u` カーネルドライバーのおかげで、**ドライバーのコンパイルが一切不要**のプラグアンドプレイを実現します。

本ガイドでは、ハードウェア仕様、ドライバーの互換性分析、検証済みの 7 ステップセットアップ手順、完全なペネトレーションテストトポロジーを網羅しています。

---

## 1. WiFi Pineapple に 5 GHz が必要な理由

| シナリオ | 2.4 GHz（内蔵） | 5 GHz（AWUS036ACM） |
|---|---|---|
| 企業 WPA2-Enterprise ネットワーク | 一部残存 | **最新デプロイの主要帯域** |
| 家庭用メッシュシステム | レガシーフォールバック | **クライアント接続のデフォルト帯域** |
| チャネル混雑 | 極度に混雑（1–11） | クリーンなスペクトラム（36–165） |

**結論**：最新のネットワークを監査するには 5 GHz が必要です。AWUS036ACM は MK7 に 5 GHz を追加する最も信頼性の高い方法です。

---

## 2. ターゲットプラットフォーム

### 2.1 ハードウェア仕様

| コンポーネント | 仕様 |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **ストレージ** | 2 GB eMMC |
| **USB Host** | 1× USB 2.0 Type-A（最大 480 Mbps） |
| **USB 給電能力** | 500 mA @ 5V |

### 2.2 ソフトウェア環境

| レイヤー | 詳細 |
|---|---|
| **OS** | OpenWrt（Hak5 カスタムビルド） |
| **カーネル** | 5.4.x（Firmware 2.x シリーズ） |
| **プリロードドライバー** | `kmod-mt76x2u`（MT7612U） |
| **パッケージマネージャー** | `opkg` |

> ✅ **重要な事実**：`kmod-mt76x2u` は Firmware 2.x にプリロード済み。AWUS036ACM は**プラグアンドプレイ**です。

---

## 3. ALFA AWUS036ACM 仕様

| 仕様 | 詳細 |
|---|---|
| **チップセット** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **周波数帯域** | 2.4 GHz + 5 GHz |
| **最大データレート** | 867 Mbps (5 GHz) |
| **モニターモード** | ✅ 対応 |
| **パケットインジェクション** | ✅ 対応 |
| **アンテナ** | 2× 5 dBi RP-SMA（着脱可能） |

---

## 4. 互換性マトリックス

| 評価項目 | 結果 |
|---|---|
| チップセット互換性 | ✅ **完全** |
| ドライバー可用性 | ✅ **プリロード済み** |
| モニターモード | ✅ **対応** |
| パケットインジェクション | ✅ **対応** |

---

## 5. ステップバイステップ設定

### 前提条件

- WiFi Pineapple MK7（Firmware 2.x）
- ALFA AWUS036ACM（PID `7612` を確認）

### ステップ 1：USB 検出の確認

```bash
ssh root@172.16.42.1
lsusb
```

### ステップ 2：ドライバー読み込み確認

```bash
lsmod | grep mt76
```

### ステップ 3：インターフェース確認

```bash
iw dev
```

### ステップ 4：モニターモード有効化

```bash
airmon-ng check kill
airmon-ng start wlan3
```

### ステップ 5：5 GHz チャネルスキャン

```bash
iw wlan3mon set channel 36
airodump-ng --band a wlan3mon
```

### ステップ 6：インジェクションテスト

```bash
aireplay-ng --test wlan3mon
```

### ステップ 7：起動時自動有効化

```bash
cat >> /etc/rc.local << 'EOF'
sleep 5
if iw dev wlan3 info > /dev/null 2>&1; then
    ip link set wlan3 down
    iw wlan3 set monitor control
    ip link set wlan3 up
    logger "AWUS036ACM set to monitor mode"
fi
EOF
```

---

## 6. 検証結果

全テストが MK7 Firmware 2.1.3 + 正規 ALFA AWUS036ACM で合格。

---


---

{{< faq >}}

## 7. 推奨

**ALFA AWUS036ACM は、WiFi Pineapple Mark VII を 5 GHz に拡張するための現在入手可能な最適なアダプターです。**

👉 [ALFA AWUS036ACM 製品ページ](/ja/products/alfa/awus036acm/)

Yupitek は ALFA Network 正規代理店です。全 ALFA × HAK5 統合シナリオに対して完全な技術サポートを提供します。

*設定サポートが必要ですか？Yupitek テクニカルサポートまで：[yupitek.com/support](/ja/support/)*

---

## 参考文献

1. [Hak5公式ドキュメント — 互換802.11acアダプターリスト](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
2. [OpenWrt mt76ドライバーリポジトリ — GitHub](https://github.com/openwrt/mt76)
3. [aircrack-ng — 無線セキュリティツールスイート公式ウェブサイト](https://www.aircrack-ng.org/)
4. [ALFA Network公式ウェブサイト — AWUS036ACM製品仕様](https://www.alfa.com.tw/)
5. [Linux Wireless — MT76x2Uドライバー説明](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
