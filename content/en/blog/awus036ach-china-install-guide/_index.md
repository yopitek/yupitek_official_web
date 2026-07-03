---
title: "ALFA AWUS036ACH Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "What chipset does AWUS036ACH use? Does it need extra drivers?"
    answer: "AWUS036ACH uses the Realtek RTL8812AU chipset. The driver is not built into the Linux kernel and needs manual installation."
  - question: "Do I need a VPN to install AWUS036ACH drivers in China?"
    answer: "No. You can complete the entire process using domestic mirrors like USTC, Aliyun, and Gitee source code mirrors."
  - question: "Does AWUS036ACH support monitor mode and packet injection?"
    answer: "Yes. After installing the RTL8812AU driver, use airmon-ng to enable monitor mode and aireplay-ng to test packet injection."
  - question: "Can AWUS036ACH work on a Raspberry Pi?"
    answer: "Yes. Use a powered USB hub and flash the Kali ARM64 image for best results."
  - question: "What is the Kali Linux command to install AWUS036ACH drivers?"
    answer: "Run sudo apt install realtek-rtl88xxau-dkms to install the pre-compiled driver on Kali."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 1
description: "Step-by-step guide to install ALFA AWUS036ACH drivers in China using domestic mirrors. Covers Kali Linux, Ubuntu 22/24, Debian, and Raspberry Pi. No GitHub required."
related_product: "/en/products/alfa/awus036ach/"
featureimage: "/images/blog/awus036ach-china-install-guide.webp"
---

You just got the AWUS036ACH and your Linux machine doesn't recognize it. That's normal — this chip needs the RTL8812AU driver, and it's not plug-and-play. This guide walks you through the full install in about 30 minutes, using only domestic mirrors. No GitHub access needed.

{{< tldr >}}
AWUS036ACH uses the RTL8812AU chipset. Install the DKMS driver via apt on Kali, or compile from Gitee on Ubuntu/Debian. Monitor mode and packet injection are ready in 30 minutes.
{{< /tldr >}}

Make sure you have these ready:






## Before You Start

Make sure you have these ready:

1. **ALFA AWUS036ACH** adapter
2. USB cable (the one that came in the box works fine)
3. A powered USB hub — required if you're on Raspberry Pi
4. Active internet connection to reach domestic mirrors

Plug in the adapter, then confirm your system sees it:

```bash
lsusb
```

Look for this in the output:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

