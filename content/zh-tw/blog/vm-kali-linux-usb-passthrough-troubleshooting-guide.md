---
title: "虛擬機 Kali Linux 抓不到外接網卡？VirtualBox/VMware USB 穿透與斷線診斷手冊"
date: 2026-08-18
draft: false
slug: "vm-kali-linux-usb-passthrough-troubleshooting-guide"
tags:
  - "Wireless"
  - "Hardware"
categories:
  - "Wireless Hardware"
  - "Technical Guide"
description: "全面解析 VirtualBox 與 VMware 的 USB 穿透機制，解決 Kali 虛擬機無法辨識外接 USB 網卡、Extension Pack 設定及自動過濾器排障方案。"
featureimage: "/images/blog/08_usb_passthrough_blueprint.jpg"
author: "benny-lai"
lastmod: 2026-08-18
faq:
  - question: "為什麼虛擬機預設使用 NAT 或 Bridge 時無法使用網卡的監聽模式？"
    answer: "NAT/Bridge 模式下虛擬機僅取得虛擬乙太網卡（eth0），只有透過 USB Pass-Through 實體穿透才能直接控制原生無線射頻介面。"
---

![Virtual Machine USB Pass-Through Blueprint](/images/blog/08_usb_passthrough_blueprint.jpg)

> **適用平台**：Windows / Linux / macOS 主機 + Oracle VirtualBox / VMware Workstation 虛擬機（Guest = Kali Linux / Debian / Ubuntu）
> **引導硬體**：ALFA AWUS036ACH（Realtek RTL8812AU）/ ALFA AWUS036AXML（MediaTek MT7921AU）
> **本篇定位**：標準化「USB 穿透（USB Pass-through）」排障診斷手冊。macOS 主機的 USB 穿透限制說明見第五章。

---

## TL;DR

很多 Kali 使用者把網卡插在主機上，卻在虛擬機裡看不到無線介面——**這幾乎都不是網卡壞掉**，而是三個非常常見的原因之一：

1. **VirtualBox 沒裝擴充套件（Extension Pack）**：沒有它，Guest 連 USB 2.0/3.0 控制器都用不了（USB 1.1 的傳輸速率上限僅 12 Mbps，根本不夠網卡用）。
2. **USB 穿透設定沒做**：主機預設「獨占」所有 USB 裝置，Guest 要嘛手動掛載、要嘛設定「USB 過濾器（VM USB Filter）」來自動接管網卡。
3. **Guest 內部的驅動程式沒載入**：USB 層穿過去了（`lsusb` 看得到），但 Linux 沒有相對應的驅動程式，所以 `ip link` 沒出現 `wlan` 介面。

診斷口訣：**主機端 `lsusb` 確認硬體正常 → Guest 端 `lsusb` 確認穿透成功 → Guest 端 `iwconfig` / `ip link` 確認無線介面 → 還沒有就看 `dmesg` 找驅動層原因。** 依序往下走，就能在三分鐘內判斷問題出在哪一層。

---

## 1. 為什麼虛擬機預設調用不到主機的無線網卡？

### 1.1 你的 USB 網卡「同時」只屬於一個作業系統

USB 的運作是**單一主控（single host）**架構：一個 USB 裝置在同一個時間點，只能被一個「USB 主控制器（Host Controller）」控制。當網卡插在主機上，裝置會先被**主機作業系統（Host OS）**列舉（enumerate）並接管，主機的驅動程式認識它、控制它。

虛擬機（Guest VM）不是插在 USB 匯流排上的實體裝置，它只是跑在主機裡、由管理程式（Hypervisor）扮演出的「假硬體」。所以 Guest 想要使用 USB 網卡，**必須由主機把裝置主動「移交」給 Guest**——這個機制就叫 **USB 穿透（USB Pass-through / USB Redirection）**。

### 1.2 USB 穿透到底穿透了什麼？

以 VirtualBox 為例，穿透流程是這樣的：

```
實體 USB 網卡（AWUS036ACH / AWUS036AXML）
       │  插在主機的 USB 實體連接埠
       ▼
主機作業系統（Host OS）的 USB 主控制器
       │  Hypervisor（VirtualBox）攔截並重新導向
       ▼
虛擬的 USB 主控制器（模擬的 EHCI / xHCI）
       │  Guest（Kali）看起來「就像插在自己身上」
       ▼
Kali 的 USB 驅動程式 → 無線網卡驅動 → wlan 介面
```

