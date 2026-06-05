---
title: "在 Raspberry Pi 搭配 Kali Linux 使用 ALFA WiFi 網路卡：完整安裝教學"
description: "在執行 Kali Linux ARM64 的 Raspberry Pi 上安裝 ALFA USB WiFi 網路卡。涵蓋 AWUS036ACH RTL8812AU 驅動程式編譯、監聽模式，以及攜帶式滲透測試平台建置。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
---

執行 Kali Linux 的筆記型電腦是標準的滲透測試工作站——但絕非唯一選擇。Raspberry Pi 4 或 Pi 5 搭配 ALFA USB WiFi 網路卡，能打造出一個體積小巧、無風扇、被動散熱的平台：可以放進夾克口袋、靠 USB-C 行動電源供電，並在目標環境中無人看守運行數小時。Kali Linux ARM64 映像由 Offensive Security 官方提供，無需模擬即可在 Pi 4 和 Pi 5 上原生執行，完整提供 Aircrack-ng、Kismet、Wireshark、Bettercap 等 Kali 標準工具包。

最大的障礙是驅動程式。AWUS036ACH 內建的 RTL8812AU 晶片不在主線核心中，這代表你不能插上網路卡就期待它直接運作。你必須針對執行中的 ARM64 核心編譯驅動程式——而編譯參數與 x86-64 不同。本教學帶你完成每一個步驟。

---

## 推薦硬體

並非每種 Pi 型號、網路卡和電源供應器的組合都能穩定運作。以下表格整理了已知可良好運作的組合及相應取捨。

| 元件 | 推薦選擇 | 備註 |
|---|---|---|
| 單板電腦 | Raspberry Pi 5（4 GB 或 8 GB） | Pi 4（4 GB+）也能正常運作；Pi 3B+ 速度不足以應付即時封包擷取 |
| 主要網路卡 | ALFA AWUS036ACH | RTL8812AU 晶片；ARM 驅動支援最佳；雙頻 AC1200 |
| 替代網路卡 | ALFA AWUS036ACM | MT7612U 晶片；驅動程式已內建核心 (mt76x2u)；Kali ARM64 免驅即插即用 |
| WiFi 6 網路卡 | ALFA AWUS036AXM 或 AXML | MT7921AUN 晶片；核心 5.18 起內建；需安裝 firmware-misc-nonfree |
| USB 集線器 | 有源 USB 3.0 集線器 | AWUS036ACH 耗電約 500 mW；不加集線器可能導致 Pi USB 電壓不足 |
| 儲存裝置 | MicroSD 32 GB+（Class 10 / A2） | A2 規格記憶卡啟動及 apt 操作明顯更快 |
| 電源供應器 | 官方 Pi USB-C 電源供應器（≥ 3 A） | 第三方變壓器是穩定性問題的常見來源 |

{{< alert "triangle-exclamation" >}}
AWUS036ACH 是高電流 USB 裝置。在沒有有源 USB 集線器的情況下直接插入 Raspberry Pi 4 或 Pi 5，可能在負載下導致 Pi 降頻或重啟。同時使用其他 USB 周邊時，務必使用有源集線器。
{{< /alert >}}

---

## 在 Raspberry Pi 上安裝 Kali Linux ARM64

### 下載 ARM 映像

Kali Linux 在 [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm) 提供 Raspberry Pi 官方 ARM64 映像。下載標示為 **Raspberry Pi 4（64 位元）** 或 **Raspberry Pi 5（64 位元）** 的映像。請勿使用 32 位元映像——本教學的驅動程式編譯步驟需要 ARM64 核心。

### 燒錄至 MicroSD

可使用 Raspberry Pi Imager 圖形工具或命令列的 `dd` 進行燒錄：

