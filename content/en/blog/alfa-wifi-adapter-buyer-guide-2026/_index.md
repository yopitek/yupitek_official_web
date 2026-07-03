---
title: "ALFA WiFi Adapter Buyer's Guide 2026: Which Model Is Right for You?"
description: "Complete ALFA Network USB WiFi adapter buyer's guide for 2026. Compare AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS across driver support, monitor mode, OS compatibility, and price."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "What are the buying criteria for ALFA adapters?"
    answer: "Criteria include chipset driver maturity, OS compatibility, monitor mode support, and transmit power. RTL8812AU has the most mature and stable driver."
  - question: "Which ALFA adapters support Monitor Mode?"
    answer: "ACH, ACM, ACS, AX, AXER, AXM, and AXML all fully support monitor mode and packet injection. EACS (RTL8821CU) does not."
  - question: "Do I need a WiFi 6E/6 adapter?"
    answer: "Only if your audit scope includes the 6 GHz band. AXML supports tri-band AX3000 and needs Linux kernel 5.18+ with firmware-misc-nonfree."
  - question: "What is the driver installation difference between RTL8812AU and MT7612U?"
    answer: "RTL8812AU requires DKMS compilation and may need rebuilding after kernel updates. MT7612U has been in the mainline kernel since 4.19 and is plug-and-play with no compilation."
  - question: "Which ALFA adapter is most recommended for 2026?"
    answer: "For red teaming, AWUS036ACH (500mW dual antenna). For budget, AWUS036ACM. For enterprise 6E, AWUS036AXML."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
featureimage: "/images/blog/alfa-wifi-adapter-buyer-guide-2026.webp"
---

This guide cuts through the noise for network security engineers, enterprise IT professionals, and red teamers who need to pick the right ALFA Network USB WiFi adapter in 2026. We cover all eight current production models — [AWUS036ACS](/en/products/alfa/awus036acs/), [AWUS036ACH](/en/products/alfa/awus036ach/), [AWUS036ACM](/en/products/alfa/awus036acm/), [AWUS036EACS](/en/products/alfa/awus036eacs/), [AWUS036AX](/en/products/alfa/awus036ax/), [AWUS036AXER](/en/products/alfa/awus036axer/), [AWUS036AXM](/en/products/alfa/awus036axm/), and [AWUS036AXML](/en/products/alfa/awus036axml/) — comparing chipsets, driver maturity, OS support, and real-world use cases so you spend less time troubleshooting drivers and more time on the actual work.

{{< tldr >}}
AWUS036ACH is the 2026 red team pick: 500 mW dual antenna AC1200 with the most mature RTL8812AU driver. For budget, choose AWUS036ACM. For enterprise 6E, choose AWUS036AXML (AX3000 tri-band).
{{< /tldr >}}





---

## How to Choose: 4 Key Questions

Before you open a product page, answer these four questions. Your answers will eliminate most of the field immediately.

### (a) What OS are you running?

Driver support is everything. Kali Linux and Ubuntu users on recent kernels have the widest selection. macOS support is thin across all models. Windows 10/11 is generally well-supported. If you are on Raspberry Pi or an ARM-based platform, chipset selection matters enormously.

- **Kali Linux / Debian:** RTL8812AU (`dkms-rtl8812au`) and MT7921AUN (kernel native ≥ 5.18) are your two primary chipset families for penetration testing.
- **Ubuntu 22.04 / 24.04:** Same driver landscape, but you may need to install HWE kernels or `firmware-misc-nonfree` for MT7921AUN.
- **Windows 10/11:** ALFA supplies signed drivers for all current models. Installation is straightforward.
- **macOS Sonoma:** Only a handful of adapters have community-maintained kext support. Expect friction; plan for a VM workflow.
- **Raspberry Pi (Kali NetHunter, ARM):** RTL8812AU models (ACH) and MT7612U models (ACM) are the safe choice. MT7921AUN can work but requires the `firmware-misc-nonfree` package and a recent enough kernel.

### (b) Do you need monitor mode and packet injection?

If your answer is yes — and for any penetration testing or wireless audit work it should be — cross the [AWUS036EACS](/en/products/alfa/awus036eacs/) off your shortlist immediately. Its RTL8821CU chipset does not support monitor mode or packet injection under Linux. Every other model in this guide does.

### (c) VM or bare metal?

