---
title: "The Most Complete 2026 Test: Monitor / Injection / AP Matrix of 9 ALFA Wi-Fi Adapters on the ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "A hands-on test of 9 ALFA Wi-Fi USB adapters on Ubuntu 24.04 ARM64 (GX10), covering Monitor, Injection, AP and WPA3-SAE behavior, plus Kali tool compatibility and selection advice. AWUS036ACH / EACS reach 100% injection."
faq:
  - question: "Can the AWUS036AXM do injection on Ubuntu?"
    answer: "Not on this platform. In our testing, both the AWUS036AXM and AWUS036AXML (both MT7921 chips) failed injection on 2.4GHz and 5GHz, mainly due to the mac80211 chanctx regression in the stock kernel 6.16+ (not inherent to the chip). We therefore don't recommend them on this platform for any use that needs injection or handshake capture."
  - question: "Which ALFA adapter has the highest injection success rate on Ubuntu?"
    answer: "In testing, the AWUS036ACH and AWUS036EACS both reached 100% injection success on 2.4GHz and 5GHz, the best two of the 9 cards in this batch."
  - question: "Do the 9 ALFA adapters need extra driver installation on Ubuntu 24.04?"
    answer: "No. On kernel 6.17 all 9 run on the kernel's in-tree (in-kernel) drivers (the rtw88 / rtw89 / mt76 families) and are recognized on plug-in; no DKMS module needs to be compiled."
  - question: "Can ALFA adapters run a WPA3-SAE hotspot on Ubuntu?"
    answer: "Yes. All 9 cards were able to set up a WPA3-SAE hotspot and let devices connect (tested on 2.4 GHz for every card except the ACS, which was tested on 5 GHz; the AXML was also tested on 6 GHz); only the AWUS036ACHM needs hostapd's sae_pwe set to 0, otherwise the older iPhone 7 Plus fails to connect."
  - question: "Can Kali Linux users rely on these Ubuntu test results?"
    answer: "Kali Linux is based on the Debian/Ubuntu lineage and uses the same rtw88 / rtw89 / mt76 in-tree drivers, so the driver compatibility and capability matrix here can in principle serve as a reference for Kali users. That said, our test platform was Ubuntu 24.04 and has not been formally re-tested on Kali, so please treat a future re-test as the authoritative result."
draft: false
---

## Summary (TL;DR)

Yupitek (ALFA Network's Taiwan distributor) tested 9 ALFA USB Wi-Fi adapters on the ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17): all 9 work in monitor mode and as an AP, the AWUS036ACH and AWUS036EACS reach 100% packet injection on both bands, and the MT7921-based AWUS036AXM / AWUS036AXML fail injection on this platform.

- **Monitor works on all of them**: all 9 can enter monitor mode; they differ only in reception strength.
- **Injection is the dividing line**: Realtek `rtw88` ACH and EACS hit 100% injection on both bands, with ACS close behind; MT7921's AXM / AXML fail to inject on this platform.
- **End-to-end handshake (capture → export `.22000`) proven on 7 of 9 cards**: ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AP and WPA3-SAE pass on nearly all**: only the AWUS036ACHM needs `sae_pwe=0` to stay compatible with older iPhones.
- **No compilation on ARM64**: all 9 run on the kernel 6.17 in-tree drivers — plug and play, no DKMS.

Yupitek is the Taiwan distributor for ALFA Network. When customers shop for a USB Wi-Fi adapter, the three questions they ask most are almost always the same: "Can this card enter monitor mode in my Linux setup? Can it do injection? Can it run an AP?" Rather than answering from a spec sheet, we put 9 current ALFA adapters on our own bench and tested each one on an **ASUS GX10 (ARM64)** running **Ubuntu 24.04 LTS**. We pulled all four capability lines — Monitor, Injection, AP, WPA3-SAE — into a single comparison, and we honestly flag which cards "can't do what" on this platform.

A word on framing first: every test here was done on Yupitek's own equipment and our own office Wi-Fi, against our own test phones. This is a distributor's hardware validation of product compatibility and capability boundaries, not an attack tutorial aimed at third-party networks. The article provides no procedures for operating against external networks; all injection and handshake work was measured in a self-owned, closed environment against our own devices.

This is a hub-style overview article. The step-by-step configuration and full evidence for each card are split out into dedicated per-card deep dives (see the further reading at the end).

## Test Platform and Method

- **Compute platform**: ASUS GX10 (ARM64 / aarch64)
- **Operating system**: Ubuntu 24.04 LTS
- **Kernel version**: kernel 6.17.0-1014-nvidia
- **Driver strategy**: all 9 cards use the kernel's in-tree (in-kernel) driver, recognized the moment they are plugged in; no third-party DKMS module is installed
- **Test device**: Apple iPhone 7 Plus (WPA3-SAE compatibility re-tested with an iPhone 15 Pro)
- **Test environment**: our own office Wi-Fi, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Test window**: live measurements from 2026-11-16 to 2026-11-18

Methodologically, we ran the same flow on every card: first confirm the driver loads and the interface is created (`wlx*`), then verify 2.4GHz / 5GHz monitor, injection, AP and WPA3-SAE connectivity in order, and finally validate the end-to-end handshake capture chain against our own test phone. Every result is recorded as an actually measured number or state, never inferred from a spec sheet.

The tables in this article use the following legend:

> ✅ pass | 🟡 partial or single-node only | ⚠️ limited | ❌ unsupported or test failed | N/A driver lacks this mode | ⬜ not tested (second device missing)

## 1. Hardware and Driver Reference

First, the hardware details of the 9 cards and the driver actually bound on kernel 6.17.

| # | Model | Chipset | USB ID | Driver (in-kernel) | Firmware | Generation / streams | Notes |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | morrownr-recommended Kali card |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R (AC600) | Single antenna |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R (AC1200) | Dual-antenna high gain |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | Lightweight, portable |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi combo |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | Same chip, embedded antenna (Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

A few key points:

**Two driver camps.** The 9 cards split between MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) and Realtek (`rtw88_*` / `rtw89_8852bu`) in-tree drivers. The chip generations span Wi-Fi 5 (6 cards) and Wi-Fi 6 (3 cards: AX and AXER on `rtw89_8852bu`; AXM and AXML on `mt7921u`).

