---
title: "NVIDIA Mellanox LinkX 光收發模組"
description: "選擇原廠 NVIDIA Mellanox LinkX 光收發模組。提供高速 25G、100G、400G 與 800G 收發器，適用於多模與單模光纖網路。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 光收發模組 — 25G 至 800G

NVIDIA LinkX® 光收發模組專為滿足高效能運算、企業級儲存與超大型資料中心環境的嚴格要求而設計。使用原廠收發模組能確保訊號完整性、極低的位元錯誤率 (BER)，並與 ConnectX 網路卡及 Quantum 交換器達到完整的相容性。

---

## 光收發模組產品目錄

以下為本公司現有的光收發模組產品庫存列表。

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR 光收發模組</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 光收發模組</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR 光收發模組</p>
  </div>
</div>

| 原廠料號 | 傳輸速率 | 介面規格 | 連接器規格 | 工作波長 | 光纖類型 | 最長傳輸距離 | 產品描述 |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC 雙工 | 850nm | 多模 (MMF) | 150m (OM4) / 100m (OM3) | 25GbE SR 光收發模組 |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | 多模 (MMF) | 100m (OM4) / 70m (OM3) | 100GbE SR4 光收發模組 (支援 DDMI) |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850nm | 多模 (MMF) | 50m (OM4) | NDR IB/ETH SR 光收發模組 (平頂版) |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850nm | 多模 (MMF) | 50m (OM4) | 2xNDR 雙埠 SR 光收發模組 (散熱片版) |

---

## 傳輸距離與佈線指南

### 1. SR、SR4 與 NDR (多模光纖解決方案)
- **25G SR (SFP28)**：搭配標準的 LC-LC 雙工多模光纖跳線，透過單通道進行資料收發。
- **100G SR4 (QSFP28)**：採用 12 芯 MPO (MPO-12) 帶狀光纖跳線 (通常為 Type-B 極性)，透過 4 個並行的 25G 通道進行傳輸。
- **400G/800G NDR (OSFP)**：採用 PAM4 調變技術，透過 MPO-12 APC (斜物理接觸) 連接器傳輸極高頻寬。斜端面設計能將反射干擾降到最低，這在高速傳輸中極其關鍵。

### 2. 單模 (LR4/FR4) vs 多模 (SR/SR4)
- **多模光纖 (MMF)**：適用於機櫃內或短距離的機櫃間佈線 (最長 100 至 150 公尺)，收發模組建置成本較低。
- **單模光纖 (SMF)**：適用於超過 150 公尺以上的長距離傳輸 (LR4 規格最遠可達 10 公里)，搭配 9/125µm 光纖及雙工 LC 連接器。

---

## 技術解析：原廠模組 vs 第三方相容模組

在選購光收發模組時，客戶常問：*「我可以使用通用的第三方模組，或寫過碼的相容模組嗎？」*

### 為什麼我們建議選擇原廠 NVIDIA LinkX：
1. **韌體相容性限制**：NVIDIA ConnectX 網路卡與 Quantum 交換器運行專用的作業系統 (如 MLNX-OS 或 Onyx)。系統進行更新時，常會鎖定或將非原廠的相容模組標記為不支援，導致連接埠無法正常啟用。
2. **診斷數據準確性 (DDM/DOM)**：原廠模組能向系統控制器 (如 iDRAC、HPE iLO 或 MLNX-OS) 準確回報運作溫度、電壓、發射 (TX) 功率與接收 (RX) 功率。精確的量測數值能避免發生錯誤的過熱警報。
3. **先進功能支援**：LinkX 模組出廠即通過前向錯誤更正 (FEC) 等關鍵網路參數的完整認證，能在高負載資料庫傳輸環境下避免封包遺失。

---

需要搭配的光纖跳線？歡迎參考我們的 [光纖跳線目錄](/zh-tw/products/mellanox/cable-fiber/)。如有客製化網路規劃需求，歡迎[聯絡 Yupitek 技術工程團隊](/zh-tw/contact/)。
