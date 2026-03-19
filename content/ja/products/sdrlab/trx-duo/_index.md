---
title: "SDRLab TRX-duo — デュアルチャンネル 16-bit ZYNQ SDR プラットフォーム"
description: "SDRLab TRX-duo、デュアルチャンネル 16-bit ADC/DAC SDR プラットフォーム、Xilinx Zynq 7010 SoC、Red Pitaya 互換、10kHz〜60MHz ダイレクトサンプリング、高度な HF 無線通信研究に最適。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---

## 製品特長

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- デュアルチャンネル送受信設計（2 RX + 2 TX）、Red Pitaya ソフトウェアエコシステムと互換
- 2× LTC2208 高精度 16-bit ADC を採用し、高ダイナミックレンジと高感度を実現
- 14-bit DAC によるデュアルチャンネル送信
- Xilinx Zynq 7010 SoC 搭載（デュアルコア ARM Cortex-A9 + FPGA）、デバイス上でデコードソフトウェアを直接実行可能
- ネットワークリモートデプロイに対応、リモート SDR 受信局の構築が可能
- HDSDR、SDR#、PowerSDR、SDR Console V3 などの主要ソフトウェアと互換
- 公式 Red Pitaya SDRlab 122-16（約 $622 USD）の約半額で購入可能

## 仕様

| 仕様項目 | 値／説明 |
|---------|---------|
| プロセッサ | デュアルコア ARM Cortex-A9（Zynq 7010 SoC） |
| FPGA | Xilinx Zynq 7010 |
| メモリ（RAM） | 512 MB |
| 受信周波数範囲 | 10 kHz – 60 MHz（ダイレクトサンプリング） |
| 受信チャンネル数 | 2（SMA コネクタ） |
| ADC 解像度 | 16-bit（LTC2208） |
| ADC サンプルレート | 125 MS/s |
| ADC フルスケール電圧 | 0.5 Vpp / −2 dBm |
| 入力電圧範囲 | DC 最大 50 V（AC 結合）、1 Vpp RF |
| 入力保護 | RF トランス + AC 結合 |
| 送信チャンネル数 | 2 |
| DAC 解像度 | 14-bit |
| DAC サンプルレート | 125 MS/s |
| 送信出力電圧 | 1 Vpp / +4 dBm |
| 送信負荷インピーダンス | 50 Ω |
| 送信出力電力 | 約 2.5 mW（外部パワーアンプが必要） |
| イーサネット | 1 Gbit |
| USB | Type-C（USB 2.0） |
| Wi-Fi | 外付け Wi-Fi ドングルが必要（付属なし） |
| 拡張 GPIO | デジタル I/O × 16、アナログ入力 × 4、アナログ出力 × 4 |
| アナログ入力電圧範囲 | 0〜3.3 V |
| アナログ出力電圧範囲 | 0〜1.8 V |
| アナログ入力サンプルレート | 100 kS/s / 12-bit |
| 通信インターフェース | I2C、UART、SPI |
| 拡張電源出力 | +3.3 V |
| オペレーティングシステム | 搭載 Linux（Red Pitaya ファームウェア） |

## 用途

- HF（短波）アマチュア無線送受信（CW、SSB、AM、FM）
- マルチバンド WSPR 弱信号モニタリング（最大 8 バンド同時）
- リモート SDR 受信局の構築（フルネットワークリモートアクセス）
- HF スペクトラム分析と信号研究
- HPSDR 互換アプリケーションソフトウェア開発
- アマチュア無線通信実験（コンテスト、天文観測）

---

{{< gallery >}}
  <img src="/images/products/sdrlab/trx-duo.png" alt="SDRLab TRX-duo" />
{{< /gallery >}}

---

{{< alert >}}
お見積もりのお問い合わせは[こちら](/ja/contact/)
{{< /alert >}}
