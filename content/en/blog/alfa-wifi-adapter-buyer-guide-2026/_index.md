---
title: "ALFA WiFi Adapter Buyer's Guide 2026: Which Model Is Right for You?"
description: "Complete ALFA Network USB WiFi adapter buyer's guide for 2026. Compare AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS across driver support, monitor mode, OS compatibility, and price."
date: 2026-04-15
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

This guide cuts through the noise for network security engineers, enterprise IT professionals, and red teamers who need to pick the right ALFA Network USB WiFi adapter in 2026. We cover all eight current production models — [AWUS036ACS](/en/products/alfa/awus036acs/), [AWUS036ACH](/en/products/alfa/awus036ach/), [AWUS036ACM](/en/products/alfa/awus036acm/), [AWUS036EACS](/en/products/alfa/awus036eacs/), [AWUS036AX](/en/products/alfa/awus036ax/), [AWUS036AXER](/en/products/alfa/awus036axer/), [AWUS036AXM](/en/products/alfa/awus036axm/), and [AWUS036AXML](/en/products/alfa/awus036axml/) — comparing chipsets, driver maturity, OS support, and real-world use cases so you spend less time troubleshooting drivers and more time on the actual work.

---

## How to Choose: 4 Key Questions

Before you open a product page, answer these four questions. Your answers will eliminate most of the field immediately.

### (a) What OS are you running?

Driver support is everything. Kali Linux and Ubuntu users on recent kernels have the widest selection. macOS support is thin across all models. Windows 10/11 is generally well-supported. If you are on Raspberry Pi or an ARM-based platform, chipset selection matters enormously.

- **Kali Linux / Debian:** RTL8812AU (`dkms-rtl8812au`) and MT7921AU (kernel native ≥ 5.18) are your two primary chipset families.
- **Ubuntu 22.04 / 24.04:** Same driver landscape, but you may need to install HWE kernels or `firmware-misc-nonfree` for MT7921AU.
- **Windows 10/11:** ALFA supplies signed drivers for all current models. Installation is straightforward.
- **macOS Sonoma:** Only a handful of adapters have community-maintained kext support. Expect friction; plan for a VM workflow.
- **Raspberry Pi (Kali NetHunter, ARM):** RTL8812AU models are the safe choice. MT7921AU can work but requires the `firmware-misc-nonfree` package and a recent enough kernel.

### (b) Do you need monitor mode and packet injection?

If your answer is yes — and for any penetration testing or wireless audit work it should be — cross the [AWUS036EACS](/en/products/alfa/awus036eacs/) off your shortlist immediately. Its QCA9377 chipset does not reliably support monitor mode or injection under Linux. Every other model in this guide does.

### (c) VM or bare metal?

USB passthrough in VirtualBox and VMware adds a layer of complexity. Any adapter on this list will work with proper passthrough configured, but RTL8812AU adapters (ACH, ACM) have the longest track record in VM environments. If you are passing through to a VM exclusively, avoid adapters that rely on firmware files loaded at runtime — lost USB connections mean lost firmware.

See [ALFA adapter setup in VirtualBox and VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/) for full setup instructions.

### (d) Budget?

The Wi-Fi 5 generation (ACH, ACM, ACS) is cheaper, has more stable drivers, and is the right choice if budget is a constraint or driver stability is paramount. The Wi-Fi 6/6E generation (AX, AXER, AXM, AXML) is where the hardware is heading, but you are paying more and accepting some driver edge cases on non-mainline kernels.

---

## Complete ALFA Adapter Comparison Table

<div style="overflow-x: auto;">

| Model | Wi-Fi Gen | Chip | Max Speed | Monitor Mode | Kali Driver | Windows | macOS | Antennas | Best For |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Lightweight travel kit |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Red team ops |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Budget dual-band |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | QCA9377 | AC1200 | ⚠️ | ath10k | ✅ | ✅ | 1× RP-SMA | General use (no injection) |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | MT7921AU | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6 audit |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | MT7921AU | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Extended range Wi-Fi 6 |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AU | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | Wi-Fi 6E entry |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7902 | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Flagship 6E |

</div>

**Legend:** ✅ Supported · ⚠️ Limited/partial · ❌ Not supported

