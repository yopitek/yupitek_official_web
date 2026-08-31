---
title: "DJI Drone Controller Antenna Upgrade: Extend Range with ALFA"
description: "Which DJI controllers accept ALFA antennas directly and which need a shell-opening mod? RC-N1 vs. RC2/RC Pro/Smart Controller, compatible models, installation steps, and legal notes."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-08-31
faq:
  - question: "Will replacing the antennas void my DJI warranty?"
    answer: "On models with exposed RP-SMA connectors like the RC-N1, external antennas are user-serviceable parts — swapping them is unlikely to affect the controller's warranty, but keep the stock antennas for reinstallation before service. RC2, RC Pro, and Smart Controller are different: opening the shell voids the warranty immediately. Confirm your model before deciding."
  - question: "My controller has no visible threaded antenna connectors. Can I still upgrade?"
    answer: "Yes, but the path is different. RC2, RC Pro, and Smart Controller have no exposed threaded ports, but you can still connect ALFA antennas by opening the shell and adding IPEX-to-RP-SMA adapter cables. This takes DIY/RF experience, voids the warranty, and may require drilling irreversible holes in the shell. If you lack the experience, use a professional mod service or stay stock."
  - question: "Can I use these ALFA antennas with non-DJI FPV systems?"
    answer: "Yes — any RP-SMA-compatible 2.4 GHz or 5.8 GHz system works, including ExpressLRS (ELRS) on 2.4 GHz, FrSky R9 (note: 915 MHz needs different antennas), TBS Crossfire (915 MHz, also incompatible), and 5.8 GHz video transmitters with RP-SMA connectors. Always match both the connector type and the frequency band."
  - question: "What's the difference between replacing one antenna vs. both on a dual-antenna RC-N1?"
    answer: "DJI's OcuSync system uses both antennas for diversity/MIMO reception, continuously selecting the stronger signal. Replacing only one antenna creates an asymmetric setup — the system favors the upgraded antenna most of the time, but performance is best when both antennas are matched. Replace both."
  - question: "Do I need to change any settings in the DJI app after upgrading?"
    answer: "No. DJI controllers manage antenna selection and frequency band selection automatically. No app configuration changes are required after a physical antenna swap."
  - question: "How do I choose between the APA-M25 and the ARS-25-57A?"
    answer: "If your controller stays pointed in roughly the same direction for most of the flight, choose the APA-M25 — the directional panel with the highest gain. If you frequently orbit, circle, or fly close-in patterns with large angle changes, or simply don't want to manage antenna pointing, choose the ARS-25-57A — the omnidirectional paddle that needs no aiming."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["DJI", "drone", "antenna-upgrade", "RP-SMA", "IPEX4", "range-extension", "ALFA-APA-M25", "ALFA-APA-M25-6E", "ALFA-ARS-25-57A", "ALFA-ARS-NT5B7"]
featureimage: "/images/blog/dji-drone-controller-antenna-upgrade.webp"
---

{{< tldr >}}
DJI controllers are not all upgradeable without opening the shell. **Only the RC-N1** keeps exposed RP-SMA female ports you can hand-tighten ALFA antennas onto. **RC2, RC Pro, and Smart Controller** — the screen-equipped models — have fixed antennas that only tilt, with internal IPEX micro-coaxial connectors; external high-gain antennas there require opening the shell, adding adapter cables, and void the warranty. This guide covers both scenarios and which ALFA antenna fits each.
{{< /tldr >}}

DJI drone controllers are not all built the same when it comes to antennas — and that is the single most important thing to know before you buy any upgrade. The **RC-N1** keeps the classic exposed RP-SMA female ports, so swapping in an ALFA antenna is a two-minute, tool-free job. The screen-equipped **RC2, RC Pro, and Smart Controller**, on the other hand, use fixed antennas with internal IPEX micro-coaxial connectors — you cannot simply unscrew them.

This guide walks through the two designs, the ALFA models that match each scenario, realistic range expectations from field observations, and the legal framework you need to respect. If you fly an RC-N1, you are one hand-tight turn away from a meaningful link upgrade. If you fly a screen controller, read the disassembly section carefully before you commit.

---

## Understanding DJI Controller Antennas

### Stock Antenna Performance

