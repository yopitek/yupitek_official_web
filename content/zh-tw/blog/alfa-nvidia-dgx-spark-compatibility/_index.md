---
title: "ALFA 無線網卡是否支援 NVIDIA DGX Spark（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "邊緣 AI / GPU 伺服器"
description: "DGX Spark 執行 NVIDIA DGX OS（基於 Ubuntu，kernel 6.x），對 ALFA 網卡的相容性與一般現代 Linux 桌面系統相同。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驅動，開箱即用；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網卡能否在 NVIDIA DGX Spark（GB10 Grace Blackwell）個人 AI 超級電腦上使用？」

簡短結論：DGX Spark 執行 NVIDIA DGX OS（基於 Ubuntu，kernel 6.x），對 ALFA 網卡的相容性與一般現代 Linux 桌面系統相同。MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）使用 in-kernel 驅動，開箱即用；Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）需編譯 out-of-tree 驅動（ARM64 / aarch64 架構）。注意：DGX Spark 的 USB 埠均為 USB Type-C，ALFA 網卡為 USB Type-A，需使用 USB-C to USB-A 轉接器或傳輸線。

判定母體：ALFA 現役 9 款 USB 網卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

## 2. 分析目標硬體規格架構

### 2.1 NVIDIA DGX Spark 硬體規格

| 項目 | 規格 |
|---|---|
| 產品名稱 | NVIDIA DGX Spark |
| 核心晶片 | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架構，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 效能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS |
| 系統記憶體 | 128GB LPDDR5x 統一記憶體（256-bit，273 GB/s） |
| 儲存 | 最高 4TB NVMe M.2 SSD（自加密） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps），其中 1 個支援 PD 輸入（180W EPR PD3.1） |
| 顯示輸出 | 1× HDMI 2.1a |
| 有線網路 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC（200G QSFP） |
| 無線網路 | Wi-Fi 7（內建）+ Bluetooth 5.4 |
| 作業系統 | NVIDIA DGX OS（基於 Ubuntu Linux，kernel 6.x） |
| 架構 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 約 1.2 kg |
| 供電 | 240W USB-C 電源供應器 |

### 2.2 軟體環境：NVIDIA DGX OS

| 項目 | 說明 |
|---|---|
| 基礎 | Ubuntu Linux（NVIDIA 客製化） |
| Kernel | Linux 6.x（具體版本隨 DGX OS 更新） |
| 架構 | aarch64（ARM64） |
| 預裝軟體 | NVIDIA AI 軟體堆疊（CUDA、cuDNN、TensorRT、PyTorch、Jupyter 等） |
| 套件管理 | apt（Debian/Ubuntu 系） |
| 驅動框架 | 標準 Linux kernel driver 架構（cfg80211 / mac80211） |

### 2.3 關鍵特徵：現代 kernel + ARM64

DGX Spark 的軟體環境對 ALFA 網卡相容性有兩個關鍵影響：

- Kernel 6.x（現代）：所有進入 mainline 的 WiFi 驅動均可直接使用，包括 mt76（MT7612U / MT7610U）和 mt7921u（MT7921AUN）。這與 Jetson Nano 的 kernel 4.9 形成鮮明對比。
- ARM64（aarch64）架構：Realtek out-of-tree 驅動（8812au / 8821cu / rtl8852bu）需在 ARM64 上編譯。這些驅動的上游（morrownr）已支援 ARM64 編譯，但需確認 Makefile 中的 CONFIG_PLATFORM_ARM64 = y。

### 2.4 USB Type-C 轉接需求

DGX Spark 的 4 個 USB 埠均為 Type-C，而 ALFA 全系列網卡（除 AXML 為 USB-C 外）均為 USB Type-A 介面：

| 機型 | 介面規格 | 是否需轉接 |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ 不需轉接（可直接插入） |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ 需要 USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ 需要 |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ 需要 |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ 需要 |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ 需要 |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ 需要 |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ 需要 |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ 需要 |

建議：使用支援 USB 3.2 Gen 2×2（20Gbps）的 USB-C to USB-A 轉接器或傳輸線，確保 AWUS036ACH / ACM / AX 等 USB 3.x 機型可發揮全速。

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網卡產品線如下（判定母體：9 款）：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Linux 驅動狀態 |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel（mt7921u，kernel 5.19+） |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel（mt7921u） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89（kernel 5.16+，USB 支援陸續合入）或 out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ 同上 |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree（morrownr/8812au，需 ARM64 編譯） |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel（mt76x0u） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel（mt76x2u）⭐ 首選 |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree（8812au 涵蓋） |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree（morrownr/8821cu） |

