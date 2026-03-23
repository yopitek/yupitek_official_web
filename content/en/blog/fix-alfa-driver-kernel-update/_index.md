---
title: "ALFA Driver Broke After Kernel Update? Here's How to Fix It"
description: "ALFA USB WiFi adapter not working after Linux kernel update? Complete fix guide for RTL8812AU, RTL8811AU, and MT7921AU drivers on Kali Linux and Ubuntu after kernel upgrades."
date: 2026-04-15
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

You run `sudo apt upgrade`, reboot, and your ALFA adapter has vanished. No interface, no lights, nothing. This is the single most common support question surrounding ALFA Network USB WiFi adapters on Linux — and kernel updates are almost always the culprit. This guide walks you through a systematic diagnosis and repair process for the two most affected chipset families: **RTL8812AU** (found in the AWUS036ACH, ACM, and ACS) and **MT7921AU** (found in the AWUS036AXM, AXML, and AX). Follow each section in order and your adapter will be back online in under 15 minutes.

---

## Why Kernel Updates Break Drivers

Linux WiFi drivers come in two flavours: **in-kernel** drivers that ship with the kernel source tree, and **out-of-tree** drivers that live outside it. Understanding which type you have explains exactly why updates break things.

### Out-of-Tree Drivers and DKMS

The RTL8812AU chipset uses an out-of-tree driver maintained by the community (most commonly the `aircrack-ng/rtl8812au` fork). Because it is not part of the official kernel source, it must be **compiled against the headers of your specific running kernel**. Every time the kernel version changes — even a minor patch release like `6.6.15` → `6.6.20` — the compiled module is no longer compatible and the kernel refuses to load it.

**DKMS (Dynamic Kernel Module Support)** is the standard solution. DKMS registers the driver's source code with a system-level hook that automatically recompiles the module whenever a new kernel package is installed. When DKMS is set up correctly, kernel updates are transparent: you reboot into the new kernel and your adapter is already working.

DKMS can silently fail for two reasons:

1. **Missing kernel headers** — the compiler needs `linux-headers-$(uname -r)` installed at the time the new kernel lands. If headers arrive after the kernel, DKMS misses its build window.
2. **Stale `dkms.conf`** — if the installed driver version has an outdated configuration file that no longer matches the source tree, the build fails with cryptic errors.

### In-Kernel Drivers (MT7921U)

The MT7921U chipset has been in the mainline kernel since version **5.18**. That means no compilation step is needed — the kernel already knows how to talk to the hardware. However, the driver still depends on a **firmware blob** (`mt7921u.bin`) supplied by a separate package. If that package is missing or if the kernel update changes the expected firmware API, the adapter can appear to load but fail to associate with any network.

### Quick Diagnostic Commands

Before touching anything, run these two commands to understand your starting point:

```bash
# What kernel is currently running?
uname -r

# What DKMS modules are built (and for which kernels)?
sudo dkms status
```

If `dkms status` shows your RTL8812AU driver built for an *older* kernel but not the current one, you have found your problem.

---

## Step 1: Diagnose Your Driver

Work through this diagnostic sequence top-to-bottom. Each check narrows down the root cause before you start making changes.

