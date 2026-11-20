---
title: "AWUS036AXM Single-Adapter Hands-On: MediaTek MT7921AU (Wi-Fi 6 2x2) Monitor / AP / WPA3 Capabilities and Injection Limitations on ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM (mt7921u) tested on ASUS GX10 / Ubuntu 24.04 ARM64: monitor, AP, and WPA3 work, but packet injection fails — not suited to penetration testing; positioned for pure AP and connectivity."
faq:
  - question: "Can AWUS036AXM do packet injection?"
    answer: "On our test platform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), no. aireplay-ng --test reports No Answer and Found 0 APs on both 2.4 GHz and 5 GHz, so it also cannot deauth or capture a WPA handshake. The root cause is the mac80211 chanctx regression in kernel 6.16+, not an inherent inability of the chip to inject; the same-family AWUS036AXML behaves identically. If you need injection, choose the tested-usable AWUS036EACS, ACH, or ACS instead."
  - question: "Is AWUS036AXM suitable for penetration testing or Kali?"
    answer: "Not recommended. Monitor works but reception is weak and client/data frames are often missed, and injection fails on this platform, so it cannot deauth or capture a handshake. Our platform is Ubuntu 24.04; we did not test the Kali distribution itself. It suits pure AP, general connectivity, and WPA3 hotspots; for penetration testing, choose AWUS036EACS, ACH, or ACS."
  - question: "Does AWUS036AXM need a separate driver on Ubuntu 24.04?"
    answer: "No. The mt7921u driver is in-kernel on kernel 6.17 and the adapter is recognized on plug-in (USB ID 0e8d:7961), with no DKMS and no compilation. The driver does not provide IBSS (Ad-hoc) or mesh modes; this is a limitation, not a config issue."
  - question: "Can AWUS036AXM run as an AP hotspot? Does it support WPA3?"
    answer: "Yes, and this is what it does best. Both 2.4 GHz (802.11n) and 5 GHz VHT80 saw an iPhone connect and reach authorized; WPA3-SAE works on 2.4 GHz (MFP: yes; 5 GHz WPA3 was not tested), and older iPhones need sae_pwe=0; concurrent STA + AP (VIF) also works. This round only covered 2.4 and 5 GHz; 6 GHz and Bluetooth were not separately tested."
  - question: "How good is AWUS036AXM's monitor mode?"
    answer: "It enters monitor and receives beacons on both 2.4 GHz and 5 GHz, but reception is weak and client/data frame counts are low, so lock to a single channel rather than hopping. For wide-area or long-range monitoring, AWUS036AXER and ACH were clearly stronger in our testing."
draft: false
---

{{< tldr >}}On ASUS GX10 / Ubuntu 24.04 ARM64, AWUS036AXM works for monitor, AP, WPA3, and VIF, but packet injection fails in testing (No Answer / Found 0 APs), so it cannot deauth or capture a handshake and is not recommended for penetration testing; positioned for pure AP and connectivity.{{< /tldr >}}

Yopitek is ALFA Network's Taiwan distributor. This is a per-adapter hands-on of the AWUS036AXM with a simple goal: to measure clearly what this Wi-Fi 6 adapter can and can't do on **ASUS GX10 (ARM64) + Ubuntu 24.04**, so buyers don't have to guess from the spec sheet.

Let's be clear on positioning up front: all of the tests below were done on Yopitek's own equipment and own office Wi-Fi, against our own test phones. This is a distributor's hardware validation of product compatibility and capability boundaries, not an attack tutorial against third-party networks. The article provides no steps for operating against external networks; all monitor- and injection-related measurements are done in our own closed environment, against our own devices.

The one thing to know about this adapter first: **its injection fails on this platform**. If your use case involves injection or handshake capture, you can jump straight to Sections Four and Five for the selection conclusion; if what you want is stable connectivity and running an AP, the AWUS036AXM is a very capable adapter.

## 1. The Adapter and the Test Platform

AWUS036AXM uses the MediaTek **MT7921AU** chip via the kernel's built-in **mt7921u** driver, spec'd as **Wi-Fi 6 (802.11ax), 2x2** dual spatial streams. The same-chip **AWUS036AXML** (MT7921AUN, with added Bluetooth) behaves identically for Wi-Fi monitor / AP / injection on this platform, so the two can cross-reference each other; the difference is that the AXML also has Bluetooth and, in our on-machine testing, a usable 6 GHz band, whereas the AXM's 6 GHz and Bluetooth were not separately tested this round.

