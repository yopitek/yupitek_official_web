---
title: "NVIDIA Mellanox LinkX Optical Transceivers"
description: "Select original NVIDIA Mellanox LinkX optical transceiver modules. High-speed 25G, 100G, 400G, and 800G transceivers for multimode and singlemode networks."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX Optical Transceivers — 25G to 800G

NVIDIA LinkX® optical transceivers are designed to meet the strict requirements of high-performance computing, enterprise storage, and hyperscale environments. Using original transceivers ensures optimal signal integrity, lowest bit error rates (BER), and full compatibility with ConnectX adapters and Quantum switches.

---

## Optical Transceiver Catalog

Below is the list of active optical transceiver models available in our inventory.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR Optical Transceiver</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 Optical Transceiver</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR Optical Transceiver</p>
  </div>
</div>

| Part Number | Speed | Interface | Connector | Wavelength | Fiber Type | Max Distance | Description |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850nm | Multimode (MMF) | 150m (OM4) / 100m (OM3) | 25GbE SR Module |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | Multimode (MMF) | 100m (OM4) / 70m (OM3) | 100GbE SR4 Module, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850nm | Multimode (MMF) | 50m (OM4) | NDR IB/ETH SR Module, Flat Top |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850nm | Multimode (MMF) | 50m (OM4) | 2xNDR Twin-Port SR Module, Finned |

---

## Distance & Cabling Reference Guide

### 1. SR vs SR4 vs NDR (Multimode Solutions)
- **25G SR (SFP28)**: Utilizes a standard LC-LC duplex multimode patch cable. Uses a single lane for transmission and reception.
- **100G SR4 (QSFP28)**: Uses a 12-fiber MPO (MPO-12) ribbon patch cable (typically Type-B polarity) to transmit across 4 parallel lanes of 25G.
- **400G/800G NDR (OSFP)**: Employs PAM4 modulation to transmit ultra-high bandwidth over MPO-12 APC (angled physical contact) connectors. The angled end-face minimizes back reflections, which is critical at higher speeds.

### 2. Singlemode (LR4/FR4) vs Multimode (SR/SR4)
- **Multimode (MMF)**: Suited for intra-rack or short-distance inter-rack cabling (up to 100–150m). Lower transceiver cost.
- **Singlemode (SMF)**: Required for distances beyond 150m (up to 10km for LR4). Uses duplex LC connectors on 9/125µm fiber.

---

## Technical Advisory: OEM vs Third-Party Modules

When purchasing transceivers, customers often ask: *"Can I use generic or programmed third-party transceivers?"*

### Why We Recommend Original NVIDIA LinkX:
1. **Firmware Compatibility**: NVIDIA ConnectX NICs and Quantum switches run specialized operating systems (like MLNX-OS or Onyx). System updates can frequently lock out or flag generic coded modules, causing port status down.
2. **Diagnostic Reliability (DDM/DOM)**: Original modules report exact temperature, voltage, TX power, and RX power values directly to system controllers (iDRAC, HPE iLO, or MLNX-OS). Correct measurements prevent false-positive thermal alerts.
3. **Advanced Features Support**: LinkX modules are certified to support critical features like Forward Error Correction (FEC) settings out of the box, preventing packet drops in high-throughput database workloads.

---

{{< alert >}}
Need a product quotation? Please [contact us](/en/contact/)
{{< /alert >}}
