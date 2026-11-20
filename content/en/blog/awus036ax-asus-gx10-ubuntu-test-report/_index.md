---
title: "ALFA AWUS036AX Card-by-Card Test: Wi-Fi 6 Monitor / Injection / AP Capability Report on ASUS GX10 + Ubuntu 24.04 (Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX (Wi-Fi 6) tested on Ubuntu 24.04 ARM64: no driver install needed, and Monitor, 2.4G injection 96%, 5G AP VHT80, WPA3-SAE, and end-to-end handshake (.22000) all pass; IBSS / mesh not supported. Platform: ASUS GX10, RTL8832BU."
faq:
  - question: "Do I need to install a driver for the AWUS036AX on Ubuntu 24.04 ARM64? What if lsusb shows 0bda:1a2b?"
    answer: "Not on the kernel 6.17 (ASUS GX10) tested here: RTL8832BU is driven by the in-kernel rtw89_8852bu, with no compiling and no DKMS. If lsusb shows 0bda:1a2b (CD-ROM mode), run sudo usb_modeswitch -v 0bda -p 1a2b -K to switch it to WLAN."
  - question: "Does the AWUS036AX support monitor mode and packet injection?"
    answer: "Yes. 2.4 GHz injection is 29/30 (96%); 5 GHz per-AP targeted testing returns Injection is working!; airodump-ng hopping scanned 14 APs and 4 clients in 60 seconds. Active monitor, IBSS, and mesh are not supported."
  - question: "Can the AWUS036AX capture a WPA handshake? Can the MT7921 AXM / AXML do it?"
    answer: "The AX can: with our own AP plus our own iPhone 7 Plus, aireplay-ng -0 triggers reconnection, airodump-ng captures the full M1-M4, and hcxpcapngtool exports the .22000. The MT7921 AXM / AXML fail injection on this platform and cannot do it. Only on networks you own or are authorized to test."
  - question: "Can the AWUS036AX act as an AP hotspot? Does it support WPA3?"
    answer: "Yes. hostapd brings up a 2.4G (802.11n) and 5G (VHT 80 MHz) AP; the iPhone 7 Plus associates showing VHT-NSS2 80 MHz; WPA3-SAE (ieee80211w=2, sae_pwe=0) associates with an iPhone 15 Pro on 2.4 GHz, MFP: yes (WPA3 on 5 GHz was not tested)."
  - question: "What is the difference between the AWUS036AX and AWUS036AXER? Which should I pick?"
    answer: "Both are RTL8832BU + rtw89_8852bu with an identical capability matrix, differing in antenna and reception: the AXER has external antennas and, in the same batch, hopping scanned 63 APs + 12 clients (the AX got 14 APs + 4 clients). For a fixed desktop pick the AX; for long range or strongest reception pick the AXER."
draft: false
---

