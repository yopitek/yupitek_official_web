---
title: "Sierra Wireless 十款蜂窩模組完整選購指南：LTE Cat 4 到 5G mmWave 怎麼選"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - cellular-module
  - 4g-lte
  - 5g-nr
  - module-selection
  - em7455
  - em9190
  - m2-pcie
  - wireless-communication
categories:
  - 產品選型指南
series:
  - sierra-wireless-selection
series_order: 1
description: "榆閤科技整理 Sierra Wireless（Semtech）十款蜂窩模組 EM/MC 系列規格比較與選型建議，橫跨 LTE Cat 4 到 5G mmWave。全系列 Sierra Wireless 模組採購請洽 Yupitek。"
author: "yupitek"
draft: false
faq:
  - question: "Sierra Wireless 有哪些型號？彼此差在哪？"
    answer: "Sierra Wireless 現有 EM 與 MC 兩大系列共十款模組，橫跨 LTE Cat 4 / Cat 6 / Cat 12 到 5G Sub-6 與 mmWave。最大差異在封裝：EM 為 M.2、MC 為 mPCIe；同晶片型號（如 EM7455 與 MC7455）效能相同，只差插槽形狀。"
  - question: "EM7455 跟 MC7455 是同一顆晶片嗎？"
    answer: "是的。兩者都採用 Qualcomm MDM9230 晶片組，下載/上傳峰值同為 300 / 50 Mbps、支援 2×CA 載波聚合，規格完全一致，唯一差別是 EM7455 為 M.2、MC7455 為 mPCIe 封裝。"
  - question: "5G 模組一定要選 mmWave（EM9191）嗎？台灣可以用嗎？"
    answer: "不一定。台灣電信目前以 Sub-6 為主，mmWave 主要佈建於美規場域（如 n260/n261）。一般台灣應用選 EM9190（Sub-6 平價 5G）即可；僅有美規毫米波需求才需 EM9191。"
  - question: "M.2 和 mPCIe 蜂窩模組該怎麼選？"
    answer: "看你的設備插槽。筆電、現代嵌入式主機板多為 M.2 B-Key，選 EM 系列；舊款工業路由器、工控機若為 mPCIe 槽，選 MC 系列。若板子只有 M.2 卻想用 MC，需加 M.2 to mPCIe 轉接板。"
  - question: "Sierra Wireless 台灣哪裡買？"
    answer: "台灣可透過榆閤科技（Yupitek）採購 Sierra Wireless 全系列蜂窩模組。請至 Yupitek 官網產品頁查詢型號與報價，或直接 email: sales@yupitek.com"
---

採購蜂窩模組最怕「規格表看不懂、型號一堆分不清、買錯封裝插不進機器」。這篇文章把 Sierra Wireless 現役與長青款共十款模組一次講清楚，幫你從 LTE Cat 4 一路選到 5G mmWave。

Sierra Wireless 現隸屬 Semtech。本文由榆閤科技（Yupitek）整理，涵蓋 Sierra Wireless 共十款蜂窩模組：EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455。其中 EM 系列為 M.2 封裝、MC 系列為 mPCIe 封裝。

本文技術資料由榆閤科技（Yupitek）整理。

Sierra Wireless 十款模組橫跨 LTE Cat 4 / 6 / 12 到 5G Sub-6 與 mmWave。EM 與 MC 系列只差封裝：EM 為 M.2、MC 為 mPCIe。

## 十款規格總表

先上表格，數字依官方 Spec Sheet 填寫，方便你直接比對。EM9190/EM9191 的上行峰值目前不同資料來源略有出入，實際採購前請以最新官方 Spec Sheet 或洽詢確認（詳見文末附錄連結）。

