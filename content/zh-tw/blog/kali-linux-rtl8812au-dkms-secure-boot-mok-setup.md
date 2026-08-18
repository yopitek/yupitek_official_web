---
title: "Kali Linux 核心更新後網卡罷工？RTL8812AU 驅動 DKMS 編譯失敗與 Secure Boot 排障"
date: 2026-08-18
draft: false
slug: "kali-linux-rtl8812au-dkms-secure-boot-mok-setup"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "詳解 Kali Linux 核心升級時 RTL8812AU 驅動失效成因，提供穩定社群驅動安裝步驟與 Secure Boot 開啟下的 MOK 模組簽署排障教學。"
featureimage: "/images/blog/05_dkms_mok_flow_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "遇到 Secure Boot 阻擋未簽署驅動時，應該關閉 Secure Boot 嗎？"
    answer: "不建議。安全作法是透過 mokutil 匯入自簽金鑰（MOK 機制），在維持系統安全防護的同時完成模組載入。"
---

![Linux Kernel DKMS and Secure Boot MOK Flowchart](/images/blog/05_dkms_mok_flow_blueprint.jpg)

> **適用硬體**：ALFA AWUS036ACH（Realtek RTL8812AU）/ ALFA AWUS1900（Realtek RTL8814AU）
> **適用平台**：Kali Linux、Debian／Ubuntu 等 Debian 系發行版（Linux x86_64／ARM64）
> **不支援**：macOS（含 Apple Silicon）——詳見下方「相容性與平台紅線」。

---

## TL;DR

AWUS036ACH 與 AWUS1900 使用的是 **非核心內建（out-of-tree）** 的 Realtek 驅動。執行 `apt upgrade` 升級核心（Kernel）後，舊模組因為核心 ABI 已變更而失效，這**不是網卡壞掉，而是驅動模組需要重新編譯**。

解法是安裝社群維護的 `aircrack-ng/rtl8812au`（或是 `morrownr/8814au`）驅動，並透過 **DKMS** 讓它在新核心安裝時自動重新編譯。如果系統開啟 **Secure Boot**，核心會拒絕載入未簽署的自訂模組，此時必須透過 **MOK（Machine Owner Key）金鑰簽署**機制匯入您的自簽金鑰——**請不要關閉 Secure Boot**。

---

## 為什麼每次 `apt upgrade` 之後網卡就罷工？

### 問題根源：核心 ABI 與 out-of-tree 模組

Linux 的硬體驅動程式多以「**核心模組（Kernel Module）**」的形式存在，副檔名通常是 `.ko`。常見的兩種類型：

| 類型 | 說明 | 核心更新後行為 |
|------|------|--------------|
| **In-tree（核心內建）** | 驅動原始碼直接收錄在 Linux Kernel 原始碼樹，例如 `mt7921u`、`mt76x2u` | 隨核心一起編譯，更新後自動可用，**不需任何手動處理** |
| **Out-of-tree（核心外掛）** | 驅動原始碼在核心樹之外，例如 Realtek `rtl8812au` | 只針對「當時的核心版本」編譯，新核心 ABI 變更後**模組失效** |

AWUS036ACH 的 `RTL8812AU` 與 AWUS1900 的 `RTL8814AU` 都屬於 out-of-tree。Linux 對模組與核心之間的相容性（Kernel ABI / vermagic）要求嚴格，模組必須與**目前執行中的核心版本完全一致**（含 `uname -r` 的完整版本字串）才允許載入。

當您執行：

```bash
sudo apt update && sudo apt upgrade -y
```

系統若更新了 `linux-image-*`（核心映像檔），重開機後執行的就是新核心；而舊核心時期編譯的 `88XXau.ko` 模組無法載入到新核心，於是發生「網卡插上去，系統卻完全抓不到」。

### 症狀快速辨識

| 症狀 | 典型原因 |
|------|---------|
| `lsusb` 看得到網卡，但 `ip link` 沒有 `wlan` 介面 | **驅動模組沒有被載入**（最常見） |
| `sudo modprobe 88XXau` 回傳錯誤 | 模組與目前核心不相容或根本不存在 |
| `dmesg` 出現 `Required key not available` | **Secure Boot 沒有簽署**（見第五章） |
| `dmesg` 出現 `Module 88XXau was not signed` 或 `signature` | Secure Boot 簽章驗證失敗 |
| 編譯時出現 `Bad return status for module build` | 缺少或版本不符的 `linux-headers`（見第四章） |

> **判斷口訣**：先看 `lsusb` 確認硬體被 USB 層抓到 → 再看 `dmesg` 確認驅動層為什麼載入失敗。兩者分開診斷，才不會誤判成硬體故障。

