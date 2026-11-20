---
title: "AWUS036ACH 单卡实测：Realtek RTL8812AU 双天线 AC1200 在 ASUS GX10（ARM64 / Ubuntu 24.04）的 Monitor・Injection・AP・WPA3 全测报告"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "AWUS036ACH（RTL8812AU）在 Ubuntu 24.04 / kernel 6.17 免装 DKMS，双频监听模式可用、数据包注入 100%，端到端 WPA handshake（.22000）已实证，并附 5G 接收卡死等限制。"
faq:
  - question: "AWUS036ACH 在 Kali 或 Ubuntu 需要装驱动吗？"
    answer: "看内核版本。Linux 内核 6.13 以上（本次实测 Ubuntu 24.04 / kernel 6.17）已内置 rtw88_8812au 驱动，插上即认、免编译、免 DKMS；内核低于 6.13 才需要另外用 DKMS 安装 lwfinger/rtw88。Kali 请先用 uname -r 确认内核版本，本次未在 Kali 实机验证。"
  - question: "AWUS036ACH 的 monitor mode 与数据包注入表现如何？"
    answer: "2.4GHz 与 5GHz 都能进 monitor mode；aireplay-ng 逐台定向注入在 2.4GHz（对 4 台 AP）与 5GHz（对 YUPITEK ch36）都是 30/30 = 100%。5GHz 注入前要先把法规网域设成允许发射的设置（例如 iw reg set US），默认 country 00 下 5GHz 禁止发射，注入会送不出去。"
  - question: "AWUS036ACH 可以截取 WPA handshake 吗？"
    answer: "可以，且端到端已实证。两频注入都是 100%；2026-11-19 补测在自有 iPhone 15 Pro、5GHz ch36 上撷到完整 4-way 交握，并用 hcxpcapngtool 转出 47 笔 hashcat .22000 hashline。仅限自有或已取得授权的网络。"
  - question: "AWUS036ACH 开 WPA3 热点，iPhone 7 Plus 连不上怎么办？"
    answer: "hostapd 要设 sae_pwe=0 并搭配 ieee80211w=2，iPhone 7 Plus 才连得上；用 sae_pwe=2 会连不上。同样的设置在 AWUS036ACHM 上也是关键。"
  - question: "AWUS036ACH 的 5GHz 接收突然卡死（抓到 0 数据包）怎么办？"
    answer: "这是 rtw88_8812au 的已知现象：反复切换模式或变更法规网域后，5GHz 接收可能卡死，软件无法复原，只能实体拔插或重开机。建议 5GHz 测试前先重新插卡，并优先完成 5GHz 项目。"
draft: false
---

> 测试单位：Yopitek（ALFA Network 台湾经销）｜测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia｜测试设备：自有 Apple iPhone 7 Plus｜测试对象：自有办公室 Wi-Fi（SSID `YUPITEK`，2.4G ch5 / 5G ch36、157）｜测试日期：2026-11-18。
>
> 本文属经销商对产品兼容性与能力边界的硬件验证：所有 Monitor / Injection / AP / handshake 量测，皆于 Yopitek 自有设备、自有办公室 Wi-Fi、对自有测试手机进行，不针对任何第三方网络，亦不提供对外部网络的攻击操作步骤。文中数据皆为实机量到的数字与状态，不以规格书推测。

## 重点摘要（TL;DR）

AWUS036ACH 于 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）实测：双频 monitor 可用，两频逐台数据包注入均为 30/30 = 100%，双频均可架设 AP 热点（纯 802.11g / 纯 802.11a）。

- kernel 6.13 以上免装 DKMS（本次 Ubuntu 24.04 / kernel 6.17），rtw88_8812au 内置、插上即认。
- 双频监听模式（monitor mode）可用，两频逐台数据包注入都是 30/30 = 100%。
- 端到端 WPA handshake 已实证：2026-11-19 补测在自有 iPhone 15 Pro、5G ch36 撷到完整 4-way，转出 47 笔 .22000 hashline。
- 5GHz 接收可能卡死，只能实体拔插或重开机。
- 单机可创建 IBSS，但不支持 802.11s mesh、active monitor 与 Wi-Fi Direct（P2P）。

