---
title: "Enterprise Wireless Security Assessment: A Complete Framework"
description: "Complete enterprise wireless security assessment framework using ALFA adapters. Covers scoping, rogue AP detection, WPA2/WPA3 audit, PMF testing, and reporting for IT security teams."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
---

{{< alert "triangle-exclamation" >}}
**Legal Notice:** All wireless security assessments must be conducted only on networks and infrastructure for which you have received explicit, written authorization. Unauthorized wireless monitoring, injection, or rogue AP deployment is illegal in most jurisdictions. Every phase described in this framework assumes a properly executed engagement letter, signed by the asset owner, covering the specific testing window and authorized scope. Authorized testing only.
{{< /alert >}}

Enterprise wireless security assessment is not simply about asking "can we crack the password." A thorough assessment examines every layer of your wireless architecture: the strength of authentication protocols, the integrity of management frame protection, the accuracy of your authorized AP inventory, the robustness of client isolation on guest segments, and the resistance of your 802.1X infrastructure to rogue RADIUS attacks.

This framework covers the complete assessment lifecycle as practiced by professional penetration testing teams working in enterprise environments. It is structured as six sequential phases — scoping and pre-engagement, passive reconnaissance, rogue AP detection, WPA2/WPA3 handshake analysis, PMF verification, client isolation testing, and EAP/RADIUS assessment — followed by a reporting template and toolkit reference. Every phase is designed to be executed with ALFA Network adapters, which provide the monitor mode stability, injection capability, and multi-band coverage that enterprise-grade wireless testing demands.

Whether you are a CISO commissioning an annual wireless audit, an internal red team preparing an assessment, or an external penetration testing firm onboarding a new enterprise client, this framework provides a repeatable, defensible methodology.

---

## Scope and Pre-Engagement Requirements

The quality of any wireless assessment is determined before a single packet is captured. Poorly scoped engagements waste time, create legal exposure, and produce findings that cannot be attributed to specific infrastructure. A well-constructed scope document eliminates ambiguity and protects both the testing team and the client.

### What Must Be in the Scope Document

The scope document must enumerate, at minimum:

- **All SSIDs under test**, including corporate SSIDs, guest SSIDs, IoT-dedicated SSIDs, and any hidden networks known to the network team
- **Frequency bands in use**: 2.4 GHz, 5 GHz, and 6 GHz (Wi-Fi 6E) — each band may present different AP models, driver behavior, and security configurations
- **Physical perimeter**: a building or campus map with floor plans indicating known AP placement, particularly relevant for multi-tenant buildings where neighboring SSIDs may appear in scan results
- **Authorized AP inventory**: the MAC address (BSSID) list of every legitimate access point, used as the baseline for rogue AP detection
- **Authorization letter** signed by the CISO, CTO, or delegated asset owner, explicitly covering the testing window (start and end date/time), the names of the testing team members, and the specific activities authorized (passive scanning, active injection, deauthentication, rogue AP simulation)

### Out of Scope by Default

Unless explicitly included in writing, the following are always out of scope:

- **Client devices**: laptops, mobile phones, and IoT endpoints connecting to the wireless network. Client-side attacks (credential harvesting via rogue RADIUS) may only be performed on designated test devices, never on production user equipment
- **Guest network users**: individuals connecting to a publicly accessible guest SSID have no expectation of being subjects of a security test
- **Adjacent networks**: SSIDs belonging to neighboring tenants in a shared building, even if they are visible in passive scans

### Legal Reminder

{{< alert "triangle-exclamation" >}}
**Always obtain written authorization** that specifies the exact testing window (dates, start time, end time, time zone), the names and MAC addresses of testing equipment, and the specific techniques authorized. A verbal go-ahead is not sufficient. Store the signed authorization letter with your engagement file and have it accessible during testing in case of law enforcement contact.
{{< /alert >}}

---

## Phase 1: Passive Reconnaissance

### Goals

Passive reconnaissance establishes the ground truth of the wireless environment without transmitting a single byte. The objectives are:

- Identify every AP broadcasting within range, including those not in the authorized inventory
- Record SSID, BSSID, operating channel, signal strength, and security settings (encryption type, PMF status)
- Detect hidden SSIDs through probe responses
- Identify co-channel and adjacent-channel interference that may affect test reliability

During passive reconnaissance, **do not inject, do not deauthenticate, do not transmit**. This phase is entirely listen-only.

