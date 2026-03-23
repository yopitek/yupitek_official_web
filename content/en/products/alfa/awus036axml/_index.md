---
title: "ALFA AWUS036AXML — Wi-Fi 6E USB-C Tri-Band USB Adapter"
description: "ALFA AWUS036AXML with MediaTek MT7921AUN chipset. Wi-Fi 6E tri-band (2.4/5/6 GHz), USB-C interface, Bluetooth 5.2, Kali Linux monitor mode supported."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 6E", "USB-C", "802.11ax", "Tri-Band", "Bluetooth 5.2", "6GHz", "Kali Linux"]
---

{{< alert "warning" >}}
**Legal Disclaimer**: Monitor Mode and Packet Injection features are for authorized security testing, educational research, and legal penetration testing only. Ensure you have explicit authorization for the target network.
{{< /alert >}}

## Product Overview

The AWUS036AXML features the MediaTek MT7921AUN chipset with Wi-Fi 6E tri-band support (2.4 GHz / 5 GHz / 6 GHz), reaching up to 3000 Mbps combined throughput, plus integrated Bluetooth 5.2. The USB-C interface comes with a 2-in-1 USB-C/USB-A cable for compatibility with modern laptops and desktops. A detachable RP-SMA antenna and screen clip mount are included.

> **macOS Notice:** All ALFA adapters have limited/no macOS support. macOS 11 Big Sur and later, and Apple Silicon (M1/M2/M3) are **NOT** supported. Maximum macOS support is 10.15 Catalina on Intel Macs.

## Key Features

- Wi-Fi 6E Tri-Band: 2.4 / 5 / 6 GHz
- MediaTek MT7921AUN chipset
- Up to 3000 Mbps combined throughput
- Bluetooth 5.2 (combo chip)
- USB-C interface (USB 3.2 Gen 1, 5 Gbps)
- Includes 2-in-1 USB-C/USB-A cable
- 1× RP-SMA detachable antenna
- Includes screen clip mount
- WPA3/WPA2/WPA/WEP/WPS
- Kali Linux Monitor Mode (kernel ≥ 5.18)

## Technical Specifications

| Item | Specification |
|------|---------------|
| Chipset | MediaTek MT7921AUN |
| WiFi Standards | IEEE 802.11 a/b/g/n/ac/ax (WiFi 6E) |
| Frequency Bands | 2.4 GHz (20/40 MHz) · 5 GHz (20/40/80 MHz) · 6 GHz (20/40/80 MHz) |
| Max Data Rate | 2.4GHz: 600 Mbps · 5GHz: 1200 Mbps · 6GHz: 1200 Mbps · Combined: 3000 Mbps |
| Bluetooth | BT 5.2 (combo chip) |
| Antenna Connector | 1× RP-SMA female (detachable) |
| USB Interface | USB 3.2 Gen 1 Type-C (5 Gbps) |
| Cable | 2-in-1 USB-C/USB-A |
| Wireless Security | WPA3 / WPA2 / WPA / WEP / WPS |
| Country of Origin | Taiwan |

## OS Support

| OS | Status | Notes |
|----|--------|-------|
| Windows 10 | ✅ Supported | 2.4 GHz and 5 GHz only; 6 GHz not available on Win10 |
| Windows 11 | ✅ Supported | Full tri-band including 6 GHz |
| macOS | ❌ Not supported | No macOS 11+ or Apple Silicon support |
| Ubuntu | ✅ Supported | In-kernel mt7921u driver, kernel ≥ 5.18 (Ubuntu 22.10+) |
| Kali Linux | ✅ Supported | Monitor mode ≥ kernel 5.18; active monitor mode ≥ 6.12; packet injection supported |
| NetHunter (Android) | ⚠️ Partial | OTG; kernel-dependent |

## Hardware Support

| Hardware | Status | Notes |
|----------|--------|-------|
| Raspberry Pi 3B+/4/5 | ✅ Supported | Updated Pi OS (kernel ≥ 5.18); may need firmware file copy |
| Desktop/Laptop PC | ✅ Supported | USB-C or USB-A via included 2-in-1 cable |
| Mac Intel | ⚠️ Limited | macOS 10.15 Catalina maximum |

## Advanced Capabilities

| Feature | Status |
|---------|--------|
| Monitor Mode | ✅ Yes (kernel ≥ 5.18; active mode ≥ 6.12) |
| Packet Injection | ✅ Yes |
| Soft AP Mode | ✅ Yes |
| Bluetooth | ✅ BT 5.2 |
| VIF | ✅ Yes |

## What's in the Box

- 1× AWUS036AXML adapter
- 1× Detachable dipole antenna
- 1× 2-in-1 USB-C/USB-A cable
- 1× Screen clip mount

## Resources & Links

| Resource | Link |
|----------|------|
| Official Product Page | https://www.alfa.com.tw/products/awus036axml |
| Official Documentation | https://docs.alfa.com.tw/ |
| Linux Driver (in-kernel) | mt7921u — built into Linux kernel ≥ 5.18 |

## Product Datasheet

| Document | Download |
|------|------|
| Official Datasheet (PDF) | [📄 Download AWUS036AXML Datasheet](/docs/alfa/AWUS036AXML_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036axml_image_1.png" alt="ALFA AWUS036AXML" />
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
Need a quote or more information? [Contact us](/en/contact/)
{{< /alert >}}
