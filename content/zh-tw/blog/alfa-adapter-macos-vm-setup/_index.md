---
title: "在 macOS 使用 ALFA WiFi 網路卡：VMware Fusion 與 Parallels USB 直通完整指南"
description: "如何在 macOS 使用 ALFA USB WiFi 網路卡。涵蓋 macOS 原生支援、VMware Fusion USB 直通、Parallels Desktop，以及在 Kali Linux 啟用監聽模式與封包注入。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "ALFA 網路卡能在 macOS 原生使用監聽模式嗎？"
    answer: "不能。macOS 的 CoreWLAN 與 IO80211Family 架構不支援第三方網路卡的監聽模式或封包注入，必須透過 VM 執行 Kali Linux 並使用 USB 直通。"
  - question: "Apple Silicon Mac 該選 VMware Fusion 還是 Parallels？"
    answer: "兩者皆可，但 Parallels Desktop 19+ 在 Apple Silicon 上的 ARM64 VM 效能與 USB 直通穩定度通常優於 VMware Fusion。"
  - question: "AWUS036AXML 在 Apple Silicon 的 Kali VM 上需要編譯驅動嗎？"
    answer: "不需要。MT7921AUN 驅動自 Linux 5.18 起內建核心，Kali ARM64 2024.x 以上版本插入即自動識別。"
  - question: "Intel Mac 可以用標準 Kali x86_64 ISO 嗎？"
    answer: "可以。Intel Mac 為 x86_64 架構，可直接使用 kali.org 官方標準 Kali Linux x86_64 ISO 建立 VM。"
  - question: "VirtualBox 適合在 Apple Silicon 上做資安測試嗎？"
    answer: "不建議。VirtualBox 對 Apple Silicon 的支援仍為實驗性，USB 直通存在已知問題，請改用 VMware Fusion 或 Parallels。"
---

macOS 無法原生支援 ALFA 網路卡的監聽模式與封包注入，唯一可靠做法是在 VM 內執行 Kali Linux 並透過 USB 直通繞過 macOS。

{{< tldr >}}
macOS 不支援 ALFA 網路卡的監聽模式與封包注入。解法是在 VMware Fusion 或 Parallels 中執行 Kali Linux VM，並透過 USB 直通將網路卡交給 VM。Apple Silicon 需使用 ARM64 Kali 映像。
{{< /tldr >}}

macOS 是一個精緻、適合生產環境的作業系統，但它並非為無線資安研究而設計。每位滲透測試人員工具箱中最核心的兩項功能——**監聽模式（Monitor Mode）** 與**封包注入（Packet Injection）**——在 macOS 的 Wi-Fi 堆疊中完全不存在。Apple 的 Wi-Fi 驅動程式提供了一個乾淨、功能完整的網路介面，僅此而已。

ALFA Network 網路卡在 Linux 上改變了這個局面，驅動程式支援深入且經過社群驗證。在 macOS 上情況則不同。即使 ALFA 網路卡被 macOS 識別，原生網路堆疊也不允許你將其切換至監聽模式或注入原始封包。唯一可靠的解決路徑是在**虛擬機器中執行 Kali Linux**，並將 USB 網路卡直接透傳給客戶端作業系統，完全繞過 macOS。

本指南涵蓋如何在兩大主流 macOS Hypervisor——VMware Fusion 與 Parallels Desktop——上正確完成這項設定，並特別針對 **Apple Silicon（M1/M2/M3）** 提供說明，因為 ARM 架構對網路卡與 ISO 映像的選擇有額外限制。

---

## macOS 原生支援：不需 VM 可以做到什麼

在直接進入 VM 設定前，了解 macOS 搭配 ALFA 網路卡能做什麼、不能做什麼是有價值的。

**AWUS036AXML（MT7921AUN 晶片）：** macOS 會將此網路卡識別為通用 USB 網路裝置。macOS 13 Ventura 及更新版本內建的 **MT7921AUN** 驅動程式會自動識別此網路卡。它會出現在**系統偏好設定 → 網路**（Ventura 以上為**系統設定 → 網路**）中，可像一般網路卡一樣連線 Wi-Fi。在較舊的 macOS 版本上可能完全無法識別。

**AWUS036ACH（RTL8812AU）與 AWUS036ACM（MT7612U）— 需要第三方 macOS 驅動程式的網路卡：** 這些網路卡在 macOS 上需要第三方驅動程式。社群和商業驅動套件都有，但相容性不穩定。macOS 小版本更新後常需重新安裝驅動程式，macOS 11 起核心延伸簽章要求更加嚴格，而在 Apple Silicon 上由於 Rosetta 對核心延伸的限制，情況更加脆弱。

