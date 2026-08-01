---
title: "Building a 4G/5G Router with Raspberry Pi and OpenWrt: Sierra Module Support Matrix and Setup Guide"
description: "Build your own OpenWrt router with a Raspberry Pi and Sierra Wireless 4G/5G modules (EM7455, EM7565, EM7511, EM919x, MC7455). Complete support matrix, QMI/MBIM configuration, wwan0 internet setup, plus power and antenna guidelines."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/en/products/sierra/"
faq:
  - question: "Which Sierra module should I pick for an OpenWrt router on a Raspberry Pi?"
    answer: "Beginners should start with the EM7455 because tutorials are abundant and issues are easy to research. Choose the EM7565 or EM7511 for high upload throughput, the EM919x for 5G, and the MC7455 for legacy mPCIe slots."
  - question: "What is the difference between QMI and MBIM?"
    answer: "QMI is Qualcomm's protocol, while MBIM is the later standardized protocol. Both work on OpenWrt, but most online guides use QMI."
  - question: "What should I do if the Raspberry Pi does not detect the module?"
    answer: "The most common cause is insufficient USB power on the Raspberry Pi (peak inrush current can reach 2.5A). Check the adapter board power delivery and cabling, and wait about ten seconds for the module to finish booting."
---

Can a Raspberry Pi turn a Sierra Wireless 4G/5G module into a fully working OpenWrt router? Yes, it can. M.2 modules such as the EM7455, EM7565, EM7511, and EM919x are natively supported in Linux. Install `kmod-usb-net-qmi-wwan` or `kmod-usb-net-cdc-mbim`, configure `wwan0`, and you are online. This article covers the full module support matrix, step by step configuration, and the power and antenna pitfalls to avoid.

{{< tldr >}}
A Raspberry Pi with a Sierra 4G/5G module makes a reliable OpenWrt router. Most M.2 modules (EM7455, EM7565, EM7511) use USB, the EM919x adds a PCIe Gen3 lane, and the MC7455 is the mPCIe version of the EM7455. On OpenWrt, the QMI protocol with `wwan0` is the recommended path: install `kmod-usb-net-qmi-wwan`, `uqmi`, and `luci-proto-qmi`, set the APN in `/etc/config/network`, then restart networking. On speed: EM7455 / MC7455 are LTE Cat 6 (300/50 Mbps), EM7565 / EM7511 are Cat 12 (600/150 Mbps), and the EM919x family delivers 5G Sub-6 (EM9190 adds mmWave).
{{< /tldr >}}

## Complete Sierra Module Support Matrix on OpenWrt

Before you start, check your module against this table:

| Model | Speed Class | Baseband Chip | Form Factor | Linux Data Path | GNSS Positioning |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (both on Linux) | adds QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | adds QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (9190 adds mmWave) | SDX55 | M.2 (52mm length) | Windows/Linux | L1 + L5 (optional) |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50.95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### How to Choose a Module

- **Makers getting started**: pick the **EM7455**. Guides are plentiful and problems are easy to research.
- **High upload demand (live streaming, surveillance)**: pick the **EM7565** or **EM7511** for up to 150 Mbps upload.
- **5G required**: pick the **EM9190** for 5G speeds.
- **Legacy mPCIe slot only**: go with the **MC7455**.

## Three Ways to Connect the Hardware

### A. Raspberry Pi 5 + M.2 HAT (PCIe)

The Pi 5 has PCIe, so an M.2 HAT+ carrier board lets you plug in an M.2 WWAN module directly (confirm it is a B-Key).

### B. Raspberry Pi 4B or Older + USB WWAN Adapter Enclosure

EM-series modules also support USB 2.0/3.0, so an M.2 to USB enclosure (usually with a built in SIM slot) plugged into the Pi's USB port is the simplest, most approachable route.

### C. MC7455 (mPCIe) Adapter

The MC7455 uses the older mPCIe interface, so you need an mPCIe to USB or mPCIe to M.2 adapter board.

> ⚠️ **Power is the biggest trap**: the module draws 3.135 to 4.4 V (typically 3.3V). A "module not detected" error usually means the Raspberry Pi's USB supply cannot deliver enough power. Inrush current can spike to 2.5A, so leave generous headroom on your power source.

## Understanding QMI and MBIM

Both protocols control how the 4G/5G module connects to the network:

- **QMI**: Qualcomm's own protocol, used by most Linux/OpenWrt guides (the interface appears as `wwan0`).
- **MBIM**: the later standardized protocol, usable on both Windows and Linux (the interface also appears as `wwan0`).

**Which one?** Most users can use QMI directly. Switch to MBIM only if your firmware specifically requires it.

## Hands On Part 1: Configure QMI on OpenWrt

Four steps, no compilation required.

### 1. Install the Packages

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Confirm the Raspberry Pi Detects the Module

```bash
lsusb                                  # look for a Sierra device
ls /dev/cdc-wdm*                       # QMI control channel
dmesg | grep qmi_wwan                  # check that the driver loaded
ip link show wwan0                     # check that the interface appeared
```

### 3. Configure the Network File (`/etc/config/network`)

Add a QMI section and replace the APN with your carrier's:

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. Restart Networking

```bash
/etc/init.d/network restart
ifup wwan
```

Done. Once `wwan0` obtains an IP address, you are online.

## Antennas and SIM: Do Not Skip These

The module has **no built in antenna**, and antenna quality directly drives your throughput.

- **Main antenna**: mandatory.
- **Auxiliary antenna (Aux)**: required for MIMO speeds; skipping it cuts throughput.
- **GNSS antenna**: only for positioning use cases. Do not confuse it with the main antenna.

## Common Pitfalls (A Must Read for Beginners)

1. **`lsusb` shows nothing**: 99% of the time this is insufficient power, a loose adapter board, or a faulty cable.
2. **Too impatient**: the module needs time to boot. Wait 10 seconds after plugging it in before issuing commands.
3. **5G modules (EM919x) run hot**: temperatures around 100°C are common (115°C max), so plan for cooling.
4. **ModemManager conflicts**: when working manually on a stock Linux system, stop `ModemManager` (`systemctl stop ModemManager`) first so it does not take over the module.

## Summary

Driving a Sierra module from a Raspberry Pi with OpenWrt is a checklist process. Verify the hardware (form factor, voltage, antennas), install the QMI/MBIM drivers, then set the APN. We hope this guide saves your project a few detours and gets your Raspberry Pi up to full 4G/5G speed.

## Purchasing Information (Call To Action)

If you need EM7455, EM7565, EM7511 modules, or matching M.2 adapter boards and antennas, Yupitek offers complete hardware solutions and technical consultation.

Email us: **sales@yupitek.com**

Browse products: [Yupitek Sierra Wireless Series](https://yupitek.com/en/products/sierra/)
