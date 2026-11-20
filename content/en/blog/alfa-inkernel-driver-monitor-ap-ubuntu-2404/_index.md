---
title: "No Driver Install: Enabling ALFA Monitor and AP Mode with In-Kernel Drivers on Ubuntu 24.04 + kernel 6.17 (rtw88 / rtw89 / mt76 tested)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "A no-driver-install guide for Ubuntu 24.04 / kernel 6.17: use the in-kernel rtw88 / rtw89 / mt76 drivers to enable ALFA adapter Monitor and AP mode, including WPA3 hotspot compatibility settings and Kali toolchain notes."
faq:
  - question: "How do I get an ALFA adapter into monitor mode on Ubuntu 24.04?"
    answer: "On kernel 6.17 or above, just hand the interface back from NetworkManager and switch it to monitor interface mode — no third-party driver needed; the rtw88 / rtw89 / mt76 driver families tested here follow an identical flow, with the detailed commands in the steps above."
  - question: "Why don't ALFA adapters need a separate driver install on Ubuntu?"
    answer: "Because Realtek rtw88 / rtw89 and MediaTek mt76 have gradually brought these USB chips into mainline in-kernel support (the minimum kernel differs per card, from 4.19 to 6.17; on Ubuntu 24.04, AX and AXER need kernel 6.17 or later, e.g. the 24.04.4 HWE); on kernel 6.17 (tested on the GX10) all 9 cards here are built in — recognized on plug-in, no compilation, no DKMS."
  - question: "My old iPhone can't connect when I run a WPA3 hotspot with an ALFA adapter. What do I do?"
    answer: "Testing found two common causes: first, hostapd's sae_pwe needs to be 0 rather than 2 for older iPhone compatibility; second, keeping 802.11n enabled can cause older devices to fail association, so when prioritizing compatibility, disabling 802.11n is recommended."
  - question: "Which of rtw88, rtw89, mt76 supports mesh or IBSS?"
    answer: "In testing, the mt76 family (e.g. AWUS036ACM / ACHM) can establish mesh (802.11s) and IBSS single-node; Realtek rtw88 can join IBSS single-node (per the ACH test) but does not support mesh, and rtw89 does not even declare IBSS support."
draft: false
---

> This is a standard Linux networking configuration guide, demonstrating how to use the **in-kernel (built-in) driver** on a recent kernel to enable Monitor and AP (hotspot) mode on ALFA Wi-Fi adapters.
> Test platform: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. All data are excerpts from Yupitek's product-compatibility testing on its own equipment and its own office Wi-Fi (SSID `YUPITEK`).
> ⚠️ **Legal use**: Monitor mode is only for listening to networks you own or are authorized to test; AP mode must comply with local radio regulations. This article involves no attack operations against any third-party network.

---

## Summary (TL;DR)

