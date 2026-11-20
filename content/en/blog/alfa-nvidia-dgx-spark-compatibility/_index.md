---
title: "ALFA Wireless Card Compatibility with NVIDIA DGX Spark (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-dgx-spark-compatibility"
tags:
  - "ALFA"
  - "NVIDIA"
  - "DGX-Spark"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Hardware Guide"
description: "9 ALFA USB Wi-Fi adapters on NVIDIA DGX Spark (GB10): ASUS GX10 tests on kernel 6.17 show in-kernel drivers, no DKMS; EACS/ACH/ACS inject best, AXM/AXML fail."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Updated with November 2026 GX10 test results: on the ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), all 9 current ALFA adapters use in-kernel drivers and work as soon as they are plugged in, with no DKMS needed. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Tested on the GX10 only; other GB10 models have not been tested individually.

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network card be used on the NVIDIA DGX Spark (GB10 Grace Blackwell) personal AI supercomputer?"

Short Conclusion: The DGX Spark runs NVIDIA DGX OS (based on Ubuntu, kernel 6.x). We tested ALFA's 9 current USB network cards on the ASUS GX10, which is also a GB10 platform (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia): all of them use in-kernel drivers and work as soon as they are plugged in, with no compilation or DKMS required. The DGX Spark uses the same GB10 chip and NVIDIA kernel series, so the same behavior is expected, but testing was done on the GX10 only; the DGX Spark itself has not been tested. Functional differences: the MediaTek MT7921 models (AWUS036AXM / AXML) fail packet injection on the stock 6.17 kernel, while monitor, AP and WPA3 work; monitor mode and injection were verified working on the other 7 models. The minimum kernel version at which each driver entered mainline differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); only older kernels below that version need community DKMS drivers. Note: All USB ports on the DGX Spark are USB Type-C, while the ALFA network cards are USB Type-A, so a USB-C to USB-A adapter or cable is required.

Assessment Subject: ALFA's current 9 USB network cards (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analysis of Target Hardware Specifications

### 2.1 NVIDIA DGX Spark Hardware Specifications

