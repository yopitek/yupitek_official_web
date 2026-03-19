---
title: "SDRLab Flipper Zero 5G 擴充板 — 雙頻 Wi-Fi 安全研究模組"
description: "Flipper Zero 5G 擴充板，RTL8720DN 雙頻（2.4+5GHz）Wi-Fi，BLE 5.0，預燒 Deauth 韌體，GPIO 供電，相容 Momentum/Unleashed。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 擴充", "5GHz", "Wi-Fi", "Deauth", "資安研究"]
---

{{< alert "warning" >}}
**合法使用聲明**：本擴充板僅供授權的資安研究及合法研究使用。請確認符合當地無線頻率使用法規。
{{< /alert >}}

## 產品特色

![SDRLab Flipper Zero 5G 擴充板](/images/products/sdrlab/flipper-5g.png)

- 基於 AI Thinker BW16 模組（RTL8720DN 晶片），原生支援 5 GHz Wi-Fi
- 雙頻覆蓋（2.4 GHz + 5 GHz），可探測現代雙頻無線網路環境
- 預燒錄 5G Wi-Fi 去驗證（Deauth）韌體，即插即用
- 直接由 Flipper Zero GPIO 供電，無需額外電源
- 支援網格網路拓撲識別與無線環境掃描
- 相容 Momentum 與 Unleashed 韌體框架
- 支援 PlatformIO 進行二次開發與自訂韌體燒錄
- Cortex-M0 低功耗核心，延長野外作業時間

## 產品規格

| 規格項目 | 數值／說明 |
|---------|-----------|
| 主晶片 | Realtek RTL8720DN（AI Thinker BW16 模組）|
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n（2.4 GHz + 5 GHz 雙頻）|
| 藍牙 | BLE 5.0 |
| Flash | 4 MB |
| 供電來源 | Flipper Zero GPIO（5 V）|
| 連接介面 | Flipper Zero 標準 GPIO 排針 |
| 預載韌體 | 5G Wi-Fi Deauth Firmware |
| 韌體相容 | Momentum、Unleashed |
| 二次開發 | PlatformIO 支援 |
| 工作溫度 | −40°C 至 85°C |
| 天線介面 | IPEX（U.FL）或板載 PCB 天線（依版本）|

## 應用環境

- 5 GHz Wi-Fi 頻段掃描與環境分析
- 無線網路去驗證（Deauth）安全研究
- 惡意接入點（Evil Portal）原型開發
- Beacon 洪水測試（Beacon Flood）
- 網格網路拓撲識別
- IoT 無線協定開發與除錯
- 授權環境下的 Wi-Fi 滲透測試教育

---

{{< alert >}}
需要詢問報價？[聯絡我們](/zh-tw/contact/)
{{< /alert >}}
