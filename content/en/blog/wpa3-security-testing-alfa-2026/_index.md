---
title: "WPA3 Security Testing with ALFA Adapters (2026)"
description: "Comprehensive guide to WPA3 security testing using ALFA Network adapters. Covers SAE handshake analysis, Dragonblood vulnerabilities, transition mode downgrade attacks, PMF enforcement, and WPA3-Enterprise EAP testing."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
---

{{< alert "triangle-exclamation" >}}
**Legal Notice:** All wireless security testing must be performed only on networks and devices for which you have explicit, written authorization. WPA3 testing techniques including SAE capture, deauthentication, and rogue AP deployment are subject to the same legal requirements as any other wireless assessment activity. Authorized testing only.
{{< /alert >}}

WPA3 represents a significant improvement over WPA2 in both personal and enterprise wireless security. Simultaneous Authentication of Equals (SAE) replaces the Pre-Shared Key (PSK) handshake with a password-authenticated key exchange that is resistant to offline dictionary attacks. Protected Management Frames (PMF) are mandatory. Forward secrecy is built in.

However, WPA3 is not without vulnerabilities. The Dragonblood research (2019) uncovered side-channel and denial-of-service vulnerabilities in the SAE handshake. Transition mode introduces downgrade attack surfaces. Enterprise deployments face the same 802.1X certificate validation weaknesses as WPA2-Enterprise. This guide covers the complete WPA3 security testing methodology using ALFA Network adapters, which provide the monitor mode stability and injection capability required for thorough assessment.

---

## WPA3 Fundamentals for Security Testers

### SAE: Simultaneous Authentication of Equals

SAE replaces the four-way handshake of WPA2-PSK with a zero-knowledge proof exchange based on the Dragonfly key exchange protocol. The key property that matters for security testing is **forward secrecy**: even if the Wi-Fi password is later compromised, previously captured traffic cannot be decrypted. This eliminates the primary value of offline passphrase cracking against a SAE-only network.

SAE also eliminates the vulnerability to PMKID attacks that affected WPA2. There is no equivalent offline-crackable artifact that a passive attacker can extract from a SAE association.

### PMF: Mandatory in WPA3

802.11w Protected Management Frames are mandatory in WPA3. Deauthentication and disassociation frames are cryptographically protected, preventing the forged deauth attacks that are trivially effective against WPA2 networks without PMF. A WPA3-only network should be immune to deauthentication-based handshake capture acceleration.

### WPA3 Transition Mode

The most common real-world deployment scenario is **WPA3 Transition Mode**: the AP accepts both WPA3-SAE and WPA2-PSK authentication simultaneously to maintain backward compatibility with devices that do not support WPA3. This mode is the primary attack surface in current enterprise environments — it reintroduces the WPA2 PSK handshake exposure on a network that advertises WPA3.

### WPA3-Enterprise

WPA3-Enterprise mandates a 192-bit security mode using GCMP-256 and HMAC-SHA-384, with certificate-based mutual authentication. It addresses the same certificate validation vulnerabilities as WPA2-Enterprise if not properly deployed. Testing methodology for the 802.1X layer is covered in the [enterprise wireless security assessment framework](/en/blog/enterprise-wireless-security-assessment/).

---

## Testing Environment and Adapter Requirements

### Adapter Selection

WPA3 testing requires an adapter with reliable monitor mode, injection support, and — for 6 GHz WPA3 networks — tri-band capability:

- **AWUS036AXML** — Required for Wi-Fi 6E (6 GHz) WPA3 networks. Mediatek MT7921AUN chipset. Full monitor mode and injection support on Kali Linux with kernel 5.18+. The only ALFA adapter that covers 6 GHz channels where WPA3-only deployments are increasingly common.
- **AWUS036ACH** — Suitable for 2.4/5 GHz WPA3 testing. RTL8812AU chipset. Maximum compatibility with the aircrack-ng toolchain and widest driver support across Kali Linux versions.

### Enable Monitor Mode

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0

# Verify monitor interface
iwconfig wlan0mon
```

For a full monitor mode setup guide, see [Enable Monitor Mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/).

### Identify WPA3 Networks in Scan Results

```bash
# Passive scan across all bands
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# Filter for WPA3 networks in results
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

In airodump-ng output, WPA3-SAE networks appear with `WPA3 SAE` in the AUTH column. Transition mode networks show `WPA2 WPA3 SAE PSK`. Open (OWE) enhanced networks show `OWE`.

---

## Phase 1: SAE Handshake Capture and Analysis

### Passive Capture Limitations

Unlike WPA2, **SAE handshakes cannot be used for offline dictionary attacks**. Capturing SAE commit and confirm frames is straightforward with any monitor mode adapter, but the captured material does not yield a crackable hash. The purpose of capturing SAE frames is for protocol-level analysis — verifying that the correct SAE variant is in use, confirming that PMF is negotiated, and providing evidence in the assessment report.

```bash
# Capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Analyze the capture in Wireshark
# Filter: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
# (0x000b = Authentication frame)
wireshark -r sae_capture-01.cap
```

