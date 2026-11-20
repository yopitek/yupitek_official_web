---
title: "2026 最完整实测：9 款 ALFA 无线网卡在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP 全矩阵"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "实测 9 款 ALFA Wi-Fi USB 网卡在 Ubuntu 24.04 ARM64（GX10）的 Monitor、Injection、AP 与 WPA3-SAE 表现，含 Kali 常用工具兼容性与选型建议，AWUS036ACH / EACS 注入达 100%。"
faq:
  - question: "AWUS036AXM 在 Ubuntu 能注入（injection）吗？"
    answer: "在本平台不能。实测中 AWUS036AXM 与 AWUS036AXML（皆为 MT7921 芯片）在 2.4GHz 与 5GHz 的 injection 皆失败，主因是 stock kernel 6.16+ 的 mac80211 chanctx 回归（非芯片先天），因此不建议在本平台用于需要注入或 handshake 截取的用途。"
  - question: "哪一款 ALFA 网卡在 Ubuntu 上 injection 成功率最高？"
    answer: "实测中 AWUS036ACH 与 AWUS036EACS 在 2.4GHz 与 5GHz 的 injection 成功率皆达 100%，是本批 9 款中表现最好的两款。"
  - question: "9 款 ALFA 网卡在 Ubuntu 24.04 需要另外装驱动吗？"
    answer: "不需要。9 款在 kernel 6.17 上全部走 kernel 内置（in-kernel）驱动（rtw88 / rtw89 / mt76 家族），插上即被辨识，不需编译 DKMS 模块。"
  - question: "ALFA 网卡在 Ubuntu 可以架 WPA3-SAE 的热点吗？"
    answer: "可以，9 款实测都能成功架设 WPA3-SAE 热点并让设备连入（除 ACS 于 5 GHz 实测外，其余皆于 2.4 GHz 实测；AXML 另于 6 GHz 实测）；唯 AWUS036ACHM 需把 hostapd 的 sae_pwe 设为 0，否则旧款 iPhone 7 Plus 会连接失败。"
  - question: "这份 Ubuntu 的测试结果，Kali Linux 用户可以参考吗？"
    answer: "Kali Linux 基于 Debian/Ubuntu 体系，使用同一套 rtw88 / rtw89 / mt76 in-kernel 驱动，因此本文的驱动兼容性与能力矩阵原则上可作为 Kali 用户的参考依据；但本文实测平台为 Ubuntu 24.04，尚未在 Kali 上正式复测，结果请以日后复测为准。"
draft: false
---

## 重点摘要（TL;DR）

Yopitek（ALFA Network 台湾经销）在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）实测 9 款 ALFA USB 无线网卡：9 款都能进 monitor mode 并作为 AP，AWUS036ACH 与 AWUS036EACS 两频注入达 100%，MT7921 的 AWUS036AXM / AWUS036AXML 在本平台注入失败。

- **Monitor 全员可用**：9 款都能进 monitor mode，差别只在收讯强弱。
- **Injection 是分水岭**：Realtek `rtw88` 的 ACH、EACS 两频注入达 100%，ACS 次之；MT7921 的 AXM / AXML 在本平台注入失败。
- **端到端 handshake（截取 → 转出 `.22000`）已实证 9 款中的 7 款**：ACM、ACHM、ACH、ACS、EACS、AX、AXER。
- **AP 与 WPA3-SAE 几乎全员过关**：仅 AWUS036ACHM 需设 `sae_pwe=0` 以兼容旧款 iPhone。
- **ARM64 免编译**：9 款全走 kernel 6.17 内置驱动，插上即用、免 DKMS。

Yopitek 是 ALFA Network 的台湾经销商。客户选购 USB 无线网卡时，最常问的三个问题几乎都一样：「这张卡在我的 Linux 环境能不能进 monitor mode？能不能做 injection？能不能架 AP？」与其凭规格表回答，我们直接把 9 款现役 ALFA 网卡搬上自家实验桌，在 **ASUS GX10（ARM64）** 搭配 **Ubuntu 24.04 LTS** 的环境逐张实测，把 Monitor、Injection、AP、WPA3-SAE 四条能力线一次拉出来比较，并且诚实标注哪几张「在这个平台做不到什么」。