穿透成功後，這個裝置在**主機端會被移轉控制權**（行為上像被「拔走」，主機上無法再使用它），轉而在 Guest 內變成一個全新的 USB 裝置。**這是正常現象，不是 bug。** 主機的一個 USB 裝置不能同時給兩邊用。

### 1.3 「抓不到」其實有三個層次

| 層次 | 檢查工具 | 症狀 | 代表意義 |
|------|---------|------|---------|
| **USB 穿透層** | Guest 內 `lsusb` | `lsusb` 完全看不到網卡的 VID:PID | 穿透失敗（Extension Pack / 控制器 / 過濾器問題） |
| **驅動程式層** | Guest 內 `dmesg` | `lsusb` 看得到，但 `dmesg` 有錯誤（如缺韌體、`Required key not available`） | Guest 內部缺驅動程式或模組載入失敗 |
| **無線介面層** | Guest 內 `iwconfig` / `ip link` | `lsusb` 與 `dmesg` 都正常，卻沒有 `wlan` 介面 | 驅動程式載入了但介面未註冊，或模式／設定問題 |

> **判斷口訣**：先看 `lsusb` 判斷「裝置有沒有穿透進 Guest」，再看 `ip link` 判斷「驅動程式有沒有認識它」。**別一開始就懷疑網卡壞了。**

---

## 2. VirtualBox：先裝 Extension Pack，再設 USB 3.0 控制器

### 2.1 擴充套件（Extension Pack）是非裝不可的

VirtualBox 基礎套件**只內建 USB 1.1（OHCI）控制器**的模擬，而 USB 1.1 的傳輸速率完全不夠網卡使用。**USB 2.0（EHCI）與 USB 3.0（xHCI）控制器都要靠 Oracle 官方「擴充套件（Extension Pack）」**才有。

沒有裝 Extension Pack 的症狀很典型：Guest 設定裡選不到 USB 2.0 / USB 3.0 控制器，或一掛載網卡就回報「裝置連線到虛擬機失敗（error code E_FAIL / VERR_PDM_NO_USB_PORTS）」。

### 2.2 版本必須「完全不差」地對上

Extension Pack 的版本**必須與 VirtualBox 主程式版本完全一致**（例如 VirtualBox 7.0.20 就要配 7.0.20 的 Extension Pack），差一個小版本都可能安裝失敗或載入失敗。

```bash
# 查看目前 VirtualBox 版本
vboxmanage --version
```

到 Oracle 官方下載頁（https://www.virtualbox.org/wiki/Downloads）下載對應版本的
`Oracle_VM_VirtualBox_Extension_Pack-<版本>.vbox-extpack`，然後：

```bash
# 方式一：GUI 安裝（VirtualBox 主程式 → 檔案 → 工具 → Extension Pack Manager → 安裝）
# 方式二：指令安裝
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# 確認已安裝
VBoxManage list extpacks
```

> 安裝時會顯示 Oracle 授權（Personal Use and Evaluation License）；個人使用免費，商用建制請依授權內容辦理。

### 2.3 Linux 主機：把自己加入 vboxusers 群組

在 Linux 主機上，VirtualBox 要存取 USB 裝置，**需要使用者屬於 `vboxusers` 群組**。很多人安裝了擴充套件卻還是失敗，就是卡在權限。

```bash
# 加入群組（以你的使用者名稱取代 <user>）
sudo usermod -aG vboxusers $USER

# 登出再登入（或重新開機）讓群組生效；確認群組已生效
id $USER
```

### 2.4 設定 USB 3.0（xHCI）控制器

1. 選取你的 Kali 虛擬機 → **設定（Settings）→ 連接埠（Ports）→ USB**。
2. 勾選「Enable USB Controller」，並選擇 **USB 3.0 (xHCI) Controller**。
   - AWUS036AXML 是 USB 3.2 Gen 1（USB-C）規格，**務必選 USB 3.0 (xHCI)**，選 USB 2.0 會限制傳輸速率。
   - AWUS036ACH 為 USB Type-A 介面，在 USB 2.0 與 USB 3.0 控制器下皆可使用；若要較佳傳輸速率，一樣選 USB 3.0 (xHCI)。
3. 修改控制器後**關機再開機**（不是在 Guest 內執行 reboot）才能套用變更。

