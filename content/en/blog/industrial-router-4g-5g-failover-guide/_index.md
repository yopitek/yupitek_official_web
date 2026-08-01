---
title: "How Industrial Routers Handle 4G/5G Failover: A Practical EM9191 Private 5G Deployment Guide"
locale: "en"
hreflang_group: "industrial-router-4g-5g-failover-guide"
description: "How do industrial routers deliver 4G/5G failover? Using the Sierra Wireless EM9191 as an example, this guide explains the difference between 5G SA private networks and LTE backup architectures, covering bands, antennas, and thermal management so you get the hardware integration right the first time."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "industrial-router-4g-5g-failover-guide"
tags: ["Sierra Wireless", "EM9191", "4G", "5G", "Failover", "Industrial Router", "LTE", "5G SA", "M.2"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/en/products/sierra/"
faq:
  - question: "Does the EM9191 support 5G mmWave?"
    answer: "No. The official specification clearly states that the EM9191 does not support FR2 (mmWave). If you need mmWave capability, choose the EM9190 instead."
  - question: "Can the EM9191 be used on a private 5G network?"
    answer: "Yes. Private 5G networks mainly rely on the SA (Standalone) architecture, and the EM9191 fully supports 5G NR FR1 SA operation."
  - question: "What should I watch out for when integrating the EM9191 into a router?"
    answer: "Four key points: 1. It measures 52mm, not 42mm. 2. All four antenna connections must be populated. 3. The supply must handle a 2.7A peak current. 4. Cooling matters; the internal temperature must stay below 115°C."
---

# How Industrial Routers Handle 4G/5G Failover: A Practical EM9191 Private 5G Deployment Guide

**In one sentence: adding a 5G module to your industrial router for failover is like buying insurance. The Sierra Wireless EM9191 supports both ultra-fast 4G (LTE Cat 20) and private 5G networks (5G SA). Run 4G failover today, and when your site builds out a private 5G network later, you keep the same hardware and switch over seamlessly.**

In a factory, every minute of network downtime burns money. Machine data stops flowing, remote monitoring goes dark, and the loss quickly outweighs the cost of a backup link. That is why failover matters so much. Rather than pulling a second physical fiber from another carrier, dropping in a SIM card and routing over the mobile network is the smartest play.

In this article we walk through the official spec sheet (EM919X Product Technical Specification) and explain why the **EM9191** is the perfect choice for backup today and private 5G tomorrow.

> Technical source: the Sierra Wireless official specification. Compiled by Yupitek.

---

## The 30-Second Overview: What Can the EM9191 Do?

| Your Need | Can the EM9191 Handle It? | Why? |
|---|---|---|
| **4G backup connectivity** | ✅ Yes, perfectly | It supports LTE Cat 20 (with powerful 7CC carrier aggregation), more than enough speed for backup. |
| **Connect to a private 5G network** | ✅ Yes, perfectly | It supports 5G FR1 (Sub-6) SA operation, the essential requirement for private 5G. |
| **5G mmWave** | ❌ No | The official docs are clear: not supported. For mmWave, buy the EM9190. |
| **Pure cost savings** | ⚠️ Consider another model | If you are 100% certain you will never need 5G, a 4G-only module (such as the EM7690 or EM7565) is much cheaper. |

---

## How Does Failover Work?

Put simply, your router runs a software watchdog that keeps pinging your primary link (for example, fiber). When it detects that the primary link is down, it shouts "switch!" and redirects all data packets to the EM9191 module in the router, sending them over 5G. When the primary link comes back, it quietly routes traffic back.

**In other words, a backup link does not need to be the fastest; it needs to never go down.** The clever part of the EM9191 is that if the 5G signal degrades, it automatically falls back to 4G and keeps transmitting, so your network never drops.

---

## Why the EM9191 Buys You Two Futures at Once

Inside the EM9191 sits the Qualcomm SDX55 5G chipset. Per the official specs, it supports the two most critical modes at the same time:

1. **LTE Only** (pure 4G mode)
2. **5G NR FR1 SA / NSA** (5G standalone and non-standalone)

What does this mean?
- **Today**: you can treat it as a premium 4G card (Cat 20 class), because public 5G coverage still has dead zones.
- **Later**: when your company decides to build a "private 5G network" (which typically uses the SA standalone architecture and Sub-6 bands), this card can connect directly to it with just a configuration change. No need to spend money on new hardware.

---

## Hard Knowledge for Engineers: 4 Pitfalls to Check Before Integration

Do not assume you can just plug the module in and be done. The EM9191 is a power-hungry, heat-generating beast. Pay attention to these four points when integrating it into a router:

### 1. Missing Antennas Cuts Speed in Half
The EM9191 has **4 MHF4 antenna connectors**. To unlock its full 4x4 MIMO capability (especially on the 5G n78 band), you must connect all four antennas. Sierra also recommends keeping cable loss under 0.5dB, so skip those long, cheap cables.

### 2. Weak Power Means Instant Disconnects
The EM9191 runs on 3.3V. Here is the key: during data transmission, the **instantaneous peak current reaches 2.7A (2700mA), and continuous draw is 2A (2000mA)**. If your router's power design is weak, the module will drag down the voltage the moment it ramps up, then reboot endlessly.

### 3. Poor Cooling Will Crash the Module
5G modules run much hotter than 4G. The official spec says the internal temperature **must never exceed 115°C (ideally keep it below 100°C)**. If you bury it inside an outdoor metal-shell router, a summer sun will guarantee a thermal shutdown. Prepare a heatsink and conduct the heat into the enclosure.

### 4. Slot Length and Interface
It uses the M.2 form factor, but the length is **52mm**, longer than the 42mm modules commonly used before. The interface can be PCIe Gen3 or USB 3.1 Gen2. Note: support for legacy USB 2.0 is not guaranteed.

---

## Conclusion

For finding a backup network for industrial equipment, the EM9191 is a choice that covers both attack and defense.
With its strong LTE Cat 20 and 5G SA support, it perfectly covers "4G backup today" and "5G private network tomorrow". As long as you take care of power (2.7A peak), cooling (the 115°C red line), and antennas (all 4 populated) during integration, it will save you when it matters most.

## Purchasing Information (Call To Action)

Want to integrate the EM9191 into your industrial router? Yupitek offers complete hardware solutions and technical support to solve the toughest cooling and antenna challenges.
Contact us: **sales@yupitek.com**
Browse the lineup: [Sierra Wireless Modules](https://yupitek.com/en/products/sierra/)
