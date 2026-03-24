---
title: "Using ALFA WiFi Adapters with Kali NetHunter via USB OTG"
description: "How to use ALFA USB WiFi adapters with Kali NetHunter on Android via USB OTG. Covers AWUS036ACH driver, monitor mode commands, OTG cable requirements, and supported devices."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
---

Your Android phone is already a powerful computer in your pocket. With Kali NetHunter installed on a rooted device and an ALFA WiFi adapter plugged in via USB OTG, it becomes a genuinely capable pocket-sized penetration testing platform. No laptop required. No bulky hardware. Just your phone, a short OTG cable, and an adapter that supports monitor mode and packet injection.

This guide covers everything you need to get an ALFA AWUS036ACH (or compatible adapter) working under NetHunter — from hardware selection through driver loading, monitor mode activation, and the wireless tools built into the NetHunter app.

---

## What Is Kali NetHunter?

Kali NetHunter is Kali Linux's official mobile penetration testing platform. Rather than replacing Android, NetHunter installs a Kali Linux chroot environment on top of your existing Android installation. Your phone continues to function as a normal Android device while simultaneously running a full Kali Linux userland with all its tools.

**Key characteristics:**

- Runs without wiping Android — your apps, contacts, and data stay intact
- Includes the NetHunter app, a dedicated launcher for attack modules and hardware control
- Provides a full terminal with access to the Kali toolset (Metasploit, Aircrack-ng, Nmap, and hundreds more)
- Requires a rooted Android device for full functionality

**Three editions:**

| Edition | Root Required | Kernel Mods | Use Case |
|---|---|---|---|
| NetHunter (Full) | Yes | Yes (custom kernel) | Full attack surface, hardware interface support |
| NetHunter Lite | Yes | No | Root-only tools, no custom kernel needed |
| NetHunter Rootless | No | No | Limited tools, no hardware attacks |

For USB OTG adapter support with monitor mode, you need the **full NetHunter edition** with a custom kernel that includes the RTL8812AU module.

