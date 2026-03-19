---
title: "SDRLab TRX-duo — Dual-Channel 16-bit ZYNQ SDR Platform"
description: "SDRLab TRX-duo, dual-channel 16-bit ADC/DAC SDR platform, Xilinx Zynq 7010 SoC, Red Pitaya compatible, 10kHz–60MHz direct sampling — built for advanced HF radio research."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
---

## Features

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- Dual-channel transceiver design (2 RX + 2 TX), fully compatible with the Red Pitaya software ecosystem
- 2× LTC2208 high-precision 16-bit ADC delivers wide dynamic range and high sensitivity
- 14-bit DAC for dual-channel transmission
- On-board Xilinx Zynq 7010 SoC (dual-core ARM Cortex-A9 + FPGA) — run decoding software directly on the device
- Supports remote network deployment for building remote SDR receive stations
- Compatible with leading SDR software: HDSDR, SDR#, PowerSDR, SDR Console V3, and more
- Priced at roughly half the cost of the official Red Pitaya SDRlab 122-16 (approx. $622 USD)

## Specifications

| Specification | Value / Description |
|---------------|---------------------|
| Processor | Dual-core ARM Cortex-A9 (Zynq 7010 SoC) |
| FPGA | Xilinx Zynq 7010 |
| RAM | 512 MB |
| Receive Frequency Range | 10 kHz – 60 MHz (direct sampling) |
| Receive Channels | 2 (SMA connectors) |
| ADC Resolution | 16-bit (LTC2208) |
| ADC Sample Rate | 125 MS/s |
| ADC Full-Scale Voltage | 0.5 Vpp / −2 dBm |
| Input Voltage Range | DC max 50 V (AC-coupled), 1 Vpp RF |
| Input Protection | RF transformer + AC coupling |
| Transmit Channels | 2 |
| DAC Resolution | 14-bit |
| DAC Sample Rate | 125 MS/s |
| Transmit Output Voltage | 1 Vpp / +4 dBm |
| Transmit Load Impedance | 50 Ω |
| Transmit Power | ~2.5 mW (external power amplifier required) |
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | External Wi-Fi dongle required (not included) |
| Expansion GPIO | 16× digital I/O, 4× analog input, 4× analog output |
| Analog Input Voltage Range | 0–3.3 V |
| Analog Output Voltage Range | 0–1.8 V |
| Analog Input Sample Rate | 100 kS/s / 12-bit |
| Communication Interfaces | I2C, UART, SPI |
| Expansion Power Output | +3.3 V |
| Operating System | On-board Linux (Red Pitaya firmware) |

## Use Cases

- HF (shortwave) amateur radio transceiving (CW, SSB, AM, FM)
- Multi-band WSPR weak-signal monitoring (up to 8 bands simultaneously)
- Remote SDR receive station deployment (full network remote access)
- HF spectrum analysis and signal research
- HPSDR-compatible application development
- Amateur radio experimentation (contests, astronomical observation)

---

{{< alert >}}
Need a quote? [Contact us](/en/contact/)
{{< /alert >}}
