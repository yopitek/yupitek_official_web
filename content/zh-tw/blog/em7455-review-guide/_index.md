---
title: "EM7455 完整評測：為什麼它是 Maker 與工程師最愛的 Sierra 網卡"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - 產品評測
series:
  - sierra-wireless-selection
series_order: 2
description: "EM7455 完整評測：規格、EM7430 差異、OpenWrt/Linux 設定、Dell/Lenovo 相容性。本文由 Yupitek（榆閤科技）整理提供技術資料。"
author: "yupitek"
draft: false
faq:
  - question: "EM7455 支援 5G 嗎？"
    answer: "不支援。EM7455 是 LTE-A Cat 6 模組，最高 300 Mbps。若需 5G（Sub-6 或 mmWave），可參考 EM9190（Sub-6）或 EM9191（Sub-6 + mmWave）。"
  - question: "EM7455 在台灣可以用嗎？"
    answer: "一般而言可以搭配台灣主流電信商 SIM 卡使用，實際訊號表現與可用頻段依基地台位置、電信商網路規劃與載波聚合支援而定，建議下單前與我們確認你所在地區與電信商的相容性。"
  - question: "EM7455 跟 MC7455 差在哪？"
    answer: "核心晶片相同，皆為 Qualcomm MDM9230，規格一致。唯一差別是封裝：EM7455 為 M.2，MC7455 為 mPCIe。選哪顆純看你的插槽。"
  - question: "EM7455 跟 EM7430 差在哪？"
    answer: "同一顆 MDM9230 晶片，核心規格相同。主要差異在於目標頻段配置：EM7455 主要涵蓋美洲與 EMEA 頻段，EM7430 主要涵蓋亞太頻段，詳細頻段清單請洽詢確認最新官方規格書。"
  - question: "Dell DW5811e 就是 EM7455 嗎？"
    answer: "是的，DW5811e 是 Dell 品牌版的 EM7455，核心為同一顆 Qualcomm MDM9230。多數 Dell 筆電社群回報不鎖 BIOS 白名單，但實際情況建議以你的機型為準。"
---

EM7455 是 Sierra Wireless 的 LTE-A Cat 6 M.2 蜂窩模組，採用 Qualcomm MDM9230 晶片，支援最高 300 Mbps 下載、50 Mbps 上傳，內建 GNSS 定位，工作溫度 -40°C 至 +85°C。本文由榆閤科技（Yupitek）整理提供規格解析與設定參考。

Sierra Wireless EM7455 為 M.2 B-Key 封裝的 4G LTE-Advanced Cat 6 模組，廣泛應用於 OpenWrt 路由器、樹莓派行動基地台、工業閘道器與商用筆電 WWAN。以下設定步驟為社群與官方文件常見流程整理，實際指令請依你的作業系統版本、韌體版本自行核對後執行，執行前建議先備份現有設定。

