---
title: "ALFA 介面卡 USB 直通：VirtualBox 與 VMware 設定指南"
description: "逐步教學：在 VirtualBox 和 VMware Workstation 上設定 ALFA USB WiFi 介面卡的 USB 直通，適用於 Kali Linux。涵蓋 AWUS036ACH、AWUS036AXML、USB 3.0 篩選器、Extension Pack 及疑難排解。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
---

在虛擬機器內執行 ALFA WiFi 介面卡並不像插上後等待客端作業系統自動偵測那麼簡單。與共用資料夾或橋接網路不同，監聽模式（monitor mode）和原始封包注入（packet injection）需要**完整的 USB 控制權**——虛擬機器必須獨佔 USB 裝置，而不是透過主機的網路堆疊共用。這稱為 USB 直通（USB passthrough），正確設定是在 VM 環境中工作的滲透測試人員和 CTF 玩家最常遇到的設定失敗原因。

本指南涵蓋 **VirtualBox 7.x** 和 **VMware Workstation 17+ / VMware Fusion 13+** 的完整直通設定，以 Kali Linux 作為客端作業系統。文中針對 AWUS036ACH（RTL8812AU 晶片組）和較新的 AWUS036AXML（MT7921AU 晶片組）分別說明行為差異。

完成後，您的 ALFA 介面卡將在 Kali 中透過 `lsusb` 顯示，正確驅動程式已載入，且 `airmon-ng` 確認監聽模式正常運作。

---

## 前置需求

開始之前，請確認您的環境符合以下要求。缺少任何一項——尤其是 VirtualBox Extension Pack——是大多數直通失敗的根本原因。

| 需求 | 詳細說明 |
|---|---|
| **Hypervisor** | VirtualBox 7.x + Extension Pack **或** VMware Workstation 17+ / Fusion 13+ |
| **客端作業系統** | Kali Linux 2024.x 或更新版本（已在 2024.1–2025.1 測試） |
| **ALFA 介面卡** | AWUS036ACH、AWUS036AXML、AWUS036ACM，或任何 RTL8812AU / MT7921AU 裝置 |
| **主機 USB 埠** | 建議使用 USB 3.0（尤其是 AWUS036AXML） |
| **主機作業系統** | Windows 10/11、Linux 或 macOS（Fusion） |
| **Sudo 權限** | Kali VM 內部需要 |

{{< alert "circle-info" >}}
若您尚未在 Kali 內安裝驅動程式，請先完成本指南的 USB 直通步驟。介面卡在 VM 中可見後，再依照 [ALFA 驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/) 編譯並載入正確的驅動程式。
{{< /alert >}}

---

## VirtualBox USB 直通——逐步操作

VirtualBox 需要一個額外的元件——**Extension Pack**——才能支援 USB 2.0 和 USB 3.0 直通。若未安裝，只能使用 USB 1.1（OHCI），這對現代 ALFA 介面卡來說是不夠的。

### 安裝 VirtualBox Extension Pack

1. 開啟 [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)。
2. 在 **VirtualBox Extension Pack** 下，按一下 **All supported platforms** 下載 `.vbox-extpack` 檔案。版本必須與您安裝的 VirtualBox 版本完全相符。
3. 開啟 VirtualBox，前往 **檔案 → 喜好設定 → 擴充套件**（macOS：**VirtualBox → 設定 → 擴充套件**）。
4. 按一下 **+** 圖示，瀏覽至下載的 `.vbox-extpack`，然後安裝。出現提示時接受授權。

若要從命令列驗證 Extension Pack 是否已啟用：

```bash
VBoxManage list extpacks
```

預期輸出：

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
若 **Usable** 欄位顯示 `false`，表示 Extension Pack 版本與 VirtualBox 版本不相符。請解除安裝後重新安裝正確版本。
{{< /alert >}}

### 將使用者加入 vboxusers 群組（僅限 Linux 主機）

在 Linux 主機上，您的使用者帳號必須是 `vboxusers` 群組的成員才能存取 USB 裝置。

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

執行後，請**登出再重新登入**（或重新開機）讓群組變更生效。您可以用以下指令驗證：

```bash
groups $USER
```

輸出應包含 `vboxusers`。

### 在 VM 設定中啟用 USB 控制器

1. 若 Kali VM 正在執行，請先關閉。
2. 選取 VM，按一下 **設定 → USB**。
3. 勾選 **啟用 USB 控制器**。
4. 從選項按鈕選取 **USB 3.0 (xHCI) 控制器**。

{{< alert "circle-info" >}}
AWUS036AXML 需要 USB 3.0（xHCI）。AWUS036ACH 本身是 USB 2.0 裝置，使用 USB 2.0（EHCI）在技術上就足夠，但使用 xHCI 不會造成問題，且能保持設定一致性。
{{< /alert >}}

### 新增 USB 裝置篩選器