DJI's stock controller antennas are **omnidirectional rubber duck dipoles** rated at roughly **2 dBi gain**. They are optimized for compact size and broad coverage rather than maximum range in any one direction. That is fine for casual short-range flying — but if you regularly operate near the edge of your legal flight zone, there is real RF margin left on the table.

### Frequency Bands

DJI's **OcuSync 3 (O3)** and **O4** transmission systems cover:

- **2.4 GHz** — better obstacle penetration, preferred in congested RF environments
- **5.1 / 5.8 GHz** — higher throughput, lower latency; preferred in open areas

Dual- and tri-band controllers keep multiple bands active and let the system pick the cleaner channel automatically.

### Connector Types: Two Completely Different Designs

This is the core point of this revised guide. DJI controllers span two generations with two fundamentally different antenna architectures:

**① Exposed RP-SMA (screw-on, tool-free)**
Older, screen-less models such as the **RC-N1** keep the traditional design: a visible knurled metal collar at the antenna base, with an **RP-SMA Female** socket on the controller. The matching antenna needs an **RP-SMA Male** plug — exactly what ALFA accessory antennas ship with. You can remove the stock antenna by hand and screw on an ALFA antenna with zero tools.

**② Internal micro-coaxial connectors (shell-opening mod required)**
The newer screen-equipped models — **RC2, RC Pro, Smart Controller** — still show two antennas on the outside, but those are **fixed, angle-adjustable designs**, not threaded and removable. Open the shell and you will find **IPEX, IPEX4**, or similar micro-coaxial connectors soldered directly to the mainboard. The housing has no threaded port reserved for the user.

> **Background:** Community discussions have floated an interesting theory — RP-SMA was originally created partly in response to US (FCC) restrictions on removable antennas. In other words, DJI's shift to internal micro-coaxial connectors on screen controllers may not be about waterproofing or looks; the design deliberately discourages user antenna swaps. It also explains why newer models keep getting harder to "un-screw."

**How to tell:** Look at the antenna base on top of the controller. If you see a distinct hexagonal or knurled metal collar and the antenna unscrews by hand, it is exposed RP-SMA. If the antenna only tilts side to side and the shell is one continuous, seamless piece, it is the internal design — a shell-opening mod is the only path.

---

## Why Panel Antennas Improve Range

### Directional vs. Omnidirectional

A stock rubber duck antenna radiates RF energy in a roughly spherical pattern — 360° in the horizontal plane, roughly hemispherical vertically. That is ideal when you do not know where the target is, but wasteful when the drone is almost always in front of you.

A **panel (patch) antenna** concentrates RF energy into a forward-facing cone. Energy that would otherwise radiate behind you, sideways, or into the ground is redirected forward — increasing effective signal strength toward the drone without raising transmit power.

### Gain Math

Take the **ALFA APA-M25** as an example:

- **8 dBi** @ 2.4 GHz
- **10 dBi** @ 5.8 GHz

Versus the stock 2 dBi antenna, the 10 dBi panel adds about **8 dB of gain** in the forward direction:

> Every 3 dB of gain roughly doubles effective radiated power in that direction.
> 8 dB improvement ≈ about **6× stronger forward signal**.

### Free Space Path Loss

At 5.8 GHz, free-space path loss over 1 km is roughly **113 dB**. A 10 dBi panel recovers 8 dB of that link budget — meaningfully pushing back the point where the link drops below minimum receiver sensitivity.

### The Trade-Off

Directional antennas require you to **keep the panel facing the drone**. For most line-of-sight flying, that is just your natural holding posture; the APA-M25's beam width of about **60–70°** covers typical flight arcs without constant re-aiming.

{{< alert "circle-info" >}}
**Tip:** If your flying style involves large azimuth sweeps — orbiting the pilot, close-in proximity flying — an omnidirectional antenna like the ARS-25-57A or ARS-NT5B7 suits better than a panel, with no pointing to manage.
{{< /alert >}}

---

## Compatible ALFA Antenna Models

All four models below use **RP-SMA Male** connectors and cover the bands DJI O3/O4 systems use:

### APA-M25 — Dual Band 2.4/5 GHz (Best Choice)

The top pick for most DJI O3/O4 pilots. Dual-band coverage matches DJI's bands exactly, and the size-to-performance ratio suits field use.

| Item | Spec |
|---|---|
| Gain | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz |
| Beam width | 66° horizontal / 16° vertical |
| Dimensions | 167.3 × 66 × 18 mm |
| Weight | 72 g |
| Connector | RP-SMA Male |