| Item | Specification |
|---|---|
| Product Name | NVIDIA DGX Spark |
| Core Chip | NVIDIA GB10 Grace Blackwell Superchip |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell architecture, 6144 CUDA cores, fifth-generation Tensor Core, fourth-generation RT Core |
| AI Performance | Up to 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| System Memory | 128GB LPDDR5x unified memory (256-bit, 273 GB/s) |
| Storage | Up to 4TB NVMe M.2 SSD (self-encrypting) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), one of which supports PD input (180W EPR PD3.1) |
| Display Output | 1× HDMI 2.1a |
| Ethernet | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (200G QSFP) |
| Wireless Network | Wi-Fi 7 (built-in) + Bluetooth 5.4 |
| Operating System | NVIDIA DGX OS (based on Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Size | 150 × 150 × 50.5 mm (1.13L) |
| Weight | Approximately 1.2 kg |
| Power Supply | 240W USB-C power supply |

### 2.2 Software Environment: NVIDIA DGX OS

| Item | Description |
|---|---|
| Base | Ubuntu Linux (NVIDIA customized) |
| Kernel | Linux 6.x (specific version varies with DGX OS updates) |
| Architecture | aarch64 (ARM64) |
| Pre-installed Software | NVIDIA AI software stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Package Management | apt (Debian/Ubuntu) |
| Driver Framework | Standard Linux kernel driver architecture (cfg80211 / mac80211) |

### 2.3 Key Features: Modern Kernel + ARM64

The software environment of the DGX Spark has two key impacts on the compatibility with the ALFA network card:

- Kernel 6.x (modern): Kernel 6.17 (the version tested on the GX10) already includes drivers for all 9 cards in this article, including mt76 (MT7612U / MT7610U, 4.19+), mt7921u (MT7921AUN, 5.18+), rtw88 (RTL8821CU 6.2+; RTL8812AU / RTL8811AU 6.13+) and rtw89 (RTL8832BU, 6.17+). This contrasts sharply with the kernel 4.9 of Jetson Nano.
- ARM64 (aarch64) architecture: With the in-kernel drivers, nothing needs to be compiled on ARM64. Only on older systems with a kernel below a card's minimum version do the Realtek models need community DKMS drivers compiled (such as the morrownr series, where you must confirm that CONFIG_PLATFORM_ARM64 = y is set in the Makefile).

### 2.4 USB Type-C Adapter Requirement

The 4 USB ports on the DGX Spark are all Type-C, while all ALFA network cards (except AXML for USB-C) are USB Type-A interface:

| Model | Interface Specification | Adapter Needed? |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ No adapter needed (can be inserted directly) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Needs USB-C to USB-A |
| AWUS036AX | USB Type-A / USB 3.2 | ✅ Needed |
| AWUS036AXER | USB Type-A / USB 3.2 | ✅ Needed |
| AWUS036ACH | USB Type-A / USB 3.0 | ✅ Needed |
| AWUS036ACHM | USB Type-A / USB 2.0 | ✅ Needed |
| AWUS036ACM | USB Type-A / USB 3.0 | ✅ Needed |
| AWUS036ACS | USB Type-A / USB 2.0 | ✅ Needed |
| AWUS036EACS | USB Type-A / USB 2.0 | ✅ Needed |

Recommendation: Use a USB-C to USB-A adapter or cable that supports USB 3.2 Gen 2×2 (20Gbps), so that USB 3.x models such as AWUS036ACH / ACM / AX can run at full speed.

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current USB wireless network card product line is as follows (assessment subject: 9 models):

| Model | Wi-Fi Level | Chipset | Interface | Linux In-kernel Driver (minimum kernel version) |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E (6GHz verified) | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ In-kernel (mt7921u, 5.18+) |
| AWUS036AXM | Wi-Fi 6E (vendor spec, 6GHz not tested) | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ In-kernel (mt7921u, 5.18+) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ In-kernel (rtw89_8852bu, 6.17+) |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ✅ In-kernel (rtw89_8852bu, 6.17+) |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ In-kernel (rtw88_8812au, 6.13+) |
| AWUS036ACHM | Wi-Fi 5 (AC600) | MediaTek MT7610U | USB 2.0 | ✅ In-kernel (mt76x0u, 4.19+) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ In-kernel (mt76x2u, 4.19+) |
| AWUS036ACS | Wi-Fi 5 (AC600) | Realtek RTL8811AU | USB 2.0 | ✅ In-kernel (rtw88_8821au, 6.13+) |
| AWUS036EACS | Wi-Fi 5 (AC600) + Bluetooth | Realtek RTL8821CU | USB 2.0 | ✅ In-kernel (rtw88_8821cu, 6.2+) |

Note: The kernel 6.17 tested on the GX10 already includes drivers for all 9 cards; the minimum kernel version differs by card (see the parentheses in the table above). Only older systems running a kernel below a card's minimum version need community-maintained DKMS drivers.

## 4. Applicable Models and Chipsets

### 4.1 Recommended Grade Classification

| Recommended Grade | Model (Chipset) | Description |
|---|---|---|
| ⭐ Top Pick for Penetration Testing | AWUS036EACS (RTL8821CU) / AWUS036ACH (RTL8812AU) / AWUS036ACS (RTL8811AU) | In-kernel driver, nothing to install; measured injection: EACS and ACH 100% on both bands, ACS 100% on 2.4GHz and 96% on 5GHz; end-to-end WPA handshake capture works |
| ✅ Recommended | AWUS036ACM (MT7612U) | In-kernel driver, nothing to install; monitor, injection (2.4GHz 63–83%, 5GHz 76%), AP and WPA3 all work |
| ✅ Recommended | AWUS036ACHM (MT7610U) | In-kernel driver, nothing to install; 2.4GHz injection 96–100%, 5GHz injection works for broadcast only; WPA3 AP requires sae_pwe=0 |
| ✅ Recommended (Wi-Fi 6) | AWUS036AX / AXER (RTL8832BU) | In-kernel driver, nothing to install; strong monitor reception, injection works (2.4GHz: AX 96%, AXER 73%), AP supports 80MHz |
| ⚠️ Connection / AP Only | AWUS036AXML / AXM (MT7921AUN) | In-kernel driver, nothing to install; monitor, AP and WPA3 work, but injection fails on the stock 6.17 kernel, so they are not suitable for penetration testing; AXML is USB-C and plugs in directly |

### 4.2 Usage Scenario Recommendations

| Usage Scenario | Recommended Model | Description |
|---|---|---|
| General Wireless Internet (simplest) | Any of the 9 models (e.g. AWUS036ACM / ACHM) | All use in-kernel drivers and work as soon as they are plugged in |
| Wireless Penetration Testing / Monitoring / Injection | AWUS036EACS / ACH / ACS | Measured injection 96–100%, end-to-end WPA handshake capture works; avoid AXM / AXML (injection fails) |
| Wi-Fi 6 + AP Hotspot | AWUS036AX / AXER | 2x2, 80MHz AP verified working |
| 6GHz Band | AWUS036AXML | Verified able to run a WPA3 AP on 6GHz; AXM uses the same chip but 6GHz was not tested |
| Already own an AWUS036ACH and want to keep using it | AWUS036ACH | Kernel 6.13 and later include rtw88_8812au, so it works as soon as it is plugged in; measured injection 100% on both bands |
| No external WiFi needed (use built-in) | — | DGX Spark has built-in Wi-Fi 7, so general internet access does not require an external ALFA card |

Note: The DGX Spark already has built-in Wi-Fi 7 + Bluetooth 5.4, so general internet use does not require an external ALFA network card. The main reasons to add an external ALFA card are penetration testing (monitoring / injection), specific chipset requirements, or situations where the built-in WiFi is not enough.

## 5. Environmental Requirements

### 5.1 Hardware Requirements

| Item | Requirement |
|---|---|
| USB Adapter | USB-C to USB-A adapter or cable (except AXML) |
| Power Supply | DGX Spark OEM 240W USB-C power supply (sufficient USB port power) |
| Cooling | Stock cooling is sufficient (a USB WiFi adapter does not noticeably increase system load) |

### 5.2 Software Requirements

| Item | Requirement |
|---|---|
| DGX OS Version | Any active version (kernel 6.x) |
| Kernel Version | Kernel 6.17 (GX10 tested on 6.17.0-1014-nvidia) includes drivers for all 9 cards, so no compilation tools are needed; the minimum version differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), and only kernels below that version need community DKMS drivers |
| Wireless Management Tools | iw, wpa_supplicant, network-manager (installed by default in DGX OS) |

