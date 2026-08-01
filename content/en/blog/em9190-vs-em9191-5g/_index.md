---
title: "EM9190 vs EM9191: Sub-6 or mmWave 5G, Which One Should You Pick?"
description: "EM9190 vs EM9191: based on the official spec (41113174 Rev 8), the EM9190 supports 5G Sub-6 plus mmWave (n257/258/260/261, NSA only), while the EM9191 is Sub-6 only. Both run the Qualcomm SDX55 in M.2. Includes a Taiwan 5G band reference, compiled by Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM9190_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "What is the real difference between the EM9190 and EM9191? Which one supports mmWave?"
    answer: "Per the official spec (41113174, Rev 8), both modules share the same Sub-6 (FR1), LTE, 3G, and GNSS capabilities. The only major difference is 5G mmWave (FR2): the EM9190 supports LTE+FR2 NSA EN-DC (with a QTM525/QTM527 mmWave antenna module, NSA mode only), while the EM9191 is marked Not supported. So the EM9190 is the one with mmWave."
  - question: "Is the EM9191 a good fit for 5G in Taiwan?"
    answer: "Yes. Taiwan's 5G core band is 3.5 GHz, which maps to 3GPP n78 (3300–3800 MHz, TDD), and both the EM9190 and EM9191 support n78. Taiwan's 28 GHz (n257) deployments are rare, and only those scenarios need the EM9190 plus mmWave antenna modules. For typical 5G FWA and industrial routers, the EM9191 is enough."
  - question: "Does buying the EM9190 automatically include mmWave?"
    answer: "No. The EM9190 has no built-in antenna. mmWave needs 1–4 optional Qualcomm QTM525 (low power, EIRP 23 dBm) or QTM527 (high power, EIRP 45 dBm) antenna modules, each connected by two MHF7S IF cables (up to 8 total), powered from an external 3.8 V supply, and FR2 runs in NSA mode only."
  - question: "How different is the power draw between the two modules?"
    answer: "Per Table 3-2 of the spec: peak current is 5.0 A for the EM9190 with mmWave, 3.0 A without mmWave, and 2.7 A for the EM9191; continuous current is 4.0 A, 2.3 A, and 2.0 A respectively. For battery-powered or thermally constrained devices, the EM9191 is easier on the power design."
  - question: "Can the EM9190 and EM9191 share a motherboard design?"
    answer: "Largely yes. Both are M.2 (WWAN Type 3042-S3-B, 52 mm long) with the same 75-pin layout, the same USB 3.1 Gen2 / PCIe Gen3 interfaces, and the same 4× MHF4 Sub-6 antenna ports. The difference: the EM9190 adds 8× MHF7S mmWave IF connectors and QTM control pins (pins 40/42/44/46/48, NC on the EM9191)."
---

# EM9190 vs EM9191: Sub-6 or mmWave 5G, Which One Should You Pick?

If you are working on a 5G project with a professor at university, or you own 5G module selection at your company, you have probably read this line: "The EM9190 is the budget Sub-6 version; the EM9191 is the flagship with mmWave."

**Wrong. It is exactly backwards.**

We are not going to rely on forum posts. This article uses a single reference: the Sierra Wireless official specification, the EM919X/EM7690 Product Technical Specification (Doc 41113174, Rev 8, May 2023). We check the differences between the two modules item by item, with special attention to the bands Taiwan readers care about most: n78 and the 28 GHz band. The goal is simple: you do not buy the wrong 5G module.

