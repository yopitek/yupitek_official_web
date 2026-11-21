---
title: "ALFA AWUS036EACS Setup Guide for China: Windows Installation & Linux Compatibility"
description: "Setup guide for ALFA AWUS036EACS in China. RTL8821CU WiFi 5 + Bluetooth 4.2 nano adapter. Windows driver available at files.alfa.com.tw. On Linux kernel 6.2+ the in-kernel rtw88_8821cu driver works out of the box — monitor mode and injection tested working."
date: 2026-04-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "What chipset does AWUS036EACS use? Does it support Bluetooth?"
    answer: "It uses the Realtek RTL8821CU chipset, supporting WiFi 5 and Bluetooth 4.2."
  - question: "Is AWUS036EACS recommended for Linux?"
    answer: "Yes. On Linux kernel 6.2+ (e.g. Ubuntu 24.04 HWE / kernel 6.17) the in-kernel rtw88_8821cu driver works out of the box with no compilation. We measured monitor mode and packet injection at 100% on both bands (2.4 GHz / 5 GHz) with end-to-end WPA .22000 capture, and Bluetooth tested working too."
  - question: "How do I install AWUS036EACS drivers on Windows?"
    answer: "Download the Windows driver package from files.alfa.com.tw, install as administrator, and reboot."
  - question: "How do I enable Bluetooth on AWUS036EACS?"
    answer: "After installing the driver, Bluetooth usually activates automatically. Turn on the Bluetooth switch in Windows settings to connect devices."
  - question: "If I need a Linux wireless security research adapter, which should I choose?"
    answer: "The AWUS036EACS itself works for monitor mode and packet injection on kernel 6.2+, with Bluetooth as a bonus. If you want more options, the AWUS036ACM and AWUS036ACS also fully support monitor mode on Linux. Use only on networks you own or are authorized to test."
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 8
related_product: "/en/products/alfa/awus036eacs/"
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
hideFeatureImage: true  # 1024x1024／16:9 原圖在 975x280 框內會裁掉過半，暫不顯示頁面封面；featureimage 保留供社群分享預覽
---

The AWUS036EACS is ALFA's nano WiFi 5 + Bluetooth 4.2 combo adapter. It is a compact wireless upgrade for Windows users, and on Linux kernel 6.2+ the in-kernel rtw88_8821cu driver supports it out of the box — no compilation needed. This guide covers Windows installation from Chinese sources and the Linux experience.

{{< tldr >}}
AWUS036EACS uses the RTL8821CU chipset. A WiFi 5 plus Bluetooth 4.2 mini adapter that is easy to install on Windows; on Linux kernel 6.2+ the in-kernel rtw88_8821cu driver is bundled, so monitor mode and packet injection work out of the box, and Bluetooth is tested working too.
{{< /tldr >}}

> **The AWUS036EACS works out of the box on Linux kernel 6.2+.** Kernels 6.2 and newer (e.g. Ubuntu 24.04 HWE / kernel 6.17) bundle the in-kernel rtw88_8821cu driver, so no compilation is needed. We measured monitor mode and packet injection at 100% on both bands (2.4 GHz / 5 GHz), captured a WPA handshake end-to-end (.22000), and Bluetooth (BT) is tested working too (BR/EDR + BLE both scan devices, and coexist with WiFi). Use only on networks you own or are authorized to test.
>
> **Operational tip:** This is a BT+WiFi combo card. After repeatedly switching modes, WiFi RX may stall (`ip link set up` returns `Operation already in progress`, and `iw ... set channel` returns `-16 busy`). Before each test stage, unplug the adapter and replug it into a different USB port to recover.
>
> Other Linux adapters in the same series:
> - **[AWUS036ACM](/en/blog/awus036acm-china-install-guide/)** — MT7612U in-kernel driver, full monitor mode + VIF
> - **[AWUS036ACS](/en/blog/awus036acs-china-install-guide/)** — RTL8811AU, budget-friendly monitor mode






## Linux Users: Please Read First

> **The AWUS036EACS works out of the box on Linux kernel 6.2+.** Kernels 6.2 and newer (e.g. Ubuntu 24.04 HWE / kernel 6.17) bundle the in-kernel rtw88_8821cu driver, so no compilation is needed. We measured monitor mode and packet injection at 100% on both bands (2.4 GHz / 5 GHz), captured a WPA handshake end-to-end (.22000), and Bluetooth (BT) is tested working too (BR/EDR + BLE both scan devices, and coexist with WiFi). Use only on networks you own or are authorized to test.
>
> **Operational tip:** This is a BT+WiFi combo card. After repeatedly switching modes, WiFi RX may stall (`ip link set up` returns `Operation already in progress`, and `iw ... set channel` returns `-16 busy`). Before each test stage, unplug the adapter and replug it into a different USB port to recover.
>
> Other Linux adapters in the same series:
> - **[AWUS036ACM](/en/blog/awus036acm-china-install-guide/)** — MT7612U in-kernel driver, full monitor mode + VIF
> - **[AWUS036ACS](/en/blog/awus036acs-china-install-guide/)** — RTL8811AU, budget-friendly monitor mode

