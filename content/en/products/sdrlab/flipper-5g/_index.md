---
title: "SDRLab Flipper Zero 5G Add-On Board — Dual-Band Wi-Fi Security Research Module"
description: "Flipper Zero 5G add-on board, RTL8720DN dual-band (2.4+5GHz) Wi-Fi, BLE 5.0, pre-flashed Deauth firmware, GPIO-powered, compatible with Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

# SDRLab Flipper Zero 5G Expansion Board — Dual-Band Wi-Fi Security Research Module

> **Legal Use Statement**: This expansion board is intended solely for authorized security research and legitimate study. Testing networks, devices, or infrastructure without your ownership or written authorization is illegal in most jurisdictions. Please ensure compliance with local radio frequency regulations and use this product responsibly and ethically.

---

## 1. What Is It

A wireless research expansion board that mounts onto the GPIO header on the back of the Flipper Zero. It upgrades your standard 2.4GHz-only Flipper with four distinct wireless capabilities in one go:

- **Dual-Band Wi-Fi 2.4GHz + 5GHz** (802.11 b/g/n/ax, Wi-Fi 6)
- **Bluetooth BLE 5.0**
- **433MHz Sub-GHz** RF
- **Active GPS**

Plus, it includes a **2.8-inch color TFT screen**, an **800mAh hot-swappable battery**, **microSD logging**, **four SMA antenna interfaces with four antennas included**, and comes with the **ESP32 Marauder 5G firmware pre-flashed** from the factory.

No need to buy a programmer or compile firmware yourself. Plug it in, set three parameters, and you’re ready to go.

---

## 2. Product Features

### Four Wireless Capabilities in One
- **Dual-Band Wi-Fi 2.4GHz + 5GHz** — Scan modern 5GHz networks, overcoming the limitation of older boards that only support 2.4GHz.
- **433MHz Sub-GHz (A07 RF Module, 10 dBm)** — Provides an alternative for environments where the Flipper’s built-in receiver performs poorly.
- **Active GPS** — Automatically adds coordinates to wardriving logs. Powered by the Flipper when connected; switches to the internal battery when detached.
- **Bluetooth BLE 5.0** — BLE device enumeration and beacon analysis, which can run simultaneously with Wi-Fi research.

### 2.8-Inch Color TFT Screen
Scan results, signal strength, battery level, and microSD usage are displayed directly on the board, eliminating the need to stare at a computer terminal. Includes the built-in Marauder UI.

### Four SMA Antenna Interfaces, Four Antennas Included
The back cover is silkscreened to clearly indicate the mapping for each interface:

| Silkscreen | Location | Purpose |
|---|---|---|
| `433M A` | Top Left | 433MHz RF (A07 Module, 10 dBm) |
| `GPS` | Top Right | Active GPS Antenna |
| `2.4G` | Left Wing | Wi-Fi 2.4GHz |
| `2.4G/5G` | Right Wing | Wi-Fi Dual-Band 2.4GHz + 5GHz |

All four interfaces use independent screw-lock SMA female connectors. **Four antennas are included with the order, each with a gain of 5dBi.**

### 800mAh Hot-Swappable Battery
Comes with a built-in 800mAh Li-Po battery. You can detach it from the Flipper to boot standalone and capture packets, then reattach it to the host as an expansion board after scanning. Charges via USB-C, taking approximately 2 hours to fully charge.

### microSD Logging for Post-Analysis
Supports **microSD cards formatted to FAT32, up to 32GB**. Captured packets are saved as `.pcap` files, which can be opened directly in Wireshark for analysis. Wardriving routes are exported separately as `wardrive_*.csv`.

### Pre-Flashed Marauder 5G Firmware
Ready to use out of the box; no separate programmer required. The board retains a USB-C programming port for advanced users who wish to upgrade the firmware manually.

### Gold Fingers + TVS Surge Protection
All signal pins are gold-plated, and each pin includes an internal TVS (Transient Voltage Suppression) diode to provide surge protection during plug/unplug operations with the Flipper.

### Firmware Ecosystem Compatibility
Compatible with custom firmwares such as Momentum, Unleashed, and Xtreme that include WiFi Marauder and GPS applications.

---

## 3. Product Specifications

| Specification | Value / Description |
|---|---|
| **Main Chip** | **Espressif ESP32-C5** (RISC-V) |
| **CPU** | RISC-V high-performance core, up to 240 MHz, plus a low-power (LP) core for background tasks |
| **Wi-Fi Standard** | **IEEE 802.11 b/g/n/ax** (Wi-Fi 6), Dual-Band 2.4GHz + 5GHz |
| **Wi-Fi Antenna Interface** | **4 SMA Female Connectors**: 433M A / GPS / 2.4G / 2.4G+5G. **Four antennas included, all 5dBi** |
| **Bluetooth** | **BLE 5.0** (⚠️ Does not support Bluetooth Classic / BR-EDR) |
| **Sub-GHz** | 433MHz A07 RF Module, **10 dBm** output |
| **GNSS** | Active GPS Module, **Automatic Power Switching** (Powered by host when connected, internal battery when detached) |
| **Screen** | **2.8-inch Color TFT**, Built-in Marauder UI |
| **Battery** | **800 mAh Li-Po**, Hot-swappable |
| **Charging** | USB-C, 5V / 2A, approx. **2 hours** to full charge (Front Top) |
| **Power Output to Flipper** | 5V / 2.4A |
| **Storage** | **microSD, FAT32 format, up to 32GB** (exFAT / NTFS not supported) |
| **Connection Interface** | Flipper Zero Standard GPIO Header (**2×8 pins**), Gold fingers + TVS protection per pin |
| **Pre-loaded Firmware** | **ESP32 Marauder 5G** (Open Source, pre-flashed at factory) |
| **Firmware Compatibility** | Momentum, Unleashed, Xtreme |
| **Case Material** | 3D Printed Plastic |
| **Available Colors** | Black / White / Clear / Red / Blue |
| **Dimensions** | **90 × 58 × 15 mm** (excluding antennas) |

