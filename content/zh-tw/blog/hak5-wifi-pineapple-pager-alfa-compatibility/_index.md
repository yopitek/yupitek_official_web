---
title: "HAK5 WiFi Pineapple Pager × ALFA Network：外接 USB 無線網卡相容性評估與設定指南"
description: "這是一份深入評估 HAK5 WiFi Pineapple Pager 在 OpenWrt 環境下與 ALFA Network 外接 USB 無線網卡相容性的技術報告與安裝指南。了解 MIPS 架構交叉編譯、USB 2.0 供電限制及驅動程式設定細節。"
date: 2026-06-19
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "HAK5 WiFi Pineapple Pager 可以外接 ALFA 網卡嗎？"
    answer: "可以，但需注意 MIPS 架構限制與 USB 2.0 供電。AWUS036ACM 為首選，核心內建驅動最穩定。"
  - question: "為什麼 Pager 需要外接供電 USB Hub？"
    answer: "Pager 僅配 USB 2.0 接口，最大輸出 500mA，高功率 ALFA 網卡峰值達 720mA，直接插入會導致重啟或核心崩潰。"
  - question: "AWUS036ACM 為什麼是 Pager 首選網卡？"
    answer: "MT7612U 驅動已整合於 OpenWrt 6.6 核心，Pager 上以 opkg 直接安裝，無需交叉編譯，最穩定可靠。"
  - question: "MIPS 架構對驅動安裝有什麼限制？"
    answer: "Pager 基於 MIPS32 的 MT7628AN，不支援 DKMS，無 GCC 工具鏈，非內建驅動必須在外部 x86 主機交叉編譯。"
  - question: "RTL8812AU 在 Pager 上有什麼已知問題？"
    answer: "RTL8812AU 在 MIPS 平台存在 wiphy_register 核心錯誤，導致介面無法載入，需套用社群修正 patch，建議改用 AWUS036ACM。"
---

HAK5 WiFi Pineapple Pager 可外接 ALFA 網卡，首選 AWUS036ACM 核心內建驅動最穩定，高功率網卡需搭配外接供電 USB Hub 避免核心崩潰。

{{< tldr >}}
Pager 採 MIPS 架構不支援 DKMS，AWUS036ACM 因 MT7612U 驅動內建於 OpenWrt 6.6 核心而隨插即用；AWUS036ACH 需交叉編譯且有 wiphy bug，USB 2.0 供電僅 500mA 需外接 Hub。
{{< /tldr >}}

# HAK5 WiFi Pineapple Pager × ALFA Network：外接 USB 無線網卡相容性評估與設定指南

無線網路安全稽核需要高度精準、多功能性以及合適的硬體支援。**HAK5 WiFi Pineapple Pager** 作為搭載強大 **PineAP v8** 引擎的超便攜、口袋型稽核工具，吸引了大量滲透測試人員的關注。

然而，為了擴大稽核範圍、執行雙頻（2.4 GHz 與 5 GHz）同步操作，或在不干擾 Pineapple 內部無線電的情況下進行多頻道被動監聽，資安專家經常會問：**我可以在 HAK5 Pager 上外接 ALFA Network 無線網卡嗎？**

簡短的答案是：**可以，但需要注意關鍵的硬體和軟體限制。**

在這份詳盡的指南中，我們將剖析技術限制（例如 CPU 架構和 USB 供電限制），評估 ALFA 現售產品線的相容性，並提供逐步的 CLI 安裝與疑難排解指南。

---

## 1. 關鍵技術限制

在將任何高功率 USB 無線網卡插入 HAK5 Pager 之前，您必須了解以下兩大主要障礙：CPU 架構與 USB 供電限制。

### 1.1 CPU 架構：MIPS 架構限制
與運行在 x86_64 的標準 Kali Linux 主機或運行在 ARM 的 Raspberry Pi 不同，HAK5 Pager 搭載的是 **MediaTek MT7628AN SoC**（一個 **MIPS32r2, Little-Endian** 核心，在 OpenWrt 中編譯為 `mipsel_24kc` 平台）。

> [!IMPORTANT]
> 由於 Pager OS 基於 **OpenWrt（版本 24.10.1，核心 6.6.86）**，因此它**不支援 DKMS**（動態核心模組支援）。您無法直接在 Pager 上編譯核心驅動程式原始碼，因為系統不含 GCC 與 Make 工具。任何非內建的驅動程式都必須在外部 x86_64 Linux 主機上，使用 OpenWrt SDK 進行交叉編譯。

