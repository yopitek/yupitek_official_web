---
title: "ALFA 無線網路卡是否支援 GIGABYTE AI TOP ATOM（GB10）"
date: 2026-09-03
draft: false
slug: "alfa-gigabyte-ai-top-atom-compatibility"
tags:
  - "ALFA"
  - "GIGABYTE"
  - "AI-TOP-ATOM"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "邊緣 AI / GPU 伺服器"
description: "ALFA 9 款 USB 網路卡在 GIGABYTE AI TOP ATOM（GB10）的相容性：ASUS GX10 實測 kernel 6.17 全部使用內建驅動、插上即用免 DKMS；EACS／ACH／ACS 注入最穩，AXM／AXML 注入失敗。"
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 本文已依 2026-11 GX10 實測更新：在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）上，ALFA 現役 9 款網路卡全部使用 kernel 內建驅動，插上即可用，不需 DKMS。完整數據見 [ALFA 9 款網路卡 ARM64 實測總表](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。僅在 GX10 實測，其他 GB10 機型未逐台測試。

## 1. 問題摘要

客戶詢問：「ALFA 系列 USB 無線網路卡能否在 GIGABYTE AI TOP ATOM（型號 ATAGB10-9000，NVIDIA GB10 Grace Blackwell）個人 AI 超級電腦上使用？」

簡短結論：GIGABYTE AI TOP ATOM 與 NVIDIA DGX Spark 使用同一款 GB10 晶片與 NVIDIA kernel 系列。我們在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）實測 ALFA 現役 9 款 USB 網路卡（AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML），全部使用 kernel 內建驅動，插上即可用，不需編譯或 DKMS。預期行為相同，但僅在 GX10 實測，GIGABYTE AI TOP ATOM 未逐台測試。功能差異：MediaTek MT7921 機型（AWUS036AXM / AXML）在 stock kernel 6.17 上封包注入（packet injection）失敗，monitor、AP、WPA3 可用；其餘 7 款的 monitor 與注入皆實測可用。各卡驅動進入主線的最低 kernel 版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低於該版本的舊 kernel 才需要社群 DKMS 驅動。注意：AI TOP ATOM 的 USB 埠均為 USB Type-C，ALFA 網路卡（AXML 除外）需使用 USB-C to USB-A 轉接器。

## 2. 分析目標硬體規格架構

### 2.1 GIGABYTE AI TOP ATOM 硬體規格

| 項目 | 規格 |
|---|---|
| 產品名稱 | GIGABYTE AI TOP ATOM（型號：ATAGB10-9000 / ATAGB10-9001） |
| 核心晶片 | NVIDIA GB10 Grace Blackwell Superchip（DGX Spark 平台） |
| CPU | 20-core Arm（10× Cortex-X925 + 10× Cortex-A725），ARMv9.2-A |
| GPU | NVIDIA Blackwell 架構，6144 CUDA 核心，第五代 Tensor Core，第四代 RT Core |
| AI 效能 | 最高 1 PetaFLOP（FP4, Sparse）/ 1000 TOPS，支援最高 2000 億參數模型 |
| 系統記憶體 | 128GB LPDDR5x 統一記憶體（256-bit，273 GB/s） |
| 儲存 | 最高 4TB M.2 NVMe SSD（ATAGB10-9000 為 PCIe Gen5 4TB；9001 為 Gen4 4TB） |
| USB | 4× USB 3.2 Gen 2×2 Type-C（20Gbps），其中 1 個為電源輸入（與 GB10 參考設計一致） |
| 顯示輸出 | 1× HDMI 2.1a（可經由 USB-C DP Alt Mode 擴充） |
| 有線網路 | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC |
| 無線網路 | Wi-Fi 7 + Bluetooth 5.4 |
| 作業系統 | NVIDIA DGX OS（基於 Ubuntu Linux，kernel 6.x） |
| 架構 | aarch64（ARM64） |
| 尺寸 | 150 × 150 × 50.5 mm（1.13L） |
| 重量 | 約 1.2 kg |
| 供電 | 240W USB-C 電源供應器 |
| 保固 | 1 年原廠保固 |

> 規格查核註記：尺寸 50.5mm / 重量 1.2kg 與 GIGABYTE 官方規格一致；藍牙版本依 GIGABYTE 官方規格頁為 **BT 5.4**（[官方規格頁](https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM/sp)）。USB 配置為 3 個資料埠 + 1 個供電埠（官方規格為 4× Type-C，其中 1 個 dedicated to system power）。

### 2.2 軟體環境：NVIDIA DGX OS

| 項目 | 內容 |
|---|---|
| 基礎 OS | Ubuntu Linux（NVIDIA 客製化） |
| Kernel | Linux 6.x |
| 架構 | aarch64（ARM64） |
| 預裝軟體 | NVIDIA AI 軟體堆疊（CUDA、cuDNN、TensorRT、PyTorch、Jupyter、Ollama 等）+ GIGABYTE AI TOP Utility |
| 套件管理 | apt |

### 2.3 與 DGX Spark 的差異

| 差異項 | AI TOP ATOM | NVIDIA DGX Spark |
|---|---|---|
| 機構設計 | GIGABYTE / AORUS 客製化機殼 | NVIDIA 參考機殼 |
| 品牌定位 | 個人 AI 超級電腦（桌面 / 辦公室） | 桌面 AI 開發參考平台 |
| 儲存 | 最高 4TB（Gen5 / Gen4 版本） | 最高 4TB |
| 配件 | GIGABYTE 原廠配件 + AI TOP Utility | NVIDIA 原廠配件 |
| 保固 | 1 年 | 依銷售通路 |

對 ALFA 相容性的影響：預期無影響（僅在 GX10 實測，其他 GB10 機型未逐台測試）。USB 控制器、kernel 版本、驅動框架均與 DGX Spark 完全相同。

### 2.4 USB Type-C 轉接需求

AI TOP ATOM 的 USB 埠均為 Type-C，ALFA 全系列網路卡（除 AXML 為 USB-C 外）均為 USB Type-A，需使用轉接器。建議選擇支援 USB 3.2 Gen 2×2（20Gbps）的轉接器，確保 AWUS036ACH / ACM / AX 等 USB 3.x 機型可發揮全速。

## 3. 分析目前 ALFA 網路卡規格和晶片組

截至 2026 年 9 月，ALFA Network 現役 USB 無線網路卡產品線如下：

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
| 桌面 AI 開發無線上網 | 9 款皆可（例如 AWUS036ACM / ACHM） | 全部為 kernel 內建驅動，插上即可用 |
| 無線滲透測試 / 安全研究 | AWUS036EACS / ACH / ACS | 注入實測 96–100%，可端到端擷取 WPA handshake；勿選 AXM / AXML（注入失敗） |
| Wi-Fi 6 + AP 熱點 | AWUS036AX / AXER | 2x2、80MHz AP 實測可用 |
| 6GHz 頻段 | AWUS036AXML | 實測可在 6GHz 建立 WPA3 AP；AXM 同晶片但 6GHz 未實測 |
| 不需要外接 WiFi | — | AI TOP ATOM 已內建 Wi-Fi 7，一般上網不需外接 |

## 5. 環境需求

### 5.1 硬體需求

| 項目 | 需求 |
|---|---|
| USB 轉接器 | USB-C to USB-A 轉接器或傳輸線（AXML 除外），建議支援 USB 3.2 Gen 2×2 |
| 供電 | GIGABYTE 原廠 240W USB-C 電源供應器 |

### 5.2 軟體需求

| 項目 | 需求 |
|---|---|
| DGX OS 版本 | 任意現役版本（kernel 6.x） |
| Kernel 版本 | kernel 6.17（實測 6.17.0-1014-nvidia）已內建全部 9 款網路卡的驅動，不需編譯工具；各卡最低版本不同（ACM／ACHM 4.19、AXM／AXML 5.18、EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），低於該版本才需安裝社群 DKMS 驅動 |
| 無線管理工具 | iw、network-manager（DGX OS 預設安裝） |

## 6. 相容性判定

### ALFA 現役機型 × GIGABYTE AI TOP ATOM（GB10）相容性矩陣

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

判定依據：2026-11-16～11-18 於 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）實機測試，測試對象為自有 Wi-Fi 與自有手機。GIGABYTE AI TOP ATOM 使用同一款 GB10 與 NVIDIA kernel 系列，預期行為相同，但僅在 GX10 實測，GIGABYTE AI TOP ATOM 未逐台測試。完整數據見 [ALFA 9 款網路卡 ARM64 實測總表](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 7. 超詳細 Step by Step 設定步驟

GIGABYTE AI TOP ATOM 的安裝步驟與 NVIDIA DGX Spark 預期相同（步驟在 GX10 實測）。以下為精簡版，完整步驟請參考 [ALFA 無線網路卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) 第 7 節。

### 7.1 MediaTek 晶片機型（AWUS036ACM / ACHM / AXM / AXML）

- 使用 USB-C to USB-A 轉接器（AXML 可直插），將 ALFA 網路卡插入 AI TOP ATOM 的 USB-C 資料埠
- 確認偵測：`lsusb`
- 確認介面：`ip link show`（應自動出現 wlx 開頭的介面）
- 連線 WiFi：`nmcli dev wifi connect "SSID" password "密碼"`

### 7.2 Realtek 晶片機型（AWUS036ACH / ACS / EACS / AX / AXER）

kernel 6.17（GX10 實測版本）已內建全部 Realtek 機型的驅動，步驟與 MediaTek 機型相同，不需編譯（最低版本：EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）：

```bash
# 1. 確認 kernel 版本 (6.17 以上即內建全部 Realtek 機型驅動; GX10 實測為 6.17.0-1014-nvidia)
uname -r

# 2. 插入網路卡後確認驅動已自動載入
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. 連線 WiFi
nmcli dev wifi connect "SSID" password "密碼"
```

各機型自動載入的模組：ACH → `rtw88_8812au`、ACS → `rtw88_8821au`、EACS → `rtw88_8821cu`、AX / AXER → `rtw89_8852bu`。若 `uname -r` 低於該卡的最低版本（舊版系統），才需要安裝社群維護的 DKMS 驅動（例如 RTL8812AU 的 morrownr/8812au-20210820）。

### 7.3 監聽模式（滲透測試）

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

## 8. 常見錯誤與排解

| 症狀 | 可能原因 | 排解方式 |
|---|---|---|
| lsusb 看不到 ALFA 網路卡 | USB-C 轉接器不良 / 僅充電規格 | 更換支援資料傳輸的 USB 3.2 Gen 2×2 轉接器；嘗試不同 USB-C 埠 |
| MediaTek 晶片無 wlan 介面 | module 未自動載入 / firmware 缺失 | `sudo modprobe mt76x2u`；`sudo apt install linux-firmware`；檢查 `dmesg \| grep mt76` |
| Realtek 卡插上後沒有 wlan 介面 | kernel 低於該卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17），未內建對應驅動 | 以 `uname -r` 確認版本；升級 kernel，或在舊 kernel 安裝社群 DKMS 驅動 |
| 反覆切換 monitor／AP 後掃不到任何訊號 | RX 停滯（RX stall） | 拔插網路卡讓 USB 重新列舉 |
| EACS／AXML 重插後沒有 wlx 介面 | 藍牙＋Wi-Fi 複合裝置 probe 卡住 | 換一個 USB 埠重插 |
| WiFi 速度慢 | 轉接器僅支援 USB 2.0 | 更換 USB 3.2 Gen 2×2 轉接器 |
| 內建 Wi-Fi 7 與外接衝突 | 路由衝突 | `sudo nmcli radio wifi off` 停用內建 WiFi 後再使用外接 |
| 6GHz 無法使用 | Regulatory Domain 限制 | `sudo iw reg set US`；確認最新法規 |
| 系統喚醒後網路卡消失 | USB 自動暫停 | `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. 已知限制

- USB Type-C 轉接需求：除 AXML 外，所有 ALFA 網路卡需 USB-C to USB-A 轉接器
- MT7921 機型注入失敗：AWUS036AXM / AXML 在 stock kernel 6.17 上封包注入失敗，無法 deauth 或擷取 handshake；monitor、AP、WPA3 可用。主因是 kernel 6.16 以後的 mac80211 chanctx 回歸，社群修補版驅動仍有速率限制
- 實測範圍：僅在 ASUS GX10（kernel 6.17.0-1014-nvidia）實測；GIGABYTE AI TOP ATOM 未逐台測試，預期行為相同
- hcxdumptool 不可用：除 EACS 在 2.4 GHz 外，其餘卡皆出現 `failed to arm`，請改用 airodump-ng + aireplay-ng
- 內建 Wi-Fi 7 可能與外接衝突：AI TOP ATOM 已內建 Wi-Fi 7 + BT 5.4
- AP 模式需手動設定：DGX OS 預設為開發環境
- 6GHz 法規限制：Wi-Fi 6E 可用性取決於法規區域
- 舊 kernel：kernel 低於該卡最低版本（EACS 6.2、ACH／ACS 6.13、AX／AXER 6.17）的系統，Realtek 機型才需社群 DKMS 驅動，且每次 kernel 更新後需重新編譯
- GIGABYTE 硬體差異不影響相容性：機構與散熱設計差異不影響 USB WiFi 驅動相容性
- 保固與技術支援：kernel 6.17 以上不需安裝第三方驅動；若在舊 kernel 安裝社群 DKMS 驅動，GIGABYTE 技術支援可能不涵蓋第三方驅動問題

反駁條件：以上判定以 DGX OS（Ubuntu 基底、kernel 6.x）為前提。GIGABYTE 若推出非 DGX OS 的自有韌體版本，判定需重新驗證；藍牙版本（5.4）以出貨批次規格為準，建議收貨後以官方頁面覆核。

## 10. 參考來源 URL

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| GIGABYTE AI TOP ATOM 官方產品頁 | AI TOP ATOM 硬體規格（ATAGB10-9000） | https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 已查核 | 2026-09-03 |
| GIGABYTE AI TOP ATOM 官方頁（簡中映像站） | 產品特色與規格 | https://www.gigabyte.cn/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ 已查核 | 2026-09-03 |
| GIGABYTE AI TOP ATOM Review（LinuxGizmos） | 第三方評測與規格確認（50.5mm） | https://linuxgizmos.com/gigabyte-ai-top-atom-introduces-nvidia-grace-blackwell-gb10-performance-for-the-desktop/ | ✅ 已查核 | 2026-09-03 |
| NVIDIA DGX Spark 官方頁面 | GB10 平台資訊 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ 已查核 | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux 驅動 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| ALFA 9 款網路卡 ARM64 實測總表（Yopitek） | ASUS GX10 + Ubuntu 24.04 ARM64 實機測試 | https://yupitek.com/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ 實測 | 2026-11-18 |
| ALFA Network 產品總覽（Yopitek） | ALFA 現役產品規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |

相關文章：[ALFA 無線網路卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 無線網路卡是否支援 ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[ALFA 無線網路卡是否支援 ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[ALFA 無線網路卡是否支援 MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

免責聲明：本文相容性判定以 2026-11 在 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17.0-1014-nvidia）的實機測試為基準。GIGABYTE AI TOP ATOM 與 GX10 使用同一款 GB10 與 NVIDIA kernel 系列，預期行為相同，但未逐台測試。GX10 實測的 kernel 6.17 已內建 ALFA 9 款網路卡的驅動（各卡最低版本不同），kernel 低於該卡最低版本時才需社群 DKMS 驅動。AI TOP ATOM 已內建 Wi-Fi 7，外接 ALFA 主要用於滲透測試或特殊晶片組需求。監聽與注入僅限在自有或已取得授權的網路進行。
