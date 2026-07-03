---
title: "不用編譯驅動！ALFA AWUS036ACM 在 Jetson Orin 邊緣 AI 主機上的免設定實戰指南"
description: "針對 AVALUE AIB-NW01（NVIDIA Jetson Orin NX/Nano）客戶，深度分析哪款 ALFA Network USB 無線網卡最適合邊緣 AI 部署，並實證說明 AWUS036ACM 如何做到真正的插上即用。"
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
featureimage: "/images/blog/awus036acm-jetson-orin-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "為什麼 USB WiFi 網卡在 Jetson Orin 上經常無法使用？"
    answer: "Jetson 使用 NVIDIA 客製化 Tegra 核心，非標準 Ubuntu 核心。第三方驅動常因核心 headers 無法取得或 ABI 不相容而編譯失敗。"
  - question: "AWUS036ACM 在 Jetson Orin 上需要編譯驅動嗎？"
    answer: "不需要。MT7612U 晶片的 mt76x2u 驅動自 Linux Kernel 4.19 起內建核心主線，AIB-NW01 的 Kernel 5.10 已包含，插入即用。"
  - question: "AWUS036ACH（RTL8812AU）能在 Jetson Orin 上使用嗎？"
    answer: "可以但需手動編譯驅動。JetPack 的 NVIDIA kernel patches 可能破壞 cfg80211 ABI，導致編譯失敗，建議有編譯經驗者才使用。"
  - question: "JetPack 升級會讓 USB WiFi 網卡失效嗎？"
    answer: "有可能。第三方驅動在 JetPack 升級後可能因核心 API 變更而失效，需重新編譯。核心內建驅動（如 mt76x2u）則不受影響。"
  - question: "AIB-NW01 使用什麼 Linux 核心版本？"
    answer: "AIB-NW01 出廠搭載 Ubuntu 20.04.6 LTS 與 JetPack 5.0，使用 NVIDIA 客製化 Tegra 核心 5.10.x-tegra，CPU 架構為 ARM64。"
---

ALFA AWUS036ACM 是 Jetson Orin 上唯一真正免編譯、即插即用的 USB WiFi 網卡，因 MT7612U 驅動自 Kernel 4.19 起內建核心主線，完全避開 Jetson 客製核心的驅動編譯問題。

{{< tldr >}}
Jetson Orin 使用 NVIDIA 客製 Tegra 核心，第三方 WiFi 驅動常編譯失敗。ALFA AWUS036ACM 採用 MT7612U 晶片，驅動自 Kernel 4.19 內建核心，插入即用，是唯一真正免編譯的方案。支援監聽模式、封包注入與 AP 模式。
{{< /tldr >}}

## 一封客戶來信，揭開一個關鍵問題

> 「我有一台 AVALUE AIB-NW01（Jetson Orin NX），要部署在沒有有線網路的環境。你們的 USB 無線網卡哪一款可以直接用？」

這是榆閤科技近期收到的客戶詢問。問題聽起來簡單，但如果你在 Jetson 開發者社群待過一陣子就會知道——**USB 無線網卡在 NVIDIA Jetson 平台上，比想像中難搞很多。**

我們從 Jetson 核心架構、NVIDIA 論壇的真實案例、GitHub 上的驅動編譯失敗回報，一路追到 ARM64 平台的實測數據，整理了這份選購指南。

---

## AIB-NW01 的無線連線選項：先了解你的平台

AVALUE AIB-NW01 是專為邊緣 AI 應用設計的**無風扇嵌入式系統**，提供四種 NVIDIA Jetson Orin SoM 配置。以下為其完整硬體規格與軟體環境：

### 硬體規格總覽

