---
title: "\"Does ALFA Wireless Card Support Tomato?\""
date: 2026-09-03
draft: false
slug: "alfa-tomato-router-compatibility"
tags:
  - "ALFA"
  - "Tomato"
  - "FreshTomato"
  - "Router"
  - "Broadcom"
  - "USB-WiFi"
  - "Compatibility"
categories:
  - "Hardware Guide"
description: "ALFA router models lack USB WiFi support on Tomato firmware, not recommended; use OpenWrt for USB WiFi compatibility."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on routers that have been flashed with Tomato firmware?"

Short Conclusion: Currently, all active models of the ALFA series are unsupported on Tomato firmware (including derivatives such as FreshTomato and AdvancedTomato), and it is not recommended to use them. Tomato is the weakest platform among the three major third-party router firmwares in terms of USB WiFi support, with its development focus entirely on the built-in WiFi of Broadcom chipsets. If USB WiFi network cards need to be used on a router, OpenWrt should be used instead.

Subject Matter: ALFA's current 9 models of USB network cards (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyzing Target Software Specifications and Requirements

### 2.1 What is Tomato?

Tomato is a long-standing open-source router third-party firmware, originally developed by Jonathan Zarate, with several branches derived from it:

| Derived Version | Maintenance Status | Supported Platforms |
|---|---|---|
| Original Tomato | Discontinued Maintenance (Early 2010s) | Broadcom MIPS routers |
| Tomato by Shibby | Discontinued Maintenance | Broadcom MIPS / ARM |
| AdvancedTomato | Discontinued Maintenance | Broadcom (GUI modification of Shibby branch) |
| FreshTomato | Active Maintenance | Broadcom MIPS / ARM (BCM47xx / BCM53xx) |
| Toastman Tomato | Discontinued Maintenance | Broadcom MIPS |

### 2.2 Tomato's USB WiFi Support Framework

The core design philosophy of Tomato is to "provide a minimalist and stable third-party firmware for Broadcom routers," with its USB functionality mainly supporting:

| USB Function Type | Support Status |
|---|---|
| USB Storage Devices (USB flash drives / hard drives) | ✅ Fully Supported (Samba / FTP / DLNA) |
| USB Printers | ✅ Supported (p910nd / CUPS) |
| USB 3G/4G Data Modems | ⚠️ Partially Supported |
| USB WiFi Network Cards | ❌ Almost Not Supported |

Tomato's core (kernel) includes only the closed-source driver (wl module) for the built-in WiFi of Broadcom routers by default, with no USB WiFi drivers. Its package management system (ipkg / Optware) also does not provide USB WiFi driver packages.

### 2.3 Key Limitations

- Tomato only supports routers with Broadcom chips, and the USB ports on Broadcom routers are usually only used for storage / printers
- Although FreshTomato is still being maintained, the focus of development is on fixing bugs on the Broadcom platform, and no new USB WiFi drivers will be added
- Tomato has a very small file system space (usually 4-16MB), even if you want to manually compile drivers, there is no space to install them
- Tomato does not have modern package management systems like opkg, and cannot install kmod drivers as easily as OpenWrt

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current USB wireless network card product line includes the following (parent models: 9):

| Model | Wi-Fi Level | Chipset | Interface | Tomato Driver Status |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ None |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ None |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ None |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ❌ None |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ❌ None |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ❌ None |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ❌ None |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ❌ None |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ❌ None |

## 4. Compatible Models and Chipsets

### 4.1 Extremely Old ALFA Models That May Be Available in Tomato (Discontinued)

| Model | Chipset | Linux Driver Module | Description |
|---|---|---|---|
| AWUS036NH | Ralink RT3070 | rt2800usb | Theoretically loadable, but Tomato does not include it by default; requires manual kernel module compilation, actual feasibility is extremely low |
| AWUS036H | Realtek RTL8187L | rtl8187 | As above, only 2.4GHz / 54Mbps, discontinued over a decade ago |

⚠️ Even for the aforementioned old models, users will need to manually cross-compile the corresponding kernel version driver modules in Tomato, and the file system space in Tomato is usually insufficient for installation. This does not constitute "support," but rather "extremely advanced hacking."

### 4.2 Current Models That Are Completely Unavailable in Tomato

All current ALFA models (see Table 3) are not available in Tomato for the following reasons:

- Realtek Chip (RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU): Tomato has no corresponding drivers, and they cannot be installed through package management
- MediaTek Chip (MT7612U / MT7610U / MT7921AUN): Tomato does not include mt76 / mt7921 drivers, and the FreshTomato development team has no plans to add them
- Even if the device is visible in lsusb (if Tomato has the USB core enabled), it is only recognized at the USB bus level and cannot establish a network interface

## 5. Environmental Requirements

Since the current ALFA models are not available on Tomato, this section lists the extreme conditions required if the customer insists on trying:

| Item | Requirement |
|---|---|
| Router Hardware | Broadcom chip router with a USB 2.0 port, Flash ≥ 32MB, RAM ≥ 256MB |
| Tomato Version | Latest version of FreshTomato (older versions have worse USB support) |
| Cross-Compilation Environment | Requires setting up a cross-compilation toolchain for the corresponding Broadcom architecture (MIPS / ARM) for Tomato |
| Driver Source Code | Requires obtaining the Linux driver source code for the corresponding chip and modifying it to match the Tomato kernel version |
| Technical Skills | Requires Linux kernel module development, cross-compilation, and debugging capabilities |
| Time Cost | Estimated to take several hours to several days, with a low success rate |

Conclusion: For 99.9% of users, using the ALFA USB WiFi adapter on Tomato is not feasible.

## 6. Compatibility Determination

### ALFA Current Models × Tomato Compatibility Matrix

| Model | Chipset | USB Core Support | USB Detection | STA Internet Access | AP Mode | Monitor | Overall Rating |
|---|---|---|---|---|---|---|---|
| AWUS036AXML | MT7921AUN | ⚠️ Requires USB Core Enablement | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036AXM | MT7921AUN | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036AX | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036AXER | RTL8832BU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036ACH | RTL8812AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036ACHM | MT7610U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036ACM | MT7612U | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036ACS | RTL8811AU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |
| AWUS036EACS | RTL8811CU | ⚠️ | ❌ | ❌ | ❌ | ❌ | Not Supported |

Determination Criteria: The official Tomato (including FreshTomato) kernel and package repository do not include any drivers for modern USB WiFi chipsets. The design goal of Tomato has never included USB WiFi expansion functionality.

## 7. Detailed Step by Step Setup Steps

Since the current ALFA models are not available on Tomato, this section provides verification steps and alternative solutions.

### 7.1 Verify if Your Tomato Router Supports USB WiFi (Troubleshooting Steps)

**Step 1: Log into the Tomato Management Interface**