{{< alert "circle-info" >}}
**macOS note:** All ALFA adapters face driver challenges on macOS Ventura and Sonoma. The most common community-maintained option is running Kali Linux in a VM with USB passthrough. AWUS036EACS is the exception — it may work via the native macOS Qualcomm driver but without monitor mode.
{{< /alert >}}

---

## Wi-Fi 5 Adapters (Best Driver Maturity)

The Wi-Fi 5 generation has had years of community development behind it. If your priority is rock-solid driver stability — especially for CTF work, professional audits, or environments where you cannot afford a broken driver after a kernel update — start here.

### AWUS036ACH — The Red Team Standard

The [AWUS036ACH](/en/products/alfa/awus036ach/) remains the most widely deployed ALFA adapter in the security community for good reason. Its RTL8812AU chipset is supported by the `aircrack-ng/rtl8812au` driver, which has been maintained and tested against every major Kali Linux release for years.

**Hardware specs:**
- Chipset: RTL8812AU (Realtek)
- Two detachable RP-SMA antenna connectors — compatible with the full ALFA antenna lineup
- 500 mW transmit power — the highest in the Wi-Fi 5 lineup
- Dual-band: 2.4 GHz and 5 GHz

**Why it leads for red teams:** 500 mW transmit power combined with dual external antennas and mature injection support means you can work at distance while maintaining reliable frame delivery. Swap the stock omni antennas for an [APA-M25](/en/products/alfa/apa-m25/) directional panel and you have a serious long-range platform. The two-antenna form factor also enables proper 2T2R MIMO when associated with target networks.

**Driver installation on Kali:**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
On kernels ≥ 6.2, the stock `rtl8812au` module included in older Kali images may fail to load. Always install `dkms-rtl8812au` from the Kali repository — it tracks kernel changes and rebuilds automatically on kernel updates via DKMS.
{{< /alert >}}

### AWUS036ACM — The Budget Dual-Band Pick

The [AWUS036ACM](/en/products/alfa/awus036acm/) shares the RTL8812AU chipset with the ACH but ships with a single RP-SMA connector and a lower price point. Functionally, monitor mode and injection support are identical.

If you only need one antenna port and do not require the extended transmit power of the ACH, the ACM covers the same use cases for less money. It is a common choice for kit deployments where you are buying adapters in quantity for an audit team.

**When to choose ACM over ACH:** Budget constraints, single-operator use, situations where antenna diversity is not a priority.

### AWUS036ACS — Lightweight and Portable

The [AWUS036ACS](/en/products/alfa/awus036acs/) uses the RTL8811AU chipset — a step down from RTL8812AU in transmit power, but still fully capable of monitor mode and packet injection. Its compact form factor and single antenna make it the carry choice for travel-heavy consultants who do not want to manage multiple RP-SMA antennas through airport security.

The RTL8811AU driver shares the same `rtl8812au-dkms` package on Kali, so the installation workflow is identical.

**Trade-offs vs. ACH/ACM:** Lower transmit power (less range at distance), single antenna (no MIMO), AC600 vs. AC1200 maximum throughput. For most capture-and-inject workflows these differences are irrelevant. For long-range ops, they matter.

### AWUS036EACS — General Use, Not for Pentesting

The [AWUS036EACS](/en/products/alfa/awus036eacs/) is powered by a Qualcomm QCA9377 chipset and uses the `ath10k` kernel driver. This chipset was designed for client connectivity, not packet manipulation. Monitor mode support under `ath10k` is unreliable, and packet injection is not supported in the standard driver configuration.

{{< alert "triangle-exclamation" >}}
**Do not use AWUS036EACS for penetration testing, red team operations, or any task requiring monitor mode or packet injection.** It is suitable for general wireless connectivity, DJI drone controller range extension (where it is commonly paired), and Windows-first deployments where standard client adapter behavior is acceptable.
{{< /alert >}}

It earns its place on this list for macOS compatibility — the QCA9377 driver situation on macOS is better than for Realtek or MediaTek chipsets — and for consumer/enterprise connectivity deployments where the adapter is used purely as a client.

---

## Wi-Fi 6 Adapters (Current Sweet Spot)

Wi-Fi 6 (802.11ax) brought meaningful improvements in dense-environment performance, target-rich MU-MIMO scenarios, and BSS Coloring for network identification. For wireless auditors, Wi-Fi 6 adapters are increasingly relevant as enterprise deployments have shifted aggressively to 802.11ax infrastructure.

