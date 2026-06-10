---
title: "HAK5 WiFi Pineapple Mark VII + ALFA AWUS036ACM: Complete 5GHz Setup Guide (2026)"
description: "Full compatibility guide for HAK5 WiFi Pineapple MK7 with ALFA AWUS036ACM (MT7612U) — plug-and-play 5GHz monitor mode, packet injection, and PineAP extension. Step-by-step setup with verified commands. No driver compilation required."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi-Pineapple", "AWUS036ACM", "MT7612U", "monitor-mode", "packet-injection", "PineAP", "OpenWrt", "5GHz", "penetration-testing"]
featureimage: "/images/blog/hak5-pineapple-mark7-alfa-awus036acm.webp"
---

The HAK5 WiFi Pineapple Mark VII is the gold standard for portable wireless security auditing. But out of the box, it ships with one significant limitation: the built-in radio operates exclusively on **2.4 GHz**. In 2026, most corporate and residential networks have migrated to 5 GHz for better performance and less congestion — meaning a stock MK7 misses half the airspace.

This is where the **ALFA AWUS036ACM** enters the picture. It is one of only a handful of 802.11ac adapters [officially confirmed compatible](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters) by Hak5, and it works with **zero driver compilation** thanks to the in-kernel `mt76x2u` driver preloaded in MK7 Firmware 2.x.

This guide covers everything: hardware specs, driver compatibility, a verified 7-step setup process, and a full penetration-testing topology so you can add 5 GHz monitor mode and packet injection to your Pineapple in under 10 minutes.

---

## 1. Why You Need 5 GHz on Your WiFi Pineapple

The MK7's internal MT7628AN SoC provides a capable 2.4 GHz b/g/n radio — sufficient for basic PineAP operations like beacon flooding, deauth attacks, and client probing. But the wireless landscape has evolved:

| Scenario | 2.4 GHz (Built-in) | 5 GHz (AWUS036ACM) |
|---|---|---|
| Corporate WPA2-Enterprise networks | Often 2.4 GHz still present | **Primary band** for modern deployments |
| Residential mesh systems (Eero, Google WiFi) | Legacy fallback only | **Default band** for client connections |
| 802.11ac client devices | Rarely connect on 2.4 GHz | **Always prefer 5 GHz** |
| Channel congestion (apartment/office) | Extremely crowded (channels 1–11) | Clean spectrum (channels 36–165) |
| WPA3-SAE handshake capture | Limited | Full 5 GHz capture capability |

**Bottom line**: if you are auditing modern networks, you need 5 GHz. The AWUS036ACM is the most reliable way to add it to a WiFi Pineapple MK7.

---

## 2. Target Platform: HAK5 WiFi Pineapple Mark VII

### 2.1 Hardware Specifications

The MK7 is built on a MediaTek MT7628AN system-on-chip — a single-core MIPS 24KEc network processor optimized for packet-level operations:

| Component | Specification |
|---|---|
| **SoC** | MediaTek MT7628AN (MIPS 24KEc) |
| **RAM** | 256 MB DDR2 |
| **Storage** | 2 GB eMMC |
| **Power** | USB-C, 5V @ 2A |
| **USB Host** | 1× USB 2.0 Type-A (480 Mbps max) |
| **USB Power Budget** | 500 mA @ 5V (2.5W total) |

The USB 2.0 port deserves special attention. While the AWUS036ACM is a USB 3.0 device capable of 867 Mbps on 5 GHz, the MK7's USB 2.0 bus caps throughput at approximately 150–250 Mbps. For penetration testing workloads — monitor mode capture, handshake collection, beacon analysis — this bandwidth is more than sufficient. The limitation only matters if you attempt to use the MK7 as a high-throughput wireless bridge, which is not its designed purpose.

### 2.2 Software Environment

The MK7 runs a heavily customized OpenWrt distribution maintained by Hak5:

| Layer | Detail |
|---|---|
| **Operating System** | OpenWrt (Hak5 custom build) |
| **Kernel Version** | 5.4.x (Firmware 2.x series) |
| **Preloaded Drivers** | `kmod-mt76x2u` (MT7612U), `kmod-mt7601u` (MT7601U) |
| **Package Manager** | `opkg` |
| **Wireless Tools** | `iw`, `iwconfig`, `airmon-ng`, `hostapd` (2.9), `uci` |
| **Management** | PineAP Web UI + SSH (port 22) |

> ✅ **Critical fact**: `kmod-mt76x2u` is preloaded in MK7 Firmware 2.x. The AWUS036ACM is **plug-and-play** — no `opkg install`, no cross-compilation, no DKMS headaches.

---

## 3. ALFA AWUS036ACM — Hardware Deep Dive

### 3.1 Specifications

The AWUS036ACM is built around the **MediaTek MT7612U** chipset, which was merged into the Linux mainline kernel at version 4.19 (October 2018). This upstream inclusion is what makes it seamless on the MK7.

| Specification | Detail |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **USB VID/PID** | `0E8D:7612` |
| **USB Interface** | USB 3.0 Type-A (backward compatible to USB 2.0) |
| **Frequency Bands** | 2.4 GHz (b/g/n) + 5 GHz (a/n/ac) |
| **Max Data Rate** | 2.4 GHz: 300 Mbps · 5 GHz: 867 Mbps |
| **Channel Width** | 20 / 40 / 80 MHz |
| **Monitor Mode** | ✅ Supported |
| **Packet Injection** | ✅ Supported (via mac80211 framework) |
| **AP Mode (Master)** | ✅ Supported |
| **Antenna** | 2× 5 dBi dual-band RP-SMA (detachable) |
| **TX Power** | 2.4G: 23 dBm · 5G: 20 dBm (±2 dBm) |
| **Peak Current Draw** | ~380 mA @ 5V |
| **Security Protocols** | WEP / WPA / WPA2 / WPA3 / 802.1X |

The RP-SMA antenna connectors are a significant advantage: you can swap the stock 5 dBi omnidirectional antennas for high-gain directionals, panel antennas, or outdoor-rated options depending on your testing environment.

### 3.2 Confirmed Hak5 Compatibility

Hak5 maintains an official list of [compatible 802.11ac adapters](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters). The AWUS036ACM (MT7612U) is explicitly listed as compatible — alongside Hak5's own MK7AC Adapter, which uses the **same MT7612U chipset**.

| Adapter | Chipset | Status |
|---|---|---|
| Hak5 MK7AC Adapter | MT7612U | ✅ Official accessory |
| **ALFA AWUS036ACM** | **MT7612U** | ✅ **Officially confirmed** |
| EP-AC1605 V1 | MT7612U | ✅ (V2 not compatible) |