## 6. Compatibility Determination

### ALFA Current Models × NVIDIA DGX Spark (GB10) Compatibility Matrix

| Model | Chipset | Driver (in-kernel) | USB Detection | STA Internet | AP Mode | Monitor | Packet Injection | Installation Difficulty | Overall Rating |
|---|---|---|---|---|---|---|---|---|---|
| AWUS036EACS | RTL8821CU | rtw88_8821cu | ✅ | ✅ | ✅ | ✅ | ✅ 100% on both bands | No installation required | ⭐ Best |
| AWUS036ACH | RTL8812AU | rtw88_8812au | ✅ | ✅ | ✅ | ✅ | ✅ 100% on both bands | No installation required | ⭐ Best |
| AWUS036ACS | RTL8811AU | rtw88_8821au | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 100% / 5G 96% | No installation required | ⭐ Best |
| AWUS036ACM | MT7612U | mt76x2u | ✅ | ✅ | ✅ | ✅ | ✅ 2.4G 63–83% / 5G 76% | No installation required | ✅ Good |
| AWUS036ACHM | MT7610U | mt76x0u | ✅ | ✅ | ✅ | ✅ | ⚠️ 2.4G 96–100% / 5G broadcast only | No installation required | ✅ Good |
| AWUS036AX | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Strong reception | ✅ 2.4G 96% / 5G works | No installation required | ✅ Good |
| AWUS036AXER | RTL8832BU | rtw89_8852bu | ✅ | ✅ | ✅ | ✅ Strong reception | ✅ 2.4G 73% / 5G works | No installation required | ✅ Good |
| AWUS036AXML | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Weak reception | ❌ Fails | No installation required | ⚠️ Connection / AP only |
| AWUS036AXM | MT7921AUN | mt7921u | ✅ | ✅ | ✅ | ⚠️ Weak reception | ❌ Fails | No installation required | ⚠️ Connection / AP only |

