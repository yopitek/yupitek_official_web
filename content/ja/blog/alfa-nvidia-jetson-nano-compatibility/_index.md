---
title: "ALFA無線ネットワークカードがNVIDIA Jetson Nanoをサポートしているかどうか"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "ハードウェアガイド"
description: "Jetson Nanoは多くのALFAネットワークアダプターを使用できますが、JetPack 4.xのLinux kernelが古い点が主な制約です。Realtekモデルはout-of-treeドライバーを直接コンパイル可能、MediaTekはbackportまたは自前でのコンパイルが必要、Wi-Fi 6Eモデルは使用不可です。ペネトレーションテストにはAWUS036ACH、一般用途にはAWUS036ACHまたはAWUS036ACMを推奨します。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

## 1. 問題要約

顧客の質問：「ALFAシリーズのUSBワイヤレスネットワークアダプターがNVIDIA Jetson Nano開発板上で使用可能か？」

簡潔な結論：Jetson Nanoは多くのALFAネットワークアダプターを使用可能ですが、主要な制約はJetPack 4.xのLinuxカーネルのバージョンが古いことです（評価基準：ALFAの現役9モデルのUSBネットワークアダプターのうち、3モデルが成熟して使用可能、2モデルが高度なコンパイルが必要、2モデルが未検証、2モデルが使用不可能）。Realtekチップセットモデル（AWUS036ACH / ACS / EACS）は、カーネル4.9のような古い環境ではout-of-treeドライバーを直接コンパイルすることができ（EACSのrtw88_8821cuはkernel 6.2からmainline内蔵）、Jetson Nano上での実用的な選択肢です；MediaTek MT7612U / MT7610Uはbackportまたは独自のmt76ドライバーのコンパイルが必要です；Wi-Fi 6EのMT7921AUNモデル（AWUS036AXML / AXM）はkernel 5.18+が必要で、実際にはJetson Nano上で使用不可能です。ペネトレーションテストのシーンではAWUS036ACH（RTL8812AU）が最適で、一般的なオンラインシーンではAWUS036ACH（安定）またはAWUS036ACM（コンパイルが必要）が最適です。

## 2. 目標ハードウェアのスペック構造の分析

### 2.1 NVIDIA Jetson Nanoのハードウェアスペック

| 項目 | 規格 |
|---|---|
| モジュール | Jetson Nanoモジュール（P3448） |
| CPU | Quad-core ARM Cortex-A57（ARMv8-A / aarch64） |
| GPU | NVIDIA Maxwellアーキテクチャ、128 CUDAコア |
| メモリ | 4GB LPDDR4（64-bit、25.6 GB/s） |
| 儲蔵 | microSD（開発板）/ eMMC（生産版モジュール） |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B（デバイスモード / 電源） |
| ネットワーク | 1x Gigabit Ethernet（RJ45） |
| ワイヤレス | 内蔵WiFi / 藍牙（USBまたはM.2拡張が必要） |
| 電源 | 5V/4A DCコネクタ（推奨）またはmicro-USB 5V/2A |
| サイズ | 100mm × 80mm（開発板） |

### 2.2 ソフトウェア環境：JetPack 4.x

| 項目 | 具体内容 |
|---|---|
| オペレーティングシステム | Linux for Tegra（L4T）、Ubuntu 18.04 LTSに基づく |
| カーネルバージョン | Linux 4.9（L4T R32.x / JetPack 4.6.x） |
| アーキテクチャ | aarch64（ARM64） |
| コンパイラ | GCC 7.5（デフォルト）/ GCC 8（インストール可能） |
| 最新バージョン | JetPack 4.6.4（L4T R32.7.4）、メンテナンスモードに入っています |
| 後続のアップグレード | Jetson NanoはJetPack 5.x（kernel 5.10）をサポートしておらず、ハードウェアの制約によるものです |

### 2.3 主要な制約：カーネル4.9

Jetson Nanoのカーネル4.9は相性判定の核心要素です：

| ドライバー | メインラインカーネルへの投入バージョン | Jetson Nano（カーネル4.9）の使用可能性 |
|---|---|---|
| mt76x2u（MT7612U） | 4.19 | ❌ バックポートまたは独自のコンパイルが必要 |
| mt76x0u（MT7610U） | 4.19 | ❌ バックポートまたは独自のコンパイルが必要 |
| mt7921u（MT7921AUN） | 5.18 | ❌ 実用的には使用不可能（大きなギャップ）。GX10（kernel 6.17）ではmonitorは動作するがインジェクションは失敗（主因はkernel 6.16以降のmac80211 chanctxリグレッションで、ファームウェアによるレート固定もあり、チップ自体の限界ではない） |
| rtl8812au（RTL8812AU） | 6.13（rtw88_8812au） | ✅ kernel 4.9には内蔵ドライバーがなく、out-of-treeドライバーのコンパイルが必要。GX10（kernel 6.17）では内蔵ドライバーで両バンドともインジェクション100%を実測 |
| rtw88_8821cu（RTL8821CU） | 6.2 | ✅ カーネル4.9（6.2より前）ではout-of-treeドライバー（8821cu）をコンパイル可能 |
| rtw89（RTL8832BU） | 6.17（rtw89_8852bu） | ❌ kernel 4.9には内蔵されておらず、独自コンパイルが必要で互換性は不明。GX10（kernel 6.17）ではmonitorが動作し、2.4Gインジェクションは AX 96%、AXER 73% |

### 2.4 USB電源制約

Jetson Nano開発板の4つのUSB 3.0 Type-Aポートは共有電源予算を共有します：

- DC電源（5V/4A）を使用している場合、USBポートの総出力は約1.5A（5V）です
- micro-USB電源（5V/2A）を使用している場合、USBポートの総出力は約0.5Aです
- ALFAハイパワーネットワークアダプター（
