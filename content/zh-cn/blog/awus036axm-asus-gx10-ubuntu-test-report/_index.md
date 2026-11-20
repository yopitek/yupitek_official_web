---
title: "AWUS036AXM 单卡实测：MediaTek MT7921AU（Wi-Fi 6 2x2）在 ASUS GX10 + Ubuntu 24.04（ARM64）的 Monitor・AP・WPA3 能力与 Injection 限制"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM（mt7921u）在 ASUS GX10／Ubuntu 24.04 ARM64 实测：monitor、AP、WPA3 可用，但 packet injection 失败，不适合渗透测试，定位纯 AP 与连接。"
faq:
  - question: "AWUS036AXM 能做数据包注入（packet injection）吗？"
    answer: "在我们的测试平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。aireplay-ng --test 在 2.4 GHz 与 5 GHz 都回报 No Answer、Found 0 APs，因此也无法 deauth 或截取 WPA handshake。根因是 kernel 6.16+ 的 mac80211 chanctx 回归，并非芯片先天不能注入；同系列的 AWUS036AXML 结果相同。需要注入请改选实测可用的 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXM 适合拿来做渗透测试或 Kali 吗？"
    answer: "不建议。monitor 能用但接收偏弱、client 与 data 数据包常漏接，而且本平台 injection 失败，无法 deauth 或截取 handshake。本文平台是 Ubuntu 24.04，未在 Kali 发行版本身测试。它适合纯 AP、一般连接与 WPA3 热点；渗透测试请选 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXM 在 Ubuntu 24.04 要另外装驱动吗？"
    answer: "不用。mt7921u 驱动在 kernel 6.17 内置，插上即辨识（USB ID 0e8d:7961），免 DKMS、免编译。驱动不提供 IBSS（Ad-hoc）与 mesh 模式，这是限制而非设置问题。"
  - question: "AWUS036AXM 可以当 AP 开热点吗？支持 WPA3 吗？"
    answer: "可以，这是它最拿手的用途。2.4 GHz（802.11n）与 5 GHz VHT80 都有 iPhone 连入并 authorized；WPA3-SAE 于 2.4 GHz 可用（MFP: yes；5 GHz 的 WPA3 未实测），旧款 iPhone 需设 sae_pwe=0；STA＋AP 并行（VIF）也可用。本轮只测 2.4 与 5 GHz，6 GHz 与蓝牙未单独实测。"
  - question: "AWUS036AXM 的 monitor mode 好用吗？"
    answer: "能进 monitor，2.4 GHz 与 5 GHz 都收得到 beacon，但接收偏弱、client 与 data 数据包量少，建议锁定单一频道而非跳频。要大范围或长距离监听，我们的测试中 AWUS036AXER 与 ACH 明显更强。"
draft: false
---

{{< tldr >}}AWUS036AXM 在 ASUS GX10／Ubuntu 24.04 ARM64 上 monitor、AP、WPA3、VIF 可用，但 packet injection 实测失败（No Answer／Found 0 APs），无法 deauth 或截取 handshake，不建议用于渗透测试；定位纯 AP 与连接。{{< /tldr >}}

Yupitek 是 ALFA Network 的台湾经销商。这篇是 AWUS036AXM 的逐卡实测，目的很单纯：把这张 Wi-Fi 6 网卡在 **ASUS GX10（ARM64）+ Ubuntu 24.04** 上「能做什么、不能做什么」量到清楚，让选购的客户不必靠规格表猜。

先把定位讲明白：以下所有测试都在 Yupitek 自有设备、自有办公室 Wi-Fi 上完成，对象是我们自己的测试手机。这是经销商对产品兼容性与能力边界的硬件验证，不是针对第三方网络的攻击教学。文中不提供任何对外部网络的操作步骤；monitor 与注入相关的量测，一律在自有封闭环境、对自有设备进行。

这张卡最需要先知道的一件事：**它在本平台的 injection（注入）是失败的**。如果你的用途会用到注入或 handshake 截取，可以直接跳到第四、第五节看选型结论；如果你要的是稳定连接与架 AP，那 AWUS036AXM 会是一张很称职的卡。

## 一、卡片与测试平台

AWUS036AXM 采用 MediaTek **MT7921AU** 芯片，走 kernel 内置的 **mt7921u** 驱动，规格为 **Wi-Fi 6（802.11ax）、2x2** 双空间流。同芯片的 **AWUS036AXML**（MT7921AUN，多了蓝牙）在本平台的 Wi-Fi monitor／AP／注入行为完全相同，两张可互相参照；差别是 AXML 另有蓝牙，且本机实测 6 GHz band 可用，而 AXM 的 6 GHz 与蓝牙本轮未单独实测。

