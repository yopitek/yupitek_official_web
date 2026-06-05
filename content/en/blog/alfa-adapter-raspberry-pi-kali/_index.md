---
title: "ALFA WiFi Adapter on Raspberry Pi with Kali Linux: Setup Guide"
description: "Install ALFA USB WiFi adapters on Raspberry Pi running Kali Linux ARM64. Covers AWUS036ACH RTL8812AU driver compile, monitor mode, and portable penetration testing setup."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
---

A laptop running Kali Linux is the standard pentesting workstation — but it is far from the only option. A Raspberry Pi 4 or Pi 5 paired with an ALFA USB WiFi adapter gives you a compact, fanless, passively-cooled platform that fits in a jacket pocket, runs on a USB-C power bank, and can be left unattended in a target environment for hours. Kali Linux ARM64 images ship directly from Offensive Security and run natively on the Pi 4 and Pi 5 without emulation, giving you the full toolset: Aircrack-ng, Kismet, Wireshark, Bettercap, and the rest of the standard Kali metapackages.

The number-one stumbling block is the driver. The RTL8812AU chipset inside the AWUS036ACH is not in the mainline kernel, which means you cannot plug the adapter in and expect it to work. You must compile the driver against your running ARM64 kernel — and the compilation flags differ from x86-64. This guide walks you through every step.

---

## Recommended Hardware

Not every combination of Pi model, adapter, and power supply works reliably. The table below reflects what is known to work well and what trade-offs to expect.

| Component | Recommended | Notes |
|---|---|---|
| Single-board computer | Raspberry Pi 5 (4 GB or 8 GB) | Pi 4 (4 GB+) works well; Pi 3B+ is too slow for real-time captures |
| Primary adapter | ALFA AWUS036ACH | RTL8812AU chipset; best ARM driver support; dual-band AC1200 |
| Alternative adapter | ALFA AWUS036ACM | MT7612U chipset; in-kernel driver (mt76x2u); plug-and-play on Kali ARM64 |
| WiFi 6 adapter | ALFA AWUS036AXM or AXML | MT7921AUN chipset; kernel-native since 5.18; needs firmware-misc-nonfree |
| USB hub | Powered USB 3.0 hub | AWUS036ACH draws ~500 mW; can brown out Pi USB ports without hub |
| Storage | MicroSD 32 GB+ (Class 10 / A2) | A2-rated cards give noticeably faster boot and apt operations |
| Power supply | Official Pi USB-C PSU (≥ 3 A) | Third-party adapters are a common source of stability problems |

{{< alert "triangle-exclamation" >}}
The AWUS036ACH is a high-current USB device. Plugging it directly into a Raspberry Pi 4 or Pi 5 without a powered USB hub can cause the Pi to throttle or restart under load. Always use a powered hub when running the AWUS036ACH alongside other USB peripherals.
{{< /alert >}}

---

## Installing Kali Linux ARM64 on Raspberry Pi

### Download the ARM Image

Kali Linux maintains first-party ARM64 images for Raspberry Pi at [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm). Download the image labelled **Raspberry Pi 4 (64-bit)** or **Raspberry Pi 5 (64-bit)**. Do not use the 32-bit image — the ARM64 kernel is required for the driver build steps in this guide.

### Flash to MicroSD

You can flash with either the Raspberry Pi Imager GUI tool or `dd` from the command line:

```bash
# Replace /dev/sdX with your actual SD card device (check with lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

With Raspberry Pi Imager, select **Use custom** → choose the Kali `.img.xz` file → select your SD card → write.

### First Boot and Initial Setup

Insert the SD card, connect to a monitor and keyboard (or set up headless access first with a serial console), and power on. Default credentials are:

- **Username:** `kali`
- **Password:** `kali`

After logging in, run `kali-tweaks` and follow the prompts to harden the default configuration. Then update the system fully before touching any drivers:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
If you plan to access the Pi over SSH rather than with a keyboard and monitor, enable SSH before first boot by placing an empty file called `ssh` in the `/boot` partition of the SD card. This is the same mechanism as standard Raspberry Pi OS.
{{< /alert >}}

---

## Installing RTL8812AU Driver on Kali ARM64 (AWUS036ACH)

The RTL8812AU driver is not included in the mainline Linux kernel. On ARM64 you must either compile from source or install the Kali-packaged DKMS version. Both paths are covered below — start with the package approach and only fall back to the manual build if you encounter kernel version mismatches.

### Option 1: Kali Package (Recommended Starting Point)

Kali Linux ships a DKMS-packaged version of the RTL8812AU driver that handles recompilation automatically whenever the kernel updates.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

After installation, reboot and verify the module loaded:

```bash
sudo modprobe 88XXau
ip link show
```

If you see a `wlan1` interface (assuming `wlan0` is the Pi's built-in adapter), the driver is working. This package may lag behind the GitHub source by a few weeks, but it is the lowest-friction starting point.

{{< alert "circle-info" >}}
The Kali package is typically sufficient for most ARM64 setups. Only proceed to the manual build below if the DKMS package fails to compile against your current kernel version, which you can check with `uname -r`.
{{< /alert >}}

### Option 2: Manual Build from Source (ARM64)

If the DKMS package fails — most commonly because your kernel is newer than the package's last tested version — build directly from the Aircrack-ng fork on GitHub. This is the authoritative source for ARM64 support.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Switch platform flags from x86 to ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

The `sed` commands are the critical difference from an x86-64 build. Without them, the Makefile defaults to x86 platform paths and the resulting module will not load on ARM64.

After a successful build, load the module and verify:

```bash
sudo modprobe 88XXau
ip link show
```

You should see a new interface — typically `wlan1` — listed. If `ip link show` shows the interface, the driver is working correctly.

---

## MT7921AUN on Raspberry Pi (AWUS036AXM / AXML)

The MediaTek MT7921AUN chipset used in the AWUS036AXM and AXML adapters has been in the mainline kernel since version 5.18. Kali Linux ARM64 images ship with a kernel well above that threshold, which means the driver loads automatically when you plug the adapter in — no compilation needed.

The only additional step is installing the closed-source firmware blob that the MT7921AUN requires:

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

After rebooting, verify the adapter is detected and the interface is up:

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

If `lsusb` shows a MediaTek device and `ip link show` lists a new wireless interface, the adapter is ready. Monitor mode support on the MT7921AUN has improved significantly since kernel 5.18 but may be less reliable than RTL8812AU-based adapters for certain packet injection tests. For maximum compatibility with older pentesting workflows, the AWUS036ACH remains the stronger choice.

---

## Enabling Monitor Mode on Raspberry Pi

The Raspberry Pi has a built-in WiFi interface (`wlan0`). Keep it connected to your network for SSH access. Use the ALFA adapter (`wlan1`) exclusively for monitor mode and packet capture. Never put `wlan0` into monitor mode on a headless Pi — you will lose your SSH connection.

```bash
# Kill processes that conflict with monitor mode (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Enable monitor mode on the ALFA adapter interface
sudo airmon-ng start wlan1

# Verify monitor mode is active
sudo iwconfig wlan1mon