```bash
# Check current kernel
uname -r

# Check if any wireless interface exists at all
ip link show | grep -E "wlan|wlp"

# Check whether the driver module is currently loaded
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# Check DKMS build status for RTL8812AU adapters
sudo dkms status

# Scan kernel ring buffer for relevant error messages
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**Interpreting the results:**

| Output | Meaning |
|---|---|
| `ip link` returns nothing wireless | Kernel module not loaded or hardware not enumerated |
| `lsmod` shows no matching module | Module failed to load — check `dmesg` for errors |
| `dkms status` shows `broken` or missing for current kernel | DKMS build failed — follow RTL8812AU fix below |
| `dmesg` shows `firmware: failed to load mt7921u` | Firmware package missing — follow MT7921U fix below |
| `dmesg` shows `disagrees about version of symbol` | Module was built against wrong kernel headers |

{{< alert "triangle-exclamation" >}}
If `ip link` shows the interface but it disappears when you try to use it, skip ahead to the adapter-specific troubleshooting table. A visible-but-non-functional interface has different causes than a completely missing one.
{{< /alert >}}

---

## Fix: RTL8812AU Driver (AWUS036ACH, ACM, ACS, EACS)

The RTL8812AU is the most widely used ALFA chipset for penetration testing because of its dual-band support and reliable monitor mode. It requires an out-of-tree driver and is therefore the chipset most frequently broken by kernel updates.

### 4.1 — Install Kernel Headers

The very first step, before touching any driver, is ensuring the headers for your *current* kernel are installed:

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

If this command exits cleanly, headers are now present and the DKMS rebuild can proceed. If it reports that the package cannot be found, your kernel may be too new for the current repository snapshot — run `sudo apt full-upgrade` first to pull in the matching headers, then reboot before continuing.

### 4.2 — Rebuild via DKMS (Fastest Path)

With headers in place, ask DKMS to rebuild all registered modules for the running kernel:

```bash
sudo dkms autoinstall
```

Watch the output carefully. A successful build ends with `DKMS: install completed`. If it succeeds, reload the module without rebooting:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

If the interface appears, you are done. Proceed to step 4.4 to verify monitor mode.

### 4.3 — Full Reinstall from Source (When DKMS Fails)

If `dkms autoinstall` reports errors, the registered driver source is corrupt or outdated. Remove it entirely and reinstall from the latest upstream source:

```bash
# Remove all DKMS-registered versions of the driver
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# Clone the latest driver source
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Register source with DKMS, compile, and install in one step
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
The version number `5.6.4.2` in the `dkms remove` command is a common release but yours may differ. Run `sudo dkms status` first and use the exact version string shown in the output.
{{< /alert >}}

After the build completes:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — Verify Monitor Mode

The adapter is physically present and the driver is loaded. Confirm that monitor mode — the feature that makes this adapter worth using for security testing — still works:

```bash
sudo airmon-ng start wlan0
```

Replace `wlan0` with your actual interface name from `ip link`. A successful response shows `monitor mode vif enabled` with a new interface name like `wlan0mon`.

### 4.5 — Kali Package Method (Easiest)

Kali Linux ships a pre-packaged DKMS build of the RTL8812AU driver that stays in sync with the Kali kernel. If you are on Kali, use this approach instead of cloning from GitHub:

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

This single command installs the driver source, registers it with DKMS, and builds it against the current kernel. Future `apt full-upgrade` runs will keep headers and driver in sync automatically.

---

## Fix: MT7921U Driver (AWUS036AX, AXM, AXML, AXER)

The MT7921U (Wi-Fi 6E) chipset takes a completely different path. Because it is an **in-kernel driver** since Linux 5.18, there is no DKMS, no compilation, and no GitHub clone involved. Kernel updates should not break it — but firmware packaging issues sometimes do.

### 5.1 — Install the Firmware Package

The kernel module (`mt7921u.ko`) is already present, but it needs a firmware binary from userspace to initialise the hardware:

```bash
sudo apt install firmware-misc-nonfree
```

On Ubuntu, this package lives in the `non-free` repository component. If the command fails, ensure you have non-free sources enabled in `/etc/apt/sources.list`.

### 5.2 — Reload the Driver

After installing firmware, force a driver reload without rebooting:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

Then check for the interface:

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — Verify Your Kernel Version

The MT7921U driver requires kernel **5.18 or newer**. If you installed a minimal Kali or Ubuntu image that shipped before this kernel version, the module simply does not exist:

```bash
uname -r
# Output must be 5.18.x or higher
```

If your kernel is older than 5.18, upgrade it (step 5.4).

### 5.4 — Upgrade the Kernel

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
Use `full-upgrade` rather than `upgrade`. The `upgrade` subcommand withholds packages that require removing others — this often means the kernel package itself is held back. `full-upgrade` allows the necessary dependency resolution.
{{< /alert >}}

### 5.5 — Verify After Reboot

After rebooting into the new kernel, confirm everything is working:

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

A healthy `dmesg` output shows the firmware loading successfully and the USB device being registered as a network interface.

---

## Keeping Drivers Alive After Future Updates

Prevention is simpler than repair. These practices stop kernel updates from breaking your adapter again.

**Always use `full-upgrade` on Kali rolling:**

```bash
sudo apt update && sudo apt full-upgrade
```

The `full-upgrade` command ensures that when a new kernel package is installed, the matching `linux-headers` package is installed in the *same transaction*. DKMS hooks fire during package installation — if headers arrive in a later `apt` run after the kernel, DKMS misses the build.