## 4. 適用機型與晶片組

### 4.1 推薦等級分類

| 推薦等級 | 機型（晶片組） | 說明 |
|---|---|---|
| ⭐ 強烈推薦 | AWUS036ACM（MT7612U） | in-kernel 驅動，開箱即用，AC1200 雙頻，支援 AP / Monitor / Injection |
| ✅ 推薦 | AWUS036ACHM（MT7610U） | in-kernel 驅動，低功耗，AC433 雙頻 |
| ✅ 推薦（Wi-Fi 6E） | AWUS036AXML / AXM（MT7921AUN） | in-kernel 驅動，Wi-Fi 6E，AXML 為 USB-C 可直插 |
| ⚠️ 可用但需編譯 | AWUS036ACH（RTL8812AU） | 需編譯 morrownr/8812au（ARM64），完成後功能完整（含 Monitor / Injection） |
| ⚠️ 可用但需編譯 | AWUS036ACS（RTL8811AU） | 由 8812au 驅動涵蓋 |
| ⚠️ 可用但需編譯 | AWUS036EACS（RTL8811CU） | 需編譯 morrownr/8821cu（ARM64） |
| ⚠️ 可用但需注意 | AWUS036AX / AXER（RTL8832BU） | kernel 6.x 的 rtw89 可能已支援 USB；若無需編譯 out-of-tree |

### 4.2 使用場景建議

| 使用場景 | 建議機型 | 說明 |
|---|---|---|
| 一般無線上網（最簡單） | AWUS036ACM / ACHM | in-kernel 驅動，免編譯，開箱即用 |
| 無線滲透測試 / 監聽 / 注入 | AWUS036ACH 或 AWUS036ACM | 兩者均支援 Monitor + Injection；ACH 需編譯，ACM 開箱即用 |
| Wi-Fi 6E / 6GHz 頻段 | AWUS036AXML / AXM | MT7921AUN in-kernel 驅動，kernel 6.x 完整支援 |
| 已有 AWUS036ACH 想繼續用 | AWUS036ACH | 編譯 ARM64 驅動即可，功能完整 |
| 不需要外接 WiFi（使用內建） | — | DGX Spark 已內建 Wi-Fi 7，一般上網不需外接 ALFA |

注意：DGX Spark 已內建 Wi-Fi 7 + Bluetooth 5.4，一般上網場景不需要外接 ALFA 網卡。外接 ALFA 的主要需求是：滲透測試（監聽/注入）、特殊晶片組需求、或內建 WiFi 不夠用的場景。

## 5. 環境需求

### 5.1 硬體需求

| 項目 | 需求 |
|---|---|
| USB 轉接器 | USB-C to USB-A 轉接器或傳輸線（AXML 除外） |
| 供電 | DGX Spark 原廠 240W USB-C 電源供應器（USB 埠供電充足） |
| 散熱 | 原廠散熱即可（USB WiFi 不會顯著增加系統負載） |

### 5.2 軟體需求

| 項目 | 需求 |
|---|---|
| DGX OS 版本 | 任意現役版本（kernel 6.x） |
| 編譯工具（Realtek 晶片需要） | build-essential、git、bc、dkms |
| 無線管理工具 | iw、wpa_supplicant、network-manager（DGX OS 預設安裝） |
| 網路 | 編譯驅動期間需有線網路（10GbE）或內建 Wi-Fi 7 聯網 |

## 6. 相容性判定

### ALFA 現役機型 × NVIDIA DGX Spark（GB10）相容性矩陣

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

判定依據：DGX OS kernel 6.x 的 mainline 驅動可用性 + morrownr 驅動的 ARM64 支援。MediaTek 晶片因驅動已進入 mainline，在 kernel 6.x 上開箱即用。Realtek 晶片需編譯 out-of-tree 驅動，但 ARM64 編譯已被上游支援。

## 7. 超詳細 Step by Step 設定步驟

### 7.1 前置作業

**步驟 1：開機並登入 DGX Spark**（透過 SSH 或直接連接鍵盤螢幕）

