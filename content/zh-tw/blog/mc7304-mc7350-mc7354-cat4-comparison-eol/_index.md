---
title: "MC7304 / MC7350 / MC7354 怎麼分？舊款 Cat 4 模組選型與長期備料建議"
description: "MC7304、MC7350、MC7354 怎麼分？本文逐項核對官方規格書與 FCC 備案，解析 LTE 頻段、下載速率、天線與溫度，揭露 Cat 3/Cat 4 速率差異，並提供舊款 mPCIe 模組備料建議與 EM7455 升級評估，工程師必看。"
date: 2026-08-01
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "mc7304", "mc7350", "mc7354", "mpcie", "cat4", "lte", "eol", "module-selection"]
featureimage: "/static/img/sierra/hero.webp"
author: "benny-lai"
lastmod: 2026-08-01
faq:
  - question: "MC7304、MC7350、MC7354 到底差在哪？"
    answer: "三顆都是 Sierra Wireless AirPrime MC 系列 mPCIe 模組，共用 MC73XX 平台（峰值下載 100 Mbps、上傳 50 Mbps，內建 GPS + GLONASS，3 個 RF 天線連接器）。差異在頻段與定位：MC7304 歐亞 LTE＋WCDMA＋GSM；MC7350 北美 LTE＋CDMA 且無 GSM；MC7354 北美多營運商全模。"
  - question: "這幾顆模組是不是停產了？該怎麼備料？"
    answer: "官方規格文件中沒有這三顆的正式停產公告，但它們屬舊款 mPCIe 世代。備料策略：先向原廠洽詢最新生命週期狀態，同步評估 MC7455（同封裝）或 EM7455/EM7565（M.2 世代）替代路徑。"
  - question: "可以直接把 MC73XX 換成 EM7455 嗎？"
    answer: "不能直接換。MC73XX 是 mPCIe 封裝，EM7455 是 M.2 封裝，插槽電氣與機構不相容。升級 EM7455 需更換載板或重新設計主機板；若只能在同插槽升級，mPCIe 後續選項是 MC7455（Cat 6、300/50 Mbps）。"
  - question: "下行速率到底是 100 Mbps 還是 150 Mbps？"
    answer: "官方 MC 系列手冊載明 MC73XX 峰值下載 100 Mbps、上傳 50 Mbps；FCC 測試備案亦歸類為 LTE Cat 3（100/50 Mbps）。「Cat 4 / 150 Mbps」說法尚待原廠最新文件確認，建議以 100/50 Mbps 為基準。"
---

# MC7304 / MC7350 / MC7354 怎麼分？舊款 Cat 4 模組選型與長期備料建議

> **先講結論**：MC7304、MC7350、MC7354 是 Sierra Wireless AirPrime MC 系列的三顆 mPCIe 蜂窩模組，同屬 MC73XX 家族。官方手冊標示它們的峰值下載為 100 Mbps、上傳 50 Mbps，支援 LTE、HSPA+ 與 GSM/GPRS/EDGE。其中 MC7354 和 MC7350 還有 CDMA 回退。三顆都內建 GPS + GLONASS 定位，需要外接 3 支天線。詳細技術資料可參考：[MC7304](/zh-tw/products/sierra/mc7304/)｜[MC7350](/zh-tw/products/sierra/mc7350/)｜[MC7354](/zh-tw/products/sierra/mc7354/)。

如果在機房、ATM 或是舊款工業閘道器裡看到這幾顆 Sierra 模組，你可能會疑惑：型號只差一點點，到底差在哪？其實它們的**頻段定位完全不同**。如果你裝錯型號，機器可能完全連不到網路。這篇文章我們整理了官方手冊和 FCC 備案資料，幫你快速搞懂這三顆模組的差異、備料策略，以及能不能升級到新款模組。

---

## 一、三顆模組的核心差異（30 秒速覽）

它們都是 mPCIe 插槽的模組，共用 MC73XX 平台（峰值下載 100 Mbps、上傳 50 Mbps），真正的差別在於你要把機器賣到哪裡：

| 問題 | 簡單解答 |
|---|---|
| **MC7304 跟 MC7350 差在哪？** | 頻段不同。MC7304 走歐亞主流頻段（LTE B1/B3/B7/B8/B20），沒有 CDMA；MC7350 走北美頻段（LTE B4/B13/B25＋CDMA），沒有 GSM。用錯地方就是沒訊號。 |
| **這幾顆是不是快停產了？** | 目前我們手邊的官方文件**沒有**寫停產（EOL）時間。但它們的確是舊世代產品，要長期備料前，建議先問問原廠最新狀況。 |
| **速度到底多快？** | 官方手冊寫下載 100 Mbps、上傳 50 Mbps；FCC 測試把它們歸在 LTE Cat 3。雖然外面常傳它們是 Cat 4（150 Mbps），但以公開文件來看，我們保守抓 100/50 Mbps 比較保險（詳見後面段落）。 |
| **有內建天線嗎？** | 沒有。三顆都有 3 個 RF 接頭（Main、Aux、GNSS），天線要自己接。 |

---

## 二、三顆型號速查表：頻段 / 認證一次看

大家最關心的硬體規格，直接幫你列在下面：

