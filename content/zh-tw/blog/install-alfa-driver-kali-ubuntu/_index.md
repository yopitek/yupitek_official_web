---
title: "如何在 Kali Linux 與 Ubuntu 24.04 安裝 ALFA USB WiFi 驅動程式（2026 完整教學）"
description: "完整說明如何在 Kali Linux 2024 和 Ubuntu 24.04 安裝 ALFA Network USB WiFi 網路卡驅動程式，涵蓋 RTL8812AU、MT7612U 及 MT7921AUN 晶片組，附除錯技巧。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["驅動程式安裝", "Kali-Linux", "Ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
---

要讓 USB WiFi 網路卡在 Linux 上正常運作，關鍵幾乎都在驅動程式。Windows 有廠商提供的安裝程式，Linux 則不同——系統使用核心模組（kernel module）來與硬體溝通，也就是由作業系統在開機時或需要時載入的編譯程式碼。理解這個機制，除錯就會變得清晰，驅動程式安裝也更有規律可循。

本教學涵蓋所有主要 ALFA Network USB WiFi 網路卡的晶片組，適用於 Kali Linux 2024/2025 和 Ubuntu 24.04 LTS。

---

## Linux 上的 USB WiFi 驅動程式運作原理

### 核心模組

Linux WiFi 驅動程式是一個**核心模組**——副檔名為 `.ko` 的檔案，在開機時或需要時載入正在運行的核心。當你插入 USB 裝置，核心會讀取其 USB Vendor ID 和 Product ID，從資料庫中找到對應的模組並自動載入。

以 MediaTek MT7612U 等常見晶片組為例，這個過程是透明的：插入網路卡、模組載入、介面出現。但對於較新或較少見的晶片組，核心內並沒有對應模組，你就必須自行從原始碼編譯。

### 非主線（Out-of-Tree）驅動程式

當驅動程式未被收錄於主線核心（稱為「非主線」或「外部」驅動程式）時，你需要：

1. 下載驅動程式原始碼
2. 針對目前執行中的核心標頭檔進行編譯
3. 將編譯產生的 `.ko` 檔案安裝至核心模組目錄
4. 用 `modprobe` 載入它

編譯步驟需要核心標頭檔已安裝，且版本必須與執行中的核心完全一致。這是驅動程式安裝失敗最常見的原因。

### DKMS：動態核心模組支援

單純執行 `make install` 只會針對當前核心編譯驅動程式。當 Kali 或 Ubuntu 更新核心時（這是常態），舊驅動程式就無法載入，你必須重新編譯。

**DKMS** 解決了這個問題——它將驅動程式原始碼註冊到一個系統背景程式，每當新核心安裝時，DKMS 會自動重新編譯所有已註冊的模組。對於任何需要非主線驅動程式的網路卡，這是推薦做法。

---

## 確認你的晶片組

你需要的驅動程式完全取決於晶片組，而非網路卡的型號名稱。相同名稱但不同硬體版本的網路卡，可能使用不同的晶片組。

### ALFA 型號與晶片組對照表