---

## 動手前先檢查：你真的需要社群驅動嗎？

### 1. 核心 6.14+ 先試內建支援

自 **Linux 6.14** 起，`rtl8812au` 系列已有以 `mac80211` 為基礎的核心內建驅動加入主線（`lwfinger/rtw88` 生態系）。若您的核心是 6.14 或更新版本，**優先試試內建驅動**：

```bash
# 先確認核心版本
uname -r

# 檢查內建模組是否已存在
lsmod | grep 88XXau
lsmod | grep rtw

# 直接插入網卡後確認介面
ip link
```

如果內建驅動就能抓到介面，您**不需要**任何 DKMS 編譯步驟。不過要注意：對資安研究而言，**完整的監聽模式（Monitor Mode）與封包注入（Packet Injection）支援**，社群驅動仍然是最成熟、最穩定的選擇——這是很多人仍選擇編譯 `rtl8812au` 社群驅動的原因。

### 2. 確認晶片與 USB ID

在動手前先確認您手上的型號與晶片對應：

| 型號 | 晶片 | USB Vendor:Product | MIMO | 頻段與速率 |
|------|------|--------------------|------|-----------|
| **ALFA AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | 2×2 | 2.4 GHz 300 Mbps ＋ 5 GHz 867 Mbps（AC1200） |
| **ALFA AWUS1900** | Realtek RTL8814AU | `0bda:8813` | 4×4 | 2.4 GHz 600 Mbps ＋ 5 GHz 1300 Mbps（AC1900） |

```bash
lsusb
# 預期看到：
# Bus ... Device ...: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...
# 或
# Bus ... Device ...: ID 0bda:8813 Realtek Semiconductor Corp. RTL8814AU ...
```

> 晶片與型號對錯，之後選錯驅動會編到懷疑人生——下載驅動前**務必先跑一次 `lsusb`**。

---

## 移除舊驅動：從乾淨環境開始

編譯新的社群驅動前，先把系統裡既有的舊版 Realtek 驅動清乾淨，避免「兩個驅動打架」導致介面名稱混亂或載入衝突。

### 方式一：透過 DKMS 卸載

如果您或先前安裝流程有用 DKMS，進到原始碼目錄執行官方移除指令：

```bash
cd rtl8812au          # 換成你之前 clone 的驅動目錄
sudo make dkms_remove
```

### 方式二：直接用 dkms 指令移除

不知道原始碼在哪也沒關係，直接用 `dkms` 列出並移除：

```bash
sudo dkms status
# 例如輸出：
# 8812au/5.6.4.2, 6.1.0-kali9-amd64, x86_64: installed

# 移除該版本的所有核心建置
sudo dkms remove 8812au/5.6.4.2 --all
```

### 方式三：把模組從核心模組目錄中移除

如果以前是用 `make install` 直接安裝（沒有 DKMS）：

```bash
# 找出殘留的模組檔
find /lib/modules -name "*88XXau*" 2>/dev/null

# 手動刪除（請依實際路徑）
sudo rm -f /lib/modules/$(uname -r)/kernel/drivers/net/wireless/rtl8812au/88XXau.ko
sudo depmod -a
sudo modprobe -r 88XXau 2>/dev/null
```

**驗證已清乾淨：**

```bash
sudo dkms status        # 應無 8812au / 8814au 相關項目
lsmod | grep 88XXau     # 應無輸出
```

---

## 用 DKMS 安裝最穩定的社群驅動

### 為什麼要用 DKMS？

DKMS（Dynamic Kernel Module Support）的核心價值：當您**之後再次升級核心**時，DKMS 會在新核心安裝完成後**自動重新編譯並安裝**驅動模組。這正是解決開頭「每次 `apt upgrade` 網卡就罷工」的根本辦法——一次設定，之後終生自動重建。

### 1. 安裝編譯相依套件

```bash
sudo apt update
sudo apt install bc mokutil build-essential libelf-dev linux-headers-$(uname -r) dkms
```

> **重點**：`linux-headers-$(uname -r)` 的版本**必須與目前執行的核心完全一致**。只要是版本對不上，編譯 100% 會失敗並回報 `Bad return status for module build`。

如果編譯時才想到要補 headers，可以先確認：

```bash
dpkg -l | grep linux-headers
# 確認裡面有 linux-headers-$(uname -r) 對應的版本
```

### 2. 抓取並用 DKMS 安裝驅動

**AVUS036ACH（RTL8812AU）** 請使用 aircrack-ng 社群長期維護的儲存庫（同時也支援 RTL8814AU）：

