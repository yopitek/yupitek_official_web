---
title: "免裝驅動：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驅動啟用 ALFA 網卡 Monitor 與 AP 模式（rtw88 / rtw89 / mt76 實測）"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Ubuntu 24.04 / kernel 6.17 免裝驅動教學：用 in-kernel rtw88 / rtw89 / mt76 驅動啟用 ALFA 網卡 Monitor 與 AP 模式，含 WPA3 熱點相容性設定與 Kali 工具鏈注意事項。"
faq:
  - question: "Ubuntu 24.04 要怎麼讓 ALFA 網卡進入 monitor mode？"
    answer: "在 kernel 6.17 以上，只要把介面交出 NetworkManager 管理、切換成 monitor 介面模式即可，不需安裝第三方驅動；本文測試的 rtw88 / rtw89 / mt76 三個驅動家族流程一致，詳細指令見文中步驟。"
  - question: "為什麼在 Ubuntu 上 ALFA 網卡不用另外裝驅動？"
    answer: "因為 Realtek rtw88／rtw89 與 MediaTek mt76 已陸續把這些 USB 晶片納入 mainline kernel 的 in-kernel 支援（各卡最低版本不同，從 4.19 到 6.17；Ubuntu 24.04 上的 AX、AXER 需要 kernel 6.17 以上，例如 24.04.4 的 HWE）；kernel 6.17（GX10 實測）9 款卡皆內建，插上即認、免編譯、免 DKMS。"
  - question: "用 ALFA 網卡架 WPA3 熱點，舊 iPhone 連不上怎麼辦？"
    answer: "實測發現兩個常見原因：一是 hostapd 的 sae_pwe 需設為 0 而非 2 才相容舊款 iPhone；二是保留 802.11n 設定可能讓舊裝置關聯失敗，相容性優先時建議關閉 802.11n。"
  - question: "rtw88、rtw89、mt76 哪個驅動家族支援 mesh 或 IBSS？"
    answer: "實測中 mt76 家族（如 AWUS036ACM / ACHM）可單機建立 mesh（802.11s）與 IBSS；Realtek rtw88 可單機 join IBSS（以 ACH 實測為準）但不支援 mesh，rtw89 則連 IBSS 都未宣告支援。"
draft: false
---

> 本文為標準 Linux 網路設定教學，示範如何在新版 kernel 用**內建（in-kernel）驅動**啟用 ALFA 無線網卡的 Monitor（監聽）與 AP（熱點）模式。
> 測試平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有數據均為 Yopitek 於自有設備、自有辦公室 Wi-Fi（SSID `YUPITEK`）上的產品相容性實測節錄。
> ⚠️ **合法使用**：Monitor 模式僅限監聽自己擁有或已取得授權的網路；AP 模式請遵守當地無線電法規。本文不涉及針對第三方網路的任何攻擊操作。

---

## 重點摘要（TL;DR）

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）上，Yopitek（ALFA Network 台灣經銷）實測的 9 款 ALFA USB 無線網卡全部走 in-kernel 驅動（`rtw88` / `rtw89` / `mt76`），免裝驅動即可用同一套流程啟用 Monitor 與 AP 模式，2.4G 與 5G AP 下 iPhone 7 Plus / 15 Pro 都能正常連線；各卡最低 kernel 介於 4.19 至 6.17。

- **新 kernel 免裝驅動**：Realtek `rtw88` / `rtw89` 與 MediaTek `mt76` 已把 ALFA 這些 USB 晶片納入 in-kernel 支援；kernel 6.17（GX10 實測）9 張卡皆內建，各卡最低版本不同，插上即用、免編譯、免 DKMS。
- **Monitor 與 AP 流程三家族一致**：交回 NetworkManager →`iw` 切 monitor／`hostapd` 起 AP。
- **兩個相容性雷**：開 AP 建議關 802.11n（`ieee80211n=0`）、WPA3-SAE 用 `sae_pwe=0`，否則舊款 iPhone 連不上。
- **進階模式分級**：mesh 僅 `mt76`；IBSS 單機 `mt76` 與 `rtw88`（ACH）可 join，`rtw89` 未宣告。
- **平台鐵則**：絕不執行 `airmon-ng check kill`（會讓 GX10 斷網），只操作外接的 `wlx*` 介面。