### Included Accessories
- 1x Main Unit (Pre-assembled, includes 3D printed case and 2.8-inch screen)
- 4x Antennas (All 5dBi) — 1x `2.4G`, 1x `2.4G+5G` Dual-Band, 1x `433M A`, 1x `GPS`
- Flipper GPIO Header Connection

### Sold Separately
- **Flipper Zero Host** (This board is an expansion module; host not included)
- **microSD Card** (FAT32, up to 32GB)

---

## 4. Getting Started: Three Required Settings

The board comes with firmware pre-flashed, so no programming is needed. After connecting to the Flipper, you only need to configure three pin settings:

| Function | Configuration Path | Value |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 or 14** |
| **ESP32 (WiFi / BLE / Marauder)** | Same as above → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS and ESP32 use two different UART pin sets and cannot be set to the same group.** Doing so will cause both GPS and Wi-Fi to become unresponsive.

After completing the settings, restart the Flipper. You will see the corresponding WiFi Marauder and GPS applications under `Apps → GPIO`.

**microSD must be manually formatted to FAT32**, and you must confirm that PCAP storage is enabled in `Device → Settings`.

---

## 5. Application Scenarios

- **Dual-Band Wi-Fi Scanning** — Passive enumeration of 2.4GHz and 5GHz networks; captures SSID, BSSID, Channel, RSSI, Encryption Type, and connected clients.
- **WPA Handshake Capture** — Sniffs EAPOL/PMKID handshake packets for security audits on authorized networks.
- **Deauth Testing** — Sends Deauth packets to test network resilience. Restricted to owned or authorized networks only.
- **BLE Device Enumeration** — Scans and identifies nearby BLE 5.0 peripheral devices; can run synchronously with Wi-Fi research.
- **Wardrive Network Topology Mapping** — GPS-tagged Wi-Fi and device records exported as CSV for further analysis.
- **433MHz RF Research** — Operated via the Flipper’s Sub-GHz menu; suitable for environments where the Flipper’s built-in receiver performs poorly.
- **Evil Portal Drills** — Prototype testing of landing pages in authorized environments.
- **IoT Wireless Protocol Research** — Analyze IoT device behavior across dual bands in controlled lab environments.

---

## 6. Known Limitations (Please Note Carefully)

- **5GHz Deauth Stability Depends on Firmware Version**. Open-source Marauder firmware support for 5GHz deauth on the ESP32-C5 is still under continuous improvement. It is recommended to perform deauth tests primarily on **2.4GHz**. For 5GHz, use scanning, signal monitoring, and wardriving logging as primary functions. Actual performance depends on the current firmware version.
- **GPS Antenna is Directional**, despite being marketed as omnidirectional. Position the antenna facing the open sky for optimal positioning. The first cold start requires several minutes to download satellite ephemeris data. Performance indoors is poor; outdoor or near-window usage is recommended.
- **GPS Reports Time in UTC+0**. There is no timezone setting option in the firmware menu. For Taiwan Time (UTC+8), manually add 8 hours.
- **microSD Supports FAT32 Only**. Does not support exFAT or NTFS, and capacity is limited to 32GB.
- **GPS and ESP32 Use Different UART Pins** (GPS: 13 or 14; ESP32: 15, 16). They cannot be set to the same group, or both GPS and Wi-Fi will become unresponsive.
- **Bluetooth Supports BLE 5.0 Only**. The ESP32-C5 hardware lacks Bluetooth Classic (BR/EDR), so it cannot pair with traditional Bluetooth speakers, headphones, or car stereos.
- **Two USB-C Ports Have Different Functions** — The front-top port is for charging (5V/2A); the front-left port is for firmware flashing only and does not charge. Plugging into the wrong port will not charge the device, but it will not damage the host.
- **GPS Automatic Power Switching** — Powered by the host when connected to the Flipper; switches to the internal battery when detached. A brief restart during switching is normal.

---

## 7. Specifications Pending Confirmation

The following items currently lack sufficient reliable written confirmation from the manufacturer. Specific numbers are omitted from this page to avoid misleading customers:

| Item | Status |
|---|---|
| Wi-Fi Transmit Power (dBm) | Confirming with Manufacturer |
| Active Operating Current (mA) | Confirming with Manufacturer |
| Operating Temperature Range | Confirming with Manufacturer |
| Battery Indicator Segments (Single or Multi-segment) | Verifying on Physical Unit |

These items will be updated once confirmed.

---

**Product Page Link**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Full User Manual**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/
