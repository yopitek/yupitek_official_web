---
title: "ALFA AWUS036ACH 安裝教學：Kali Linux 監聽模式與封包注入完整設定"
description: "ALFA AWUS036ACH 在 Kali Linux 上的完整安裝教學，包含 RTL8812AU 驅動程式安裝、airmon-ng 啟用監聽模式、封包注入測試與常見問題排解。"
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "監聽模式", "封包注入", "RTL8812AU", "airmon-ng"]
---

## 前言

ALFA AWUS036ACH 搭載 Realtek **RTL8812AU** 晶片組，長期以來是 Kali Linux 無線滲透測試社群中評價最高、使用最廣泛的 USB 無線網卡之一。它同時支援 2.4 GHz 與 5 GHz 雙頻、具備完整的監聽模式（Monitor Mode）與封包注入（Packet Injection）能力，加上 aircrack-ng 官方維護的開源驅動，幾乎成為所有 Wi-Fi 安全教學的標配器材。

本教學將從零開始，帶你完成 AWUS036ACH 在 Kali Linux 上的完整安裝與設定流程，包含驅動安裝、監聽模式啟用、封包注入測試，以及常見問題的排解方法。

---

## 系統需求

在開始之前，請確認你的環境符合以下條件：

| 項目 | 需求 |
|------|------|
| 作業系統 | Kali Linux 2024.x 或更新版本 |
| USB 接埠 | USB 3.0（建議，向下相容 USB 2.0 但效能較低） |
| 核心版本 | Linux kernel 5.x 以上 |
| 磁碟空間 | 至少 500 MB 可用空間（用於驅動編譯） |
| 網路連線 | 安裝驅動期間需要網際網路連線 |
| 權限 | 需要 sudo 管理員權限 |

> **重要提示**：本教學中的所有無線測試指令，僅限用於你擁有合法授權的網路環境。未經授權對他人網路進行測試是違法行為。

---

## 步驟 1：連接網卡並確認偵測

將 AWUS036ACH 插入電腦的 USB 接埠後，先確認系統是否正確識別到設備。

### 使用 lsusb 確認 USB 裝置

```bash
lsusb
```

在輸出結果中，應可看到類似以下的行：

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

關鍵識別碼為 `0bda:8812`，其中 `0bda` 是 Realtek 的廠商 ID，`8812` 對應 RTL8812AU 晶片。

### 確認核心訊息

```bash
dmesg | grep -i "rtl\|usb" | tail -20
```

若驅動尚未安裝，你可能會看到「driver not found」或類似的訊息，這是正常現象，我們將在下一步安裝驅動。

---

## 步驟 2：安裝 RTL8812AU 驅動程式

RTL8812AU 的驅動程式需要手動安裝，以下提供兩種方法，建議新手優先選擇方法二（DKMS），以確保核心更新後驅動仍可持久使用。

### 方法一：aircrack-ng 官方版（Kali Linux 推薦）

這是 aircrack-ng 專案維護的驅動版本，針對滲透測試功能進行了優化，是 Kali Linux 官方推薦的安裝方式。

```bash
# 步驟 2-1：更新套件清單並安裝必要工具
sudo apt update
sudo apt install -y git dkms build-essential linux-headers-$(uname -r)

# 步驟 2-2：複製 aircrack-ng 官方驅動倉庫
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 步驟 2-3：編譯驅動
make

# 步驟 2-4：安裝驅動
sudo make install

# 步驟 2-5：載入核心模組
sudo modprobe 88XXau
```

### 方法二：DKMS 安裝（跨核心更新持久化，強烈推薦）

DKMS（Dynamic Kernel Module Support）可確保每次核心更新後，驅動程式自動重新編譯，避免升級後需要手動重裝的麻煩。

```bash
# 步驟 2-1：安裝必要套件
sudo apt update
sudo apt install -y git dkms build-essential linux-headers-$(uname -r)

# 步驟 2-2：複製驅動倉庫
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 步驟 2-3：使用 DKMS 安裝
sudo make dkms_install

# 步驟 2-4：確認 DKMS 模組狀態
dkms status
```

成功安裝後，`dkms status` 輸出應包含類似 `88XXau/5.6.4.2, 6.x.x-kali, x86_64: installed` 的行。

### 驗證驅動安裝成功

```bash
# 確認模組已載入
lsmod | grep 88XXau

# 查看網路介面
ip link show
# 或使用舊式指令
iwconfig
```

此時應可看到新的無線介面，通常命名為 `wlan0` 或 `wlan1`（取決於系統上已有的介面數量）。

---

## 步驟 3：啟用監聽模式

監聽模式是 Wi-Fi 安全測試的核心功能，有兩種主要啟用方法：

### 方法一：使用 airmon-ng（推薦）

`airmon-ng` 是 aircrack-ng 套件中的標準工具，可自動處理監聽模式切換的相關細節。

```bash
# 首先，停止可能干擾的行程
sudo airmon-ng check kill

# 啟用監聽模式（將 wlan0 替換為你的實際介面名稱）
sudo airmon-ng start wlan0
```

成功啟用後，你會看到類似以下輸出：

```
PHY     Interface   Driver      Chipset

phy1    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)
                (mac80211 station mode vif disabled for [phy1]wlan0)
```