## 1. 為什麼「免裝驅動」是這一代的重點

過去在 Linux 上使用 ALFA 這類 USB 無線網卡，最常見的門檻就是驅動。RTL8812AU、MT7610U 這些晶片早年都沒有進 mainline kernel，使用者得從 GitHub 抓 out-of-tree 專案（例如 `morrownr/USB-WiFi`、`aircrack-ng/rtl8812au`），再透過 DKMS 綁定當前 kernel 版本編譯。每次 kernel 更新，DKMS 就得重編一次；一旦編譯失敗，網卡就直接消失。對需要穩定維運的經銷驗證或教學環境來說，這是長期的痛點。

近年的 mainline kernel 讓情況出現轉折：Realtek 的 `rtw88`、`rtw89` 與 MediaTek 的 `mt76` 三大驅動家族陸續把這些 USB 晶片正式納入 in-kernel 支援。kernel 6.17（GX10 實測）9 張卡皆內建，各卡最低版本不同（見下表「最低 kernel」欄），**插上即認、免編譯、免 DKMS**。更重要的是，原本兩個最多人用的 out-of-tree 專案（morrownr 與 aircrack-ng 的 rtl8812au）現在都已改為導向這顆內建驅動，bug 回報也統一回到 `lwfinger/rtw88`。換句話說，手動編驅動這個步驟，在新 kernel 上已經可以直接省略。

`lwfinger/rtw88` 社群仍在活躍維護，持續把修正往上游送，內建驅動的穩定度因此跟著 kernel 一起更新，使用者不必再各自維護分支、也不會每次升級就被 DKMS 編譯失敗卡住。對經銷驗證與教學環境來說，同一套操作步驟能跨多張卡、跨多次 kernel 更新重複使用，維護成本明顯下降，這也是本文把重點放在「免裝驅動」的原因。

本文測試涵蓋的晶片與對應內建驅動模組如下：

| 晶片家族 | 晶片型號 | 內建驅動模組 | 最低 kernel | 世代 / 串流 | 代表卡 |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1（+BT） | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> 若你的系統 kernel 低於該卡的最低版本（見上表），才需要走舊路：用 DKMS 安裝 out-of-tree 驅動（rtw88 系列可用 `lwfinger/rtw88`）。以 Ubuntu 24.04 為例：GA kernel 6.8 已內建 ACM、ACHM、AXM、AXML、EACS 的驅動；HWE 6.14 再加上 ACH、ACS。AX、AXER 需要 kernel 6.17 以上（例如 24.04.4 的 HWE）。本文以 GX10 的 kernel 6.17 為準。

---

## 2. 確認驅動已載入並綁定

在切換任何模式前，先確認卡被正確辨識、驅動已綁定、介面名稱已生成。以 Realtek 的 AWUS036ACH（`rtw88_8812au`）為例，四個檢查步驟如下。

**步驟一：確認 USB 裝置被列舉。** 用 `lsusb` 找 USB ID（Realtek 多為 `0bda:xxxx`，MediaTek 多為 `0e8d:xxxx`）：

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**步驟二：確認驅動綁定與 USB 速率。** `lsusb -t` 可同時看到綁定的 driver 與連線速度（`5000M` 代表走 USB 3.0）：

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

MediaTek 卡則可改用 `dmesg` 觀察驅動初始化訊息，同時確認介面改名：

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**步驟三：取得介面名稱。** Ubuntu 採可預測命名（predictable naming），ALFA 外接卡一律是 `wlx` 加上 MAC 位址。這個名稱由 MAC 決定，**重新插拔後不會改變**，方便腳本化。內建的對外網卡則是另一組名稱（GX10 上為 `wlP9s9`），務必分辨清楚：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**步驟四：查詢晶片宣告支援的介面模式。** 這一步決定了後面哪些模式能用：

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88（ACH）會列出 `IBSS / managed / AP / AP/VLAN / monitor`，但**沒有** mesh 與 P2P；MediaTek mt76（ACHM）則會額外列出 `mesh point / P2P-client / P2P-GO`。這份清單就是各家族能力差異的第一手依據，詳見第 5 節。

---

## 3. 啟用 Monitor 模式（2.4 GHz / 5 GHz）