USB passthrough in VirtualBox and VMware adds a layer of complexity. Any adapter on this list will work with proper passthrough configured, but RTL8812AU adapters (ACH) and MT7612U adapters (ACM) have the longest track record in VM environments. If you are passing through to a VM exclusively, avoid adapters that rely on firmware files loaded at runtime — lost USB connections mean lost firmware.

See [ALFA adapter setup in VirtualBox and VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/) for full setup instructions.

### (d) Budget?

The Wi-Fi 5 generation (ACH, ACM, ACS) is cheaper, has more stable drivers, and is the right choice if budget is a constraint or driver stability is paramount. The Wi-Fi 6/6E generation (AX, AXER, AXM, AXML) is where the hardware is heading, but you are paying more and accepting some driver edge cases on non-mainline kernels.

---

## Complete ALFA Adapter Comparison Table

<div style="overflow-x: auto;">

| Model | Wi-Fi Gen | Chip | Max Speed | Monitor Mode | Kali Driver | Windows | macOS | Antennas | Best For |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Lightweight travel kit |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅✅ Best | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Red team ops |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Linux plug & play |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ❌ | rtl88xxcu (OOK) | ✅ | ⚠️ | Integrated 2dBi | Windows home WiFi + BT |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1200 | ⚠️ Limited | OOK (<6.14) | ✅ | ❌ | Integrated | Windows WiFi 6 |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ⚠️ Limited | OOK (<6.14) | ✅ | ❌ | Integrated nano | Compact travel adapter |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E + dual antenna |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | WiFi 6E + Linux + USB-C |

</div>

**Legend:** ✅ Supported · ⚠️ Limited/partial · ❌ Not supported

{{< alert "circle-info" >}}
**macOS note:** All ALFA adapters face driver challenges on macOS Ventura and Sonoma. The most common community-maintained option is running Kali Linux in a VM with USB passthrough. AWUS036EACS (RTL8821CU) may work on macOS via third-party drivers for standard client connectivity, but monitor mode is not supported.
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

### AWUS036ACM — The Linux Plug-and-Play Pick

The [AWUS036ACM](/en/products/alfa/awus036acm/) uses the MediaTek MT7612U chipset — a different family from the ACH's RTL8812AU. Its biggest advantage is mainline Linux kernel support since kernel 4.19 as the `mt76x2u` driver, meaning zero driver compilation on any modern Kali Linux or Ubuntu system. It ships with two RP-SMA connectors for dual-antenna operation.

Functionally, monitor mode and injection support are fully capable for security work.

If you only need one antenna port and do not require the extended transmit power of the ACH, the ACM covers the same use cases for less money. It is a common choice for kit deployments where you are buying adapters in quantity for an audit team.

**When to choose ACM over ACH:** Zero-hassle Linux driver setup, plug-and-play on Ubuntu/Kali without compiling, dual-antenna coverage at a lower price point than the ACH.

### AWUS036ACS — Lightweight and Portable

The [AWUS036ACS](/en/products/alfa/awus036acs/) uses the RTL8811AU chipset — a step down from RTL8812AU in transmit power, but still fully capable of monitor mode and packet injection. Its compact form factor and single antenna make it the carry choice for travel-heavy consultants who do not want to manage multiple RP-SMA antennas through airport security.

The RTL8811AU driver shares the same `rtl8812au-dkms` package on Kali, so the installation workflow is identical.

**Trade-offs vs. ACH/ACM:** Lower transmit power (less range at distance), single antenna (no MIMO), AC600 vs. AC1200 maximum throughput. For most capture-and-inject workflows these differences are irrelevant. For long-range ops, they matter.

### AWUS036EACS — General Use, Not for Pentesting

The [AWUS036EACS](/en/products/alfa/awus036eacs/) is powered by a Realtek RTL8821CU chipset. Linux driver support for RTL8821CU is limited — monitor mode and packet injection are not supported. This adapter is designed for Windows client connectivity and includes Bluetooth 4.2, not for security testing tasks.

{{< alert "triangle-exclamation" >}}
**Do not use AWUS036EACS for penetration testing, red team operations, or any task requiring monitor mode or packet injection.** It is suitable for general wireless connectivity, DJI drone controller range extension (where it is commonly paired), and Windows-first deployments where standard client adapter behavior is acceptable.
{{< /alert >}}

It earns its place on this list for its Bluetooth 4.2 combo capability and Windows out-of-box support. On macOS, community RTL8821CU driver support is limited and monitor mode is not available.

---

