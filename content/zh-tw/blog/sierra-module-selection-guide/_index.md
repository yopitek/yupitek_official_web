---
title: "Sierra Wireless 十款蜂窩模組完整選購指南：LTE Cat 4 到 5G mmWave 怎麼選"
description: "榆閤科技整理 Sierra Wireless（Semtech）十款蜂窩模組 EM/MC 系列規格比較與選型建議，橫跨 LTE Cat 4 到 5G mmWave。全系列 Sierra Wireless 模組採購請洽 Yupitek。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
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

# Sierra Wireless 十款蜂窩模組完整選購指南：LTE Cat 4 到 5G mmWave 怎麼選

不管你是正在做物聯網專題的大學生，還是在實驗室搞網通設備，買通訊模組最怕遇到什麼？絕對是「規格表看半天、型號分不清，最後買錯封裝根本插不進機器」！

這篇文章幫大家把 Sierra Wireless（現在隸屬於 Semtech）現役跟長青款的 10 款模組一次講清楚，帶你從基礎的 LTE Cat 4 一路看懂到 5G mmWave。本文提到的 EM 系列全部是 M.2 封裝，而 MC 系列則是 mPCIe 封裝。

本文技術資料由榆閤科技（Yupitek）整理提供。

## 十款規格總表：直接看數據最準

先上重點表格！裡面的數字都是依照官方 Spec Sheet 整理的，方便大家直接比對。另外提醒一下，EM9190/EM9191 的上行峰值在不同資料來源可能會有一點點出入，如果是真的要採購做專案，建議先去翻一下最新的官方 Spec Sheet 或是直接問我們確認（文末有附錄連結）。

