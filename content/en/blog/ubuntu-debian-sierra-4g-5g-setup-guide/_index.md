---
title: "Complete Guide to Installing Sierra 4G/5G Modules on Ubuntu / Debian / Linux Mint: EM7455, EM7565, EM919x, MC7455 Setup and GNSS Positioning"
description: "How do you install a Sierra 4G/5G module on Ubuntu/Debian/Linux Mint? This guide walks you through installing ModemManager, dialing in with qmicli/mbimcli, and setting up GNSS positioning. Covers EM7455, EM7565, EM919x, and MC7455."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/en/products/sierra/"
faq:
  - question: "Can Ubuntu use a Sierra 4G/5G module to get online directly?"
    answer: "Yes. Install the modemmanager, libqmi-utils, and related packages, then enter your APN in NetworkManager and you are online."
  - question: "How do I enable GNSS positioning for a Sierra module on Linux?"
    answer: "Use ModemManager commands: first run mmcli -m 0 --location-enable-gps-raw, then retrieve coordinates with --location-get. Make sure the GNSS antenna is connected."
---

Want to install a Sierra Wireless module (EM7455, EM7565, MC7455, EM919x) on Ubuntu, Debian, or Linux Mint? Linux supports these devices natively. You just need to know which packages to install, such as ModemManager and libqmi-utils. This article covers everything step by step, from wiring up the hardware and installing drivers, to dialing in and going online, and finally turning on the GNSS positioning feature. Whether you are building a drone or an industrial computer, following along will get you there.

{{< tldr >}}
Want to install a Sierra Wireless module (EM7455, EM7565, MC7455, EM919x) on Ubuntu, Debian, or Linux Mint? Linux supports these devices natively. Just install the right packages, ModemManager and libqmi-utils. From wiring up the hardware and installing drivers to dialing in and enabling GNSS positioning, following along works for both drones and industrial computers.
{{< /tldr >}}

**In one sentence: installing these Sierra modules on Linux is straightforward. Install `modemmanager` and the related tools with `apt`, connect through NetworkManager, and you can even read out GPS positions without breaking a sweat.**

Many people receive an EM7455, EM7565, EM919x, or MC7455, plug it into the motherboard, and then have no idea how to get online. In fact, support for these modules on Linux is very mature. They all communicate over USB using the QMI or MBIM protocols. In this guide we walk you through the setup one step at a time.

> All specifications and technical references come from the Sierra Wireless official documentation. Compiled by Yupitek.

---

## Before You Start: Know Your Hardware

If the hardware is wrong, no amount of software commands will help.

| Module | Form Factor | Speed Class | Main Linux Protocol | Antenna Count |
|---|---|---|---|---|
| **EM7455** | M.2 (42mm long) | Cat 6 (300/50 Mbps) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (42mm long) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (**52mm** long) | 5G NR / LTE Cat 20 | MBPW and other broadband packages | 4 or more |
| **MC7455** | mPCIe (legacy slot) | Cat 6 (300/50 Mbps) | QMI | 3 U.FL connectors |

**Two hardware gotchas to remember:**
1. **The EM919x is longer**: at 52mm it will not fit a 42mm slot. Forcing it in will damage the board.
2. **No antenna, no signal**: at minimum, connect the main antenna (Main). If you want positioning, buy a GPS antenna and plug it into the dedicated **GNSS connector**.

---

## Step 1: Install the Essential Linux Tools

On Ubuntu / Debian / Linux Mint you do not need to write or compile any drivers yourself. The package repositories have everything ready.

Open a terminal and run these two lines:
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
After the install, confirm the service is running:
```bash
systemctl status ModemManager
```
With these tools in place, your Linux system can now understand this 4G/5G card.

---

## Step 2: Confirm the System Sees the Card

With the card installed and the machine booted, run these three commands to check:

1. **Check the USB hardware:**
   ```bash
   lsusb
   ```
   (You should see a Sierra or Qualcomm device.)

2. **Check the kernel driver:**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (Seeing `cdc-wdm0` and `wwan0` means the interface mounted successfully.)

3. **Check the ModemManager state:**
   ```bash
   mmcli -L
   ```
   (This lists the modems with their numbers. Note the number down, usually `0`.)

---

## Step 3: Dialing In the Easy Way (with NetworkManager)

If you run the desktop edition of Ubuntu or Mint, the built in network manager is the most convenient option.

```bash
# Create a connection (replace "internet" with your carrier's APN)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# Bring it up!
nmcli connection up mobile
```
That is all it takes. You can verify that `wwan0` received an IP with `ip addr show`.

### (Advanced) Text Mode Connection Without a Desktop
On a headless server or an embedded board, you can drive the module directly with `qmicli`:
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## Step 4: Turn On GPS Positioning!

These modules all come with a built in GNSS positioning system (supporting GPS, GLONASS, and more).
According to the official specifications:
- EM7455 / EM7565 / MC7455: 1 second hot start, 32 seconds cold start. Horizontal accuracy around 2 to 5 meters.
- The 5G EM919x: faster cold start (≤28 seconds) with slightly better accuracy (<4m at 95%).

**To grab coordinates on Linux, this is the fastest way:**

1. Enable the GPS feature:
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. Fetch the current coordinates:
```bash
mmcli -m 0 --location-get
```
Your current latitude and longitude will print right out. If you want to stream the position to other programs in real time, pair it with `gpsd`.

---

## Common Pitfalls and Quick Fixes

1. **`mmcli -L` shows nothing**: `ModemManager` may have crashed, or your USB power delivery simply cannot drive the card.
2. **GPS positioning keeps failing**: did you plug the GPS antenna into Main or Aux? The GNSS port is a dedicated connector!
3. **The EM919x will not reach full speed**: it is a 5G card that supports USB 3.1 Gen 2 and even PCIe Gen 3. If you plug it into a USB 2.0 port, the vendor does not guarantee performance.

## Conclusion

Working with Sierra modules on Linux is not as hard as it seems. Confirm the hardware slot and antennas, install the `modemmanager` family of packages, set the APN, and you are online. This workflow fits engineers working on edge computing or industrial IoT (IIoT) perfectly.

## Where to Buy (Call To Action)

Want to integrate a Sierra module into your Ubuntu device? Yupitek offers complete module, antenna, and adapter board solutions, plus first line technical support.
Contact us: **sales@yupitek.com**
Browse the range: [Sierra Wireless Series](https://yupitek.com/en/products/sierra/)

{{< faq >}}
