---
title: "Wireless Auditing in the WPA3-SAE Era: Handshake Capture Capability of 9 ALFA Cards, and the sae_pwe iPhone Compatibility Pitfall"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "A hands-on test of ALFA adapters' WPA3-SAE handshake capture capability on Ubuntu (extendable to Kali): injection rates and end-to-end .22000 capture results for 9 cards, the sae_pwe compatibility pitfall, and selection advice."
faq:
  - question: "Can the AWUS036AXM capture a WPA handshake on Ubuntu?"
    answer: "Not on this platform. In testing, the AWUS036AXM and AWUS036AXML (MT7921 chips) fail injection and cannot send a deauth, so the whole 4-way handshake capture chain breaks with it — unsuitable for uses needing handshake capture."
  - question: "Which ALFA adapter captures a WPA handshake most reliably?"
    answer: "In testing the AWUS036EACS was the most solid: 100% injection on both bands, 79 ACKs after deauth, and a successfully exported hashcat-ready .22000 file — the most complete end-to-end validation in the batch."
  - question: "Why can't an old iPhone connect to a WPA3-SAE hotspot?"
    answer: "The key is hostapd's sae_pwe parameter: set to 2 (forced H2E), the iPhone 7 Plus fails to connect; switching back to sae_pwe=0 (Hunting-and-Pecking) lets it complete the 4-way handshake and connect normally."
  - question: "Can you still capture a 4-way handshake in a WPA3 environment?"
    answer: "A pure WPA3-SAE environment forces PMF on (ieee80211w=2), and classic techniques aimed at management frames are blocked; in practice you can still capture a handshake, usually because the target runs a WPA2/WPA3 transition mode rather than pure WPA3."
  - question: "An ALFA adapter's 5GHz injection doesn't test out — is it a hardware problem?"
    answer: "Not necessarily. The default regulatory domain restricts transmit power on some 5GHz bands, causing injection to \"not get sent out\"; in testing, after switching the regulatory domain to a transmit-capable state, the previously failing 5GHz injection became usable. We suggest confirming the regulatory domain setting first before judging whether it's a hardware limitation."
draft: false
---

> Testing unit: Yopitek (ALFA Network Taiwan distributor) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Test device: our own iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro) | Test target: our own office Wi-Fi (SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> This article is a capability and compatibility overview of ALFA Wi-Fi adapters. All Monitor / Injection / handshake capture was performed on Yopitek's own equipment, our own office Wi-Fi, against our own test phone — a distributor's legitimate hardware capability validation; it targets no third-party network and provides no attack procedures.

## Summary (TL;DR)

On the ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), 7 of the 9 ALFA cards tested (ACM, ACHM, ACH, ACS, EACS, AX, AXER) completed end-to-end WPA handshake capture to `.22000`; the AWUS036EACS reached 100% injection on both bands with 79 ACKs, while the MT7921-based AXM / AXML fail injection on this platform.

- Once WPA3-SAE is widespread, the audit focus shifts from "can it monitor" to "end-to-end handshake capture capability" and "`sae_pwe` endpoint compatibility."
- **End-to-end `.22000` proven on 7 of 9 cards**: ACM, ACHM, ACH, ACS, EACS, AX, AXER; of these, EACS is the most solid (100% dual-band injection, 79 ACKs).
- **AXM / AXML (MT7921) fail injection on this platform**, cannot deauth, and cannot capture a handshake — be sure to avoid them for audit use.
- `sae_pwe` pitfall: older iPhones need `sae_pwe=0` to connect; before 5G injection, `iw reg set US` to unlock TX.
- Pure WPA3 enforces PMF (`ieee80211w=2`); if capture still succeeds in the field, it's usually because the target runs a WPA2/WPA3 transition mode.

## 1. WPA3-SAE Adoption Has Raised the Bar for Wireless Auditing Across the Board

For the past decade, authorized wireless audits almost always revolved around the WPA2-PSK 4-way handshake: capture one complete handshake and the back end can compare it offline. But ever since Wi-Fi 6 certification made WPA3 mandatory, SAE (Simultaneous Authentication of Equals, commonly called Dragonfly) has gradually replaced PSK, narrowing the old road of "capture the handshake, verify offline" more and more.

For distributors and front-line engineers, WPA3-SAE brings three practical changes:

1. **PMF (Protected Management Frame) becomes mandatory.** The WPA3-SAE spec forces `ieee80211w=2` on, so management frames are protected and the classic "toss out a deauth to knock a device offline" approach is blocked outright in a pure WPA3 environment.
2. **Transition mode still keeps the 4-way.** In reality, large numbers of APs run a WPA2/WPA3 mixed transition mode, retaining the WPA2 4-way handshake for backward compatibility with older devices — which is the main reason authorized audits can still capture a handshake today. Whether you can capture one depends heavily on which mode the field target is running.
3. **Endpoint compatibility becomes a new pitfall.** SAE has different password-element derivation methods (controlled by `sae_pwe`), and once an AP parameter is set wrong, even your own old iPhone can't connect — let alone reproduce a client endpoint's connection behavior in an audit setting.

So when a customer asks "which ALFA card can be used for WPA3-related authorized audits," the answer is no longer as simple as "can it monitor." It comes down to two things: **end-to-end handshake capture capability**, and **compatibility with WPA3-SAE parameters and real-device endpoints**. This report is the capability comparison compiled after testing 9 ALFA cards on the same ARM64 platform.

## 2. What "End-to-End Handshake Capture Capability" Means (Conceptual Layer)

Here we first break the capability into three stages, explained purely conceptually, involving no operating commands against any third-party network:

- **Stage 1: Injection (active injection).** The adapter must be able to "send out" specific management frames to prompt an already-connected client to re-associate. Many cards can only passively monitor (receive packets) but cannot inject (actively transmit). This is the stage of the whole chain where you get stuck most easily. This batch quantified the injection success rate with `aireplay-ng --test`, and in the handshake test used the number of ACKs returned by the client to verify the frames actually arrived.
- **Stage 2: 4-way handshake capture.** When the client re-associates, WPA exchanges four EAPOL messages (M1–M4). In monitor mode, the adapter must capture all four frames completely — none can be missing.
- **Stage 3: Export hashcat `.22000`.** Convert the captured pcap to hashcat's `.22000` format with `hcxpcapngtool --all`, handing it to the back end for offline verification.

**Only when all three stages run through on real hardware does it count as "end-to-end"**: actually sending a deauth to our own iPhone 7 Plus (injection) → capturing the complete M1–M4 → exporting a `.22000` on file. Receive-only with no transmit, or an incomplete set of four frames, or a conversion that won't produce a file — none of these count as end-to-end. This article lists no step-by-step attack commands; the comparison below answers just one question: which card makes it all the way through this capability chain.

Taking this batch's most solid card, the EACS, as an example, one successful end-to-end run looks like this: after the deauth is sent the client returns **79 ACKs** (confirming the frames actually reached that phone), `aircrack-ng` determines YUPITEK has 1 handshake, each of the EAPOL M1 / M2 / M3 / M4 four frames is received once, the captured client MAC begins with an Apple OUI (confirming it's that iPhone 7 Plus), and finally `hcxpcapngtool --all` exports a roughly 784-byte `.22000`. Miss any one of these four conditions and the capture doesn't count. This is exactly why "can monitor" and "can capture end-to-end" are two completely different things.

## 3. Handshake Capability Comparison for the 9 Cards

| # | Model | Chip / generation | Injection 2.4G | Injection 5G | WPA handshake capture capability |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 · 2T2R | usable 63–83% | usable 76% | **End-to-end `.22000` proven** (lower injection rate) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 · 1T1R | usable 96–100% | broadcast only | **End-to-end `.22000` proven (on 5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 · 2T2R | **100%** | **100%** | **End-to-end `.22000` proven (re-tested 2026-11-19)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 · 1x1 | **100%** | 96% | **End-to-end `.22000` proven** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 · 1x1 | **100%** | **100%** | **End-to-end `.22000` proven (79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 · 2x2 | 96% | usable | **End-to-end `.22000` proven** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 · 2x2 | 73% | usable | **End-to-end `.22000` proven** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6 · 2x2 | fail | fail | Unsupported: injection fails, cannot capture |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 · 2x2 | fail | fail | Unsupported: injection fails, cannot capture |

**Two tiers, at a glance:**

- **End-to-end proven (capture → `.22000` on file, 7 of 9 cards)**: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX, and AWUS036AXER. Among them EACS injects at 100% on both bands and received 79 ACKs after deauth, making it the most solid handshake performer in the batch; AWUS036ACH (RTL8812AU dual-antenna high gain) injects at 100% on both bands and, on 2026-11-19, was re-tested to export a `.22000` with 47 hashlines, placing it alongside EACS as a top pick for penetration testing. **Seven models completed end-to-end handshake capture: ACM, ACHM, ACH, ACS, EACS, AX, AXER.** The ACM injects at a lower rate (2.4G 63–83% / 5G 76%) and the ACHM completed it on 5 GHz (ch36), but both produced a `.22000`.
- **Cannot capture (2 cards)**: AWUS036AXM and AWUS036AXML (MT7921 fails injection on this platform, cannot deauth, and naturally cannot capture a handshake).

