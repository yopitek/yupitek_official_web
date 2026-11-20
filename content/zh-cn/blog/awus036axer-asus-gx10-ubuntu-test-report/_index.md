---
title: "AWUS036AXER 实测报告：ASUS GX10 + Ubuntu 24.04（ARM64）上接收最强的 Wi-Fi 6 网卡"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER 在 ASUS GX10／Ubuntu 24.04 ARM64 免装驱动（rtw89_8852bu）：monitor 60 秒扫到 63 AP＋12 client，注入 73%（2.4G）、5G VHT80 AP 与 WPA3 皆通过。"
faq:
  - question: "AWUS036AXER 在 Ubuntu 24.04 或 Kali 需要另外装驱动吗？"
    answer: "在 Ubuntu 24.04（ARM64，kernel 6.17.0-1014-nvidia）不用：内置的 rtw89_8852bu 驱动插上即辨识，免编译、免 DKMS（firmware rtw8852b_fw 0.29.29.5）。本文平台是 Ubuntu 而非 Kali 发行版，Kali 本体未测；Kali 常用工具 airmon-ng、kismet、bettercap、wifite、Wireshark 在此平台可使用。kernel 较旧时不保证内置，请先确认版本。"
  - question: "AWUS036AXER 支持 monitor mode 吗？接收有多强？"
    answer: "支持，2.4 GHz 与 5 GHz 都能进 monitor。我们在自有办公室用 airodump-ng 跳频扫描 60 秒，扫到 63 个 AP 与 12 个 client，是我们同场测试的九款卡中接收最强的一张；同芯片的 AWUS036AX 另次测试为 14 AP＋4 client（两次异步量测，仅供参考）。"
  - question: "AWUS036AXER 能做数据包注入（packet injection）吗？"
    answer: "可以。2.4 GHz 的 aireplay-ng --test 回应率 73%（22/30）并显示 Injection is working!，5 GHz 逐台自测也通过；我们在自有网络与自有设备上完成 handshake 截取并转出 .22000。若要两频接近 100%，本平台实测以 AWUS036EACS、ACH、ACS 更稳。仅限自有或已授权的网络。"
  - question: "AWUS036AXER 和 AWUS036AX 差在哪？"
    answer: "两者同为 Realtek RTL8832BU、同用 rtw89_8852bu，在本平台的模式支持与注入行为一致；差别在天线调校与增益带来的接收表现（AXER 60 秒 63 AP＋12 client，AX 为 14 AP＋4 client）。两者皆为内嵌天线、无 RP-SMA，天线规格请以产品页为准。"
  - question: "AWUS036AXER 可以当 AP 或开 WPA3 吗？不支持哪些模式？"
    answer: "可以。2.4 GHz 802.11n 与 5 GHz VHT80（VHT-NSS2、351 Mbit）都有 iPhone 连入并 authorized；WPA3-SAE 以 sae_pwe=0 让 iPhone 15 Pro 连入（于 2.4 GHz；5 GHz 的 WPA3 未实测）；STA＋AP 并行可用。但 rtw89_8852bu 不支持 active monitor、IBSS、mesh。"
draft: false
---

{{< tldr >}}AWUS036AXER 在 ASUS GX10／Ubuntu 24.04 ARM64 插上即用（内置 rtw89_8852bu）；monitor 60 秒扫到 63 AP＋12 client，2.4 GHz 注入 73%，AP 与 WPA3 皆通过；不支持 active monitor、IBSS、mesh。{{< /tldr >}}

> 本文为 Yupitek（ALFA 台湾经销）于自有设备上的产品兼容性与能力实测。
> 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。测试环境为自有办公室 Wi-Fi（SSID `YUPITEK`），对自有测试手机 iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）进行。
> ⚠️ **合法使用**：Monitor 与 Injection 仅限自己拥有或已取得授权的网络与设备；AP 模式请遵守当地无线电法规。本文聚焦网卡能力、兼容性、设置与选型，不涉及针对第三方网络的任何攻击操作。

---

## 1. 这张卡与测试平台

AWUS036AXER 是 ALFA 的 Wi-Fi 6（802.11ax）2x2 USB 网卡，采 Realtek RTL8832BU 芯片（无蓝牙）。它与同厂的 AWUS036AX 用的是**同一颗芯片、同一支驱动**（`rtw89_8852bu`），在本平台上的模式支持与行为一致；两者真正的差别在**天线调校与增益**，而不是外置或内置——AXER 采**内嵌（Nano）天线设计、无 RP-SMA**，靠芯片与 RF 调校把接收拉到最满。先记住这篇的核心结论：在我们同场比较的九张 ALFA 卡里，AXER 的**接收是最强的一张**。

