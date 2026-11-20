---
title: "AWUS036AXML Hands-On: A Wi-Fi 6 + Bluetooth Combo Adapter on ASUS GX10 (ARM64 / Ubuntu 24.04) — An Honest Report of Stable AP and Failed Injection"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML (Wi-Fi + Bluetooth) tested on ASUS GX10 / Ubuntu 24.04 ARM64: AP, WPA3, and monitor work, but injection fails and handshake capture is impossible — not recommended for penetration testing."
faq:
  - question: "Can AWUS036AXML do packet injection?"
    answer: "On our test platform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), no. aireplay-ng --test reports No Answer and Found 0 APs; per-AP tests against a specified AP only return No such BSSID available. Even though a normal scan can see that AP (about -54 dBm), under the injection tool's context it still can't receive that AP's beacon, so deauth and handshake capture (0 captured) are both unusable. The root cause is the mac80211 chanctx regression in kernel 6.16+, not an inherent inability of the chip to inject; AWUS036AXM gives the same result. If you need injection, choose AWUS036EACS, ACH, or ACS instead."
  - question: "Does AWUS036AXML's Bluetooth work on Ubuntu?"
    answer: "Bluetooth works in our on-machine testing: with bluetoothctl/hciconfig we confirmed the hci controller is UP, could scan BLE and classic Bluetooth devices, and Wi-Fi and Bluetooth can be used at the same time (coexistence). It's a Wi-Fi + Bluetooth combo device; note: on re-plug it occasionally gets stuck at WiFi probe and fails to produce a wlx interface — re-plug into a different USB port to recover."
  - question: "Does AWUS036AXML need a separate driver on Ubuntu 24.04?"
    answer: "No. The mt7921u driver is in-kernel on kernel 6.17; after plug-in, dmesg shows mt7921u renaming the interface to wlx plus the MAC (USB ID 0e8d:7961), with no DKMS and no compilation. The driver does not provide IBSS or mesh modes."
  - question: "Can AWUS036AXML run an AP and support WPA3?"
    answer: "Yes, and this is its most stable use. Both 2.4 GHz (802.11n, MCS 10) and 5 GHz VHT80 (VHT-NSS2) saw an iPhone connect and reach authorized; WPA3-SAE with sae_pwe=0 let an iPhone 15 Pro connect (MFP: yes; tested on 2.4 GHz and 6 GHz, not on 5 GHz); with concurrent STA + AP the STA-side ping was about 4.4 ms. Although classed as a Wi-Fi 6 chip, our on-machine test found the 6 GHz band usable (self-hosted 6135 MHz AP, iPhone 15 Pro connected over 802.11ax and got an IP)."
  - question: "What's the difference between AWUS036AXML and AWUS036AXM, and which should I pick?"
    answer: "On this platform the two have identical Wi-Fi behavior: same mt7921u driver, injection fails the same way, monitor reception is equally weak, and AP, WPA3, and VIF all work the same. The difference is that the AXML also has Bluetooth (usable in our on-machine test) and a usable 6 GHz band in our on-machine test, whereas the AXM's Bluetooth and 6 GHz were not separately tested this round. For pure AP or general connectivity either is fine; for injection or handshake, pick neither."
draft: false
---

{{< tldr >}}On ASUS GX10 / Ubuntu 24.04 ARM64, AWUS036AXML works for AP, WPA3, VIF, and passive monitor, with Bluetooth and the 6 GHz band also usable in our on-machine test, but injection fails in testing (No Answer / Found 0 APs), so it cannot deauth or capture a handshake and is not recommended for penetration testing; positioned for pure AP and general connectivity.{{< /tldr >}}

The ALFA AWUS036AXML is the only "MediaTek Wi-Fi 6 + Bluetooth" combo model among this batch of 9 adapters. It's the same chip generation as the Bluetooth-free AWUS036AXM (MT7921, via the `mt7921u` driver); the difference is just the added Bluetooth. The three questions customers ask most are still: Can it enter monitor? Can it inject? Can it run an AP? This article pulls the AWUS036AXML out on its own and tests it item by item on ASUS GX10 (ARM64) with Ubuntu 24.04, spelling out what it can and can't do, especially that most critical limitation: **injection fails on this platform**.