### 2.5 手動掛載：視窗右下角的 USB 圖示

開啟 Kali 虛擬機後，注意視窗**右下角的 USB 圖示**（一支 USB 插頭）：

1. 點 USB 圖示 → 會列出目前插在主機上的 USB 裝置。
2. 你的網卡應該顯示類似 `Realtek 802.11ac NIC`（ACH），或 `ALFA AWUS036AXML` / MediaTek（AXML）。
3. 點它一下，裝置就會「移交」給 Kali。

如果清單是空的，代表穿透層出了問題——回去 2.2 / 2.3 檢查，或直接跑第六章排障工作表。

### 2.6 VMware 對照：內建支援，但有兩個檢查點

VMware Workstation / Fusion **不需要**額外擴充套件就有 USB 穿透功能，但有兩個常見檢查點：

1. **主機端服務**：Linux 主機上請確認 `vmware-usbarbitrator`（USB 仲裁服務）有在跑：
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # 如果沒在跑，啟動並設為開機自動執行
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **虛擬機設定**：虛擬機設定 → USB Controller → 勾選 **USB 3.1（或 USB 3.0）**。
3. **手動連線**：VMware 視窗選單 → **可移除裝置（Removable Devices）→ 你的網卡 → 連線（Connect）**。

> **對照重點**：VirtualBox 卡在「沒裝擴充套件」；VMware 卡在「仲裁服務沒跑」或「控制器 USB 3.0 沒開」。先確認你用的是哪家，再對號入座。

---

## 3. 診斷工具三步驟：lsusb → iwconfig → dmesg

穿透設定做完後，用三個指令把問題定位到「穿透層」還是「驅動層」。

### 第 0 步：主機端先確認硬體正常（別把問題賴給網卡）

在**主機作業系統**開終端機執行：

```bash
lsusb
```

預期看到（依型號）：

```
# AWUS036ACH（Realtek RTL8812AU）
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# 或 AWUS036AXML（MediaTek MT7921AU）
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- 主機看得到 → 硬體與線材正常，問題在穿透或 Guest 驅動。
- 主機也看不到 → **先檢查主機端**（換 USB 連接埠、換線、另一台主機交叉測試），再考慮開技術支援單。

### 第 1 步：Guest 端 lsusb——穿透成功沒有？

在 **Kali 虛擬機內**執行：

```bash
lsusb
```

- 看得到同樣的 VID:PID → **穿透成功**，跳到第 2 步。
- 看不到 → **穿透失敗**，回去檢查第二章（Extension Pack / 控制器 / vboxusers 群組），或確認網卡是否被主機的其他軟體占用。

### 第 2 步：iwconfig / ip link——無線介面出現沒有？

```bash
iwconfig
# 或（較新版本）
iw dev
ip link
```

- 出現 `wlan0` / `wlx...` 介面 → **全部打通**，可以開始使用了。
- 沒有無線介面但 `lsusb` 看得到 → 問題在 **Guest 的驅動程式層**，看第 3 步。

### 第 3 步：dmesg——驅動層為什麼失敗？

```bash
# 觀察核心剛才的訊息
sudo dmesg | tail -30
# 過濾 USB 與無線相關的訊息
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

常見的 `dmesg` 結果對照：

| `dmesg` 訊息 | 原因 | 處理方式 |
|-------------|------|---------|
| `usb 3-1: new high-speed USB device ...` 之後沒有後續 | 裝置列舉完成，但沒有可用的驅動程式 | Guest 內安裝對應驅動程式（見 FAQ Q4） |
| `Direct firmware load failed` / `firmware_loading` | 缺少韌體（firmware）檔案 | `apt install firmware-realtek` 後重新載入模組 |
| `Required key not available` | Secure Boot 開啟，模組未簽署 | 透過 MOK 金鑰簽署（請勿關閉 Secure Boot） |
| `disagrees about version of symbol` | 驅動版本與核心不符 | 重新以 DKMS 編譯安裝 |

> **重點理解**：`lsusb` 看得到只能證明「USB 穿透了吧」，**不代表驅動程式已載入**。常見的「穿透成功但沒有 wlan」就是卡在 Guest 內部沒有對應的驅動程式。

---

## 4. USB VM Filter：插上就自動掛載 + 斷線疑難

### 4.1 為什麼要設 USB 過濾器（USB Filter）？