测试平台为 ASUS GX10，搭载 NVIDIA GB10 超级芯片与 128GB 统一内存，操作系统 Ubuntu 24.04 LTS、架构 ARM64（aarch64）、kernel `6.17.0-1014-nvidia`。所有结果均于 2026-11-18 在这台机器实机跑出，测试设备为自有的 iPhone 7 Plus（WPA3 另测 iPhone 15 Pro），测试网络为自有办公室 Wi-Fi。对经销验证而言，ARM64 搭配新版 kernel 是相对严苛的组合，底下第 2 节会说明为什么这一代反而更省事。

补一点规格脉络：AXER 是 2x2（双空间串流）的 Wi-Fi 6 卡，可同时收发两条空间串流，这也对应到后面 5 GHz AP 实测协商出的 VHT-NSS2。但这张卡在本轮胜出，靠的是天线设计与 RF 调校，不是串流数（AX 同样是 2x2）。芯片、驱动、平台三者全部相同，天线调校几乎是唯一变因，所以 AXER 和 AX 的接收差距可以干净地归到内嵌天线设计与增益调校。

---

## 2. 硬件与驱动（内嵌天线，免装驱动）

AWUS036AXER 在 Ubuntu 24.04 的 6.17 kernel 上**插上即认、免编译、免 DKMS**。驱动 `rtw89_8852bu` 已经是 in-kernel 模块，firmware 为 `rtw8852b_fw`（版本 0.29.29.5），开机即加载，不需要再去 GitHub 抓 out-of-tree 项目或绑 DKMS。对需要长期维运、跨多次 kernel 更新的经销与教学环境来说，少掉编驱动这一步就是少掉一个最常见的故障点。

对照旧路会更有感：过去 Realtek 这类 USB 芯片多半没进 mainline kernel，用户得从 GitHub 抓 out-of-tree 项目（例如 `morrownr/USB-WiFi`）再用 DKMS 绑当前 kernel 编译，每逢 kernel 更新就要重编一次，一旦编译失败网卡就直接消失。rtw89 正式纳入 in-kernel 之后，这些步骤在 6.17 上可以整段省略，同一套操作也能跨多张同驱动的卡重复沿用。

先确认卡被正确辨识：

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

正常 WLAN 模式的 USB ID 是 `0bda:b832`。如果看到的是 `0bda:1a2b`，代表卡还停在「光盘模式」（CD-ROM mode），运行一次 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN 模式即可；本测试单位这张卡是直接以 WLAN 模式枚举，没有遇到光盘模式。

接口名称采 `wlx` + MAC 命名（例如 `wlxAABBCCDDEEFF`），插在哪台机器都不会变，方便脚本固定绑定。查找这张卡支持哪些模式：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

实测回报的模式为 managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO。这里没有 IBSS、mesh，也没有 active monitor，这是 rtw89 驱动的先天限制，第 4 节会诚实说明，别在选型时误判。

天线部分：AXER 采内嵌（Nano）天线设计、无 RP-SMA，和同芯片的 AX 相比，差别在天线调校与增益，实务上最直接的反映就是收讯。下一节的 monitor 数据会把这点讲清楚。

---

## 3. 实测能力

把三项内核能力（Monitor / Injection / AP）与 WPA3 的实测结果先列成一张表，细节在表后逐项展开：

| 能力 | 2.4 GHz | 5 GHz | 实测重点 |
|---|---|---|---|
| **Monitor（监听）** | ✅ 强 | ✅ 强 | 跳频扫到 **63 AP + 12 client**，九张卡中接收最强 |
| **Injection（注入）** | ✅ 73% | ✅ 可用 | 2.4G `22/30 73%`；5G `Injection is working!` |
| **AP（热点）** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone 连入；5G VHT-NSS2、351 Mbit |
| **WPA3-SAE** | ✅ | 未实测 | AP 端 iPhone 15 Pro 连入（`sae_pwe=0`）；仅在 2.4 GHz 实测 |
| **WPA handshake 截取** | ✅ 端到端 | — | 自有网络＋自有设备，4-way（M1–M4）→ `.22000` |

### 3-1. Monitor（本篇亮点：接收最强）

切 monitor 是标准的 `iw` 流程：先把接口交回自己管（`nmcli dev set $IF managed no`）、关接口、设 monitor type、开接口、设频道：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; 2.4 GHz 用 channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

2.4 GHz 与 5 GHz 各在 6 秒内收满 100 frames。真正拉开差距的是跳频扫描：`sudo airodump-ng --band abg $IF` 跑 60 秒，**扫到 63 个 AP 加 12 个 client**。这是本轮九张卡里抓到最多目标的一张，直接反映内嵌天线设计与 RF 调校带来的接收优势。对于现场盘点（site survey）、长距离监听、或是信号偏弱的环境，这个接收能力就是 AXER 的核心价值。