```bash
git clone -b v5.6.4.2 https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**AWUS1900（RTL8814AU）** 若您想抓專門為 8814 優化的維護版本，可使用 morrownr 的儲存庫：

```bash
git clone https://github.com/morrownr/8814au.git
cd 8814au
sudo make dkms_install
```

> 以 `-b v5.6.4.2` 固定版本可以避免「最新 master 與特定核心不相容」的風險，這是社群實務上最穩定的做法。安裝完成後**重開機一次**，讓新核心最乾淨的狀態重新載入。

### 3. 驗證驅動已載入

```bash
lsusb                              # 仍須看到 0bda:8812 或 0bda:8813
sudo modprobe 88XXau               # 手動載入（若未自動載入）
lsmod | grep 88XXau                # 應列出 88XXau
ip link                            # 應出現 wlan0 / wlan1 等無線介面
sudo dkms status                   # 應顯示 installed
```

若介面被命名成 `wlx...`，那是 NetworkManager 的 predictible naming 正常行為，不影響使用。

---

## 啟用監聽模式（Monitor Mode）與封包注入測試

這個網卡被拿來做資安研究的核心原因，就是監聽模式與封包注入。在確認驅動載入、介面出現後，可以用標準流程驗證：

```bash
# 1. 關閉會干擾監聽的網路服務
sudo airmon-ng check kill

# 2. 把介面（以 wlan1 為例）切換到監聽模式
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# 3. 確認已進入 monitor 模式
iwconfig
# wlan1   IEEE 802.11 ... Mode:Monitor ...

# 4. 封包注入測試
sudo aireplay-ng --test wlan1
# 預期看到：Injection is working!
```

> **合法性提醒**：Monitor Mode 與封包注入僅限用於**您擁有或已獲明確授權**的網路環境（自家實驗室、教學課程、企業委託的滲透測試）。請遵守當地法規，並只對授權目標操作。

---

## Secure Boot 下的安全排障：MOK 金鑰簽署

### 為什麼核心會拒絕載入自訂模組？

現代的 Ubuntu／Kali 安裝預設啟用 **UEFI Secure Boot**。這是 UEFI 韌體與核心共同建立的一道**開機鏈信任防線**：核心只會載入**經過信任金鑰簽署**的模組。發行版官方模組由發行版的簽署金鑰簽署；而您**自己編譯的 DKMS 模組**沒有這個簽章，因此核心會拒絕載入並回報 `Required key not available`。

**正確且安全的解法**，是讓您的機器「信任您自己的金鑰」——也就是把您這台機器產生的公鑰，註冊為 **MOK（Machine Owner Key，機器擁有者金鑰）**。這完全是自行掌控、不需要關閉任何安全防護的做法。

> ⚠️ **安全紅線**：請**不要**為了讓驅動載入而關閉 Secure Boot。Secure Boot 是系統啟動鏈的重要防護，關閉它等同於降低整台機器對 rootkit 與開機層攻擊的防禦。透過 MOK 簽署即可安全載入驅動，不需要付出這個代價。

### MOK 運作原理（白話版）

```
您編譯出的模組（88XXau.ko）
        │  以「機器本金鑰」簽署（private key / mok.key）
        ▼
核心載入前檢查簽章
        │  用「MOK 公鑰」（mok.pub）驗證
        ▼
核心信任此金鑰？（已在 UEFI MOK 清單中？）
   │是                     │否
   ▼                       ▼
載入成功 ✅         拒絕載入：Required key not available ❌
```

### 1. 檢查 DKMS 的簽署金鑰是否已自動產生

在 Ubuntu／Kali 這類發行版，啟用 Secure Boot 時，**DKMS 會在第一次編譯時自動產生一對簽署金鑰**：

```bash
ls -l /var/lib/dkms/mok.key /var/lib/dkms/mok.pub
# mok.key  = 私鑰（本機簽署用，切勿外流）
# mok.pub  = 公鑰（匯入 UEFI 用）
```

> 若這兩個檔案不存在，代表您的 DKMS 版本較舊或 Secure Boot 偵測未正確觸發。先執行一次 `sudo dkms autoinstall` 讓它產生；若仍無，再回來確認 Secure Boot 狀態。

### 2. 匯入 MOK 公鑰（mokutil --import）

```bash
sudo mokutil --import /var/lib/dkms/mok.pub
```

執行後系統會請您**設定一組一次性密碼（One-time password）**。這組密碼只在下一次重新啟動、於 UEFI 的 MOK 管理畫面中使用，**請務必記住**。

確認匯入已排入佇列：

```bash
sudo mokutil --list-new
# 應列出 /var/lib/dkms/mok.pub
```

### 3. 重新啟動，進入 MOK 管理畫面完成註冊

1. 重新開機。
2. 開機過程中會出現 **MOK Management（藍底白字的 UEFI 管理畫面）**。
3. 依序操作：
   - 選擇 **Enroll MOK** → **Continue** → **Yes**
   - 輸入您在第 2 步設定的**一次性密碼**
   - 選擇 **Reboot** 完成註冊並重新開機。

> **小提醒**：如果沒看到 MOK 管理畫面，通常是因為您的裝置是透過 `shim` 開機才不會顯示；請確認開機載入器（如 GRUB）是透過 shim 被簽署的，一般 Ubuntu／Kali 預設即是如此。

### 4. 驗證 MOK 已生效

```bash
# 檢查 MOK 公鑰是否已被核心信任
sudo mokutil --test-key /var/lib/dkms/mok.pub