需要先讲清楚定位：本文所有测试都在 Yopitek 自有的设备与自有办公室 Wi-Fi 上完成，对象是我们自己的测试手机。这是经销商对产品兼容性与能力边界的硬件验证，不是针对第三方网络的攻击教学。文中不提供任何对外部网络的操作步骤；injection 与 handshake 相关能力，一律在自有封闭环境、对自有设备量测。

这是一篇总表型的 Hub 文章。每一张卡的逐步设置与完整证据，会另外拆成单卡深入文（见文末延伸阅读）。

## 测试平台与方法

- **运算平台**：ASUS GX10（ARM64 / aarch64）
- **操作系统**：Ubuntu 24.04 LTS
- **内核版本**：kernel 6.17.0-1014-nvidia
- **驱动策略**：9 款全部使用 kernel 内置（in-kernel）驱动，插上即辨识，不安装任何第三方 DKMS 模块
- **测试设备**：Apple iPhone 7 Plus（WPA3-SAE 兼容性另以 iPhone 15 Pro 复测）
- **测试环境**：自有办公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36、ch157
- **测试期间**：2026-11-16 至 2026-11-18 实机量测

方法上，我们对每张卡都跑同一组流程：先确认驱动加载与接口生成（`wlx*`），再依序验证 2.4GHz / 5GHz 的 monitor、injection、AP 与 WPA3-SAE 连接，最后对自有测试手机做端到端 handshake 截取链路的验收。每一项结果都以实际量到的数字或状态记录，不以规格书推测。

本文表格采用以下图例：

> ✅ 通过 ｜ 🟡 部分或单机可成立 ｜ ⚠️ 有限制 ｜ ❌ 不支持或测试失败 ｜ N/A 驱动不具此模式 ｜ ⬜ 未测（缺第二台设备）

## 一、硬件与驱动对照

先看 9 款的硬件底细与在 kernel 6.17 上实际挂载的驱动。

| # | 型号 | 芯片 | USB ID | 驱动（in-kernel） | 固件 | 世代 / 串流 | 备注 |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | morrownr 推荐 Kali 卡 |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R（AC600） | 单天线 |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R（AC1200） | 双天线高增益 |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | 轻量随身 |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | BT + WiFi 复合 |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | 同芯片，内嵌天线（Nano） |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

几个重点：

**两大驱动阵营。** 9 款分属 MediaTek（`mt76x2u` / `mt76x0u` / `mt7921u`）与 Realtek（`rtw88_*` / `rtw89_8852bu`）两套 in-kernel 驱动。芯片世代涵盖 Wi-Fi 5（6 款）与 Wi-Fi 6（3 款：AX、AXER 走 `rtw89_8852bu`；AXM、AXML 走 `mt7921u`）。

**ARM64 上最实际的优势是「免编译」。** 这 9 款在 kernel 6.17 全走 in-kernel 驱动，插上即被辨识，不需要在 aarch64 上处理 out-of-tree DKMS 模块。这点在 ARM64 上特别有感：许多第三方 Realtek 驱动缺 aarch64 的 prebuilt，往往得自源代码编译、对核版，踩雷概率高。这批卡直接免除这段流程。

**同芯片不同型号。** AWUS036AX 与 AWUS036AXER 是同一颗 RTL8832BU、同一支 `rtw89_8852bu` 驱动，差别在天线设计（AXER 采内嵌天线 Nano 设计，无 RP-SMA），这会反映在后面的收讯与注入数字上。

**两款是 BT + WiFi 复合设备。** AWUS036EACS（RTL8821CU）与 AWUS036AXML（MT7921AUN）同时带蓝牙，这个特性在重插卡时有个实务副作用，后面「平台注意事项」会说明。

