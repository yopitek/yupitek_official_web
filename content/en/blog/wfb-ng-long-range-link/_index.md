---
title: "DIY Long-Range Digital FPV & Telemetry Link with ALFA AWUS036ACH and wfb-ng (2026)"
description: "Build a low-latency, encrypted long-range digital video and MAVLink telemetry link using the ALFA AWUS036ACH adapter and open-source wfb-ng. Complete hardware list, Raspberry Pi setup guide, and power supply troubleshooting."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "drone-video-link", "digital-FPV", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "long-range-video", "telemetry-link"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "What makes wfb-ng different from regular WiFi?"
    answer: "Standard WiFi requires association handshakes and ACK confirmations, which perform poorly over long distances. wfb-ng bypasses 802.11 connection overhead by using raw packet injection with FEC forward error correction, keeping end-to-end latency down to tens of milliseconds."
  - question: "Why does the onboard ALFA adapter need its own power supply?"
    answer: "The AWUS036ACH draws significant current during TX bursts. Plugging it directly into a Raspberry Pi USB 2.0 port causes voltage drops that reset the adapter, drop the link, or corrupt packets. Use a dedicated 5V BEC, and add a 470µF low-ESR capacitor across +5V and GND for filtering."
  - question: "I have a connection but no video or telemetry — what now?"
    answer: "The most common cause is a key mismatch — verify that drone.key on the aircraft matches gs.key on the ground station. Also confirm wifi_channel and link_domain match on both ends. Run journalctl -xu wifibroadcast@gs to inspect real-time logs."
  - question: "Do I have to use the ALFA AWUS036ACH for wfb-ng?"
    answer: "Any RTL8812AU-based adapter should work theoretically, but the AWUS036ACH is the hardware the wfb-ng project officially tests against. Its driver support is the most stable, especially for high-power, long-range scenarios where ALFA's power design and detachable antennas give a clear advantage."
---
> Author: Yupitek Technology Team (Official ALFA Network Distributor, Taiwan)
> Audience: Drone enthusiasts, makers, security researchers, agri-spray and inspection UAV developers
> Difficulty: ★★★☆☆ (requires basic Linux and flight controller knowledge)

{{< tldr >}}
wfb-ng is an open-source project that turns WiFi adapters with monitor mode support — like the **ALFA AWUS036ACH** — into purpose-built long-range radios for drones. It lets you build a low-latency, encrypted video and MAVLink telemetry link using off-the-shelf hardware.
{{< /tldr >}}

---

## 1. Why Build a Digital FPV Link with an ALFA Card?

If you have used analog FPV (5.8 GHz analog video), you know the drill: signal obstruction turns the screen into snow, range drops fast, and **anyone with a receiver can watch your feed** — no encryption, no telemetry return channel.

Over the past year, our team has set up links for agri-spray operators, inspection teams, and security training clients. One question kept coming up: **Can I use a common ALFA USB adapter with open-source software to build a digital, encrypted, long-range link that carries both video and telemetry?**

The answer is yes — and it is simpler than you might think.

Compared to traditional analog FPV, running the open-source **wfb-ng** on an ALFA adapter gives you several decisive advantages:

- **Low latency**: Raw WiFi injection bypasses 802.11 ACK and handshake overhead. End-to-end delay drops to tens of milliseconds — FPV feel is close to analog.
- **Digital encryption**: Video and telemetry packets use libsodium encryption. Even if someone captures the signal, they cannot decode your feed or flight data.
- **One link, multiple streams**: A single adapter on one frequency handles:
  - Live video (RTP / RTSP)
  - MAVLink telemetry (bidirectional, flight controller ↔ ground station)
  - A TCP/IP tunnel (for VPN, SSH, or file transfer)
- **TX diversity**: Multiple adapters can work together for transmit diversity, improving obstruction resistance.
- **Open source, fully customizable**: The ALFA AWUS036ACH combined with wfb-ng costs a fraction of commercial digital FPV systems (DJI O3, Walksnail, etc.) — and every line of code is open.

