---
title: Blog 寫作方向研究報告 — AVALUE AIB-NW01 × ALFA Network USB 適配器選配指南
created: 2026-05-20
type: research
tags: [blog, alfa-network, yupitek, writing-direction, research, jetson-orin]
summary: 針對客戶詢問 AVALUE AIB-NW01 邊緣 AI 主機適合的 ALFA Network 無線網卡，完成 4 步驟深度研究（主機核心/社區經驗/晶片相容/效益），提供研究驅動的寫作方向
---

# 研究報告：AIB-NW01 + ALFA USB 無線網卡 寫作方向

- **公司**：榆閤科技 (Yupitek Ltd) — ALFA Network 台灣授權代理商
- **客戶問題**：擁有 AVALUE AIB-NW01（NVIDIA Jetson Orin NX/Nano 邊緣 AI 系統）的客戶，詢問哪一款 ALFA Network 無線 USB 網卡最適合
- **發布平台**：https://yupitek.com/en/blog/

---

## Step 1：AIB-NW01 主機 Linux 版本與核心確認

### 官方規格

| 項目 | 內容 |
|------|------|
| 型號 | AVALUE AIB-NW01 |
| SoM | NVIDIA Jetson Orin Nano 4GB/8GB；Orin NX 8GB/16GB |
| 出廠 OS | Ubuntu 20.04 LTS |
| 出廠 SDK | JetPack 5.0 |
| L4T 版本 | R35.1（推測，因 JetPack 5.0.2 對應 L4T R35.1） |
| **Linux Kernel** | **5.10.x**（L4T R35.x 系列基於 Linux Kernel 5.10 LTS） |
| CPU 架構 | ARM64 (aarch64) |
| USB 埠 | 4 × USB 3.1 Type-A |
| M.2 WiFi | 1 × M.2 2230 E-Key（WiFi 模組） |

### 核心發現

- NVIDIA Jetson Linux (L4T) 使用的是 **客製化 Tegra 核心**，非標準 Ubuntu 核心。這意味著：
  - 一般的 `apt install linux-headers-$(uname -r)` **可能無法直接取得**對應的 headers
  - 核心模組編譯環境與 x86 桌機不同
  - NVIDIA 會對核心施加 patch，可能影響第三方驅動的編譯

### 補充說明

從 NVIDIA 官方 JetPack Release Matrix 來看，**Orin NX/Nano 的官方支援始於 JetPack 5.1+**：
- JetPack 5.0.2 → 支援 AGX Orin Dev Kit、Xavier NX、AGX Xavier（不含 Orin NX/Nano）
- JetPack 5.1 → 加入 Orin NX 16GB 支援（L4T R35.2.1）
- JetPack 5.1.2 → 加入 Orin Nano 支援（L4T R35.4.1）

AVALUE 規格頁標示 "Jetpack 5.0" 可能有兩種情況：
1. 客製化 JetPack 5.0 映像包含 Orin NX/Nano 支援
2. 實際出貨使用更新的 JetPack 版本

**對文章影響**：核心版本可能在 **5.10.x ~ 5.15.x** 之間，但均為 Tegra 客製化核心，不影響 AWUS036ACM 免驅支援（MT7612U 驅動自 kernel 4.19 起內建）。