## Wi-Fi 6 Adapters (Windows-Focused)

Wi-Fi 6 (802.11ax) brought meaningful improvements in dense-environment performance, target-rich MU-MIMO scenarios, and BSS Coloring for network identification. The AWUS036AX and AWUS036AXER are ALFA's Wi-Fi 6 adapters, designed primarily for Windows connectivity.

Both Wi-Fi 6 ALFA adapters use the Realtek RTL8832BU chipset. On Linux, the RTL8832BU driver is out-of-kernel (OOK) on kernels below 6.14, which means **limited monitor mode and packet injection support**. If your primary use case is penetration testing on Linux, choose the AWUS036ACH or AWUS036AXML instead.

### AWUS036AX — Wi-Fi 6 Windows Adapter

The [AWUS036AX](/en/products/alfa/awus036ax/) is ALFA's Wi-Fi 6 adapter with an integrated antenna (no external RP-SMA connector). It delivers AX1200 speeds on 2.4 and 5 GHz bands and is well-suited for Windows 10/11 connectivity.

**Driver status:**
- Windows: Full support via ALFA-supplied driver
- Linux kernel ≥ 6.14: In-kernel RTL8832BU driver
- Linux kernel < 6.14: Out-of-kernel driver required
- Monitor mode: ⚠️ Limited
- Packet injection: ⚠️ Limited

{{< alert "triangle-exclamation" >}}
**Linux penetration testing note:** The AWUS036AX uses the RTL8832BU chipset, which has limited monitor mode and packet injection support on Linux kernels below 6.14. For Kali Linux security work, use the [AWUS036ACH](/en/products/alfa/awus036ach/) (RTL8812AU) or [AWUS036AXML](/en/products/alfa/awus036axml/) (MT7921AUN) instead.
{{< /alert >}}

### AWUS036AXER — Compact Travel Wi-Fi 6 Adapter

The [AWUS036AXER](/en/products/alfa/awus036axer/) uses the same RTL8832BU chipset as the AWUS036AX but in an ultra-compact nano form factor (10.5g). The driver situation is identical — same RTL8832BU, same Linux limitations, same Windows compatibility.

Choose AXER over AX when portability is the deciding factor: business travel, minimal-footprint setups, or situations where a compact dongle is preferred over a full-size adapter.

---

## Wi-Fi 6E Adapters (Future-Proof)

Wi-Fi 6E extends 802.11ax into the 6 GHz band, providing access to the new 5.925–7.125 GHz spectrum. In practice, this means less interference, wider channel widths (up to 160 MHz), and access to a band that older equipment cannot see or reach. As enterprise networks deploy Wi-Fi 6E infrastructure, auditors need 6E-capable adapters to assess the full attack surface.

Both Wi-Fi 6E ALFA adapters require kernel ≥ 5.18 for 6 GHz support. The 6 GHz band requires regulatory domain to be set correctly — regulatory enforcement for 6 GHz is stricter than for 2.4/5 GHz in most jurisdictions.

### AWUS036AXM — Wi-Fi 6E Entry Point

The [AWUS036AXM](/en/products/alfa/awus036axm/) uses the MT7921AUN chipset with full tri-band support including 6 GHz. It ships with two RP-SMA connectors for 2T2R dual-antenna operation.

For operators who primarily work 2.4 and 5 GHz environments but want 6 GHz capability for emerging network assessments without paying flagship prices, the AXM is the logical entry point.

**Band coverage:** 2.4 GHz, 5 GHz, 6 GHz (tri-band)
**Antennas:** 2× RP-SMA — swappable for any compatible ALFA antenna

### AWUS036AXML — The Flagship 6E Adapter

The [AWUS036AXML](/en/products/alfa/awus036axml/) is ALFA's current flagship adapter. It features the MT7921AUN chipset, USB-C 3.2 connectivity, Bluetooth 5.2, and a single high-gain RP-SMA connector.

**Key specs:**
- Chipset: MT7921AUN (MediaTek)
- 1× RP-SMA connector — compatible with the full ALFA antenna lineup
- Tri-band: 2.4 GHz + 5 GHz + 6 GHz
- AX3000 class (up to 3000 Mbps theoretical across bands)
- USB-C 3.2 — faster host bus bandwidth vs. USB-A