### 3-2. Injection（注入）

Injection 用 aireplay-ng 的自测模式验证，测的是网卡本身的能力，不是对外攻击：

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

2.4 GHz 回应率 73%（22/30），判定为可用。5 GHz 逐台对指定 AP 自测也回报 `Injection is working!`。补一个平台通则：**5 GHz 要发送/注入前，先 `iw reg set US` 解锁 TX 功率，测完记得 `iw reg set TW` 切回台湾法规频段**。

### 3-3. AP 热点（2.4 GHz 802.11n、5 GHz VHT 80 MHz）

AXER 两个频段都能起 hostapd AP。2.4 GHz 以 `hw_mode=g` + `ieee80211n=1` 起 802.11n 热点，iPhone 7 Plus 连入协商到 MCS 15、authorized。5 GHz 以 `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1` 起 VHT 80 MHz 热点，iPhone 7 Plus 连入协商到 **VHT-NSS2、80 MHz、351 Mbit、authorized**。起 AP 的前置是 `sudo nmcli dev set $IF managed no`，`wpa_passphrase` 至少 8 码，否则 hostapd 会回 `invalid WPA passphrase length`。

### 3-4. WPA3-SAE 与 handshake 截取

WPA3-SAE 在 AP 端设 `wpa_key_mgmt=SAE`、`ieee80211w=2`、`sae_pwe=0`，实测 iPhone 15 Pro 连入。**`sae_pwe` 是 ALFA 这批卡上的兼容性雷区**：部分设备在 `sae_pwe=2`（Hash-to-Element）时连不上，设 `sae_pwe=0` 可兼容较旧的 iPhone。

handshake 能力则是在**自有办公室 Wi-Fi（YUPITEK）＋ 自有测试设备**上做的端到端验证：截取到完整 4-way（M1/M2/M3/M4），再用 `hcxpcapngtool` 转出 hashcat 可读的 `.22000`。这里要点出一个 GX10 平台的共通现象：**`hcxdumptool` 在本平台除 AWUS036EACS 的 2.4 GHz 外，所有 USB 卡都会 `failed to arm`**（GX10 三频内置网卡枚举冲突，加上驱动没有 active monitor），所以 handshake 流程改走 aircrack-ng 套件（airodump-ng + aireplay-ng）。AXER 的注入能力在这条路上是够用的。

---

## 4. 高级功能与诚实限制

**VIF（STA + AP 并行）✅**：AXER 可以同时当 station 连上游 Wi-Fi、又开一个 AP VIF。实测主接口连 YUPITEK、AP VIF 开在 ch36 VHT80 并行，STA 端 ping 3.5 ms，适合要「边连网边开热点」的场景。

**Wi-Fi Direct（P2P）未测（⬜）**：驱动有声明 P2P-client / P2P-GO，但要完整验证需要第二台对接设备，本轮略过，因此不列入已验证能力。这类「驱动声明支持、但未实机跑过」的项目，我们一律诚实标为未测，不灌水当成通过。

**不支持的三个模式（N/A）**：`rtw89_8852bu` 驱动**不提供 active monitor、Ad-hoc（IBSS）、Mesh（802.11s）**。`iw dev $IF set type ibss` 或 `mp` 会直接失败，这是驱动层的限制，无法用设置绕过。如果用途是 mesh 或 IBSS 实验，要改看 MediaTek mt76 系列（如 AWUS036ACM / ACHM）。

**平台共通注意事项：**

- 绝对不要跑 `airmon-ng check kill`，它会关掉 NetworkManager，让 GX10 对外断线。只操作 `wlx*` 接口，不要碰内置的对外上网网卡。
- 反复切 monitor/AP 后若突然扫不到东西（RX stall），把卡**拔插一次**即可复原（USB 重枚举，接口名由 MAC 决定，不会变）。
- ARM64 平台上 aircrack-ng 需要自源代码编译；wifite 用 git 版，绕过 apt 依赖冲突。

**Kali 工具兼容性**：airmon-ng、kismet 2026.10、bettercap 2.32、wifite（git）、Wireshark / tshark 4.2 都能正常把 AXER 当数据源或管理接口使用。

---

## 5. 适用情境与选型建议

一句话定位：**AXER 是「接收取向」的 Wi-Fi 6 卡**。它和 AX 同芯片、功能一致，差别在天线调校与增益带来的收讯优势，所以选型逻辑很清楚：

