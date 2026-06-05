---
title: "ALFA AWUS036ACH — AC1200 Dual-Band High-Power USB-C Wireless Adapter"
description: "ALFA AWUS036ACH, Realtek RTL8812AU, AC1200 dual-band, USB-C, dual 5 dBi detachable antennas. Gold standard for Kali Linux penetration testing with Monitor Mode and Packet Injection."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC1200", "USB-C", "Dual Antenna", "Monitor Mode", "Kali Linux", "Security Research"]
---

{{< alert "warning" >}}
**Legal Disclaimer**: Monitor Mode and Packet Injection features are for authorized security testing, educational research, and legal penetration testing only. Ensure you have explicit authorization for the target network.
{{< /alert >}}

## Product Overview

The AWUS036ACH is Alfa Network's most iconic security research adapter — the gold standard for Kali Linux penetration testing since 2017. Powered by the battle-tested Realtek RTL8812AU chipset, it delivers rock-solid monitor mode and packet injection support, a built-in power amplifier for long-range reception, and two detachable 5 dBi antennas. It was the world's first WiFi 5 adapter with a USB Type-C connector.

> **macOS Notice:** All ALFA adapters have limited/no macOS support. macOS 11 Big Sur and later, and Apple Silicon (M1/M2/M3) are **NOT** supported. Maximum macOS support is 10.15 Catalina on Intel Macs.

## Key Features

- Realtek RTL8812AU — most widely tested chipset for WiFi security research
- WiFi 5 AC1200 dual-band: 5 GHz 867 Mbps + 2.4 GHz 300 Mbps
- Built-in power amplifier — up to 3× the range of typical laptop cards
- 2× RP-SMA female with 2× 5 dBi detachable dual-band antennas (upgradeable)
- World's first WiFi 5 USB-C adapter
- Screen clip mount included
- Kali Linux support since 2017.1

## Technical Specifications

| Parameter | Value |
|------|------|
| Chipset | Realtek RTL8812AU |
| WiFi Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequency Bands | Dual-band 2.4 GHz / 5 GHz |
| Max Data Rate | 802.11n: 300 Mbps · 802.11ac: 867 Mbps |
| Combined Max Speed | AC1200 (867 + 300 Mbps) |
| Antenna Connectors | 2× RP-SMA female |
| Included Antennas | 2× dual-band dipole omni, 5 dBi |
| USB Interface | Type-C SuperSpeed (5 Gbps); USB 2.0 backward compatible |
| Power Amplifier | Yes — extended range |
| Wireless Security | WPA3 / WPA2 / WPA / WEP / WPS / 802.1X |
| Country of Origin | Taiwan |

## OS Support

| OS | Status | Notes |
|------|---------|------|
| Windows 10/11 | ✅ Supported | Download driver from Alfa website; WPA3 supported |
| macOS 10.15 Catalina | ⚠️ Limited | Manual install; macOS 11+ and Apple Silicon NOT supported |
| Ubuntu | ✅ Supported | Manual RTL8812AU DKMS install; in-kernel on kernel ≥ 6.14 |
| Kali Linux | ✅ Excellent | Since Kali 2017.1; full monitor mode + packet injection; use aircrack-ng driver |
| NetHunter (Android) | ✅ Supported | OTG USB; widely confirmed working |

## Hardware Support

| Hardware | Status | Notes |
|------|---------|------|
| Raspberry Pi 3B+/4/5 | ✅ Supported | Manual driver via morrownr DKMS script |
| Desktop/Laptop PC | ✅ Supported | USB-C or USB-A via included cable |
| Mac (Intel) | ⚠️ Limited | macOS 10.15 Catalina maximum |

## Advanced Capabilities

| Feature | Status |
|------|------|
| Monitor Mode | ✅ Excellent (gold standard — community-proven since 2017) |
| Packet Injection | ✅ Excellent |
| Soft AP Mode | ✅ Yes |
| Bluetooth | ❌ No |
| VIF | ⚠️ Limited |

## What's in the Box

- 1× AWUS036ACH adapter
- 2× Detachable 5 dBi dual-band dipole antennas
- 1× USB-C to USB-A cable
- 1× Screen clip mount

## Resources & Links

| Resource | Link |
|------|------|
| Official Product Page | https://www.alfa.com.tw/products/awus036ach_1 |
| Official Documentation | https://docs.alfa.com.tw/Product/AWUS036ACH/ |
| Driver (aircrack-ng, best for Kali) | https://github.com/aircrack-ng/rtl8812au |
| Driver (morrownr, general Linux) | https://github.com/morrownr/8812au-20210708 |

## Product Datasheet

| Document | Download |
|------|------|
| Official Datasheet (PDF) | [📄 Download AWUS036ACH Datasheet](/docs/alfa/AWUS036ACH_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/alfa/awus036ach_image_1.png" alt="ALFA AWUS036ACH" />
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