**TL;DR**: In hands-on testing by Yopitek (ALFA Network's Taiwan distributor), the AWUS036AX needs no driver install on the ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) and works for dual-band monitor; 2.4G injection is 96%, 5G AP runs VHT80, end-to-end .22000 passes, and IBSS / mesh are not supported.

> This article is a product compatibility and capability test completed by Yopitek on **our own equipment, our own office Wi-Fi (SSID `YUPITEK`), and our own test phone**, with the subject being the ALFA **AWUS036AX** (Realtek RTL8832BU, Wi-Fi 6 2x2).
> Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`; reference device Apple iPhone 7 Plus (WPA3 and VIF also tested on iPhone 15 Pro).
> ⚠️ **Legal use**: Monitor and injection were performed only on networks we own or are authorized to use; for AP mode, follow your local radio regulations. This article does not involve any attack operation against third-party networks.

---

## 1. This Card and the Test Platform

The AWUS036AX is ALFA's current-generation Wi-Fi 6 USB adapter, using the Realtek RTL8832BU chipset with 2x2 dual spatial streams and support for dual-band 2.4 GHz and 5 GHz. In ALFA's lineup it shares the same chipset and the same driver with the external-antenna AWUS036AXER, differing in antenna form and receive gain; versus the MediaTek Wi-Fi 6 models AWUS036AXM / AXML it is an entirely different chipset path, and the test conclusions differ greatly too (covered in Section 5).

This test does not discuss the datasheet's theoretical rates; it only answers the three things distributors and field engineers care about most: how easy is it to install on recent Linux, which wireless capabilities actually work, and which are inherently impossible in the driver and not worth wasting time on. The conclusions must be reproducible, so every command was run line by line on the physical GX10 on 2026-11-18, and the "measured output" below is a genuine excerpt (MAC addresses masked with `xx`).

Let's be clear about the test boundary first: everything was done in our own office, against our own `YUPITEK` network and our own phone. Monitor only receives packets in our own environment; injection and handshake were only performed against our own AP and our own iPhone. The goal is to verify "what this card can do on this machine," not to demonstrate attacking a third-party network.

---

## 2. Hardware and Driver (Wi-Fi 6, No Install)

The most practical benefit this generation is: **recognized on plug-in, no compiling, no DKMS**. The RTL8832BU's `rtw89_8852bu` driver is already an in-kernel module in kernel 6.17, bound at boot on the GX10, so there is no need to pull an out-of-tree project from GitHub to compile by hand.

The chipset info and verification steps are as follows. First use `lsusb` to confirm the card enumerates in WLAN mode:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

You should expect to see `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`. Our test unit's card appeared directly in WLAN mode and was not stuck in CD-ROM mode; if your card shows `0bda:1a2b`, it is still in CD-ROM mode, and `sudo usb_modeswitch -v 0bda -p 1a2b -K` switches it to WLAN.

Next, confirm the driver and firmware are loaded:

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

What loaded on the physical machine is `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`. Both driver and firmware are built into the kernel, so no separate package install is needed.

The last step is to look closely at which interface modes this driver **declares support for**, which directly determines which capabilities are present and which are N/A later:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

The physical machine lists `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`. IBSS, mesh point, and active-monitor are absent from the list. This is not a misconfiguration; `rtw89_8852bu` simply never implemented these three modes, and Section 4 marks them N/A accordingly.

---

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

First, a capability summary table, each cell corresponding to a measured excerpt below:

| Capability | 2.4 GHz | 5 GHz | Measured excerpt |
|---|---|---|---|
| **Monitor** | ✅ Strong | ✅ Strong | airodump hopping scanned **14 APs + 4 clients** in 60 seconds |
| **Injection** | ✅ **96%** | ✅ usable | 2.4G `aireplay-ng --test` 29/30 (96%); 5G per-AP `Injection is working!` |
| **AP hotspot** | ✅ 802.11n (HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus associates: 2.4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | Not tested | iPhone 15 Pro associates, MFP: yes (`sae_pwe=0`); tested on 2.4 GHz only |
| **WPA handshake capture** | ✅ **end-to-end** | — | deauth our own iPhone → capture full 4-way → convert to hashcat `.22000` |

**Monitor (monitor mode / receive) ✅ Strong.** After switching to monitor, both 2.4 GHz and 5 GHz receive plenty of packets (about 100 packets/6 seconds each). Using `airodump-ng --band abg` to hop and scan for 60 seconds, it found 14 APs plus 4 clients — receive performance on par with ALFA's Wi-Fi 5 ACM / ACHM, and far ahead of the two MediaTek MT7921 cards (the AXM / AXML measured as weak receivers). For field surveys and channel-occupancy audits, this card's reception is sufficient.

**Injection (packet injection) ✅ usable, and this is the key difference between the AX and the MediaTek models.** Running `aireplay-ng --test` on 2.4 GHz (ch6), the measured result is `29/30: 96%`, `Injection is working!`, a 96% response rate. On 5 GHz (ch36) the broadcast test may return `Found 0 APs` (modern APs don't reply to broadcast probes, which is normal), but a per-AP test specifying the BSSID returns `Injection is working!`, confirming 5 GHz injection is usable. By contrast, the MediaTek AXM / AXML — also Wi-Fi 6 — **fail injection outright** on this platform (mainly a mac80211 chanctx regression in kernel 6.16 and later, plus firmware that locks injection rates to 1/6 Mbps; not a limit of the chip itself); be sure to keep this distinction clear when selecting.

**AP hotspot ✅ both bands can be brought up, 5 GHz reaches VHT80.** Using hostapd to start an AP, 2.4 GHz with 802.11n (`ieee80211n=1`, HT20) had the iPhone 7 Plus associate showing MCS 12, authorized; 5 GHz with VHT 80 MHz (`vht_oper_chwidth=1`, `ht_capab=[HT40+]`) had the iPhone 7 Plus associate showing VHT-NSS2 80 MHz, authorized. Both bands bring clients up stably, and the 80 MHz bandwidth did negotiate successfully.

**WPA3-SAE ✅ (2.4 GHz; 5 GHz not tested).** Changing the AP's `wpa_key_mgmt` to `SAE` and `ieee80211w=2`, the measured result had the iPhone 15 Pro associate with MFP (Management Frame Protection) showing yes. There is a compatibility detail here: `sae_pwe` must be set to `0` (Hunting-and-Pecking) for older iPhones to connect.

**WPA handshake capture ✅ end-to-end success.** On our own `YUPITEK` network, against our own iPhone 7 Plus, the full flow ran through: monitor the channel on the side → `aireplay-ng -0` sends a deauth to trigger reconnection → `airodump-ng` captures the full four-way handshake (M1/M2/M3/M4) → use `hcxpcapngtool` to export the hashcat `.22000` format. Because this card's injection is usable, the whole chain ran; a card that fails injection (like the AXM / AXML) breaks at the deauth step. The common Kali tools used in this handshake capture chain (aircrack-ng, hcxtools) all run directly on Ubuntu 24.04 ARM64.

---

## 4. Advanced and Limitations (rtw89 Driver's N/A Items)

This section states plainly, in one place, both "the advanced features it can do" and "what the driver inherently cannot do," to avoid wasting time in the field.

| Feature | Status | Note |
|---|---|---|
| **VIF (STA + AP concurrent)** | ✅ | Main interface connected to `YUPITEK`, AP VIF (ch36 VHT80) open at the same time, both running in parallel; STA-side ping 3.2 ms |
| **WPA handshake capture** | ✅ end-to-end | Captures M1–M4, `hcxpcapngtool` exports `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` lacks this mode (not in `iw phy`'s supported modes) |
| **Ad-hoc (IBSS)** | **N/A** | Driver does not support it |
| **Mesh (802.11s)** | **N/A** | Driver does not support it |
| **Wi-Fi Direct (P2P)** | ⬜ Untested | Driver declares support, but it needs a second device, skipped this time |

**VIF ✅.** Create an AP virtual interface (different MAC, unmanaged), keep the main interface connected to Wi-Fi, and open the AP on the same channel. Measured, with the main interface connected to `YUPITEK`, the AP VIF ran VHT80 on ch36, both interfaces operating in parallel, STA-side ping 3.2 ms. This is viable for the "connected to the internet on one side, running a test hotspot on the other" scenario.

**Active monitor / IBSS / Mesh are N/A, not broken.** These three modes do not appear in the supported interface modes from the `iw phy info` in Section 2, meaning the `rtw89_8852bu` driver simply never implemented them. Commands like `sudo iw dev $IF set type ibss` fail outright, and there is no workaround: this isn't something a parameter or firmware can fix — to use these three modes you must switch chipset paths (for example, MediaTek mt76's ACM / ACHM can create IBSS / mesh on a single node).

**One platform-level limitation to know up front: hcxdumptool `failed to arm` on the GX10.** This is not an AX-specific problem. `hcxdumptool 8.x` needs active-monitor, and the GX10 has a built-in tri-band adapter, so when a USB card is enumerated, `-I` easily mis-maps to the built-in phy, and every USB card under test fails to arm on this machine (the only exception is the AWUS036EACS on 2.4 GHz). The practical approach is to **use the aircrack-ng suite** (airodump-ng + aireplay-ng) for capture; this card's injection is usable, so the whole chain still completes end-to-end (see Section 3).

**Safety rule (common across the GX10 platform):** never run `airmon-ng check kill` — it shuts down NetworkManager and cuts the GX10's upstream connectivity; when operating, only touch the `wlx*` interface and do not disturb the built-in upstream adapter.

---

## 5. Use Cases and Selection (Wi-Fi 6 AP Hotspot, Back to the Hub)

Turning the test conclusions into selection advice: **the AWUS036AX's sweet spot is "Wi-Fi 6 + AP hotspot" scenarios that also need injection capability.**

| Use | AWUS036AX fit | Note |
|---|---|---|
| Wi-Fi 6 AP hotspot / edge access | ★ Top choice | 2x2 VHT80 dual-band can be brought up, WPA3-SAE usable |
| Injection + handshake auditing | ★ Capable | 2.4G 96%, 5G usable, end-to-end capture succeeds |
| Strongest reception / long-range monitor | ○ Sufficient, but AXER is top choice | The same-chipset AXER has external antennas and stronger reception |
| mesh / IBSS experiments | ✗ Not applicable | Driver N/A, choose mt76's ACM / ACHM instead |

**Typical deployment: as a Wi-Fi 6 hotspot, letting edge devices connect back to a central Hub.** Using the tested AP (VHT80) and VIF capabilities, deploy the GX10 with this card as a Wi-Fi 6 access point; edge devices like test phones and IoT sensors associate, and traffic then returns through the main interface to the central Hub (gateway). The VIF test proved that "the main interface connecting back to the upper network" and "opening an AP downstream" can run in parallel, with STA-side latency 3.2 ms — a topology verified as viable on this platform. If the edge access segment needs modern encryption, just add WPA3-SAE.

**Selection pitfall: for injection / handshake uses, don't pick the AWUS036AXM / AXML.** Although these two are also Wi-Fi 6 2x2 and can bring up an AP, MediaTek MT7921 **fails injection** on this platform — it cannot deauth and cannot capture a handshake. If a customer only wants a plain Wi-Fi 6 AP / general connectivity card and never touches injection, the MediaTek models are fine and stable; but as soon as the use involves wireless auditing, choose the Realtek AX (or the external-antenna AXER).

**How to distinguish it from the same-chipset AXER?** Both share chipset, driver, and capability matrix; the AXER is the external-antenna version with stronger reception and long-range monitor (in the same batch, the AXER's hopping scan found 63 APs + 12 clients). For a fixed desktop with low antenna needs, pick the AX; for extended range and strongest reception, go with the AXER.

---

## Frequently Asked Questions (FAQ)

**Q: Do I need to install a driver for the AWUS036AX on Ubuntu 24.04 ARM64? What if lsusb shows 0bda:1a2b?**
Not on the kernel 6.17 (ASUS GX10) tested here: RTL8832BU is driven by the in-kernel rtw89_8852bu, with no compiling and no DKMS. If lsusb shows `0bda:1a2b` (CD-ROM mode), run `sudo usb_modeswitch -v 0bda -p 1a2b -K` to switch it to WLAN.

**Q: Does the AWUS036AX support monitor mode and packet injection?**
Yes. 2.4 GHz injection is 29/30 (96%); 5 GHz per-AP targeted testing returns `Injection is working!`; airodump-ng hopping scanned 14 APs and 4 clients in 60 seconds. Active monitor, IBSS, and mesh are not supported.

**Q: Can the AWUS036AX capture a WPA handshake? Can the MT7921 AXM / AXML do it?**
The AX can: with our own AP plus our own iPhone 7 Plus, `aireplay-ng -0` triggers reconnection, `airodump-ng` captures the full M1–M4, and `hcxpcapngtool` exports the .22000. The MT7921 AXM / AXML fail injection on this platform and cannot do it. Only on networks you own or are authorized to test.

**Q: Can the AWUS036AX act as an AP hotspot? Does it support WPA3?**
Yes. `hostapd` brings up a 2.4G (802.11n) and 5G (VHT 80 MHz) AP; the iPhone 7 Plus associates showing VHT-NSS2 80 MHz; WPA3-SAE (ieee80211w=2, sae_pwe=0) associates with an iPhone 15 Pro on 2.4 GHz, MFP: yes (WPA3 on 5 GHz was not tested).

**Q: What is the difference between the AWUS036AX and AWUS036AXER? Which should I pick?**
Both are RTL8832BU + rtw89_8852bu with an identical capability matrix, differing in antenna and reception: the AXER has external antennas and, in the same batch, hopping scanned 63 APs + 12 clients (the AX got 14 APs + 4 clients). For a fixed desktop pick the AX; for long range or strongest reception pick the AXER.

---

## 6. Further Reading

- "Capability Master Table of 9 ALFA Wireless Adapters on ASUS GX10 + Ubuntu ARM64" — Monitor / Injection / AP / handshake for every model, compared at once → [Master Table Hub](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [No driver install: enabling Monitor and AP with in-kernel drivers on Ubuntu 24.04 + kernel 6.17](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) — the common configuration flow across rtw88 / rtw89 / mt76
- [AWUS036AXER card-by-card test](/en/blog/awus036axer-asus-gx10-ubuntu-test-report/) — the same-chipset external-antenna version, compared on reception and long-range monitor
- [WPA3-SAE handshake capture capability test and sae_pwe compatibility](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/) — the `sae_pwe` minefield for iPhone connectivity

---

*Test unit: Yopitek (ALFA distributor) — https://www.yupitek.com | Test environment: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Reference device: Apple iPhone 7 Plus (WPA3 / VIF also tested on iPhone 15 Pro)*
