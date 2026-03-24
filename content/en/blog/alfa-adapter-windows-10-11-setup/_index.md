---
title: "ALFA Adapter Setup Guide for Windows 10 and Windows 11"
description: "How to install and configure ALFA USB WiFi adapters on Windows 10/11. Driver download, monitor mode with Acrylic WiFi, troubleshooting, and adapter comparison for Windows users."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-adapter", "driver-install", "acrylic-wifi"]
---

ALFA Network USB WiFi adapters are well known in security research and networking circles, but most tutorials focus exclusively on Linux. The good news for Windows users: every major ALFA adapter works on Windows 10 and Windows 11 with manufacturer-provided drivers — no source compilation required.

The critical difference from Linux is monitor mode. On Linux, tools like `aircrack-ng` and `airodump-ng` leverage raw 802.11 capture with packet injection. On Windows, the driver model (NDIS) does not expose the same hardware capabilities. Full monitor mode and packet injection are **not available natively on Windows**. What Windows does well — and does very well — is plug-and-play connectivity and WiFi scanning with polished tools like Acrylic WiFi Analyzer.

This guide walks through driver installation, WiFi scanning, and an honest assessment of what Windows can and cannot do with an ALFA adapter.

---

## Compatible ALFA Adapters for Windows

All adapters below are officially supported on Windows 10 and Windows 11. Driver availability and monitor mode capability differ by chipset.

| Model | Chipset | Windows 10 | Windows 11 | Monitor Mode Support |
|---|---|---|---|---|
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | ✅ Full support | ✅ Full support | ⚠️ Passive scan only (Acrylic WiFi Pro) |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | ✅ Full support | ✅ Full support | ⚠️ Passive scan only |
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | ✅ Full support | ✅ Full support | ⚠️ Passive scan only |
| [AWUS036AX](/en/products/alfa/awus036ax/) | MT7921AU | ⚠️ Manual driver download | ✅ In-box driver | ⚠️ Limited |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | MT7921AU | ⚠️ Manual driver download | ✅ In-box driver | ⚠️ Limited |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AU | ⚠️ Manual driver download | ✅ In-box driver | ❌ Not supported |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7902 | ⚠️ Manual driver download | ✅ In-box driver | ❌ Not supported |

{{< alert "circle-info" >}}
For pure Windows day-to-day use, the AWUS036ACH (RTL8812AU) and AWUS036ACM (MT7612U) are the most battle-tested choices. Both receive Realtek/MediaTek WHQL-signed drivers and have the broadest Windows compatibility record.
{{< /alert >}}

---

## Installing the Driver

### Method A: Windows Update (Recommended)

Windows Update is the easiest path for most adapters. When you plug in a supported ALFA adapter, Windows automatically queries Windows Update for a matching NDIS driver.

1. Plug the ALFA adapter into a USB 3.0 port.
2. Wait 30–60 seconds. Windows will show a notification: *"Device driver software installed successfully"* (Windows 10) or silently complete in Windows 11.
3. Open **Device Manager** (`Win + X` → Device Manager).
4. Expand **Network Adapters**. You should see the adapter listed (e.g., *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* or *"MediaTek Wi-Fi 6 MT7921U Wireless LAN Card"*).
5. If the adapter appears with a yellow warning icon, proceed to Method B.

{{< alert "circle-info" >}}
Windows Update requires an active internet connection to download drivers. If you're setting up an isolated lab machine, download the driver package on another computer and transfer it manually before using Method B.
{{< /alert >}}

### Method B: Manual Driver Install — RTL8812AU (AWUS036ACH / AWUS036ACM / AWUS036ACS)

