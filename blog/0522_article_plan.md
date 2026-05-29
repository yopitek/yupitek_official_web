# ALFA Network 網路卡 Soft AP / WiFi Hotspot 功能深度調查報告

**調查日期：** 2026年5月  
**調查目的：** 評估 Yupitek 銷售之 ALFA Network USB 無線網路卡在 Kali Linux、Ubuntu、Debian、Raspberry Pi 4/5 等平台上的 Soft AP（hostapd/WiFi Hotspot）功能支援狀況  
**資料來源：** GitHub (morrownr/USB-WiFi)、Reddit、Raspberry Pi 官方論壇、技術部落格、Rokland、Lab401、Yupitek 現有文章

---

## 一、什麼是 Soft AP / WiFi Hotspot？

Soft AP（Software Access Point，軟體存取點）是指在不使用專用 AP 硬體的情況下，透過軟體（主要是 **hostapd**）將 USB 無線網路卡設定為無線基地台（Access Point），讓其他裝置可以連接並上網。

在 Linux 環境中，這整套功能依賴：
- **nl80211 驅動框架**（Linux 無線子系統標準）
- **hostapd**（建立 AP 的主程式）
- **dnsmasq**（DHCP 派發 IP 給連線客戶端）
- **iptables / nftables**（NAT 路由）

關鍵的驅動層支援稱為 **Master Mode**（AP Mode / Infrastructure Mode）。若晶片驅動不支援此模式，hostapd 無法運作，即無法建立 Soft AP。

---

## 二、Yupitek 銷售的 ALFA 產品線與晶片一覽

| 型號 | 晶片組 | 驅動類型 | WiFi 標準 |
|------|--------|----------|-----------|
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel（需手動安裝；kernel 6.14+ 納入 in-kernel） | WiFi 5 AC1200 雙頻 |
| AWUS036ACM | MediaTek MT7612U | **In-kernel**（kernel 4.19 起） | WiFi 5 AC1200 雙頻 |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel（kernel 5.18 起） | WiFi 6E AX3000 三頻 |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel（kernel 5.18 起） | WiFi 6E AX3000 三頻 |
| AWUS036AX | Realtek RTL8832BU | Out-of-kernel（kernel 6.12+ 強烈建議） | WiFi 6 AX1800 雙頻 |
| AWUS036AXER | Realtek RTL8832BU | Out-of-kernel（同上） | WiFi 6 AX1800 雙頻 |

> **注意：** AWUS036ACHM（MT7610U）已停產（discontinued），Yupitek 產品頁面不再列出。本報告以現售產品為主。

---

## 三、各型號 Soft AP 支援詳細分析

---

### 3.1 AWUS036ACM（MT7612U）— ⭐ Soft AP 首選

**晶片：** MediaTek MT7612U  
**驅動：** `mt76x2u`，Linux kernel 4.19 起內建，零編譯、即插即用

#### Soft AP 支援狀態：✅ 完整支援

此款是 ALFA 現售產品中 **Soft AP 支援最完整、最穩定** 的選擇。

**主要優勢：**
- **WPA2 / WPA3** 雙重支援（MediaTek in-kernel 驅動原生支援 WPA3）
- **VIF（虛擬介面）支援**：可同時運行 AP 模式 + Managed 模式 + Monitor 模式於同一張網卡，無需額外設備
- **低耗電**：最大電流需求約 400mA，適合 Raspberry Pi（Pi 4 USB 子系統僅有 1200mA 總量）
- **跨平台穩定性**：在 Kali Linux、Ubuntu、Debian、Raspberry Pi OS 均有大量成功案例

**已知的 hostapd.conf 正確設定（MT7612U）：**
```
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
```

> ⚠️ 常見錯誤：初始設定時若 `ht_capab` 包含不符合 MT7612U 能力的旗標，hostapd 會崩潰。移除不支援的 capability 旗標即可解決。（來源：GitHub morrownr/USB-WiFi issue #2）

