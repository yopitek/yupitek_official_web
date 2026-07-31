---
title: "Sierra EM7455 完整評測：為什麼它是 Maker 與實驗室做專題最愛的 Sierra 網卡"
description: "EM7455 完整評測：規格、EM7430 差異、OpenWrt/Linux 設定、Dell/Lenovo 相容性。本文由 Yupitek（榆閤科技）整理提供技術資料。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "EM7455 支援 5G 嗎？"
    answer: "不支援。它是一張 LTE-A Cat 6 的模組，速度最快是 300 Mbps。如果需要 5G，要改看 EM9190 或是 EM9191。"
  - question: "EM7455 在台灣可以用嗎？"
    answer: "可以搭配台灣主流電信商使用，但實際訊號與支援頻段依基地台位置而定，建議下單前先確認你所在地區與電信商的相容性。"
  - question: "EM7455 跟 MC7455 差在哪？"
    answer: "核心都是 Qualcomm MDM9230 晶片，規格完全一致。唯一差別是外觀封裝：EM7455 為 M.2，MC7455 為 mPCIe。選哪張純看你的插槽。"
  - question: "EM7455 跟 EM7430 差在哪？"
    answer: "同一顆 MDM9230 晶片，核心規格一樣。主要差異在打的頻段不同：EM7455 涵蓋美洲與 EMEA 頻段，EM7430 涵蓋亞太頻段。"
  - question: "Dell DW5811e 就是 EM7455 嗎？"
    answer: "是的，DW5811e 是 Dell 貼牌版的 EM7455，核心為同一顆 Qualcomm MDM9230。"
---

# Sierra EM7455 完整評測：為什麼它是 Maker 與實驗室做專題最愛的 Sierra 網卡

如果有在玩樹莓派加上 OpenWrt，或者想幫實驗室的設備升級 4G 網路，那你一定聽過 Sierra EM7455 這張神卡！它是 Sierra Wireless 推出的一款 LTE-A Cat 6 M.2 蜂窩模組，搭載了 Qualcomm MDM9230 晶片，最高支援 300 Mbps 的下載以及 50 Mbps 的上傳速度，而且還內建了 GNSS 定位功能，工作溫度甚至能扛住 -40°C 到 +85°C 的極端環境。

這篇文章由榆閤科技（Yupitek）整理，帶大家看懂這張 M.2 B-Key 封裝的 4G LTE-Advanced Cat 6 模組為什麼這麼紅，以及怎麼在 Linux 系統下把驅動跟設定搞定。

> 產品連結：[EM7455 — Yupitek 產品頁](/zh-tw/products/sierra/em7455/) | 官方規格書：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完整規格表：硬核數據一次看

下面的數字都是從 Sierra Wireless 官方規格書整理出來的。老話一句，如果真的要下單做專案，建議先跟我們索取最新版的官方文件核對一下，尤其是頻段或是韌體版本這類可能會更新的項目。

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
| **Linux 驅動** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主流發行版基本上都內建了） |
| **通用韌體** | 請以官方 source.sierrawireless.com 最新版本為準 |
| **運營商認證** | 依地區時有變動（例如 AT&T、Verizon、Vodafone 等），請洽詢確認最新清單 |

---

## EM7455 適合拿來做什麼專案？

**簡單來說，EM7455 絕對是以下三種應用的救星：（1）自己用開源系統架 4G LTE 路由器（像是 OpenWrt 或 ROOter）、（2）幫 Dell 或 Lenovo 筆電升級 WWAN 上網卡、（3）工控實驗室做的物聯網閘道器或車聯網追蹤。**

它最大的優勢就在於 Linux 驅動太成熟了，社群網路上一堆教學資源，而且支援的頻段也很廣。

### 如果你是 Maker 或學生在做專題

| 應用 | 怎麼搭配 | 為什麼選它 |
|---|---|---|
| 樹莓派 4G 路由器 | 樹莓派 4/5 + M.2轉USB板 + OpenWrt / ROOter | 在 OpenWrt 社群裡相容性超穩，uqmi 套件也很好用 |
| GL.iNet 路由器升級 | GL-MT1300 / GL-AR750S + USB 轉接 | 網路上找得到 ROOter 的 `create_connect.sh` 設定討論可以抄作業 |
| 戶外可攜式 LTE 熱點 | 電池供電 + USB 轉接 + 小型路由器 | 發熱低散熱好，帶去戶外做物件追蹤很適合 |