### Tools

**airodump-ng** is suitable for snapshot scans and handshake capture. For continuous logging with richer metadata, **Kismet** is preferred — it produces structured logs that can be imported into reporting tools and correlates probe requests to device identities over time.

```bash
# Passive scan across all bands — DO NOT inject or deauth during recon
sudo airodump-ng wlan0mon --band abg -w enterprise_recon

# Kismet for comprehensive, continuous logging
sudo kismet -c wlan0mon
```

Kismet writes `.kismet` SQLite database files and `.pcapng` captures simultaneously, giving you a persistent record that survives the assessment window.

### What to Record

For each discovered AP, record:

| Field | Notes |
|---|---|
| BSSID | MAC address of the AP radio |
| SSID | Network name (empty if hidden) |
| Encryption | WPA2-PSK, WPA2-Enterprise, WPA3-SAE, WPA3-Enterprise, Open |
| Channel | Note dual-radio APs appearing on both 2.4 and 5 GHz |
| Signal (dBm) | Useful for physical location estimation |
| PMF Status | Extract from RSN IE in beacon frames: Required / Capable / Disabled |
| Vendor | Derive from BSSID OUI — useful for identifying unauthorized consumer-grade hardware |

### Adapter Recommendations

- **AWUS036AXML** — Tri-band (2.4/5/6 GHz), required for detecting Wi-Fi 6E APs operating on 6 GHz channels. Essential in modern enterprise environments deploying Wi-Fi 6E infrastructure
- **AWUS036ACH** — Dual-band (2.4/5 GHz), reliable RTL8812AU chipset, excellent for environments where 6 GHz is not in use and maximum compatibility with existing tooling is preferred

---

## Phase 2: Rogue AP Detection

A rogue access point is any AP operating within your environment that is not in the authorized AP inventory. Two categories are operationally relevant:

1. **Unauthorized AP connected to the internal network** — a well-intentioned employee plugs in a consumer router, or an attacker who has gained physical access installs a hidden AP on an Ethernet drop. These APs are on your internal network and bypass all perimeter controls.
2. **Evil twin AP** — an AP broadcasting a legitimate-looking SSID (identical to or closely mimicking the corporate SSID) operated by an attacker to capture credentials or perform man-in-the-middle attacks. These are typically not connected to your network.

### Detection Method

Compare the BSSID list from your passive reconnaissance against the authorized AP inventory provided during scoping. Any BSSID broadcasting a corporate SSID that is not in the inventory is a rogue AP candidate.

```bash
# Filter scan output for corporate SSID to isolate all APs broadcasting it
sudo airodump-ng wlan0mon | grep "CorporateSSID"

# Compare discovered BSSIDs against authorized list (example using diff)
# Save airodump BSSID column to discovered.txt, authorized list to authorized.txt
diff <(sort discovered.txt) <(sort authorized.txt)
```

Any BSSID appearing in `discovered.txt` but not in `authorized.txt` is a finding.

### Deauthentication-Based Detection (If Authorized)

If deauthentication is explicitly in scope, you can use client reconnection behavior to determine whether a rogue AP is connected to the internal network: deauth a client from the suspect AP, observe whether the client reassociates to a legitimate AP on the same SSID. If the client roams cleanly, the rogue AP may share the same backend network. If the client fails to reconnect, the rogue AP is likely isolated (evil twin scenario).

### WIDS Validation

If the organization has deployed a Wireless Intrusion Detection/Prevention System (WIDS/WIPS), this phase should include a controlled test to verify the WIDS detects the test rogue AP within an acceptable time window. Deploy a test AP with the corporate SSID using a non-inventory MAC address and measure detection latency. A detection window exceeding 60 seconds represents a meaningful gap in coverage.

---

## Phase 3: WPA2/WPA3 Handshake Analysis

### WPA2: 4-Way Handshake Capture

Capturing the WPA2 4-way handshake allows offline verification that the network's passphrase meets the organization's password complexity policy. This is not an endorsement of passphrase cracking as an engagement goal — rather, it is a compliance verification: can the captured hash be cracked within a reasonable time by an adversary using commodity hardware?

```bash
# Target specific AP on channel 6 and write capture to file
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Convert captured .cap to hashcat format for offline audit
hcxpcapngtool -o hash.hc22000 handshake-01.cap
```