**Raspberry Pi 4/5 實測：**  
morrownr（GitHub 最具權威的 Linux USB WiFi 知識庫維護者）親身測試，AWUS036ACM 在 Raspberry Pi 4B 上用作主要 AP 設備，評價「outstanding」。Yupitek 部落格亦記錄此款在 RPi 3B+、4、5 全系列上的完整相容性。

**社群評價摘要（GitHub / Reddit / eBay 評論）：**
> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. In my opinion, it is an outstanding USB WiFi adapter." — morrownr
>
> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers." — eBay 用戶評論
>
> "The ACM is a little bit more versatile and easier to set up for AP mode." — GitHub issue #2 討論

---

### 3.2 AWUS036ACH（RTL8812AU）— Soft AP 可用，但需注意

**晶片：** Realtek RTL8812AU  
**驅動：** 長期依賴社群維護的 out-of-kernel driver（aircrack-ng/rtl8812au）；kernel 6.14 起已合併 in-kernel 支援（rtw88 框架）

#### Soft AP 支援狀態：⚠️ 有條件支援

**可以運作，但存在以下已知問題：**

1. **WPA3 不支援**：RTL8812AU 驅動雖宣稱支援 WPA3，但實際上無法正常運作，已被多名使用者確認。只能使用 WPA2。
2. **VIF 介面組合不支援**：無法同時跑 AP + Monitor 模式；Realtek 驅動不支援 `iw list` 所見的介面組合能力。
3. **驅動安裝複雜**：Kali Linux 2025.x 環境下，最新版 aircrack-ng/rtl8812au 驅動有已知相容問題，需回退至特定 commit（63cf0b4）方可正常運作。Kernel 6.14 後改用 in-kernel rtw88 驅動可能改善此問題。
4. **高耗電**：最大約 800mA，在 Raspberry Pi 上使用 USB 設備較多時可能觸發電力不足（brown out）問題。
5. **AP 功能本身可運作**：若單純建立 Soft AP（無需同時 monitor），配合正確的 hostapd 設定可以成功。

**已知的 hostapd.conf 設定（RTL8812AU）：**
```
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
```

**社群評價摘要：**
> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine." — GitHub issue #2
>
> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek." — morrownr 技術說明

**Raspberry Pi 建議：** 使用 USB 3.0 埠（Pi 4 才有），並確認電源供應充足（建議 5A 電源）。

---

### 3.3 AWUS036AXML / AWUS036AXM（MT7921AUN）— Soft AP 條件可用，有已知問題

**晶片：** MediaTek MT7921AUN  
**驅動：** `mt7921u`，kernel 5.18 起 in-kernel；AP 模式 kernel 5.19 起加入

#### Soft AP 支援狀態：⚠️ 部分支援，有已知韌體/驅動問題

這兩款是 WiFi 6E 三頻（2.4/5/6 GHz）產品，in-kernel 驅動已列出 AP 模式支援，但使用者反映較多問題。

**AP 模式正式支援的 kernel 版本：**
- `managed` 模式：kernel 5.18+
- **`AP` 模式：kernel 5.19+**
- `AP/VLAN`：kernel 5.19+
- `P2P-GO`（Wi-Fi Direct AP）：kernel 6.4+

**已知問題（2024–2025年社群反映）：**

1. **Bluetooth 衝突導致 WiFi 崩潰**：MT7921AUN 晶片同時整合 BT 5.2，在部分 kernel（6.6 以後至近期）存在 BT 子系統影響 WiFi 穩定性的問題。**解決方案：禁用 Bluetooth 驅動**
   ```bash
   echo "install btusb /bin/false" >> /etc/modprobe.d/local-dontload.conf
   ```
