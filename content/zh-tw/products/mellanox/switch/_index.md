---
title: "NVIDIA Mellanox InfiniBand 與乙太網路交換器"
description: "高密度企業級網路交換器。提供 Mellanox EDR (100G)、HDR (200G) 及 NDR (400G) 交換器，專為高效能運算 (HPC) 與 AI 叢集打造。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox InfiniBand 與乙太網路交換器 — EDR, HDR & NDR

NVIDIA Mellanox InfiniBand 交換器是現代 AI 訓練叢集與高效能運算 (HPC) 環境的骨幹架構。具備高埠數密度、極低交換延遲以及先進擁塞管理機制，能實現多節點系統的無縫擴充。

---

## 交換器產品目錄

以下為本公司現有的 1U 機架式網管型與非網管型交換器庫存列表。

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*NVIDIA Mellanox Quantum HDR 40 埠 InfiniBand 交換器*

| 原廠料號 | 晶片世代 | 網管功能 | 埠數配置 | 連接埠速率 | 外觀尺寸 | 風道方向 | 電源供應 |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | 是 (x86) | 36x QSFP28 | 100Gb/s | 1U 標準 | 埠向電源風道 (P2C) | 雙交流電源 |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | 否 | 36x QSFP28 | 100Gb/s | 1U 標準 | 電源向埠風道 (C2P) | 雙交流電源 |
| **MQM8700-HS2F** | Quantum (HDR) | 是 (x86) | 40x QSFP56 | 200Gb/s | 1U 標準 | 埠向電源風道 (P2C) | 雙交流電源 |
| **MQM8790-HS2F** | Quantum (HDR) | 否 | 40x QSFP56 | 200Gb/s | 1U 標準 | 埠向電源風道 (P2C) | 雙交流電源 |
| **MQM9700-NS2F** | Quantum 2 (NDR) | 是 | 32x OSFP (支援 64 個 NDR 埠) | 400Gb/s (OSFP) | 1U 標準 | 埠向電源風道 (P2C) | 雙交流電源 |
| **MQM9790-NS2F** | Quantum 2 (NDR) | 否 | 32x OSFP (支援 64 個 NDR 埠) | 400Gb/s (OSFP) | 1U 標準 | 埠向電源風道 (P2C) | 雙交流電源 |

---

## InfiniBand 各世代規格對比

| 世代規格 | 晶片世代 | 單埠最大速率 | 交換容量 | 訊號傳輸率 / 調變方式 | 延遲時間 |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7.2 Tb/s | 25 Gb/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gb/s | 16.0 Tb/s | 50 Gb/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gb/s (相容 800G) | 51.2 Tb/s | 100 Gb/s PAM4 | 205 ns |

---

## InfiniBand 網路拓撲指南

為 AI 訓練或物理模擬構建大規模擴充叢集時，需要使用特定的網路拓撲架構：

![NVIDIA Mellanox Fat-Tree InfiniBand Topology](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. 胖樹 (Fat-Tree) 拓撲 (無阻塞 CLOS 架構)
這是 InfiniBand 網路的標準架構，將交換器分為分層結構 (Leaf 葉交換器與 Spine 脊交換器) 以提供多條並行路徑。
- **無阻塞 (1:1 收容比)**：所有節點可同時以全線速進行通訊。這需要連至 Spine 交換器的上行頻寬與連至節點的下行頻寬完全相等。
- **超收 (例如 2:1 收容比)**：透過減少連至 Spine 交換器的鏈路數量來降低建置成本，適合計算通訊較為局部的應用負載。

### 2. 軌道優化 (Rail-Optimized) AI 網路
在多 GPU 節點中 (如搭載 8 顆 GPU 的 NVIDIA HGX H100)，每顆 GPU 都配有專屬的 ConnectX 網路卡。軌道優化技術將所有伺服器上的「GPU 1」網卡連接到專用的「軌道交換器 1 (Rail Switch 1)」，將所有「GPU 2」連接到「軌道交換器 2」，依此類推。這種設計將深度學習通訊庫 (NCCL) 的環狀通訊模式 (Ring-communication) 直接對應到實體交換器上，能最大程度降低延遲。

---

## 網管 vs 非網管交換器與子網路管理程式 (Subnet Manager)

與乙太網路透過 ARP 隨插即用不同，InfiniBand 網路**若沒有啟動的子網路管理程式 (Subnet Manager, SM)，將無法傳輸任何封包**。SM 負責偵測網路拓撲、分配區域識別碼 (LID) 並計算路由路徑。
- **網管型交換器 (Managed Switches)**：內建運行 MLNX-OS/Onyx 的 CPU，並提供嵌入式子網路管理程式。適合獨立運作的中小型叢集 (約 36 個節點以內)。
- **非網管型交換器 (Unmanaged Switches)**：具備極低的延遲，但無內建 CPU。需要透過主機伺服器運行外部 SM (如 OpenSM)，或由同網路中的其他網管型交換器來管理。

---

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}
