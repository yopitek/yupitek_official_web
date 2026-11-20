---
title: "ALFA AWUS036EACS — AC600 + Bluetooth 4.2 Nano USB Adapter"
description: "ALFA AWUS036EACS, Realtek RTL8821CU, AC600 dual-band, USB 2.0 Nano form factor, Bluetooth 4.2. Mainline rtw88_8821cu driver since kernel 6.2; GX10 tests passed monitor mode and injection on both bands."
date: 2026-03-12
lastmod: 2026-11-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "Nano", "Bluetooth 4.2", "Windows", "Home"]
---

## Product Overview

The AWUS036EACS is Alfa's ultra-compact WiFi + Bluetooth combination adapter, designed for home and office users who want both wireless connectivity in a single discreet USB dongle. Built around the Realtek RTL8821CU chipset, it integrates AC600 dual-band WiFi and Bluetooth 4.2 in a nano form factor with built-in driver support on Windows. Its Soft AP mode lets you share your internet connection. On Linux, the mainline rtw88_8821cu driver has been included since kernel 6.2. In GX10 testing (Ubuntu 24.04, kernel 6.17), monitor mode and packet injection both reached 100% on 2.4 GHz and 5 GHz, an end-to-end WPA handshake capture succeeded, and Bluetooth and Wi-Fi worked at the same time.

> ⚠️ **Note:** AWUS036EACS is designed for Windows home use, but it also works on Linux with the mainline rtw88_8821cu driver (kernel 6.2+). No RP-SMA port — antenna is non-upgradeable.

## Product Features

- 802.11ac AC600 dual-band WiFi + Bluetooth 4.2 in a single nano USB adapter
- Plug-and-play on Windows — built-in driver installs automatically
- Soft AP mode — create a WiFi hotspot directly from the adapter
- Ultra-compact and portable — disappears into any USB port
- Dual-band: 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps)
- Integrated 2 dBi antenna — no external RP-SMA connector
- Ideal for desktops, embedded systems, or home PCs needing WiFi + BT in minimal space
- Bluetooth 4.2 supports audio streaming, keyboards, mice, and other peripherals

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| Chipset | Realtek RTL8821CU |
| WiFi Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Bluetooth | BT 4.2 (2.4 GHz) |
| Frequency Bands | WiFi: 2.4 GHz · 5 GHz · BT: 2.4 GHz |
| Max Data Rate | 802.11b: 11 Mbps · 802.11g: 54 Mbps · 802.11n: 150 Mbps · 802.11ac: 433 Mbps |
| Combined Max Speed | AC600 (150 + 433 Mbps) |
| Antenna | Integrated, 2 dBi (non-removable, no RP-SMA) |
| USB Interface | USB 2.0 |
| Output Power | 17 dBm typical |
| Receive Sensitivity | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| Wireless Security | WEP / WPA-PSK / WPA2-PSK / 802.1X |
| Operating Temperature | −10°C to 60°C |
| Form Factor | Nano / low-profile |
| Country of Origin | Taiwan |

## OS Compatibility

| OS | Status | Notes |
|----|--------|-------|
| Windows XP–10 | ✅ Supported | Built-in driver; plug and play. Check Alfa driver page for Windows 11 compatibility. |
| macOS | ⚠️ Limited | Exact version range TBC. No Apple Silicon support. |
| Ubuntu / Linux | ✅ Kernel 6.2+ | Mainline rtw88_8821cu driver, no installation needed (tested on GX10, Ubuntu 24.04, kernel 6.17). |
| Kali Linux | ✅ Supported | Monitor mode and packet injection verified on GX10 (Ubuntu 24.04, kernel 6.17): 100% on both bands, end-to-end WPA handshake capture succeeded. Not tested on a real Kali install. |
| NetHunter (Android) | ❌ Not recommended | RTL8821CU not confirmed working with NetHunter. |

## Hardware Support

| Hardware | Status | Notes |
|----------|--------|-------|
| Raspberry Pi | ⚠️ Not tested | Not tested by us; kernel 6.2+ includes the mainline rtw88_8821cu driver. |
| Desktop / Laptop PC | ✅ Supported | Windows only recommended. |
| Embedded / IoT (Windows) | ⚠️ Windows only | Compact design suits embedded Windows systems. |

## Advanced Capabilities

| Feature | Status |
|---------|--------|
| Monitor Mode | ✅ Yes (GX10 test: 100% on both bands) |
| Packet Injection | ✅ Yes (GX10 test: 100% on both bands) |
| Soft AP Mode | ✅ Yes |
| Bluetooth | ✅ BT 4.2 (usable at the same time as Wi-Fi) |
| VIF | 🟡 Partial (passive monitor + managed on the same channel; no independent dual VIF) |

## What's in the Box

- 1× AWUS036EACS nano adapter

## Resources & Links

| Resource | Link |
|----------|------|
| Official Product Page | https://www.alfa.com.tw/products/awus036eacs_1 |
| Official Documentation | https://docs.alfa.com.tw/Product/AWUS036EACS/ |

## Datasheet Download

Official datasheet coming soon.

{{< gallery >}}
  <img src="/images/products/alfa/awus036eacs_image_1.png" alt="ALFA AWUS036EACS" />
{{< /gallery >}}

---

## Compatible Antenna Upgrades

All ALFA adapters feature a standard RP-SMA connector. Upgrade with an optional external antenna for greater range and gain:

| Antenna | Frequency | Gain | Type |
|---------|-----------|------|------|
| [ALFA APA-M04](/en/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | Indoor Panel |
| [ALFA APA-M25](/en/products/alfa/apa-m25/) | 2.4 / 5 GHz | 8 / 10 dBi | Dual-Band Indoor Panel |
| [ALFA APA-M25-6E](/en/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 8 / 10 / 9 dBi | Tri-Band Indoor Panel |
| [ARS 25-57A](/en/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 5 / 7 dBi | Outdoor Omni |
| [ARS NT5B7](/en/products/alfa/ars-nt5b7/) | 2.4 / 5 / 6 GHz | 4 / 5 / 7 dBi | Omni |

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}
