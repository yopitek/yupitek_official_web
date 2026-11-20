---
title: "AWUS036ACH Single-Card Test: Realtek RTL8812AU Dual-Antenna AC1200 on ASUS GX10 (ARM64 / Ubuntu 24.04) — Full Monitor, Injection, AP, WPA3 Report"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH (RTL8812AU) needs no DKMS on Ubuntu 24.04 / kernel 6.17; dual-band monitor mode works, packet injection is 100%, end-to-end WPA handshake (.22000) is proven, and limitations like 5G receive lockup are documented."
faq:
  - question: "Does AWUS036ACH need a driver on Kali or Ubuntu?"
    answer: "It depends on the kernel version. Linux kernel 6.13 and above (this round tested Ubuntu 24.04 / kernel 6.17) already ships the rtw88_8812au driver built in — recognized on plug-in, no compiling, no DKMS; only kernels below 6.13 need a separate DKMS install of lwfinger/rtw88. On Kali, confirm the kernel version with uname -r first; we did not verify it on real Kali hardware this time."
  - question: "How do monitor mode and packet injection perform on AWUS036ACH?"
    answer: "Both 2.4GHz and 5GHz can enter monitor mode; aireplay-ng per-AP directed injection is 30/30 = 100% on both 2.4GHz (against 4 APs) and 5GHz (against YUPITEK ch36). Before 5GHz injection, set the regulatory domain to one that allows transmission (e.g. iw reg set US); under the default country 00, 5GHz transmission is forbidden and injection won't go out."
  - question: "Can AWUS036ACH capture a WPA handshake?"
    answer: "Yes, and it's proven end-to-end. Injection is 100% on both bands; a 2026-11-19 retest on our own iPhone 15 Pro at 5GHz ch36 captured a complete 4-way handshake, and hcxpcapngtool exported 47 hashcat .22000 hashlines. Only on networks you own or are authorized to test."
  - question: "What should I do if the iPhone 7 Plus can't connect to AWUS036ACH's WPA3 hotspot?"
    answer: "hostapd must be set to sae_pwe=0 together with ieee80211w=2 for the iPhone 7 Plus to connect; sae_pwe=2 won't connect. The same setting is also key on the AWUS036ACHM."
  - question: "What should I do if AWUS036ACH's 5GHz reception suddenly locks up (captures 0 packets)?"
    answer: "This is a known behavior of rtw88_8812au: after repeatedly switching modes or changing the regulatory domain, 5GHz reception may lock up and cannot be recovered in software — only a physical re-plug or reboot works. We recommend re-plugging the card before 5GHz testing and completing the 5GHz items first."
draft: false
---

> Tested by: Yopitek (ALFA Network's Taiwan distributor) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Test device: our own Apple iPhone 7 Plus | Test target: our own office Wi-Fi (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157) | Test date: 2026-11-18.
>
> This article is a distributor's hardware verification of product compatibility and capability boundaries: all Monitor / Injection / AP / handshake measurements were performed on Yopitek's own equipment, our own office Wi-Fi, against our own test phones; it does not target any third-party network, nor does it provide attack procedures against external networks. All data are numbers and states measured on real hardware, not inferred from spec sheets.

## TL;DR

On the ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), the AWUS036ACH works in dual-band monitor mode, reaches 30/30 = 100% per-AP packet injection on both bands, and runs an AP hotspot on both bands (pure 802.11g / pure 802.11a).

- Kernel 6.13 and above needs no DKMS install (this round Ubuntu 24.04 / kernel 6.17); rtw88_8812au is built in and recognized on plug-in.
- Dual-band monitor mode works; per-AP packet injection on both bands is 30/30 = 100%.
- End-to-end WPA handshake is proven: a 2026-11-19 retest on our own iPhone 15 Pro at 5G ch36 captured a complete 4-way and exported 47 .22000 hashlines.
- 5GHz reception may lock up; only a physical re-plug or reboot recovers it.
- Single-node IBSS can be created, but 802.11s mesh, active monitor, and Wi-Fi Direct (P2P) are not supported.

## 1. This Card and the Test Platform

The AWUS036ACH is ALFA Network's "dual-antenna high-gain" USB wireless NIC, built on the Realtek RTL8812AU chip, spec'd as Wi-Fi 5 (802.11ac), 2T2R, dual-band AC1200. Compared with the single-antenna AWUS036ACHM (MediaTek MT7610U, AC600) in the same series, the ACH trades two external high-gain antennas for better reception and steadier injection performance, making it a common candidate when customers ask about "long-range monitor" and "dual-band injection."

The test platform and conditions this round are as follows:

- Compute platform: ASUS GX10 (ARM64 / aarch64)
- Operating system: Ubuntu 24.04 LTS
- Kernel version: kernel 6.17.0-1014-nvidia
- Test device: Apple iPhone 7 Plus (2.4G / 5G / WPA3 all tested on this device)
- Test environment: our own office Wi-Fi, SSID `YUPITEK` (2.4GHz ch5 / 5GHz ch36, ch157)
- Test date: hands-on measurement on 2026-11-18

Throughout, we only operate the `wlx*` interface belonging to the ALFA card, never touch the GX10's built-in upstream NIC, and never run `airmon-ng check kill` (that command shuts down NetworkManager and takes the host offline).

## 2. Hardware and Driver (chip / USB ID / in-kernel, no install)

| Item | Spec |
|---|---|
| Model | AWUS036ACH |
| Chipset | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| Driver | `rtw88_8812au` (kernel built-in, mainline ≥ 6.13) |
| Firmware | `rtw88/rtw8812a_fw.bin` (bundled with the system) |
| Generation / Streams | Wi-Fi 5 (802.11ac) / 2T2R |
| Bandwidth class | Dual-band AC1200 |
| Antenna | Dual-antenna high-gain (external) |
| USB interface | USB 3.0 (enumerated as 5000M in testing) |

On the GX10's 6.17 kernel, the ACH is genuinely plug-and-play: `lsusb` sees `0bda:8812`, the `rtw88_8812au` driver binds automatically, the firmware `rtw8812a_fw.bin` is already bundled with the system, no compiling, no DKMS. This matters especially for ARM64 environments. Many old out-of-tree Realtek drivers have to be compiled from source on aarch64, whereas the two long-running projects morrownr/USB-WiFi and aircrack-ng/rtl8812au now both redirect to this built-in driver, with bug reports consolidated to lwfinger/rtw88. So users on kernel ≥ 6.13 (including the GX10's 6.17) no longer need to touch third-party DKMS; only old kernels (< 6.13) need a separate DKMS install of `lwfinger/rtw88`. This upstream project is still actively maintained (the latest commit is 2026-10-24, with content including a Bluetooth 1T1R fix for the 8812A), meaning mainline support for this chip is still being updated — not a stale old driver.

One detail to note for the hardware connection: the ACH has a USB-A male plug, so use a USB-C→A adapter to plug it directly into the GX10's USB-C port, over USB 3.0 (enumerated as 5000M). If you connect it behind a USB 2.0 hub shared with keyboard/mouse, it will be rate-limited and you can't measure USB3 behavior.

On interface modes, `iw phy` reports support for IBSS / managed / AP / AP-VLAN / monitor, but not mesh, P2P, or active-monitor — this line directly determines some of the limitations in Section 4.

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

| Feature | 2.4 GHz | 5 GHz | Measured data |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames; 5G ch36/149/157 = 260/137/127 frames |
| Injection (broadcast probe) | ✅ | ✅ | `aireplay-ng --test` broadcast probe returns Injection is working on both bands |
| Injection (per-AP directed) | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G against 4 APs (including YUPITEK); 5G against YUPITEK ch36 |
| AP hotspot (iPhone 7 Plus) | ✅ pure 802.11g | ✅ pure 802.11a (ch36) | 4-way handshake completed, connected on first try |
| WPA3-SAE AP | ✅ (`sae_pwe=0`) | Not tested | With `ieee80211w=2`, iPhone 7 Plus connects (tested on 2.4 GHz only) |

**Monitor**: on 2.4GHz, ch1 / ch6 / ch11 captured 92 / 214 / 71 frames respectively; on 5GHz, ch36 / ch149 / ch157 captured 260 / 137 / 127 frames. Monitor is normal on both bands, and 5GHz's capture count is even higher than 2.4GHz's (ch36 captured 260 frames), consistent with the dual-antenna high-gain positioning.

**Injection**: this is the ACH's strength. On 2.4GHz, `aireplay-ng --test` first does a broadcast probe (reporting Injection is working, Found 4 APs), then goes per-AP directed, with response rates of 30/30 = 100% against all 4 APs including YUPITEK, min/avg/max RTT about 4.9 / 39.2 / 99.0 ms, Power about -47. The dual-antenna ACH's 2.4G injection is clearly steadier than the single-antenna ACHM. In practice, remember to add `--ignore-negative-one`: this is a known behavior from lwfinger/rtw88 #453 — with the STA interface up, the monitor channel may report `-1`, and without this flag it would be misjudged as an injection failure. Also, per upstream records, under heavy-load injection the built-in driver occasionally does a USB reset, but we did not observe it in this roughly 90-second measurement. On 5GHz, per-AP directed against YUPITEK (ch36) is likewise 30/30 = 100%, average RTT 13.6 ms, Power -69.1. This was measured under the premise of "freshly plugged card + regdomain set to one that allows TX" (details in Section 4's 5G notes).

