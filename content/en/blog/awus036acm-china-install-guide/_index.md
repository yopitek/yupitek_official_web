---
title: "ALFA AWUS036ACM Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "What chipset does AWUS036ACM use? Does it need drivers?"
    answer: "It uses the MediaTek MT7612U chipset. The mt76x2u driver has been built into the Linux kernel since 4.19. In most cases, it is plug-and-play."
  - question: "Does AWUS036ACM support VIF virtual interfaces?"
    answer: "Yes. MT7612U fully supports kernel-native VIF, allowing simultaneous monitor and managed mode interfaces without patching."
  - question: "Do I need a VPN to install AWUS036ACM in China?"
    answer: "No. The driver is already in the kernel. You only need to install the firmware-misc-nonfree package from domestic mirrors."
  - question: "How much power does AWUS036ACM draw on Raspberry Pi?"
    answer: "About 400mW at full load. A powered USB hub is recommended to prevent Pi throttling."
  - question: "Why does Debian recognize the AWUS036ACM but it does not work?"
    answer: "Missing the firmware-misc-nonfree package. Install it and the adapter will initialize properly."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 2
description: "Step-by-step guide to install ALFA AWUS036ACM drivers in China using domestic mirrors. MT7612U in-kernel driver, full VIF support. Covers Kali Linux, Ubuntu 22/24, Debian, and Raspberry Pi. No GitHub required."
related_product: "/en/products/alfa/awus036acm/"
featureimage: "/images/blog/awus036acm-china-install-guide.webp"
---

The AWUS036ACM is one of the easiest Alfa adapters to set up on Linux. Its MT7612U chip uses the `mt76x2u` driver, which is built into the Linux kernel since version 4.19. On most modern systems, the adapter works with two or three commands. This guide covers the full setup — driver verification, monitor mode, packet injection, and VIF — using only domestic mirrors. No GitHub required.

{{< tldr >}}
AWUS036ACM with MT7612U chipset has an in-kernel driver with no compilation needed. It supports monitor mode, packet injection, and simultaneous VIF operation. In China, only the firmware package needs installing.
{{< /tldr >}}

Make sure you have these ready:






## Before You Start

Make sure you have these ready:

1. **ALFA AWUS036ACM** adapter
2. USB cable (the one in the box works fine)
3. A powered USB hub — required if you are on Raspberry Pi
4. Active internet connection to reach domestic mirrors

Plug in the adapter, then confirm your system sees it:

```bash
lsusb
```

Look for this in the output:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

If you see `0e8d:7612`, the adapter is detected. Move to your OS section below.

If you don't see it, try a different USB port or swap the cable, then run `lsusb` again.

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

The MT7612U driver is already in the Kali kernel. In most cases the adapter works the moment you plug it in. The steps below verify the driver is loaded and walk you through monitor mode.

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

### Step 2: Verify the Driver

Check if the module loaded automatically when you plugged in the adapter.

```bash
lsmod | grep mt76
```

You should see output containing `mt76x2u`. If nothing appears, load it manually.

```bash
sudo modprobe mt76x2u
```

Run `lsmod | grep mt76` again to confirm. Then verify the adapter is up.

```bash
iwconfig
```

Look for a wireless interface — typically `wlan0` or `wlan1`. If the interface appears with an ESSID or `unassociated`, the driver is working.

---

### Step 2 (Alternative): Install Extra Kernel Modules

If `modprobe mt76x2u` gives a "Module not found" error, your kernel build may be missing the MT76 modules. Install them from the China mirror.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

After the install completes, load the module again.

```bash
sudo modprobe mt76x2u
```