**硬性限制——沒有監聽模式：** 無論使用哪款網路卡或安裝何種驅動程式，macOS 不提供原始監聽模式介面。CoreWLAN 框架與底層 `IO80211Family.kext` 架構不支援第三方網路卡的監聽模式。對於資安測試，必須使用搭載 USB 直通的 Kali Linux VM。

{{< alert "circle-info" >}}
如果你的目標僅是被動 Wi-Fi 流量擷取（用於除錯，非資安測試），macOS 允許按住 Option 並點選選單列的 Wi-Fi 圖示進入診斷模式。但這無法取代正式的監聽模式工作流程。
{{< /alert >}}

---

## Apple Silicon（M1/M2/M3）vs Intel Mac

你的 Mac 架構決定了需要哪個 Kali Linux 映像，以及哪些 Hypervisor 可用。

**Intel Mac（x86_64）：**
三大主流 Hypervisor——VMware Fusion、Parallels Desktop 與 VirtualBox——在 Intel Mac 上均可原生運行。可使用來自 kali.org 官方下載頁面的標準 **Kali Linux x86_64 ISO**。VM 內的驅動程式編譯步驟與所有線上 Kali 指南一致。

**Apple Silicon（M1/M2/M3）：**
Apple Silicon 是 ARM64 架構。標準 x86_64 Kali ISO 即使在 Hypervisor 內也無法在 Apple Silicon 硬體上開機——沒有 x86 模擬層（Rosetta 只適用於 macOS 使用者空間應用程式，不適用於完整 OS 虛擬化）。必須使用 **Kali Linux ARM64** 映像，可在 [kali.org/get-kali](https://www.kali.org/get-kali/) 的 Apple Silicon / ARM 區段找到。

| Hypervisor | Intel Mac | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ 個人使用免費 | ✅ 支援 ARM64 VM |
| Parallels Desktop 19+ | ✅ | ✅ Apple Silicon 最佳效能 |
| VirtualBox 7.x | ✅ | ⚠️ Apple Silicon 上仍為實驗性 |

{{< alert "triangle-exclamation" >}}
VirtualBox 對 Apple Silicon 的支援仍標記為實驗性。USB 直通在 M 晶片 Mac 上存在已知問題。對於資安測試工作流程，請在 Apple Silicon 硬體上使用 VMware Fusion 或 Parallels Desktop。
{{< /alert >}}

**USB 直通與架構無關：** ALFA 網路卡本身是 USB 裝置。主機 CPU 是 x86_64 還是 ARM64 不影響 USB 直通的運作方式。網路卡透過 USB 匯流排移交給客戶端 VM，由 Kali 內的驅動程式接管。架構只影響使用哪個 Kali 映像以及 VM 內驅動程式的編譯方式。

---

## 方案 A：VMware Fusion USB 直通

VMware Fusion 自 Fusion 13 起個人使用免費，是 macOS 使用者尋求零成本 Hypervisor 的預設推薦，且具備穩定的 USB 直通支援。

### 步驟 1 — 安裝 VMware Fusion 13+

從 [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html) 下載 VMware Fusion。安裝時需在**系統偏好設定 → 安全性與隱私權 → 一般**中允許 VMware 系統延伸。此延伸批准是 USB 直通正常運作的必要條件——沒有它，VMware 無法從 macOS USB 堆疊攔截 USB 事件。批准後 macOS 可能要求重新啟動，請完成重新啟動後再繼續。

### 步驟 2 — 建立 Kali Linux VM

- **Apple Silicon Mac：** 從 kali.org 下載 Kali Linux ARM64 安裝 ISO 或預建的 VMware ARM 映像，在 VMware Fusion 中建立新 VM 並選擇該 ARM64 ISO。
- **Intel Mac：** 下載標準 Kali Linux x86_64 安裝 ISO，建立新 VM 並選擇該 ISO 作為安裝媒體。

至少分配 **4 GB RAM** 與 **40 GB 磁碟**。Kali 安裝時選擇完整預設套件集，以預先安裝無線工具（aircrack-ng、airmon-ng、airodump-ng）。

### 步驟 3 — 透過 USB 直通連接 ALFA 網路卡

在 Kali VM 執行中且 ALFA 網路卡插入 Mac USB 埠的情況下：

1. VMware Fusion 會顯示彈出視窗：**「USB 裝置正在請求連接到您的虛擬機器。」**
2. 點擊**連接到 [VM 名稱]** 將網路卡直接移交給 Kali VM。
3. macOS 此時會失去對該網路卡的可見性——它現在由 VM 獨佔。

{{< alert "circle-info" >}}
如果彈出視窗未出現（例如 VM 啟動前網路卡已插入，或你關閉了彈出視窗），請前往 VMware Fusion 選單列：**虛擬機器 → USB 與藍牙 → [ALFA 網路卡名稱] → 連接（從 Mac 中斷連接）**，手動將 USB 裝置指派給 VM。
{{< /alert >}}

### 步驟 4 — 在 Kali 內驗證

在 Kali VM 的終端機中確認網路卡可見：

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

如果兩個指令都沒有輸出，表示直通未完成——請重新檢查 VMware 裝置選單。

### 步驟 5 — 載入驅動程式並驗證監聽模式

MT7921AUN（AWUS036AXML）的驅動程式已內建於 Kali 核心。RTL8812AU 網路卡需要安裝驅動程式——請參閱[驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)。驅動程式啟用後：

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

airodump-ng 顯示即時掃描輸出即表示直通、驅動程式載入與監聽模式全部正常運作。

---

## 方案 B：Parallels Desktop USB 直通

Parallels Desktop 是 Apple Silicon Mac 效能優先時的首選 Hypervisor。它需要訂閱授權，但其 ARM64 VM 支援與 USB 直通實作在 Apple Silicon 硬體上比 VMware Fusion 更成熟。

### 步驟 1 — Parallels Desktop 19+

從 [parallels.com](https://www.parallels.com) 安裝 Parallels Desktop。與 VMware Fusion 相同，需在**安全性與隱私權**中允許 Parallels 系統延伸並重新啟動。

### 步驟 2 — 建立 Kali Linux ARM64 VM

在 Apple Silicon 上，Parallels 僅支援 ARM64 客戶端 OS 映像。從 kali.org 下載 Kali Linux ARM64 映像，在 Parallels 中使用該映像建立新 VM。

{{< alert "circle-info" >}}
Parallels Desktop 19+ 在 Apple Silicon 上的新 VM 精靈中可直接下載並安裝 Kali Linux ARM——你可能不需要手動下載 ISO。
{{< /alert >}}

在 Intel Mac 上，標準 x86_64 Kali ISO 可直接在 Parallels 中使用。

### 步驟 3 — 透過 USB 連接 ALFA 網路卡

在 Kali VM 執行中且 ALFA 網路卡插入的情況下：

1. 在 macOS 選單列，前往**裝置 → USB 與藍牙**。
2. 在清單中找到你的 ALFA 網路卡（可能顯示為 **Realtek 802.11ac NIC**、**MediaTek Wi-Fi** 或類似名稱）。
3. 點擊它並選擇**連接到 Linux**（或你的 VM 名稱）。

### 步驟 4 — 使用 lsusb 驗證

在 Kali VM 終端機中：

```bash
lsusb
ip link show
```

ALFA 網路卡應出現在 `lsusb` 輸出中，並作為新的 `wlan` 介面出現在 `ip link show` 中。

{{< alert "circle-info" >}}
在 Apple Silicon 上，Parallels 的 I/O 密集型 VM 工作負載效能通常優於 VMware Fusion。如果你進行長時間的 airodump-ng 會話或大量封包擷取，Parallels 通常會產生較低的 CPU 負載。
{{< /alert >}}

---

## Kali on Apple Silicon：ARM64 驅動程式說明

在 Apple Silicon 的 VM 中執行 Kali ARM64 會改變驅動程式編譯環境。大多數線上指南假設 x86_64，但步驟幾乎相同——關鍵差異在於預安裝的套件以及 DKMS 如何處理 ARM 核心標頭。

**RTL8812AU on ARM64：**
來自 [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) 的 RTL8812AU 驅動程式可在 ARM64 上正確編譯。DKMS 建置流程與 x86_64 相同：

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

**MT7921AUN on ARM64：**
`mt7921u` 驅動程式自 **Linux 5.18 起已內建於核心**，包含在 Kali ARM64 2024.x 及更新版本中。AWUS036AXML 在 Kali ARM64 上不需要手動編譯。USB 直通後網路卡會自動識別。

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**M 晶片 Mac 推薦：** 如果你是專門為在 Apple Silicon Mac 上的 VM 中使用而購買 ALFA 網路卡，**AWUS036AXML（MT7921AUN）** 是更好的選擇。其內建核心驅動程式完全省去 DKMS 編譯步驟，並在 ARM64 Kali 上可靠運作。

---

## 監聽模式與注入測試

完成 USB 直通後，執行以下指令序列驗證完整堆疊是否正常運作：

```bash
# 1. 確認 USB 裝置可見
lsusb

# 2. 列出無線介面
ip link show

# 3. 終止衝突的程序
sudo airmon-ng check kill

# 4. 在無線介面上啟動監聽模式
sudo airmon-ng start wlan1

# 5. 確認監聽介面已建立
ip link show wlan1mon

# 6. 開始被動掃描
sudo airodump-ng wlan1mon
```

airodump-ng 顯示掃描輸出（SSID、BSSID、頻道、客戶端裝置）即表示整個流程正常。

**如果直通後 `wlan1` 未出現：**

1. 從 Mac 拔出 ALFA 網路卡。
2. 等待五秒後重新插入。
3. 透過 Hypervisor 的 USB 裝置選單重新指派給 VM。
4. 在 Kali 內再次執行 `lsusb` 確認裝置出現。

{{< alert "triangle-exclamation" >}}
不要嘗試對 VM 內預設的 `wlan0` 介面執行 `airmon-ng start wlan0`——該介面通常是 VMware/Parallels 用於網際網路連線的虛擬網路介面，而非透傳的 ALFA 網路卡。使用錯誤的介面會在沒有啟用監聽模式的情況下中斷你的 VM 網路連線。
{{< /alert >}}

---

## 效能與限制

**USB 直通延遲：** 透過 Hypervisor 層傳遞 USB 裝置比在裸機 Linux 上使用網路卡多約 1–2 ms 的處理延遲。對於 802.11 資安測試目的，這個延遲在操作上並不顯著。

**獨佔所有權：** macOS 無法同時與 Kali VM 共享 ALFA 網路卡。一旦網路卡透傳給 VM，它就會從 macOS 完全消失。若要將網路卡還給 macOS，請透過 Hypervisor 的 USB 裝置選單從 VM 中斷連接，然後拔出並重新插入網路卡。

**電力消耗：** 在 VM 中執行 USB Wi-Fi 網路卡（最高 100 mW 射頻輸出）同時還執行 Mac 自身的 Wi-Fi 無線電，電力消耗相當可觀。**長時間測試時請使用充電器**，尤其是在 Apple Silicon MacBook 上。

---

## 疑難排解

| 症狀 | 可能原因 | 解決方案 |
|---|---|---|
| ALFA 網路卡未出現在 Hypervisor USB 選單 | macOS 系統延伸未批准 | **系統偏好設定 → 安全性與隱私權 → 一般** → 允許 VMware/Parallels 延伸，然後重新啟動 |
| Kali VM 內 `lsusb` 未顯示 ALFA 網路卡 | USB 直通未完成 | 透過 VM → USB 與藍牙選單手動連接；重新插拔網路卡 |
| 直通後缺少 `wlan1` 介面 | 驅動程式未載入（RTL8812AU） | 透過 DKMS 安裝 RTL8812AU 驅動程式；請參閱[驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` 失敗並顯示「Operation not permitted」 | NetworkManager 佔用介面 | 先執行 `sudo airmon-ng check kill`，然後重試 |
| 監聽模式啟動但 airodump-ng 未顯示網路 | 頻道或介面錯誤 | 用 `ip link show` 確認 `wlan1mon` 存在；嘗試 `sudo airodump-ng --band abg wlan1mon` |
| 插入 ALFA 網路卡時 VM 當機 | USB 控制器衝突（VMware） | 關閉 VM，前往 VM 設定 → USB，將控制器從 USB 3.0 切換為 USB 2.0，重新啟動 VM |

{{< alert "circle-info" >}}
在 Apple Silicon 上，如果 ALFA 網路卡被識別但介面未出現在 Kali 中，請在插入後立即執行 `dmesg | tail -30`。輸出會顯示核心是否偵測到裝置以及哪個驅動程式正在嘗試綁定。
{{< /alert >}}

---

{{< faq >}}




## 相關指南

針對在 Windows 和 Linux 主機上使用 VirtualBox 或 VMware Workstation 的使用者，請參閱配套指南：[ALFA 網路卡 USB 直通：VirtualBox 與 VMware 設定指南](/zh-tw/blog/alfa-adapter-virtualbox-vmware-usb/)。

有關本指南推薦的 AWUS036AXML 網路卡詳細資訊，包括 6 GHz 頻段效能基準測試與驅動程式版本說明，請參閱完整評測：[ALFA AWUS036AXML WiFi 6E 評測](/zh-tw/blog/awus036axml-wifi-6e-review/)。

## 參考來源

1. [ALFA Network 官方網站](https://www.alfa.com.tw/)
2. [Kali Linux 官方下載頁面](https://www.kali.org/get-kali/)
3. [VMware Fusion 產品頁面](https://www.vmware.com/products/fusion.html)
4. [Parallels Desktop 官方網站](https://www.parallels.com/)
5. [aircrack-ng rtl8812au 驅動專案](https://github.com/aircrack-ng/rtl8812au)
