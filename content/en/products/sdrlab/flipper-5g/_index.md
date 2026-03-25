---
title: "SDRLab Flipper Zero 5G Add-On Board — Dual-Band Wi-Fi Security Research Module"
description: "Flipper Zero 5G add-on board, RTL8720DN dual-band (2.4+5GHz) Wi-Fi, BLE 5.0, pre-flashed Deauth firmware, GPIO-powered, compatible with Momentum/Unleashed."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero Add-On", "5GHz", "Wi-Fi", "Deauth", "Security Research"]
---

{{< alert "warning" >}}
**Legal Use Notice**: This add-on board is intended solely for authorized security research and lawful testing. Ensure compliance with local wireless frequency regulations before use.
{{< /alert >}}

## Features

![SDRLab Flipper Zero 5G Add-On Board](/images/products/sdrlab/flipper-5g.png)

- **Dual-Band Coverage** — 2.4 GHz + 5 GHz (IEEE 802.11 a/b/g/n); accesses modern 5 GHz networks previously unreachable with older Flipper add-ons
- **Realtek RTL8720DN via AI Thinker BW16** — industry-standard dual-band SoC with FCC/CE pre-certified module
- **Dual-Core CPU** — ARM Cortex-M4 @ 200 MHz handles active protocols; Cortex-M0 @ 20 MHz runs low-power background tasks
- **Pre-flashed Marauder 5G Firmware** — includes scan, deauth, beacon flood, sniff (EAPOL/PMKID), and evil portal modes; plug in and go
- **BLE 5.0** — Bluetooth Low Energy device enumeration and beacon analysis alongside Wi-Fi research
- **GPIO Powered** — draws 5 V directly from Flipper Zero's GPIO header; no external power supply needed
- **Antenna Upgrade Path** — IPEX (U.FL) connector on supported revisions for attaching a high-gain external antenna
- **Firmware Ecosystem** — compatible with Momentum and Unleashed custom firmware frameworks
- **PlatformIO Development** — full custom firmware development support via Arduino-compatible Ameba D framework
- **Rugged Operating Range** — −40°C to 85°C for field use in any climate

## Specifications

| Specification | Value / Description |
|---------------|---------------------|
| Main Chip | Realtek RTL8720DN (AI Thinker BW16 module) |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi Standard | IEEE 802.11 a/b/g/n (2.4 GHz + 5 GHz dual-band) |
| Wi-Fi TX Power | ~17 dBm (subject to regional regulation) |
| Bluetooth | BLE 5.0 |
| Flash | 4 MB |
| Power Source | Flipper Zero GPIO (5 V) |
| Typical Current Draw | 150–250 mA (active scanning) |
| Connection Interface | Flipper Zero standard GPIO header (2×8 pin) |
| Pre-loaded Firmware | Marauder 5G (scan, deauth, beacon, sniff, evil portal) |
| Firmware Compatibility | Momentum, Unleashed |
| Custom Development | PlatformIO (Ameba D / RTL8720DN framework) |
| Operating Temperature | −40°C to 85°C |
| Antenna Interface | IPEX (U.FL) or on-board PCB antenna (varies by revision) |
| Form Factor | Flipper Zero GPIO add-on board |

## Use Cases

- **Dual-Band Wi-Fi Scanning** — passively enumerate 2.4 GHz and 5 GHz networks; capture SSID, BSSID, channel, RSSI, encryption type, and connected clients
- **Wi-Fi Deauthentication Research** — send 802.11 deauth frames to test network resilience and evaluate 802.11w/PMF (Protected Management Frames) protection on authorized networks
- **WPA Handshake Capture** — sniff EAPOL/PMKID handshakes for authorized network security auditing
- **Evil Portal Development** — prototype rogue AP captive portal scenarios for phishing-awareness testing (authorized environments only)
- **Beacon Flood Testing** — broadcast custom SSIDs to study RF congestion impact and client behavior
- **BLE Device Enumeration** — scan and identify nearby BLE 5.0 peripherals alongside Wi-Fi research
- **Mesh Network Topology Mapping** — identify mesh AP relationships, backhaul channels, and hidden SSID configurations
- **IoT Wireless Protocol Research** — analyze IoT device behavior on both Wi-Fi bands in a controlled lab environment
- **Authorized Penetration Testing Education** — hands-on learning platform for Wi-Fi security fundamentals in authorized environments

---

{{< alert "warning" >}}
**New to this board?** Follow our step-by-step beginner guide — covering prerequisites, firmware setup, first scan, and all key features.
[📖 Open Online User Manual](/en/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
Need a quote? [Contact us](/en/contact/)
{{< /alert >}}
