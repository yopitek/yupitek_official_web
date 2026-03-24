---
title: "AWUS036AXML 監控模式韌體修復：解決主動模式當機問題"
description: "如何修復 AWUS036AXML 在 Kali Linux 上的監控模式韌體當機問題。涵蓋 MT7921AU 韌體更新、核心版本需求、主動與被動模式的解決方案，以及 hcxdumptool 替代方案。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AU", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
---

**ALFA AWUS036AXML** 是 ALFA Network 的旗艦 WiFi 6E 網卡，搭載 MediaTek MT7921AU 晶片組，支援三頻（2.4 / 5 / 6 GHz），是 2026 年少數能在 6 GHz 頻段進行被動監聽的 USB 網卡之一。在站點勘查、封包擷取、PMKID 收集等使用情境下，它的表現相當出色。

但有一個已知問題會讓使用者措手不及：**主動監控模式指令會導致韌體當機**。執行 `aireplay-ng` 或 `mdk4` 等工具後，`wlan0mon` 介面會完全消失，必須拔插網卡才能恢復。這不是硬體缺陷，而是目前 Linux `mt7921u` 驅動程式與韌體的限制。

本指南說明根本原因，提供完整的診斷步驟，以及具體的修復與暫時解決方案，讓您不必中斷工作。

---

## 問題說明：主動監控模式當機

### 症狀

啟用監控模式並執行主動指令（如 `aireplay-ng --test wlan0mon` 或任何取消驗證/注入操作）後，`wlan0mon` 介面從 `ip link` 和 `iwconfig` 輸出中消失。網卡變得無回應，必須實體拔除並重新插入才能恢復。部分情況下，`dmesg` 會在當機後立即顯示韌體錯誤或重置事件。

被動操作（使用 `airodump-ng` 掃描、擷取原始封包）在觸發主動注入前後均可正常運作。

### 根本原因

**MT7921AU 晶片組**採用韌體式 MAC 架構。Linux 核心的 `mt7921u` 驅動程式依賴晶片組內嵌韌體來處理某些底層操作，包括監控模式下的封包注入。目前的韌體與驅動程式組合未完整實作 Linux 主動注入監控模式所需的指令路徑。

相較之下，**被動監聽**（嗅探空中已有的封包）不需要韌體傳送任何內容，不會觸發當機。問題僅限於傳送路徑操作：取消驗證封包、探測請求、關聯洪水等主動操作。

{{< alert "triangle-exclamation" >}}
**已知韌體當機錯誤。** 這是 2026 年初 Linux `mt7921u` 驅動程式中已確認的問題，影響 AWUS036AXML 及其他 MT7921AU 的 USB 網卡。未來的核心或韌體更新可能會修復此問題——請查閱[驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)以獲取最新狀態。
{{< /alert >}}

---

## 診斷：確認是否為此問題

按以下步驟確認您遇到的是 MT7921AU 主動模式當機，而非其他問題：

```bash
# 確認網卡已識別
lsusb | grep -i mediatek

# 確認驅動程式已載入
lsmod | grep mt7921u

# 確認核心版本（必須 >= 5.18）
uname -r

# 啟動監控模式
sudo airmon-ng start wlan0

# 測試被動擷取（應正常運作）
sudo airodump-ng wlan0mon

# 測試主動注入（可能當機）
sudo aireplay-ng --test wlan0mon
```

若 `aireplay-ng --test` 後網卡從 `ip link` 消失，即確認遇到韌體當機錯誤。

透過核心日誌進行額外驗證：

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

注意是否有 `mt7921u: firmware crash`、`mt7921u: chip reset` 或 `usb disconnect` 等訊息緊接在 aireplay-ng 指令後出現，這些均確認是韌體層面的失敗。

{{< alert "circle-info" >}}
**被動擷取不受影響。** 若 `airodump-ng` 正常但 `aireplay-ng` 導致當機，這正是已知的 MT7921AU 錯誤。請繼續查看以下修復方案。
{{< /alert >}}

---

## 修復方案一：更新韌體套件

最有效的第一步是確保您擁有最新的 MT7921 韌體檔案。較舊的韌體版本更容易發生當機；更新的韌體可改善部分主動操作的穩定性。

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# 或從 linux-firmware 倉庫手動安裝最新 mt7921 韌體
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

更新韌體檔案後，重新載入驅動程式並再次測試主動模式：

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

---

## 修復方案二：使用最新核心

`mt7921u` 驅動程式在上游 Linux 核心中持續維護。自 5.18 版本以來，驅動程式的穩定性修補、韌體指令處理和監控模式改善已納入核心更新。執行較新的核心是改善行為最可靠的方式之一。

確認目前核心版本：

```bash
uname -r
```

在 Kali Linux 上更新至最新可用核心：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

目標：**核心 6.1 LTS 或更新版本**，以獲得最完整的 `mt7921u` 驅動程式修補。核心 6.6 及更新版本包含 MediaTek USB 驅動程式堆疊的額外改善，使用者回報有正面效果。

