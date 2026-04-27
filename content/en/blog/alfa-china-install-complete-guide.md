---
title: "Complete Guide: Installing All Alfa USB WiFi Adapters on Linux in China - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
description: "The ultimate guide to installing all Alfa USB WiFi adapters on Linux in China. Covers Kali Linux, Ubuntu 22/24, Debian, and Raspberry Pi. No GitHub needed - use domestic mirrors only."
---

## Welcome to the Ultimate Alfa Linux Installation Guide

If you're reading this, you probably bought an Alfa USB WiFi adapter and found yourself stuck because:

- You're in China and can't access GitHub
- The driver installation seems complicated
- You need to enable monitor mode and packet injection for wireless testing
- You're not sure which driver your specific Alfa model needs

This guide solves **all of those problems**. We'll walk you through installing **every Alfa USB WiFi adapter** on **all major Linux distributions**, using only **China-accessible mirrors**. No GitHub. No frustration.

---

## Why This Guide Exists

Alfa USB WiFi adapters are popular among penetration testers, network engineers, and wireless enthusiasts. They support monitor mode and packet injection — features most consumer WiFi adapters don't have.

But here's the problem: **Most driver installation guides assume you can access GitHub**. If you're in China, that's not possible. This guide is specifically designed for Chinese users, using only mirrors and resources that work within China's internet infrastructure.

---

## Quick Model Reference

Before we dive in, let's figure out which Alfa adapter you have and what chip it uses:

### AX Series (Wi-Fi 6 / 802.11ax)

| Model | Chipset | Driver | Best For |
|-------|---------|--------|----------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | General use, good range |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Compact design |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | Ultra-compact |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | Enhanced power |

### AC Series (Wi-Fi 5 / 802.11ac)

| Model | Chipset | Driver | Best For |
|-------|---------|--------|----------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | High power, great range |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Best VIF support**, plug-and-play |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | Budget-friendly |

### Which Adapter Do You Have?

1. Look at the label on your adapter
2. Check the box it came in
3. If you bought it online, check your order history

Once you know your model, jump to that section below or follow the general workflow.

---

## Before You Start: What You Need

Make sure you have these ready before beginning:

1. **Alfa USB WiFi adapter** — The correct model for your needs
2. **USB cable** — The one that came in the box works fine
3. **Powered USB hub** — Required if you're on Raspberry Pi
4. **Active internet connection** — To reach domestic mirrors in China
5. **Sudo privileges** — You'll need admin access to install drivers

Plug in the adapter first to verify your system sees it:

```bash
lsusb
```

Look for your adapter's vendor ID in the output:

- **Alfa adapters** show up as `0e8d` (MediaTek) or `0bda` (Realtek)
- Example: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- Example: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

If you see the ID, your adapter is detected. Move to the driver installation section below.

If you don't see it, try a different USB port, swap the cable, then run `lsusb` again.

---

## Choose Your Operating System

Jump to the right section for your OS:

- [Kali Linux](#kali-linux-installation)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404-installation)
- [Debian 12 (Bookworm)](#debian-12-bookworm-installation)
- [Raspberry Pi OS (64-bit)](#raspberry-pi-os-installation)

Already have the driver installed? Skip to the advanced sections:

- [Enable Monitor Mode](#enable-monitor-mode-on-any-adapter)
- [Test Packet Injection](#test-packet-injection)
- [Virtual Interface (VIF) Support](#virtual-interface-vif-support)
- [VM USB Passthrough](#virtual-machine-usb-passthrough)

---

## China-Accessible Mirror Reference

All resources in this guide use these China-accessible mirrors:

| Resource | URL | Use For |
|----------|-----|---------|
| **Alfa official downloads** | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages, firmware |
| **Alfa documentation** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Product manuals, English |
| **清华大学镜像 (Tsinghua)** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里云镜像 (Aliyun)** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommended) |
| **中科大镜像 (USTC)** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommended) |
| **华为云镜像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM images (backup) |
| **Gitee (GitHub alternative)** | [gitee.com](https://gitee.com) | Driver source code |

---

## Kali Linux Installation

Kali Linux comes with wireless tools pre-installed. Getting Alfa adapters working takes just a few steps.

### Step 1: Switch to China Mirror

Open your sources list:

```bash
sudo nano /etc/apt/sources.list
```

Replace everything with this:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save: **Ctrl+O**, Enter, then **Ctrl+X**. Refresh:

```bash
sudo apt update
```

> **Backup mirror:** If 中科大 (USTC) is slow, use 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### Step 2: Install Driver by Chipset

#### AX Series (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC Series - Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC Series - MediaTek (MT7612U)

The MT7612U driver is built into the Kali kernel. Verify it loaded:

```bash
lsmod | grep mt76
```

If you see `mt76x2u`, you're done. If not:

```bash
sudo modprobe mt76x2u
```

### Step 3: Verify Driver Loaded

Run `lsusb` again. Your adapter should show up. Then check wireless interfaces:

```bash
iwconfig
```

Look for `wlan0` or `wlan1`. If the interface appears, the driver is working.

### Step 4: Enable Monitor Mode

Stop interfering processes:

```bash
sudo airmon-ng check kill
```

Start monitor mode:

```bash
sudo airmon-ng start wlan0
```

Verify:

```bash
iwconfig
```

Look for `wlan0mon` with `Mode:Monitor`. Done!

---

## Ubuntu 22.04 / 24.04 Installation

### Step 1: Switch to China Mirror

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Replace with:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Save with **Ctrl+O**, exit with **Ctrl+X**.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Replace with:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Save and exit.

#### Refresh package index

```bash
sudo apt update
```

### Step 2: Install Build Dependencies

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Step 3: Install Driver

#### AX Series (RTL8832BU)

Clone from Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC Series - Realtek (RTL8812AU)

Clone from Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC Series - MediaTek (MT7612U)

The driver is built into the Ubuntu kernel. Load it:

```bash
sudo modprobe mt76x2u
```

### Step 4: Enable Monitor Mode

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Look for `wlan0mon` with `Mode:Monitor`.

---

## Debian 12 (Bookworm) Installation

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Replace with:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Save and exit. Refresh:

```bash
sudo apt update
```

### Step 2: Install Non-Free Firmware

```bash
sudo apt install -y firmware-misc-nonfree
```

### Step 3: Install Build Dependencies

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Step 4: Install Driver

#### AX Series (RTL8832BU)

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### AC Series - Realtek (RTL8812AU)

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### AC Series - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Step 5: Install Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### Step 6: Enable Monitor Mode

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Look for `wlan0mon` with `Mode:Monitor`.

---

## Raspberry Pi OS Installation

> **IMPORTANT:** The AWUS036ACH draws ~500mW. The AWUS036ACM draws ~400mW. **Always use a powered USB hub** to prevent the Pi from throttling or crashing under load.

### Step 1: Download Kali Linux ARM64 Image

Go to: https://www.kali.org/get-kali/#kali-arm

Pick **Raspberry Pi 4 (64-bit)** or **Raspberry Pi 5 (64-bit)**. Do NOT use 32-bit — 64-bit is required.

> **China mirror:** If kali.org is slow, use 华为云: https://repo.huaweicloud.com/kali-images/

### Step 2: Flash to MicroSD

Check your SD card's device path:

```bash
lsblk
```

Flash the image (replace `/dev/sdX` with your actual card):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Wait for `sync` to complete. Boot the Pi. Default credentials: **kali / kali**.

### Step 3: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Replace with:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save and apply:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Step 4: Install Driver

#### AX Series (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### AC Series - Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### AC Series - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Step 5: Enable Monitor Mode

On a Pi with built-in Wi-Fi, the Alfa adapter shows as `wlan1`:

```bash
iwconfig
```

Then:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

Look for `wlan1mon` with `Mode:Monitor`.

---

## Enable Monitor Mode on Any Adapter

Once the driver is installed, monitor mode is easy to enable:

### Step 1: Check Your Interface Name

```bash
iwconfig
```

Note whether it's `wlan0` or `wlan1`.

### Step 2: Kill Interfering Processes

```bash
sudo airmon-ng check kill
```

### Step 3: Start Monitor Mode

```bash
sudo airmon-ng start wlan0
```

Replace `wlan0` with your actual interface name if it's different.

### Step 4: Verify

```bash
iwconfig
```

Look for your interface ending in `mon` (like `wlan0mon`) with `Mode:Monitor`.

---

## Test Packet Injection

This confirms your adapter can send crafted packets — essential for wireless testing.

```bash
sudo aireplay-ng --test wlan0mon
```

**Success looks like:**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**If it fails:**
- Reboot and try again
- Confirm no other process holds the interface (`iwconfig`)
- Move closer to a WiFi AP for the test
- Ensure you're using `wlan0mon`, not `wlan0`

---

## Virtual Interface (VIF) Support

VIF (Virtual Interface Functionality) lets you run multiple interfaces on one adapter simultaneously. For example:

- **Managed mode** (`wlan0`) + **Monitor mode** (`mon0`) at the same time
- Run while staying connected to a network AND capturing traffic

### Which Adapters Support VIF?

| Chipset | VIF Support | Notes |
|---------|-------------|-------|
| **MT7612U (AWUS036ACM)** | ✅ Full native support | Best choice for VIF workflows |
| **RTL8812AU (AWUS036ACH)** | ⚠️ Limited | Cannot run managed + monitor simultaneously |
| **RTL8832BU (AX series)** | ⚠️ Limited | Check specific model docs |

### Creating a Virtual Interface (MT7612U)

If you have the AWUS036ACM (MT7612U):

```bash
# Create monitor interface while wlan0 stays in managed mode
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Verify both interfaces are active:

```bash
iwconfig
```

You should see:
- `wlan0` — managed mode (associated to AP)
- `mon0` — monitor mode (capturing all traffic)

### Use Cases

**Capture traffic while staying connected:**

```bash
sudo airodump-ng mon0
```

Your `wlan0` continues normal operation while `mon0` captures everything.

**Fake AP + Monitor:**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## Virtual Machine USB Passthrough

Running Linux inside a VM? You need to pass the USB adapter through to the guest.

### VirtualBox

1. Power off the VM
2. Go to **Settings → USB**
3. Enable **USB 3.0 (xHCI) Controller**
4. Click **+** to add a USB filter
5. Select your Alfa adapter (ID: `0bda:8812` or `0e8d:7612`)
6. Start the VM

Inside the VM, run `lsusb` to confirm, then follow the Kali Linux steps above.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Start the VM
2. Menu: **Virtual Machine → USB & Bluetooth**
3. Find your Alfa adapter and click **Connect**
4. The adapter appears inside the VM

Run `lsusb` to confirm, then follow the driver installation steps.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show adapter ID | Bad cable or no power | Try different USB port. Use powered hub on Pi. |
| `modprobe` says "Module not found" | Missing kernel modules | Run `sudo apt install linux-modules-extra-$(uname -r)` |
| Driver works but won't switch to monitor mode | NetworkManager interfering | Run `sudo airmon-ng check kill` first |
| Monitor mode starts but captures nothing | Wrong interface or channel | Run `iwconfig`. Set channel: `iwconfig wlan0mon channel 6` |
| Injection test fails | Using wrong interface | Use `wlan0mon`, not `wlan0` |
| VIF creation fails | Driver not fully loaded | Unplug and replug adapter, or reload module |

---

## Appendix: Complete Alfa Model List

| Model | Chipset | Driver | China Mirror Source |
|-------|---------|--------|---------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | Built-in kernel driver |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## Final Notes

This guide covers **all Alfa USB WiFi adapters** on **all major Linux distributions**, using **only China-accessible resources**. You should now be able to:

✅ Install drivers for any Alfa adapter  
✅ Enable monitor mode on Kali, Ubuntu, Debian, or Raspberry Pi  
✅ Test packet injection  
✅ Use virtual interfaces (VIF) with supported models  
✅ Pass adapters through to VMs  

**Questions or issues?** Check out the specific model guides in our series, or contact us at [yupitek.com](https://yupitek.com/en/contact/).

---

## Related Guides

This is part of the **Alfa China Install Guide** series:

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, best VIF support
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/) — RTL8811AU, budget option
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/) — Wi-Fi 6, RTL8832BU
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — Wi-Fi 6, compact design
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/) — Wi-Fi 6, ultra-compact
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/) — Wi-Fi 6, enhanced power
- [AWUS036EAC China Install Guide](/en/blog/awus036eacs-china-install-guide/) — RTL8814AU, high power

---

*Last updated: April 24, 2026*
