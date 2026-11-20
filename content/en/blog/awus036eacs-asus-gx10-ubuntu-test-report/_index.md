---
title: "ALFA AWUS036EACS Single-Card Test: RTL8821CU (BT + WiFi Combo) on ASUS GX10 (ARM64 / Ubuntu 24.04) — Monitor, Injection, AP, End-to-End Handshake"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS (Bluetooth + Wi-Fi combo) tested on Ubuntu 24.04 ARM64: no driver install needed, 100% injection on both bands, Monitor, AP, WPA3-SAE, and end-to-end handshake (79 ACKs, .22000) all pass. Includes the USB re-plug risk. Platform: ASUS GX10, RTL8821CU."
faq:
  - question: "Do I need to install a driver for the AWUS036EACS on Ubuntu 24.04 ARM64?"
    answer: "Not on the kernel 6.17 (ASUS GX10) tested here: RTL8821CU is driven by the in-kernel rtw88_8821cu, recognized on plug-in with no compiling and no DKMS; the interface is named wlx plus the MAC and does not change across re-plugs."
  - question: "How do monitor mode and packet injection perform on the AWUS036EACS?"
    answer: "Monitor is steady on both 2.4G and 5G, with most channels receiving a full 300 frames; aireplay-ng --test is 30/30 (100%) on both bands. Before 5G injection, run iw reg set US to lift the TW restriction on TX."
  - question: "Can the AWUS036EACS capture a WPA handshake?"
    answer: "Yes. Tested end-to-end with our own AP plus our own iPhone 7 Plus: the deauth received 79 ACKs, the full M1-M4 was captured, and hcxpcapngtool --all exported the .22000 (784 bytes, 2 EAPOL pairs). Only on networks you own or are authorized to test."
  - question: "The AWUS036EACS shows up in lsusb after plug-in but has no wlx network interface — what do I do?"
    answer: "This is the probe race of a BT+Wi-Fi combo device: Bluetooth has bound to btusb while the Wi-Fi rtw88_8821cu is stuck. In practice, reloading the module or manually binding usually fails; the reliable fix is to unplug the card and re-insert it into a different USB port."
  - question: "Does the AWUS036EACS support mesh, IBSS, or hcxdumptool?"
    answer: "No. rtw88's active-monitor, IBSS, mesh, and P2P return -95 or an invalid join; hcxdumptool 8.x arms only on 2.4 GHz (5 GHz fails to arm), so use airodump-ng + aireplay-ng. VHT is 80 MHz only. For mesh / IBSS, choose the AWUS036ACM / ACHM."
draft: false
---

