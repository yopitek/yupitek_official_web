---
title: "\"Does ALFA Wireless Card Support MSI EdgeXpert (GB10)\""
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
description: "MSI EdgeXpert & NVIDIA DGX Spark share GB10 hardware & DGX OS, ALFA card compatibility identical; MediaTek models use in-kernel drivers, Realtek models need ARM64 out-of-tree drivers; note USB-C to..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on the MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) AI supercomputer?"

Short Conclusion: The MSI EdgeXpert shares the same GB10 hardware platform and DGX OS software environment as the NVIDIA DGX Spark, ensuring full compatibility with the ALFA network cards. MediaTek chip models (AWUS036ACM / ACHM / AXML / AXM) use in-kernel drivers and are ready to use out of the box; Realtek chip models (AWUS036ACH / ACS / EACS / AX / AXER) require compiling out-of-tree drivers on ARM64. Note: All four USB ports on the EdgeXpert are USB Type-C (20Gbps), and the ALFA network cards (except AXML) require a USB-C to USB-A adapter.

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
| Suite Management | apt |

### 2.3 Differences from DGX Spark

MSI EdgeXpert is an OEM version of the DGX Spark platform, with identical core hardware and software:

| Item | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Institutional Design | MSI Customized Chassis, Industrial Edition Options | NVIDIA Reference Chassis |
| Storage Options | 1TB / 4TB | Up to 4TB |
| Target Market | Edge AI / Industrial AI / Desktop Development | Desktop AI Development |
| Accessories | MSI Original Accessories | NVIDIA Original Accessories |

Impact on ALFA Compatibility: No impact. USB controllers, kernel versions, and driver frameworks are all identical to those of DGX Spark.

### 2.4 USB Type-C Conversion Requirements

All 4 USB ports on the EdgeXpert are Type-C, while ALFA's full series of network cards (except AXML for USB-C) are USB Type-A, requiring a converter. It is recommended to choose a converter that supports USB 3.2 Gen 2×2 (20Gbps).

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current USB wireless network card product line includes the following models (parent models: 9):

| Model | Wi-Fi Level | Chipset | Interface | Linux Driver Status |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Same as above |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recommended |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au coverage) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Applicable Models and Chipsets

### 4.1 Recommended Grade Classification