監聽模式介面通常會在原介面名稱後加上 `mon`，例如 `wlan0mon`。

### 方法二：使用 iw 指令

如果偏好手動控制，可以使用 `iw` 指令：

```bash
# 先關閉介面
sudo ip link set wlan0 down

# 切換至監聽模式
sudo iw dev wlan0 set type monitor

# 重新啟用介面
sudo ip link set wlan0 up
```

---

## 步驟 4：確認監聽模式已啟用

使用 `iwconfig` 確認介面已成功切換至監聽模式：

```bash
iwconfig
```

在輸出中，找到你的無線介面，應看到 `Mode:Monitor` 欄位：

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

`Mode:Monitor` 確認監聽模式已成功啟用。

你也可以使用 `airodump-ng` 快速測試，確認能夠掃描到附近的無線網路：

```bash
sudo airodump-ng wlan0mon
```

若能看到附近的 BSSID 清單，代表監聽模式運作正常。按 `Ctrl+C` 停止掃描。

---

## 步驟 5：封包注入測試

確認封包注入功能正常運作，使用 `aireplay-ng` 的測試模式：

```bash
sudo aireplay-ng --test wlan0mon
```

正常輸出應類似：

```
12:34:56  Trying broadcast probe requests...
12:34:56  Injection is working!
12:34:57  Found 3 APs

12:34:57  Trying directed probe requests...
12:34:57  XX:XX:XX:XX:XX:XX - channel: 6 - 'NetworkName'
12:34:58   30/30: 100%
```

`Injection is working!` 訊息確認封包注入功能正常。若測試成功率低於 80%，可能需要調整天線位置或檢查干擾源。

### 指定頻道測試

若要針對特定頻道或頻段進行注入測試：

```bash
# 指定 5 GHz 頻段（頻道 36）
sudo aireplay-ng --test -c 36 wlan0mon
```

---

## 常見問題排解

### 問題 1：找不到無線介面

**症狀**：`iwconfig` 或 `ip link show` 沒有顯示新的無線介面。

**排解步驟**：
```bash
# 確認 USB 裝置已被識別
lsusb | grep -i realtek

# 確認驅動模組已載入
lsmod | grep 88XXau

# 若模組未載入，手動載入
sudo modprobe 88XXau

# 查看核心訊息以獲取更多線索
dmesg | tail -30
```

若 `lsusb` 找不到裝置，請嘗試更換 USB 埠，或確認網卡連接是否穩固。

---

### 問題 2：驅動未載入或載入失敗

**症狀**：`modprobe 88XXau` 報錯，或 `dmesg` 顯示驅動錯誤。

**排解步驟**：
```bash
# 確認核心標頭已安裝
sudo apt install -y linux-headers-$(uname -r)

# 重新編譯驅動
cd rtl8812au
make clean
make
sudo make install
sudo modprobe 88XXau
```

若問題持續，確認 `uname -r` 顯示的核心版本與安裝的 `linux-headers` 版本一致。

---

### 問題 3：NetworkManager 干擾監聽模式

**症狀**：啟用監聽模式後，介面自動切回 Managed 模式，或 `airmon-ng` 提示有行程干擾。

**排解步驟**：
```bash
# 查看干擾行程
sudo airmon-ng check

# 停止 NetworkManager 與 wpa_supplicant
sudo airmon-ng check kill

# 或手動停止
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

測試完成後，記得重新啟動 NetworkManager：
```bash
sudo systemctl start NetworkManager
```

---

### 問題 4：封包注入測試成功率低

**症狀**：`aireplay-ng --test` 顯示成功率低於 50%。

**排解步驟**：
1. 調整天線方向與位置，靠近目標 AP
2. 確認網卡的 TX Power 設定（`iwconfig wlan0mon txpower 30`）
3. 嘗試更換 USB 埠，確保供電充足（建議使用 USB 3.0）
4. 若使用 USB Hub，改用直接連接到主機的 USB 埠

---

## 恢復正常模式

測試完成後，將網卡切換回一般 Managed 模式並重啟網路管理：

```bash
# 使用 airmon-ng 停止監聽模式
sudo airmon-ng stop wlan0mon

# 重啟 NetworkManager
sudo systemctl start NetworkManager
```

---

## 產品資訊

ALFA AWUS036ACH 由台灣授權代理商**榆閤科技（Yopitek）**在台灣獨家代理銷售，提供原廠保固與中文技術支援。

👉 [查看 AWUS036ACH 產品頁面](/zh-tw/products/alfa/awus036ach/)

👉 [查看 ALFA Network 全系列產品](/zh-tw/products/alfa/)

---

## 小結

完成本教學後，你已成功在 Kali Linux 上設定好 ALFA AWUS036ACH，具備了執行 Wi-Fi 安全測試的基礎能力：

- ✅ RTL8812AU 驅動程式安裝（支援 DKMS 持久化）
- ✅ 監聽模式啟用（airmon-ng 與 iw 兩種方法）
- ✅ 封包注入功能驗證
- ✅ 常見問題排解方法

有了正確運作的無線網卡，你可以進一步學習使用 `airodump-ng`、`aireplay-ng`、`aircrack-ng` 等工具，探索 Wi-Fi 安全的更多面向。記得所有測試必須在合法授權的環境中進行。