### 1.2 USB 2.0 供電：電壓穩定性限制
HAK5 Pager 僅配備單個 USB 2.0 Host 接口。根據標準 USB 2.0 規範，其最大電流輸出為 **500 mA @ 5V（2.5W）**。

像 ALFA AWUS036ACH（RTL8812AU）或 AWUS036AXML（MT7921AUN）這類高功率無線網卡，在執行主動注入（Packet Injection）或密集封包掃描時，其峰值耗電量高達 **720 mA（3.6W）**。

> [!WARNING]
> 若將高功率 ALFA 網卡直接插入 Pager 的 USB 接口，會導致電壓不穩，從而引發**設備重啟、核心崩潰（Kernel Panic）或網卡斷線**。若要穩定運作高功率網卡，您**必須**透過一個**帶外部供電的 USB Hub（5V/2A 以上）**連接網卡。

---

## 2. ALFA 網卡相容性評估矩陣

下表評估了目前在售的 ALFA Network USB 無線網卡與運行 Pager OS（核心 6.6）之 HAK5 Pager 的相容性：

| ALFA 型號 | 晶片組 | 支援頻段 | USB 耗電量 | 核心 6.6 支援狀態 | 安裝方式 | Monitor 與 Injection 支援 | 評估結論與採購建議 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | ~600 mA (需 Hub) | **核心內建 (Native)** | 使用 `opkg` 直接安裝 | ✅ 支援 / ✅ 支援 | 🏆 **首選推薦（最穩定）** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | ~720 mA (需供電 Hub) | 核心未內建 (Out-of-Kernel) | 需使用 SDK 交叉編譯 | ✅ 支援 / ✅ 支援 | ⭐⭐ **進階用戶**（MIPS 平台有 wiphy bug） |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4/5/6 GHz (WiFi 6E) | ~720 mA (需供電 Hub) | **核心內建 (Native)** | 使用 `opkg` + 手動置入韌體 | ✅ 支援 / ✅ 支援 | ⭐⭐⭐ **潛力大**，但供電要求嚴格 |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | ~400 mA (Pager 可直接供電) | 部分內建 | 使用 `opkg` 安裝 | ✅ 支援 / ✅ 支援 | ⭐⭐⭐ **預算折衷方案** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | ~500 mA (邊緣) | 核心未內建 | 需使用 SDK 交叉編譯 | ✅ 支援 / ✅ 支援 | ⭐⭐ **普通**（需要手動編譯驅動） |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | ~500 mA | 核心未內建 | 不建議 | ❌ **不支援監聽** | ❌ **無法使用** |

---

## 3. 逐步設定指南

以下為最推薦型號的 CLI 詳細設定指令。

### 3.1 方案 A：AWUS036ACM (MT7612U) — 免驅動直接支援（最推薦）

**AWUS036ACM** 是 HAK5 Pager 的最佳搭配。其搭載的 MediaTek `mt76` 主線驅動已完整整合於 Linux 6.6 核心中，完全無需繁瑣的核心編譯。

#### 步驟 1：連接硬體
1. 將有源 USB Hub 連接至 HAK5 Pager 的 USB 接口。
2. 將 AWUS036ACM 插入 Hub 中。
3. 透過 SSH 登入 Pager：
   ```bash
   ssh root@172.16.42.1
   ```

