---
title: "SDRLab Flipper Zero 5G 擴充板 — 雙頻 Wi-Fi 安全研究模組"
seo_title: "Flipper Zero 5G 擴充板 SDRLab 台灣 | Yopitek"
description: "Flipper Zero 5G 擴充板，ESP32-C5 雙頻 2.4/5 GHz Wi-Fi、433 MHz 模組、主動 GPS、2.8 吋螢幕，可向 Yopitek 詢價。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 擴充", "5GHz", "Wi-Fi", "Deauth", "資安研究"]
faq:
  - question: "SDRLab Flipper Zero 5G 擴充板使用什麼晶片與 Wi-Fi 頻段？"
    answer: "採用 Espressif ESP32-C5，支援 2.4 GHz 與 5 GHz 雙頻 Wi-Fi，出廠預燒 ESP32 Marauder 5G 韌體。"
  - question: "Flipper Zero 5G 擴充板附哪些天線？"
    answer: "附四支天線：2.4G、2.4G/5G 雙頻、433M 與 GPS，各自對應獨立 SMA 介面。Wi-Fi 天線為 3 dBi（11 cm），433M 天線為 3 dBi，GPS 天線為 20 dBi。"
  - question: "接上 Flipper Zero 後需要做哪些設定？"
    answer: "在 GPIO 腳位設定中，將 GPS Pin 設為 13 或 14、ESP32 Pin 設為 15、16，並把 Sub-GHz 模組設為 External。GPS 與 ESP32 使用不同的 UART 腳位，不可設成同一組。"
  - question: "套件是否包含 Flipper Zero 主機？可搭配哪些韌體？"
    answer: "不包含，Flipper Zero 主機需另購。本板相容 Momentum、Unleashed、Xtreme 等自訂韌體，僅限用於授權的資安研究。"
---


# SDRLab Flipper Zero 5G 擴充板 — 雙頻 Wi-Fi 安全研究模組

> **合法使用聲明**：本擴充板僅供授權的資安研究及合法研究使用。對未經你擁有或未取得書面授權的網路、裝置或基礎設施進行測試，在多數國家均屬違法行為。請確認符合當地無線頻率使用法規，並負責任、合乎倫理地使用本產品。


Flipper Zero 5G 擴充板供授權資安研究，含 ESP32-C5 雙頻 2.4/5 GHz Wi-Fi、433 MHz、主動 GPS。歡迎聯絡 Yopitek 取得台灣報價。

## 一、這是什麼

一塊裝在 Flipper Zero 背面 GPIO 排針上的無線研究擴充板。把你手裡那台只有 2.4GHz 的 Flipper，一次補齊三種無線能力：

- **Wi-Fi 雙頻 2.4GHz + 5GHz**
- **433MHz Sub-GHz** 射頻
- **主動 GPS**

外加一塊 **2.8 吋彩色 TFT 螢幕**、**800mAh 可熱插拔電池**、**四組 SMA 天線介面與四支天線全附**，以及**出廠預燒好的 ESP32 Marauder 5G 韌體**。

不需要買刷機器、不需要自己編譯韌體。接上、設定三個參數，就能開始用。


## 二、產品特色

### 三種無線一次到位
- **Wi-Fi 雙頻 2.4GHz + 5GHz** — 掃描現代 5GHz 網路，補足舊板只能看 2.4GHz 的限制
- **433MHz Sub-GHz（A07 射頻模組，10 dBm）** — 讓 Flipper 內建收訊不良的環境多一個選擇
- **主動 GPS** — wardrive 記錄可以自動加上座標，接上 Flipper 時由主機供電、脫離時自動切換內建電池

### 2.8 吋彩色 TFT 螢幕
掃描結果、訊號強度、電量直接顯示在板上，不用盯著電腦終端機猜。內建 Marauder UI。

### 四組 SMA 天線介面，四支天線全附
背殼絲印清楚標示四個介面對應關係：

| 絲印 | 位置 | 用途 |
|---|---|---|
| `433M A` | 上緣左 | 433MHz 射頻（A07 模組，10 dBm） |
| `GPS` | 上緣右 | 主動 GPS 天線 |
| `2.4G` | 左翼 | Wi-Fi 2.4GHz |
| `2.4G/5G` | 右翼 | Wi-Fi 雙頻 2.4GHz + 5GHz |

四個介面為獨立的螺絲固定式 SMA 母座，**四支天線皆隨貨附上**：Wi-Fi 天線 3 dBi（11 cm）、433M 天線 3 dBi、GPS 天線 20 dBi。

### 800mAh 熱插拔電池
出機箱就內建 800mAh 鋰聚合物電池。可以脫離 Flipper 單機開機抓封包，掃完再插回主機當擴充板用。

### 出廠預燒 Marauder 5G 韌體
開箱即用，不需要另外購買刷機器。板上保留 USB-C 燒錄口，供進階使用者自行升級韌體。