- **Compute platform**: ASUS GX10 (ARM64 / aarch64)
- **OS**: Ubuntu 24.04 LTS
- **Kernel version**: kernel 6.17.0-1014-nvidia
- **Test device**: Apple iPhone 7 Plus (WPA3-SAE and VIF re-tested with an iPhone 15 Pro)
- **Test environment**: own office Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36
- **Test period**: on-machine measurements from 2026-11-16 to 2026-11-18

## 2. Hardware and Driver (Works Out of the Box)

The mt7921u driver is already built into kernel 6.17, so the AWUS036AXM is recognized the moment it's plugged into the GX10 — no DKMS, no compiling any third-party driver yourself. This is where this generation of MediaTek adapters is least hassle on ARM64.

| Item | Detail |
|---|---|
| Model | AWUS036AXM |
| Chip | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| Driver (in-kernel) | `mt7921u` |
| Generation / streams | Wi-Fi 6 (802.11ax) / 2x2 |
| Interface modes | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| Unsupported modes | IBSS (Ad-hoc), Mesh (802.11s) |

Confirm the adapter is recognized:

```bash
lsusb | grep 0e8d:7961
```

Expected output is `ID 0e8d:7961 MediaTek Inc. Wireless_Device`. Also note that the interface modes listed by `iw phy info` include no IBSS and no mesh point; this is an inherent limitation of mt7921u, not a config issue — for mesh / IBSS scenarios, use the `mt76`-based AWUS036ACM / ACHM instead.

## 3. Measured Capabilities: Monitor / AP / WPA3, Plus an Honest Account of Injection Failure

Here's a core capability matrix first, followed by item-by-item detail.

| Capability | 2.4 GHz | 5 GHz | Measurement note |
|---|---|---|---|
| Monitor | ✅ Works (weaker RX) | ✅ Works (weaker RX) | Receives beacons; client / data frame counts are low |
| **Injection** | ❌ **Fails on this platform** | ❌ **Fails on this platform** | Root cause is the kernel 6.16+ mac80211 chanctx regression (not inherent to the chip) |
| AP | ✅ incl. 802.11n (HT20) | ✅ VHT 80 MHz | iPhone 7 Plus connected on hardware, authorized |
| WPA3-SAE | ✅ | Not tested | MFP: yes, `sae_pwe=0` for older iPhone compatibility; tested on 2.4 GHz only |
| VIF (STA + AP) | ✅ | ✅ | One adapter, dual use, STA-side ping 17 ms |

### Monitor ✅ Works, but Reception Is Weak

Both 2.4GHz and 5GHz can switch into monitor mode, and both receive beacons. But to be honest: the AWUS036AXM's reception is noticeably weaker than the same-platform AWUS036ACM / ACHM, with low measured frame counts and not many client or data packets captured. In practice, we recommend **locking to a single channel** for capture rather than hopping, which yields steadier results.

There's also a point that's easy to misread: in monitor mode `txpower` reports 3 dBm, which is a reporting artifact (actual hardware TX is about 20 dBm, verified via `txpower_sku`) and does not mean transmission is really pinned that low. The AWUS036AXM was never designed for wide-area capture; to scan wide and receive far, look to the AWUS036AXER with stronger antenna tuning and more aggressive hopping, or the dual-antenna high-gain AWUS036ACH — both have clearly stronger monitor reception on the same platform.

### AP ✅ This Is Where the AXM Shines

On 2.4GHz the AP can run 802.11n (HT20) simultaneously, with the iPhone 7 Plus connecting and negotiating MCS 7, authorized. On 5GHz it goes up to **VHT 80 MHz**, with the iPhone connecting as VHT-NSS2, authorized. On both 2.4G and 5G, the AWUS036AXM is stable as a hotspot — this is its most worthwhile capability on this platform.

### WPA3-SAE ✅

With WPA3-SAE enabled on the AP side, the iPhone 7 Plus connected successfully, with MFP (Management Frame Protection) showing `yes`. Practical reminder: setting `sae_pwe=0` provides compatibility with older devices like the iPhone 7 Plus; with `sae_pwe=2`, older iPhones may fail to connect.

### VIF (STA + AP, One Adapter, Dual Use) ✅

The AWUS036AXM can act as a STA connected to an existing Wi-Fi while also running an AP virtual interface (VIF). In testing, when an iPhone 15 Pro connected to the AP VIF, the STA side's ping to `YUPITEK` was about 17 ms, with connectivity normal. For the "one adapter online while sharing a hotspot" need, it's usable.

### Injection ❌ Fails on This Platform — The Selection Dividing Line

