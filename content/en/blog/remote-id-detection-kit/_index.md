---
title: "ALFA AWUS036ACH × Raspberry Pi: Standard Remote ID Drone Detection Kit Complete Guide (2026)"
description: "Build a legal passive Remote ID drone detection kit using the ALFA AWUS036ACH and Raspberry Pi. Covers ASTM F3411 standard analysis, hardware list, step-by-step setup, and a technical clarification of DJI OcuSync vs. standard RID."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "drone-detection", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Why is the AWUS036ACH the first choice instead of newer Wi-Fi 6/6E adapters?"
    answer: "Remote ID capture requires stable monitor mode and raw packet injection. The most mature community driver branch today is Realtek rtl88xxau (RTL8812AU / RTL8814AU). Wi-Fi 6/6E chipsets (MediaTek MT7921AUN, Realtek RTL8832BU) lack injection drivers in the mainstream penetration/sniffing toolchain and are effectively invisible for this use case. The AWUS036ACH is dual-verified by the community and this kit."
  - question: "Is the nRF52840 required?"
    answer: "For Wi-Fi Remote ID only (NAN / Beacon), no — the AWUS036ACH is sufficient. To capture Bluetooth 5 Long Range broadcasts simultaneously, you need the nRF52840 (flashed with sniffer firmware). We recommend including this module for full coverage."
  - question: "Can this kit decode DJI drones?"
    answer: "It handles DJI's standard Wi-Fi / BT Remote ID broadcasts. However, DJI's proprietary OcuSync DroneID is not part of the standard protocol — the ALFA adapter cannot decode it. You would need a separate SDR (ANTSDR / HackRF) with a Kismet plugin. Both can be deployed alongside each other."
  - question: "Which Raspberry Pi generation should I use?"
    answer: "Raspberry Pi 4 (2 GB+) offers the best balance. Pi 3B has been validated by the unix_rid_capture author in testing. Pi 5 also works (watch cooling and power). The Pi's built-in WiFi cannot reliably enter monitor mode — an external AWUS036ACH is required."
  - question: "Is passive reception legal?"
    answer: "Receiving publicly broadcast Remote ID information from drones is legal — equivalent to reading publicly available information. Active jamming, however, is strictly regulated and outside the scope of this kit."
---
> Yupitek Technical Team | Official ALFA Network Distributor, Taiwan

{{< tldr >}}
The Remote ID detection kit uses the **ALFA AWUS036ACH** adapter's monitor mode to passively receive the identity and position information that drones are legally required to broadcast — think of it as a "license plate reader" for the airspace. It gives site security managers a legal, low-cost situational awareness tool.
{{< /tldr >}}

---

## 1. Why You Need a Remote ID Detection Kit

Drone regulation worldwide has entered the "broadcast identity" era. Standards require drones to continuously broadcast the following information while in flight:

| Broadcast Field | Description |
|---|---|
| UAS / Operator ID | Serial number or registration code |
| Current position (lat, lon, altitude) | WGS-84 / barometric altitude |
| Velocity and heading | Horizontal / vertical speed |
| Operator position | Launch point or current location |

Broadcast uses two types of wireless carriers:

- **Bluetooth**: BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- **Wi-Fi**: NAN (Wi-Fi Aware, 2.4 / 5 GHz), Beacon (2.4 / 5 GHz)

