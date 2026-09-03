---
title: "ALFA 無線網卡是否支援 MSI EdgeXpert（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "邊緣 AI / GPU 伺服器"
description: "MSI EdgeXpert 與 NVIDIA DGX Spark 共享相同的 GB10 硬體平台與 DGX OS 軟體環境，對 ALFA 網卡的相容性完全一致。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驅動，開箱即用；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需在..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在 MSI EdgeXpert（NVIDIA GB10 Grace Blackwell）AI 超級電腦上使用？」

簡短結論：MSI EdgeXpert 與 NVIDIA DGX Spark 共享相同的 GB10 硬體平台與 DGX OS 軟體環境，對 ALFA 網卡的相容性完全一致。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驅動，開箱即用；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需在 ARM64 上編譯 out-of-tree 驅動。注意：EdgeXpert 的 4 個 USB 埠均為 USB Type-C（20Gbps），ALFA 網卡（AXML 除外）需使用 USB-C to USB-A 轉接器。

判定母體：ALFA 現役 9 款 USB 網卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目標硬體規格架構

### 2.1 MSI EdgeXpert 硬體規格

| 項目 | 規格 |
|---|---|
| 產品名稱 | MSI EdgeXpert（型號：EdgeXpert-MS-C931 / 59STW 等） |
| 核心晶片 | NVIDIA GB10 Grace Blackwell Superchip（DGX Spark 平台） |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架構，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 效能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS |
| 系統記憶體 | 128GB LPDDR5x 統一記憶體（256-bit，273 GB/s） |
| 儲存 | 1TB 或 4TB NVMe M.2 SSD（自加密，PCIe Gen5） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（最高 20Gbps） |
| 顯示輸出 | 1× HDMI 2.1a（4× DP1.4a 可經由 USB-C Alt Mode） |
| 有線網路 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（QSFP 200GbE，系統間互連） |
| 無線網路 | Wi-Fi 7 + Bluetooth 5.4 |
| 作業系統 | NVIDIA DGX OS（基於 Ubuntu Linux，kernel 6.x） |
| 架構 | aarch64（ARM64） |
| 尺寸 | 151 × 151 × 52 mm（約 5.95" × 5.95" × 2.05"） |
| 重量 | 約 1.2 kg（2.65 lbs） |
| 供電 | 240W USB-C 電源供應器 |
| 版本 | 消費版 / 工業版（EdgeXpert-MS-C931，寬溫 / 工業級應用） |

### 2.2 軟體環境：NVIDIA DGX OS

MSI EdgeXpert 出廠預裝 NVIDIA DGX OS，與 DGX Spark / ASUS GX10 完全相同：

| 項目 | 說明 |
|---|---|
| 基礎 | Ubuntu Linux（NVIDIA 客製化） |
| Kernel | Linux 6.x |
| 架構 | aarch64（ARM64） |
| 預裝軟體 | NVIDIA AI 軟體堆疊（CUDA、cuDNN、TensorRT、PyTorch、Jupyter 等） |
| 套件管理 | apt |

### 2.3 與 DGX Spark 的差異

MSI EdgeXpert 是 DGX Spark 平台的 OEM 版本，核心硬體與軟體完全相同：

| 項目 | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| 機構設計 | MSI 客製化機殼，工業版選項 | NVIDIA 參考機殼 |
| 儲存選項 | 1TB / 4TB | 最高 4TB |
| 目標市場 | 邊緣 AI / 工業 AI / 桌面開發 | 桌面 AI 開發 |
| 配件 | MSI 原廠配件 | NVIDIA 原廠配件 |

對 ALFA 相容性的影響：零影響。USB 控制器、kernel 版本、驅動框架均與 DGX Spark 完全相同。

### 2.4 USB Type-C 轉接需求

EdgeXpert 的 4 個 USB 埠均為 Type-C，ALFA 全系列網卡（除 AXML 為 USB-C 外）均為 USB Type-A，需使用轉接器。建議選擇支援 USB 3.2 Gen 2×2（20Gbps）的轉接器。

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下（判定母體：9 款）：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Linux 驅動狀態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel（mt7921u） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel（mt7921u） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree（8812au） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel（mt76x2u）⭐ 首選 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree（8812au 涵蓋） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree（8821cu） |