**Driver notes for AXML:**
- MT7921AUN is supported under the `mt7921u` driver family on kernel ≥ 5.18
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
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | `mt76x2u` (in-kernel) | In-kernel ≥4.19 | ✅ native | ✅ ALFA driver |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` (OOK) | OOK | ❌ Not supported | ✅ ALFA driver |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Limited | ✅ ALFA driver |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Limited | ✅ ALFA driver |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | In-kernel ≥5.18 | ✅ firmware req. | ✅ ALFA driver |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | In-kernel ≥5.18 | ✅ firmware req. | ✅ ALFA driver |

</div>

**RTL8812AU kernel history:** The RTL8812AU driver was partially integrated into the mainline kernel in Linux 5.2, but with significant limitations — no monitor mode, no injection. Full penetration testing capability requires the out-of-tree `rtl8812au` driver, packaged as `dkms-rtl8812au` on Kali. The DKMS package rebuilds automatically when the kernel is updated, making it essentially maintenance-free on Kali Linux systems.

**MT7921AUN kernel history:** Native integration arrived in Linux 5.18 via the `mt7921u` USB driver. The firmware file `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (and related firmware blobs) must be present in `/lib/firmware/mediatek/`. On Kali these are pulled in by `firmware-misc-nonfree`. On Ubuntu 22.04 LTS with the default kernel, you may need to install the HWE stack (`linux-generic-hwe-22.04`) to reach ≥ 5.18.

**Raspberry Pi specifics:** The RTL8812AU driver compiles cleanly on Raspberry Pi OS (32-bit and 64-bit) using `dkms-rtl8812au`. It is the safest choice for NetHunter deployments. MT7921AUN adapters (AXM, AXML) can work on Pi 4/5 but require `firmware-misc-nonfree` and a recent enough Raspberry Pi OS kernel (2023+ images should be fine).

---

## Best ALFA Adapter By Use Case

### Red Team Operations

**Recommended: [AWUS036ACH](/en/products/alfa/awus036ach/)**

The ACH's 500 mW transmit power, dual antennas, and battle-tested RTL8812AU driver make it the default for red team engagements. You can rely on it to work after a kernel update, to pass through a VM reliably, and to accept any RP-SMA antenna you bring. If budget allows and 6E coverage is in scope, add an [AWUS036AXML](/en/products/alfa/awus036axml/) as a secondary adapter for 6 GHz network discovery.

### CTF Competitions

**Recommended: [AWUS036ACM](/en/products/alfa/awus036acm/)**

CTF wireless challenges typically involve controlled environments where transmit power is not the critical variable. The ACM provides full monitor mode and injection capability with zero-hassle Linux driver setup (MT7612U in-kernel since 4.19). Its compact dual-antenna form factor is easy to pack and deploy. If the CTF involves Wi-Fi 6 challenges (still rare but growing), reach for the [AWUS036AXML](/en/products/alfa/awus036axml/) instead.

### Raspberry Pi / Kali NetHunter

**Recommended: [AWUS036ACH](/en/products/alfa/awus036ach/) or [AWUS036ACM](/en/products/alfa/awus036acm/)**

The RTL8812AU (ACH) and MT7612U (ACM) adapters have a proven track record on Raspberry Pi hardware. Avoid MT7921AUN models (AXM, AXML) for Pi deployments unless you have confirmed kernel and firmware compatibility on your specific image. The ACH is the safer choice if you are building a dedicated NetHunter Pi that needs to be reliable in the field.

### Enterprise Wireless Audit

**Recommended: [AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)**

A modern enterprise wireless audit should cover 2.4, 5, and 6 GHz bands. The AXML covers the full tri-band spectrum including 6E, while the ACH provides a stable, high-power fallback for 5 GHz work. Running both simultaneously with separate capture interfaces gives you complete band coverage without driver compromises. Use the ACH for active injection tasks and AXML for passive 6 GHz monitoring.

### DJI Drone Range Extension

**Recommended: [AWUS036EACS](/en/products/alfa/awus036eacs/)**

DJI range extension via Litchi or DJI GO is a common legitimate use case. The EACS with RTL8821CU is recommended here because it works natively on Windows (where DJI software runs) without additional drivers, and its general-purpose connectivity profile suits this use case. No monitor mode required; client-mode connectivity and transmit power are what matter. Pair with an [APA-M25](/en/products/alfa/apa-m25/) panel antenna for maximum effective range.

---

## OS-Specific Recommendations

### Kali Linux

