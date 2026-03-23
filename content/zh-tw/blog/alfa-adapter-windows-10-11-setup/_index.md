---
title: "ALFA 無線網路卡 Windows 10/11 安裝設定完整指南"
description: "如何在 Windows 10/11 安裝與設定 ALFA USB WiFi 網路卡。驅動程式下載、使用 Acrylic WiFi 的監聽模式、疑難排解，以及 Windows 使用者的網路卡比較。"
date: 2026-04-15
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-網路卡", "驅動程式安裝", "acrylic-wifi"]
---

ALFA Network USB WiFi 網路卡在資安研究與網路工程領域廣為人知，但大多數教學文章都以 Linux 為主。對 Windows 使用者來說，好消息是：所有主要 ALFA 網路卡均可在 Windows 10 與 Windows 11 上使用製造商提供的驅動程式正常運作，無需自行編譯原始碼。

與 Linux 最關鍵的差異在於監聽模式（Monitor Mode）。在 Linux 上，`aircrack-ng` 和 `airodump-ng` 等工具可透過原始 802.11 封包擷取與封包注入（Packet Injection）操作硬體。在 Windows 上，驅動程式模型（NDIS）並未開放相同的硬體功能。**Windows 原生並不支援完整的監聽模式與封包注入。** Windows 的優勢在於即插即用的連線能力，以及使用 Acrylic WiFi Analyzer 等精緻工具進行 WiFi 掃描。

本指南將說明驅動程式安裝、WiFi 掃描，並客觀評估 Windows 搭配 ALFA 網路卡的使用限制與能力。

---

## 支援 Windows 的 ALFA 網路卡一覽

以下所有網路卡均正式支援 Windows 10 與 Windows 11。驅動程式支援狀況與監聽模式能力因晶片組而異。

| 型號 | 晶片組 | Windows 10 | Windows 11 | 監聽模式支援 |
|---|---|---|---|---|
| [AWUS036ACH](/zh-tw/products/alfa/awus036ach/) | RTL8812AU | ✅ 完整支援 | ✅ 完整支援 | ⚠️ 僅被動掃描（Acrylic WiFi Pro）|
| [AWUS036ACM](/zh-tw/products/alfa/awus036acm/) | MT7612U | ✅ 完整支援 | ✅ 完整支援 | ⚠️ 僅被動掃描 |
| [AWUS036ACS](/zh-tw/products/alfa/awus036acs/) | RTL8811AU | ✅ 完整支援 | ✅ 完整支援 | ⚠️ 僅被動掃描 |
| [AWUS036AX](/zh-tw/products/alfa/awus036ax/) | MT7921AU | ⚠️ 需手動下載驅動程式 | ✅ 內建驅動程式 | ⚠️ 功能受限 |
| [AWUS036AXER](/zh-tw/products/alfa/awus036axer/) | MT7921AU | ⚠️ 需手動下載驅動程式 | ✅ 內建驅動程式 | ⚠️ 功能受限 |
| [AWUS036AXM](/zh-tw/products/alfa/awus036axm/) | MT7921AU | ⚠️ 需手動下載驅動程式 | ✅ 內建驅動程式 | ❌ 不支援 |
| [AWUS036AXML](/zh-tw/products/alfa/awus036axml/) | MT7902 | ⚠️ 需手動下載驅動程式 | ✅ 內建驅動程式 | ❌ 不支援 |

{{< alert "circle-info" >}}
若以 Windows 日常使用為主要需求，AWUS036ACH（RTL8812AU）與 AWUS036ACM（MT7612U）是最經過實戰驗證的選擇。兩款均有 Realtek／MediaTek WHQL 簽署驅動程式，Windows 相容性紀錄最為完整。
{{< /alert >}}

---

## 安裝驅動程式

### 方法 A：Windows Update（建議）

對大多數網路卡而言，Windows Update 是最簡單的安裝方式。插入支援的 ALFA 網路卡後，Windows 會自動向 Windows Update 查詢對應的 NDIS 驅動程式。

1. 將 ALFA 網路卡插入 USB 3.0 連接埠。
2. 等待 30–60 秒。Windows 10 會顯示通知：*「裝置驅動程式軟體已成功安裝」*；Windows 11 則會靜默完成安裝。
3. 開啟**裝置管理員**（`Win + X` → 裝置管理員）。
4. 展開**網路介面卡**。應可看到網路卡列表（例如 *「Realtek 8812AU Wireless LAN 802.11ac USB NIC」* 或 *「MediaTek Wi-Fi 6 MT7921U Wireless LAN Card」*）。
5. 若網路卡旁出現黃色警告圖示，請繼續使用方法 B。

