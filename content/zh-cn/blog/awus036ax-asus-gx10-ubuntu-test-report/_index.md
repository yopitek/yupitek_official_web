---
title: "ALFA AWUS036AX 逐卡实测：ASUS GX10 + Ubuntu 24.04 的 Wi-Fi 6 Monitor / Injection / AP 能力报告（Realtek RTL8832BU / rtw89_8852bu）"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX（Wi-Fi 6）在 Ubuntu 24.04 ARM64 实测：免装驱动，Monitor、2.4G 注入 96%、5G AP VHT80、WPA3-SAE、端到端 handshake（.22000）通过；不支持 IBSS / mesh。平台 ASUS GX10、RTL8832BU。"
faq:
  - question: "AWUS036AX 在 Ubuntu 24.04 ARM64 要装驱动吗？lsusb 显示 0bda:1a2b 怎么办？"
    answer: "在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8832BU 由内置 rtw89_8852bu 驱动，免编译、免 DKMS。若 lsusb 显示 0bda:1a2b（光盘模式），运行 sudo usb_modeswitch -v 0bda -p 1a2b -K 切成 WLAN。"
  - question: "AWUS036AX 支持 monitor mode 与数据包注入吗？"
    answer: "支持。2.4 GHz 注入 29/30（96%）；5 GHz 逐台指定 AP 测试回 Injection is working!；airodump-ng 跳频 60 秒扫到 14 个 AP 与 4 个 client。不支持 active monitor、IBSS、mesh。"
  - question: "AWUS036AX 能截取 WPA handshake？MT7921 的 AXM / AXML 行吗？"
    answer: "AX 能：自有 AP 加自有 iPhone 7 Plus，aireplay-ng -0 触发重连、airodump-ng 截取完整 M1–M4，hcxpcapngtool 转出 .22000。MT7921 的 AXM / AXML 在本平台注入失败，做不到。仅限自有或已授权网络。"
  - question: "AWUS036AX 可以当 AP 热点吗？支持 WPA3 吗？"
    answer: "可以。hostapd 开 2.4G（802.11n）与 5G（VHT 80 MHz）AP，iPhone 7 Plus 连入显示 VHT-NSS2 80 MHz；WPA3-SAE（ieee80211w=2、sae_pwe=0）以 iPhone 15 Pro 于 2.4 GHz 连入，MFP: yes（5 GHz 的 WPA3 未实测）。"
  - question: "AWUS036AX 和 AWUS036AXER 差在哪？该选哪张？"
    answer: "两者同为 RTL8832BU + rtw89_8852bu，能力矩阵一致，差在天线与接收：AXER 外置天线，同批测试跳频扫到 63 AP + 12 client（AX 为 14 AP + 4 client）。桌面固定选 AX，要长距离或最强接收选 AXER。"
draft: false
---

**重点摘要（TL;DR）**：Yopitek（ALFA Network 台湾经销）实测，AWUS036AX 在 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）免装驱动，双频 monitor 可用；2.4G 注入 96%、5G AP VHT80，端到端 .22000 通过，不支持 IBSS / mesh。