## 二、内核能力矩阵：Monitor / Injection / AP / WPA3

这是本文的主表，也是选型时最该先看的一张。

| # | 型号 | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ 仅广播 | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅（频宽未确认） | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 6 | AWUS036AX | ✅ 强 | ✅ 强 | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ 强 | ✅ 强 | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ 弱 | ✅ 弱 | ❌ **失败** | ❌ **失败** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ 弱 | ✅ 弱 | ❌ **失败** | ❌ **失败** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* AWUS036ACHM 的 WPA3 需设 `sae_pwe=0`；在 `sae_pwe=2` 时 iPhone 7 Plus 连不上。
>
> WPA3-SAE 栏：所示频段为实际测过的频段（除 ACS 于 5G 实测外，其余皆为 2.4G；AXML 另于 6G 实测），其他频段未实测。

逐项解读：

**Monitor：9 款全数可用，差在收讯强弱。** 不论 2.4GHz 或 5GHz，9 款都能进 monitor mode，没有例外。差别在扫描的积极度与收讯灵敏度：Wi-Fi 6 的 AX / AXER 收讯最强、扫描最积极；MT7921 的 AXM / AXML 可进 monitor，但相对弱。只需要被动侧录或频谱盘点的话，9 款都能用。

**Injection：差距从这里开始拉开。** Realtek `rtw88` 系列表现最好：ACH 与 EACS 在 2.4GHz / 5GHz 都达 **100%**，ACS 也有 2.4GHz 100% / 5GHz 96%。MediaTek `mt76` 的 ACM 可用但数字落在中段（2.4GHz 63–83%、5GHz 76%）；ACHM 的 5GHz 只能广播、无法对特定目标注入。`rtw89` 的 AX / AXER 可注入，其中 AXER 的 2.4GHz 注入率（73%）比 AX（96%）低一截。

**最重要的诚实限制：MT7921（AXM / AXML）injection 在本平台失败。** 这不是参数没调好，也不是芯片先天不能注入——主因是 kernel 6.16+ 的 mac80211 chanctx 回归；社区同型号改用 git／patched 驱动虽可运作，但 firmware 会锁速率（对应 morrownr/USB-WiFi #387、morrownr/mt76 #18）。在本平台因注入失败，这两款无法 deauth，也就无法走完 handshake 截取链路。需要 injection 的用途，这两张在本平台请直接排除。

**AP 与 WPA3：几乎全数过关。** 9 款都能当 AP，多数支持 5GHz VHT80（80MHz）；WPA3-SAE 连接在已测频段也全数可成立（见表下说明）。唯一要注意的是 AWUS036ACHM，WPA3 需把 hostapd 的 `sae_pwe` 设为 0，否则旧款 iPhone 7 Plus 会连不上（以 iPhone 15 Pro 复测可连，属兼容性设置差异）。

## 三、高级功能与 handshake 能力摘要

把范围再拉深一层，看 handshake 端到端、虚拟接口（VIF）、active monitor 与 mesh / IBSS。

| # | 型号 | WPA handshake 截取 | VIF | Active monitor | Ad-hoc（IBSS） | Mesh（802.11s） |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **端到端**（.22000） | ✅ STA+AP / AP+mon | 🟡 可设置，ACK 未验 | 🟡 单机 | 🟡 单机 |
| 2 | AWUS036ACHM | ✅ **端到端**（.22000，于 5 GHz ch36） | ✅ | 🟡 | 🟡 单机 | 🟡 单机 |
| 3 | AWUS036ACH | ✅ **端到端**（.22000） | ✅ STA+mon | ❌ -95 | 🟡 单机 | ❌ -95 |
| 4 | AWUS036ACS | ✅ **端到端**（.22000） | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **端到端**（.22000，79 ACKs） | 🟡 被动 monitor + managed 同频道并存（software monitor）；不支持独立双 VIF | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **端到端**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **端到端**（.22000） | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ 注入失败 | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ 注入失败 | ✅ | 🟡 | N/A | N/A |