```bash
ssh username@<dgx-spark-ip>
```

**步驟 2：確認系統架構與 kernel 版本**

```bash
uname -m
# 預期：aarch64
uname -r
# 預期：6.x.x（DGX OS kernel）
```

**步驟 3：（Realtek 晶片需要）安裝編譯工具**

```bash
sudo apt update
sudo apt install -y build-essential git bc dkms
```

### 7.2 路徑 A：MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）— 開箱即用

**步驟 1：插入網卡**

使用 USB-C to USB-A 轉接器（AXML 可直接插入 USB-C 埠），將 ALFA 網卡插入 DGX Spark 的 USB 埠。

**步驟 2：確認網卡被偵測**

```bash
lsusb
# 預期輸出範例（AWUS036ACM / MT7612U）：
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**步驟 3：確認網路介面已自動建立**

```bash
ip link show
# 預期出現 wlan0 或 wlp... 介面（in-kernel 驅動自動載入）
```

**步驟 4：掃描 WiFi 網路**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**步驟 5：連線到 WiFi（使用 NetworkManager）**

```bash
nmcli dev wifi list
nmcli dev wifi connect "你的WiFi名稱" password "你的WiFi密碼"
```

**步驟 6：（可選）啟用監聽模式**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 路徑 B：Realtek 晶片機型（AWUS036ACH / ACS / EACS）— 需編譯

以 AWUS036ACH（RTL8812AU）為例：

**步驟 1：下載驅動原始碼**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**步驟 2：確認 ARM64 編譯選項**

編輯 Makefile，確認 `CONFIG_PLATFORM_ARM64 = y`（多數新版本自動偵測 aarch64）。

**步驟 3：編譯與安裝**

```bash
make
sudo make install
sudo modprobe 8812au
```

**步驟 4：插入 ALFA 網卡（透過 USB-C to USB-A 轉接器），確認介面**

```bash
ip link show
# 預期出現 wlan0
```

**步驟 5：連線方式同 7.2 步驟 5（使用 nmcli）**

**步驟 6：（可選）監聽模式與注入**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 路徑 C：Wi-Fi 6 機型（AWUS036AX / AXER，RTL8832BU）

**步驟 1：先檢查 kernel 是否已有 rtw89 USB 支援**

```bash
# 插入網卡後檢查
lsusb
dmesg | grep -i "rtw89\|rtl8852\|8832"
ip link show
# 若自動出現 wlan0，代表 kernel 6.x 的 rtw89 已支援，可直接使用
```

**步驟 2：若 kernel 未自動支援，編譯 out-of-tree 驅動**

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
# 確認 CONFIG_PLATFORM_ARM64 = y
make
sudo make install
sudo modprobe rtl8852bu
```

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網卡 | USB-C 轉接器不良 / 接觸不良 | 更換 USB-C to USB-A 轉接器；確認轉接器支援資料傳輸（非僅充電）；嘗試不同 USB-C 埠 |
| MediaTek 晶片插入後無 wlan 介面 | kernel module 未自動載入 / firmware 缺失 | 手動載入：`sudo modprobe mt76x2u`；檢查 `dmesg \| grep mt76`；安裝 firmware：`sudo apt install linux-firmware` |
| Realtek 驅動 make 報錯 aarch64-linux-gnu-gcc: not found | 交叉編譯設定錯誤 | 確認在 DGX Spark 上原生編譯（非交叉編譯）；Makefile 中不應設定 CROSS_COMPILE |
| modprobe 8812au 報 Operation not permitted | Secure Boot / 模組簽章 | DGX Spark 預設不啟用 Secure Boot；若有啟用，需簽章模組或關閉 Secure Boot |
| WiFi 連線不穩 / 速度慢 | USB-C 轉接器僅支援 USB 2.0 | 更換支援 USB 3.2 Gen 2×2 的轉接器；確認轉接器標示「Data」而非「Charge Only」 |
| 內建 Wi-Fi 7 與外接 ALFA 衝突 | 兩個無線介面路由衝突 | 停用內建 WiFi：`sudo nmcli radio wifi off` 或在 BIOS/UEFI 中停用；或設定路由優先順序 |
| 6GHz（Wi-Fi 6E）無法使用 | Regulatory Domain 限制 | 設定法規區域：`sudo iw reg set US`（美國開放 6GHz）；確認 AWUS036AXML/AXM 的 firmware 支援 6GHz |
| AP 模式啟動失敗 | NetworkManager 與 hostapd 衝突 | 參考 Yupitek ALFA Soft AP 指南；停用 NetworkManager 管理該介面後手動設定 hostapd |
| 喚醒後網卡消失 | USB 自動暫停 | 停用 USB 自動暫停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 轉接需求：除 AXML 外，所有 ALFA 網卡需 USB-C to USB-A 轉接器，轉接器品質會影響效能與穩定性
- Realtek 晶片需手動編譯：RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU 未進入 mainline，需在 ARM64 上編譯 out-of-tree 驅動
- 內建 Wi-Fi 7 可能與外接衝突：DGX Spark 已內建 Wi-Fi 7，同時使用內建與外接 WiFi 時可能出現路由或資源衝突
- AP 模式需手動設定：DGX OS 預設為開發環境，AP 熱點模式需手動安裝設定 hostapd / dnsmasq
- 6GHz 法規限制：Wi-Fi 6E 的 6GHz 頻段可用性取決於法規區域設定，台灣地區 6GHz 開放狀況需確認最新法規
- 驅動更新依賴上游：Realtek out-of-tree 驅動由社群（morrownr）維護，DGX OS kernel 更新後可能需要重新編譯
- 滲透測試功能差異：MediaTek mt76 系列的注入功能在 kernel 6.x 上已改善，但 Realtek 8812au 仍是滲透測試社群的傳統首選
- 藍牙功能：AWUS036AXM 的藍牙 5.2 功能在 DGX OS 上未經廣泛驗證（DGX Spark 已內建 BT 5.4）
- ⚠️ **RTL8832BU（AWUS036AX/AXER）驅動維護者已公開建議避免使用**：驅動維護者 morrownr 官方聲明指出 rtl8852/32au 系列「是很糟糕的驅動，懷疑晶片本身有問題」，建議 Linux 使用者現階段避開（來源見第 10 節）。本文第 4、6 節對這兩款機型的「⚠️ 可用但需注意」評級應理解為業界共識偏向不建議，而非單純的安裝難度問題
- 本文所引用的 RTL8812AU「out-of-tree」判定為 2026 年初資訊；實際上該晶片的 mac80211 標準相容 in-kernel 驅動已於 **kernel 6.13 併入主線、6.14 起品質成熟**（morrownr 官方公告），DGX OS 若採用 6.14+ 核心，AWUS036ACH 有機會不需編譯即可使用，建議客服在回覆前先請客戶回報 `uname -r` 確認