{{< alert "circle-info" >}}
This guide is not about replacing DJI's stock FPV system. It is a practical open-source path for anyone who wants to **own their link, build secondary redundancy, or create custom payloads**.
{{< /alert >}}

---

## 2. What This Is: wfb-ng Explained

**wfb-ng** (Wireless Fibre / WiFi Broadcast – next generation) is an open-source digital FPV and telemetry project with a clever core idea:

> It does not use WiFi as a "network." It uses WiFi as a "radio."

Standard 802.11 was designed for local area networking — association, ACK, retransmission. Over long distances, with moving vehicles and weak signals, that overhead becomes a liability. wfb-ng takes a different approach with **raw WiFi injection**:

- The adapter enters **monitor mode** — it does not "connect" to anything.
- Raw WiFi frames are injected directly. **No ACK, no retransmission** (FEC forward error correction handles packet loss).
- This bypasses the range and latency limits of standard 802.11, pushing distance and stability to the hardware's physical limit.

In simple terms: it turns a common USB adapter into a pair of "digital radios" that can carry RTP video, MAVLink telemetry, and even an IP tunnel.

- Project homepage (GitHub): https://github.com/svpcom/wfb-ng.git
- Widely used in the PX4 / ArduPilot ecosystem for DIY digital FPV. Active community, and a common open-source link in the Ukrainian drone community.

---

## 3. The Star: ALFA AWUS036ACH

The "radio" of this link is the **ALFA AWUS036ACH**.

It uses the **Realtek RTL8812AU** chipset with **802.11ac (WiFi 5)**, **dual-band 2.4 GHz / 5 GHz**, USB 3.0 Type-C, and detachable RP-SMA antennas. Critically, **wfb-ng's official test hardware runs AWUS036ACH on both ends at 5 GHz**. This adapter is the model the project author validated for the most stable driver support.

Three reasons it stands out:

1. **Enough power**: ALFA's signature high-power design, combined with external high-gain antennas, delivers far better long-range performance than any laptop internal card.
2. **Monitor mode + injection**: With the patched driver (detailed below), RTL8812AU reliably supports monitor mode and raw packet injection — the prerequisite for wfb-ng.
3. **Universal and durable**: USB form factor works on both the air and ground ends. No need to buy different adapters for different machines. If one fails, swap in another.

{{< alert "triangle-exclamation" >}}
**Note**: wfb-ng requires a **patched driver** (e.g., `rtl88xxau_wfb`). The stock Linux kernel driver cannot enter the injection mode wfb-ng needs. Installation instructions are covered in the Software List and Step-by-Step sections below.
{{< /alert >}}

---

## 4. Hardware List

The link splits into **Drone (airborne)** and **Ground Station** sides.

### Drone (Airborne)

| Item | Recommended Model / Notes |
|---|---|
| Onboard computer | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (for 1080p, use **Pi 4 or Zero 2 W**) |
| Camera | Raspberry Pi Camera (CSI) or Logitech C920 (USB) |
| WiFi adapter | **ALFA AWUS036ACH** (or any RTL8812AU-based adapter) |
| Power supply | **5V BEC** (dedicated power for the adapter — see troubleshooting note) |
| Filter capacitor | **470µF low-ESR capacitor** (across adapter +5V and GND) |
| Flight controller | Pixhawk or similar (MAVLink over UART to onboard computer) |

### Ground Station

| Item | Recommended Model / Notes |
|---|---|
| Computer | Linux machine (Ubuntu / Debian x86-64), or another Raspberry Pi |
| WiFi adapter | **ALFA AWUS036ACH** |
| Monitoring software | Machine running **QGroundControl** (can be the same as the ground station computer) |

> Note: For **receive-only (RX)** setups, any adapter that supports monitor mode will work — even a router flashed with OpenWRT. But the official tested setup and this guide use the AWUS036ACH.

