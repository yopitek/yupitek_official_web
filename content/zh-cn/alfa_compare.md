---
title: "ALFA Network 无线网卡完整对比"
description: "ALFA Network 9 款 USB 无线网卡完整规格对比：芯片、Linux 驱动、Monitor／Injection／AP 能力，含 ASUS GX10（Ubuntu 24.04 ARM64、kernel 6.17）实测结果。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
showTableOfContents: true
---

下表汇总了 ALFA Network 9 款 USB 无线网卡的完整规格。Monitor、Injection、AP 以及端到端 handshake 各栏均为 Yopitek 在 ASUS GX10（Ubuntu 24.04 LTS / ARM64 / kernel 6.17）上，使用自有设备和自有办公室 Wi-Fi 得出的实测结果，并非照抄规格书。

## 完整规格对比

手机上请左右滑动表格；点击型号可前往产品页。

| 型号 | Wi-Fi 世代 | 芯片 | 频段 | 最高速率 | USB 接口 | 天线 | MIMO | Monitor 模式 | 数据包注入 | 端到端 handshake（GX10 实测） | Linux 驱动 | 驱动类型 | AP 模式 | 最大功耗 | 蓝牙 | 适用场景 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AWUS036AXML](/zh-cn/products/alfa/awus036axml/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz | 3000 Mbps | USB-C 3.2 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支持 | ❌ 原生 6.17 内核下失败 | ❌ 否（注入失败） | 内核内置 ≥5.18 | 内核内置（免安装） | ✅ 原生支持 | 3.6W | BT 5.2 | Wi-Fi 6E＋Linux＋USB-C |
| [AWUS036AXM](/zh-cn/products/alfa/awus036axm/) | WiFi 6E | MT7921AUN | 2.4 + 5 + 6 GHz（6 GHz 未测试） | 3000 Mbps | USB-A 3.2 L | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支持 | ❌ 原生 6.17 内核下失败 | ❌ 否（注入失败） | 内核内置 ≥5.18 | 内核内置（免安装） | ✅ 原生支持 | 3.6W | BT 5.2 | Wi-Fi 6E＋双天线 |
| [AWUS036AX](/zh-cn/products/alfa/awus036ax/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1200 Mbps | USB-A 3.2 Gen 1 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支持 | ✅ 支持 | ✅ 端到端（.22000） | 内核内置 ≥6.17 | 内核内置（免安装） | ✅ 原生支持 | 3.6W | — | Wi-Fi 6＋AP 热点 |
| [AWUS036AXER](/zh-cn/products/alfa/awus036axer/) | WiFi 6 | RTL8832BU | 2.4 + 5 GHz | 1800 Mbps | USB-A 3.2 | 内置（nano） | 2×2 MIMO | ✅ 支持 | ✅ 支持 | ✅ 端到端（.22000） | 内核内置 ≥6.17 | 内核内置（免安装） | ✅ 原生支持 | 3.0W | — | 小巧便携型 |
| [AWUS036ACH](/zh-cn/products/alfa/awus036ach/) | WiFi 5 | RTL8812AU | 2.4 + 5 GHz | 867 Mbps | USB-C 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅✅ 最佳 | ✅✅ 最佳 | ✅ 端到端（.22000） | 内核内置 ≥6.13 | 内核内置（免安装） | ✅ 原生支持 | 3.6W | — | Kali Linux 首选 |
| [AWUS036ACM](/zh-cn/products/alfa/awus036acm/) | WiFi 5 | MT7612U | 2.4 + 5 GHz | 867 Mbps | USB-A 3.0 | 2× RP-SMA 5dBi | 2×2 MIMO | ✅ 支持 | ✅ 支持 | ✅ 端到端（.22000） | 内核内置 ≥4.19 | 内核内置（免安装） | ✅ 原生支持 | 3.0W | — | Linux 免驱动 |
| [AWUS036ACHM](/zh-cn/products/alfa/awus036achm/) | WiFi 5 | MT7610U | 2.4 + 5 GHz | 433 Mbps | USB 2.0 | 1× RP-SMA 5dBi | 1×1 SISO | ✅ 支持 | ✅ 2.4 GHz／⚠️ 5 GHz 仅广播 | ✅ 端到端（.22000） | 内核内置 ≥4.19 | 内核内置（免安装） | ✅ 原生支持 | — | — | 小巧 AC600，Linux 免驱动 |
| [AWUS036ACS](/zh-cn/products/alfa/awus036acs/) | WiFi 5 | RTL8811AU | 2.4 + 5 GHz | 433 Mbps | USB-A 2.0 | 1× RP-SMA 2dBi | 1×1 SISO | ✅ 支持 | ✅ 支持 | ✅ 端到端（.22000） | 内核内置 ≥6.13 | 内核内置（免安装） | ✅ 原生支持（5 GHz 以 802.11a 20 MHz 测试；未测试 VHT80） | 2.5W | — | 高性价比安全测试 |
| [AWUS036EACS](/zh-cn/products/alfa/awus036eacs/) | WiFi 5 | RTL8821CU | 2.4 + 5 GHz | 433 Mbps | USB 2.0 nano | 内置 2dBi | 1×1 SISO | ✅ 支持 | ✅✅ 最佳 | ✅ 端到端（.22000） | 内核内置 ≥6.2 | 内核内置（免安装） | ✅ 原生支持（5 GHz 以 802.11a 20 MHz 测试；未测试 VHT80） | 2.5W | BT 4.2 | Windows 家用 Wi-Fi＋蓝牙 |

## 按用途快速选型

**🔴 Kali Linux / 渗透测试** — 推荐: AWUS036ACH

RTL8812AU — 在 Kali 上 monitor 模式与数据包注入最为成熟；在 GX10（kernel 6.17）上双频段注入成功率均为 100%。内核内置 rtw88_8812au 驱动自 6.13 起提供。提示：较旧内核请使用固定在稳定 commit 63cf0b4 的 aircrack-ng DKMS 驱动。

**🔵 WiFi 6E（三频）进阶用户** — 推荐: AWUS036AXML or AWUS036AXM

MT7921AUN — Linux 内核内置驱动自 5.18 起提供，支持 6 GHz 频段（已在 AXML 上验证；AXM 未测试），蓝牙 5.2。注意：在原生 kernel 6.17 上数据包注入失败（自 6.16 起的 mac80211 回归），因此不适合用于渗透测试。外形差异：AXML 采用可拆卸 USB-C 接头，单天线机身带双输出；AXM 采用内置 L 型 USB-A 外形。

**🌐 Soft-AP / 热点模拟** — 推荐: AWUS036ACM

MT7612U — 通过 Linux 内核原生 hostapd 即插即用支持 AP 模式。与需要自行编译、问题较多的 hostapd 版本的 Realtek 网卡不同，MediaTek 方案顺畅稳定，适合 Rogue AP / Evil Twin 模拟。

**🟢 Linux 日常使用（免驱动）** — 推荐: AWUS036ACM

MT7612U — 内核 4.19 起内置，在 Ubuntu / Debian / Fedora 上无需任何驱动设置。Linux 使用体验最省心。

**🟣 Raspberry Pi / 嵌入式** — 推荐: AWUS036ACM

低功耗加上内核内置驱动，非常适合 Raspberry Pi。注意：大功率型号（ACH、AXML）最高会消耗 3.6W，需搭配带外接供电的 USB hub，以免 Pi 出现电压下降和连接重置。

**🟡 高性价比 / 入门安全测试** — 推荐: AWUS036ACS

RTL8811AU — 入门级的实惠之选，支持 monitor 模式与数据包注入。单天线，机身小巧。

**⚡ 小巧便携型** — 推荐: AWUS036AXER

超薄纳米机身，仅 10.5g。WiFi 6（1800 Mbps），USB-A。适合商务出差，以 Windows 使用为主。

**🏠 Windows 家庭用户＋蓝牙** — 推荐: AWUS036EACS

RTL8821CU — WiFi 5 与蓝牙 4.2 二合一双模。纳米外形。适合没有 PCIe 插槽、需要快速添加无线与蓝牙的台式机。

**🍎 macOS 兼容性** — 推荐: AWUS036ACH or AWUS036AXML

ACH 通过第三方驱动对 macOS 支持良好。AXML 的 MT7921AUN 有社区提供的 macOS 支持。请务必确认 macOS 版本兼容性。Intel Mac 的驱动历史支持比 M 系列更完善。

## 按平台／操作系统快速选型

| 平台／操作系统 | 首选 | 次选 | 说明 |
|---|---|---|---|
| 🐧 Kali Linux | AWUS036ACH | AWUS036ACM | ACH = monitor 模式表现最佳；ACM = 内核支持最容易。虚拟机使用时：请将虚拟机配置为 USB 3.0（xHCI）控制器，以防掉线。 |
| 🐧 Ubuntu / Debian | AWUS036ACM | AWUS036AXML | MT7612U 自 4.19 起内核内置；MT7921AUN 自 5.18 起内置 |
| 🐧 Raspberry Pi OS | AWUS036ACM | AWUS036ACH | 低功耗加内核内置驱动，无需手动编译。大功率网卡建议搭配带外接供电的 USB hub，以避免重置。 |
| 🪟 Windows 10 / 11 | AWUS036AX | AWUS036EACS | WiFi 6 性能；EACS 另带蓝牙二合一 |
| 🍎 macOS | AWUS036ACH | AWUS036AXML | 有第三方驱动可用，请确认 macOS 版本。Intel Mac 有历史驱动；Apple Silicon（M1/M2/M3）仅有受限的实验性支持。 |
| 📱 Android / NetHunter | AWUS036ACH | AWUS036ACS | RTL8812AU 与 RTL8811AU 支持 NetHunter；需要 OTG 转接器并自行编译内核。 |

---

实测平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia（2026-11）。各网卡的完整报告请见[博客](/zh-cn/blog/)。