Submit the resulting `.hc22000` hash to an offline password auditor against the organization's approved word list and rule set. If the passphrase is recoverable against common password lists (rockyou, company name variations, keyboard walks), report as a Medium or High finding depending on the SSID's network access level.

### WPA3: SAE and Transition Mode

WPA3 uses Simultaneous Authentication of Equals (SAE), which provides forward secrecy and is resistant to offline dictionary attacks. However, many organizations deploy **WPA3 Transition Mode** to maintain compatibility with WPA2 clients — this mode accepts both SAE and PSK authentication. Test whether an attacker can force a WPA3 client to downgrade to WPA2 by presenting a WPA2-only beacon for the same SSID; a successful downgrade is a High finding.

For more detail on WPA3-specific testing, see our [WPA3 security testing guide](/en/blog/wpa3-security-testing-alfa-2026/).

---

## Phase 4: PMF (Protected Management Frames) Testing

### Why PMF Matters

802.11w Protected Management Frames (PMF) prevent deauthentication and disassociation attacks. Without PMF, an attacker can send forged deauth frames to any client, forcing disconnection and enabling handshake capture, credential harvesting via rogue AP, or simple denial-of-service. PMF is mandatory in WPA3 and optional (but strongly recommended) in WPA2.

### Test Procedure

Attempt a deauthentication attack against a test client associated with each SSID under test. The result reveals whether PMF is enforced:

```bash
# Attempt deauthentication flood against AP
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon

# If connected test client disconnects: PMF NOT enforced — reportable finding
# If test client remains connected: PMF enforced — pass
```

Always perform this test against designated test equipment, never against production clients.

### Reporting PMF Status

Document each SSID with its PMF enforcement level:

| SSID | Encryption | PMF Status | Finding |
|---|---|---|---|
| Corp-WiFi | WPA2-Enterprise | Capable (not required) | Medium |
| Corp-WiFi-6E | WPA3-Enterprise | Required | Pass |
| CorpGuest | WPA2-PSK | Disabled | High |

**PMF Disabled on any SSID** is at minimum a Medium finding. PMF Disabled on a corporate SSID with access to internal resources is High. For full details on PMF testing methodology, see our [packet injection guide](/en/blog/packet-injection-guide/).

---

## Phase 5: Client Isolation Testing

### Guest Network Isolation

Guest SSIDs must enforce client isolation — the inability for one guest client to communicate directly with another guest client. Without isolation, a malicious actor on the guest network can conduct ARP poisoning, LLMNR/NBT-NS spoofing, or direct attacks against other guests.

**Test procedure:**

1. Connect two dedicated test devices (not production user devices) to the guest SSID
2. From Device A, attempt ICMP ping to Device B's IP address
3. From Device A, attempt an ARP scan of the guest subnet

A guest SSID that fails client isolation (pings succeed between test devices) is a High finding.

### Guest-to-Internal Isolation

Verify the guest network cannot reach internal network ranges:

```bash
# From a test device on guest SSID, ARP scan the internal network range
sudo arp-scan -l --interface wlan0
# Zero responses from internal range = pass
# Any response from internal range = Critical finding
```

Additionally, attempt DNS resolution of internal hostnames and direct TCP connections to internal management interfaces (SSH, HTTP admin panels). Any successful connection from the guest segment to internal infrastructure is a Critical finding.

---

## Phase 6: EAP/RADIUS Assessment (Enterprise SSIDs)

### 802.1X Authentication and the Rogue RADIUS Attack

WPA2-Enterprise and WPA3-Enterprise use 802.1X EAP authentication, where clients authenticate to a RADIUS server. The critical security control is **server certificate validation**: each client must verify the RADIUS server's certificate before submitting credentials. If clients do not validate the certificate, an attacker can deploy a rogue AP with a rogue RADIUS server and harvest NTLMv2 hashes or EAP credentials.

### Test Procedure

Deploy a rogue AP using `hostapd-wpe` configured with the corporate SSID. This creates an 802.1X-capable AP backed by a rogue RADIUS server that logs all authentication attempts:

```bash
# Install hostapd-wpe
sudo apt install hostapd-wpe

# Configure with the corporate SSID and appropriate channel
# Edit /etc/hostapd-wpe/hostapd-wpe.conf with target SSID/channel details
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes in the output
```

