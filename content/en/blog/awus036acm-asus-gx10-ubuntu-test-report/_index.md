---
title: "AWUS036ACM Card-by-Card Test: MediaTek MT7612U (mt76x2u) on ASUS GX10 + Ubuntu 24.04 (ARM64) — Monitor / Injection / AP and Mesh Capability Report"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM (MT7612U) needs no driver install on Ubuntu 24.04 ARM64; dual-band monitor mode and aircrack-ng (common on Kali) work, packet injection 63–83% on 2.4G and 76% on 5G, with VIF support and single-node mesh / IBSS."
faq:
  - question: "Does AWUS036ACM need a driver on Ubuntu or Kali?"
    answer: "No. The MT7612U is handled by the kernel's built-in mt76x2u driver; Ubuntu 24.04 (kernel 6.17) recognizes it on plug-in with no DKMS and no manual firmware. This round was tested on Ubuntu 24.04 ARM64; Kali should behave the same in principle as long as the kernel is recent enough, but we did not verify it on real Kali hardware this time."
  - question: "Can AWUS036ACM enter monitor mode and do packet injection? What is the success rate?"
    answer: "Yes. Both 2.4GHz and 5GHz can enter monitor mode and capture normally; aireplay-ng injection tests measured 63–83% on 2.4GHz and 76% on 5GHz, mid-pack among the nine cards. For 100% injection on both bands, Yopitek's testing favors the AWUS036ACH and AWUS036EACS."
  - question: "Can AWUS036ACM run a hotspot and stay online at the same time (VIF)?"
    answer: "Yes. We verified both STA+AP (connect upstream on one side while running a hotspot on the other) and AP+monitor (run a hotspot while monitoring). This is where the mt76 driver's multi-interface concurrency is more complete; the 5GHz hotspot can run at VHT 80 MHz."
  - question: "Does AWUS036ACM support mesh (802.11s) and IBSS?"
    answer: "They can be created single-node. On Ubuntu 24.04 / kernel 6.17, AWUS036ACM can bring up 802.11s mesh and IBSS (Ad-hoc) interfaces; but we had no second node this round, so multi-node interconnect is not yet verified, which is why we only claim single-node creation."
  - question: "Can AWUS036ACM capture a WPA handshake?"
    answer: "Yes. Against our own AP and our own iPhone 7 Plus, the end-to-end run succeeded: deauth, a complete 4-way (M1–M4) capture, and a hashcat .22000 export with hcxpcapngtool --all. Only on networks you own or are authorized to test."
draft: false
---

> This article is Yopitek's record of the ALFA AWUS036ACM's product compatibility and capability testing on a current Linux platform, for selection and evaluation.
> Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. All data are excerpts from Yopitek's hands-on testing against **our own equipment and our own office Wi-Fi** (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157) and **our own test phones** (Apple iPhone 7 Plus; WPA3 re-tested with an iPhone 15 Pro).
> ⚠️ **Legal and scope statement**: Monitor, injection, and handshake capture were performed only on networks and devices we own or are authorized to test; AP mode must comply with local radio regulations. This article focuses on the card's own capabilities, compatibility, and configuration, and **does not involve any attack operations against third-party networks**.

## TL;DR

On the ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), Yopitek (ALFA Network's Taiwan distributor) measured the AWUS036ACM working in dual-band monitor mode, with packet injection at 63–83% on 2.4G and 76% on 5G, and as an AP hotspot on both bands (5G at VHT 80 MHz).

- No driver install on Ubuntu 24.04 (ARM64): the MT7612U is handled by kernel 6.17's built-in mt76x2u, recognized on plug-in, no DKMS.
- Dual-band monitor mode works; packet injection is 63–83% on 2.4G and 76% on 5G, mid-pack among the nine cards.
- Single-node 802.11s mesh and IBSS can be created, with VIF support (STA+AP, AP+monitor).
- WPA handshake capture is end-to-end (complete 4-way, exported to hashcat `.22000`); one of 7 of the 9 cards that completed it.
- For 100% injection on both bands, we recommend the AWUS036ACH or AWUS036EACS instead.

---

## 1. This Card and the Test Platform

The AWUS036ACM is a MediaTek dual-band card in ALFA's lineup, built on the MT7612U, Wi-Fi 5 (802.11ac), 2T2R dual spatial streams, dual-band 2.4GHz / 5GHz. It has long been listed as a recommended Kali card on morrownr's list — not for throughput numbers, but because the `mt76` driver family's support for Linux monitor, injection, and multi-interface concurrency (VIF) is relatively complete; on this platform, experimental modes like 802.11s mesh only come up on the mt76 camp (Realtek cards can only create single-node IBSS and cannot bring up mesh). So when evaluating this card, the point is not speed but whether the capability surface is complete, whether mt76's strengths actually materialize, and which items have to be honestly marked as boundaries.

This round reuses the same operational scenario: the GX10's built-in NIC (`wlP9s9`) handles upstream connectivity, while the AWUS036ACM connects over USB and carries only the test workload; switching to monitor or AP never touches the host's own network. Throughout, we only operate the `wlx*` interface belonging to the ALFA card and never touch the built-in upstream NIC.

| Item | Details |
|---|---|
| Model | AWUS036ACM |
| Chipset | MediaTek MT7612U (Wi-Fi 5 / 802.11ac, 2T2R dual-stream) |
| Driver | `mt76x2u` (in-kernel, built into kernel 6.17) |
| Generation / Streams | Wi-Fi 5 / 2T2R |
| Note | morrownr-recommended Kali card |
| Platform | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Test device | Apple iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro) |
| Test environment | Our own office Wi-Fi, SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157 |