| 型號 | 蜂窩標準 | 晶片組 | 下載 / 上傳峰值 | 載波聚合 | 5G | mmWave | 封裝 | GNSS | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/zh-tw/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 入門 Cat 6（實際頻段配置請洽詢確認） |
| [EM7455](https://yupitek.com/zh-tw/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 社群最熱門、教學最多 |
| [EM7511](https://yupitek.com/zh-tw/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 高上行 Cat 12 |
| [EM7565](https://yupitek.com/zh-tw/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 支援 CBRS/LAA 頻段（實際認證範圍請洽詢確認）、最多頻段、最高上行 |
| [EM9190](https://yupitek.com/zh-tw/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下行 2.5 Gbps（上行峰值請洽詢確認） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 平價 5G 入門 |
| [EM9191](https://yupitek.com/zh-tw/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下行最高 4.5 Gbps（含 mmWave）/ Sub-6 2.5 Gbps（上行峰值請洽詢確認） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 旗艦 5G、含毫米波 |
| [MC7304](https://yupitek.com/zh-tw/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | 入門 Cat 4（接近 EOL） |
| [MC7350](https://yupitek.com/zh-tw/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、北美頻段 |
| [MC7354](https://yupitek.com/zh-tw/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、全球頻段 |
| [MC7455](https://yupitek.com/zh-tw/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | mPCIe 版 EM7455 |

> 備註：EM9190 與 EM9191 共用同一份 EM919x/EM7690 規格書；EM9190 為 Sub-6 平價 5G，EM9191 加 mmWave 為旗艦。該份官方規格書為會員登入下載，我們目前引用的下行峰值數字係整理自公開資料，上行峰值等細節數字建議下單前直接向我們確認最新版本。

## EM 系列（M.2）vs MC 系列（mPCIe）封裝差異

這是選型第一道關卡，也是最多人買錯的地方。

**EM 系列 = M.2 B-Key 封裝**：體積小（約 30×42 mm），專為筆電 WWAN 槽、嵌入式 M.2 插槽設計，現代工控主機板與迷你 PC 多數採用。

**MC 系列 = Mini PCIe（mPCIe）封裝**：外觀與一般電腦擴充卡相同，適合舊款工業路由器、工控機的 mPCIe 插槽。若你的板子只有 M.2 槽，MC 系列需加轉接板（M.2 to mPCIe）才能使用。

**共同硬體需求**：兩者都需外接 SIM 卡座與天線。天線多為 U.FL 接頭，典型配置為 2×2 MIMO（主天線 + 分集天線）再加上一支 GNSS 定位天線。

**一個常被問的重點**：EM7455 與 MC7455 是「同一顆晶片、只差封裝」——兩者皆採 Qualcomm MDM9230，規格完全相同，差別只在 M.2 與 mPCIe。所以選哪顆，純看你的機器插槽長怎樣。

## 依應用場景的選型建議

### 無線路由器 / CPE（OpenWrt / ROOter）

**推薦：[EM7455](https://yupitek.com/zh-tw/products/sierra/em7455/) / [MC7455](https://yupitek.com/zh-tw/products/sierra/mc7455/)**
理由：社群資源最多，ROOter（基于 OpenWrt 的蜂窩路由韌體）教學與 QMI/MBIM 設定範例最完整，出問題 google 得到答案。

### 筆電 WWAN 升級

**推薦：[EM7430](https://yupitek.com/zh-tw/products/sierra/em7430/) / [EM7455](https://yupitek.com/zh-tw/products/sierra/em7455/)**
理由：皆為 M.2 封裝，對應 Dell、Lenovo 等商用機的 WWAN 插槽；EM7455 頻段配置較廣為人知、二手價低，是升級首選（實際頻段與您所在電信商相容性建議下單前先跟我們確認）。

### 工業路由器 / 閘道器（寬溫、認證、長供貨）

**推薦：EM75 系列（[EM7511](https://yupitek.com/zh-tw/products/sierra/em7511/)、[EM7565](https://yupitek.com/zh-tw/products/sierra/em7565/)）、[EM9190](https://yupitek.com/zh-tw/products/sierra/em9190/)/[EM9191](https://yupitek.com/zh-tw/products/sierra/em9191/)、[MC7455](https://yupitek.com/zh-tw/products/sierra/mc7455/)**
理由：工業場域重視寬溫（−40°C 等級選項）、認證完整性與長期供貨保證；Cat 12 與 5G 模組提供更高上行與未來頻寬餘裕。實際寬溫規格與認證清單以官方規格書為準，建議正式選型時向我們索取最新版本確認。

### 車聯網 / 車隊 Telematics（GNSS 定位）

**推薦：[EM7455](https://yupitek.com/zh-tw/products/sierra/em7455/) / [EM7565](https://yupitek.com/zh-tw/products/sierra/em7565/) / [EM9191](https://yupitek.com/zh-tw/products/sierra/em9191/)**
理由：三者皆內建 GNSS，適合車載追蹤與定位回傳；需要 5G 高頻寬車載應用時選 EM9191。

### 5G 專網 / CBRS 私有網路

**推薦：[EM9191](https://yupitek.com/zh-tw/products/sierra/em9191/)（支援 CBRS 頻段）、[EM7565](https://yupitek.com/zh-tw/products/sierra/em7565/)（支援 CBRS/LAA 頻段）**
理由：CBRS（美規 3.5 GHz 共享頻段）與 LAA 為私有網路常見需求；EM9191、EM7565 硬體皆支援對應頻段。實際導入私網前，頻段搭配與相關認證仍需依當地法規與電信環境確認，建議與我們聯繫做完整技術評估。

### 視訊監控 / 數位看板高頻寬回傳

**推薦：[EM9190](https://yupitek.com/zh-tw/products/sierra/em9190/) / [EM9191](https://yupitek.com/zh-tw/products/sierra/em9191/)**
理由：5G 高頻寬（下行最高 Sub-6 2.5 Gbps、含 mmWave 最高 4.5 Gbps）適合多路影像即時回傳與 4K 看板串流。

### 舊機維修 / 長期備料（Cat 4）

**推薦：[MC7304](https://yupitek.com/zh-tw/products/sierra/mc7304/) / [MC7350](https://yupitek.com/zh-tw/products/sierra/mc7350/) / [MC7354](https://yupitek.com/zh-tw/products/sierra/mc7354/)**
理由：mPCIe 封裝的 Cat 4 老機維修料首選。但需誠實提醒：MC73xx 系列已接近 EOL（停產週期），長期備料建議評估遷移至 [EM7455](https://yupitek.com/zh-tw/products/sierra/em7455/) 或 [EM7565](https://yupitek.com/zh-tw/products/sierra/em7565/)，以取得更長的供貨保證。

## 聯絡採購

選型還是拿不準？台灣可透過 Yupitek 榆閤科技採購本文十款 EM/MC 系列 Sierra 蜂窩模組，包含相關天線、SIM 轉接與評估板。我們提供規格確認、頻段比對、量價報價與技術導入支援。

## 常見問題 FAQ

**Q1：Sierra Wireless 有哪些型號？彼此差在哪？**
Sierra Wireless 現有 EM 與 MC 兩大系列共十款模組，橫跨 LTE Cat 4 / Cat 6 / Cat 12 到 5G Sub-6 與 mmWave。最大差異在封裝：EM 為 M.2、MC 為 mPCIe；同晶片型號（如 EM7455 與 MC7455）效能相同，只差插槽形狀。

**Q2：EM7455 跟 MC7455 是同一顆晶片嗎？**
是的。兩者都採用 Qualcomm MDM9230 晶片組，下載/上傳峰值同為 300 / 50 Mbps、支援 2×CA 載波聚合，規格完全一致，唯一差別是 EM7455 為 M.2、MC7455 為 mPCIe 封裝。

**Q3：5G 模組一定要選 mmWave（EM9191）嗎？台灣可以用嗎？**
不一定。台灣電信目前以 Sub-6 為主，mmWave 主要佈建於美規場域（如 n260/n261）。一般台灣應用選 EM9190（Sub-6 平價 5G）即可；僅有美規毫米波需求才需 EM9191。

**Q4：M.2 和 mPCIe 蜂窩模組該怎麼選？**
看你的設備插槽。筆電、現代嵌入式主機板多為 M.2 B-Key，選 EM 系列；舊款工業路由器、工控機若為 mPCIe 槽，選 MC 系列。若板子只有 M.2 卻想用 MC，需加 M.2 to mPCIe 轉接板。

**Q5：Sierra Wireless 台灣哪裡買？**
台灣可透過榆閤科技（Yupitek）採購 Sierra Wireless 全系列蜂窩模組。請至 Yupitek 官網產品頁查詢型號與報價，或直接 email: sales@yupitek.com

## 附錄：十款型號官方 Spec Sheet 連結

以下連結提供各型號規格書 PDF 副本（可直接下載，無需登入），來源為 Sierra Wireless 官方技術資源庫（source.sierrawireless.com）。MC7350、MC7354 因無個別 PDF 檔案，仍保留官方外部連結（需會員登入）。本文規格數字整理自公開資料，若需逐項核對的最終規格數字（尤其是 EM9190/EM9191 上行峰值），建議直接向我們索取官方文件確認：

- **EM7430**：https://yupitek.com/docs/sierra/em7430_spec.pdf
- **EM7455**：https://yupitek.com/docs/sierra/em7455_spec.pdf
- **EM7511**：https://yupitek.com/docs/sierra/EM7511_spec.pdf
- **EM7565**：https://yupitek.com/docs/sierra/EM7565_spec.pdf
- **EM9190 / EM9191**：https://yupitek.com/docs/sierra/EM919x.pdf
- **MC7304**：https://yupitek.com/docs/sierra/MC7304_spec.pdf
- **MC7350**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**：https://yupitek.com/docs/sierra/mc7455_spec.pdf
