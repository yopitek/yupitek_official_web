---
title: "\"ALFA Wireless Card Compatibility with OpenWrt\""
date: 2026-09-03
draft: false
slug: "alfa-openwrt-router-compatibility"
tags:
  - "ALFA"
  - "OpenWrt"
  - "Router"
  - "kmod-mt76"
  - "AWUS036ACM"
  - "AWUS036ACH"
  - "Soft-AP"
categories:
  - "Hardware Guide"
description: "OpenWrt offers top ALFA USB WiFi card support, with direct official support for MediaTek models and community-maintained drivers for Realtek, with AWUS036ACM (MT7612U) as the recommended choice."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network card be used on an OpenWrt router?"

Short Conclusion: OpenWrt is the best-supported platform among the three major third-party router firmwares (DD-WRT / OpenWrt / Tomato) for ALFA USB WiFi network cards. MediaTek chip models (AWUS036ACM / ACHM / AXML / AXM) can be directly supported through the official kmod-mt76 series package; Realtek chip models (AWUS036ACH / ACS / EACS / AX / AXER) require the use of community-maintained out-of-tree driver packages, with availability varying depending on the OpenWrt version. The preferred choice is AWUS036ACM (MT7612U), which has mature, stable drivers and supports monitoring and injection.

Assessment Base: ALFA's current 9 USB network cards (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyzing Target Software Specifications and Requirements

### 2.1 What is OpenWrt

OpenWrt is a highly modular open-source router firmware that uses the Linux kernel and the opkg package management system. Unlike DD-WRT / Tomato, OpenWrt's drivers are provided as individually installable kernel module (kmod) packages, allowing users to install USB WiFi drivers as needed without recompiling the entire firmware.

### 2.2 OpenWrt's USB WiFi Driver Framework

The OpenWrt official package repository includes the following USB WiFi drivers:

| Driver Package | Source | Covered Chip / Model | Maintenance Status |
|---|---|---|---|
| kmod-mt76-usb + kmod-mt76x2u | Official in-kernel | MediaTek MT7612U (AWUS036ACM) | Active, stable |
| kmod-mt76-usb + kmod-mt76x0u | Official in-kernel | MediaTek MT7610U (AWUS036ACHM) | Active |
| kmod-mt7921u | Official in-kernel | MediaTek MT7921AUN (AWUS036AXML / AXM) | Available in 23.05+ versions |
| kmod-rtl8812au-ct | Community out-of-tree | Realtek RTL8812AU / RTL8811AU (AWUS036ACH / ACS) | Community maintained, kernel crash reports in 24.10 |
| kmod-rtl8821cu | Community out-of-tree | Realtek RTL8811CU (AWUS036EACS) | Community maintained |
| kmod-rtw89 / kmod-rtl8852bu | Under development | Realtek RTL8832BU (AWUS036AX / AXER) | rtw89 USB support is gradually integrated, requires a newer kernel |

### 2.3 Prerequisites: USB Core Support

Before installing the WiFi driver, it is necessary to ensure that OpenWrt has USB core support enabled:

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

Most modern OpenWrt versions already include kmod-usb-core by default, but usbutils (which provides the lsusb command) needs to be installed manually.

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current USB wireless network card product line includes the following models (parent models: 9):