这里的「端到端」有明确定义：用该卡对 **Yopitek 自有的 iPhone 7 Plus**（连在自家 `YUPITEK` SSID 上）运行 injection，截取完整的 4-way handshake（M1–M4），再用 `hcxpcapngtool --all` 转成 hashcat 的 `.22000` 格式。整条链路能不能跑通，才是「渗透测试能力」的验收点，不是「能进 monitor」就算。

- **端到端通过（9 款中的 7 款）**：ACM、ACHM、ACH、ACS、EACS、AX、AXER 都能产出 `.22000`，其中 EACS 收到 79 个 ACK，信号回馈最扎实；ACH 两频注入 100%，已于 2026-11-19 补测转出 47 行 hashline 的 `.22000`。ACHM 在 5GHz（ch36）完成；ACM 虽注入成功率较低，仍完成端到端。
- **端到端断链**：AXM / AXML 因 injection 失败，整条 handshake 跟着断。这再次印证：MT7921 在本平台不适合渗透测试用途。
- **VIF（虚拟接口并存）**：9 款都支持某种形式的多接口并存；Realtek rtw89 可同时跑 STA + AP，而 EACS 仅支持被动 monitor 与 managed 同频道并存（software monitor），不支持独立双 VIF。
- **Active monitor（带 ACK 回报）**：`rtw88` 的 ACH / ACS / EACS 回报 -95（不支持）；`rtw89` 的 AX / AXER 驱动不具此模式（N/A）；`mt76` / `mt7921u` 为部分可（🟡）。
- **Mesh（802.11s）**：只有 `mt76` 的 ACM / ACHM 能在单机创建（🟡，需第二台卡才能完整互连验证）；Realtek `rtw88` 回 -95 不支持、`rtw89` 与 `mt7921u` 的驱动不具此模式。做 mesh 实验，MediaTek `mt76` 是这批里唯一的选项。
- **IBSS（Ad-hoc）**：`mt76` 的 ACM / ACHM 与 `rtw88` 的 ACH 均可单机 join（🟡）；EACS 虽列出 iftype 但实测 join 无效，`rtw89` 的 AX / AXER 则无 IBSS iftype（N/A）。

### Kali / aircrack 工具层级兼容性（平台共通）

以下工具在 9 款上属平台层级表现，与个别卡无关：

| 工具 | 状态 | 说明 |
|---|---|---|
| airmon-ng | ✅ | 全卡可侦测 / 管理；**严禁 `check kill`**（会关掉 NetworkManager 使 GX10 断网） |
| kismet | ✅ | 各卡可当 data source 启动并产出 `.kismet` log |
| bettercap | ✅ | `wifi.recon` 与 channel hopper 正常 |
| wifite（git 3.0.0） | ✅ | 可扫描建目标清单（须用 git 版，apt 版与自编 aircrack-ng 冲突） |
| Wireshark / tshark | ✅ | monitor 截取与解析正常 |
| **hcxdumptool 8.x** | ⚠️ | **全卡 failed to arm，唯 EACS 在 2.4 GHz 可 arm（5 GHz 失败）**：需要 active-monitor，而 `rtw88` / `rtw89` / `mt7921u` 皆不支持 → 改用 `airodump-ng` + `aireplay-ng` |

ARM64 补充：`aircrack-ng` 需自源代码编译，`wifite` 建议用 git 3.0.0 版，以绕开 apt 套件与自编版本之间的依赖冲突。

## 四、依用途选型建议

把上面三张表收敛成「照用途直接选」。