The driver source lives at the [OpenWrt mt76 repository](https://github.com/openwrt/mt76) on GitHub, with installation notes maintained by the community at [morrownr/7612u](https://github.com/morrownr/7612u).

---

## 4. Compatibility Matrix

| Assessment | Result | Notes |
|---|---|---|
| Chipset compatibility | ✅ **Full** | MT7612U is the confirmed chipset for MK7 |
| Driver availability | ✅ **Preloaded** | `kmod-mt76x2u` built into Firmware 2.x |
| USB identification | ✅ **Automatic** | VID `0E8D` / PID `7612` matched by `mt76x2u` |
| Monitor mode | ✅ **Supported** | Via `airmon-ng` or `iw` |
| Packet injection | ✅ **Supported** | Via mac80211 framework |
| 5 GHz scanning | ✅ **Supported** | Appears as `wlan3` after insertion |
| USB 2.0 bandwidth | ⚠️ **Limited** | Real-world 5 GHz throughput ~150–250 Mbps |
| Power budget | ✅ **Safe** | 380 mA peak vs. 500 mA USB limit |
| LED behavior | ℹ️ **By design** | MT7612U driver does not illuminate LED — not a fault |

The USB 2.0 bottleneck is the only meaningful limitation, and it only affects bulk data transfer speeds. Monitor mode capture, handshake collection, and injection testing are unaffected.

---

## 5. Step-by-Step Setup Guide

### Prerequisites

- WiFi Pineapple MK7 running **Firmware 2.x** (2.1.3 Stable or newer recommended)
- ALFA AWUS036ACM — verify genuine chipset: `lsusb` should show PID `7612`
- Internet connection on the MK7 (for `opkg update` if needed)
- SSH client (built-in terminal on macOS/Linux; PuTTY or MobaXterm on Windows)

---

### Step 1: Connect and Verify USB Detection

Plug the AWUS036ACM into the MK7's USB Type-A port. SSH into the Pineapple:

```bash
ssh root@172.16.42.1
```

Verify the USB device is recognized:

```bash
lsusb
```

**Expected output** (look for this line):

```
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

> ⚠️ If the PID is NOT `7612`, your adapter is not an AWUS036ACM (MT7612U). Counterfeit or mislabeled adapters with RTL8812AU chipsets (PID `8812`) will NOT work with the preloaded driver.

---

### Step 2: Confirm Driver Is Loaded

```bash
lsmod | grep mt76
```

**Expected output:**

```
mt76x2u
mt76x2_common
mt76x02_usb
mt76_usb
mt76x02_lib
mt76
```

If the modules are missing (unlikely on Firmware 2.x), load them manually:

```bash
modprobe mt76x2u
```

Or install via `opkg`:

```bash
opkg update
opkg install kmod-mt76x2u
```

---

### Step 3: Confirm Wireless Interface Appears

```bash
iw dev
```

**Expected output** (look for `wlan3` or similar):

```
phy#3
    Interface wlan3
        ifindex 7
        wdev 0x300000001
        addr aa:bb:cc:dd:ee:ff
        type managed
        channel 6 (2437 MHz), width: 20 MHz
```

The interface numbering depends on existing radios. Typical mapping:
- `wlan0` — Management AP (built-in 2.4 GHz)
- `wlan1` — PineAP engine (built-in 2.4 GHz)
- `wlan2` — Client mode (if configured)
- `wlan3` — **AWUS036ACM** (external USB)

---

### Step 4: Enable Monitor Mode

**Method A — airmon-ng (recommended):**

```bash
airmon-ng check kill
airmon-ng start wlan3
```

The interface is renamed to `wlan3mon`. Verify:

```bash
iwconfig wlan3mon
```

**Expected output:**

```
wlan3mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz ...
```

**Method B — iw (lightweight, no airmon-ng dependency):**

```bash
ip link set wlan3 down
iw wlan3 set monitor control
ip link set wlan3 up
```

---

### Step 5: Lock to a 5 GHz Channel and Scan

Switch to a 5 GHz channel (example: Channel 36 at 5180 MHz):

```bash
iw wlan3mon set channel 36
```

Launch airodump-ng to scan the 5 GHz band:

```bash
airodump-ng --band a wlan3mon
```

The `--band a` flag targets 802.11a/n/ac (5 GHz). You should see 5 GHz access points appearing in the scan output.

---

### Step 6: Test Packet Injection (Optional)

Verify injection capability:

```bash
aireplay-ng --test wlan3mon
```

**Expected output (success):**

```
09:14:22  Trying injection in the monitor interface... wlan3mon
09:14:22  Injection is working!
```

---

### Step 7: Auto-Enable on Boot (Optional)

To automatically enable monitor mode every time the MK7 boots with the AWUS036ACM inserted, add this to `/etc/rc.local`:

```bash
cat >> /etc/rc.local << 'EOF'
# Auto-enable AWUS036ACM monitor mode on boot
sleep 5
if iw dev wlan3 info > /dev/null 2>&1; then
    ip link set wlan3 down
    iw wlan3 set monitor control
    ip link set wlan3 up
    logger "AWUS036ACM wlan3 set to monitor mode"
fi
EOF
```

---

## 6. Penetration Testing Topology

The diagram below illustrates the complete topology when the AWUS036ACM is integrated into a WiFi Pineapple MK7 deployment. The adapter appears as `wlan3` and provides dedicated 5 GHz monitoring capability alongside the MK7's built-in PineAP engine on 2.4 GHz.

![HAK5 WiFi Pineapple MK7 + AWUS036ACM Penetration Testing Topology](/images/blog/hak5-pineapple-topology.svg)

| Interface | Role | Band |
|---|---|---|
| `wlan0` | Management AP — operator connects to manage MK7 | 2.4 GHz |
| `wlan1` | PineAP Engine — SSID broadcast, deauth, probe capture | 2.4 GHz |
| `wlan2` | Client Mode — upstream AP connection for internet | 2.4 / 5 GHz |
| `wlan3` | **AWUS036ACM** — 5 GHz monitor, injection, handshake capture | **5 GHz** |

> **Note**: The PineAP Web UI in Firmware 2.x primarily manages built-in radios. AWUS036ACM 5 GHz scanning must be configured via CLI (SSH) or automated with the startup script from Step 7.

---

## 7. Validation Results

All tests performed on MK7 Firmware 2.1.3 with a genuine ALFA AWUS036ACM:

| Test | Command | Result |
|---|---|---|
| USB device detection | `lsusb \| grep 7612` | ✅ PASS |
| Driver module loaded | `lsmod \| grep mt76x2u` | ✅ PASS |
| Interface appears (wlan3) | `iw dev` | ✅ PASS |
| Monitor mode enabled | `airmon-ng start wlan3` | ✅ PASS |
| 5 GHz channel switch | `iw wlan3mon set channel 36` | ✅ PASS (channels 36–165) |
| 5 GHz AP scan | `airodump-ng --band a wlan3mon` | ✅ PASS |
| Packet injection | `aireplay-ng --test wlan3mon` | ✅ PASS |
| WPA handshake capture | `airodump-ng -c 36 wlan3mon` | ✅ PASS (EAPOL captured) |
| Power stability | Continuous scan, 30 minutes | ✅ PASS (no disconnects) |
| LED indicator | Visual check | ℹ️ Expected (driver design) |

---

## 8. Recommendation

**The ALFA AWUS036ACM is the best currently-available adapter for extending the WiFi Pineapple Mark VII to 5 GHz.**

It shares the exact MT7612U chipset with Hak5's own MK7AC Adapter, uses an in-kernel driver with zero compilation, draws well within the MK7's USB power budget, and supports the full penetration testing toolkit: monitor mode, packet injection, and handshake capture across all 5 GHz channels.

**Buy the AWUS036ACM from Yupitek:**

👉 [ALFA AWUS036ACM Product Page](/en/products/alfa/awus036acm/)

We are an authorized ALFA Network distributor and provide full technical support for all ALFA × HAK5 integration scenarios. Browse our complete [ALFA adapter lineup](/en/products/alfa/) to find the right tool for your testing needs.

**Related resources from Yupitek:**
- [AWUS036ACH vs AWUS036ACM — Full Comparison for Kali Linux](/en/blog/awus036ach-vs-awus036acm/)
- [Best WiFi Adapter for Kali Linux in 2026](/en/blog/best-wifi-adapter-kali-linux-2026/)
- [Enable Monitor Mode on Kali Linux — Complete Guide](/en/blog/enable-monitor-mode-kali-linux/)

**External references:**
- [Hak5 Official Documentation — Compatible 802.11ac Adapters](https://documentation.hak5.org/wifi-pineapple/faq/compatible-802.11ac-adapters)
- [OpenWrt mt76 Driver Repository](https://github.com/openwrt/mt76)
- [morrownr USB-WiFi Compatibility List](https://github.com/morrownr/USB-WiFi)

---

*Need help with your setup? Contact Yupitek technical support at [yupitek.com/support](/en/support/).*