#### 步驟 2：驗證裝置識別
執行 `lsusb` 確認系統已成功識別 MediaTek 晶片組：
```bash
lsusb
# 應顯示以下資訊：
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### 步驟 3：使用 opkg 安裝驅動套件
更新套件來源並安裝必要的核心模組與韌體：
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### 步驟 4：修正 MIPS 架構下的 USB Scatter-Gather 崩潰問題
在 MIPS 架構的 OpenWrt 設備上，`mt76-usb` 驅動程式在啟用 USB Scatter-Gather (USB SG) 時，上傳韌體極易崩潰（回報 `-110` 錯誤）。

> [!TIP]
> 為確保無線連線的穩定性，必須透過核心參數停用 USB SG 模式。

在 `/etc/modules.d/` 下寫入停用參數：
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
重啟 Pager 以載入全新參數：
```bash
reboot
```

#### 步驟 5：驗證 Monitor Mode 與封包注入
重啟完成後，SSH 登入並檢查無線網卡介面：
```bash
iw dev
# 應看到新增的 wlan 介面（如 wlan2）
```

啟用 Monitor Mode：
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
驗證介面狀態：
```bash
iw dev wlan2 info
# 應看到："type monitor"
```

---

### 3.2 方案 B：AWUS036ACH (RTL8812AU) — 進階交叉編譯

**AWUS036ACH** 在 Kali Linux 下極具威力和靈敏度，但在 OpenWrt 主線核心 6.6 中未包含其驅動程式，必須手動進行交叉編譯。

#### 前置條件
- 一台運行 Ubuntu 22.04 或 Debian 12 的開發主機 (x86_64)。
- 適用於 `ramips/mt76x8` 目標板的 OpenWrt SDK。

#### 步驟 1：在開發主機上下載並解壓縮 SDK
在您的 Ubuntu 主機上執行：
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### 步驟 2：匯入 rtl8812au 驅動原始碼
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### 步驟 3：設定與編譯核心模組
進入設定選單並選取無線網卡驅動：
```bash
make menuconfig
# 進入：Kernel modules -> Wireless Drivers -> 勾選 kmod-rtl8812au
```
開始編譯：
```bash
make package/kernel/rtl8812au/compile V=s
```

#### 步驟 4：傳送並安裝 `.ipk` 至 Pager
編譯完成後，生成的 `.ipk` 安裝包會位於 `bin/packages/mipsel_24kc/` 中。將其複製至 Pager 安裝：
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> 在 MIPS 架構平台上，`rtl8812au` 外置驅動程式存在知名的 `wiphy_register` 核心錯誤，會導致硬體介面無法在系統中載入。若遇到此情況，必須在編譯前套用社群提供的 MIPS 修正 patch。因此我們仍極度建議優先採用 **AWUS036ACM**。

---

## 4. 解鎖的無線滲透稽核能力

在 HAK5 Pager 上外接相容的 ALFA 網卡可直接解鎖多項高階資安測試功能：

1. **5 GHz 頻段稽核擴展**：Pager 內建的無線晶片能力有限，新增外接雙頻網卡能保證您的監聽及攻擊範圍擴充至 5 GHz 頻段，捕獲現代企業級 AP 的 WPA/WPA2 握手包。
2. **專用攻擊發射電台**：您可以將 Pager 內建的無線電專用於 client 欺騙（Evil Twin / KARMA 攻擊），而將外接的 ALFA 網卡 (`wlan2`) 專門配置為連續的 Deauth 斷線訊號注入源。
3. **PineAP 深度整合**：可在 Pager Web 管理介面或命令行中，將外置網卡設定為 PineAP 的主要偵測或射頻發射介面，將 client 誘捕與回應速度提升 100 倍以上。

---

---

{{< faq >}}

---

## 5. 結論與採購建議

將 ALFA Network 無線網卡整合到 HAK5 WiFi Pineapple Pager 中，可構建一個低調且性能強大的行動滲透測試基站。然而，硬體配置細節至關重要：

- **快速部署、免維護首選**：請購買 [ALFA AWUS036ACM](https://yupitek.com/zh-tw/products/alfa/awus036acm)。其原生 MediaTek 驅動在 OpenWrt 6.6 核心上極為穩定且開箱即用。
- **供電保證**：務必隨身攜帶優質的 **外置供電 USB Hub**，以確保高功率網卡的射頻輸出功率穩定，防止斷線。

如有進一步技術諮詢、大宗硬體採購或客製化 OpenWrt SDK 編譯需求，歡迎隨時聯絡 **Yupitek 技術支援團隊**：

- 🌐 官方網站：[www.yupitek.com](https://www.yupitek.com)
- 📧 聯絡信箱：[sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 聯絡電話：+886-2-87325338
- 📍 公司地址：台北市信義區富陽街34巷72號1樓

---

## 參考來源

1. [Hak5 官方文件 — WiFi Pineapple 產品文件](https://documentation.hak5.org/)
2. [OpenWrt 官方網站 — OpenWrt 24.10 發行版](https://openwrt.org/)
3. [OpenWrt mt76 驅動程式倉庫 — GitHub](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au — 社群驅動 GitHub 倉庫](https://github.com/aircrack-ng/rtl8812au)
5. [ALFA Network 官方網站](https://www.alfa.com.tw/)