Kali Linux is the primary supported platform for all ALFA adapters used in security work. The Kali repository includes `dkms-rtl8812au` for RTL8812AU/RTL8811AU adapters and `firmware-misc-nonfree` for MT7921AUN adapters. Keep your Kali install updated — the DKMS package tracks kernel changes automatically.

**Quick setup (RTL8812AU family):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Quick setup (MT7921AUN family — AXM, AXML):**
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

Ubuntu 24.04 ships with kernel 6.8. MT7921AUN adapters (AXM, AXML) will work out of the box once `firmware-misc-nonfree` is installed:
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

All ALFA adapters ship with Windows 10/11 compatible drivers. Download the driver package from the ALFA Network website or install via Windows Update for MT7921AUN (Microsoft provides a WHQL-signed inbox driver). RTL8812AU adapters require the ALFA-supplied Realtek driver package; Windows Update drivers for RTL8812AU are inconsistently available.

For use with tools like Acrylic Wi-Fi, inSSIDer, or the Windows version of Wireshark, the ALFA drivers provide a functional monitor mode wrapper on Windows via NDIS monitor mode — though this is substantially less capable than Linux monitor mode for active injection work.

### macOS Sonoma

There is no officially supported ALFA adapter for macOS Sonoma in 2026. Community kext projects exist for RTL8812AU but are unsigned and require disabling System Integrity Protection (SIP). The practical recommendation is to run Kali Linux in a VM (Parallels, VMware Fusion, or UTM) with USB passthrough to the ALFA adapter.

The AWUS036EACS with RTL8821CU may have limited macOS driver support via community projects, but monitor mode is not available on any platform.

### Raspberry Pi / Kali NetHunter

On Raspberry Pi 4 and Pi 5 running Kali NetHunter:

```bash
# For RTL8812AU adapters (ACH, ACS):
sudo apt update && sudo apt install -y dkms-rtl8812au

# For MT7921AUN adapters (AXM, AXML — Pi 5 with recent kernel recommended):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
If you are building a dedicated NetHunter dropbox, use the [AWUS036ACH](/en/products/alfa/awus036ach/) or [AWUS036ACM](/en/products/alfa/awus036acm/). The RTL8812AU (ACH) and MT7612U (ACM) drivers compile reliably on ARM and have no firmware file dependency. MT7921AUN models (AXM, AXML) are functional on Pi but add a dependency on firmware files that can cause headaches in offline deployments.
{{< /alert >}}

---

{{< faq >}}

## Final Recommendation

After evaluating all eight adapters across driver maturity, hardware capability, and real-world use cases, these are the three choices that cover most professionals:

**Budget Pick: [AWUS036ACM](/en/products/alfa/awus036acm/)**
The MT7612U adapter with dual RP-SMA connectors delivers full monitor mode and packet injection support with zero-configuration Linux driver setup (in-kernel since 4.19). Ideal for consultants who want a reliable, hassle-free tool, or teams buying adapters in quantity.

**Versatile Pick: [AWUS036ACH](/en/products/alfa/awus036ach/)**
The dual-antenna, 500 mW RTL8812AU adapter is the most widely recommended single adapter for security professionals. Covers 2.4 and 5 GHz, accepts external antennas, has the most mature driver stack of any adapter on this list, and costs only modestly more than the ACM. If you are buying one adapter and you are not yet sure what you need, buy this one.

**Enterprise / Future-Proof Pick: [AWUS036AXML](/en/products/alfa/awus036axml/)**
If your audit scope includes Wi-Fi 6E infrastructure — which it should for any engagement starting in 2026 — the AXML is the only adapter that gives you USB-C 3.2, 6 GHz capability, and Bluetooth 5.2 in one package. Pair it with an ACH for a two-adapter kit that covers every band from 2.4 GHz to 6 GHz with no compromises. For dual-antenna 6E coverage, consider the AWUS036AXM instead.

For detailed setup and configuration instructions, see:
- [Install ALFA driver on Kali Linux and Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- [Fix ALFA driver after kernel update](/en/blog/fix-alfa-driver-kernel-update/)
- [Enable monitor mode on Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
- [AWUS036AXML Wi-Fi 6E review and driver testing](/en/blog/awus036axml-wifi-6e-review/)

## References

1. [aircrack-ng rtl8812au Driver](https://github.com/aircrack-ng/rtl8812au)
2. [Wi-Fi Alliance Official Website](https://www.wi-fi.org/)
3. [ALFA Network Official Website](https://www.alfa.com.tw)
4. [Linux Kernel mt76 Driver](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
