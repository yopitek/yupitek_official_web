---
title: "AWUS036AXER Hands-On Report: The Strongest-Receiving Wi-Fi 6 Adapter on ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER on ASUS GX10 / Ubuntu 24.04 ARM64, driver-free (rtw89_8852bu): 60-second monitor scan caught 63 APs + 12 clients, 73% injection (2.4G), and both 5G VHT80 AP and WPA3 passed."
faq:
  - question: "Does AWUS036AXER need a separate driver on Ubuntu 24.04 or Kali?"
    answer: "On Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia), no: the in-kernel rtw89_8852bu driver recognizes it on plug-in, with no compilation and no DKMS (firmware rtw8852b_fw 0.29.29.5). Our platform is Ubuntu, not the Kali distribution, so Kali itself was not tested; common Kali tools airmon-ng, kismet, bettercap, wifite, and Wireshark all work on this platform. On older kernels the in-kernel driver is not guaranteed, so check your version first."
  - question: "Does AWUS036AXER support monitor mode? How strong is its reception?"
    answer: "Yes, it enters monitor on both 2.4 GHz and 5 GHz. In our own office we ran a 60-second channel-hopping airodump-ng scan and caught 63 APs and 12 clients, the strongest reception of the nine adapters we tested side by side; the same-chip AWUS036AX caught 14 APs + 4 clients in a separate test (two non-simultaneous measurements, for reference only)."
  - question: "Can AWUS036AXER do packet injection?"
    answer: "Yes. On 2.4 GHz, aireplay-ng --test gave a 73% response rate (22/30) and showed Injection is working!; 5 GHz passed per-AP self-tests as well. We completed handshake capture and exported .22000 on our own network and our own devices. For near-100% on both bands, our testing found AWUS036EACS, ACH, and ACS more consistent. Only on networks you own or are authorized to test."
  - question: "What's the difference between AWUS036AXER and AWUS036AX?"
    answer: "Both use the Realtek RTL8832BU and the same rtw89_8852bu driver, with identical mode support and injection behavior on this platform; the difference is in antenna tuning and gain, which drives reception (AXER: 63 APs + 12 clients in 60s; AX: 14 APs + 4 clients). Both use embedded antennas with no RP-SMA; refer to the product page for antenna specs."
  - question: "Can AWUS036AXER run as an AP or use WPA3? Which modes are unsupported?"
    answer: "Yes. Both 2.4 GHz 802.11n and 5 GHz VHT80 (VHT-NSS2, 351 Mbit) saw an iPhone connect and reach authorized; WPA3-SAE with sae_pwe=0 let an iPhone 15 Pro connect (on 2.4 GHz; 5 GHz WPA3 was not tested); concurrent STA + AP works. However, rtw89_8852bu does not support active monitor, IBSS, or mesh."
draft: false
---

{{< tldr >}}On ASUS GX10 / Ubuntu 24.04 ARM64, AWUS036AXER is plug-and-play (in-kernel rtw89_8852bu); a 60-second monitor scan caught 63 APs + 12 clients, 2.4 GHz injection hit 73%, and both AP and WPA3 passed; active monitor, IBSS, and mesh are unsupported.{{< /tldr >}}

> This article is Yopitek's (ALFA's Taiwan distributor) product-compatibility and capability testing on our own equipment.
> Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. The test environment was our own office Wi-Fi (SSID `YUPITEK`), against our own test phone, an iPhone 7 Plus (WPA3 separately tested with an iPhone 15 Pro).
> ⚠️ **Legal use**: Monitor and injection are limited to networks and devices you own or are authorized to test; for AP mode, follow your local radio regulations. This article focuses on adapter capability, compatibility, configuration, and selection, and does not cover any attack operations against third-party networks.

---

## 1. This Adapter and the Test Platform

AWUS036AXER is ALFA's Wi-Fi 6 (802.11ax) 2x2 USB adapter built on the Realtek RTL8832BU chipset (no Bluetooth). It uses the **same chip and the same driver** (`rtw89_8852bu`) as ALFA's AWUS036AX, with identical mode support and behavior on this platform; the real difference between them is **antenna tuning and gain**, not external versus internal — the AXER uses an **embedded (Nano) antenna design with no RP-SMA**, relying on the chip and RF tuning to push reception to the maximum. Keep the core conclusion of this article in mind up front: among the nine ALFA adapters we compared side by side, the AXER has **the strongest reception of the lot**.