**The most practical advantage on ARM64 is "no compilation."** On kernel 6.17 all 9 run on in-tree drivers and are recognized on plug-in, with no need to deal with out-of-tree DKMS modules on aarch64. This matters a lot on ARM64: many third-party Realtek drivers lack prebuilt aarch64 binaries, so you often have to compile from source and match the kernel version — a high-risk process. These cards skip that entirely.

**Same chip, different models.** The AWUS036AX and AWUS036AXER share the same RTL8832BU and the same `rtw89_8852bu` driver; they differ in antenna design (the AXER uses an embedded Nano antenna with no RP-SMA), which shows up in the reception and injection numbers later.

**Two are BT + WiFi combo devices.** The AWUS036EACS (RTL8821CU) and AWUS036AXML (MT7921AUN) both carry Bluetooth, a trait that has a practical side effect when re-plugging the card — explained later in "Platform notes."

## 2. Core Capability Matrix: Monitor / Injection / AP / WPA3

This is the article's main table, and the first one to look at when choosing a card.

| # | Model | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ broadcast only | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅ (width not confirmed) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 6 | AWUS036AX | ✅ strong | ✅ strong | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ strong | ✅ strong | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ weak | ✅ weak | ❌ **fail** | ❌ **fail** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ weak | ✅ weak | ❌ **fail** | ❌ **fail** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* The AWUS036ACHM's WPA3 needs `sae_pwe=0`; with `sae_pwe=2` the iPhone 7 Plus cannot connect.
>
> WPA3-SAE column: the band shown is the band actually tested (2.4G for all cards except the ACS, tested on 5G; the AXML was also tested on 6G). Other bands were not tested.

Line-by-line reading:

**Monitor: all 9 work, differing in reception strength.** On both 2.4GHz and 5GHz, all 9 can enter monitor mode, with no exceptions. The difference is in scanning aggressiveness and reception sensitivity: the Wi-Fi 6 AX / AXER have the strongest reception and scan most aggressively; the MT7921 AXM / AXML can enter monitor but are relatively weak. For passive side-capture or spectrum surveying, all 9 will do.

**Injection: the gap starts opening here.** The Realtek `rtw88` series performs best: ACH and EACS both reach **100%** on 2.4GHz / 5GHz, and ACS also does 2.4GHz 100% / 5GHz 96%. The MediaTek `mt76` ACM is usable but lands mid-pack (2.4GHz 63–83%, 5GHz 76%); the ACHM's 5GHz can only broadcast and cannot inject at a specific target. The `rtw89` AX / AXER can inject, with the AXER's 2.4GHz injection rate (73%) notably lower than the AX's (96%).

