---
title: "ALFA AWUS036AXML Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Step-by-step guide to install ALFA AWUS036AXML drivers in China using domestic mirrors. MT7921AUN WiFi 6E in-kernel driver, full monitor mode and VIF support. Covers Kali Linux, Ubuntu 22/24, Debian, and Raspberry Pi. No GitHub required."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 7
related_product: "/en/products/alfa/awus036axml/"
---

The AWUS036AXML is ALFA's WiFi 6E flagship — a tri-band USB-C adapter covering 2.4 GHz, 5 GHz, and the uncongested 6 GHz band. Its MT7921AUN chip uses the `mt7921u` driver, built into the Linux kernel since version 5.18. On Ubuntu 24.04 and Kali 2025 it is plug-and-play once the firmware package is installed from a domestic mirror. This guide covers the full setup — firmware, driver verification, monitor mode, packet injection, and VIF — without touching GitHub.

## Before You Start

Make sure you have these ready:

1. **ALFA AWUS036AXML** adapter and USB-C cable
2. A powered USB hub — required if you are on Raspberry Pi
3. Active internet connection to reach domestic mirrors

Plug in the adapter, then confirm your system sees it:

```bash
lsusb
```

Look for this in the output:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

If you see `0e8d:7961`, the adapter is detected. Move to your OS section below.

If you do not see it, try a different USB-C port or cable, then run `lsusb` again.

## Choose Your Operating System

Jump to the right section for your OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Already installed? Skip to:

