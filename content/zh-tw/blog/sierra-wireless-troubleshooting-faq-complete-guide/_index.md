---
title: "Sierra Wireless 模組常見問題全集：從裝置抓不到到連不上網路的排錯地圖"
locale: "zh-TW"
hreflang_group: "sierra-wireless-troubleshooting-faq-complete-guide"
description: "Sierra Wireless 4G/5G 模組排錯地圖：從裝置抓不到、QMI/MBIM 介面消失、SIM 無法註冊到連不上網路，本文教你用 AT 指令與 Linux/Windows 工具，分四層精準診斷問題點，不走冤枉路。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "sierra-wireless-troubleshooting-faq-complete-guide"
tags: ["Sierra Wireless", "EM7455", "EM7565", "EM919x", "MC7455", "故障排除", "QMI", "MBIM", "AT指令", "LTE"]
categories: ["Technical"]
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/zh-tw/products/sierra/"
faq:
  - question: "Sierra Wireless 模組在電腦上完全抓不到，最可能的原因是？"
    answer: "最常見是硬體層問題：供電不足導致斷電重啟、M.2 插槽接觸不良、或 W_DISABLE# 腳位被主機板拉低進入飛航模式。請先用 lsusb 或裝置管理員確認。"
  - question: "USB 看得到模組，但 Linux 下沒有撥號介面怎麼辦？"
    answer: "這代表主機沒有綁定正確的介面驅動。可能是 Linux 核心缺少 qmi_wwan / cdc_mbim 驅動，或是模組內部的 USB composition 設定錯誤，隱藏了上網通道。"
  - question: "介面都正常，但 4G 一直連不上網路，問題會在哪？"
    answer: "九成出在 SIM 卡或 APN。請打開終端機輸入 AT+CPIN? 確認 SIM 卡狀態，再用 AT!GSTATUS? 確認是否連上基地台。最後確認你輸入的 APN 參數是否符合電信商要求。"
---

# Sierra Wireless 模組常見問題全集：從裝置抓不到到連不上網路的排錯地圖

**一句話總結：網卡連不上網路？先查「電腦有沒有看到它」（USB列舉），再查「有沒有資料通道」（QMI/MBIM介面），接著看「SIM卡跟APN通不通」，最後才看「天線跟散熱」。九成的人都死在第三步，千萬不要一開始就瞎猜是韌體壞掉而去亂刷機！**

玩 Sierra Wireless 的 4G/5G 模組（不管是 EM7455、EM7565 還是最新的 EM919x），最怕的就是插上去「沒反應」或是「連不上網」。
網路上的教學很散，有時候叫你刷韌體，有時候叫你改設定。這篇文章幫你整理出一張「四層排錯地圖」，跟著步驟一步步查，你一定能找到問題點。

> 資料來源：Sierra Wireless 官方規格書。排錯流程為實戰經驗整理。本文由榆閤科技（Yupitek）整理。

---

## 30 秒快速定位問題

先看看你的症狀符合哪一條，直接跳到對應的樓層！

| 你的症狀 | 是哪一層出包？ | 該下什麼指令查？ |
|---|---|---|
| **電腦完全看不到模組** | **L1 (硬體/USB層)** | Windows 裝置管理員 / Linux `lsusb` |
| **看得到 USB，但沒有撥號介面** | **L2 (介面/驅動層)** | Linux `ls /dev/cdc-wdm*` 或看驅動綁定 |
| **有介面，但一直撥號失敗或沒 IP** | **L3 (SIM/APN層)** | 進入終端機下 `AT+CPIN?` 跟 `AT!GSTATUS?` |
| **連得上，但速度很慢、常斷線或沒 GPS** | **L4 (天線/散熱層)** | `AT!PCTEMP` 看溫度，`AT+CSQ` 看訊號 |

---

## 第一層（L1）：電腦完全抓不到模組

這時候連打 AT 指令的機會都沒有。如果 `lsusb` 敲下去完全沒有出現 Sierra 或 1199 開頭的設備，這 **100% 是硬體問題**。

**兇手通常是這三個：**
1. **電沒給夠**：模組吃的是 3.3V（有些是 3.7V）的電，瞬間開機可能會抽到 2A 以上的電流。如果你用便宜的 USB 轉接盒，供電不足就會一直斷電重啟。
2. **接觸不良**：卡扣沒壓緊，或是轉接板壞了。
3. **被「飛航模式」腳位關掉了**：M.2 插槽有一根 `W_DISABLE#` 腳位，如果主機板把它拉成低電位，模組就會直接裝死不開機。

