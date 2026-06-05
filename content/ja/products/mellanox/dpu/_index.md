---
title: "NVIDIA BlueField データ処理ユニット (DPU)"
description: "NVIDIA BlueField DPUソリューションをご紹介。ARMベースのプログラマブルSmartNICにより、ネットワーク、ストレージ、セキュリティなどのインフラサービスをオフロード、高速化、隔離します。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField データ処理ユニット (DPU)

NVIDIA® BlueField® データ処理ユニット（DPU）は、データセンターのアーキテクチャに大きな変革をもたらす製品です。業界をリードするConnectXネットワークアダプターと、プログラマブルなARM® CPUコア、ハードウェアアクセラレーションエンジンを統合し、インフラ処理タスクをサーバーのCPUからオフロード、高速化、隔離します。

---

## BlueField DPU 取扱製品一覧

Yupitekでは、クラウド規模の仮想化、ソフトウェア定義ストレージ、ゼロトラストセキュリティ向けに構成されたBlueField DPU製品を提供しています。

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField プログラマブル・インフラストラクチャ・アダプター*

| 型番 | 製品名 | コアネットワーク仕様 | ARM CPUコア | メモリ | インターフェース | プロトコル | 形状 |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | デュアルポート 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | デュアルポート 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe（暗号化機能対応） |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | シングルポート 100GbE / EDR IB| 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe（暗号化機能対応） |

---

## 主要なDPUテクノロジー

### 1. インフラタスクのオフロード（SmartNIC+）
ハイパーバイザーのネットワークスイッチング（OVS）、仮想化トンネリング（VXLAN、NVGRE）、ネットワークアドレス変換（NAT）などに、ホストサーバーの貴重なCPUサイクルを消費する必要はありません。DPUは、**NVIDIA ASAP²（Accelerated Switch and Packet Processing）**テクノロジーを利用して、これらの処理をハードウェア上で直接ワイヤースピードにて実行します。

### 2. ソフトウェア定義ストレージの高速化
**NVMe SNAP™（Software-defined Network Accelerated Processing）**を用いることで、BlueField DPUは（RoCEv2またはTCP経由の）リモートストレージを、ホストOSに対してローカルの物理NVMeドライブとして認識させることができます。エミュレーション、暗号化、データ圧縮などの全処理がDPU上で完結するため、仮想化環境におけるストレージのボトルネックを解消します。

### 3. ゼロトラストセキュリティと環境隔離
DPUは、内蔵のARMコア上でホストサーバーから完全に独立した独自のLinux OS（主にUbuntu）を稼働させます。これにより、万が一ホスト側のOSが侵害された場合でも、DPU上で動作しているセキュリティエージェント、エージェントレスファイアウォール、ネットワーク暗号化処理（IPsec、TLS）などは影響を受けず、安全に稼働し続けます。

### 4. NVIDIA DOCA ソフトウェアフレームワーク
BlueField DPUは、**NVIDIA DOCA™**ソフトウェアフレームワークを用いて開発が可能です。DOCAはネットワーク、セキュリティ、ストレージ、テレメトリーといったインフラアプリケーション開発向けに、業界標準のAPIを提供します。

---

## 主なユースケース

- **次世代クラウドプロバイダー**：インフラ管理機能を完全にDPU側に隔離することで、セキュアなベアメタルホスティング環境を提供できます。
- **エンタープライズ向けハイパーコンバージドインフラ（HCI）**：ストレージやネットワークのオーバーレイ（VMware NSXやProxmox OVSなど）の処理をオフロードし、仮想マシンの集約密度を最大化します。
- **高度なセキュリティ環境**：ネットワーク境界上で直接、セキュリティ監視（IDS/IPS）や暗号化処理（IPsec/TLS）を実行します。

---

{{< alert >}}
製品のお見積もりをご希望ですか？[お問い合わせ](/ja/contact/)ください。
{{< /alert >}}
