---
title: "ALFA AWUS036AXER Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Step-by-step guide to install ALFA AWUS036AXER drivers in China using domestic mirrors. RTL8832BU driver, WiFi 6 nano adapter. Covers Kali Linux, Ubuntu 22/24 (in-kernel on 24.04), Debian, and Raspberry Pi. No GitHub required."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
related_product: "/en/products/alfa/awus036axer/"
---

The AWUS036AXER is ALFA's WiFi 6 nano adapter — a compact dongle designed to stay plugged into a laptop permanently. Its RTL8832BU chip is out-of-kernel on Linux below 6.14 but is included natively in Ubuntu 24.04 (kernel 6.8). This guide uses Gitee mirrors for older kernels. No GitHub required.

> **Security research note:** The RTL8832BU has limited monitor mode support. Results vary by kernel and driver version. For reliable packet injection on Kali Linux, the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/) or [AWUS036ACH](/en/blog/awus036ach-china-install-guide/) are better choices.

> **Range note:** The AWUS036AXER has an integrated non-removable antenna. For security research, adapters with external RP-SMA antennas (AWUS036ACH, AWUS036ACM) provide significantly better range.

## Before You Start

1. **ALFA AWUS036AXER** adapter
2. USB-A cable
3. Active internet connection

```bash
lsusb
```

Look for:

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Choose Your Operating System

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### Step 1: Switch to China Mirror

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Step 2: Install Build Dependencies

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Step 3: Clone Driver from Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **NOTE:** If that Gitee URL does not load, search Gitee for `rtl8852bu` and pick the most recently updated fork. You can also download archives from [files.alfa.com.tw](https://files.alfa.com.tw).

### Step 4: Compile and Install

```bash
sudo ./install-driver.sh
sudo reboot
```

Verify the driver loaded:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Step 5: Enable Monitor Mode {#enable-monitor-mode}

> **Note:** Monitor mode support is limited on the RTL8832BU. The following commands work on most setups but results may vary.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Step 6: Test Packet Injection {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

If injection is unreliable, consider the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/) for penetration testing work.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — driver in-kernel, no Gitee needed

Ubuntu 24.04 ships kernel 6.8, which includes the RTL8832BU driver natively.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo modprobe 88x2bu
iwconfig
```

If the module loads and an interface appears, you are done. Proceed to monitor mode steps above.

---

### Ubuntu 22.04 (Jammy) — DKMS required

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Enable monitor mode same as Kali steps above.

---

## Raspberry Pi 4B / 5

Switch to China mirror first:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Virtual Machine USB Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Settings → USB** → Enable **USB 3.0 (xHCI)**.
2. Add filter: **Realtek** (ID: 0bda:885a).
3. Start VM → `lsusb` to confirm → follow Kali steps.

### VMware

1. **Virtual Machine → USB & Bluetooth** → Find **Realtek RTL8832BU** → **Connect**.
2. `lsusb` to confirm → follow Kali steps.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0bda:885a | Adapter not detected | Try different USB port |
| `install-driver.sh` fails | Missing headers | `sudo apt install linux-headers-$(uname -r)` |
| Gitee clone fails | Network issue | Search gitee.com for `rtl8852bu` |
| Ubuntu 24.04: `modprobe 88x2bu` fails | Module not present | Install `linux-modules-extra-$(uname -r)` |
| Monitor mode unreliable | RTL8832BU limitation | Use AWUS036ACM for pentest work |

> **Note on VIF:** The RTL8832BU out-of-kernel driver does not support Virtual Interfaces (VIF).

## China Mirror Reference

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | RTL8832BU driver |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## More Alfa Adapter Guides for China

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, full VIF
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/) — RTL8811AU, monitor mode
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← you are here
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — MT7921AUN, L-shape
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Install Guide](/en/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).
