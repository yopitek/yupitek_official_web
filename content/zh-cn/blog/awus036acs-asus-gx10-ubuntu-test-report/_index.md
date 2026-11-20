---
title: "AWUS036ACS 逐卡实测：RTL8811AU 轻量随身卡在 ASUS GX10 + Ubuntu 24.04（ARM64）的兼容性与能力报告"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS 在 Ubuntu 24.04 ARM64 实测：免装驱动，Monitor、注入（2.4G 100%、5G 96%）、AP、WPA3-SAE 与端到端 handshake（.22000）皆通过。平台 ASUS GX10、kernel 6.17、RTL8811AU。"
faq:
  - question: "AWUS036ACS 在 Ubuntu 24.04 ARM64 要装驱动吗？"
    answer: "在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8811AU 由内置 rtw88_8821au 驱动，插上即认，免编译、免 DKMS。kernel 较旧时，先用 modinfo rtw88_8821au 确认模块存在。"
  - question: "AWUS036ACS 支持 monitor mode 和 packet injection 吗？"
    answer: "支持。2.4 GHz、5 GHz 都能 monitor；aireplay-ng --test 注入 2.4G 为 100%（30/30）、5G 为 96%（29/30，需先 iw reg set US 解除 TW 限制）。不支持 active monitor。"
  - question: "AWUS036ACS 能截取 WPA handshake 并转成 hashcat .22000 吗？"
    answer: "能。在自有 AP 与自有 iPhone 7 Plus 上端到端实测：定向 deauth 触发重连，截取完整 4-way（M1–M4），再用 hcxpcapngtool --all 转出 .22000。仅限自己拥有或已授权的网络。"
  - question: "AWUS036ACS 可以当 AP 热点吗？支持 WPA3 吗？"
    answer: "可以。hostapd 开 2.4G 与 5G 热点（5G 频宽未确认），iPhone 7 Plus 连入并完成 4-way；5G 的 WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）也连入成功（2.4G 的 WPA3 未实测）。"
  - question: "AWUS036ACS 不支持哪些模式？hcxdumptool 能用吗？"
    answer: "不支持 active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）。hcxdumptool 8.x 会 failed to arm interface，请改用 airodump-ng + aireplay-ng。要 mesh / IBSS 请选 AWUS036ACM / ACHM。"
draft: false
---

**重点摘要（TL;DR）**：Yupitek（ALFA Network 台湾经销）实测，AWUS036ACS 在 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）免装驱动，双频 monitor 与 AP（5G AP 可用，频宽未确认）可用；注入 2.4G 100%、5G 96%，端到端 .22000 通过，不支持 mesh / IBSS。

> 本文是 Yupitek 针对 ALFA AWUS036ACS 在新版 Linux 平台上的产品兼容性与能力实测纪录，供评估选型用。
> 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有数据均为 Yupitek 于**自有设备、自有办公室 Wi-Fi**（SSID `YUPITEK`，2.4G ch5 / 5G ch36）对**自有测试手机**（Apple iPhone 7 Plus）的实测节录，MAC 地址部分屏蔽。
> ⚠️ **合法与范围声明**：Monitor、Injection、handshake 截取仅于自己拥有或已取得授权的网络与设备上进行；AP 模式请遵守当地无线电法规。本文聚焦网卡本身的能力、兼容性与设置，**不涉及针对第三方网络的任何攻击操作**。

---

## 1. 这张卡与测试平台

AWUS036ACS 是 ALFA 产品线里的轻量随身型无线网卡，芯片是 Realtek RTL8811AU，Wi-Fi 5（802.11ac）世代、1x1 单空间流。定位很直白：体积小、功耗低、单天线，是带出门做现场盘点的卡，不是拼最高吞吐或最远距离的重装卡。所以评估它的时候，问题不在「它多快」，而在「这么轻的规格下，哪些实务能力还是完整可用」。

这一轮测试把它摆进一个典型的维运情境：GX10 的内置网卡（`wlP9s9`）负责对外上网，AWUS036ACS 走 USB 外置，只扛测试任务。这样切 Monitor 或 AP，都动不到主机自己的网络。全程只碰 ALFA 卡对应的 `wlx*` 接口，不去动内置的对外网卡。