### 如果是企業專案或工業應用

| 應用 | 怎麼搭配 | 為什麼選它 |
|---|---|---|
| 工業路由器 | 帶有 M.2 插槽的工業閘道器（如 Advantech） | 耐操，-40~85°C 的寬溫規格很安心，頻段也夠多 |
| 車聯網 telematics | 車載閘道器 + GNSS 天線 | 有內建 GPS/GLONASS 等定位功能，連網加定位一張卡搞定 |
| 筆電 WWAN 升級 | Dell Latitude / Lenovo ThinkPad 系列 | M.2 B-Key 直接插上去，Linux 隨插即用機率很高 |
| 備援 WAN | OpenWrt / pfSense 雙 WAN 備援 | 支援 QMI/MBIM 雙模式（不過 pfSense 支援度比較玄學，建議用 OpenWrt） |

---

## EM7455 跟 EM7430 到底差在哪？

大家很常問這個問題。其實 **EM7455 跟 EM7430 根本是用同一顆 Qualcomm MDM9230 晶片，所以核心規格（像是 Cat 6、300/50 Mbps、2×CA、GNSS）一模一樣。它們最大的差別在於「打的市場頻段不同」**。EM7455 主要是給美洲跟歐洲/中東/非洲（EMEA）用的，而 EM7430 主要是給亞太（APAC）地區用的。

| 項目 | EM7455 | EM7430 |
|---|---|---|
| **晶片組** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **蜂窩標準** | LTE-A Cat 6 | LTE-A Cat 6 |
| **下載峰值** | 300 Mbps | 300 Mbps |
| **上傳峰值** | 50 Mbps | 50 Mbps |
| **載波聚合** | 2×CA | 2×CA |
| **封裝** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **目標區域** | 美洲、EMEA | 亞太（APAC） |

**選型小建議**：如果你專題或設備的 SIM 卡是以北美或歐洲為主，選 **EM7455**；如果是在亞太區（像台灣、日本、澳洲），理論上 **EM7430** 比較對口。不過因為台灣電信業者的頻段配置比較特別，下單前最好先找我們確認一下你的電信商配哪一張比較順。

---

## EM7455 vs MC7455：完全一樣的晶片，只差腳位形狀

剛剛講過，EM7455（M.2）和 MC7455（mPCIe）都是用同一顆 Qualcomm MDM9230，電氣規格也是完全一樣的。唯一的差別就是那層「皮」（封裝）：

| 項目 | EM7455 | MC7455 |
|---|---|---|
| **封裝** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **尺寸** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **適合裝置** | 筆電 WWAN 槽、現代開發板 | 比較舊的工控機 mPCIe 插槽 |
| **通用 VID:PID** | `1199:9079` | `1199:9071` |

**這題很簡單，看你的設備插槽長怎樣就選哪張。** 萬一選錯了，其實也能買轉接板（M.2 轉 mPCIe 或反過來）來補救。

---

## 在 Linux 下怎麼設定？（Ubuntu / Debian / Linux Mint 適用）

EM7455 在常見的 Linux 系統上支援度非常好，下面分享社群常用的基礎設定步驟。不過記得，每台機器的作業系統版本或 kernel 都不太一樣，建議先在測試機上玩過一次，不要直接上生產環境。

### 步驟 1：檢查有沒有抓到硬體

```bash
lsusb | grep -i sierra
# 應該會看到類似這個輸出：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 步驟 2：把該裝的工具裝一裝

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 步驟 3：把 USB 模式切換成 QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# 檢查一下模式切換成功沒
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 應該會看到：USB composition 6: DM, NMEA, AT, QMI
```

> 如果有些特定的運營商要求走 MBIM 模式，你可以去查 `AT!USBCOMP` 這個指令然後改用 `mbimcli` 來連線。