Both Wi-Fi 6 ALFA adapters use the MediaTek MT7921AU chipset, which was integrated into the mainline Linux kernel in version 5.18 as the `mt7921u` driver.

### AWUS036AX — The Clean Wi-Fi 6 Choice

The [AWUS036AX](/en/products/alfa/awus036ax/) is the direct Wi-Fi 6 successor to the ACH configuration: dual external RP-SMA antennas, 2T2R operation, and AX1800 (up to 1800 Mbps theoretical) on 2.4 and 5 GHz bands.

**Driver status:**
- Kernel ≥ 5.18: driver loads automatically, no additional packages needed on updated Kali/Ubuntu systems
- Older kernels: `firmware-misc-nonfree` required; consider upgrading kernel first
- Monitor mode: supported
- Packet injection: supported

**Practical note on monitor mode:** The MT7921AU's monitor mode implementation has shown occasional firmware crashes on specific kernel/firmware combinations when performing aggressive channel hopping. This affects the entire MT7921AU family. Pin your kernel if stability is critical, and test before a live engagement.

{{< alert "circle-info" >}}
**Kernel check:** Run `uname -r` to confirm your kernel version before purchasing. On Kali 2024.x, the default kernel is ≥ 6.x, so MT7921AU will work out of the box. On Ubuntu 22.04 LTS with HWE stack, you should be on 6.5+.
{{< /alert >}}

### AWUS036AXER — Extended Range Variant

The [AWUS036AXER](/en/products/alfa/awus036axer/) is hardware-identical to the AWUS036AX in chipset and antenna configuration but adds enhanced RF amplification for extended operating range. The driver situation is identical — same MT7921AU, same kernel support path, same monitor mode and injection behavior.

Choose AXER over AX when operating range is the deciding factor: site surveys of large campuses, outdoor assessments, or scenarios where the AP is at distance. The price premium is moderate and justifiable if range matters to your deployment.

---

## Wi-Fi 6E Adapters (Future-Proof)

Wi-Fi 6E extends 802.11ax into the 6 GHz band, providing access to the new 5.925–7.125 GHz spectrum. In practice, this means less interference, wider channel widths (up to 160 MHz), and access to a band that older equipment cannot see or reach. As enterprise networks deploy Wi-Fi 6E infrastructure, auditors need 6E-capable adapters to assess the full attack surface.

Both Wi-Fi 6E ALFA adapters require kernel ≥ 5.18 for 6 GHz support. The 6 GHz band requires regulatory domain to be set correctly — regulatory enforcement for 6 GHz is stricter than for 2.4/5 GHz in most jurisdictions.

### AWUS036AXM — Wi-Fi 6E Entry Point

The [AWUS036AXM](/en/products/alfa/awus036axm/) uses the MT7921AU chipset with 6 GHz band support enabled. It ships with a single RP-SMA connector, making it more compact than the AXML.

For operators who primarily work 2.4 and 5 GHz environments but want 6 GHz capability for emerging network assessments without paying flagship prices, the AXM is the logical entry point.

**Band coverage:** 2.4 GHz, 5 GHz, 6 GHz (tri-band)
**Antenna:** 1× RP-SMA — swappable for any compatible ALFA antenna

### AWUS036AXML — The Flagship 6E Adapter

The [AWUS036AXML](/en/products/alfa/awus036axml/) is ALFA's current top-of-line adapter. It features the MT7902 chipset (an upgrade over MT7921AU), dual RP-SMA connectors for 2T2R operation, and the highest transmit power rating in the 6E lineup.

**Key specs:**
- Chipset: MT7902 (MediaTek)
- 2× RP-SMA connectors — full 2T2R configuration
- Tri-band: 2.4 GHz + 5 GHz + 6 GHz
- AX3000 class (up to 3000 Mbps theoretical across bands)
- Highest power output in the ALFA 6E lineup

**Driver notes for AXML:**
- MT7902 is supported under the same `mt7921u` driver family on kernel ≥ 5.18
- Monitor mode is supported; active monitor with firmware has shown firmware restart issues on some kernels — see the [AWUS036AXML detailed review](/en/blog/awus036axml-wifi-6e-review/) for full testing data
- The 6 GHz band in monitor mode requires your regulatory domain to permit passive scanning on 6 GHz channels

