---
title: "AWUS036ACS Card-by-Card Test: RTL8811AU Lightweight Travel Adapter on ASUS GX10 + Ubuntu 24.04 (ARM64) — Compatibility and Capability Report"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS tested on Ubuntu 24.04 ARM64: no driver install needed, and Monitor, injection (2.4G 100%, 5G 96%), AP, WPA3-SAE, and end-to-end handshake (.22000) all pass. Platform: ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "Do I need to install a driver for the AWUS036ACS on Ubuntu 24.04 ARM64?"
    answer: "Not on the kernel 6.17 (ASUS GX10) tested here: RTL8811AU is driven by the in-kernel rtw88_8821au, recognized on plug-in with no compiling and no DKMS. On older kernels, first run modinfo rtw88_8821au to confirm the module exists."
  - question: "Does the AWUS036ACS support monitor mode and packet injection?"
    answer: "Yes. It can monitor on both 2.4 GHz and 5 GHz; aireplay-ng --test injection is 100% (30/30) on 2.4G and 96% (29/30) on 5G, after first running iw reg set US to lift the TW restriction. Active monitor is not supported."
  - question: "Can the AWUS036ACS capture a WPA handshake and convert it to a hashcat .22000?"
    answer: "Yes. Tested end-to-end against our own AP and our own iPhone 7 Plus: a targeted deauth triggers reconnection, the full 4-way (M1-M4) is captured, and hcxpcapngtool --all exports the .22000. Only on networks you own or are authorized to test."
  - question: "Can the AWUS036ACS act as an AP hotspot? Does it support WPA3?"
    answer: "Yes. hostapd brings up 2.4G and 5G hotspots (5G was tested as 802.11a at 20 MHz; VHT80 was not tested), an iPhone 7 Plus associates and completes the 4-way; the 5G WPA3-SAE (SAE-only, ieee80211w=2, sae_pwe=0) also associates successfully (WPA3 on 2.4G was not tested)."
  - question: "Which modes does the AWUS036ACS not support? Does hcxdumptool work?"
    answer: "Active monitor, IBSS, mesh (802.11s), and Wi-Fi Direct (P2P) are not supported. hcxdumptool 8.x returns failed to arm interface; use airodump-ng + aireplay-ng instead. For mesh / IBSS, choose the AWUS036ACM / ACHM."
draft: false
---