## 4. 適用機型與晶片組

### 4.1 推薦等級分類

| 推薦等級 | 機型（晶片組） | 說明 |
|---|---|---|
| ⭐ 強烈推薦 | AWUS036ACM（MT7612U） | in-kernel 驅動，開箱即用，AC1200 雙頻，支援 AP / Monitor / Injection |
| ✅ 推薦 | AWUS036ACHM（MT7610U） | in-kernel 驅動，低功耗，AC433 雙頻 |
| ✅ 推薦（Wi-Fi 6E） | AWUS036AXML / AXM（MT7921AUN） | in-kernel 驅動，Wi-Fi 6E，AXML 為 USB-C 可直插 |
| ⚠️ 可用但需編譯 | AWUS036ACH（RTL8812AU） | 需編譯 morrownr/8812au（ARM64），完成後功能完整 |
| ⚠️ 可用但需編譯 | AWUS036ACS / EACS | 需編譯對應 out-of-tree 驅動 |
| ⚠️ 可用但需注意 | AWUS036AX / AXER（RTL8832BU） | kernel 6.x 的 rtw89 可能已支援；若無需編譯 |

### 4.2 使用場景建議

| 使用場景 | 建議機型 | 說明 |
|---|---|---|
| 邊緣 AI 閘道無線上網 | AWUS036ACM / ACHM | in-kernel 驅動，穩定，免維護 |
| 工業環境無線滲透測試 | AWUS036ACH 或 AWUS036ACM | 兩者均支援 Monitor + Injection |
| Wi-Fi 6E / 6GHz 頻段 | AWUS036AXML / AXM | MT7921AUN in-kernel 驅動 |
| 不需要外接 WiFi | — | EdgeXpert 已內建 Wi-Fi 7，一般上網不需外接 |

## 5. 環境需求

### 5.1 硬體需求

| 項目 | 需求 |
|---|---|
| USB 轉接器 | USB-C to USB-A 轉接器或傳輸線（AXML 除外），建議支援 USB 3.2 Gen 2×2 |
| 供電 | MSI EdgeXpert 原廠 240W USB-C 電源供應器 |

### 5.2 軟體需求

| 項目 | 需求 |
|---|---|
| DGX OS 版本 | 任意現役版本（kernel 6.x） |
| 編譯工具（Realtek 晶片需要） | build-essential、git、bc、dkms |
| 無線管理工具 | iw、network-manager（DGX OS 預設安裝） |

## 6. 相容性判定

### ALFA 現役機型 × MSI EdgeXpert（GB10）相容性矩陣

| 機型 | 晶片組 | 驅動方式 | USB 偵測 | STA 上網 | AP 模式 | Monitor | 安裝難度 | 綜合評價 |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | 免安裝 | ⭐ 最佳 |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安裝 | ✅ 良好 |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安裝 | ✅ 良好 |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ 有限 | 免安裝 | ✅ 良好 |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | 中（編譯） | ⚠️ 可用 |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | 中（編譯） | ⚠️ 可用 |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | 中（編譯） | ⚠️ 可用 |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | 中-高 | ⚠️ 可用 |
| AWUS036AXER | RTL8832BU | 同上 | ✅ | ⚠️ | ⚠️ | ❌ | 中-高 | ⚠️ 可用 |

判定依據：MSI EdgeXpert 與 DGX Spark 共享相同的 GB10 硬體平台與 DGX OS（kernel 6.x, aarch64），相容性判定與 DGX Spark 完全一致。

## 7. 超詳細 Step by Step 設定步驟

MSI EdgeXpert 的安裝步驟與 NVIDIA DGX Spark 完全相同。以下為精簡版，完整步驟請參考 [ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) 第 7 節。

### 7.1 MediaTek 晶片機型（開箱即用）

**步驟 1：插入網卡**

使用 USB-C to USB-A 轉接器（AXML 可直插），將 ALFA 網卡插入 EdgeXpert 的 USB-C 埠。

