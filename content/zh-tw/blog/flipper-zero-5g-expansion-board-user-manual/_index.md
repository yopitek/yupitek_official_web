---
title: "Flipper Zero 5G Expansion Board 圖解安裝與使用手冊 (v2.0)"
description: "本指南為 Flipper Zero 5G 擴充模組安裝與操作指引 v2.0，配有完整高清 isometric 工程設計圖，帶領新手無痛安裝天線、插槽及 GPIO 設定。"
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Flipper Zero 5G Expansion Board 圖解安裝與使用手冊 (v2.0)

> **目標讀者**：完全沒有接觸過本模組的新手客戶。  
> **編寫原則**：針對所有「容易出錯」或「術語難懂」的步驟提供高清設計圖解，告別文字猜測，實現一步一圖的無痛安裝。

---

## 00. 開箱與配件清單

歡迎使用 Flipper Zero 5G 擴充模組！在開始前，請先確認您的包裝內包含以下配件。

![開箱全家福與配件圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*圖 1：開箱配件全家福*

### ⚠️ 配件清單說明
*   **標配包含**：
    1.  5G 擴充板主模組 (5G Expansion Board) x 1
    2.  433MHz 棒狀天線 (短黑天線) x 1
    3.  GPS 陶瓷主動式天線 (正方形天線) x 1
    4.  WiFi 雙頻貼片天線 (黑色扁平天線) x 1
*   **不包含 (需自行準備)**：
    *   **Flipper Zero 主機** (本模組不附帶主機)
    *   **MicroSD 記憶卡** (模組運作必需，需自行購買)

---

## 01. 認識你的 5G 模組

在插上天線或連接主機前，請先花一分鐘熟悉模組上的各個關鍵介面與硬體佈局。

### 正面介面說明

![模組正面標註圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*圖 2：正面硬體配置標註*

*   **螢幕 (LCD Screen)**：顯示目前的連接狀態、IP 位址與運作模式。
*   **撥動開關 (Toggle Switch)**：控制模組螢幕的電源，往上撥為開啟。
*   **MicroSD 卡槽 (SD Card Slot)**：用於儲存系統韌體設定與 Log 資料。
*   **GPIO 插槽**：與 Flipper Zero 主機頂部對接的母座。
*   **指示燈 (LED Indicators)**：顯示電源與充電狀態。

### 側面天線埠說明

![側面天線埠標註圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*圖 3：天線埠位置與功能印刷*

*   **433M A**：連接 433MHz 棒狀天線。
*   **GPS**：連接 GPS 陶瓷天線。
*   **2.4G** 與 **2.4G/5G**：連接 WiFi 雙頻貼片天線。

> ⚠️ **出貨批次版本重要提醒**：  
> 天線埠位置會依據生產批次而有微幅調整（如 GPS 與 WiFi 連接口位置可能左右對調）。**請務必以您手上模組外殼上的實際印刷標籤為準**，切勿單憑記憶盲插，以免訊號不佳或損壞硬體。

---

## 02. 安裝步驟指引 (Step-by-Step)

### Step 1 | 準備與安裝 MicroSD 記憶卡

5G 模組需要一張記憶卡來儲存設定。

1.  **規格要求**：容量為 **32GB 以下**，格式必須為 **FAT32**。
2.  **卡片方向**：請金屬接腳朝下，插入 MicroSD 卡槽內，輕壓至卡住。

![MicroSD 卡插槽特寫](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*圖 4：MicroSD 卡正確插入方向特寫*

---

### Step 2 | 安裝三根天線

請將標配的三根天線鎖入對應的 SMA 天線接頭。注意不要用力過猛，轉至緊貼即可。

![天線安裝接線圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*圖 5：三種天線鎖附與對接路徑示意*

| 天線類型 | 對應天線埠 | 安裝說明 |
| :--- | :--- | :--- |
| **GPS 陶瓷天線** | **GPS 埠** | 接頭為正方形陶瓷座，帶有長線 |
| **WiFi 雙頻貼片天線** | **2.4G/5G 埠** | 黑色扁平貼片天線 |
| **433MHz 棒狀天線** | **433M A 埠** | 黑色短棒狀硬天線 |

#### ⚠️ GPS 天線擺放方向警告
GPS 天線具有方向性。安裝時，**陶瓷面 (通常有黏貼雙面膠的反面，或無文字面) 必須朝上 (面向天空)**，否則將無法成功定位！

![GPS 天線朝向對比圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*圖 6：GPS 天線正確 (朝天) 與錯誤 (朝地) 擺放對比*

---

### Step 3 | 與 Flipper Zero 主機對接

將 5G 模組插入 Flipper Zero 頂部的 GPIO 針腳。

1.  請先**將 Flipper Zero 關機**，以防熱插拔造成硬體損壞。
2.  對齊 Flipper Zero 頂部的 GPIO 針腳與模組底部的插槽。

![GPIO 對接 alignment 圖](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*圖 7：GPIO 對接位置與對齊線*

3.  雙手均勻施力，將模組**輕壓到底**。
4.  **檢查平整度**：完成後，請從側面觀察，模組與 Flipper Zero 之間應**完全貼合、沒有任何縫隙**。

![GPIO 插入貼合度確認](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*圖 8：完全插入且無縫隙的正確對接狀態*

---

### Step 4 | Flipper Zero 軟體設定

對接完成後，將 Flipper Zero 開機，接著進行軟體針腳 (GPIO Pin) 設定。

以 **Momentum 韌體** 為例，請至以下路徑進行設定：

1.  **開啟螢幕電源**：將模組左前方的撥動開關撥至 **UP** 位置。
    ![螢幕撥動開關 UP 特寫](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *圖 9：螢幕撥動開關切換至 UP 位置以開啟顯示*

2.  **GPS Pin 設定**：
    *   路徑：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   設定值：改為 **13** 或 **14** (依手冊或硬體出貨說明)。
3.  **ESP32 Pin 設定 (WiFi/藍牙功能)**：
    *   路徑：`Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   設定值：改為 **15, 16**。
4.  **433MHz 射頻模組設定**：
    *   進入 `Sub-GHz` ➔ `Advanced Settings` ➔ 將 Module 改為 **External** (啟用外接天線)。

---

### Step 5 | 充電與電量檢查

本模組內建可充電式電池。

![USB-C 介面對比與警告](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*圖 10：上方充電專用孔 (CHARGE ONLY) 與側面燒錄專用孔 (FLASH ONLY) 對照*

*   **頂部 USB-C 埠**：**僅供充電使用** (標示有 CHARGE ONLY)。請務必插在此孔進行充電！
*   **側面 USB-C 埠**：**僅供韌體燒錄使用** (標示有 FLASH ONLY)。切勿用於日常充電，否則無法補充電力。

#### 電量 LED 指示燈狀態：
模組正面有 4 顆電量指示燈，代表不同的剩餘電量百分比：

![電量指示燈圖解](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*圖 11：4 顆 LED 燈對應的剩餘電量*

*   1 顆燈亮：電量約 25% (請儘速充電)
*   2 顆燈亮：電量約 50%
*   3 顆燈亮：電量約 75%
*   4 顆燈亮：電量 100% (已充滿)

---

## 03. 常見錯誤自我檢查表 (新手疑難排解)

如果您的模組無法正常運作，請逐一檢查以下項目：

*   [ ] **GPIO 針腳是否完全插到底？** (模組與 Flipper Zero 頂部應無縫隙貼合，參考圖 8)
*   [ ] **GPS 天線方向是否正確？** (陶瓷面必須面朝天空，參考圖 6)
*   [ ] **天線是否鎖錯孔？** (不同批次的位置可能不同，請核對外殼文字印刷，參考圖 3)
*   [ ] **MicroSD 卡規格是否符合？** (容量需 32GB 以下，且格式為 FAT32，參考圖 4)
*   [ ] **螢幕開關是否已撥至 UP？** (參考圖 9)

---

## 04. 韌體升級與燒錄 (進階功能)

當官方發布新版韌體時，您需要透過側面 USB-C 埠進行韌體燒錄。

1.  準備一條連接至電腦的 USB-C 線。
2.  **關鍵步驟**：在將線插入模組**側面 USB-C 埠 (FLASH ONLY)** 的同時，**按住模組背面/右側的燒錄按鍵**，使晶片進入 Boot 燒錄模式。

![韌體燒錄按鍵與插入順序](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*圖 12：按住燒錄鍵並同時插入 USB 傳輸線的步驟示意*
