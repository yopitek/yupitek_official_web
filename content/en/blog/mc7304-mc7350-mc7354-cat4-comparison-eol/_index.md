---
title: "Sierra MC7304 vs MC7350 vs MC7354: Choosing Legacy Cat 4 Modules and Long-Term Stocking"
description: "How do the MC7304, MC7350, and MC7354 differ? This article cross-checks the official specifications and FCC filings to break down LTE bands, downlink rates, antennas, and temperature ratings, exposes the Cat 3/Cat 4 rate debate, and offers stocking advice for legacy mPCIe modules plus an EM7455 upgrade assessment. A must-read for engineers."
date: 2026-08-01
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "mc7304", "mc7350", "mc7354", "mpcie", "cat4", "lte", "eol", "module-selection"]
author: "benny-lai"
lastmod: 2026-08-01
faq:
  - question: "What is the actual difference between the MC7304, MC7350, and MC7354?"
    answer: "All three are Sierra Wireless AirPrime MC-series mPCIe modules built on the MC73XX platform (peak downlink 100 Mbps, peak uplink 50 Mbps, built-in GPS + GLONASS, and 3 RF antenna connectors). The difference lies in bands and positioning: the MC7304 covers EMEA LTE plus WCDMA and GSM; the MC7350 covers North American LTE plus CDMA with no GSM; the MC7354 is the full multi-carrier North American variant."
  - question: "Are these modules discontinued? How should we stock spares?"
    answer: "The official documentation contains no formal end-of-life (EOL) announcement for these three, but they belong to an older mPCIe generation. Stocking strategy: first ask the original manufacturer about the latest lifecycle status, and evaluate the MC7455 (same form factor) or the EM7455/EM7565 (M.2 generation) as replacement paths in parallel."
  - question: "Can I simply swap the MC73XX for an EM7455?"
    answer: "No. The MC73XX uses mPCIe packaging while the EM7455 uses M.2, and the slots are electrically and mechanically incompatible. Upgrading to the EM7455 requires a new carrier board or a motherboard redesign. If you must stay in the same slot, the mPCIe upgrade path is the MC7455 (Cat 6, 300/50 Mbps)."
  - question: "Is the downlink rate 100 Mbps or 150 Mbps?"
    answer: "The official MC-series manual lists a peak downlink of 100 Mbps and peak uplink of 50 Mbps for the MC73XX, and FCC test filings also classify them as LTE Cat 3 (100/50 Mbps). The 'Cat 4 / 150 Mbps' claim still awaits confirmation from the latest vendor documentation, so we recommend using 100/50 Mbps as the baseline."
---


> **Bottom line first**: the MC7304, MC7350, and MC7354 are three Sierra Wireless AirPrime MC-series mPCIe cellular modules from the same MC73XX family. The official manual lists a peak downlink of 100 Mbps and peak uplink of 50 Mbps, with support for LTE, HSPA+, and GSM/GPRS/EDGE. The MC7354 and MC7350 also add CDMA fallback. All three integrate GPS + GLONASS positioning and require 3 external antennas. Detailed technical references: [MC7304](/en/products/sierra/mc7304/) | [MC7350](/en/products/sierra/mc7350/) | [MC7354](/en/products/sierra/mc7354/).

If you have seen these Sierra modules inside a server room, an ATM, or a legacy industrial gateway, you may wonder what actually differs between model numbers that look almost identical. The answer is that their **band configurations target completely different markets**. Install the wrong model and the device may not connect to the network at all. In this article, we cross-check the official manuals and FCC filings to help you quickly understand the differences between these three modules, how to stock spares, and whether an upgrade to a newer module is feasible.

---

## 1. Core Differences at a Glance (30-Second Overview)

All three are mPCIe slot modules sharing the MC73XX platform (peak downlink 100 Mbps, peak uplink 50 Mbps). The real difference comes down to where you plan to deploy the device:

| Question | Short answer |
|---|---|
| **What is the difference between the MC7304 and MC7350?** | The bands. The MC7304 covers mainstream EMEA bands (LTE B1/B3/B7/B8/B20) with no CDMA; the MC7350 covers North American bands (LTE B4/B13/B25 plus CDMA) with no GSM. Use it in the wrong region and you get no signal. |
| **Are these modules close to being discontinued?** | The official documents we have on hand do **not** list an end-of-life (EOL) date. They are, however, an older-generation product, so check the latest status with the manufacturer before committing to long-term stocking. |
| **How fast are they actually?** | The official manual lists 100 Mbps downlink and 50 Mbps uplink; FCC tests classify them as LTE Cat 3. Although they are commonly marketed as Cat 4 (150 Mbps), we conservatively go with 100/50 Mbps based on public documents (details in a later section). |
| **Do they have built-in antennas?** | No. All three have 3 RF connectors (Main, Aux, GNSS), and the antennas must be connected externally. |

---

## 2. Quick Reference Table: Bands and Certifications

Here are the hardware specifications everyone cares about most:

| Item | MC7304 | MC7350 | MC7354 |
|---|---|---|---|
| **Packaging and dimensions** | mPCIe (50 x 30 x 2.7 mm) | mPCIe | mPCIe (50.95 x 30 x 2.75 mm, 8.6 g) |
| **Supported networks** | LTE, HSPA+, GSM/GPRS/EDGE | LTE, HSPA+, CDMA 1xRTT/EV-DO | LTE, HSPA+, GSM/GPRS/EDGE, CDMA 1xRTT/EV-DO |
| **Peak downlink / uplink** | 100 / 50 Mbps | 100 / 50 Mbps | 100 / 50 Mbps |
| **LTE bands** | B1, B3, B7, B8, B20 | B4, B13, B25 | B2, B4, B5, B13, B17, B25 |
| **WCDMA bands** | B1, B2, B5, B8 | (per distributor) | B1, B2, B4, B5, B8 |
| **CDMA / GSM** | GSM only | CDMA only | Both |
| **GNSS positioning** | GPS, GLONASS | GPS, GLONASS | GPS, GLONASS |
| **Antenna connectors** | 3 (Main, Aux, GNSS) | 3 | 3 |
| **USB interface** | USB 2.0 High Speed | USB 2.0 High Speed | USB 2.0 |
| **Operating temperature** | -40°C to +85°C | -40°C to +85°C | Class A: -30°C to +70°C; Class B: -40°C to +85°C |

> **Note**: carrier and regulatory certifications change over time. The bands listed here come from the specification sheets of their era, so confirm current availability with a distributor before purchasing.

---

## 3. Band Philosophy: Who Is Each Module Designed For?

### MC7304: The EMEA All-Rounder
This module covers mainstream EMEA LTE bands (B1/B3/B7/B8/B20) with WCDMA and GSM support, and it deliberately avoids CDMA. If your device is deployed in Taiwan, Europe, or the Asia-Pacific region, this is the safest choice.

### MC7350: The North American Trimmed-Down Option
This module was built for Verizon and Sprint in North America, with LTE support on B4/B13/B25, CDMA included but **no GSM**. Use it in Asia and it is essentially useless.

### MC7354: The Full North American Option
This is the most band-complete North American variant in the family. Besides LTE (B2/B4/B5/B13/B17/B25), it packs in UMTS, CDMA, and GSM. If your device needs to work across multiple carriers in North America, this module offers much more peace of mind than the MC7350.

---

## 4. The Perennial Question: Is It Cat 3 or Cat 4?

Many people in the market call these "Cat 4 modules," but honestly, the claim is debatable:

1. Both the **official manual** and **FCC tests** list the MC73XX at **100 Mbps downlink and 50 Mbps uplink**, which is the Cat 3 standard.
2. Rumor has it the vendor's internal specification sheet lists Cat 4 (150 Mbps), but that document has not been made public.
3. The chipset is also cited two ways: the official documentation says Qualcomm MDM9215, while some distributors list MDM9615.

**Our recommendation**: treat them as 100/50 Mbps. There is no need to fight the spec sheet over an extra 50 Mbps of theoretical headroom.

---

## 5. What About Existing Deployments? Stock Spares or Upgrade?

For these aging mPCIe modules, the thing enterprises fear most is suddenly being unable to source them.

### Long-Term Stocking Strategy
Since no one knows exactly when they will be discontinued, the first step is to ask the manufacturer or distributor about the current lifecycle status. If the modules are still orderable, stock extra units based on your installed base. Also, back up the firmware versions that currently work well, so you are not caught off guard by issues in a new production batch.

### Upgrade Paths (Can I Move to the EM7455?)
If you want to upgrade to the newer **EM7455** (Cat 6, 300/50 Mbps), note that **the slots are different!**
The MC73XX is mPCIe; the EM7455 is M.2. You would have to change the motherboard or add an adapter board.
If you do not want to touch the motherboard, you can directly pick the **MC7455**, which is also mPCIe, and get a seamless speed upgrade.

---

## 6. Common Pitfalls

1. **Buying on the "Cat 4" label alone**: if you test it in the field and only get 100 Mbps, trust the FCC test data.
2. **Buying the MC7350 for use in Asia**: the bands do not match, and it will not connect at all.
3. **Forgetting that the slots differ**: you want to upgrade to an M.2 module, but the motherboard only has an mPCIe slot.

## Conclusion

The MC7304, MC7350, and MC7354 trio is actually easy to tell apart: **choose the 04 for Asia and the 50 or 54 for North America**. The speed may only be Cat 3 level, but on legacy industrial equipment they remain a very stable choice. For a long-term solution, find out the EOL timeline first, then decide whether to do a seamless upgrade to the MC7455.

## FAQ

{{< faq >}}

## Sourcing Information (Call to Action)

Need these modules or unsure how to choose? Yupitek is a professional hardware integration partner that can help you confirm bands, slots, and stocking questions.

- **Product pages**: [MC7304](/en/products/sierra/mc7304/) | [MC7350](/en/products/sierra/mc7350/) | [MC7354](/en/products/sierra/mc7354/)
- **Email**: sales@yupitek.com
