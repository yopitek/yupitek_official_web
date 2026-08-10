---
title: "ALFA AWUS036AXML 安裝教學：Wi-Fi 6E 網卡在 Kali Linux 上的監聽模式與封包注入實測"
locale: "zh-TW"
hreflang_group: "awus036axml-wifi6e-kali-linux-setup"
description: "ALFA AWUS036AXML（MT7921AUN 晶片）在 Kali Linux 上的安裝教學：內建 mt7921u 驅動、kernel 版本條件、監聽模式、封包注入實測與常見排錯。"
date: 2026-08-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-wifi6e-kali-linux-setup"
tags: ["Fi 6E 網卡在 Kali Linux 上的監聽模式與封包注入實測", "TW", "wifi6e-kali-linux-setup", "wifi6e-kali-linux-setup", "08-10", "AWUS036AXML", "Kali Linux", "Fi 6E 監聽模式與封包注入教學｜Yupitek"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-08-10
---


# ALFA AWUS036AXML 安裝教學：Wi-Fi 6E 網卡在 Kali Linux 上的監聽模式與封包注入實測

> TL;DR：ALFA AWUS036AXML 搭載 MediaTek MT7921AUN 晶片，在 Kali Linux（kernel 5.18+）使用**內建 `mt7921u` 驅動即可運作**，不需要另外編譯驅動；若要做穩定的 active monitor mode / 封包注入，建議 kernel 6.12+ 與附電源的 USB Hub。插入後 `lsusb` 應看到 `0e8d:7961`，接著用 `airmon-ng` 或 `iw` 切換監聽模式即可。

## 為什麼 Wi-Fi 6E 網卡開始被滲透測試關注？

Wi-Fi 6E 新增的 **6 GHz 頻段**（5925–7125 MHz）是近年企業無線網路升級的重點：新世代 AP、高密度會議室、工廠物聯網都開始部署 6 GHz。對資安稽核人員來說，如果稽核對象的環境已導入 6 GHz，你的測試網卡**必須能聽得到這個頻段**——否則稽核範圍直接少了一大塊。

AWUS036AXML 是 ALFA Network 推出的 Wi-Fi 6E USB 網卡，支援 2.4 / 5 / 6 GHz 三頻，與前一代熱門的 AWUS036ACH（RTL8812AU，僅 2.4/5 GHz）相比，最大差異就是補上了 6 GHz 監聽能力。如果你已熟悉 AWUS036ACH 的流程，這篇的步驟會非常親切。

## AWUS036AXML 規格與版本條件

| 項目 | AWUS036AXML | AWUS036ACH（對照） | AWUS036ACM（對照） |
|---|---|---|---|
| 晶片組 | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| 頻段 | 2.4 / 5 / 6 GHz（Wi-Fi 6E） | 2.4 / 5 GHz | 2.4 / 5 GHz |
| Linux 驅動 | `mt7921u`（**核心內建**） | `88XXau`（需自行編譯/DKMS） | `mt76`（核心內建） |
| 建議 kernel | ≥ 5.18（6 GHz 支援） | 5.x（較舊亦可） | 5.x |
| active monitor mode | 建議 kernel ≥ 6.12 | 通用 | 通用 |
| USB ID（lsusb） | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| 功耗 | 約 2.7 W（建議附電源 Hub） | 較低 | 較低 |
| 封包注入 | 支援（建議實測） | 支援 | 支援 |

> 版本條件說明：`mt7921u` 自 kernel 5.18 起進入主線，6 GHz 頻段支援隨核心逐步補齊；**active monitor mode（主動式監聽）建議 kernel 6.12+**。Kali 2026 預設核心已是 6.14 等級，直接符合條件。

## 事前準備

1. **Kali Linux 2024.x 以上**（建議更新到最新：`sudo apt update && sudo apt full-upgrade -y`）。
2. 確認核心版本：`uname -r`，若低於 5.18 請先升級系統。
3. 一張可用的 USB 3.0 連接埠；若接在樹莓派或 USB Hub 上，**建議用附電源 Hub**（AWUS036AXML 功耗約 2.7 W，供電不足會出現「插了卻抓不到」）。
4. 合法測試權限：本教學所有指令僅限用於你擁有或獲得授權的網路環境。

## 步驟 1：連接網卡並確認系統抓到

插入網卡後，用 `lsusb` 確認裝置是否被識別：

```bash
lsusb
```

預期輸出中應有：

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` 就是 MT7921AUN 的 USB ID。若看不到，先检查供電（換 USB 埠或加供電 Hub）再試。

確認驅動有載入：

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

Kali 2026 預設核心內含 `mt7921u`，正常情況下插上即載入，**不需要下載或編譯任何驅動**——這與 AWUS036ACH（RTL8812AU 需手動裝 `88XXau`）是最大差別。

## 步驟 2：確認無線介面

```bash
ip link show
# 或
iwconfig
```

應看到新的無線介面，通常是 `wlan0` 或 `wlan1`（取決於系統既有介面數量）。以下範例以 `wlan1` 為準，請依實際名稱替換。

## 步驟 3：啟用監聽模式

### 方法一：airmon-ng（推薦）

```bash
# 終止可能干擾的服務
sudo airmon-ng check kill

# 啟用監聽模式（wlan1 換成你的介面名稱）
sudo airmon-ng start wlan1
```

成功後會看到 `wlan1mon` 虛擬介面。

### 方法二：iw（精簡控制）

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

此方法直接改現有介面，不會建立 `wlan1mon`。

## 步驟 4：確認監聽模式已啟用

```bash
iwconfig
```

關鍵欄位應為 `Mode:Monitor`：

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

也可以用 `iw dev` 確認 `type monitor`。接著用 `airodump-ng` 做端到端測試：

```bash
sudo airodump-ng wlan1mon
```

若能看到周邊 BSSID 清單（含頻道、訊號強度、加密類型），代表監聽模式正常。**掃描 6 GHz 頻段**：

```bash
sudo airodump-ng --band 6g wlan1mon
```

> 注意：6 GHz 掃描需要你的網卡驅動/核心支援該頻段（kernel 6.12+ 較穩）；若 `--band 6g` 不支援，先掃 5 GHz（`--band a`）確認基本功能，再更新核心後重試。

## 步驟 5：封包注入測試

```bash
sudo aireplay-ng --test wlan1mon
```

預期輸出關鍵行：

```text
Injection is working!
```

成功率 80% 以上代表運作可靠；若低於 50%，檢查天線方向、USB 供電，或改用 USB 3.0 直連埠。

## 樹莓派補充：可攜式 Wi-Fi 稽核平台

AWUS036AXML 也支援 Raspberry Pi 3B+ / 4 / 5（官方產品頁列出），適合組成可攜稽核工具組。重點提醒：

- **供電**：Pi 的 USB 供電較緊，建議用附電源 USB Hub，避免「偶爾抓不到」。
- **系統**：Kali ARM64 官方映像（Raspberry Pi 版）即可，安裝後同樣是內建 `mt7921u`。
- **驗證**：`lsusb` 看到 `0e8d:7961`、`lsmod | grep mt7921` 有輸出，就代表平台就緒。

## 常見排錯

**Q：`lsusb` 看不到 `0e8d:7961` 怎麼辦？**
99% 是供電不足或連接鬆動。換一個 USB 3.0 直連埠；若接 Hub，改接附電源 Hub；再不行換一條短一點的 USB 線。

**Q：啟用監聽模式後介面自動跳回 managed？**
通常是 NetworkManager / wpa_supplicant 在背景搶回控制權。重跑 `sudo airmon-ng check kill`，或手動 `sudo systemctl stop NetworkManager wpa_supplicant`。

**Q：`iwconfig` 顯示 `Mode:Managed` 或介面消失？**
驅動可能未被正確載入或核心太舊。先 `lsmod | grep mt7921` 確認模組，再 `uname -r` 確認 kernel ≥ 5.18。

**Q：6 GHz 掃不到任何網路？**
先確認 `iw dev wlan1mon info` 支援的頻段；6 GHz 環境本身較少（新部署），且台灣 6 GHz 執照頻段開放進度請依 NCC 公告為準。也可以先用 2.4/5 GHz 驗證網卡功能正常。

**Q：跟 AWUS036ACH 比，該買哪張？**
稽核對象已有 6 GHz 環境 → 選 AWUS036AXML；只需要 2.4/5 GHz 且預算優先 → AWUS036ACH 仍是非常成熟的選擇。兩者都在 Kali 上可用，差異在頻段涵蓋與驅動安裝方式（AXML 內建免編譯）。

## 常見問題（FAQ）

**Q1：AWUS036AXML 在 Kali Linux 需要另外裝驅動嗎？**
不需要。它使用核心內建的 `mt7921u` 驅動（kernel 5.18+），插入即用；不需要像 AWUS036ACH 那樣編譯 DKMS 驅動。

**Q2：AWUS036AXML 支援監聽模式嗎？**
支援。用 `airmon-ng` 或 `iw` 即可啟用；要做 active monitor mode（如 deauth 相關測試）建議 kernel 6.12+。

**Q3：Wi-Fi 6E 的 6 GHz 頻段在台灣能用於稽核嗎？**
6 GHz 屬於受監管頻段，使用前請確認 NCC 對 6 GHz 頻段的開放進度與授權規定，並僅測試自己有權限的環境。

**Q4：接在樹莓派上抓不到網卡怎麼辦？**
優先檢查供電——AWUS036AXML 功耗約 2.7 W，建議用附電源 USB Hub，並使用品質好的 USB 線。

**Q5：AWUS036AXML 跟 AWUS036ACH 差在哪？**
AXML 是 Wi-Fi 6E（多了 6 GHz）且驅動核心內建；ACH 是雙頻（2.4/5 GHz）、RTL8812AU 需手動裝驅動。兩者都是 Kali 上成熟的稽核網卡。

## 總結

AWUS036AXML 的安裝流程比你想像的簡單：**核心 5.18+ → 插入即用（`mt7921u`）→ 確認 `0e8d:7961` → airmon-ng 切監聽 → aireplay-ng 驗證注入**。它與 AWUS036ACH 的差異核心在於 6 GHz 頻段與免編譯驅動——如果你的稽核範圍已進入 Wi-Fi 6E 世代，這張卡是補齊頻段覆蓋的選擇。記得所有測試只在合法授權環境進行。

ALFA Network 系列網卡由 Yupitek（榆閤科技）在台灣提供銷售與技術支援；需要 AWUS036AXML 或搭配的供電 Hub、天線，歡迎來信 [sales@yupitek.com](mailto:sales@yupitek.com)。