Determination Criteria: Hands-on tests on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) from 2026-11-16 to 2026-11-18, using our own Wi-Fi network and our own phone as test targets. The DGX Spark uses the same GB10 chip and NVIDIA kernel series, so the same behavior is expected, but testing was done on the GX10 only; the DGX Spark itself has not been tested. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detailed Step by Step Setup Steps

### 7.1 Preparation

**Step 1: Power on and log in to the DGX Spark** (via SSH or with a keyboard and monitor attached directly)

```bash
ssh username@<dgx-spark-ip>
```

**Step 2: Check the system architecture and kernel version**

```bash
uname -m
# Expected: aarch64
uname -r
# Expected: 6.x.x (DGX OS kernel)
```

**Step 3: Confirm the kernel is 6.17 or later**

Kernel 6.17 and later include drivers for all 9 cards, so there is no need to install compilation tools. The minimum version differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); below that version, only the Realtek models need community DKMS drivers (see the last paragraph of 7.3).

### 7.2 Path A: MediaTek Chip Models (AWUS036ACM / ACHM / AXML / AXM) — Ready to Use

**Step 1: Insert the network card**

Use a USB-C to USB-A adapter (AXML can be inserted directly into a USB-C port) to plug the ALFA network card into a USB port on the DGX Spark.

**Step 2: Confirm the network card is detected**

```bash
lsusb
# Expected output example (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Step 3: Confirm the network interface was created automatically**

```bash
ip link show
# Expect an interface whose name starts with wlx (named after the MAC address; the in-kernel driver loads automatically)
```

**Step 4: Scan for WiFi networks** (wlan0 is used below as an example; replace it with the interface name shown by `ip link show`)

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Step 5: Connect to WiFi (using NetworkManager)**

```bash
nmcli dev wifi list
nmcli dev wifi connect "YourWiFiName" password "YourWiFiPassword"
```

**Step 6: (Optional) Enable monitor mode**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info
```

### 7.3 Path B: Realtek Wi-Fi 5 Models (AWUS036ACH / ACS / EACS) — Nothing to Install on Kernel 6.13+ (EACS 6.2+)

**Step 1: Insert the network card and confirm the driver loaded automatically**

```bash
uname -r          # ACH/ACS need 6.13 or later, EACS needs 6.2 or later
lsusb
lsmod | grep rtw88
ip link show
```

