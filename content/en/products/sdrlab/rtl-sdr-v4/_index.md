---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Entry-Level SDR Receiver"
description: "RTL-SDR Blog RTL SDR V4, 500kHz–1.7GHz wideband SDR receiver, 1PPM TCXO, built-in HF upconverter, USB 2.0 — the go-to choice for getting started in RF research."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Do I need direct sampling mode to receive HF on the RTL-SDR Blog V4?"
    answer: "No. The V4 has a built-in upconverter instead of a direct sampling circuit, so HF signals are upconverted by 28.8 MHz and the driver handles the frequency shift. Enabling direct sampling on a V4 gives no results."
  - question: "Does the RTL-SDR Blog V4 need special drivers?"
    answer: "Yes. The V4 requires the RTL-SDR Blog drivers, which are backward compatible with V3 and older units. The default Osmocom branch now also supports the V4."
  - question: "How does the bias tee on the RTL-SDR Blog V4 work?"
    answer: "The bias tee is software controlled and rated at 4.5 V, supplying up to 180 mA continuously. On Linux it is switched with rtl_biast. Do not enable it with a DC-shorted antenna unless an LNA or powered device is in the chain."
---

## Features

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- Upgraded R828D tuner delivers lower noise and better sensitivity compared to the previous R820T/R860
- Built-in upconverter enables HF reception down to 500 kHz (standard RTL-SDR dongles bottom out at 24 MHz)
- 1 PPM Temperature-Compensated Crystal Oscillator (TCXO) for significantly improved frequency stability
- Software-controlled Bias-Tee powers external LNAs or active antennas
- Triple-notch frontend filter effectively suppresses broadcast FM/AM/DAB interference
- Redesigned low-noise PCB with enhanced ESD protection and passive-cooling aluminum enclosure
- Bundled multipurpose dipole antenna kit — ready to use right out of the box

## Specifications

| Specification | Value / Description |
|---------------|---------------------|
| Tuner Chip | Rafael Micro R828D |
| ADC Chip | RTL2832U |
| Frequency Range | 500 kHz – 1.7 GHz (including HF mode) |
| Maximum Bandwidth | 3.2 MHz (stable at 2.4 MHz) |
| ADC Resolution | 8-bit |
| Frequency Accuracy | 1 PPM TCXO |
| RF Connector | SMA Female (F) |
| Bias-Tee | Software-enabled, max 4.5 V |
| HF Reception | Built-in upconverter with 28.8 MHz low-pass filter |
| Enclosure | Aluminum alloy, passive cooling |
| Interface | USB 2.0 (requires RTL-SDR Blog driver) |
| OS Support | Windows, Linux, macOS, Android |
| Accessories | Dipole antenna kit (2× telescopic antennas, 3 m extension cable, tripod, suction cup mount) |

## Use Cases

- ADS-B aircraft tracking
- Maritime AIS vessel monitoring
- NOAA / Meteor M2 weather satellite image reception
- Amateur radio (HF/VHF/UHF receive)
- Radio astronomy (hydrogen line observation)
- P25 and MotoTRBO digital voice decoding
- APRS and ACARS packet tracking
- DAB digital radio reception
- RF spectrum monitoring and security research

---

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}

{{< faq >}}

[Setup guides and technical details — doc.yupitek.com](https://doc.yupitek.com/sdrlab/hardware/rtl-sdr-v4/)
