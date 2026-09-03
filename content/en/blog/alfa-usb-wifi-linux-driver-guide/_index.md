---
title: "\"Choosing MediaTek vs Realtek Linux USB Network Card Drivers\""
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Hardware Guide"
description: "\"Yupitek ALFA USB网卡技术文档初版，涵盖6款型号，包括MediaTek和Realtek芯片。\""
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **Technical Support Document · Initial Version 2026-09-03 (written according to blog-writing-rules.md v1.0 specifications)**
> Subject Matter: This technical document matrix includes 6 models of Yupitek current ALFA USB network cards (3 models from MediaTek, 3 models from Realtek).
> Related Articles: [Does the ALFA Wireless Network Card Support NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/) | [Does the ALFA Wireless Network Card Support OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/) | [Does the ALFA Wireless Network Card Support NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) | [Does the ALFA Wireless Network Card Support Tomato](https://yupitek.com/zh-tw/blog/alfa-tomato-router-compatibility/) | [Does the ALFA Wireless Network Card Support DD-WRT](https://yupitek.com/zh-tw/blog/alfa-ddwrt-router-compatibility/)

## One-Liner Conclusion

**Among the 6 listed models, 3 with MediaTek chips (MT7610U / MT7612U / MT7921AUN) have built-in drivers in the modern kernel, plug and play; while 3 with Realtek chips (RTL8812AU / RTL8811CU / RTL8832BU) all require manual out-of-tree driver compilation.** If convenience is a priority, check the chip before placing an order.

---

## Act One: Scene - Why Some Can Use It Out of the Box While Others Spend Two Hours Compiling

Two Real Scenarios:

- Customer A plugs in the **AWUS036ACM** to an Ubuntu desktop, runs `lsusb`, and NetworkManager automatically recognizes wlan0 - without any software installed.
- Customer B plugs in the **AWUS036ACH** to the same machine, and the network card doesn't respond. They have to go to GitHub to pull the source code, install build tools, compile, and then reboot.

The difference isn't luck or the Linux distribution; it's about which camp the **chipset** belongs to: MediaTek's USB WiFi chipset drivers (mt76 series) have long been integrated into the Linux kernel mainline; Realtek's advanced USB WiFi chipset drivers are still distributed out-of-tree (outside the kernel), requiring manual installation from a community-maintained driver repository.

## Act II: Mechanisms — What's the Difference Between in-kernel and out-of-tree?

### MediaTek: mt76 Mainline Driver, Plug and Play

The MediaTek USB chip drivers are covered by the kernel's **mt76** subsystem:

| Model | Chipset | Kernel Driver Module | Translation-Free Conditions |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | Kernel built-in, no version threshold concerns |
| AWUS036ACM | MT7612U | mt76x2u | Kernel built-in, no version threshold concerns |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | ** Requires kernel 5.19+** |

⚠️ The only pitfall: **The kernel threshold for MT7921AUN is 5.19+. Old platforms (such as Jetson Nano's JetPack 4.x, kernel 4.9) cannot backport and are not usable directly — this is a conclusion we have verified in our Jetson Nano technical documentation (see [Does ALFA Wireless Card Support NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4)).

### Realtek: out-of-tree, all manual compilation

Realtek USB chips do not have a usable mainline driver and rely on community-maintained driver repos. The most active maintainer is **morrownr**, and this inventory covers 3 chips corresponding to 3 repos:

| Model | Chipset | Driver Repo (maintained by morrownr) | As of 2026-09-03 Verification |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ Verified |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ Verified |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ Verified |

### Applying to Three Typical Environments

| Environment | Kernel | MediaTek Camp (3 Models) | Realtek Camp (3 Models) |
|---|---|---|---|
| GB10 / DGX Spark-like Platforms | 6.x + aarch64 | All available (mt76 built-in) | All require compilation (ARM64 possible) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U available; MT7921AUN **not available** | 8812au can be compiled (ARM64 supported); others unverified |
| OpenWrt Router | Depending on Version | All available (MT7921AUN requires 23.05+) | Requires corresponding kmod or compilation, high difficulty |

(Complete judgment matrices for each environment can be found in [Does ALFA Wireless Card Support NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/), [Does ALFA Wireless Card Support NVIDIA Jetson Nano](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/), [Does ALFA Wireless Card Support OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/).)

## Act 3: Toolbox - Three-Minute Decision Process and Installation Steps

### Decision Table: First Three Steps to Take When You Get the Network Card

```bash
# Step 1: Confirm the system recognizes the network card (note VID:PID)
lsusb

# Step 2: Check if the corresponding driver has been loaded into the kernel
lsmod | grep -E "mt76|rtl8"

# Step 3: Confirm the kernel version (determine if MT7921AUN can be used)
uname -r
```

Decision Logic (Parent: Table 6 Models Above):

1. `lsusb` shows **MediaTek / MT76xx** → in-kernel camp, kernel ≥ 5.19 (MT7921AUN models) or any recent kernel, plug and play.
2. `lsusb` shows **Realtek RTL88xx** → out-of-tree camp, follow the installation steps below.
3. `lsusb` **completely** does not show any new devices → first change USB port/cable to rule out hardware issues, then confirm if the model is a Wi-Fi 6 RTL8832BU (some batches require `usb_modeswitch`, this step is an individual model issue and is not within the scope of this overview, will not be expanded upon).

### Universal Installation for Realtek Camp (Exampled with AWUS036ACH)

```bash
# Step 1: Install build dependencies (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# Step 2: Obtain the driver source code (model-specific repo see table above)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# Step 3: Install (DKMS register, no need to reinstall when changing kernel)
sudo ./install-driver.sh

# Step 4: Verify after reboot
lsmod | grep 88XXau
ip link   # Should show a new wlan interface
```

> **Table 1 Conclusion: Decision Before Installation - First look at the chip set, 90 seconds to decide if you are "plug and play" or "compile from repo", no need to hit a wall first.**

### Purchase Recommendations (Conclusion)

- **No Compilation Needed**: Choose MediaTek camp (AWUS036ACHM / ACM / AXML), recent kernels all plug and play.
- **Need Wi-Fi 6 and No Compilation**: Choose AWUS036AXML (MT7921AUN), but first confirm kernel ≥ 5.19.
- **Have Special Requirements and Realtek is a Must** (such as specific monitor mode toolchains): Reserve 20-40 minutes for driver compilation and confirm that the target platform has kernel headers.

## Known Limitations and Counterconditions

The conclusions of this article are not valid under the following conditions, please adopt alternative solutions:

1. **Kernel 5.19 and Below + MT7921AUN**: The mt7921u driver cannot be backported (depends on modern kernel infrastructure), and the conclusion is reversed to "not available". This is the most important exception in this article.
2. **Non-x86/ARM64 Linux** (such as some MIPS routers): The morrownr repository is not guaranteed to be compilable, and the kmod from OpenWrt should be prioritized (see [Does ALFA Wireless Card Support OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)).
3. **Driver Repository Version Evolution**: The morrownr repository is named by date (e.g., rtl8852bu-20250826), and future versions may be updated or removed; please ensure the repository status before installation.
4. **Monitor Mode / AP Mode Capabilities**: Different kernel versions of the same chip have different capabilities (for example, the rtl8812au-ct in OpenWrt 22.03+ has crash reports in 24.10), and the detailed capability matrix should be referred to in specialized articles for each environment.
5. **RTL8832BU (AWUS036AX/AXER) is not included in the 6 models listed in this article, but customer service is often asked about it**: The driver maintainer morrownr has publicly stated that the chip series "is a very bad driver, suspecting there are problems with the chip itself", and it is recommended that Linux users avoid it at this stage, not just because of the difficulty of compiling. When responding to customers, it should be explained truthfully.

## Reference Sources

| Source | Description | URL | Verification Status | Verification Date |
|---|---|---|---|---|
| morrownr/8812au GitHub | RTL8812AU Linux Driver | https://github.com/morrownr/8812au-20210820 | ✅ Verified | 2026-09-03 |
| morrownr/8821cu GitHub | RTL8811CU Linux Driver | https://github.com/morrownr/8821cu-20210916 | ✅ Verified | 2026-09-03 |
| morrownr/rtl8852bu GitHub | RTL8832BU Linux Driver | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verified | 2026-09-03 |
| Yupitek ALFA Product Overview | Current Models and Specifications | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verified | 2026-09-03 |
| Yupitek Blog: Soft AP Guide | AP Mode Implementation Verification Articles | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verified | 2026-09-03 |
| This Site Technical Documents 9 Articles | Determinant Matrices and Environmental Verification Basics | Relative Links (see "Related Articles" at the top of the article) | ✅ Verified | 2026-09-03 |

> Official kernel mt76 wiki page: https://wireless.wiki.kernel.org/en/users/drivers/mediatek (Verified, lists the starting kernel version supported by each chip, which can be used as a quick reference)

## Disclaimer

This document is compiled by Yupitek Ltd's Technical Support, and the specifications and driver status may vary with updates to the kernel and driver repositories. Please refer to the official repositories and the manufacturer's specifications page before installation. ALFA Network is an authorized agent brand for our company.