| 項目 | 規格 |
|------|------|
| **SoM 選項** | Jetson Orin NX 16GB / NX 8GB / Orin Nano 8GB / Orin Nano 4GB |
| **CPU** | ARM Cortex-A78AE v8.2 64-bit（NX 16GB: 8-core @ 2.0 GHz / NX 8GB: 6-core @ 2.0 GHz / Nano: 6-core @ 1.5 GHz） |
| **GPU** | NVIDIA Ampere 架構（NX: 1024 CUDA Cores + 32 Tensor Cores / Nano 4GB: 512 CUDA Cores + 16 Tensor Cores） |
| **AI 算力** | 100 / 70 / 40 / 20 TOPS（依 SoM 配置） |
| **記憶體** | LPDDR5（NX 16GB/8GB: 128-bit 102.4 GB/s / Nano 8GB: 128-bit 68 GB/s / Nano 4GB: 64-bit 34 GB/s） |
| **儲存** | 128GB M.2 2280 NVMe SSD（內建） |
| **網路** | 2 × GbE RJ-45（10/100/1000 Mbps） |
| **USB** | 4 × USB 3.1 Type-A、1 × Micro USB OTG |
| **顯示** | 1 × HDMI Type-A |
| **序列埠** | 2 × DB9（RS-232 / RS-485 可跳線切換） |
| **擴充插槽** | 1 × M.2 M-Key 2242/2280（NVMe SSD）、1 × M.2 E-Key 2230（WiFi/BT 模組）、1 × M.2 B-Key 3042/3052（5G/LTE 模組，限常溫使用） |
| **SIM** | 1 × Micro SIM 插槽 |
| **電源** | DC 10~24V（2-pin 端子台） |
| **尺寸** | 125 × 196 × 66 mm（不含壁掛架） |
| **重量** | 1.4 kg |
| **機殼材質** | 鋁擠型 + 鋼板、無風扇散熱設計 |
| **運作溫度** | -15°C ~ 60°C（依 IEC60068-2，0.5 m/s 風流） |
| **儲存溫度** | -40°C ~ 80°C |
| **安規認證** | CE、FCC Class A |

### 軟體環境

| 項目 | 規格 |
|------|------|
| **作業系統** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **NVIDIA SDK** | JetPack 5.0（內含 CUDA 11.4、cuDNN 8.4、TensorRT 8.4） |
| **Linux 核心** | 5.10.x-tegra（NVIDIA 客製化 Tegra 核心，**非標準 Ubuntu 核心**） |
| **CPU 架構** | ARM64 (aarch64) |
| **AI SDK 資源** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **關鍵提醒**：Jetson 平台使用的是 NVIDIA 維護的客製化核心 `linux-tegra`，而非標準 Ubuntu 核心。這對第三方驅動的相容性有深遠影響——詳見下方「USB 無線網卡在 Jetson Orin 上的三大挑戰」。

這台主機提供了三種無線連線路徑：

### M.2 2230 E-Key（WiFi 模組插槽）

**優點**：速率高、內建於主機板、不佔用 USB 埠
**缺點**：需拆機安裝、天線連接器固定在機殼內、更換不易、模組相容性需逐一驗證

### USB 3.1 Type-A（4 埠）

**優點**：熱插拔、免拆機、天線可放置於最佳訊號位置、可跨設備共用
**缺點**：USB 網卡體積較大、速度上限取決於 USB 介面

### 5G M.2 B-Key（選配）

**優點**：獨立連線、不需依賴場域 WiFi 基礎設施
**缺點**：成本高、需 SIM 卡與月費方案、設定複雜

對於大多數邊緣 AI 部署場景——POC 階段、戶外監控、工廠產線——**USB 無線網卡是彈性最高、成本最低的選擇。**

但問題來了：隨便買一張 USB WiFi 網卡插上 Jetson，能用嗎？

答案是：**不一定。而且失敗的機率比你想像的高很多。**

---

## USB 無線網卡在 Jetson Orin 上的三大挑戰

大多數 USB WiFi 文章只談 x86 Linux，但 Jetson 平台完全是另一回事。

### 挑戰一：你的核心不是 Ubuntu 核心

Jetson 運行的是 **NVIDIA 客製化的 Tegra Linux 核心**，而非標準的 Ubuntu 核心。這意味著：

- `apt install linux-headers-$(uname -r)` 很可能**無法取得對應的核心 headers**
- NVIDIA 會對核心施加 patch，可能破壞第三方驅動所需的 ABI
- 核心模組編譯環境與 x86 桌機完全不同

一般的「支援 Linux」USB 網卡，**不保證能在 Jetson 上編譯成功**。

### 挑戰二：第三方驅動編譯在 Jetson 上經常失敗

GitHub 上的真實案例（2025 年 4 月）：在 JetPack 6.2 (kernel 5.15.148-tegra) 上，RTL8812EU 驅動的 `make` 和 `dkms` 都報錯。社群分析後發現——**JetPack 的 NVIDIA kernel patches 會破壞 cfg80211 ABI**，導致第三方 WiFi 驅動無法正確編譯。

