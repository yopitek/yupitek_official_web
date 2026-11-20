---
title: "ALFA 無線網路卡是否支援 NVIDIA DGX Spark（GB10）"
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
description: "ALFA 9 款 USB 網路卡在 NVIDIA DGX Spark（GB10）的相容性：ASUS GX10 實測 kernel 6.17 全部使用內建驅動、插上即用免 DKMS；EACS／ACH／ACS 注入最穩，AXM／AXML 注入失敗。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本文已依 2026-11 GX10 實測更新：在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）上，ALFA 現役 9 款網路卡全部使用 kernel 內建驅動，插上即可用，不需 DKMS。完整數據見 [ALFA 9 款網路卡 ARM64 實測總表](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。僅在 GX10 實測，其他 GB10 機型未逐台測試。

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網路卡能否在 NVIDIA DGX Spark（GB10 Grace Blackwell）個人 AI 超級電腦上使用？」

簡短結論：DGX Spark 執行 NVIDIA DGX OS（基於 Ubuntu，kernel 6.x）。我們在同為 GB10 平台的 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）實測 ALFA 現役 9 款 USB 網路卡，全部使用 kernel 內建驅動，插上即可用，不需編譯或 DKMS。DGX Spark 使用同一款 GB10 與 NVIDIA kernel 系列，預期行為相同，但僅在 GX10 實測，DGX Spark 未逐台測試。功能差異：MediaTek MT7921 機型（AWUS036AXM / AXML）在 stock kernel 6.17 上封包注入失敗，monitor、AP、WPA3 可用；其餘 7 款的 monitor 與注入皆實測可用。各卡驅動進入主線的最低 kernel 版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低於該版本的舊 kernel 才需要社群 DKMS 驅動。注意：DGX Spark 的 USB 埠均為 USB Type-C，ALFA 網路卡為 USB Type-A，需使用 USB-C to USB-A 轉接器或傳輸線。

判定母體：ALFA 現役 9 款 USB 網路卡（AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM）。

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

DGX Spark 的軟體環境對 ALFA 網路卡相容性有兩個關鍵影響：

- Kernel 6.x（現代）：kernel 6.17（GX10 實測版本）已內建本文 9 款網路卡的驅動，包括 mt76（MT7612U / MT7610U，4.19+）、mt7921u（MT7921AUN，5.18+）、rtw88（RTL8821CU 6.2+；RTL8812AU / RTL8811AU 6.13+）與 rtw89（RTL8832BU，6.17+）。這與 Jetson Nano 的 kernel 4.9 形成鮮明對比。
- ARM64（aarch64）架構：使用 kernel 內建驅動時不需要在 ARM64 上編譯任何東西；只有 kernel 低於該卡最低版本的舊系統，Realtek 機型才需要編譯社群 DKMS 驅動（如 morrownr 系列，需確認 Makefile 中 CONFIG_PLATFORM_ARM64 = y）。

### 2.4 USB Type-C 轉接需求

DGX Spark 的 4 個 USB 埠均為 Type-C，而 ALFA 全系列網路卡（除 AXML 為 USB-C 外）均為 USB Type-A 介面：

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

截至 2026 年 9 月，ALFA Network 現役 USB 無線網路卡產品線如下（判定母體：9 款）：

| 機型 | Wi-Fi 等級 | 晶片組 | 介面 | Linux 內建驅動（最低 kernel 版本） |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E（6GHz 實測可用） | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ 內建（mt7921u，5.18+） |
| AWUS036AXM | Wi-Fi 6E（廠商標示，6GHz 未實測） | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ 內建（mt7921u，5.18+） |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 內建（rtw89_8852bu，6.17+） |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ 內建（rtw89_8852bu，6.17+） |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ 內建（rtw88_8812au，6.13+） |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ 內建（mt76x0u，4.19+） |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ 內建（mt76x2u，4.19+） |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ 內建（rtw88_8821au，6.13+） |
| AWUS036EACS | Wi-Fi 5 (AC600) + 藍牙 | Realtek RTL8821CU | USB 2.0 | ✅ 內建（rtw88_8821cu，6.2+） |