| 型號 | 蜂窩標準 | 晶片組 | 下載 / 上傳峰值 | 載波聚合 | 5G | mmWave | 封裝 | GNSS | 備註 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/zh-tw/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 入門 Cat 6（實際頻段配置請洽詢確認） |
| [EM7455](/zh-tw/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 開源社群最熱門、網路教學最多 |
| [EM7511](/zh-tw/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 高上行 Cat 12 |
| [EM7565](/zh-tw/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 支援 CBRS/LAA 頻段、支援最多頻段與最高上行 |
| [EM9190](/zh-tw/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下行 2.5 Gbps（上行峰值請洽詢確認） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 平價 5G 入門款 |
| [EM9191](/zh-tw/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下行最高 4.5 Gbps（含 mmWave）/ Sub-6 2.5 Gbps（上行峰值請洽詢確認） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 旗艦 5G，把毫米波也包進來了 |
| [MC7304](/zh-tw/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | 入門 Cat 4（已接近 EOL 停產週期） |
| [MC7350](/zh-tw/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、主打北美頻段 |
| [MC7354](/zh-tw/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、主打全球頻段 |
| [MC7455](/zh-tw/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | 簡單來說就是 mPCIe 版本的 EM7455 |

> 備註：EM9190 和 EM9191 其實是共用同一份 EM919x/EM7690 規格書。EM9190 是 Sub-6 的平價 5G，而 EM9191 加上了 mmWave 算是旗艦款。官方規格書需要登入會員才能下載，上面表格的下行峰值是我們從公開資料整理來的，至於上行峰值等細節，建議下單前還是找我們確認一下最新版本比較保險。

## 第一道關卡：EM 系列（M.2）跟 MC 系列（mPCIe）差在哪？

這絕對是新手選型最容易踩雷的地方！買錯插不進去真的很尷尬。

**EM 系列 = M.2 B-Key 封裝**：你可以想像成筆電裡面插 SSD 的那種介面，體積很小（大約 30×42 mm）。它是專門為筆電 WWAN 插槽、嵌入式 M.2 插槽設計的，現在比較新的工控主機板或迷你 PC 大多是用這種。

**MC 系列 = Mini PCIe（mPCIe）封裝**：外觀看起來就像以前電腦的擴充卡，比較適合舊款的工業路由器或工控機的 mPCIe 插槽。如果你的板子只有 M.2 插槽，想用 MC 系列就必須另外買一塊轉接板（M.2 轉 mPCIe）才行。

**它們的共通點**：兩種都需要外接 SIM 卡座和天線。天線接頭通常是 U.FL，標準配置是 2×2 MIMO（一根主天線 + 一根分集天線），還會額外有一根 GNSS 定位天線。

**大家常問的問題**：EM7455 跟 MC7455 到底差在哪？答案是：「同一顆晶片，只差封裝」。兩張卡都是用 Qualcomm MDM9230，規格一模一樣，所以選哪張真的就是看你的板子長什麼樣子。

## 依照你的專題或應用場景，我們推薦這樣選：

### 1. 自己架無線路由器 / CPE（用 OpenWrt 或 ROOter）

**推薦：[EM7455](/zh-tw/products/sierra/em7455/) / [MC7455](/zh-tw/products/sierra/mc7455/)**
理由很簡單，因為網路上的開源社群資源最多！如果你用 ROOter（一個基於 OpenWrt 的韌體），相關的教學跟 QMI/MBIM 設定範例非常完整，踩坑了隨便 google 都有救。

### 2. 幫舊筆電升級 WWAN 網卡

**推薦：[EM7430](/zh-tw/products/sierra/em7430/) / [EM7455](/zh-tw/products/sierra/em7455/)**
這兩款都是 M.2 封裝，很適合對應 Dell、Lenovo 等商務筆電的 WWAN 插槽。特別是 EM7455 二手價通常滿香的，是升級首選（但實際頻段能不能合你的電信商，下單前還是先問我們確認一下）。

### 3. 工業路由器 / 物聯網閘道器（需要耐操、寬溫）

**推薦：EM75 系列（[EM7511](/zh-tw/products/sierra/em7511/)、[EM7565](/zh-tw/products/sierra/em7565/)）、[EM9190](/zh-tw/products/sierra/em9190/)/[EM9191](/zh-tw/products/sierra/em9191/)、[MC7455](/zh-tw/products/sierra/mc7455/)**
做工業專案最在意的就是寬溫（例如 -40°C ~ +85°C 這種嚴苛環境）、認證完不完整以及能不能長期買得到。Cat 12 跟 5G 模組上傳頻寬比較大，未來擴充性也比較好。不過實際的寬溫規格請以官方最新文件為準。

### 4. 車聯網 / 車隊追蹤（需要 GNSS 定位）

**推薦：[EM7455](/zh-tw/products/sierra/em7455/) / [EM7565](/zh-tw/products/sierra/em7565/) / [EM9191](/zh-tw/products/sierra/em9191/)**
做車聯網專題通常需要精準定位，這三款都有內建 GNSS，可以一次解決連網跟定位的需求。如果需要用到 5G 的大頻寬，直上 EM9191 準沒錯。

### 5. 5G 專網 / CBRS 私有網路實驗

**推薦：[EM9191](/zh-tw/products/sierra/em9191/)（支援 CBRS 頻段）、[EM7565](/zh-tw/products/sierra/em7565/)（支援 CBRS/LAA 頻段）**
如果你在實驗室研究 CBRS（美規 3.5 GHz 共享頻段）或 LAA，這兩款在硬體上都有支援。但要注意，真正在當地測試私網還是要看當地的法規跟電信環境，建議導入前跟我們討論一下技術細節。

### 6. 視訊監控 / 高畫質影音回傳

**推薦：[EM9190](/zh-tw/products/sierra/em9190/) / [EM9191](/zh-tw/products/sierra/em9191/)**
因為 5G 頻寬夠大（下行最高 Sub-6 有 2.5 Gbps、如果算上 mmWave 最高可以到 4.5 Gbps），非常適合用來做多路影像即時回傳或是 4K 的影像串流。

### 7. 舊設備維修 / 實驗室老機器備料（Cat 4）

**推薦：[MC7304](/zh-tw/products/sierra/mc7304/) / [MC7350](/zh-tw/products/sierra/mc7350/) / [MC7354](/zh-tw/products/sierra/mc7354/)**
這是 mPCIe 封裝的老機器維修首選。不過要老實說：MC73xx 系列已經接近 EOL（停產週期）了，如果是長期的專案，建議大家考慮改用 [EM7455](/zh-tw/products/sierra/em7455/) 或是 [EM7565](/zh-tw/products/sierra/em7565/) 會比較有保障。

## 選型還是霧煞煞？找我們幫忙吧

如果看完還是不知道怎麼挑，在台灣你可以透過 Yupitek 榆閤科技採購這十款 EM/MC 系列的蜂窩模組，連天線、SIM 轉接板或評估板都可以一起搞定。不管是確認規格、比對頻段，還是專案需要的報價與技術支援，都可以找我們。

## 常見問題快速 Q&A

{{< faq >}}

## 附錄：十款型號官方 Spec Sheet 傳送門

下面這些連結都是連到 Sierra Wireless 官方的技術資源庫（source.sierrawireless.com）。**有些文件需要註冊登入才能下載 PDF**。文章裡的數據是整理自公開資料，如果你需要逐項確認超細節的規格（例如 EM9190/EM9191 的上行峰值），建議直接聯絡我們索取最新的官方文件。

- **EM7430**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