Monitor（監聽）模式讓網卡不關聯任何 AP、直接接收空中的 802.11 frame，常用於自家網路的封包診斷、頻譜巡檢與訊號覆蓋評估。三個家族的啟用流程一致，差別只在個別家族的穩定性注意事項（見第 5、6 節）。

**通用啟用步驟：**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # 交回給我們自己管, 避免 NetworkManager 介入
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

看到 `type monitor` 就代表切換成功。接著指定要監聽的頻道。**2.4 GHz** 用 `set channel`：

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

**5 GHz** 用頻率指定較不易出錯（ch36 = 5180 MHz）：

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**預期結果（實測節錄）：** AWUS036ACH 於 ch1 / ch6 / ch11 分別抓到 92 / 214 / 71 個 frame；5 GHz 的 ch36 / ch149 / ch157 分別抓到 260 / 137 / 127 個 frame，代表 2.4G 與 5G 監聽都正常。MediaTek 的 ACHM 以 `airodump-ng --band abg` 跳頻掃描 120 秒，可在 ch1/5/6/36/149/157 一帶找到 19 個基地台、14 個用戶端。某頻道抓到 0 封包，通常只是當下該頻道沒有 AP，不是網卡故障。

切到 monitor 模式後，常見的標準診斷工具都能直接在 `wlx*` 介面上運作：`airmon-ng` 用來列出網卡與驅動狀態、`kismet` 可當成資料來源即時側錄並產生 `.kismet` log、`Wireshark` 與 `tshark` 負責解析擷取到的封包、`bettercap` 則可做頻道巡檢。這些工具在三個家族上都實測可用，很適合用來盤點自家無線環境的頻道使用狀況與訊號覆蓋。唯一要注意的是 `hcxdumptool` 8.x 在本平台對三個家族都會 `failed to arm`，唯 EACS 在 2.4 GHz 例外（內建驅動不提供 active-monitor），若需要類似功能請改用 `airodump-ng` 搭配 aircrack-ng 套件。

> **5 GHz 提醒：** 預設 regdomain（`country 00`）下，許多 5 GHz 頻道是 passive/no-IR，監聽可以但主動傳送受限。若後續要做授權範圍內的 5 GHz 測試，請先 `sudo iw reg set US` 解鎖、測完再 `sudo iw reg set TW` 設回。Realtek `rtw88_8812au` 另有已知的 5G RX-stuck 現象（反覆切模式後 5G 收不到封包），遇到時請實體拔插一次卡再優先做 5G。

---

## 4. 啟用 AP / 熱點模式（2.4 GHz / 5 GHz）

AP（熱點）模式用 `hostapd` 把網卡變成一個 Wi-Fi 基地台。三個家族的流程相同：先把介面交出 NetworkManager，再用一份 `hostapd` 設定檔啟動。以下是通用的最小設定。

**4-1. 2.4 GHz（純 802.11g）**