### 步驟 4：解鎖 FCC Auth

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# 如果你是用 ModemManager 想要全自動的話：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 步驟 5：用 NetworkManager 連上線

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn '你的APN'
sudo nmcli connection up 'EM7455 LTE'
```

### 步驟 6：手動 QMI 連線（如果你想進階排錯的話）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='你的APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## 如果你玩 OpenWrt，可以這樣設定 QMI

EM7455 在 OpenWrt 社群裡的評價滿高的，如果你有台分享器刷了 OpenWrt，可以參考下面的 QMI 設定方式。

### 安裝必要套件

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### 編輯網路設定檔

打開 `/etc/config/network`，加上這段介面設定：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### 把網路重新啟動

```bash
/etc/init.d/network restart
```

如果你比較喜歡點滑鼠（LUCI Web 介面）：到「網路」→「介面」→ 新增新介面，協定選「QMI」，裝置選 `/dev/cdc-wdm0`，把你的 APN 填進去就搞定了。

> 小撇步：如果你是玩樹莓派的同學，強烈建議可以試試看 ROOter（一個基於 OpenWrt 專門搞 4G/5G 路由的韌體），裡面內建了很多方便的設定掛鉤。

---

## 品牌筆電相容性大哉問：Dell 與 Lenovo

### Dell 筆電（有張卡叫 DW5811e 就是它）

在網路上常常看到 Dell DW5811e，其實它就是 Dell 貼牌版的 EM7455（VID 變成了 `413c`、PID 變成了 `81b6`），裡面的晶片一模一樣是 MDM9230。大部分的 Linux `qmi_wwan` 驅動早就認得它了。

```bash
lsusb | grep 413c
# 應該會看到類似：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

好消息是，Dell 大部分的筆電（像 Latitude, Precision 等等）據社群討論，通常沒有鎖討厭的 BIOS 白名單，所以常常可以直接插上去用。

### Lenovo 筆電（麻煩的白名單）

如果你是用 Lenovo ThinkPad，就要小心了。這家有時候會在 BIOS 裡設白名單，只准你用 Lenovo 原廠 FRU 版本的卡。論壇上有些大神分享了繞過限制的 AT 指令，給有挑戰精神的同學參考：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **警告：這些指令是從論壇爬下來的，如果執行不當可能會把網卡變成磚頭喔！** 如果你不是那種喜歡拆裝硬體、承擔風險的進階玩家，建議下單前先問問我們有沒有比較安全的替代方案。

---

## 到底支援哪些平台？一張表看懂

| 你的平台 | 支援度 | 連線方式 | 備註 |
|---|---|---|---|
| 樹莓派 + OpenWrt | ✅✅ 超穩，教學多 | QMI / MBIM | 要自己買一張 M.2 轉 USB 的小板子 |
| 樹莓派 + ROOter | ✅✅ | QMI | 強烈推薦給樹莓派玩家 |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | 隨插即用機率非常高 |
| DD-WRT | ⚠️ 要看運氣 | QMI / PPP | 網路上沒什麼人討論，不建議新手碰 |
| pfSense | ⚠️ 很玄學 | QMI / PPP | 建議評估改用 OpenWrt 比較不折騰 |
| Dell 筆電 | ✅ | QMI / MBIM | 基本上 Linux 都抓得到 |
| Lenovo 筆電 | ⚠️ 可能要破解 | QMI | 小心 BIOS 白名單，亂刷指令有變磚風險 |

---

## 哪裡找更多資源？

做專題如果卡關，可以去這幾個開源社群挖寶：

- **danielewood 的 GitHub**：有 EM7455/MC7455 很完整的腳本跟討論區。
- **Gentoo Wiki**：Linux 大神們在那邊整理了很詳盡的疑難排解。
- **OpenWrt LTE Wiki**：官方的文件，設定網路前必看。

## 常見問題快速 Q&A

{{< faq >}}

---

## 實驗室想採購？找我們就對了

這篇文章是由榆閤科技（Yupitek）的工程團隊整理出來的。不管是做大學專題、實驗室計畫，還是企業需要大量採購 EM7455 或其他 Sierra 模組，都可以來找我們討論！

- **逛逛這張卡**：[https://yupitek.com/zh-tw/products/sierra/em7455/](/zh-tw/products/sierra/em7455/)
- **看所有 Sierra 型號**：[https://yupitek.com/zh-tw/products/sierra/](/zh-tw/products/sierra/)
- **寄信問我們**：sales@yupitek.com