1. Visit the [ALFA Network download page](https://www.alfa.com.tw/service_1.html) or the Realtek driver archive and download the latest Windows WHQL driver for RTL8812AU.
2. Extract the `.zip` archive to a local folder (e.g., `C:\Drivers\RTL8812AU`).
3. Run the `.exe` installer as Administrator. Accept the UAC prompt.
4. Follow the installer wizard. When prompted, leave the default installation path.
5. Reboot when the installer completes.
6. Open **Device Manager** → **Network Adapters**. Confirm the adapter appears without a warning icon.

To verify the driver version:

1. Right-click the adapter in Device Manager → **Properties**.
2. Click the **Driver** tab.
3. Note the **Driver Version** and **Driver Date** for future reference.

### Method B: Manual Driver Install — MT7921AU (AWUS036AX / AWUS036AXER / AWUS036AXM / AWUS036AXML)

MediaTek's MT7921AU driver is included in Windows 11's driver store (build 22000+). For Windows 10:

1. Download the MediaTek MT7921 driver package from [MediaTek's official site](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) or ALFA Network's support page.
2. Extract the package and run `Setup.exe` as Administrator.
3. Reboot after installation.

{{< alert "circle-info" >}}
Windows 11 users with MT7921AU/MT7902 adapters typically get a working driver within minutes of plugging in the adapter, even on a fresh install — no manual download needed.
{{< /alert >}}

### Common Device Manager Error Codes

| Error Code | Meaning | First Fix |
|---|---|---|
| **Code 43** | Driver reported a failure | Uninstall driver → reboot → reinstall |
| **Code 10** | Device cannot start | Try a different USB port; disable USB selective suspend |
| **Code 28** | No drivers installed | Run Windows Update or install driver manually |
| **Code 45** | Device not connected | Reconnect adapter; try different USB cable if using extension |

---

## Using ALFA Adapter for WiFi Scanning on Windows

### Native Windows Command-Line Scanning

Windows includes a built-in WiFi scanning command that requires no extra software:

```cmd
netsh wlan show networks mode=bssid
```

This outputs every visible SSID along with BSSID (MAC address), signal strength, radio type, channel, and authentication type. It's useful for quick diagnostics but lacks real-time channel graphs or hidden SSID detection.

### Acrylic WiFi Analyzer (Free)

For serious WiFi analysis on Windows, [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) is the recommended tool. The free version provides:

- Real-time scanning across 2.4 GHz, 5 GHz, and 6 GHz bands
- Channel occupancy graphs — instantly identify congested channels
- Hidden SSID detection (shows networks broadcasting empty SSIDs)
- Signal history charts for individual access points
- Vendor OUI lookup for BSSID identification

Acrylic WiFi works with any Windows-compatible WiFi adapter, including all ALFA models listed above. Its NDIS driver extension integrates directly with the Windows wireless stack, which is why it works without Linux-style monitor mode.

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer is the closest Windows equivalent to tools like `airodump-ng` for passive scanning. If your workflow is WiFi surveying, site analysis, or channel planning, it covers nearly everything you need without leaving Windows.
{{< /alert >}}

### Wireshark Capture on Windows

Wireshark can capture WiFi traffic on Windows with the help of Npcap (see the dedicated section below). However, without true monitor mode, you capture only:

- Frames addressed to your adapter (unicast to your MAC)
- Broadcast and multicast frames on your associated network

You do **not** capture traffic between other devices unless they happen to be on the same broadcast domain and Wireshark is running in promiscuous mode on a switched network. Full 802.11 frame capture (management frames, beacon frames from foreign APs) is restricted.

---

## Monitor Mode on Windows (The Honest Truth)

This is where expectations need to be set clearly.

**Monitor mode on Windows is fundamentally different from Linux monitor mode.**

On Linux, drivers like `aircrack-ng/rtl8812au` expose a true monitor-mode interface (`wlan0mon`) that receives all 802.11 frames in the radio environment — management frames, data frames from other networks, probe requests, and beacon frames — without requiring association. The adapter also supports packet injection: sending raw 802.11 frames at the hardware level.

On Windows, the NDIS driver model does not expose these capabilities. The two practical approaches for Windows-based monitoring are:

**Approach A: Acrylic WiFi Pro + compatible driver**

Acrylic WiFi Pro uses a custom NDIS driver extension to enable *passive 802.11 scanning*. This lets you receive beacon frames and probe responses from access points you're not connected to — enough for RF surveys, channel analysis, and AP enumeration. It does **not** support packet injection or full handshake capture.

**Approach B: Kali Linux live USB**

For workflows that require full monitor mode with packet injection — WPA handshake capture, deauth testing, beacon flooding — the correct platform is Kali Linux. You have two options:

- Boot a **Kali Linux live USB** on the same machine (bare metal, full hardware access)
- Run a **Kali Linux VM** (VMware or VirtualBox) with USB passthrough to hand the ALFA adapter directly to the VM's USB stack

See the [VirtualBox/VMware USB passthrough guide](/en/blog/alfa-adapter-virtualbox-vmware-usb/) for detailed VM setup instructions.

{{< alert "triangle-exclamation" >}}
If your workflow requires monitor mode + packet injection — for WPA handshake capture, deauthentication frames, or any active 802.11 attack — Windows cannot do this reliably. Kali Linux (bare metal or VM with USB passthrough) is the correct platform. No Windows driver currently supports raw 802.11 injection for ALFA adapters.
{{< /alert >}}

---

## Troubleshooting

### Adapter Not Recognized at All

1. Try a different USB port — preferably USB 3.0 (blue port). Some USB hubs lack sufficient power for dual-band adapters.
2. Open Device Manager and look under **Other Devices** for an entry with a yellow question mark. This confirms Windows sees the hardware but lacks a driver.
3. Right-click → **Update Driver** → **Browse my computer** and point to the manually downloaded driver folder.
4. If nothing appears in Device Manager even under Other Devices, try a different USB cable (if using an extension) or test the adapter on another computer to rule out hardware failure.

### Adapter Visible in Device Manager but No Networks Found

1. Temporarily disable Windows Defender Firewall to confirm it's not blocking adapter initialization. Re-enable after testing.
2. In Device Manager, right-click the adapter → **Properties** → **Advanced** tab. Look for **Wireless Mode** or **Band** settings. If set to 5 GHz only, you'll see no networks in a 2.4 GHz-only environment.
3. Confirm the adapter is not disabled: right-click → **Enable Device**.
4. Run `netsh wlan show interfaces` in an elevated Command Prompt to verify the adapter's operational state.

### Slow Speeds or Frequent Disconnects on Windows 11

Windows 11's **Connected Standby** (Modern Standby) can interfere with USB WiFi adapters by aggressively suspending USB devices.

Disable USB selective suspend:

1. Open **Control Panel** → **Power Options** → **Change plan settings** → **Change advanced power settings**.
2. Expand **USB settings** → **USB selective suspend setting**.
3. Set to **Disabled** for both **On battery** and **Plugged in**.
4. Click **Apply** → **OK**, then reboot.

### Code 43: Driver Reported Failure

1. Open Device Manager, right-click the adapter → **Uninstall device**. Check *"Delete the driver software for this device"* if the option appears.
2. Unplug the adapter.
3. Reboot the computer.
4. Plug the adapter back in.
5. Reinstall the driver using Method B above.

If Code 43 persists after a clean reinstall, try a different USB port or test on another machine. A persistent Code 43 on multiple machines typically indicates a hardware fault with the adapter itself.

---

## ALFA Adapter + Wireshark Setup

Wireshark on Windows requires **Npcap** as its packet capture library. WinPcap (the legacy alternative) is outdated and does not support modern Windows versions reliably.

### Step 1: Install Npcap

1. Download Npcap from [https://npcap.com/](https://npcap.com/) (free for personal and educational use).
2. Run the installer as Administrator.
3. During installation, check **"Install Npcap in WinPcap API-compatible mode"** if you plan to use any legacy tools alongside Wireshark.
4. Reboot.

### Step 2: Configure Wireshark

1. Open Wireshark. Your ALFA adapter will appear in the interface list.
2. Double-click the adapter interface to start a capture.
3. To filter for 802.11 management frames (beacon frames, probe requests), use the Wireshark display filter:

```
wlan.fc.type == 0
```

4. To filter for probe requests specifically:

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
The `wlan.fc.type` filter only works when Wireshark receives actual 802.11 frames with visible headers. On Windows without monitor mode, most captures show Ethernet II frames even over WiFi — the NDIS layer strips the 802.11 header before passing frames to Npcap. Full 802.11 header capture requires a true monitor mode interface, available on Linux.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Capturing network traffic without authorization is illegal in most jurisdictions. Only capture traffic on networks you own or have explicit written permission to test.
{{< /alert >}}

---

## Summary: Windows vs Linux for ALFA Adapters

| Feature | Windows 10/11 | Kali Linux |
|---|---|---|
| **Plug & play** | ✅ Automatic driver install | ⚠️ Varies by chipset |
| **WiFi scanning** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **Monitor mode** | ⚠️ Passive only (Acrylic Pro) | ✅ Full monitor mode |
| **Packet injection** | ❌ Not supported | ✅ Full injection |
| **Wireshark capture** | ⚠️ Limited (no 802.11 headers) | ✅ Full 802.11 capture |
| **WPA handshake capture** | ❌ Not reliable | ✅ aircrack-ng / hcxdumptool |
| **Best use case** | Day-to-day connectivity, WiFi surveying, channel analysis | Security testing, CTF challenges, penetration testing |

The bottom line: Windows is an excellent platform for ALFA adapters when your goal is network connectivity, WiFi analysis, and channel planning. The moment your workflow requires raw 802.11 frame injection or WPA handshake capture, switch to Kali Linux — either natively or via a VM with USB passthrough.

---

## Related Guides

- [VirtualBox & VMware USB Passthrough for ALFA Adapters](/en/blog/alfa-adapter-virtualbox-vmware-usb/) — Run Kali Linux in a VM with full ALFA adapter support
- [Driver Install Guide for Kali Linux & Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/) — Complete chipset-specific driver installation
- [ALFA WiFi Adapter Buyer Guide 2026](/en/blog/alfa-wifi-adapter-buyer-guide-2026/) — Which adapter is right for your use case