- **运算平台**：ASUS GX10（ARM64 / aarch64）
- **操作系统**：Ubuntu 24.04 LTS
- **内核版本**：kernel 6.17.0-1014-nvidia
- **测试设备**：Apple iPhone 7 Plus（WPA3-SAE 与 VIF 另以 iPhone 15 Pro 复测）
- **测试环境**：自有办公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36
- **测试期间**：2026-11-16 至 2026-11-18 实机量测

## 二、硬件与驱动（免装即用）

mt7921u 驱动已内置于 kernel 6.17，AWUS036AXM 插上 GX10 就被辨识，不需要 DKMS、不需要自行编译任何第三方驱动。这是这代 MediaTek 卡在 ARM64 上最省事的地方。

| 项目 | 内容 |
|---|---|
| 型号 | AWUS036AXM |
| 芯片 | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| 驱动（in-kernel） | `mt7921u` |
| 世代 / 串流 | Wi-Fi 6（802.11ax）/ 2x2 |
| 接口模式 | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| 不支持模式 | IBSS（Ad-hoc）、Mesh（802.11s） |

确认网卡被辨识：

```bash
lsusb | grep 0e8d:7961
```

预期输出为 `ID 0e8d:7961 MediaTek Inc. Wireless_Device`。另外留意一下，`iw phy info` 列出的接口模式里没有 IBSS 与 mesh point，这是 mt7921u 的先天限制，不是设置问题；要跑 mesh / IBSS 的场景，改用 `mt76` 的 AWUS036ACM / ACHM。

## 三、实测能力：Monitor / AP / WPA3，以及 Injection 失败的诚实说明

先给一张内核能力矩阵，再逐项说明。

| 能力项目 | 2.4 GHz | 5 GHz | 实测备注 |
|---|---|---|---|
| Monitor（监听） | ✅ 可用（接收较弱） | ✅ 可用（接收较弱） | 收得到 beacon，client / data frame 量偏少 |
| **Injection（注入）** | ❌ **本平台失败** | ❌ **本平台失败** | 根因为 kernel 6.16+ mac80211 chanctx 回归（非芯片先天） |
| AP（热点） | ✅ 含 802.11n（HT20） | ✅ VHT 80 MHz | iPhone 7 Plus 实机连入、authorized |
| WPA3-SAE | ✅ | 未实测 | MFP: yes，`sae_pwe=0` 兼容旧 iPhone；仅在 2.4 GHz 实测 |
| VIF（STA + AP） | ✅ | ✅ | 一卡两用，STA 侧 ping 17 ms |

### Monitor（监听）✅ 可用，但接收偏弱

2.4GHz 与 5GHz 都能切进 monitor 模式，也都收得到 beacon。但要诚实说：AWUS036AXM 的接收明显比同平台的 AWUS036ACM / ACHM 弱，实测 frame 数偏少，client 与 data 数据包截取量不多。实务上建议**锁定单一频道**侧录，不要跳频，收获会稳定一些。

还有一个容易误判的点：monitor 模式下 `txpower` 会回报 3 dBm，这是回报假象（硬件实际 TX 约 20 dBm，已由 `txpower_sku` 验证），不代表发射真被压到那么低。AWUS036AXM 本来就不是为大范围侧录设计的；要扫得广、收得远，就看天线调校更强、跳频更积极的 AWUS036AXER，或双天线高增益的 AWUS036ACH，这两张在同平台的 monitor 收讯明显更强。

### AP（热点）✅ 这是 AXM 最拿手的场景

2.4GHz 开 AP 可同时开 802.11n（HT20），iPhone 7 Plus 连入协商到 MCS 7、authorized。5GHz 可开到 **VHT 80 MHz**，iPhone 连入为 VHT-NSS2、authorized。无论 2.4G 或 5G，AWUS036AXM 当热点都稳定，这是它在本平台最值得买单的能力。

### WPA3-SAE ✅

AP 端开 WPA3-SAE，iPhone 7 Plus 成功连入，MFP（Management Frame Protection）显示 `yes`。实务提醒：设 `sae_pwe=0` 可兼容 iPhone 7 Plus 这类较旧设备；若设 `sae_pwe=2`，旧 iPhone 可能连不上。

### VIF（STA + AP 一卡两用）✅

AWUS036AXM 可以同时当 STA 连上既有 Wi-Fi，又开一个 AP 虚拟接口（VIF）。实测 iPhone 15 Pro 连入 AP VIF 时，STA 这端对 `YUPITEK` 的 ping 约 17 ms，连接正常。对「一张卡同时上网又分享热点」的需求是可用的。

### Injection（注入）❌ 本平台失败 —— 这是选型的分水岭