In the Authentication frames, verify the SAE commit and confirm exchange. The RSN Information Element in Beacon frames should show:
- **AKM Suite**: 00-0F-AC:8 (SAE) for WPA3-Personal
- **PMF**: Required (MFPR bit set in RSN Capabilities)

### PMKID Testing on SAE Networks

Tools like `hcxdumptool` will attempt PMKID extraction on all networks, but SAE networks do not expose a crackable PMKID. Running the tool is worthwhile to confirm the absence of WPA2 PMKID exposure:

```bash
# Attempt PMKID capture — SAE networks should yield no crackable PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

# Convert and inspect
hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng

# An empty or absent hash file confirms no WPA2 PMKID exposure
wc -l wpa3_hashes.hc22000
```

If `hcxpcapngtool` outputs a populated `.hc22000` file for a network advertised as WPA3-only, this indicates the AP is operating in transition mode and exposing a WPA2 PMKID — a significant finding.

---

## Phase 2: Transition Mode Downgrade Attack Testing

### The Downgrade Attack Surface

WPA3 Transition Mode is the most impactful WPA3 vulnerability in current enterprise environments. When an AP operates in transition mode, it accepts both SAE and PSK associations. An attacker who can observe client probe requests can craft a rogue AP that presents only WPA2-PSK capabilities for the same SSID — if the client connects without requiring SAE, a standard WPA2 4-way handshake is captured and can be attacked offline.

### Test Procedure

```bash
# Step 1: Confirm the target is in transition mode (shows WPA2+WPA3 in airodump-ng)
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# Step 2: Capture the legitimate AP's beacon to note its channel and configuration
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# Step 3: Create a WPA2-only rogue AP on the same channel using hostapd
# Create /tmp/rogue_wpa2.conf:
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# Step 4: Monitor for client associations on the rogue AP
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**Critical finding:** If a client that previously connected via SAE associates to the WPA2-only rogue AP (evidenced by a 4-way handshake in the capture file), the client OS is not enforcing WPA3-SAE requirement. This represents a successful downgrade attack.

**Pass condition:** The client ignores the WPA2-only AP or displays an alert, and does not complete a WPA2 handshake.

### Downgrade Indicator in hcxpcapngtool Output

```bash
# Convert rogue AP capture — presence of hash confirms WPA2 association occurred
hcxpcapngtool -o downgrade_hash.hc22000 downgrade_capture-01.cap
cat downgrade_hash.hc22000
# Non-empty output = downgrade attack succeeded
```

---

## Phase 3: Dragonblood Vulnerability Assessment

### Background

The Dragonblood research (Vanhoef & Ronen, 2019) identified multiple vulnerabilities in the SAE handshake implementation:

- **CVE-2019-9494 / CVE-2019-9496**: Side-channel attacks (cache-based and timing-based) against the SAE commit frame, allowing offline dictionary attacks against unpatched implementations
- **CVE-2019-9499**: SAE confirmation bypass leading to WPA3-Personal downgrade to WPA2-PSK
- **DoS via SAE commit flooding**: Exhausting AP state tables by sending large numbers of SAE commit frames

Most modern AP firmware has patched the original Dragonblood vulnerabilities. However, testing for them remains relevant in environments with older or unpatched AP firmware.

### SAE Anti-Clogging Token Testing

WPA3-SAE includes an anti-clogging mechanism to prevent DoS via commit flooding. Test whether the target AP correctly implements anti-clogging:

```bash
# Install hcxtools
sudo apt install hcxtools

# Use hcxdumptool to observe SAE commit/confirm frame exchange rate limiting
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3

# In Wireshark, filter for Authentication frames and observe:
# wlan.fc.type_subtype == 0x000b
# Look for Anti-Clogging Token (ACT) responses in commit frames
wireshark -r dragonblood_test.pcapng
```

In a correctly implemented AP, rapid SAE commit requests from multiple source MAC addresses should trigger Anti-Clogging Token responses (the AP returns a token that must be included in subsequent commit frames). APs that do not implement ACT are vulnerable to SAE commit flooding DoS.

### Checking AP Firmware Version

AP firmware version is a strong indicator of patch status. Compare the discovered AP firmware version against vendor security advisories:

- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+ patches Dragonblood
- Ubiquiti: UniFi Network 6.0+ patches Dragonblood
- MikroTik: RouterOS 6.45.7+ patches Dragonblood

Document the AP firmware version in the assessment report. An AP running firmware predating these releases should be flagged as potentially vulnerable regardless of whether active exploitation was confirmed.

---

## Phase 4: PMF Enforcement Testing on WPA3 Networks

### Why PMF Testing Still Applies

Although PMF is mandatory in WPA3, testing the actual enforcement behavior matters because:

1. Transition mode APs may have PMF set to "capable" rather than "required" on the WPA2 path, allowing deauth attacks against WPA2-connected clients
2. AP misconfiguration may result in PMF not being negotiated even on SAE associations
3. Client implementations may not correctly enforce PMF even when the AP advertises it as required

### Deauthentication Test

```bash
# Attempt deauth against a test client associated via WPA3-SAE
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon

# Expected result on a correctly configured WPA3 network:
# - Test client does NOT disconnect (PMF-protected management frames dropped)
# - airodump-ng shows no handshake captured

