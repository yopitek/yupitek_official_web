---
title: "SDRLab Flipper Zero Плата расширения 5G — Двухдиапазонный модуль исследования безопасности Wi-Fi"
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/flipper-5g.png"
hideFeatureImage: true
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Расширение Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Исследование безопасности"]
---

# SDRLab Flipper Zero 5G Expansion Board — Dual-Band Wi-Fi Security Research Module

> **Legal Use Statement**: This expansion board is intended solely for authorized cybersecurity research and lawful study. Testing networks, devices, or infrastructure without your ownership or written authorization is illegal in most jurisdictions. Please ensure compliance with local radio frequency regulations and use this product responsibly and ethically.

---

## 1. Product Overview

A wireless research expansion board that mounts onto the GPIO header on the back of the Flipper Zero. This module expands your device’s capabilities beyond the standard 2.4GHz limitation, adding three distinct wireless functionalities:

- **Dual-Band Wi-Fi 2.4GHz + 5GHz**
- **433MHz Sub-GHz** RF
- **Active GPS**

Additionally, it features a **2.8-inch color TFT screen**, an **800mAh hot-swappable battery**, **four SMA antenna interfaces with four antennas included**, and comes with the **ESP32 Marauder 5G firmware pre-flashed**.

No flashing hardware or firmware compilation is required. Simply connect, configure three parameters, and begin usage.

---

## 2. Key Features

### Three Wireless Capabilities in One Module
- **Dual-Band Wi-Fi 2.4GHz + 5GHz** — Scans modern 5GHz networks, overcoming the limitation of older boards that only support 2.4GHz.
- **433MHz Sub-GHz (A07 RF Module, 10 dBm)** — Provides an alternative for environments where the Flipper’s built-in receiver performs poorly.
- **Active GPS** — Automatically adds coordinates to wardriving logs. Powered by the host when connected to the Flipper; switches to the internal battery when detached.

### 2.8-Inch Color TFT Screen
Displays scan results, signal strength, battery level directly on the board, eliminating the need to monitor a computer terminal. Includes the built-in Marauder UI.

### Four SMA Antenna Interfaces with Four Antennas Included
The back cover is clearly silkscreened to indicate the correspondence between interfaces:

| Silkscreen Label | Position | Function |
|---|---|---|
| `433M A` | Top Left | 433MHz RF (A07 Module, 10 dBm) |
| `GPS` | Top Right | Active GPS Antenna |
| `2.4G` | Left Wing | Wi-Fi 2.4GHz |
| `2.4G/5G` | Right Wing | Dual-Band Wi-Fi 2.4GHz + 5GHz |

All four interfaces use independent screw-lock SMA female connectors. **Four antennas are included with the product: Wi-Fi 2.4G and 2.4G+5G (3 dBi, 11 cm), 433M (3 dBi), and GPS (20 dBi).**

### 800mAh Hot-Swappable Battery
The module includes a built-in 800mAh Li-Po battery. It can operate independently to capture packets when detached from the Flipper, and can be reattached to function as an expansion board.

### Pre-Flashed Marauder 5G Firmware
Ready to use out of the box; no separate flashing hardware is required. A USB-C (TypeC) programming port is retained on the front-left of the board for advanced users to upgrade the firmware manually.

### Gold-Plated Contacts + TVS Surge Protection
All signal pins are gold-plated, and each pin includes an integrated TVS (Transient Voltage Suppression) diode to provide surge protection during connection and disconnection.

### Firmware Ecosystem Compatibility
Compatible with custom firmwares such as Momentum, Unleashed, and Xtreme, which include WiFi Marauder and GPS applications.

---

## 3. Technical Specifications