2. **韌體版本問題**：需安裝最新韌體（2024年11月版：`WM Firmware Version: ____010000, Build Time: 20241106151045`）才能穩定運作。
3. **AP 模式下 Tx Power 顯示異常**：`iw` 顯示僅 3 dBm，無法調整，但實際上晶片有內建放大器，此為 kernel 驅動的顯示問題而非硬體限制。
4. **部分 kernel 版本下 monitor mode 損壞**：截至 2025年12月，kernel 6.18 及部分較早版本的 mt7921u 驅動有 monitor mode 異常的問題。
5. **Raspberry Pi 5 上的 AP 模式**：GitHub issue #476 中有用戶成功在 RPi3B（ArchLinux ARM aarch64）上運作 AP 模式，但不是所有設定都能直接成功。

**成功的使用者案例：**
> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. Its the most stable mt7921 in my collection. I am running hostapd compiled from git though." — fhteagle，GitHub issue #476

**推薦 Kernel 版本（2025年底）：** kernel 6.6 LTS 或 6.12+

**韌體更新步驟（若系統韌體過舊）：**
```bash
# 從 kernel.org 下載最新 MediaTek 韌體
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek
sudo reboot
```

---

### 3.4 AWUS036AX / AWUS036AXER（RTL8832BU）— Soft AP 不建議，有重大限制

**晶片：** Realtek RTL8832BU  
**驅動：** Multi-state 裝置（內建 Windows 驅動），out-of-kernel；Linux kernel 6.2 起有 in-kernel 支援，但建議 kernel 6.12+

#### Soft AP 支援狀態：❌ 不推薦用於 Soft AP

**主要問題：**
1. **Multi-state 裝置**：內建 Windows 驅動，需要 USB mode switch 才能在 Linux 下正常運作，增加部署複雜度。
2. **Monitor Mode 有限制**：kernel 6.14 以下 monitor mode 支援不完整。
3. **Soft AP / hostapd 支援狀態**：社群文件（morrownr/USB-WiFi）將此晶片標記為「不建議用於 penetration testing」，AP 模式未被廣泛測試驗證。
4. **社群案例極少**：相較於 MT7612U 和 RTL8812AU，RTL8832BU 用於 Soft AP 的實際案例幾乎找不到。

> Yupitek 官方文章明確指出：「AWUS036AX / AWUS036AXER 的 RTL8832BU 晶片在 kernel 6.14 以下有有限的 monitor mode 支援，不建議用於 penetration testing，請改用 AWUS036ACH 或 AWUS036AXML。」

---

## 四、各平台相容性矩陣

### AWUS036ACM（MT7612U）
| 平台 | Soft AP | 備注 |
|------|---------|------|
| Kali Linux 2022.x ~ 2025.x | ✅ 完整支援 | Kernel 5.x / 6.x，in-kernel，即插即用 |
| Ubuntu 22.04 / 24.04 | ✅ 完整支援 | in-kernel，零設定 |
| Debian 11 / 12 | ✅ 完整支援 | in-kernel |
| Raspberry Pi 4（Raspberry Pi OS） | ✅ 完整支援 | 最低耗電，morrownr 親自驗證 |
| Raspberry Pi 5（Raspberry Pi OS） | ✅ 完整支援 | 與 Pi 4 相同驅動 |

### AWUS036ACH（RTL8812AU）
| 平台 | Soft AP | 備注 |
|------|---------|------|
| Kali Linux 2022.x ~ 2025.x | ⚠️ 有條件支援 | 需安裝外部驅動，舊 driver commit；kernel 6.14+ 改善 |
| Ubuntu 22.04 / 24.04 | ⚠️ 有條件支援 | 可能需手動安裝 rtw88 或社群驅動 |
| Debian 11 / 12 | ⚠️ 有條件支援 | 同上 |
| Raspberry Pi 4 | ⚠️ 需注意電源 | 可運作，高耗電，建議有源 USB Hub |
| Raspberry Pi 5 | ⚠️ 需注意電源 | 同上 |