> 💡 **小知識**：如果模組供電不穩導致連續當機 6 次，它會進入 **SED (Smart Error Detection) 保護模式**（俗稱變磚），這時候就需要重插 USB 並用官方工具重新刷入韌體來救活它。

---

## 第二層（L2）：USB 看得到，但沒有通訊介面

這時候 `lsusb` 看到了設備，但是在 Linux 底下卻找不到 `/dev/ttyUSB*`（打 AT 指令的洞）或是 `/dev/cdc-wdm0`（撥號上網的洞）。

**兇手是誰？**
1. **Linux 驅動沒裝**：請確保你的系統有裝好 `qmi_wwan`（走 QMI）或 `cdc_mbim`（走 MBIM）模組。
2. **USB Composition（介面組合）錯了**：模組裡面有個設定叫 USB Composition。有時候它被設定成「純診斷模式」，只留幾個 COM Port 給你，把上網的通道藏起來了。你需要用 `AT!USBCOMP?` 指令去查，並把它切換回有 QMI 或 MBIM 的模式。

---

## 第三層（L3）：介面都對，但就是連不上網（九成苦主卡這關）

所有的洞都出現了，但就是撥號失敗。請打開你的終端機軟體（如 minicom 或是 putty），連進模組的 AT Port，依序打這幾個指令「辦案」：

### 1. 查 SIM 卡是不是正常的？
```text
AT+CPIN?
```
- 回傳 `READY`：代表 SIM 卡正常讀到，也沒有鎖密碼。
- 回傳 `SIM PIN` 甚至 `ERROR`：恭喜你找到問題了，卡沒插好或是被鎖住了。

### 2. 查有沒有抓到基地台？
```text
AT!GSTATUS?
```
這是一個超強的 Sierra 專屬指令（如果報錯，可能要先下 `AT!ENTERCND="<密碼>"` 解鎖權限）。它會告訴你現在連在哪個頻段、訊號多強、有沒有註冊上網路。

### 3. APN 設對了嗎？
這不需要打指令，請回去看你的撥號軟體（例如 NetworkManager 或 OpenWrt 的設定）。如果你用的是中華電信、台灣大哥大等，通常 APN 會是 `internet`。如果有申請固定 IP 專案，APN 絕對不一樣，請打電話問電信商。

---

## 第四層（L4）：連得上，但速度慢、斷線或沒 GPS

### 1. 天線接錯或沒接滿
這幾張網卡都有 3 到 4 個天線小圓孔（MHF4 或是 U.FL）。
**至少要把 MAIN 跟 AUX 接上！** 只接 MAIN 雖然能上網，但速度跟穩定度會大打折扣。
另外，如果要用 GPS 定位，天線一定要接在寫著 **GNSS** 的那個洞上。

### 2. 忘了打開 GPS
如果你天線接對了還是定不到位，可能是模組把 GPS 關起來省電了。打這個指令把它叫醒：
```text
AT!CUSTOM="GPSENABLE"
```

### 3. 被熱當了
把它關在一個沒冷氣的戶外鐵箱裡？打這個指令看看它發高燒了沒：
```text
AT!PCTEMP
```
- **EM7455 / MC7455**：內部極限 93°C
- **EM7565**：內部極限 90°C
- **EM919x (5G)**：內部極限 115°C

只要超過建議的工作溫度，模組就會自己降速，甚至斷開連線來保護自己。請加個散熱片吧！

---

## 結論

遇到 4G/5G 模組不乖乖工作時，千萬不要病急亂投醫、到處亂刷韌體。只要拿著這份地圖，從 **電源硬體 → 驅動介面 → SIM與APN設定 → 散熱與天線**，一層一層往下查，所有妖魔鬼怪都會現出原形！

## 常見問題快速 Q&A

{{< faq >}}

## 採購資訊（Call To Action）

你的專案還卡在連線問題上嗎？想要尋找穩定可靠的 Sierra Wireless 模組與技術支援？Yupitek（榆閤科技）有提供完整的硬體方案與第一線技術支援，幫你擺脫踩坑的地獄。
歡迎來信：**sales@yupitek.com**
看看產品：[Sierra Wireless 模組專區](/zh-tw/products/sierra/)