註：GX10 實測的 kernel 6.17 已內建全部 9 款驅動；各卡最低 kernel 版本不同（見上表括號）。kernel 低於該卡最低版本的舊系統，才需要安裝社群維護的 DKMS 驅動。

## 4. 適用機型與晶片組

### 4.1 推薦等級分類

| 推薦等級 | 機型（晶片組） | 說明 |
|---|---|---|
| ⭐ 滲透測試首選 | AWUS036EACS（RTL8821CU）/ AWUS036ACH（RTL8812AU）/ AWUS036ACS（RTL8811AU） | 內建驅動免安裝；注入實測 EACS、ACH 兩頻 100%，ACS 2.4GHz 100%、5GHz 96%；可端到端擷取 WPA handshake |
| ✅ 推薦 | AWUS036ACM（MT7612U） | 內建驅動免安裝；monitor、注入（2.4GHz 63–83%、5GHz 76%）、AP、WPA3 皆可用 |
| ✅ 推薦 | AWUS036ACHM（MT7610U） | 內建驅動免安裝；2.4GHz 注入 96–100%，5GHz 注入僅廣播可用；WPA3 AP 需設定 sae_pwe=0 |
| ✅ 推薦（Wi-Fi 6） | AWUS036AX / AXER（RTL8832BU） | 內建驅動免安裝；monitor 收訊強，注入可用（2.4GHz：AX 96%、AXER 73%），AP 支援 80MHz |
| ⚠️ 僅適合連線／AP | AWUS036AXML / AXM（MT7921AUN） | 內建驅動免安裝；monitor、AP、WPA3 可用，但 stock kernel 6.17 上注入失敗，不適合滲透測試；AXML 為 USB-C 可直插 |

### 4.2 使用場景建議

| 使用場景 | 建議機型 | 說明 |
|---|---|---|
| 一般無線上網（最簡單） | 9 款皆可（例如 AWUS036ACM / ACHM） | 全部為 kernel 內建驅動，插上即可用 |
| 無線滲透測試 / 監聽 / 注入 | AWUS036EACS / ACH / ACS | 注入實測 96–100%，可端到端擷取 WPA handshake；勿選 AXM / AXML（注入失敗） |
| Wi-Fi 6 + AP 熱點 | AWUS036AX / AXER | 2x2、80MHz AP 實測可用 |
| 6GHz 頻段 | AWUS036AXML | 實測可在 6GHz 建立 WPA3 AP；AXM 同晶片但 6GHz 未實測 |
| 已有 AWUS036ACH 想繼續用 | AWUS036ACH | kernel 6.13 以上內建 rtw88_8812au，插上即可用，兩頻注入實測 100% |
| 不需要外接 WiFi（使用內建） | — | DGX Spark 已內建 Wi-Fi 7，一般上網不需外接 ALFA |

注意：DGX Spark 已內建 Wi-Fi 7 + Bluetooth 5.4，一般上網場景不需要外接 ALFA 網路卡。外接 ALFA 的主要需求是：滲透測試（監聽/注入）、特殊晶片組需求、或內建 WiFi 不夠用的場景。

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
| Kernel 版本 | kernel 6.17（GX10 實測 6.17.0-1014-nvidia）已內建全部 9 款網路卡的驅動，不需編譯工具；各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低於該版本才需安裝社群 DKMS 驅動 |
| 無線管理工具 | iw、wpa_supplicant、network-manager（DGX OS 預設安裝） |

## 6. 相容性判定

### ALFA 現役機型 × NVIDIA DGX Spark（GB10）相容性矩陣

