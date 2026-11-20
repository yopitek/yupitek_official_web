---
title: "ALFA Wireless Card Compatibility with ALTOS BrainSphere GB10 F1"
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
description: "9 ALFA USB Wi-Fi adapters on ALTOS BrainSphere GB10 F1: ASUS GX10 tests on kernel 6.17 show in-kernel drivers, no DKMS; EACS/ACH/ACS inject best, AXM/AXML fail."
featureimage: ""
author: "benny-lai"
lastmod: 2026-11-20
---

> 📌 Updated with November 2026 GX10 test results: on the ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia), all 9 current ALFA adapters use in-kernel drivers and work as soon as they are plugged in, with no DKMS needed. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/). Tested on the GX10 only; other GB10 models have not been tested individually.

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network cards be used on the ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell) AI workstation?"

Short Conclusion: The ALTOS BrainSphere GB10 F1 and the NVIDIA DGX Spark use the same GB10 chip and the same NVIDIA kernel series. We tested ALFA's 9 current USB network cards (AWUS036ACM / ACHM / ACH / ACS / EACS / AX / AXER / AXM / AXML) on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia): all of them use in-kernel drivers and work as soon as they are plugged in, with no compilation or DKMS required. The same behavior is expected, but testing was done on the GX10 only; the ALTOS BrainSphere GB10 F1 itself has not been tested. Functional differences: the MediaTek MT7921 models (AWUS036AXM / AXML) fail packet injection on the stock 6.17 kernel, while monitor, AP and WPA3 work; monitor mode and injection were verified working on the other 7 models. The minimum kernel version at which each driver entered mainline differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17); only older kernels below that version need community DKMS drivers. Note: The BrainSphere GB10 F1 has USB ports as 3 Type-C data ports + 1 Type-C PD input port, and the ALFA network cards (excluding AXML) require a USB-C to USB-A adapter.

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
| Package Management | apt |

### 2.3 Differences with DGX Spark

| Difference Item | BrainSphere GB10 F1 | NVIDIA DGX Spark |
|---|---|---|
| Included Software | Altos aiGeni AI Development Platform | NVIDIA Reference Software Stack |
| Mechanical Design | Altos / Acer customized chassis | NVIDIA Reference Chassis |
| Target Market | Enterprise AI / Research Institutions / Education | Desktop AI Development |
| Maximum Power Consumption | 170W | Approximately 240W (including power conversion) |

Impact on ALFA Compatibility: No impact expected (tested on the GX10 only; other GB10 models have not been tested individually). Altos aiGeni is an application layer software that does not affect the kernel driver framework. USB controllers, kernel versions, and driver architectures are all identical to those of DGX Spark.

### 2.4 USB Type-C Conversion Requirements

The BrainSphere GB10 F1 has 4 USB ports, all of which are Type-C (3 data + 1 PD input), while the ALFA full series network cards (except AXML for USB-C) are USB Type-A, requiring a converter.

## 3. Analysis of Current ALFA Network Card Specifications and Chipsets

As of September 2026, ALFA Network's current lineup of USB wireless network cards is as follows:

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
| Corporate AI Lab Wireless Internet | Any of the 9 models (e.g. AWUS036ACM / ACHM) | All use in-kernel drivers and work as soon as they are plugged in |
| Wireless Penetration Testing / Security Research | AWUS036EACS / ACH / ACS | Measured injection 96–100%, end-to-end WPA handshake capture works; avoid AXM / AXML (injection fails) |
| Wi-Fi 6 + AP Hotspot | AWUS036AX / AXER | 2x2, 80MHz AP verified working |
| 6GHz Band | AWUS036AXML | Verified able to run a WPA3 AP on 6GHz; AXM uses the same chip but 6GHz was not tested |
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
| Kernel Version | Kernel 6.17 (tested on 6.17.0-1014-nvidia) includes drivers for all 9 cards, so no compilation tools are needed; the minimum version differs by card (ACM/ACHM 4.19, AXM/AXML 5.18, EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), and only kernels below that version need community DKMS drivers |
| Wireless Management Tools | iw, network-manager (pre-installed in DGX OS) |
| aiGeni Notes | If using aiGeni's container environment, ensure that the USB device is correctly mounted to the container (usually recommended to set up at the host OS level for general internet access) |