手動掛載（第二章 2.5）的問題是：**每次重開 Kali 虛擬機都要再點一次**。設定「USB 過濾器」後，只要網卡一插上（或虛擬機一開機），VirtualBox 就會**自動把符合條件的裝置轉進 Guest**。

設定方法（VirtualBox）：

1. 虛擬機設定 → USB → 點右邊 **「＋」新增過濾器 → 選擇你的網卡裝置**。
2. VirtualBox 會自動填入一筆過濾規則（含供應商 ID / 產品 ID / 序號等欄位）：
   - **名稱（Name）**：例如 `ALFA AWUS036AXML` 或 `AWUS036ACH`
   - **供應商 ID（Vendor ID）**：AWUS036ACH 為 `0bda`、AWUS036AXML 為 `0e8d`
   - **產品 ID（Product ID）**：AWUS036ACH 為 `8812`、AWUS036AXML 為 `7961`
3. 若有多支同型號網卡，把「序號（Serial Number）」欄位也補上，避免過濾到另一支。

> 小技巧：過濾器上按滑鼠右鍵 → **編輯過濾器**，可只保留 Vendor ID 與 Product ID（寬鬆匹配）或補上序號（精準匹配）。

### 4.2 頻繁斷線：通常不是網卡壞，是供電或控制器

高功率網卡（AWUS036ACH 監聽／注入時瞬時電流較高；AWUS036AXML 為 USB 3 規格）在虛擬機內偶發「用一用就掉卡／斷線」的典型原因與對策：

| 現象 | 原因 | 對策 |
|------|------|------|
| 穿透後供電不足、一直掉卡 | 虛擬 USB 控制器模擬的供電能力較保守，或主機連接埠供電不足 | 主機端改用**主機板背板 USB 連接埠**或有獨立供電的 USB Hub |
| 網卡一下有一下沒有 | 主機的 **USB 省電（autosuspend）** 把裝置睡掉了 | 在主機設定中關閉「該裝置」的 USB 自動休眠（請勿關閉系統整體安全防護） |
| 掛載即失敗、error code 一串 | 控制器選錯（USB 1.1/2.0 撐不起 USB 3 裝置） | 改選「USB 3.0 (xHCI) Controller」並關機重開 |
| 主機待命（sleep）後醒來網卡失效 | 主機睡眠時 Hypervisor 的 USB 重新導向斷裂 | 使用前避免主機待命；或喚醒後重新掛載一次 |

### 4.3 安全提醒

要降低掉卡，可關閉**單一 USB 裝置**的自動休眠，但這僅限「該裝置」層級。請**不要**為了省麻煩而關閉系統層級的安全性防護（防火牆、Secure Boot），那會付出不成比例的代價。

---

## 5. macOS 主機的限制與平台紅線

### 5.1 macOS 主機的 USB 穿透有先天限制

從 macOS 主機跑虛擬機做 USB 穿透，是**最容易卡關的組合**，請先確認你的情況：

| macOS 主機 | VirtualBox | VMware Fusion |
|-----------|-----------|---------------|
| **Apple Silicon（M1/M2/M3/M4）** | ⚠️ **USB 穿透支援受限／不完整**，官方公告的已知限制之一；即使網卡驅動正常，穿透層也可能直接用不了 | ⚠️ 支援較完整，但仍建議先「主機直插」確認網卡在 macOS 端正常 |
| **Intel（Intel Mac）** | ✅ 可用，但需先通過**核心延伸功能（Kernel Extension）認可**流程（系統設定 → 安全性與隱私權 → 允許 Oracle 相關核心延伸功能），並安裝與版本完全相符的 Extension Pack | ✅ 可用 |

**建議**：若你的主機是 macOS，優先以「主機直插 → `system_profiler SPUSBDataType` → 確認網卡在主機端正常」作為所有排障的第一關。**macOS 端不支援的型號請勿貼進虛擬機排障清單**，那會浪費大量時間。

### 5.2 平台紅線（Support Boundary）