At 72 grams, the APA-M25 does not cause noticeable fatigue on long flights, and the panel sits flat against the top of most DJI controllers for natural hand-held flying. If your model has two removable antennas (RC-N1), replacing both with APA-M25 panels gives the best result.

👉 [View the APA-M25 product page](/en/products/alfa/apa-m25/)

### APA-M25-6E — Triple Band with 6 GHz (Future-Proof)

Adds **6 GHz** band support on top of the APA-M25's dual-band foundation.

| Item | Spec |
|---|---|
| Gain | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz / **9 dBi @ 6 GHz** |
| Beam width | 60° horizontal / approx. 40–45° vertical (varies slightly by batch — check the package label) |
| Dimensions / weight | Same as APA-M25: 167.3 × 66 × 18 mm, 72 g |
| Connector | RP-SMA Male |

**Current DJI relevance:** No current DJI consumer drone uses 6 GHz for its primary control/video link. Consider this model if you also use the antenna with Wi-Fi 6E access points or adapters, if you expect future DJI systems to adopt 6 GHz spectrum, or if you run 6 GHz FPV setups. For DJI controllers alone, the standard APA-M25 delivers equal practical performance at lower cost.

👉 [View the APA-M25-6E product page](/en/products/alfa/apa-m25-6e/)

### ARS-25-57A — Dual Band Paddle (Everyday Upgrade, No Aiming)

A step up from a rubber duck without the directional awareness a panel demands — the **simplest upgrade path**: unscrew the stock antenna, screw on the ARS-25-57A, and fly. No pointing required.

| Item | Spec |
|---|---|
| Gain | 5 dBi @ 2.4 GHz / 7 dBi @ 5 GHz |
| Radiation pattern | Omnidirectional |
| Dimensions | 18.5 × 231 mm |
| VSWR | 2.5:1 |
| Operating temperature | −10°C to +55°C |
| Connector | RP-SMA Male |

Expect a measurable **3–5 dB** link quality improvement over stock (band-dependent) with none of the pointing overhead. Ideal for pilots who want a one-step upgrade and do not want to think about antenna orientation mid-flight.

👉 [View the ARS-25-57A product page](/en/products/alfa/ars-25-57a/)

### ARS-NT5B7 — Tri-Band Dipole (All-Weather)

An industrial-grade omnidirectional dipole covering all three modern Wi-Fi bands — lighter and more compact than a panel.

| Item | Spec |
|---|---|
| Gain | 4 dBi @ 2.4 GHz / 5 dBi @ 5 GHz / 7 dBi @ 6 GHz |
| Dimensions / weight | ⌀13 × 196 mm, 20 g |
| Operating temperature | **−40°C to +85°C** (industrial grade) |
| Connector | RP-SMA Male |

The industrial temperature rating suits extreme-weather flying — winter mountains, summer deserts. Where the APA-M25 offers higher forward gain, the ARS-NT5B7 keeps a full omnidirectional pattern for situations where precise pointing is impractical (vehicle mounts, tripod setups, multi-operator flights). The slim profile also catches less wind when hand-held in strong conditions.

👉 [View the ARS-NT5B7 product page](/en/products/alfa/ars-nt5b7/)

> **Note:** We also carry the single-band **APA-M04** (7 dBi @ 2.4 GHz), but since it only covers 2.4 GHz, we do not recommend it for DJI's dual/tri-band systems — which is why it is not in this lineup.

---

## Connector Compatibility Guide

### RP-SMA vs SMA: Critical Distinction

Nearly identical in appearance, physically and electrically incompatible:

| Feature | Standard SMA | RP-SMA (Reverse Polarity SMA) |
|---|---|---|
| Male plug center | Pin (solid) | Socket (hole) |
| Female jack center | Socket (hole) | Pin (solid) |
| Used in | Military/industrial RF | Consumer Wi-Fi, DJI RC-N1, etc. |
| ALFA antennas | ❌ Not used | ✅ All ALFA accessory antennas |

The RC-N1 uses an **RP-SMA Female** socket; ALFA accessory antennas use **RP-SMA Male** plugs — directly compatible, hand-tighten and go.

{{< alert "triangle-exclamation" >}}
**Never use a standard SMA antenna on an RP-SMA port.** The center pin/socket orientation is reversed. Forcing the connection can bend or snap the center pin, causing permanent damage. Always confirm RP-SMA compatibility before connecting any third-party antenna.
{{< /alert >}}

