---
title: "NVIDIA Mellanox LinkX 光トランシーバー"
description: "純正のNVIDIA Mellanox LinkX光トランシーバーモジュールをご案内。マルチモードおよびシングルモード向けに、25G、100G、400G、800Gの高速光トランシーバーをラインナップ。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 光トランシーバー — 25G〜800G

NVIDIA LinkX® 光トランシーバーは、ハイパフォーマンス・コンピューティング（HPC）、エンタープライズストレージ、およびハイパースケール環境の厳しい要求を満たすよう設計されています。純正トランシーバーを使用することで、最適な信号整合性の確保、ビット誤り率（BER）の極小化、およびConnectXアダプターやQuantumスイッチとの完全な互換性を保証します。

---

## 光トランシーバー 製品カタログ

以下は、現在弊社で取り扱っている光トランシーバーモデルの一覧です。

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR 光トランシーバー</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 光トランシーバー</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR 光トランシーバー</p>
  </div>
</div>

| 型番 | 速度 | インターフェース | コネクタ形状 | 波長 | ファイバー種別 | 最大伝送距離 | 説明 |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC 2芯（LC Duplex） | 850nm | マルチモード (MMF) | 150m (OM4) / 100m (OM3) | 25GbE SR モジュール |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | マルチモード (MMF) | 100m (OM4) / 70m (OM3) | 100GbE SR4 モジュール、DDMI対応 |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850nm | マルチモード (MMF) | 50m (OM4) | NDR IB/ETH SR モジュール、フラットトップ型 |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850nm | マルチモード (MMF) | 50m (OM4) | 2xNDR ツインポート SR モジュール、フィン（ヒートシンク）型 |

---

## 伝送距離＆配線ガイド

### 1. SR、SR4、NDR（マルチモードソリューション）
- **25G SR (SFP28)**：標準的な LC-LC 2芯マルチモード光パッチケーブルを使用します。送受信にそれぞれ1レーンを使用する最も一般的な接続方法です。
- **100G SR4 (QSFP28)**：12芯の MPO (MPO-12) リボンパッチケーブル（通常は Type-B 極性）を使用します。25Gの並列4レーンを利用して100Gの伝送を行います。
- **400G/800G NDR (OSFP)**：PAM4変調技術を駆使し、MPO-12 APC（斜め物理接触）コネクタ経由で極めて高い帯域幅を伝送します。端面を傾斜カットすることで後方反射（バックリフレクション）を抑えており、高速伝送時でも高い品質を保てます。

### 2. シングルモード（LR4/FR4）とマルチモード（SR/SR4）
- **マルチモード (MMF)**：同一ラック内や近接するラック間などの短距離配線（最長100〜150m）に適しています。トランシーバー本体の導入コストを抑えられるメリットがあります。
- **シングルモード (SMF)**：150mを超える長距離伝送（LR4で最長10km）の際に必要です。9/125µm径のファイバーと、2芯の LC コネクタを使用します。

---

## 技術解説：純正品（OEM）とサードパーティ製品の違い

トランシーバーの導入検討時によく「安価なサードパーティ製品やプログラミング済みの互換モジュールでも問題ないか」というご質問をいただきます。

### 弊社が純正の NVIDIA LinkX を強く推奨する理由：
1. **ファームウェアの互換性**：NVIDIA ConnectX NICやQuantumスイッチは、専用のオペレーティングシステム（MLNX-OSやOnyxなど）で動作しています。システムのアップデートを行った際に、他社互換モジュールが認識されなくなったり、エラーフラグが立ってポートが停止（Link Down）したりするトラブルが後を絶ちません。
2. **診断機能（DDM/DOM）の信頼性**：純正モジュールは、動作温度、電圧、送信（TX）/受信（RX）電力などの測定値を正確にシステムコントローラー（DellのiDRAC、HPEのiLO、またはMLNX-OS）に報告します。データにブレがないため、誤検知による温度警告やシャットダウンを防止できます。
3. **高度な機能のサポート**：LinkX モジュールは、前方誤り訂正（FEC）などの主要なエラー訂正設定があらかじめ検証された状態で出荷されます。大量のデータが流れるデータベース処理などにおいて、パケットロスを最小限に抑えます。

---

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