{{< alert "triangle-exclamation" >}}
**AWUS036AXML firmware note:** On kernels below 6.1, some users experience firmware crashes when switching the AXML between monitor mode and managed mode repeatedly. If your workflow requires frequent mode switching, run kernel ≥ 6.1 and install the latest `firmware-misc-nonfree` package.
{{< /alert >}}

---

## Driver Compatibility Deep Dive

<div style="overflow-x: auto;">

| Model | Chip | Kali Package | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | Manual build | ✅ rtl8812au-dkms | ✅ ALFA driver |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | Manual build | ✅ rtl8812au-dkms | ✅ ALFA driver |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | RTL8812AU | `dkms-rtl8812au` | Manual build | ✅ rtl8812au-dkms | ✅ ALFA driver |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | QCA9377 | `ath10k-firmware` | Kernel built-in | ⚠️ Limited | ✅ Built-in |
| [AWUS036AX](/en/products/alfa/awus036ax/) | MT7921AU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ ALFA driver |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | MT7921AU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ ALFA driver |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ ALFA driver |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7902 | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ ALFA driver |

</div>

**RTL8812AU kernel history:** The RTL8812AU driver was partially integrated into the mainline kernel in Linux 5.2, but with significant limitations — no monitor mode, no injection. Full penetration testing capability requires the out-of-tree `rtl8812au` driver, packaged as `dkms-rtl8812au` on Kali. The DKMS package rebuilds automatically when the kernel is updated, making it essentially maintenance-free on Kali Linux systems.

**MT7921AU kernel history:** Native integration arrived in Linux 5.18 via the `mt7921u` USB driver. The firmware file `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (and related firmware blobs) must be present in `/lib/firmware/mediatek/`. On Kali these are pulled in by `firmware-misc-nonfree`. On Ubuntu 22.04 LTS with the default kernel, you may need to install the HWE stack (`linux-generic-hwe-22.04`) to reach ≥ 5.18.

**Raspberry Pi specifics:** The RTL8812AU driver compiles cleanly on Raspberry Pi OS (32-bit and 64-bit) using `dkms-rtl8812au`. It is the safest choice for NetHunter deployments. MT7921AU adapters can work on Pi 4/5 but require `firmware-misc-nonfree` and a recent enough Raspberry Pi OS kernel (2023+ images should be fine).

---

## Best ALFA Adapter By Use Case

### Red Team Operations

**Recommended: [AWUS036ACH](/en/products/alfa/awus036ach/)**

The ACH's 500 mW transmit power, dual antennas, and battle-tested RTL8812AU driver make it the default for red team engagements. You can rely on it to work after a kernel update, to pass through a VM reliably, and to accept any RP-SMA antenna you bring. If budget allows and 6E coverage is in scope, add an [AWUS036AXML](/en/products/alfa/awus036axml/) as a secondary adapter for 6 GHz network discovery.

### CTF Competitions

**Recommended: [AWUS036ACM](/en/products/alfa/awus036acm/)**

CTF wireless challenges typically involve controlled environments where transmit power is not the critical variable. The ACM provides full monitor mode and injection capability at a lower price point. Its compact single-antenna form factor is easy to pack and deploy. If the CTF involves Wi-Fi 6 challenges (still rare but growing), reach for the [AWUS036AX](/en/products/alfa/awus036ax/) instead.

### Raspberry Pi / Kali NetHunter

**Recommended: [AWUS036ACH](/en/products/alfa/awus036ach/) or [AWUS036ACM](/en/products/alfa/awus036acm/)**

Both RTL8812AU adapters have a proven track record on Raspberry Pi hardware. Avoid MT7921AU models for Pi deployments unless you have confirmed kernel and firmware compatibility on your specific image. The ACH is the safer choice if you are building a dedicated NetHunter Pi that needs to be reliable in the field.

### Enterprise Wireless Audit

**Recommended: [AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)**

A modern enterprise wireless audit should cover 2.4, 5, and 6 GHz bands. The AXML covers the full tri-band spectrum including 6E, while the ACH provides a stable, high-power fallback for 5 GHz work. Running both simultaneously with separate capture interfaces gives you complete band coverage without driver compromises. Use the ACH for active injection tasks and AXML for passive 6 GHz monitoring.

### DJI Drone Range Extension

**Recommended: [AWUS036EACS](/en/products/alfa/awus036eacs/)**

DJI range extension via Litchi or DJI GO is a common legitimate use case. The EACS with QCA9377 is specifically recommended here because it works natively on Windows (where DJI software runs) without additional drivers, and its general-purpose connectivity profile suits this use case. No monitor mode required; client-mode connectivity and transmit power are what matter. Pair with an [APA-M25](/en/products/alfa/apa-m25/) panel antenna for maximum effective range.

---

## OS-Specific Recommendations

### Kali Linux

Kali Linux is the primary supported platform for all ALFA adapters used in security work. The Kali repository includes `dkms-rtl8812au` for RTL8812AU/RTL8811AU adapters and `firmware-misc-nonfree` for MT7921AU/MT7902 adapters. Keep your Kali install updated — the DKMS package tracks kernel changes automatically.

**Quick setup (RTL8812AU family):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Quick setup (MT7921AU family):**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Reboot or reload the module:
sudo modprobe mt7921u
```