> 來源：[GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### 挑戰三：JetPack 升級可能讓你的網卡「失效」

NVIDIA 論壇案例（2024 年 10 月）：RTL8188EUS 在 JetPack 5.1.x 上運作正常，升級到 JetPack 6 後**完全無法辨識**。解法是從 GitHub 手動重新編譯驅動——但如果新的 JetPack 又改了核心 API 呢？

> 來源：[Jetson Orin Nano — JetPack 6 不支援 RTL8188EUS](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### 教訓總結

> **在 Jetson 平台上，唯一真正可靠的選擇，是使用 Linux 核心內建（in-kernel）驅動的 USB 無線網卡。**

因為 NVIDIA 必須維持核心內建驅動的相容性——這是你的網卡在 JetPack 升級後還能繼續用的唯一保障。

---

## 晶片相容性總覽：一張表看懂

以下整理 Jetson Orin 常見的 ALFA Network USB 無線網卡晶片相容狀況：

| 晶片 | ALFA 型號 | 驅動方式 | 最低 Kernel 需求 | Jetson Orin 結論 |
|------|-----------|----------|-----------------|------------------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** | **4.19+** | ✅ 完美相容，插上即用 |
| RTL8812AU | AWUS036ACH | Out-of-tree（需編譯） | 需手動編譯 | ⚠️ 可考慮但編譯有風險 |
| RTL8811AU | AWUS036ACS | Out-of-tree（需編譯） | 需手動編譯 | ⚠️ 同 RTL8812AU 問題 |
| RTL8812BU | AWUS036AX | Out-of-tree（需編譯） | 需手動編譯 | ⚠️ 需編譯，有已知問題 |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | **5.18+** | ❌ K5.10/5.15 不滿足 |
| RTL8832CU | AWUS036AXER | Out-of-tree（需編譯） | 需手動編譯 | ❌ 不建議，ARM64 支援不明 |

數據來源：[morrownr/USB-WiFi 晶片支援表](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## 首選推薦：ALFA AWUS036ACM（MediaTek MT7612U）

### 產品規格速覽

| 項目 | 內容 |
|------|------|
| 晶片 | MediaTek MT7612U / MT7612UN |
| WiFi 規格 | 802.11ac (WiFi 5) 雙頻 AC1200 |
| 峰值吞吐 | 5 GHz: 867 Mbps / 2.4 GHz: 300 Mbps |
| 天線 | 2 × RP-SMA 可拆式 5 dBi 雙頻天線 |
| 介面 | USB 3.0（USB-C 接頭） |
| 發射功率 | 標準功率，適合 USB 埠直插 |

**產品頁面**：https://yupitek.com/zh-tw/products/alfa/awus036acm/

### 推薦原因一：唯一「真·免驅動」方案

AWUS036ACM 使用的 MT7612U 晶片，其驅動 `mt76x2u` 自 **Linux Kernel 4.19（2018 年 10 月）** 起已內建於核心主線。AIB-NW01 的核心版本是 5.10.x，因此：

**插上就能用。不用編譯、不用設定。**

這在 Jetson 平台上至關重要——你完全避開了前面提到的三大挑戰（客製核心、編譯失敗、升級失效）。

### 推薦原因二：ARM64 平台實證可用

GitHub 使用者在 ARM64 + Kernel 5.10.198 環境下測試 AWUS036ACM：

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**開箱即用**，模組名為 `mt76x2u`，無需任何額外步驟。

> 來源：[GitHub issue #574 — AWUS036ACM on ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### 推薦原因三：完整專業功能支援

這張網卡不只是能上網，還支援完整的無線網路專業功能：

- 監控模式 (Monitor mode) — 適用於網路診斷與分析
- 封包注入 (Packet injection) — 適用於滲透測試與研究
- AP 模式 — 可將 AIB-NW01 變成 WiFi 熱點（5 GHz 可能需要 `disable_usb_sg` 模組參數）
- VIF (Virtual Interface) — 可在同一張網卡上同時跑 monitor + managed 介面

### 推薦原因四：天線彈性無可比擬

2 × RP-SMA 外接天線設計，意味著你可以：

- 更換高增益天線（如 9 dBi）擴大覆蓋範圍
- 使用指向性天線集中訊號於特定方向
- 透過延長線將天線延伸至金屬機殼外部（工業機櫃場景中尤其重要）

---

## AWUS036ACM 帶來的五大具體效益

### 效益一：立即連線，部署零延遲

插入後立即被系統辨識為 `wlan0`（或 `wlx...`）介面。使用者只需三個指令：

```bash
# 掃描可用網路
sudo nmcli device wifi list

# 連線
sudo nmcli device wifi connect "你的SSID" password "你的密碼"
```

不用編譯、不用重開機、也不用裝任何套件。

### 效益二：避開 M.2 WiFi 模組的所有限制

| M.2 WiFi 模組 | USB 無線網卡 (AWUS036ACM) |
|---------------|--------------------------|
| 需拆機安裝 | 外接即可，免拆機 |
| 天線固定在機殼內 | 天線可放置於最佳訊號位置 |
| 更換困難 | 熱插拔，秒換 |
| 僅限該台主機使用 | 可跨設備共用 |

### 效益三：適合各種工業部署情境

邊緣 AI 專案的典型場景，AWUS036ACM 都能應付：

- **工廠產線** — 設備旁沒有有線網路埠？插上即可無線連線
- **戶外監控** — WiFi 是唯一的資料回傳通道
- **臨時部署** — POC 階段，不想拆機裝 M.2 模組
- **移動載具** — AGV/AMR 需要穩定的無線連線

### 效益四：長期維護成本最低

使用 in-kernel 驅動的好處很實際：

- JetPack 升級後網卡照樣能用（NVIDIA 自己維護核心內建驅動）
- 不用管 DKMS 或自己編譯驅動
- 核心安全更新不會被卡住
- 省下後續的維護和支援成本

### 效益五：訊號覆蓋可依需求優化

2 × RP-SMA 外接天線設計，讓這張網卡同時也是一個可調配的無線方案。你可以根據部署環境：

- 更換高增益天線（如 9 dBi）擴大覆蓋範圍
- 使用指向性天線集中訊號
- 透過延長線將天線放置於金屬機殼外部（工業機櫃場景）
- 搭配磁性底座天線，吸附於金屬表面

---

## 安裝步驟：真的只要三步

### Step 1：插入

將 AWUS036ACM 插入 AIB-NW01 的 USB 3.0 Type-A 埠。

### Step 2：確認驅動已載入

```bash
lsusb | grep MediaTek
# 預期輸出：ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# 預期輸出：mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### Step 3：連線 WiFi

```bash
# 掃描可用網路
sudo nmcli device wifi list

# 連線
sudo nmcli device wifi connect "Your_SSID" password "Your_Password"

# 確認連線狀態
ip addr show wlx...
```

完成。你的 Jetson Orin 已經連上網路。

---

## 注意事項與誠實說明

### AWUS036ACM 是 WiFi 5（AC1200）

它不是市面上最快的選項。AWUS036AXM（WiFi 6E，MT7921AU）理論上更快，但在 AIB-NW01 的 Kernel 5.10 上**無法使用**（需 Kernel 5.18+）。對大多數邊緣 AI 應用的頻寬需求（資料傳輸、模型更新、遠端 SSH）而言，AC1200 已綽綽有餘。

### ARM64 實驗證據

GitHub issue #574 的驗證是在 **Odroid M1**（ARM64 + Kernel 5.10）上完成，並非直接在 AIB-NW01 上測試。兩者使用相同的核心架構與驅動堆疊，我們高度確信結果一致，但仍建議使用者進行實機確認。

### 其他型號的適用場景

AWUS036ACH（RTL8812AU）和 AWUS036AX（RTL8812BU）並非不能使用，只是需要在 Jetson 上手動編譯驅動。如果你有編譯環境的經驗且願意維護驅動，這些型號也值得考慮。

---

{{< faq >}}

## 結語：最簡單的方案往往是最好的

回到最開始的客戶問題：哪一款 ALFA USB 無線網卡最適合 AVALUE AIB-NW01？

答案是 **ALFA AWUS036ACM**。

不是因為它最快或最便宜——而是它是在 Jetson 這種特殊平台上，**唯一真正插上去就能用的方案**。在一個連編譯驅動都經常失敗的平台上，in-kernel 驅動才是王道。

### 立即行動

- 查看產品詳情：https://yupitek.com/zh-tw/products/alfa/awus036acm/
- 技術支援：榆閤科技提供台灣本地技術支援，歡迎聯繫我們

### 延伸閱讀

- [AWUS036ACH vs AWUS036ACM：RTL8812AU 與 MT7612U 驅動方式完整比較](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [ALFA Network Linux 相容性總表](https://docs.alfa.com.tw/Support/Compat/)
- [NVIDIA 官方驗證 WiFi 模組清單（AGX Orin）](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **標籤**：#JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yupitek
>
> **作者**：榆閤科技 (Yupitek Ltd) — ALFA Network 台灣授權代理商
>
> **免責聲明**：本文研究資料截至 2026 年 5 月。Jetson 平台與 Linux Kernel 持續更新，建議部署前確認最新的 JetPack 版本與核心內建驅動支援狀況。

## 參考來源

1. [AVALUE Technology AIB-NW01 產品頁面](https://www.avalue.com.tw/)
2. [NVIDIA Jetson 官方開發者論壇](https://forums.developer.nvidia.com/)
3. [morrownr/USB-WiFi 晶片支援表](https://github.com/morrownr/USB-WiFi)
4. [Linux Kernel mt76 驅動文件](https://wireless.wiki.kernel.org/en/users/drivers/mt76)
5. [ALFA Network Linux 相容性總表](https://docs.alfa.com.tw/Support/Compat/)
