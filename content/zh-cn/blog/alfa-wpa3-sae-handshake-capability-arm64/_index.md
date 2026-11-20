---
title: "WPA3-SAE 时代的无线审核：9 款 ALFA 卡 handshake 截取能力实测，与 iPhone 连接的 sae_pwe 兼容性雷区"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "ALFA 网卡在 Ubuntu（可延伸至 Kali）的 WPA3-SAE handshake 截取能力实测：9 款注入率与端到端 .22000 截取结果，sae_pwe 兼容性雷区与选型建议。"
faq:
  - question: "AWUS036AXM 在 Ubuntu 能截取 WPA handshake 吗？"
    answer: "在本平台不能。实测中 AWUS036AXM 与 AWUS036AXML（MT7921 芯片）因 injection 失败、无法送出 deauth，整条 4-way handshake 截取链路跟着断，不适合需要 handshake 截取的用途。"
  - question: "哪一款 ALFA 网卡的 WPA handshake 截取最可靠？"
    answer: "实测中 AWUS036EACS 表现最扎实：两频 injection 皆达 100%，deauth 后收到 79 个 ACK 回报，并成功转出 hashcat 可用的 .22000 文件，是本批端到端验证最完整的一款。"
  - question: "WPA3-SAE 的热点为什么旧 iPhone 连不上？"
    answer: "关键在 hostapd 的 sae_pwe 参数：设为 2（强制 H2E）时 iPhone 7 Plus 会连接失败；改回 sae_pwe=0（Hunting-and-Pecking）后才能正常完成 4-way 交握并连入。"
  - question: "WPA3 环境下还能截取到 4-way handshake 吗？"
    answer: "纯 WPA3-SAE 环境会强制激活 PMF（ieee80211w=2），传统针对管理框的手法会被挡下；实务上仍能截取到 handshake，多半是因为目标跑的是 WPA2/WPA3 过渡模式，而非纯 WPA3。"
  - question: "ALFA 网卡的 5GHz injection 测不出来，是硬件问题吗？"
    answer: "不一定。默认法规网域会限制部分 5GHz 频段的发射功率，导致注入「发不出去」；实测中把法规网域切换为可发射状态后，原本失败的 5GHz 注入即转为可用，建议先确认法规网域设置，再判断是否为硬件限制。"
draft: false
---

> 测试单位：Yopitek（ALFA Network 台湾经销）｜测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17｜测试设备：自有 iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）｜测试对象：自有办公室 Wi-Fi（SSID YUPITEK，2.4G ch5 / 5G ch36、157）。
>
> 本文为 ALFA 无线网卡的能力与兼容性总览。所有 Monitor / Injection / handshake 截取，均于 Yopitek 自有设备、自有办公室 Wi-Fi、对自有测试手机进行，属经销商对硬件的正当能力验证；不针对任何第三方网络，亦不提供攻击操作步骤。

## 重点摘要（TL;DR）

在 ASUS GX10（ARM64 / Ubuntu 24.04 / kernel 6.17）实测的 9 款 ALFA 网卡中，共 7 款（ACM、ACHM、ACH、ACS、EACS、AX、AXER）完成端到端 WPA handshake 截取并转出 `.22000`；AWUS036EACS 两频注入 100%、收到 79 个 ACK，MT7921 的 AXM / AXML 则在本平台注入失败。

- WPA3-SAE 普及后，审核重点从「能不能 monitor」转为「端到端 handshake 截取能力」与「`sae_pwe` 端点兼容性」。
- **端到端 `.22000` 已实证 9 款中的 7 款**：ACM、ACHM、ACH、ACS、EACS、AX、AXER；其中 EACS 最扎实（两频注入 100%、79 ACKs）。
- **AXM / AXML（MT7921）在本平台 injection 失败**，无法 deauth，截取不到 handshake，审核用途务必避开。
- `sae_pwe` 雷区：旧款 iPhone 需 `sae_pwe=0` 才连得上；5G 注入前先 `iw reg set US` 解锁 TX。
- 纯 WPA3 强制 PMF（`ieee80211w=2`），现场仍能截取多半因目标跑 WPA2/WPA3 过渡模式。

## 1. WPA3-SAE 普及，把无线审核的门槛整个抬高了

过去十年，授权范围内的无线审核（authorized wireless audit）几乎都围着 WPA2-PSK 的 4-way handshake 打转：截取一次完整握手，后端就能脱机比对。但自从 Wi-Fi 6 认证把 WPA3 纳入强制项目，SAE（Simultaneous Authentication of Equals，俗称 Dragonfly）逐步取代 PSK，把「截取握手、脱机验证」这条老路堵得越来越窄。

对经销商与第一线工程师来说，WPA3-SAE 带来三个实务上的改变：