## 1. 这张卡与测试平台

AWUS036ACH 是 ALFA Network 定位在「双天线高增益」的 USB 无线网卡，采用 Realtek RTL8812AU 芯片，规格为 Wi-Fi 5（802.11ac）、2T2R、双频 AC1200。相较于同系列单天线的 AWUS036ACHM（MediaTek MT7610U，AC600），ACH 以两根外置高增益天线换取更好的接收与较稳的 injection 表现，是客户询问「长距离 monitor」与「两频注入」时的常见候选。

本次测试平台与条件如下：

- 运算平台：ASUS GX10（ARM64 / aarch64）
- 操作系统：Ubuntu 24.04 LTS
- 内核版本：kernel 6.17.0-1014-nvidia
- 测试设备：Apple iPhone 7 Plus（2.4G / 5G / WPA3 皆以此机实测）
- 测试环境：自有办公室 Wi-Fi，SSID `YUPITEK`（2.4GHz ch5 / 5GHz ch36、ch157）
- 测试日期：2026-11-18 实机量测

全程只操作 ALFA 卡对应的 `wlx*` 接口，不碰 GX10 对外上网的内置网卡，也不运行 `airmon-ng check kill`（该指令会关掉 NetworkManager，导致主机断线）。

## 2. 硬件与驱动（芯片 / USB ID / in-kernel 免装）

| 项目 | 规格 |
|---|---|
| 型号 | AWUS036ACH |
| 芯片 | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| 驱动 | `rtw88_8812au`（kernel 内置，mainline ≥ 6.13） |
| 固件 | `rtw88/rtw8812a_fw.bin`（系统内附） |
| 世代 / 串流 | Wi-Fi 5（802.11ac）/ 2T2R |
| 带宽等级 | 双频 AC1200 |
| 天线 | 双天线高增益（外置） |
| USB 接口 | USB 3.0（实测枚举为 5000M） |

ACH 在 GX10 的 6.17 kernel 上是真正的随插即用：`lsusb` 认到 `0bda:8812`，驱动 `rtw88_8812au` 自动绑定，固件 `rtw8812a_fw.bin` 系统已内附，免编译、免 DKMS。这一点对 ARM64 环境特别重要。许多旧的 out-of-tree Realtek 驱动在 aarch64 上得自源代码编译，而 morrownr/USB-WiFi 与 aircrack-ng/rtl8812au 这两个老项目现在都已改导向这颗内置驱动，bug 回报集中到 lwfinger/rtw88。因此 kernel ≥ 6.13（含 GX10 的 6.17）的用户不必再碰第三方 DKMS；只有旧 kernel（< 6.13）才需要另外 DKMS 安装 `lwfinger/rtw88`。这个上游项目目前仍在活跃维护（最新 commit 为 2026-10-24，内容包含 8812A 的蓝牙 1T1R 修正），代表这颗芯片在主线的支持还在持续更新，不是停更的老驱动。

硬件连接有一个细节要注意：ACH 是 USB-A 公头，请用 USB-C→A 转接头直插 GX10 的 USB-C 端口，走 USB 3.0（枚举显示 5000M）。若把它接在键鼠的 USB 2.0 hub 后面会被限速，量不出 USB3 的行为。

接口模式方面，`iw phy` 回报支持 IBSS / managed / AP / AP-VLAN / monitor，但没有 mesh、P2P 与 active-monitor，这条界线直接决定了第 4 节的部分限制。

## 3. 实测能力：Monitor / Injection / AP / WPA3

