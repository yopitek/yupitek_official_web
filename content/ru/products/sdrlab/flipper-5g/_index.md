---
title: "SDRLab Flipper Zero Плата расширения 5G — Двухдиапазонный модуль исследования безопасности Wi-Fi"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Расширение Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Исследование безопасности"]
---

# SDRLab Flipper Zero 5G Expansion Board — Dual-Band Wi-Fi Security Research Module

> **Legal Use Statement**: This expansion board is intended solely for authorized cybersecurity research and lawful study. Testing networks, devices, or infrastructure without your ownership or written authorization is illegal in most jurisdictions. Please ensure compliance with local radio frequency regulations and use this product responsibly and ethically.

---

## 1. Product Overview

A wireless research expansion board that mounts onto the GPIO header on the back of the Flipper Zero. This module expands your device’s capabilities beyond the standard 2.4GHz limitation, adding four distinct wireless functionalities:

- **Dual-Band Wi-Fi 2.4GHz + 5GHz** (802.11 b/g/n/ax, Wi-Fi 6)
- **Bluetooth BLE 5.0**
- **433MHz Sub-GHz** RF
- **Active GPS**

Additionally, it features a **2.8-inch color TFT screen**, an **800mAh hot-swappable battery**, **microSD logging**, **four SMA antenna interfaces with four antennas included**, and comes with the **ESP32 Marauder 5G firmware pre-flashed**.

No flashing hardware or firmware compilation is required. Simply connect, configure three parameters, and begin usage.

---

## 2. Key Features

### Four Wireless Capabilities in One Module
- **Dual-Band Wi-Fi 2.4GHz + 5GHz** — Scans modern 5GHz networks, overcoming the limitation of older boards that only support 2.4GHz.
- **433MHz Sub-GHz (A07 RF Module, 10 dBm)** — Provides an alternative for environments where the Flipper’s built-in receiver performs poorly.
- **Active GPS** — Automatically adds coordinates to wardriving logs. Powered by the host when connected to the Flipper; switches to the internal battery when detached.
- **Bluetooth BLE 5.0** — Enables BLE device enumeration and beacon analysis, which can run concurrently with Wi-Fi research.

### 2.8-Inch Color TFT Screen
Displays scan results, signal strength, battery level, and microSD usage directly on the board, eliminating the need to monitor a computer terminal. Includes the built-in Marauder UI.

### Four SMA Antenna Interfaces with Four Antennas Included
The back cover is clearly silkscreened to indicate the correspondence between interfaces:

| Silkscreen Label | Position | Function |
|---|---|---|
| `433M A` | Top Left | 433MHz RF (A07 Module, 10 dBm) |
| `GPS` | Top Right | Active GPS Antenna |
| `2.4G` | Left Wing | Wi-Fi 2.4GHz |
| `2.4G/5G` | Right Wing | Dual-Band Wi-Fi 2.4GHz + 5GHz |

All four interfaces use independent screw-lock SMA female connectors. **Four antennas are included with the product, each with a gain of 5dBi.**

### 800mAh Hot-Swappable Battery
The module includes a built-in 800mAh Li-Po battery. It can operate independently to capture packets when detached from the Flipper, and can be reattached to function as an expansion board. Charges via USB-C in approximately 2 hours.

### microSD Logging for Post-Analysis
Supports microSD cards formatted in **FAT32 with a capacity of up to 32GB**. Captured packets are saved as `.pcap` files, which can be analyzed directly in Wireshark. Wardriving routes are exported separately as `wardrive_*.csv` files.

### Pre-Flashed Marauder 5G Firmware
Ready to use out of the box; no separate flashing hardware is required. A USB-C port is retained on the board for advanced users to upgrade the firmware manually.

### Gold-Plated Contacts + TVS Surge Protection
All signal pins are gold-plated, and each pin includes an integrated TVS (Transient Voltage Suppression) diode to provide surge protection during connection and disconnection.

### Firmware Ecosystem Compatibility
Compatible with custom firmwares such as Momentum, Unleashed, and Xtreme, which include WiFi Marauder and GPS applications.

---

## 3. Technical Specifications

| Specification | Value / Description |
|---|---|
| **Main Chip** | **Espressif ESP32-C5** (RISC-V) |
| **CPU** | High-performance RISC-V core, up to 240 MHz, plus a Low-Power (LP) core for background tasks |
| **Wi-Fi Standard** | **IEEE 802.11 b/g/n/ax** (Wi-Fi 6), Dual-Band 2.4GHz + 5GHz |
| **Wi-Fi Antenna Interface** | **4 SMA Female Connectors**: 433M A / GPS / 2.4G / 2.4G+5G. **Four antennas included, all 5dBi** |
| **Bluetooth** | **BLE 5.0** (⚠️ Does not support Bluetooth Classic / BR-EDR) |
| **Sub-GHz** | 433MHz A07 RF Module, **10 dBm** output |
| **GNSS** | Active GPS Module, **Automatic Power Switching** (Host power when connected, internal battery when detached) |
| **Screen** | **2.8-inch Color TFT**, Built-in Marauder UI |
| **Battery** | **800 mAh Li-Po**, Hot-swappable |
| **Charging** | USB-C, 5V / 2A, approx. **2 hours** to full charge (Front Top) |
| **Power Output to Flipper** | 5V / 2.4A |
| **Storage** | **microSD, FAT32 format, up to 32GB** (exFAT/NTFS not supported) |
| **Connection Interface** | Flipper Zero Standard GPIO Header (**2x8 pins**), Gold-plated contacts + per-pin TVS protection |
| **Pre-loaded Firmware** | **ESP32 Marauder 5G** (Open Source, pre-flashed) |
| **Firmware Compatibility** | Momentum, Unleashed, Xtreme |
| **Enclosure Material** | 3D Printed Plastic |
| **Available Colors** | Black / White / Transparent / Red / Blue |
| **Dimensions** | **90 × 58 × 15 mm** (excluding antennas) |