```bash
# 將 /dev/sdX 替換為你的實際 SD 卡裝置（用 lsblk 確認）
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

使用 Raspberry Pi Imager 時，選擇**使用自訂映像** → 選擇 Kali `.img.xz` 檔案 → 選擇 SD 卡 → 開始燒錄。

### 首次開機與初始設定

插入 SD 卡，連接螢幕和鍵盤（或先設定無頭存取），然後開機。預設帳號密碼為：

- **使用者名稱：** `kali`
- **密碼：** `kali`

登入後執行 `kali-tweaks` 並依提示強化預設設定。在安裝任何驅動程式前，先完整更新系統：

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
若計畫透過 SSH 存取 Pi，在首次開機前，可在 SD 卡的 `/boot` 分區放置一個名為 `ssh` 的空白檔案來啟用 SSH。此機制與標準 Raspberry Pi OS 相同。
{{< /alert >}}

---

## 在 Kali ARM64 安裝 RTL8812AU 驅動程式（AWUS036ACH / ACM）

RTL8812AU 驅動程式未包含在主線 Linux 核心中。在 ARM64 上，你必須從原始碼編譯，或安裝 Kali 打包的 DKMS 版本。以下介紹兩種方法——建議先嘗試套件方式，僅在遇到核心版本不相容時才改用手動編譯。

### 方法一：Kali 套件（建議起點）

Kali Linux 提供 RTL8812AU 驅動程式的 DKMS 打包版本，核心更新時會自動重新編譯。

```bash
sudo apt install realtek-rtl88xxau-dkms
```

安裝完成後重啟，並驗證模組已載入：

```bash
sudo modprobe 88XXau
ip link show
```

若看到 `wlan1` 介面（假設 `wlan0` 是 Pi 的內建網路卡），表示驅動程式運作正常。此套件可能比 GitHub 原始碼晚幾週，但是最簡便的起點。

{{< alert "circle-info" >}}
Kali 套件通常足以應付大多數 ARM64 環境。只有在 DKMS 套件無法針對目前核心版本編譯時，才需進行以下的手動編譯（可用 `uname -r` 查看核心版本）。
{{< /alert >}}

### 方法二：從原始碼手動編譯（ARM64）

若 DKMS 套件失敗——最常見的原因是核心版本比套件最後測試的版本更新——請從 GitHub 的 Aircrack-ng fork 直接編譯。這是 ARM64 支援的權威來源。

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 將平台旗標從 x86 切換至 ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

`sed` 指令是與 x86-64 編譯的關鍵差異。若不執行這些指令，Makefile 會預設使用 x86 平台路徑，產生的模組將無法在 ARM64 上載入。

編譯成功後，載入模組並驗證：

```bash
sudo modprobe 88XXau
ip link show
```

應會看到新的介面——通常是 `wlan1`。若 `ip link show` 顯示該介面，表示驅動程式運作正常。

---

## Raspberry Pi 上的 MT7921AUN（AWUS036AXM / AXML）

AWUS036AXM 和 AXML 使用的 MediaTek MT7921AUN 晶片自核心 5.18 起已內建於主線核心。Kali Linux ARM64 映像使用的核心版本遠高於此門檻，這代表插上網路卡驅動程式就會自動載入——無需編譯。

唯一需要的額外步驟是安裝 MT7921AUN 所需的閉源韌體：

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

重啟後，確認網路卡已被偵測且介面已啟動：

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

若 `lsusb` 顯示 MediaTek 裝置，且 `ip link show` 列出新的無線介面，網路卡即已就緒。MT7921AUN 的監聽模式支援自核心 5.18 起已大幅改善，但在某些封包注入測試中可能不如 RTL8812AU 穩定。若需最大程度相容舊有滲透測試工作流程，AWUS036ACH 仍是更穩健的選擇。

---

## 在 Raspberry Pi 上啟用監聽模式

Raspberry Pi 有內建 WiFi 介面（`wlan0`）。保持它連線至你的網路以維持 SSH 存取。專用 ALFA 網路卡（`wlan1`）只用於監聽模式和封包擷取。在無頭 Pi 上絕不要將 `wlan0` 切換至監聽模式——這會中斷你的 SSH 連線。

```bash
# 終止干擾監聽模式的程序（NetworkManager、wpa_supplicant）
sudo airmon-ng check kill

# 在 ALFA 網路卡介面上啟用監聽模式
sudo airmon-ng start wlan1

# 確認監聽模式已啟動
sudo iwconfig wlan1mon

