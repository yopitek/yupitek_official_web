---
title: "SDRLab Flipper Zero 5G Add-On Board — Dual-Band Wi-Fi Security Research Module"
seo_title: "Flipper Zero 5G Add-On Board | SDRLab Taiwan | Yopitek"
description: "SDRLab Flipper Zero 5G add-on board: ESP32-C5 dual-band 2.4/5 GHz Wi-Fi, 433 MHz module, active GPS, 2.8-inch TFT. Available in Taiwan from Yopitek."
date: 2026-03-12
draft: false
featureimage: "/images/products/sdrlab/flipper-5g.png"
hideFeatureImage: true
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
faq:
  - question: "Which chip and Wi-Fi bands does the SDRLab Flipper Zero 5G board use?"
    answer: "It uses an Espressif ESP32-C5 with dual-band 2.4 GHz and 5 GHz Wi-Fi. The ESP32 Marauder 5G firmware comes pre-flashed from the factory."
  - question: "Which antennas are included with the Flipper Zero 5G board?"
    answer: "Four antennas are included: 2.4G, 2.4G/5G dual-band, 433M and GPS, each on its own SMA connector. Wi-Fi antennas are 3 dBi (11 cm), the 433M antenna is 3 dBi and the GPS antenna is 20 dBi."
  - question: "What settings are required after connecting the board to a Flipper Zero?"
    answer: "Set the GPS Pin to 13 or 14 and the ESP32 Pin to 15, 16 in the GPIO pin settings, and set the Sub-GHz module to External. GPS and ESP32 use different UART pins and cannot share the same group."
  - question: "Does the board include a Flipper Zero, and which firmware works?"
    answer: "No, the Flipper Zero host is sold separately. The board is compatible with custom firmware such as Momentum, Unleashed and Xtreme, and is intended for authorized security research only."
---

# SDRLab Flipper Zero 5G Expansion Board — Dual-Band Wi-Fi Security Research Module

> **Legal Use Statement**: This expansion board is intended solely for authorized security research and legitimate study. Testing networks, devices, or infrastructure without your ownership or written authorization is illegal in most jurisdictions. Please ensure compliance with local radio frequency regulations and use this product responsibly and ethically.

---

The SDRLab Flipper Zero 5G Add-On Board is a GPIO expansion board for authorized wireless security research and education. It adds ESP32-C5 dual-band 2.4/5 GHz Wi-Fi, a 433 MHz module, active GPS and a 2.8-inch TFT, with Marauder 5G firmware pre-flashed. Contact Yopitek for a quotation in Taiwan.

## 1. What Is It

A wireless research expansion board that mounts onto the GPIO header on the back of the Flipper Zero. It upgrades your standard 2.4GHz-only Flipper with three distinct wireless capabilities in one go:

- **Dual-Band Wi-Fi 2.4GHz + 5GHz**
- **433MHz Sub-GHz** RF
- **Active GPS**

Plus, it includes a **2.8-inch color TFT screen**, an **800mAh hot-swappable battery**, **four SMA antenna interfaces with four antennas included**, and comes with the **ESP32 Marauder 5G firmware pre-flashed** from the factory.

No need to buy a programmer or compile firmware yourself. Plug it in, set three parameters, and you’re ready to go.

---

## 2. Product Features

### Three Wireless Capabilities in One
- **Dual-Band Wi-Fi 2.4GHz + 5GHz** — Scan modern 5GHz networks, overcoming the limitation of older boards that only support 2.4GHz.
- **433MHz Sub-GHz (A07 RF Module, 10 dBm)** — Provides an alternative for environments where the Flipper’s built-in receiver performs poorly.
- **Active GPS** — Automatically adds coordinates to wardriving logs. Powered by the Flipper when connected; switches to the internal battery when detached.

### 2.8-Inch Color TFT Screen
Scan results, signal strength, and battery level are displayed directly on the board, eliminating the need to stare at a computer terminal. Includes the built-in Marauder UI.

### Four SMA Antenna Interfaces, Four Antennas Included
The back cover is silkscreened to clearly indicate the mapping for each interface:

| Silkscreen | Location | Purpose |
|---|---|---|
| `433M A` | Top Left | 433MHz RF (A07 Module, 10 dBm) |
| `GPS` | Top Right | Active GPS Antenna |
| `2.4G` | Left Wing | Wi-Fi 2.4GHz |
| `2.4G/5G` | Right Wing | Wi-Fi Dual-Band 2.4GHz + 5GHz |

All four interfaces use independent screw-lock SMA female connectors. **Four antennas are included with the order**: Wi-Fi antennas 3 dBi (11 cm), 433M antenna 3 dBi, GPS antenna 20 dBi.

