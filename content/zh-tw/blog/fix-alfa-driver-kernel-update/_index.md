---
title: "ALFA 驅動程式在核心更新後失效？完整修復指南"
description: "Linux 核心更新後 ALFA USB WiFi 網路卡無法使用？完整修復指南：涵蓋 Kali Linux 與 Ubuntu 上的 RTL8812AU、RTL8811AU 及 MT7921AU 驅動程式修復方式。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

你執行了 `sudo apt upgrade`，重新開機後 ALFA 網路卡消失了——沒有介面、沒有燈號、什麼都沒有。這是 Linux 使用者詢問 ALFA Network USB WiFi 網路卡時最常見的問題，而核心更新幾乎是所有問題的根源。本指南將帶你系統性地診斷並修復兩種最常受影響的晶片組：**RTL8812AU**（AWUS036ACH、ACM、ACS）與 **MT7921AU**（AWUS036AXM、AXML、AX）。按照各節步驟操作，你的網路卡應在 15 分鐘內恢復正常。

---

## 為什麼核心更新會破壞驅動程式

Linux WiFi 驅動程式分為兩種：**核心內建**驅動（隨核心原始碼一同發布）與**核心外**驅動（獨立存在於核心之外）。了解你使用的是哪一種，就能清楚知道為何更新會造成問題。

### 核心外驅動程式與 DKMS

RTL8812AU 晶片組使用由社群維護的核心外驅動（最常見的是 `aircrack-ng/rtl8812au` 分支）。由於它不屬於官方核心原始碼，必須**針對你目前執行的核心標頭（headers）重新編譯**。每當核心版本變更——即使只是小版本更新，如 `6.6.15` → `6.6.20`——已編譯的模組便不再相容，核心會拒絕載入它。

**DKMS（動態核心模組支援）** 是標準解決方案。DKMS 會將驅動程式的原始碼註冊至系統層級的掛鉤，每當安裝新核心套件時自動重新編譯模組。若 DKMS 設定正確，核心更新對你來說是透明的：重新開機進入新核心後，網路卡已自動就緒。

DKMS 可能在以下兩種情況下靜默失敗：

1. **缺少核心標頭** — 編譯器需要在新核心安裝時同步安裝 `linux-headers-$(uname -r)`。若標頭在核心之後才到，DKMS 就錯過了建置時機。
2. **過時的 `dkms.conf`** — 若已安裝驅動程式版本的設定檔已不符合原始碼樹的結構，建置將以不明確的錯誤訊息失敗。

### 核心內建驅動程式（MT7921U）

MT7921U 晶片組自核心 **5.18** 版本起已納入主線核心。這意味著不需要編譯步驟——核心已內建與硬體溝通的能力。然而，驅動程式仍依賴一個由獨立套件提供的**韌體二進位檔**（`mt7921u.bin`）。若該套件缺失，或核心更新改變了預期的韌體 API，網路卡可能看似已載入但無法連線。

### 快速診斷指令

在動手修改任何設定前，先執行以下兩條指令了解當前狀況：

```bash
# 目前執行的核心版本為何？
uname -r

# 哪些 DKMS 模組已建置（以及針對哪些核心）？
sudo dkms status
```

若 `dkms status` 顯示 RTL8812AU 驅動程式只針對*舊版*核心建置，而非當前核心，那你已找到問題所在。

---

## 第一步：診斷驅動程式狀況

依序執行以下診斷步驟，每個檢查都能在你開始修改前縮小問題根源。

