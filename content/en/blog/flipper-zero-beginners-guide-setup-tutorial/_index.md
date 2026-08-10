---
title: "Flipper Zero Beginner’s Guide: Unboxing, Setup, Firmware Updates, and 5 Key Features"
locale: en
hreflang_group: flipper-zero-beginners-guide-setup-tutorial
slug: flipper-zero-beginners-guide-setup-tutorial
published: 2026-08-10
author: Yupitek
category: Technical
tags:
  - Flipper Zero
  - Tutorial
hero_image: /static/img/flipper-zero/hero.webp
hero_alt: "Flipper Zero Beginner’s Guide: Unboxing, Firmware Updates, and 5 Key Features Tested | Yupitek"
seo_description: "What is Flipper Zero? From unboxing, microSD setup, and qFlipper firmware updates to hands-on tests of RFID, Sub-GHz, NFC, IR, and BadUSB, this guide helps you get started with Flipper Zero."
---

# Flipper Zero Beginner’s Guide: Unboxing, Setup, Firmware Updates, and 5 Key Features

> TL;DR: Flipper Zero is a pocket-sized hardware exploration tool featuring 125 kHz RFID, Sub-GHz, NFC, Infrared, and BLE. It connects via USB-C to emulate a keyboard (BadUSB). After unboxing, install a microSD card, update the firmware using qFlipper or the mobile app, and start exploring with RFID reading and IR remote control. Always use these features only on **devices you own or have explicit authorization to test**.

## What is Flipper Zero? Who Is It For?

Flipper Zero is a palm-sized, multi-functional portable device positioned as a "hardware exploration tool." It is not a typical consumer gadget but a device designed for cybersecurity researchers, penetration testing beginners, Makers, and IoT engineers to read, analyze, and emulate common wireless protocols and digital signals.

Core hardware features include:

- **125 kHz RFID**: Read and emulate low-frequency access cards.
- **Sub-GHz Wireless** (CC1101 Chipset): Analyze signals from remotes, garage doors, and IoT sensors in the 300–928 MHz range.
- **NFC (13.56 MHz)**: Read, write, and emulate high-frequency cards.
- **Infrared (IR)**: Learn and retransmit IR codes for TVs, air conditioners, and more.
- **BLE**: Pair and control via the mobile app.
- **USB-C**: Connect to a computer for firmware updates and keyboard emulation (BadUSB / DuckyScript).
- **GPIO / iButton**: 1-Wire contact keys and hardware expansion.

**Ideal for:** Students preparing for wireless security research, engineers verifying the reliability of their own access control systems or sensors, and Makers interested in RFID/NFC principles. If you are simply looking for a "remote copier," its Sub-GHz capabilities can achieve this, but please verify local laws and usage scenarios first.

## Unboxing and Initial Setup: Install microSD Before Powering On

Flipper Zero ships without a microSD card, but using one for firmware and data storage is **highly recommended**. Follow these steps:

1. **Prepare the microSD Card**: Use a card of 4 GB or larger, formatted as FAT32 (FAT16/FAT32/exFAT are supported). Insert the card into the slot at the bottom of the device with the **chip side facing up**.
2. **Charge**: Connect the device to a charger or computer via USB-C and fully charge it before first use.
3. **Power On**: Press and hold the Back button on the rear of the device for about 3 seconds. The dolphin animation indicates successful boot.
4. **Check System Version**: Navigate to `Settings → About` to record the current firmware version before proceeding with updates.

> Note: Flipper Zero defaults to an English interface. While some third-party firmwares offer Chinese language support, **new users are advised against** installing third-party firmware initially. Familiarize yourself with the official firmware workflow first.

## Firmware Updates: qFlipper Desktop and Mobile App

Updating the firmware is the most critical step in getting started with Flipper Zero. The manufacturer continuously fixes bugs and adds protocol support; older firmware versions may fail to read certain cards or signals.

### Method 1: qFlipper Desktop (Recommended)

1. Download qFlipper for your platform (Windows / macOS / Linux) from the official Flipper website.
2. Connect Flipper Zero to your computer via USB-C and launch qFlipper.
3. Click the wrench icon (Advanced controls) in the top-right corner and select "Firmware update channel."
4. Select **Release (Stable)** and click Update.
5. Wait for the update to complete (approximately 5–10 minutes). The device will restart automatically.

### Method 2: Mobile App

1. Install the official Flipper Mobile App (iOS / Android).
2. Enable Bluetooth on your phone and pair it with Flipper Zero (on the device: `Settings → Bluetooth`).
3. Tap Update within the app to transfer the firmware via BLE, which takes approximately 10 minutes.

### How to Choose a Firmware Channel?

| Channel | Stability | Target Audience |
|---|---|---|
| Release (Stable) | High | **New users should always choose this** |
| Release Candidate (RC) | Medium | Users wanting to test new features early |
| Development | Low | Developers and testers |

> ⚠️ Do not disconnect the cable or lose power during the update process. If the device gets stuck on the boot screen, you can enter recovery mode to reflash (press Reset twice quickly). While third-party firmwares (e.g., Xtreme) offer extended features, they may be unstable. New users should stick to the official stable version.