这是 AWUS036AXM 最重要、也最需要诚实交代的一条。实测 `aireplay-ng --test` 的输出是：

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

2.4GHz 与 5GHz 都一样失败。先厘清一个常见误会：monitor 模式下 `iw` 回报 txpower 只有 3 dBm 是**回报假象**，硬件实际 TX 约 20–23 dBm（已由 `txpower_sku` 验证），发射功率并没有被压低，不是失败主因。真正的根因在**软件层**：kernel 6.16 之后 mac80211 的 channel context（chanctx）出现回归，让 stock 驱动在 active monitor／注入情境下收不到目标 beacon，`aireplay-ng` 于是判定 `No Answer`。这是 **kernel 端的回归，不是 MT7921 芯片先天不能注入**。现象记录在 morrownr/USB-WiFi issue #387，根因分析则在 morrownr/mt76 issue #18。

要补充的是：社区实测指出，在同型号上改用 git／patched 驱动，确实能让 active monitor 加注入运作起来；但即使如此，MT7921 firmware 仍把注入**锁在 1 Mbps／6 Mbps 的基础速率**，无法以 HT／VHT 速率注入。换句话说，就算绕过 kernel 回归，这张卡的注入能力也受限。对照 Realtek 的 rtw89 卡（如 AWUS036AX／AXER）在同一套 aircrack-ng、同一个 GX10 平台上注入可用，MT7921 这条路在 **stock kernel 6.17** 上是不通的。

再强调一次，这不是单张卡故障，也不是设置调错。同芯片的 AWUS036AXML 行为一模一样，在 stock kernel 6.17 上改参数、换频道、改 regulatory domain 都救不回来——根因是 kernel 6.16+ 的 mac80211 chanctx 回归，再加上 firmware 的注入速率锁，并非芯片硬件缺陷。直接的后果：AWUS036AXM 在本平台**无法 deauth、无法主动截取 WPA handshake**。需要这些能力，请改用下一节的 Realtek / mt76x 方案。

至于高级功能，整理如下：

| 高级功能 | 状态 | 说明 |
|---|---|---|
| WPA handshake 截取 | ❌ | 因注入失败而不可用，改用 ACM / ACHM / ACH / ACS / EACS |
| VIF（STA + AP） | ✅ | 一卡两用可用 |
| Active monitor | 🟡 | `set monitor active` 被接受，ACK 未验证 |
| Ad-hoc（IBSS） | N/A | mt7921u 不支持 |
| Mesh（802.11s） | N/A | mt7921u 不支持 |
| Wi-Fi Direct（P2P） | ⬜ | 驱动声明支持，缺第二台设备未测 |

### 操作安全与实务提醒

几个在 GX10 上操作这张卡的实务重点，先讲在前面可以少踩雷：

- **别切断自己的网络**：绝对不要运行 `airmon-ng check kill`，它会关掉 NetworkManager、让整台 GX10 断网。操作时只动外置的 `wlx*` 接口，不要碰 GX10 内置的对外上网主线。
- **AP 密码要 8 码以上**：否则 hostapd 会回 `invalid WPA passphrase length` 而起不来。
- **手机扫不到 SSID 时**：把网卡拔插一次重置、或把手机靠近即可解决（monitor 模式回报的 3 dBm 是假象、非真实功率，并非主因）。
- **RX stall 排除**：反复切换 monitor / AP 之后若突然扫不到任何东西，多半是 RX stall，拔插网卡一次即可复原（接口名以 MAC 命名、不会改变）。

## 四、适合与不适合的用途

把上面的量测收敛成一句话：AWUS036AXM 是张优秀的「连接 / AP」卡，但不是「注入 / 攻防」卡。

**适合的用途**

- 稳定的日常连接（Wi-Fi 6、2x2）
- 架设 2.4GHz / 5GHz AP 热点（含 802.11n 与 VHT80）
- WPA3-SAE 兼容性验证与布建测试
- STA + AP 一卡两用（VIF）
- 被动侧录 beacon 的轻量 monitor 需求

**不适合的用途（避雷）**

- injection / deauth
- WPA handshake 截取、主动式攻防演练
- 需要 IBSS（Ad-hoc）或 Mesh 的实验
- 需要长距离、高灵敏度的大范围 monitor 侧录

**最重要的一条避雷**：如果你的用途是 **injection 或 handshake**，**请勿选 AWUS036AXM（或同芯片的 AWUS036AXML）**。MT7921 在 ASUS GX10（ARM64 / Ubuntu 24.04 / stock kernel 6.17）这个平台上注入失败，根因是 kernel 6.16+ 的 mac80211 chanctx 回归、并非芯片先天不能注入；截至 2026-11-18 的 stock 环境无法以调参解决，把它留给「纯连接 / 纯 AP」的场景即可。