| 用途 | 首选 | 说明 |
|---|---|---|
| **渗透测试（injection + handshake）** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | 两频注入最佳（EACS、ACH 达 100%）；端到端 `.22000` 以 EACS、ACS、ACH 佐证（ACH 于 2026-11-19 补测） |
| **最强接收 / 长距离 monitor** | **AWUS036AXER** / AWUS036ACH | AXER 跳频一次扫到 63 个 AP + 12 个 client；ACH 双天线高增益 |
| **Wi-Fi 6 + AP 热点** | AWUS036AX / AWUS036AXER | 2x2 VHT80，AP 稳定且注入可用 |
| **纯 AP / 一般连接（不需注入）** | AWUS036AXM / AWUS036AXML | MediaTek 连接稳定，但**注入失败**，不适合渗透用途 |
| **mesh / IBSS 实验** | AWUS036ACM / AWUS036ACHM | `mt76` 驱动单机可创建 mesh 与 IBSS（`rtw88` 的 ACH 仅 IBSS 单机可 join、不支持 mesh；`rtw89` 两者皆未声明） |

几句白话总结：

- **要做渗透测试、要截取 handshake**：端到端 `.22000` 已落档实证的共 9 款中的 7 款——**AWUS036EACS**（最扎实，79 ACKs）、**AWUS036ACS**，Wi-Fi 6 的 AWUS036AX / AWUS036AXER，**AWUS036ACM** 与 **AWUS036ACHM**（5GHz），以及 **AWUS036ACH**（两频注入 100%，于 2026-11-19 补测转出 47 行 hashline 的 `.22000`）。
- **要最远的接收距离、最广的侧录**：AWUS036AXER（Wi-Fi 6，内嵌天线 Nano 设计＋芯片调校，跳频扫描最积极）或双天线高增益的 AWUS036ACH。
- **要架 Wi-Fi 6 热点**：AWUS036AX / AWUS036AXER，2x2 VHT80 且同时支持注入。
- **只要稳定连接 / 单纯当 AP**：AWUS036AXM / AWUS036AXML 的 MediaTek 方案连接稳定，日常使用没问题。
- **要玩 mesh**：这批里只有 `mt76` 的 AWUS036ACM / AWUS036ACHM 做得到（IBSS 单机另有 `rtw88` 的 AWUS036ACH 可 join）。

**避雷（最重要的一条）**：如果你的用途是 **injection 或 handshake**，**请勿选 AWUS036AXM / AWUS036AXML**。MT7921 在 ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）这个平台上注入失败，主因是 kernel 6.16+ 的 mac80211 chanctx 回归（非芯片先天），不是设置问题；社区同型号改用 git／patched 驱动虽可运作，但 firmware 会锁速率，本平台 stock kernel 下仍无法注入。把它们留给「纯连接 / 纯 AP」的场景即可。

## 五、平台注意事项（GX10 ARM64 实务）

这些是在 ASUS GX10 + Ubuntu 24.04（ARM64）上操作这批卡时，9 款共通的实务要点：

1. **别切断自己的网络**：绝对不要运行 `airmon-ng check kill`，它会关掉 NetworkManager 导致整台 GX10 断网。操作时只动外置的 `wlx*` 接口，不要碰内置的对外上网主线。
2. **RX stall 排除**：反复切换 monitor / AP 之后，若突然扫不到任何东西，通常是 RX stall，把卡拔插一次即可复原（USB 重新枚举，接口名以 MAC 命名、不会改变）。
3. **BT + WiFi 复合设备**：EACS 与 AXML 同时带蓝牙，重插时偶尔会卡在 WiFi probe、生不出 `wlx` 接口；换一个 USB 孔通常就能解决。
4. **5GHz 的 TX 解锁**：在自有环境做 5GHz injection 前，需先设置正确的法规网域（regulatory domain）以解锁 TX 功率，测试结束后再设回在地网域。这是 5GHz 能否正常发射的前提。
5. **handshake 截取的小技巧**：办公室内常有多台同名 AP，实务上不锁定单一 BSSID、改截取整个频道较稳，转档时用 `hcxpcapngtool --all`。
6. **hcxdumptool 全平台 failed to arm（例外：EACS 在 2.4 GHz）**：三频内置卡与上述驱动都不支持 active-monitor，直接改用 aircrack-ng 套件（`airodump-ng` + `aireplay-ng`）。
7. **ARM64 的编译细节**：`aircrack-ng` 需自源代码编译，`wifite` 用 git 版绕过 apt 依赖冲突。