| Model | Wi-Fi Level | Chipset | Interface | OpenWrt Driver Package |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | kmod-mt7921u (23.05+) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | kmod-mt7921u (23.05+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | kmod-rtw89 (in development) / Self-compiled rtl8852bu |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | As above |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | kmod-rtl8812au-ct (community) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | kmod-mt76x0u (official) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | kmod-mt76x2u (official)⭐ Recommended |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | kmod-rtl8812au-ct (inclusive) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | kmod-rtl8821cu (community) |

## 4. Applicable Models and Chipsets

### 4.1 Recommended Grade Classification

| Recommended Grade | Model (Chipset) | Description |
|---|---|---|
| ⭐ Highly Recommended | AWUS036ACM (MT7612U) | Official drivers mature and stable, supports AP / STA / Monitor / Injection, the best choice on OpenWrt |
| ✅ Recommended | AWUS036ACHM (MT7610U) | Official drivers, dual-band but only 433Mbps, suitable for low-power consumption scenarios |
| ✅ Recommended (New Version) | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, official drivers, requires OpenWrt 23.05+ and kernel 5.15+ |
| ⚠️ Available but with Caution | AWUS036ACH (RTL8812AU) | Community drivers, kernel crash reports in version 24.10, recommended to use 23.05 |
| ⚠️ Available but with Caution | AWUS036ACS (RTL8811AU) | As above, covered by 8812au drivers |
| ⚠️ Available but with Caution | AWUS036EACS (RTL8811CU) | Community drivers, stability moderate |
| ❌ Not Recommended | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, rtw89 USB support still in development, most OpenWrt versions cannot be used directly |

### 4.2 Router Hardware Requirements

| Item | Minimum Requirement | Recommended Requirement |
|---|---|---|
| USB Port | USB 2.0 (AWUS036ACHM / ACS / EACS) | USB 3.0 (AWUS036ACH / ACM / AX series) |
| Flash | 16MB (driver installation + dependency packages) | 32MB+ |
| RAM | 128MB | 256MB+ (AP mode + multi-user) |
| OpenWrt Version | 21.02+ | 23.05.x (stable version) |

## 5. Environmental Requirements

### 5.1 Software Environment

- OpenWrt Stable Version: 23.05.x (kernel 5.15) or 24.10.x (kernel 6.6)
- Package Source: Official opkg package repository (https://downloads.openwrt.org/releases/{version}/packages/{arch}/)
- Network Connection: The router must be online during the driver installation process (via the WAN port)

### 5.2 Hardware Environment

- OpenWrt compatible router with USB 2.0 / 3.0 port
- High-power models (AWUS036ACH) are recommended to use a powered USB 3.0 Hub to avoid insufficient power supply from the router's USB port
- AWUS036AXML is a USB-C interface, ensure that the router has a USB-C port or use a USB-C to USB-A adapter

## 6. Compatibility Determination

### ALFA Current Models × OpenWrt Compatibility Matrix

| Model | Chipset | Driver Method | USB Detection | STA Internet | AP Mode | Monitor | Minimum Version | Overall Rating |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | kmod-mt76x2u | ✅ | ✅ | ✅ | ✅ | 21.02+ | ⭐ Best |
| AWUS036ACHM | MT7610U | kmod-mt76x0u | ✅ | ✅ | ✅ | ⚠️ Limited | 21.02+ | ✅ Good |
| AWUS036AXML | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limited | 23.05+ | ✅ Good |
| AWUS036AXM | MT7921AUN | kmod-mt7921u | ✅ | ✅ | ✅ | ⚠️ Limited | 23.05+ | ✅ Good |
| AWUS036ACH | RTL8812AU | kmod-rtl8812au-ct | ✅ | ✅ | ✅ | ⚠️ Limited | 22.03+（24.10 has crash） | ⚠️ Available |
| AWUS036ACS | RTL8811AU | kmod-rtl8812au-ct | ✅ | ✅ | ⚠️ | ❌ | 22.03+ | ⚠️ Available |
| AWUS036EACS | RTL8811CU | kmod-rtl8821cu | ✅ | ⚠️ | ❌ | ❌ | 23.05+ | ⚠️ Available |
| AWUS036AX | RTL8832BU | rtw89（under development） | ⚠️ | ❌ | ❌ | ❌ | Requires custom compilation | ❌ Not Recommended |
| AWUS036AXER | RTL8832BU | rtw89（under development） | ⚠️ | ❌ | ❌ | ❌ | Requires custom compilation | ❌ Not Recommended |

Determination Criteria: Availability of kmod packages in the OpenWrt official package repository (23.05 / 24.10) + user reports from the OpenWrt forum. The Realtek chip drivers are maintained by the community, and their stability and functionality are not as complete as MediaTek mt76 series.

## 7. Detailed Step by Step Setup Steps

### 7.1 Preparatory Steps: Enabling USB Core Support

**Step 1: SSH into the OpenWrt Router**

```bash
ssh root@192.168.1.1
```

**Step 2: Update Package Repository and Install USB Core Support**

```bash
opkg update
opkg install kmod-usb-core kmod-usb2 kmod-usb3 usbutils
```

**Step 3: Insert the ALFA Network Card and Confirm USB Detection**

```bash
lsusb
# Expected output example (AWUS036ACM / MT7612U):
# Bus 002 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

### 7.2 Path A: MediaTek Chipset Models (AWUS036ACM / ACHM / AXML / AXM)

Using AWUS036ACM (MT7612U) as an example:

**Step 1: Install Driver Packages**

```bash
# AWUS036ACM (MT7612U)
opkg install kmod-mt76-usb kmod-mt76x2u

# AWUS036ACHM (MT7610U) — Use instead
# opkg install kmod-mt76-usb kmod-mt76x0u

# AWUS036AXML / AXM (MT7921AUN) — Use instead (requires 23.05+)
# opkg install kmod-mt7921u
```

**Step 2: Install Wireless Management Tools**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Step 3: Confirm Network Interface Established**

```bash
iw dev
# Expected to see wlan0 or wlan1 interface
```

**Step 4: Scan Nearby WiFi (Verify Functionality)**

```bash
iw dev wlan0 scan | grep -E "SSID|signal"
```

**Step 5: Set as STA Client Mode (Connect to Existing AP)**

Edit /etc/config/wireless:

```text
config wifi-device 'radio1'
       option type 'mac80211'
       option path 'platform/usb1/1-1/1-1:1.0'
       option channel 'auto'
       option htmode 'VHT80'

config wifi-iface 'wifinet2'
       option device 'radio1'
       option mode 'sta'
       option network 'wwan'
       option ssid 'Your WiFi Name'
       option encryption 'psk2'
       option key 'Your WiFi Password'
```

**Step 6: Restart Wireless Service**

```bash
/etc/init.d/network restart
```

**Step 7: Set as AP Hotspot Mode (Share Network)**

Edit /etc/config/wireless, change mode to ap:

```text
config wifi-iface 'wifinet2'
   option device 'radio1'
   option mode 'ap'
   option network 'lan'
   option ssid 'ALFA-OpenWrt-AP'
   option encryption 'psk2'
   option key 'Your Hotspot Password'
```

**Step 8: Enable Monitor Mode (For Penetration Testing)**

```bash
opkg install aircrack-ng
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
iw dev wlan0 set channel 6
# Verify
iw dev wlan0 info
# type should show monitor
```

### 7.3 Path B: Realtek Chipset Models (AWUS036ACH / ACS / EACS)

Using AWUS036ACH (RTL8812AU) as an example:

**Step 1: Install Community Drivers**

```bash
opkg update
opkg install kmod-rtl8812au-ct

# AWUS036EACS (RTL8811CU) — Use instead
# opkg install kmod-rtl8821cu
```

**Step 2: Install Wireless Management Tools**

```bash
opkg install iw iwinfo wireless-tools hostapd-common wpa-supplicant
```

**Step 3: Confirm Interface**

```bash
iw dev
# Note: The interface name for the rtl8812au-ct driver may be wlan0 or wlan1
```

The setup method is the same as Step 5-7 of 7.2 (STA / AP mode settings).

**Step 4: Monitor Mode**

```bash
# rtl8812au-ct driver supports monitor mode
ip link set wlan0 down
iw dev wlan0 set type monitor
ip link set wlan0 up
# Packet injection functionality is limited, recommend using mt76 chipset for penetration testing
```

**Step 5: If Kernel Crash Occurs (Known issue in 24.10 version)**

```bash
# Roll back to 23.05 stable version, or use custom compiled drivers
# Check crash logs
logread | grep -i "panic\|crash\|rtl8812"
```

### 7.4 Path C: Wi-Fi 6 Models (AWUS036AX / AXER, RTL8832BU)

⚠️ This path requires custom compiling OpenWrt, not suitable for general users.

**Step 1: Confirm if OpenWrt Version Includes rtw89 USB Support**

```bash
opkg list | grep rtw89
# If no results, the version does not include it
```

**Step 2: If Needed, Compile OpenWrt Image File Yourself**

Add kmod-rtw89 and corresponding firmware.

**Alternative Suggestion**: For the need to use Wi-Fi 6 USB network cards on OpenWrt routers, currently using AWUS036AXML (MT7921AUN) as an alternative is recommended.

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not show ALFA Network Card | USB core not installed / insufficient power supply | Confirm that kmod-usb-core, kmod-usb2, and kmod-usb3 are installed; use a powered USB Hub |
| lsusb shows the card but iw dev has no interface | Drivers not installed / incompatible drivers | Install the corresponding kmod package; check dmesg for firmware missing errors |
| opkg install kmod-mt76x2u reports 'kernel version mismatch' | OpenWrt version does not match the package repository version | Run opkg update and try again; confirm that the firmware version matches the package repository architecture |
| AP mode fails to start (hostapd error) | Driver does not support AP / incorrect channel settings | Confirm that the chip supports AP mode; try setting a fixed channel (e.g., 6 or 149); check Regulatory Domain |
| Monitor mode cannot inject packets | Driver does not support injection / channel collision | MediaTek mt76 series supports the best; Realtek 8812au-ct injection functionality is limited; confirm airmon-ng check kill |
| AWUS036ACH disconnects when high power is used | Insufficient USB power supply | Use a powered USB 3.0 Hub; set option txpower '20' in /etc/config/wireless to reduce power |
| Kernel panic after installing rtl8812au-ct on 24.10 | Known driver compatibility issues | Roll back to 23.05.x stable version; or track GitHub issues for fixes |
| MT7921 (AXML/AXM) cannot use 6GHz | Regulatory Domain restriction / kernel version | Requires kernel 5.19+ and correct Wi-Fi 6E regulatory domain settings; 6GHz support in OpenWrt 23.05 is still in testing |

## 9. Known Limitations

- Realtek chip drivers are maintained by the community: `kmod-rtl8812au-ct`, `kmod-rtl8821cu` are not officially maintained by OpenWrt, and stability and update schedules cannot be guaranteed.
- Kernel crash reports for the 24.10 version of `rtl8812au-ct`: It is recommended that users of Realtek chips maintain version 23.05.x.
- Insufficient support for Wi-Fi 6 (RTL8832BU): The `rtw89` USB driver is still under development, and most OpenWrt versions cannot directly use AWUS036AX / AXER.
- Limited AP mode performance: When using USB WiFi as an AP, throughput is lower than the router's built-in WiFi (due to USB bus bandwidth + driver overhead).
- Differences in monitor/inject functions: MediaTek mt76 series supports the most complete; the injection function of Realtek chips is limited and not suitable for professional penetration testing.
- Router hardware resources: On low-end routers (16MB Flash / 128MB RAM), installing drivers may result in insufficient space, affecting other functions.
- USB 3.0 interference: USB 3.0 devices may interfere with 2.4GHz WiFi, and it is recommended to use a USB 2.0 port or a well-isolated USB Hub.
- Using multiple network cards simultaneously: When using the router's built-in WiFi + USB WiFi at the same time, channel conflicts or resource contention may occur.
- ⚠️ **Driver maintainers for RTL8832BU (AWUS036AX/AXER) have publicly recommended avoiding its use**: The marking in Section 4.1 as "❌ Not Recommended" is not just because the `rtw89` USB is still under development, but also because the driver maintainer morrownr has publicly stated that the chip series "is a very bad driver, and there are doubts about the chip itself," recommending that Linux users avoid it for the time being (source see Section 10).
- **Clarification needed for kernel version threshold terms**: The wording in Section 4.1 "MT7921AUN requires OpenWrt 23.05+ and kernel 5.15+" is easy to mislead——the `mt7921u` driver itself actually needs **kernel 5.19+** on desktop Linux (see the original words of the driver maintainer), but the official OpenWrt package often includes it early through the backport mechanism, so OpenWrt 23.05 (although marked with a base kernel of 5.15) still has user reports of successful installation of `kmod-mt7921u`. **Please judge based on the actual query results of the customer version `opkg list`, and do not infer the kernel version**.

Counter-arguments: If the OpenWrt subsequent package update fixes the kernel crash issue of 24.10 `rtl8812au-ct`, the recommendations for AWUS036ACH in Section 4.1 and Section 6 can be upgraded from "maintain 23.05"; if the official support for `rtw89` USB is officially included in the OpenWrt official package repository, the "not recommended" judgment for AWUS036AX / AXER needs to be reconsidered; if the official releases a complete support statement for MT7921's 6GHz, the limitations of AXML / AXM need to be updated.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| OpenWrt Official Documentation | OpenWrt official document entry (Wireless Settings / Package Management) | https://openwrt.org/docs/start | ✅ Verified | 2026-09-03 |
| OpenWrt Official Forum | USB WiFi Driver Discussion Entry | https://forum.openwrt.org/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver Upstream | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yupitek) | ALFA current product specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Driver Maintainer's Official Statement: Suggest to avoid rtl8852/32au (RTL8832BU) chip | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verified | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko appears in the kernel only with kernel 5.19+ (Driver Maintainer's Original Words) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Verified | 2026-09-03 |
| OpenWrt Official Forum — Best USB WiFi Dongle for Raspberry Pi 4B | User Reports Successful Installation of kmod-mt7921u with OpenWrt 23.05.0 | https://forum.openwrt.org/t/best-usb-wifi-dongle-for-raspberry-pi-4b/160103 | ✅ Verified | 2026-09-03 |

Related Articles: [Is ALFA Wireless Network Card Compatible with DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)｜[Is ALFA Wireless Network Card Compatible with Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/)｜[Is ALFA Wireless Network Card Compatible with NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Is ALFA Wireless Network Card Compatible with NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Disclaimer: The compatibility determination in this article is based on the official package repository of OpenWrt 23.05.x / 24.10.x. The availability of packages may vary depending on different router architectures (ath79 / ramips / mvebu / x86, etc.). Realtek chip drivers are maintained by the community, and actual stability may vary with version changes. It is recommended to prioritize MediaTek chip models (AWUS036ACM as the first choice) for OpenWrt USB WiFi.
