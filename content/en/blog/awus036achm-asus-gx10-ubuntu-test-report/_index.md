---
title: "AWUS036ACHM Card-by-Card Test: MediaTek MT7610U Single-Antenna AC600 on ASUS GX10 (ARM64 / Ubuntu 24.04) — Monitor, Injection, AP, WPA3 Capability"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "AWUS036ACHM (MT7610U) needs no driver install on Ubuntu 24.04; dual-band monitor mode works and 2.4G packet injection is 96–100%. Running an AP requires disabling 802.11n, and WPA3 requires sae_pwe=0 for older iPhones to connect."
faq:
  - question: "Does AWUS036ACHM need a driver on Ubuntu 24.04?"
    answer: "No. The MT7610U is handled by the kernel's built-in mt76x0u driver; Ubuntu 24.04 (kernel 6.17) recognizes it on plug-in with no DKMS and no extra firmware; lsusb shows USB ID 0e8d:7610."
  - question: "Can AWUS036ACHM enter monitor mode? How many APs can it scan?"
    answer: "Yes. Both 2.4GHz and 5GHz can enter monitor mode; a 120-second full-band frequency-hop scan with airodump-ng found 19 APs and 14 clients, spread across ch1, 2, 5, 6, 36, 149, 157."
  - question: "What is AWUS036ACHM's packet injection success rate? Does 5GHz work?"
    answer: "On 2.4GHz channel 6, per-AP injection response rate was 96–100% (aireplay-ng --test, found 4 APs). On 5GHz (ch36, ch149) only broadcast injection was verified; the per-AP test reported Found 0 APs, so no percentage was obtained this time, cause under investigation."
  - question: "What should I do if the iPhone shows 'Unable to Join the Network' or 'Incorrect Password' when AWUS036ACHM runs an AP?"
    answer: "First disable 802.11n: don't add ieee80211n=1 or ht_capab to the hostapd config; use pure hw_mode=g for 2.4GHz and pure hw_mode=a (20 MHz) for 5GHz. Otherwise hostapd repeatedly shows handle_assoc_cb: STA not found, which looks like an incorrect password but is actually an 802.11n association failure."
  - question: "Why can't an older iPhone connect to AWUS036ACHM's WPA3-SAE?"
    answer: "It's usually hostapd's sae_pwe setting. In testing, with sae_pwe=0 both iPhone 7 Plus and iPhone 15 Pro connect; with sae_pwe=2 the iPhone 7 Plus associates but the 4-way handshake fails and it drops, which looks like an incorrect password. Pair it with ieee80211w=2, and after changing the config have the iPhone forget the network and reconnect."
draft: false
---

> Tested by: Yopitek (ALFA Network's Taiwan distributor) | Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | Test device: our own iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro) | Test target: our own office Wi-Fi (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157).
>
> This article is a distributor's hardware verification of product compatibility and capability boundaries. All Monitor / Injection / AP / WPA3 tests were performed on Yopitek's own equipment, our own office Wi-Fi, against our own test phones — a legitimate capability check; it does not target any third-party network, nor does it provide attack procedures. The injection in this article only sends probe requests for a capability self-test, not attack packets.

## TL;DR

On the ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), the AWUS036ACHM works in dual-band monitor mode, reaches 96–100% packet injection on 2.4G (on 5G only broadcast injection was verified), and runs an AP hotspot on both bands (802.11n must be disabled).

- No driver install on Ubuntu 24.04: the MT7610U is handled by kernel 6.17's built-in mt76x0u, recognized on plug-in, no DKMS and no extra firmware.
- Dual-band monitor mode works; 2.4G packet injection is 96–100%.
- On 5GHz only broadcast injection was verified; the per-AP response rate was not obtained this time (cause under investigation).
- Running an AP requires disabling 802.11n; WPA3 requires `sae_pwe=0` for older iPhones to connect.
- Single-antenna 1T1R (AC600); throughput and positioning are a different class from the 2T2R ACM / ACH.

## 1. This Card and This Platform

The AWUS036ACHM is ALFA's single-antenna AC600 card, built on the MediaTek MT7610U, matching the Linux built-in driver `mt76x0u`. It's the single-stream sister to the AWUS036ACM (MT7612U, 2T2R): spec-wise it's 1T1R (AC600), one spatial stream short, but in exchange it offers a smaller form factor and community-recognized long-range reception. The morrownr/USB-WiFi community lists it on both the recommended Kali list and "The Short List," marking VIF, Active monitor, and WPA3 all as Yes, Very Long range, single-stream, in-kernel.

We plugged it into the ASUS GX10 (NVIDIA GB10, 128GB UMA, ARM64) and measured Monitor, Injection, AP, and WPA3-SAE item by item on Ubuntu 24.04 LTS, kernel 6.17. The conclusion first: this card works on this platform, and its 2.4GHz capabilities are quite complete. But there are two compatibility traps to know first: running an AP requires disabling 802.11n, and WPA3 requires `sae_pwe=0`; additionally, 5GHz per-AP injection was only verified as broadcast this time. The table below is the overall overview:

| Capability | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor (capture) | ✅ | ✅ |
| Injection | ✅ 96–100% | ⚠️ broadcast only, per-AP response rate not obtained |
| AP hotspot | ✅ (requires pure 802.11g) | ✅ (requires pure 802.11a, 20 MHz) |
| WPA3-SAE | ✅ (requires `sae_pwe=0`) | Not tested |

> Legend: ✅ tested and passed | 🟡 partial or single-node works | ⚠️ limited | ❌ unsupported or failed.

## 2. Hardware and Driver (No Install)

After plugging the ACHM into the GX10, kernel 6.17's built-in `mt76x0u` recognizes it directly, with no DKMS, no extra firmware, and no need to compile an out-of-tree driver from GitHub. Three commands to confirm the card:

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

The interface is named after the MAC (`wlx<MAC>`); the name stays the same after re-plugging, so you can bind it directly in scripts. The interface modes declared as supported by `iw phy info` include `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO`, covering all the scenarios this article tests.

The two platform-common safety rules apply to the ACHM as well: first, never run `airmon-ng check kill`, which shuts down NetworkManager and takes the GX10 offline; second, throughout, only operate the `wlx*` interface and never touch the built-in `wlP9s9` (the GX10's upstream main line). To enter monitor / AP, always use `iw` with `nmcli dev set $IF managed no`, never touching the system's main NIC.

## 3. Measured Capabilities: Monitor / Injection / AP / WPA3

### 3-1. Monitor (2.4 + 5 GHz) ✅

Capture is normal on both bands. On 2.4GHz channel 6, the 300-packet capture cap was filled in 8 seconds; on 5GHz it varies by frequency activity: ch36 (5180) filled 300 in 8 seconds, 5745 captured 254, 5785 captured 54 (few packets on a channel usually means there's no active AP on it at the moment, not a card problem).

A frequency-hop full-band scan best reveals a single-antenna card's reception:

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

The 120-second scan found 19 base stations and 14 clients, spread across ch1/2/5/6/36/149/157. For a single-stream AC600 card, this coverage is enough to be a stable capture source, and echoes the community's "Very Long range" rating.

### 3-2. Injection (2.4 + 5 GHz)

This is where the ACHM's two bands differ most, and something to watch carefully during selection.

A `aireplay-ng --test` capability self-test on 2.4GHz channel 6 gave a beautiful result:

```text
Injection is working!
Found 4 APs
30/30: 100%
```

The four base stations' response rates landed at 96–100%; injection capability is complete.

But switching to 5GHz (both ch36 and ch149 were tried) is different:

```text
Injection is working!
Found 0 APs
```

In other words, 5GHz broadcast injection works (the driver reports `Injection is working!`), but `aireplay-ng --test`'s per-AP response rate is `Found 0 APs` on both 5G channels, with no percentage obtained this time. This is the measured behavior of the ACHM single-antenna card on this platform; the cause is still being traced, and we won't make up a number we didn't measure. Honestly: if your use case needs stable 5GHz per-AP injection, the ACHM only verified a complete injection rate on 2.4GHz this time.

### 3-3. AP Hotspot (2.4 + 5 GHz) ✅ — but 802.11n must be disabled

The ACHM's first compatibility trap is here. When running an AP, don't add `ieee80211n=1` or `ht_capab` to the hostapd config: 2.4GHz uses pure `hw_mode=g`, 5GHz uses pure `hw_mode=a` (20 MHz). A minimal working 2.4GHz config looks like this:

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# Pure 802.11g, don't add ieee80211n=1 or ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=change-this-to-your-password-at-least-8-chars
```

In testing, the iPhone 7 Plus connected on both bands: on 2.4GHz you can see `AP-STA-CONNECTED` followed by `EAPOL-4WAY-HS-COMPLETED`; on 5GHz (ch36, 20 MHz) it measured -71 dBm, rx 54 Mbit, `authorized: yes`.

Conversely, if the config keeps `ieee80211n=1`, hostapd repeatedly spews `handle_assoc_cb: STA not found`, and the iPhone shows "Unable to Join the Network" or "Incorrect Password" — but that's actually an 802.11n association failure, not a password problem. Removing 802.11n fixes it. The ACHM is a single-antenna card; the 5GHz AP used 20 MHz this time and VHT80 was not tried.

### 3-4. WPA3-SAE ✅ — but `sae_pwe=0` is required (the easiest trap to hit)

The ACHM's second, and most-worth-calling-out, compatibility trap. For WPA3-SAE, hostapd's `sae_pwe` controls how the password element is derived: `0` is Hunting-and-Pecking only, `1` is Hash-to-Element (H2E) only, `2` is both (supporting Hunting-and-Pecking and H2E at once). The difference directly decides whether an older iPhone connects:

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 forces PMF
ieee80211w=2
# Key: compatibility with older endpoints like the iPhone 7 Plus
sae_pwe=0
sae_password=change-this-to-your-password
```

Measured comparison:

- `sae_pwe=0`: iPhone 15 Pro and iPhone 7 Plus **both connect** (`authorized: yes`, `MFP: yes`).
- `sae_pwe=2`: the iPhone 7 Plus **associates but the 4-way key handshake fails and it drops**, which on the surface again looks like "incorrect password"; the iPhone 15 Pro can connect.

The conclusion is direct: to be compatible with older iPhones (including 2016 models like the iPhone 7 Plus), hostapd must set `sae_pwe=0`. After changing the config, have the iPhone "forget this network" and reconnect, to avoid a false failure from a leftover association state. In the nine-card master table, the ACHM's WPA3 field is specially marked with "✅*" (with an asterisk).

## 4. Advanced Capabilities and Limitations

First, a table to consolidate the ACHM's full coverage and status this time, with the key points expanded in the sections below:

| Feature | Status | Key measured point |
|---|---|---|
| Monitor (2.4 + 5 GHz) | ✅ | 120s frequency-hop scan found 19 APs + 14 clients |
| Injection 2.4 GHz | ✅ | Response rate 96–100% |
| Injection 5 GHz | ⚠️ | Broadcast works, per-AP response rate not obtained |
| AP (2.4 + 5 GHz) | ✅ | iPhone connects on both bands, 802.11n must be disabled |
| WPA3-SAE | ✅* | Tested on 2.4 GHz (5 GHz not tested); both old and new iPhones connect, `sae_pwe=0` required |
| VIF (STA+AP, AP+monitor) | ✅ | Hotspot while online, download 198 Mbit/s |
| WPA handshake capture | ✅ end-to-end (.22000, on 5 GHz ch36) | Deauth our own iPhone, capture a complete 4-way M1–M4, export hashcat `.22000` |
| Active monitor | 🟡 | Capture configurable, ACK not verified |
| Ad-hoc (IBSS) | 🟡 | Creatable single-node, not interconnected with a second node |
| Mesh (802.11s) | 🟡 | Can join single-node, no peer link |
| Wi-Fi Direct (P2P) | ⬜ | Needs a second device, skipped |

> ✅* = WPA3-SAE works but requires `sae_pwe=0`; see Section 3-4.

**VIF (virtual interfaces, same channel, up to 2 interfaces).** The ACHM supports splitting one card into multiple interfaces running at once, provided each VIF uses a different MAC, the AP VIF is not handed to NetworkManager, all VIFs are on the same channel, and the ACHM additionally needs 802.11n disabled on the AP. Both combinations were tested:

- **STA + AP (online while acting as a hotspot)**: while the iPhone 7 Plus is connected to the AP (-66 dBm, authorized), the main interface is connected to YUPITEK, ping 30/30, avg 3.2 ms, download 198 Mbit/s.
- **AP + Monitor**: capturing while the AP is running, 300 frames in 8 seconds, including 46 beacons from our own AP.

**handshake capture.** The ACHM completed the end-to-end chain on 5 GHz (ch36): deauth our own iPhone, capture a complete 4-way (M1–M4), and export a hashcat `.22000`. It is one of the 7 of 9 cards that completed end-to-end (ACM, ACHM, ACH, ACS, EACS, AX, AXER). Its 5GHz per-AP injection response rate (`aireplay-ng --test`) was still not obtained.

**mesh / IBSS (creatable single-node).** This is the mt76 family's difference versus Realtek rtw88/rtw89. IBSS (Ad-hoc) reaches `Joined IBSS` in about 9 seconds and can emit beacons; Mesh (802.11s) can enter `type mesh point` and emit mesh beacons. Both were single-node only this time with no second-node interconnect (skipped for lack of a second device), so marked 🟡. Realtek's rtw88/rtw89 cards (such as the AWUS036ACH), though they can create single-node IBSS on this platform, do not support 802.11s mesh, so for 802.11s mesh experiments the two mt76 cards ACM and ACHM are instead among the few choices.

**Active monitor 🟡.** Configurable and capture is normal, but the ACK reply behavior needs a second device to verify and was not verified this time.

**Kali tools (platform-level, common across cards).** `airmon-ng`, `kismet`, `bettercap`, `wifite` (git version), and Wireshark/tshark can all use the ACHM as a source; only `hcxdumptool` on this platform `failed to arm interface` (except the AWUS036EACS on 2.4 GHz; the built-in driver has no active-monitor support), so for capture use `airodump-ng` with the aircrack-ng suite. Also note for ARM64: `aircrack-ng` often lacks a prebuilt package and must be compiled from source, and `wifite` is best used from the GitHub version to bypass apt dependency conflicts.

## 5. Use Cases and Selection (back to the Hub)

Placing the ACHM back into the nine-card selection context, its position is clear:

**Suitable for**

- **mesh (802.11s) experiments**: the mt76 driver can create 802.11s mesh (and IBSS) single-node; Realtek cards can create single-node IBSS but cannot do 802.11s mesh.
- **long-range single-stream monitor capture**: a 120s frequency-hop scan found 19 APs + 14 clients, rated Very Long range by the community.
- **2.4GHz injection, and AP / WPA3 hotspot**: 2.4G injection 96–100%, and with `sae_pwe=0` set correctly, both old and new iPhones connect to WPA3.

**Watch out for (honest limitations)**

- 5GHz per-AP injection was only verified as broadcast this time, no percentage.
- Running an AP requires disabling 802.11n, and WPA3 requires `sae_pwe=0`; getting either wrong will make an older iPhone "look like an incorrect password."
- Single-antenna 1T1R; throughput and positioning are a different class from the 2T2R ACM / ACH.

**Selection guidance**: if your core need is stable injection on both bands plus end-to-end handshake, the AWUS036EACS / AWUS036ACH / AWUS036ACS among the nine are more suitable; for Wi-Fi 6 + AP hotspot, look at the AWUS036AX / AWUS036AXER; if the focus is mesh / IBSS single-node experiments or long-range capture, the ACHM (or its 2T2R sister the ACM) is the right tool. A final trap warning: for injection / handshake use, don't choose the AWUS036AXM / AXML — their MT7921 injection fails on this platform.

For the full nine-model hardware, driver, Monitor / Injection / AP / WPA3 matrix and use-case-based selection review, see the Hub master table: [Full Test Matrix of 9 ALFA Wireless NICs on ARM64 / GX10](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## FAQ

**Q: Does AWUS036ACHM need a driver on Ubuntu 24.04?**
No. The MT7610U is handled by the kernel's built-in mt76x0u driver; Ubuntu 24.04 (kernel 6.17) recognizes it on plug-in with no DKMS and no extra firmware; lsusb shows USB ID 0e8d:7610.

**Q: Can AWUS036ACHM enter monitor mode? How many APs can it scan?**
Yes. Both 2.4GHz and 5GHz can enter monitor mode; a 120-second full-band frequency-hop scan with airodump-ng found 19 APs and 14 clients, spread across ch1, 2, 5, 6, 36, 149, 157.

**Q: What is AWUS036ACHM's packet injection success rate? Does 5GHz work?**
On 2.4GHz channel 6, per-AP injection response rate was 96–100% (aireplay-ng --test, found 4 APs). On 5GHz (ch36, ch149) only broadcast injection was verified; the per-AP test reported Found 0 APs, so no percentage was obtained this time, cause under investigation.

**Q: What should I do if the iPhone shows "Unable to Join the Network" or "Incorrect Password" when AWUS036ACHM runs an AP?**
First disable 802.11n: don't add ieee80211n=1 or ht_capab to the hostapd config, use pure hw_mode=g for 2.4GHz and pure hw_mode=a (20 MHz) for 5GHz. Otherwise hostapd repeatedly shows handle_assoc_cb: STA not found, which looks like an incorrect password but is actually an 802.11n association failure.

**Q: Why can't an older iPhone connect to AWUS036ACHM's WPA3-SAE?**
It's usually hostapd's sae_pwe setting. In testing, with sae_pwe=0 both iPhone 7 Plus and iPhone 15 Pro connect; with sae_pwe=2 the iPhone 7 Plus associates but the 4-way handshake fails and it drops, which looks like an incorrect password. Pair it with ieee80211w=2, and after changing the config have the iPhone forget the network and reconnect.

## 6. Further Reading

- [Hub master table] Full Monitor, Injection, AP matrix and selection review of 9 ALFA wireless NICs on ASUS GX10 (ARM64 / Ubuntu 24.04) → [/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Sister model] AWUS036ACM (MT7612U / 2T2R) card-by-card test — internal link pending (placeholder)
- [Platform guide] No driver install: using in-kernel drivers to enable ALFA NIC Monitor and AP on Ubuntu 24.04 + kernel 6.17 — internal link pending (placeholder)
- [Feature] Handshake capture capability and `sae_pwe` compatibility traps in the WPA3-SAE era — internal link pending (placeholder)

---

*Tested by: Yopitek (ALFA Network's Taiwan distributor) — https://www.yupitek.com | Test environment: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Test device: Apple iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro). Data cited from the hands-on test reports of 2026-11-16 to 11-18; does not target any third-party network, nor does it provide attack procedures.*
