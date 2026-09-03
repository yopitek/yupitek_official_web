---
title: "\"ALFA Wireless Card Compatibility with NVIDIA DGX Spark (GB10)\""
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
description: "DGX Spark runs on NVIDIA DGX OS with ALFA network card compatibility similar to modern Linux desktops; MediaTek models use in-kernel drivers, while Realtek models require out-of-tree compilation fo..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Problem Summary

Customer Inquiry: "Can the ALFA series USB wireless network card be used on the NVIDIA DGX Spark (GB10 Grace Blackwell) personal AI supercomputer?"

Short Conclusion: The DGX Spark runs NVIDIA DGX OS (based on Ubuntu, kernel 6.x), and its compatibility with the ALFA network card is the same as that of a general modern Linux desktop system. MediaTek chip models (AWUS036ACM / ACHM / AXML / AXM) use in-kernel drivers and are ready to use out of the box; Realtek chip models (AWUS036ACH / ACS / EACS / AX / AXER) require compiling out-of-tree drivers (ARM64 / aarch64 architecture). Note: All USB ports on the DGX Spark are USB Type-C, while the ALFA network cards are USB Type-A, so a USB-C to USB-A adapter or cable is required.

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

- Kernel 6.x (modern): All WiFi drivers that have entered the mainline can be used directly, including mt76 (MT7612U / MT7610U) and mt7921u (MT7921AUN). This contrasts sharply with the kernel 4.9 of Jetson Nano.
- ARM64 (aarch64) architecture: Realtek out-of-tree drivers (8812au / 8821cu / rtl8852bu) need to be compiled on ARM64. These drivers' upstream (morrownr) already supports ARM64 compilation, but it is necessary to confirm that CONFIG_PLATFORM_ARM64 = y is set in the Makefile.

### 2.4 USB Type-C Adapter Requirement

The 4 USB ports on the DGX Spark are all Type-C, while all ALFA network cards (except AXML for USB-C) are USB Type-A interface:

| Model | Interface Specification | Does it need an adapter |
|---|---|---|
| AWUS036AXML | USB-C / USB 3.2 | ❌ No adapter needed (can be inserted directly) |
| AWUS036AXM | USB Type-A / USB 3.2 | ✅ Needs USB-C to USB-A |
| AWUS