## Hands-On Test: 5 Key Features

### 1. 125 kHz RFID: Read and Emulate Low-Frequency Cards

Older access cards (125 kHz) typically contain only an ID code without encryption. Flipper Zero has an LF antenna at the bottom; simply bring the card close to read it:

1. Main Menu → `125 kHz RFID` → `Read`.
2. Place the card flat against the bottom of the device. Upon successful reading, the UID and data will be displayed.
3. To emulate, select `Emulate` after reading. The device can now act as a temporary replacement card.

### 2. Sub-GHz: Analyze 300–928 MHz Wireless Signals

The built-in CC1101 transceiver can capture signals from remotes, garage doors, and IoT sensors:

1. Main Menu → `Sub-GHz` → `Read Raw`.
2. Press a button on the remote. The screen will display the frequency and signal waveform.
3. Save the signal and select `Replay` to retransmit. You can also manually set frequencies to scan the environment for wireless activity.

### 3. NFC: Read, Write, and Emulate 13.56 MHz Cards

The NFC module supports common 13.56 MHz standards. It can read the UID and data blocks of contactless cards like transit cards (full emulation depends on the card's encryption mechanism):

1. Main Menu → `NFC` → `Read`.
2. Place the card on the back of the device to read its information.
3. Depending on the card type, select `Emulate` or `Write`.

### 4. IR: Learn and Retransmit Infrared Codes

The built-in IR transmitter/receiver can learn codes from TVs, air conditioners, and projectors and retransmit them:

1. Main Menu → `Infrared` → `Learn`.
2. Point the remote at the IR window on top of the device and press a button. Once learned, name and save the code.
3. You can retransmit the code anytime via `Infrared → Saved`.

### 5. BadUSB / DuckyScript: USB-C Keyboard Emulation

When connected to a computer, Flipper Zero can emulate a USB keyboard to execute DuckyScript scripts (automated keystrokes):

1. Place your `.txt` script (written in DuckyScript syntax) in the `badusb/` folder on the microSD card.
2. Connect Flipper Zero to the target computer via USB-C. In the Main Menu, go to `BadUSB` and select the script to run.

> ⚠️ **BadUSB is a highly sensitive feature**: Scripts execute commands on the computer via keyboard input, effectively acting as "someone typing at the computer." Use this only on your own computer or in environments with explicit authorization for testing.

## Legal Usage Reminder (Mandatory Reading)

Flipper Zero itself is a legal tool, but its usage scenarios have clear legal boundaries:

- **Copying/Emulating Access Cards and Remotes**: Only do this for systems you own or have administrator authorization for. Unauthorized reading or emulation of others' access cards or garage remotes may involve legal liabilities under criminal law (privacy violations), telecommunications laws, or data protection regulations.
- **BadUSB**: Executing scripts on others' computers without authorization is illegal.
- **Signal Interference**: Intentionally interfering with others' wireless devices (e.g., garage doors) carries legal risks.

**The principle is simple: Only test devices you own or have written authorization to test.**

## Frequently Asked Questions (FAQ)

**Q1: Do I need to install a microSD card in Flipper Zero?**
It is not mandatory, but highly recommended. Most apps, signal libraries, and BadUSB scripts are stored on the microSD card. Without it, functionality is significantly limited.

**Q2: Will updating the firmware brick the device?**
The risk with official stable firmware is extremely low. As long as the update process is not interrupted by power loss or cable disconnection, failures are rare. In case of anomalies, you can reflash using recovery mode.

**Q3: Can I copy a transit card (e.g., EasyCard)?**
Most modern transit cards have encryption and key protection. Flipper Zero can only read the UID or unencrypted blocks and cannot fully copy the card. Additionally, unauthorized copying of transit cards is illegal.

**Q4: What is the difference between Flipper Zero and an SDR (Software Defined Radio)?**
Flipper Zero's built-in Sub-GHz transceiver focuses on common protocols (OOK/ASK/FSK, etc.) with intuitive operation. SDRs (like HackRF, RTL-SDR) offer a wider frequency range and raw spectrum analysis but require a computer and deeper technical background. They are complementary tools.

**Q5: Where can I buy Flipper Zero?**
Yupitek provides Flipper Zero products and related accessories, along with technical consultation. For setup questions after purchase, please email sales@yupitek.com.

**Q6: Can I install third-party firmware?**
Yes, but it is not recommended for beginners. Third-party firmwares (e.g., Xtreme) offer interface customization and extra features, but stability and security must be evaluated independently, and you may lose official update support.

## Summary

The path to getting started with Flipper Zero is straightforward: **Install microSD → Update to official stable firmware → Start with RFID reading and IR remote control → Explore Sub-GHz and BadUSB once familiar.** It is an excellent starting point for understanding wireless protocols and hardware security. However, remember: the more powerful the tool, the greater the need for self-discipline—only test devices you have permission to access.

For Flipper Zero or related accessories, please contact [sales@yupitek.com](mailto:sales@yupitek.com). Yupitek provides product and technical consultation services.