| 功能 | 2.4 GHz | 5 GHz | 实测数据 |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames；5G ch36/149/157 = 260/137/127 frames |
| Injection（广播探测） | ✅ | ✅ | `aireplay-ng --test` broadcast probe 两频皆回 Injection is working |
| Injection（逐台定向） | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G 对 4 台 AP（含 YUPITEK）；5G 对 YUPITEK ch36 |
| AP 热点（iPhone 7 Plus） | ✅ 纯 802.11g | ✅ 纯 802.11a（ch36） | 4-way handshake 完成，首次即连上 |
| WPA3-SAE AP | ✅（`sae_pwe=0`） | 未实测 | 搭 `ieee80211w=2`，iPhone 7 Plus 连上（仅在 2.4 GHz 实测） |

**Monitor**：2.4GHz 在 ch1 / ch6 / ch11 分别抓到 92 / 214 / 71 个 frame；5GHz 在 ch36 / ch149 / ch157 抓到 260 / 137 / 127 个 frame。两频 monitor 皆正常，5GHz 的收量甚至高于 2.4GHz（ch36 抓到 260 frame），与双天线高增益的定位相符。

**Injection**：这是 ACH 的强项。2.4GHz 下 `aireplay-ng --test` 先做 broadcast probe（回报 Injection is working、Found 4 APs），再逐台定向，对含 YUPITEK 在内的 4 台 AP 回应率都是 30/30 = 100%，min/avg/max RTT 约 4.9 / 39.2 / 99.0 ms、Power 约 -47。双天线 ACH 的 2.4G injection 比单天线 ACHM 明显更稳。实作上要记得加 `--ignore-negative-one`：这是 lwfinger/rtw88 #453 的已知现象：STA 接口开着时，monitor channel 可能回报 `-1`，不加这个旗标会被误判成注入失败。另外依上游纪录，重负载 injection 下内置 driver 偶有 USB reset，但本次约 90 秒的量测并未观察到。5GHz 下对 YUPITEK（ch36）逐台定向同样 30/30 = 100%，平均 RTT 13.6 ms、Power -69.1。这是在「新插卡 + regdomain 设为可 TX 的法规」前提下量到的结果（细节见第 4 节的 5G 注意事项）。

**AP 热点**：以 hostapd 开台，2.4GHz 走纯 802.11g（`ieee80211n=0`）、5GHz 走纯 802.11a（ch36），iPhone 7 Plus 两频都第一次就连上，没有 association 失败；log 可见 authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED 完整四步。实测经验是：ACH 在「关掉 802.11n、纯 g / 纯 a」的设置下连接最干净。

**WPA3-SAE**：开 SAE-only AP 时，关键参数是 `sae_pwe=0`（hunting-and-pecking）搭配 `ieee80211w=2`，iPhone 7 Plus 才连得上；若用 `sae_pwe=2` 会连不上。这与同系列 ACHM 踩到的是同一个兼容性雷点。

## 4. 高级能力与 handshake：可行范围与诚实限制

| 高级能力 | 结果 | 说明 / 证据 |
|---|---|---|
| VIF（STA + monitor 同时） | ✅ 实测可用 | 主接口 managed 与 `mon9`（monitor）同时 up，monitor VIF 8 秒抓 100 frame |
| WPA handshake 截取 | ✅ 端到端（.22000）已实证 | 两频注入 100%；2026-11-19 补测 5G ch36 撷到完整 4-way，hcxpcapngtool 转出 47 笔 `.22000` hashline |
| macchanger（改 MAC） | ✅ | 随机 MAC 设置与还原皆正常（需先 `ip link down`） |
| Ad-hoc（IBSS） | 🟡 单机 | 单机 `Joined IBSS` 成功；peer link 因无第二台设备未测 |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh（802.11s） | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct（P2P） | ❌ | `Operation not supported (-95)` |