### Extension Cables

To mount antennas on a tripod or ground-station stand while operating the controller separately, use **RP-SMA extension cables**:

- **RG-316** — low-loss coaxial, flexible, good for field runs up to 50 cm
- **RG-174** — slightly lower loss than RG-316 at short lengths, very flexible
- Avoid generic **RG-58** — loss at 5.8 GHz is high enough to eat your antenna gain

A 30 cm RG-316 run typically adds under 1 dB of loss — acceptable for most setups.

---

## Controller Compatibility Reference

| DJI Controller Model | Frequency Bands | External Antenna Design | Internal Connector | ALFA Antenna Without Opening Shell? |
|---|---|---|---|---|
| **RC-N1** | 2.4 / 5.8 GHz | Removable threaded antennas | RP-SMA Female (exposed) | ✅ **Yes** — hand-tighten and fly |
| **RC2** (Air 3 / Air 3S / Mini 4 Pro) | 2.4 / 5.1 / 5.8 GHz | Fixed, angle-adjustable | IPEX4 (internal) | ❌ No — needs shell opening + adapter cables + drilling |
| **RC Pro** | 2.4 / 5.8 GHz | Fixed, angle-adjustable | Internal micro connector (IPEX4 or similar, model-dependent) | ❌ No — needs shell opening + adapter cables |
| **Smart Controller** | 2.4 / 5.8 GHz | Fixed | IPEX (internal) | ❌ No — needs shell opening + adapter cables |
| DJI Goggles 2 | 2.4 / 5.8 GHz | Model-dependent | Model-dependent | Verify individually — not covered in this table |

{{< alert "circle-info" >}}
**Tip:** Not sure which class your controller falls into? Check the antenna base — a visible knurled threaded collar that unscrews by hand means exposed RP-SMA like the RC-N1; antennas that only tilt with a seamless shell mean the internal design. **Do not force a twist on an internal antenna** — you can damage the antenna base and the controller port. Confirm your model before trying anything.
{{< /alert >}}

---

## Range Test Results (Real-World Expectations)

The figures below are typical field observations in clear line-of-sight environments. Actual results vary significantly with local RF interference, terrain, atmospheric conditions, and drone model.

| Setup | Typical Effective Range | Notes |
|---|---|---|
| Stock DJI antennas (both) | 1.5 – 3 km | Clear LOS, low interference |
| RC-N1 + APA-M25 (one) + stock | 2.5 – 4 km | Controller pointed at drone |
| RC-N1 + APA-M25 (both replaced) | 4 – 7 km | Both panels pointed at drone |
| RC-N1 + ARS-25-57A (both replaced) | 2 – 4.5 km | Omnidirectional, no pointing |
| RC-N1 + ARS-NT5B7 (both replaced) | 2 – 4 km | Industrial omni, similar pattern |
| RC2/Smart Controller shell mod + external high-gain | ~30–50% over stock per community builds (e.g., 3 km → 4 km class) | Requires shell opening and drilling; results vary widely with mod quality and environment — reference only |

{{< alert "triangle-exclamation" >}}
**Legal range reminder:** Extended antenna range does not authorize flying beyond any country's legal boundaries. In most jurisdictions — Taiwan, the EU, the US, Japan, Australia — recreational and commercial drone operations require maintaining **visual line of sight (VLOS)** at all times. The technical figures above may far exceed your legal operating envelope. Antenna upgrades deliver the most value by improving link **reliability and signal margin within legal VLOS range** — not by breaking past it.
{{< /alert >}}

---

## Legal and Regulatory Considerations

{{< alert "triangle-exclamation" >}}
**Important:** Extending your controller's RF range grants no permission to fly beyond legally established limits. Flying beyond visual line of sight (BVLOS) without specific authorization is illegal in most countries and carries serious penalties.
{{< /alert >}}

### VLOS Requirements

| Jurisdiction | Standard Limit | BVLOS Authorization |
|---|---|---|
| Taiwan (CAA) | VLOS required | Waiver/permit required |
| USA (FAA Part 107) | VLOS required | BVLOS waiver required |
| European Union (EASA) | VLOS required | Specific operations authorization |
| Japan (MLIT) | VLOS required | Level 4 certification required |

### Type Certification Implications