### AWUS036AXML / AWUS036AXM（MT7921AUN）
| 平台 | Soft AP | 備注 |
|------|---------|------|
| Kali Linux 2022.x（kernel 5.18+） | ✅ 支援，需禁 BT | 需更新韌體，禁用 btusb |
| Kali Linux 2024.x / 2025.x | ⚠️ 不穩定 | kernel 6.11+ 有 BT/WiFi 衝突問題 |
| Ubuntu 24.04（kernel 6.8+） | ⚠️ 部分問題 | morrownr 2024年底報告有問題 |
| Ubuntu 25.04（kernel 6.14，GNOME） | ✅ 即插即用 | CachyOS kernel 6.15.2 亦確認正常 |
| Debian 12 | ⚠️ 視 kernel 版本 | 較舊 kernel 可能較穩定 |
| Raspberry Pi 4 | ⚠️ 有案例成功 | 需確認韌體版本 |
| Raspberry Pi 5 | ⚠️ 有案例成功 | 有使用者在 Pi 5 + Kali ARM 測試成功 |

### AWUS036AX / AWUS036AXER（RTL8832BU）
| 平台 | Soft AP | 備注 |
|------|---------|------|
| Kali Linux | ❌ 不建議 | Multi-state，mode switch 需求 |
| Ubuntu / Debian | ❌ 不建議 | 同上，Soft AP 實測案例極少 |
| Raspberry Pi 4/5 | ❌ 不建議 | 同上 |

---

## 五、Soft AP 技術機制深入說明

### 5.1 hostapd 工作原理

`hostapd` 是 Linux 下建立 AP 的標準工具，它透過 `nl80211` 介面向 kernel 的 WiFi 驅動發出指令，將網路卡切換到 **Master Mode**（AP 模式）。若驅動的 `iw list` 輸出中的 `Supported interface modes:` 包含 `AP`，則代表硬體層面支援 Soft AP。

可用以下指令確認支援狀況：
```bash
iw list | grep -A 10 "Supported interface modes"
```

### 5.2 VIF（Virtual Interface）對 Soft AP 的重要性

VIF 允許同一張網路卡同時以多種模式運作（例如同時作為 AP + 連線到上游路由器）。只有 MediaTek in-kernel 驅動（mt7612u、mt7610u、mt7921au）完整支援 VIF；Realtek 的 out-of-kernel 驅動基本上不支援此功能。

對 Soft AP 使用場景而言，若需要：
- **網路分享（NAT/路由）**：不一定需要 VIF，可以 eth0 接上游、wlan 跑 AP
- **無線橋接（雙無線介面）**：需要 VIF 或兩張網路卡
- **監控 + AP 同時運作（如 Rogue AP 研究）**：需要 VIF 支援

### 5.3 WPA3 支援

| 晶片 | WPA2 | WPA3 |
|------|------|------|
| MT7612U（ACM） | ✅ | ✅ |
| MT7921AUN（AXML/AXM） | ✅ | ✅ |
| RTL8812AU（ACH） | ✅ | ❌ |
| RTL8832BU（AX/AXER） | ✅ | 未確認 |

### 5.4 DFS（Dynamic Frequency Selection）5GHz 頻道

DFS 頻道（如 ch100–ch140）需要 kernel 層面的 DFS 支援。使用者回報 MT7610U / MT7612U 缺乏 DFS 支援，因此在 5GHz AP 模式時建議使用非 DFS 頻道（如 ch36、ch40、ch44、ch48）。RTL8812AU 有 DFS 支援的記錄，但實際效能依環境而異。

---

## 六、實際使用案例與社群反饋整理

### 案例 1：Raspberry Pi 4B + AWUS036ACM = 穩定 Soft AP
**來源：** morrownr GitHub 7612u repo  
**場景：** RPi4B 作為家用 5GHz AP，搭配內建 2.4GHz 提供雙頻服務  
**結果：** 長期穩定運作，作者長期以此作為主要測試 AP 設備  
**配置：** hostapd + dnsmasq + NAT