### 800mAh Hot-Swappable Battery
Comes with a built-in 800mAh Li-Po battery. You can detach it from the Flipper to boot standalone and capture packets, then reattach it to the host as an expansion board after scanning.

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
| **Main Chip** | **Espressif ESP32-C5** |
| **Wi-Fi Band** | Dual-Band 2.4GHz + 5GHz |
| **Wi-Fi Antenna Interface** | **4 SMA Female Connectors**: 433M A / GPS / 2.4G / 2.4G+5G. **Four antennas included**: Wi-Fi 3 dBi (11 cm), 433M 3 dBi, GPS 20 dBi |
| **Sub-GHz** | 433MHz A07 RF Module, **10 dBm** output |
| **GNSS** | Active GPS Module, **Automatic Power Switching** (Powered by host when connected, internal battery when detached) |
| **Screen** | **2.8-inch Color TFT**, Built-in Marauder UI |
| **Battery** | **800 mAh Li-Po**, Hot-swappable |
| **Connection Interface** | Flipper Zero Standard GPIO Header (**2×8 pins**), Gold fingers + TVS protection per pin |
| **Pre-loaded Firmware** | **ESP32 Marauder 5G** (Open Source, pre-flashed at factory) |
| **Firmware Compatibility** | Momentum, Unleashed, Xtreme |

### Included Accessories
- 1x Main Unit (Pre-assembled, includes case and 2.8-inch screen)
- 4x Antennas — 1x `2.4G`, 1x `2.4G+5G` Dual-Band, 1x `433M A`, 1x `GPS` (Wi-Fi 3 dBi / 433M 3 dBi / GPS 20 dBi)
- Flipper GPIO Header Connection

### Sold Separately
- **Flipper Zero Host** (This board is an expansion module; host not included)

---

## 4. Getting Started: Three Required Settings

The board comes with firmware pre-flashed, so no programming is needed. After connecting to the Flipper, you only need to configure three pin settings:

| Function | Configuration Path | Value |
|---|---|---|
| **GPS** | Momentum → Protocol Settings → GPIO Pin Settings → **GPS Pin** | **13 or 14** |
| **ESP32 (WiFi / Marauder)** | Same as above → **ESP32 Pin** | **15, 16** |
| **433MHz Sub-GHz** | Flipper → Sub-GHz → Advanced Settings → **Module** | **External** |

> ⚠️ **GPS and ESP32 use two different UART pin sets and cannot be set to the same group.** Doing so will cause both GPS and Wi-Fi to become unresponsive.

After completing the settings, restart the Flipper. You will see the corresponding WiFi Marauder and GPS applications under `Apps → GPIO`.

---

## 5. Application Scenarios

- **Dual-Band Wi-Fi Scanning** — Passive enumeration of 2.4GHz and 5GHz networks; captures SSID, BSSID, Channel, RSSI, Encryption Type, and connected clients.
- **WPA Handshake Capture** — Sniffs EAPOL/PMKID handshake packets for security audits on authorized networks.
- **Deauth Testing** — Sends Deauth packets to test network resilience. Restricted to owned or authorized networks only.
- **Wardrive Network Topology Mapping** — GPS-tagged Wi-Fi and device records exported as CSV for further analysis.
- **433MHz RF Research** — Operated via the Flipper’s Sub-GHz menu; suitable for environments where the Flipper’s built-in receiver performs poorly.
- **Evil Portal Drills** — Prototype testing of landing pages in authorized environments.
- **IoT Wireless Protocol Research** — Analyze IoT device behavior across dual bands in controlled lab environments.

---

## 6. Known Limitations (Please Note Carefully)

- **5GHz Deauth Stability Depends on Firmware Version**. Open-source Marauder firmware support for 5GHz deauth on the ESP32-C5 is still under continuous improvement. It is recommended to perform deauth tests primarily on **2.4GHz**. For 5GHz, use scanning, signal monitoring, and wardriving logging as primary functions. Actual performance depends on the current firmware version.
- **GPS Antenna is Directional**, despite being marketed as omnidirectional. Position the antenna facing the open sky for optimal positioning. The first cold start requires several minutes to download satellite ephemeris data. Performance indoors is poor; outdoor or near-window usage is recommended.
- **GPS Reports Time in UTC+0**. There is no timezone setting option in the firmware menu. For Taiwan Time (UTC+8), manually add 8 hours.
- **GPS and ESP32 Use Different UART Pins** (GPS: 13 or 14; ESP32: 15, 16). They cannot be set to the same group, or both GPS and Wi-Fi will become unresponsive.
- **Firmware Flashing Port** — The USB-C port on the front-left is for firmware flashing.
- **GPS Automatic Power Switching** — Powered by the host when connected to the Flipper; switches to the internal battery when detached. A brief restart during switching is normal.

---

**Product Page Link**: https://yupitek.com/zh-tw/products/sdrlab/flipper-5g/
**Full User Manual**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/
**Manufacturer store page (OpenSourceSDRLab)**: https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754

{{< faq >}}
