---
title: "ALFA USB 網卡 Linux 驅動怎麼選：MediaTek 免編譯 vs Realtek 需編譯"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "驅動 / 選購指南"
description: "> **技術支援文件 · 2026-09-03 初版（依 blog-writing-rules.md v1.0 規範撰寫）** > 判定母體：Yupitek 現役 ALFA USB 網卡中本次技術文件矩陣已收錄的 6 款機型（3 款 MediaTek、3 款 Realtek）。 > 相關文章：[AL"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **技術支援文件 · 2026-09-03 初版（依 blog-writing-rules.md v1.0 規範撰寫）**
> 判定母體：Yupitek 現役 ALFA USB 網卡中本次技術文件矩陣已收錄的 6 款機型（3 款 MediaTek、3 款 Realtek）。
> 相關文章：[ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)｜[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)｜[ALFA 無線網卡是否支援 Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[ALFA 無線網卡是否支援 DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## 一句話結論

**6 款盤點機型中，3 款 MediaTek 晶片（MT7610U / MT7612U / MT7921AUN）在現代 kernel 已內建驅動、插上即用；3 款 Realtek 晶片（RTL8812AU / RTL8811CU / RTL8832BU）一律需要手動編譯 out-of-tree 驅動。** 想省事，先看晶片再下單。

---

## 第一幕：場景——為什麼有人插上就能用，有人編譯兩小時

兩個真實情境：

- 客戶 A 把 **AWUS036ACM** 插上 Ubuntu 桌機，`lsusb` 一跑、NetworkManager 直接出現 wlan0——什麼都沒裝。
- 客戶 B 把 **AWUS036ACH** 插上同樣的機器，網卡完全沒反應，得上 GitHub 拉原始碼、裝 build 工具、編譯、重開機。

差別不在運氣，也不在 Linux 發行版，而在**晶片組屬於哪個陣營**：MediaTek 的 USB WiFi 晶片驅動（mt76 系列）早已進入 Linux kernel mainline；Realtek 的高階 USB WiFi 晶片驅動至今仍以 out-of-tree（核心之外）形式散布，要靠社群維護的驅動 repo 手動安裝。

## 第二幕：機制——in-kernel 與 out-of-tree 差在哪

### MediaTek：mt76 主線驅動，插上即用

MediaTek USB 晶片的驅動由 kernel 的 **mt76** 子系統涵蓋：

| 機型 | 晶片組 | kernel 驅動模組 | 免編譯條件 |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | kernel 內建，無版本門檻疑慮 |
| AWUS036ACM | MT7612U | mt76x2u | kernel 內建，無版本門檻疑慮 |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **需 kernel 5.19+** |

⚠️ 唯一的坑：**MT7921AUN 的 kernel 門檻是 5.19+**。老平台（如 Jetson Nano 的 JetPack 4.x，kernel 4.9）無法 backport，直接不可用——這是我們在 Jetson Nano 技術文件中驗證過的結論（見 [ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4）。

### Realtek：out-of-tree，一律手動編譯

Realtek USB 晶片沒有可用的 mainline 驅動，依賴社群維護的驅動 repo。目前最活躍的維護者是 **morrownr**，本盤點 3 款晶片對應 3 個 repo：

| 機型 | 晶片組 | 驅動 repo（morrownr 維護） | 2026-09-03 查核 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ 已查核 |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ 已查核 |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ 已查核 |

### 套用到三種典型環境

| 環境 | kernel | MediaTek 陣營（3 款） | Realtek 陣營（3 款） |
|---|---|---|---|
| GB10 / DGX Spark 類平台 | 6.x + aarch64 | 全數可用（mt76 內建） | 全數需編譯（ARM64 可成） |
| Jetson Nano（JetPack 4.x） | 4.9 | 7610U/7612U 可用；MT7921AUN **不可用** | 8812au 可編譯（ARM64 支援）；其餘未驗證 |
| OpenWrt 路由器 | 依版本 | 全數可用（MT7921AUN 需 23.05+） | 需對應 kmod 或編譯，難度高 |

（各環境的完整判定矩陣見 [ALFA 無線網卡是否支援 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)、[ALFA 無線網卡是否支援 NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)、[ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)。）

## 第三幕：工具箱——三分鐘判定流程與安裝步驟

### 判定表：拿到網卡先做這三步

```bash
# 步驟 1：確認系統看得到網卡（記下 VID:PID）
lsusb

# 步驟 2：查 kernel 是否已載入對應驅動
lsmod | grep -E "mt76|rtl8"

# 步驟 3：確認 kernel 版本（決定 MT7921AUN 可否使用）
uname -r
```

判定邏輯（母體：上表 6 款機型）：

1. `lsusb` 出現 **MediaTek / MT76xx** → in-kernel 陣營，kernel ≥ 5.19（MT7921AUN 機型）或任意近代 kernel，即插即用。
2. `lsusb` 出現 **Realtek RTL88xx** → out-of-tree 陣營，走下方安裝步驟。
3. `lsusb` **完全沒有**新裝置 → 先換 USB 埠／線材排除硬體問題，再確認機型是否為 Wi-Fi 6 的 RTL8832BU（部分批次需 `usb_modeswitch`，該步驟屬於個別機型問題，不在本盤點矩陣內，暫不展開）。

### Realtek 陣營通用安裝（以 AWUS036ACH 為例）

```bash
# 步驟 1：安裝編譯依賴（Debian/Ubuntu 系）
sudo apt install build-essential dkms linux-headers-$(uname -r)

# 步驟 2：取得驅動原始碼（機型對應 repo 見上表）
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# 步驟 3：安裝（DKMS 註冊，換 kernel 不用重裝）
sudo ./install-driver.sh

# 步驟 4：重開機後驗證
lsmod | grep 88XXau
ip link   # 應出現新的 wlan 介面
```

> **表 1 結論：判定先於安裝——先看晶片組，90 秒決定你是「插上即用」還是「進 repo 編譯」，不必先撞牆。**

### 選購建議（結論句）

- **要免編譯**：選 MediaTek 陣營（AWUS036ACHM / ACM / AXML），近代 kernel 全部即插即用。
- **要 Wi-Fi 6 且免編譯**：選 AWUS036AXML（MT7921AUN），但先確認 kernel ≥ 5.19。
- **有特殊需求非 Realtek 不可**（如特定 monitor mode 工具鏈）：預留 20–40 分鐘做驅動編譯，並確認目標平台有 kernel headers。

## 已知限制與反駁條件

本文結論在以下條件**不成立**，請改採替代方案：

1. **kernel 5.19 以下 + MT7921AUN**：mt7921u 無法 backport（依賴現代 kernel 基礎設施），結論反轉為「不可用」。這是本文最重要的例外。
2. **非 x86/ARM64 Linux**（如某些 MIPS 路由器）：morrownr repo 未保證可編譯，需以 OpenWrt 的 kmod 優先（見 [ALFA 無線網卡是否支援 OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)）。
3. **驅動 repo 版本演進**：morrownr repo 以日期命名（如 rtl8852bu-20250826），未來可能改版或移除；安裝前請以 repo 現況為準。
4. **monitor mode / AP 模式能力**：同晶片不同 kernel 版本的能力有差異（例如 OpenWrt 22.03+ 的 rtl8812au-ct 在 24.10 有 crash 回報），精細的能力矩陣以各環境專文為準。
5. **RTL8832BU（AWUS036AX/AXER）不在本文盤點的 6 款機型內，但客服常會被連帶問到**：驅動維護者 morrownr 已公開表示該晶片系列「是很糟糕的驅動，懷疑晶片本身有問題」，建議 Linux 使用者現階段避開，不只是「需要編譯」的難度問題，回覆客戶時應如實說明。

## 參考來源

| 來源 | 說明 | URL | 查核狀態 | 查核日期 |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux 驅動 | https://github.com/morrownr/8812au-20210820 | ✅ 已查核 | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux 驅動 | https://github.com/morrownr/8821cu-20210916 | ✅ 已查核 | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux 驅動 | https://github.com/morrownr/rtl8852bu-20250826 | ✅ 已查核 | 2026-09-03 |
| Yupitek ALFA 產品總覽 | 現役機型與規格 | https://yupitek.com/zh-tw/products/alfa/ | ✅ 已查核 | 2026-09-03 |
| Yupitek Blog：Soft AP 指南 | AP 模式實作驗證文 | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ 已查核 | 2026-09-03 |
| 本站技術文件 9 篇 | 判定矩陣與環境驗證基礎 | 相對連結（見文首「相關文章」） | ✅ 已查核 | 2026-09-03 |

> kernel mt76 官方 wiki 頁：https://wireless.wiki.kernel.org/en/users/drivers/mediatek （已查核，列出各晶片支援起始 kernel 版本，可作為快速核對依據）

## 免責聲明

本文件由榆閤科技（Yopitek Ltd）技術支援整理，規格與驅動狀態可能隨 kernel 與驅動 repo 更新而變動，安裝前請以官方 repo 與原廠規格頁為準。ALFA Network 為本公司正式授權代理品牌。