{{< alert "circle-info" >}}
**核心 6.6+ 改善。** 多份社群回報指出，使用核心 6.6 搭配更新韌體可減少（但不一定完全消除）MT7921AU 的主動模式當機。升級後請重新執行診斷步驟，評估您的特定組合。
{{< /alert >}}

---

## 暫時解決方案：使用 hcxdumptool（被動 PMKID 擷取）

若韌體修復無法完全解決當機問題，`hcxdumptool` 提供一個完全不需要封包注入的高效替代工作流程。

`hcxdumptool` 以**被動模式**運作——直接從存取點廣播的信標和探測封包中擷取 PMKID 值。不傳送取消驗證封包、不進行注入、不觸發韌體當機。AWUS036AXML 能完美處理此工作流程。

```bash
sudo apt install hcxdumptool hcxtools

# 被動擷取——無需取消驗證，無韌體當機風險
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# 轉換為 hashcat 格式
hcxpcapngtool -o hash.hc22000 capture.pcapng

# 使用 hashcat 破解
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

此工作流程從信標封包中擷取 PMKID，完全不傳送任何內容——從無線介質的角度來看是完全被動的。

{{< alert "circle-info" >}}
**PMKID 擷取適用於所有現代 WPA2/WPA3 網路。** 存取點無論是否有用戶端關聯，都會在信標封包中廣播 PMKID。您只需在 AP 的範圍內，不需要用戶端在場，非常適合無法使用取消驗證的情境。
{{< /alert >}}

---

## 暫時解決方案：使用 AWUS036ACH 進行主動注入

對於確實需要主動封包注入的任務（強制 WPA 握手擷取、WPS 列舉等），**AWUS036ACH**（RTL8812AU 晶片組）是在 Kali Linux 上擁有成熟、經過充分測試驅動程式支援的首選解決方案。

推薦的雙網卡專業設定：

- **AWUS036AXML** → 5 GHz / 6 GHz 被動掃描與擷取
- **AWUS036ACH** → 2.4 GHz / 5 GHz 主動注入

這個組合讓您完整覆蓋所有頻段，注入由 RTL8812AU 負責（其 Linux 主動模式支援已穩定多年），AWUS036AXML 負責 6 GHz 探索和高品質被動擷取。

請參閱 [AWUS036AXML 評測](/zh-tw/blog/awus036axml-wifi-6e-review/)和[封包注入指南](/zh-tw/blog/packet-injection-guide/)以了解兩個網卡的設定詳情。

---

## 主動模式可正常運作的情境

在某些條件下，MT7921AU 的主動模式已有穩定或接近穩定的使用者回報：

- **核心 6.6 或更新版本**搭配 firmware-misc-nonfree 20240610 或更新版本
- 避免以爆發模式使用 `aireplay-ng --deauth`（高封包率取消驗證洪水比單一封包操作更容易觸發當機）
- 使用 `--deauth 1` 或 `--deauth 3`，而非持續的取消驗證串流
- 確保網卡連接至 USB 3.0 連接埠（USB 2.0 頻寬限制會增加韌體指令管線的壓力）
- 在 2.4 GHz 而非 5 GHz 進行注入操作（部分驅動程式版本中低頻段似乎更穩定）

{{< alert "triangle-exclamation" >}}
**在實際評估前請先測試。** 即使主動模式看似正常，MT7921AU 韌體仍可能在高負載下於操作途中當機。使用 AWUS036AXML 進行主動操作時，請務必備有恢復計畫（備用網卡或純被動工作流程）。
{{< /alert >}}

---

## 確認韌體是否已更新

```bash
# 確認目前韌體檔案日期
ls -la /lib/firmware/mediatek/mt7921*

# 確認驅動程式版本
modinfo mt7921u | grep -E "version|filename"

# 確認核心訊息中的韌體載入狀態
sudo dmesg | grep mt7921
```

韌體成功載入時，`dmesg` 輸出應顯示類似以下內容：

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

---

## 摘要：AWUS036AXML 最佳使用情境

- ✅ **被動 WiFi 6E 掃描與 PCAP 擷取** — 表現完美
- ✅ **hcxdumptool PMKID 擷取** — 無需注入，無韌體當機風險
- ✅ **6 GHz 網路探索** — airodump-ng 被動掃描 6 GHz 頻段
- ✅ **WiFi 6E 站點勘查與干擾分析** — 三頻被動監聽
- ✅ **基線 WPA2 握手擷取** — 從現有流量被動擷取握手封包
- ⚠️ **主動封包注入** — 韌體成熟前請改用 AWUS036ACH
- ⚠️ **取消驗證洪水** — 有當機風險；在核心 6.6+ 上謹慎測試
- ⭐ **最佳工作流程：同時攜帶 AWUS036AXML + AWUS036ACH**，實現全頻段全功能覆蓋

---

## 相關指南

- [AWUS036AXML 完整評測](/zh-tw/blog/awus036axml-wifi-6e-review/)
- [封包注入指南](/zh-tw/blog/packet-injection-guide/)
- [驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)