建立設定檔 `/tmp/ap24.conf`：

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<你的密碼至少8碼>
```

啟動：

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

當用戶端連上時，`hostapd` 會依序輸出 `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED`，看到最後一行就代表四向交握完成、連線成功。

**4-2. 5 GHz（純 802.11a，ch36）**

把上面設定改成 5 GHz：

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2 的卡（如 rtw89 的 AX/AXER、mt76 的 ACM/AXM）可再加 VHT80 設定拉到 80 MHz 頻寬；單天線或求相容性時，維持 20 MHz 純 a 即可。

**4-3. 兩個關鍵相容性設定**

1. **開 AP 建議關 802.11n**（`ieee80211n=0`，走純 g / 純 a）。實測舊款用戶端（iPhone 7 Plus）在保留 `ieee80211n=1` 時會關聯失敗、畫面誤報「密碼錯誤」，實際是 `handle_assoc_cb: STA not found`；移除 802.11n 即第一次就連上。
2. **WPA3-SAE 請用 `sae_pwe=0`**（hunting-and-pecking）。用 `sae_pwe=2`（強制 H2E）時舊機金鑰交握會失敗。WPA3 段落範例：

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

這兩個雷在 Realtek 與 MediaTek 卡上都一樣會遇到，屬於用戶端相容性而非驅動差異。本文測試的九張卡在 2.4G 與 5G AP 下都能讓 iPhone 7 Plus / 15 Pro 正常連入。

**4-4. 一邊上網、一邊當熱點（STA + AP）**

mt76 家族支援用一張卡同時連上現有 Wi-Fi、又另建一個 AP VIF 當中繼熱點。實測 ACHM 在主介面連著 YUPITEK 的同時開出 5 GHz 熱點讓 iPhone 連入，下載仍有 198 Mbit/s、ping 平均 3.2 ms。此組合需滿足三個條件：AP VIF 要用不同的 MAC、介面名稱維持 `wlx` 格式、且所有 VIF 都在同一個頻道。Realtek 卡此組合未被 phy 保證（rtw88 的 managed + monitor 雖可用，但 STA + AP 並不穩定），要做中繼熱點建議優先選 mt76 家族。

---

## 5. 三晶片家族差異與限制

基本的 managed / monitor / AP 三模式，三個家族都支援、表現一致。差異在**進階介面模式**（mesh、IBSS、active monitor、P2P）：這完全取決於驅動宣告，和卡的天線數無關。以下是實測彙整。

| 進階模式 | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor（2.4G/5G） | ✅ | ✅ | ✅ |
| AP（hostapd） | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS（單機） | 🟡 單機可建立 | 🟡 單機可建立 | ❌ 驅動未宣告 |
| Mesh（802.11s，單機） | 🟡 單機可建立 | ❌ `-95` 不支援 | ❌ 驅動未宣告 |
| Active monitor | 🟡 可設定 | ❌ `-95` 不支援 | N/A |
| Wi-Fi Direct（P2P） | 需第二台裝置 | ❌ `-95` 不支援 | N/A |

**MediaTek mt76（ACM / ACHM / AXM / AXML）** 是進階模式最完整的一家。`iw phy info` 就宣告了 `mesh point`、`IBSS`、`P2P-client/GO`。實測單機即可 `Joined IBSS`、`type mesh point` 並發出對應 beacon（與第二台 peer link 因缺第二台設備未驗）。如果你的用途是 mesh 或 IBSS 單機實驗，mt76 家族是首選。要特別注意的是 Wi-Fi 6 的 MT7921（AXM/AXML）雖然模式齊全、AP 穩定，但在本平台無法做 frame injection（主因是 stock kernel 6.16+ 的 mac80211 chanctx 回歸，非晶片先天；社群同型號改用 git／patched 驅動雖可運作但 firmware 鎖速率，對應 morrownr/USB-WiFi #387、morrownr/mt76 #18），不適合需要注入的進階測試。

**Realtek rtw88（ACH / ACS / EACS）** 支援 `IBSS / managed / AP / AP/VLAN / monitor`。IBSS 單機可建立（`Joined IBSS`，以 ACH 實測為準；EACS 雖列出 iftype 但實測 join 無效），但 **mesh（802.11s）、active monitor、Wi-Fi Direct 三者實測皆回 `Operation not supported (-95)`**。另一個 rtw88 專屬特性是 VIF：`iw phy` 旗標雖寫「interface combinations are not supported」，但 ACH 實測 managed + monitor 兩介面可同時 up、monitor VIF 抓到 100 個 frame，「邊上網邊側錄」可行；不過 phy 未保證此組合，重負載長跑仍建議用 mt76 家族。

**Realtek rtw89（AX / AXER）** 是本文最新的 Wi-Fi 6 家族，monitor 與 AP（含 VHT80）都表現良好、接收靈敏度強。但在進階模式上，active monitor / mesh / IBSS / P2P 在驅動層即未宣告（N/A），因此這些單機實驗請改用 mt76 卡。rtw89 的定位是穩定的 Wi-Fi 6 監聽與熱點，不是進階介面模式的實驗平台。

> 一句話選型：**要 mesh / IBSS 單機 → mt76（ACM / ACHM）；要 Wi-Fi 6 熱點與強接收 → rtw89（AX / AXER）；要雙頻通用與 VIF → rtw88（ACH）。**

---

## 6. 平台安全注意（GX10 + Ubuntu ARM64）

在 GX10 這類「內建網卡負責對外上網、外接 ALFA 卡做測試」的機器上，以下幾點是維運鐵則，照做才不會把自己弄斷網。

1. **絕不執行 `airmon-ng check kill`。** 這個指令會關掉 NetworkManager，連帶讓 GX10 的對外連線中斷。本文全程只用 `iw` 與 `nmcli dev set <介面> managed no`，不碰 `check kill`。
2. **只操作 `wlx*`，絕不碰內建 `wlP9s9`。** `wlP9s9` 是 GX10 對外上網的主線，任何 down / 改模式的動作都只能對 ALFA 的 `wlx*` 介面下，下指令前務必用 `echo $IF` 確認目標。
3. **RX stall 用拔插復原。** 反覆切換 monitor / AP 後若掃不到任何東西，多半是驅動的接收卡死（Realtek 5G 尤其常見）。軟體通常救不回來，直接**實體拔插一次**卡，USB 會重新列舉、介面名稱因 MAC 不變而維持一致。
4. **BT+WiFi 複合卡換 USB 孔。** EACS、AXML 這類藍牙加 Wi-Fi 的複合裝置，重插時偶爾 Wi-Fi probe 會卡死、生不出 `wlx` 介面，換一個 USB 孔通常就正常。
5. **5 GHz 傳送先設 regdomain。** 預設 `country 00` 下 5 GHz 多為 no-IR、禁止主動傳送。授權範圍內測試前 `sudo iw reg set US` 解鎖，測完 `sudo iw reg set TW` 設回。
6. **ARM64 的套件注意。** GX10 是 aarch64，`aircrack-ng` 常缺 prebuilt wheel/package，需自原始碼編譯；`wifite` 建議用 GitHub 版以繞過 apt 依賴衝突。另外 `hcxdumptool` 8.x 在本平台對三個家族都會 `failed to arm`，唯 EACS 在 2.4 GHz 例外（內建驅動無 active-monitor 支援），監聽擷取請改用 `airodump-ng` 搭配 aircrack-ng 套件。

**測試結束後恢復一般模式：**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # 預期 type managed
```