**Officially supported devices** include models from OnePlus, Google Pixel, and selected Samsung Galaxy devices. For the complete and current list, see the [official NetHunter device page](https://www.kali.org/docs/nethunter/).

**USB OTG is a mandatory requirement.** Before purchasing hardware, verify that your specific device model supports USB OTG. Most modern devices do, but some budget models and older hardware may lack the necessary USB controller support.

---

## Hardware Requirements

Getting this setup right means choosing compatible hardware at every level. A mismatch anywhere in the chain — device, cable, or adapter — will result in the adapter never appearing in `lsusb`, intermittent disconnects, or driver failures.

| Item | Requirement | Notes |
|---|---|---|
| Android device | Rooted, NetHunter-supported, USB OTG capable | Verify OTG support before purchasing; full NetHunter with custom kernel required |
| USB OTG cable / adapter | USB-C OTG or Micro-USB OTG depending on device port | Quality matters — cheap cables cause intermittent disconnects |
| ALFA WiFi adapter | AWUS036ACH or AWUS036ACM recommended | AWUS036ACH (RTL8812AU) has best NetHunter kernel module support; AWUS036ACM (MT7612U) also compatible |
| Powered USB OTG hub | Strongly recommended | Prevents adapter-induced battery drain and USB instability |

{{< alert "triangle-exclamation" >}}
The AWUS036ACH draws approximately **500mW** from the USB port. Powering it directly from a phone battery without a dedicated power source will drain your battery significantly faster and may cause the adapter to reset or disconnect under load. A powered OTG hub — one that takes power from a wall adapter and passes data through to the phone — eliminates this problem entirely.
{{< /alert >}}

**On choosing a powered OTG hub:**

Look for a hub explicitly marketed as supporting USB OTG with power delivery passthrough. This means the hub takes 5V from a USB charger, powers attached devices from the charger rather than the phone, and still passes data between the phone and attached devices. Not all USB hubs support this — check the product specifications carefully before buying.

---

## Supported ALFA Adapters for NetHunter

NetHunter's custom kernel includes pre-compiled kernel modules for a specific set of chipsets. The RTL8812AU chipset family has the strongest support because it was integrated early and is actively maintained.

| Adapter | Chipset | NetHunter Support | Notes |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ Best support | NetHunter kernel includes `88XXau` module; monitor mode and packet injection fully supported |
| AWUS036ACM | MT7612U | ✅ Good support | Alternative chipset; generally works; verify against your specific device kernel |
| AWUS036ACS | RTL8811AU | ✅ Works | Same driver family as RTL8812AU; lower power draw (~300mW); single-band 2.4/5 GHz |
| AWUS036AXM | MT7921AUN | ⚠️ Limited | WiFi 6E adapter; kernel module availability depends on device and kernel version |
| AWUS036AXML | MT7921AUN | ⚠️ Limited | Same chipset as AXM; not universally supported in NetHunter kernels |

**Recommendation:** For reliable NetHunter operation, stick with RTL8812AU-based adapters. The `88XXau` driver is specifically included in most NetHunter custom kernels, you'll find extensive community documentation for it, and the troubleshooting path is well-understood. The WiFi 6E adapters are technically impressive but not worth the compatibility risk for a mobile pentest setup where reliability matters more than raw throughput.

If you want dual-band AC1200 capability with broad NetHunter compatibility, the **AWUS036ACH** is the correct choice.

---

## Setup Steps

The following steps assume you have a rooted Android device with full NetHunter installed and a USB OTG cable or powered hub ready.

### Step 1: Open the NetHunter App

Launch the NetHunter app on your Android device. Navigate to **Kali Services** to verify that the chroot environment is running. If it is not running, tap **Start** to bring it up. The chroot must be active before the kernel can expose USB devices to Kali tools.

### Step 2: Connect the ALFA Adapter via OTG

Plug your USB OTG cable or hub into the phone's USB port, then connect the ALFA adapter to the OTG cable or hub. If you are using a powered hub, connect the hub's power adapter to a wall outlet first.

### Step 3: Grant USB Permission

Android will display a permission dialog asking whether the NetHunter app is allowed to access the USB device. Tap **OK** and check **Always allow** if you want to skip this prompt in future sessions. If you dismiss this dialog without granting permission, the adapter will not be accessible from the Kali chroot.

### Step 4: Verify the Adapter in `lsusb`

Open the NetHunter terminal and run:

```bash
lsusb
```

You should see an entry containing **Realtek Semiconductor** along with the device ID. For the AWUS036ACH, expect something like:

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

If the Realtek device does not appear, the issue is at the hardware level — check the OTG cable, try a different cable, or verify that OTG is enabled in your device's developer settings.

### Step 5: Load the Driver

```bash
sudo modprobe 88XXau
```

On most NetHunter builds the driver loads automatically when the adapter is detected. If the interface does not appear after connecting the adapter, run this command manually. The `88XXau` module is the Aircrack-ng maintained RTL8812AU driver included in NetHunter's custom kernel.

### Step 6: Verify the Interface

```bash
ip link show | grep wlan
```

You should see `wlan1` (or `wlan2` if your device has a built-in WiFi interface on `wlan0`). Confirm the interface is listed before attempting to enable monitor mode.

### Step 7: Enable Monitor Mode

```bash
sudo airmon-ng start wlan1
```

If `airmon-ng` reports processes that could interfere with monitor mode, kill them first (see the commands section below), then re-run this command. The interface will be renamed to `wlan1mon` after monitor mode is activated.

---

## Monitor Mode Commands on NetHunter

The following command sequence covers the full workflow from adapter verification through active capture:

```bash
# Check adapter is recognized by the system
lsusb | grep -i realtek

# Load driver if not auto-loaded after connecting adapter
sudo modprobe 88XXau

# Kill processes that interfere with monitor mode (NetworkManager, wpa_supplicant, etc.)
sudo airmon-ng check kill

# Start monitor mode on the ALFA adapter interface
sudo airmon-ng start wlan1

# Scan all visible networks (press Ctrl+C to stop)
sudo airodump-ng wlan1mon

# Capture traffic from a specific network
# -c: channel, --bssid: target AP MAC address, -w: output file prefix
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

**To stop monitor mode and return to managed mode:**

```bash
sudo airmon-ng stop wlan1mon
```

**To check adapter capabilities and confirm monitor mode is active:**

```bash
iwconfig wlan1mon
```

The output should show `Mode:Monitor` if everything is working correctly.

---

## NetHunter WiFi Attacks (Authorized Testing Only)

The NetHunter app includes built-in GUI interfaces for several WiFi-focused attack modules. These are accessible without typing any terminal commands, making them useful for demonstrations or when operating in the field.

{{< alert "triangle-exclamation" >}}
All wireless security testing must be performed **only on networks and devices you own or have explicit written authorization to test**. Unauthorized access to computer networks is illegal in most jurisdictions worldwide. The tools described here are for authorized penetration testing, security research, and educational purposes only. Yupitek accepts no liability for misuse.
{{< /alert >}}

**WiFi Evil Portal (WPS3):** Available directly in the NetHunter app's main menu. Creates a rogue access point with a captive portal for credential harvesting during authorized social engineering assessments. Requires an external adapter with AP mode support.

**MANA Rogue AP Toolkit:** Located at **NetHunter app > Wireless Attacks > MANA Toolkit**. MANA extends the standard rogue AP concept with KARMA-style attacks and SSL stripping capabilities. The full functionality requires a compatible external WiFi adapter — the internal Android WiFi chip is not sufficient for most MANA configurations.

Both modules interface directly with your ALFA adapter, which is why external adapter support is essential for practical use of these built-in tools.

---

## Battery and Power Management

Running an AWUS036ACH from a phone is demanding on the battery and the USB power delivery subsystem. Here is what to expect and how to mitigate it:

**Power draw:** The AWUS036ACH draws approximately 500mW continuously during active use. On a typical 3,500 mAh Android battery, this will roughly double your battery drain rate compared to normal phone usage.

**Using a powered OTG hub:** This is the most effective solution. The hub draws power from a wall adapter and supplies it to the ALFA adapter. The phone's USB port only carries data, not power to the adapter. Battery drain returns to near-normal levels.

**Operating while charging:** If a powered hub is not available, you can mitigate battery drain by simultaneously charging the phone using a USB-C with PD passthrough hub. This requires a hub that supports both data passthrough (for the OTG function) and simultaneous charging input — these are available but require careful product selection.

**Display management:** The screen is the other major power consumer during field operations. Set display timeout to 30 seconds (**Settings > Display > Sleep**) and reduce brightness to minimum. Combined with a powered hub, this gives you practical multi-hour operation time.

**Thermal considerations:** Extended adapter operation in a phone case can cause heat buildup. If the phone's thermal protection throttles the USB controller, adapter disconnects may occur. Remove the phone case during extended capture sessions.

---

## Troubleshooting

**Adapter not recognized (`lsusb` shows nothing):**
1. Verify USB OTG is enabled — check **Settings > Developer Options > OTG** (location varies by Android version and manufacturer)
2. Try a different OTG cable — cable quality is a common failure point
3. Try the adapter in a different USB device to confirm the adapter itself is functional
4. Confirm your device supports USB OTG by checking the manufacturer specifications

**Driver not loading (no `wlan1` interface after `modprobe`):**
1. Check `dmesg` in the NetHunter terminal for USB and driver error messages: `dmesg | tail -30`
2. Verify the NetHunter chroot is running and you are executing commands inside it
3. Confirm your NetHunter build includes the `88XXau` module: `find /lib/modules -name "*88XX*"`

**`wlan1` interface disappears during use:**
This is almost always a USB power issue. The adapter is drawing more current than the phone's USB port can sustain. Use a powered OTG hub. As a temporary measure, reduce transmission power with `sudo iw dev wlan1 set txpower fixed 1000` (sets to 10 dBm).

**Permission denied errors:**
Ensure you are running commands as root in the NetHunter chroot. Run `sudo su` first, then execute the commands. Alternatively, prefix each command with `sudo`.

**Monitor mode starts but no networks appear in `airodump-ng`:**
1. Confirm the channel is set correctly — try `sudo airodump-ng --band abg wlan1mon` to scan all bands
2. Check that `airmon-ng check kill` was run before starting monitor mode
3. Verify the antenna is properly connected to the adapter

---

## Related Guides

For other platforms and use cases with ALFA adapters:

- [AWUS036ACH setup guide on Kali Linux (desktop/laptop)](/en/blog/awus036ach-kali-linux-setup/)
- [Using ALFA adapters with Raspberry Pi and Kali](/en/blog/alfa-adapter-raspberry-pi-kali/)