**步驟 2：確認 USB 偵測**

```bash
lsusb
# 預期輸出範例（AWUS036ACM / MT7612U）：
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**步驟 3：確認網路介面**

```bash
ip link show
# 應自動出現 wlan0（in-kernel 驅動自動載入）
```

**步驟 4：連線 WiFi**

```bash
nmcli dev wifi connect "SSID" password "密碼"
```

### 7.2 Realtek 晶片機型（需編譯）

以 AWUS036ACH（RTL8812AU）為例：

**步驟 1：安裝編譯工具**

```bash
sudo apt update && sudo apt install -y build-essential git bc dkms
```

**步驟 2：下載並編譯驅動**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# 確認 Makefile 中 CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe 8812au
```

**步驟 3：插入網卡後確認介面**

```bash
ip link show
```

**步驟 4：連線 WiFi**

```bash
nmcli dev wifi connect "SSID" password "密碼"
```

### 7.3 監聽模式（滲透測試）

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網卡 | USB-C 轉接器不良 / 僅充電規格 | 更換支援資料傳輸的 USB 3.2 Gen 2×2 轉接器；嘗試不同 USB-C 埠 |
| MediaTek 晶片無 wlan 介面 | module 未自動載入 / firmware 缺失 | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；檢查 `dmesg \| grep mt76` |
| Realtek 驅動編譯失敗 | 交叉編譯設定錯誤 | 確認在 EdgeXpert 上原生編譯；Makefile 不應設定 CROSS_COMPILE |
| WiFi 速度慢 | 轉接器僅支援 USB 2.0 | 更換 USB 3.2 Gen 2×2 轉接器 |
| 內建 Wi-Fi 7 與外接衝突 | 路由衝突 | `sudo nmcli radio wifi off` 停用內建 WiFi 後再使用外接 |
| 工業環境高溫下不穩定 | 散熱 / 工業版差異 | 確認使用工業版 EdgeXpert（MS-C931）；確保環境溫度在規格範圍內 |

## 9. 已知限制

- USB Type-C 轉接需求：除 AXML 外，所有 ALFA 網卡需 USB-C to USB-A 轉接器
- Realtek 晶片需手動編譯：RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU 未進入 mainline
- 內建 Wi-Fi 7 可能與外接衝突：EdgeXpert 已內建 Wi-Fi 7 + BT 5.4
- AP 模式需手動設定：DGX OS 預設為開發環境
- 6GHz 法規限制：Wi-Fi 6E 可用性取決於法規區域
- 驅動更新依賴上游：Realtek out-of-tree 驅動由社群維護，kernel 更新後需重新編譯
- 工業版差異不影響相容性：MSI 工業版（MS-C931）的硬體規格與消費版相同，USB WiFi 相容性一致

反駁條件：若 MSI 官方規格頁變更（USB 埠規格調整、kernel 版本低於 6.x），或實機測試發現 mt76x2u / mt7921u 在 DGX OS 上無法自動載入，本文第 6 節相容性矩陣需重新檢視；若 morrownr 驅動停止維護 ARM64 分支，Realtek 機型判定需重審。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| MSI EdgeXpert 官方商城（US） | EdgeXpert 消費版規格 | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ 已查核 | 2026-09-03 |
| MSI EdgeXpert 商城（TW） | EdgeXpert 消費版規格（23STW） | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ 已查核 | 2026-09-03 |
| MSI 工業電腦官方公告 | EdgeXpert 產品發布資訊 | https://ipc.msi.com/en/news/146241 | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX Spark 官方頁面 | GB10 平台資訊 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 無線網卡是否支援 ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 無線網卡是否支援 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 無線網卡是否支援 GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責聲明：本文相容性判定以 MSI EdgeXpert 預裝的 NVIDIA DGX OS（kernel 6.x, aarch64）為基準。EdgeXpert 與 DGX Spark 共享相同硬體平台，相容性完全一致。MediaTek 晶片驅動為 Linux mainline，穩定性高；Realtek 晶片驅動為社群維護。EdgeXpert 已內建 Wi-Fi 7，外接 ALFA 主要用於滲透測試或特殊晶片組需求。