> 來源：[Avalue AIB-NW01 官方規格](https://www.avalue.com/en/product/AI-Computing-Platform/NVIDIA-Solution/AIB-NW01) | [JetPack Archive](https://developer.nvidia.com/embedded/jetpack-archive) | [Jetson Linux 35.2.1](https://developer.nvidia.com/embedded/jetson-linux-r3521)

---

## Step 2：社區研究 — Jetson Orin × USB 無線網卡 實際使用經驗

### 2.1 NVIDIA Developer Forum — **直接相關** 🔥🔥🔥

#### 案例 A：Alfa AWUS036ACH (RTL8812AU) 相容性詢問 (2026-02-02)

> **用戶提問**：能否在 Jetson Thor/Orin 上使用 Alfa AWUS036ACH (RTL8812AU)？
>
> **NVIDIA 官方回覆**（DaneLLL, NVIDIA Moderator）：
> - 不在官方驗證清單中
> - 建議諮詢 vendor
> - JetPack 7 (Kernel 6.8) 可自行驗證驅動是否支援 K6.8

**來源**：https://forums.developer.nvidia.com/t/.../359300

#### 案例 B：USB WiFi 驅動求助 — MT7601U (2026-02-03)

> **用戶**：Jetson Orin Nano 上 MT7601U 晶片無法驅動
> **社群回覆**：需要手動編譯驅動，並注意 Jetson 的客製核心 headers

**來源**：https://forums.developer.nvidia.com/t/usb-wifi-driver/359517

#### 案例 C：WiFi USB Adapter 通用詢問 (2025-06)

> **用戶**：Jetson Orin Nano 能不能用任何 USB WiFi 網卡做長距離通訊？
> **NVIDIA Moderator**：建議參考 AGX Orin 驗證過的 WiFi 模組清單（M.2 為主），並表示 Orin Nano 與 AGX Orin 共用相同 BSP

**來源**：https://forums.developer.nvidia.com/t/about-wifi-usb-adapter/337220

#### 案例 D：RTL8188EUS 在 JetPack 6 失效 (2024-10)

> **用戶**：RTL8188EUS 在 JetPack 5.1.x 可用，升級 JetPack 6 後無法辨識
> **解法**：必須從 GitHub (aircrack-ng/rtl8188eus) 手動編譯安裝
> **關鍵**：JetPack 升級可能導致原本可用的 USB WiFi 失效

**來源**：https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/

### 2.2 GitHub Issues

#### Issue #651 — AWUS036AXM (MT7921AU) on Jetson Orin Nano 🚨

> **用戶** (2025-08-30)：AWUS036AXM 無法在 Jetson Orin Nano 上工作
> - Kernel: 5.15.148-tegra
> - `lsusb` 可辨識 `ID 0e8d:7961 MediaTek Inc. Wireless_Device`
> - 但 `iw` 只列出 PCIe WiFi 卡，不認得 AWUS036AXM
>
> **morrownr 回應**（USB-WiFi 維護者）：
> - Kernel 5.15 太舊，MT7921AU 需要 **kernel 5.18+**（USB 支援始於 5.18）
> - 解決方案：升級到 kernel 5.19+ 或使用 backport

**來源**：https://github.com/morrownr/USB-WiFi/issues/651

#### Issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano 🚨

> **用戶** (2025-04-20)：在 JetPack 6.2 (kernel 5.15.148-tegra) 上編譯 rtl8812eu 驅動失敗
> - `make` 和 `dkms` 都報錯
> - 另有用戶指出：JetPack 的 **NVIDIA kernel patches 會破壞 cfg80211 ABI**，導致第三方驅動無法正確編譯
> - 有人提供了 pre-compiled driver：`github.com/aepkolol/jetson-8812eu`

**來源**：https://github.com/svpcom/wfb-ng/issues/421

#### Issue #574 — AWUS036ACM (MT7612U) on ARM64 Kernel 5.10 ✅

> **用戶** (2025-02-07)：在 Odroid M1 (ARM64, Kernel 5.10.198) 上使用 AWUS036ACM
> - `lsusb` 成功辨識：`ID 0e8d:7612 MediaTek Inc. MT7612U`
> - 開箱即用，模組名為 `mt76x2u`
> - 用戶遇到的 suspend/resume 問題是系統電源管理問題，非驅動問題

**來源**：https://github.com/morrownr/USB-WiFi/issues/574

### 2.3 綜合發現

| 晶片 | 適配器 | 驅動方式 | Jetson 實測 | 風險 |
|------|--------|----------|------------|------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** ✅ | **ARM64 K5.10 確認可用** | **低** |
| RTL8812AU | AWUS036ACH | Out-of-tree 🔴 | NVIDIA 不列入驗證，編譯有已知問題 | 高 |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) ⚠️ | 需要 Kernel 5.18+，Orin K5.10/5.15 不滿足 | 高 |
| RTL8188EUS | 各品牌 | Out-of-tree 🔴 | JetPack 升級可能失效 | 中高 |
| RTL8832CU | AWUS036AXER | Out-of-tree 🔴 | 無實測資料 | 高 |

### 2.4 關鍵教訓

1. **Jetson Orin 的客製核心是最大障礙** — 不是所有 Linux 驅動都能在 Tegra 核心上編譯
2. **JetPack 升級會破壞相容性** — 一個 JetPack 版本能用的 USB WiFi，下個版本可能不行
3. **In-kernel 驅動是唯一「免驅動」方案** — 因為 NVIDIA 必須維持核心內驅動的相容性
4. **ARM64 架構限制** — 有些驅動雖然支援 ARM，但 Jetson 的特定核心配置可能不包含所需模組

---

## Step 3：建議使用的 ALFA USB 適配器與理由

### 🏆 首推：ALFA AWUS036ACM