| 項目 | MC7304 | MC7350 | MC7354 |
|---|---|---|---|
| **封裝與尺寸** | mPCIe（50 × 30 × 2.7 mm） | mPCIe | mPCIe（50.95 × 30 × 2.75 mm，8.6 g） |
| **支援網路** | LTE、HSPA+、GSM/GPRS/EDGE | LTE、HSPA+、CDMA 1xRTT/EV-DO | LTE、HSPA+、GSM/GPRS/EDGE、CDMA 1xRTT/EV-DO |
| **峰值下載／上傳** | 100 / 50 Mbps | 100 / 50 Mbps | 100 / 50 Mbps |
| **LTE 頻段** | B1, B3, B7, B8, B20 | B4, B13, B25 | B2, B4, B5, B13, B17, B25 |
| **WCDMA 頻段** | B1, B2, B5, B8 | （以代理商為準） | B1, B2, B4, B5, B8 |
| **CDMA / GSM** | 只有 GSM | 只有 CDMA | 兩者都有 |
| **GNSS 定位** | GPS、GLONASS | GPS、GLONASS | GPS、GLONASS |
| **天線接頭** | 3 個（Main、Aux、GNSS） | 3 個 | 3 個 |
| **USB 介面** | USB 2.0 High Speed | USB 2.0 High Speed | USB 2.0 |
| **工作溫度** | -40°C ~ +85°C | -40°C ~ +85°C | Class A: -30°C ~ +70°C；Class B: -40°C ~ +85°C |

> ⚠️ **注意**：電信商與法規認證是動態變化的，這裡列的頻段是規格書當年的資料，採購前請務必找代理商確認現在還能不能用。

---

## 三、頻段哲學：這三顆到底設計給誰用？

### MC7304：歐亞通吃的選擇
這顆專走歐亞 LTE 頻段（B1/B3/B7/B8/B20），支援 WCDMA 和 GSM，但**不碰 CDMA**。如果你的設備要放在台灣、歐洲或亞太地區，這顆是最穩妥的選擇。

### MC7350：北美精簡版
這顆是為了北美的 Verizon 和 Sprint 打造的，LTE 支援 B4/B13/B25，有 CDMA 但**沒有 GSM**。把它拿來亞洲用，基本上就是個廢物。

### MC7354：北美全餐版
這是同系列裡面頻段給得最齊全的北美版，除了 LTE（B2/B4/B5/B13/B17/B25），還把 UMTS、CDMA 跟 GSM 全部塞進去。如果你的設備要在北美跨電信商使用，這顆會比 MC7350 讓人安心很多。

---

## 四、那個永遠吵不完的問題：到底是 Cat 3 還是 Cat 4？

市場上很多人都叫這幾顆「Cat 4 模組」，但老實說，這點有爭議：

1. **官方手冊**和 **FCC 測試** 都把 MC73XX 標為 **下載 100 Mbps、上傳 50 Mbps**（這是 Cat 3 的標準）。
2. 傳聞中原廠的內部規格書寫它是 Cat 4（150 Mbps），但那份文件並未公開。
3. 晶片組也分成兩派說法：官方寫 Qualcomm MDM9215，但有些代理商標示 MDM9615。

**我們的建議**：就當它是 100/50 Mbps 就好。不要為了多那 50M 的理論值跟規格過不去。

---

## 五、舊設備怎麼辦？備料還是升級？

對於這些有點年紀的 mPCIe 模組，企業最怕的就是突然買不到。

### 長期備料策略
既然不知道什麼時候停產，第一步就是去問原廠或代理商「現在的生命週期狀態」。確定還買得到，就依照機台數量多備一些。另外，把現在用得順的韌體版本備份下來，免得之後買到新批次出問題。

### 升級方案（想換 EM7455 可以嗎？）
如果想升級到新款的 **EM7455**（Cat 6，300/50 Mbps），請注意：**插槽不一樣！**
MC73XX 是 mPCIe，EM7455 是 M.2。你必須要換主機板，不然就得加上轉接板。
如果你不想動主機板，那可以直接選同為 mPCIe 的 **MC7455**，這樣就能無痛升級速度。

---

## 六、常見踩坑指南

1. **只看「Cat 4」就買**：買回來實測發現只有 100 Mbps，請以 FCC 測試資料為準。
2. **把 MC7350 買來亞洲用**：頻段不對，完全連不上。
3. **忘記插槽不一樣**：想升級 M.2 模組，結果主機板只有 mPCIe 槽。

## 結論

MC7304、MC7350、MC7354 這三兄弟其實很好分：**亞洲選 04，北美選 50 或 54**。雖然速度可能只有 Cat 3 等級，但在舊工業設備上，它們依然是很穩定的選擇。如果想要長久之計，先打聽好停產時間，再考慮要不要無痛升級到 MC7455 吧！

## 常見問題快速 Q&A

{{< faq >}}

## 採購資訊（Call To Action）

需要這幾款模組或是不知道怎麼選？Yupitek（榆閤科技）是專業的硬體整合夥伴，可以幫你確認頻段、插槽和備料問題。

- **產品頁**：[MC7304](/zh-tw/products/sierra/mc7304/)｜[MC7350](/zh-tw/products/sierra/mc7350/)｜[MC7354](/zh-tw/products/sierra/mc7354/)
- **Email**：sales@yupitek.com