**Critical finding:** If any client (including test clients that have previously connected to the production 802.1X SSID) connects to the rogue RADIUS without displaying a certificate warning, or if the user accepts a certificate warning and credentials are captured, this is a Critical finding. It indicates clients are not enforcing certificate pinning or proper chain validation.

**Remediation:** Deploy certificate pinning via MDM (Mobile Device Management) configuration profiles specifying the exact RADIUS server certificate or issuing CA. Ensure end users receive awareness training on rejecting unexpected certificate prompts.

---

## Assessment Toolkit Reference

The following tools cover the complete enterprise wireless assessment workflow. All are compatible with ALFA Network adapters in monitor mode. For adapter setup, see our guide on [enabling monitor mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/).

| Tool | Purpose | Recommended Adapter | Key Command |
|---|---|---|---|
| airodump-ng | Passive scanning, handshake capture | Any ALFA (AWUS036AXML / AWUS036ACH) | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID capture, passive handshake harvest | AWUS036AXML (Wi-Fi 6E) | `sudo hcxdumptool -i wlan0mon -o out.pcapng` |
| hcxpcapngtool | Convert captures to hashcat format | N/A (post-processing) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Kismet | Continuous logging, SSID/client correlation | AWUS036ACH | `sudo kismet -c wlan0mon` |
| aireplay-ng | PMF testing, deauth injection | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd-wpe | Rogue AP / rogue RADIUS for EAP testing | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |
| Wireshark | Packet-level analysis of captures | Any (via capture file) | `wireshark -r handshake-01.cap` |
| arp-scan | Guest/internal isolation verification | Any | `sudo arp-scan -l --interface wlan0` |

---

## Reporting Template

### Executive Summary

The executive summary should be readable by a CTO or CISO with no wireless security background. It must include:

- **Overall risk rating**: Critical / High / Medium / Low — derived from the highest confirmed finding severity
- **Key findings count** by severity tier
- **Compliance gap statement**: reference to any relevant standards (PCI-DSS 4.0 Requirement 11.2, ISO/IEC 27001 A.13.1, NIST 800-153) and whether the assessed wireless environment meets those requirements
- **Immediate action items**: findings that require remediation before the next business day

### Findings Table

All technical findings should be presented in a standardized table that maps each finding to a severity, affected infrastructure, and a concrete remediation recommendation:

| ID | Severity | Finding | Affected SSID(s) | Recommendation |
|---|---|---|---|---|
| WL-01 | Critical | Guest SSID has no client isolation; test devices communicated directly | CorpGuest | Enable AP client isolation in WLAN controller; verify via re-test |
| WL-02 | Critical | 802.1X clients connect to rogue RADIUS without certificate warning | Corp-WiFi | Deploy certificate pinning via MDM; configure RADIUS server CA trust anchor |
| WL-03 | High | PMF disabled on corporate SSID; deauth attack succeeded | Corp-WiFi | Enable PMF Required on all WPA2 SSIDs; upgrade to WPA3 where hardware allows |
| WL-04 | High | Rogue AP detected with corporate SSID on non-inventory BSSID | Corp-WiFi-5G | Investigate physical AP; deploy WIDS alert for unknown BSSIDs |
| WL-05 | Medium | WPA2 passphrase recoverable from common dictionary in under 4 hours | Corp-IoT | Enforce 16+ character random passphrase; rotate quarterly |
| WL-06 | Low | AP vendor/model identifiable from beacon OUI and probe responses | All | Consider AP fingerprint obfuscation if threat model warrants |

### Severity Definitions for Wireless Findings

| Severity | Definition | Example |
|---|---|---|
| Critical | Immediate, exploitable path to credential capture or internal network access | Open auth SSID, no encryption, guest-to-internal breach, 802.1X rogue RADIUS success |
| High | Significant control failure requiring prompt remediation | WPA2 with PMF Disabled, confirmed rogue AP on network, WPA3 downgrade attack success |
| Medium | Control gap that increases risk but requires additional conditions to exploit | Weak passphrase policy, WPA3 Transition Mode without downgrade protection |
| Low | Informational or defense-in-depth gap | AP model fingerprinting, SSID information disclosure |

---

## Related Resources

- [Packet Injection Guide: Testing Your WiFi Adapter with aireplay-ng](/en/blog/packet-injection-guide/)
- [WPA3 Security Testing with ALFA Adapters (2026)](/en/blog/wpa3-security-testing-alfa-2026/)
- [Enable Monitor Mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