Let's be clear on positioning up front: all of the measurements below were done on Yopitek's own equipment, own office Wi-Fi (SSID `YUPITEK`), against our own test phone (iPhone 7 Plus, with WPA3 re-tested on an iPhone 15 Pro). This is a distributor's hardware validation of product compatibility and capability boundaries, not an operational tutorial against third-party networks. The monitor, AP, and injection self-tests in this article were all done in our own closed environment, against our own devices.

## 1. This Adapter and the Test Platform

- **Compute platform**: ASUS GX10 (ARM64 / aarch64)
- **OS**: Ubuntu 24.04 LTS
- **Kernel version**: kernel 6.17.0-1014-nvidia
- **Adapter under test**: ALFA AWUS036AXML (MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **Test device**: Apple iPhone 7 Plus (WPA3-SAE re-tested with an iPhone 15 Pro)
- **Test environment**: own office Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Test period**: on-machine measurements from 2026-11-16 to 2026-11-18

All results are recorded as actually measured numbers or states, not inferred from the datasheet; MAC addresses are masked with `xx` in the output.

## 2. Hardware and Driver: MT7921AUN, Works Out of the Box

| Item | Spec |
|---|---|
| Model | AWUS036AXML |
| Chip | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| in-kernel driver | `mt7921u` |
| Generation / streams | Wi-Fi 6 / 2x2 (2T2R) |
| Bluetooth | Yes (BT + WiFi combo device; on-machine test: hci controller UP, can scan BLE and classic Bluetooth devices, WiFi+BT coexistence) |
| USB enumeration | USB 3 |
| Interface naming | `wlx<MAC>` (e.g. `wlx00c0cabd65b9`) |

Identification is straightforward: after plug-in, use `lsusb` to see MediaTek's USB ID, and `dmesg` to see `mt7921u` loading and renaming the interface:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

Two key points. First, no compilation: the AWUS036AXML uses the mt7921u driver built into kernel 6.17 and is recognized on plug-in, with no need to deal with any out-of-tree DKMS module on aarch64 — which is especially convenient on the ARM64 platform. Second, it enumerates as USB 3 (some prior-generation models' OTG cables were only USB 2.0), so transfer bandwidth isn't a bottleneck.

One often-misunderstood point to add: the AWUS036AXML is positioned as a Wi-Fi 6 (not 6E) chip, but **the 6 GHz band is usable in our on-machine test** — we self-hosted a 6135 MHz AP, and an iPhone 15 Pro connected over 802.11ax and got an IP. Bluetooth is also usable in testing: `hciconfig` / `bluetoothctl` showed the hci controller state UP, able to scan BLE and classic Bluetooth devices, with Wi-Fi and Bluetooth operating simultaneously (coexistence).

Checking the supported interface modes again reveals a detail that matters for selection — there's no IBSS and no mesh point:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

In other words, managed, AP, monitor, and P2P are all there, but ad-hoc (IBSS) and 802.11s mesh — these two modes — are simply not provided by the `mt7921u` driver. Customers doing mesh / IBSS experiments should rule this adapter out directly (look instead at the `mt76`-based ACM / ACHM).

## 3. Measured Capabilities: Monitor / AP / WPA3, Plus the Honest Injection Limitation

Core capabilities at a glance:

| Capability | 2.4GHz | 5GHz | Notes |
|---|---|---|---|
| Monitor | ✅ (weak) | ✅ (weak) | Can capture beacons; client / data frames often missed |
| **Injection** | ❌ **Fails** | ❌ **Fails** | `aireplay-ng` injection / deauth doesn't work; root cause is the kernel 6.16+ mac80211 chanctx regression (not inherent to the chip) |
| AP hotspot | ✅ incl. 802.11n | ✅ VHT80 (80MHz) | iPhone 7 Plus connected, `authorized: yes` |
| WPA3-SAE | ✅ | Not tested | iPhone 15 Pro connected, `MFP: yes` (`sae_pwe=0`); also tested on 6 GHz (ch37, 6135 MHz) |

### Monitor: Enters Both Bands, but Reception Is Weak

The AWUS036AXML can enter monitor mode on 2.4GHz (ch1 / 6 / 11) and 5GHz (ch36 / 149 / 157), and capturing beacons is no problem. The setup is the standard four-step `iw dev` flow:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # for 2.4GHz use set channel 6
```

Honestly: its monitor reception is noticeably weaker than the same-batch MT7612U (ACM) or the Wi-Fi 6 AXER. Beacons can be captured, but client / data frames are often missed; when channel-hopping with `airodump-ng` it's easy to miss some APs. In practice, we recommend locking to a single channel (`-c <ch>`) rather than hopping, which yields steadier results. Also, in monitor mode `iw info` reports `txpower` of just 3 dBm — this is a **reporting artifact** (actual hardware TX is about 20–23 dBm, verified via `txpower_sku`), not the power really being pinned to 3 dBm; the "notes" section later covers this together.

### AP Hotspot: 2.4GHz with HT, 5GHz Reaches VHT80

AP is the AWUS036AXML's most stable area. On 2.4GHz you can keep 802.11n (HT) directly, without disabling HT like the single-antenna ACHM; on 5GHz it goes up to VHT 80MHz. Both bands were tested with the iPhone 7 Plus connecting, `authorized: yes`.

Key hostapd settings for 5GHz VHT80:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

After connecting in testing it was VHT-NSS2, 80MHz. For the 2.4GHz version, change `hw_mode` to `g`, `channel=6`, and keep `ieee80211n=1` and `ht_capab=[HT20]`; the iPhone connects at MCS 10 (802.11n).

### WPA3-SAE: Works, Remember sae_pwe=0

Change the AP's `wpa_key_mgmt` to `SAE`, add `ieee80211w=2` and `sae_pwe=0`, and you can run WPA3-SAE. In testing an iPhone 15 Pro connected on 2.4 GHz (and on 6 GHz; 5 GHz was not tested), `authorized: yes`, `MFP: yes`. The `sae_pwe=0` is for compatibility with older iPhones, the same gotcha as the ACHM — with `sae_pwe=2`, older phones often fail to connect.

### VIF: Online and a Hotspot at the Same Time, Workable

The AWUS036AXML supports multiple concurrent interfaces. Create an AP VIF (different MAC, unmanaged), have the main interface connect to Wi-Fi, and run the AP on the same channel; in testing, when the iPhone 7 Plus connected to the AP VIF, the STA's ping to `YUPITEK` was 4.4 ms. For the "one adapter online + sharing a hotspot" need, it holds up.

### Honest Limitation: Injection Fails on This Platform

This is the point that most needs spelling out for the AWUS036AXML (and its Bluetooth-free twin, the AXM). On ASUS GX10 + kernel 6.17, we ran an injection self-test against our own test environment, and the result was failure:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Even specifying our own AP's BSSID for a per-AP test only returned `No such BSSID available`. The key is this: a normal scan can plainly see that AP (signal -54 dBm), but the moment it enters the injection tool's context, the adapter "can't hear" the target's beacon, deauth can't be sent, and the 4-way handshake capture count is 0.

This is not poorly-tuned parameters, nor a single-adapter defect. The real root cause is at the **software layer**: after kernel 6.16, mac80211's channel context (chanctx) has a regression that leaves the stock driver unable to receive the target beacon in injection scenarios, so `aireplay-ng` judges `No Answer`, and it is **not an inherent inability of the MT7921 chip to inject**. The phenomenon is recorded in morrownr/USB-WiFi issue #387, and the root-cause analysis is in morrownr/mt76 issue #18. Community testing indicates that a git/patched driver on the same model can make active monitor plus injection work, but the MT7921 firmware still locks injection to the 1 Mbps / 6 Mbps base rates and can't inject at HT / VHT; both the AXM and AXML are hit the same way on **stock kernel 6.17**, and as of 2026-11-18 it can't be solved by tuning parameters.

Therefore, any capability involving injection — such as deauth, WPA handshake capture, or penetration testing premised on injection — is something the AWUS036AXML can't do on this platform. For such uses, switch to a model with tested-usable injection (see the selection section below).

### Other Advanced Modes at a Glance

| Advanced feature | Status | Notes |
|---|---|---|
| VIF (concurrent STA + AP) | ✅ | Same channel ch36; STA ping 4.4 ms when iPhone connected |
| WPA handshake capture | ❌ | Injection fails → deauth can't be sent, handshake 0 |
| Active monitor | 🟡 | `set monitor active` is accepted, ACK not verified |
| Ad-hoc (IBSS) | N/A | The `mt7921u` driver lacks this mode |
| Mesh (802.11s) | N/A | The `mt7921u` driver lacks this mode |
| Wi-Fi Direct (P2P) | ⬜ | Driver advertises support, needs a second device, skipped |

## 4. Bluetooth Combo Notes and Suitable / Unsuitable Uses

### Practical Side Effects of a BT + WiFi Combo Adapter

The AWUS036AXML includes Bluetooth and is one of the two combo devices in this batch (the other is Realtek's EACS). Bluetooth has been tested usable on-machine (hci controller UP, able to scan BLE and classic Bluetooth devices, coexisting with Wi-Fi, as noted earlier); here's one practical side effect of a combo device: on re-plug it occasionally gets stuck at WiFi probe and fails to produce a `wlx` interface, with the symptom being that after re-plugging, `ls /sys/class/net` keeps waiting without a network adapter. The fix is simple: **re-plug into a different USB port**, and it usually enumerates normally.

Another small move to remember: in AP mode, if the phone suddenly can't see your SSID, just unplug and re-plug the adapter once to reset it, with no need to change settings. (Note: as mentioned, the 3 dBm reported in monitor mode is an artifact, not real power, and is not the cause of the SSID disappearing.)

### Platform Safety Rules

- Never run `airmon-ng check kill`: it shuts down NetworkManager and cuts the entire GX10 offline. Operate only on the external `wlx*` interface, and don't touch the built-in uplink.
- `hcxdumptool 8.x` fails with `failed to arm` on this machine (except the AWUS036EACS on 2.4 GHz) (a GX10 tri-band built-in adapter enumeration conflict + the driver's lack of active monitor); this is a platform-wide issue unrelated to the AXML. When you need similar functionality, use `airodump-ng` with other aircrack-ng tools instead.
- ARM64 note: `aircrack-ng` must be compiled from source, and the git version of `wifite` is recommended to bypass apt dependency conflicts.

### Suitable / Unsuitable at a Glance

| Suitable use | Unsuitable use |
|---|---|
| Pure AP / hotspot (2.4G incl. HT, 5G VHT80) | injection / deauth |
| WPA3-SAE hotspot | WPA handshake capture |
| General managed connectivity | A primary adapter for injection-premised penetration testing |
| Passive monitor / spectrum survey (lock single channel) | mesh / IBSS experiments |
| Concurrent STA + AP (VIF, online while sharing) | Long-range capture requiring strong reception |

## 5. Selection Advice (Linking Back to the Overview)

Placing the AWUS036AXML back into the full picture of the 9 adapters, its positioning is clear: MediaTek is stable for connectivity, needs no compilation, and reaches VHT80 on both AP bands — a capable "pure connectivity / pure AP" adapter; the moment injection is involved, it's not its arena.

| Need | Recommended model |
|---|---|
| Pure AP / general connectivity (no injection) | **AWUS036AXML / AWUS036AXM** (this adapter applies) |
| injection + handshake (penetration testing) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS experiments | AWUS036ACM / AWUS036ACHM |
| Strongest reception / long-range monitor | AWUS036AXER / AWUS036ACH |

If you're deciding among the 9, for the complete Monitor / Injection / AP / WPA3 matrix and by-use-case selection, see the overview:

- [The most complete 2026 hands-on: full matrix of 9 ALFA wireless adapters on ASUS GX10](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

One line to avoid pitfalls: **for injection or handshake, don't choose the AWUS036AXML / AWUS036AXM**; for pure connectivity or running a hotspot, it works very well.

## FAQ

**Q1. Can AWUS036AXML do packet injection?**
On our test platform (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), no. `aireplay-ng --test` reports `No Answer` and `Found 0 APs`; per-AP tests against a specified AP only return `No such BSSID available`. Even though a normal scan can see that AP (about -54 dBm), under the injection tool's context it still can't receive that AP's beacon, so deauth and handshake capture (0 captured) are both unusable. The root cause is the mac80211 chanctx regression in kernel 6.16+, not an inherent inability of the chip to inject; AWUS036AXM gives the same result. If you need injection, choose AWUS036EACS, ACH, or ACS instead.

**Q2. Does AWUS036AXML's Bluetooth work on Ubuntu?**
Bluetooth works in our on-machine testing: with `bluetoothctl` / `hciconfig` we confirmed the hci controller is UP, could scan BLE and classic Bluetooth devices, and Wi-Fi and Bluetooth can be used at the same time (coexistence). It's a Wi-Fi + Bluetooth combo device; note: on re-plug it occasionally gets stuck at WiFi probe and fails to produce a `wlx` interface — re-plug into a different USB port to recover.

**Q3. Does AWUS036AXML need a separate driver on Ubuntu 24.04?**
No. The mt7921u driver is in-kernel on kernel 6.17; after plug-in, dmesg shows mt7921u renaming the interface to `wlx` plus the MAC (USB ID `0e8d:7961`), with no DKMS and no compilation. The driver does not provide IBSS or mesh modes.

**Q4. Can AWUS036AXML run an AP and support WPA3?**
Yes, and this is its most stable use. Both 2.4 GHz (802.11n, MCS 10) and 5 GHz VHT80 (VHT-NSS2) saw an iPhone connect and reach authorized; WPA3-SAE with `sae_pwe=0` let an iPhone 15 Pro connect (`MFP: yes`; tested on 2.4 GHz and 6 GHz, not on 5 GHz); with concurrent STA + AP the STA-side ping was about 4.4 ms. Although classed as a Wi-Fi 6 chip, our on-machine test found the 6 GHz band usable (self-hosted 6135 MHz AP, iPhone 15 Pro connected over 802.11ax and got an IP).

**Q5. What's the difference between AWUS036AXML and AWUS036AXM, and which should I pick?**
On this platform the two have identical Wi-Fi behavior: same mt7921u driver, injection fails the same way, monitor reception is equally weak, and AP, WPA3, and VIF all work the same. The difference is that the AXML also has Bluetooth (usable in our on-machine test) and a usable 6 GHz band in our on-machine test, whereas the AXM's Bluetooth and 6 GHz were not separately tested this round. For pure AP or general connectivity either is fine; for injection or handshake, pick neither.

## Further Reading

(Links coming online, under construction)

- Same-chip Bluetooth-free version: [AWUS036AXM Single-Adapter Hands-On](/en/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- Injection-usable alternatives: [AWUS036EACS Single-Adapter Hands-On](/en/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACH Single-Adapter Hands-On](/en/blog/awus036ach-asus-gx10-ubuntu-test-report/), [AWUS036ACS Single-Adapter Hands-On](/en/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- Topic article: [Driver-free: Enabling Monitor and AP Modes on Ubuntu (ARM64)](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Topic article: [WPA3-SAE Connectivity and Handshake Practice (Validated in an Owned Environment)](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Overview Hub: [Full matrix of 9 ALFA adapters on ASUS GX10](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*Tested by: Yopitek (ALFA Network Taiwan distributor) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Test device: Apple iPhone 7 Plus (WPA3 separately tested with iPhone 15 Pro) | Test environment: own office Wi-Fi (SSID YUPITEK). This article is product-compatibility and capability validation, not an operational tutorial against third-party networks.*