```bash
# 確認目前核心版本
uname -r

# 確認是否存在任何無線介面
ip link show | grep -E "wlan|wlp"

# 確認驅動程式模組是否已載入
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# 確認 RTL8812AU 網路卡的 DKMS 建置狀態
sudo dkms status

# 掃描核心訊息緩衝區中的相關錯誤
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**解讀結果：**

| 輸出 | 含義 |
|---|---|
| `ip link` 未顯示無線介面 | 核心模組未載入或硬體未被列舉 |
| `lsmod` 未顯示對應模組 | 模組載入失敗——檢查 `dmesg` 的錯誤訊息 |
| `dkms status` 顯示當前核心為 `broken` 或缺失 | DKMS 建置失敗——請按 RTL8812AU 修復步驟操作 |
| `dmesg` 顯示 `firmware: failed to load mt7921u` | 韌體套件缺失——請按 MT7921U 修復步驟操作 |
| `dmesg` 顯示 `disagrees about version of symbol` | 模組針對錯誤的核心標頭建置 |

{{< alert "triangle-exclamation" >}}
若 `ip link` 顯示介面存在，但使用時介面消失，請直接跳至網路卡特定問題排除表格。可見但無法正常使用的介面與完全消失的介面，其原因不同。
{{< /alert >}}

---

## 修復：RTL8812AU 驅動程式（AWUS036ACH、ACM、ACS、EACS）

RTL8812AU 是 ALFA 晶片組中用於滲透測試最廣泛的型號，原因在於其雙頻支援與可靠的監聽模式。它需要核心外驅動，因此也是最常被核心更新破壞的晶片組。

### 4.1 — 安裝核心標頭

在修改任何驅動程式之前，第一步是確認*目前*核心的標頭已安裝：

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

若指令順利完成，標頭現已存在，DKMS 重建可以繼續。若回報找不到套件，你的核心可能太新，目前的套件庫快照尚無對應版本——請先執行 `sudo apt full-upgrade` 取得匹配的標頭，然後重新開機再繼續。

### 4.2 — 透過 DKMS 重建（最快路徑）

標頭就緒後，請 DKMS 為目前執行的核心重建所有已註冊的模組：

```bash
sudo dkms autoinstall
```

仔細觀察輸出。成功的建置以 `DKMS: install completed` 結束。若成功，無需重新開機即可重新載入模組：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

若介面出現，即完成。繼續步驟 4.4 驗證監聽模式。

### 4.3 — 從原始碼完整重裝（DKMS 失敗時）

若 `dkms autoinstall` 回報錯誤，代表已註冊的驅動程式原始碼已損毀或過舊。請完整移除後，從最新上游原始碼重新安裝：

```bash
# 移除所有 DKMS 已註冊的驅動程式版本
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# 複製最新驅動程式原始碼
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# 一步完成：向 DKMS 註冊原始碼、編譯並安裝
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
`dkms remove` 指令中的版本號 `5.6.4.2` 是常見版本，你的版本可能不同。請先執行 `sudo dkms status` 確認輸出中顯示的確切版本字串。
{{< /alert >}}

建置完成後：

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — 驗證監聽模式

網路卡實體存在且驅動程式已載入。確認監聽模式——這也是使此網路卡適用於安全測試的功能——仍然正常：

```bash
sudo airmon-ng start wlan0
```

請將 `wlan0` 替換為 `ip link` 顯示的實際介面名稱。成功回應將顯示 `monitor mode vif enabled`，並出現如 `wlan0mon` 的新介面名稱。

### 4.5 — Kali 套件方法（最簡便）

Kali Linux 提供預先封裝的 RTL8812AU 驅動程式 DKMS 建置，與 Kali 核心保持同步。如果你使用 Kali，請使用此方法而非從 GitHub 複製：

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

此單一指令將安裝驅動程式原始碼、向 DKMS 註冊，並針對目前核心進行建置。後續的 `apt full-upgrade` 執行將自動保持標頭與驅動程式同步。

---

## 修復：MT7921U 驅動程式（AWUS036AX、AXM、AXML、AXER）

MT7921U（Wi-Fi 6E）晶片組採用完全不同的路徑。由於自 Linux 5.18 起即為**核心內建驅動程式**，無需 DKMS、無需編譯、也無需從 GitHub 複製。核心更新本不應破壞它——但韌體封裝問題有時會造成影響。

### 5.1 — 安裝韌體套件

核心模組（`mt7921u.ko`）已存在，但它需要來自使用者空間的韌體二進位檔來初始化硬體：

```bash
sudo apt install firmware-misc-nonfree
```

在 Ubuntu 上，此套件位於 `non-free` 套件庫元件中。若指令失敗，請確認 `/etc/apt/sources.list` 中已啟用非自由套件來源。

### 5.2 — 重新載入驅動程式

安裝韌體後，無需重新開機即可強制重新載入驅動程式：

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

然後檢查介面：

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — 確認核心版本

MT7921U 驅動程式需要核心 **5.18 或更新版本**。若你安裝的是早於此核心版本的 Kali 或 Ubuntu 最小映像，模組根本不存在：

```bash
uname -r
# 輸出必須為 5.18.x 或更高
```

若核心版本低於 5.18，請升級核心（步驟 5.4）。

### 5.4 — 升級核心

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
請使用 `full-upgrade` 而非 `upgrade`。`upgrade` 子指令會擱置需要移除其他套件的套件更新——這通常意味著核心套件本身被保留不更新。`full-upgrade` 允許進行必要的相依性解析。
{{< /alert >}}

### 5.5 — 重新開機後驗證

重新開機進入新核心後，確認一切正常運作：

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

健康的 `dmesg` 輸出將顯示韌體成功載入，以及 USB 裝置被註冊為網路介面。

---

## 讓驅動程式在未來更新後保持正常

預防比修復簡單。以下做法可防止核心更新再次破壞你的網路卡。

**在 Kali rolling 上始終使用 `full-upgrade`：**

```bash
sudo apt update && sudo apt full-upgrade
```

`full-upgrade` 指令確保當安裝新核心套件時，匹配的 `linux-headers` 套件在*同一次交易*中安裝。DKMS 掛鉤在套件安裝期間觸發——若標頭在核心之後才透過另一次 `apt` 執行到達，DKMS 就會錯過建置。

**安裝 DKMS 元套件：**

