---
title: "Flipper Zero 入門教學：開箱設定、韌體更新與五大實用功能"
locale: "zh-TW"
hreflang_group: "flipper-zero-beginners-guide-setup-tutorial"
description: "Flipper Zero 是什麼？從開箱、microSD 設定、qFlipper 韌體更新，到 RFID／Sub-GHz／NFC／IR／BadUSB 五大功能實測，一篇帶你完成 Flipper Zero 入門。"
date: 2026-08-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-beginners-guide-setup-tutorial"
tags: ["TW", "zero-beginners-guide-setup-tutorial", "zero-beginners-guide-setup-tutorial", "08-10", "Flipper Zero", "Tutorial", "zero/hero.webp", "GHz／NFC／IR／BadUSB 五大功能實測，一篇帶你完成 Flipper Zero 入門。"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-08-10
---


# Flipper Zero 入門教學：開箱設定、韌體更新與五大實用功能

> TL;DR：Flipper Zero 是一台掌上型的硬體探索工具，內建 125 kHz RFID、Sub-GHz、NFC、紅外線與 BLE，可用 USB-C 連接電腦模擬鍵盤（BadUSB）。入手後先裝 microSD、用 qFlipper 或手機 App 更新韌體，再從 RFID 讀卡與 IR 遙控開始玩，就能快速上手。所有功能請只用在**你擁有或獲得授權的裝置**上。

## Flipper Zero 是什麼？適合誰用？

Flipper Zero 是一台約巴掌大小的多功能攜帶裝置，定位是「硬體探索工具」。它不是一般消費性 gadget，而是為資安研究人員、滲透測試新手、Maker 與 IoT 工程師設計的設備，用來讀取、分析、模擬常見的無線協定與數位訊號。

核心硬體包含：

- **125 kHz RFID**：讀取與模擬低頻門禁卡
- **Sub-GHz 無線**（CC1101 晶片）：分析 300–928 MHz 的遙控器、車庫門、IoT 感測器訊號
- **NFC（13.56 MHz）**：讀取、寫入與模擬高頻卡
- **紅外線（IR）**：學習並重發電視、冷氣等紅外遙控碼
- **BLE**：透過手機 App配對控制與更新
- **USB-C**：連接電腦更新韌體、模擬鍵盤（BadUSB / DuckyScript）
- **GPIO / iButton**：1-Wire 接觸鑰匙與硬體擴充

適合的讀者：準備投入無線安全研究的學生、需要驗證自家門禁/感測器可靠度的工程師、以及想了解 RFID/NFC 原理的 Maker。如果你只是想要一支「遙控器複製器」，它的 Sub-GHz 功能可以做到，但請先確認當地法令與使用場景。

## 開箱與初始設定：先裝 microSD，再開機

Flipper Zero 出廠時不含 microSD 卡，但韌體與資料儲存**強烈建議**使用記憶卡。設定步驟如下：

1. **準備 microSD 卡**：建議 4 GB 以上，格式為 FAT32（FAT16/FAT32/exFAT 皆可）。將卡片**晶片朝上**插入機身底部卡槽。
2. **充電**：用 USB-C 連接充電器或電腦，第一次使用前充飽。
3. **開機**：長按機身背面的返回鍵（Back）約 3 秒，畫面出現海豚動畫即完成開機。
4. **確認系統版本**：進入 `設定 → 關於`，記錄目前韌體版本，下一步更新。

> 注意：Flipper Zero 開機預設是英文介面；部分第三方韌體提供中文語系，但**不建議**新手先碰第三方韌體，等官方韌體流程跑熟再考慮。

## 韌體更新：qFlipper 桌面版與手機 App

韌體更新是 Flipper Zero 入門最重要的一步——原廠會持續修正 Bug、加入新協定支援，舊韌體可能無法讀取某些卡或訊號。

### 方法一：qFlipper 桌面版（推薦）

1. 到 Flipper 官方網站下載對應平台的 qFlipper（Windows / macOS / Linux）。
2. 用 USB-C 連接 Flipper Zero 與電腦，開啟 qFlipper。
3. 點右上角扳手圖示（Advanced controls），選「Firmware update channel」。
4. 選 **Release（穩定版）**，點 Update。
5. 等待更新完成（約 5–10 分鐘），裝置會自動重啟。

### 方法二：手機 App

1. 安裝官方 Flipper Mobile App（iOS / Android）。
2. 手機開啟藍牙，與 Flipper Zero 配對（裝置端：`設定 → Bluetooth`）。
3. 在 App 內點 Update，透過 BLE 傳輸更新，約需 10 分鐘。

### 韌體頻道怎麼選？

| 頻道 | 穩定性 | 適合對象 |
|---|---|---|
| Release（穩定版） | 高 | **新手一律選這個** |
| Release Candidate（RC） | 中 | 想提前試新功能的使用者 |
| Development（開發版） | 低 | 開發者、測試者 |

> ⚠️ 更新過程不要拔線或斷電；萬一卡在開機畫面，可進入 recovery 模式重刷（連按兩次 Reset）。第三方韌體（如 Xtreme）雖有擴充功能，但可能不穩定，新手請先用官方穩定版。

## 五大實用功能實測

### 1. 125 kHz RFID：讀取與模擬低頻卡

老式門禁卡（125 kHz）通常只有 ID 編碼、沒有驗證機制。Flipper Zero 底部有 LF 天線，靠近卡片即可讀取：

1. 主選單 → `125 kHz RFID` → `Read`。
2. 將卡片平放靠近機身底部，讀取成功會顯示 UID 與資料。
3. 若要模擬，讀取後選 `Emulate`，即可當作臨時替代卡使用。

### 2. Sub-GHz：分析 300–928 MHz 無線訊號

內建 CC1101 收發器，可捕捉遙控器、車庫門、IoT 感測器發送的訊號：

1. 主選單 → `Sub-GHz` → `Read Raw`。
2. 按下遙控器按鈕，畫面會顯示頻率與訊號波形。
3. 儲存後可 `Replay` 重發；也可以手動設定頻率掃描環境中的無線活動。

### 3. NFC：讀取、寫入與模擬 13.56 MHz 卡

NFC 模組支援常見的 13.56 MHz 標準，可讀取悠遊卡等非接觸卡的 UID 與資料區塊（能否完整模擬取決於卡片加密機制）：

1. 主選單 → `NFC` → `Read`。
2. 將卡片放上機背感應區，讀取卡片資訊。
3. 依卡片類型可選 `Emulate` 或 `Write`。

### 4. IR：學習與重發紅外遙控

內建紅外發射/接收，可學習電視、冷氣、投影機的遙控碼並重發：

1. 主選單 → `Infrared` → `Learn`。
2. 對準機頂紅外窗按下遙控器按鈕，學習成功後命名儲存。
3. 之後在 `Infrared → Saved` 即可隨時重發。

### 5. BadUSB / DuckyScript：USB-C 鍵盤模擬

連接電腦時，Flipper Zero 可模擬 USB 鍵盤，執行 DuckyScript 腳本（自動輸入指令）：

1. 在 microSD 卡的 `badusb/` 資料夾放入 `.txt` 腳本（DuckyScript 語法）。
2. 用 USB-C 連接目標電腦，主選單 → `BadUSB` → 選擇腳本執行。

> ⚠️ **BadUSB 是高度敏感功能**：腳本會以鍵盤輸入方式在電腦上執行指令，等同於「有人坐在電腦前打字」。只可以在你自己的電腦或明確授權測試的環境使用。

## 合法使用提醒（必讀）

Flipper Zero 本身是合法工具，但使用場景有明確的法律邊界：

- **複製/模擬門禁卡、遙控器**：只能針對你擁有或管理員授權的系統。未經授權讀取或模擬他人門禁卡、車庫遙控器，在台灣可能涉及刑法妨害祕密、電信法或個資法相關責任。
- **BadUSB**：未經授權在他人電腦執行腳本，屬違法行為。
- **訊號干擾**：刻意干擾他人無線設備（如車庫門）同樣有法律風險。

**原則很簡單：只測試自己的東西，或白紙黑字拿到授權的東西。**

## 常見問題（FAQ）

**Q1：Flipper Zero 需要先裝 microSD 卡嗎？**
不是強制，但強烈建議。多數 App、訊號庫與 BadUSB 腳本都儲存在 microSD，沒有卡片會大幅限制功能。

**Q2：更新韌體會讓設備變磚嗎？**
官方穩定版韌體風險極低；只要更新過程不斷電、不拔線，幾乎不會失敗。萬一異常，可用 recovery 模式重刷。

**Q3：可以複製悠遊卡嗎？**
多數新一代票證卡有加密與金鑰保護，Flipper Zero 只能讀取 UID 或未加密區塊，無法完整複製。且未經授權複製票證本身即違法。

**Q4：Flipper Zero 和 SDR（軟體定義無線電）有什麼差別？**
Flipper Zero 內建 Sub-GHz 收發器專攻常見協定（OOK/ASK/FSK 等），操作直覺；SDR（如 HackRF、RTL-SDR）頻率範圍更廣、可看原始頻譜，但需要電腦與較深背景。兩者是互補工具。

**Q5：哪裡可以買到 Flipper Zero？**
Yupitek（榆閤科技）提供 Flipper Zero 產品與相關配件，並提供技術諮詢；購買後可來信 sales@yupitek.com 詢問設定問題。

**Q6：可以裝第三方韌體嗎？**
可以，但新手不建議。第三方韌體（如 Xtreme）提供介面美化與額外功能，但穩定性與安全性需自行評估，且可能失去原廠更新支援。

## 總結

Flipper Zero 的入門路徑很單純：**裝 microSD → 更新官方穩定韌體 → 從 RFID 讀卡與 IR 遙控玩起 → 熟悉後再碰 Sub-GHz 與 BadUSB**。它是了解無線協定與硬體安全的絕佳起點，但請永遠記得：功能越強，越要自律——只測試自己有權限的設備。

需要 Flipper Zero 或相關配件，歡迎來信 [sales@yupitek.com](mailto:sales@yupitek.com)，Yupitek 提供產品與技術諮詢服務。