# Failure condition (finding):
# - Test client disconnects and reassociates
# - airodump-ng captures a new handshake
```

### PMF Capability vs. Required

Check the RSN Information Element in beacon frames to confirm PMF configuration:

```bash
# Capture beacon frames and decode RSN IE
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

Output interpretation:
- `1,1` — PMF Required (MFPR=1, MFPC=1): Correct for WPA3
- `1,0` — PMF Capable but not Required: Medium finding on WPA3 networks, High on corporate SSIDs
- `0,0` — PMF Disabled: High finding on any WPA3-advertised network; indicates AP misconfiguration

---

## Phase 5: OWE (Opportunistic Wireless Encryption) Testing

### OWE Overview

OWE (Wi-Fi Enhanced Open) is the WPA3 replacement for completely open (unencrypted) guest networks. OWE performs an unauthenticated Diffie-Hellman key exchange to establish per-session encryption without requiring a password. It protects against passive eavesdropping on guest networks but provides no authentication.

### Testing OWE Transition Mode

Many APs deploy OWE in transition mode alongside a legacy open SSID (the open SSID is hidden, the OWE SSID is visible). Test whether clients can be forced to connect to the legacy open SSID:

```bash
# Scan for hidden SSIDs paired with OWE networks
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"

# A hidden SSID with no encryption paired with an OWE SSID is the transition SSID
# Clients with WPA3 support should prefer OWE; legacy clients fall back to open
```

**Finding:** If a WPA3-capable client connects to the open transition SSID instead of the OWE SSID, the client OS is not correctly handling OWE transition mode. All traffic from that client is unencrypted.

---

## Phase 6: WPA3-Enterprise Assessment

### 192-Bit Security Mode Verification

WPA3-Enterprise mandates GCMP-256 encryption and HMAC-SHA-384 authentication in the 192-bit security mode. Verify via the RSN IE in beacon frames:

```bash
# Capture and decode RSN IE for enterprise SSID
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

Expected values for WPA3-Enterprise 192-bit:
- **Pairwise Cipher Suite**: GCMP-256 (00-0F-AC:9)
- **AKM Suite**: EAP-SHA384 (00-0F-AC:12) or FT-EAP-SHA384 (00-0F-AC:13)

Presence of CCMP-128 on a WPA3-Enterprise network is a Medium finding; the AP is not enforcing the 192-bit security requirement.

### Rogue RADIUS Testing

WPA3-Enterprise is vulnerable to rogue RADIUS attacks if clients do not validate the server certificate. The test methodology is identical to WPA2-Enterprise:

```bash
# Deploy rogue AP with rogue RADIUS using hostapd-wpe
sudo apt install hostapd-wpe

# Edit /etc/hostapd-wpe/hostapd-wpe.conf for target SSID and channel
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes
```

For the complete EAP/RADIUS testing procedure, see the [enterprise wireless security assessment framework](/en/blog/enterprise-wireless-security-assessment/).

---

## Toolkit Reference for WPA3 Testing

| Tool | Purpose | Adapter | Key Command |
|---|---|---|---|
| airodump-ng | WPA3 network discovery, SAE frame capture | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | PMKID/SAE capture, transition mode detection | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | Convert captures, detect WPA2 exposure in transition mode | N/A (post-processing) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | RSN IE analysis, PMF capability, SAE frame inspection | Any (via capture file) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | PMF enforcement testing (deauth) | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | WPA2-only rogue AP for downgrade testing | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | Rogue RADIUS for WPA3-Enterprise EAP testing | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

---

## Findings Summary for WPA3 Assessments

| ID | Severity | Finding | Condition |
|---|---|---|---|
| W3-01 | Critical | WPA3 downgrade to WPA2 succeeded; handshake captured and crackable | Client associated to WPA2-only rogue AP; hash recovered |
| W3-02 | High | Transition mode without SAE enforcement; WPA2 PMKID exposed | hcxpcapngtool returns crackable hash from WPA3 network |
| W3-03 | High | PMF not enforced on WPA3 SSID; deauth attack succeeded | Test client disconnected by aireplay-ng deauth |
| W3-04 | High | WPA3-Enterprise clients accept rogue RADIUS without certificate warning | hostapd-wpe captures EAP credentials from test client |
| W3-05 | Medium | PMF Capable but not Required on WPA3 SSID | RSN IE shows MFPC=1, MFPR=0 |
| W3-06 | Medium | WPA3-Enterprise not using 192-bit security mode | RSN IE shows CCMP-128 instead of GCMP-256 |
| W3-07 | Medium | AP firmware predates Dragonblood patches | Firmware version comparison against vendor advisories |
| W3-08 | Low | OWE transition mode; legacy clients connect unencrypted | Open SSID visible alongside OWE SSID |

---

## Related Resources

- [Enterprise Wireless Security Assessment: A Complete Framework](/en/blog/enterprise-wireless-security-assessment/)
- [Packet Injection Guide: Testing Your WiFi Adapter with aireplay-ng](/en/blog/packet-injection-guide/)
- [Enable Monitor Mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
