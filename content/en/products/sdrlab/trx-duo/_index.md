---
title: "SDRLab TRX-duo — Dual-Channel 16-bit ZYNQ SDR Platform"
seo_title: "TRX-duo | SDRLab Taiwan | Yopitek"
description: "SDRLab TRX-duo dual-channel 16-bit ADC/DAC SDR platform with Xilinx Zynq 7010 SoC, 125 MS/s, Red Pitaya compatible. Available in Taiwan from Yopitek."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "TRX-duo", "ZYNQ", "Red Pitaya", "16-bit ADC"]
faq:
  - question: "What processor and interfaces does the SDRLab TRX-duo have?"
    answer: "It uses a Xilinx Zynq 7010 SoC with a dual-core ARM Cortex-A9, 512 MB RAM, 1 Gbit Ethernet and USB Type-C (USB 2.0). Wi-Fi requires an external dongle, which is not included."
  - question: "What are the receive and transmit specifications of the TRX-duo?"
    answer: "Receive uses 2 × LTC2208 16-bit ADCs at 125 MS/s with 0.5 Vpp / −2 dBm full scale. Transmit uses 2 channels of 14-bit DAC at 125 MS/s, 1 Vpp / +4 dBm into 50 Ω."
  - question: "Which software is the TRX-duo compatible with?"
    answer: "It is compatible with the Red Pitaya software ecosystem and with SDR software such as HDSDR, SDR#, PowerSDR and SDR Console V3."
  - question: "What expansion I/O does the TRX-duo provide?"
    answer: "It provides 16 digital I/O, 4 analog inputs (0–3.3 V, 100 kS/s, 12-bit) and 4 analog outputs (0–1.8 V), with I2C, UART and SPI plus a +3.3 V supply output."
---

The SDRLab TRX-duo is a dual-channel 16-bit SDR transceiver platform built on a Xilinx Zynq 7010 SoC and compatible with the Red Pitaya software ecosystem, for advanced radio research and amateur radio. It has 2 × LTC2208 16-bit ADCs at 125 MS/s and two 14-bit DAC transmit channels. Contact Yopitek for a quotation in Taiwan.

## Features

![SDRLab TRX-duo](/images/products/sdrlab/trx-duo.png)

- Dual-channel transceiver design (2 RX + 2 TX), fully compatible with the Red Pitaya software ecosystem
- 2× LTC2208 high-precision 16-bit ADC delivers wide dynamic range and high sensitivity
- 14-bit DAC for dual-channel transmission
- On-board Xilinx Zynq 7010 SoC (dual-core ARM Cortex-A9 + FPGA) — run decoding software directly on the device
- Supports remote network deployment for building remote SDR receive stations
- Compatible with leading SDR software: HDSDR, SDR#, PowerSDR, SDR Console V3, and more

## Specifications

| Specification | Value / Description |
|---------------|---------------------|
| Processor | Dual-core ARM Cortex-A9 (Zynq 7010 SoC) |
| FPGA | Xilinx Zynq 7010 |
| RAM | 512 MB |
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
| Ethernet | 1 Gbit |
| USB | Type-C (USB 2.0) |
| Wi-Fi | External Wi-Fi dongle required (not included) |
| Expansion GPIO | 16× digital I/O, 4× analog input, 4× analog output |
| Analog Input Voltage Range | 0–3.3 V |
| Analog Output Voltage Range | 0–1.8 V |
| Analog Input Sample Rate | 100 kS/s / 12-bit |
| Communication Interfaces | I2C, UART, SPI |
| Expansion Power Output | +3.3 V |

## Use Cases

- HF (shortwave) amateur radio transceiving (CW, SSB, AM, FM)
- Remote SDR receive station deployment (full network remote access)
- HF spectrum analysis and signal research
- Amateur radio experimentation (contests, astronomical observation)

---

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}

[Manufacturer store page (OpenSourceSDRLab)](https://opensourcesdrlab.com/products/trx-duo-compatible-with-red-pitaya-sdr-dual-16bit-adc-zynq7010?VariantsId=10980)

{{< faq >}}