| Specification | Value / Description |
|---|---|
| **Main Chip** | **Espressif ESP32-C5** (Wi-Fi 2.4GHz + 5GHz) |
| **Wi-Fi Antenna Interface** | **4 SMA Female Connectors**: 433M A / GPS / 2.4G / 2.4G+5G. **Four antennas included**: Wi-Fi 3 dBi (11 cm), 433M 3 dBi, GPS 20 dBi |
| **Sub-GHz** | 433MHz A07 RF Module, **10 dBm** output |
| **GNSS** | Active GPS Module, **Automatic Power Switching** (Host power when connected, internal battery when detached) |
| **Screen** | **2.8-inch Color TFT**, Built-in Marauder UI |
| **Battery** | **800 mAh Li-Po**, Hot-swappable |
| **Connection Interface** | Flipper Zero Standard GPIO Header (**2x8 pins**), Gold-plated contacts + per-pin TVS protection |
| **Pre-loaded Firmware** | **ESP32 Marauder 5G** (Open Source, pre-flashed) |
| **Firmware Compatibility** | Momentum, Unleashed, Xtreme |

### Included Accessories
- 1x Main Unit (Assembled, includes 2.8-inch screen)
- 4x Antennas — 1x `2.4G` (3 dBi, 11 cm), 1x `2.4G+5G` Dual-Band (3 dBi, 11 cm), 1x `433M A` (3 dBi), 1x `GPS` (20 dBi)
- Flipper GPIO Header Connection

### Sold Separately
- **Flipper Zero Main Unit** (This board is an expansion module and does not include the main unit)

---

## 4. Getting Started: Three Required Settings

The board comes with pre-flashed firmware and requires no flashing. After connecting to the Flipper, only three pin configurations are necessary:

| Function | Configuration Path | Value |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 or 14** |
| **ESP32 (WiFi / Marauder)** | Same as above → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS and ESP32 use separate UART pins and cannot be set to the same group.** Doing so will cause both GPS and Wi-Fi to become unresponsive.

After configuration, restart the Flipper. You will see the corresponding WiFi Marauder and GPS applications under `Apps → GPIO`.

---

## 5. Application Scenarios

- **Dual-Band Wi-Fi Scanning** — Passive enumeration of 2.4GHz and 5GHz networks; captures SSID, BSSID, channel, RSSI, encryption type, and connected clients.
- **WPA Handshake Capture** — Sniffs EAPOL/PMKID handshake packets for security auditing of authorized networks.
- **Deauth Testing** — Sends Deauth packets to test network resilience. Restricted to owned or authorized networks only.
- **Wardrive Network Topology Mapping** — GPS-tagged Wi-Fi and device records exported as CSV for further analysis.
- **433MHz RF Research** — Operated via the Flipper’s Sub-GHz menu; suitable for environments where the Flipper’s built-in receiver performs poorly.
- **Evil Portal Simulation** — Prototype testing of landing pages in authorized environments.
- **IoT Wireless Protocol Research** — Analyzes IoT device behavior on dual-band frequencies in controlled lab environments.

---

## 6. Known Limitations (Please Note)

- **5GHz Deauth Stability Depends on Firmware Version**. Support for 5GHz deauth on the ESP32-C5 with open-source Marauder firmware is still under improvement. It is recommended to perform deauth tests primarily on **2.4GHz**. For 5GHz, use scanning, signal monitoring, and wardriving logging as primary functions. Actual performance depends on the current firmware version.
- **GPS Antenna is Directional**. Although marketed as omnidirectional, the antenna performs best when pointed towards an open sky for positioning. The first cold start requires several minutes to download satellite ephemeris data. Performance indoors is poor; outdoor or window-side usage is recommended.
- **GPS Reports Time in UTC+0**. There is no timezone setting in the firmware menu. For Taiwan Time (UTC+8), please manually add 8 hours.
- **GPS and ESP32 Use Separate UART Pins** (GPS: 13 or 14; ESP32: 15, 16). They cannot be configured to the same group, or both GPS and Wi-Fi will fail to respond.
- **GPS Automatic Power Switching** — Powered by the host when connected to the Flipper; switches to the internal battery when detached. A brief restart during switching is normal.

---

**Manufacturer Store Page (OpenSourceSDRLab)**: https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754
**Product Page Link**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Full User Manual**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/