### 金手指 + TVS 突波保護
所有訊號腳位鍍金，每腳內建 TVS 瞬態電壓抑制二極體，插拔 Flipper 時提供突波保護。

### 韌體生態相容
適用 Momentum、Unleashed、Xtreme 等含 WiFi Marauder 與 GPS 應用的客製韌體。


## 三、產品規格

| 規格項目 | 數值／說明 |
|---|---|
| **主晶片** | **Espressif ESP32-C5** |
| **Wi-Fi 頻段** | 2.4GHz + 5GHz 雙頻 |
| **Wi-Fi 天線介面** | **4 組 SMA 母座**：433M A／GPS／2.4G／2.4G+5G，**四支天線全附**：Wi-Fi 3 dBi（11 cm）、433M 3 dBi、GPS 20 dBi |
| **Sub-GHz** | 433MHz A07 射頻模組，**10 dBm** 輸出 |
| **GNSS** | 主動 GPS 模組，**自動切換供電**（接主機用主機電源、脫離用內建電池） |
| **螢幕** | **2.8 吋彩色 TFT**，內建 Marauder UI |
| **電池** | **800 mAh 鋰聚合物**，可熱插拔 |
| **連接介面** | Flipper Zero 標準 GPIO 排針（**2×8 針**），金手指 + 每腳 TVS 保護 |
| **預載韌體** | **ESP32 Marauder 5G**（開源，出廠預燒） |
| **韌體相容** | Momentum、Unleashed、Xtreme |

### 隨附配件
- 主機 ×1（已組裝，含外殼與 2.8 吋螢幕）
- 天線 ×4 — `2.4G`／`2.4G+5G` 雙頻／`433M A`／`GPS` 各 1 支（Wi-Fi 3 dBi／433M 3 dBi／GPS 20 dBi）
- Flipper GPIO 排針連接

### 需另行購買
- **Flipper Zero 主機**（本板為擴充板，不含主機）


## 四、開始使用：三個必設參數

本板出廠已燒好韌體，不需要刷寫。接上 Flipper 之後只需要設定三組腳位：

| 功能 | 設定路徑 | 值 |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 或 14** |
| **ESP32（WiFi / Marauder）** | 同上 → **ESP32 Pin** | **15、16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS 與 ESP32 是兩組不同的 UART 腳位，不可設成同一組**，否則 GPS 與 Wi-Fi 都會沒有反應。

設定完成後重新啟動 Flipper，進入 `Apps → GPIO` 即可看到對應的 WiFi Marauder 與 GPS 應用程式。


## 五、應用環境

- **雙頻 Wi-Fi 掃描** — 被動枚舉 2.4GHz 與 5GHz 網路；擷取 SSID、BSSID、頻道、RSSI、加密類型及連線客戶端
- **WPA 握手包擷取** — 嗅探 EAPOL／PMKID 握手封包，用於已授權網路的安全稽核
- **Deauth 測試** — 傳送 Deauth 封包測試網路韌性，僅限自有或已授權網路
- **Wardrive 網路拓撲映射** — GPS 標記的 Wi-Fi 與裝置記錄，輸出 CSV 供後續分析
- **433MHz 射頻研究** — 透過 Flipper 的 Sub-GHz 選單操作，適合評估 Flipper 內建收訊不良的環境
- **Evil Portal 演練** — 在授權環境下原型設計測試入口頁
- **IoT 無線協定研究** — 在受控實驗環境分析 IoT 裝置在雙頻上的行為


## 六、已知限制（請務必留意）

- **5GHz Deauth 的穩定度取決於韌體版本**。開源 Marauder 韌體在 ESP32-C5 上對 5GHz deauth 的支援仍在持續改進中，建議以 **2.4GHz** 進行 deauth 測試為主；5GHz 建議以掃描、訊號監測、wardrive 記錄為主要用途。實際表現請以當下韌體版本實測為準。
- **GPS 天線具方向性**，雖然商品標示為全向天線。天線請朝向開闊天空方向放置以取得定位，首次冷啟動需要數分鐘下載衛星星曆資料。室內效果較差，建議到戶外或靠窗使用。
- **GPS 回報時間為 UTC+0**，韌體選單中沒有時區設定選項。台灣時間（UTC+8）請自行加 8 小時。
- **GPS 與 ESP32 是兩組不同的 UART 腳位**（GPS：13 或 14；ESP32：15、16），兩者不可設成同一組，否則 GPS 與 Wi-Fi 都會無回應。
- **韌體燒錄埠** — 正面左側的 USB-C 埠供燒錄韌體使用。
- **GPS 自動切換供電** — 接在 Flipper 上時由主機供電，脫離後改用內建電池，切換瞬間可能有短暫重啟，屬正常現象。


**產品頁連結**：https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**完整使用手冊**：https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/
**原廠商店頁（OpenSourceSDRLab）**：https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754

{{< faq >}}