> 產品連結：[EM7455 — Yupitek 產品頁](https://yupitek.com/zh-tw/products/sierra/em7455/) | 官方規格書：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完整規格表

以下規格數字整理自 Sierra Wireless 官方規格書與公開資料，實際下單前建議向我們索取最新官方文件逐項核對，尤其是頻段、韌體版本等會隨時間更新的項目。

| 項目 | 規格 |
|---|---|
| **型號** | AirPrime EM7455 |
| **蜂窩標準** | LTE-A Cat 6 |
| **晶片組** | Qualcomm MDM9230（Snapdragon X7 LTE） |
| **下載峰值** | 300 Mbps（LTE-A，2×CA） |
| **上傳峰值** | 50 Mbps（LTE-A） |
| **載波聚合** | 2×CA（支援多種組合，詳見官方 AT 指令參考） |
| **封裝** | PCI Express M.2 B-Key（52-pin） |
| **尺寸** | 42 × 30 × 2.3 mm |
| **工作溫度** | -40°C ~ +85°C（工業級） |
| **GNSS** | GPS、GLONASS、BeiDou、Galileo |
| **通訊介面** | USB 3.0 / USB 2.0 High Speed |
| **LTE 頻段** | 涵蓋美洲與 EMEA（歐洲/中東/非洲）主流頻段，詳細頻段清單請洽詢確認最新官方規格書 |
| **3G WCDMA 頻段** | 請洽詢確認最新官方規格書 |
| **通用 VID:PID** | `1199:9079`（EM7455，一般版本） |
| **Dell DW5811e VID:PID** | `413c:81b6`（品牌版本，請以實機 `lsusb` 結果為準） |
| **Linux 驅動** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主流發行版皆已內建，具體最低 kernel 版本請以你的發行版說明為準） |
| **通用韌體** | 請以官方 source.sierrawireless.com 最新版本為準，本文不寫死特定版本號以免過時 |
| **運營商認證** | 依電信商與地區時有變動（如 AT&T、Verizon、T-Mobile、Bell、Rogers、Telus、Vodafone 等），請洽詢確認你所在地區最新認證清單 |

---

## EM7455 適合什麼用途？

**EM7455 最適合三類用途：（1）自組 4G LTE 路由器（OpenWrt / ROOter），（2）筆電 WWAN 升級（Dell / Lenovo），（3）工業物聯網閘道器與車聯網 telematics。** 它的核心優勢在於 Linux 驅動成熟度高、社群資源豐富，以及美洲/EMEA 頻段覆蓋較廣。

### 個人 Maker 場景

| 應用 | 搭配 | 理由 |
|---|---|---|
| 樹莓派 4G 路由器 | 樹莓派 4/5 + M.2→USB 轉接板 + OpenWrt / ROOter | EM7455 在 OpenWrt 社群案例中相容性穩定，uqmi 套件成熟 |
| GL.iNet 路由器升級 | GL-MT1300 / GL-AR750S + USB 轉接 | 社群已有 ROOter 掛鉤與 `create_connect.sh` 相關討論可參考 |
| 戶外可攜式 LTE 熱點 | 電池供電 + USB 轉接 + 小型路由器 | EM7455 發熱低、散熱良好，適合物件追蹤 |

### 企業 / 工業場景

| 應用 | 搭配 | 理由 |
|---|---|---|
| 工業路由器 | M.2 插槽工業閘道器（如 Advantech、Cincoze） | 寬溫 -40~85°C，頻段涵蓋範圍廣 |
| 車聯網 telematics | 車載閘道器 + GNSS 天線 | 內建 GPS/GLONASS/BeiDou/Galileo，單一模組解決連網＋定位 |
| 筆電 WWAN 升級 | Dell Latitude / Precision / Lenovo ThinkPad | M.2 B-Key 直插，Linux 驅動支援度高 |
| 備援 WAN | OpenWrt / pfSense 雙 WAN 備援 | QMI/MBIM 雙模式支援，惟 pfSense 支援度相對較弱，建議優先評估 OpenWrt |

---

## EM7455 跟 EM7430 差在哪？

**EM7455 與 EM7430 採用同一顆 Qualcomm MDM9230 晶片，核心規格相同（Cat 6、300/50 Mbps、2×CA、GNSS），主要差異在於目標頻段配置：EM7455 主要涵蓋美洲與 EMEA 頻段，EM7430 主要涵蓋亞太（APAC）頻段。**

| 項目 | EM7455 | EM7430 |
|---|---|---|
| **晶片組** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **蜂窩標準** | LTE-A Cat 6 | LTE-A Cat 6 |
| **下載峰值** | 300 Mbps | 300 Mbps |
| **上傳峰值** | 50 Mbps | 50 Mbps |
| **載波聚合** | 2×CA | 2×CA |
| **封裝** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **目標區域** | 美洲、EMEA（歐洲/中東/非洲） | 亞太（APAC） |
| **詳細頻段清單** | 請洽詢確認最新官方規格書 | 請洽詢確認最新官方規格書 |

> 兩款模組的精確逐頻段清單目前建議以官方最新 Spec Sheet 為準，本文暫不列出逐頻段編號，避免資訊隨官方版本更新而過時或不準確。若您已知道所在地區使用的電信商與頻段需求，歡迎直接與我們聯繫核對哪一款更適合。

**選型建議**：若你的 SIM 卡運營商以北美或歐洲為主，可優先評估 **EM7455**；若主要使用亞太地區運營商（如台灣、日本、澳洲等），可優先評估 **EM7430**。台灣市場因電信業者頻段配置關係，兩款是否皆可運作、哪一款更匹配，建議下單前與我們確認實際頻段需求。

---

## EM7455 vs MC7455：同一顆晶片，只差封裝

EM7455（M.2）與 MC7455（mPCIe）採用同一個 Qualcomm MDM9230 晶片組，核心電氣規格相同。主要差別是**封裝介面**：

| 項目 | EM7455 | MC7455 |
|---|---|---|
| **封裝** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **尺寸** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **適合裝置** | 筆電 WWAN 槽、現代 M.2 主機板 | 舊款工業路由器 mPCIe 插槽 |
| **通用 VID:PID** | `1199:9079` | `1199:9071` |

**選哪個純看你的設備插槽**。若主板只有 M.2，選 EM7455；若只有 mPCIe，選 MC7455。若選錯封裝，可透過轉接板（M.2→mPCIe 或 mPCIe→M.2）解決。

---

## Linux 設定（Ubuntu / Debian / Linux Mint）

EM7455 在主流 Linux 發行版上驅動支援度較高，以下為社群常見的基本設定步驟，實際環境（發行版版本、kernel 版本、韌體版本）可能造成細節差異，建議先在測試環境驗證過再導入正式系統。

### 步驟 1：硬體偵測

```bash
lsusb | grep -i sierra
# 預期輸出類似：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 步驟 2：安裝工具套件

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 步驟 3：切換 USB 組合模式為 QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# 驗證組合模式
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 預期結果類似：USB composition 6: DM, NMEA, AT, QMI
```

> 若只要 MBIM 模式（部分運營商要求），可查詢 `AT!USBCOMP` 相關設定並改用 `mbimcli`，實際數值請以官方 AT 指令參考文件為準。

### 步驟 4：FCC Auth 解鎖

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# 若使用 ModemManager 內建自動化：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 步驟 5：NetworkManager 連線

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn '你的APN'
sudo nmcli connection up 'EM7455 LTE'
```

### 步驟 6：手動 QMI 連線（進階/排錯）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='你的APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## OpenWrt QMI 設定

EM7455 在 OpenWrt 上是社群回報相容性較佳的型號之一，以下是 QMI 模式的基本設定範例。

### 安裝套件

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### 編輯網路設定檔

編輯 `/etc/config/network`，新增以下介面設定：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### 重啟網路

```bash
/etc/init.d/network restart
```

若用 LUCI Web 介面：網路 → 介面 → 新增新介面 → 協定選「QMI」，裝置選 `/dev/cdc-wdm0`，填入 APN 即可。

> ROOter（基於 OpenWrt 的蜂窩路由韌體）對 Sierra QMI 模組有社群回報的支援案例，內建 `create_connect.sh` 相關掛鉤，若你是樹莓派玩家，可評估直接使用 ROOter 韌體，惟正式支援範圍建議以 ROOter 官方公告為準。

---

## 品牌機相容性：Dell / Lenovo 筆電

### Dell 筆電（DW5811e 對應 EM7455 平台）

Dell DW5811e 是 Dell 品牌版的 EM7455（VID `413c`、PID `81b6`），核心晶片同為 Qualcomm MDM9230。多數主流 Linux 發行版的 `qmi_wwan` 驅動已收錄常見品牌版 ID，實際是否需要額外設定，建議先實測確認：

```bash
lsusb | grep 413c
# 預期類似：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Dell 多數機種（Latitude、Precision、XPS）過往社群回報不設 BIOS 白名單，DW5811e 多可直接安裝使用，但實際情況可能因機型與 BIOS 版本而異，建議以你手上的實際機型為準。

### Lenovo 筆電（EM7455 FRU）

Lenovo ThinkPad 有 BIOS 白名單限制的相關社群回報——部分機型只認 Lenovo FRU 版本的模組。以下是社群討論中曾出現、用於嘗試繞過此限制的 AT 指令範例：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **這組指令我們尚未逐一核對原始出處與正確性，且屬於改動模組底層韌體行為的操作，執行錯誤有導致模組無法使用（俗稱「變磚」）的風險**。這是整理自公開社群討論的範例，並非 Yupitek 已驗證過的標準流程。若你要嘗試，強烈建議：先確認並備份目前韌體版本、僅在非關鍵測試環境操作、且自行承擔操作風險。若不確定，建議直接與我們聯繫討論你的實際需求與可行方案。

### ThinkPad 機型（社群回報曾用於此類設定的機型）

以下清單整理自社群討論，實際是否適用及是否需要 BIOS/韌體更新，請以你手上機型的官方規格與 BIOS 版本為準，我們建議下手前先與我們或 Lenovo 官方管道確認：

- 60 系列：T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- 70 系列：T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## 平台相容性總覽

| 平台 | 支援度 | 連線方式 | 備註 |
|---|---|---|---|
| 樹莓派 + OpenWrt | ✅✅ 社群案例較多 | QMI / MBIM | 需 M.2→USB 轉接板 |
| 樹莓派 + ROOter | ✅✅ | QMI（社群回報內建掛鉤） | 建議樹莓派玩家優先評估 |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | 主流發行版驅動支援度較高 |
| DD-WRT | ⚠️ 支援度較弱 | QMI / PPP | 需求較新 BETA build，社群案例有限 |
| pfSense / FreeBSD | ⚠️ 支援度較弱 | QMI / PPP（多走 AT command） | FreeBSD 原生蜂窩驅動有限，需個案評估 |
| Dell 筆電（DW5811e） | ✅ | QMI / MBIM | 多數主流發行版可辨識，個別機型建議實測 |
| Lenovo 筆電 | ⚠️ 需額外設定 | QMI | 部分機型有 BIOS 白名單限制，處理方式風險較高，見上方說明 |

---

## 社群資源與延伸閱讀

以下是與 EM7455 相關、公開可查的社群與官方資源，供進一步研究參考：

- **danielewood/sierra-wireless-modems**：EM7455/MC7455 相關設定腳本與社群討論：[GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)**：Linux 設定相關社群整理（含 kernel 選項、韌體更新、疑難排解）：[Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE 維基**：官方 LTE 數據機支援列表與設定：[OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen**：工程模式相關工具，可能涉及 PRI 與頻段設定：[GitHub](https://github.com/bkerler/SierraWirelessGen)

> 以上第三方資源連結內容非我們維護，實際使用前請自行評估其正確性與時效性。

---

## 常見問題 FAQ

**Q1：EM7455 支援 5G 嗎？**
不支援。EM7455 是 LTE-A Cat 6 模組，最高 300 Mbps。若需 5G（Sub-6 或 mmWave），可參考 EM9190（Sub-6）或 EM9191（Sub-6 + mmWave）。

**Q2：EM7455 在台灣可以用嗎？**
一般而言可以搭配台灣主流電信商 SIM 卡使用，實際訊號表現與可用頻段依基地台位置、電信商網路規劃與載波聚合支援而定，建議下單前與我們確認你所在地區與電信商的相容性。

**Q3：EM7455 跟 MC7455 差在哪？**
核心晶片相同，皆為 Qualcomm MDM9230，規格一致。唯一差別是封裝：EM7455 為 M.2，MC7455 為 mPCIe。選哪顆純看你的插槽。

**Q4：EM7455 在 Ubuntu 上抓不到怎麼辦？**
先確認 `lsusb` 是否看到 `1199:9079`，若沒有可嘗試改用 USB 2.0 埠（部分案例中 USB 3.0 可能造成干擾）。接著確認 `qcserial` 與 `qmi_wwan` 已載入：執行 `lsmod | grep qmi`。也可嘗試停用 ModemManager（`systemctl stop ModemManager`）再手動執行 `qmicli` 排查。若仍無法解決，建議與我們聯繫協助排查。

**Q5：Dell DW5811e 就是 EM7455 嗎？**
是的，DW5811e 是 Dell 品牌版的 EM7455，核心為同一顆 Qualcomm MDM9230 晶片。Dell 版本在二手市場流通量較大、取得成本相對較低，且多數 Dell 筆電社群回報不鎖 BIOS 白名單，但實際情況建議以你的機型為準。

---

## 聯絡採購

以上 EM7455 規格與設定資訊由榆閤科技（Yupitek）整理提供。若需採購 EM7455、EM7430、MC7455 或 Sierra Wireless 全系列蜂窩模組，請至產品頁查詢報價或聯絡技術團隊。

- **產品頁**：[https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **全系列產品**：[https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **Email**：sales@yupitek.com