> Product pages: [EM9190 — Yupitek](/en/products/sierra/em9190/) | [EM9191 — Yupitek](/en/products/sierra/em9191/) | Official spec: [EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## Debunking the Myth: What Is the Real Difference?

**In short, the EM9190 and EM9191 come from the same family: same series, same baseband chip. Both support 5G Sub-6, 4G LTE, and GNSS positioning. The only difference: the EM9190 adds 5G mmWave (FR2), and the EM9191 does not.**

To get mmWave on the EM9190, you must also pair it with a Qualcomm QTM525 or QTM527 antenna module (and it runs in NSA mode only).

| Your question | The answer from the official spec |
|---|---|
| **What is the difference between the two cards?** | mmWave (FR2). The EM9190 spec reads "LTE+FR2 NSA EN-DC Supported"; the EM9191 reads "Not supported". Everything else, Sub-6 bands and LTE included, is identical. |
| **Does the EM9190 have mmWave?** | Yes, but not out of the box. You add a Qualcomm mmWave antenna module (up to 4), covering n257/n258/n260/n261, and it only runs in NSA (non-standalone) mode. |
| **Does the EM9191 have mmWave?** | No. Table 1-1 explicitly marks it "Not supported", and every mmWave-related signal pin on the board is NC (no connection). |
| **Which one should I buy for a 5G project in Taiwan?** | Taiwan 5G mostly runs on 3.5 GHz (n78), which both modules support. 28 GHz (n257) is rare in Taiwan; only for that kind of experiment do you need the EM9190 plus mmWave antennas. |
| **Who should buy which?** | **EM9190**: US/JP market, lab mmWave testing, outdoor CPE equipment that needs very wide bandwidth.<br>**EM9191**: Sub-6 projects in Taiwan or Asia, lower power draw, tighter budget. |

> **One more time**: stop believing the "EM9191 is the mmWave flagship" story. The official spec says in black and white that **the EM9190 is the one with mmWave**. Getting it backwards is an expensive mistake.

---

## One Family, Three Brothers: EM9190 / EM9191 / EM7690

The EM91 family has three members. Per the spec:

- **EM9190**: the full package (LTE + 5G Sub-6 + 5G mmWave)
- **EM9191**: the practical standard model (LTE + 5G Sub-6, no mmWave)
- **EM7690**: the downgraded model (LTE only, no 5G)

This article focuses on the two 5G siblings. EM7690 is just for context.

---

## Hardcore Spec Comparison (From Official 41113174 Rev 8)

Every figure below comes from the official spec. If you are an engineer, this table is the fastest way in:

| Item | EM9190 | EM9191 | Source |
|---|---|---|---|
| **5G NR Sub-6 (FR1)** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave (FR2)** | ✓ (NSA mode only, external antenna modules required) | ✗ | Table 1-1 |
| **FR2 mmWave bands** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **FR1 Sub-6 bands** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | Same for both | Table 4-4 |
| **Baseband chipset** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **Cellular standard** | 5G 3GPP Release 15; LTE Release 15 | Same for both | Table 2-1 |
| **Form factor** | M.2 (WWAN Type 3042-S3-B, 52 mm long) | Same for both | §1.2 |
| **Host interface** | USB 3.1 Gen2, PCIe Gen3 single lane | Same for both | §1.3 |
| **Sub-6 antenna ports** | 4× MHF4 (MAIN/MIMO1/MIMO2/AUX) | Same for both | §4.1 |
| **mmWave antenna ports** | 8× MHF7S (up to 4 external antenna modules) | None | §4.1 |
| **Peak current** | 5.0 A (with mmWave) / 3.0 A (without) | 2.7 A | Table 3-2 |
| **Operating temperature** | -30°C to +70°C (Class A); -40°C to +85°C (Class B, reduced performance) | Same for both | Table 7-1 |
| **GNSS** | L1 (GPS/GLONASS etc.) + L5 (optional) | Same for both | Table 4-13 |

> **Quick note**: this spec is from May 2023. Some bands (n7, n8, n20 and others) vary by firmware or shipping SKU. Before ordering for a project, ask us for the latest official documents to cross-check.

---

## mmWave Is Not Included: The Hidden Cost of the EM9190

Many students and makers assume that buying the EM9190 means you can test mmWave right away. That is completely wrong.

The spec is explicit: "**The EM9190 supports 5G mmWave only when paired with the optional Qualcomm mmWave antenna modules.**" On top of that, it only runs in NSA (non-standalone) mode, so you need a 4G LTE signal as an anchor to connect at all.

### How do you configure mmWave antennas?

You buy Qualcomm QTM525 (low power) or QTM527 (high power) antenna modules. Different antenna modules cover different bands (see Table 4-2 of the official spec):

- To test **n257** (Taiwan's 28 GHz band), you need the QTM525-2, QTM525-5, or QTM527-2. Buy the QTM527-1 and you get no n257.

**Engineer beware**: an outdoor 5G receiver (CPE) built on the EM9190 may need all four high-power QTM527 antennas. That means eight expensive MHF7S cables, a separate 3.8 V supply for the antenna modules, and serious cooling. The engineering cost here is often much higher than the module itself.

---

## Building 5G in Taiwan? The EM9191 Is Enough

**Taiwan 5G runs mostly on 3.5 GHz, which is 3GPP n78, and both the EM9190 and EM9191 support n78 perfectly.**

If your project only needs 5G in Taiwan, or you are building industrial routers for regular customers:

- Both modules support Taiwan's 5G n78 (3300–3800 MHz).
- Both support Taiwan's existing 4G bands (fine as an NSA anchor).

**Why do we recommend the EM9191?** Because if you do not need mmWave, paying for the EM9190 is wasted money. And with no mmWave hardware, the EM9191 peaks at 2.7 A, far easier on the power design than the EM9190 (details below).

---

## Power Draw Comparison: Don't Mess Up Your Power Design

Anyone who builds hardware knows that an underpowered supply causes random reboots. Official figures from Table 3-2:

| Power parameter | EM9190 (with mmWave) | EM9190 (without mmWave) | EM9191 |
|---|---|---|---|
| Peak current | 5.0 A | 3.0 A | 2.7 A |
| Continuous current | 4.0 A | 2.3 A | 2.0 A |

All modules run on 3.135 V to 4.4 V (usually designed at 3.3 V). Turn on mmWave on the EM9190 and peak current jumps to 5.0 A. That is a serious challenge for battery-powered or compact devices. If you only need Sub-6 5G, the EM9191's 2.7 A peak keeps the power design simple.

---

## Pin Layout: Can the Two Share a Board Design?

**Yes, you can share the Sub-6 design.**

Both modules use the M.2 form factor (52 mm long, a bit longer than the 42 mm found in laptops, so watch your mechanical space) with the same 75-pin layout.

The only difference: to control its mmWave antennas, the EM9190 uses pins that are otherwise empty, such as QTM_PON on pins 40/42/44/46 and the 1.9 V supply on pin 48. These pins are NC on the EM9191. So design a universal EM9191 board first, then add the EM9190 control lines when you actually need mmWave.

---

## Verdict: Which One Should You Buy?

| Your requirement | Choose EM9190 | Choose EM9191 |
|---|---|---|
| Need to test mmWave bands like 28 GHz | ✅ The only option (add the antennas) | ❌ Not supported |
| Project in Taiwan using only 5G Sub-6 (n78) | Works (but wasteful) | ✅ Recommended, cheaper and more efficient |
| Board power can't handle big current draw | ⚠️ Peak can hit 5.0 A | ✅ 2.7 A peak is much easier |

**Pitfall guide**:

1. Stop getting it backwards: the EM9190 is the one with mmWave.
2. Buying the EM9190 does not give you mmWave. You also buy the special antennas and run the cabling.
3. Many bands (n7, n8, n28 and others) are limited by firmware version and region. Confirm with your supplier whether your SKU can unlock those bands before buying.

---

## Quick FAQ

{{< faq >}}

---

## Ready to Buy or Discuss? Talk to Us

If you have hardware integration questions after reading this, or your lab or company wants to procure these two 5G modules, reach out to the Yupitek engineering team. We also carry matching antennas and adapter boards.

- **EM9190 (the real flagship with mmWave) product page**: [https://yupitek.com/en/products/sierra/em9190/](/en/products/sierra/em9190/)
- **EM9191 (the practical Sub-6 model) product page**: [https://yupitek.com/en/products/sierra/em9191/](/en/products/sierra/em9191/)
- **All Sierra models**: [https://yupitek.com/en/products/sierra/](/en/products/sierra/)
- **Email us**: sales@yupitek.com