**handshake 截取能力要讲清楚**：ACH 的两频 injection 都是 100%，而 injection 正是「deauth 自有测试手机 → 截取完整 4-way（M1–M4）→ 以 hcxpcapngtool 转出 hashcat `.22000`」这条端到端工作流的发动端。2026-11-19 补测在自有 iPhone 15 Pro、5GHz ch36 上撷到完整 4-way 交握，并以 hcxpcapngtool 转出 47 笔 `.22000` hashline，因此 ACH 的端到端 handshake 截取已实证。在我们 9 款卡的总表中，端到端（`.22000`）已实证的共 7 款：AWUS036ACM、AWUS036ACHM、AWUS036ACH、AWUS036ACS、AWUS036EACS、AWUS036AX 与 AWUS036AXER。所有截取仅限于自有或已取得授权的网络。

**VIF**：`iw phy` 的旗标写 interface combinations are not supported，但实机上 managed 主接口与另开的 monitor 接口 `mon9` 可以同时 up，`mon9` 在 8 秒内抓到 100 个 frame，也就是「边上网边侧录」在 ACH 上行得通。要提醒的是：phy 并未保证此组合，长时间或重负载情境建议改用 mt76 系列（ACM / ACHM）。

**三个要特别标注的限制：**

1. **不支持 Active monitor、Mesh（802.11s）与 Wi-Fi Direct（P2P）**：三者实测皆回 `Operation not supported (-95)`。需要这三项能力请改用 mt76 系列卡（ACM / ACHM 的 phy 有声明 mesh / P2P / active-monitor）。
2. **5G RX 卡死（`rtw88_8812au` 已知现象）**：刚插卡时 5G monitor / injection 正常，但反复切换模式或变更 regdomain 后，5G 接收可能卡死（抓到 0 数据包），且软件无法复原，只能实体拔插或重开机。建议做 5G 测试前先拔插一次、并优先完成 5G 项目。这里也补充 5G injection 能送出的前提：默认 `country 00` 下 5G 全是 passive / no-IR（禁止 TX），定向注入根本送不出去；要设成能 TX 的法规（`iw reg set US` 可解锁 ch36 / ch149，`TW` 只放行 ch149 以上、不含 ch36），测完再设回 `TW`。而「新插卡」指的是实体拔插到 USB 重新枚举：`dmesg` 要看到 `USB disconnect` 与 `renamed from wlan0`、bus 编号改变才算数；若 5G 已卡死，aireplay 会回 `No such BSSID available`。
3. **hcxdumptool 在本平台除 AWUS036EACS 的 2.4 GHz 外，其余卡皆 `failed to arm`**：因为它需要 active-monitor，而 rtw88 / rtw89 / mt7921u 都不支持；要截取 handshake 请改走 airodump-ng + aireplay-ng 这条路。

### 工具链兼容性（Kali）

针对 Kali 常用工具对 ACH 做了一轮快筛（环境目标为自有 `YUPITEK`），结果如下：

| 工具 | 状态 | 说明 |
|---|---|---|
| airmon-ng | ✅ | 正确列出 `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` 抓到 beacon（含 YUPITEK），20 packets captured |
| kismet | ✅ 已安装 | `/usr/bin/kismet`，可当 data source 启动 |
| bettercap | ✅ 已安装 | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | 已安装，但本平台 `failed to arm`（需 active-monitor，见上） |
| macchanger | ✅ | GNU 1.7.0；`-r` 随机、`-p` 还原，实测正常 |
| wifite | ❌ 未安装 | 本机无此指令，需另装（建议用 git 版，避开与自编 aircrack-ng 的 apt 依赖冲突） |

结论很单纯：airmon-ng 能正确辨识并管理 ACH，一般 monitor 与截取流程走 aircrack-ng 套件（airodump-ng + aireplay-ng）最稳定；需要 active-monitor 的 hcxdumptool 在本平台无法 arm，不要卡在它身上。

## 5. 适用情境与选型建议（回到总表 Hub）

把 ACH 放回整条产品线来看，它的定位很清楚：双天线高增益、两频 injection 100%、端到端 WPA handshake（.22000）已实证，是「需要稳定注入又想要较强接收」的客户的务实选择。