```bash
sudo apt install dkms linux-headers-generic
```

這將 `linux-headers-generic` 作為 DKMS 套件的相依性引入，使標頭始終與核心保持同步更新。

**Ubuntu HWE 核心堆疊：**

在 Ubuntu LTS 上，硬體啟用核心堆疊比 GA 核心接收更頻繁的更新和更好的硬體支援。安裝一次後，更新將自動處理：

```bash
sudo apt install linux-generic-hwe-24.04
```

**驗證 DKMS 自動安裝已啟用：**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

若此行被注解或設為 `no`，DKMS 將不會自動重建模組。請在 `/etc/dkms/framework.conf` 中取消注解或設為 `yes`。

---

## 網路卡特定問題排除表格

| 症狀 | 可能晶片組 | 根本原因 | 快速修復 |
|---|---|---|---|
| 重新開機後介面消失 | RTL8812AU | DKMS 建置失敗 | `sudo dkms autoinstall` |
| 介面消失，`dmesg` 顯示韌體錯誤 | MT7921AU | 缺少韌體套件 | `sudo apt install firmware-misc-nonfree` |
| 介面出現但 30 秒後消失 | RTL8812AU | 模組版本不符 | `sudo dkms remove --all && sudo make dkms_install` |
| 監聽模式失敗，顯示 `SIOCSIFFLAGS` | RTL8812AU | 驅動程式分支錯誤 | 複製 `aircrack-ng/rtl8812au` 並重新安裝 |
| `iwconfig` 顯示無無線擴充功能 | 任何 | 模組未載入 | `sudo modprobe 88XXau` 或 `sudo modprobe mt7921u` |
| 介面存在但找不到任何網路 | MT7921AU | 核心 < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` 顯示 `broken` | RTL8812AU | 原始碼/標頭不符 | `sudo apt install linux-headers-$(uname -r)` 後重建 |
| 發射功率限制在 20 dBm | RTL8812AU | 法規網域鎖定 | `sudo iw reg set US`（依你的地區調整） |

---

## 若一切都無效：全新安裝方法

當多次重建嘗試均失敗，且 `dkms status` 顯示來自多次部分安裝的混亂輸出時，從頭開始比除錯更快：

```bash
# 若已安裝 Kali 套件，請先移除
sudo apt purge realtek-rtl88xxau-dkms

# 移除所有 rtl8812au 的 DKMS 條目
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# 移除殘留的原始碼目錄（若存在）
sudo rm -rf /usr/src/rtl8812au*

# 清除任何過期的模組快取
sudo depmod -a

# 全新複製並安裝
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
移除 DKMS 條目的迴圈若找不到任何版本將靜默失敗——這是正常的。重要步驟是 `sudo rm -rf /usr/src/rtl8812au*`，它能移除任何可能處於損毀狀態的原始碼樹。
{{< /alert >}}

---

## 預防清單

在每次系統更新前使用此清單，避免在執行任務時出現意外：

**在 `apt upgrade` 之前：**

```bash
# 確認哪些核心套件正在等待更新
apt list --upgradable 2>/dev/null | grep linux-image
```

若有新核心即將到來，請在任何正式作業前安排測試重新開機。

**每次升級並重新開機後：**

```bash
# 確認網路卡已恢復
ip link show | grep -E "wlan|wlp"

# 確認監聽模式仍然正常
sudo airmon-ng check
```

**保留備用方案：**
- 準備一個裝有 Kali Live 映像的 USB 隨身碟（或備用網路卡使用已知正常運作的驅動程式）。在預約好的測試期間發生連線問題代價高昂——一個實體備用方案只需幾分鐘即可準備好，關鍵時刻能救你一命。

**在 Kali 上鎖定關鍵驅動程式套件：**

```bash
# 防止特定驅動程式套件在升級期間被自動移除
sudo apt-mark hold realtek-rtl88xxau-dkms
```

在明確升級驅動程式之前，先解除鎖定：

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## 總結

ALFA 驅動程式在核心更新後的失效問題遵循可預測的模式，也有可預測的解決方案。RTL8812AU 網路卡需要 `dkms autoinstall`（或從 `aircrack-ng/rtl8812au` 全新複製）加上匹配的核心標頭。MT7921U 網路卡需要 `firmware-misc-nonfree` 以及 5.18 或更新的核心。兩種情況的長期修復方案，都是確保以 `apt full-upgrade` 而非 `apt upgrade` 作為標準更新指令，讓標頭與核心保持同步。

---

**相關指南：**
- [如何在 Kali Linux 與 Ubuntu 上安裝 ALFA USB WiFi 驅動程式](/zh-tw/blog/install-alfa-driver-kali-ubuntu/) — 若你從未安裝過驅動程式，請從這裡開始
- [AWUS036ACH Kali Linux 設定指南](/zh-tw/blog/awus036ach-kali-linux-setup/) — 完整設定說明，包含監聽模式與封包注入驗證