For site managers at airports, industrial parks, prisons, and large events, **passively receiving these public broadcasts** (essentially seeing a drone's "tail number") is a compliant and low-cost approach to situational awareness — no active interference needed.

{{< alert "triangle-exclamation" >}}
**Legal note**: Every method described in this guide is **passive reception of publicly broadcast data**. Active jamming is strictly regulated in all jurisdictions and is neither part of this kit nor recommended.
{{< /alert >}}

---

## 2. Product Positioning: Lowest-Risk Open-Source Path

After evaluating multiple technical approaches, we chose a configuration centered on the **ALFA AWUS036ACH**:

- The AWUS036ACH uses the **Realtek RTL8812AU** chipset, dual-band 2.4 + 5 GHz (802.11ac), 2×2 MIMO, two detachable 5 dBi high-gain RP-SMA antennas, and ample USB 3.0 bandwidth.
- The community-maintained `rtl88xxau` driver provides stable **monitor mode** and **raw packet injection** — the prerequisite for capturing Wi-Fi RID Beacon / NAN frames.
- Crucially, the `sxjack/unix_rid_capture` README **explicitly states "Tested using an rtl8812au based WiFi dongle, an nRF52840 dongle and a Raspberry Pi 3B"**. The community has already done the hardware validation for us. Reproducing their architecture for a productized kit is the lowest-risk path.

---

## 3. Hardware List

| Item | Model / Spec | Role | Requirement |
|---|---|---|---|
| **Core adapter** | ALFA **AWUS036ACH** (RTL8812AU, dual-band 2.4/5 GHz, USB 3.0, dual 5 dBi RP-SMA antennas) | Wi-Fi Remote ID capture (monitor mode) | **Required** |
| Single-board computer | Raspberry Pi 4 (2 GB+ recommended; 3B / 5 also work) | Compute host | **Required** |
| Storage | microSD 16 GB+ (Samsung / SanDisk Endurance recommended) | System disk | **Required** |
| Bluetooth 5 capture | **nRF52840** USB Dongle (flashed with sniffer firmware, e.g., Nordic Sniffer) | BT5 Long Range Remote ID capture | Recommended (optional) |
| Power | 5 V / 3 A USB-C (official Pi PSU) | Power supply | **Required** |
| Network | Ethernet cable or WiFi credentials | Upload / management | **Required** |
| Antenna upgrade | ALFA **APA-M25** directional panel antenna | Extended receive range, ambient noise rejection | Optional |

> Note: The community `DroneAware` project originally specified the **AWUS036N (Ralink RT3070, 2.4 GHz single-band)**. This kit upgrades to the **AWUS036ACH (dual-band)** to cover both 2.4 GHz and 5 GHz **NAN and Beacon** Wi-Fi RID transmission methods — broader coverage and better future-proofing.

---

## 4. Software List

| Software / Package | Purpose | Source |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | Operating system (headless) | raspberrypi.com |
| **rtl88xxau driver** | RTL8812AU monitor / injection driver | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | `unix_rid_capture` build dependencies | APT |
| **opendroneid-core-c** | Open Drone ID message encode/decode C library (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Linux Wi-Fi / BT RID capture program (JSON output) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (optional) | One-click community real-time map integration | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR plugin (DJI path) | Decode DJI OcuSync DroneID (requires SDR hardware) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub Project Links

```text
# Core decode library (ASTM F3411 / EN 4709-002 message encode/decode)
https://github.com/opendroneid/opendroneid-core-c

# Linux capture program (this kit's main software, validated on rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Community real-time map network (one-click install, auto-uploads to droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Wireless detection framework (DJI OcuSync path requires SDR plugin)
https://github.com/kismetwireless/kismet

# RTL8812AU monitor / injection driver (required for AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. Step-by-Step Setup

### Step 1 — Flash the system

Use **Raspberry Pi Imager** to write **Raspberry Pi OS Lite (64-bit)**. Click the gear icon (advanced settings):

- Hostname: `droneid-kit`
- Enable SSH and set credentials
- Enter WiFi credentials (saves having to connect Ethernet later)

### Step 2 — Connect and verify hardware

Plug the AWUS036ACH directly into the Pi's **USB 3.0** port (blue / labeled `SS`). Make sure both antennas are tight. After boot, SSH in:

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

You should see:

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Step 3 — Install the rtl88xxau monitor driver

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Step 4 — Verify monitor mode

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

The output should show **`Mode:Monitor`**.

### Step 5 — Install build dependencies

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Step 6 — Build opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Produces libopendroneid/libopendroneid.so and test/odidtest
```

### Step 7 — Build unix_rid_capture

`unix_rid_capture` requires `opendroneid.c` / `opendroneid.h`. Copy them from the previous step:

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Step 8 — Run capture

Root privileges or `cap_net_raw` are required:

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Capture and save as JSON
```

Live UDP output (open another terminal):

```bash
nc -lu 32001
```

### Step 9 — Visualize flight paths (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # Generate .gpx
```

Open the .gpx file in Google Earth to see the drone's flight path. A typical detection JSON entry looks like:

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Step 10 — (Optional) Connect to the DroneAware community live map

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**Security note**: For any third-party `curl ... | sudo bash` script, we recommend downloading and reviewing it first: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. The installer auto-detects USB adapters, prompts for a node name, and guides you through droneaware.io registration. Detections appear on the live map in real time.
{{< /alert >}}

---

## 7. Important Technical Clarification: Standard RID vs. DJI OcuSync

This is where the expertise matters — make sure your customers understand the difference:

| Path | What It Covers | Hardware | Works with ALFA AWUS036ACH? |
|---|---|---|---|
| **Standard Remote ID** | ASTM F3411 Wi-Fi / BT broadcast | AWUS036ACH + nRF52840 | ✅ Yes (this article's main subject) |
| **DJI OcuSync DroneID** | DJI proprietary protocol (not standard Wi-Fi) | Full SDR (ANTSDR / HackRF / USRP) + Kismet `kismet_cap_antsdr_droneid` plugin | ❌ No |

- The ALFA AWUS036ACH is a **Wi-Fi band (2.4 / 5 / 6 GHz) receiver**. It handles standard RID completely.
- DJI's proprietary **OcuSync** DroneID does not use standard Wi-Fi protocols. **The ALFA adapter cannot decode it**. You need an SDR covering 2.4 / 5.8 GHz (e.g., ANTSDR E200) with the `alphafox02/antsdr_dji_droneid` + Kismet plugin.
- ⚠️ Note: **Standard RTL-SDR has a bandwidth ceiling of about 1.7 GHz** — it cannot see OcuSync at 2.4 / 5.8 GHz. You must choose an SDR that supports higher frequencies.
- The two paths are **complementary**: the ALFA adapter handles standard RID broadcast detection, while the SDR handles DJI's proprietary protocol — together forming a complete Counter-UAV / RF situational awareness front end.

---

{{< faq >}}

---

## Appendix: Glossary for Beginners

If you are new to drone regulation and counter-UAV technology, here is a quick plain-English reference for the terms used in this guide:

| Term | Plain Explanation |
|---|---|
| **Remote ID** | A drone's "digital license plate." Regulations require drones to continuously broadcast their identity, position, and other information so people on the ground — especially regulators — can see "whose drone that is and where it's going." |
| **ASTM F3411 / EN 4709-002** | The US and EU standards respectively for Remote ID broadcast specifications. They define what information must be broadcast and how it should be formatted, ensuring interoperability between different drone brands and detection equipment. |
| **Passive Detection** | Only "listening" to publicly broadcast messages. No active signals are transmitted to interfere with or attack the drone. Legally very different from active jamming. |
| **Monitor Mode** | A state where a WiFi adapter stops trying to connect to access points and instead "passively listens" to all radio packets in the air — the prerequisite for capturing Remote ID broadcasts. |
| **NAN (Wi-Fi Aware) / Beacon** | Two Wi-Fi frame formats drones use to broadcast Remote ID. This kit attempts to decode both. |
| **Bluetooth 5 Long Range** | In addition to Wi-Fi, some drones broadcast Remote ID over Bluetooth. An additional nRF52840 dongle is required to capture these. |
| **DJI OcuSync / DroneID** | DJI's proprietary video and telemetry transmission protocol. It is **not** standard Wi-Fi and is **not** the Remote ID protocol covered in this article. It requires completely different SDR hardware and plugins — see Section 7 for details. |
| **SDR (Software Defined Radio)** | A general-purpose radio receiver whose frequency range and demodulation methods can be configured in software. Devices like ANTSDR and HackRF can cover frequency bands that the ALFA adapter cannot reach (such as DJI OcuSync). |
| **RTL8812AU** | The Realtek chipset inside the ALFA AWUS036ACH. This chip determines whether the adapter supports monitor mode. |
| **GPX file** | A standard format for recording GPS coordinate tracks. You can open it directly in Google Earth and similar software to visualize a drone's flight path. |

> In one sentence: This guide teaches you how to turn an ALFA adapter into a "drone identity scanner" — passively receiving the public information that drones are legally required to broadcast. It is a legal method for site security management.

---

## References

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture (rtl8812au + nRF52840 + RPi validated)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Community Remote ID detection network](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Wireless detection framework](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR decoder](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux monitor/injection driver](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH product page (Yupitek)](https://yupitek.com/en/products/alfa/awus036ach/)
8. [Contact and ordering (Yupitek)](https://www.yupitek.com/en/contact/)

---

*This article was compiled by the Yupitek technical team. AWUS036ACH and related hardware are available through Yupitek with authorized distribution and technical support.*