- **渗透测试（injection + handshake）**：首选群为 AWUS036EACS / AWUS036ACH / AWUS036ACS，三者两频注入表现都在高档。
- **最强接收 / 长距离 monitor**：AWUS036AXER 与 AWUS036ACH，ACH 以双天线高增益见长。
- **需要 802.11s mesh / active-monitor / P2P**：ACH（Realtek rtw88）做不到（实测回 `-95`），请改用 mt76 驱动的 AWUS036ACM / AWUS036ACHM；ACH 的 IBSS 仅单机可创建、peer-link 未测。
- **只需纯 AP 或一般连接、不做注入**：MediaTek 的 AWUS036AXM / AXML 更稳，但注意它们在本平台 injection 失败，不适合渗透用途。

一句话避雷：如果客户的需求明确是注入与 handshake，就不要选 AWUS036AXM / AXML（MT7921 芯片的注入在本平台实测失败，无法 deauth 或截取 handshake）；这种需求 ACH 反而是稳妥的候选。选型时也别只看带宽数字，双天线高增益带来的接收稳定度，在实际侧录距离上的差异往往比纸面规格更有感。选型决策与平台共通踩雷点，请见总表 Hub：[9 款 ALFA 无线网卡在 ASUS GX10（ARM64）的 Monitor・Injection・AP 全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

## 常见问题（FAQ）

**Q：AWUS036ACH 在 Kali 或 Ubuntu 需要装驱动吗？**
看内核版本。Linux 内核 6.13 以上（本次实测 Ubuntu 24.04 / kernel 6.17）已内置 rtw88_8812au 驱动，插上即认、免编译、免 DKMS；内核低于 6.13 才需要另外用 DKMS 安装 lwfinger/rtw88。Kali 请先用 uname -r 确认内核版本，本次未在 Kali 实机验证。

**Q：AWUS036ACH 的 monitor mode 与数据包注入表现如何？**
2.4GHz 与 5GHz 都能进 monitor mode；aireplay-ng 逐台定向注入在 2.4GHz（对 4 台 AP）与 5GHz（对 YUPITEK ch36）都是 30/30 = 100%。5GHz 注入前要先把法规网域设成允许发射的设置（例如 iw reg set US），默认 country 00 下 5GHz 禁止发射，注入会送不出去。

**Q：AWUS036ACH 可以截取 WPA handshake 吗？**
可以，且端到端已实证。两频注入都是 100%；2026-11-19 补测在自有 iPhone 15 Pro、5GHz ch36 上撷到完整 4-way 交握，并用 hcxpcapngtool 转出 47 笔 hashcat .22000 hashline。仅限自有或已取得授权的网络。

**Q：AWUS036ACH 开 WPA3 热点，iPhone 7 Plus 连不上怎么办？**
hostapd 要设 sae_pwe=0 并搭配 ieee80211w=2，iPhone 7 Plus 才连得上；用 sae_pwe=2 会连不上。同样的设置在 AWUS036ACHM 上也是关键。

**Q：AWUS036ACH 的 5GHz 接收突然卡死（抓到 0 数据包）怎么办？**
这是 rtw88_8812au 的已知现象：反复切换模式或变更法规网域后，5GHz 接收可能卡死，软件无法复原，只能实体拔插或重开机。建议 5GHz 测试前先重新插卡，并优先完成 5GHz 项目。

## 6. 延伸阅读

- 总表 Hub：[9 款 ALFA 无线网卡 ARM64 全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 免装驱动在 Ubuntu（ARM64）激活 Monitor 与 AP：[placeholder](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- WPA3-SAE handshake 截取与 `sae_pwe` 兼容性：[placeholder](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 姊妹卡对照：AWUS036ACHM（单天线 AC600）单卡实测 [placeholder]
- 本型号完整证据路径（内部）：`AWUS036ACH_evidence/`（p0 枚举、p1_gx10 行为、retest 排查）

<!-- hreflang：zh-TW 为主稿；zh-CN / en / ja / ko / de / fr / es 待本稿定稿后生成并补 rel=alternate。 -->