Modules loaded automatically for each model: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu` (EACS also includes Bluetooth, verified working).

**Step 2: Connect the same way as Step 5 in 7.2 (using nmcli)**

**Step 3: (Optional) Monitor mode and injection**

⚠️ Only perform monitoring and injection tests on networks you own or are authorized to test.

```bash
sudo apt install -y aircrack-ng
IF=wlx00c0cafe0000   # replace with the interface name shown by ip link
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
sudo aireplay-ng --test $IF
```

- Do not run `airmon-ng check kill`: it stops NetworkManager and cuts the host off the network.
- On the stock 6.17 kernel, `aireplay-ng --test` fails on AWUS036AXM / AXML (Found 0 APs), so deauth and handshake capture are not possible.
- hcxdumptool 8.x reports `failed to arm` on all 9 cards except the EACS on 2.4 GHz (the drivers do not support active monitor); use airodump-ng + aireplay-ng instead.

**Steps needed only on older kernels (ACH/ACS below 6.13, EACS below 6.2)**: install `build-essential git bc dkms`, then compile a community driver, for example morrownr/8812au-20210820 for RTL8812AU (confirm `CONFIG_PLATFORM_ARM64 = y` in the Makefile). If your kernel version is new enough, simply use the in-kernel driver.

### 7.4 Path C: Wi-Fi 6 Models (AWUS036AX / AXER, RTL8832BU) — Nothing to Install on Kernel 6.17+

```bash
lsusb                      # expect 0bda:b832
lsmod | grep rtw89_8852bu
ip link show
```

GX10 test results: the in-kernel `rtw89_8852bu` loads automatically, monitor reception is strong, injection works (2.4GHz: AX 96%, AXER 73%), and AP supports 80MHz. rtw89_8852bu entered mainline only in kernel 6.17, so systems running kernel 6.16 or earlier need the community DKMS driver (morrownr/rtl8852bu-20250826).

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not see the ALFA network card | Faulty USB-C adapter / poor contact | Replace the USB-C to USB-A adapter; make sure the adapter supports data transfer (not charge-only); try a different USB-C port |
| MediaTek chip shows no wlan interface after plugging in | Kernel module not loaded automatically / firmware missing | Load manually: `sudo modprobe mt76x2u`; check `dmesg \| grep mt76`; install firmware: `sudo apt install linux-firmware` |
| Realtek card shows no wlan interface after plugging in | Kernel below that card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), so the matching driver is not built in | Check the version with `uname -r`; upgrade the kernel, or install a community DKMS driver on the older kernel |
| modprobe reports Operation not permitted after installing a DKMS driver on an older kernel | Secure Boot / module signing | Sign the module or disable Secure Boot (does not occur with the in-kernel drivers) |
| No networks visible after repeatedly switching between monitor and AP | RX stall | Unplug and replug the card so USB re-enumerates it |
| EACS / AXML shows no wlx interface after replugging | Bluetooth + Wi-Fi composite device probe hangs | Replug into a different USB port |
| Unstable WiFi connection / slow speed | USB-C adapter only supports USB 2.0 | Replace with an adapter that supports USB 3.2 Gen 2×2; make sure the adapter is labeled "Data" rather than "Charge Only" |
| Built-in Wi-Fi 7 conflicts with the external ALFA card | Routing conflict between two wireless interfaces | Disable built-in WiFi: `sudo nmcli radio wifi off`, or disable it in BIOS/UEFI; or set route priorities |
| 6GHz (Wi-Fi 6E) cannot be used | Regulatory Domain restriction | Set the regulatory region: `sudo iw reg set US` (6GHz is open in the US); AXML has been verified working on 6GHz, AXM has not been tested |
| AP mode fails to start | Conflict between NetworkManager and hostapd | See the Yopitek ALFA Soft AP guide; stop NetworkManager from managing the interface, then configure hostapd manually |
| Network card disappears after wake-up | USB autosuspend | Disable USB autosuspend: `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |

## 9. Known Limitations