- [Enable Monitor Mode](#enable-monitor-mode)
- [Test Packet Injection](#test-packet-injection)
- [Virtual Interface (VIF)](#virtual-interface-vif)
- [VM USB Passthrough](#virtual-machine-usb-passthrough)

---

## Kali Linux

The MT7921AUN driver is already in the Kali kernel. All you need is the MediaTek firmware package, available from domestic mirrors.

### Step 1: Switch to China Mirror

Open your sources list in the terminal.

```bash
sudo nano /etc/apt/sources.list
```

Delete whatever is there, then paste this line:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save: press **Ctrl+O**, then Enter, then Ctrl+X to exit. Refresh the package index.

```bash
sudo apt update
```

> **Backup mirror:** If 中科大 (USTC) is slow, use 清华 (Tsinghua) instead:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Step 2: Install Firmware

The MT7921AUN requires firmware blobs from `firmware-misc-nonfree` and `linux-firmware`. Without them the driver loads but the adapter fails to initialise.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Step 3: Verify the Driver

After reboot, plug in the adapter and check.

```bash
lsmod | grep mt7921
```

You should see `mt7921u` in the output. Then confirm a wireless interface appeared.

```bash
iwconfig
```

Look for `wlan0` or `wlan1`. If it appears, the driver is working.

---

### Step 4: Enable Monitor Mode {#enable-monitor-mode}

Check the interface name first.

```bash
iwconfig
```

Use the name you see (e.g. `wlan1`). Kill interfering processes, then switch to monitor mode.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

Confirm the switch.

```bash
iwconfig
```

Look for `Mode:Monitor` on the interface.

---

### Step 5: Test Packet Injection {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

A successful result:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

If it fails, reboot and try again.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — kernel 6.8, plug-and-play

Ubuntu 24.04 ships kernel 6.8, which includes the MT7921AUN driver natively.

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Delete everything and paste:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Save with `Ctrl+O`, then exit with `Ctrl+X`.

```bash
sudo apt update
```

### Step 2: Install Firmware

```bash
sudo apt install -y linux-firmware
sudo reboot
```

### Step 3: Verify and Enable Monitor Mode

After reboot, run `lsmod | grep mt7921` to confirm the driver loaded, then follow the Kali monitor mode steps above (Step 4).

---

### Ubuntu 22.04 (Jammy) — HWE kernel required

Ubuntu 22.04 ships kernel 5.15. The MT7921AUN driver requires kernel ≥ 5.18. Install the HWE kernel first.

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Replace all lines with:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Save and exit (`Ctrl+O`, then `Ctrl+X`).

```bash
sudo apt update
```

### Step 2: Install HWE Kernel

```bash
sudo apt install -y linux-generic-hwe-22.04
sudo reboot
```

After reboot, confirm kernel version:

```bash
uname -r
```

You should see 5.19 or higher. Then install firmware and enable monitor mode as above.

### Step 3: Install Firmware

```bash
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Delete everything and paste (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Save with `Ctrl+O`, then exit with `Ctrl+X`.

```bash
sudo apt update
```

### Step 2: Install Firmware

Debian 12 Bookworm ships kernel 6.1 — compatible with MT7921AUN.

```bash
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

### Step 3: Verify and Enable Monitor Mode

```bash
lsmod | grep mt7921
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Step 4: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1
```

`Injection is working!` confirms the adapter is fully operational.

---

## Raspberry Pi 4B / 5

> The AWUS036AXML draws up to 2.7W under load. Always use a powered USB hub on Raspberry Pi.

### Step 1: Download Kali Linux ARM64 Image

Official page: https://www.kali.org/get-kali/#kali-arm

Pick **Raspberry Pi 4 (64-bit)** or **Raspberry Pi 5 (64-bit)** — 64-bit is required.

> **China mirror:** https://repo.huaweicloud.com/kali-images/ — browse to the latest release folder and download the ARM64 image.

### Step 2: Flash to MicroSD

```bash
lsblk
# Replace /dev/sdX with your actual SD card
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Default credentials: **kali / kali**.

### Step 3: Switch to China Mirror and Install Firmware

```bash
sudo nano /etc/apt/sources.list
```

Replace with:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Then:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

### Step 4: Verify Driver

```bash
lsmod | grep mt7921
```

`mt7921u` should appear.

### Step 5: Enable Monitor Mode

On a Pi with built-in Wi-Fi, the AWUS036AXML shows up as `wlan1`.

```bash
iwconfig
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Step 6: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1
```

---

## Virtual Machine USB Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. Power off the VM. Go to **Settings → USB**.
2. Enable **USB 3.0 (xHCI) Controller**.
3. Click **+** to add a USB filter.
4. Select: **MediaTek Inc.** (ID: 0e8d:7961).
5. Start the VM — the adapter appears inside Kali.

Run `lsusb` in the VM to confirm `0e8d:7961`, then follow the Kali steps above.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Start the VM.
2. Menu: **Virtual Machine → USB & Bluetooth**.
3. Find **MediaTek MT7921AUN** and click **Connect**.
4. Run `lsusb` in the VM to confirm, then follow the Kali steps above.

---

## Virtual Interface (VIF) {#virtual-interface-vif}

The MT7921AUN has full kernel-native VIF support. You can run a monitor interface and a managed interface on the same adapter simultaneously — no patches required.

### Create a Monitor Interface Alongside Managed Mode

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
iwconfig
```

You should see both `wlan0` (managed) and `mon0` (monitor) active at the same time.

### Monitor While Staying Connected

```bash
sudo airodump-ng mon0
```

`wlan0` stays associated while `mon0` captures everything in range.

### Fake AP + Monitor

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
iwconfig
```

> **Note on hostapd:** Full AP operation requires configuring `hostapd`. The steps above confirm the adapter can create the interface — actual AP configuration is a separate topic.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0e8d:7961 | Adapter not powered or bad cable | Try a different USB-C port. Use powered hub on Raspberry Pi. |
| `lsmod` shows no mt7921u | Firmware not installed or old kernel | Run `sudo apt install linux-firmware firmware-misc-nonfree && sudo reboot` |
| Ubuntu 22.04 doesn't load driver | Kernel 5.15 too old | Install HWE: `sudo apt install linux-generic-hwe-22.04` |
| Interface appears but won't associate | Firmware blobs missing | Run `sudo apt install firmware-misc-nonfree` then reboot |
| Monitor mode switch fails | Interface still up | Run `sudo ip link set wlan1 down` before the `iw dev` command |
| Injection test says "No Answer" | AP too far or wrong interface | Move closer. Verify `Mode:Monitor` with `iwconfig`. |
| VIF interface creation fails | Driver not fully loaded | Unplug, then: `sudo rmmod mt7921u && sudo modprobe mt7921u` |

## China Mirror Reference

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages, firmware |
| Alfa documentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Product manuals |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommended) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommended) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM images (backup) |

## More Alfa Adapter Guides for China

This is part of the **Alfa China Install Guide** series:

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, full VIF
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/) — RTL8811AU, monitor mode
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — MT7921AUN, L-shape USB-A
- AWUS036AXML ← you are here
- [AWUS036EACS China Install Guide](/en/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).