> This round's master table does not record the USB ID or firmware version fields for the AWUS036ACM (marked "—"), so this article does not speculate on those two values; all capability data below follow the ACM rows of the master table.

---

## 2. Hardware and Driver (No Install)

This card is recognized on plug-in on the GX10, with no compilation and no DKMS. The MT7612U is handled directly by the mainline kernel's built-in `mt76x2u` driver, with no need for any out-of-tree project and no need to manually load a firmware blob. For ARM64, this is mt76's most practical benefit. Many third-party Realtek drivers have no prebuilt for aarch64 and have to be compiled against the kernel version yourself; mt76 is in-kernel, so a kernel upgrade won't get stuck on a driver dependency.

After plugging in, the interface is named `wlx` + MAC (e.g. `wlxXXXXXXXXXXXX`); the name is bound to the MAC and stays the same across re-plugs, which makes it easy to pin in scripts. To confirm driver binding and interface creation, use the generic checks below (interface names and phy numbers differ per machine):

```bash
# Find the ALFA card's interface name (only pick wlx-prefixed, leave built-in wlP9s9 alone)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# Confirm the bound driver is mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# List the interface modes this phy declares support for (determines which capabilities are usable later)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

Per this round's testing, `mt76x2u`'s available interface modes are more complete than Realtek's `rtw88`: beyond managed / AP / monitor, IBSS and mesh point can also be brought up single-node (see Section 4). This is the foundation for the ACM running mesh / IBSS single-node later; the Realtek cards on the same platform (such as the AWUS036ACH), though they can also create single-node IBSS, cannot bring up 802.11s mesh or active monitor on this platform.

---

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

First the core capability summary (taken from row 1 of the nine-card master table), then each item in detail. All items were completed against our own `YUPITEK` AP and our own iPhone 7 Plus.

| Capability | 2.4 GHz | 5 GHz | Notes |
|---|---|---|---|
| Monitor (receive capture) | ✅ | ✅ | Both bands can enter monitor and capture normally |
| Injection (packet injection) | ✅ 63–83% | ✅ 76% | Injection success rate in the standard injection test |
| AP hotspot (hostapd) | ✅ | ✅ 80MHz | 5G can run at VHT 80 MHz |
| WPA3-SAE (AP side) | ✅ | Not tested | WPA3-SAE was tested on 2.4 GHz only; 5 GHz was not tested |

### 3-1. Monitor (2.4 GHz + 5 GHz) ✅

Both 2.4 GHz and 5 GHz can enter monitor normally and capture packets — the least contentious capability of this card. For a 2T2R dual-antenna card, reception on both bands is stable, enough to support on-site channel surveys and packet diagnostics.

### 3-2. Injection (packet injection) ✅ (mid-pack level)

Measuring packet-injection reliability with the standard injection test, the AWUS036ACM is 63–83% on 2.4 GHz and 76% on 5 GHz. Among the nine cards it is mid-pack, clearly behind the Realtek RTL8812AU (AWUS036ACH, 100% on both bands) and RTL8821CU (AWUS036EACS, 100% on both bands), but fully functional and sufficient in practice. The ACM can inject, just not with the highest stability in class; if a customer puts "top injection success rate" first, it isn't the first choice (see Section 5 on selection).

One configuration detail to note before 5 GHz injection: the default regulatory domain locks active transmission on part of the UNII bands, so before testing you must switch the regulatory domain to a setting that allows transmission, then set it back to the local domain afterward (`iw reg set US` → test → `iw reg set TW`). This is a prerequisite for 5 GHz transmission and is unrelated to the card's own capability.

### 3-3. AP Hotspot and WPA3-SAE ✅

The AWUS036ACM can act as an AP, on both 2.4 GHz and 5 GHz, and 5 GHz can even run at 80 MHz bandwidth (VHT80). With WPA3-SAE enabled on the AP side on 2.4 GHz, our own test phone connects normally (5 GHz WPA3 was not tested).

It's worth contrasting with the single-antenna model AWUS036ACHM, also mt76: the ACHM's WPA3 specifically requires setting hostapd's `sae_pwe` to 0, or the iPhone 7 Plus cannot connect. The AWUS036ACM did not hit this limitation this round — WPA3-SAE works directly.

---

## 4. Advanced Capabilities: VIF / Mesh / IBSS Single-Node and Limitations

Going one level deeper into handshake, virtual interfaces (VIF), active monitor, and mesh / IBSS. This section is also where the AWUS036ACM pulls ahead of the Realtek cards.

| Advanced Item | ACM Result | Notes |
|---|---|---|
| WPA handshake capture | ✅ end-to-end (.22000) | Deauth our own iPhone 7 Plus, capture a complete 4-way M1–M4, export hashcat `.22000` |
| VIF (multi-interface concurrency) | ✅ STA+AP / AP+mon | Can run STA+AP or AP+monitor simultaneously |
| Active monitor | 🟡 configurable, ACK not verified | Mode can be created, ACK reply behavior not verified |
| Ad-hoc (IBSS) | 🟡 single-node | Interface creatable single-node, interconnect needs a second node |
| Mesh (802.11s) | 🟡 single-node | Interface creatable single-node, interconnect needs a second node |
| Wi-Fi Direct (P2P) | ⬜ needs second node | Not tested this round |

### 4-1. VIF (virtual interface concurrency) — the ACM's strength ✅

This card can run two virtual interfaces at once. This round we verified both STA+AP (connect upstream on one side, run a hotspot on the other) and AP+monitor (run a hotspot on one side, monitor on the other), suitable for scenarios like "connect and observe at once" or "one card acting as both client and base station." This is where the `mt76` driver's multi-interface concurrency is more complete.

### 4-2. Mesh / IBSS "single-node OK" — mt76's key difference 🟡

The AWUS036ACM can bring up 802.11s mesh and ad-hoc (IBSS) interfaces single-node; Realtek `rtw88` / `rtw89` (AWUS036ACH, AWUS036AX, etc.), though they can also create single-node IBSS, do not support 802.11s mesh on this platform. So for 802.11s mesh experiments, the mt76 cards (ACM / ACHM) have a starting point the Realtek cards lack.

To mark the boundary clearly: what this round confirmed is "the interface can be created single-node"; full multi-node interconnect still needs a second card / second node, which has not been done, so this is marked 🟡 (single-node) rather than ✅.

### 4-3. Honest Capability Boundaries

- **handshake**: the ACM completed the full end-to-end chain (deauth our own device → capture a complete 4-way M1–M4 → `hcxpcapngtool --all` to export a hashcat `.22000`), even though its injection success rate (2.4G 63–83% / 5G 76%) is lower than the Realtek cards'.
- **active monitor**: the mode can be set up, but the ACK reply behavior was not verified this round (marked 🟡). Relatedly, platform-level `hcxdumptool` 8.x `failed to arm` on all cards except the AWUS036EACS on 2.4 GHz (it wants active-monitor, which this platform's tri-band built-in and current drivers do not provide), so the ACM's handshake flow uses `airodump-ng` + `aireplay-ng` instead.
- **Wi-Fi Direct (P2P)**: not tested this round, needs a second device.

### 4-4. Platform Operation Notes (GX10 ARM64, ACM-related)

1. **Don't cut off your own network**: never run `airmon-ng check kill` (it shuts down NetworkManager and takes the GX10 offline); only touch `wlx*`, never the built-in upstream `wlP9s9`.
2. **RX stall recovery**: if after repeatedly switching monitor / AP you suddenly can't scan anything, just **unplug and re-plug the card once** to recover (USB re-enumerates; the interface name is MAC-determined and unchanged).
3. **5 GHz TX unlock**: before doing 5 GHz injection, set the correct regulatory domain to unlock TX power, and set it back to the local domain after testing.
4. **handshake capture tips**: offices often have multiple same-name APs, so in practice it's more stable not to lock a single `--bssid` and to capture the whole channel instead; use `hcxpcapngtool --all` for conversion.
5. **ARM64 toolchain**: `aircrack-ng` must be compiled from source; use `wifite` git 3.0.0 (to bypass apt dependency conflicts).

Platform-level Kali tools (`airmon-ng`, `kismet`, `bettercap`, the `wifite` git version, Wireshark / tshark) can all use the ACM as a data source normally; the only exception is the aforementioned `hcxdumptool`, which needs active-monitor.

---

## 5. Use Cases and Selection (back to the Hub)

Mapping the above capabilities back to product positioning, the AWUS036ACM's role is actually quite clear: a Wi-Fi 5 2T2R card that is capability-balanced, driverless, and uniquely has mt76's mesh / IBSS / VIF advantages. So where should it be used?

- **First choice for mesh (802.11s) experiments**: among these nine cards, only the mt76 ACM / ACHM can create an 802.11s mesh interface single-node; Realtek `rtw88` / `rtw89` can create single-node IBSS but do not support 802.11s mesh. For mesh experiments, the ACM is the right starting point.
- **When you need VIF concurrency**: STA+AP and AP+monitor both work, suitable for one card acting as both client and AP, or monitoring while connected.
- **When you value driverless operation**: in-kernel `mt76x2u`, kernel upgrades don't get stuck on drivers, and it spares you compiling out-of-tree modules on ARM64.
- **Cases where it isn't the best fit**: if the core need is "highest injection success rate," the ACM's injection (2.4G 63–83% / 5G 76%) isn't the highest in class — we recommend the Realtek AWUS036EACS / ACH / ACS instead; if you're after the strongest reception / long-range monitor, look at the AWUS036AXER / ACH.

Compared with the same family, the positioning differences are as follows:

| Need | Recommended Card | Reason |
|---|---|---|
| mesh (802.11s) single-node experiment | **AWUS036ACM** / AWUS036ACHM | `mt76` driver can create 802.11s mesh single-node (Realtek can only do single-node IBSS, no mesh) |
| VIF concurrency (STA+AP / AP+mon) | **AWUS036ACM** | Multi-interface concurrency works |
| 100% injection on both bands / end-to-end handshake | AWUS036EACS, AWUS036ACH, AWUS036ACS | Best injection on both bands, `.22000` end-to-end already proven |
| Strongest reception / long-range monitor | AWUS036AXER, AWUS036ACH | Frequency-hop to more targets / dual-antenna high gain |

Selection in one line: to play with mesh / IBSS, to want VIF concurrency, and to want driverless operation, the AWUS036ACM is the best-fit mt76 card in this batch; for 100% injection on both bands, go toward the EACS / ACH. For the full nine-card cross comparison and selection decisions, see the [ALFA Wireless NIC Overall Review Hub (nine-card master table)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## FAQ

**Q: Does AWUS036ACM need a driver on Ubuntu or Kali?**
No. The MT7612U is handled by the kernel's built-in mt76x2u driver; Ubuntu 24.04 (kernel 6.17) recognizes it on plug-in with no DKMS and no manual firmware. This round was tested on Ubuntu 24.04 ARM64; Kali should behave the same in principle as long as the kernel is recent enough, but we did not verify it on real Kali hardware this time.

**Q: Can AWUS036ACM enter monitor mode and do packet injection? What is the success rate?**
Yes. Both 2.4GHz and 5GHz can enter monitor mode and capture normally; aireplay-ng injection tests measured 63–83% on 2.4GHz and 76% on 5GHz, mid-pack among the nine cards. For 100% injection on both bands, Yopitek's testing favors the AWUS036ACH and AWUS036EACS.

**Q: Can AWUS036ACM run a hotspot and stay online at the same time (VIF)?**
Yes. We verified both STA+AP (connect upstream on one side while running a hotspot on the other) and AP+monitor (run a hotspot while monitoring). This is where the mt76 driver's multi-interface concurrency is more complete; the 5GHz hotspot can run at VHT 80 MHz.

**Q: Does AWUS036ACM support mesh (802.11s) and IBSS?**
They can be created single-node. On Ubuntu 24.04 / kernel 6.17, AWUS036ACM can bring up 802.11s mesh and IBSS (Ad-hoc) interfaces; but we had no second node this round, so multi-node interconnect is not yet verified, which is why we only claim single-node creation.

**Q: Can AWUS036ACM capture a WPA handshake?**
Yes. Against our own AP and our own iPhone 7 Plus, the end-to-end run succeeded: deauth, a complete 4-way (M1–M4) capture, and a hashcat .22000 export with hcxpcapngtool --all. Only on networks you own or are authorized to test.

---

## 6. Further Reading

- Full capability comparison and overall review of the nine ALFA cards → [ALFA Wireless NIC Overall Review Hub (nine-card master table)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- No driver install: enabling Monitor / AP on Ubuntu 24.04 + kernel 6.17 (rtw88 / rtw89 / mt76 tested) (placeholder, link under construction)
- Step-by-step guide to WPA3-SAE and end-to-end handshake capture (placeholder, link under construction)
- The single-antenna model, also mt76 → AWUS036ACHM card-by-card test (placeholder, link under construction)

---

*Tested by: Yopitek (ALFA Network's Taiwan distributor) — https://www.yupitek.com | Test environment: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Test device: Apple iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro)*
