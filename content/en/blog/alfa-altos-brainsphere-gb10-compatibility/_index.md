---
title: "\"ALFA Wireless Card Compatibility with ALTOS BrainSphere GB10 F1\""
date: 2026-09-03
draft: false
slug: "alfa-altos-brainsphere-gb10-compatibility"
tags:
  - "ALFA"
  - "Altos"
  - "BrainSphere-GB10"
  - "NVIDIA-GB10"
  - "AWUS036ACM"
  - "ARM64"
  - "DGX-OS"
categories:
  - "Hardware Guide"
description: "ALTOS GB10 F1 shares hardware and software with NVIDIA DGX Spark, compatible with ALFA USB network cards, with MediaTek models plug-and-play and Realtek models requiring ARM64 drivers."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on the ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell) AI workstation?"

Short Conclusion: The ALTOS BrainSphere GB10 F1 shares the same GB10 hardware platform and DGX OS software environment as the NVIDIA DGX Spark, ensuring complete compatibility with the ALFA network cards (judgment basis: ALFA's current 9 models of USB network cards). MediaTek chip models (AWUS036ACM / ACHM / AXML / AXM, 4 models) use in-kernel drivers and are ready to use out of the box; Realtek chip models (AWUS036ACH / ACS / EACS / AX / AXER, 5 models) require compiling out-of-tree drivers on ARM64. Note: The BrainSphere GB10 F1 has USB ports as 3 Type-C data ports + 1 Type-C PD input port, and the ALFA network cards (excluding AXML) require a USB-C to USB-A adapter.

## 2. Analysis of Target Hardware Specification Architecture

### 2.1 ALTOS BrainSphere GB10 F1 Hardware Specifications

| Item | Specification |
|---|---|
| Product Name | ALTOS BrainSphere GB10 F1 (Acer / Altos Computing) |
| Core Chip | NVIDIA GB10 Grace Blackwell Superchip (DGX Spark Platform) |
| CPU | 20-core Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | NVIDIA Blackwell Architecture, 6144 CUDA Cores, 5th Generation Tensor Core, 4th Generation RT Core |
| AI Performance | Up to 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, supports up to 20 billion parameter models |
| System Memory | 128GB LPDDR5x Unified Memory (256-bit, 273 GB/s) |
| Storage | 4TB NVMe M.2 SSD (Self-encrypting) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode) + 1× USB 3.2 Gen 2×2 Type-C (PD Input, 180W EPR PD3.1) |
| Display Output | 1× HDMI 2.1a |
| Wired Network | 1× 10GbE RJ45 + NVIDIA ConnectX-7 NIC (200G × 2 QSFP) |
| Wireless Network | Wi-Fi 7 + Bluetooth 5.4 with LE |
| Operating System | NVIDIA DGX OS (Based on Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 50 mm (1.13L) |
| Weight | < 1.5 kg |
| Maximum Power Consumption | 170W |
| Included Software | Altos aiGeni (One-click AI development platform, supports TensorFlow / PyTorch / Jupyter / Ollama) |

> Specification Verification: The above dimensions / weight / power consumption / USB configuration are consistent with the Altos official Product Sheet PDF (see Section 10 Reference Sources).

### 2.2 Software Environment: NVIDIA DGX OS + Altos aiGeni

| Item | Content |
|---|---|
| Basic OS | Ubuntu Linux (NVIDIA customized, DGX OS) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| AI Platform | Altos aiGeni (One-click environment deployment, automatic backup, real-time monitoring, intelligent tools) |
| Pre-installed Frameworks | TensorFlow, PyTorch, Jupyter, Ollama |
| Suite Management | apt |

### 2.3 Differences with DGX Spark

| Difference Item | BrainSphere GB10 F1 | NVIDIA DGX Spark |
|---|---|---|
| Included Software | Altos aiGeni AI Development Platform | NVIDIA Reference Software Stack |
| Institutional Design | Altos / Acer customized chassis | NVIDIA Reference Chassis |
| Target Market | Enterprise AI / Research Institutions / Education | Desktop AI Development |
| Maximum Power Consumption | 170W | Approximately 240W (including power conversion) |

Impact on ALFA Compatibility: No impact. Altos aiGeni is an application layer software that does not affect the kernel driver framework. USB controllers, kernel versions, and driver architectures are all identical to those of DGX Spark.

### 2.4 USB Type-C Conversion Requirements

The BrainSphere GB10 F1 has 4 USB ports, all of which are Type-C (3 data + 1 PD input), while the ALFA full series network cards (except AXML for USB-C) are USB Type-A, requiring a converter.

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current lineup of USB wireless network cards is as follows:

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
| ⚠️ Available but requires translation | AWUS036ACH (RTL8812AU) | Requires translation of morrownr/8812au (ARM64), complete after translation |
| ⚠️ Available but requires translation | AWUS036ACS / EACS | Requires translation of corresponding out-of-tree driver |
| ⚠️ Available but requires attention | AWUS036AX / AXER (RTL8832BU) | The rtw89 in kernel 6.x may already support it; no need to translate if not required |

### 4.2 Usage Scenario Recommendations

| Usage Scenario | Recommended Model | Description |
|---|---|---|
| Corporate AI Lab Wireless Internet | AWUS036ACM / ACHM | in-kernel driver, stable, no maintenance required, suitable for corporate environments |
| Wireless Penetration Testing / Security Research | AWUS036ACH or AWUS036ACM | Both support Monitor + Injection |
| Wi-Fi 6E / 6GHz Band | AWUS036AXML / AXM | MT7921AUN in-kernel driver |
| No need for external WiFi | — | BrainSphere is built-in with Wi-Fi 7, general internet access does not require external WiFi |

## 5. Environmental Requirements

### 5.1 Hardware Requirements

| Item | Requirement |
|---|---|
| USB Adapter | USB-C to USB-A adapter or cable (except AXML), recommended to support USB 3.2 Gen 2×2 |
| Power Supply | ALTOS OEM USB-C power supply (180W EPR PD3.1) |

### 5.2 Software Requirements

| Item | Requirement |
|---|---|
| DGX OS Version | Any active version (kernel 6.x) |
| Compilation Tools (required for Realtek chip) | build-essential, git, bc, dkms |
| Wireless Management Tools | iw, network-manager (pre-installed in DGX OS) |
| aiGeni Notes | If using aiGeni's container environment, ensure that the USB device is correctly mounted to the container (usually recommended to set up at the host OS level for general internet access) |

## 6. Compatibility Determination

### ALFA Current Models × ALTOS BrainSphere GB10 F1 Compatibility Matrix

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

Determination Criteria: The ALTOS BrainSphere GB10 F1 shares the same GB10 hardware platform and DGX OS (kernel 6.x, aarch64) with DGX Spark, and the compatibility determination is completely consistent with DGX Spark. Altos aiGeni is an application layer software that does not affect driver compatibility.

## 7. Detailed Step by Step Setup Steps

The installation steps for the ALTOS BrainSphere GB10 F1 are identical to those for NVIDIA DGX Spark. The following is a simplified version; for the complete steps, please refer to Section 7 of [Does ALFA Wireless Network Card Support NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek Chip Model (Ready to Use)

- Use a USB-C to USB-A adapter (AXML can be directly inserted) to insert the ALFA network card into the BrainSphere's USB-C port
- Confirm detection: `lsusb`
- Confirm interface: `ip link show` (wlan0 should appear automatically)
- Connect to WiFi: `nmcli dev wifi connect "SSID" password "password"`

### 7.2 Realtek Chip Model (Compilation Required)

Taking AWUS036ACH (RTL8812AU) as an example:

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

### 7.4 Using WiFi in aiGeni Container (Advanced)

If you need to use the ALFA network card in the Altos aiGeni Docker container:

1. First complete the driver installation and WiFi connection on the host OS (DGX OS)
2. When starting the container, add `--network=host` or mount the corresponding network interface
3. It is recommended to complete general internet usage on the host OS level, with the container using `--network=bridge` to share the network

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not see ALFA network card | Poor USB-C adapter / Only charging specification | Replace with a USB 3.2 Gen 2×2 adapter that supports data transfer; try a different USB-C port |
| MediaTek chip has no wlan interface | Module not automatically loaded / Firmware missing | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; check `dmesg | grep mt76` |
| Realtek driver compilation fails | Cross-compilation settings error | Confirm native compilation on BrainSphere; Makefile should not set CROSS_COMPILE |
| WiFi speed is slow | Adapter only supports USB 2.0 | Replace with a USB 3.2 Gen 2×2 adapter |
| Built-in Wi-Fi 7 and external interference | Routing conflict | `sudo nmcli radio wifi off` to disable built-in WiFi before using the external one |
| WiFi is not visible in aiGeni container | Container network mode issue | Use `--network=host`; or allow the container to share the network after connecting to the host OS |
| 6GHz cannot be used | Regulatory Domain restriction | `sudo iw reg set US`; confirm the latest regulations |

## 9. Known Limitations

- USB Type-C Conversion Requirement: All ALFA network cards, except for AXML, require a USB-C to USB-A adapter.
- Realtek Chip Requires Manual Compilation: RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU have not been integrated into the mainline.
- Potential Conflict with Built-in Wi-Fi 7: BrainSphere is built with Wi-Fi 7 + BT 5.4.
- AP Mode Requires Manual Configuration: DGX OS is set as a development environment by default.
- 6GHz Regulatory Limitations: Wi-Fi 6E availability depends on the regulatory region.
- Driver Updates Depend on Upstream: Realtek out-of-tree drivers are maintained by the community, and recompilation is required after kernel updates.
- aiGeni Container Isolation: If using WiFi within an aiGeni container, pay attention to network namespace and device mounting; it is recommended to manage WiFi at the host OS level.
- Altos Software Differences Do Not Affect Compatibility: aiGeni is an application layer platform and does not affect the compatibility of kernel USB WiFi drivers.

Countercondition: The above judgments are based on DGX OS (Ubuntu-based, kernel 6.x). If Altos switches to a non-Ubuntu-based self-developed OS in the future, or if the DGX OS kernel major version changes, the in-kernel/out-of-tree judgments need to be revalidated.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| ALTOS BrainSphere GB10 F1 Official Product Sheet (PDF) | Hardware specifications (170W / 50mm / USB configuration) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verified | 2026-09-03 |
| Altos Computing Official Website | BrainSphere GB10 F1 Product Information | https://www.altoscomputing.com/en-Us | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Spark Official Page | GB10 Platform Information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yupitek) | ALFA Current Product Specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |

Related Articles: [Does ALFA Wireless Network Card Support NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Does ALFA Wireless Network Card Support ASUS Ascent GX10](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Does ALFA Wireless Network Card Support GIGABYTE AI TOP ATOM](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Does ALFA Wireless Network Card Support MSI EdgeXpert](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Disclaimer: The compatibility determination in this article is based on the NVIDIA DGX OS (kernel 6.x, aarch64) pre-installed on the ALTOS BrainSphere GB10 F1. BrainSphere and DGX Spark share the same hardware platform, with complete consistency in compatibility. Altos aiGeni is an application layer software that does not affect driver compatibility. MediaTek chip drivers are for Linux mainline, with high stability; Realtek chip drivers are community maintained. BrainSphere is built-in with Wi-Fi 7, and ALFA is mainly used for penetration testing or special chip set requirements.
