---
title: "YPB01 BLE 5.0 Beacon"
description: "YPB01 Bluetooth Low Energy (BLE 5.0) coin-cell beacon. Features replaceable CR2477 battery, 100m range, IP67 waterproof design for indoor location and asset tracking."
date: 2026-06-04
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["ibeacon"]
tags: ["iBeacon", "BLE 5.0", "Bluetooth", "Yupitek", "CR2477", "Waterproof"]
---

## Product Overview

The **YPB01** is a compact, robust Bluetooth® Low Energy (BLE 5.0) beacon designed for indoor location systems, activity monitoring, and asset tracking. Based on the ultra-low power nRF52 series chipset, it broadcasts standard iBeacon and Eddystone (UID, URL, TLM) frames simultaneously.

Its smart, rotatable mechanical housing allows for easy coin-cell battery replacement while achieving an IP67 waterproof rating, making it ideal for deployments in humid or demanding environments.

---

## Technical Specifications

| Parameter | Specifications | Remarks |
| :--- | :--- | :--- |
| **Chip Model** | nRF52 series | Ultra-low power consumption |
| **Bluetooth Version** | BLE 5.0 | High efficiency and speed |
| **Waterproof Level** | IP67 | Splash and dust resistant (1m immersion) |
| **Transmission Range** | Up to 100 meters | Open space |
| **Antenna Impedance** | 50 ohm | On-board / PCB Antenna |
| **Power Source** | 1 × CR2477 coin battery | Replaceable (3.0V, 1000mAh) |
| **Operating Voltage** | 1.8V - 3.9V | DC |
| **Peak Current** | 5.3 mA | Tested at 0dBm transmission power |
| **Dimensions** | Φ39 × 15.5 mm | Compact circular shape |
| **Default Settings** | UUID: E2C56DB5-DFFB-48D2-B060-D0F5A71096E0<br>Radio Tx Power: 0 dBm (Level 6)<br>Adv. Interval: 900 ms | Configurable via App |

---

## Key Features

* **High Protection Enclosure:** Rated IP67 waterproof and dustproof, allowing indoor and light outdoor installation.
* **Replaceable Battery:** Long-lasting CR2477 battery (1000mAh) is easily replaced using the rotatable housing mechanism.
* **Simultaneous Broadcasts:** Supports broadcasting up to 6 distinct advertising slots simultaneously, covering iBeacon and Eddystone protocols.
* **Physical Power Control:** Equipped with an internal push button to turn the beacon ON or OFF to save battery during transit/storage.

---

## Operational Guide

### How to Turn the Beacon ON
1. Open the rotatable housing clockwisely.
2. Locate the internal "push button" and hold it down for **3 seconds**.
3. The blue LED indicator will turn on for **5 seconds** and then turn off. The YPB01 is now activated and broadcasting.

### How to Turn the Beacon OFF
1. Press and hold the internal push button for **3 seconds**.
2. The blue LED will blink for **5 seconds** and then turn off. The beacon is now powered down.

---

## Configuration Guidance

The parameters of YPB01 (including UUID, Major, Minor, Tx Power, and Broadcast Interval) are configured wirelessly via the **BeaconSET+** application:
1. Download **BeaconSET+** from Google Play or the Apple App Store.
2. Ensure your phone's Bluetooth and Location services are enabled.
3. Open the app, scan for the beacon's MAC address, and click to connect.
4. Input the secure default configuration password to unlock and edit parameters.

---

## Product Gallery

{{< gallery >}}
  <img src="/images/products/ibeacon/ypb01.png" alt="Yupitek YPB01 BLE 5.0 Coin Beacon" />
{{< /gallery >}}

---

{{< alert >}}
Need a custom quotation or integration solution? Please contact our sales team directly at: **sales@yupitek.com**
{{< /alert >}}
