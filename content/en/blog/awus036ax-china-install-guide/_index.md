---
title: "ALFA AWUS036AX Driver Install Guide for China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Step-by-step guide to install ALFA AWUS036AX drivers in China using domestic mirrors. RTL8832BU driver, WiFi 6 AX1800. Covers Kali Linux, Ubuntu 22/24 (DKMS), Debian, and Raspberry Pi."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "What chipset does AWUS036AX use? Does it support WiFi 6?"
    answer: "It uses the Realtek RTL8832BU chipset, supporting WiFi 6 (802.11ax) high-speed networking."
  - question: "Does AWUS036AX need a driver on Ubuntu 24.04?"
    answer: "It depends on your kernel. Linux kernel 6.17 and newer (for example Ubuntu 24.04 HWE / kernel 6.17) ships the in-kernel rtw89_8852bu driver — plug-and-play, no DKMS. Only on kernels older than 6.17 do you build the community rtl8852bu driver (morrownr/rtl8852bu-20250826) once via DKMS. Check with uname -r first."
  - question: "Is AWUS036AX suitable for wireless security research?"
    answer: "Yes. With the in-kernel rtw89_8852bu driver on kernel 6.17+, monitor mode and packet injection both work in our testing (Ubuntu 24.04 / kernel 6.17: injection 96% on 2.4GHz, and an end-to-end WPA .22000 capture). Note: on older kernels using the community DKMS driver, monitor support may be limited. Only on networks you own or are authorized to test."
  - question: "Do I need a VPN to install AWUS036AX in China?"
    answer: "Not necessarily. Clone the driver from the verified GitHub repository (morrownr/rtl8852bu-20250826); if GitHub is slow, use a proxy or mirror you trust. Build tools can still be installed from domestic mirrors."
  - question: "What is the USB ID of AWUS036AX?"
    answer: "The Realtek RTL8832BU vendor ID is 0bda. The product ID is 8832 or 885a depending on the unit, so confirm yours with lsusb."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 4
related_product: "/en/products/alfa/awus036ax/"
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

The AWUS036AX is ALFA's WiFi 6 AX1800 dual-band adapter. Its RTL8832BU chip is supported by the **in-kernel rtw89_8852bu driver on Linux kernel 6.17 and newer** (for example Ubuntu 24.04 HWE / kernel 6.17) — plug-and-play, no compile. Only on **older kernels** (below 6.17) do you build the community rtl8852bu driver once with DKMS. This guide covers both. The driver source is cloned from the verified GitHub repository; if GitHub is slow, use a proxy or mirror you trust.

{{< tldr >}}
AWUS036AX uses the RTL8832BU chipset with WiFi 6 support. Kernel 6.17+ (incl. Ubuntu 24.04 / kernel 6.17) has the in-kernel rtw89_8852bu driver — no DKMS, with monitor mode and injection working in testing. Older kernels need the community rtl8852bu driver via DKMS.
{{< /tldr >}}





> **Security research note:** With the **in-kernel rtw89_8852bu driver on kernel 6.17+**, AWUS036AX's monitor mode and packet injection work in testing (Ubuntu 24.04 / kernel 6.17: 2.4GHz injection 96%, end-to-end WPA .22000). Only on older kernels using the community DKMS driver is monitor support limited. Check `uname -r` first. Only on networks you own or are authorized to test.

## Before You Start

1. **ALFA AWUS036AX** adapter
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

> **Works on kernel 6.17+:** With the in-kernel rtw89_8852bu driver, monitor mode works:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> On older kernels using the community DKMS driver, monitor support may be limited — there you can switch to an in-kernel MediaTek adapter such as the [AWUS036ACM](/en/blog/awus036acm-china-install-guide/).

### Step 6: Test Packet Injection {#test-packet-injection}

> **Works on kernel 6.17+:** After entering monitor mode, test injection with aireplay-ng (96% on 2.4GHz in testing):
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Only on networks you own or are authorized to test. On older kernels where the community DKMS driver lacks monitor mode, injection is unavailable too.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

On Ubuntu 24.04, only an **HWE kernel 6.17 or newer** (e.g. the 24.04.4 HWE) includes the in-kernel rtw89_8852bu driver — just plug in, no build needed. On the **GA kernel 6.8** or the **HWE kernel 6.14** (neither includes this driver), switch to a domestic mirror and build the community driver as for Ubuntu 22.04 below, or upgrade to an HWE kernel 6.17 or newer to get the in-kernel driver.

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

After the reboot, run `sudo modprobe 8852bu` and `iwconfig`. If the module loads and an interface appears, you are done (this is the community DKMS driver path for older kernels, where monitor support may be limited; on kernel 6.17+ the in-kernel rtw89_8852bu is used and monitor mode and injection work).

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

This community DKMS driver path applies to kernels older than 6.17, where monitor support may be limited (see Kali Step 5). On kernel 6.17+ the in-kernel rtw89_8852bu driver is used and monitor mode works.

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
| Monitor mode / injection does not work | Kernel older than 6.17 using the community rtl8852bu DKMS driver (monitor support may be limited) | Check `uname -r`; use kernel 6.17+ (in-kernel rtw89_8852bu), or AWUS036ACM on older kernels |

> **Note on VIF:** The RTL8832BU out-of-kernel driver does not support Virtual Interfaces (VIF).

## China Mirror Reference

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver packages |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | RTL8832BU driver |
| 清华大学镜像 (Tsinghua University mirror) | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 (Aliyun mirror) | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| 中科大镜像 (USTC mirror) | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| 华为云镜像 (Huawei Cloud mirror) | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

## More Alfa Adapter Guides for China

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, full VIF
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/) — RTL8811AU, monitor mode
- AWUS036AX ← you are here
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — MT7921AUN, L-shape
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [AWUS036EACS China Install Guide](/en/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).

## References

1. [Realtek Official Website](https://www.realtek.com/)
2. [ALFA Network Official Website](https://www.alfa.com.tw/)
3. [Kali Linux Official Documentation](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