Enter 192.168.1.1 (or your router's IP) in the browser.

**Step 2: Check if the USB Core is Enabled**

- Go to USB and NAS > USB Support
- Confirm that Core USB Support, USB 2.0 Support, USB 3.0 Support (if available) are checked
- Confirm USB Wireless Device Support (if available) — Most Tomato versions do not have this option

**Step 3: Insert the ALFA network card into the router's USB port**

**Step 4: Check USB Detection on the Router via SSH / Telnet**

```bash
# Check if lsusb is available (Tomato may not have it by default)
which lsusb
# If lsusb is not available, check /proc/bus/usb or dmesg
cat /proc/bus/usb/devices
# Or
dmesg | grep -i usb
```

**Step 5: Check the Network Interface**

```bash
ifconfig -a
# If you only have vlan0 / br0 / eth0 / eth1 (router's built-in interfaces), and there is no wlan0 / wlan1, it means the USB WiFi is not driven
```

**Step 6: Check Available Kernel Modules**

```bash
lsmod
# Expected to only have wl (Broadcom built-in WiFi driver), et (Ethernet driver) etc.
# There should not be mt76 / rtl8812 / cfg80211 / mac80211 etc. USB WiFi drivers
```

**Step 7: Check if Additional Packages Can Be Installed**

```bash
# Tomato uses ipkg, but the package repository is very limited
ipkg list | grep -i "wifi\|wireless\|8812\|mt76"
# Expected result is empty
```

### 7.2 Recommended Alternatives

#### Solution 1: Switch to OpenWrt (Strongly Recommended)

If your router model is also supported by OpenWrt, it is recommended to flash the firmware from Tomato to OpenWrt. OpenWrt has a complete USB WiFi driver package library that supports most ALFA models.

- Confirm if your router is on the OpenWrt Supported Devices list
- If supported, refer to the installation steps in [Is ALFA Wireless Card Supported by OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

#### Solution 2: Use the Router's Built-in WiFi

Tomato has excellent support for the built-in WiFi of Broadcom routers. If your needs are for general internet access or AP hotspot, you can directly use the router's built-in WiFi without the need for an external ALFA network card.

#### Solution 3: Replace Hardware

If you need specific features of USB WiFi (such as high-power output, monitor mode, packet injection), the Tomato platform cannot meet your needs. It is recommended:

- Use a router supported by OpenWrt + ALFA network card
- Or use an x86 mini PC to install OpenWrt / pfSense + ALFA network card
- Or directly use the ALFA network card on a Kali Linux / Ubuntu computer

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| Tomato management interface does not have the "USB Wireless Device Support" option | The Tomato version does not have USB WiFi support translated | This is normal, not a bug; most Tomato versions do not have this feature |
| After inserting the ALFA network card, dmesg shows USB detection but no network interface | Missing driver | Unresolvable, Tomato has no corresponding driver |
| Want to manually install ipkg packages but cannot find WiFi drivers | Tomato package repository does not have USB WiFi drivers | This is normal; it is recommended to use OpenWrt instead |
| Old ALFA (RT3070) can be detected on Tomato but cannot connect | Driver incomplete / firmware missing | Even with old chips, there is no guarantee of usability; it is recommended to use OpenWrt |
| After flashing Tomato, the USB port on the router can only read flash drives | Tomato's USB functionality is designed only for storage / printers | This is expected behavior; Tomato does not support USB WiFi |

## 9. Known Limitations

- **Complete Lack of USB WiFi Drivers**: The official Tomato (including FreshTomato) kernel does not include any drivers for modern USB WiFi chips, which is the most fundamental limitation.
- **Broadcom Closed-Source Driver Binding**: Tomato relies on Broadcom's closed-source `wl` driver and cannot coexist with open-source `mac80211`/`cfg80211` architecture-based USB WiFi drivers.
- **Lack of Package Management Ecosystem**: Tomato's ipkg package repository contains very few packages, unlike OpenWrt which has thousands of installable packages.
- **Insufficient Flash/RAM Space**: Most Tomato routers have only 4-16MB of Flash, even if drivers are compiled, there is no space to install them.
- **Different Development Direction**: The FreshTomato development team's priority is to fix the stability of the Broadcom platform, and they will not invest resources in adding USB WiFi support.
- **No Support for Monitoring/Injection**: Tomato's WiFi architecture (Broadcom `wl` driver) itself does not support penetration testing features, and attaching an external USB WiFi does not change this.
- **No AP Mode Expansion**: Even if old chips can load the driver, Tomato's network settings interface does not support setting the USB WiFi to AP mode.

**Counterarguments**: If a future version of FreshTomato explicitly adds USB WiFi driver support in the official release notes, or if a widely verified FreshTomato mt76/rtl8812au module porting project appears in the community, the "Not Supported" determination in Section 6 of this document needs to be re-evaluated; if FreshTomato switches to an open-source `mac80211` architecture kernel, the limitation description also needs to be updated.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| FreshTomato Official Website | FreshTomato Latest Version and Supported Devices List | https://freshtomato.org/ | ✅ Verified | 2026-09-03 |
| OpenWrt Official Documentation | USB WiFi Drivers and Wireless Configuration (Comparison Reference) | https://openwrt.org/docs/start | ✅ Verified | 2026-09-03 |
| OpenWrt Official Forum | USB WiFi Driver Discussions (Comparison Reference) | https://forum.openwrt.org/ | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yupitek) | ALFA Current Product Specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |

Related Articles: [Is ALFA Wireless Network Card Compatible with DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/) | [Is ALFA Wireless Network Card Compatible with OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [Is ALFA Wireless Network Card Compatible with NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) | [Is ALFA Wireless Network Card Compatible with NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Disclaimer: The compatibility determination in this article is based on the official Tomato / FreshTomato core and package repository. A very small number of advanced users may be able to implement basic functions on specific old chips through self-cross compiling, but this does not fall within the official support scope and is not recommended for general users to attempt. For scenarios where USB WiFi needs to be used on a router, OpenWrt is the only practical third-party firmware option available.