The test platform is an ASUS GX10 with the NVIDIA GB10 superchip and 128GB of unified memory, running Ubuntu 24.04 LTS, ARM64 (aarch64), kernel `6.17.0-1014-nvidia`. All results were produced on this machine on 2026-11-18; the test device was our own iPhone 7 Plus (WPA3 separately tested with an iPhone 15 Pro), and the test network was our own office Wi-Fi. For distributor validation, ARM64 paired with a recent kernel is a relatively demanding combination; Section 2 below explains why this generation is actually less work.

A bit of spec context: the AXER is a 2x2 (dual spatial stream) Wi-Fi 6 adapter that can transmit and receive two spatial streams simultaneously, which also corresponds to the VHT-NSS2 negotiated in the 5 GHz AP test later. But what won this round for this adapter is the antenna design and RF tuning, not the stream count (the AX is also 2x2). With the chip, driver, and platform all identical, antenna tuning is nearly the only variable, so the reception gap between the AXER and the AX can be cleanly attributed to the embedded antenna design and gain tuning.

---

## 2. Hardware and Driver (Embedded Antenna, No Driver Install)

On Ubuntu 24.04's 6.17 kernel, AWUS036AXER is **recognized on plug-in, with no compilation and no DKMS**. The `rtw89_8852bu` driver is already an in-kernel module, with firmware `rtw8852b_fw` (version 0.29.29.5) loaded at boot, so there's no need to pull an out-of-tree project from GitHub or bind to DKMS. For distribution and teaching environments that need long-term maintenance across many kernel updates, dropping the driver-compile step removes one of the most common points of failure.

The contrast with the old path makes it hit home: Realtek USB chips like this historically did not make it into the mainline kernel, so users had to pull an out-of-tree project from GitHub (for example `morrownr/USB-WiFi`) and compile it against the current kernel with DKMS, rebuilding on every kernel update — and the moment a compile failed, the adapter simply vanished. Now that rtw89 is officially in-kernel, these steps can be skipped entirely on 6.17, and the same procedure can be reused across multiple adapters sharing the driver.

First confirm the adapter is recognized correctly:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

The USB ID in normal WLAN mode is `0bda:b832`. If you see `0bda:1a2b` instead, the adapter is still stuck in "CD-ROM mode"; running `sudo usb_modeswitch -v 0bda -p 1a2b -K` once switches it to WLAN mode. Our unit enumerated directly in WLAN mode and did not hit CD-ROM mode.

The interface name uses `wlx` + MAC naming (for example `wlxAABBCCDDEEFF`), which stays the same on whatever machine it's plugged into, making it easy to pin in scripts. To query which modes this adapter supports:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

The modes reported in testing were managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO. There's no IBSS, no mesh, and no active monitor here; this is an inherent limitation of the rtw89 driver, honestly spelled out in Section 4, so don't misjudge it during selection.

On antennas: the AXER uses an embedded (Nano) antenna design with no RP-SMA, and compared to the same-chip AX, the difference lies in antenna tuning and gain, which shows up most directly as reception. The monitor data in the next section makes this clear.

---

## 3. Measured Capabilities

The three core capabilities (Monitor / Injection / AP) plus the WPA3 results are listed first in a table, with details expanded item by item below:

| Capability | 2.4 GHz | 5 GHz | Measurement highlight |
|---|---|---|---|
| **Monitor** | ✅ Strong | ✅ Strong | Channel-hopping scan caught **63 APs + 12 clients**, strongest reception of the nine |
| **Injection** | ✅ 73% | ✅ Works | 2.4G `22/30 73%`; 5G `Injection is working!` |
| **AP** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone connected; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | Not tested | AP side, iPhone 15 Pro connected (`sae_pwe=0`); tested on 2.4 GHz only |
| **WPA handshake capture** | ✅ End-to-end | — | Own network + own device, 4-way (M1–M4) → `.22000` |

### 3-1. Monitor (The Highlight: Strongest Reception)

Switching to monitor is the standard `iw` flow: hand the interface back to yourself (`nmcli dev set $IF managed no`), bring the interface down, set the monitor type, bring it up, and set the channel:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; use channel 6 for 2.4 GHz
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

Both 2.4 GHz and 5 GHz filled 100 frames within 6 seconds each. What really opened up the gap was the channel-hopping scan: `sudo airodump-ng --band abg $IF` run for 60 seconds **caught 63 APs plus 12 clients**. That's the most targets captured by any of the nine adapters this round, directly reflecting the reception advantage from the embedded antenna design and RF tuning. For site surveys, long-range monitoring, or weak-signal environments, this reception capability is the AXER's core value.

### 3-2. Injection