{{< alert "circle-info" >}}
Windows Update 需要有效的網路連線才能下載驅動程式。若您正在設定隔離的實驗室機器，請先在另一台電腦上下載驅動程式套件，再以手動方式傳輸後使用方法 B 安裝。
{{< /alert >}}

### 方法 B：手動安裝驅動程式 — RTL8812AU（AWUS036ACH / AWUS036ACM / AWUS036ACS）

1. 前往 [ALFA Network 下載頁面](https://www.alfa.com.tw/service_1.html) 或 Realtek 驅動程式封存庫，下載 RTL8812AU 最新的 Windows WHQL 驅動程式。
2. 將 `.zip` 壓縮檔解壓縮至本機資料夾（例如 `C:\Drivers\RTL8812AU`）。
3. 以系統管理員身分執行 `.exe` 安裝程式，並接受 UAC 提示。
4. 按照安裝精靈進行。出現提示時，保留預設安裝路徑即可。
5. 安裝完成後重新開機。
6. 開啟**裝置管理員** → **網路介面卡**，確認網路卡顯示時無警告圖示。

驗證驅動程式版本：

1. 在裝置管理員中對網路卡按右鍵 → **內容**。
2. 點選**驅動程式**索引標籤。
3. 記下**驅動程式版本**與**驅動程式日期**以備日後參考。

### 方法 B：手動安裝驅動程式 — MT7921AU（AWUS036AX / AWUS036AXER / AWUS036AXM / AWUS036AXML）

MediaTek MT7921AU 驅動程式已內建於 Windows 11 驅動程式存放區（組建 22000 以上）。Windows 10 請依下列步驟操作：

1. 從 [MediaTek 官方網站](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) 或 ALFA Network 支援頁面下載 MediaTek MT7921 驅動程式套件。
2. 解壓縮套件後，以系統管理員身分執行 `Setup.exe`。
3. 安裝完成後重新開機。

{{< alert "circle-info" >}}
使用 MT7921AU／MT7902 網路卡的 Windows 11 使用者，即使是全新安裝，通常在插入網路卡數分鐘內便可取得可用的驅動程式，無需手動下載。
{{< /alert >}}

### 常見裝置管理員錯誤代碼

| 錯誤代碼 | 說明 | 初步解決方式 |
|---|---|---|
| **Code 43** | 驅動程式回報失敗 | 解除安裝驅動程式 → 重新開機 → 重新安裝 |
| **Code 10** | 裝置無法啟動 | 嘗試不同的 USB 連接埠；停用 USB 選擇性暫停 |
| **Code 28** | 未安裝驅動程式 | 執行 Windows Update 或手動安裝驅動程式 |
| **Code 45** | 裝置未連接 | 重新插接網路卡；若使用延長線請嘗試更換 USB 線 |

---

## 在 Windows 上使用 ALFA 網路卡進行 WiFi 掃描

### Windows 原生命令列掃描

Windows 內建 WiFi 掃描指令，無需額外安裝軟體：

```cmd
netsh wlan show networks mode=bssid
```

此指令可輸出所有可見的 SSID，包含 BSSID（MAC 位址）、訊號強度、無線電類型、頻道與驗證類型。適合快速診斷，但缺乏即時頻道圖表或隱藏 SSID 偵測功能。

### Acrylic WiFi Analyzer（免費版）

若要在 Windows 上進行進階 WiFi 分析，[Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) 是推薦工具。免費版提供：

- 2.4 GHz、5 GHz 與 6 GHz 頻段即時掃描
- 頻道佔用圖表 — 立即識別擁塞頻道
- 隱藏 SSID 偵測（顯示廣播空白 SSID 的網路）
- 個別存取點的訊號歷程圖
- BSSID 識別的廠商 OUI 查詢

Acrylic WiFi 可與所有 Windows 相容的 WiFi 網路卡搭配使用，包含上述所有 ALFA 型號。其 NDIS 驅動程式擴充模組直接整合至 Windows 無線網路堆疊，因此無需 Linux 風格的監聽模式即可運作。

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer 是 Windows 上最接近 `airodump-ng` 被動掃描功能的工具。若您的工作流程是 WiFi 勘測、場地分析或頻道規劃，它幾乎涵蓋所有需求，無需離開 Windows 環境。
{{< /alert >}}

### 在 Windows 上使用 Wireshark 擷取封包

在 Npcap 的輔助下，Wireshark 可在 Windows 上擷取 WiFi 流量（詳見下方專屬章節）。然而，在沒有真正監聽模式的情況下，您只能擷取：

- 傳送至您的網路卡的封包（單播至您的 MAC 位址）
- 所連接網路的廣播與多播封包

除非其他裝置恰好位於相同的廣播網域且 Wireshark 在交換式網路上以混雜模式運作，否則您**無法**擷取其他裝置之間的流量。完整的 802.11 封包擷取（管理訊框、來自外部 AP 的信標訊框）功能受到限制。

---

## Windows 的監聽模式（真相）

這部分需要明確說明期望。

**Windows 的監聽模式與 Linux 的監聽模式有根本性的差異。**

在 Linux 上，`aircrack-ng/rtl8812au` 等驅動程式可開放真正的監聽模式介面（`wlan0mon`），無需連線即可接收無線電環境中的所有 802.11 訊框——管理訊框、來自其他網路的資料訊框、探測請求與信標訊框。網路卡同時支援封包注入：在硬體層級傳送原始 802.11 訊框。

在 Windows 上，NDIS 驅動程式模型未開放這些功能。Windows 環境下監聽的兩種實際方案為：

**方案 A：Acrylic WiFi Pro + 相容驅動程式**

Acrylic WiFi Pro 使用自訂 NDIS 驅動程式擴充模組來啟用*被動 802.11 掃描*。這讓您可以接收非連線存取點的信標訊框與探測回應——足以用於 RF 勘測、頻道分析與 AP 列舉。**不支援**封包注入或完整握手封包擷取。

**方案 B：Kali Linux Live USB**

對於需要完整監聽模式與封包注入的工作流程——WPA 握手封包擷取、去驗證測試、信標洪水攻擊——正確的平台是 Kali Linux。您有兩種選擇：

- 在同一台機器上啟動 **Kali Linux Live USB**（裸機，完整硬體存取）
- 執行 **Kali Linux 虛擬機器**（VMware 或 VirtualBox），透過 USB 直通將 ALFA 網路卡直接交給虛擬機器的 USB 堆疊

詳細的虛擬機器設定說明，請參閱 [VirtualBox／VMware USB 直通指南](/zh-tw/blog/alfa-adapter-virtualbox-vmware-usb/)。

{{< alert "triangle-exclamation" >}}
若您的工作流程需要監聽模式加封包注入——WPA 握手封包擷取、去驗證訊框或任何主動 802.11 攻擊——Windows 無法可靠地完成這些任務。Kali Linux（裸機或透過 USB 直通的虛擬機器）才是正確的平台。目前沒有任何 Windows 驅動程式支援 ALFA 網路卡的原始 802.11 注入功能。
{{< /alert >}}

---

## 疑難排解

### 網路卡完全無法識別

1. 嘗試不同的 USB 連接埠，優先選用 USB 3.0（藍色連接埠）。部分 USB 集線器對雙頻網路卡供電不足。
2. 開啟裝置管理員，在**其他裝置**下尋找帶有黃色問號的項目。這表示 Windows 偵測到硬體但缺少驅動程式。
3. 按右鍵 → **更新驅動程式** → **瀏覽電腦上的驅動程式**，並指向手動下載的驅動程式資料夾。
4. 若裝置管理員中（包含「其他裝置」）完全沒有顯示，請嘗試更換 USB 線（若使用延長線），或在另一台電腦上測試網路卡以排除硬體故障。

### 裝置管理員中可見網路卡但找不到任何網路

1. 暫時停用 Windows Defender 防火牆，確認是否影響網路卡初始化。測試後請重新啟用。
2. 在裝置管理員中，對網路卡按右鍵 → **內容** → **進階**索引標籤。尋找**無線模式**或**頻段**設定。若設為僅 5 GHz，在純 2.4 GHz 環境中將看不到任何網路。
3. 確認網路卡未被停用：按右鍵 → **啟用裝置**。
4. 在提升權限的命令提示字元中執行 `netsh wlan show interfaces`，確認網路卡的運作狀態。

### Windows 11 速度緩慢或頻繁斷線

Windows 11 的**連線待命**（Modern Standby）功能可能因積極暫停 USB 裝置而干擾 USB WiFi 網路卡。

停用 USB 選擇性暫停：

1. 開啟**控制台** → **電源選項** → **變更計劃設定** → **變更進階電源設定**。
2. 展開 **USB 設定** → **USB 選擇性暫停設定**。
3. 將**使用電池**與**已插上電源**均設為**已停用**。
4. 按一下**套用** → **確定**，然後重新開機。

### Code 43：驅動程式回報失敗

1. 開啟裝置管理員，對網路卡按右鍵 → **解除安裝裝置**。若出現*「刪除此裝置的驅動程式軟體」*選項，請勾選。
2. 拔除網路卡。
3. 重新開機。
4. 重新插入網路卡。
5. 使用上述方法 B 重新安裝驅動程式。

若完整重新安裝後 Code 43 仍然持續，請嘗試不同的 USB 連接埠或在另一台機器上測試。若在多台機器上持續出現 Code 43，通常表示網路卡硬體本身發生故障。

---

## ALFA 網路卡 + Wireshark 設定

Windows 上的 Wireshark 需要 **Npcap** 作為封包擷取函式庫。WinPcap（舊版替代方案）已過時，無法在現代 Windows 版本上可靠運作。

### 步驟一：安裝 Npcap

1. 從 [https://npcap.com/](https://npcap.com/) 下載 Npcap（個人與教育用途免費）。
2. 以系統管理員身分執行安裝程式。
3. 安裝過程中，若計劃在 Wireshark 旁邊使用任何舊版工具，請勾選**「Install Npcap in WinPcap API-compatible mode」**。
4. 重新開機。

### 步驟二：設定 Wireshark

1. 開啟 Wireshark。ALFA 網路卡將出現在介面清單中。
2. 雙擊網路卡介面以開始擷取。
3. 若要篩選 802.11 管理訊框（信標訊框、探測請求），請使用 Wireshark 顯示篩選器：

```
wlan.fc.type == 0
```

4. 若要專門篩選探測請求：

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
`wlan.fc.type` 篩選器僅在 Wireshark 接收到含有可見標頭的實際 802.11 訊框時才有效。在 Windows 未啟用監聽模式的情況下，即使透過 WiFi 連線，大多數擷取結果仍會顯示 Ethernet II 訊框——NDIS 層在將訊框傳遞至 Npcap 之前已剝離 802.11 標頭。完整的 802.11 標頭擷取需要真正的監聽模式介面，僅在 Linux 上可用。
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
未經授權擷取網路流量在大多數司法管轄區屬於違法行為。請僅對您所擁有或已取得明確書面授權的網路進行流量擷取。
{{< /alert >}}

---

## 總結：ALFA 網路卡在 Windows 與 Linux 的比較

| 功能 | Windows 10/11 | Kali Linux |
|---|---|---|
| **即插即用** | ✅ 自動安裝驅動程式 | ⚠️ 因晶片組而異 |
| **WiFi 掃描** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **監聽模式** | ⚠️ 僅被動（Acrylic Pro）| ✅ 完整監聽模式 |
| **封包注入** | ❌ 不支援 | ✅ 完整注入 |
| **Wireshark 擷取** | ⚠️ 受限（無 802.11 標頭）| ✅ 完整 802.11 擷取 |
| **WPA 握手封包擷取** | ❌ 不可靠 | ✅ aircrack-ng / hcxdumptool |
| **最佳使用場景** | 日常連線、WiFi 勘測、頻道分析 | 資安測試、CTF 挑戰、滲透測試 |

結論：若您的目標是網路連線、WiFi 分析與頻道規劃，Windows 是搭配 ALFA 網路卡的絕佳平台。一旦您的工作流程需要原始 802.11 訊框注入或 WPA 握手封包擷取，請切換至 Kali Linux——無論是裸機安裝或透過 USB 直通的虛擬機器。

---

## 相關指南

- [VirtualBox 與 VMware USB 直通 ALFA 網路卡](/zh-tw/blog/alfa-adapter-virtualbox-vmware-usb/) — 在虛擬機器中以完整 ALFA 網路卡支援執行 Kali Linux
- [Kali Linux 與 Ubuntu 驅動程式安裝指南](/zh-tw/blog/install-alfa-driver-kali-ubuntu/) — 各晶片組完整驅動程式安裝說明
- [ALFA WiFi 網路卡選購指南 2026](/zh-tw/blog/alfa-wifi-adapter-buyer-guide-2026/) — 哪款網路卡最適合您的使用需求