反駁條件：若 DGX OS 更新後 kernel 版本或 USB 控制器驅動變動導致行為不同，或 morrownr 驅動停止維護 ARM64 分支，本文第 6 節相容性矩陣需重新檢視；若 rtw89 USB 支援在 kernel 6.x 正式完整落地，AWUS036AX / AXER 的判定可由「可用但需注意」升級。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| NVIDIA DGX Spark 官方頁面 | DGX Spark 規格與平台資訊 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX 文檔 | DGX OS 系統架構與 kernel 版本 | https://docs.nvidia.com/dgx/dgx-spark | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動（ARM64 支援） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驅動 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驅動 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Linux kernel mt76 驅動文檔 | MediaTek mt76 / mt7921 mainline 驅動說明（含各晶片支援起始 kernel 版本） | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | ALFA 在 Linux 上的 AP 模式設定指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA Network 產品總覽（Yupitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驅動維護者官方聲明：建議避開 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU 驅動狀態最新公告（kernel 6.13 併入主線、6.14 品質成熟） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網卡是否支援 MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[ALFA 無線網卡是否支援 ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 無線網卡是否支援 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 無線網卡是否支援 GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責聲明：本文相容性判定以 NVIDIA DGX OS（kernel 6.x, aarch64）為基準。MediaTek 晶片驅動為 Linux mainline，穩定性高；Realtek 晶片驅動為社群維護（morrownr），實際穩定性可能隨版本變化。DGX Spark 已內建 Wi-Fi 7，外接 ALFA 網卡主要用於滲透測試或特殊晶片組需求。USB-C 轉接器的品質會直接影響使用體驗，建議選擇有品牌、標示 USB 3.2 Gen 2×2 的轉接器。