USB 裝置篩選器讓 VirtualBox 在每次插入 ALFA 介面卡時自動擷取它，無需每次手動操作。

1. 在同一個 **設定 → USB** 面板中，按一下 **+** 圖示（從裝置新增 USB 篩選器）。
2. 若 ALFA 介面卡尚未連接，現在插入。VirtualBox 會在下拉選單中顯示它。
3. 選取裝置。通常顯示為 **"Realtek 802.11ac NIC"**（AWUS036ACH）或 **"MediaTek Corp. 802.11 b/g/n"**（AWUS036AXML）。
4. 按一下 **確定** 儲存。

### 啟動 VM 並用 lsusb 驗證

啟動您的 Kali VM。桌面載入後，開啟終端機並執行：

```bash
lsusb
```

您應該會看到類似以下的輸出：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

或 AWUS036AXML：

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### 載入驅動程式

**AWUS036ACH（RTL8812AU）：**

```bash
sudo modprobe 88XXau
```

若失敗（找不到模組），請先安裝 DKMS 套件：

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML（MT7921AU）：**

```bash
sudo modprobe mt7921u
```

### 驗證監聽模式

```bash
sudo airmon-ng start wlan1
```

成功後，**Mode** 欄位應顯示 `Monitor`：

```bash
sudo iwconfig wlan1mon
```

### VirtualBox 常見錯誤

| 錯誤 | 原因 | 修復方法 |
|---|---|---|
| USB 設定中「無可用 USB 裝置」 | 未安裝 Extension Pack 或版本不符 | 安裝對應版本的 Extension Pack |
| 介面卡未被擷取 / lsusb 中不可見 | 使用者不在 `vboxusers` 群組（Linux 主機） | `sudo usermod -aG vboxusers $USER`，然後登出/登入 |
| 「USB 裝置正被先前的請求使用」 | 主機上的其他程序正在使用該裝置 | 啟動 VM 前拔除並重新插入介面卡 |
| 裝置在 VM 內持續斷線 | 未啟用 USB 3.0 控制器；VM 使用 OHCI | 在 VM 設定 → USB 中切換至 USB 3.0（xHCI） |
| 篩選器已新增但裝置未自動擷取 | 在安裝 Extension Pack 之前建立篩選器 | 刪除篩選器，安裝 Extension Pack，再重新新增 |

---

## VMware Workstation / VMware Fusion USB 直通

VMware 處理 USB 直通的方式與 VirtualBox 不同。無需安裝額外擴充套件——USB 2.0 和 3.0 支援已內建於 VMware Workstation 17+ 和 Fusion 13+。主要機制是 **USB 仲裁器服務**，負責監控主機 USB 事件並將裝置路由至 VM。

### 透過裝置選單連接介面卡

在 VM 執行期間插入 ALFA 介面卡時，VMware 通常會顯示彈出視窗詢問哪個 VM 應擁有該裝置。若錯過彈出視窗：

1. 在 Kali VM 執行時，前往選單列的 **VM → 可移除裝置**。
2. 展開清單，找到您的 ALFA 介面卡（例如 **Realtek 802.11ac NIC**）。
3. 按一下 **連線（從主機斷開）**。

### VMware Fusion（macOS）

1. 前往 **虛擬機器 → USB 與藍牙**。
2. 在清單中找到 ALFA 介面卡。
3. 將連線切換至 **連線至 Linux**（或您的 Kali VM 名稱）。

### 驗證並載入驅動程式

連線後，在 Kali 內部驗證：

```bash
lsusb
```

然後依照上述 VirtualBox 章節載入適當的驅動程式。

### 檢查 VMware USB 仲裁器服務

若 ALFA 介面卡未出現在 **可移除裝置** 選單中，USB 仲裁器服務可能未執行。在 Linux 主機上：

```bash
sudo systemctl status vmware-usbarbitrator
```

若已停止：

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### 在 VMware 中啟用 USB 3.0

開啟 Kali VM 的 `.vmx` 檔案，確認或新增：

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
需要 VMware 硬體版本 14 或更新版本才能支援 USB 3.0（xHCI）。若您的 VM 是以舊版硬體版本建立的，請透過 **VM → 管理 → 變更硬體相容性** 升級。
{{< /alert >}}

### VMware 常見錯誤

| 錯誤 | 原因 | 修復方法 |
|---|---|---|
| 可移除裝置選單中找不到介面卡 | USB 仲裁器未執行 | 啟動 `vmware-usbarbitrator` 服務 |
| 裝置連線後立即斷線 | 主機作業系統驅動程式奪回裝置 | 停用主機的介面卡 WiFi 驅動程式，或更快速地重新連線 |
| 「裝置已被主機使用」 | 主機作業系統已宣告該裝置 | 在 VM 中連線前，先從主機移除（例如停用主機網路介面卡） |
| VM 內無 USB 3.0 速度 | VM 硬體版本 < 14 或未啟用 xHCI | 升級硬體版本，在 .vmx 中新增 `usb_xhci.present = "TRUE"` |
| 直通後監聽模式仍失敗 | Kali 內驅動程式錯誤或缺失 | 依照 [驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/) 操作 |