再次强调定位：上述 injection / deauth / handshake 的能力，全部在 Yopitek 自有封闭环境、对自有测试设备量测，用途是验证产品能力与兼容性边界。本文不提供、也不建议对任何第三方网络进行上述操作。

## 小结

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）这个平台上，9 款 ALFA 卡的总评可以浓缩成三句话：**Monitor 全员可用、AP 与 WPA3 几乎全员过关、分水岭在 Injection。** 需要注入与 handshake 的专业用途，Realtek `rtw88` 的 EACS / ACH / ACS 是最稳的选择；要收讯与 Wi-Fi 6，看 AXER / AX；MT7921 的 AXM / AXML 留给纯连接场景。全数免编译、插上即用，是这批卡在 ARM64 上最大的共同优点。

## 常见问题（FAQ）

**Q：AWUS036AXM 在 Ubuntu 能注入（injection）吗？**
A：在本平台不能。实测中 AWUS036AXM 与 AWUS036AXML（皆为 MT7921 芯片）在 2.4GHz 与 5GHz 的 injection 皆失败，主因是 stock kernel 6.16+ 的 mac80211 chanctx 回归（非芯片先天），因此不建议在本平台用于需要注入或 handshake 截取的用途。

**Q：哪一款 ALFA 网卡在 Ubuntu 上 injection 成功率最高？**
A：实测中 AWUS036ACH 与 AWUS036EACS 在 2.4GHz 与 5GHz 的 injection 成功率皆达 100%，是本批 9 款中表现最好的两款。

**Q：9 款 ALFA 网卡在 Ubuntu 24.04 需要另外装驱动吗？**
A：不需要。9 款在 kernel 6.17 上全部走 kernel 内置（in-kernel）驱动（rtw88 / rtw89 / mt76 家族），插上即被辨识，不需编译 DKMS 模块。

**Q：ALFA 网卡在 Ubuntu 可以架 WPA3-SAE 的热点吗？**
A：可以，9 款实测都能成功架设 WPA3-SAE 热点并让设备连入（除 ACS 于 5 GHz 实测外，其余皆于 2.4 GHz 实测；AXML 另于 6 GHz 实测）；唯 AWUS036ACHM 需把 hostapd 的 `sae_pwe` 设为 0，否则旧款 iPhone 7 Plus 会连接失败。

**Q：这份 Ubuntu 的测试结果，Kali Linux 用户可以参考吗？**
A：Kali Linux 基于 Debian/Ubuntu 体系，使用同一套 rtw88 / rtw89 / mt76 in-kernel 驱动，因此本文的驱动兼容性与能力矩阵原则上可作为 Kali 用户的参考依据；但本文实测平台为 Ubuntu 24.04，尚未在 Kali 上正式复测，结果请以日后复测为准。

## 延伸阅读

本文为总表 Hub。以下深入文与逐卡实测陆续上线（链接施工中）：

- 《免装驱动：在 Ubuntu（ARM64）上激活 Monitor 与 AP 模式》 → [`/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE handshake 截取实务（自有环境验证）》 → [`/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 篇逐卡深入实测：

- [AWUS036ACM 单卡实测](/zh-cn/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM 单卡实测](/zh-cn/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH 单卡实测](/zh-cn/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS 单卡实测](/zh-cn/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS 单卡实测](/zh-cn/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX 单卡实测](/zh-cn/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER 单卡实测](/zh-cn/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM 单卡实测](/zh-cn/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML 单卡实测](/zh-cn/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*测试单位：Yopitek（ALFA Network 台湾经销）｜ 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）｜ 测试环境：自有办公室 Wi-Fi。本文为产品兼容性与能力验证，非针对第三方网络之操作教学。*
