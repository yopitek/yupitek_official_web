---
title: "Does ALFA Wireless Card Support MSI EdgeXpert (GB10)"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Hardware Guide"
description: "9 ALFA USB Wi-Fi adapters on MSI EdgeXpert (GB10): ASUS GX10 tests on kernel 6.17 show in-kernel drivers, no DKMS; EACS/ACH/ACS inject best, AXM/AXML fail."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Updated with November 2026 GX10 test results: on the ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), all 9 current ALFA adapters use in-kernel drivers and work as soon as they are plugged in, with no DKMS needed. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Tested on the GX10 only; other GB10 models have not been tested individually.

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on the MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) AI supercomputer?"

Short Conclusion: The MSI EdgeXpert and the NVIDIA DGX Spark use the same GB10 chip and the same NVIDIA kernel series. We tested ALFA's 9 current USB network cards (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML) on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia): all of them use in-kernel drivers and work as soon as they are plugged in, with no compilation or DKMS required. The same behavior is expected, but testing was done on the GX10 only; the MSI EdgeXpert itself has not been tested. Functional differences: the MediaTek MT7921 models (AWUS036AXM / AXML) fail packet injection on the stock 6.17 kernel, while monitor, AP and WPA3 work; monitor mode and injection were verified working on the other 7 models. The minimum kernel version at which each driver entered mainline differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); only older kernels below that version need community DKMS drivers. Note: All four USB ports on the EdgeXpert are USB Type-C (20Gbps), and the ALFA network cards (except AXML) require a USB-C to USB-A adapter.

Assessment Subject: ALFA's current 9 USB network cards (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analysis of Target Hardware Specification Architecture

### 2.1 MSI EdgeXpert Hardware Specifications

| Item | Specification |
|---|---|
| Product Name | MSI EdgeXpert (Models: EdgeXpert-MS-C931 / 59STW, etc.) |
| Core Chip | NVIDIA GB10 Grace Blackwell Superchip (DGX Spark Platform) |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell Architecture, 6144 CUDA Cores, 5th Generation Tensor Core, 4th Generation RT Core |
| AI Performance | Up to 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| System Memory | 128GB LPDDR5x Unified Memory (256-bit, 273 GB/s) |
| Storage | 1TB or 4TB NVMe M.2 SSD (Self-encrypting, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (Up to 20Gbps) |
| Display Output | 1× HDMI 2.1a (4× DP1.4a via USB-C Alt Mode) |
| Wired Network | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, interconnect between systems) |
| Wireless Network | Wi-Fi 7 + Bluetooth 5.4 |
| Operating System | NVIDIA DGX OS (Based on Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 151 × 151 × 52 mm (Approx. 5.95" × 5.95" × 2.05") |
| Weight | Approx. 1.2 kg (2.65 lbs) |
| Power Supply | 240W USB-C Power Supply |
| Version | Consumer Edition / Industrial Edition (EdgeXpert-MS-C931, Wide Temperature / Industrial Grade Applications) |

### 2.2 Software Environment: NVIDIA DGX OS

The MSI EdgeXpert comes pre-installed with NVIDIA DGX OS, identical to that of DGX Spark / ASUS GX10:

| Item | Description |
|---|---|
| Basic | Ubuntu Linux (NVIDIA Customized) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Pre-installed Software | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Package Management | apt |

### 2.3 Differences from DGX Spark

MSI EdgeXpert is an OEM version of the DGX Spark platform, with identical core hardware and software:

| Item | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Mechanical Design | MSI Customized Chassis, Industrial Edition Options | NVIDIA Reference Chassis |
| Storage Options | 1TB / 4TB | Up to 4TB |
| Target Market | Edge AI / Industrial AI / Desktop Development | Desktop AI Development |
| Accessories | MSI Original Accessories | NVIDIA Original Accessories |

Impact on ALFA Compatibility: No impact expected (tested on the GX10 only; other GB10 models have not been tested individually). USB controllers, kernel versions, and driver frameworks are all identical to those of DGX Spark.

### 2.4 USB Type-C Conversion Requirements

All 4 USB ports on the EdgeXpert are Type-C, while ALFA's full series of network cards (except AXML for USB-C) are USB Type-A, requiring a converter. It is recommended to choose a converter that supports USB 3.2 Gen 2×2 (20Gbps).

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current USB wireless network card product line includes the following models (parent models: 9):

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
| Edge AI Gateway Wireless Internet Access | Any of the 9 models (e.g. AWUS036ACM / ACHM) | All use in-kernel drivers and work as soon as they are plugged in |
| Industrial Environment Wireless Penetration Testing | AWUS036EACS / ACH / ACS | Measured injection 96–100%, end-to-end WPA handshake capture works; avoid AXM / AXML (injection fails) |
| Wi-Fi 6 + AP Hotspot | AWUS036AX / AXER | 2x2, 80MHz AP verified working |
| 6GHz Band | AWUS036AXML | Verified able to run a WPA3 AP on 6GHz; AXM uses the same chip but 6GHz was not tested |
| No External WiFi Required | — | EdgeXpert is built-in with Wi-Fi 7, general internet access does not require external WiFi |

## 5. Environmental Requirements

### 5.1 Hardware Requirements

| Item | Requirement |
|---|---|
| USB Adapter | USB-C to USB-A adapter or cable (except AXML), recommended to support USB 3.2 Gen 2×2 |
| Power Supply | MSI EdgeXpert OEM 240W USB-C power supply |

### 5.2 Software Requirements

| Item | Requirement |
|---|---|
| DGX OS Version | Any active version (kernel 6.x) |
| Kernel Version | Kernel 6.17 (tested on 6.17.0-1014-nvidia) includes drivers for all 9 cards, so no compilation tools are needed; the minimum version differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), and only kernels below that version need community DKMS drivers |
| Wireless Management Tools | iw, network-manager (pre-installed in DGX OS) |

## 6. Compatibility Determination

### ALFA Current Models × MSI EdgeXpert (GB10) Compatibility Matrix

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

Determination Criteria: Hands-on tests on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) from 2026-11-16 to 2026-11-18, using our own Wi-Fi network and our own phone as test targets. The MSI EdgeXpert uses the same GB10 chip and NVIDIA kernel series, so the same behavior is expected, but testing was done on the GX10 only; the MSI EdgeXpert itself has not been tested. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detailed Step by Step Setup Steps

