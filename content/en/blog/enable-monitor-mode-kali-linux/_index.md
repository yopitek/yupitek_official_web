---
title: "How to Enable Monitor Mode on Kali Linux 2026: Complete WiFi Adapter Guide"
description: "Step-by-step guide to enabling monitor mode on Kali Linux 2024/2025 using airmon-ng or iw command. Covers compatible ALFA adapters, troubleshooting, and verification with airodump-ng."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["monitor-mode", "kali-linux", "airmon-ng", "iw", "wifi-adapter", "ALFA-Network"]
---

## What Is Monitor Mode and Why It Matters for Pentesting

Monitor mode is a special operating mode for wireless network interface cards (NICs) that allows the adapter to capture **all** 802.11 frames in the air — not just those addressed to your device. In normal "managed" mode, your adapter only receives packets destined for its MAC address and discards everything else. Monitor mode lifts that filter entirely.

For wireless penetration testers, monitor mode is foundational. Without it, tools like **airodump-ng**, **Wireshark** (in wireless capture mode), or **Kismet** cannot passively intercept network traffic. Monitor mode enables:

- **Passive reconnaissance** — Scanning all nearby access points and clients without transmitting any frames.
- **Handshake capture** — Listening for WPA/WPA2 4-way handshakes during client authentication.
- **Deauthentication attacks** — Sending 802.11 management frames (requires packet injection in addition to monitor mode).
- **Rogue AP detection** — Identifying unauthorized access points on a network.
- **Protocol analysis** — Deep inspection of 802.11 management, control, and data frames.

Not every wireless adapter supports monitor mode. The capability is determined by the **chipset** and the **driver** compiled into the kernel. Consumer-grade adapters sold for home use are almost never compatible. Adapters specifically marketed for security research — such as the ALFA Network line — are built with chipsets and drivers that expose monitor mode cleanly.

---

## Prerequisites

Before enabling monitor mode, confirm the following:

1. You are running **Kali Linux** (2024.1 or later recommended) with a compatible kernel.
2. Your wireless adapter is plugged in (USB adapters) or installed (PCIe/mini-PCIe).
3. You have **root or sudo** privileges.
4. You have identified your interface name: run `ip link` or `iwconfig` and note the wireless interface (commonly `wlan0`, `wlan1`, or `wlx...`).

```bash
ip link show
```

Look for an entry that starts with `wlan` or has a long MAC-based name beginning with `wlx`.

---

## Method 1: Enable Monitor Mode with airmon-ng

`airmon-ng` is part of the **aircrack-ng** suite and is the most common tool used to toggle monitor mode on Kali Linux. It handles many edge cases automatically, including stopping processes that interfere with the mode switch.

### Step 1 — Kill interfering processes

NetworkManager, wpa_supplicant, and dhclient all compete with monitor mode. Kill them first:

```bash
sudo airmon-ng check kill
```

> **Why this step?** NetworkManager and wpa_supplicant hold an exclusive lock on WiFi interfaces. Without terminating them first, the mode switch appears to succeed but silently fails — your interface stays in managed mode. Always kill these processes before switching modes.

Expected output:

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **Note:** This will drop your existing network connections. If you need internet access during the test, use a wired connection or a second wireless adapter in managed mode.

### Step 2 — Start monitor mode

```bash
sudo airmon-ng start wlan0
```

Expected output:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

The adapter is now in monitor mode and a new virtual interface — typically **wlan0mon** — has been created.

### Step 3 — Specify a channel (optional but recommended)

By default, the adapter hops across channels. Lock it to a specific channel for targeted capture:

```bash
sudo iwconfig wlan0mon channel 6
```

---

## Method 2: Enable Monitor Mode with iw

The `iw` command is the modern low-level wireless configuration utility. This method gives you more direct control and is useful when `airmon-ng` is unavailable or misbehaving.

```bash
# Bring the interface down
sudo ip link set wlan0 down

# Set monitor mode
sudo iw dev wlan0 set type monitor

# Bring the interface back up
sudo ip link set wlan0 up
```

All three commands chained:

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

This modifies the existing `wlan0` interface in place rather than creating a new `wlan0mon` interface. Verify the change was applied:

```bash
iw dev wlan0 info
```

Look for `type monitor` in the output.

---

## Verifying Monitor Mode

### Using iwconfig

```bash
iwconfig
```

A monitor-mode interface will show:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

The key field is **Mode:Monitor**.

### Using iw dev

```bash
iw dev
```

Look for `type monitor` under your interface entry. If it shows `type managed`, monitor mode was not applied successfully.

---

## Testing with airodump-ng

Once monitor mode is active, test it end-to-end with `airodump-ng`:

```bash
sudo airodump-ng wlan0mon
```

You should immediately see a live list of nearby access points scrolling on screen, showing BSSID, channel, signal strength (PWR), encryption type, and ESSID. If the screen is blank or shows an error, refer to the troubleshooting section below.

To scan only the 5 GHz band:

```bash
sudo airodump-ng --band a wlan0mon
```

To capture a specific network and save the output for later analysis:

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## ALFA Adapter Compatibility Table

[ALFA Network](/en/products/alfa/) adapters are the industry standard for Kali Linux wireless testing. The following models fully support monitor mode:

| Model | Chipset | Band | Monitor Mode | Injection | Notes |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ | ✅ | Most popular for pentesting |
| AWUS036AXML | MT7921AUN | 2.4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E, kernel 5.18+ required |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ | ✅ | Excellent Linux driver support |
| AWUS036NHA | AR9271 | 2.4 GHz | ✅ | ✅ | Classic 2.4 GHz workhorse |
| AWUS036NH | RTL8187 | 2.4 GHz | ✅ | ✅ | Long-range with high-gain antenna |
| AWUS1900 | RTL8814AU | 2.4 / 5 GHz | ✅ | ✅ | 4×4 MIMO, maximum signal capture |

All models listed above have verified driver support in Kali Linux 2024.x and 2025.x. For chipsets like RTL8812AU and RTL8814AU, you may need to install the driver from the Aircrack-ng GitHub repository if your kernel version is very recent.

---

## Troubleshooting

### "Cannot enable monitor mode" or interface disappears

This usually happens when NetworkManager reclaims the interface. Run `airmon-ng check kill` again, then retry. If the problem persists, manually stop NetworkManager:

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### Monitor mode reverts to managed mode

Some drivers reset to managed mode automatically after a few seconds. This typically means wpa_supplicant restarted in the background. Check running processes:

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

Kill any found processes by PID, then re-enable monitor mode.

### Interface name is different after airmon-ng

On some systems, the new interface may be named `wlan0mon`, `mon0`, or something else entirely. Always check with `iwconfig` or `iw dev` after running `airmon-ng start` to confirm the actual interface name before using it with airodump-ng.

### "Fixed channel wlan0mon: -1" error in airodump-ng

This means airodump-ng cannot change channels. The most common cause is a regulatory domain restriction. Fix:

```bash
# Set a permissive regulatory domain (for authorized testing environments only)
sudo iw reg set BO
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
```

If that fails, kill any remaining wpa_supplicant processes and retry.

```bash
sudo iwconfig wlan0mon channel 1
```

### RTL8812AU driver issues on newer kernels

The in-kernel RTL8812AU driver on very recent kernels sometimes lacks full monitor mode support. Install the community driver:

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Reboot after installation.

---

## Disabling Monitor Mode When Done

Always restore your adapter to managed mode when you finish testing. Leaving it in monitor mode prevents normal network connectivity.

### With airmon-ng:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### With iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

Verify the interface is back in managed mode with `iwconfig` and reconnect to your network.

---

## Summary

Enabling monitor mode on Kali Linux is a two-step process: stop interfering services, then switch the interface mode using either `airmon-ng` or `iw`. The key to success is using an adapter with a supported chipset. ALFA Network adapters with RTL8812AU, MT7921AUN, MT7612U, AR9271, and RTL8814AU chipsets provide the most reliable out-of-the-box experience on Kali Linux.

Browse the full range of [ALFA Network wireless adapters available from Yopitek](/en/products/alfa/) — Taiwan's authorized ALFA Network distributor — to find the right adapter for your wireless security research.