**Install the DKMS meta-package:**

```bash
sudo apt install dkms linux-headers-generic
```

This pulls in `linux-headers-generic` as a dependency of the DKMS package, so headers always stay current alongside the kernel.

**Ubuntu HWE kernel stack:**

On Ubuntu LTS, the Hardware Enablement kernel stack receives more frequent updates and better hardware support than the GA kernel. Install it once and updates are handled automatically:

```bash
sudo apt install linux-generic-hwe-24.04
```

**Verify DKMS autoinstall is enabled:**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

If this line is commented out or set to `no`, DKMS will not rebuild modules automatically. Uncomment it or set it to `yes` in `/etc/dkms/framework.conf`.

---

## Adapter-Specific Troubleshooting Table

| Symptom | Likely Chipset | Root Cause | Quick Fix |
|---|---|---|---|
| Interface missing after reboot | RTL8812AU | DKMS build failed | `sudo dkms autoinstall` |
| Interface missing, `dmesg` shows firmware error | MT7921AU | Missing firmware package | `sudo apt install firmware-misc-nonfree` |
| Interface appears but disappears after 30s | RTL8812AU | Module version mismatch | `sudo dkms remove --all && sudo make dkms_install` |
| Monitor mode fails with `SIOCSIFFLAGS` | RTL8812AU | Wrong driver branch | Clone `aircrack-ng/rtl8812au` and reinstall |
| `iwconfig` shows no wireless extensions | Any | Module not loaded | `sudo modprobe 88XXau` or `sudo modprobe mt7921u` |
| Interface present but no networks found | MT7921AU | Kernel < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` shows `broken` | RTL8812AU | Source/header mismatch | `sudo apt install linux-headers-$(uname -r)` then rebuild |
| TX power capped at 20 dBm | RTL8812AU | Regulatory domain lock | `sudo iw reg set US` (adjust for your region) |

---

## If Nothing Works: Fresh Install Method

When multiple rebuild attempts have failed and `dkms status` is showing confusing output from several partial installs, a clean slate is faster than debugging:

```bash
# Purge the Kali package if it was installed
sudo apt purge realtek-rtl88xxau-dkms

# Remove all DKMS entries for rtl8812au
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# Remove leftover source directory if present
sudo rm -rf /usr/src/rtl8812au*

# Clean any stale module cache
sudo depmod -a

# Fresh clone and install
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
The loop that removes DKMS entries will fail silently if no versions are found — that is fine. The important step is `sudo rm -rf /usr/src/rtl8812au*` which removes any source tree that may have been left in a broken state.
{{< /alert >}}

---

## Prevention Checklist

Use this checklist before every system update to avoid surprises during an engagement:

**Before `apt upgrade`:**

```bash
# See exactly which kernel packages are pending
apt list --upgradable 2>/dev/null | grep linux-image
```

If a new kernel is incoming, plan for a test reboot before any production work.

**After every upgrade and reboot:**

```bash
# Confirm the adapter is back
ip link show | grep -E "wlan|wlp"

# Confirm monitor mode still works
sudo airmon-ng check
```

**Keep a fallback:**
- Maintain a USB drive with a Kali Live image (or a second adapter on a known-working driver). Connectivity issues during a scheduled engagement are costly — a physical fallback takes minutes to prepare and can save the day.

**Pin critical driver packages on Kali:**

```bash
# Prevent a specific driver package from being auto-removed during upgrades
sudo apt-mark hold realtek-rtl88xxau-dkms
```

Release the hold before explicitly upgrading the driver:

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## Summary

ALFA driver failures after kernel updates follow a predictable pattern and have predictable solutions. RTL8812AU adapters need `dkms autoinstall` (or a fresh clone from `aircrack-ng/rtl8812au`) plus matching kernel headers. MT7921U adapters need `firmware-misc-nonfree` and a kernel of 5.18 or newer. The long-term fix in both cases is ensuring `apt full-upgrade` — not `apt upgrade` — is your standard update command, which keeps headers and kernels in lockstep.

---

**Related guides:**
- [How to Install ALFA USB WiFi Driver on Kali Linux & Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/) — start here if you have never installed the driver before
- [AWUS036ACH Kali Linux Setup Guide](/en/blog/awus036ach-kali-linux-setup/) — full setup walkthrough including monitor mode and packet injection verification