---

## 介面卡特定說明

### AWUS036ACH（RTL8812AU）

AWUS036ACH 是 **USB 2.0** 裝置，在 VM 環境中是測試最充分的介面卡之一。VirtualBox 和 VMware 都能可靠地處理它。驅動程式套件：`realtek-rtl88xxau-dkms`。模組名稱：`88XXau`。

### AWUS036AXML（MT7921AU）

AWUS036AXML 是支援 WiFi 6E 的 **USB 3.0** 裝置，在 VM 環境中有一些特殊情況。**必須**使用 USB 3.0（xHCI）USB 控制器。固件套件：`firmware-misc-nonfree`。某些早期型號在 VirtualBox USB 3.0 仲裁下可能發生週期性凍結問題。VMware Workstation 對 AWUS036AXML 的 USB 3.0 直通通常比 VirtualBox 更穩定。

完整評測：[AWUS036AXML WiFi 6E 評測](/zh-tw/blog/awus036axml-wifi-6e-review/)。

### AWUS036ACM（RTL8812AU，單天線）

從驅動程式和直通角度來看，與 AWUS036ACH 行為完全相同。使用相同的 `88XXau` 模組和相同的 VirtualBox/VMware 設定。

---

## 效能調校建議

**停用主機的 USB 自動暫停。** Linux 主機可能積極暫停 USB 裝置，導致 VM 失去連線：

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**分配足夠的 VM 資源。** 封包注入和擷取工作負載需要大量 CPU。至少分配：
- **2 個 CPU 核心**（建議 4 個）
- **2 GB RAM**（若執行完整 Kali 桌面，建議 4 GB）

**在滲透測試作業前建立 VM 快照。** 若驅動程式崩潰或韌體更新損壞您的設定，還原快照可在幾秒內回到已知良好狀態。

{{< alert "circle-info" >}}
對於超過 30 分鐘的擷取會話，考慮在介面卡和主機之間使用有源 USB 集線器。它提供穩定的電源，防止電壓降導致介面卡在關鍵擷取期間斷線。
{{< /alert >}}

---

## 裸機 vs VM：誠實比較

| 功能 | 裸機 Kali | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **驅動程式支援** | 完整、直接 | 良好（需 Extension Pack） | 良好（內建 USB） |
| **監聽模式穩定性** | 優秀 | 良好 | 良好–優秀 |
| **封包注入可靠性** | 優秀 | 良好（偶爾封包遺失） | 良好–優秀 |
| **設定時間** | 高（需專用硬體） | 低–中 | 低–中 |
| **可攜性** | 低 | 高（快照、可攜） | 高 |
| **CTF / 實驗室使用** | 大材小用 | 理想 | 理想 |
| **專業滲透測試** | 建議 | 可接受 | 可接受 |

---

## 疑難排解快速參考

| 症狀 | 最可能原因 | 解決方案 |
|---|---|---|
| Kali 內 `lsusb` 無顯示 | USB 直通未設定 | 新增 USB 篩選器（VBox）或透過可移除裝置連線（VMware） |
| VirtualBox USB 設定中「無 USB 裝置」 | Extension Pack 缺失或版本不符 | 安裝對應版本的 Extension Pack |
| `lsusb` 可見介面卡但無 `wlan` 介面 | 驅動程式未載入 | `sudo modprobe 88XXau` 或 `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | 未安裝 DKMS 套件 | `sudo apt install realtek-rtl88xxau-dkms` |
| 介面出現後消失 | USB 自動暫停或 VBox xHCI 仲裁 | 停用自動暫停；ACH 嘗試 USB 2.0 控制器 |
| `airmon-ng` 啟動但監聽模式靜默失敗 | 驅動程式錯誤或網路管理員衝突 | `sudo airmon-ng check kill`，然後重試 |
| VirtualBox USB 篩選器在開機時未自動擷取 | 在安裝 Extension Pack 之前新增篩選器 | 刪除篩選器，安裝 Extension Pack，重新新增 |
| VMware 在長時間會話中失去裝置 | VMware USB 仲裁器服務停止 | 重新啟用並設為自動啟動 |

---

## 後續步驟

設定好 USB 直通並驗證監聽模式後，您可以繼續：

- **安裝或更新驅動程式：** [Kali 與 Ubuntu 的 ALFA 驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)
- **完整 AWUS036ACH 設定教學：** [AWUS036ACH Kali Linux 設定指南](/zh-tw/blog/awus036ach-kali-linux-setup/)
- **AWUS036AXML 硬體評測：** [AWUS036AXML WiFi 6E 評測](/zh-tw/blog/awus036axml-wifi-6e-review/)