1. **PMF（Protected Management Frame）变成强制**。WPA3-SAE 规范强制打开 `ieee80211w=2`，management frame 受到保护，传统那种「随手一个 deauth 把设备踢下线」的做法，在纯 WPA3 环境会被直接挡下。
2. **过渡模式（transition mode）仍保留 4-way**。现实中大量 AP 跑的是 WPA2/WPA3 混合过渡模式，为了兼容旧设备仍会保留 WPA2 的 4-way handshake，这也是目前授权审核仍截取得到握手的主因。能不能截取到握手，很大一部分要看现场目标开在哪一种模式。
3. **端点兼容性成为新雷区**。SAE 有不同的 password element 推导方式（由 `sae_pwe` 控制），AP 参数一旦设错，连自家的旧 iPhone 都连不上，更别说要在审核现场重现客户端点的连接行为。

因此，当客户问「哪一张 ALFA 卡能拿来做 WPA3 相关的授权审核」，答案已经不是「能不能 monitor」这么简单，而是要看两件事：**端到端的 handshake 截取能力**，以及**对 WPA3-SAE 参数与实机端点的兼容性**。这份报告就是用 9 款 ALFA 卡、在同一套 ARM64 平台上实测后，整理出的能力对照。

## 2. 什么叫「端到端 handshake 截取能力」（概念层）

这里先把能力拆成三段，纯概念说明，不涉及任何针对第三方网络的操作指令：

- **第一段：Injection（主动注入）**。网卡要能「发得出去」特定的管理框，才能促使一个已连接的 client 重新进行关联。很多卡只能被动 monitor（收数据包），却无法 injection（主动发送）。这是整条链最容易卡关的一段。本批测试以 `aireplay-ng --test` 量化注入成功率，并在 handshake 测试中以 client 回传的 ACKs 数，验证框是否真的送达。
- **第二段：4-way handshake 截取**。当 client 重新关联时，WPA 会交换四个 EAPOL 消息（M1–M4）。网卡在 monitor 模式下，必须把这四框完整收齐，缺一不可。
- **第三段：转出 hashcat `.22000`**。把截取到的 pcap 用 `hcxpcapngtool --all` 转成 hashcat 的 `.22000` 格式，交由后端做脱机验证。

**三段全部在实机跑通，才算「端到端」**：真的对自家 iPhone 7 Plus 送出 deauth（injection）→ 收齐完整 M1–M4 → 转出 `.22000` 落档。只能收不能发、或四框收不齐、或转不出档，都不算端到端。本文不列任何逐步攻击指令；下列对照只回答一个问题：哪一张卡在这条能力链上走得完。

以本批最扎实的 EACS 为例，一次成功的端到端长这样：deauth 送出后 client 回传 **79 个 ACKs**（确认框确实到达那支手机）、`aircrack-ng` 判定 YUPITEK 有 1 个 handshake、EAPOL 的 M1 / M2 / M3 / M4 四框各收到 1 份、截取到的 client MAC 开头为 Apple OUI（确认就是那支 iPhone 7 Plus），最后 `hcxpcapngtool --all` 转出约 784 bytes 的 `.22000`。这四个条件缺一，这场截取就不算数。这也是为什么「能 monitor」和「能端到端截取」是两件完全不同的事。

## 3. 9 款卡 handshake 能力对照表

| # | 型号 | 芯片 / 世代 | Injection 2.4G | Injection 5G | WPA handshake 截取能力 |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5・2T2R | 可用 63–83% | 可用 76% | **端到端 `.22000` 已实证**（注入率较低） |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5・1T1R | 可用 96–100% | 仅广播 | **端到端 `.22000` 已实证（于 5 GHz ch36）** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5・2T2R | **100%** | **100%** | **端到端 `.22000` 已实证（2026-11-19 补测）** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5・1x1 | **100%** | 96% | **端到端 `.22000` 已实证** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5・1x1 | **100%** | **100%** | **端到端 `.22000` 已实证（79 ACKs）** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6・2x2 | 96% | 可用 | **端到端 `.22000` 已实证** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6・2x2 | 73% | 可用 | **端到端 `.22000` 已实证** |
| 8 | AWUS036AXM | MT7921AU / Wi-Fi 6・2x2 | 失败 | 失败 | 不支持：注入失败，无法截取 |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6・2x2 | 失败 | 失败 | 不支持：注入失败，无法截取 |

**两个梯队，一眼看懂：**

- **端到端已实证（截取 → `.22000` 落档，9 款中的 7 款）**：AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX 与 AWUS036AXER。其中 EACS 两频注入都 100%、deauth 收到 79 个 ACKs，是本批握手能力最扎实的一张；AWUS036ACH（RTL8812AU 双天线高增益）两频注入 100%，于 2026-11-19 补测转出 47 行 hashline 的 `.22000`，与 EACS 并列渗透测试首选。**完成端到端 handshake 截取的型号共七款：ACM、ACHM、ACH、ACS、EACS、AX、AXER。** ACM 注入率较低（2.4G 63–83% / 5G 76%），ACHM 于 5 GHz（ch36）完成，两者皆已转出 `.22000`。
- **无法截取（2 款）**：AWUS036AXM 与 AWUS036AXML（MT7921 在本平台 injection 失败，无法 deauth、自然也截取不到 handshake）。