**Enable monitor mode:**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04 ships with kernel 6.8. MT7921AU adapters will work out of the box once `firmware-misc-nonfree` is installed:
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

RTL8812AU support on Ubuntu requires building the DKMS module:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

All ALFA adapters ship with Windows 10/11 compatible drivers. Download the driver package from the ALFA Network website or install via Windows Update for MT7921AU (Microsoft provides a WHQL-signed inbox driver). RTL8812AU adapters require the ALFA-supplied Realtek driver package; Windows Update drivers for RTL8812AU are inconsistently available.

For use with tools like Acrylic Wi-Fi, inSSIDer, or the Windows version of Wireshark, the ALFA drivers provide a functional monitor mode wrapper on Windows via NDIS monitor mode — though this is substantially less capable than Linux monitor mode for active injection work.

### macOS Sonoma

There is no officially supported ALFA adapter for macOS Sonoma in 2026. Community kext projects exist for RTL8812AU but are unsigned and require disabling System Integrity Protection (SIP). The practical recommendation is to run Kali Linux in a VM (Parallels, VMware Fusion, or UTM) with USB passthrough to the ALFA adapter.

The AWUS036EACS with QCA9377 has the most functional macOS support through the native Qualcomm/Atheros kext, but only for standard client connectivity — not monitor mode.

### Raspberry Pi / Kali NetHunter

On Raspberry Pi 4 and Pi 5 running Kali NetHunter:

```bash
# For RTL8812AU adapters:
sudo apt update && sudo apt install -y dkms-rtl8812au

# For MT7921AU adapters (Pi 5 with recent kernel recommended):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
If you are building a dedicated NetHunter dropbox, use the [AWUS036ACH](/en/products/alfa/awus036ach/) or [AWUS036ACM](/en/products/alfa/awus036acm/). Their RTL8812AU driver compiles reliably on ARM and has no firmware file dependency. MT7921AU models are functional on Pi but add a dependency on firmware files that can cause headaches in offline deployments.
{{< /alert >}}

---

## Final Recommendation

After evaluating all eight adapters across driver maturity, hardware capability, and real-world use cases, these are the three choices that cover most professionals:

**Budget Pick: [AWUS036ACM](/en/products/alfa/awus036acm/)**
The single-antenna RTL8812AU adapter delivers full monitor mode and packet injection support at the lowest price in the dual-band lineup. Ideal for consultants who want a reliable tool without overspending, or teams buying adapters in quantity.

**Versatile Pick: [AWUS036ACH](/en/products/alfa/awus036ach/)**
The dual-antenna, 500 mW RTL8812AU adapter is the most widely recommended single adapter for security professionals. Covers 2.4 and 5 GHz, accepts external antennas, has the most mature driver stack of any adapter on this list, and costs only modestly more than the ACM. If you are buying one adapter and you are not yet sure what you need, buy this one.

**Enterprise / Future-Proof Pick: [AWUS036AXML](/en/products/alfa/awus036axml/)**
If your audit scope includes Wi-Fi 6E infrastructure — which it should for any engagement starting in 2026 — the AXML is the only adapter that gives you dual-antenna 6 GHz capability. Pair it with an ACH for a two-adapter kit that covers every band from 2.4 GHz to 6 GHz with no compromises.

For detailed setup and configuration instructions, see:
- [Install ALFA driver on Kali Linux and Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- [Fix ALFA driver after kernel update](/en/blog/fix-alfa-driver-kernel-update/)
- [Enable monitor mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E review and driver testing](/en/blog/awus036axml-wifi-6e-review/)