| 機型 | 晶片組 | 驅動（kernel 內建） | USB 偵測 | STA 上網 | AP 模式 | Monitor | 封包注入 | 安裝難度 | 綜合評價 |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 兩頻 100% | 免安裝 | ⭐ 最佳 |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 兩頻 100% | 免安裝 | ⭐ 最佳 |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100%／5G 96% | 免安裝 | ⭐ 最佳 |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83%／5G 76% | 免安裝 | ✅ 良好 |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100%／5G 僅廣播 | 免安裝 | ✅ 良好 |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 收訊強 | ✅ 2.4G 96%／5G 可用 | 免安裝 | ✅ 良好 |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ 收訊強 | ✅ 2.4G 73%／5G 可用 | 免安裝 | ✅ 良好 |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 收訊弱 | ❌ 失敗 | 免安裝 | ⚠️ 僅連線／AP |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ 收訊弱 | ❌ 失敗 | 免安裝 | ⚠️ 僅連線／AP |

判定依據：2026-11-16～11-18 於 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）實機測試，測試對象為自有 Wi-Fi 與自有手機。DGX Spark 使用同一款 GB10 與 NVIDIA kernel 系列，預期行為相同，但僅在 GX10 實測，DGX Spark 未逐台測試。完整數據見 [ALFA 9 款網路卡 ARM64 實測總表](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 7. 超詳細 Step by Step 設定步驟

### 7.1 前置作業

**步驟 1：開機並登入 DGX Spark**（透過 SSH 或直接連接鍵盤螢幕）

```bash
ssh username@<dgx-spark-ip>
```

**步驟 2：確認系統架構與 kernel 版本**

```bash
uname -m
# 預期: aarch64
uname -r
# 預期: 6.x.x (DGX OS kernel)
```

**步驟 3：確認 kernel 版本是否為 6.17 以上**

kernel 6.17 以上已內建全部 9 款網路卡的驅動，不需要安裝編譯工具。各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）；低於該版本時，Realtek 機型才需要社群 DKMS 驅動（見 7.3 最後一段）。

### 7.2 路徑 A：MediaTek 晶片機型（AWUS036ACM / ACHM / AXML / AXM）— 開箱即用

**步驟 1：插入網路卡**

使用 USB-C to USB-A 轉接器（AXML 可直接插入 USB-C 埠），將 ALFA 網路卡插入 DGX Spark 的 USB 埠。

**步驟 2：確認網路卡被偵測**

```bash
lsusb
# 預期輸出範例 (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**步驟 3：確認網路介面已自動建立**

```bash
ip link show
# 預期出現 wlx 開頭的介面 (依 MAC 命名, in-kernel 驅動自動載入)
```

**步驟 4：掃描 WiFi 網路**（以下以 wlan0 示意，請換成 `ip link show` 查到的介面名稱）

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

### 7.3 路徑 B：Realtek Wi-Fi 5 機型（AWUS036ACH / ACS / EACS）— kernel 6.13+ 免安裝（EACS 6.2+）

**步驟 1：插入網路卡並確認驅動已自動載入**

```bash
uname -r          # ACH/ACS 需 6.13 以上, EACS 需 6.2 以上
lsusb
lsmod | grep rtw88
ip link show
```

各機型自動載入的模組：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`（EACS 另含藍牙，實測可用）。

**步驟 2：連線方式同 7.2 步驟 5（使用 nmcli）**

**步驟 3：（可選）監聽模式與注入**

⚠️ 僅在自有或已取得授權的網路進行監聽與注入測試。

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # 換成 ip link 查到的介面名稱
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- 不要執行 `airmon-ng check kill`：它會關閉 NetworkManager，讓主機對外斷線。
- AWUS036AXM / AXML 在 stock kernel 6.17 上 `aireplay-ng --test` 會失敗（Found 0 APs），無法 deauth 或擷取 handshake。
- hcxdumptool 8.x 在 9 款卡上都出現 `failed to arm`（EACS 在 2.4 GHz 除外；驅動不支援 active monitor），請改用 airodump-ng + aireplay-ng。

**舊 kernel（ACH／ACS 低於 6.13、EACS 低於 6.2）才需要的步驟**：安裝 `build-essential git bc dkms` 後，編譯社群驅動，例如 RTL8812AU 使用 morrownr/8812au-20210820（確認 Makefile 中 `CONFIG_PLATFORM_ARM64 = y`）。版本足夠時請直接使用內建驅動。

### 7.4 路徑 C：Wi-Fi 6 機型（AWUS036AX / AXER，RTL8832BU）— kernel 6.17+ 免安裝

```bash
lsusb                      # 預期出現 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

GX10 實測：kernel 內建 `rtw89_8852bu` 自動載入，monitor 收訊強，注入可用（2.4GHz：AX 96%、AXER 73%），AP 支援 80MHz。rtw89_8852bu 自 kernel 6.17 才進入主線，kernel 6.16 以下的系統需要社群 DKMS 驅動（morrownr/rtl8852bu-20250826）。

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網路卡 | USB-C 轉接器不良 / 接觸不良 | 更換 USB-C to USB-A 轉接器；確認轉接器支援資料傳輸（非僅充電）；嘗試不同 USB-C 埠 |
| MediaTek 晶片插入後無 wlan 介面 | kernel module 未自動載入 / firmware 缺失 | 手動載入：`sudo modprobe mt76x2u`；檢查 `dmesg \| grep mt76`；安裝 firmware：`sudo apt install linux-firmware` |
| Realtek 卡插上後沒有 wlan 介面 | kernel 低於該卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），未內建對應驅動 | 以 `uname -r` 確認版本；升級 kernel，或在舊 kernel 安裝社群 DKMS 驅動 |
| 舊 kernel 安裝 DKMS 驅動後 modprobe 報 Operation not permitted | Secure Boot / 模組簽章 | 需簽章模組或關閉 Secure Boot（使用內建驅動不會遇到）|
| 反覆切換 monitor／AP 後掃不到任何訊號 | RX 停滯（RX stall） | 拔插網路卡讓 USB 重新列舉 |
| EACS／AXML 重插後沒有 wlx 介面 | 藍牙＋Wi-Fi 複合裝置 probe 卡住 | 換一個 USB 埠重插 |
| WiFi 連線不穩 / 速度慢 | USB-C 轉接器僅支援 USB 2.0 | 更換支援 USB 3.2 Gen 2×2 的轉接器；確認轉接器標示「Data」而非「Charge Only」 |
| 內建 Wi-Fi 7 與外接 ALFA 衝突 | 兩個無線介面路由衝突 | 停用內建 WiFi：`sudo nmcli radio wifi off` 或在 BIOS/UEFI 中停用；或設定路由優先順序 |
| 6GHz（Wi-Fi 6E）無法使用 | Regulatory Domain 限制 | 設定法規區域：`sudo iw reg set US`（美國開放 6GHz）；AXML 已實測可在 6GHz 運作，AXM 未實測 |
| AP 模式啟動失敗 | NetworkManager 與 hostapd 衝突 | 參考 Yopitek ALFA Soft AP 指南；停用 NetworkManager 管理該介面後手動設定 hostapd |
| 喚醒後網路卡消失 | USB 自動暫停 | 停用 USB 自動暫停：`echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 轉接需求：除 AXML 外，所有 ALFA 網路卡需 USB-C to USB-A 轉接器，轉接器品質會影響效能與穩定性
- MT7921 機型注入失敗：AWUS036AXM / AXML 在 stock kernel 6.17 上封包注入失敗，無法 deauth 或擷取 handshake；monitor、AP、WPA3 可用。主因是 kernel 6.16 以後的 mac80211 chanctx 回歸，社群修補版驅動仍有速率限制
- 實測範圍：僅在 ASUS GX10（kernel 6.17.0-1014-nvidia）實測；DGX Spark 未逐台測試，預期行為相同
- hcxdumptool 不可用：除 EACS 在 2.4 GHz 外，其餘卡皆出現 `failed to arm`，請改用 airodump-ng + aireplay-ng
- 內建 Wi-Fi 7 可能與外接衝突：DGX Spark 已內建 Wi-Fi 7，同時使用內建與外接 WiFi 時可能出現路由或資源衝突
- AP 模式需手動設定：DGX OS 預設為開發環境，AP 熱點模式需手動安裝設定 hostapd / dnsmasq
- 6GHz 法規限制：Wi-Fi 6E 的 6GHz 頻段可用性取決於法規區域設定，台灣地區 6GHz 開放狀況需確認最新法規
- 舊 kernel：kernel 低於該卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）的系統，Realtek 機型才需社群 DKMS 驅動（morrownr），且每次 kernel 更新後需重新編譯
- 滲透測試功能差異：GX10 實測注入成功率以 Realtek rtw88 機型最高（EACS、ACH 兩頻 100%）；MediaTek mt76 機型（ACM / ACHM）可用；MT7921（AXM / AXML）失敗
- 藍牙功能：AWUS036AXML 與 AWUS036EACS 的藍牙在 GX10 上實測可用；AWUS036AXM 的藍牙未單獨驗證（DGX Spark 已內建 BT 5.4）
- RTL8832BU（AWUS036AX / AXER）：驅動維護者 morrownr 曾公開建議避開 rtl8852/32au 系列的 out-of-tree 驅動（來源見第 10 節）。本次 GX10 實測使用的是 kernel 內建 `rtw89_8852bu`，monitor、注入、AP、WPA3 皆可用；此結論僅適用於 kernel 6.17 以上的內建驅動
- RTL8812AU（AWUS036ACH）：mac80211 標準的 in-kernel 驅動 `rtw88_8812au` 已於 kernel 6.13 併入主線、6.14 起品質成熟（morrownr 公告）。GX10 實測 kernel 6.17 插上即用、兩頻注入 100%。客服回覆前可先請客戶回報 `uname -r` 確認是否為 6.13 以上

反駁條件：若 DGX OS 更新後 kernel 版本或 USB 控制器驅動變動導致行為不同，或在 DGX Spark 實機上測得與 GX10 不同的結果，本文第 6 節相容性矩陣需重新檢視；若日後 kernel 修正 mt7921u 的注入問題，AWUS036AXM / AXML 的評價可由「僅連線／AP」升級。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| NVIDIA DGX Spark 官方頁面 | DGX Spark 規格與平台資訊 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX 文件 | DGX OS 系統架構與 kernel 版本 | https://docs.nvidia.com/dgx/dgx-spark | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動（ARM64 支援） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux 驅動（舊 kernel 用） | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驅動 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Linux kernel mt76 驅動文件 | MediaTek mt76 / mt7921 mainline 驅動說明（含各晶片支援起始 kernel 版本） | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ 已查核 | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yopitek） | ALFA 在 Linux 上的 AP 模式設定指南 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| ALFA 9 款網路卡 ARM64 實測總表（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 實機測試 | https://yupitek.com/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 實測 | 2026-11-18 |
| ALFA Network 產品總覽（Yopitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | 驅動維護者官方聲明：建議避開 rtl8852/32au（RTL8832BU）晶片 | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | RTL8812AU 驅動狀態最新公告（kernel 6.13 併入主線、6.14 品質成熟） | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網路卡是否支援 MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)｜[ALFA 無線網路卡是否支援 ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 無線網路卡是否支援 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 無線網路卡是否支援 GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[ALFA 無線網路卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

免責聲明：本文相容性判定以 2026-11 在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）的實機測試為基準。DGX Spark 與 GX10 使用同一款 GB10 與 NVIDIA kernel 系列，預期行為相同，但未逐台測試。GX10 實測的 kernel 6.17 已內建 ALFA 9 款網路卡的驅動（各卡最低版本不同），kernel 低於該卡最低版本時才需社群 DKMS 驅動（morrownr）。DGX Spark 已內建 Wi-Fi 7，外接 ALFA 網路卡主要用於滲透測試或特殊晶片組需求。USB-C 轉接器的品質會直接影響使用體驗，建議選擇有品牌、標示 USB 3.2 Gen 2×2 的轉接器。監聽與注入僅限在自有或已取得授權的網路進行。
