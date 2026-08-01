---
title: "Sierra Wireless Firmware Update & Brand Lock Switching Guide: The Safe Way to Flash Without Bricking"
locale: "en"
hreflang_group: "sierra-firmware-update-brand-lock-guide"
description: "Complete guide to updating firmware and switching OEM brand locks on Sierra Wireless modules (EM7455, EM7565, MC7455): FOTA and USB flashing workflows, AT+GMR version checks, firmware backups, SED brick recovery, and the correct steps to avoid a failed flash."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "sierra-firmware-update-brand-lock-guide"
tags: ["Sierra Wireless", "firmware-update", "qmi-firmware-update", "EM7455", "EM7565", "MC7455", "brand-lock", "SED", "flashing"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/en/products/sierra/"
faq:
  - question: "Will flashing a Sierra Wireless module always brick it?"
    answer: "No. The official specification documents the SED (Smart Error Detection) mechanism: after 6 consecutive failed reboots the module enters boot-and-hold mode and waits for a firmware download. That is the official recovery path. Most bricking happens from losing power mid-flash or writing an incompatible firmware."
  - question: "Can the brand lock (Dell / Lenovo / Generic) be switched?"
    answer: "This is a community-proven approach: flashing a different firmware image changes the module's identity so it matches the laptop's BIOS whitelist. Before you try it, confirm your module model and have the correct image ready."
  - question: "What do I do if the flash fails and the module keeps rebooting?"
    answer: "Let the module reboot until it reaches boot-and-hold mode (after 6 consecutive reboots), reconnect it over USB, and use a flashing tool to write the correct firmware image."
---

# Sierra Wireless Firmware Update & Brand Lock Switching Guide: The Safe Way to Flash Without Bricking

**The short version: you can update Sierra module firmware over the air (FOTA, pushed by the carrier) or by flashing it yourself over USB. The brand lock everyone worries about (the difference between Dell or Lenovo editions and the generic one) is actually just a firmware image swap. Check the version with `AT+GMR` before you flash, never cut power mid-flash, and if it does fail, the module ships with a built-in SED recovery mode that can bring it back.**

Plenty of people buy Sierra Wireless modules on the secondhand market, slot them into their laptop or router, and find the card won't work. The culprit is usually the OEM brand lock. This guide combines the hard facts from the official specification with what the community has learned the hard way, so you can flash your module safely.

> Technical sources: Sierra Wireless official specifications (EM7455, EM7565, MC7455). Brand lock switching and third-party tools are based on community practice. Compiled by Yupitek.

---

## The Key Concepts in 30 Seconds

Flashing is not dangerous. What is dangerous is skipping backups, grabbing the wrong file, and unplugging power mid-flash.

| What you need to know | Documented in the spec? | In plain terms |
|---|---|---|
| **FOTA (over-the-air update)** | ✅ Yes | The carrier pushes the update to you directly, but only if the carrier supports it. |
| **USB flashing (vendor tools)** | ✅ Yes | Connect the module to a PC over USB and write the firmware yourself. The most controlled approach. |
| **Check firmware version (AT+GMR)** | ✅ Yes | This AT command shows the current firmware version. Do it before every flash! |
| **Brand lock (Dell/Lenovo)** | ⚠️ Not directly | The spec only mentions "OEM label support". The actual locking mechanism is a whitelist implemented by the laptop makers. |
| **qmi-firmware-update** | ⚠️ Not documented | The go-to flashing tool in the Linux open source community. |

---

## What Is the Brand Lock (OEM Lock) Anyway?

When Dell or Lenovo buy modules from Sierra Wireless, they ask for the module to carry their logo and a dedicated firmware image, and they bake a "whitelist" into the laptop BIOS.

If your module is the Dell edition and you plug it into a Lenovo laptop, the machine may hang or throw an error at boot.
If your module is the Generic edition and the laptop enforces a strict whitelist, you are out of luck too.

**That is why people want to "switch the brand lock"**: in practice this means downloading the firmware image for the right brand (or the generic version) and forcing it onto the module over USB, so the module presents itself as the other edition.

> ⚠️ **Note**: flashing the wrong brand's firmware carries real risk. Find out exactly which version your motherboard wants before you touch anything.

---

## Before You Flash: Three Steps That Keep You Away from a Brick

Do not rush to flash the moment you have a file. Follow the spec and take care of these three things first:

### 1. Check the Current Firmware Version
Open a terminal (minicom or PuTTY work well), connect to the module's AT port, and type:
```text
AT+GMR
```
Screenshot the version string that comes back. If a flash goes wrong, this tells you which version to flash back.

### 2. Back Up Your Settings
The spec does not cover backups, but in practice you should write down your current APN settings and PRI parameters before touching anything.

### 3. Understand "Safe Shutdown"
Cutting power directly is the cardinal sin, both after a flash and before pulling the module. The spec explicitly warns that sudden power loss can damage the module's file system.
- **EM7455 / EM7565**: pull the `Full_Card_Power_Off#` pin low, wait about 20 to 25 seconds, then remove power.
- **MC7455**: issue `AT!PCOFFEN=0` first, then pull `W_DISABLE_N` low, wait tens of seconds, then unplug.

---

## Flashing in Practice: The USB Workflow

If you use `qmi-firmware-update`, the community favorite on Linux, the flow looks roughly like this (always defer to the tool's official documentation):

1. **Get the right file**: obtain the firmware package for your exact model from the vendor or the official site. EM7455 and EM7565 use completely different chips, so never mix their images!
2. **Plug in the module**: confirm the device shows up in `lsusb`.
3. **Stop interfering services**: shut down `ModemManager` and similar network services so they do not grab the USB port.
4. **Run the flashing tool**: feed it the file and start the flash.
5. **Hands off the keyboard**: during the flash the module is in an unstable state. **Never cut power or unplug the cable!** This is where most people brick their module.
6. **Reboot and verify**: after the flash, shut down safely, power back up, and run `AT+GMR` to confirm the version changed.

---

## What If It Is Already a Brick? (The SED Recovery Mechanism)

If the module keeps rebooting in a loop after a flash and never reaches the system, do not throw it in the bin just yet.

Sierra modules carry a built-in lifeline called **SED (Smart Error Detection)**.
The spec is explicit: **if the module crashes and reboots 6 times in a row at boot, it gives up and enters "boot-and-hold" mode.** That mode is the door left open for you to reinstall the firmware.

**Recovery steps:**
1. Let it keep rebooting. After the 6th cycle it will settle and hold (boot-and-hold mode).
2. Reconnect the USB cable.
3. Open your flashing tool, pick a known-good firmware package, and flash again.
4. In most cases that brings the module back to life.

> If USB will not connect at all, try triggering a hardware reset (RESET#). The timing differs per module: about 3 to 5.5 seconds on the EM7455, and 0.2 to 2.5 seconds on the EM7565. Wait too long and the cycle restarts, so you will need to time it.

---

## Conclusion

Flashing a Sierra Wireless module or switching its brand lock is a lot like flashing a phone: **there is a standard procedure and a recovery mechanism, so as long as you do not improvise, you will be fine.**

The big pitfalls are really just:
1. Grabbing the firmware for the wrong model.
2. Kicking the power cable mid-flash.
3. Forgetting to shut the module down safely.

Check the version (`AT+GMR`) before you start, have the correct image ready, and give the module a steady power supply. You will be able to give your WWAN card a new lease on life with confidence.

## Where to Buy (Call To Action)

Not sure whether your module is the Dell or the Lenovo edition? Looking for a reliable Sierra module to upgrade your device? Yupitek offers complete hardware solutions and technical consultation.
Email us: **sales@yupitek.com**
Browse the lineup: [Sierra Wireless Modules](https://yupitek.com/en/products/sierra/)