Injection was validated with aireplay-ng's self-test mode, which tests the adapter's own capability, not an attack against anything external:

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

The 2.4 GHz response rate was 73% (22/30), judged usable. On 5 GHz, per-AP self-tests against a specified AP also reported `Injection is working!`. One platform-wide rule to add: **before transmitting/injecting on 5 GHz, first run `iw reg set US` to unlock TX power, and remember to run `iw reg set TW` afterward to return to Taiwan's regulatory band**.

### 3-3. AP Mode (2.4 GHz 802.11n, 5 GHz VHT 80 MHz)

The AXER can bring up a hostapd AP on both bands. On 2.4 GHz, `hw_mode=g` + `ieee80211n=1` brings up an 802.11n hotspot, and the iPhone 7 Plus connected, negotiating MCS 15 and reaching authorized. On 5 GHz, `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` brings up a VHT 80 MHz hotspot, and the iPhone 7 Plus connected, negotiating **VHT-NSS2, 80 MHz, 351 Mbit, authorized**. The prerequisite for bringing up an AP is `sudo nmcli dev set $IF managed no`, and `wpa_passphrase` must be at least 8 characters, or hostapd returns `invalid WPA passphrase length`.

### 3-4. WPA3-SAE and Handshake Capture

For WPA3-SAE, set `wpa_key_mgmt=SAE`, `ieee80211w=2`, and `sae_pwe=0` on the AP side; an iPhone 15 Pro connected in testing. **`sae_pwe` is a compatibility minefield across this batch of ALFA adapters**: some devices can't connect when `sae_pwe=2` (Hash-to-Element), and setting `sae_pwe=0` restores compatibility with older iPhones.

