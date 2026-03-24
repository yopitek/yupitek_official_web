---
title: "How to Install ALFA USB WiFi Driver on Kali Linux & Ubuntu 24.04 (2026)"
description: "Complete guide to installing ALFA Network USB WiFi adapter drivers on Kali Linux 2024 and Ubuntu 24.04 for RTL8812AU, MT7612U, and MT7921AUN chipsets, with troubleshooting tips."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["driver-install", "kali-linux", "ubuntu", "RTL8812AU", "MT7612U", "MT7921AUN", "ALFA-Network"]
---

Getting a USB WiFi adapter working on Linux often comes down to one thing: the driver. Unlike Windows, where manufacturers bundle drivers into executable installers, Linux uses kernel modules — compiled code that the operating system loads to communicate with hardware. Understanding this model makes troubleshooting straightforward and driver installation predictable.

This guide covers driver installation for every major ALFA Network USB WiFi adapter chipset on both Kali Linux 2024/2025 and Ubuntu 24.04 LTS.

---

## How USB WiFi Drivers Work on Linux

### Kernel Modules

A Linux WiFi driver is a **kernel module** — a `.ko` file loaded into the running kernel at boot time or on demand. When you plug in a USB device, the kernel reads its USB Vendor ID and Product ID, looks up a matching module in its database, and loads it automatically.

For common chipsets like the MediaTek MT7612U, this happens transparently: plug in the adapter, a module loads, an interface appears. For newer or less common chipsets, no in-tree module exists, and you must compile one from source.

### Out-of-Tree Drivers

When a driver isn't included in the mainline kernel (called an "out-of-tree" or "external" driver), you must:

1. Download the driver source code
2. Compile it against your running kernel's headers
3. Install the resulting `.ko` file into the kernel module directory
4. Load it with `modprobe`

The compilation step requires that your kernel headers are installed and match your running kernel exactly. This is the most common source of driver installation failures.

### DKMS: Dynamic Kernel Module Support

A plain `make install` compiles the driver for your current kernel. When Kali or Ubuntu updates the kernel — which happens regularly — the old driver no longer loads, and you must recompile.

**DKMS** solves this by registering the driver source code with a system daemon that automatically recompiles registered modules whenever a new kernel is installed. It's the recommended approach for any adapter requiring an out-of-tree driver.

---

## Identify Your Chipset

The driver you need depends entirely on your chipset, not the adapter's marketing name. Two adapters with the same name but different hardware revisions may use different chipsets.

### ALFA Model to Chipset Mapping

| ALFA Model | Chipset | USB IDs | Driver |
|---|---|---|---|
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACHM](/en/products/alfa/awus036achm/) | MT7610U | 0e8d:7610 | mt76x0u (in-kernel, EOL) |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u (in-kernel) |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK driver (<6.14) |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u (kernel 5.18+) |

### Identify Your Adapter with lsusb

Plug in your adapter and run:

```bash
lsusb
```

Sample output:

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
```

Cross-reference the `ID xx:xx` value against the table above to confirm your chipset.

---

## Prepare Your System

Regardless of which chipset you have, install the common build prerequisites first:

**Kali Linux:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

Confirm headers are installed for your exact running kernel:

```bash
uname -r
# Example: 6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# Should exist — if not, headers aren't installed
```

---

## RTL8812AU Driver (AWUS036ACH)

The RTL8812AU requires an out-of-tree driver. Two community-maintained forks exist; choose based on your OS.

### Option A: aircrack-ng/rtl8812au (Kali Linux — Recommended)

This fork is maintained by the Aircrack-ng team with explicit Kali compatibility and optimized packet injection support:

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

Verify the interface appeared:

```bash
ip link show | grep wlan
# Should show wlan0 or similar
```

### Option B: morrownr/8812au-20210708 (Ubuntu 24.04 — Recommended)

The morrownr fork is optimized for Ubuntu and includes a convenient install script with DKMS integration:

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

The install script handles DKMS registration automatically. After running it:

```bash
# Reboot to load the new module
sudo reboot

# After reboot, verify
lsmod | grep 8812au
```

### Manual DKMS Registration (Either Fork)

If you prefer manual control:

```bash
# Clone driver (use either fork)
git clone https://github.com/aircrack-ng/rtl8812au

# Get version from Makefile
grep "^MODULE_VERSION" rtl8812au/Makefile
# Note the version, e.g. v5.6.4.2 → use 5.6.4.2

# Copy source to DKMS directory
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# Register, build, install
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# Verify
dkms status
# Expected: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### Expected lsusb and lsmod Output

After successful installation:

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## MT7612U Driver (AWUS036ACM, AWUS036ACX)

The MT7612U chipset is the easiest of the four to get working because its driver has been part of the mainline Linux kernel since version **4.19**. On Kali Linux 2022+ and Ubuntu 20.04+, no driver installation is needed at all.

### Check Kernel Version

```bash
uname -r
```

If the output is 4.19 or higher (which it will be on any modern Kali or Ubuntu), the `mt76x2u` module is available.

### Load the Module

```bash
sudo modprobe mt76x2u
```

Verify it loaded:

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

A wireless interface should appear immediately:

```bash
ip link show
# wlan0: ...
```

### Make the Module Load at Boot

On most systems, the module loads automatically when the adapter is detected. To explicitly ensure it loads at boot:

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### No Compilation Needed

This is the major advantage of the MT7612U chipset: zero compilation, no driver source, no dependency on kernel headers. It works out of the box on every supported distribution. For users who don't want driver management hassle, the [AWUS036ACM](/en/products/alfa/awus036acm/) is the most plug-and-play pentesting adapter available.

---