On the ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), all 9 ALFA USB Wi-Fi adapters tested by Yupitek (ALFA Network's Taiwan distributor) run on in-kernel drivers (`rtw88` / `rtw89` / `mt76`) with no driver install, enable Monitor and AP mode through the same flow, and let the iPhone 7 Plus / 15 Pro connect normally under 2.4G and 5G AP; the minimum kernel ranges from 4.19 to 6.17 depending on the card.

- **No driver install on recent kernels**: Realtek `rtw88` / `rtw89` and MediaTek `mt76` already include these ALFA USB chips in in-kernel support; on kernel 6.17 (tested on the GX10) all 9 cards are built in, though the minimum kernel differs per card — plug and play, no compilation, no DKMS.
- **The Monitor and AP flow is identical across the three families**: hand the interface back from NetworkManager → `iw` to switch to monitor / `hostapd` to bring up an AP.
- **Two compatibility pitfalls**: when running an AP, disabling 802.11n is recommended (`ieee80211n=0`), and WPA3-SAE should use `sae_pwe=0`, otherwise older iPhones cannot connect.
- **Advanced mode tiers**: mesh is `mt76` only; for IBSS single-node, `mt76` and `rtw88` (ACH) can join, while `rtw89` does not declare it.
- **Platform iron rule**: never run `airmon-ng check kill` (it disconnects the GX10); only operate the external `wlx*` interface.

## 1. Why "No Driver Install" Is the Headline This Generation

Historically, the most common hurdle when using ALFA-style USB Wi-Fi adapters on Linux was the driver. Chips like the RTL8812AU and MT7610U were not in the mainline kernel in the early days, so users had to grab an out-of-tree project from GitHub (e.g. `morrownr/USB-WiFi`, `aircrack-ng/rtl8812au`) and compile it against the current kernel version through DKMS. Every kernel update meant another DKMS rebuild; and once a build failed, the adapter simply vanished. For distributor validation or teaching environments that need stable operations, this was a long-standing pain point.

Recent mainline kernels turned things around: Realtek's `rtw88` and `rtw89` and MediaTek's `mt76` — the three major driver families — gradually brought these USB chips into official in-kernel support. The minimum kernel differs per card (see the "Min. kernel" column below); on kernel 6.17 (tested on the GX10) all nine cards tested in this article are built in — **recognized on plug-in, no compilation, no DKMS**. More importantly, the two most-used out-of-tree projects (morrownr's and aircrack-ng's rtl8812au) now both redirect to this in-kernel driver, and bug reports are consolidated back to `lwfinger/rtw88`. In other words, the manual driver-compilation step can now simply be skipped on recent kernels.

The `lwfinger/rtw88` community is still actively maintained and keeps sending fixes upstream, so the in-tree driver's stability improves alongside the kernel. Users no longer maintain their own branches, nor get blocked by a DKMS build failure on every upgrade. For distributor validation and teaching environments, the same operating steps can be reused across many cards and across many kernel updates, and the maintenance cost drops noticeably — which is why this article focuses on "no driver install."

The chips and their corresponding in-kernel driver modules covered in this test are as follows:

| Chip family | Chip model | In-kernel driver module | Min. kernel | Generation / streams | Representative card |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1 (+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> If your system's kernel is below the minimum version for your card (see the table above), you'll need the old path: install an out-of-tree driver via DKMS (`lwfinger/rtw88` for the rtw88 cards). On Ubuntu 24.04, for example: the GA kernel 6.8 already includes the drivers for ACM, ACHM, AXM, AXML and EACS; HWE 6.14 adds ACH and ACS. AX and AXER need kernel 6.17 or later (e.g. the 24.04.4 HWE). This article is based on the GX10's kernel 6.17.

---

## 2. Confirm the Driver Is Loaded and Bound

Before switching to any mode, first confirm the card is correctly recognized, the driver is bound, and the interface name is generated. Using Realtek's AWUS036ACH (`rtw88_8812au`) as an example, here are the four check steps.

**Step 1: Confirm the USB device is enumerated.** Use `lsusb` to find the USB ID (Realtek is usually `0bda:xxxx`, MediaTek usually `0e8d:xxxx`):

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Step 2: Confirm driver binding and USB rate.** `lsusb -t` shows both the bound driver and the link speed at once (`5000M` means USB 3.0):

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

For MediaTek cards, use `dmesg` instead to observe the driver initialization messages and confirm the interface rename:

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**Step 3: Get the interface name.** Ubuntu uses predictable naming, and ALFA external cards are always `wlx` plus the MAC address. This name is determined by the MAC and **does not change after unplug/replug**, which is convenient for scripting. The built-in uplink NIC has a different name (on the GX10 it's `wlP9s9`), so be sure to tell them apart:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**Step 4: Query the interface modes the chip declares it supports.** This step determines which modes will be usable later:

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Realtek rtw88 (ACH) lists `IBSS / managed / AP / AP/VLAN / monitor`, but **not** mesh or P2P; MediaTek mt76 (ACHM) additionally lists `mesh point / P2P-client / P2P-GO`. This list is the firsthand basis for each family's capability differences — see Section 5.

---

## 3. Enabling Monitor Mode (2.4 GHz / 5 GHz)

Monitor mode lets the adapter associate with no AP and directly receive 802.11 frames from the air, commonly used for packet diagnostics, spectrum surveys, and signal-coverage assessment on your own network. The enabling flow is identical across the three families; only the per-family stability notes differ (see Sections 5 and 6).

**Common enabling steps:**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # hand it back to us to manage, keeping NetworkManager out
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

Seeing `type monitor` means the switch succeeded. Next, specify the channel to monitor. For **2.4 GHz** use `set channel`:

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

For **5 GHz**, specifying by frequency is less error-prone (ch36 = 5180 MHz):

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**Expected result (test excerpt):** the AWUS036ACH captured 92 / 214 / 71 frames on ch1 / ch6 / ch11 respectively, and 260 / 137 / 127 frames on 5 GHz ch36 / ch149 / ch157, indicating both 2.4G and 5G monitoring work. The MediaTek ACHM, with `airodump-ng --band abg` hopping for 120 seconds, found 19 access points and 14 clients around ch1/5/6/36/149/157. Capturing 0 packets on some channel usually just means no AP was on that channel at the moment, not a card fault.

Once in monitor mode, common standard diagnostic tools run directly on the `wlx*` interface: `airmon-ng` lists card and driver status, `kismet` can act as a data source for live side-capture and produce a `.kismet` log, `Wireshark` and `tshark` parse the captured packets, and `bettercap` does channel surveying. These tools were all tested working across the three families and are well suited to surveying channel usage and signal coverage of your own wireless environment. The one thing to note is that `hcxdumptool` 8.x will `failed to arm` for all three families on this platform, except the EACS on 2.4 GHz (the in-kernel driver doesn't provide active-monitor); if you need similar functionality, switch to `airodump-ng` with the aircrack-ng suite.

> **5 GHz reminder:** under the default regdomain (`country 00`), many 5 GHz channels are passive/no-IR — monitoring is fine but active transmission is restricted. If you later do 5 GHz testing within authorized scope, first `sudo iw reg set US` to unlock, then `sudo iw reg set TW` to set it back when done. Realtek `rtw88_8812au` also has a known 5G RX-stuck behavior (after repeated mode switches, 5G stops receiving packets); when you hit it, physically unplug/replug the card once and do 5G first.

---

## 4. Enabling AP / Hotspot Mode (2.4 GHz / 5 GHz)

AP (hotspot) mode uses `hostapd` to turn the adapter into a Wi-Fi access point. The flow is the same across the three families: first hand the interface back from NetworkManager, then start it with a `hostapd` config file. Below is the common minimal configuration.

**4-1. 2.4 GHz (pure 802.11g)**

Create config file `/tmp/ap24.conf`:

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<your password, at least 8 characters>
```

Start it:

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

When a client connects, `hostapd` outputs `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED` in order; seeing the last line means the four-way handshake is complete and the connection succeeded.

**4-2. 5 GHz (pure 802.11a, ch36)**

Change the above config to 5 GHz:

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

2x2 cards (such as the rtw89 AX/AXER and the mt76 ACM/AXM) can add VHT80 settings to reach 80 MHz bandwidth; for single-antenna cards or when prioritizing compatibility, stick with pure 20 MHz a.

**4-3. Two key compatibility settings**

1. **Disabling 802.11n is recommended when running an AP** (`ieee80211n=0`, use pure g / pure a). In testing, older clients (iPhone 7 Plus) failed to associate when `ieee80211n=1` was kept, with the screen falsely reporting "wrong password" — the real issue was `handle_assoc_cb: STA not found`; removing 802.11n connected on the first try.
2. **Use `sae_pwe=0` for WPA3-SAE** (hunting-and-pecking). With `sae_pwe=2` (forced H2E), key exchange fails on older devices. WPA3 section example:

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

Both pitfalls occur equally on Realtek and MediaTek cards — they're client compatibility issues rather than driver differences. All nine cards tested here can let the iPhone 7 Plus / 15 Pro connect normally under 2.4G and 5G AP.

**4-4. Online and a hotspot at the same time (STA + AP)**

The mt76 family supports using one card to connect to an existing Wi-Fi and build another AP VIF as a relay hotspot at the same time. In testing, the ACHM opened a 5 GHz hotspot for an iPhone to join while its main interface stayed connected to YUPITEK, still getting 198 Mbit/s download and an average ping of 3.2 ms. This combination requires three conditions: the AP VIF must use a different MAC, the interface name must keep the `wlx` format, and all VIFs must be on the same channel. This combination is not guaranteed by the phy on Realtek cards (rtw88's managed + monitor works, but STA + AP is unstable), so for a relay hotspot prefer the mt76 family.

---

## 5. Three-Chip-Family Differences and Limitations

For the basic managed / monitor / AP trio of modes, all three families support them with consistent behavior. The differences are in the **advanced interface modes** (mesh, IBSS, active monitor, P2P): these depend entirely on driver declaration and have nothing to do with the card's antenna count. Here is the test summary.

| Advanced mode | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor (2.4G/5G) | ✅ | ✅ | ✅ |
| AP (hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS (single-node) | 🟡 can establish single-node | 🟡 can establish single-node | ❌ not declared by driver |
| Mesh (802.11s, single-node) | 🟡 can establish single-node | ❌ `-95` unsupported | ❌ not declared by driver |
| Active monitor | 🟡 configurable | ❌ `-95` unsupported | N/A |
| Wi-Fi Direct (P2P) | needs a second device | ❌ `-95` unsupported | N/A |

**MediaTek mt76 (ACM / ACHM / AXM / AXML)** is the most complete family for advanced modes. `iw phy info` declares `mesh point`, `IBSS`, `P2P-client/GO`. In testing it could `Joined IBSS` and `type mesh point` single-node and send the corresponding beacons (the peer link with a second device was unverified due to the missing second device). If your use case is mesh or IBSS single-node experiments, the mt76 family is the top pick. Note especially that the Wi-Fi 6 MT7921 (AXM/AXML), though complete in modes and stable as an AP, cannot do frame injection on this platform (the main cause is the mac80211 chanctx regression in stock kernel 6.16+, not inherent to the chip; the community's same-model units can work with a git / patched driver but the firmware locks the rate — see morrownr/USB-WiFi #387, morrownr/mt76 #18), making it unsuitable for advanced testing that needs injection.

**Realtek rtw88 (ACH / ACS / EACS)** supports `IBSS / managed / AP / AP/VLAN / monitor`. IBSS can be established single-node (`Joined IBSS`, per the ACH test; EACS lists the iftype but its join is ineffective in testing), but **mesh (802.11s), active monitor, and Wi-Fi Direct all return `Operation not supported (-95)` in testing**. Another rtw88-specific trait is VIF: although the `iw phy` flag says "interface combinations are not supported," the ACH test brought up managed + monitor on two interfaces at once, with the monitor VIF capturing 100 frames — so "online while side-capturing" is feasible; however the phy doesn't guarantee this combination, so for heavy, long-running loads still prefer the mt76 family.

**Realtek rtw89 (AX / AXER)** is the newest Wi-Fi 6 family in this article, with good monitor and AP (including VHT80) behavior and strong reception sensitivity. But for advanced modes, active monitor / mesh / IBSS / P2P are not even declared at the driver layer (N/A), so for these single-node experiments switch to an mt76 card. The rtw89's role is stable Wi-Fi 6 monitoring and hotspots, not a platform for experimenting with advanced interface modes.

> Selection in one line: **for mesh / IBSS single-node → mt76 (ACM / ACHM); for a Wi-Fi 6 hotspot and strong reception → rtw89 (AX / AXER); for dual-band general use and VIF → rtw88 (ACH).**

---

## 6. Platform Safety Notes (GX10 + Ubuntu ARM64)

On GX10-style machines where "the built-in NIC handles the Internet uplink and the external ALFA card does the testing," the following points are operational iron rules — follow them so you don't knock yourself offline.

1. **Never run `airmon-ng check kill`.** This command shuts down NetworkManager and, with it, the GX10's uplink. Throughout this article we only use `iw` and `nmcli dev set <interface> managed no`, never touching `check kill`.
2. **Only operate `wlx*`, never touch the built-in `wlP9s9`.** `wlP9s9` is the GX10's Internet uplink; any down / mode-change action must target the ALFA `wlx*` interface only, and always confirm the target with `echo $IF` before issuing a command.
3. **Recover from an RX stall by unplugging/replugging.** After repeatedly switching monitor / AP, if you can't scan anything, it's usually a driver RX stall (especially common on Realtek 5G). Software usually can't recover it — just **physically unplug and replug** the card once; USB re-enumerates and the interface name stays consistent since the MAC doesn't change.
4. **Switch USB ports for BT+WiFi combo cards.** For BT-plus-Wi-Fi combo devices like the EACS and AXML, on re-plug the Wi-Fi probe occasionally hangs and fails to create the `wlx` interface; switching to a different USB port usually fixes it.
5. **Set regdomain before 5 GHz transmission.** Under the default `country 00`, 5 GHz is mostly no-IR and active transmission is prohibited. Before testing within authorized scope, `sudo iw reg set US` to unlock, and `sudo iw reg set TW` to set it back afterward.
6. **ARM64 package notes.** The GX10 is aarch64; `aircrack-ng` often lacks a prebuilt wheel/package and must be built from source; `wifite` is best run from the GitHub version to bypass apt dependency conflicts. Also, `hcxdumptool` 8.x will `failed to arm` for all three families on this platform, except the EACS on 2.4 GHz (the in-kernel driver has no active-monitor support), so for capture use `airodump-ng` with the aircrack-ng suite.

**Restore normal mode after testing:**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # expect type managed
```

---

## Frequently Asked Questions (FAQ)

**Q: How do I get an ALFA adapter into monitor mode on Ubuntu 24.04?**
A: On kernel 6.17 or above, just hand the interface back from NetworkManager and switch it to monitor interface mode — no third-party driver needed; the rtw88 / rtw89 / mt76 driver families tested here follow an identical flow, with the detailed commands in the steps above.

**Q: Why don't ALFA adapters need a separate driver install on Ubuntu?**
A: Because Realtek `rtw88` / `rtw89` and MediaTek `mt76` have gradually brought these USB chips into mainline in-kernel support (the minimum kernel differs per card, from 4.19 to 6.17; on Ubuntu 24.04, AX and AXER need kernel 6.17 or later, e.g. the 24.04.4 HWE); on kernel 6.17 (tested on the GX10) all 9 cards here are built in — recognized on plug-in, no compilation, no DKMS.

**Q: My old iPhone can't connect when I run a WPA3 hotspot with an ALFA adapter. What do I do?**
A: Testing found two common causes: first, hostapd's `sae_pwe` needs to be 0 rather than 2 for older iPhone compatibility; second, keeping 802.11n enabled can cause older devices to fail association, so when prioritizing compatibility, disabling 802.11n is recommended.

**Q: Which of `rtw88`, `rtw89`, `mt76` supports mesh or IBSS?**
A: In testing, the `mt76` family (e.g. AWUS036ACM / ACHM) can establish mesh (802.11s) and IBSS single-node; Realtek `rtw88` can join IBSS single-node (per the ACH test) but does not support mesh, and `rtw89` does not even declare IBSS support.

## 7. Further Reading

- Full capability comparison and selection verdict for the 9 ALFA cards → [ALFA Wireless Adapter Overall Review Hub (master table)](/en/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Step-by-step guide for the representative Realtek rtw88 card → [AWUS036ACH single-card test](/en/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- Step-by-step guide for the representative MediaTek mt76 card → [AWUS036ACHM single-card test](/en/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*Testing unit: Yupitek (ALFA Network Taiwan distributor) — https://www.yupitek.com | Test environment: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Test device: Apple iPhone 7 Plus (WPA3 also tested with iPhone 15 Pro)*
