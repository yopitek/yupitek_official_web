---
title: "AWUS036AXML Monitor Mode Firmware Fix: Resolve Active Mode Crashes"
description: "How to fix AWUS036AXML monitor mode firmware crashes on Kali Linux. Covers MT7921AUN firmware update, kernel version requirements, active vs passive mode workaround, and hcxdumptool alternative."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AUN", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
featureimage: "/images/blog/awus036axml-firmware-monitor-mode-fix.webp"
---

The **ALFA AWUS036AXML** is ALFA Network's flagship WiFi 6E adapter, built on the MediaTek MT7921AUN chipset. It brings tri-band support (2.4 / 5 / 6 GHz) to security researchers and is one of the only USB adapters capable of passive monitoring on the 6 GHz band in 2026. For many use cases — site surveys, PCAP capture, PMKID collection — it performs exceptionally well.

But there is a known issue that catches users off guard: **active monitor mode commands crash the firmware**. Running tools like `aireplay-ng` or `mdk4` causes the `wlan0mon` interface to disappear entirely, forcing you to unplug and replug the adapter to recover. This is not a hardware defect — it is a driver and firmware limitation in the current Linux `mt7921u` stack.

This guide explains the root cause, walks through the diagnostic steps, and provides concrete fixes and workarounds so you can keep working without losing the session. Whether you are a pentester mid-engagement or a researcher setting up a new lab, this will get you unstuck.

---

## The Problem: Active Monitor Mode Crashes

### Symptom

After enabling monitor mode and running an active command such as `aireplay-ng --test wlan0mon` or any deauthentication/injection operation, the `wlan0mon` interface vanishes from `ip link` and `iwconfig` output. The adapter becomes unresponsive and cannot be recovered without physically disconnecting and reconnecting it. In some cases `dmesg` shows a firmware error or reset event immediately after the crash.

Passive operations — scanning with `airodump-ng`, capturing raw frames — continue to work correctly before and after the crash, as long as no active injection is triggered.

### Root Cause

The **MT7921AUN chipset** uses a firmware-based MAC architecture. The `mt7921u` Linux kernel driver relies on the chipset's embedded firmware to handle certain lower-layer operations, including frame injection in monitor mode. The current firmware and driver combination does not fully implement the command path required for active injection in monitor mode on Linux.

In contrast, **passive monitoring** (sniffing frames already in the air) does not require the firmware to transmit anything and works without triggering the crash. The issue is specific to transmit-path operations: deauthentication frames, probe requests, association floods, and similar active operations.

{{< alert "triangle-exclamation" >}}
**Known firmware crash bug.** This is a confirmed issue in the Linux `mt7921u` driver as of early 2026. It affects AWUS036AXML and other MT7921AUN-based USB adapters. It may be resolved in future kernel or firmware updates — check the [driver install guide](/en/blog/install-alfa-driver-kali-ubuntu/) for the latest status.
{{< /alert >}}

---

## Diagnostic: Is This Your Problem?

Run through this sequence to confirm you are hitting the MT7921AUN active mode crash rather than a different issue:

```bash
# Check adapter is recognized
lsusb | grep -i mediatek

# Check driver loaded
lsmod | grep mt7921u

# Check kernel version (must be >= 5.18)
uname -r

# Start monitor mode
sudo airmon-ng start wlan0

# Test passive capture (should work fine)
sudo airodump-ng wlan0mon

# Test active injection (may crash)
sudo aireplay-ng --test wlan0mon
```

If the adapter disappears from `ip link` after `aireplay-ng --test`, you have confirmed the firmware crash bug.

Additional verification via kernel logs:

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

Look for messages like `mt7921u: firmware crash`, `mt7921u: chip reset`, or `usb disconnect` immediately following the aireplay-ng call. Those confirm the firmware-level failure.

{{< alert "circle-info" >}}
**Passive capture is unaffected.** If `airodump-ng` works but `aireplay-ng` crashes, this is exactly the known MT7921AUN bug. Proceed to the fixes below.
{{< /alert >}}

---

## Fix 1: Update Firmware Package

The most impactful first step is ensuring you have the latest MT7921 firmware files. Older firmware versions are more prone to the crash; updated firmware improves stability for some active operations.

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# Or manually install latest mt7921 firmware from linux-firmware repo
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

After updating firmware files, reload the driver and re-test active mode:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

Some combinations of firmware version and kernel version show significantly improved stability with active commands. Even if the crash is not fully resolved, updated firmware reduces the frequency of failures and may allow limited active operations to complete successfully.

---

## Fix 2: Use Latest Kernel

The `mt7921u` driver is actively maintained in the upstream Linux kernel. Driver-level patches for stability, firmware command handling, and monitor mode have been included in kernel updates since 5.18. Running a newer kernel is one of the most reliable ways to improve behavior.

Check your current kernel version:

```bash
uname -r
```

Update to the latest available kernel on Kali Linux:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

After rebooting, confirm the new kernel version:

```bash
uname -r
```

Target: **kernel 6.1 LTS or newer** for the most complete `mt7921u` driver patches. Kernel 6.6 and later includes additional improvements to the MediaTek PCIe/USB driver stack that have shown positive results in user reports. As of 2026, Kali Linux ships a 6.x kernel by default, so a standard `full-upgrade` typically gets you to a sufficiently modern version without manual kernel installation.

{{< alert "circle-info" >}}
**Kernel 6.6+ improvement.** Several community reports indicate that kernel 6.6 with updated firmware reduces (but does not always eliminate) active mode crashes on MT7921AUN. After upgrading, re-run the diagnostic sequence to assess your specific combination.
{{< /alert >}}

---

## Workaround: Use hcxdumptool (Passive PMKID Capture)