This is the most important and most honesty-demanding point about the AWUS036AXM. The measured `aireplay-ng --test` output is:

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

It fails the same way on both 2.4GHz and 5GHz. First, to clear up a common misconception: the `txpower` of just 3 dBm that `iw` reports in monitor mode is a **reporting artifact** — actual hardware TX is about 20–23 dBm (verified via `txpower_sku`), transmit power is not being pinned low, and this is not the cause of the failure. The real root cause is at the **software layer**: after kernel 6.16, mac80211's channel context (chanctx) has a regression that leaves the stock driver unable to receive target beacons in active-monitor/injection scenarios, so `aireplay-ng` judges `No Answer`. This is a **kernel-side regression, not an inherent inability of the MT7921 chip to inject**. The phenomenon is recorded in morrownr/USB-WiFi issue #387, and the root-cause analysis is in morrownr/mt76 issue #18.

To add: community testing indicates that switching to a git/patched driver on the same model can indeed make active monitor plus injection work; but even so, the MT7921 firmware still **locks injection to the 1 Mbps / 6 Mbps base rates** and cannot inject at HT / VHT rates. In other words, even if you bypass the kernel regression, this adapter's injection capability is limited. By contrast, Realtek's rtw89 adapters (such as AWUS036AX / AXER) have working injection on the same aircrack-ng suite and the same GX10 platform; the MT7921 path does not work on **stock kernel 6.17**.

Once more: this is not a single-adapter defect, nor a misconfiguration. The same-chip AWUS036AXML behaves exactly the same, and on stock kernel 6.17 no amount of changing parameters, switching channels, or changing the regulatory domain brings it back — the root cause is the kernel 6.16+ mac80211 chanctx regression, plus the firmware's injection rate lock, not a chip hardware defect. The direct consequence: on this platform the AWUS036AXM **cannot deauth and cannot actively capture a WPA handshake**. If you need those capabilities, switch to the Realtek / mt76x options in the next section.

As for advanced features, here's the summary:

| Advanced feature | Status | Notes |
|---|---|---|
| WPA handshake capture | ❌ | Unavailable due to injection failure; use ACM / ACHM / ACH / ACS / EACS |
| VIF (STA + AP) | ✅ | One adapter, dual use, usable |
| Active monitor | 🟡 | `set monitor active` is accepted, ACK not verified |
| Ad-hoc (IBSS) | N/A | mt7921u does not support it |
| Mesh (802.11s) | N/A | mt7921u does not support it |
| Wi-Fi Direct (P2P) | ⬜ | Driver advertises support, not tested for lack of a second device |

### Operational Safety and Practical Reminders

A few practical points for operating this adapter on the GX10, stated up front so you hit fewer pitfalls:

- **Don't cut your own network**: never run `airmon-ng check kill`; it shuts down NetworkManager and cuts the entire GX10 offline. Operate only on the external `wlx*` interface, and don't touch the GX10's built-in uplink.
- **AP password must be 8+ characters**: otherwise hostapd returns `invalid WPA passphrase length` and won't come up.
- **When the phone can't see the SSID**: unplug and re-plug the adapter once to reset it, or move the phone closer (the 3 dBm reported in monitor mode is an artifact, not real power, and not the cause).
- **Clearing RX stall**: if after repeatedly switching monitor / AP it suddenly scans nothing, it's usually an RX stall; unplug and re-plug the adapter once to recover (the interface name is MAC-based and won't change).

## 4. Suitable and Unsuitable Uses

Boiling the measurements above down to one sentence: the AWUS036AXM is an excellent "connectivity / AP" adapter, but not an "injection / offense-defense" adapter.

**Suitable uses**

- Stable everyday connectivity (Wi-Fi 6, 2x2)
- Running 2.4GHz / 5GHz AP hotspots (including 802.11n and VHT80)
- WPA3-SAE compatibility validation and deployment testing
- STA + AP, one adapter, dual use (VIF)
- Lightweight monitor needs for passive beacon capture

**Unsuitable uses (avoid)**

- injection / deauth
- WPA handshake capture, active offense-defense exercises
- Experiments requiring IBSS (Ad-hoc) or Mesh
- Long-range, high-sensitivity, wide-area monitor capture

**The single most important caution**: if your use is **injection or handshake**, **do not choose the AWUS036AXM (or the same-chip AWUS036AXML)**. On this ASUS GX10 platform (ARM64 / Ubuntu 24.04 / stock kernel 6.17), MT7921 injection fails; the root cause is the kernel 6.16+ mac80211 chanctx regression, not an inherent inability of the chip to inject, and as of 2026-11-18 it cannot be solved by tuning parameters in the stock environment. Reserve it for "pure connectivity / pure AP" scenarios.

