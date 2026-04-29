---
title: "ALFA AWUS036ACS Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Step-by-step guide to install ALFA AWUS036ACS drivers in China using domestic mirrors. RTL8811AU DKMS driver, full monitor mode and packet injection. Covers Kali Linux, Ubuntu 22/24, Debian, and Raspberry Pi. No GitHub required."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 3
related_product: "/en/products/alfa/awus036acs/"
---

The AWUS036ACS is ALFA's compact dual-band security research adapter. Its RTL8811AU chip supports full monitor mode and packet injection on Kali Linux — but because the driver is out-of-kernel, you need to compile it from source. In China, GitHub is blocked, so this guide uses Gitee mirrors exclusively. No GitHub required.

## Before You Start

Make sure you have these ready:

1. **ALFA AWUS036ACS** adapter
2. USB cable (USB-A 2.0, the one in the box works fine)
3. Active internet connection to reach domestic mirrors

Plug in the adapter, then confirm your system sees it:

```bash
lsusb
```

Look for this in the output:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

If you see `0bda:0811`, the adapter is detected. Move to your OS section below.

## Choose Your Operating System

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

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Delete whatever is there, then paste:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Save with **Ctrl+O**, Enter, then Ctrl+X. Refresh:

```bash
sudo apt update
```

> **Backup mirror:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Step 2: Install Build Dependencies

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Step 3: Clone Driver from Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **NOTE:** If that Gitee URL does not load, search Gitee for `8821au` and pick the most recently updated fork. You can also download driver archives from [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Step 4: Compile and Install

```bash
sudo ./install-driver.sh
sudo reboot
```

After reboot, verify the driver loaded.

```bash
lsmod | grep 88XXau
```

You should see a `88XXau` module listed. Then confirm the interface appeared.

```bash
iwconfig
```

Look for `wlan0` or `wlan1`.

---

### Step 5: Enable Monitor Mode {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirm with `iwconfig` — look for `wlan1mon` with `Mode:Monitor`.

---

### Step 6: Test Packet Injection {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Step 1: Switch to China Mirror

#### Ubuntu 24.04 (Noble)

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

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Replace all lines with:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Step 2: Install Build Dependencies

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Step 3: Clone and Install Driver from Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Step 4: Enable Monitor Mode

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Step 5: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

Paste (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Step 2: Install Build Dependencies

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Step 3: Clone and Install

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Step 4: Enable Monitor Mode

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirm: `iwconfig` → look for `wlan1mon` with `Mode:Monitor`.

### Step 5: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Step 1: Download and Flash Kali ARM64

Official: https://www.kali.org/get-kali/#kali-arm — pick Raspberry Pi 4/5 64-bit.

China mirror: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Default credentials: **kali / kali**.

### Step 2: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Step 3: Install Build Dependencies

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Step 4: Clone and Install Driver

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Step 5: Enable Monitor Mode

On a Pi with built-in Wi-Fi, AWUS036ACS appears as `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Step 6: Test Packet Injection

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Virtual Machine USB Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. Power off the VM → **Settings → USB** → Enable **USB 2.0 Controller**.
2. Click **+** → Select: **Realtek** (ID: 0bda:0811).
3. Start the VM. Run `lsusb` to confirm `0bda:0811`, then follow Kali steps above.

### VMware Fusion / Workstation

1. **Virtual Machine → USB & Bluetooth** → Find **Realtek 8811AU** → **Connect**.
2. Run `lsusb` to confirm, then follow Kali steps above.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0bda:0811 | Adapter not powered or bad cable | Try different USB port |
| `install-driver.sh` fails | Missing headers | Run `sudo apt install linux-headers-$(uname -r)` |
| Gitee clone fails | Network issue | Search gitee.com for `8821au`, try a different fork |
| `airmon-ng start` fails | NetworkManager running | Run `sudo airmon-ng check kill` first |
| No traffic in monitor mode | Wrong channel | Set channel: `iwconfig wlan1mon channel 6` |
| Injection "No Answer" | AP too far | Move closer. Use `wlan1mon`, not `wlan1`. |

> **Note on VIF:** The RTL8811AU driver does not support Virtual Interfaces (VIF). Concurrent monitor + managed mode is not available on this adapter.

## China Mirror Reference

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages |
| Alfa documentation | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Product manuals |
| 8821au driver (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | RTL8811AU driver |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recommended) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recommended) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM images |

## More Alfa Adapter Guides for China

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, full VIF
- AWUS036ACS ← you are here
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — MT7921AUN, L-shape
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Install Guide](/en/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).