| ALFA 型號 | 晶片組 | USB ID | 驅動程式 |
|---|---|---|---|
| [AWUS036ACH](/zh-tw/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACHM](/zh-tw/products/alfa/awus036achm/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/zh-tw/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u（內建核心）|
| [AWUS036ACX](/zh-tw/products/alfa/awus036acx/) | MT7612U | 0e8d:7612 | mt76x2u（內建核心）|
| [AWUS036AX](/zh-tw/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK driver (<6.14)|
| [AWUS036AXML](/zh-tw/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u（核心 5.18+）|
| [AWUS1900](/zh-tw/products/alfa/awus1900/) | RTL8814AU | 0bda:8813 | morrownr/8814au |

### 用 lsusb 確認網路卡型號

插入網路卡後執行：

```bash
lsusb
```

輸出範例：

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
Bus 003 Device 004: ID 0bda:8813 Realtek Semiconductor Corp. RTL8814AU 802.11a/b/g/n/ac
```

將 `ID xx:xx` 的值對照上方表格，確認你的晶片組。

---

## 準備系統環境

無論你的晶片組是哪一種，請先安裝通用的編譯相依套件：

**Kali Linux：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04：**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

確認標頭檔已針對目前執行的核心安裝完成：

```bash
uname -r
# 範例：6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# 應該存在——若不存在，表示標頭檔未安裝
```

---

## RTL8812AU 驅動程式（AWUS036ACH、AWUS036ACHM）

RTL8812AU 需要非主線驅動程式。目前有兩個由社群維護的 fork 可供選擇，依作業系統決定。

### 方案 A：aircrack-ng/rtl8812au（Kali Linux — 推薦）

此 fork 由 Aircrack-ng 團隊維護，對 Kali 有明確的相容性支援，並針對封包注入做了最佳化：

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

確認介面是否出現：

```bash
ip link show | grep wlan
# 應顯示 wlan0 或類似名稱
```

### 方案 B：morrownr/8812au-20210708（Ubuntu 24.04 — 推薦）

morrownr fork 針對 Ubuntu 最佳化，內含整合 DKMS 的便利安裝腳本：

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

安裝腳本會自動處理 DKMS 註冊。執行完成後：

```bash
# 重新開機以載入新模組
sudo reboot

# 重開機後確認
lsmod | grep 8812au
```

### 手動 DKMS 註冊（任一 fork 皆適用）

如果你偏好手動控制：

```bash
# 複製驅動程式（使用任一 fork）
git clone https://github.com/aircrack-ng/rtl8812au

# 從 Makefile 取得版本號
grep "^MODULE_VERSION" rtl8812au/Makefile
# 記下版本，例如 v5.6.4.2 → 使用 5.6.4.2

# 將原始碼複製到 DKMS 目錄
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# 註冊、編譯、安裝
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# 確認
dkms status
# 預期結果：rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### 安裝成功後的 lsusb 與 lsmod 輸出

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## MT7612U 驅動程式（AWUS036ACM、AWUS036ACX）

MT7612U 晶片組是四款中最容易設定的，因為它的驅動程式自 Linux 核心 **4.19** 起就已內建。在 Kali Linux 2022+ 和 Ubuntu 20.04+ 上，完全不需要另外安裝驅動程式。

### 確認核心版本

```bash
uname -r
```

只要輸出為 4.19 或以上（任何現代 Kali 或 Ubuntu 皆符合），`mt76x2u` 模組就已可用。

### 載入模組

```bash
sudo modprobe mt76x2u
```

確認已載入：

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

無線介面應立即出現：

```bash
ip link show
# wlan0: ...
```

### 設定開機自動載入模組

大多數系統偵測到網路卡時會自動載入模組。若要明確確保開機時載入：

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### 無需編譯

這是 MT7612U 晶片組的最大優勢：完全不需要編譯、不需要驅動程式原始碼、也不依賴核心標頭檔。在所有受支援的發行版上都能直接使用。對於不想花時間管理驅動程式的用戶，[AWUS036ACM](/zh-tw/products/alfa/awus036acm/) 是目前最即插即用的滲透測試網路卡。

---

## MT7921AUN 驅動程式（AWUS036AXM、AWUS036AXML — Wi-Fi 6E）

MT7921AUN 是 MediaTek 的 Wi-Fi 6E 晶片組。其 Linux 驅動程式 `mt7921u` 已在核心 **5.18 版**被合併進主線。

### 確認核心版本

```bash
uname -r
```

**Kali Linux 2022.2 及以後版本**預裝核心 5.18 或更新——已支援。
**Ubuntu 22.04 LTS** 預裝核心 5.15——**不支援**，需升級核心。
**Ubuntu 24.04 LTS** 預裝核心 6.8——完整支援。

### 載入模組（核心 5.18+）

```bash
sudo modprobe mt7921u
```

確認：

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04：核心升級路徑

如果你使用的是 Ubuntu 22.04 搭配核心 5.15，有兩種選擇：

**方案 A：HWE 核心**（推薦）

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

Ubuntu 22.04 的 HWE（硬體啟用）核心為 6.2+，支援 mt7921u。

**方案 B：升級至 Ubuntu 24.04**

Ubuntu 24.04 LTS 預裝核心 6.8，完整支援 mt7921u。這是最乾淨的長期解決方案。

### Wi-Fi 6E 與監聽模式現況

截至 2026 年，mt7921u 驅動程式在 2.4 GHz、5 GHz 和 6 GHz 頻段上的受管理模式（連線至網路）已穩定運作。2.4 GHz 和 5 GHz 的監聽模式功能正常。**6 GHz 監聽模式**仍在持續完善中——在用於 6 GHz 評估前，請先確認 `mt76` 核心驅動程式 issue tracker 上的最新狀態。

---

## RTL8814AU 驅動程式（AWUS1900）

RTL8814AU 搭載於 [AWUS1900](/zh-tw/products/alfa/awus1900/)——ALFA 功率最強的網路卡，配備四根天線並支援 AC1900 規格。它需要來自 `morrownr/8814au` 儲存庫的非主線驅動程式。

### 安裝方式

```bash
git clone https://github.com/morrownr/8814au
cd 8814au
sudo ./install-driver.sh
```

安裝腳本已整合 DKMS。安裝完成後重新開機：

```bash
sudo reboot
```

重開機後確認：

```bash
lsmod | grep 8814au
# 8814au    3825664  0

ip link show | grep wlan
# wlan0: ...
```

### 手動編譯（不使用 install-driver.sh）

```bash
make
sudo make install
sudo modprobe 88XXau_btcoex
```

注意：RTL8814AU 的模組名稱為 `88XXau_btcoex`（或依 fork 版本為 `8814au`）。安裝後使用 `lsmod | grep 88` 確認正確名稱。

---

## DKMS：核心更新後保持驅動程式正常運作

Kali Linux 和 Ubuntu 都會定期更新核心。若未使用 DKMS，每次核心更新後非主線驅動程式（RTL8812AU、RTL8814AU）就會失效，直到你手動重新編譯為止。

正確設定 DKMS 後，執行 `apt upgrade` 時重新編譯會自動完成。

### 確認 DKMS 正在管理你的驅動程式

```bash
dkms status
```

正確管理的輸出範例：

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### 核心更新時的流程

```
apt upgrade
→ 下載新核心套件
→ 觸發 DKMS hook
→ 針對新核心重新編譯 rtl8812au 原始碼
→ 安裝新的 .ko 檔案
→ 系統重開機進入新核心
→ 驅動程式自動載入
```

若 DKMS 在更新過程中失敗（透過 `dkms status` 顯示「built」但非「installed」），手動重新安裝：

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## 除錯

| 症狀 | 可能原因 | 解決方法 |
|---|---|---|
| 插入後沒有出現 wlan 介面 | 驅動程式未載入 | `sudo modprobe 88XXau` 或 `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | 驅動程式未針對當前核心編譯 | 重新編譯驅動程式或執行 `sudo dkms install` |
| 介面出現後數秒消失 | 電源管理干擾 | `sudo iwconfig wlan0 power off` |
| `make` 失敗：「linux/module.h not found」 | 核心標頭檔未安裝 | `sudo apt install linux-headers-$(uname -r)` |
| `make` 失敗：版本不符 | 標頭檔與執行中的核心不符 | 對照 `uname -r` 與 `ls /lib/modules`，重新安裝對應標頭檔 |
| lsusb 顯示裝置但沒有介面 | 模組已載入但未建立介面 | 執行 `dmesg \| tail -30` 查看錯誤訊息 |
| 監聽模式失敗：「Operation not supported」 | 驅動程式版本不支援監聽模式 | 改用 aircrack-ng fork，而非發行版內建的驅動程式 |
| aireplay-ng 注入測試：0% | 介面未進入監聽模式 | 用 `iwconfig` 確認，重新執行 `airmon-ng start` |
| 驅動程式正常但重開機後失效 | 模組未加入 initramfs | `sudo update-initramfs -u` 或使用 DKMS |
| 核心更新後 DKMS 編譯失敗 | 新核心缺少標頭檔 | `sudo apt install linux-headers-$(uname -r)` |

### 詳細診斷指令

```bash
# 檢查所有已載入的無線模組
lsmod | grep -E "8812|8814|mt76|mt79"

# 查看 USB 和無線相關的核心訊息
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# 列出所有無線介面
iw dev

# 查看特定介面使用的驅動程式
ethtool -i wlan0 | grep driver

# 查看 USB 裝置詳細資訊
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# 確認所有已註冊模組的 DKMS 狀態
dkms status
```

---

## 快速查詢：哪款網路卡用哪個驅動程式

| 你的網路卡 | 晶片組 | Kali Linux | Ubuntu 24.04 |
|---|---|---|---|
| [AWUS036ACH](/zh-tw/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` | `morrownr/8812au-20210708` |
| [AWUS036ACM](/zh-tw/products/alfa/awus036acm/) | MT7612U | 內建（`mt76x2u`）| 內建（`mt76x2u`）|
| [AWUS036AX](/zh-tw/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | N/A |
| [AWUS036AXML](/zh-tw/products/alfa/awus036axml/) | MT7921AUN | 內建（`mt7921u`，核心 5.18+）| 內建（`mt7921u`，核心 6.8）|
| [AWUS1900](/zh-tw/products/alfa/awus1900/) | RTL8814AU | `morrownr/8814au` | `morrownr/8814au` |

---

## 確保購買到原廠正品

驅動程式問題有時源自仿冒品——這類產品可能回報錯誤的 USB ID，或使用與標示不符的劣質晶片組。從授權經銷商購買的正品 ALFA Network 網路卡，其行為與本文說明完全一致。

Yopitek 是 ALFA Network 的授權經銷商。歡迎瀏覽完整的 [ALFA Network 產品目錄](/zh-tw/products/alfa/)，確保你購買到附原廠保固、驅動程式相容性有保障的正品硬體。

---

## 總結

Linux WiFi 驅動程式安裝有一套簡單的決策流程：

1. **用 `lsusb` 搭配上方對照表確認晶片組**
2. **MT7612U 或 MT7921AUN（核心 5.18+）？** → 執行 `modprobe`，完成
3. **RTL8812AU 或 RTL8814AU？** → Clone 對應儲存庫，執行 `make && sudo make install`，啟用 DKMS 確保持久運作
4. **有問題？** → 查看除錯表、確認標頭檔與核心版本一致、檢查 `dmesg`

ALFA Network 網路卡的優勢在於：四款主要晶片組都有文件完整、積極維護的驅動程式解決方案，不會讓你陷入無支援的困境。
