---
title: "NVIDIA BlueField 數據處理器 (DPU)"
description: "深入瞭解 NVIDIA BlueField DPU 解決方案。透過基於 ARM 的可程式化智慧網卡 (SmartNIC)，卸載、加速並隔離網路、儲存和安全性等基礎架構服務。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField 數據處理器 (DPU)

NVIDIA® BlueField® 數據處理器 (DPU) 代表了資料中心架構的變革。它將業界領先的 ConnectX 網路卡、可程式化 ARM® CPU 核心與硬體加速引擎整合在一起，能將基礎架構工作從伺服器 CPU 中卸載、加速並進行實體隔離。

---

## BlueField DPU 產品目錄

我們提供專為雲端級虛擬化、軟體定義儲存及零信任安全架構設計的 BlueField DPU 系列產品。

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField 可程式化基礎架構介面卡*

| 原廠料號 | 產品名稱 | 核心網路速率 | ARM CPU 核心 | 記憶體 | 匯流排介面 | 支援協定 | 外觀尺寸 |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | 雙埠 100GbE / EDR IB | 8 核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | 雙埠 100GbE / EDR IB | 8 核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (支援加密功能) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | 單埠 100GbE / EDR IB | 8 核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (支援加密功能) |

---

## DPU 核心技術

### 1. 基礎架構卸載 (智慧型網卡)
以往需要耗費伺服器 CPU 運算資源來處理的虛擬交換器網路切換 (OVS)、虛擬通道封裝 (VXLAN, NVGRE) 或網路位址轉換 (NAT)，現在能透過 DPU 上的 **NVIDIA ASAP² (加速交換與封包處理)** 技術，直接在硬體中以線速 (Wire-speed) 進行處理。

### 2. 軟體定義儲存加速
透過 **NVMe SNAP™ (軟體定義網路加速處理)** 技術，BlueField DPU 能將遠端網路儲存 (透過 RoCEv2 或 TCP) 對伺服器作業系統模擬呈現為本機實體 NVMe 硬碟。所有的硬碟模擬、加密及壓縮工作完全在 DPU 上處理，可有效消除虛擬化儲存的效能瓶頸。

### 3. 零信任安全與實體隔離
DPU 在其內建的 ARM 核心上運行獨立的 Linux 作業系統 (通常為 Ubuntu)，與伺服器主機完全隔離。即使主機作業系統受到安全性危害，在 DPU 上運行的資安防護軟體、無代理程式防火牆以及網路加密 (IPsec、TLS) 依然能不受干擾地持續運作。

### 4. NVIDIA DOCA 軟體架構
BlueField DPU 採用 **NVIDIA DOCA™** 軟體架構進行程式開發。該架構提供業界標準的 API，便於開發針對網路、安全、儲存和遙測應用的硬體加速程式。

---

## 常見應用場景

- **新世代雲端服務商**：實現虛擬化基礎架構管理與租戶主機完全隔離的裸金屬 (Bare-metal) 代管服務。
- **企業超融合基礎架構 (HCI)**：將儲存與網路堆疊 (如 VMware NSX 或 Proxmox OVS) 卸載至 DPU，以極大化虛擬機 (VM) 的部署密度。
- **高安全性需求環境**：直接在網路邊界上運行網路安全監控 (IDS/IPS) 與資料加密工作負載。

---

如需技術整合支援或索取報價，歡迎[聯絡 Yupitek 銷售團隊](/zh-tw/contact/)。