| 平台 | 支援狀態 | 說明 |
|------|---------|------|
| Windows 主機 + VirtualBox / VMware + Kali Guest | ✅ 支援 | 本章所有流程皆適用 |
| Linux 主機 + VirtualBox / VMware + Kali Guest | ✅ 支援 | 記得 vboxusers 群組（VB）與 vmware-usbarbitrator 服務（VMware） |
| **macOS（Apple Silicon）** + VirtualBox | ⚠️ **USB 穿透受限** | 建議改用 VMware Fusion，或使用 Linux／Windows 主機 |
| macOS（Intel）+ VirtualBox | ✅ 支援 | 需完成核心延伸功能認可 + 版本相符的 Extension Pack |
| **Guest 為 macOS** | ❌ 不建議 | 本文以 Kali / Debian / Ubuntu 等 Linux Guest 為前提 |

> **支援邊界**：排障時請務必先確認「主機端網卡是否正常」，再談虛擬機設定的問題。若主機端本身抓不到網卡，任何虛擬機設定都救不回來——那時的下一步是主機端的驅動程式問題（可參考本站其他驅動排障文章）。

---

## 6. 標準排障工作表：報修前先跑一遍（客服 Intake）

> 遇到「虛擬機抓不到網卡」，依序完成下表，並把結果記下來。**完整跑過這份工作表，再決定要不要開技術支援單**——很多時候自己就解掉了，也大幅縮短客服來回時間。

### Step 1：主機端硬體檢查

| 檢查項 | 指令 | 記錄欄 |
|-------|------|-------|
| 主機作業系統與架構 | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| 主機看得到網卡？ | 主機 `lsusb` | VID:PID \_\_\_\_\_ |
| USB 連接埠與線材 | 換 port、換線再試一次 | 結果 \_\_\_\_\_ |

### Step 2：虛擬化軟體（Hypervisor）層檢查