## 6. Compatibility Determination

### ALFA Current Models × ALTOS BrainSphere GB10 F1 Compatibility Matrix

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

Determination Criteria: Hands-on tests on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia) from 2026-11-16 to 2026-11-18, using our own Wi-Fi network and our own phone as test targets. The ALTOS BrainSphere GB10 F1 uses the same GB10 chip and NVIDIA kernel series, so the same behavior is expected, but testing was done on the GX10 only; the ALTOS BrainSphere GB10 F1 itself has not been tested. Full data: [ALFA 9-Card ARM64 Test Matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## 7. Detailed Step by Step Setup Steps

The installation steps for the ALTOS BrainSphere GB10 F1 are expected to be identical to those for NVIDIA DGX Spark (the steps were tested on the GX10). The following is a simplified version; for the complete steps, please refer to Section 7 of [Does ALFA Wireless Network Card Support NVIDIA DGX Spark](/en/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 MediaTek Chip Models (AWUS036ACM / ACHM / AXM / AXML)

- Use a USB-C to USB-A adapter (AXML can be directly inserted) to insert the ALFA network card into the BrainSphere's USB-C port
- Confirm detection: `lsusb`
- Confirm interface: `ip link show` (an interface whose name starts with wlx should appear automatically)
- Connect to WiFi: `nmcli dev wifi connect "SSID" password "password"`

### 7.2 Realtek Chip Models (AWUS036ACH / ACS / EACS / AX / AXER)

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

### 7.4 Using WiFi in aiGeni Container (Advanced)

If you need to use the ALFA network card in the Altos aiGeni Docker container:

1. First confirm on the host OS (DGX OS) that the driver loaded automatically, and connect to WiFi there
2. When starting the container, add `--network=host` or mount the corresponding network interface
3. It is recommended to complete general internet usage on the host OS level, with the container using `--network=bridge` to share the network

## 8. Common Errors and Troubleshooting

| Symptom | Possible Cause | Resolution |
|---|---|---|
| lsusb does not see ALFA network card | Poor USB-C adapter / Only charging specification | Replace with a USB 3.2 Gen 2×2 adapter that supports data transfer; try a different USB-C port |
| MediaTek chip has no wlan interface | Module not automatically loaded / Firmware missing | `sudo modprobe mt76x2u`; `sudo apt install linux-firmware`; check `dmesg | grep mt76` |
| Realtek card shows no wlan interface after plugging in | Kernel below that card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), so the matching driver is not built in | Check the version with `uname -r`; upgrade the kernel, or install a community DKMS driver on the older kernel |
| No networks visible after repeatedly switching between monitor and AP | RX stall | Unplug and replug the card so USB re-enumerates it |
| EACS / AXML shows no wlx interface after replugging | Bluetooth + Wi-Fi composite device probe hangs | Replug into a different USB port |
| WiFi speed is slow | Adapter only supports USB 2.0 | Replace with a USB 3.2 Gen 2×2 adapter |
| Built-in Wi-Fi 7 and external interference | Routing conflict | `sudo nmcli radio wifi off` to disable built-in WiFi before using the external one |
| WiFi is not visible in aiGeni container | Container network mode issue | Use `--network=host`; or allow the container to share the network after connecting to the host OS |
| 6GHz cannot be used | Regulatory Domain restriction | `sudo iw reg set US`; confirm the latest regulations |

## 9. Known Limitations

- USB Type-C Conversion Requirement: All ALFA network cards, except for AXML, require a USB-C to USB-A adapter.
- MT7921 Models Fail Injection: AWUS036AXM / AXML fail packet injection on the stock 6.17 kernel, so deauth and handshake capture are not possible; monitor, AP and WPA3 work. The main cause is a mac80211 chanctx regression in kernel 6.16 and later, and the community-patched driver is still rate-limited.
- Test Scope: Tested only on the ASUS GX10 (kernel 6.17.0-1014-nvidia); the ALTOS BrainSphere GB10 F1 has not been tested individually, but the same behavior is expected.
- hcxdumptool Not Usable: All cards except the EACS on 2.4 GHz report `failed to arm`; use airodump-ng + aireplay-ng instead.
- Potential Conflict with Built-in Wi-Fi 7: BrainSphere is built with Wi-Fi 7 + BT 5.4.
- AP Mode Requires Manual Configuration: DGX OS is set as a development environment by default.
- 6GHz Regulatory Limitations: Wi-Fi 6E availability depends on the regulatory region.
- Older Kernels: On systems with a kernel below a card's minimum version (EACS 6.2, ACH/ACS 6.13, AX/AXER 6.17), the Realtek models need community DKMS drivers, which must be recompiled after every kernel update.
- aiGeni Container Isolation: If using WiFi within an aiGeni container, pay attention to network namespace and device mounting; it is recommended to manage WiFi at the host OS level.
- Altos Software Differences Do Not Affect Compatibility: aiGeni is an application layer platform and does not affect the compatibility of kernel USB WiFi drivers.

Countercondition: The above judgments are based on DGX OS (Ubuntu-based, kernel 6.x). If Altos switches to a non-Ubuntu-based self-developed OS in the future, or if the DGX OS kernel major version changes, the in-kernel driver determination needs to be re-tested.

## 10. Reference URLs

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| ALTOS BrainSphere GB10 F1 Official Product Sheet (PDF) | Hardware specifications (170W / 50mm / USB configuration) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Verified | 2026-09-03 |
| Altos Computing Official Website | BrainSphere GB10 F1 Product Information | https://www.altoscomputing.com/en-Us | ✅ Verified | 2026-09-03 |
| NVIDIA DGX Spark Official Page | GB10 Platform Information | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Verified | 2026-09-03 |
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| ALFA Network Product Overview (Yopitek) | ALFA Current Product Specifications | /en/products/alfa/ | ✅ Verified | 2026-09-03 |
| ALFA 9-Card ARM64 Test Matrix (Yopitek) | Hands-on tests on ASUS GX10 + Ubuntu 24.04 ARM64 | https://yupitek.com/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/ | ✅ Tested | 2026-11-18 |

Related Articles: [Does ALFA Wireless Network Card Support NVIDIA DGX Spark](/en/blog/alfa-nvidia-dgx-spark-compatibility/) | [Does ALFA Wireless Network Card Support ASUS Ascent GX10](/en/blog/alfa-asus-ascent-gx10-compatibility/) | [Does ALFA Wireless Network Card Support GIGABYTE AI TOP ATOM](/en/blog/alfa-gigabyte-ai-top-atom-compatibility/) | [Does ALFA Wireless Network Card Support MSI EdgeXpert](/en/blog/alfa-msi-edgexpert-compatibility/)

Disclaimer: The compatibility determination in this article is based on hands-on tests performed in November 2026 on an ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17.0-1014-nvidia). The ALTOS BrainSphere GB10 F1 uses the same GB10 chip and NVIDIA kernel series as the GX10, so the same behavior is expected, but it has not been tested individually. Altos aiGeni is an application layer software that does not affect driver compatibility. The kernel 6.17 tested on the GX10 already includes drivers for all 9 ALFA network cards (the minimum version differs by card); community DKMS drivers are needed only when the kernel is below a card's minimum version. BrainSphere is built-in with Wi-Fi 7, and ALFA is mainly used for penetration testing or special chipset requirements. Monitoring and injection must only be performed on networks you own or are authorized to test.