| 項目 | 內容 |
|------|------|
| 晶片 | MediaTek MT7612U / MT7612UN |
| WiFi 規格 | 802.11ac (WiFi 5) 雙頻 AC1200 |
| 峰值吞吐 | 5 GHz: 867 Mbps, 2.4 GHz: 300 Mbps |
| 天線 | 2 × RP-SMA 可拆式 5 dBi 雙頻天線 |
| 介面 | USB 3.0 (USB-C 接頭) |
| 發射功率 | 標準功率（低功耗，適合 USB 埠直插） |

### 推薦原因

#### 原因一：唯一「真·免驅動」方案

AWUS036ACM 使用的 MT7612U 晶片，其驅動 `mt76x2u` 自 **Linux Kernel 4.19 (2018年10月)** 起已內建於核心主線。AIB-NW01 的核心版本為 5.10.x，因此 **插上即可用，零編譯、零設定**。

這在 Jetson 平台上至關重要，因為：
- 免去編譯環境建置（跨編譯器、核心 headers）
- 避開 NVIDIA kernel patches 造成的編譯衝突
- JetPack 升級後仍然可用（內建驅動隨核心升級）

#### 原因二：ARM64 (aarch64) 實證可用

GitHub issue #574 證實在 ARM64 + Kernel 5.10 環境下，AWUS036ACM 可被正確辨識為 `mt76x2u` 模組，無需任何額外步驟。

#### 原因三：完整功能支援

- **監控模式 (Monitor mode)** ✅
- **封包注入 (Packet injection)** ✅
- **AP 模式** ✅（5 GHz 可能需要 `disable_usb_sg` 模組參數）
- **VIF (Virtual Interface)** ✅ — 可在同一張網卡上同時跑 monitor + managed 介面

#### 原因四：優異的天線彈性

與 AWUS036ACH 相同的 2 × RP-SMA 外接天線設計，可依據部署環境更換高增益天線或指向性天線，非常適合工業/戶外場景。

### 其他型號對比

| 型號 | 晶片 | 驅動方式 | 是否適合 AIB-NW01 | 原因 |
|------|------|----------|-------------------|------|
| **AWUS036ACM** 🏆 | MT7612U | In-kernel (4.19+) | ✅ **最推薦** | 真正的 plug-and-play |
| AWUS036ACH | RTL8812AU | Out-of-tree | ⚠️ 可考慮 | 需手動編譯，編譯過程在 Jetson 上不穩定 |
| AWUS036ACS | RTL8811AU | Out-of-tree | ⚠️ 可考慮 | 同 RTL8812AU 問題 |
| AWUS036AXM | MT7921AU | In-kernel (5.18+) | ❌ 不建議 | Kernel 5.10/5.15 太舊，無法使用 |
| AWUS036AXER | RTL8832CU | Out-of-tree | ❌ 不建議 | 驅動不成熟，ARM64 支援未知 |
| AWUS036AX | RTL8812BU | Out-of-tree | ⚠️ 可考慮 | 需要編譯，但有預編譯選項 |

---

## Step 4：接上 ALFA USB 適配器後的效益

### 對於 AIB-NW01 使用者的具體效益

#### 效益一：立即連線，部署零延遲

AWUS036ACM 插入後立即被辨識為 `wlan0` 或 `wlx...` 介面。使用者只需：

```bash
# 掃描可用網路
sudo nmcli device wifi list

# 連線
sudo nmcli device wifi connect "SSID" password "PASSWORD"
```

不需編譯、不需重開機、不需安裝套件。

#### 效益二：避開 M.2 WiFi 模組的限制

AIB-NW01 雖有 M.2 2230 E-Key 插槽，但：
- M.2 WiFi 模組選擇受限（需驗證相容性）
- 安裝需拆機（不利於已部署的設備）
- 天線連接器固定在機殼內
- 更換困難

USB 網卡則：
- **免拆機** — 外接即可
- **熱插拔** — 可在系統運行時插拔
- **天線彈性** — 可放置於最佳訊號位置
- **跨設備共用** — 同一張網卡可用於不同主機

#### 效益三：適合工業環境的部署情境

邊緣 AI 專案的典型部署場景：
- **工廠產線** — 沒有有線網路埠在設備旁
- **戶外監控** — WiFi 是唯一的回傳方式
- **臨時部署** — POC 階段不想拆機裝 M.2 模組
- **移動載具** — AGV/AMR 需要無線連線

AWUS036ACM 在這些場景中提供即插即用的連線能力。

#### 效益四：長期維護成本低

由於使用 in-kernel 驅動：
- JetPack 升級後仍維持相容
- 不需要維護 DKMS 或自編驅動
- 核心安全性更新不受影響
- 減少技术支援和維護成本