The ones that deserve a specific callout are the **AXM / AXML**: both are Wi-Fi 6 with normal monitor and AP, but injection simply doesn't work on this platform — the main cause is the mac80211 chanctx regression in stock kernel 6.16+ (not inherent to the chip); the community's same-model units can work with a git / patched driver but the firmware then locks the rate (see morrownr/USB-WiFi #387, morrownr/mt76 #18). Pure Internet use and running a hotspot are fine, but **for any audit use that needs injection or handshake capture, avoid them entirely on this platform**.

## 4. The WPA3-SAE Compatibility Pitfall: Set a Parameter Wrong and Your Own iPhone Won't Connect

Beyond capability, WPA3-SAE's parameter compatibility is the place most likely to trip you up in the field. This batch hit two key pitfalls:

### 4-1. The ACHM Must Use `sae_pwe=0`, Otherwise the iPhone 7 Plus Won't Connect

SAE derives its password element in different ways, and hostapd controls this via `sae_pwe`. When this batch set up the AWUS036ACHM as pure WPA3-SAE (`wpa_key_mgmt=SAE` + forced PMF `ieee80211w=2`), once `sae_pwe` was set to `2` the **iPhone 7 Plus simply couldn't connect**; after switching back to `sae_pwe=0` (Hunting-and-Pecking, compatible with older endpoints), the iPhone 7 Plus (iOS 15) connected smoothly and completed the 4-way.

The point of this pitfall: when you want to "reproduce" in the field a WPA3 environment dominated by older iOS endpoints, the AP-side `sae_pwe` must match the endpoint's capability, otherwise you get a "can't connect" false negative rather than a genuine compatibility conclusion. The EACS and ACS WPA3-SAE AP tests likewise used `sae_pwe=0` + `ieee80211w=2`, and the iPhone 7 Plus connected on both; `sae_pwe=0` is this batch's safe value validated against older iPhone endpoints.

### 4-2. Before 5G Injection, `iw reg set US` to Unlock TX

The second pitfall concerns the regulatory domain. The default `reg=TW` locks TX on some UNII bands, causing 5 GHz injection / deauth to "not get sent." Before doing 5G injection, this batch always `iw reg set US` to unlock TX first, then `iw reg set TW` to restore immediately after. The ACS's 5G injection went from fail to 96% after unlocking, while EACS and ACH went straight to 100%. Forget to unlock reg and you'll misjudge a card with normal injection capability as "5G unusable."

### 4-3. A Side Note: PMF Is Mandatory in WPA3

The WPA3-SAE spec forces `ieee80211w=2` (Management Frame Protection). This means in a pure WPA3 environment, classic techniques aimed at management frames are blocked by PMF; the reason real audits can still capture a 4-way is usually that the target still runs a WPA2/WPA3 transition mode. Factor this in when choosing a card, so you don't carry the wrong expectations for a pure-WPA3 target.

## 5. Toolchain Overview: What Actually Runs on the ARM64 Platform

Beyond hardware capability, the platform toolchain affects audit efficiency just as much. Here are a few test takeaways this batch compiled on the GX10 (ARM64):

- **Always convert with `hcxpcapngtool --all`.** The default parameters are stricter and often return "not enough M1" and won't produce a file; adding `--all` lets a complete M1–M4 export a `.22000` reliably.
- **When the office has multiple same-named APs, don't lock `--bssid`.** The Yopitek office has multiple same-named YUPITEK APs on the same channel, and the iPhone connects to whichever has the strongest signal. If you lock a single BSSID with `--bssid` during capture, you may filter out the very AP the iPhone is actually on and come up empty. The tested conclusion is to **not lock the BSSID and capture the whole channel directly**, then pick the complete handshake out of the on-file capture.
- **`hcxdumptool` 8.x `failed to arm` on this platform, except the EACS on 2.4 GHz (5 GHz fails).** rtw88 / rtw89 / mt7921u none provide active-monitor, which hcxdumptool 8.x requires; the fix is to switch to the traditional aircrack-ng flow of `airodump-ng` + `aireplay-ng`.
- **If you can't scan anything after repeated mode switches, unplug/replug the card first.** rtw88 / rtw89 can hit an RX stall (scanning 0 packets) after repeatedly switching monitor / AP; USB re-enumeration recovers it, and the interface name is derived from the MAC and unchanged after a replug. Before capturing a handshake, the first thing to do is reseat the card once.
- **BT+WiFi combo devices (EACS / AXML) have a re-plug race.** Bluetooth-bearing combo cards, when re-plugged or placed in certain USB ports, can hang during WiFi probe and fail to create the `wlx` interface; the fix is to re-plug into a different USB port — `modprobe` or manual bind is mostly ineffective.
- **ARM64 tool-install quirks.** aircrack-ng often lacks a prebuilt package on aarch64 and must be built from source; wifite uses the git version (the apt version has a dependency conflict with the self-built aircrack-ng).
- **Safety rule: never `airmon-ng check kill`.** The GX10's Internet uplink relies on the built-in NIC, and `check kill` shuts down NetworkManager too, taking the host offline. This batch only operated the ALFA cards' `wlx*` interfaces throughout, never touching the built-in uplink.

## 6. Selection Summary: Which Cards to Pick for WPA3-Related Audits

Looking at capability, compatibility and the platform toolchain together, for "WPA3-related authorized audit" use, this batch's recommendations are:

| Need scenario | Recommended model | Reason |
|---|---|---|
| Overall top pick (injection + end-to-end handshake) | **AWUS036EACS** | 100% dual-band injection, 79 ACKs on deauth, end-to-end `.22000` proven; the only caveat is it's a BT+WiFi combo device that occasionally needs a different USB port on re-plug |
| High gain / long range + strong injection | **AWUS036ACH** | RTL8812AU dual antenna, 100% dual-band injection, strong reception |
| Lightweight and portable | **AWUS036ACS** | Single stream, end-to-end `.22000` proven, 96% 5G injection |
| Wi-Fi 6 needs | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, end-to-end `.22000` proven; the AXER's embedded Nano antenna design plus chip tuning gives the widest scan coverage |
| **Be sure to avoid** | AWUS036AXM / AWUS036AXML | MT7921 fails injection on this platform and cannot capture a handshake |

In one line: **for WPA3-related audits, favor the EACS, then the ACH / ACS; for Wi-Fi 6 pick the AX / AXER; be sure to avoid the AXM / AXML.** Of the seven cards that completed end-to-end handshake capture, all the Realtek ones (rtw88 / rtw89) can inject, and the MediaTek ACM and ACHM (mt76) also made it through; the MT7921 AXM / AXML cannot. When choosing, going by chipset is more reliable than going by model name.

## Frequently Asked Questions (FAQ)

**Q: Can the AWUS036AXM capture a WPA handshake on Ubuntu?**
A: Not on this platform. In testing, the AWUS036AXM and AWUS036AXML (MT7921 chips) fail injection and cannot send a deauth, so the whole 4-way handshake capture chain breaks with it — unsuitable for uses needing handshake capture.

**Q: Which ALFA adapter captures a WPA handshake most reliably?**
A: In testing the AWUS036EACS was the most solid: 100% injection on both bands, 79 ACKs after deauth, and a successfully exported hashcat-ready `.22000` file — the most complete end-to-end validation in the batch.

**Q: Why can't an old iPhone connect to a WPA3-SAE hotspot?**
A: The key is hostapd's `sae_pwe` parameter: set to 2 (forced H2E), the iPhone 7 Plus fails to connect; switching back to `sae_pwe=0` (Hunting-and-Pecking) lets it complete the 4-way handshake and connect normally.

**Q: Can you still capture a 4-way handshake in a WPA3 environment?**
A: A pure WPA3-SAE environment forces PMF on (`ieee80211w=2`), and classic techniques aimed at management frames are blocked; in practice you can still capture a handshake, usually because the target runs a WPA2/WPA3 transition mode rather than pure WPA3.

**Q: An ALFA adapter's 5GHz injection doesn't test out — is it a hardware problem?**
A: Not necessarily. The default regulatory domain restricts transmit power on some 5GHz bands, causing injection to "not get sent out"; in testing, after switching the regulatory domain to a transmit-capable state, the previously failing 5GHz injection became usable. We suggest confirming the regulatory domain setting first before judging whether it's a hardware limitation.

## 7. Further Reading

- [Master table and selection verdict for the 9 ALFA adapters on ARM64](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Per-card tests by model: [AWUS036EACS single-card test](/en/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACS single-card test](/en/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*All tests in this article were performed on Yopitek's own office Wi-Fi (SSID YUPITEK), against our own iPhone 7 Plus — a distributor's legitimate capability validation of ALFA Wi-Fi adapters. Data cited from the 2026-11-16 to 11-18 hands-on test reports. It targets no third-party network and provides no attack procedures. Testing unit: Yopitek (ALFA Network Taiwan distributor) — https://www.yupitek.com*