Replacing a controller's external antennas may affect its **CE, FCC, or local type certification** status. The controller was type-certified with its stock antennas; a higher-gain antenna can push the system past the certified equivalent isotropic radiated power (EIRP) for its band.

- Taiwan: operating radio equipment above NCC (National Communications Commission) EIRP limits violates the Telecommunications Management Act.
- USA: FCC Part 15 rules restrict EIRP for unlicensed devices.
- **ALFA antennas are sold as accessory replacement components.** Installation, compliance verification, and legal responsibility rest with the end user.
- For shell-opening models (RC2/RC Pro/Smart Controller), factor in **warranty loss** and **irreversible shell drilling** before you start.

{{< alert "circle-info" >}}
**Practical note:** For most DJI controllers operating within their designed EIRP budget, swapping a 2 dBi stock antenna for a high-gain ALFA panel changes antenna gain while transmit power output stays the same. Whether the resulting EIRP exceeds local limits depends on your specific controller model's original certified output power — check the DJI controller's regulatory documentation for its certified EIRP values.
{{< /alert >}}

---

## Installation Steps

Installation differs dramatically by model — first check the Controller Compatibility Reference above to see which class you are in, then follow the matching section.

### A. RC-N1 (Exposed RP-SMA, No Shell Opening)

**What you need:** ALFA antenna(s) with RP-SMA Male connector, your DJI controller.

1. **Power off the controller** before disconnecting any antenna.
2. **Grasp the stock antenna at its base**, near the controller body — not the antenna itself.
3. **Rotate counterclockwise** to unscrew; it should come free after 3–4 turns.
4. **Inspect the RP-SMA Female port** for debris or bent pins.
5. **Thread the ALFA antenna's RP-SMA Male plug** on by hand, clockwise.
6. **Tighten to hand-tight** — firm contact, no tools, no over-torquing. SMA/RP-SMA connectors are rated for hand-tightening only.
7. **Repeat for the second antenna** if your controller has dual ports.
8. **Store the stock antennas safely** — you will need them if the controller goes in for service.
9. **Power on and test** signal strength and flight behavior in a safe, open area.

**Antenna orientation:**

- Panel antennas (APA-M25 / APA-M25-6E): the **flat face points toward your primary flight area**; with two panels, mount them side by side at the same angle or in a slight **V (about 15°)** for wider horizontal coverage.
- Dipole/paddle antennas (ARS-NT5B7, ARS-25-57A): mount **vertically** for the best omnidirectional coverage in the horizontal plane.

### B. RC2 / RC Pro / Smart Controller (Internal — Shell-Opening Mod)

{{< alert "triangle-exclamation" >}}
**This procedure opens the controller shell and may require drilling — an irreversible mod that voids the DJI warranty immediately.** Intended for users with DIY/RF modification experience. If you are not confident opening the device, use a professional mod service or stay with the stock setup.
{{< /alert >}}

**What you need:**

- IPEX (or IPEX4, confirm per model) female → RP-SMA female (bulkhead) adapter cables × 2
- Phillips screwdriver
- Drill or craft knife (if drilling holes for RP-SMA bulkhead mounts; hole diameter follows the adapter spec, typically about 6–8 mm)
- ALFA antennas × 2 (APA-M25 or ARS-25-57A recommended)
- Hot glue or waterproof sealant (to secure bulkheads and seal drilled holes against dust and moisture)
- Smart Controller additionally: heat gun (to soften and remove the side pads)

**Steps:**

1. **Power off and remove the battery / disconnect power** to avoid short-circuit risk.
2. **Open the shell:** remove the rear housing screws (Smart Controller: soften the side pads with a heat gun first, then remove the back cover screws), carefully release the clips, and never yank ribbon cables.
3. **Locate the stock antenna connectors:** find the IPEX/IPEX4 antenna connectors on the mainboard.
4. **Unplug the stock connectors:** pull straight up gently — excessive force can damage the board-side sockets.
5. **Choose drill positions** (if needed): pick shell sides or top spots that do not interfere with grip or internal space.
6. **Drill and test-fit the bulkheads;** confirm a snug fit and deburr the edges.
7. **Connect the adapter cables:** plug the IPEX end into the original board socket, and mount the RP-SMA female end from inside the shell so the threads protrude outside.
8. **Do both antennas** — avoid asymmetric diversity/MIMO reception.
9. **Seal against dust:** reinforce along the hole edges to keep out debris and moisture.
10. **Reassemble the shell** and refit all original screws.
11. **Screw on the ALFA antennas** hand-tight — no excessive force.
12. **Power on and test** signal and range in a safe, open area.

