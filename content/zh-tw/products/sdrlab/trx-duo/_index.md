---
title: "SDRLab TRX-duo — 雙通道 16-bit ZYNQ SDR 平台"
seo_title: "TRX-duo SDRLab 台灣 | Yopitek"
description: "SDRLab TRX-duo 雙通道 16-bit ADC/DAC SDR 平台，Zynq 7010、125 MS/s，相容 Red Pitaya，可向 Yopitek 詢價。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
faq:
  - question: "SDRLab TRX-duo 的處理器與介面為何？"
    answer: "採用 Xilinx Zynq 7010 SoC（雙核 ARM Cortex-A9），512 MB RAM、1 Gbit 乙太網路與 USB Type-C（USB 2.0）。Wi-Fi 需外接加密狗，未附。"
  - question: "TRX-duo 的接收與發射規格為何？"
    answer: "接收為 2 顆 LTC2208 16-bit ADC，取樣率 125 MS/s，全量程 0.5 Vpp / −2 dBm；發射為 2 通道 14-bit DAC，125 MS/s，1 Vpp / +4 dBm，負載 50 Ω。"
  - question: "TRX-duo 相容哪些軟體？"
    answer: "相容 Red Pitaya 軟體生態系，以及 HDSDR、SDR#、PowerSDR、SDR Console V3 等 SDR 軟體。"
  - question: "TRX-duo 提供哪些擴充 I/O？"
    answer: "提供 16 個數位 I/O、4 路類比輸入（0–3.3 V、100 kS/s、12-bit）與 4 路類比輸出（0–1.8 V），支援 I2C、UART、SPI，並有 +3.3 V 電源輸出。"
---

TRX-duo 是 Zynq 7010 雙通道 16-bit SDR 收發平台，相容 Red Pitaya，具 2 顆 125 MS/s ADC。歡迎聯絡 Yopitek 取得台灣報價。

## 產品特色

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- 雙通道收發設計（2 RX + 2 TX），相容 Red Pitaya 軟體生態系
- 採用 2× LTC2208 高精度 16-bit ADC，具備高動態範圍與高靈敏度
- 14-bit DAC 實現雙通道發射
- 板載 Xilinx Zynq 7010 SoC（雙核 ARM Cortex-A9 + FPGA），可直接在裝置上執行解碼軟體
- 支援網路遠端部署，可架設遠端 SDR 接收站
- 相容 HDSDR、SDR#、PowerSDR、SDR Console V3 等主流軟體

## 產品規格

| 規格項目 | 數值／說明 |
|---------|-----------|
| 處理器 | 雙核 ARM Cortex-A9（Zynq 7010 SoC）|
| FPGA | Xilinx Zynq 7010 |
| 記憶體（RAM）| 512 MB |
| 接收通道數 | 2（SMA 連接器）|
| ADC 解析度 | 16-bit（LTC2208）|
| ADC 取樣率 | 125 MS/s |
| ADC 全量程電壓 | 0.5 Vpp / −2 dBm |
| 輸入電壓範圍 | DC 最大 50 V（AC 耦合），1 Vpp RF |
| 輸入保護 | RF 變壓器 + AC 耦合 |
| 發射通道數 | 2 |
| DAC 解析度 | 14-bit |
| DAC 取樣率 | 125 MS/s |
| 發射輸出電壓 | 1 Vpp / +4 dBm |
| 發射負載阻抗 | 50 Ω |
| 乙太網路 | 1 Gbit |
| USB | Type-C（USB 2.0）|
| Wi-Fi | 需外接 Wi-Fi 加密狗（不含）|
| 擴充 GPIO | 數位 I/O × 16、類比輸入 × 4、類比輸出 × 4 |
| 類比輸入電壓範圍 | 0–3.3 V |
| 類比輸出電壓範圍 | 0–1.8 V |
| 類比輸入取樣率 | 100 kS/s / 12-bit |
| 通訊介面 | I2C、UART、SPI |
| 擴充電源輸出 | +3.3 V |

## 應用環境

- HF（短波）業餘無線電收發（CW、SSB、AM、FM）
- 遠端 SDR 接收站架設（全網路遠端存取）
- HF 頻譜分析與信號研究
- 業餘無線電通訊實驗（無線電競賽、天文觀測）

---

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}

[原廠商店頁（OpenSourceSDRLab）](https://opensourcesdrlab.com/products/trx-duo-compatible-with-red-pitaya-sdr-dual-16bit-adc-zynq7010?VariantsId=10980)

{{< faq >}}