| 檢查項 | 操作 | 記錄欄 |
|-------|------|-------|
| 虛擬化軟體與版本 | VirtualBox：`vboxmanage --version` ／ VMware：Help → About | \_\_\_\_\_ |
| 擴充套件版本相符？ | VirtualBox：`VBoxManage list extpacks` | 版本 \_\_\_\_\_ |
| 主機權限 / 服務 | Linux 主機：`id` 看是否有 vboxusers；VMware：`systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| USB 控制器設定 | VirtualBox：USB 3.0 (xHCI) Controller 有勾？ | 是 / 否 |

### Step 3：穿透結果檢查

| 檢查項 | 指令 | 記錄欄 |
|-------|------|-------|
| Guest 看得到網卡？ | Guest 內 `lsusb` | \_\_\_\_\_ |
| 無線介面出現？ | Guest 內 `iwconfig` / `ip link` | \_\_\_\_\_ |
| 驅動層訊息 | Guest 內 `sudo dmesg \| tail -30` | \_\_\_\_\_ |
| 使用的 Guest 核心 | `uname -r` | \_\_\_\_\_ |

### Step 4：判斷與紀錄

- `lsusb`（Guest）看不到 → **穿透層**問題 → 複習第二章與 Step 2。
- `lsusb` 看得到、`ip link` 沒有 wlan → **驅動層**問題 → 複習第三章第 3 步。
- 都正常但不穩定 → **供電／省電／控制器**問題 → 第四章。

### 客服 Intake 資訊封包

打通技術支援電話／送出工單前，一次附上下列資訊，就能讓客服直接切入正題：

> **主機 OS + 架構、虛擬化軟體與版本、是否安裝擴充套件及版本、主機端 `lsusb` 輸出、Guest 端 `lsusb` 輸出、Guest 端 `ip link` / `iwconfig` 輸出、`dmesg` 相關訊息、網卡型號與連接方式（USB-C / USB-A、直插或 Hub）**

---

## 7. 常見問題（FAQ）

**Q1：我換了 USB 連接埠結果 `lsusb` 就消失了，是網卡壞了嗎？**
不一定。先確認你插的是不是「僅充電」連接埠，或主機為了省電把裝置休眠了。換回主機板背板的一般 USB 連接埠，或重新插拔一次，多半就恢復。

**Q2：VM 視窗右下角 USB 圖示是空的，怎麼辦？**
依序檢查：① 擴充套件版本是否與 VirtualBox 完全相符；② Linux 主機是否在 `vboxusers` 群組（需重新登入）；③ 主機端 `lsusb` 還看不看得到網卡；④ 是否有其他軟體（例如主機端驅動工具）佔用了裝置。

**Q3：設定 USB 過濾器後，主機自己反而不能用網卡了？**
這是正常的。穿透給 Guest 後，裝置控制權在 Guest 身上，主機端無法同時使用。要用回主機做其他事情時，先在 VM 視窗的 USB 圖示把它「退還（release）」回主機。

**Q4：Guest 內 `lsusb` 看得到，但沒 wlan 介面，該裝什麼驅動？**
看晶片：
- **AWUS036AXML（MediaTek MT7921AU）**：核心內建 `mt7921u` 驅動，Kernel 5.18+ 隨插即用；先確認 `apt install linux-firmware` 已更新。
- **AWUS036ACH（Realtek RTL8812AU）**：屬於核心外掛（out-of-tree）驅動，需安裝社群維護的 `aircrack-ng/rtl8812au` 並用 DKMS 編譯（並留意 Secure Boot 的 MOK 簽署，請勿關閉 Secure Boot）。

**Q5：為什麼選了 USB 3.0 控制器 Guest 反而進不了系統？**
少數舊版 Guest 核心對 xHCI 的支援較差。若 Kali 是較舊版本，可先試「關機 → 改回 USB 2.0 (EHCI) Controller → 開機 → 升級核心 → 再改回 USB 3.0」。盡量讓 Kali 保持最新版本，xHCI 支援較完整。

**Q6：網卡在真機上很快，進虛擬機就變慢，是正常的嗎？**
是的，虛擬機內的網卡效能大致等同「透過 USB 模擬層的轉介」，會比真機直插多一些損耗（overhead）；正確的 USB 3.0 (xHCI) 控制器與更新版 Hypervisor 能把損耗壓到最低。若效能嚴重低落，優先確認控制器不是停在 USB 1.1。

---

## 8. 結論與硬體建議

「虛擬機抓不到外接網卡」九成以上不是硬體故障，而是**穿透設定**或**Guest 驅動**兩件事其中一件沒做好。把本文的動作照順序跑完：

1. **主機端 `lsusb` 先確認硬體沒問題。**
2. **VirtualBox 一定裝版本相符的 Extension Pack**、Linux 主機記得加入 `vboxusers` 群組；VMware 確認 `vmware-usbarbitrator` 服務在跑。
3. **USB 控制器設為 USB 3.0 (xHCI)**，並用 USB 過濾器讓網卡自動掛載。
4. **Guest 內依 `lsusb → iwconfig / ip link → dmesg` 定位層次**，缺驅動補驅動，別再猜網卡壞了。

**推薦硬體**：ALFA AWUS036AXML（MediaTek MT7921AU）在較新核心的 Kali 上**核心內建驅動、隨插即用**，虛擬機穿透後最省心；ALFA AWUS036ACH（Realtek RTL8812AU）同樣堪用，但要記得在 Guest 內以 DKMS 編譯社群驅動並處理 Secure Boot 簽署（可參考本站關於 RTL8812AU DKMS 排障的文章）。兩者皆建議在主機端使用有獨立供電的 USB 連接埠／Hub，把「掉卡」的變數一次排除。

**下一步**：把第六章的排障工作表存一份在你的 Kali 虛擬機桌面；每次「抓不到網卡」就先整份跑完，再決定要不要開技術支援單——照表操課，資料治百病。

---

## 參考資源

| 資源 | 連結 |
|------|------|
| Oracle VirtualBox 官方下載頁（Extension Pack） | https://www.virtualbox.org/wiki/Downloads |
| VirtualBox 官方手冊：USB 設定與過濾器 | https://www.virtualbox.org/manual/（搜尋「USB」章節） |
| VirtualBox 手冊：已知限制（含 Apple Silicon USB 穿透限制） | https://www.virtualbox.org/manual/（Changelog / Limitations） |
| VirtualBox Extension Pack 安裝指令 | `vboxmanage help extpack` |
| aircrack-ng RTL8812AU 社群驅動（AWUS036ACH Guest 內使用） | https://github.com/aircrack-ng/rtl8812au |
| ALFA AWUS036ACH 官方產品頁 | https://www.alfa.com.tw/products/awus036ach_1 |
| ALFA AWUS036AXML 官方產品頁 | https://www.alfa.com.tw/ |
| Yupitek 技術支援 | https://yupitek.com/ |

> **合法使用聲明**：在虛擬機內啟用監聽模式、封包注入等資安操作，僅限於您擁有或已獲得明確授權之網路環境。使用者須自行遵守所在地法律規範，並確保所有測試皆有合法授權依據。