### 案例 2：RPi3B+ + AWUS036ACM AP 初始崩潰，調整 ht_capab 後成功
**來源：** GitHub morrownr/USB-WiFi issue #2  
**問題：** hostapd 崩潰，原因為 `ht_capab` 包含不支援的旗標  
**解決：** 移除多餘旗標（特別是 USB 2.0 限制下某些 HT40 設定），在 Kali 上成功啟動

### 案例 3：Pi PwnBox RogueAP 使用 AWUS036ACH 跑 Soft AP
**來源：** GitHub koutto/pi-pwnbox-rogueap  
**場景：** 紅隊測試，RPi3B+ 上同時使用兩張 Alfa 網卡，一張（RTL8812AU）負責 AP，另一張（RT3070）負責攻擊  
**結果：** RTL8812AU 跑 AP 模式成功  
**備注：** Kali out-of-box 支援，但 RTL8812AU 不支援 VIF，所以需要兩張卡分工

### 案例 4：AWUS036ACHM（MT7610U）在 Pi4 上達到全速 AP
**來源：** GitHub morrownr/USB-WiFi Discussion #31  
**場景：** 使用者希望在 Pi 4 上以 5GHz AC 全速（433 Mbps link rate）跑 AP  
**問題：** 初始配置只達 65 Mbps link speed  
**解決：** 加入正確的 `vht_oper_chwidth=1` 和 `vht_oper_centr_freq_seg0_idx` 設定後達到全速  
**備注：** 此型號已停產，但技術細節對 MT7612U（ACM）同樣有參考價值

### 案例 5：AWUS036AXML 在 RPi3B ArchLinux ARM 上跑 AP 穩定
**來源：** GitHub morrownr/USB-WiFi issue #476  
**評語：** 「It's the most stable mt7921 in my collection. I am running hostapd compiled from git though.」  
**備注：** 需從 git 編譯最新版 hostapd，說明系統 hostapd 版本可能對 AX 支援不完整

---

## 七、重要限制與注意事項

1. **Raspberry Pi 5 差異**：RPi5 使用新的 USB controller，部分 out-of-kernel 驅動在 RPi5 上可能有不同表現，建議以 in-kernel 驅動（MT7612U 的 ACM）為優先。

2. **Kali Linux 2025.x 已知問題（RTL8812AU）**：最新版 Kali 2025.x 的 RTL8812AU 驅動安裝方式有變，需使用較舊的 commit 或等待 kernel 6.14+ 的 in-kernel rtw88 驅動。

3. **MT7921AUN 的 Bluetooth 干擾問題（2024–2025）**：這是目前 AWUS036AXML/AXM 最主要的不穩定來源，預計隨 kernel 更新和韌體更新逐步解決。在 AP 用途上，禁用 btusb 是目前最可靠的工作繞過方案。

4. **電源管理**：Raspberry Pi 在 USB WiFi AP 用途下需要穩定電源。建議使用官方 Pi 5A 電源，或使用外部有源 USB Hub（特別是使用高耗電的 RTL8812AU 時）。

5. **5GHz 與 DFS**：若需要 5GHz Soft AP，應避開 DFS 頻道（100–144），使用 UNII-1 頻段（36–48）最為安全，幾乎所有晶片都支援。

---

## 八、產品選購建議（針對 Soft AP 用途）

### 優先推薦
**AWUS036ACM（MT7612U）**  
最佳選擇。in-kernel 驅動、WPA3、VIF、低耗電，Kali/Ubuntu/Debian/RPi 4/5 全平台穩定。無需手動安裝驅動，零配置即可。

### 次要推薦
**AWUS036ACH（RTL8812AU）**  
可用，但需接受：需安裝驅動、不支援 WPA3、不支援 VIF、耗電較高。若已有此款，可正常用於 Soft AP；若尚未購買且主要目的是 Soft AP，建議選 ACM。