The handshake capability was validated end-to-end on **our own office Wi-Fi (YUPITEK) plus our own test devices**: a complete 4-way (M1/M2/M3/M4) was captured and then converted with `hcxpcapngtool` into a hashcat-readable `.22000`. One GX10-platform-wide phenomenon to call out here: **`hcxdumptool` fails with `failed to arm` on every USB adapter on this platform except the AWUS036EACS on 2.4 GHz** (a GX10 tri-band built-in adapter enumeration conflict, plus the driver's lack of active monitor), so the handshake flow is routed through the aircrack-ng suite (airodump-ng + aireplay-ng) instead. The AXER's injection capability is sufficient on this path.

---

## 4. Advanced Features and Honest Limitations

**VIF (concurrent STA + AP) ✅**: the AXER can act as a station connected to an upstream Wi-Fi while also running an AP VIF. In testing, the main interface connected to YUPITEK while the AP VIF ran concurrently on ch36 VHT80, with the STA side pinging at 3.5 ms — suitable for "connect and run a hotspot at the same time" scenarios.

**Wi-Fi Direct (P2P) not tested (⬜)**: the driver advertises P2P-client / P2P-GO, but full validation requires a second peer device, which we skipped this round, so it is not listed as a verified capability. Items like this — "driver advertises support but not actually run on hardware" — we consistently mark as not tested, rather than padding them in as passing.

**Three unsupported modes (N/A)**: the `rtw89_8852bu` driver **does not provide active monitor, Ad-hoc (IBSS), or Mesh (802.11s)**. `iw dev $IF set type ibss` or `mp` fails outright; this is a driver-layer limitation that cannot be worked around via configuration. If your use case is mesh or IBSS experimentation, look instead at the MediaTek mt76 series (such as AWUS036ACM / ACHM).

**Platform-wide notes:**

- Never run `airmon-ng check kill`; it shuts down NetworkManager and cuts the GX10's connectivity. Operate only on the `wlx*` interface, and don't touch the built-in uplink adapter.
- If after repeatedly switching monitor/AP the adapter suddenly scans nothing (RX stall), just **unplug and re-plug it once** to recover (USB re-enumeration; the interface name is determined by MAC and won't change).
- On the ARM64 platform, aircrack-ng must be compiled from source; use the git version of wifite to bypass apt dependency conflicts.

**Kali tool compatibility**: airmon-ng, kismet 2026.10, bettercap 2.32, wifite (git), and Wireshark / tshark 4.2 can all use the AXER as a data source or management interface normally.

---

## 5. Use Cases and Selection Advice

In one sentence: **the AXER is a "reception-oriented" Wi-Fi 6 adapter**. It shares the chip with the AX and is functionally identical; the difference is the reception advantage from antenna tuning and gain, so the selection logic is clear:

| Your need | Is the AXER the top pick | Notes |
|---|---|---|
| Strongest reception / long-range monitor / site survey | ✅ **Top pick** | Channel-hopping scan caught 63 APs + 12 clients, strongest of the nine; pair with AWUS036ACH (dual-antenna high-gain) to complement |
| Wi-Fi 6 + AP hotspot | ✅ Suitable | 2x2, 5G VHT80; on par with AWUS036AX |
| Injection + end-to-end handshake | 🟡 Usable | 2.4G 73% usable; for near-100% on both bands, AWUS036EACS / ACH / ACS are more consistent |
| mesh / IBSS experiments | ❌ Not suitable | rtw89 doesn't support them; use AWUS036ACM / ACHM (mt76) instead |

A typical deployment: use the AXER as a **remote wireless monitoring node**, placed at weak-signal or distant points, leveraging its embedded antenna's reception advantage to capture as many of the site's APs/clients as possible, with scan results aggregated back to a central host for unified review. Since it has an embedded (Nano) antenna with no RP-SMA, the antenna is not replaceable; when you need higher gain or stronger directionality, complement it with the dual-antenna high-gain AWUS036ACH.

Conversely, if your use is pure AP or general connectivity with no injection at all, MediaTek's AWUS036AXM / AXML also work; but **the moment injection or handshake is involved, don't choose the AXM / AXML** — their injection fails on this platform (mainly a mac80211 chanctx regression in kernel 6.16 and later, plus firmware that locks injection rates to 1/6 Mbps; not a limit of the chip itself). The AXER is exactly the opposite: injection works, and reception is the strongest of all.

To see the full matrix and cross-comparison of all nine adapters at once, return to the overview page → [`/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## FAQ

**Q1. Does AWUS036AXER need a separate driver on Ubuntu 24.04 or Kali?**
On Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia), no: the in-kernel `rtw89_8852bu` driver recognizes it on plug-in, with no compilation and no DKMS (firmware `rtw8852b_fw` 0.29.29.5). Our platform is Ubuntu, not the Kali distribution, so Kali itself was not tested; common Kali tools airmon-ng, kismet, bettercap, wifite, and Wireshark all work on this platform. On older kernels the in-kernel driver is not guaranteed, so check your version first.

**Q2. Does AWUS036AXER support monitor mode? How strong is its reception?**
Yes, it enters monitor on both 2.4 GHz and 5 GHz. In our own office we ran a 60-second channel-hopping airodump-ng scan and caught 63 APs and 12 clients, the strongest reception of the nine adapters we tested side by side; the same-chip AWUS036AX caught 14 APs + 4 clients in a separate test (two non-simultaneous measurements, for reference only).

**Q3. Can AWUS036AXER do packet injection?**
Yes. On 2.4 GHz, `aireplay-ng --test` gave a 73% response rate (22/30) and showed `Injection is working!`; 5 GHz passed per-AP self-tests as well. We completed handshake capture and exported `.22000` on our own network and our own devices. For near-100% on both bands, our testing found AWUS036EACS, ACH, and ACS more consistent. Only on networks you own or are authorized to test.

**Q4. What's the difference between AWUS036AXER and AWUS036AX?**
Both use the Realtek RTL8832BU and the same `rtw89_8852bu` driver, with identical mode support and injection behavior on this platform; the difference is in antenna tuning and gain, which drives reception (AXER: 63 APs + 12 clients in 60s; AX: 14 APs + 4 clients). Both use embedded antennas with no RP-SMA; refer to the product page for antenna specs.

**Q5. Can AWUS036AXER run as an AP or use WPA3? Which modes are unsupported?**
Yes. Both 2.4 GHz 802.11n and 5 GHz VHT80 (VHT-NSS2, 351 Mbit) saw an iPhone connect and reach authorized; WPA3-SAE with `sae_pwe=0` let an iPhone 15 Pro connect (on 2.4 GHz; 5 GHz WPA3 was not tested); concurrent STA + AP works. However, `rtw89_8852bu` does not support active monitor, IBSS, or mesh.

---

## 6. Further Reading

- Full matrix and selection table for all nine ALFA adapters (Monitor · Injection · AP comparison) → `/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- Same-chip AWUS036AX hands-on (different antenna tuning) → `/en/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- Driver-free: enabling Monitor and AP modes with the in-kernel driver → `/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- Handshake capture in the WPA3-SAE era and `sae_pwe` compatibility → `/en/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- Further-reading internal links to be finalized with official hreflang-paired URLs; the above are en slug placeholders. -->

---

*Tested by: Yopitek (ALFA distributor) — https://www.yupitek.com | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Test device: Apple iPhone 7 Plus (WPA3 separately tested with iPhone 15 Pro)*