- USB Type-C Adapter Requirement: All ALFA network cards except AXML require a USB-C to USB-A adapter, and the adapter quality affects performance and stability.
- MT7921 Models Fail Injection: AWUS036AXM / AXML fail packet injection on the stock 6.17 kernel, so deauth and handshake capture are not possible; monitor, AP and WPA3 work. The main cause is a mac80211 chanctx regression in kernel 6.16 and later, and the community-patched driver is still rate-limited.
- Test Scope: Tested only on the ASUS GX10 (kernel 6.17.0-1014-nvidia); the DGX Spark has not been tested individually, but the same behavior is expected.
- hcxdumptool Not Usable: All cards except the EACS on 2.4 GHz report `failed to arm`; use airodump-ng + aireplay-ng instead.
- Built-in Wi-Fi 7 May Conflict with External Devices: The DGX Spark has built-in Wi-Fi 7, and using built-in and external WiFi at the same time can cause routing or resource conflicts.
- AP Mode Requires Manual Configuration: DGX OS is set up as a development environment by default; AP hotspot mode requires installing and configuring hostapd / dnsmasq manually.
- 6GHz Regulatory Limitations: Availability of the Wi-Fi 6E 6GHz band depends on the regulatory region setting; check the latest regulations for 6GHz availability in Taiwan.
- Older Kernels: On systems with a kernel below a card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), the Realtek models need community DKMS drivers (morrownr), which must be recompiled after every kernel update.
- Penetration Testing Differences: In the GX10 tests, the Realtek rtw88 models had the highest injection success rates (EACS and ACH 100% on both bands); the MediaTek mt76 models (ACM / ACHM) work; MT7921 (AXM / AXML) fails.
- Bluetooth: Bluetooth on the AWUS036AXML and AWUS036EACS was verified working on the GX10; Bluetooth on the AWUS036AXM was not verified separately (the DGX Spark already has built-in BT 5.4).
- RTL8832BU (AWUS036AX / AXER): Driver maintainer morrownr has publicly advised avoiding the out-of-tree drivers for the rtl8852/32au series (see Section 10 for the source). This GX10 test used the in-kernel `rtw89_8852bu`, with which monitor, injection, AP and WPA3 all work; this conclusion applies only to the in-kernel driver on kernel 6.17 and later.
- RTL8812AU (AWUS036ACH): The mac80211-based in-kernel driver `rtw88_8812au` was merged into mainline in kernel 6.13 and has been mature since 6.14 (per morrownr's announcement). In the GX10 test on kernel 6.17 it worked as soon as it was plugged in, with 100% injection on both bands. Before answering a customer, support staff can ask them to report `uname -r` to confirm the kernel is 6.13 or later.

Counter-conditions: If a DGX OS update changes the kernel version or USB controller driver and the behavior differs, or if testing on an actual DGX Spark produces results different from the GX10, the compatibility matrix in Section 6 of this article needs to be reviewed again; if a future kernel fixes the mt7921u injection issue, the rating of AWUS036AXM / AXML can be upgraded from "Connection / AP only".

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| NVIDIA DGX Spark Official Page | DGX Spark specifications and platform information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Documentation | DGX OS system architecture and kernel version | https://docs.nvidia.com/dgx/dgx-spark | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux driver (ARM64 support) | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8821CU Linux driver (for older kernels) | https://github.com/morrownr/8821cu-20210916 | ✅ Verified | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux driver | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verified | 2026-09-03 |
| Linux kernel mt76 driver documentation | MediaTek mt76 / mt7921 mainline driver notes (including the first kernel version supporting each chip) | https://wireless.wiki.kernel.org/en/users/drivers/mediatek | ✅ Verified | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide (Yopitek) | Guide to configuring ALFA AP mode on Linux | /en/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verified | 2026-09-03 |
| ALFA 9-Card ARM64 Test Matrix (Yopitek) | Hands-on tests on ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Tested | 2026-11-18 |
| ALFA Network Product Overview (Yopitek) | ALFA Current Product Specifications | /en/products/alfa/ | ✅ Verified | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Official statement from the driver maintainer: recommends avoiding the rtl8852/32au (RTL8832BU) chips | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Verified | 2026-09-03 |
| morrownr/8812au-20210820 GitHub | Latest RTL8812AU driver status announcement (merged into mainline in kernel 6.13, mature from 6.14) | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |

Related Articles: [Is ALFA Wireless Card Compatible with MSI EdgeXpert](/en/blog/alfa-msi-edgexpert-compatibility/) | [Is ALFA Wireless Card Compatible with ASUS Ascent GX10](/en/blog/alfa-asus-ascent-gx10-compatibility/) | [Is ALFA Wireless Card Compatible with ALTOS BrainSphere GB10 F1](/en/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Is ALFA Wireless Card Compatible with GIGABYTE AI TOP ATOM](/en/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Is ALFA Wireless Card Compatible with NVIDIA Jetson Nano](/en/blog/alfa-nvidia-jetson-nano-compatibility/)

Disclaimer: The compatibility determination in this article is based on hands-on tests performed in November 2026 on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). The DGX Spark uses the same GB10 chip and NVIDIA kernel series as the GX10, so the same behavior is expected, but it has not been tested individually. The kernel 6.17 tested on the GX10 already includes drivers for all 9 ALFA network cards (the minimum version differs by card); community DKMS drivers are needed only when the kernel is below a card's minimum version (morrownr). The DGX Spark has built-in Wi-Fi 7, and an external ALFA network card is mainly used for penetration testing or special chipset requirements. The quality of the USB-C adapter directly affects the user experience, so choose a branded adapter labeled USB 3.2 Gen 2×2. Monitoring and injection must only be performed on networks you own or are authorized to test.