# 查看核心憑證鏈（應能看到 MOK 相關項目）
sudo dmesg | grep -i cert

# 現在重新載入模組
sudo modprobe 88XXau
lsmod | grep 88XXau
```

若 `dmesg` 不再出現 `Required key not available`，且 `88XXau` 成功載入，您的驅動就在 Secure Boot 開啟的狀態下正常運作了。

### 常見簽署錯誤對照表

| `dmesg` 訊息 | 原因 | 正確做法 |
|-------------|------|---------|
| `Required key not available` | 模組未簽署，或 MOK 尚未註冊 | 完成 `mokutil --import` ＋ MOK 註冊流程（本節步驟 2–3） |
| `Module XXX was not signed` | Secure Boot 開啟但 DKMS 未簽署 | 確認 `/var/lib/dkms/mok.key` 存在並重新 `sudo dkms autoinstall` |
| `Bad return status for module build` | headers 缺失或與核心不符 | `apt install linux-headers-$(uname -r)` 後重編 |
| `disagrees about version of symbol` | 模組與目前核心版本不同步 | 重新 `sudo make dkms_install`，勿跨版本混用 |

---

## 採購前相容性確認工作表

> 如果您正在評估要不要購入 AWUS036ACH / AWUS1900，請先逐項核對下列清單，避免買回家才發現環境不符——這份表格同時也是日後開技術支援單時的自助檢查表。

| # | 檢查項目 | 通過條件 | 過不了怎麼辦 |
|---|---------|---------|------------|
| 1 | 作業系統 | Linux（Kali / Debian / Ubuntu） | **macOS 不使用此二型號**（見下方紅線） |
| 2 | 核心版本 | 已知版本並有對應 headers | 手動編譯前先 `lsusb` 確認晶片 |
| 3 | 是否有編譯環境 | 可執行 `gcc`、`make`、`dkms` | `apt install build-essential dkms` |
| 4 | Secure Boot 狀態 | 已知是否開啟 | `mokutil --sb-state` 查詢 |
| 5 | USB 供電 | 直插主機板 USB 3.0 或**有供電的 USB Hub** | 高功率網卡需穩定供電（ACH 最高 0.7A@5V） |
| 6 | 需要監聽／注入？ | 是→社群驅動 DKMS；否→可考慮核心 ≥6.14 內建 | 見第二章 |

### 平台紅線（Support Boundary）

| 平台 | 支援狀態 | 說明 |
|------|---------|------|
| Kali Linux / Debian / Ubuntu | ✅ 支援 | 需 DKMS 編譯社群驅動 |
| Raspberry Pi 3B+ / 4 / 5（Linux） | ✅ 支援 | 建議 2.5A–3A 電源，避免注入時壓降掉卡 |
| **macOS（Intel）** | ⚠️ 最高 10.15 Catalina，且需舊驅動 | 不建議，官方已停止支援 |
| **macOS（Apple Silicon M1/M2/M3/M4）** | ❌ **不支援** | 無可用驅動，請改用原生核心支援的 MediaTek 型號（如 AWUS036AXML） |
| Windows 10 / 11 | ✅ 支援 | 使用 Realtek 官方驅動 |

---

## 常見問題（FAQ）

**Q1：為什麼我每次升級核心，網卡就失靈，難道是硬體壞了？**
不是。RTL8812AU/RTL8814AU 的驅動是 out-of-tree（核心外掛），它只針對「安裝時的特定核心版本」編譯。核心更新後舊模組與新核心不相容，系統就載入失敗。**用 DKMS 安裝後，之後的核心更新會自動重建模組，問題就不再出現。**

**Q2：Secure Boot 開著，會不會永遠灌不了這個驅動？**
不會。只要透過 MOK 機制把機器自己的公鑰（`/var/lib/dkms/mok.pub`）註冊為信任金鑰，DKMS 重新編譯後會自動用 `mok.key` 簽署模組，核心即可載入。這完全不需要關閉 Secure Boot。

**Q3：`aircrack-ng/rtl8812au` 和 `morrownr` 的儲存庫差在哪？怎麼選？**
`aircrack-ng/rtl8812au` 是 aircrack-ng 社群長期維護、被 Kali 官方文件引用最廣的版本，支援 RTL8812AU 與 RTL8814AU；`morrownr/8814au` 則是專門為 RTL8814AU（AWUS1900）優化的維護分支。**AWUS036ACH 建議用 `aircrack-ng/rtl8812au`（固定 `v5.6.4.2`），AWUS1900 可用 `aircrack-ng` 或 `morrownr/8814au`**。兩者皆是 DKMS 安裝、日後自動重建，功能與穩定性都在業界水準之上。

**Q4：我看到有人說直接關掉 Secure Boot 最省事，我可以做嗎？**
**不建議。** Secure Boot 是開機鏈的信任根基，關閉會讓整台機器暴露在針對開機程序與 rootkit 的攻擊風險中。用 MOK 簽署只花您一次重新開機的時間，就能在保留防護的前提下載入驅動——**安全做法才值得複製到工作機上**。

**Q5：核心升級後，DKMS 到底要不要我再去手動跑一次？**
一般**不需要**。DKMS 安裝後，系統每當安裝新核心，都會自動觸發重新編譯您的模組。您只需要在升級後重開機；萬一看到編譯失敗訊息，優先檢查 `linux-headers-$(uname -r)` 是否已同步更新即可。

**Q6：Raspberry Pi 上插入後頻繁斷線或注入到一半掉卡，是驅動問題嗎？**
多半是**供電不足**。這兩款高功率網卡在封包注入時瞬間電流較高（AWUS036ACH 最高約 0.7A@5V），Pi 的 USB 電源若不足會直接掉卡。請改用 **2.5A–3A 的電源供應器**或**有獨立供電的 USB Hub**，並可加入 `options 88XXau rtw_power_mgnt=0 rtw_enusbss=0` 關閉 USB 省電，避免動態省電干擾注入。

---

## 結論

Kali Linux 核心更新後網卡「罷工」是 out-of-tree 驅動最典型的宿命，**不是硬體故障，也不是系統中毒**。只要掌握三件事就能根治：

1. **認清根源**——RTL8812AU/RTL8814AU 需要為每個核心版本重新編譯，內建驅動（核心 ≥6.14）或原生核心支援型號（如 MediaTek MT7921AU）可省去大部分編譯麻煩。
2. **用 DKMS 一勞永逸**——`sudo make dkms_install` 之後，未來核心升級會自動重建模組，不再需要每次手動處理。
3. **Secure Boot 不是障礙**——透過 MOK 金鑰簽署（`mokutil --import /var/lib/dkms/mok.pub` ＋ UEFI 註冊）即可安全載入自訂模組，全程不需關閉任何安全防護。

如果您正在採購，AWUS036ACH（RTL8812AU）與 AWUS1900（RTL8814AU）都是 Linux 資安社群高度驗證的選擇；而若您希望**隨插即用、零編譯**，可參考原生核心支援的 MediaTek 系列型號。動手之前，記得先跑完「採購前相容性確認工作表」，並確認您使用網卡的目的符合法規與授權範圍。

---

## 參考資源

| 資源 | 連結 |
|------|------|
| aircrack-ng RTL8812AU 社群驅動（含 RTL8814AU） | https://github.com/aircrack-ng/rtl8812au |
| morrownr RTL8814AU 驅動（AWUS1900） | https://github.com/morrownr/8814au |
| morrownr USB-WiFi 情境指南（含 MOK 說明） | https://github.com/morrownr/USB-WiFi |
| Linux 核心內建 RTL8xxx（rtw88/mac80211 生態系） | https://github.com/lwfinger/rtw88 |
| ALFA AWUS036ACH 官方產品頁 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036ACH 官方文件 | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Ubuntu Secure Boot 簽署 DKMS 模組指引 | https://ubuntu.com/ 搜尋「dkms secure boot mok」 |
| Yupitek 技術支援 | https://yupitek.com/ |

> **合法使用聲明**：本文所述之監聽模式、封包注入等操作，僅限於您擁有或已獲得明確授權之網路環境。使用者須自行遵守所在地法律規範，並確保所有測試皆有合法授權依據。
