---
title: "NVIDIA Mellanox LinkX Direct Attach Copper (DAC) Cables"
description: "High-performance Mellanox passive copper DAC cables. 25G SFP28, 40G QSFP, 100G QSFP28, and 200G QSFP56 direct attach copper cables (straight and breakout)."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX DAC Copper Cables — 25G to 200G

NVIDIA LinkX® Direct Attach Copper (DAC) cables are copper-based interconnects that offer the lowest cost and lowest latency path for high-speed network connections up to 5 meters. Suited for top-of-rack (ToR) switch-to-server cabling in enterprise datacenters and storage clusters.

---

## DAC Product Catalog

Below is the list of original Mellanox DAC passive copper cables in our inventory, categorized by speed and structure.

:::carousel
![25G SFP28 DAC](/images/products/mellanox/ai-generated/dac-sfp28-25g.jpg)
*NVIDIA Mellanox 25G SFP28 Passive DAC Cable*
<!-- slide -->
![100G QSFP28 DAC](/images/products/mellanox/ai-generated/dac-qsfp28-100g.jpg)
*NVIDIA Mellanox 100G QSFP28 Passive DAC Cable*
<!-- slide -->
![200G QSFP56 DAC](/images/products/mellanox/ai-generated/dac-qsfp56-200g.jpg)
*NVIDIA 200G QSFP56 Passive DAC Cable*
<!-- slide -->
![100G QSFP28 to 4xSFP28 Breakout](/images/products/mellanox/ai-generated/dac-qsfp28-100g-4x25g.jpg)
*NVIDIA Mellanox 100G QSFP28 to 4x SFP28 Breakout DAC Cable*
:::

### 1. 25G, 40G & 56G DAC Cables

| Part Number | Speed | Connector | Length | Wire Gauge | Description |
|-------------|-------|-----------|--------|------------|-------------|
| **MCP2M00-A002** | 25G | SFP28 to SFP28 | 2.0m | 30AWG | 25GbE Passive Copper, Black |
| **MCP2M00-A003E30L**| 25G | SFP28 to SFP28 | 3.0m | 30AWG | 25GbE Passive Copper, CA-L |
| **MCP1700-B002** | 40G | QSFP to QSFP | 2.0m | 30AWG | 40GbE Passive Copper, Black |
| **MCP1700-B003** | 40G | QSFP to QSFP | 3.0m | 30AWG | 40GbE Passive Copper, Pulltab|
| **MC2207128-003** | 56G | QSFP to QSFP | 3.0m | 30AWG | 56G IB Passive Copper Cable |

### 2. 100G & 200G Straight DAC Cables

| Part Number | Speed | Protocol | Connector | Length | Wire Gauge | Target Environment |
|-------------|-------|----------|-----------|--------|------------|--------------------|
| **MCP1600-E002E30** | 100G | InfiniBand | QSFP28 to QSFP28 | 2.0m | 30AWG | EDR InfiniBand |
| **MCP1600-E003E26** | 100G | InfiniBand | QSFP28 to QSFP28 | 3.0m | 26AWG | EDR InfiniBand |
| **MCP1600-C01A** | 100G | Mixed/VPI | QSFP28 to QSFP28 | 1.5m | 30AWG | EDR IB & 100GbE |
| **MCP1600-C002** | 100G | Mixed/VPI | QSFP28 to QSFP28 | 2.0m | 30AWG | EDR IB & 100GbE |
| **MCP1600-C02A** | 100G | Mixed/VPI | QSFP28 to QSFP28 | 2.5m | 30AWG | EDR IB & 100GbE |
| **MCP1600-C003E30L**| 100G | Ethernet | QSFP28 to QSFP28 | 3.0m | 30AWG | 100GbE Network |
| **MCP1600-C005E26** | 100G | Ethernet | QSFP28 to QSFP28 | 5.0m | 26AWG | 100GbE Network |
| **MCP1650-H001E30** | 200G | Mixed/VPI | QSFP56 to QSFP56 | 1.0m | 30AWG | HDR IB & 200GbE |
| **MCP1650-H002E26** | 200G | Mixed/VPI | QSFP56 to QSFP56 | 2.0m | 26AWG | HDR IB & 200GbE |

### 3. Breakout DAC Cables (Splitter Cables)

| Part Number | Base Speed | Split Configuration | Connector Type | Length | Target Environment |
|-------------|------------|---------------------|----------------|--------|--------------------|
| **MCP7H00-G002R** | 100G | 1x 100G → 2x 50G | QSFP28 to 2x QSFP28 | 2.0m | Ethernet, Colored, 30AWG |
| **MCP7H00-G02B2R** | 100G | 1x 100G → 2x 50G | QSFP28 to 2x QSFP28 | 2.25m | Ethernet, Colored, 26AWG |
| **MCP7F00-A02AR** | 100G | 1x 100G → 4x 25G | QSFP28 to 4x SFP28 | 2.5m | Ethernet split to 25G |
| **MCP7F00-A003R** | 100G | 1x 100G → 4x 25G | QSFP28 to 4x SFP28 | 3.0m | Ethernet split to 25G |
| **MCP7H50-H01AR30** | 200G | 1x 200G → 2x 100G | QSFP56 to 2x QSFP56 | 1.5m | 200GbE to 2x100G, 30AWG |
| **MCP7H50-H002R26** | 200G | 1x 200G → 2x 100G | QSFP56 to 2x QSFP56 | 2.0m | 200GbE to 2x100G, 26AWG |

---

## Technical Features: Passive vs Active DAC

Direct Attach Copper cables come in two configurations:

### 1. Passive DAC (LinkX Standard)
Passive copper cables have no active electronics inside the connector shells.
- **Latency**: Zero latency (determined only by speed of light through copper).
- **Power Consumption**: 0 Watts (does not draw power from switch or host ports).
- **Distance**: Typically capped at 3–5 meters due to signal attenuation.
- **Reliability**: Highest MTBF (Mean Time Between Failures) because there are no electronic components to fail.

### 2. Active DAC (ACC)
Active copper cables incorporate analog equalizer chips inside the connector to boost the signal.
- **Latency**: Negligible (sub-nanosecond).
- **Power Consumption**: Approx. 0.1–0.5 Watts per end.
- **Distance**: Extends copper reach up to 7–10 meters.

---

## Cable Thickness: 30AWG vs 26AWG

When looking at part numbers, you will notice wire gauges listed (e.g., 30AWG vs 26AWG):
- **30AWG**: Thinner, highly flexible cable. Ideal for intra-rack routing where space is tight. However, higher attenuation limits this wire size to shorter lengths (typically up to 2m or 3m).
- **26AWG**: Thicker, stiffer cable. Used for longer runs (3m to 5m) to maintain signal integrity over distance. Requires careful planning for bend radii in server cabinets.

---

Need help planning your rack cable management? [Contact the Yupitek engineering desk](/en/contact/) for expert advice.
