---
title: "ACS ACR122U — USB NFC Reader"
description: "ACS ACR122U, USB NFC reader supporting ISO 14443 A/B, MIFARE, and FeliCa at 13.56 MHz. Ideal for NFC research and application development."
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
brands: ["acr"]
tags: ["NFC", "RFID", "ISO 14443", "MIFARE", "USB", "Card Reader"]
faq:
  - question: "Do I need to install an ACS driver for the ACR122U on Windows?"
    answer: "No. ACS states that the ACR122U is PC/SC compliant and uses the standard Microsoft CCID driver, so no ACS driver is required on Windows because the driver is already built into the operating system."
  - question: "Which cards and tags can the ACR122U read and write?"
    answer: "According to ACS, it accesses ISO 14443-4 Type A and Type B cards, MIFARE, FeliCa and all four types of NFC (ISO/IEC 18092) tags, with a card reading distance of up to 50 mm depending on the tag type. Its built-in anti-collision means only one tag is accessed at a time."
  - question: "How do I program the ACR122U in my own application?"
    answer: "The ACR122U supports PC/SC, and CT-API through a wrapper on top of PC/SC. Commands for ISO 18092 tags and for the LED and buzzer are sent as pseudo-APDUs. ACS also lists support for Android 3.1 and above."
---

ACR122U

## Product Overview

The ACR122U is a PC-linked contactless smart card reader/writer based on 13.56 MHz RFID technology. Compliant with the ISO/IEC 18092 NFC standard, it supports MIFARE®, ISO 14443 Type A/B, and all four NFC tag types. It is a PC/SC and CCID compliant plug-and-play USB device with access speed up to 424 Kbps and USB Full Speed (12 Mbps) interface. Operating distance is up to 50 mm.

## Key Specifications

| Specification | Details |
|---------------|---------|
| Operating Frequency | 13.56 MHz |
| Operating Distance | Up to 50 mm (depending on tag type) |
| Read/Write Speed | 106 Kbps / 212 Kbps / 424 Kbps |
| USB Interface | USB Full Speed (12 Mbps) |
| Supply Voltage | 5V DC regulated |
| Supply Current | 200 mA max / 100 mA normal / 50 mA standby |
| Antenna Size | 50 mm × 40 mm |
| Dimensions | 98 × 65 × 12.8 mm |
| Weight | 70 g |
| Operating Temperature | 0°C – 60°C |
| Humidity | Max. 90% (non-condensing) |
| MTBF | 408,500 hrs |
| LED | 1 bi-color Red/Green (user-controllable) |
| Buzzer | Monotone (user-controllable) |
| SAM Slot | 1 × ISO 7816-3 (optional) |
| Compliance | PC/SC, CCID, CE, FCC, RoHS |

## Key Features

- USB Full Speed Interface
- CCID and PC/SC compliant, plug-and-play
- Read/write speed up to 424 Kbps
- Built-in antenna, card reading distance up to 50 mm
- Supports all 4 NFC tag types (ISO/IEC 18092)
- Supports MIFARE Ultralight C, MIFARE Plus, DESFire EV1
- Reader/writer for ISO 14443 Type A/B, MIFARE, FeliCa and NFC tags
- Built-in anti-collision (1 tag at a time)
- User-controllable bi-color LED and buzzer
- Optional ISO 7816-3 SAM slot for enhanced security
- Available in module form for POS/access control integration
- Supports PC/SC and CT-API

## Supported Tag Types

| Tag / Card Type | Standard |
|-----------------|----------|
| NFC Tag Type 1 | ISO 14443 Type A |
| NFC Tag Type 2 | ISO 14443 Type A |
| NFC Tag Type 3 | FeliCa |
| NFC Tag Type 4 | ISO 14443 Type A and B |
| MIFARE Classic (1K, 4K, MINI) | ISO 14443 Type A |
| MIFARE Ultralight / Ultralight C | ISO 14443 Type A |
| MIFARE Plus | ISO 14443 Type A |
| MIFARE DESFire / DESFire EV1 | ISO 14443 Type A |
| FeliCa | ISO 18092 |
| ISO 14443 Type A cards | ISO 14443 |
| ISO 14443 Type B cards | ISO 14443 |

## Supported Operating Systems

- Windows CE 5.0, Windows Embedded Compact 6.0 / 7
- Windows XP, Vista, 7, 8, 8.1, 10
- Windows Server 2003 / 2008 / 2012 / 2016
- Linux®
- macOS®
- Solaris
- Android™ 3.1 and later


## 📄 Product Datasheet

| Resource | Link |
|----------|------|
| 📄 ACR122U Datasheet (PDF) | [Download PDF](/docs/acr/ACR122U_spec.pdf) |

{{< gallery >}}
  <img src="/images/products/acr/acr122u.webp" alt="ACS ACR122U NFC Reader" />
{{< /gallery >}}

---

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}

{{< faq >}}

[Setup guides and technical details — doc.yupitek.com](https://doc.yupitek.com/acs/products/acr122u/)