## 五、选型建议（纯 AP／连接）

| 你的需求 | 建议选择 | 理由 |
|---|---|---|
| 纯 AP / 稳定连接（不需注入） | **AWUS036AXM** / AWUS036AXML | MediaTek 连接稳定，AP 与 WPA3 表现好 |
| 渗透测试（injection + handshake） | AWUS036EACS / AWUS036ACH / AWUS036ACS | 两频注入可用，端到端 handshake 跑得通 |
| 最强接收 / 长距离 monitor | AWUS036AXER / AWUS036ACH | AXER 跳频扫描积极，ACH 双天线高增益 |
| Wi-Fi 6 + AP 且要注入 | AWUS036AX / AWUS036AXER | 2x2 VHT80，AP 稳定且注入可用 |
| mesh / IBSS 实验 | AWUS036ACM / AWUS036ACHM | `mt76` 驱动单机可创建 |

一句白话：要稳定连接、要当 AP，AWUS036AXM 很称职；只要牵涉注入或 handshake，就换 Realtek 的 EACS / ACH / ACS。同一批卡在 ARM64 上的完整比较，以及 9 款 Monitor / Injection / AP / WPA3 全矩阵，请见总表 Hub：

- [2026 最完整实测：9 款 ALFA 无线网卡在 ASUS GX10（ARM64 / Ubuntu 24.04）全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

再次强调定位：本文所有 monitor / 注入相关的量测，全部在 Yupitek 自有封闭环境、对自有测试设备进行，用途是验证产品能力与兼容性边界，不提供也不建议对任何第三方网络进行上述操作。

## 常见问题（FAQ）

**Q1. AWUS036AXM 能做数据包注入（packet injection）吗？**
在我们的测试平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。`aireplay-ng --test` 在 2.4 GHz 与 5 GHz 都回报 `No Answer`、`Found 0 APs`，因此也无法 deauth 或截取 WPA handshake。根因是 kernel 6.16+ 的 mac80211 chanctx 回归，并非芯片先天不能注入；同系列的 AWUS036AXML 结果相同。需要注入请改选实测可用的 AWUS036EACS、ACH 或 ACS。

**Q2. AWUS036AXM 适合拿来做渗透测试或 Kali 吗？**
不建议。monitor 能用但接收偏弱、client 与 data 数据包常漏接，而且本平台 injection 失败，无法 deauth 或截取 handshake。本文平台是 Ubuntu 24.04，未在 Kali 发行版本身测试。它适合纯 AP、一般连接与 WPA3 热点；渗透测试请选 AWUS036EACS、ACH 或 ACS。

**Q3. AWUS036AXM 在 Ubuntu 24.04 要另外装驱动吗？**
不用。mt7921u 驱动在 kernel 6.17 内置，插上即辨识（USB ID `0e8d:7961`），免 DKMS、免编译。驱动不提供 IBSS（Ad-hoc）与 mesh 模式，这是限制而非设置问题。

**Q4. AWUS036AXM 可以当 AP 开热点吗？支持 WPA3 吗？**
可以，这是它最拿手的用途。2.4 GHz（802.11n）与 5 GHz VHT80 都有 iPhone 连入并 authorized；WPA3-SAE 于 2.4 GHz 可用（`MFP: yes`；5 GHz 的 WPA3 未实测），旧款 iPhone 需设 `sae_pwe=0`；STA＋AP 并行（VIF）也可用。本轮只测 2.4 与 5 GHz，6 GHz 与蓝牙未单独实测。

**Q5. AWUS036AXM 的 monitor mode 好用吗？**
能进 monitor，2.4 GHz 与 5 GHz 都收得到 beacon，但接收偏弱、client 与 data 数据包量少，建议锁定单一频道而非跳频。要大范围或长距离监听，我们的测试中 AWUS036AXER 与 ACH 明显更强。

## 六、延伸阅读

以下相关文章陆续上线（链接施工中）：

- 《免装驱动：在 Ubuntu（ARM64）上激活 Monitor 与 AP 模式》 → [`/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 《WPA3-SAE 能力与 handshake 实务（自有环境验证）》 → [`/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 《AWUS036AXML 单卡实测（同 MT7921 芯片 + BT）》 →（施工中）
- 《为什么 mt7921u 在 kernel 6.16 以后无法注入：chanctx 回归与固件速率锁说明》 →（施工中）

---

*测试单位：Yupitek（ALFA 经销）｜ 平台：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 测试设备：Apple iPhone 7 Plus（WPA3 / VIF 另测 iPhone 15 Pro）*