需要特别点名的是 **AXM / AXML**：两款都是 Wi-Fi 6、monitor 与 AP 都正常，唯独在本平台 injection 无法运作——主因是 stock kernel 6.16+ 的 mac80211 chanctx 回归（非芯片先天），社区同型号改用 git／patched 驱动虽可运作但 firmware 会锁速率（对应 morrownr/USB-WiFi #387、morrownr/mt76 #18）。纯上网、做热点没问题，但**凡是要注入或截取 handshake 的审核用途，在本平台一律避开**。

## 4. WPA3-SAE 兼容雷区：参数设错，自家 iPhone 都连不上

能力之外，WPA3-SAE 的参数兼容性，是最容易在现场翻车的地方。本批实测踩到两个关键雷：

### 4-1. ACHM 必须 `sae_pwe=0`，否则 iPhone 7 Plus 连不上

SAE 的 password element 推导有不同方式，hostapd 以 `sae_pwe` 控制。本批把 AWUS036ACHM 架成纯 WPA3-SAE（`wpa_key_mgmt=SAE` + 强制 PMF `ieee80211w=2`）时，一旦 `sae_pwe` 设成 `2`，**iPhone 7 Plus 直接连不上**；改回 `sae_pwe=0`（Hunting-and-Pecking，兼容旧端点）之后，iPhone 7 Plus（iOS 15）才顺利连入并完成 4-way。

这条雷的意义在于：当你要在审核现场「重现」一个以旧 iOS 端点为主的 WPA3 环境，AP 端的 `sae_pwe` 必须配合端点能力，否则得到的会是「连不上」的假阴性，而不是真正的兼容性结论。EACS、ACS 的 WPA3-SAE AP 测试同样采 `sae_pwe=0` + `ieee80211w=2`，iPhone 7 Plus 均能连入；`sae_pwe=0` 就是本批对旧 iPhone 端点验证过的安全值。

### 4-2. 5G injection 前，先 `iw reg set US` 解锁 TX

第二个雷与法规域（regulatory domain）有关。默认 `reg=TW` 会锁住部分 UNII 频段的 TX，导致 5 GHz 的 injection / deauth「发不出去」。本批在做 5G 注入前一律先 `iw reg set US` 解锁 TX，测完立即 `iw reg set TW` 还原。ACS 的 5G 注入在解锁后由失败转为 96%，EACS、ACH 则直上 100%。忘了解锁 reg，会把一张注入能力正常的卡误判成「5G 不能用」。

### 4-3. 顺带一提：PMF 在 WPA3 是强制的

WPA3-SAE 规范强制 `ieee80211w=2`（Management Frame Protection）。这代表纯 WPA3 环境下，传统针对 management frame 的手法会被 PMF 挡住；现实审核之所以还能截取到 4-way，多半是因为目标仍跑 WPA2/WPA3 过渡模式。选卡时把这点一并纳入考量，才不会对纯 WPA3 目标抱错期待。

## 5. 工具链概述：ARM64 平台上实际能跑的那一套

硬件能力之外，平台工具链同样影响审核效率。以下是本批在 GX10（ARM64）上整理出的几个实测心得：

- **转档一律 `hcxpcapngtool --all`**。默认参数较严格，常回「not enough M1」而转不出档；加上 `--all`，才能由完整的 M1–M4 稳定转出 `.22000`。
- **办公室多台同名 AP 时，不要锁 `--bssid`**。Yopitek 办公室同一个频道上有多台同名 YUPITEK AP，iPhone 会连上信号最强的那一台。截取时若用 `--bssid` 锁单一 BSSID，很可能把 iPhone 实际连上的那台滤掉、整场截取落空。实测结论是**不锁 BSSID、直接截取整个频道**，再从落档里挑出完整握手。
- **`hcxdumptool` 8.x 在本平台除 EACS 的 2.4 GHz 外皆 `failed to arm`（5 GHz 失败）**。rtw88 / rtw89 / mt7921u 都不提供 active-monitor，而 hcxdumptool 8.x 需要它；解法是改用 `airodump-ng` + `aireplay-ng` 这套传统 aircrack-ng 流程。
- **反复切换模式后扫不到东西，先拔插卡**。rtw88 / rtw89 在反复切 monitor / AP 之后可能发生 RX stall（扫描 0 数据包）；USB 重新枚举即可复原，且接口名由 MAC 决定、拔插后不变。截取 handshake 前，建议第一件事就是重插一次卡。
- **BT+WiFi 复合设备（EACS / AXML）重插有竞态**。含蓝牙的复合卡在重插、或插在某些 USB 孔时，会发生 WiFi 功能 probe 卡死、生不出 `wlx` 接口；解法是换一个 USB 孔重插，`modprobe` 或手动 bind 多半无效。
- **ARM64 的工具安装眉角**。aircrack-ng 在 aarch64 常缺 prebuilt 套件，需自源代码编译；wifite 则用 git 版（apt 版与自编 aircrack-ng 相依冲突）。
- **安全守则：绝不 `airmon-ng check kill`**。GX10 对外上网靠内置网卡，`check kill` 会连 NetworkManager 一起关掉、使主机断网。本批全程只操作 ALFA 卡的 `wlx*` 接口，不碰内置对外主线。