---

## 5. Software List

### Operating System

- **Raspberry Pi OS** / **Debian** / **Ubuntu** (Linux kernel ≥ 4.x)

### Core Projects

- **wfb-ng** (svpcom/wfb-ng): digital FPV / telemetry main program
- **Patched driver**:
  - RTL8812AU → `svpcom/rtl8812au` (branch **v5.2.20**, install via dkms)
  - RTL8812EU → `svpcom/rtl8812eu`
  - After loading, the adapter appears as `rtl88xxau_wfb` (or `rtl8812eu`)

### System Dependencies

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### Encryption

- **libsodium**: Use `wfb_keygen` to generate `drone.key` (airborne) and `gs.key` (ground station)

### Ground Station Playback

- **QGroundControl**: monitor flight controller status and telemetry
- **GStreamer / RTSP**: receive and play live video from the airborne end

---

## 6. GitHub Links and ALFA AWUS036ACH Spec Sheet

### Official Links

| Item | Link |
|---|---|
| wfb-ng project | https://github.com/svpcom/wfb-ng.git |
| Patched driver (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| Patched driver (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH product page | https://yupitek.com/en/products/alfa/awus036ach/ |
| PX4 WFB-ng tutorial | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH Spec Sheet

| Spec | Detail |
|---|---|
| Chipset | Realtek **RTL8812AU** |
| Wireless standard | 802.11a / b / g / n / **ac (WiFi 5)** |
| Frequency | **2.4 GHz + 5 GHz** dual-band |
| Interface | USB 3.0 **Type-C** |
| Antenna | 2 × detachable **RP-SMA** (2T2R MIMO) |
| Monitor mode | Supports monitor mode + packet injection (requires wfb-ng patched driver) |
| wfb-ng driver | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| Status | wfb-ng **officially tested adapter** (5 GHz on both ends) |

---

## 7. Step-by-Step Setup

This section has four parts. **Path A (Raspberry Pi Quick Start)** is the most recommended — nearly a burn-and-go experience. **Path B** is for manual x86 Linux ground station installation. **Paths C and D** cover key pairing and configuration; both paths use those.

### A. Raspberry Pi Quick Start (Recommended)

wfb-ng provides pre-built Raspberry Pi images. Flash one for the drone and one for the ground station — boot and they work.

**1. Download and flash the image**

Go to the wfb-ng GitHub **Releases** page, download the latest `*.img.gz`, extract it, and flash it to **two** SD cards (one for the drone, one for the ground station).

```bash
# Extract the image (filename varies by release)
gunzip wfb-ng-*.img.gz
# Flash to SD card using Raspberry Pi Imager, dd, or balenaEtcher
```

**2. Insert the adapter, boot, and SSH in**

Plug an ALFA AWUS036ACH into both boards, power on, and SSH in (default IP and credentials below):

```bash
ssh pi@192.168.0.111
# Password: raspberry
```

**3. Enable Ground Station services**

On the **ground station Pi**, run:

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. Enable Drone services**

On the **drone Pi**, run:

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. Monitor link status from the ground station**

```bash
wfb-cli gs
```

> When you see connection, channel, and packet loss information, the link is up. Open QGroundControl to access telemetry and video.

---

### B. Debian / Ubuntu Ground Station Manual Installation

If you are using an x86-64 Linux desktop or laptop as the ground station, install manually.

**1. Install dkms and the patched driver**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. Verify the adapter is using the wfb-ng driver**

```bash
# Should show wlan0 with MTU 2312
ifconfig

# Driver name should be rtl88xxau_wfb (RTL8812AU) or rtl8812eu (RTL8812EU)
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
If `ethtool -i wlan0` shows plain `rtl8812au` instead of `rtl88xxau_wfb`, the patched driver was not installed correctly and wfb-ng will not be able to enter injection mode. Re-check the dkms installation for errors.
{{< /alert >}}

**3. Run the official auto-install script**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. Monitor the link**

```bash
wfb-cli gs
```

---

### C. Key Pairing

wfb-ng video and telemetry are encrypted. The airborne and ground station ends must use **matching keys** to communicate.

```bash
# Generate keys (do this on the drone side, then distribute)
wfb_keygen

# Place drone.key on the drone
# Place gs.key on the ground station
# Both must match — otherwise the link shows "connected" but no data
```

> If you used **Path B's auto-install script (install_gs.sh)**, it generates and configures keys automatically. For manual installation, make sure `drone.key` and `gs.key` belong to the same pair.

---

### D. Key Configuration File: /etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` is wfb-ng's core configuration file. These are the parameters you will most likely need to adjust:

```ini
[common]
# Channel 165 = 5825 MHz (5.8 GHz band)
wifi_channel = 165

# Set the country code to 'BO' (Bolivia) to unlock maximum TX power
wifi_region = 'BO'

[drone]
# link_domain MUST be identical on both drone and ground station
link_domain = "my_wfb_link_01"

[drone_mavlink]
# Receive MAVLink from the flight controller UART (set UART to 1500000 baud)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Same as above — must match the drone
link_domain = "my_wfb_link_01"
```

**Three most common pitfalls:**

1. **`wifi_channel` must match on both ends**: This guide uses 165 (5825 MHz, 5.8 GHz). Set it the same on both drone and ground station.
2. **`link_domain` must match on both ends**: This is the link identifier. Different values means no connection.
3. **Flight controller UART baud rate must be 1500000**: `peer = 'serial:ttyS0:1500000'` requires the flight controller UART to be set to 1500000 baud, or MAVLink will not work.

{{< alert "triangle-exclamation" >}}
**Note**: `wifi_region = 'BO'` unlocks maximum TX power, but **this does not mean it is legal in your location**. Check the regulatory notice below.
{{< /alert >}}

---

## 8. Practical Notes and Common Pitfalls

This section covers issues we actually hit during real deployments. Read it.

### Pitfall 1: Insufficient Adapter Power Causes Port Resets and Packet Drops

The AWUS036ACH draws **significant current during TX bursts**. Plugged into a Raspberry Pi standard USB 2.0 port, the Pi's USB power cannot sustain the peak draw. Result: **adapter port resets, link drops, packet corruption, frozen video**.

Solution (mandatory on the drone side):

- Power the adapter **directly from a 5V BEC** (not from the Pi's USB). Connect the BEC output to the adapter.
- Add a **470µF low-ESR capacitor across +5V and GND** at the adapter to absorb TX current spikes.
- On the ground station side, a **laptop USB 3.0 port with the original USB 3.0 cable** usually provides enough power — no extra BEC needed.

> This single step determines whether your link is stable. We have seen countless cases of packet loss traced back to poor power delivery.

### Pitfall 2: Encryption Errors / No Connection

If `wfb-cli gs` shows "connected" but **there is no video or telemetry**, the causes are almost always:

- **Key mismatch**: Verify `drone.key` on the drone matches `gs.key` on the ground station.
- **Channel or link_domain mismatch**: Both ends must have identical `wifi_channel` and `link_domain` settings.

Debug command:

```bash
# Check ground station service logs for encryption / connection errors
journalctl -xu wifibroadcast@gs
```

### Pitfall 3: Regulatory Compliance (Important)

This link transmits radio waves. It is a wireless transmission device.

- **Verify that your local regulations permit this type of WiFi transmission at the power level and frequencies you plan to use.**
- Taiwan, China, the EU, and the US each have their own rules for 5.8 GHz ISM band TX power, available channels, and "non-association" transmission.
- Setting `wifi_region = 'BO'` unlocks the hardware power ceiling, but **it does not make it legal in your country**. Adjust channels and power to comply with local radio regulations.
- Use only in authorized environments (private farmland, closed test ranges, training facilities). Do not interfere with other communications.

---

## 9. Conclusion

With a single ALFA AWUS036ACH and the open-source wfb-ng project, we built a link that delivers:

- **Cost advantage**: Total BOM cost is far below any commercial digital FPV solution.
- **Open source**: Every line of code, every driver, every configuration is publicly available.
- **Fully customizable**: Channels, power, encryption keys, MAVLink routing — all under your control.
- **Long range**: Digital video and telemetry on one link, 5 GHz field-tested range well beyond analog, with encryption and obstruction resistance.

For agri-spray, inspection, security training, or anyone who wants to understand how digital FPV really works under the hood, this is a path worth walking.

Our team will continue sharing ALFA adapter drone-link implementation notes on this blog. If you run into issues during setup, feel free to reach out — **hands-on building is the fastest way to learn**.

---

{{< faq >}}

---

## Appendix: Glossary for Beginners

If this is your first time with drone link technology, here is a quick plain-English reference for the terms used in this guide:

| Term | Plain Explanation |
|---|---|
| **FPV** (First Person View) | A live camera feed from the drone to a screen or goggles on the ground — like sitting in the pilot's seat. |
| **Digital FPV vs Analog FPV** | Analog is like old TV: weak signal means snow and anyone can tune in. Digital encodes video into data packets — it can be encrypted, handles interference better, but requires more complex hardware and setup. |
| **Monitor Mode** | Normal WiFi adapters only connect to access points. Monitor mode makes the adapter listen to (and transmit) raw radio signals without associating to anything — the foundation of this guide. |
| **Packet Injection** | Under monitor mode, you can inject custom radio frames directly into the air without going through normal WiFi connection procedures. wfb-ng uses this mechanism to send video and telemetry. |
| **wfb-ng** | Open-source software that repurposes a WiFi adapter as a drone-specific radio link rather than a general network adapter. The core software in this guide. |
| **FEC (Forward Error Correction)** | The transmitter sends extra redundant data. If some packets are lost in the air, the receiver reconstructs the original data from the redundancy — no need for retransmission (which would be too slow over long, fast-moving links). |
| **MAVLink** | The common protocol that drone flight controllers (Pixhawk, etc.) use to talk to ground stations — carrying flight status, commands, and telemetry data. |
| **RTP / RTSP** | Standard protocols for streaming live video over a network. Your IP camera and security system likely use the same kind of protocol. |
| **libsodium Encryption** | The open-source crypto library used in this guide to encrypt video and telemetry. Only the paired drone and ground station can decrypt the content. |
| **TX Diversity (Transmit Diversity)** | Using multiple adapters to transmit the same data simultaneously. If one adapter's signal is blocked, another one covers it — like a dual-redundancy system. |
| **BEC (Battery Eliminator Circuit)** | A voltage regulator module that steps the drone battery voltage down to the 5 V the adapter needs, handling the high current spikes without power dips that could drop the link. |
| **RTL8812AU** | The Realtek chipset inside the ALFA AWUS036ACH. This chip determines whether the adapter supports monitor mode and packet injection. |

> In one sentence: wfb-ng turns the ALFA adapter into a dedicated drone radio station, letting video and flight data travel long distances over an open-source, encrypted link — your own private channel.

---

## References

- **wfb-ng project (svpcom/wfb-ng)**: https://github.com/svpcom/wfb-ng.git
- **ALFA AWUS036ACH product page**: https://yupitek.com/en/products/alfa/awus036ach/
- **Patched driver (RTL8812AU)**: https://github.com/svpcom/rtl8812au
- **Patched driver (RTL8812EU)**: https://github.com/svpcom/rtl8812eu
- **PX4 WFB-ng tutorial**: https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*This article was written by the Yupitek technical team (official ALFA Network distributor, Taiwan), based on wfb-ng official documentation and hands-on implementation experience. Before building this link, verify your local radio regulations and adjust TX power and frequencies accordingly.*