If you see `0bda:8812`, the adapter is detected. Move to your OS section below.

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
- [VM USB Passthrough](#virtual-machine-usb-passthrough)

---

## Kali Linux

Kali comes with strong wireless tooling built in. Getting the AWUS036ACH driver running takes four steps. Start by switching to a fast Chinese mirror so every download stays quick.

### Step 1: Switch to China Mirror

Open your sources list in the terminal.

```bash
sudo nano /etc/apt/sources.list
```

Delete whatever is there, then paste this line:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save the file: press **Ctrl+O**, then Enter, then Ctrl+X to exit. Refresh the package index.

```bash
sudo apt update
```

> **Backup mirror:** If 中科大 (USTC) is slow on your connection, use 清华 (Tsinghua) instead:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Step 2: Install the Driver

Kali's package repository includes a prebuilt DKMS driver. Install it with one command.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

DKMS automatically recompiles the driver whenever your kernel updates, so you will not need to reinstall manually after an upgrade.

Verify the driver loaded correctly.

```bash
modinfo 88XXau | grep -E "filename|version"
```

You should see a `filename` line ending in `.ko` and a `version` line showing a version string like `5.6.4.2`. If both appear, the driver is ready.

---

### Step 2 (Alternative): Manual Compile from Source

Only follow this section if the `apt install` above failed. First install the build dependencies.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Download the driver source from Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **NOTE:** If that URL does not load, search Gitee for `rtl8812au` and pick the most recently updated fork. You can also download a source archive directly from [files.alfa.com.tw](https://files.alfa.com.tw).

Move into the cloned directory, then compile and install.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Load the driver into the running kernel.

```bash
sudo modprobe 88XXau
```

---

### Step 3: Enable Monitor Mode {#enable-monitor-mode}

Before putting the adapter into monitor mode, check which interface name your system assigned it.

```bash
iwconfig
```

Look for a `wlan0` or `wlan1` entry. Use that name in the commands below.

Stop NetworkManager and wpa_supplicant — both fight over the adapter and will block monitor mode.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirm the switch worked.

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

If the test fails, reboot the machine and run the test again. If it still fails after a reboot, confirm no other process holds the interface — run `iwconfig` and make sure only `wlan0mon` appears, with nothing else claiming the adapter.

---

## Ubuntu 22.04 / 24.04

Ubuntu splits into two branches with different package file formats. The steps below handle both. Use **阿里云 (Aliyun)** as your mirror — it's fast, reliable, and maintained by Alibaba.

### Step 1: Switch to China Mirror

Pick your Ubuntu version and follow that path only.

#### Ubuntu 24.04 (Noble)

Open the new DEB822-format sources file:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Delete everything in the file and paste this exact content:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Save with `Ctrl+O`, then exit with `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Open the classic sources file instead:

```bash
sudo nano /etc/apt/sources.list
```

Replace all existing lines with:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Save and exit the same way (`Ctrl+O`, then `Ctrl+X`).

#### Refresh the package index

Run this for both versions after editing your sources file:

```bash
sudo apt update
```

---

### Step 2: Install Build Dependencies

The driver compiles from source, so you need the kernel headers and build tools first:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

This pulls in gcc, make, and the exact headers that match your running kernel. The `$(uname -r)` part auto-detects your kernel version — no need to type it manually.

---

### Step 3: Download Driver Source (China Mirror)

Clone the driver repository from Gitee, which is accessible inside China:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Then move into the cloned folder:

```bash
cd rtl8812au
```

> **Note:** If that URL times out or returns a 404, go to [gitee.com](https://gitee.com) and search for `rtl8812au`. Pick the fork with the most recent commit date.

---

### Step 4: Compile and Install

Build the kernel module from source:

```bash
make
```

Install it into the system:

```bash
sudo make install
```

Register the module with DKMS so it survives kernel upgrades:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Load the module into the running kernel:

```bash
sudo modprobe 88XXau
```

Verify the module loaded correctly:

```bash
modinfo 88XXau | grep filename
```

You should see a path ending in `88XXau.ko` or similar. If the command returns output, the driver is active.

---

### Step 5: Enable Monitor Mode

First, kill any processes that might interfere with the wireless interface:

```bash
sudo airmon-ng check kill
```

Then put the adapter into monitor mode:

```bash
sudo airmon-ng start wlan0
```

> **Note:** Your interface may be named `wlan1` instead of `wlan0`. Run `iwconfig` first to see all wireless interfaces listed, then substitute the correct name in the command above.

---

### Step 6: Test Packet Injection

With the adapter in monitor mode, run the injection test:

```bash
sudo aireplay-ng --test wlan0mon
```

A successful result shows lines like `Injection is working!`. If you see errors about the interface, double-check that monitor mode is active with `iwconfig wlan0mon`.

---

## Debian

Debian's package manager points to overseas servers by default. Switching to 清华大学 (Tsinghua University) mirror brings download speeds from overseas crawl to local sprint.

### Step 1: Switch to China Mirror

Open the sources list:

```bash
sudo nano /etc/apt/sources.list
```

Delete everything inside and paste these three lines (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Save with `Ctrl+O`, then exit with `Ctrl+X`. Refresh the package index:

```bash
sudo apt update
```

### Step 2: Install Build Dependencies

The AWUS036ACH driver compiles from source, so you need the kernel headers and build tools:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

This command tailors the header package to your running kernel version automatically.

### Step 3: Download Driver Source (China Mirror)

Clone the driver repository from Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Move into the project folder:

```bash
cd rtl8812au
```

> **Can't reach that URL?** Search Gitee for `rtl8812au` and pick the most recently updated fork.

### Step 4: Compile and Install

Run these commands in sequence inside the `rtl8812au` folder:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

`dkms` registers the driver so it survives kernel updates automatically.

### Step 5: Enable Monitor Mode

**Kill interfering processes** before switching modes:

```bash
sudo airmon-ng check kill
```

Start monitor mode on your adapter:

```bash
sudo airmon-ng start wlan0
```

If `airmon-ng` is missing, install it first:

```bash
sudo apt install -y aircrack-ng
```

Confirm the interface came up:

```bash
iwconfig
```

Look for an interface named `wlan0mon` in the output.

### Step 6: Test Packet Injection

```bash
sudo aireplay-ng --test wlan0mon
```

A stream of injection test results confirms the adapter works. You're ready to go.

---

## Raspberry Pi 4B / 5

> The AWUS036ACH draws ~500mW. Plugging it directly into a Raspberry Pi USB port can cause the Pi to throttle or restart under load. **Always use a powered USB hub.**

---

### Step 1: Download Kali Linux ARM64 Image

Go to the official Kali ARM downloads page:
https://www.kali.org/get-kali/#kali-arm

Pick **Raspberry Pi 4 (64-bit)** or **Raspberry Pi 5 (64-bit)** to match your board. Do not download the 32-bit image — the driver build requires a 64-bit kernel.

> **China mirror:** If kali.org loads slowly, try 华为云 instead:
> https://repo.huaweicloud.com/kali-images/
> Browse to the latest release folder and download the same ARM64 image from there.

---

### Step 2: Flash to MicroSD

Insert your microSD card, then check its device path before writing anything.

```bash
lsblk
```

Find your card in the list — it will show as something like `sdb` or `mmcblk0`. Then flash the image, replacing `/dev/sdX` with your actual path.

```bash
# Replace /dev/sdX with your actual SD card (check with lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Wait for `sync` to finish before pulling the card. Boot the Pi from the card. Default credentials after boot: **kali / kali**.

---

### Step 3: Switch to China Mirror

After first boot, open the package sources file.

```bash
sudo nano /etc/apt/sources.list
```

Delete everything in the file and replace it with this single line:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save: press **Ctrl+O**, then Enter, then Ctrl+X. Now apply the mirror and upgrade the system.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

The reboot picks up any kernel updates before you install the driver.

---

### Step 4: Install Driver (ARM64)

The DKMS package works on ARM64 exactly the same as x86 — no special steps needed.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

If that command returns an error saying the package is not found, compile the driver from source instead.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Step 5: Enable Monitor Mode

Before touching the adapter, check which interface name the Pi assigned it.

```bash
iwconfig
```

On a Pi with a built-in Wi-Fi chip, the AWUS036ACH shows up as `wlan1` — the built-in radio takes `wlan0`. Use whatever name `iwconfig` reported above.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Run `iwconfig` again and look for an entry ending in `mon` — `wlan1mon` in the typical Pi case — with `Mode:Monitor`. That confirms the adapter switched successfully.

---

### Step 6: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

Replace `wlan1mon` with whatever monitor interface name appeared in Step 5. A working adapter prints `Injection is working!`. If the test fails, reboot and try once more. A bad USB connection through an unpowered hub is the most common cause on Pi — double-check you are using the powered hub.

---

## Virtual Machine USB Passthrough

Running Kali Linux inside a VM on macOS or Windows? You need to pass the USB adapter through to the guest OS.

### VirtualBox

1. With the VM powered off, go to **Settings → USB**.
2. Enable **USB 3.0 (xHCI) Controller**.
3. Click the **+** icon to add a USB filter.
4. Select: **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Start the VM — the adapter appears inside Kali.

Inside the VM, run `lsusb` to confirm `0bda:8812` appears, then follow the Kali Linux steps above.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Start the VM.
2. In the menu: **Virtual Machine → USB & Bluetooth**.
3. Find **Realtek 802.11ac NIC** and click **Connect**.
4. The adapter disconnects from the host and appears inside the VM.

Run `lsusb` inside the VM to confirm, then follow the Kali Linux steps above.

### A Note on VIF (Virtual Interface)

The RTL8812AU chip in the AWUS036ACH has limited VIF support on Linux. You cannot reliably run managed mode and monitor mode (or AP mode) at the same time on the same adapter.

If your workflow needs VIF — for example, running fake APs while monitoring simultaneously — the AWUS036ACH is the wrong tool. Check the [AWUS036ACM install guide](/en/blog/awus036acm-china-install-guide/) instead. That adapter uses the MT7612U chip, which has full kernel-native VIF support and handles simultaneous virtual interfaces without patches.

---

{{< faq >}}

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0bda:8812 | Adapter not powered or bad cable | Try a different USB port. Use a powered hub on Raspberry Pi. |
| `make` fails with header errors | Kernel headers missing or version mismatch | Run `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` fails | Secure Boot blocking unsigned modules | Disable Secure Boot in BIOS, or sign the module |
| Driver disappears after kernel update | Driver not registered with DKMS | Re-run `sudo dkms install rtl8812au/$(cat VERSION)` from the source directory |
| `airmon-ng start wlan0` fails | NetworkManager still running | Run `sudo airmon-ng check kill` first |
| Monitor mode starts but captures no traffic | Wrong channel or wrong interface name | Check interface with `iwconfig`. Set channel: `iwconfig wlan0mon channel 6` |
| Injection test says "No Answer" | AP too far away, or using wrong interface | Move closer to the AP. Use `wlan0mon` not `wlan0` |

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
| RTL8812AU driver (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Manual compile fallback |

## More Alfa Adapter Guides for China

This is part of the **Alfa China Install Guide** series. Each article covers one adapter model:

- AWUS036ACH ← you are here
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, best VIF support
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/)
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/)
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/)
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/)
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/)
- [AWUS036EAC China Install Guide](/en/blog/awus036eacs-china-install-guide/)

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).

## References

1. [aircrack-ng Official Documentation](https://www.aircrack-ng.org/)
2. [ALFA Network Official Website](https://www.alfa.com.tw/)
3. [Kali Linux Official Documentation](https://www.kali.org/docs/)
4. [Gitee rtl8812au Mirror](https://gitee.com/mirrors/rtl8812au)
5. [Realtek RTL8812AU Driver](https://www.realtek.com/)
