---
title: "ALFA AWUS036ACS — AC600 Dual-Band USB Adapter (Budget Security Research)"
description: "ALFA AWUS036ACS, Realtek RTL8811AU, AC600 dual-band USB 2.0, 1× 2 dBi RP-SMA detachable antenna, supports Monitor Mode and Packet Injection — ideal entry-level security research adapter."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["alfa"]
tags: ["Wi-Fi 5", "AC600", "USB 2.0", "RP-SMA", "Monitor Mode", "Kali Linux", "Budget"]
---

{{< alert "warning" >}}
**Legal Disclaimer**: Monitor Mode and Packet Injection features are intended solely for authorized security testing, educational research, and lawful penetration testing. Always ensure you have explicit permission from the target network owner before use.
{{< /alert >}}

## Product Overview

The AWUS036ACS is Alfa's most affordable entry point into the dual-band 802.11ac lineup with monitor mode and packet injection support. Powered by the Realtek RTL8811AU chipset, it is compact and lightweight with a single detachable RP-SMA antenna that can be upgraded for better range. While not as powerful as the ACH or ACM, it is a practical choice for beginners in wireless security research or users who need a budget-friendly 5 GHz adapter with external antenna capability.

> **macOS Notice:** All ALFA adapters have limited macOS support. macOS 10.15 Catalina and later, and all Apple Silicon (M1/M2/M3) Macs, are **not supported**. The AWUS036ACS supports up to macOS 10.14 Mojave (Intel Mac only).

## Key Features

- Realtek RTL8811AU chipset — monitor mode and packet injection supported
- WiFi 5 (802.11ac) dual-band — 2.4 GHz (150 Mbps) + 5 GHz (433 Mbps) = AC600
- 1× RP-SMA female connector with 1× 2 dBi mini detachable antenna — upgradeable to panel or high-gain antennas
- Compact form factor — small profile for easy portability
- USB 2.0 (USB-A) interface — compatible with any USB port
- Compatible with Alfa APA-M25 dual-band panel antenna for directional reception
- Supports Kali Linux on Raspberry Pi (KaliPi) — driver installation via DKMS

## Technical Specifications

| Parameter | Value |
|---|---|
| Chipset | Realtek RTL8811AU |
| WiFi Standards | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| Frequency Bands | 2.4 GHz (150 Mbps) · 5 GHz (433 Mbps) |
| Combined Max Speed | AC600 (150 + 433 Mbps) |
| Antenna Connector | 1× RP-SMA female |
| Included Antenna | 1× dual-band dipole mini, 2 dBi gain |
| USB Interface | USB 2.0 Type-A |
| Receive Sensitivity | 802.11b: −85 dBm · 802.11g: −69 dBm · 802.11n: −68 dBm · 802.11ac: −59 dBm |
| Wireless Security | WPA2 / WPA / WEP / 802.1X |
| Country of Origin | Taiwan |

> ⚠️ **NOTE:** USB 2.0 only — maximum 480 Mbps data bus speed. Throughput capped at 433 Mbps. For maximum speed, use AWUS036ACM or AWUS036ACH with USB 3.0.

## OS Support

| OS | Status | Notes |
|---|---|---|
| Windows XP–11 | ✅ Supported | Driver available from Alfa website |
| macOS 10.5–10.14 | ⚠️ Limited | macOS 10.15+ and Apple Silicon NOT supported |
| Ubuntu | ✅ Supported | Manual DKMS driver install required (morrownr/8821au). No in-kernel support. |
| Kali Linux | ✅ Supported | Monitor mode + packet injection supported. Community driver from morrownr GitHub. |
| NetHunter (Android) | ✅ Supported | OTG USB connection; RTL8811AU has confirmed NetHunter compatibility |

## Hardware Support

| Hardware | Status | Notes |
|---|---|---|
| Raspberry Pi 3B+/4/5 | ✅ Supported | KaliPi-specific install available via morrownr DKMS. |
| Desktop/Laptop PC | ✅ Supported | Standard USB-A |
| Mac (Intel) | ⚠️ Limited | macOS 10.5–10.14 only |

## Advanced Capabilities

| Feature | Status |
|---|---|
| Monitor Mode | ✅ Yes |
| Packet Injection | ✅ Yes |
| Soft AP Mode | ✅ Yes |
| Bluetooth | ❌ No |
| VIF | ⚠️ Limited |

## What's in the Box

- 1× AWUS036ACS adapter
- 1× Detachable 2 dBi dual-band mini dipole antenna

## Resources & Links

| Resource | Link |
|---|---|
| Official Product Page | https://www.alfa.com.tw/products/awus036acs_1 |
| Official Documentation | https://docs.alfa.com.tw/Product/AWUS036ACS/ |
| Linux Driver (RTL8811AU) | https://github.com/morrownr/8821au-20210708 |

## Datasheet Download

[📄 Download AWUS036ACS Datasheet](/docs/alfa/AWUS036ACS_spec.pdf)

## Gallery

{{< gallery >}}<img src="/images/products/alfa/awus036acs_image_1.png" alt="ALFA AWUS036ACS" />{{< /gallery >}}

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