---

## Frequently Asked Questions

**Q: Will replacing the antennas void my DJI warranty?**

A: On models with exposed RP-SMA connectors like the RC-N1, the external antennas are user-serviceable parts — swapping them is unlikely to affect the controller's warranty, but keep the stock antennas so you can reinstall them before sending the controller in for service. **RC2, RC Pro, and Smart Controller are a different story: opening the shell voids the warranty immediately.** Confirm your model before you decide.

---

**Q: My controller has no visible threaded antenna connectors. Can I still upgrade?**

A: Yes, but the path is different. RC2, RC Pro, and Smart Controller have no exposed threaded ports, but you can still connect ALFA antennas by opening the shell and adding adapter cables. That takes DIY/RF modification experience, voids the warranty, and may require drilling irreversible holes in the shell. If you do not have the experience, use a professional mod service or stay with the stock setup.

---

**Q: Can I use these ALFA antennas with non-DJI FPV systems?**

A: Yes — any RP-SMA-compatible 2.4 GHz or 5.8 GHz system works, including:

- **ExpressLRS (ELRS)** transmitters and receivers on 2.4 GHz
- **FrSky R9** systems (note: R9 runs on 915 MHz — a different frequency that needs different antennas)
- **TBS Crossfire** (915 MHz — also incompatible; requires 900 MHz antennas)
- **5.8 GHz video transmitters (VTX)** with RP-SMA connectors

Always match both the connector type **and** the frequency band when choosing a replacement antenna.

---

**Q: What's the difference between replacing one antenna vs. both on a dual-antenna RC-N1?**

A: DJI's OcuSync system uses both antennas for **diversity/MIMO reception**, continuously selecting the stronger signal. Replacing only one antenna with a high-gain panel creates an asymmetric setup where the two antennas perform very differently. The system will favor the upgraded antenna most of the time, but performance is best when both antennas are matched — replace both.

---

**Q: Do I need to change any settings in the DJI app after upgrading?**

A: No. DJI controllers manage antenna selection and frequency band selection automatically. No app configuration changes are required after a physical antenna swap.

---

**Q: How do I choose between the APA-M25 and the ARS-25-57A?**

A: If your controller stays pointed in roughly the same direction for most of the flight, choose the **APA-M25** — the directional panel with the highest gain. If you frequently orbit, circle, or fly close-in patterns with large angle changes — or simply do not want to manage antenna pointing — choose the **ARS-25-57A**, the omnidirectional paddle that needs no aiming.

---

{{< faq >}}

## Conclusion

Upgrading DJI controller antennas delivers very different results and complexity depending on your model. The **RC-N1**, with its exposed RP-SMA ports, is one of the most accessible and cost-effective RF improvements available to drone operators — a hand-tightened swap with zero tools. The newer screen-equipped **RC2, RC Pro, and Smart Controller** use fixed internal antenna designs; external high-gain antennas there mean opening the shell, adding adapter cables, and accepting warranty loss — know this before you start.

Whichever class your controller falls into, the goal of an antenna upgrade is improved **reliability and link margin within your legal flight zone** — not a license to fly beyond regulatory limits. Fly responsibly, keep your stock parts safe, and enjoy the improved link quality.

---

## References

1. [DJI Official Website — Controller Product Specs](https://www.dji.com/)
2. [DJI RC 2 Support Page](https://www.dji.com/support/product/rc-2)
3. [FCC Part 15 — Unlicensed RF Equipment Regulations](https://www.fcc.gov/engineering-technology-laboratory-division/general/radio-spectrum-and-rulemaking)
4. [ALFA Network Official Website — Antenna Accessory Specs](https://www.alfa.com.tw/)
5. [Taiwan NCC — Telecommunications Management Act](https://www.ncc.gov.tw/)
6. [IEEE 802.11 Standards — Wireless LAN Specifications](https://standards.ieee.org/ieee/802.11/)
7. mavicpilots.com community threads: "RC2 / RC external antenna mod", "RC 2 and RC Pro controller external antennae", "Connecting external antennas to the RC Plus" (2024)
8. Alientech — "How to modify antenna of the DJI smart controller" mod tutorial (2019)