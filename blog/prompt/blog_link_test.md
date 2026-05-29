# Blog 文章連結驗證報告

**文章**：0522_article_final2.md  
**文章語言**：zh-TW（繁體中文）  
**測試日期**：2026-05-22  
**測試工具**：Playwright (1.60.0) + curl（二次確認）

---

## 一、測試摘要

| 指標 | 數量 |
|--------|-------|
| 總連結數 | 14 |
| ✅ PASS | 12 |
| ⚠️ WARN | 0 |
| ❌ FAIL | 2 |
| 🔍 語系不符（zh-TW 文章 → /en/ 連結） | 7 |

> ⚠️ 2 個 FAIL 中：1 個為真實 404（blog 文章不存在），1 個為間接連結（DeepWiki 從 curl 確認活著但 Playwright JS timeout）

---

## 二、核心發現：語系不符問題（⚠️ 重要）

> **文章是 zh-TW（繁體中文），但所有 yupitek.com 產品/部落格連結全部指向 /en/（英文版）頁面。**
>
> 繁體中文讀者點擊文章中的連結後，會被帶到英文頁面——這對使用者體驗和轉換率都有負面影響。

### 語系對照表

| 連結名稱 | 當前 /en/ URL | zh-TW 替代 URL | zh-TW 是否存在？ |
|---------|--------------|-------------------|---------------|
| AWUS036ACM 產品頁 | `/en/products/alfa/awus036acm/` | `/zh-tw/products/alfa/awus036acm/` | ✅ 存在 (HTTP 200) |
| AWUS036ACH 產品頁 | `/en/products/alfa/awus036ach/` | `/zh-tw/products/alfa/awus036ach/` | ✅ 存在 (HTTP 200) |
| AWUS036AXML 產品頁 | `/en/products/alfa/awus036axml/` | `/zh-tw/products/alfa/awus036axml/` | ✅ 存在 (HTTP 200) |
| ALFA 全系列產品 | `/en/products/alfa/` | `/zh-tw/products/alfa/` | ✅ 存在 (HTTP 200) |
| ACH vs ACM 部落格 | `/en/blog/awus036ach-vs-awus036acm/` | `/zh-tw/blog/awus036ach-vs-awus036acm/` | ✅ 存在 (HTTP 200) |
| Kali 2026 最佳網卡 | `/en/blog/best-wifi-adapters-kali-linux-2026/` | `/zh-tw/blog/best-wifi-adapters-kali-linux-2026/` | ❌ **不存在 (404)** |
| Blog 首頁 | `/en/blog/` | `/zh-tw/blog/` | ✅ 存在 (HTTP 200) |

> ✅ **好消息**：7 個產品/部落格連結中，6 個的 zh-TW 版本都存在且正常運作。只需把 `/en/` 改為 `/zh-tw/` 即可。
>
> ❌ **注意**：`best-wifi-adapters-kali-linux-2026` 這篇文章在 en 和 zh-tw 都不存在（404），需移除或用現有文章替代。

---

## 三、逐項測試結果

### ✅ 正常連結（12 個）

| 連結名稱 | URL | HTTP | 頁面標題 |
|---------|-----|------|---------|
| AWUS036ACM 產品頁 | yupitek.com/en/products/alfa/awus036acm/ | 200 | ALFA AWUS036ACM — AC1200 Dual-Band USB 3.0 Adapter |
| AWUS036ACH 產品頁 | yupitek.com/en/products/alfa/awus036ach/ | 200 | ALFA AWUS036ACH — AC1200 Dual-Band High-Power USB-C |
| AWUS036AXML 產品頁 | yupitek.com/en/products/alfa/awus036axml/ | 200 | ALFA AWUS036AXML — Wi-Fi 6E USB-C Tri-Band USB Adapter |
| ALFA 全系列產品 | yupitek.com/en/products/alfa/ | 200 | ALFA Network Wireless Adapters |
| ACH vs ACM 部落格 | yupitek.com/en/blog/awus036ach-vs-awus036acm/ | 200 | ALFA AWUS036ACH vs AWUS036ACM: Full Comparison |
| Blog 首頁 | yupitek.com/en/blog/ | 200 | Blog · ALFA Network Authorized Distributor Taiwan |
| yupitek 首頁 (zh-TW) | yupitek.com/zh-tw/ | 200 | ALFA Network 無線網卡台灣代理 | 榆閤科技 |
| GitHub issue #2 | github.com/morrownr/USB-WiFi/issues/2 | 200 | Alfa AWUS036ACM Master Mode · Issue #2 |
| GitHub issue #476 | github.com/morrownr/USB-WiFi/issues/476 | 200 | ALFA AWUS036AXML · Issue #476 |
| GitHub discussion #31 | github.com/morrownr/USB-WiFi/discussions/31 | 200 | Get the full speed out of ALFA AWUS036ACHM |
| GitHub USB-WiFi repo | github.com/morrownr/USB-WiFi | 200 | USB WiFi Adapter Information for Linux |
| GitHub 7612u | github.com/morrownr/7612u | 200 (curl) | MT7612U 專屬文件（Playwright timeout，curl 確認可存取） |