# 開始在所有頻道上擷取
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` 會建立名為 `wlan1mon` 的新介面。後續工具請一律針對 `wlan1mon` 而非 `wlan1` 執行。可用 `iwconfig` 或 `ip link show` 確認介面名稱。
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
執行 `airmon-ng check kill` 會停止 NetworkManager 和 wpa_supplicant。若你透過 `wlan0` 以 SSH 連線，這也會中斷你的 SSH 工作階段。對於無頭設定，在執行這些指令前請先透過乙太網路或第二個有線介面連線，或使用 `tmux` 讓工作階段在斷線後仍可恢復。
{{< /alert >}}

若要停用監聽模式並恢復 managed 模式：

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## 攜帶式滲透測試設定技巧

讓硬體正常運作只是一半的工作。以下實用建議是穩定野外套件與惱人故障堆之間的差異所在。

**網路架構：** 使用 `wlan0`（Pi 內建 WiFi）維持管理連線——從同一 LAN 或熱點上的筆電透過 SSH 連入 Pi。`wlan1`（ALFA 網路卡）完全用於滲透測試活動。絕不混用兩個角色。

**無頭操作：** 避免在野外連接鍵盤、滑鼠和螢幕。在首次開機時設定好 SSH，透過筆電上的終端機存取所有功能。`tmux` 工作階段在重新連線後仍可恢復，在網路狀況不穩定時特別寶貴。

**電源：** 使用最低 3 A 的官方 Raspberry Pi USB-C 電源供應器。若使用 AWUS036ACH，另加一個額定 2.5 A 以上的有源 USB 集線器。優質 USB-C 行動電源（65 W+）可同時為 Pi、集線器和網路卡供電，依負載可持續 4–6 小時。

**儲存：** 將 Kismet 記錄和擷取檔案寫入 USB SSD，而非 MicroSD 卡。MicroSD 卡有寫入次數限制，在持續記錄工作負載下會快速劣化。連接至有源集線器的 USB 3.0 SSD 更快且更耐用。

**外殼：** 選擇有開放 USB 端口或切口的 Pi 外殼，以容納有源集線器。帶被動散熱鰭片的鋁製外殼有助於在持續擷取時控制溫度。

---

## 在 Raspberry Pi 上執行 Kismet

Kismet 是被動 WiFi 掃描器，以背景伺服器模式執行，並提供瀏覽器基礎的網頁介面。非常適合無頭 Pi 部署：讓 Pi 持續運行，從同一網路上的任何裝置查看網頁介面。

```bash
sudo apt install kismet

# 使用 ALFA 網路卡以監聽模式啟動 Kismet
kismet -c wlan1
```

{{< alert "circle-info" >}}
直接傳入介面名稱時，Kismet 會自行將介面切換至監聽模式。啟動 Kismet 前無需執行 `airmon-ng start`，Kismet 會在內部管理介面生命週期。
{{< /alert >}}

啟動後，從網路上任何瀏覽器存取 Kismet 網頁介面：

```
http://raspberrypi.local:2501
```

首次執行時，Kismet 會提示你建立管理員帳號和密碼。登入後，你可以查看偵測到的網路、關聯的客戶端、訊號強度歷史記錄，以及已連接 GPS 裝置的 GPS 資料。

Kismet 預設將所有資料記錄至 `~/.kismet/` 中的 `.kismet` 資料庫檔案，稍後可以匯出供分析或上傳至 WiGLE。

---

## 使用案例：戰駕（Wardriving）設定

執行 Kismet 並搭配 ALFA 網路卡和 GPS 裝置的 Raspberry Pi，是一套完整的自給自足戰駕套件——比任何專用戰駕設備都更小巧、更便宜。

**所需元件：**
- Raspberry Pi 4 或 Pi 5
- ALFA AWUS036ACH
- USB GPS 裝置（u-blox 晶片與 Kismet 相容性良好）
- 有源 USB 集線器
- USB-C 行動電源（65 W+，支援直通充電）

**設定步驟：**

1. 安裝 Kismet 和 GPS 套件：

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. 設定 `gpsd` 讀取 GPS 裝置：

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. 啟動帶 GPS 支援的 Kismet：

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. 將 Pi、集線器、網路卡和行動電源裝入袋子或外殼，放置於車輛中。透過連接至與 Pi 相同 WiFi 網路的手機熱點或平板電腦存取 Kismet 網頁介面。

Kismet 記錄會為每個偵測到的網路儲存 GPS 座標。使用 `kismetdb_to_wigle`（Kismet 附帶）將 `.kismet` 資料庫匯出為 WiGLE CSV 格式，並上傳至 WiGLE 進行地圖標記。

{{< alert "triangle-exclamation" >}}
進行任何網路掃描活動前，請務必遵守當地法律。在許多司法管轄區，僅進行被動掃描的戰駕是合法的；未經授權主動探測或連接網路則不合法。請了解你所在地區的相關法規。
{{< /alert >}}

---

## 延伸閱讀

關於桌上型 Kali Linux 和 Ubuntu 上完整的 RTL8812AU 驅動程式安裝指南，請參閱[在 Kali Linux 和 Ubuntu 安裝 ALFA 驅動程式](/zh-tw/blog/install-alfa-driver-kali-ubuntu/)。若尚在考慮購買哪款網路卡，[2026 ALFA WiFi 網路卡購買指南](/zh-tw/blog/alfa-wifi-adapter-buyer-guide-2026/)涵蓋每款現行型號的晶片組詳情和使用場景建議。