> 本文为 Yopitek 于**自有设备、自有办公室 Wi-Fi（SSID `YUPITEK`）、自有测试手机**上完成的产品兼容性与能力实测，对象为 ALFA **AWUS036AX**（Realtek RTL8832BU、Wi-Fi 6 2x2）。
> 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`；对照设备 Apple iPhone 7 Plus（WPA3 与 VIF 另测 iPhone 15 Pro）。
> ⚠️ **合法使用**：Monitor 与 Injection 仅限自己拥有或已取得授权的网络；AP 模式请遵守当地无线电法规。本文不涉及任何针对第三方网络的攻击操作。

---

## 1. 这张卡与测试平台

AWUS036AX 是 ALFA 这一代的 Wi-Fi 6 USB 网卡，采 Realtek RTL8832BU 芯片、2x2 双空间串流，支持 2.4 GHz 与 5 GHz 双频。在 ALFA 的产品线里，它和外置天线版的 AWUS036AXER 共用同一颗芯片与同一支驱动，差别在天线形式与接收增益；跟同属 Wi-Fi 6 的 MediaTek 款 AWUS036AXM / AXML 则是完全不同的芯片路线，实测结论也差很多（第 5 节会交代）。

这次测试不谈规格书上的理论速率，只回答经销与工程现场最在意的三件事：在新版 Linux 上好不好装？哪些无线能力真的能用？哪些是驱动天生做不到、不该白花时间的？结论要能复现，所以所有指令都在 2026-11-18 当天于 GX10 实机逐条跑过，下文的「实测输出」都是真实节录（MAC 地址以 `xx` 屏蔽）。

测试边界先说清楚：全程在自家办公室、对自有的 `YUPITEK` 网络与自有手机进行。Monitor 只收自己环境的数据包，Injection 与 handshake 只对自家 AP 与自家 iPhone 操作。目的是验证「这张卡在这台机器上能做到什么」，不是示范攻击第三方网络。

---

## 2. 硬件与驱动（Wi-Fi 6，免装）

这代最实际的好处是：**插上即认、免编译、免 DKMS**。RTL8832BU 的 `rtw89_8852bu` 驱动已经是 kernel 6.17 的 in-kernel 模块，GX10 开机就绑好，不必再去 GitHub 抓 out-of-tree 项目手动编。

芯片信息与验证步骤如下。先用 `lsusb` 确认卡以 WLAN 模式枚举：

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

预期会看到 `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`。本测试单位的这张卡直接以 WLAN 模式现身，没有卡在光盘（CD-ROM）模式；若你拿到的卡显示 `0bda:1a2b`，代表它还在光盘模式，用 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN 即可。

接着确认驱动与固件加载：

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

实机加载的是 `rtw89/rtw8852b_fw-1.bin`，firmware version `0.29.29.5`。驱动与固件都随 kernel 内置，不需要另外安装套件。

最后一步是先看清楚这颗驱动**声明支持哪些接口模式**，这一步会直接决定后面哪些能力有、哪些是 N/A：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

实机列出的是 `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`。清单里看不到 IBSS、mesh point 和 active-monitor。这不是设置没调对，而是 `rtw89_8852bu` 本来就没做这三个模式，第 4 节会据此标成 N/A。

---

## 3. 实测能力：Monitor / Injection / AP / WPA3

先给一张能力总表，每一格都对应下面的实测节录：

| 能力 | 2.4 GHz | 5 GHz | 实测节录 |
|---|---|---|---|
| **Monitor** | ✅ 强 | ✅ 强 | airodump 跳频 60 秒扫到 **14 AP + 4 client** |
| **Injection** | ✅ **96%** | ✅ 可用 | 2.4G `aireplay-ng --test` 29/30（96%）；5G 逐台 `Injection is working!` |
| **AP 热点** | ✅ 802.11n（HT） | ✅ **VHT 80 MHz** | iPhone 7 Plus 连入：2.4G MCS 12、5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | 未实测 | iPhone 15 Pro 连入，MFP: yes（`sae_pwe=0`）；仅在 2.4 GHz 实测 |
| **WPA handshake 截取** | ✅ **端到端** | — | deauth 自有 iPhone → 截取完整 4-way → 转 hashcat `.22000` |

**Monitor（监听模式／接收）✅ 强。** 切到 monitor 后，2.4 GHz 与 5 GHz 都收得到大量数据包（各约 100 封/6 秒）。用 `airodump-ng --band abg` 跳频扫 60 秒，实测找到 14 个 AP 加 4 个 client，接收表现和 ALFA Wi-Fi 5 的 ACM / ACHM 同级，远胜 MediaTek MT7921 那两张（AXM / AXML 实测接收偏弱）。对现场勘查、通道占用盘点这类工作，这张卡的接收够用。

**Injection（数据包注入）✅ 可用，这也是 AX 对上 MediaTek 款的关键差异。** 2.4 GHz（ch6）跑 `aireplay-ng --test`，实测 `29/30: 96%`、`Injection is working!`，回应率 96%。5 GHz（ch36）对广播测试可能回 `Found 0 APs`（现代 AP 不回广播 probe，属正常），但逐台指定 AP BSSID 测就会回 `Injection is working!`，确认 5 GHz 注入可用。相对地，同样是 Wi-Fi 6 的 MediaTek AXM / AXML 在本平台**注入直接失败**（主因是 kernel 6.16 以后的 mac80211 chanctx 回归，另有固件把注入速率锁在 1/6 Mbps，并非芯片本身的限制），这点在选型时务必分清楚。

**AP 热点 ✅ 双频可开，5 GHz 上得了 VHT80。** 用 hostapd 起 AP，2.4 GHz 开 802.11n（`ieee80211n=1`、HT20），iPhone 7 Plus 连入后显示 MCS 12、authorized；5 GHz 开 VHT 80 MHz（`vht_oper_chwidth=1`、`ht_capab=[HT40+]`），iPhone 7 Plus 连入后显示 VHT-NSS2 80 MHz、authorized。两频都能稳定带起用户端，80 MHz 带宽也确实协商成功。

**WPA3-SAE ✅（2.4 GHz；5 GHz 未实测）。** 把 AP 的 `wpa_key_mgmt` 改成 `SAE`、`ieee80211w=2`，实测 iPhone 15 Pro 连入，MFP（Management Frame Protection）显示 yes。这里有个兼容性细节：`sae_pwe` 要设 `0`（Hunting-and-Pecking），旧款 iPhone 才连得上。

**WPA handshake 截取 ✅ 端到端成功。** 在自家 `YUPITEK` 网络、对自有 iPhone 7 Plus 走完整流程：monitor 侧录该通道 → `aireplay-ng -0` 送 deauth 触发重连 → `airodump-ng` 截取到完整四次握手（M1/M2/M3/M4）→ 用 `hcxpcapngtool` 转出 hashcat 的 `.22000` 格式。因为这张卡注入可用，整条链路才跑得通；注入失败的卡（如 AXM / AXML）到 deauth 这步就断了。这条握手（handshake）截取链用到的 Kali 常用工具（aircrack-ng、hcxtools）都直接在 Ubuntu 24.04 ARM64 上运行。

---

## 4. 高级与限制（rtw89 驱动的 N/A 项）

这一节把「能做的高级功能」与「驱动天生做不到的」一次讲白，避免现场白花时间。

| 功能 | 状态 | 说明 |
|---|---|---|
| **VIF（STA + AP 并行）** | ✅ | 主接口连 `YUPITEK`，同时开 AP VIF（ch36 VHT80），两接口并行；STA 端 ping 3.2 ms |
| **WPA handshake 截取** | ✅ 端到端 | 截取 M1–M4，`hcxpcapngtool` 转出 `.22000` |
| **Active monitor** | **N/A** | `rtw89_8852bu` 不具此模式（不在 `iw phy` 的 supported modes） |
| **Ad-hoc（IBSS）** | **N/A** | 驱动不支持 |
| **Mesh（802.11s）** | **N/A** | 驱动不支持 |
| **Wi-Fi Direct（P2P）** | ⬜ 未测 | 驱动声明支持，但需第二台设备，本次略过 |

**VIF ✅。** 建一个 AP 虚拟接口（不同 MAC、unmanage），主接口保持连 Wi-Fi，同通道开 AP。实测主接口连 `YUPITEK` 的同时，AP VIF 在 ch36 跑 VHT80，两个接口并行运作，STA 端 ping 3.2 ms。对「一边连上网、一边开测试热点」的场景可行。

**Active monitor / IBSS / Mesh 是 N/A，不是坏掉。** 这三个模式没有出现在第 2 节 `iw phy info` 的 supported interface modes 里，代表 `rtw89_8852bu` 这支驱动根本没实作。`sudo iw dev $IF set type ibss` 之类的指令会直接失败，而且没有解法：这不是参数或固件能救的，要用到这三个模式就得换芯片路线（例如 MediaTek mt76 的 ACM / ACHM 在单机下可建 IBSS / mesh）。

**一个平台层级的限制要先知道：hcxdumptool 在 GX10 上 `failed to arm`。** 这不是 AX 专属问题。`hcxdumptool 8.x` 需要 active-monitor，而 GX10 内置三频网卡，USB 卡枚举时容易被 `-I` 误映射到内置 phy，所有受测 USB 卡在这台机器上都会 arm 失败（唯一例外是 AWUS036EACS 在 2.4 GHz）。实务做法是**改用 aircrack-ng 套件**（airodump-ng + aireplay-ng）跑截取，本卡注入可用，整条链路照样端到端走完（见第 3 节）。

**安全守则（GX10 平台共通）：** 绝对不要跑 `airmon-ng check kill`，它会关掉 NetworkManager 让 GX10 对外断线；操作时只动 `wlx*` 接口，不要碰内置的对外上网主线网卡。

---

## 5. 适用情境与选型（Wi-Fi 6 AP 热点，连回 Hub）

把实测结论换成选型建议：**AWUS036AX 的甜蜜点是「Wi-Fi 6 + AP 热点」且同时需要注入能力的场景。**

| 用途 | AWUS036AX 适合度 | 说明 |
|---|---|---|
| Wi-Fi 6 AP 热点 / 边缘接取 | ★ 首选 | 2x2 VHT80 双频可开，WPA3-SAE 可用 |
| Injection + handshake 审核 | ★ 可胜任 | 2.4G 96%、5G 可用、端到端截取成功 |
| 最强接收 / 长距离 monitor | ○ 够用，但首选 AXER | 同芯片的 AXER 外置天线、接收更强 |
| mesh / IBSS 实验 | ✗ 不适用 | 驱动 N/A，改选 mt76 的 ACM / ACHM |

**典型部署：当成 Wi-Fi 6 热点，让边缘设备连回中央 Hub。** 用实测过的 AP（VHT80）与 VIF 能力，把 GX10 搭这张卡布成一个 Wi-Fi 6 接取点，测试手机、IoT 传感器这类边缘设备连上后，流量再经主接口回到中央 Hub（gateway）。VIF 实测已证明「主接口连回上层网络」和「对下开 AP」能并行，STA 端延迟 3.2 ms，这个拓扑在本平台验证过可行。边缘接取段要再上现代加密，加 WPA3-SAE 即可。

**选型避雷：要注入 / handshake 用途，别挑 AWUS036AXM / AXML。** 这两张虽然同为 Wi-Fi 6 2x2、AP 也开得起来，但 MediaTek MT7921 在本平台**注入失败**，无法 deauth、截取不到 handshake。若客户只是要一张单纯的 Wi-Fi 6 AP / 一般连接卡、完全不碰注入，MediaTek 款稳定也无妨；但只要用途沾到无线审核，就该选 Realtek 的 AX（或外置天线的 AXER）。

**和同芯片的 AXER 怎么分？** 两者芯片、驱动、能力矩阵一致；AXER 是外置天线版，接收与长距离 monitor 更强（同批测试中 AXER 跳频扫到 63 AP + 12 client）。桌面固定、天线需求不高就选 AX；要拉距离、要最强接收就上 AXER。

---

## 常见问题（FAQ）

**Q：AWUS036AX 在 Ubuntu 24.04 ARM64 要装驱动吗？lsusb 显示 0bda:1a2b 怎么办？**
在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8832BU 由内置 rtw89_8852bu 驱动，免编译、免 DKMS。若 lsusb 显示 `0bda:1a2b`（光盘模式），运行 `sudo usb_modeswitch -v 0bda -p 1a2b -K` 切成 WLAN。

**Q：AWUS036AX 支持 monitor mode（监听模式）与数据包注入吗？**
支持。2.4 GHz 注入 29/30（96%）；5 GHz 逐台指定 AP 测试回 `Injection is working!`；airodump-ng 跳频 60 秒扫到 14 个 AP 与 4 个 client。不支持 active monitor、IBSS、mesh。

**Q：AWUS036AX 能截取 WPA handshake（握手数据包）？MT7921 的 AXM / AXML 行吗？**
AX 能：自有 AP 加自有 iPhone 7 Plus，`aireplay-ng -0` 触发重连、`airodump-ng` 截取完整 M1–M4，`hcxpcapngtool` 转出 .22000。MT7921 的 AXM / AXML 在本平台注入失败，做不到。仅限自有或已授权网络。

**Q：AWUS036AX 可以当 AP 热点吗？支持 WPA3 吗？**
可以。`hostapd` 开 2.4G（802.11n）与 5G（VHT 80 MHz）AP，iPhone 7 Plus 连入显示 VHT-NSS2 80 MHz；WPA3-SAE（ieee80211w=2、sae_pwe=0）以 iPhone 15 Pro 于 2.4 GHz 连入，MFP: yes（5 GHz 的 WPA3 未实测）。

**Q：AWUS036AX 和 AWUS036AXER 差在哪？该选哪张？**
两者同为 RTL8832BU + rtw89_8852bu，能力矩阵一致，差在天线与接收：AXER 外置天线，同批测试跳频扫到 63 AP + 12 client（AX 为 14 AP + 4 client）。桌面固定选 AX，要长距离或最强接收选 AXER。

---

## 6. 延伸阅读

- 〈9 款 ALFA 无线网卡 ASUS GX10 + Ubuntu ARM64 能力总表〉—— 全型号 Monitor / Injection / AP / handshake 一次对照 → [总表 Hub](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [免装驱动：Ubuntu 24.04 + kernel 6.17 用 in-kernel 驱动激活 Monitor 与 AP](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)——rtw88 / rtw89 / mt76 共通设置流程
- [AWUS036AXER 逐卡实测](/zh-cn/blog/awus036axer-asus-gx10-ubuntu-test-report/)——同芯片外置天线版，接收与长距离 monitor 对比
- [WPA3-SAE handshake 截取能力实测与 sae_pwe 兼容性](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)——iPhone 连接的 `sae_pwe` 雷区

---

*测试单位：Yopitek（ALFA 经销）— https://www.yupitek.com ｜ 测试环境：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 ｜ 对照设备：Apple iPhone 7 Plus（WPA3 / VIF 另测 iPhone 15 Pro）*