| Recommended Grade | Model (Chipset) | Description |
|---|---|---|
| ⭐ Highly Recommended | AWUS036ACM (MT7612U) | in-kernel driver, ready to use, AC1200 dual-band, supports AP / Monitor / Injection |
| ✅ Recommended | AWUS036ACHM (MT7610U) | in-kernel driver, low power consumption, AC433 dual-band |
| ✅ Recommended (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | in-kernel driver, Wi-Fi 6E, AXML is USB-C plug and play |
| ⚠️ Available but Requires Compilation | AWUS036ACH (RTL8812AU) | Requires compilation of morrownr/8812au (ARM64), complete after compilation |
| ⚠️ Available but Requires Compilation | AWUS036ACS / EACS | Requires compilation of corresponding out-of-tree driver |
| ⚠️ Available but Requires Attention | AWUS036AX / AXER (RTL8832BU) | The rtw89 in kernel 6.x may already support it; no need to compile if not required |

### 4.2 Usage Scenario Recommendations

| Usage Scenario | Recommended Model | Description |
|---|---|---|
| Edge AI Gateway Wireless Internet Access | AWUS036ACM / ACHM | in-kernel driver, stable, no maintenance required |
| Industrial Environment Wireless Penetration Testing | AWUS036ACH or AWUS036ACM | Both support Monitor + Injection |
| Wi-Fi 6E / 6GHz Band | AWUS036AXML / AXM | MT7921AUN in-kernel driver |
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
| Compilation Tools (required for Realtek chip) | build-essential, git, bc, dkms |
| Wireless Management Tools | iw, network-manager (pre-installed in DGX OS) |

## 6. Compatibility Determination

### ALFA Current Models × MSI EdgeXpert (GB10) Compatibility Matrix

| Model | Chipset | Driver Method | USB Detection | STA Internet | AP Mode | Monitor | Installation Difficulty | Overall Rating |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | No installation required | ⭐ Best |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limited | No installation required | ✅ Good |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limited | No installation required | ✅ Good |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limited | No installation required | ✅ Good |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Medium (translation) | ⚠️ Available |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Medium (translation) | ⚠️ Available |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Medium (translation) | ⚠️ Available |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Medium-High | ⚠️ Available |
| AWUS036AXER | RTL8832BU | Same as above | ✅ | ⚠️ | ⚠️ | ❌ | Medium-High | ⚠️ Available |

Determination Criteria: MSI EdgeXpert shares the same GB10 hardware platform and DGX OS (kernel 6.x, aarch64) with DGX Spark, and the compatibility determination is completely consistent with DGX Spark.

## 7. Detailed Step by Step Setup Steps

The installation steps for MSI EdgeXpert are identical to those for NVIDIA DGX Spark. The following is a simplified version; for the complete steps, please refer to Section 7 of [Is ALFA Wireless Card Compatible with NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek Chipset Models (Ready to Use)

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
# Should automatically appear as wlan0 (in-kernel driver automatically loaded)
```

**Step 4: Connect to WiFi**

```bash
nmcli dev wifi connect "SSID" password "password"
```

### 7.2 Realtek Chipset Models ( Requires Compilation)

Taking AWUS036ACH (RTL8812AU) as an example:

**Step 1: Install Compilation Tools**

```bash
sudo apt update && sudo apt install -y build-essential git bc dkms
```

**Step 2: Download and Compile the Driver**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Confirm CONFIG_PLATFORM_ARM64 = y in Makefile
make
sudo make install
sudo modprobe 8812au
```

**Step 3: Confirm Interface After Inserting the Network Card**

```bash
ip link show
```

**Step 4: Connect to WiFi**

```bash
nmcli dev wifi connect "SSID" password "password"
```

### 7.3 Monitor Mode (Penetration Testing)

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not see ALFA network card | Poor USB-C adapter / Only charging specification | Replace with a USB 3.2 Gen 2×2 adapter that supports data transfer; try a different USB-C port |
| MediaTek chip has no wlan interface | Module not automatically loaded / Firmware missing | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; check `dmesg | grep mt76` |
| Realtek driver compilation fails | Incorrect cross-compilation settings | Confirm native compilation on EdgeXpert; Makefile should not set CROSS_COMPILE |
| Slow WiFi speed | Adapter only supports USB 2.0 | Replace with a USB 3.2 Gen 2×2 adapter |
| Built-in Wi-Fi 7 and external interference | Router conflict | Disable built-in WiFi with `sudo nmcli radio wifi off` before using the external one |
| Unstable under high temperature in industrial environments | Cooling / Industrial version differences | Confirm using the industrial version of EdgeXpert (MS-C931); ensure the environmental temperature is within the specification range |

## 9. Known Limitations

- USB Type-C Conversion Requirement: All ALFA network cards, except for AXML, require a USB-C to USB-A converter.
- Realtek Chip Needs Manual Compilation: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU have not been integrated into the mainline.
- Potential Conflict with Built-in Wi-Fi 7: EdgeXpert is built-in with Wi-Fi 7 + BT 5.4.
- AP Mode Requires Manual Configuration: DGX OS is set as a development environment by default.
- 6GHz Regulatory Limitations: Wi-Fi 6E availability depends on the regulatory region.
- Driver Updates Depend on Upstream: Realtek out-of-tree drivers are maintained by the community, and need to be recompiled after kernel updates.
- Industrial Edition Differences Do Not Affect Compatibility: The hardware specifications of MSI industrial edition (MS-C931) are the same as the consumer edition, and USB WiFi compatibility is consistent.

Counter-conditions: If the official specifications page of MSI changes (USB port specifications adjustment, kernel version lower than 6.x), or if real-world testing finds that mt76x2u / mt7921u cannot be automatically loaded on DGX OS, the compatibility matrix in Section 6 of this document needs to be reviewed again; if the morrownr driver stops maintaining the ARM64 branch, the Realtek model determination needs to be reconsidered.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| MSI EdgeXpert Official Store (US) | EdgeXpert Consumer Edition Specifications | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Verified | 2026-09-03 |
| MSI EdgeXpert Store (TW) | EdgeXpert Consumer Edition Specifications (23STW) | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Verified | 2026-09-03 |
| MSI Industrial Computer Official Announcement | EdgeXpert Product Release Information | https://ipc.msi.com/en/news/146241 | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Spark Official Page | GB10 Platform Information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yupitek) | ALFA Current Product Specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |

Related Articles: [Is ALFA Wireless Card Compatible with NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Is ALFA Wireless Card Compatible with ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Is ALFA Wireless Card Compatible with ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Is ALFA Wireless Card Compatible with GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Is ALFA Wireless Card Compatible with NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Disclaimer: The compatibility determination in this article is based on the NVIDIA DGX OS pre-installed in MSI EdgeXpert (kernel 6.x, aarch64). EdgeXpert and DGX Spark share the same hardware platform, with complete compatibility. MediaTek chip drivers are for Linux mainline, with high stability; Realtek chip drivers are community-maintained. EdgeXpert is built-in with Wi-Fi 7, and ALFA is mainly used for penetration testing or special chip set requirements.
