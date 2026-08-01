---
title: "Cellular Backhaul for Video Surveillance and Digital Signage: Cat 6 to 5G, What Should You Pick?"
locale: "en"
hreflang_group: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
description: "Which cellular module do you need for surveillance cameras and digital signage? The answer is all about uplink vs. downlink. Based on the official spec sheets, we compare the EM7455 (Cat 6), EM7565 (Cat 12) and EM9191 (5G) so you can pick the right one without wasting money."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
tags: ["Sierra Wireless", "EM7455", "EM7565", "EM9191", "4G surveillance backhaul", "digital signage", "5G video backhaul", "Cat 6", "LTE"]
categories: ["Technical"]
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/en/products/sierra/"
faq:
  - question: "For 4G backhaul from surveillance cameras, how much uplink speed is enough?"
    answer: "A single 1080p H.264 stream needs roughly 2~6 Mbps. With the EM7455, which tops out at 50 Mbps uplink, you can carry about 4~6 1080p streams reliably. For larger demands, upgrading to the EM7565 is recommended."
  - question: "Is Cat 6 enough for connecting digital signage?"
    answer: "Digital signage is mostly downlink traffic. Cat 6 (such as the EM7455) offers 300 Mbps downlink, which is plenty for routine image and video updates. If you need to push very large 4K video files frequently, the EM7565 (600 Mbps) shortens download time."
  - question: "What should I watch out for when putting a 4G/5G module inside an outdoor enclosure?"
    answer: "Two things: heat and power. Internal module temperature must usually stay under 90°C~115°C, and outdoor metal boxes overheat easily, so you need proper heat conduction. Also, a 5G module can draw up to 2.7 A instantaneously, so the power converter must handle the surge."
---

# Cellular Backhaul for Video Surveillance and Digital Signage: Cat 6 to 5G, What Should You Pick?

**The short version: do not get excited just because it says 5G. First ask whether your device is "upload heavy" or "download heavy". A surveillance camera keeps pushing video to the cloud, so watch the uplink speed. A digital signage screen keeps pulling new clips down to play, so watch the downlink speed. If you only need to send a few 1080p streams, the cheapest Cat 6 card is already enough!**

Many project owners ask for a 5G module the moment they start planning the network for a street surveillance camera or a chain store advertising screen.
Then they spend a fortune and find out they never needed it.

Picking a modem is not like picking a sports car. Faster is not automatically better. You need the right tool for the job. This article takes the three most common Sierra Wireless M.2 modules (EM7455, EM7565 and EM9191) and shows you, using the numbers in the official spec sheets, how to choose the most cost-effective one.

> Technical data source: Sierra Wireless official specification sheets. Compiled by Yupitek.

---

## The 30 Second Guide: Which Card Should You Buy?

| Your application | Traffic focus | Which card? | Why? |
|---|---|---|---|
| **Small job: 1~4 1080p surveillance cameras** | Uplink (UL) | **EM7455 (Cat 6)** | Uplink tops out at 50 Mbps, which handles a few 1080p cameras with room to spare, and it is the cheapest. |
| **Medium to large: 5~10 1080p or 4K cameras** | Uplink (UL) | **EM7565 (Cat 12)** | Uplink jumps to 150 Mbps, leaving plenty of headroom. |
| **Digital signage updating ads** | Downlink (DL) | **EM7565 (Cat 12)** | Downlink reaches 600 Mbps, so multi-GB 4K ad files download in no time. |
| **Heavy monster: multi-channel 4K live streaming plus signage** | Both directions need speed | **EM9191 (5G)** | 5G plus LTE Cat 20 is a brute force spec. Buy it if budget is not a concern. |

---

## Why Separate Uplink and Downlink?

Because in the 4G/5G world, **downlink speed is usually 5 to 6 times the uplink speed!**

Take the entry level EM7455. The official spec lists 300 Mbps downlink but only **50 Mbps** uplink.
If you look at that 300 Mbps number and decide to run 10 4K cameras on it, you will end up questioning your life choices, because the cameras only see that thin 50 Mbps!

| Device | Its network behavior | The spec that matters |
|---|---|---|
| **Surveillance camera / NVR** | Keeps pushing video out for others to watch | **Uplink (Uplink, UL)** |
| **Digital signage** | Pulls finished videos down and plays them slowly | **Downlink (Downlink, DL)** |
| **Interactive kiosk** | Downloads videos, occasionally sends back click data | **Mostly downlink, uplink secondary** |

---

## The Math: How Much Uplink Does a Surveillance Camera Actually Need?

(Note: these are industry rule-of-thumb figures and vary with codec and scene motion)

- 1 channel of **1080p (H.264)** = roughly **2~6 Mbps**
- 1 channel of **4K (H.265)** = roughly **8~16 Mbps**

If you have 6 1080p cameras, the math is `6 cameras × 5 Mbps = 30 Mbps`.
Using the EM7455 (50 Mbps uplink) looks like it fits, right? Wrong! **In reality you will never reach the theoretical limit.** Once you factor in signal attenuation, you are already running at the edge. We recommend jumping straight to the EM7565 (150 Mbps uplink) for a stable setup.

---

## Three Generations Side by Side: EM7455 vs EM7565 vs EM9191

Here are the hardware numbers from the official spec sheets:

| Spec | EM7455 (Cat 6) | EM7565 (Cat 12) | EM9191 (5G) |
|---|---|---|---|
| **Downlink max (DL)** | 300 Mbps | 600 Mbps | Cat 20 (very fast) |
| **Uplink max (UL)** | 50 Mbps | 150 Mbps | Cat 12 class uplink |
| **Antenna ports** | 3 | 3 | 4 (connect them all) |
| **Max operating temperature** | Internal must stay under 93°C | Internal must stay under 90°C | Internal must stay under 115°C |
| **Peak current** | 1.5A | 1.5A (2.5A surge) | Spikes to 2.7A (2700mA) |

---

## Putting the Module in an Outdoor Enclosure? Watch Out for Heat!

If you install these modules inside a roadside surveillance box or a digital signage cabinet, watch out for these two monsters:

### 1. They Run Hot
All three modules hate heat. The official guidance is to keep them under 80°C~100°C. In a Taiwan summer, an outdoor metal box easily exceeds 60°C. If you do not attach heat sinks and pull the heat out, the module will throttle and eventually crash in front of you.

### 2. Give It Enough Power
The EM9191 in particular is a 5G beast. When it is hammering data, its instantaneous current draw can hit **2.7A**! If your power board is built too cheap, the voltage will sag and the module will reboot endlessly.

---

## Conclusion

Buying a modem is like renting a truck. Match the truck size to the load.

- **Budget first**: if you run 1080p surveillance cameras (4 or fewer) or text-only, simple-image signage, buy the **EM7455** with your eyes closed.
- **Best value pick**: if you have many high-res cameras or your signage frequently pulls large files, the **EM7565** with 150 Mbps uplink and 600 Mbps downlink is the current sweet spot.
- **Future-proof**: unless the client insists on 5G or you need several 4K streams live simultaneously, think twice about the hot and power-hungry **EM9191** 5G module.

---

## Quick FAQ

{{< faq >}}

---

## Ready to Buy (Call To Action)

Planning a video backhaul or digital signage connectivity project? Yupitek offers the full Sierra Wireless module lineup plus professional technical consulting to help you find the most cost-effective combination!
Email us: **sales@yupitek.com**
Browse the products: [https://yupitek.com/en/products/sierra/](/en/products/sierra/)