**AP hotspot**: running the AP with hostapd, 2.4GHz on pure 802.11g (`ieee80211n=0`) and 5GHz on pure 802.11a (ch36), the iPhone 7 Plus connected on the first try on both bands with no association failure; the log shows the complete four steps authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED. Experience shows the ACH connects cleanest under a "802.11n off, pure g / pure a" config.

**WPA3-SAE**: when running a SAE-only AP, the key parameters are `sae_pwe=0` (hunting-and-pecking) with `ieee80211w=2` for the iPhone 7 Plus to connect; using `sae_pwe=2` won't connect. This is the same compatibility trap that the same-series ACHM hit.

## 4. Advanced Capabilities and Handshake: Feasible Range and Honest Limitations

| Advanced Capability | Result | Notes / Evidence |
|---|---|---|
| VIF (STA + monitor at once) | ✅ tested, works | Main managed interface and `mon9` (monitor) up at the same time; the monitor VIF captured 100 frames in 8 seconds |
| WPA handshake capture | ✅ end-to-end (.22000) proven | Injection 100% on both bands; 2026-11-19 retest at 5G ch36 captured a complete 4-way, hcxpcapngtool exported 47 `.22000` hashlines |
| macchanger (change MAC) | ✅ | Random MAC set and restore both normal (requires `ip link down` first) |
| Ad-hoc (IBSS) | 🟡 single-node | Single-node `Joined IBSS` succeeded; peer link untested for lack of a second device |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh (802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct (P2P) | ❌ | `Operation not supported (-95)` |

**Handshake capture capability, to be clear**: the ACH's injection is 100% on both bands, and injection is exactly the trigger end of the end-to-end workflow "deauth our own test phone → capture a complete 4-way (M1–M4) → export a hashcat `.22000` with hcxpcapngtool." A 2026-11-19 retest on our own iPhone 15 Pro at 5GHz ch36 captured a complete 4-way handshake and exported 47 `.22000` hashlines with hcxpcapngtool, so the ACH's end-to-end handshake capture is proven. In our nine-card master table, 7 of 9 cards have end-to-end (`.22000`) proven: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX, and AWUS036AXER. All captures are limited to networks you own or are authorized to test.

**VIF**: the `iw phy` flag says interface combinations are not supported, but on real hardware the managed main interface and a separately created monitor interface `mon9` can be up at once, and `mon9` captured 100 frames within 8 seconds — meaning "capture while online" works on the ACH. One caveat: the phy does not guarantee this combination, so for long-duration or heavy-load scenarios we recommend the mt76 series (ACM / ACHM) instead.

**Three limitations to specifically flag:**

1. **No support for Active monitor, Mesh (802.11s), or Wi-Fi Direct (P2P)**: all three return `Operation not supported (-95)` in testing. For these three capabilities, use the mt76 series cards instead (the ACM / ACHM phy declares mesh / P2P / active-monitor).
2. **5G RX lockup (`rtw88_8812au` known behavior)**: 5G monitor / injection is normal right after plugging in, but after repeatedly switching modes or changing the regdomain, 5G reception may lock up (captures 0 packets), and cannot be recovered in software — only a physical re-plug or reboot works. We recommend re-plugging once before 5G testing and completing the 5G items first. Also a note on the premise for 5G injection to transmit: under the default `country 00`, 5G is all passive / no-IR (TX forbidden), so directed injection simply can't go out; set a regulatory domain that allows TX (`iw reg set US` unlocks ch36 / ch149; `TW` only allows ch149 and above, not ch36), then set it back to `TW` after testing. And "freshly plugged card" means a physical re-plug to USB re-enumeration: `dmesg` must show `USB disconnect` and `renamed from wlan0` with a changed bus number to count; if 5G has already locked up, aireplay returns `No such BSSID available`.
3. **hcxdumptool `failed to arm` on all cards on this platform except the AWUS036EACS on 2.4 GHz**: because it needs active-monitor, which rtw88 / rtw89 / mt7921u all do not support; to capture a handshake, use the airodump-ng + aireplay-ng route instead.

### Toolchain Compatibility (Kali)

We ran a quick screen of common Kali tools against the ACH (with our own `YUPITEK` as the target environment); the results are as follows:

| Tool | Status | Notes |
|---|---|---|
| airmon-ng | ✅ | Correctly lists `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` captured beacons (including YUPITEK), 20 packets captured |
| kismet | ✅ installed | `/usr/bin/kismet`, can start as a data source |
| bettercap | ✅ installed | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | Installed, but `failed to arm` on this platform (needs active-monitor, see above) |
| macchanger | ✅ | GNU 1.7.0; `-r` random, `-p` restore, both work in testing |
| wifite | ❌ not installed | Not present on this machine, needs a separate install (the git version is recommended, to avoid an apt dependency conflict with the self-compiled aircrack-ng) |

The conclusion is simple: airmon-ng can correctly identify and manage the ACH, and for general monitor and capture flows the aircrack-ng suite (airodump-ng + aireplay-ng) is the most stable; hcxdumptool, which needs active-monitor, can't arm on this platform, so don't get stuck on it.

## 5. Use Cases and Selection Advice (back to the master-table Hub)

Placing the ACH back into the whole product line, its positioning is clear: dual-antenna high-gain, 100% injection on both bands, end-to-end WPA handshake (.22000) proven — a practical choice for customers who "need stable injection and also want stronger reception."

- **Penetration testing (injection + handshake)**: the first-choice group is AWUS036EACS / AWUS036ACH / AWUS036ACS, all three with high-end injection on both bands.
- **Strongest reception / long-range monitor**: the AWUS036AXER and AWUS036ACH, with the ACH excelling via dual-antenna high gain.
- **Need 802.11s mesh / active-monitor / P2P**: the ACH (Realtek rtw88) can't do it (tests return `-95`); use the mt76-driver AWUS036ACM / AWUS036ACHM instead; the ACH's IBSS is single-node only, peer-link untested.
- **Only need pure AP or general connectivity, no injection**: the MediaTek AWUS036AXM / AXML are steadier, but note their injection fails on this platform, making them unsuitable for pentest use.

A one-line trap warning: if the customer's need is clearly injection and handshake, don't choose the AWUS036AXM / AXML (the MT7921 chip's injection fails in testing on this platform and cannot deauth or capture a handshake); for that need the ACH is instead a safe candidate. When selecting, don't look only at bandwidth numbers — the reception stability from dual-antenna high gain often makes a more noticeable difference at real capture distances than paper specs. For selection decisions and platform-common traps, see the master-table Hub: [Full Monitor, Injection, AP Matrix of 9 ALFA Wireless NICs on ASUS GX10 (ARM64)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## FAQ

**Q: Does AWUS036ACH need a driver on Kali or Ubuntu?**
It depends on the kernel version. Linux kernel 6.13 and above (this round tested Ubuntu 24.04 / kernel 6.17) already ships the rtw88_8812au driver built in — recognized on plug-in, no compiling, no DKMS; only kernels below 6.13 need a separate DKMS install of lwfinger/rtw88. On Kali, confirm the kernel version with uname -r first; we did not verify it on real Kali hardware this time.

**Q: How do monitor mode and packet injection perform on AWUS036ACH?**
Both 2.4GHz and 5GHz can enter monitor mode; aireplay-ng per-AP directed injection is 30/30 = 100% on both 2.4GHz (against 4 APs) and 5GHz (against YUPITEK ch36). Before 5GHz injection, set the regulatory domain to one that allows transmission (e.g. iw reg set US); under the default country 00, 5GHz transmission is forbidden and injection won't go out.

**Q: Can AWUS036ACH capture a WPA handshake?**
Yes, and it's proven end-to-end. Injection is 100% on both bands; a 2026-11-19 retest on our own iPhone 15 Pro at 5GHz ch36 captured a complete 4-way handshake, and used hcxpcapngtool to export 47 hashcat .22000 hashlines. Only on networks you own or are authorized to test.

**Q: What should I do if the iPhone 7 Plus can't connect to AWUS036ACH's WPA3 hotspot?**
hostapd must be set to sae_pwe=0 together with ieee80211w=2 for the iPhone 7 Plus to connect; using sae_pwe=2 won't connect. The same setting is also key on the AWUS036ACHM.

**Q: What should I do if AWUS036ACH's 5GHz reception suddenly locks up (captures 0 packets)?**
This is a known behavior of rtw88_8812au: after repeatedly switching modes or changing the regulatory domain, 5GHz reception may lock up and cannot be recovered in software — only a physical re-plug or reboot works. We recommend re-plugging the card before 5GHz testing and completing the 5GHz items first.

## 6. Further Reading

- Master-table Hub: [Full ARM64 Matrix of 9 ALFA Wireless NICs](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Enabling Monitor and AP with no driver install on Ubuntu (ARM64): [placeholder](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE handshake capture and `sae_pwe` compatibility: [placeholder](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Sister-card comparison: AWUS036ACHM (single-antenna AC600) single-card test [placeholder]
- This model's full evidence path (internal): `AWUS036ACH_evidence/` (p0 enumeration, p1_gx10 behavior, retest troubleshooting)

<!-- hreflang: zh-TW is the master draft; zh-CN / en / ja / ko / de / fr / es to be generated and have rel=alternate added once this draft is finalized. -->