---

## 常見問題（FAQ）

**Q：Ubuntu 24.04 要怎麼讓 ALFA 網卡進入 monitor mode？**
A：在 kernel 6.17 以上，只要把介面交出 NetworkManager 管理、切換成 monitor 介面模式即可，不需安裝第三方驅動；本文測試的 rtw88 / rtw89 / mt76 三個驅動家族流程一致，詳細指令見文中步驟。

**Q：為什麼在 Ubuntu 上 ALFA 網卡不用另外裝驅動？**
A：因為 Realtek `rtw88`／`rtw89` 與 MediaTek `mt76` 已陸續把這些 USB 晶片納入 mainline kernel 的 in-kernel 支援（各卡最低版本不同，從 4.19 到 6.17；Ubuntu 24.04 上的 AX、AXER 需要 kernel 6.17 以上，例如 24.04.4 的 HWE）；kernel 6.17（GX10 實測）9 款卡皆內建，插上即認、免編譯、免 DKMS。

**Q：用 ALFA 網卡架 WPA3 熱點，舊 iPhone 連不上怎麼辦？**
A：實測發現兩個常見原因：一是 hostapd 的 `sae_pwe` 需設為 0 而非 2 才相容舊款 iPhone；二是保留 802.11n 設定可能讓舊裝置關聯失敗，相容性優先時建議關閉 802.11n。

**Q：`rtw88`、`rtw89`、`mt76` 哪個驅動家族支援 mesh 或 IBSS？**
A：實測中 `mt76` 家族（如 AWUS036ACM / ACHM）可單機建立 mesh（802.11s）與 IBSS；Realtek `rtw88` 可單機 join IBSS（以 ACH 實測為準）但不支援 mesh，`rtw89` 則連 IBSS 都未宣告支援。

## 7. 延伸閱讀

- 九張 ALFA 卡的完整能力比較與選型總評 → [ALFA 無線網卡總評 Hub（總表）](/zh-tw/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Realtek rtw88 代表卡逐步教學 → [AWUS036ACH 單卡實測](/zh-tw/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- MediaTek mt76 代表卡逐步教學 → [AWUS036ACHM 單卡實測](/zh-tw/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*測試單位：Yopitek（ALFA Network 台灣經銷）— https://www.yupitek.com ｜ 測試環境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 測試裝置：Apple iPhone 7 Plus（WPA3 另測 iPhone 15 Pro）*