## MT7921AUN Driver (AWUS036AXM, AWUS036AXML — Wi-Fi 6E)

The MT7921AUN is MediaTek's Wi-Fi 6E chipset. Its Linux driver, `mt7921u`, was merged into the mainline kernel in **version 5.18**.

### Check Kernel Version

```bash
uname -r
```

**Kali Linux 2022.2 and later** ships with kernel 5.18 or newer — supported.
**Ubuntu 22.04 LTS** ships with kernel 5.15 — **not supported** without a kernel upgrade.
**Ubuntu 24.04 LTS** ships with kernel 6.8 — fully supported.

### Load the Module (Kernel 5.18+)

```bash
sudo modprobe mt7921u
```

Verify:

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04: Kernel Upgrade Path

First, verify your currently running kernel version (important on HWE systems where the running kernel may differ from what you expect):

```bash
# Check running kernel
uname -r

# Verify matching headers are installed
dpkg -l | grep "linux-headers-$(uname -r)"
# If no output: sudo apt install linux-headers-$(uname -r)
```

If you're on Ubuntu 22.04 with kernel 5.15, you have two options:

**Option A: HWE Kernel** (recommended)

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

The HWE (Hardware Enablement) kernel for Ubuntu 22.04 is 6.2+, which supports mt7921u.

**Option B: Upgrade to Ubuntu 24.04**

Ubuntu 24.04 LTS ships with kernel 6.8 and full mt7921u support. This is the cleanest long-term solution.

### Wi-Fi 6E and Monitor Mode Status

As of 2026, the mt7921u driver provides stable support for managed mode (connecting to networks) on 2.4 GHz, 5 GHz, and 6 GHz bands. Monitor mode support on 2.4 and 5 GHz is functional. **6 GHz monitor mode** is still maturing — check the current status in the `mt76` kernel driver issue tracker before relying on it for 6 GHz assessments.

---

---

## DKMS: Keeping Drivers Working After Kernel Updates

Both Kali Linux and Ubuntu update the kernel regularly. Without DKMS, your out-of-tree drivers (RTL8812AU) stop working after a kernel update until you manually recompile.

With DKMS properly configured, the recompilation happens automatically during `apt upgrade`.

### Verify DKMS is Managing Your Driver

```bash
dkms status
```

Sample output showing properly managed drivers:

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### What Happens During a Kernel Update

```
apt upgrade
→ New kernel package downloaded
→ DKMS hook triggered
→ rtl8812au source recompiled for new kernel
→ New .ko installed
→ System reboots into new kernel
→ Driver loads automatically
```

If DKMS fails during an upgrade (visible via `dkms status` showing "built" but not "installed"), manually reinstall:

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---|---|---|
| No wlan interface after plugging in | Driver not loaded | `sudo modprobe 88XXau` or `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | Driver not compiled for current kernel | Recompile driver or run `sudo dkms install` |
| Interface appears but disappears after seconds | Power management interfering | `sudo iwconfig wlan0 power off` |
| `make` fails with "linux/module.h not found" | Kernel headers not installed | `sudo apt install linux-headers-$(uname -r)` |
| `make` fails with version mismatch | Headers don't match running kernel | `uname -r` vs `ls /lib/modules` — reinstall matching headers |
| Device shows in lsusb but no interface | Module loaded but interface not created | Check `dmesg \| tail -30` for errors |
| Monitor mode fails: "Operation not supported" | Driver version doesn't support monitor mode | Use aircrack-ng fork instead of distro-packaged driver |
| aireplay-ng injection test: 0% | Interface not in monitor mode | Verify with `iwconfig`, re-run `airmon-ng start` |
| Driver works but stops after reboot | Module not added to initramfs | `sudo update-initramfs -u` or use DKMS |
| DKMS build fails after kernel update | Missing headers for new kernel | `sudo apt install linux-headers-$(uname -r)` |

### Detailed Diagnostic Commands

```bash
# Check all loaded wireless modules
lsmod | grep -E "8812|8814|mt76|mt79"

# Check kernel messages for USB and wireless events
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# List all wireless interfaces
iw dev

# Check what driver a specific interface uses
ethtool -i wlan0 | grep driver

# Check USB device details
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# Verify DKMS status for all registered modules
dkms status
```

---

## Quick Reference: Which Driver for Which Adapter

| You have | Chipset | Kali/Ubuntu x86 | Raspberry Pi ARM |
|---|---|---|---|
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` (DKMS) | Manual DKMS + ARM headers |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | Built-in (`mt76x2u`) ✅ | Built-in — plug-and-play ✅ |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | N/A |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | Built-in (`mt7921u`, kernel 5.18+) | `linux-firmware` pkg |

---

## Ensure You're Getting Genuine Hardware

Driver issues are sometimes caused by counterfeit adapters that misreport their USB IDs or use inferior chipsets that don't match the stated model. Genuine ALFA Network adapters from authorized distributors behave exactly as documented.

Yopitek is an authorized ALFA Network distributor. Browse the full [ALFA Network product range](/en/products/alfa/) to ensure you're purchasing genuine hardware with manufacturer warranty and predictable driver compatibility.

---

## Summary

Linux WiFi driver installation follows a simple decision tree:

1. **Identify your chipset** with `lsusb` and the mapping table above
2. **MT7612U or MT7921AUN (on kernel 5.18+)?** → Just run `modprobe`, you're done
3. **RTL8812AU?** → Clone `aircrack-ng/rtl8812au`, run `make && sudo make install`, enable DKMS for persistence
4. **Something not working?** → Check the troubleshooting table, verify headers match kernel, check `dmesg`

The beauty of ALFA Network adapters is that all four major chipsets have well-documented, actively maintained driver solutions. You're never stuck in unsupported territory.