| 项目 | 内容 |
|---|---|
| 型号 | AWUS036ACS |
| 芯片 | Realtek RTL8811AU（Wi-Fi 5 / 802.11ac，1x1 单串流） |
| USB ID | `0bda:0811` |
| 驱动 | `rtw88_8821au`（in-kernel，kernel 6.17 内置） |
| 固件 | 42.4.0（实测 dmesg） |
| 平台 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 测试设备 | Apple iPhone 7 Plus |

---

## 2. 硬件与驱动（免装）

这张卡在 GX10 上插上就认，不必编译、也不用 DKMS。RTL8811AU / RTL8821AU 这颗芯片自 mainline kernel 6.13 起正式并入 Realtek 的 in-kernel `rtw88` 驱动家族，GX10 搭的 6.17 已内置 `rtw88_8821au` 模块，不需要再去 GitHub 抓任何 out-of-tree 项目。（与旧版安装指南不同：早期站文以 `morrownr` out-of-tree 驱动或较旧 kernel 为前提，称需自行 DKMS 编译；在 kernel 6.17 的 in-kernel 驱动下这已不再需要。）过去常见的 `morrownr/8821au-20210708` 现在已转为 legacy（只建议低于 6.13 的内核使用，而且装了它会把内置驱动 blacklist 掉），新 kernel 上没必要再走这条旧路。维运成本上的好处更实在：in-kernel 驱动跟着 kernel 一起更新，用户不必各自维护分支，也不会每次升级就卡在 DKMS 编译失败，同一套操作跨好几次 kernel 更新都能重复用。固件由 `linux-firmware` 随系统带，本机实测是 42.4.0，一样不用手动处理。

确认卡片已被辨识、驱动已绑定、接口也生出来了：

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

固件版本可从 `dmesg` 确认（实测为 42.4.0）：

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

声明支持的接口模式（这决定后面哪些能力能用）：

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

这份清单列出了 `IBSS / managed / AP / AP/VLAN / monitor`。这里要特别提醒：虽然清单列了 IBSS，实测 `ibss join` 之后 `iw link` 却显示 Not connected，连不起来；mesh、active-monitor、P2P 则根本不在清单上（详见第 4 节限制）。这是 RTL8811AU 的硬件与驱动现况，跟天线数无关。

频段涵盖：2.4 GHz ch1–13（ch14 disabled）；5 GHz ch36–165（其中 ch52–144 标记 radar / DFS）。默认 regdomain 为 `TW`，TX 功率 2.4 GHz 30 dBm、5 GHz UNII-1/2 23 dBm、UNII-3 30 dBm。

---

## 3. 实测能力：Monitor / Injection / AP / WPA3

先看内核能力总表，再逐项展开。所有项目都在自有 YUPITEK AP + 自有 iPhone 7 Plus 上完成。

| 能力 | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor（监听接收） | ✅ 强 | ✅ 强 |
| Injection（数据包注入） | ✅ **100%**（30/30） | ✅ **96%**（29/30，需先解锁 reg） |
| AP 热点（hostapd） | ✅ iPhone 连入 + 完成 handshake | ✅ **稳定**（频宽未确认） |
| AP WPA3-SAE | 未实测 | ✅ iPhone 连入（SAE-only + PMF） |

### 3-1. Monitor（监听模式，2.4 GHz + 5 GHz）✅

切到 monitor 后，六个频道各做一次定长截取，接收都正常。热门频道在 6 秒内即达 300 帧的截取上限：

| 频道 | 截取 frames |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

2.4 GHz 与 5 GHz 都收得稳。对一张单天线的随身卡来说，这个接收表现足以应付现场频道盘点和数据包诊断。ch11、ch149、ch157 的帧数偏低，是那几个频道当下空中流量本来就少，不是网卡收不到；热门的 ch1、ch6、ch36 六秒内就打满 300 帧上限，接收显然不是它的瓶颈。

### 3-2. Injection（数据包注入）✅

以 `aireplay-ng --test` 对自家 YUPITEK AP 做定向注入测试。2.4 GHz 达 100%（30/30，`Injection is working!`），5 GHz 则是 96%（29/30）。5 GHz 有个设置细节要留意：默认 `reg=TW` 会锁住部分 UNII 频段的主动发送，测试前先 `sudo iw reg set US` 解锁、测完再 `sudo iw reg set TW` 设回。