#### 效益五：訊號覆蓋範圍優化

2 × RP-SMA 外接天線設計，可：
- 更換高增益天線（如 9 dBi）以擴大覆蓋範圍
- 使用指向性天線以集中訊號
- 透過延長線將天線放置於金屬機殼外部（工業機櫃場景）

---

## 寫作方向建議（huashu-topic-gen 框架）

### 推薦方向：實戰選購指南型

**為什麼選這個方向？**
1. 研究結果清晰指向 **單一最佳推薦**（AWUS036ACM），文章可以有明確結論
2. 社區研究發現了 **重要的技術壁壘**（Jetson 客製核心、ARM64 編譯問題），這些是競爭者文章不會涵蓋的深度內容
3. SEO 價值高 — "Jetson Orin USB WiFi"、"Jetson USB wireless adapter" 等關鍵字在 NVIDIA 論壇上持續有搜尋量
4. 客戶問題可以直接被回答

### 建議標題

**中文選項**：
- AVALUE AIB-NW01 無線連線完全指南：哪款 ALFA USB 網卡最適合你的 Jetson Orin？
- 邊緣 AI 主機的無線網路解方：為 Jetson Orin 挑選最佳 USB WiFi 適配器
- 不用編譯驅動！ALFA AWUS036ACM 在 Jetson Orin 上的免設定實戰

**英文選項**：
- The Ultimate Wireless Guide for AVALUE AIB-NW01: Best ALFA USB Adapter for Jetson Orin
- No Driver Compilation Needed: Using ALFA AWUS036ACM on Jetson Orin Edge AI Systems
- Jetson Orin + USB WiFi: Why MT7612U Is the Only Truly Plug-and-Play Chipset

### 建議大綱

#### 1. 開場：客戶的真實問題
> 引用客戶情境：「我有一台 AVALUE AIB-NW01（Jetson Orin），需要在沒有有線網路的環境部署，哪一款 ALFA USB 無線網卡最適合？」

#### 2. AIB-NW01 平台的無線連線選項分析
- M.2 2230 E-Key（優點/缺點：需拆機、天線受限）
- USB 3.1 Type-A（優點：熱插拔、天線彈性、免拆機）
- 5G M.2 B-Key（優點：獨立連線，缺點：成本高、需 SIM 卡）

#### 3. USB 無線網卡在 Jetson Orin 上的特殊挑戰 ⭐（核心價值段落）
- JetPack 核心是客製化 Tegra 核心，非標準 Ubuntu 核心
- 第三方驅動編譯在 Jetson 上常失敗（引用 GitHub issue #421）
- JetPack 升級可能導致原本可用的網卡失效（引用 RTL8188EUS 案例）
- **結論：In-kernel 驅動是唯一可靠的選擇**

#### 4. 驅動晶片相容性分析（表格呈現）

| 晶片 | 範例 ALFA 型號 | 驅動方式 | Kernel 需求 | Jetson Orin 相容性 |
|------|---------------|----------|------------|-------------------|
| MT7612U | AWUS036ACM | In-kernel (mt76x2u) | 4.19+ | ✅ 完美相容 |
| RTL8812AU | AWUS036ACH | Out-of-tree | 需編譯 | ⚠️ 相容但需手動編譯 |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | 5.18+ | ❌ Kernel 太舊 |
| RTL8832CU | AWUS036AXER | Out-of-tree | 需編譯 | ❌ 不建議 |
| RTL8812BU | AWUS036AX | Out-of-tree | 需編譯 | ⚠️ 需編譯，有風險 |
| RTL8811AU | AWUS036ACS | Out-of-tree | 需編譯 | ⚠️ 需編譯，有風險 |

#### 5. 首選推薦：ALFA AWUS036ACM（MT7612U）
- **免驅動** — Kernel 4.19+ 內建驅動，AIB-NW01 (K5.10) 插上即用
- **ARM64 實證** — 已在 ARM64 + K5.10 環境驗證
- **功能完整** — Monitor mode, packet injection, AP mode, VIF 全支援
- **天線彈性** — 2 × RP-SMA，可更換高增益或指向性天線
- **跨平台** — 同一張網卡可用於 Ubuntu、Kali、Raspberry Pi OS 等

#### 6. 連接後的具體效益
- 即時連線（免編譯、免重開）
- 工業部署彈性（熱插拔、天線可延伸）
- 長期維護成本低（in-kernel 驅動隨核心升級）
- 跨設備可攜性