### 謹慎選擇
**AWUS036AXML / AWUS036AXM（MT7921AUN）**  
AP 功能有，但目前有 BT/WiFi 干擾問題需手動處理。若需要 WiFi 6E 的 6GHz 掃描能力，且願意接受偶爾需要調整設定，可以選擇。對於穩定度要求高的生產環境 Soft AP，不建議。

### 不建議
**AWUS036AX / AWUS036AXER（RTL8832BU）**  
Soft AP 用途缺乏社群驗證，multi-state 裝置帶來額外複雜度，不建議用於此用途。

---

## 九、部落格文章建議結構

根據以上調查，建議在 Yupitek 部落格（https://yupitek.com/zh-tw/blog/）發表的文章架構如下：

**標題：** 「ALFA 網路卡 Soft AP 完整指南：在 Kali Linux、Ubuntu、Debian 與 Raspberry Pi 4/5 上建立 WiFi 熱點」

**段落順序：**
1. 什麼是 Soft AP 及常見應用場景（家用/旅行路由器、滲透測試練習環境、IoT 中繼等）
2. 晶片與驅動選擇的關鍵（為何 MediaTek in-kernel 驅動更適合）
3. AWUS036ACM 完整設定教學（hostapd + dnsmasq，含完整設定檔）
4. AWUS036ACH 設定說明（含 WPA3 限制說明）
5. AWUS036AXML/AXM 的 AP 設定（含 BT 問題解決步驟）
6. 各平台相容性表格
7. 常見疑難排解

---

## 十、資料來源

1. **morrownr/USB-WiFi**（GitHub）— Linux USB WiFi 最權威社群知識庫，包含 iw_list、hostapd 設定樣板及各型號詳細說明  
   https://github.com/morrownr/USB-WiFi

2. **morrownr/7612u**（GitHub）— MT7612U 晶片專屬文件，含 Bridged AP on RPi4B 完整教學  
   https://github.com/morrownr/7612u

3. **morrownr/USB-WiFi Issues #2**（AWUS036ACM Master Mode on RPi）— 2021年討論，仍為最詳細的 ACM AP 設定參考  
   https://github.com/morrownr/USB-WiFi/issues/2

4. **morrownr/USB-WiFi Issues #476**（AWUS036AXML on RPi5 + Kali）— MT7921AUN AP 問題最新討論  
   https://github.com/morrownr/USB-WiFi/issues/476

5. **morrownr/USB-WiFi Discussions #31**（AWUS036ACHM 全速 AP 設定）  
   https://github.com/morrownr/USB-WiFi/discussions/31

6. **koutto/pi-pwnbox-rogueap**（GitHub）— 以 Alfa 網路卡建立 RogueAP 的實際案例  
   https://github.com/koutto/pi-pwnbox-rogueap

7. **Rokland**（授權 Alfa 零售商）— AWUS036ACM、AWUS036ACH、AWUS036AXML Linux 支援頁  
   https://store.rokland.com

8. **Lab401**（歐洲滲透測試設備零售商）— AWUS036ACHM 評測及 2025 滲透測試最佳選擇報告  
   https://lab401.com/products/alpha-awus036achm

9. **Yupitek 部落格現有文章**  
   - AWUS036ACM China Install Guide（含 VIF 設定）  
   - AWUS036AXML WiFi 6E Review  
   - Best WiFi Adapters for Kali Linux in 2026  
   - AWUS036ACM IBSS & Mesh on Raspberry Pi  
   https://yupitek.com/en/blog/

10. **morrownr/USB-WiFi DeepWiki**（自動整理的知識庫）  
    https://deepwiki.com/morrownr/USB-WiFi

11. **ALFA Network 官方網站**  
    https://www.alfa.com.tw/

---

*本報告由 Yupitek 內部研究整理，日期：2026年5月。如需更新請重新確認 morrownr/USB-WiFi 及各 kernel 發布記錄的最新資訊。*