If the package is not available for your exact kernel version, compile the driver from source instead.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **NOTE:** If that Gitee URL does not load, search Gitee for `mt76` and pick the most recently updated fork. You can also download driver archives directly from [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Step 3: Enable Monitor Mode {#enable-monitor-mode}

Before switching to monitor mode, check which interface name the system assigned to the adapter.

```bash
iwconfig
```

Look for `wlan0` or `wlan1`. Use that name in the commands below.

Stop NetworkManager and wpa_supplicant so they don't interfere.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirm the switch.

```bash
iwconfig
```

Look for an entry like `wlan0mon` with `Mode:Monitor`. When you see that, the adapter is ready for packet capture.

---

### Step 4: Test Packet Injection {#test-packet-injection}

Run the injection test against the monitor interface.

```bash
sudo aireplay-ng --test wlan0mon
```

A successful result looks like this:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

If the test fails, reboot and run it again. If it still fails, confirm no other process holds the interface with `iwconfig`.

---

## Ubuntu 22.04 / 24.04

The MT7612U driver is in the Ubuntu kernel too, but it may ship in the `linux-modules-extra` package rather than the base kernel image. The steps below handle both cases.

### Step 1: Switch to China Mirror

#### Ubuntu 24.04 (Noble)

Open the DEB822-format sources file:

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

#### Ubuntu 22.04 (Jammy)

Open the classic sources file:

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

#### Refresh the package index

```bash
sudo apt update
```

---

### Step 2: Load the Driver

Try loading the module directly first.

```bash
sudo modprobe mt76x2u
```

If that gives a "Module not found" error, install the extra modules package.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Verify the adapter is visible.

```bash
iwconfig
```

An interface like `wlan0` or `wlan1` in the output confirms the driver is active.

---

### Step 3: Install Wireless Tools

Install aircrack-ng for monitor mode and injection testing.

```bash
sudo apt install -y aircrack-ng
```

---

### Step 4: Enable Monitor Mode

Kill interfering processes, then start monitor mode.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Note:** Your interface may be `wlan1` if another wireless card is present. Run `iwconfig` first to check.

---

### Step 5: Test Packet Injection

```bash
sudo aireplay-ng --test wlan0mon
```

A successful result shows `Injection is working!`. If you see interface errors, verify monitor mode is active with `iwconfig wlan0mon`.

---

## Debian

The MT7612U driver is in the Debian kernel but sometimes requires the `firmware-misc-nonfree` package to initialise fully.

### Step 1: Switch to China Mirror

Open the sources list:

```bash
sudo nano /etc/apt/sources.list
```

Delete everything and paste these three lines (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Save with `Ctrl+O`, then exit with `Ctrl+X`. Refresh:

```bash
sudo apt update
```

### Step 2: Install Non-Free Firmware

The MT7612U requires firmware files from the `firmware-misc-nonfree` package. Without this, the adapter initialises but may not associate or switch to monitor mode.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Step 3: Load the Driver

```bash
sudo modprobe mt76x2u
```

If the module is missing, install extra kernel modules first.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Confirm the interface appeared.

```bash
iwconfig
```

### Step 4: Enable Monitor Mode

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirm monitor mode with `iwconfig` — look for `wlan0mon` with `Mode:Monitor`.

### Step 5: Test Packet Injection

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` confirms the adapter is fully operational.

---

## Raspberry Pi 4B / 5

> The AWUS036ACM draws around 400mW under load. Use a powered USB hub to prevent the Pi from throttling.

---

### Step 1: Download Kali Linux ARM64 Image

Go to the official Kali ARM downloads page:
https://www.kali.org/get-kali/#kali-arm

Pick **Raspberry Pi 4 (64-bit)** or **Raspberry Pi 5 (64-bit)**. Do not use the 32-bit image — 64-bit is required.

> **China mirror:** If kali.org is slow, use 华为云:
> https://repo.huaweicloud.com/kali-images/
> Browse to the latest release folder and download the ARM64 image from there.

---

### Step 2: Flash to MicroSD

Check the device path of your card first.

```bash
lsblk
```

Then flash, replacing `/dev/sdX` with your actual card path.

```bash
# Replace /dev/sdX with your actual SD card (check with lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Wait for `sync` to complete, then boot. Default credentials: **kali / kali**.

---

### Step 3: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Replace the contents with:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save and apply.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Step 4: Verify Driver

After reboot, plug in the adapter and check.

```bash
lsmod | grep mt76
```

If `mt76x2u` appears, you are done. If not:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Step 5: Enable Monitor Mode

On a Pi with built-in Wi-Fi, the AWUS036ACM shows up as `wlan1` — the built-in radio occupies `wlan0`.

```bash
iwconfig
```

Note the interface name, then start monitor mode on it.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirm with `iwconfig` — look for `wlan1mon` with `Mode:Monitor`.

---

### Step 6: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` confirms full operation. If it fails, recheck you are using a powered hub.

---

## Virtual Machine USB Passthrough

### VirtualBox

1. Power off the VM. Go to **Settings → USB**.
2. Enable **USB 3.0 (xHCI) Controller**.
3. Click **+** to add a USB filter.
4. Select: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. Start the VM — the adapter appears inside Kali.

Run `lsusb` in the VM to confirm `0e8d:7612`, then follow the Kali steps above.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Start the VM.
2. Menu: **Virtual Machine → USB & Bluetooth**.
3. Find **MediaTek MT7612U** and click **Connect**.
4. Run `lsusb` in the VM to confirm, then follow the Kali steps above.

---

## Virtual Interface (VIF)

This is where the AWUS036ACM pulls ahead of the ACH. The MT7612U chip has full kernel-native VIF support. You can run a monitor interface and a managed or AP interface on the same adapter simultaneously — no patches, no hacks.

### Create a Second Virtual Interface

With the adapter in managed mode as `wlan0`, add a monitor interface alongside it.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Now verify both interfaces are active.

```bash
iwconfig
```

You should see both `wlan0` (associated, managed mode) and `mon0` (monitor mode). The adapter is doing both at the same time.

### Use Case: Monitor While Staying Connected

This lets you capture traffic on `mon0` while `wlan0` stays connected to a network — useful for correlated analysis.

```bash
sudo airodump-ng mon0
```

`wlan0` continues its normal association while `mon0` captures everything in range.

### Use Case: Fake AP + Monitor

Create an AP interface and a monitor interface together.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Run `iwconfig` to confirm all three interfaces (`wlan0`, `ap0`, `mon0`) are active.

> **Note on hostapd:** Full AP operation requires configuring `hostapd`. That is outside the scope of this guide. The steps above confirm the adapter can create the interface — actual AP configuration is a separate topic.

---

{{< faq >}}

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0e8d:7612 | Adapter not powered or bad cable | Try a different USB port. Use powered hub on Raspberry Pi. |
| `modprobe mt76x2u` says "Module not found" | Kernel missing extra modules | Run `sudo apt install linux-modules-extra-$(uname -r)` |
| Interface appears but won't associate | Firmware file missing | Run `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` fails | NetworkManager still running | Run `sudo airmon-ng check kill` first |
| Monitor mode starts but no traffic captured | Wrong channel or wrong interface name | Set channel: `iwconfig wlan0mon channel 6` |
| Injection test says "No Answer" | AP too far or wrong interface | Move closer to the AP. Use `wlan0mon`, not `wlan0`. |
| VIF interface creation fails | Driver not fully loaded | Unplug adapter, reload module: `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## China Mirror Reference

All resources used in this guide — no GitHub required:

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages, firmware |
| Alfa documentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Product manuals |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommended) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommended) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM images (backup) |
| MT76 driver (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Manual compile fallback |

## More Alfa Adapter Guides for China

This is part of the **Alfa China Install Guide** series. Each article covers one adapter model:

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- AWUS036ACM ← you are here
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/)
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China Install Guide](/en/blog/awus036eacs-china-install-guide/)

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).

## References

1. [Linux Kernel mt76 Driver](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [aircrack-ng Official Documentation](https://www.aircrack-ng.org/)
3. [ALFA Network Official Website](https://www.alfa.com.tw/)
4. [Kali Linux Official Documentation](https://www.kali.org/docs/)
5. [Debian firmware-misc-nonfree Package](https://packages.debian.org/bookworm/firmware-misc-nonfree)