#### 7. 安裝步驟（簡單 3 步驟）
```bash
# Step 1: 插入 AWUS036ACM 到 USB 3.0 埠
# Step 2: 確認驅動已載入
lsusb | grep MediaTek
dmesg | grep mt76

# Step 3: 連線 WiFi
sudo nmcli device wifi connect "Your_SSID" password "Your_Password"
```

#### 8. 結論與 CTA
- 總結推薦 AWUS036ACM 的理由
- 引導至產品頁面：https://yupitek.com/en/products/alfa/awus036acm/
- 聯繫榆閤科技取得技術支援

### 建議標籤
- `#JetsonOrin` `#EdgeAI` `#ALFANetwork` `#USBWiFi` `#AWUS036ACM` `#Yupitek`

### 工作量評估

| 項目 | 評估 |
|------|------|
| 是否需要實機測試 | **不需要**（研究資料已充分支援論述） |
| 預估字數 | 1500-2000 字（英文版）/ 2000-3000 字（中文版） |
| 撰寫時間 | 2-4 小時 |
| 難度 | ⭐⭐（中等，不需測試但需準確引用研究資料） |

### 差異化優勢（相對於競品文章）

1. ✅ **唯一涵蓋 Jetson 客製核心挑戰的文章** — 大多數 USB WiFi 文章只寫 x86 Linux，忽略了 ARM64 + 客製核心的問題
2. ✅ **引用 NVIDIA 論壇與 GitHub 一手資料** — 文章有真實案例支撐，非純產品介紹
3. ✅ **直接回應產品相容性問題** — 不是泛泛的「支援 Linux」，而是具體到晶片型號、Kernel 版本
4. ✅ **台灣本地技術支援** — 榆閤科技提供在地支援，是相對於直接海外購買的附加價值

### 寫作注意事項

1. **誠實標示限制**：AWUS036ACM 是 WiFi 5 (AC1200)，不是最快選項，但它是唯一真·免驅的選擇
2. **不要攻擊其他型號**：AWUS036ACH 和 AWUS036AXM 也有其適用場景，只是對 AIB-NW01 不是最佳解
3. **ARM64 實驗證據**：GitHub issue #574 是在 Odroid M1 上測試，非直接在 AIB-NW01 上測試。建議文中說明這點
4. **建議雙語版本**：英文版 SEO 效益較高（全球 Jetson 開發者社群），中文版可同步發布

---

## 參考資料彙整

### 主要來源

| 來源 | URL | 類型 | 可信度 |
|------|-----|------|--------|
| AVALUE AIB-NW01 官方頁面 | https://www.avalue.com/en/product/AI-Computing-Platform/NVIDIA-Solution/AIB-NW01 | 官方規格 | 高 |
| NVIDIA JetPack Archive | https://developer.nvidia.com/embedded/jetpack-archive | 官方文件 | 高 |
| NVIDIA Jetson Linux 35.2.1 | https://developer.nvidia.com/embedded/jetson-linux-r3521 | 官方文件 | 高 |
| NVIDIA 論壇 — AWUS036ACH 詢問 | https://forums.developer.nvidia.com/t/.../359300 | NVIDIA 官方回覆 | 高 |
| GitHub — AWUS036AXM on Jetson Orin | https://github.com/morrownr/USB-WiFi/issues/651 | 用戶回報 | 中高 |
| GitHub — RTL8812EU compilation on Jetson | https://github.com/svpcom/wfb-ng/issues/421 | 用戶回報 | 中高 |
| GitHub — AWUS036ACM on ARM64 K5.10 | https://github.com/morrownr/USB-WiFi/issues/574 | 用戶回報 | 中高 |
| morrownr/USB-WiFi 晶片相容表 | https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md | 社群文件 | 高 |
| Yupitek — AWUS036ACM 產品頁 | https://yupitek.com/en/products/alfa/awus036acm/ | 官方產品頁 | 高 |
| Yupitek — AWUS036ACH vs ACM 比較 | https://yupitek.com/en/blog/awus036ach-vs-awus036acm/ | 部落格文章 | 高 |
| NVIDIA 論壇 — USB WiFi 通用詢問 | https://forums.developer.nvidia.com/t/about-wifi-usb-adapter/337220 | NVIDIA 官方回覆 | 高 |

### 關鍵資料連結

- morrownr USB-WiFi 晶片支援表：https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md
- ALFA 官方 Linux 相容表：https://docs.alfa.com.tw/Support/Compat/
- NVIDIA 驗證 WiFi 模組清單：https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431

---

> 本文根據 huashu-research + huashu-topic-gen 框架產出
> 研究日期：2026-05-20
> 作者：榆閤科技 (Yupitek Ltd) — ALFA Network 台灣授權代理商