**The most important honest limitation: MT7921 (AXM / AXML) injection fails on this platform.** This is not a case of mistuned parameters, nor an inherent inability of the chip to inject — the main cause is the mac80211 chanctx regression in kernel 6.16+. The community's same-model units can work with a git / patched driver, but the firmware then locks the rate (see morrownr/USB-WiFi #387, morrownr/mt76 #18). Because injection fails on this platform, these two cards cannot deauth and therefore cannot complete the handshake capture chain. For any use that needs injection, rule these two out on this platform.

**AP and WPA3: nearly all pass.** All 9 can act as an AP, and most support 5GHz VHT80 (80MHz); WPA3-SAE connections also all succeed on the band tested (see the note under the table). The one thing to watch is the AWUS036ACHM: its WPA3 requires hostapd's `sae_pwe` set to 0, otherwise the older iPhone 7 Plus cannot connect (re-tested with an iPhone 15 Pro it connects, so this is a compatibility setting difference).

## 3. Advanced Features and Handshake Capability Summary

Going one layer deeper: end-to-end handshake, virtual interfaces (VIF), active monitor, and mesh / IBSS.

| # | Model | WPA handshake capture | VIF | Active monitor | Ad-hoc (IBSS) | Mesh (802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **end-to-end** (.22000) | ✅ STA+AP / AP+mon | 🟡 configurable, ACK unverified | 🟡 single-node | 🟡 single-node |
| 2 | AWUS036ACHM | ✅ **end-to-end** (.22000, on 5 GHz ch36) | ✅ | 🟡 | 🟡 single-node | 🟡 single-node |
| 3 | AWUS036ACH | ✅ **end-to-end** (.22000) | ✅ STA+mon | ❌ -95 | 🟡 single-node | ❌ -95 |
| 4 | AWUS036ACS | ✅ **end-to-end** (.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **end-to-end** (.22000, 79 ACKs) | 🟡 passive monitor + managed on the same channel (software monitor); no independent dual VIF | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **end-to-end** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **end-to-end** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ injection fail | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ injection fail | ✅ | 🟡 | N/A | N/A |

"End-to-end" here has a precise definition: use the card to perform injection against **Yupitek's own iPhone 7 Plus** (connected to our own `YUPITEK` SSID), capture the complete 4-way handshake (M1–M4), then convert it to hashcat's `.22000` format with `hcxpcapngtool --all`. Whether the whole chain runs through is the real "penetration-testing capability" checkpoint — not merely "can enter monitor."

- **End-to-end passed (7 of 9 cards)**: ACM, ACHM, ACH, ACS, EACS, AX, AXER can all produce a `.22000`. Among them EACS received 79 ACKs, giving the most solid signal feedback; ACH injects at 100% on both bands and, on 2026-11-19, was re-tested to export a `.22000` with 47 hashlines. ACHM completed it on 5GHz (ch36); ACM completed it even though its injection success rate is lower.
- **End-to-end broken**: AXM / AXML have the whole handshake chain broken because injection fails. This again confirms: MT7921 is unsuitable for penetration-testing use on this platform.
- **VIF (coexisting virtual interfaces)**: all 9 support some form of concurrent interfaces; Realtek rtw89 can run STA + AP simultaneously, while the EACS only supports a passive monitor alongside a managed interface on the same channel (software monitor), not independent dual VIFs.
- **Active monitor (with ACK reporting)**: `rtw88`'s ACH / ACS / EACS report -95 (unsupported); `rtw89`'s AX / AXER drivers lack this mode (N/A); `mt76` / `mt7921u` are partially capable (🟡).
- **Mesh (802.11s)**: only the `mt76` ACM / ACHM can establish it single-node (🟡, a second card is needed to fully verify interconnection); Realtek `rtw88` returns -95 unsupported, and the `rtw89` and `mt7921u` drivers lack this mode. For mesh experiments, MediaTek `mt76` is the only option in this batch.
- **IBSS (Ad-hoc)**: the `mt76` ACM / ACHM and the `rtw88` ACH can all join single-node (🟡); EACS lists the iftype but its join is ineffective in testing, and the `rtw89` AX / AXER have no IBSS iftype (N/A).

### Kali / aircrack Tool Compatibility (common across the platform)

The following tools behave at the platform level across all 9 cards, independent of any individual card:

| Tool | Status | Notes |
|---|---|---|
| airmon-ng | ✅ | Detects / manages all cards; **never run `check kill`** (it shuts down NetworkManager and disconnects the GX10) |
| kismet | ✅ | Each card can start as a data source and produce a `.kismet` log |
| bettercap | ✅ | `wifi.recon` and the channel hopper work normally |
| wifite (git 3.0.0) | ✅ | Can scan and build target lists (use the git version; the apt version conflicts with the self-built aircrack-ng) |
| Wireshark / tshark | ✅ | Monitor capture and parsing work normally |
| **hcxdumptool 8.x** | ⚠️ | **All cards fail to arm, except the EACS on 2.4 GHz (5 GHz fails)**: it requires active-monitor, which `rtw88` / `rtw89` / `mt7921u` do not support → switch to `airodump-ng` + `aireplay-ng` |

ARM64 note: `aircrack-ng` must be built from source, and `wifite` is best run from the git 3.0.0 version to avoid dependency conflicts between the apt package and the self-built version.

## 4. Selection Advice by Use Case

Condensing the three tables above into "pick directly by use case."

| Use case | Top pick | Notes |
|---|---|---|
| **Penetration testing (injection + handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | Best dual-band injection (EACS, ACH reach 100%); end-to-end `.22000` corroborated by EACS, ACS, ACH (ACH re-tested 2026-11-19) |
| **Strongest reception / long-range monitor** | **AWUS036AXER** / AWUS036ACH | AXER scanned 63 APs + 12 clients in a single hop; ACH is dual-antenna high gain |
| **Wi-Fi 6 + AP hotspot** | AWUS036AX / AWUS036AXER | 2x2 VHT80, stable AP and usable injection |
| **Pure AP / general connectivity (no injection needed)** | AWUS036AXM / AWUS036AXML | MediaTek connects stably, but **injection fails** — not suitable for pen-testing |
| **mesh / IBSS experiments** | AWUS036ACM / AWUS036ACHM | The `mt76` driver can establish mesh and IBSS single-node (`rtw88`'s ACH can only join IBSS single-node and does not support mesh; `rtw89` declares neither) |

A few plain-language takeaways:

- **For penetration testing and handshake capture**: 7 of 9 cards have an on-file, proven end-to-end `.22000` — **AWUS036EACS** (most solid, 79 ACKs), **AWUS036ACS**, the Wi-Fi 6 AWUS036AX / AWUS036AXER, **AWUS036ACM** and **AWUS036ACHM** (5 GHz), and **AWUS036ACH** (100% dual-band injection, re-tested 2026-11-19 to export a `.22000` with 47 hashlines).
- **For the longest reception range and widest side-capture**: the AWUS036AXER (Wi-Fi 6, embedded Nano antenna design plus chip tuning, most aggressive hopping scan) or the dual-antenna high-gain AWUS036ACH.
- **For running a Wi-Fi 6 hotspot**: the AWUS036AX / AWUS036AXER, 2x2 VHT80 with injection support too.
- **For stable connectivity / plain AP only**: the MediaTek-based AWUS036AXM / AWUS036AXML connect stably and are fine for everyday use.
- **For playing with mesh**: in this batch only the `mt76` AWUS036ACM / AWUS036ACHM can do it (for IBSS single-node, the `rtw88` AWUS036ACH can also join).

**Pitfall to avoid (the single most important line)**: if your use case is **injection or handshake**, **do not pick the AWUS036AXM / AWUS036AXML**. MT7921 fails to inject on the ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17) platform — the main cause is the mac80211 chanctx regression in kernel 6.16+ (not inherent to the chip), not a configuration problem; the community's same-model units can work with a git / patched driver, but the firmware then locks the rate, and on this platform's stock kernel injection still fails. Leave these two for "pure connectivity / pure AP" scenarios.

## 5. Platform Notes (GX10 ARM64 Practice)

These are the practical points common to all 9 cards when operating this batch on an ASUS GX10 + Ubuntu 24.04 (ARM64):

1. **Don't cut off your own network**: absolutely never run `airmon-ng check kill` — it shuts down NetworkManager and disconnects the whole GX10. When operating, touch only the external `wlx*` interface; don't touch the built-in uplink that carries your Internet connection.
2. **Clearing an RX stall**: after repeatedly switching between monitor / AP, if you suddenly can't scan anything, it's usually an RX stall — just unplug and replug the card once to recover (USB re-enumerates, and the interface name is derived from the MAC and won't change).
3. **BT + WiFi combo devices**: EACS and AXML both carry Bluetooth, and on re-plug they occasionally get stuck during WiFi probe and fail to create the `wlx` interface; switching to a different USB port usually fixes it.
4. **Unlocking 5GHz TX**: before doing 5GHz injection in your own environment, set the correct regulatory domain first to unlock TX power, then set it back to the local domain after testing. This is the prerequisite for whether 5GHz transmits normally.
5. **A handshake-capture tip**: the office often has multiple APs with the same name, so in practice it's more reliable not to lock onto a single BSSID but to capture the whole channel, using `hcxpcapngtool --all` for conversion.
6. **hcxdumptool fails to arm across the platform (the exception is the EACS on 2.4 GHz)**: the three-band built-in cards and the drivers above do not support active-monitor, so switch directly to the aircrack-ng suite (`airodump-ng` + `aireplay-ng`).
7. **ARM64 build details**: `aircrack-ng` must be built from source, and `wifite` uses the git version to bypass apt dependency conflicts.

To reiterate the framing: all of the injection / deauth / handshake capabilities above were measured in Yupitek's own closed environment against our own test devices, for the purpose of validating product capability and compatibility boundaries. This article does not provide, nor recommend, performing any of the above against any third-party network.

## Conclusion

On the ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17) platform, the overall verdict on the 9 ALFA cards boils down to three sentences: **Monitor works on all of them, AP and WPA3 pass on nearly all, and the dividing line is Injection.** For professional uses needing injection and handshake, the Realtek `rtw88` EACS / ACH / ACS are the most reliable picks; for reception and Wi-Fi 6, look to the AXER / AX; leave the MT7921 AXM / AXML for pure-connectivity scenarios. No compilation, plug and play — that's this batch's biggest shared advantage on ARM64.

## Frequently Asked Questions (FAQ)

**Q: Can the AWUS036AXM do injection on Ubuntu?**
A: Not on this platform. In our testing, both the AWUS036AXM and AWUS036AXML (both MT7921 chips) failed injection on 2.4GHz and 5GHz, mainly due to the mac80211 chanctx regression in the stock kernel 6.16+ (not inherent to the chip). We therefore don't recommend them on this platform for any use that needs injection or handshake capture.

**Q: Which ALFA adapter has the highest injection success rate on Ubuntu?**
A: In testing, the AWUS036ACH and AWUS036EACS both reached 100% injection success on 2.4GHz and 5GHz, the best two of the 9 cards in this batch.

**Q: Do the 9 ALFA adapters need extra driver installation on Ubuntu 24.04?**
A: No. On kernel 6.17 all 9 run on the kernel's in-tree (in-kernel) drivers (the rtw88 / rtw89 / mt76 families) and are recognized on plug-in; no DKMS module needs to be compiled.

**Q: Can ALFA adapters run a WPA3-SAE hotspot on Ubuntu?**
A: Yes. All 9 cards were able to set up a WPA3-SAE hotspot and let devices connect (tested on 2.4 GHz for every card except the ACS, which was tested on 5 GHz; the AXML was also tested on 6 GHz); only the AWUS036ACHM needs hostapd's `sae_pwe` set to 0, otherwise the older iPhone 7 Plus fails to connect.

**Q: Can Kali Linux users rely on these Ubuntu test results?**
A: Kali Linux is based on the Debian/Ubuntu lineage and uses the same rtw88 / rtw89 / mt76 in-tree drivers, so the driver compatibility and capability matrix here can in principle serve as a reference for Kali users. That said, our test platform was Ubuntu 24.04 and has not been formally re-tested on Kali, so please treat a future re-test as the authoritative result.

## Further Reading

This is the overview hub. The following deep dives and per-card tests are coming online (links under construction):

- "No Driver Install: Enabling Monitor and AP Mode on Ubuntu (ARM64)" → [`/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- "WPA3-SAE Handshake Capture in Practice (validated in a self-owned environment)" → [`/en/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 per-card deep-dive tests:

- [AWUS036ACM single-card test](/en/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM single-card test](/en/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH single-card test](/en/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS single-card test](/en/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS single-card test](/en/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX single-card test](/en/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER single-card test](/en/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM single-card test](/en/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML single-card test](/en/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*Testing unit: Yupitek (ALFA Network Taiwan distributor) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Test device: Apple iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro) | Test environment: our own office Wi-Fi. This article is product compatibility and capability validation, not an operating tutorial aimed at third-party networks.*
