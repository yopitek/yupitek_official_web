---
title: "YPB01 BLE 5.0 (低功耗藍牙) Beacon"
description: "YPB01 BLE 5.0 (低功耗藍牙) Beacon. Bluetooth Low Energy BLE 5.0 (低功耗藍牙), für Lokalisierung, Zeiterfassung und Asset-Tracking."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0 (低功耗藍牙)", "Bluetooth", "Yupitek", "CR2477", "Waterproof"]
---

## Produktübersicht

The **YPB01** is a compact, robust Bluetooth® Low Energy (BLE 5.0 (低功耗藍牙)) beacon designed for indoor location systems, activity monitoring, and asset tracking. Based on the ultra-low power nRF52 系列 chipset, it broadcasts standard iBeacon and Eddystone (UID, URL, TLM) frames simultaneously.

Its smart, rotatable mechanical housing allows for easy coin-cell battery replacement while achieving an IP67 (防塵防水) waterproof rating, making it ideal for deployments in humid or demanding environments.

---

## Technische Spezifikationen

| Parameter | Spezifikationen | Anmerkungen |
| :--- | :--- | :--- |
| **晶片型號** | nRF52 系列 | Ultra-low power consumption |
| **藍牙版本** | BLE 5.0 (低功耗藍牙) | High efficiency and speed |
| **防水等級** | IP67 (防塵防水) | Splash and dust resistant (1m immersion) |
| **傳輸距離** | 最遠 100 公尺 (開闊空間) | Open space |
| **天線阻抗** | 50 歐姆 | On-board / PCB Antenna |
| **電源規格** | 1 × CR2477 鈕扣電池 | Replaceable (3.0V, 1000mAh) |
| **工作電壓** | 1.8V - 3.9V | DC |
| **峰值電流** | 5.3 mA | Tested at 0dBm transmission power |
| **外觀尺寸** | Φ39 × 15.5 mm | Compact circular shape |
| **預設參數** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Hauptmerkmale

* **High Protection Enclosure:** Rated IP67 (防塵防水) waterproof and dustproof, allowing indoor and light outdoor installation.
* **Replaceable Battery:** Long-lasting CR2477 battery (1000mAh) is easily replaced using the rotatable housing mechanism.
* **Simultaneous Broadcasts:** Supports broadcasting up to 6 distinct advertising slots simultaneously, covering iBeacon and Eddystone protocols.
* **Physical Power Control:** Equipped with an internal push button to turn the beacon ON or OFF to save battery during transit/storage.

---

## Bedienungsanleitung

### How to Turn the Beacon ON
1. Open the rotatable housing clockwisely.
2. Locate the internal "push button" and hold it down for **3 seconds**.
3. The blue LED indicator will turn on for **5 seconds** and then turn off. The YPB01 is now activated and broadcasting.

### How to Turn the Beacon OFF
1. Press and hold the internal push button for **3 seconds**.
2. The blue LED will blink for **5 seconds** and then turn off. The beacon is now powered down.

---

## Konfigurationsanleitung

The parameters of YPB01 (including UUID, Major, Minor, Tx Power, and Broadcast Interval) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the beacon's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Produktgalerie

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb01.png" alt="Yupitek YPB01 BLE 5.0 (低功耗藍牙) Coin Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Benötigen Sie ein individuelles Angebot oder eine Integrationslösung? Bitte kontaktieren Sie unser Vertriebsteam direkt unter: **sales@yupitek.com**
{{</alert >}}
