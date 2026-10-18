---
title: "ALFA AWUS036AXER Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Step-by-step guide to install ALFA AWUS036AXER drivers in China using domestic mirrors. RTL8832BU driver, WiFi 6 nano adapter. Covers Kali Linux, Ubuntu 22/24 (DKMS), Debian, and Raspberry Pi."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "What chipset does AWUS036AXER use? Is it the same as AWUS036AX?"
    answer: "Same Realtek RTL8832BU chipset with WiFi 6 support, but in a smaller, more portable form factor."
  - question: "Does AWUS036AXER need a driver on Ubuntu 24.04?"
    answer: "Yes. The RTL8832BU is not in the Ubuntu 24.04 kernel. Build the community rtl8852bu driver (morrownr/rtl8852bu-20250826) once via DKMS; it is then rebuilt automatically on kernel updates."
  - question: "Is AWUS036AXER suitable for wireless security research?"
    answer: "No. The community rtl8852bu driver does not support monitor mode or packet injection. Use an adapter with an in-kernel MediaTek driver such as the AWUS036ACM instead."
  - question: "What is the USB ID of AWUS036AXER?"
    answer: "The Realtek RTL8832BU vendor ID is 0bda. The product ID is 8832 or 885a depending on the unit, so confirm yours with lsusb."
  - question: "Do I need a VPN to install AWUS036AXER in China?"
    answer: "Not necessarily. Clone the driver from the verified GitHub repository (morrownr/rtl8852bu-20250826); if GitHub is slow, use a proxy or mirror you trust. Build tools can still be installed from domestic mirrors."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/en/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
---

The AWUS036AXER is ALFA's WiFi 6 nano adapter — a compact dongle designed to stay plugged into a laptop permanently. Its RTL8832BU chip has no in-kernel Linux driver, so you build the community rtl8852bu driver once with DKMS on every distribution, including Ubuntu 24.04. The driver source is cloned from the verified GitHub repository; if GitHub is slow, use a proxy or mirror you trust. Monitor mode is not supported by this driver.

{{< tldr >}}
AWUS036AXER uses the RTL8832BU chipset. A mini portable WiFi 6 adapter. The driver is not in the kernel: every distribution (including Ubuntu 24.04) needs rtl8852bu built via DKMS. Monitor mode is not supported.
{{< /tldr >}}





> **Security research note:** The community rtl8852bu driver does **not** support monitor mode or packet injection. For security research use an in-kernel MediaTek adapter such as the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/).

> **Range note:** The AWUS036AXER has an integrated non-removable antenna. For security research, adapters with external RP-SMA antennas (AWUS036ACH, AWUS036ACM) provide significantly better range.

## Before You Start

1. **ALFA AWUS036AXER** adapter
2. USB-A cable
3. Active internet connection

```bash
lsusb
```

Look for a line like this (example output; the vendor ID is always `0bda`, and the product ID is `8832` or `885a` depending on the unit):

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

### Step 3: Clone Driver from GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **NOTE:** The maintained upstream driver is [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). If GitHub is slow, use a proxy or mirror you trust. You can also download archives from [files.alfa.com.tw](https://files.alfa.com.tw).

### Step 4: Compile and Install

```bash
sudo ./install-driver.sh
sudo reboot
```

Verify the driver loaded:

```bash
lsmod | grep 8852bu
iwconfig
```

### Step 5: Enable Monitor Mode {#enable-monitor-mode}

> **Not supported:** The community rtl8852bu driver for the RTL8832BU does not support monitor mode, so there are no commands to run here. If you need monitor mode, use an adapter with an in-kernel MediaTek driver such as the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/).

### Step 6: Test Packet Injection {#test-packet-injection}

> **Not supported:** Packet injection depends on monitor mode, which this driver does not provide. Use the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/) (in-kernel MediaTek driver) for injection testing.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — DKMS required

Ubuntu 24.04 (kernel 6.8) does not include a driver for the RTL8832BU. Switch to a domestic mirror, then build the driver as for Ubuntu 22.04 below.

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
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

After the reboot, run `sudo modprobe 8852bu` and `iwconfig`. If the module loads and an interface appears, you are done (managed mode only; monitor mode is not supported).

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Monitor mode is not supported by this driver (see Kali Step 5).

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
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Virtual Machine USB Passthrough {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Settings → USB** → Enable **USB 3.0 (xHCI)**.
2. Add filter: **Realtek** (Vendor ID: 0bda, Product ID: 8832 or 885a).
3. Start VM → `lsusb` to confirm → follow Kali steps.

### VMware

1. **Virtual Machine → USB & Bluetooth** → Find **Realtek RTL8832BU** → **Connect**.
2. `lsusb` to confirm → follow Kali steps.

---

{{< faq >}}

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `lsusb` doesn't show 0bda:8832 or 0bda:885a | Adapter not detected | Try different USB port |
| `install-driver.sh` fails | Missing headers | `sudo apt install linux-headers-$(uname -r)` |
| GitHub clone fails or is slow | Network issue | Use a proxy or mirror you trust |
| `modprobe 8852bu` fails | Driver not built or not loaded | Re-run `sudo ./install-driver.sh`, check `sudo dkms status`, then reboot |
| Monitor mode / injection does not work | Not supported by the rtl8852bu driver | Use AWUS036ACM for pentest work |

> **Note on VIF:** The RTL8832BU out-of-kernel driver does not support Virtual Interfaces (VIF).

## China Mirror Reference

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU driver |
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

## References

1. [Realtek Official Website](https://www.realtek.com/)
2. [ALFA Network Official Website](https://www.alfa.com.tw/)
3. [Kali Linux Official Documentation](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
