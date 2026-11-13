---
title: "OpenSourceSDRLab RTL-SDR Blog V4 — Entry-Level SDR Receiver"
seo_title: "RTL-SDR Blog V4 | SDRLab Taiwan | Yopitek"
description: "SDRLab RTL-SDR Blog V4 USB SDR receiver: 500 kHz–1.766 GHz, R828D tuner, built-in HF upconverter, 1 PPM TCXO, bias tee. Available in Taiwan from Yopitek."
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["SDR", "RTL-SDR", "Radio Reception", "USB", "GNU Radio"]
faq:
  - question: "Do I need direct sampling mode to receive HF on the RTL-SDR Blog V4?"
    answer: "No. According to RTL-SDR Blog, activating direct sampling mode on a V4 dongle yields no results. The built-in upconverter upconverts HF by 28.8 MHz, and the RTL-SDR Blog drivers handle the offset."
  - question: "Does the RTL-SDR Blog V4 need special drivers?"
    answer: "Yes. The V4 requires the RTL-SDR Blog drivers, which are backward compatible with V3 and older units. Without them the V4 will not function correctly."
  - question: "How does the bias tee on the RTL-SDR Blog V4 work?"
    answer: "The bias tee is software controlled and rated at 4.5 V, supplying up to 180 mA continuously. On Linux it is switched with rtl_biast, and it only works with the RTL-SDR Blog drivers."
  - question: "What frequency range does the RTL-SDR Blog V4 cover?"
    answer: "It covers 500 kHz to 1.766 GHz. HF is upconverted by 28.8 MHz, the TCXO provides 1 PPM frequency accuracy, and the RF connector is SMA."
---

The RTL-SDR Blog V4 is an entry-level USB software-defined radio receiver for hobbyists, amateur radio users and RF researchers. It covers 500 kHz–1.766 GHz with an R828D tuner, a built-in HF upconverter and a 1 PPM TCXO. Contact Yopitek for a quotation in Taiwan.

## Features

![RTL-SDR Blog RTL SDR V4](/images/products/sdrlab/rtl-sdr-v4.png)

- R828D tuner with three inputs; a triplexer splits the SMA input into HF, VHF and UHF bands for better out-of-band isolation
- Built-in HF upconverter: HF is upconverted by 28.8 MHz, so no direct sampling mode is needed (lowest tuning limit 500 kHz)
- 1 PPM Temperature-Compensated Crystal Oscillator (TCXO) for significantly improved frequency stability
- Software-controlled Bias-Tee powers external LNAs or active antennas
- Switchable notch filter for the broadcast AM, broadcast FM and DAB bands reduces strong-station interference
- Conductive black metal enclosure that shields and doubles as a heatsink, plus USB noise choking and improved ESD protection
- Bundled multipurpose dipole antenna kit — ready to use right out of the box

## Specifications

| Specification | Value / Description |
|---------------|---------------------|
| Tuner Chip | Rafael Micro R828D |
| ADC Chip | RTL2832U |
| Frequency Range | 500 kHz – 1.766 GHz (including HF mode) |
| Frequency Accuracy | 1 PPM TCXO |
| RF Connector | SMA |
| Bias-Tee | Software-enabled, max 4.5 V |
| HF Reception | Built-in upconverter (HF upconverted by 28.8 MHz; no direct sampling needed) |
| Enclosure | Conductive black metal enclosure (shield and heatsink) |
| Interface | USB (requires RTL-SDR Blog drivers) |
| OS Support | Windows, Linux, macOS, Android |
| Accessories | Dipole antenna kit (dipole base with 60 cm RG174 cable, 4× telescopic antennas (2× 23 cm–1 m, 2× 5–13 cm), 3 m RG174 extension cable, tripod, suction cup mount) |

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

[RTL-SDR Blog official V4 guide](https://www.rtl-sdr.com/v4/)

[Manufacturer store page (OpenSourceSDRLab)](https://opensourcesdrlab.com/products/rtl-sdr-v4)