```bash
# 2.4 GHz (YUPITEK 实际在 ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

单天线卡能在 2.4 GHz 拿到 100%、5 GHz 拿到 96%，已经是相当可靠的注入能力，这也是它能完成后面端到端 handshake 截取的基础。

### 3-3. AP 热点（2.4 GHz / 5 GHz）✅

用 `hostapd` 把卡变成基地台，三种设置都让 iPhone 7 Plus 成功连入并完成 4-way handshake（`EAPOL-4WAY-HS-COMPLETED`）：

- **5 GHz（频宽未确认）**：最稳定的一组，iPhone 连入、handshake 完成、`AP-DISABLED` 干净收尾。
- **2.4 GHz（WPA2-PSK）**：iPhone 连入、handshake 完成，断线后干净关闭。这里诚实记一个状况：前一轮同样设置，曾在 STA 断线后出现 `key not allowed / Failed to set beacon parameters` 而中止，重测却无法重现，判定是 rtw88_8821au 偶发的 beacon re-key，不是固定瑕疵。长时间、高频率重连的场景还是建议留意，或干脆改用 5 GHz AP。
- **WPA3-SAE（5 GHz，PMF 强制；2.4 GHz 未实测）**：关键设置为 `wpa_key_mgmt=SAE`（纯 WPA3、无 WPA2 fallback）、`ieee80211w=2`（强制 Management Frame Protection）、`sae_pwe=0`（兼容旧端点）。iPhone 7 Plus（iOS 15）以 SAE 成功连入。AP 只开 SAE、没有 WPA2 退路，能完成关联就代表 SAE 认证握手成立。RTL8811AU + rtw88_8821au 在 AP 端的 WPA3-SAE 可用。

---

## 4. 端到端 handshake 能力与限制

### 4-1. 端到端 handshake 截取 ✅

这是验证注入加截取能不能真正「串起来」的综合测试，全程在自有 YUPITEK AP、自有 iPhone 7 Plus、已授权的前提下进行。流程是：monitor 到目标频道 → 对自有设备送定向 deauth 触发重连 → 截取完整的 4-way（M1–M4）→ 用 `hcxpcapngtool --all` 转出 hashcat 可读的 `.22000`。

实测结果：`aircrack-ng` 判定 YUPITEK 取得 1 个 handshake，EAPOL 四个消息 M1–M4 全到齐，client 为 Apple OUI（`b8:53:ac`，确认是 iPhone 7 Plus），转出的 `.22000` 可直接喂 hashcat。这代表 AWUS036ACS 具备完整的端到端 handshake 截取能力。

两个实测要点值得记录（完整逐步设置另见专文）：

1. **办公室同频有多台同名 AP 时，不要用 `--bssid` 锁单一台**，改截取整个频道，才不会漏掉连在另一台上的设备。
2. `hcxpcapngtool` 默认较严格，可能回「not enough M1」；加 `--all` 即可由完整 M1–M4 转出 `.22000`。

这条握手（handshake）截取链所用的 Kali 常用工具（aircrack-ng、hcxtools）都是直接在 Ubuntu 24.04 ARM64 上运行，airodump-ng、aireplay-ng、hcxpcapngtool 皆正常运作。

### 4-2. VIF（虚拟接口）✅

`iw dev $IF interface add mon9 type monitor` 可创建 monitor VIF 并截取到 100 frames；另以脚本创建「主接口连 YUPITEK 当 STA + 一个 AP VIF」，单芯片可同时扮演 STA 与 AP。

### 4-3. 诚实限制（实测回报）

| 高级模式 / 工具 | 状态 | 实测 |
|---|---|---|
| Active monitor | ❌ 不支持 | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc（IBSS） | ❌ 不支持 | 模式列出但 `ibss join` 后 `iw link` = Not connected |
| Mesh（802.11s） | ❌ 不支持 | `set type mp` → `-95` |
| Wi-Fi Direct（P2P） | ❌ 不支持 | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ 无法 arm | `failed to arm interface`：rtw88_8821au 不提供 active-monitor；改用 airodump-ng + aireplay-ng |

另外还有两个维运面的限制要知道。单串流 1x1 决定了它的理论上限（HT Max RX 150 Mbps、VHT80 约 433 Mbps），吞吐本来就不是它的强项。反复切换 monitor / AP 之后，RX 偶尔会短暂 degraded（扫不到东西），这时实体拔插一次卡就能复原，接口名称由 MAC 决定，拔插后维持不变。

---

## 5. 适用情境与选型（轻量随身，连回 Hub）

把上面这些能力对回产品定位，AWUS036ACS 的角色很清楚：一张能力完整、但主打轻便的随身卡。那它适合用在哪些情境？

- **现场快速盘点 / 随身诊断**：单天线、小体积、低功耗，带出门做频道盘点、信号巡检、数据包诊断都合用。搭配 GX10 这类中央平台，随身卡在现场截取，把数据连回 Hub 做集中分析，分工清楚。
- **教学与验证**：Monitor / Injection / AP / WPA3-SAE / 端到端 handshake 这条主线它全数走得通，适合当示范与授权范围内的验证用卡。
- **不适合的情境**：需要最高吞吐、最远距离，或需要 mesh / IBSS / P2P / active-monitor 的场景，这张卡不是对的选择。

轻量不等于功能缩水。主线能力它一条都没少，被取舍掉的是吞吐天花板和高级接口模式。所以选不选它，看你要的是「带着走」还是「跑得满」。

和同家族相比，定位差异如下：

| 需求 | 建议卡 | 理由 |
|---|---|---|
| 轻量随身 + 主线能力完整 | **AWUS036ACS** | 2.4G 注入 100%、5G 96%、端到端 handshake 可用，单天线轻便 |
| 双频注入都要 100% / 更稳的渗透验证 | AWUS036EACS、AWUS036ACH | 两频注入 100%，EACS 另含 BT |
| 最强接收 / 长距离 monitor | AWUS036AXER、AWUS036ACH | 跳频扫到更多目标 / 双天线高增益 |
| mesh / IBSS 单机实验 | AWUS036ACM、AWUS036ACHM | mt76 驱动单机可创建（Realtek rtw88 不支持） |

一句话选型：要轻便、又要主线能力齐全，AWUS036ACS 是合适的随身选择；要双频注入都 100%、或更重的渗透验证，就往 EACS / ACH 走。

---

## 常见问题（FAQ）

**Q：AWUS036ACS 在 Ubuntu 24.04 ARM64 要装驱动吗？**
在本文测试的 kernel 6.17（ASUS GX10）上不用：RTL8811AU 由内置 rtw88_8821au 驱动，插上即认，免编译、免 DKMS。kernel 较旧时，先用 `modinfo rtw88_8821au` 确认模块存在。

**Q：AWUS036ACS 支持 monitor mode（监听模式）和 packet injection（数据包注入）吗？**
支持。2.4 GHz、5 GHz 都能 monitor；`aireplay-ng --test` 注入 2.4G 为 100%（30/30）、5G 为 96%（29/30，需先 `iw reg set US` 解除 TW 限制）。不支持 active monitor。

**Q：AWUS036ACS 能截取 WPA handshake（握手数据包）并转成 hashcat .22000 吗？**
能。在自有 AP 与自有 iPhone 7 Plus 上端到端实测：定向 deauth 触发重连，截取完整 4-way（M1–M4），再用 `hcxpcapngtool --all` 转出 .22000。仅限自己拥有或已授权的网络。

**Q：AWUS036ACS 可以当 AP 热点吗？支持 WPA3 吗？**
可以。`hostapd` 开 2.4G 与 5G 热点（5G 频宽未确认），iPhone 7 Plus 连入并完成 4-way；5G 的 WPA3-SAE（SAE-only、ieee80211w=2、sae_pwe=0）也连入成功（2.4G 的 WPA3 未实测）。

**Q：AWUS036ACS 不支持哪些模式？hcxdumptool 能用吗？**
不支持 active monitor、IBSS、mesh（802.11s）、Wi-Fi Direct（P2P）。hcxdumptool 8.x 会 failed to arm interface，请改用 airodump-ng + aireplay-ng。要 mesh / IBSS 请选 AWUS036ACM / ACHM。

---

## 6. 延伸阅读

- 九张 ALFA 卡的完整能力比较与选型总评 → [ALFA 无线网卡总评 Hub（总表）](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [免装驱动：Ubuntu 24.04 + kernel 6.17 激活 Monitor / AP（rtw88 / rtw89 / mt76 实测）](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [WPA3-SAE 与端到端 handshake 截取逐步教学](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 同家族 BT+WiFi 复合卡 → [AWUS036EACS 逐卡实测](/zh-cn/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*测试单位：Yupitek（ALFA Network 台湾经销）— https://www.yupitek.com ｜ 测试环境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 测试设备：Apple iPhone 7 Plus*