### ❌ 失敗連結（2 個）

| 連結名稱 | URL | 狀態 | 問題 |
|---------|-----|------|------|
| **Kali 2026 最佳網卡** | `yupitek.com/en/blog/best-wifi-adapters-kali-linux-2026/` | **404** | 這篇文章在 en 和 zh-tw 都不存在 |
| **DeepWiki morrownr** | `deepwiki.com/morrownr/USB-WiFi` | 200 (curl) | Playwright JS timeout，但 curl 確認 HTTP 200 |

---

## 四、詳細結果（JSON）

```json
[
  {
    "label": "AWUS036ACM product",
    "url": "https://yupitek.com/en/products/alfa/awus036acm/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "AWUS036ACH product",
    "url": "https://yupitek.com/en/products/alfa/awus036ach/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "AWUS036AXML product",
    "url": "https://yupitek.com/en/products/alfa/awus036axml/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "ALFA all products",
    "url": "https://yupitek.com/en/products/alfa/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "ACH vs ACM blog",
    "url": "https://yupitek.com/en/blog/awus036ach-vs-awus036acm/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "Kali 2026 best adapters",
    "url": "https://yupitek.com/en/blog/best-wifi-adapters-kali-linux-2026/",
    "status": 404,
    "result": "FAIL",
    "zhTWExists": false,
    "issue": "Page does not exist on any locale"
  },
  {
    "label": "Blog home",
    "url": "https://yupitek.com/en/blog/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "yupitek home zh-TW",
    "url": "https://yupitek.com/zh-tw/",
    "status": 200,
    "result": "PASS",
    "zhTWExists": true,
    "localeMismatch": "zh-TW article but /en/ link"
  },
  {
    "label": "GitHub issue #2",
    "url": "https://github.com/morrownr/USB-WiFi/issues/2",
    "status": 200,
    "result": "PASS"
  },
  {
    "label": "GitHub issue #476",
    "url": "https://github.com/morrownr/USB-WiFi/issues/476",
    "status": 200,
    "result": "PASS"
  },
  {
    "label": "GitHub discussion #31",
    "url": "https://github.com/morrownr/USB-WiFi/discussions/31",
    "status": 200,
    "result": "PASS"
  },
  {
    "label": "GitHub USB-WiFi repo",
    "url": "https://github.com/morrownr/USB-WiFi",
    "status": 200,
    "result": "PASS"
  },
  {
    "label": "GitHub 7612u",
    "url": "https://github.com/morrownr/7612u",
    "status": 200,
    "result": "PASS (curl confirmed, Playwright timeout)"
  },
  {
    "label": "DeepWiki morrownr",
    "url": "https://deepwiki.com/morrownr/USB-WiFi",
    "status": 200,
    "result": "PASS (curl confirmed, Playwright timeout)"
  }
]
```

---

## 五、修正建議

### 🔴 必須修正

1. **移除或替換 `best-wifi-adapters-kali-linux-2026`** — 這篇文章在 en 和 zh-tw 都不存在（HTTP 404）。建議：
   - 移除該連結，或
   - 替換為現有文章如 `https://yupitek.com/zh-tw/blog/awus036ach-vs-awus036acm/`
   - 如果計劃發布該文章，先發布後再加入連結

### 🟡 建議修正（語系一致性）

將以下 7 個 yupitek.com 連結從 `/en/` 改為 `/zh-tw/`，與文章語言保持一致：

| # | 當前（/en/） | 建議改為（/zh-tw/） |
|---|-------------|-------------------|
| 1 | `/en/products/alfa/awus036acm/` | `/zh-tw/products/alfa/awus036acm/` |
| 2 | `/en/products/alfa/awus036ach/` | `/zh-tw/products/alfa/awus036ach/` |
| 3 | `/en/products/alfa/awus036axml/` | `/zh-tw/products/alfa/awus036axml/` |
| 4 | `/en/products/alfa/` | `/zh-tw/products/alfa/` |
| 5 | `/en/blog/awus036ach-vs-awus036acm/` | `/zh-tw/blog/awus036ach-vs-awus036acm/` |
| 6 | `/en/blog/best-wifi-adapters-kali-linux-2026/` | ⚠️ 先移除（不存在） |
| 7 | `/en/blog/` | `/zh-tw/blog/` |

### 🟢 不需修正

- GitHub 外部連結（github.com）— 無語系區別，正常
- DeepWiki 外部連結 — HTTP 200（curl 確認），正常

---

## 六、ALFA 全系列產品連結（已修正）

原連結 `https://yupitek.com/en/products/category/alfa-network/` 已修正為 `https://yupitek.com/en/products/alfa/` ✅

（若語系一併修正，最終應為 `https://yupitek.com/zh-tw/products/alfa/`）

---

> **測試時間**：2026-05-22 22:23 UTC+8  
> **測試環境**：Playwright 1.60.0 / Chromium / Ubuntu 24.04 ARM64  
> **curl 二次確認**：對 Playwright timeout 的連結以 curl 驗證 HTTP status