**TL;DR**: In hands-on testing by Yopitek (ALFA Network's Taiwan distributor), the AWUS036ACS needs no driver install on the ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) and works for dual-band monitor and AP (5G AP usable: 802.11a, 20 MHz tested; VHT80 not tested); injection is 100% on 2.4G and 96% on 5G, end-to-end .22000 passes, and mesh / IBSS are not supported.

> This is Yopitek's product compatibility and capability test log for the ALFA AWUS036ACS on a recent Linux platform, intended for evaluation and selection.
> Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. All data are excerpts from Yopitek's hands-on testing on **our own equipment and our own office Wi-Fi** (SSID `YUPITEK`, 2.4G ch5 / 5G ch36) against **our own test phone** (Apple iPhone 7 Plus); MAC addresses are partially masked.
> ⚠️ **Legal and scope statement**: Monitor, injection, and handshake capture were performed only on networks and devices we own or are authorized to test; for AP mode, follow your local radio regulations. This article focuses on the adapter's own capabilities, compatibility, and configuration, and **does not involve any attack operation against third-party networks**.

---

## 1. This Card and the Test Platform

The AWUS036ACS is a lightweight travel-class wireless adapter in ALFA's lineup. Its chipset is the Realtek RTL8811AU, a Wi-Fi 5 (802.11ac) generation part with a single 1x1 spatial stream. Its positioning is plain: small, low-power, single-antenna — a card to carry out for on-site surveys, not a heavy rig built for peak throughput or maximum range. So when you evaluate it, the question is not "how fast is it" but "with specs this light, which practical capabilities remain fully usable."

This round of testing drops it into a typical operations scenario: the GX10's built-in adapter (`wlP9s9`) handles upstream connectivity, while the AWUS036ACS attaches over USB and carries only the test workload. That way, switching into Monitor or AP never touches the host's own networking. Throughout, we only touch the `wlx*` interface belonging to the ALFA card and never disturb the built-in upstream adapter.

| Item | Detail |
|---|---|
| Model | AWUS036ACS |
| Chipset | Realtek RTL8811AU (Wi-Fi 5 / 802.11ac, 1x1 single stream) |
| USB ID | `0bda:0811` |
| Driver | `rtw88_8821au` (in-kernel, built into kernel 6.17) |
| Firmware | 42.4.0 (per dmesg) |
| Platform | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Test device | Apple iPhone 7 Plus |

---

## 2. Hardware and Driver (No Install)

This card is recognized on plug-in on the GX10 — no compiling, no DKMS. Since mainline kernel 6.13, the RTL8811AU / RTL8821AU chip has been officially merged into Realtek's in-kernel `rtw88` driver family, and the 6.17 that ships on the GX10 already includes the `rtw88_8821au` module, so there is no need to pull any out-of-tree project from GitHub. (This differs from older install guides: earlier site articles assumed the `morrownr` out-of-tree driver or an older kernel and said you had to DKMS-compile it yourself; under the in-kernel driver on kernel 6.17 this is no longer necessary.) The once-common `morrownr/8821au-20210708` is now legacy (recommended only for kernels below 6.13, and installing it blacklists the built-in driver), and there is no reason to take that old path on a new kernel. The operational benefit is even more tangible: the in-kernel driver updates along with the kernel, so users don't each maintain a branch and don't get stuck on a DKMS build failure every upgrade — the same procedure is repeatable across several kernel updates. Firmware comes from `linux-firmware` with the system; on this machine it tested as 42.4.0, again with nothing to handle manually.

Confirm the card is recognized, the driver is bound, and the interface has appeared:

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

The firmware version can be confirmed from `dmesg` (measured as 42.4.0):

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

The declared supported interface modes (these determine which capabilities are usable later):

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

This list shows `IBSS / managed / AP / AP/VLAN / monitor`. One caveat here: although the list includes IBSS, after an `ibss join` the measured `iw link` shows Not connected — it will not come up. Mesh, active-monitor, and P2P are not on the list at all (see the limitations in Section 4). This reflects the current hardware and driver state of the RTL8811AU and has nothing to do with antenna count.

Band coverage: 2.4 GHz ch1–13 (ch14 disabled); 5 GHz ch36–165 (of which ch52–144 are marked radar / DFS). The default regdomain is `TW`, with TX power of 30 dBm on 2.4 GHz, 23 dBm on 5 GHz UNII-1/2, and 30 dBm on UNII-3.

---

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

First the core capability summary, then each item in detail. All items were completed against our own YUPITEK AP plus our own iPhone 7 Plus.

| Capability | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor (receive) | ✅ Strong | ✅ Strong |
| Injection | ✅ **100%** (30/30) | ✅ **96%** (29/30, reg must be unlocked first) |
| AP hotspot (hostapd) | ✅ iPhone associates + completes handshake | ✅ **Stable** (802.11a, 20 MHz tested; VHT80 not tested) |
| AP WPA3-SAE | Not tested | ✅ iPhone associates (SAE-only + PMF) |

### 3-1. Monitor (Monitor Mode, 2.4 GHz + 5 GHz) ✅

After switching to monitor, a fixed-length capture was run once on each of six channels, and reception was normal throughout. Busy channels hit the 300-frame capture limit within 6 seconds:

| Channel | Captured frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

Reception is steady on both 2.4 GHz and 5 GHz. For a single-antenna travel card, this receive performance is enough for on-site channel surveys and packet diagnostics. The lower frame counts on ch11, ch149, and ch157 reflect low over-the-air traffic on those channels at the time, not an inability of the card to receive; the busy ch1, ch6, and ch36 hit the 300-frame limit within six seconds, so reception is clearly not its bottleneck.

### 3-2. Injection (Packet Injection) ✅

Targeted injection testing against our own YUPITEK AP using `aireplay-ng --test`. 2.4 GHz reached 100% (30/30, `Injection is working!`), while 5 GHz was 96% (29/30). There is a configuration detail to watch on 5 GHz: the default `reg=TW` locks active transmission on part of the UNII bands, so run `sudo iw reg set US` to unlock before testing and `sudo iw reg set TW` to restore afterward.

```bash
# 2.4 GHz (YUPITEK is actually on ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

A single-antenna card reaching 100% on 2.4 GHz and 96% on 5 GHz is already quite reliable injection, and it is the foundation for the end-to-end handshake capture that follows.

### 3-3. AP Hotspot (2.4 GHz / 5 GHz) ✅

Using `hostapd` to turn the card into a base station, all three configurations let the iPhone 7 Plus associate and complete the 4-way handshake (`EAPOL-4WAY-HS-COMPLETED`):

- **5 GHz (802.11a, 20 MHz tested; VHT80 not tested)**: the most stable of the set — iPhone associated, handshake completed, and a clean `AP-DISABLED` shutdown.
- **2.4 GHz (WPA2-PSK)**: iPhone associated, handshake completed, and a clean shutdown after disconnect. An honest note here: in a previous round with the same configuration, a `key not allowed / Failed to set beacon parameters` once aborted after the STA disconnected, but a retest could not reproduce it — judged to be an occasional rtw88_8821au beacon re-key, not a fixed defect. For long-running, high-frequency reconnection scenarios it is still worth watching, or simply use a 5 GHz AP.
- **WPA3-SAE (5 GHz, PMF enforced; 2.4 GHz not tested)**: the key settings are `wpa_key_mgmt=SAE` (pure WPA3, no WPA2 fallback), `ieee80211w=2` (enforced Management Frame Protection), and `sae_pwe=0` (compatible with older endpoints). The iPhone 7 Plus (iOS 15) associated successfully via SAE. Since the AP only enables SAE with no WPA2 fallback, a successful association means the SAE authentication handshake held. WPA3-SAE on the AP side is usable with RTL8811AU + rtw88_8821au.

---

## 4. End-to-End Handshake Capability and Limitations

### 4-1. End-to-End Handshake Capture ✅

This is the integrated test that verifies whether injection plus capture can truly be "chained together," performed entirely against our own YUPITEK AP and our own iPhone 7 Plus under authorized conditions. The flow is: monitor the target channel → send a targeted deauth to our own device to trigger reconnection → capture the full 4-way (M1–M4) → use `hcxpcapngtool --all` to export a hashcat-readable `.22000`.

Measured result: `aircrack-ng` judged that YUPITEK obtained 1 handshake, all four EAPOL messages M1–M4 arrived, the client is an Apple OUI (`b8:53:ac`, confirmed to be the iPhone 7 Plus), and the exported `.22000` can be fed directly to hashcat. This means the AWUS036ACS has full end-to-end handshake capture capability.

Two practical points worth recording (full step-by-step config in a separate article):

1. **When the office has multiple identically named APs on the same channel, do not use `--bssid` to lock to a single one**; capture the entire channel instead, so you don't miss a device connected to another one.
2. `hcxpcapngtool` defaults are stricter and may return "not enough M1"; adding `--all` lets it export the `.22000` from a complete M1–M4.

The common Kali tools used in this handshake capture chain (aircrack-ng, hcxtools) all run directly on Ubuntu 24.04 ARM64; airodump-ng, aireplay-ng, and hcxpcapngtool all function normally.

### 4-2. VIF (Virtual Interface) ✅

`iw dev $IF interface add mon9 type monitor` can create a monitor VIF and captured 100 frames; separately, a script that creates "the main interface associated to YUPITEK as a STA + an AP VIF" showed that the single chip can simultaneously act as both STA and AP.

### 4-3. Honest Limitations (As Measured)

| Advanced mode / tool | Status | Measured |
|---|---|---|
| Active monitor | ❌ Not supported | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc (IBSS) | ❌ Not supported | Mode listed but after `ibss join`, `iw link` = Not connected |
| Mesh (802.11s) | ❌ Not supported | `set type mp` → `-95` |
| Wi-Fi Direct (P2P) | ❌ Not supported | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ Cannot arm | `failed to arm interface`: rtw88_8821au does not provide active-monitor; use airodump-ng + aireplay-ng |

There are also two operational limitations to know. The single 1x1 stream caps its theoretical ceiling (HT Max RX 150 Mbps, VHT80 ~433 Mbps), so throughput was never its strength. After repeatedly switching between monitor / AP, RX occasionally becomes briefly degraded (scans nothing); a single physical unplug-replug of the card recovers it, and the interface name is determined by the MAC, so it stays the same across unplug-replug.

---

## 5. Use Cases and Selection (Lightweight Travel Card, Back to the Hub)

Mapping the above capabilities back to the product positioning, the AWUS036ACS's role is clear: a card with complete capabilities but built foremost for portability. So where does it fit?

- **Fast on-site surveys / portable diagnostics**: single-antenna, small, low-power — fit for channel surveys, signal walkthroughs, and packet diagnostics in the field. Paired with a central platform like the GX10, the travel card captures on-site and sends the data back to the Hub for centralized analysis — a clean division of labor.
- **Teaching and verification**: it clears the entire main line of Monitor / Injection / AP / WPA3-SAE / end-to-end handshake, making it suitable as a demonstration and within-scope verification card.
- **Not a fit for**: scenarios needing peak throughput, maximum range, or mesh / IBSS / P2P / active-monitor — this card is not the right choice.

Lightweight does not mean cut-down features. It skips none of the main-line capabilities; what was traded away is the throughput ceiling and the advanced interface modes. So whether you pick it comes down to whether you want "carry it with you" or "run it flat out."

Compared to the rest of the family, the positioning differences are:

| Need | Recommended card | Reason |
|---|---|---|
| Lightweight travel + complete main-line capability | **AWUS036ACS** | 2.4G injection 100%, 5G 96%, end-to-end handshake usable, single-antenna and portable |
| Both bands at 100% injection / tougher pen-test verification | AWUS036EACS, AWUS036ACH | 100% injection on both bands; EACS also includes BT |
| Strongest reception / long-range monitor | AWUS036AXER, AWUS036ACH | hopping scans more targets / dual-antenna high gain |
| Single-node mesh / IBSS experiments | AWUS036ACM, AWUS036ACHM | mt76 driver can create them on a single node (Realtek rtw88 does not support them) |

Selection in one line: if you want portability with a complete main-line capability set, the AWUS036ACS is a fitting travel choice; if you want 100% injection on both bands or heavier pen-test verification, move toward the EACS / ACH.

---

## Frequently Asked Questions (FAQ)

**Q: Do I need to install a driver for the AWUS036ACS on Ubuntu 24.04 ARM64?**
Not on the kernel 6.17 (ASUS GX10) tested here: RTL8811AU is driven by the in-kernel rtw88_8821au, recognized on plug-in, with no compiling and no DKMS. On older kernels, first run `modinfo rtw88_8821au` to confirm the module exists.

**Q: Does the AWUS036ACS support monitor mode and packet injection?**
Yes. It can monitor on both 2.4 GHz and 5 GHz; `aireplay-ng --test` injection is 100% (30/30) on 2.4G and 96% (29/30) on 5G, after first running `iw reg set US` to lift the TW restriction. Active monitor is not supported.

**Q: Can the AWUS036ACS capture a WPA handshake and convert it to a hashcat .22000?**
Yes. Tested end-to-end against our own AP and our own iPhone 7 Plus: a targeted deauth triggers reconnection, the full 4-way (M1–M4) is captured, and `hcxpcapngtool --all` exports the .22000. Only on networks you own or are authorized to test.

**Q: Can the AWUS036ACS act as an AP hotspot? Does it support WPA3?**
Yes. `hostapd` brings up 2.4G and 5G hotspots (5G was tested as 802.11a at 20 MHz; VHT80 was not tested), an iPhone 7 Plus associates and completes the 4-way; the 5G WPA3-SAE (SAE-only, ieee80211w=2, sae_pwe=0) also associates successfully (WPA3 on 2.4G was not tested).

**Q: Which modes does the AWUS036ACS not support? Does hcxdumptool work?**
Active monitor, IBSS, mesh (802.11s), and Wi-Fi Direct (P2P) are not supported. hcxdumptool 8.x returns failed to arm interface; use airodump-ng + aireplay-ng instead. For mesh / IBSS, choose the AWUS036ACM / ACHM.

---

## 6. Further Reading

- Full capability comparison and selection overview of nine ALFA cards → [ALFA Wireless Adapter Overview Hub (Master Table)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [No driver install: enabling Monitor / AP on Ubuntu 24.04 + kernel 6.17 (rtw88 / rtw89 / mt76 tested)](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [WPA3-SAE and end-to-end handshake capture step-by-step guide](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Same-family BT+WiFi combo card → [AWUS036EACS card-by-card test](/en/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*Test unit: Yopitek (ALFA Network distributor in Taiwan) — https://www.yupitek.com | Test environment: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Test device: Apple iPhone 7 Plus*
