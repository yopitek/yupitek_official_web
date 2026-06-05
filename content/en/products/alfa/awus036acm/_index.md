---
title: "ALFA AWUS036ACM — AC1200 Dual-Band USB 3.0 Adapter (Best Linux Plug & Play)"
description: "ALFA AWUS036ACM, MediaTek MT7612U, AC1200 dual-band USB 3.0, in-kernel Linux driver since kernel 4.19 (plug & play, zero compilation). Full monitor mode, packet injection, and VIF support. Best Alfa adapter for Raspberry Pi."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB 3.0", "Dual-Band", "Monitor Mode", "Kali Linux", "Raspberry Pi"]
---

{{< alert "warning" >}}
**Legal Disclaimer**: Monitor Mode and Packet Injection features are for authorized security testing, educational research, and legal penetration testing only. Ensure you have explicit authorization from the target network owner before use.
{{< /alert >}}

## Product Overview

The AWUS036ACM is the top recommendation for Linux users who want zero-hassle setup. Its MediaTek MT7612U chipset has been built into the Linux kernel since version 4.19 — meaning it works out of the box on Ubuntu, Kali Linux, Raspberry Pi OS, Arch Linux, and virtually any modern distribution without compiling a single line of code. It matches the AWUS036ACH in physical size and antenna configuration but uses MediaTek's rock-solid in-kernel driver. Monitor mode, packet injection, and VIF (Virtual Interface) are all fully supported.

> **macOS Notice:** All ALFA adapters have limited or no macOS support. macOS 11+ and Apple Silicon (M1/M2/M3) are **NOT supported**. The AWUS036ACM supports a maximum of macOS 10.12 Sierra — stricter than most other models.

## Key Features

- MediaTek MT7612U chipset — in-kernel Linux driver since kernel 4.19 (plug & play, no compilation needed)
- WiFi 5 (802.11ac) dual-band AC1200 — up to 867 Mbps on 5 GHz, 300 Mbps on 2.4 GHz
- 2× RP-SMA female connectors with 2× 5 dBi detachable dual-band antennas — identical physical format to AWUS036ACH
- USB 3.0 (USB-A) interface
- Full monitor mode, packet injection, and AP mode support
- VIF (Virtual Interface) support in Kali Linux
- Included USB 3.0 extension cable
- TAA compliant — suitable for US government procurement (GSA compatible)
- Works out of the box on Raspberry Pi OS — no driver installation

## Technical Specifications

| Parameter | Value |
|-----------|-------|
| Chipset | MediaTek MT7612U |
| WiFi Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequency Bands | 2.4 GHz (2.412–2.472 GHz) · 5 GHz (5.15–5.825 GHz) |
| Channel Widths | 20 / 40 / 80 MHz |
| Max Data Rate | 5 GHz: up to 867 Mbps · 2.4 GHz: up to 300 Mbps |
| Combined Max Speed | AC1200 (867 + 300 Mbps) |
| Antenna Connectors | 2× RP-SMA female |
| Included Antennas | 2× dual-band dipole, 5 dBi gain |
| USB Interface | USB 3.0 Type-A (backward compatible with USB 2.0) |
| Output Power | 802.11a: 20 dBm · 802.11b: 23 dBm · 802.11g: 23 dBm · 802.11n: 21 dBm · 802.11ac: 20 dBm |
| Receive Sensitivity | 802.11a: −92 dBm · 802.11b: −97 dBm · 802.11g: −90 dBm · 802.11n: −90 dBm |
| Wireless Security | WPA2 / WPA / WEP / WPA-PSK / 802.1X |
| LED | Yes (power + WLAN activity) |
| Accessories | USB 3.0 extension cable |
| Country of Origin | Taiwan |

## OS Support

| OS | Status | Notes |
|----|--------|-------|
| Windows XP–11 | ✅ Supported | Driver from Alfa website. Windows 10/11 recommended. |
| macOS 10.7–10.12 | ⚠️ Limited | Official support ends at macOS 10.12 Sierra. macOS 11+ and Apple Silicon NOT supported. |
| Ubuntu 19.04+ | ✅ Plug & Play | In-kernel mt76 driver (kernel ≥ 4.19). Zero driver installation on Ubuntu 20.04 LTS and later. |
| Kali Linux 2019.3+ | ✅ Plug & Play | In-kernel driver. Monitor mode confirmed. VIF (Virtual Interface) supported. AP mode on 5 GHz may require `disable_usb_sg` module parameter. |
| NetHunter (Android) | ✅ Supported | OTG USB; in-kernel driver means broader Android compatibility than RTL adapters. |

## Hardware Support

| Hardware | Status | Notes |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Excellent | Works out of the box on Raspberry Pi OS — no driver installation required. Best Alfa adapter for Pi. |
| Desktop/Laptop PC | ✅ Supported | Standard USB-A, with included extension cable. |
| Mac (Intel) | ⚠️ Limited | macOS 10.7–10.12 only. |

## Advanced Capabilities

| Feature | Status |
|---------|--------|
| Monitor Mode | ✅ Yes (in-kernel, no extra steps on modern distros) |
| Packet Injection | ✅ Yes |
| Soft AP Mode | ✅ Yes (5 GHz AP: add `disable_usb_sg` module parameter for best performance) |
| Bluetooth | ❌ No |
| VIF (Virtual Interface) | ✅ Yes (full VIF support in Kali) |

## What's in the Box

- 1× AWUS036ACM adapter
- 2× Detachable 5 dBi dual-band dipole antennas
- 1× USB 3.0 extension cable
- 1× Driver CD (Windows)

## Resources & Links

| Resource | Link |
|----------|------|
| Official Product Page | https://www.alfa.com.tw/products/awus036acm_1 |
| Official Documentation | https://docs.alfa.com.tw/Product/AWUS036ACM/ |
| Linux Driver Info (in-kernel) | mt76 driver — included in Linux kernel ≥ 4.19, no installation needed |

## Datasheet Download

| Document | Download |
|----------|----------|
| Official Datasheet (PDF) | [📄 Download AWUS036ACM Datasheet](/docs/alfa/AWUS036ACM_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036acm_image_1.png" alt="ALFA AWUS036ACM" />
{{< /gallery >}}

---

## Compatible Antenna Upgrades

All ALFA adapters feature a standard RP-SMA connector. Upgrade with an optional external antenna for greater range and gain:

| Antenna | Frequency | Gain | Type |
|---------|-----------|------|------|
| [ALFA APA-M04](/en/products/alfa/apa-m04/) | 2.4 GHz | 7 dBi | Indoor Panel |
| [ALFA APA-M25](/en/products/alfa/apa-m25/) | 2.4 / 5 GHz | 7 dBi | Dual-Band Indoor Panel |
| [ALFA APA-M25-6E](/en/products/alfa/apa-m25-6e/) | 2.4 / 5 / 6 GHz | 7 dBi | Tri-Band Indoor Panel |
| [ARS 25-57A](/en/products/alfa/ars-25-57a/) | 2.4 / 5 GHz | 2.5 / 7 dBi | Outdoor Omni |
| [ARS NT5B7](/en/products/alfa/ars-nt5b7/) | 2.4 / 5 GHz | 5 / 7 dBi | Omni |

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}