## 5. Selection Advice (Pure AP / Connectivity)

| Your need | Recommended choice | Reason |
|---|---|---|
| Pure AP / stable connectivity (no injection) | **AWUS036AXM** / AWUS036AXML | MediaTek is stable for connectivity, with good AP and WPA3 performance |
| Penetration testing (injection + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | Injection works on both bands, end-to-end handshake runs through |
| Strongest reception / long-range monitor | AWUS036AXER / AWUS036ACH | AXER hops aggressively, ACH is dual-antenna high-gain |
| Wi-Fi 6 + AP and needs injection | AWUS036AX / AWUS036AXER | 2x2 VHT80, stable AP and working injection |
| mesh / IBSS experiments | AWUS036ACM / AWUS036ACHM | The `mt76` driver can build them on a single machine |

In plain terms: for stable connectivity and running an AP, the AWUS036AXM is very capable; the moment injection or handshake is involved, switch to Realtek's EACS / ACH / ACS. For the full comparison of this batch on ARM64, plus the complete 9-adapter Monitor / Injection / AP / WPA3 matrix, see the overview hub:

- [The most complete 2026 hands-on: full matrix of 9 ALFA wireless adapters on ASUS GX10 (ARM64 / Ubuntu 24.04)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

To reiterate the positioning: all monitor/injection-related measurements in this article were done entirely in Yopitek's own closed environment, against our own test devices, to validate product capabilities and compatibility boundaries; we neither provide nor recommend performing the above operations against any third-party network.

## FAQ

**Q1. Can AWUS036AXM do packet injection?**
On our test platform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), no. `aireplay-ng --test` reports `No Answer` and `Found 0 APs` on both 2.4 GHz and 5 GHz, so it also cannot deauth or capture a WPA handshake. The root cause is the mac80211 chanctx regression in kernel 6.16+, not an inherent inability of the chip to inject; the same-family AWUS036AXML behaves identically. If you need injection, choose the tested-usable AWUS036EACS, ACH, or ACS instead.

**Q2. Is AWUS036AXM suitable for penetration testing or Kali?**
Not recommended. Monitor works but reception is weak and client/data frames are often missed, and injection fails on this platform, so it cannot deauth or capture a handshake. Our platform is Ubuntu 24.04; we did not test the Kali distribution itself. It suits pure AP, general connectivity, and WPA3 hotspots; for penetration testing, choose AWUS036EACS, ACH, or ACS.

**Q3. Does AWUS036AXM need a separate driver on Ubuntu 24.04?**
No. The mt7921u driver is in-kernel on kernel 6.17 and the adapter is recognized on plug-in (USB ID `0e8d:7961`), with no DKMS and no compilation. The driver does not provide IBSS (Ad-hoc) or mesh modes; this is a limitation, not a config issue.

**Q4. Can AWUS036AXM run as an AP hotspot? Does it support WPA3?**
Yes, and this is what it does best. Both 2.4 GHz (802.11n) and 5 GHz VHT80 saw an iPhone connect and reach authorized; WPA3-SAE works on 2.4 GHz (`MFP: yes`; 5 GHz WPA3 was not tested), and older iPhones need `sae_pwe=0`; concurrent STA + AP (VIF) also works. This round only covered 2.4 and 5 GHz; 6 GHz and Bluetooth were not separately tested.

**Q5. How good is AWUS036AXM's monitor mode?**
It enters monitor and receives beacons on both 2.4 GHz and 5 GHz, but reception is weak and client/data frame counts are low, so lock to a single channel rather than hopping. For wide-area or long-range monitoring, AWUS036AXER and ACH were clearly stronger in our testing.

## 6. Further Reading

The following related articles are coming online (links under construction):

- "Driver-free: Enabling Monitor and AP Modes on Ubuntu (ARM64)" → [`/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- "WPA3-SAE Capability and Handshake Practice (Validated in an Owned Environment)" → [`/en/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- "AWUS036AXML Single-Adapter Hands-On (Same MT7921 Chip + BT)" → (under construction)
- "Why mt7921u Can't Inject on Kernel 6.16+: The chanctx Regression and the Firmware Rate Lock Explained" → (under construction)

---

*Tested by: Yopitek (ALFA distributor) | Platform: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Test device: Apple iPhone 7 Plus (WPA3 / VIF separately tested with iPhone 15 Pro)*