| 你的需求 | AXER 是否首选 | 说明 |
|---|---|---|
| 最强接收 / 长距离 monitor / 现场盘点 | ✅ **首选** | 跳频扫到 63 AP + 12 client，九张卡最强；可搭 AWUS036ACH（双天线高增益）互补 |
| Wi-Fi 6 + AP 热点 | ✅ 适合 | 2x2、5G VHT80；与 AWUS036AX 同级 |
| Injection + 端到端 handshake | 🟡 可用 | 2.4G 73% 可用；若要两频接近 100%，AWUS036EACS / ACH / ACS 更稳 |
| mesh / IBSS 实验 | ❌ 不适合 | rtw89 不支持，改用 AWUS036ACM / ACHM（mt76） |

典型落地场景：把 AXER 当成**远程无线监测节点**，放在信号较弱或距离较远的点位，靠它内嵌天线的接收优势把现场的 AP / client 尽量收全，扫描结果再汇整回中央主机统一查看。由于是内嵌（Nano）天线、无 RP-SMA，天线不可更换；需要更高增益或更强指向性时，改搭双天线高增益的 AWUS036ACH 互补即可。

反过来说，如果用途是纯 AP 或一般连接、完全不需要注入，MediaTek 的 AWUS036AXM / AXML 也能用；但**只要牵涉注入或 handshake，就不要选 AXM / AXML**，它们在本平台注入是失败的（主因是 kernel 6.16 以后的 mac80211 chanctx 回归，另有固件把注入速率锁在 1/6 Mbps，并非芯片本身的限制）。AXER 刚好相反：注入可用、接收又最强。

想一次看完九款卡的完整矩阵与交叉比较，可回到总评页 → [`/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

---

## 常见问题（FAQ）

**Q1. AWUS036AXER 在 Ubuntu 24.04 或 Kali 需要另外装驱动吗？**
在 Ubuntu 24.04（ARM64，kernel 6.17.0-1014-nvidia）不用：内置的 `rtw89_8852bu` 驱动插上即辨识，免编译、免 DKMS（firmware `rtw8852b_fw` 0.29.29.5）。本文平台是 Ubuntu 而非 Kali 发行版，Kali 本体未测；Kali 常用工具 airmon-ng、kismet、bettercap、wifite、Wireshark 在此平台可使用。kernel 较旧时不保证内置，请先确认版本。

**Q2. AWUS036AXER 支持 monitor mode 吗？接收有多强？**
支持，2.4 GHz 与 5 GHz 都能进 monitor。我们在自有办公室用 airodump-ng 跳频扫描 60 秒，扫到 63 个 AP 与 12 个 client，是我们同场测试的九款卡中接收最强的一张；同芯片的 AWUS036AX 另次测试为 14 AP＋4 client（两次异步量测，仅供参考）。

**Q3. AWUS036AXER 能做数据包注入（packet injection）吗？**
可以。2.4 GHz 的 `aireplay-ng --test` 回应率 73%（22/30）并显示 `Injection is working!`，5 GHz 逐台自测也通过；我们在自有网络与自有设备上完成 handshake 截取并转出 `.22000`。若要两频接近 100%，本平台实测以 AWUS036EACS、ACH、ACS 更稳。仅限自有或已授权的网络。

**Q4. AWUS036AXER 和 AWUS036AX 差在哪？**
两者同为 Realtek RTL8832BU、同用 `rtw89_8852bu`，在本平台的模式支持与注入行为一致；差别在天线调校与增益带来的接收表现（AXER 60 秒 63 AP＋12 client，AX 为 14 AP＋4 client）。两者皆为内嵌天线、无 RP-SMA，天线规格请以产品页为准。

**Q5. AWUS036AXER 可以当 AP 或开 WPA3 吗？不支持哪些模式？**
可以。2.4 GHz 802.11n 与 5 GHz VHT80（VHT-NSS2、351 Mbit）都有 iPhone 连入并 authorized；WPA3-SAE 以 `sae_pwe=0` 让 iPhone 15 Pro 连入（于 2.4 GHz；5 GHz 的 WPA3 未实测）；STA＋AP 并行可用。但 `rtw89_8852bu` 不支持 active monitor、IBSS、mesh。

---

## 6. 延伸阅读

- 九款 ALFA 卡总矩阵与选型总表（Monitor・Injection・AP 全比较）→ `/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- 同芯片的 AWUS036AX 实测（天线调校不同） → `/zh-cn/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- 免装驱动：in-kernel 驱动激活 Monitor 与 AP 模式 → `/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- WPA3-SAE 时代的 handshake 截取能力与 `sae_pwe` 兼容性 → `/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- 延伸阅读内链待定稿后补上正式 hreflang 对应 URL；上列为 zh-TW slug placeholder。 -->

---

*测试单位：Yupitek（ALFA 经销）— https://www.yupitek.com ｜ 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）*
