---
title: "NVIDIA Mellanox LinkX 光纖跳線"
description: "選擇通過認證的 NVIDIA Mellanox LinkX 光纖跳線。專為 NVIDIA 網路優化的高密度 OM4 多模 MPO-12 光纖跳線，確保資料傳輸零錯誤。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 光纖跳線 — OM4 多模 MPO

NVIDIA LinkX® 光纖跳線用於光收發模組之間的物理連接。採用 LinkX 原廠光纖線材，能確保連接器、插芯拋光以及玻璃光纖品質符合高速乙太網路與 InfiniBand 網路對於插入損耗 (Insertion Loss) 與反射損耗 (Return Loss) 的嚴格規範。

---

## 光纖跳線產品目錄

以下為本公司現有的原廠認證光纖線材庫存列表。

![Mellanox MPO Fiber Patch Cable](/images/products/mellanox/ai-generated/fiber-patch-mpo.jpg)
*NVIDIA Mellanox 高密度 OM4 多模 MPO-12 光纖跳線*

| 原廠料號 | 連接器規格 | 線材長度 | 光纖類型 | 極性規格 | 適用網路環境 |
|-------------|----------------|--------|------------|----------|--------------------|
| **MFP7E10-N003** | MPO-12 (母頭) 至 MPO-12 (母頭) | 3.0m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |
| **MFP7E10-N005** | MPO-12 (母頭) 至 MPO-12 (母頭) | 5.0m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |
| **MFP7E10-N010** | MPO-12 (母頭) 至 MPO-12 (母頭) | 10m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |
| **MFP7E10-N015** | MPO-12 (母頭) 至 MPO-12 (母頭) | 15m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |
| **MFP7E10-N020** | MPO-12 (母頭) 至 MPO-12 (母頭) | 20m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |
| **MFP7E10-N030** | MPO-12 (母頭) 至 MPO-12 (母頭) | 30m | 多模 OM4 | Type-B (反向) | 100G/200G/400G 光收發模組跳線 |

---

## 技術指南：光纖線材規格

### 1. OM4 多模光纖 (MMF)
- **纖芯直徑**：50µm (微米) 纖芯與 125µm 包層。
- **外被顏色**：水藍色 (Aqua) / 紫羅蘭色 (Erika Violet)。
- **頻寬與傳輸距離**：專為工作波長 850nm 的 VCSEL 雷射進行優化。在 100Gb/s (SR4) 速率下，OM4 支援最遠 100 公尺的傳輸距離；在 25Gb/s (SR) 速率下最遠支援 150 公尺。

### 2. MPO-12 連接器
- **公母針腳規格**：MPO 連接器有分公母頭。由於光收發模組內部通常為公頭 (有定位針)，因此對接的光纖跳線必須為**無針的母頭 (具有導向孔)**才能成功接合。
- **端面拋光方式**：標準 MPO 連接器採用 **PC / UPC** (平直面) 拋光。而高速單模 MPO 以及新型 400G/800G 多模 OSFP/QSFP112 光收發模組，則需要 **APC (斜物理接觸，8 度角斜面)** 拋光以消除反射損耗。APC 連接器通常以綠色外殼標示。

### 3. MPO 極性標準
在 MPO-12 佈線系統中，極性設計用於確保一端的傳送端 (TX) 能正確連接到另一端的接收端 (RX)：
- **Type-A (定位鍵朝上對朝下 Key Up to Key Down)**：直通接線。第 1 針連接到另一端的第 1 針。
- **Type-B (定位鍵朝上對朝上 Key Up to Key Up)**：反向接線。第 1 針連接到另一端的第 12 針。**這是直接連接兩個 SR4 光收發模組的業界標準規格。**
- **Type-C (成對交叉接線 Pair-wise Flipped)**：第 1/2 針交叉、3/4 針交叉，依此類推。主要用於結構化骨幹佈線。

---

{{< alert >}}
需要詢問產品報價?請來信[與我們聯絡](/zh-tw/contact/)
{{< /alert >}}
