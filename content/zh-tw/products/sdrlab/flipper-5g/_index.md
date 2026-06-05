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

- **雙頻覆蓋** — 2.4 GHz + 5 GHz（IEEE 802.11 a/b/g/n）；可探測過去僅 2.4 GHz 擴充板無法訪問的現代 5 GHz 網路
- **Realtek RTL8720DN（AI Thinker BW16 模組）** — 業界標準雙頻 SoC，具 FCC/CE 預認證模組
- **雙核心 CPU** — ARM Cortex-M4 @ 200 MHz 處理主動協定；Cortex-M0 @ 20 MHz 執行低功耗背景任務
- **預載 Marauder 5G 韌體** — 包含掃描、Deauth、Beacon 洪水、封包嗅探（EAPOL/PMKID）及 Evil Portal 模式；即插即用
- **BLE 5.0** — 藍牙低能耗裝置枚舉與信標分析，與 Wi-Fi 研究並行
- **GPIO 供電** — 直接取用 Flipper Zero GPIO 排針之 5 V；無需額外電源供應器
- **天線升級路徑** — 支援版本配備 IPEX（U.FL）連接器，可外接高增益天線
- **韌體生態相容** — 支援 Momentum 與 Unleashed 自訂韌體框架
- **PlatformIO 開發** — 透過 Arduino 相容的 Ameba D 框架提供完整自訂韌體開發支援
- **堅固工作範圍** — −40°C 至 85°C，適合各種氣候環境的野外使用

## 產品規格

| 規格項目 | 數值／說明 |
|---------|-----------|
| 主晶片 | Realtek RTL8720DN（AI Thinker BW16 模組）|
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi 標準 | IEEE 802.11 a/b/g/n（2.4 GHz + 5 GHz 雙頻）|
| Wi-Fi 發射功率 | ~17 dBm（受地區法規限制）|
| 藍牙 | BLE 5.0 |
| Flash | 4 MB |
| 供電來源 | Flipper Zero GPIO（5 V）|
| 典型電流消耗 | 150–250 mA（主動掃描時）|
| 連接介面 | Flipper Zero 標準 GPIO 排針（2×8 針）|
| 預載韌體 | Marauder 5G（掃描、Deauth、Beacon、嗅探、Evil Portal）|
| 韌體相容 | Momentum、Unleashed |
| 二次開發 | PlatformIO（Ameba D / RTL8720DN 框架）|
| 工作溫度 | −40°C 至 85°C |
| 天線介面 | IPEX（U.FL）或板載 PCB 天線（依版本）|
| 外形規格 | Flipper Zero GPIO 擴充板 |

## 應用環境

- **雙頻 Wi-Fi 掃描** — 被動枚舉 2.4 GHz 與 5 GHz 網路；擷取 SSID、BSSID、頻道、RSSI、加密類型及連線客戶端
- **Wi-Fi Deauth 安全研究** — 傳送 802.11 Deauth 封包測試網路韌性，並評估已授權網路的 802.11w/PMF（受保護管理幀）防護能力
- **WPA 握手包擷取** — 嗅探 EAPOL/PMKID 握手包，用於授權網路安全稽核
- **Evil Portal 開發** — 在授權環境下原型設計惡意 AP 入口，用於網路釣魚意識測試
- **Beacon 洪水測試** — 廣播自訂 SSID 以研究射頻擁塞影響及客戶端行為
- **BLE 裝置枚舉** — 掃描並識別附近的 BLE 5.0 外圍裝置，與 Wi-Fi 研究同步進行
- **網格網路拓撲映射** — 識別網格 AP 關係、回程頻道及隱藏 SSID 配置
- **IoT 無線協定研究** — 在受控實驗室環境中分析 IoT 裝置在雙頻上的行為
- **授權滲透測試教育** — 在授權環境下學習 Wi-Fi 安全基礎的實踐平台

---

{{< alert "warning" >}}
**初次使用此擴充板？** 請參考我們的分步驟初學者指南，涵蓋前置條件、韌體設定、首次 5G 掃描及所有核心功能。
[📖 開啟線上使用手冊](/zh-tw/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}
