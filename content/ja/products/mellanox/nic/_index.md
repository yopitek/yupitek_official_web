---
title: "NVIDIA Mellanox ConnectX ネットワークインターフェースカード (NIC)"
description: "NVIDIA Mellanox ConnectX-4 Lx、ConnectX-5、ConnectX-6 Dx/Lx、ConnectX-7 NIC アダプターを比較。PCIe Gen3/4/5 に対応し、10G、25G、50G、100G、200G、400Gの各製品を取り扱い。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Mellanox / NVIDIA ConnectX ネットワークカード — 10G〜400G

NVIDIA Mellanox ConnectX アダプターは、企業向けサーバーやAIクラスタへ業界最高水準の帯域幅と極めて低いレイテンシを提供します。以下は、Yupitekが取り扱うConnectXシリーズの製品カタログです。通信速度別に分類しています。

---

## 10GbE / 25GbE ネットワークカード

一般的なエンタープライズサーバー、仮想化環境（VMware ESXi）、高性能NASストレージなどに最適です。

### 10Gモデル

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | ブラケット |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | デュアル | 10GbE | PCIe 3.0 x8 | SFP28 | Ethernet | フルハイト |

### 25Gモデル

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*NVIDIA ConnectX-4 Lx 25GbE デュアルポート アダプター*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*NVIDIA ConnectX-5 25GbE デュアルポート アダプター*

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | ブラケット / 形状 | 特徴・仕様 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | デュアル | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | フルハイトブラケット | 標準PCIeカード |
| **MCX4121A-ACUT** | ConnectX-4 Lx | デュアル | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | フルハイトブラケット | UEFI対応 |
| **MCX512A-ACAT** | ConnectX-5 EN | デュアル | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | フルハイトブラケット | 強化RoCEv2対応 |
| **MCX512A-ACUT** | ConnectX-5 EN | デュアル | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | フルハイトブラケット | UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | デュアル | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | フルハイトブラケット | セキュアブート、暗号化非対応 |
| **MCX623432AS-ADAB**| ConnectX-6 Lx | デュアル | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | OCP 3.0（つまみねじ） | セキュアブート、OCP 3.0仕様 |

---

## 50GbE / 100GbE ネットワークカード

高速なNVMe over Fabrics（NVMe-oF）ストレージ、ハイパーコンバージドインフラ（HCI）、データベースサーバーなどに最適です。

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*NVIDIA ConnectX-5 100GbE アダプター*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*NVIDIA ConnectX-6 Dx 100GbE デュアルポート アダプター*

### 50Gモデル

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | ブラケット |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | シングル | 50GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | フルハイト |

### 100Gモデル

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | 形状 | 特徴・仕様 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | シングル | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | フルハイトPCIe | 標準100G NIC |
| **MCX555A-ECAT** | ConnectX-5 VPI | シングル | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | フルハイトPCIe | EDR IB & 100GbE対応 |
| **MCX516A-CCAT** | ConnectX-5 EN | デュアル | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | フルハイトPCIe | デュアルポート100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | デュアル | 100GbE | PCIe 4.0 x16 | QSFP28 | Ethernet | フルハイトPCIe | PCIe 4.0対応 |
| **MCX556A-ECAT** | ConnectX-5 VPI | デュアル | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | フルハイトPCIe | デュアルポートEDR IB対応 |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| デュアル | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | フルハイトPCIe | PCIe 4.0デュアルポートEDR対応 |
| **MCX653105A-ECAT**| ConnectX-6 VPI | シングル | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | フルハイトPCIe | HDR100 IB & 100GbE対応 |
| **MCX653106A-ECAT**| ConnectX-6 VPI | デュアル | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | フルハイトPCIe | HDR100 IB & 100GbE対応 |
| **MCX623106AN-CDAT**| ConnectX-6 Dx | デュアル | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | フルハイトPCIe | デュアルポート100G（SFP56/QSFP56） |
| **MCX623436AN-CDAB**| ConnectX-6 Dx | デュアル | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | OCP 3.0（つまみねじ） | OCP 3.0仕様 |

---

## 200GbE / 400GbE ネットワークカード

AI GPUサーバーノード（NVIDIA HGX/DGXなど）、高頻度取引（HFT）、HPCネットワークバックボーン向けに設計されたフラグシップアダプター。

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*NVIDIA ConnectX-7 400G OSFP アダプター*

### 200Gモデル

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | 形状 | 特徴・仕様 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | シングル | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | フルハイトPCIe | HDR IB & 200GbE対応 |
| **MCX653106A-HDAT**| ConnectX-6 VPI | デュアル | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | フルハイトPCIe | デュアルポート HDR/200G |
| **MCX623105A-VDAT**| ConnectX-6 Dx | シングル | 200GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | フルハイトPCIe | シングルポート 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | シングル | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | フルハイトPCIe | NDR200、Socket Direct対応 |
| **MCX755106AS-HEAT**| ConnectX-7 VPI | デュアル | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | フルハイトPCIe | 第1ポート: IB、第2ポート: VPI |
| **MCX753436MS-HEAB**| ConnectX-7 VPI | デュアル | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0（つまみねじ） | OCPマルチホスト / Socket Direct対応 |

### 400Gモデル

| 型番 | 世代 / チップセット | ポート数 | 速度 | PCIeスロット | コネクタ形状 | プロトコル | 形状 | 特徴・仕様 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | シングル | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | フルハイトPCIe | NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | シングル | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | フルハイトPCIe | NDR OSFP、Socket Direct対応 |

---

## 技術選定ガイド

ConnectX アダプターを選定する際は、以下のポイントをご確認ください。

### 1. プロトコルモード（VPI と EN）
- **EN アダプター**：Ethernet ネットワークのみに対応しています。
- **VPI アダプター**：ファームウェア設定により、InfiniBand または Ethernet のいずれかのモードで動作させることができます。システムの構成変更に柔軟に対応できるため、インフラの流動性が高い環境に適しています。

### 2. PCIe 帯域幅の要件
ホストサーバーの PCIe バージョンとスロット数が、カードの最大性能を引き出すのに十分か確認してください。
- 例えば、デュアルポートの 100G NIC で両ポートのフル帯域（計200G）を同時に引き出すには、PCIe 4.0 x16 スロットが必要です。
- PCIe 4.0 対応カードは PCIe 3.0 スロットとも後方互換性がありますが、通信スループットは PCIe 3.0 の物理上限（x8 スロットで約 64Gbps、x16 スロットで約 128Gbps）に制限されます。

### 3. OCP 3.0 と標準 PCIe フォームファクター
型番の末尾が `-ADAB`、`-CDAB`、`-HEAB` などで終わるモデルは、**OCP NIC 3.0** フォームファクターを採用しています。これらのカードは、主要サーバーベンダー（Supermicro、Dell、HPE、Lenovoなど）の最新世代サーバーに搭載されている専用スロットに差し込んで使用します。標準的な PCIe スロットには装着できませんのでご注意ください。

---

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