### Included Accessories
- 1x Main Unit (Assembled, includes 3D printed enclosure and 2.8-inch screen)
- 4x Antennas (All 5dBi) — 1x `2.4G`, 1x `2.4G+5G` Dual-Band, 1x `433M A`, 1x `GPS`
- Flipper GPIO Header Connection

### Sold Separately
- **Flipper Zero Main Unit** (This board is an expansion module and does not include the main unit)
- **microSD Card** (FAT32, up to 32GB)

---

## 4. Getting Started: Three Required Settings

The board comes with pre-flashed firmware and requires no flashing. After connecting to the Flipper, only three pin configurations are necessary:

| Function | Configuration Path | Value |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 or 14** |
| **ESP32 (WiFi / BLE / Marauder)** | Same as above → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS and ESP32 use separate UART pins and cannot be set to the same group.** Doing so will cause both GPS and Wi-Fi to become unresponsive.

After configuration, restart the Flipper. You will see the corresponding WiFi Marauder and GPS applications under `Apps → GPIO`.

**microSD must be manually formatted to FAT32**, and PCAP storage must be enabled in `Device → Settings`.

---

## 5. Application Scenarios

- **Dual-Band Wi-Fi Scanning** — Passive enumeration of 2.4GHz and 5GHz networks; captures SSID, BSSID, channel, RSSI, encryption type, and connected clients.
- **WPA Handshake Capture** — Sniffs EAPOL/PMKID handshake packets for security auditing of authorized networks.
- **Deauth Testing** — Sends Deauth packets to test network resilience. Restricted to owned or authorized networks only.
- **BLE Device Enumeration** — Scans and identifies nearby BLE 5.0 peripheral devices; can run synchronously with Wi-Fi research.
- **Wardrive Network Topology Mapping** — GPS-tagged Wi-Fi and device records exported as CSV for further analysis.
- **433MHz RF Research** — Operated via the Flipper’s Sub-GHz menu; suitable for environments where the Flipper’s built-in receiver performs poorly.
- **Evil Portal Simulation** — Prototype testing of landing pages in authorized environments.
- **IoT Wireless Protocol Research** — Analyzes IoT device behavior on dual-band frequencies in controlled lab environments.

---

## 6. Known Limitations (Please Note)

- **5GHz Deauth Stability Depends on Firmware Version**. Support for 5GHz deauth on the ESP32-C5 with open-source Marauder firmware is still under improvement. It is recommended to perform deauth tests primarily on **2.4GHz**. For 5GHz, use scanning, signal monitoring, and wardriving logging as primary functions. Actual performance depends on the current firmware version.
- **GPS Antenna is Directional**. Although marketed as omnidirectional, the antenna performs best when pointed towards an open sky for positioning. The first cold start requires several minutes to download satellite ephemeris data. Performance indoors is poor; outdoor or window-side usage is recommended.
- **GPS Reports Time in UTC+0**. There is no timezone setting in the firmware menu. For Taiwan Time (UTC+8), please manually add 8 hours.
- **microSD Support is Limited to FAT32**. exFAT and NTFS are not supported, and capacity is limited to 32GB.
- **GPS and ESP32 Use Separate UART Pins** (GPS: 13 or 14; ESP32: 15, 16). They cannot be configured to the same group, or both GPS and Wi-Fi will fail to respond.
- **Bluetooth Supports BLE 5.0 Only**. The ESP32-C5 hardware lacks Bluetooth Classic (BR/EDR), so it cannot pair with traditional Bluetooth speakers, headphones, or car stereos.
- **Two USB-C Ports Have Different Functions** — The front-top port is for charging (5V/2A); the front-left port is for firmware flashing only and does not charge. Plugging into the wrong port will not charge the device but will not damage the host.
- **GPS Automatic Power Switching** — Powered by the host when connected to the Flipper; switches to the internal battery when detached. A brief restart during switching is normal.

---

## 7. Specifications Pending Confirmation

The following items currently lack sufficient reliable written confirmation from the manufacturer. Specific values are omitted from this page to avoid misleading information:

| Item | Status |
|---|---|
| Wi-Fi Transmit Power (dBm) | Confirming with Manufacturer |
| Active Current Consumption (mA) | Confirming with Manufacturer |
| Operating Temperature Range | Confirming with Manufacturer |
| Battery Indicator Segments (Single or Multi-segment) | Verifying on Physical Unit |

These items will be updated once confirmed.

---

**Product Page Link**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Full User Manual**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/