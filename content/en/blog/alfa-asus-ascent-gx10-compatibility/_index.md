---
title: "\"ALFA Wireless Card Compatibility with ASUS Ascent GX10 (GB10)\""
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Hardware Guide"
description: "ASUS GX10 shares hardware and software with NVIDIA DGX Spark, compatible with ALFA USB network cards; MediaTek models use in-kernel drivers, Realtek models require ARM64 out-of-tree drivers, all wi..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on the ASUS Ascent GX10 (NVIDIA GB10 Grace Blackwell) AI supercomputer?"

Short Conclusion: The ASUS Ascent GX10 shares the same GB10 hardware platform and DGX OS software environment as the NVIDIA DGX Spark, ensuring full compatibility with the ALFA network cards (judgment basis: ALFA's current 9 models of USB network cards). MediaTek chip models (AWUS036ACM / ACHM / AXML / AXM, 4 models) use in-kernel drivers and are ready to use out of the box; Realtek chip models (AWUS036ACH / ACS / EACS / AX / AXER, 5 models) require compiling out-of-tree drivers on ARM64. Note: All USB ports on the GX10 are USB Type-C (3 data ports + 1 PD input port), and the ALFA network cards (except for AXML) require a USB-C to USB-A adapter.

## 2. Analysis of Target Hardware Specification Architecture

### 2.1 ASUS Ascent GX10 Hardware Specifications

| Item | Specification |
|---|---|
| Product Name | ASUS Ascent GX10 |
| Core Chip | NVIDIA GB10 Grace Blackwell Superchip (DGX Spark Platform) |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell Architecture, 6144 CUDA Cores, 5th Generation Tensor Core, 4th Generation RT Core |
| AI Performance | Up to 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| System Memory | 128GB LPDDR5x Unified Memory (256-bit, 273 GB/s) |
| Storage | Up to 4TB NVMe M.2 SSD (Self-encrypting) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode / DisplayPort 2.1) + 1× USB 3.2 Gen 2×2 Type-C (PD Input, 180W EPR PD3.1) |
| Display Output | 1× HDMI 2.1 (Can be paired with USB-C DP Alt Mode for multi-display output) |
| Wired Network | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (2× 200G QSFP112) |
| Wireless Network | Wi-Fi 7 (MediaTek AW-EM637, 2×2 MIMO) + Bluetooth 5.4 |
| Operating System | NVIDIA DGX OS (Based on Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 51 mm (5.91 × 5.91 × 2.01 inch) |
| Weight | 1.48 kg |
| Cooling | ASUS Proprietary Cooling System (Silent Fan + Heat Pipe) |
| Other | Kensington Lock Slot |

> ⚠️ Specification Note: The original draft wrote "150 × 150 × 50 mm" and did not include weight. After verification, ASUS official techspec is **150 × 150 × 51 mm / 1.48 kg**, which has been corrected. The HDMI version is 2.1 (the original draft wrote 2.1b and has been corrected). See Section 10 for reference sources.

### 2.2 Software Environment: NVIDIA DGX OS

| Item | Content |
|---|---|
| Basic OS | Ubuntu Linux (NVIDIA Customized) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Pre-installed Software | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Package Management | apt |

### 2.3 Differences with DGX Spark

| Difference Item | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| Cooling Design | ASUS Proprietary Cooling System | NVIDIA Reference Cooling |
| Chassis Design | ASUS Customized Chassis | NVIDIA Reference Chassis |
| Wireless Module | MediaTek AW-EM637 (Wi-Fi 7) |同级 Wi-Fi 7 Module |
| Accessories | ASUS OEM Accessories | NVIDIA OEM Accessories |
| Warranty | ASUS Warranty | NVIDIA Warranty |

Impact on ALFA Compatibility: No impact. USB controllers, kernel versions, and driver frameworks are all identical to DGX Spark.

### 2.4 USB Type-C Conversion Requirements

The GX10 has 4 USB ports, all of which are Type-C:

- 3 Data Ports (Support DP Alt Mode, can connect to screens)
- 1 PD Input Port (Used for power supply)

ALFA's full series of network cards (except AXML for USB-C) are USB Type-A and require a converter.

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, the current ALFA Network USB wireless network card product line is as follows:

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
| ✅ Recommended (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | in-kernel driver, Wi-Fi 6E, AXML is USB-C plug-and-play |
| ⚠️ Available but Requires Compilation | AWUS036ACH (RTL8812AU) | Requires compilation of morrownr/8812au (ARM64), complete after compilation |
| ⚠️ Available but Requires Compilation | AWUS036ACS / EACS | Requires compilation of corresponding out-of-tree driver |
| ⚠️ Available but Requires Attention | AWUS036AX / AXER (RTL8832BU) | The rtw89 in kernel 6.x may already support it; no need to compile if not required |

### 4.2 Usage Scenario Recommendations

| Usage Scenario | Recommended Model | Description |
|---|---|---|
| General Wireless Internet (simplest) | AWUS036ACM / ACHM | in-kernel driver, no compilation required |
| Wireless Penetration Testing / Monitoring / Injection | AWUS036ACH or AWUS036ACM | Both support Monitor + Injection |
| Wi-Fi 6E / 6GHz | AWUS036AXML / AXM | MT7921AUN in-kernel driver |
| No External WiFi Required | — | GX10 is built-in with Wi-Fi 7, general internet access does not require external WiFi |

## 5. Environmental Requirements

### 5.1 Hardware Requirements

| Item | Requirement |
|---|---|
| USB Adapter | USB-C to USB-A adapter or cable (except AXML), recommended to support USB 3.2 Gen 2×2 |
| Power Supply | ASUS GX10 OEM USB-C power supply (180W EPR PD3.1) |

### 5.2 Software Requirements

| Item | Requirement |
|---|---|
| DGX OS Version | Any active version (kernel 6.x) |
| Compilation Tools (required for Realtek chip) | build-essential, git, bc, dkms |
| Wireless Management Tools | iw, network-manager (pre-installed in DGX OS) |

## 6. Compatibility Determination

### ALFA Current Models × ASUS Ascent GX10 (GB10) Compatibility Matrix

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

Determination Criteria: The ASUS GX10 and DGX Spark share the same GB10 hardware platform and DGX OS (kernel 6.x, aarch64), and the compatibility determination is identical to that of DGX Spark.

## 7. Detailed Step by Step Setup Steps

The installation steps for the ASUS GX10 are identical to those for NVIDIA DGX Spark. The following is a simplified version; for the complete steps, please refer to Section 7 of [Does ALFA Wireless Network Card Support NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek Chip Model (Ready to Use)

- Use a USB-C to USB-A adapter (AXML can be directly inserted) to insert the ALFA network card into the USB-C port of the GX10
- Confirm detection: `lsusb`
- Confirm interface: `ip link show` (wlan0 should appear automatically)
- Connect to WiFi: `nmcli dev wifi connect "SSID" password "password"`

### 7.2 Realtek Chip Model (Compilation Required)

Example using AWUS036ACH (RTL8812AU):

```bash
# 1. Install compilation tools
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Download and compile the driver
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Confirm CONFIG_PLATFORM_ARM64 = y in Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Confirm interface after inserting the network card
ip link show

# 4. Connect to WiFi
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
| Realtek driver compilation fails | Cross-compilation settings error | Confirm native compilation on GX10; Makefile should not set CROSS_COMPILE |
| WiFi speed is slow | Adapter only supports USB 2.0 | Replace with a USB 3.2 Gen 2×2 adapter |
| Built-in Wi-Fi 7 and external interference | Routing conflict | Use `sudo nmcli radio wifi off` to disable built-in WiFi before using the external one |
| 6GHz cannot be used | Regulatory Domain restriction | `sudo iw reg set US`; confirm the latest regulations |

## 9. Known Limitations

- USB Type-C Conversion Requirement: All ALFA network cards, except for AXML, require a USB-C to USB-A converter.
- Realtek Chip Needs Manual Compilation: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU have not been integrated into the mainline.
- Built-in Wi-Fi 7 May Conflict with External Devices: GX10 is built-in with Wi-Fi 7 (MediaTek AW-EM637).
- AP Mode Requires Manual Configuration: DGX OS is set as a development environment by default.
- 6GHz Regulatory Limitations: Wi-Fi 6E availability depends on the regulatory region.
- Driver Updates Depend on Upstream: Realtek out-of-tree drivers are maintained by the community, and recompilation is required after kernel updates.
- ASUS Hardware Differences Do Not Affect Compatibility: Differences in cooling and mechanical design do not affect USB WiFi driver compatibility.

Countercondition: The above judgments are based on the DGX OS (Ubuntu-based, kernel 6.x). If ASUS releases non-DGX OS firmware (such as its own Android or customized system versions) in the future, the judgments need to be revalidated.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| ASUS Ascent GX10 Official Techspec | GX10 Hardware Specifications (**150×150×51mm / 1.48kg** / USB Configuration / HDMI 2.1) | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ Verified | 2026-09-03 |
| ASUS Ascent GX10 Official Store (UK) | GX10 Product Page (150 × 150 × 51mm) | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Spark Official Page | GB10 Platform Information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide (Yupitek) | ALFA Linux AP Mode Guide | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yupitek) | ALFA Current Product Specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |

Related Articles: [Is ALFA Wireless Card Compatible with NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Is ALFA Wireless Card Compatible with ALTOS BrainSphere GB10 F1](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Is ALFA Wireless Card Compatible with GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Is ALFA Wireless Card Compatible with MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Disclaimer: The compatibility determination in this article is based on the NVIDIA DGX OS pre-installed on the ASUS Ascent GX10 (kernel 6.x, aarch64). The GX10 and DGX Spark share the same hardware platform, with complete compatibility. MediaTek chip drivers are for Linux mainline, with high stability; Realtek chip drivers are community-maintained. The GX10 is built-in with Wi-Fi 7, and ALFA is mainly used for penetration testing or special chip set requirements.