## 6. 选型小结：要做 WPA3 相关审核，该选哪几款

把能力、兼容性与平台工具链合在一起看，对「WPA3 相关的授权审核」用途，本批的建议是：

| 需求情境 | 建议型号 | 理由 |
|---|---|---|
| 综合首选（注入 + 端到端 handshake） | **AWUS036EACS** | 两频注入 100%、deauth 收 79 ACKs、端到端 `.22000` 已实证；唯一要注意的是 BT+WiFi 复合设备，重插偶尔要换 USB 孔 |
| 高增益 / 长距离 + 强注入 | **AWUS036ACH** | RTL8812AU 双天线、两频注入 100%，接收能力强 |
| 轻量随身 | **AWUS036ACS** | 单串流、端到端 `.22000` 已实证，5G 注入 96% |
| Wi-Fi 6 需求 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80、端到端 `.22000` 已实证；AXER 内嵌天线（Nano）设计＋芯片调校、扫描覆盖最广 |
| **务必避开** | AWUS036AXM / AWUS036AXML | MT7921 在本平台 injection 失败，无法截取 handshake |

一句话总结：**要做 WPA3 相关审核，优先 EACS，其次 ACH / ACS；需要 Wi-Fi 6 选 AX / AXER；务必避开 AXM / AXML。** 七款完成端到端 handshake 截取的卡里，Realtek（rtw88 / rtw89）全数可注入，MediaTek 的 ACM 与 ACHM（mt76）也跑通；MT7921 的 AXM / AXML 则不行。选型时，认芯片比认型号名更准。

## 常见问题（FAQ）

**Q：AWUS036AXM 在 Ubuntu 能截取 WPA handshake 吗？**
A：在本平台不能。实测中 AWUS036AXM 与 AWUS036AXML（MT7921 芯片）因 injection 失败、无法送出 deauth，整条 4-way handshake 截取链路跟着断，不适合需要 handshake 截取的用途。

**Q：哪一款 ALFA 网卡的 WPA handshake 截取最可靠？**
A：实测中 AWUS036EACS 表现最扎实：两频 injection 皆达 100%，deauth 后收到 79 个 ACK 回报，并成功转出 hashcat 可用的 `.22000` 文件，是本批端到端验证最完整的一款。

**Q：WPA3-SAE 的热点为什么旧 iPhone 连不上？**
A：关键在 hostapd 的 `sae_pwe` 参数：设为 2（强制 H2E）时 iPhone 7 Plus 会连接失败；改回 `sae_pwe=0`（Hunting-and-Pecking）后才能正常完成 4-way 交握并连入。

**Q：WPA3 环境下还能截取到 4-way handshake 吗？**
A：纯 WPA3-SAE 环境会强制激活 PMF（`ieee80211w=2`），传统针对管理框的手法会被挡下；实务上仍能截取到 handshake，多半是因为目标跑的是 WPA2/WPA3 过渡模式，而非纯 WPA3。

**Q：ALFA 网卡的 5GHz injection 测不出来，是硬件问题吗？**
A：不一定。默认法规网域会限制部分 5GHz 频段的发射功率，导致注入「发不出去」；实测中把法规网域切换为可发射状态后，原本失败的 5GHz 注入即转为可用，建议先确认法规网域设置，再判断是否为硬件限制。

## 7. 延伸阅读

- [9 款 ALFA 无线网卡 ARM64 实测总表与选型总评](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 各型号逐卡实测：[AWUS036EACS 单卡实测](/zh-cn/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 单卡实测](/zh-cn/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*本文所有测试均于 Yopitek 自有办公室 Wi-Fi（SSID YUPITEK）、对自有 iPhone 7 Plus 进行，属经销商对 ALFA 无线网卡的正当能力验证。数据引用自 2026-11-16～11-18 的实机测试报告，不针对任何第三方网络，亦不提供攻击操作步骤。测试单位：Yopitek（ALFA Network 台湾经销）— https://www.yupitek.com*