> Test unit: Yopitek (ALFA Network distributor in Taiwan) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Test device: our own iPhone 7 Plus (WPA3 also tested on iPhone 15 Pro) | Target: our own office Wi-Fi (SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> This article is a single-card capability and compatibility test of the AWUS036EACS. All Monitor / Injection / handshake capture was performed on Yopitek's own equipment, our own office Wi-Fi, against our own test phone — a legitimate hardware capability verification by the distributor. It targets no third-party network and provides no attack procedures.

**TL;DR**: The AWUS036EACS needs no driver install on the GX10 / Ubuntu 24.04 (kernel 6.17); injection is 100% on both bands, end-to-end .22000 passes (79 ACKs); as a BT+Wi-Fi combo card, watch out for re-plugging.

## 1. This Card and the Test Platform

The AWUS036EACS is a lightweight travel-class Wi-Fi 5 (802.11ac) USB adapter from ALFA. Its chipset is the Realtek RTL8821CU — 1x1 single stream, dual-band 2.4 GHz and 5 GHz — and it also has built-in Bluetooth, making it a BT + WiFi combo device. This article puts it alone on Yopitek's test bench and runs through each item in an ASUS GX10 (ARM64) + Ubuntu 24.04 environment, answering the questions customers care about most: does the driver work on ARM64, which modes can it enter, and how far does performance go.

First, let's be clear about the framing. This is a distributor's verification of the compatibility and capability boundaries of its own product, not an attack tutorial. Every injection- and handshake-related capability measurement in this article was performed in our own closed environment against our own devices, and no procedure against any external network is provided.

The test platform and method follow the other single-card articles in this batch:

- Compute platform: ASUS GX10 (ARM64 / aarch64)
- Operating system: Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- Driver strategy: use the kernel's in-kernel driver, recognized on plug-in, with no third-party DKMS module installed
- Test device: Apple iPhone 7 Plus (WPA3-SAE re-tested on iPhone 15 Pro)
- Test environment: our own office Wi-Fi, SSID YUPITEK, 2.4 GHz ch5 / 5 GHz ch36, ch157
- Safety rule: only operate the `wlx*` interface throughout, never touch the built-in upstream line; never run `airmon-ng check kill` (it shuts down NetworkManager and cuts the GX10's upstream connectivity)

## 2. Hardware and Driver: The Truth About a BT + WiFi Combo Device

First, the details. The table below is the AWUS036EACS's actual attachment state on kernel 6.17:

| Item | Detail |
|---|---|
| Chipset | Realtek RTL8821CU (1x1 single stream) |
| Generation | Wi-Fi 5 (802.11ac), 2.4 + 5 GHz |
| Combo function | BT + WiFi combo device (Bluetooth included) |
| USB ID | `0bda:c820` |
| Driver | `rtw88_8821cu` (in-kernel, USB supported since kernel 6.2) |
| Firmware | 24.11.0 (H2C version 12, per dmesg) |
| VHT bandwidth | 80 MHz only (no 160 / 80+80) |

Via `iw phy`, the supported interface modes are `managed` / `AP` / `AP/VLAN` / `monitor` (`IBSS` is listed but join does not work in practice); band coverage is 2.4 GHz ch1–13 and 5 GHz ch36–165 (of which ch52–144 are DFS); ciphers include CCMP-256, GCMP-128 / GCMP-256, and CMAC, meeting the conditions to run WPA3 on the AP side.

There is no suspense on the driver side. USB support for the RTL8821CU was merged into mainline `rtw88` from kernel 6.2, and the GX10's kernel 6.17 already includes `rtw88_8821cu`, which loads on plug-in with no compiling or DKMS. Early in-kernel versions had an AP-mode bug, fixed by the macid patch (from linux-next-20240911 onward); on kernel 6.17 here, all three AP modes finished cleanly. To confirm:

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

After loading, the Wi-Fi interface is named `wlx` + MAC (e.g. `wlx00c0cab3a52e`) rather than `wlan0`; the name does not change across re-plugs, so it can be referenced stably in scripts.

What really needs attention is the "combo device" fact. Inspecting with `lsusb -t`, you'll see multiple USB interfaces under the same RTL8821CU: the Bluetooth function binds `btusb`, while the Wi-Fi function separately binds `rtw88_8821cu`.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(Bus/Port numbers change with each plug-unplug cycle; the point is that interfaces 0/1 go to `btusb` and interface 2 is the Wi-Fi `rtw88_8821cu`.)

**The re-plug risk of a BT + WiFi combo device (read before deployment).** Because Bluetooth and Wi-Fi share the same USB device, in certain USB ports or with fast re-plugging there can be a race where Bluetooth has already bound `btusb` but the probe of the Wi-Fi interface gets stuck — the result is that `lsusb` sees `0bda:c820` but no `wlx` interface appears. In testing, reloading after `modprobe -r`, or a manual `bind`, mostly failed (`bind` returns `Operation already in progress`). The only reliable fix: unplug the card and re-insert it into a different USB port — after switching ports, enumeration is clean and the `wlx` interface appears normally. This is an extra operational detail to know compared to the non-combo AWUS036ACS (RTL8811AU); knowing it in advance avoids misdiagnosing it as a faulty card.

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

The table below is the summary of the AWUS036EACS's core capability tests, each run on the physical GX10 on 2026-11-18:

| Capability | 2.4 GHz | 5 GHz | Measured highlight |
|---|---|---|---|
| Monitor | ✅ Strong | ✅ Strong | Most channels at a full 300 frames; community #453 "ch1 stuck" not reproduced |
| Injection | ✅ 100% (30/30) | ✅ 100% (30/30) | Power 2.4G -38.27 / 5G -76.10; strongest injection among the ac cards in this batch |
| AP hotspot | ✅ clean shutdown | ✅ VHT 80 MHz | `hostapd` brings up the station, iPhone 7 Plus associates and completes the 4-way |
| WPA3-SAE (AP side) | ✅ iPhone associates | Not tested | SAE-only + enforced PMF (`ieee80211w=2`, `sae_pwe=0`) |
| WPA handshake capture | — | ✅ end-to-end | M1–M4 complete, deauth received 79 ACKs, exported `.22000` |

Monitor (monitor mode) is steady on both 2.4 and 5 GHz. Capturing on each of six channels, most received a full 300 frames. For the 8821cu there is an important positive result here: GitHub #453, long tracked by the rtw88 community ("8821cu monitor stuck on ch1 when STA is up on kernel ≥6.9"), was not reproduced in this GX10 environment — 5 GHz ch36, ch149, and ch157 all steadily filled 300 frames. For cross-band 2.4 / 5 GHz spectrum surveys or packet analysis, this card's monitor can be used with confidence.

Injection (packet injection) is the standout. Measured with `aireplay-ng --test`, both 2.4 GHz and 5 GHz are 30/30, 100% — the strongest injection among the ac cards in this batch (the AWUS036ACS, also 1x1, is only 96% on 5G). There is a Taiwan-local detail here: 5 GHz TX is locked when the regulatory domain is set to TW, so run `iw reg set US` to unlock before measuring and `iw reg set TW` to restore afterward.

On the AP hotspot side, using `hostapd` to set up 2.4 GHz (WPA2), 5 GHz (VHT 80 MHz), and WPA3-SAE separately, the iPhone 7 Plus could associate and complete the 4-way handshake in all cases, with clean shutdowns (`AP-DISABLED` / `TERMINATING`). There was none of the beacon re-key issue some cards exhibit, so on 2.4G this is steadier than its sister card the ACS. WPA3 uses SAE-only with enforced PMF (`ieee80211w=2`, `sae_pwe=0`), and the iPhone 15 Pro associated successfully, confirming that RTL8821CU's WPA3-SAE on the AP side is usable.

The Kali toolchain (platform layer) also comes up fine on this card: `airmon-ng` detects the EACS (`rtw88_8821cu`), but again don't use `check kill`; `kismet` started successfully with this card as a data source and produced a `.kismet` log of about 733 KB; `bettercap` 2.32's `wifi.recon on` works normally (the txpower warning can be ignored); `wifite` (git 3.0.0) scanned 10+ APs including our own YUPITEK (ch5, PWR 84) — this version has no `--band` flag, so use `-c 1,6,11,36,149,157` to specify channels; `Wireshark` / `tshark` 4.x captured and parsed 325 frames in monitor ch6; and `macchanger`'s random MAC spoofing also works. This tool-layer section is consistent with the other cards in this batch; the differences lie mainly in the injection and monitor hardware capabilities above.

## 4. End-to-End Handshake: Highlights and Honest Limitations

This card's highlight capability is chaining injection and capture into one complete, usable pipeline. Between our own YUPITEK AP and our own iPhone 7 Plus, the whole chain ran through on the physical machine: send deauth to our own iPhone (injection, 79 ACKs received in practice, confirming the injected packets actually reached the client) → on reconnection, collect the full 4-way handshake (M1, M2, M3, M4, one each) → use `hcxpcapngtool --all` to export the hashcat-format `.22000` (784 bytes, 2 EAPOL pairs, RC checked). The entire flow was only to verify the card's capability; the target throughout was our own AP and our own phone, and no third-party network was involved.

Two key practical details worth noting: the office has multiple identically named YUPITEK APs on ch36 at once, so when capturing, do not lock `--bssid` — capture the whole channel directly, or you may filter out the one the iPhone actually connects to; also, `hcxpcapngtool` defaults are stricter, so you need `--all` to export the `.22000`.

The honest limitations, all at once:

- **No active-monitor / IBSS (Ad-hoc) / Mesh (802.11s) / Wi-Fi Direct (P2P) support.** These modes return `-95` (Operation not supported) under `rtw88`, or are listed but with an invalid join — a driver-layer limitation with no workaround. Customers needing mesh / IBSS experiments should switch to MediaTek's AWUS036ACM / ACHM.
- **`hcxdumptool` 8.x is limited.** It needs active-monitor; on this card it arms only on 2.4 GHz and fails to arm on 5 GHz (the other cards in the batch all return `failed to arm interface`); use `airodump-ng` + `aireplay-ng` instead — this card's injection is 100%, so it is unaffected.
- **VHT is 80 MHz only.** Single stream, no 160 MHz or 80+80 — positioned as a lightweight travel card, not a throughput contender.
- **VIF is partial.** Only a passive monitor interface running alongside a managed interface on the same channel (software monitor) works (100 frames measured); independent dual VIFs are not supported.

## 5. Use Cases and Selection

Taken together, the AWUS036EACS's positioning is clear: if you need dual-band Monitor + Injection + end-to-end handshake verification and also want a compact travel card with built-in Bluetooth, it is a fitting solution. Its 100% injection on both bands and clean AP / WPA3 performance place it, within authorized scope, in the top-choice group for wireless auditing and security education alongside the AWUS036ACH and AWUS036ACS.

When to pick a different card instead:

- **Frequent on-site re-plugging, or chassis USB ports of uneven quality** → the combo device's probe race adds friction; consider the non-combo AWUS036ACS (RTL8811AU, also 1x1 ac, without the Bluetooth variable).
- **Doing mesh / IBSS experiments** → `rtw88` doesn't support them; switch to MediaTek's AWUS036ACM / ACHM.
- **Seeking strongest reception or long-range monitor** → the dual-antenna AWUS036ACH or the Wi-Fi 6 AWUS036AXER is more suitable.
- **Pitfall to avoid**: if your purpose is injection / handshake, do not choose the MT7921-based AWUS036AXM / AXML — injection outright fails on this platform.

To see the full cross-comparison of Monitor / Injection / AP / WPA3 and the complete selection matrix for all 9 ALFA cards in one place, go back to the master table: [The most complete 2026 test: 9 ALFA wireless adapters on the ASUS GX10, full matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Frequently Asked Questions (FAQ)

**Q: Do I need to install a driver for the AWUS036EACS on Ubuntu 24.04 ARM64?**
Not on the kernel 6.17 (ASUS GX10) tested here: RTL8821CU is driven by the in-kernel rtw88_8821cu, recognized on plug-in, with no compiling and no DKMS; the interface is named wlx plus the MAC and does not change across re-plugs.

**Q: How do monitor mode and packet injection perform on the AWUS036EACS?**
Monitor is steady on both 2.4G and 5G, with most channels receiving a full 300 frames; `aireplay-ng --test` is 30/30 (100%) on both bands. Before 5G injection, run `iw reg set US` to lift the TW restriction on TX.

**Q: Can the AWUS036EACS capture a WPA handshake?**
Yes. Tested end-to-end with our own AP plus our own iPhone 7 Plus: the deauth received 79 ACKs, the full M1–M4 was captured, and `hcxpcapngtool --all` exported the .22000 (784 bytes, 2 EAPOL pairs). Only on networks you own or are authorized to test.

**Q: The AWUS036EACS shows up in lsusb after plug-in but has no wlx network interface — what do I do?**
This is the probe race of a BT+Wi-Fi combo device: Bluetooth has bound btusb while the Wi-Fi rtw88_8821cu is stuck. In practice, reloading the module or manually binding usually fails; the reliable fix is to unplug the card and re-insert it into a different USB port.

**Q: Does the AWUS036EACS support mesh, IBSS, or hcxdumptool?**
No. rtw88's active-monitor, IBSS, mesh, and P2P return -95 or an invalid join; hcxdumptool 8.x arms only on 2.4 GHz (5 GHz fails to arm), so use airodump-ng + aireplay-ng. VHT is 80 MHz only. For mesh / IBSS, choose the AWUS036ACM / ACHM.

---

## 6. Further Reading

- [The most complete 2026 test: 9 ALFA wireless adapters on the ASUS GX10 (ARM64 / Ubuntu 24.04), full Monitor, Injection, AP matrix](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/) (Hub master table)
- [Wireless auditing in the WPA3-SAE era: handshake capture capability of 9 ALFA cards, tested](/en/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [No driver install: enabling ALFA adapter Monitor and AP modes with in-kernel drivers on Ubuntu 24.04 + kernel 6.17](/en/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Also an rtw88 USB ac card → [AWUS036ACS single-card test report (RTL8811AU)](/en/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Test unit: Yopitek (ALFA Network distributor in Taiwan) — https://www.yupitek.com*