The installation steps for MSI EdgeXpert are expected to be identical to those for NVIDIA DGX Spark (the steps were tested on the GX10). The following is a simplified version; for the complete steps, please refer to Section 7 of [Is ALFA Wireless Card Compatible with NVIDIA DGX Spark](/en/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek Chipset Models (AWUS036ACM / ACHM / AXM / AXML)

**Step 1: Insert the Network Card**

Use a USB-C to USB-A adapter (AXML can be plugged in directly) to insert the ALFA network card into the USB-C port of EdgeXpert.

**Step 2: Confirm USB Detection**

```bash
lsusb
# Expected output example (AWUS036ACM / MT7612U):
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Step 3: Confirm Network Interface**

```bash
ip link show
# An interface whose name starts with wlx should appear automatically (in-kernel driver loads automatically)
```

**Step 4: Connect to WiFi**

```bash
nmcli dev wifi connect "SSID" password "password"
```

### 7.2 Realtek Chipset Models (AWUS036ACH / ACS / EACS / AX / AXER)

Kernel 6.17 (the version tested on the GX10) already includes drivers for all Realtek models, so the steps are the same as for the MediaTek models and no compilation is needed (minimum versions: EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17):

```bash
# 1. Check the kernel version (6.17 or later has drivers for all Realtek models built in; the GX10 test ran 6.17.0-1014-nvidia)
uname -r

# 2. After inserting the network card, confirm the driver loaded automatically
lsusb
lsmod | grep -E "rtw88|rtw89"
ip link show

# 3. Connect to WiFi
nmcli dev wifi connect "SSID" password "password"
```

Modules loaded automatically for each model: ACH → `rtw88_8812au`, ACS → `rtw88_8821au`, EACS → `rtw88_8821cu`, AX / AXER → `rtw89_8852bu`. Only if `uname -r` reports a version below that card's minimum version (older systems) do you need a community-maintained DKMS driver (for example morrownr/8812au-20210820 for RTL8812AU).

### 7.3 Monitor Mode (Penetration Testing)

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

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not see ALFA network card | Poor USB-C adapter / Only charging specification | Replace with a USB 3.2 Gen 2×2 adapter that supports data transfer; try a different USB-C port |
| MediaTek chip has no wlan interface | Module not automatically loaded / Firmware missing | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; check `dmesg | grep mt76` |
| Realtek card shows no wlan interface after plugging in | Kernel below that card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), so the matching driver is not built in | Check the version with `uname -r`; upgrade the kernel, or install a community DKMS driver on the older kernel |
| No networks visible after repeatedly switching between monitor and AP | RX stall | Unplug and replug the card so USB re-enumerates it |
| EACS / AXML shows no wlx interface after replugging | Bluetooth + Wi-Fi composite device probe hangs | Replug into a different USB port |
| Slow WiFi speed | Adapter only supports USB 2.0 | Replace with a USB 3.2 Gen 2×2 adapter |
| Built-in Wi-Fi 7 and external interference | Routing conflict | Disable built-in WiFi with `sudo nmcli radio wifi off` before using the external one |
| Unstable under high temperature in industrial environments | Cooling / Industrial version differences | Confirm using the industrial version of EdgeXpert (MS-C931); ensure the environmental temperature is within the specification range |

## 9. Known Limitations

- USB Type-C Conversion Requirement: All ALFA network cards, except for AXML, require a USB-C to USB-A converter.
- MT7921 Models Fail Injection: AWUS036AXM / AXML fail packet injection on the stock 6.17 kernel, so deauth and handshake capture are not possible; monitor, AP and WPA3 work. The main cause is a mac80211 chanctx regression in kernel 6.16 and later, and the community-patched driver is still rate-limited.
- Test Scope: Tested only on the ASUS GX10 (kernel 6.17.0-1014-nvidia); the MSI EdgeXpert has not been tested individually, but the same behavior is expected.
- hcxdumptool Not Usable: All cards except the EACS on 2.4 GHz report `failed to arm`; use airodump-ng + aireplay-ng instead.
- Potential Conflict with Built-in Wi-Fi 7: EdgeXpert is built-in with Wi-Fi 7 + BT 5.4.
- AP Mode Requires Manual Configuration: DGX OS is set as a development environment by default.
- 6GHz Regulatory Limitations: Wi-Fi 6E availability depends on the regulatory region.
- Older Kernels: On systems with a kernel below a card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), the Realtek models need community DKMS drivers, which must be recompiled after every kernel update.
- Industrial Edition Differences Do Not Affect Compatibility: The hardware specifications of MSI industrial edition (MS-C931) are the same as the consumer edition, and USB WiFi compatibility is consistent.

Counter-conditions: If the official specifications page of MSI changes (USB port specifications adjustment, kernel version lower than 6.x), or if real-world testing finds that mt76x2u / mt7921u cannot be automatically loaded on DGX OS, the compatibility matrix in Section 6 of this document needs to be reviewed again; if the in-kernel driver behavior changes after an NVIDIA kernel update, the cards need to be re-tested.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| MSI EdgeXpert Official Store (US) | EdgeXpert Consumer Edition Specifications | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Verified | 2026-09-03 |
| MSI EdgeXpert Store (TW) | EdgeXpert Consumer Edition Specifications (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Verified | 2026-09-03 |
| MSI Industrial Computer Official Announcement | EdgeXpert Product Release Information | https://ipc.msi.com/en/news/146241 | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Spark Official Page | GB10 Platform Information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yopitek) | ALFA Current Product Specifications | /en/products/alfa/ | ✅ Verified | 2026-09-03 |
| ALFA 9-Card ARM64 Test Matrix (Yopitek) | Hands-on tests on ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Tested | 2026-11-18 |

Related Articles: [Is ALFA Wireless Card Compatible with NVIDIA DGX Spark](/en/blog/alfa-nvidia-dgx-spark-compatibility/) | [Is ALFA Wireless Card Compatible with ASUS Ascent GX10](/en/blog/alfa-asus-ascent-gx10-compatibility/) | [Is ALFA Wireless Card Compatible with ALTOS BrainSphere GB10 F1](/en/blog/alfa-altos-brainsphere-gb10-compatibility/) | [Is ALFA Wireless Card Compatible with GIGABYTE AI TOP ATOM](/en/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Is ALFA Wireless Card Compatible with NVIDIA Jetson Nano](/en/blog/alfa-nvidia-jetson-nano-compatibility/)

Disclaimer: The compatibility determination in this article is based on hands-on tests performed in November 2026 on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). The MSI EdgeXpert uses the same GB10 chip and NVIDIA kernel series as the GX10, so the same behavior is expected, but it has not been tested individually. The kernel 6.17 tested on the GX10 already includes drivers for all 9 ALFA network cards (the minimum version differs by card); community DKMS drivers are needed only when the kernel is below a card's minimum version. EdgeXpert is built-in with Wi-Fi 7, and ALFA is mainly used for penetration testing or special chipset requirements. Monitoring and injection must only be performed on networks you own or are authorized to test.