---

## Windows 10 / 11 Setup

### Step 1: Download Driver from Alfa

The official Alfa driver server is accessible from China:

https://files.alfa.com.tw

Navigate to the **AWUS036EACS** product folder and download the Windows driver package (`.zip` or `.exe`).

Alternatively, visit the documentation page:
https://docs.alfa.com.tw/Product/AWUS036EACS/

### Step 2: Install the Driver

1. Extract the downloaded zip file.
2. Right-click the installer `.exe` and select **Run as administrator**.
3. Follow the on-screen instructions.
4. Reboot when prompted.

### Step 3: Verify the Adapter

After reboot, open **Device Manager** (press Win+X → Device Manager).

Under **Network Adapters**, you should see:

```
Realtek 8821CU Wireless LAN 802.11ac USB NIC
```

The adapter is now ready to connect to 2.4 GHz and 5 GHz networks.

### Step 4: Connect to WiFi

1. Click the WiFi icon in the taskbar.
2. Select your network.
3. Enter the password and connect.

---

## Bluetooth Setup (Windows)

The AWUS036EACS includes Bluetooth 4.2. After the driver is installed:

1. Open **Settings → Bluetooth & devices**.
2. Toggle Bluetooth **On**.
3. Click **Add device** to pair keyboards, mice, headphones, or other Bluetooth peripherals.

---

## Linux Compatibility Details

On **kernel 6.2+** the RTL8821CU is driven by the in-kernel `rtw88_8821cu` module, so there is nothing to compile — plug it in and it is recognized. Confirm your kernel first with `uname -r`.

### Kali Linux

With a 6.2+ kernel the bundled `rtw88_8821cu` driver loads automatically. We tested monitor mode and packet injection at 100% on both bands (2.4 GHz / 5 GHz) and captured a WPA handshake end-to-end (.22000). Use only on networks you own or are authorized to test.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu 22.04 / 24.04

Ubuntu 24.04 ships the in-kernel `rtw88_8821cu` driver (mainline since kernel 6.2) on both the GA kernel 6.8 and the HWE kernel (e.g. kernel 6.17) — monitor mode, packet injection, and client connections work out of the box. On an older kernel (below 6.2, e.g. the Ubuntu 22.04 GA kernel), update to the HWE kernel to get the in-kernel driver.

### Debian / Raspberry Pi

Same story: once the kernel is 6.2 or newer (including ARM64 builds), the in-kernel `rtw88_8821cu` driver handles the adapter with no compilation.

### Operational tip (BT+WiFi combo card)

Because the EACS carries both Bluetooth and WiFi on one chip, repeatedly switching modes can leave WiFi RX stalled — `ip link set up` returns `Operation already in progress` and `iw ... set channel` returns `-16 busy`. Before each test stage, unplug the adapter and replug it into a different USB port to clear the state. Bluetooth (BR/EDR + BLE) is tested working and coexists with WiFi.

---

{{< faq >}}

## China Resources

| Resource | URL | Use for |
|----------|-----|---------|
| Alfa official drivers | [files.alfa.com.tw](https://files.alfa.com.tw) | EACS Windows driver |
| Alfa documentation | [docs.alfa.com.tw](https://docs.alfa.com.tw) | Setup guide, FAQ |
| Alfa wiki | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Product manuals |

## More Alfa Adapter Guides for China

- [AWUS036ACH China Install Guide](/en/blog/awus036ach-china-install-guide/) — RTL8812AU, high power
- [AWUS036ACM China Install Guide](/en/blog/awus036acm-china-install-guide/) — MT7612U, full VIF
- [AWUS036ACS China Install Guide](/en/blog/awus036acs-china-install-guide/) — RTL8811AU, monitor mode
- [AWUS036AX China Install Guide](/en/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [AWUS036AXER China Install Guide](/en/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [AWUS036AXM China Install Guide](/en/blog/awus036axm-china-install-guide/) — MT7921AUN, L-shape
- [AWUS036AXML China Install Guide](/en/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- AWUS036EACS ← you are here

Questions? Leave a comment below or contact us at [yupitek.com](https://yupitek.com/en/contact/).

## References

1. [ALFA Network Official Website](https://www.alfa.com.tw/)
2. [ALFA Official Driver Downloads](https://files.alfa.com.tw)
3. [Realtek Official Website](https://www.realtek.com/)
