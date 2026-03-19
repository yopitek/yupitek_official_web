---
title: "SDRLab TRX-duo — 雙通道 16-bit ZYNQ SDR 平台"
description: "SDRLab TRX-duo，雙通道 16-bit ADC/DAC SDR 平台，Xilinx Zynq 7010 SoC，相容 Red Pitaya，10kHz–60MHz 直接取樣，適合進階 HF 無線通訊研究。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---

## 產品特色

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- 雙通道收發設計（2 RX + 2 TX），相容 Red Pitaya 軟體生態系
- 採用 2× LTC2208 高精度 16-bit ADC，具備高動態範圍與高靈敏度
- 14-bit DAC 實現雙通道發射
- 板載 Xilinx Zynq 7010 SoC（雙核 ARM Cortex-A9 + FPGA），可直接在裝置上執行解碼軟體
- 支援網路遠端部署，可架設遠端 SDR 接收站
- 相容 HDSDR、SDR#、PowerSDR、SDR Console V3 等主流軟體
- 比官方 Red Pitaya SDRlab 122-16（約 $622 USD）便宜約一半

## 產品規格

| 規格項目 | 數值／說明 |
|---------|-----------|
| 處理器 | 雙核 ARM Cortex-A9（Zynq 7010 SoC）|
| FPGA | Xilinx Zynq 7010 |
| 記憶體（RAM）| 512 MB |
| 接收頻率範圍 | 10 kHz – 60 MHz（直接取樣）|
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
| 發射功率 | 約 2.5 mW（需外接功率放大器）|
| 乙太網路 | 1 Gbit |
| USB | Type-C（USB 2.0）|
| Wi-Fi | 需外接 Wi-Fi 加密狗（不含）|
| 擴充 GPIO | 數位 I/O × 16、類比輸入 × 4、類比輸出 × 4 |
| 類比輸入電壓範圍 | 0–3.3 V |
| 類比輸出電壓範圍 | 0–1.8 V |
| 類比輸入取樣率 | 100 kS/s / 12-bit |
| 通訊介面 | I2C、UART、SPI |
| 擴充電源輸出 | +3.3 V |
| 作業系統 | 板載 Linux（Red Pitaya 韌體）|

## 應用環境

- HF（短波）業餘無線電收發（CW、SSB、AM、FM）
- 多頻段 WSPR 弱信號監測（最多 8 頻段同時）
- 遠端 SDR 接收站架設（全網路遠端存取）
- HF 頻譜分析與信號研究
- HPSDR 相容應用軟體開發
- 業餘無線電通訊實驗（無線電競賽、天文觀測）

---

{{< alert >}}
需要詢問報價？[聯絡我們](/zh-tw/contact/)
{{< /alert >}}