If firmware-level fixes do not fully resolve the crash for your engagement, `hcxdumptool` provides a highly effective alternative workflow that does not require any frame injection at all.

`hcxdumptool` operates in **passive mode** — it captures PMKID values directly from beacon and probe frames broadcast by access points. No deauthentication frames are sent, no injection occurs, and no firmware crash is triggered. The AWUS036AXML handles this workflow perfectly.

```bash
sudo apt install hcxdumptool hcxtools

# Passive capture — no deauth, no firmware crash
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Convert to hashcat format
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Crack with hashcat
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

This workflow captures PMKIDs from beacon frames without transmitting anything — completely passive from the wireless medium's perspective. For PMKID-based WPA/WPA2 assessments, it is arguably more efficient than the traditional deauth-and-capture approach because it does not depend on a client being present or responding.

{{< alert "circle-info" >}}
**PMKID capture works on all modern WPA2/WPA3 networks.** Access points broadcast PMKIDs in their beacon frames regardless of whether any client is associated. You do not need to be in range of a client — only the AP. This makes passive PMKID capture ideal for scenarios where deauthentication is not an option, either due to firmware limitations or engagement scope.
{{< /alert >}}

---

## Workaround: Use AWUS036ACH for Active Injection

For tasks that genuinely require active frame injection — forced WPA handshake capture via deauthentication, WPS enumeration, or similar operations — the **AWUS036ACH** (RTL8812AU chipset) is the established solution with mature, well-tested driver support in Kali Linux.

The recommended dual-adapter professional setup:

- **AWUS036AXML** → passive scanning and capture on 5 GHz / 6 GHz
- **AWUS036ACH** → active injection on 2.4 GHz / 5 GHz

This combination gives you complete coverage across all bands with injection handled by the RTL8812AU, whose active mode support on Linux has been stable for years. The AWUS036AXML takes over for 6 GHz discovery and high-quality passive capture, while the AWUS036ACH handles any active operations your assessment requires.

Most modern laptops and USB hubs handle both adapters simultaneously without issue. Assign them to separate logical roles at the start of an engagement to keep the workflow clean.

See the [AWUS036AXML review](/en/blog/awus036axml-wifi-6e-review/) and [packet injection guide](/en/blog/packet-injection-guide/) for setup details on both adapters.

---

## When Active Mode Works

It is worth noting that active mode does not fail universally. Several conditions have been reported by community members to produce stable or near-stable active mode behavior on MT7921AUN:

- **Kernel 6.6 or newer** with firmware-misc-nonfree 20240610 or later
- Avoiding `aireplay-ng --deauth` in burst mode (high packet-rate deauth floods are more likely to trigger the crash than single-frame operations)
- Using `--deauth 1` or `--deauth 3` rather than continuous deauth streams
- Ensuring the adapter is connected to a USB 3.0 port (USB 2.0 bandwidth constraints add stress to the firmware command pipeline)
- Operating at 2.4 GHz rather than 5 GHz for injection (lower-frequency band appears more stable in some driver versions)

If your engagement allows for careful testing before going operational, verify each active operation in isolation on a test network before relying on it. Note which specific commands and parameters work reliably on your specific kernel and firmware combination.

{{< alert "triangle-exclamation" >}}
**Test before production engagements.** Even when active mode appears to work, the MT7921AUN firmware can crash mid-operation under load. Always have a recovery plan (backup adapter or passive-only workflow) when using AWUS036AXML for active operations.
{{< /alert >}}

---

## Checking If Your Firmware Is Updated

To verify you have the latest firmware files and understand exactly what version is loaded:

```bash
# Check current firmware file date
ls -la /lib/firmware/mediatek/mt7921*

# Check driver version and source
modinfo mt7921u | grep -E "version|filename"

# Check kernel messages for firmware loading
sudo dmesg | grep mt7921
```

The `dmesg` output on successful firmware load should show something like:

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

If you see `firmware load failed` or similar errors, the firmware files are missing or corrupted. Reinstall `firmware-misc-nonfree` or copy files manually from the `linux-firmware` repository as described in Fix 1.

Cross-reference firmware file dates against the `linux-firmware` repository commit history to determine whether you are running the most recent available version for MT7921.

---

## Summary: AWUS036AXML Best Use Cases

Understanding the MT7921AUN's current Linux limitations helps you deploy the AWUS036AXML where it genuinely excels:

- ✅ **Passive WiFi 6E scanning and PCAP capture** — performs flawlessly
- ✅ **hcxdumptool PMKID capture** — no injection required, no firmware crash
- ✅ **6 GHz network discovery** — airodump-ng passive scanning on the 6 GHz band
- ✅ **WiFi 6E site survey and interference analysis** — tri-band passive monitoring
- ✅ **Baseline WPA2 handshake capture** — passive capture of handshakes from existing traffic
- ⚠️ **Active frame injection** — use AWUS036ACH instead until MT7921AUN firmware matures
- ⚠️ **Deauthentication floods** — risk of firmware crash; test carefully on kernel 6.6+
- ⭐ **Best workflow: carry both AWUS036AXML + AWUS036ACH** for full coverage

The AWUS036AXML is an exceptional passive capture adapter and the right tool for 6 GHz work. Pair it with the AWUS036ACH for injection and you have a professional-grade setup that covers every band and every operation type without relying on firmware that is still maturing.

---

## Related Guides

- [AWUS036AXML Full Review](/en/blog/awus036axml-wifi-6e-review/) — complete hardware review and Kali Linux setup
- [Packet Injection Guide](/en/blog/packet-injection-guide/) — using aireplay-ng and injection testing methodology
- [Driver Install Guide](/en/blog/install-alfa-driver-kali-ubuntu/) — installing MT7921AUN and RTL8812AU drivers on Kali and Ubuntu