# Begin capturing on all channels
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` creates a new interface called `wlan1mon`. Always run subsequent tools against `wlan1mon`, not `wlan1`. You can confirm the interface name with `iwconfig` or `ip link show`.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Running `airmon-ng check kill` stops NetworkManager and wpa_supplicant. If you are connected over SSH through `wlan0`, this will also bring down your SSH session. For headless setups, connect via Ethernet or a second wired interface before running these commands, or use `tmux` so your session survives a disconnect.
{{< /alert >}}

To disable monitor mode and restore managed mode:

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## Portable Pentest Setup Tips

Getting the hardware working is only half the job. These practical choices make the difference between a stable field kit and a frustrating pile of cables.

**Network architecture:** Use `wlan0` (Pi's built-in WiFi) to maintain your management connection — SSH into the Pi from a laptop on the same LAN or hotspot. Dedicate `wlan1` (ALFA adapter) entirely to pentesting activity. Never mix the two roles.

**Headless operation:** Avoid connecting a keyboard, mouse, and monitor in the field. Configure SSH on first boot, and access everything through a terminal emulator on your laptop. `tmux` sessions persist across reconnects, which is invaluable when network conditions are unstable.

**Power:** Use the official Raspberry Pi USB-C power supply rated at 3 A minimum. For the AWUS036ACH, add a powered USB hub rated at 2.5 A or higher. A quality USB-C power bank (65 W+) can power the Pi, hub, and adapter simultaneously for 4–6 hours depending on load.

**Storage:** Write Kismet logs and capture files to a USB SSD rather than the MicroSD card. MicroSD cards have limited write cycles and degrade quickly under sustained logging workloads. A USB 3.0 SSD attached to the powered hub is faster and more durable.

**Enclosure:** Select a Pi case with open USB ports or cutouts that accommodate the powered hub. Aluminium cases with passive heatsink fins help manage thermals during sustained captures.

---

## Running Kismet on Raspberry Pi

Kismet is a passive WiFi scanner that runs as a background server and exposes a browser-based web UI. It is well-suited to headless Pi deployments: you leave the Pi running and check the web interface from any device on the same network.

```bash
sudo apt install kismet

# Launch Kismet using the ALFA adapter in monitor mode
kismet -c wlan1
```

{{< alert "circle-info" >}}
Kismet will place the interface into monitor mode itself if you pass the interface name directly. You do not need to run `airmon-ng start` before launching Kismet. Kismet manages the interface lifecycle internally.
{{< /alert >}}

Once running, access the Kismet web UI from any browser on your network:

```
http://raspberrypi.local:2501
```

On first run, Kismet prompts you to create an admin username and password. After logging in, you can view detected networks, associated clients, signal strength history, and GPS data if a GPS dongle is connected.

Kismet logs everything to `.kismet` database files in `~/.kismet/` by default. These can be exported later for analysis or upload to WiGLE.

---

## Use Case: Wardriving Setup

A Raspberry Pi running Kismet with an ALFA adapter and a GPS dongle is a complete, self-contained wardriving kit — smaller and cheaper than any dedicated wardriving appliance.

**Required components:**
- Raspberry Pi 4 or Pi 5
- ALFA AWUS036ACH
- USB GPS dongle (u-blox chipsets work well with Kismet)
- Powered USB hub
- USB-C power bank (65 W+, with pass-through charging)

**Setup steps:**

1. Install Kismet and the GPS packages:

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. Configure `gpsd` to read from your GPS dongle:

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. Start Kismet with GPS support:

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Mount the Pi, hub, adapter, and power bank in a bag or enclosure and place it in your vehicle. Access the Kismet web UI from your phone's hotspot or a tablet connected to the same WiFi network as the Pi.

Kismet logs capture GPS coordinates for every detected network. Export the `.kismet` database to WiGLE CSV format using `kismetdb_to_wigle` (included with Kismet) and upload to WiGLE for mapping.

{{< alert "triangle-exclamation" >}}
Always comply with local laws before conducting any network scanning activity. In many jurisdictions, wardriving with passive scanning only is legal; active probing or connecting to networks without authorisation is not. Know your local regulations.
{{< /alert >}}

---

## Further Reading

For the full RTL8812AU driver installation guide on desktop Kali Linux and Ubuntu, see the [Install ALFA Driver on Kali Linux & Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/) guide. If you are still deciding which adapter to buy, the [ALFA WiFi Adapter Buyer Guide 2026](/en/blog/alfa-wifi-adapter-buyer-guide-2026/) covers every current model with chipset details and use-case recommendations.
