---
title: "AWUS036ACM 逐卡实测：MediaTek MT7612U（mt76x2u）在 ASUS GX10 + Ubuntu 24.04（ARM64）的 Monitor / Injection / AP 与 mesh 能力报告"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "AWUS036ACM（MT7612U）在 Ubuntu 24.04 ARM64 免装驱动，双频监听模式与 aircrack-ng（Kali 常用）可用，数据包注入 2.4G 63–83%、5G 76%，支持 VIF 与单机 mesh / IBSS。"
faq:
  - question: "AWUS036ACM 在 Ubuntu 或 Kali 需要装驱动吗？"
    answer: "不需要。MT7612U 由 kernel 内置的 mt76x2u 驱动接管，Ubuntu 24.04（kernel 6.17）插上即认，不用 DKMS、不用手动灌固件。本次实测平台是 Ubuntu 24.04 ARM64，Kali 只要内核够新原则上相同，但本次未在 Kali 实机验证。"
  - question: "AWUS036ACM 可以进 monitor mode 和做数据包注入吗？成功率多少？"
    answer: "可以。2.4GHz 与 5GHz 都能进 monitor mode 并正常截取；aireplay-ng 注入测试 2.4GHz 为 63–83%、5GHz 为 76%，在九张卡中属中段。要双频注入都 100%，Yopitek 实测以 AWUS036ACH、AWUS036EACS 为佳。"
  - question: "AWUS036ACM 可以同时开热点又连上网（VIF）吗？"
    answer: "可以。实测 STA+AP（一边连上游、一边开热点）与 AP+monitor（开热点同时监听）两种组合都成立，这是 mt76 驱动多接口并发较完整的地方；5GHz 热点可开到 VHT 80 MHz。"
  - question: "AWUS036ACM 支持 mesh（802.11s）和 IBSS 吗？"
    answer: "单机可创建。在 Ubuntu 24.04 / kernel 6.17 上，AWUS036ACM 能创建 802.11s mesh 与 IBSS（Ad-hoc）接口；但本次没有第二台节点，尚未验证多节点互连，所以只能说单机可创建。"
  - question: "AWUS036ACM 可以截取 WPA handshake 吗？"
    answer: "可以。针对自有 AP 与自有 iPhone 7 Plus，端到端已实测成功：deauth、截取完整 4-way（M1–M4），并以 hcxpcapngtool --all 转出 hashcat .22000。仅限自有或已取得授权的网络。"
draft: false
---

> 本文是 Yopitek 针对 ALFA AWUS036ACM 在新版 Linux 平台上的产品兼容性与能力实测纪录，供评估选型用。
> 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`。所有数据均为 Yopitek 于**自有设备、自有办公室 Wi-Fi**（SSID `YUPITEK`，2.4G ch5 / 5G ch36、ch157）对**自有测试手机**（Apple iPhone 7 Plus；WPA3 另以 iPhone 15 Pro 复测）的实测节录。
> ⚠️ **合法与范围声明**：Monitor、injection、handshake 截取仅于自己拥有或已取得授权的网络与设备上进行；AP 模式请遵守当地无线电法规。本文聚焦网卡本身的能力、兼容性与设置，**不涉及针对第三方网络的任何攻击操作**。

## 重点摘要（TL;DR）

Yopitek（ALFA Network 台湾经销）于 ASUS GX10 / Ubuntu 24.04 ARM64（kernel 6.17）实测：AWUS036ACM 双频 monitor 可用，数据包注入 2.4G 为 63–83%、5G 为 76%，双频 AP 热点均可架设（5G 可跑 VHT 80 MHz）。

- Ubuntu 24.04（ARM64）免装驱动：MT7612U 由 kernel 6.17 内置的 mt76x2u 接管，插上即认，不用 DKMS。
- 双频监听模式（monitor mode）可用；数据包注入 2.4G 为 63–83%、5G 为 76%，在九卡中属中段。
- 单机可创建 802.11s mesh 与 IBSS，并支持 VIF（STA+AP、AP+monitor）。
- WPA handshake 截取为端到端（完整 4-way，已转出 hashcat `.22000`）；为 9 张卡中完成端到端的 7 张之一。
- 要双频注入都 100%，建议改选 AWUS036ACH 或 AWUS036EACS。

---

## 1. 这张卡与测试平台

AWUS036ACM 是 ALFA 产品线里的 MediaTek 双频卡，芯片 MT7612U，Wi-Fi 5（802.11ac）、2T2R 双空间流、2.4GHz / 5GHz 双频。它在 morrownr 的清单上长期列为 Kali 推荐卡，靠的不是吞吐数字，而是 `mt76` 系列驱动对 Linux 的 Monitor、injection 与多接口并发（VIF）支持相对完整；802.11s mesh 这类实验性模式，在本平台也只有 mt76 阵营还起得来（Realtek 卡仅能创建单机 IBSS、起不了 mesh）。所以评估这张卡，重点不在速度，而在能力面齐不齐、mt76 的特色能不能真的落地，以及哪些项目得老实标成边界。

本轮沿用同一套维运情境：GX10 的内置网卡（`wlP9s9`）负责对外上网，AWUS036ACM 走 USB 外置、只承担测试任务；切 Monitor 或 AP 都不动到主机本身的网络。全程只操作 ALFA 卡对应的 `wlx*` 接口，不碰内置对外网卡。

| 项目 | 内容 |
|---|---|
| 型号 | AWUS036ACM |
| 芯片 | MediaTek MT7612U（Wi-Fi 5 / 802.11ac，2T2R 双串流） |
| 驱动 | `mt76x2u`（in-kernel，kernel 6.17 内置） |
| 世代 / 串流 | Wi-Fi 5 / 2T2R |
| 备注 | morrownr 推荐 Kali 卡 |
| 平台 | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| 测试设备 | Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro） |
| 测试环境 | 自有办公室 Wi-Fi，SSID `YUPITEK`，2.4G ch5 / 5G ch36、ch157 |

> 本轮总表未登录 AWUS036ACM 的 USB ID 与固件版本字段（标为「—」），故本文不臆测这两项数值；下文所有能力数据均以总表 ACM 各列为准。

---

## 2. 硬件与驱动（免装）

这张卡在 GX10 上插上即认，不用编译、也不用 DKMS。MT7612U 由 mainline kernel 内置的 `mt76x2u` 驱动直接接管，不必插件任何 out-of-tree 项目，也不必手动灌固件 blob。对 ARM64 来说这是 mt76 最实际的好处。很多第三方 Realtek 驱动在 aarch64 没有 prebuilt，得自己对着内核版本编译；mt76 走 in-kernel，kernel 升级就不会被驱动相依卡住。

插卡后，接口会以 `wlx` + MAC 命名（例如 `wlxXXXXXXXXXXXX`），名称绑定 MAC、重插不变，利于写进脚本固定指定。确认驱动绑定与接口生成，可用下列通用检查（不同机器的接口名与 phy 编号会不同）：

```bash
# 找出 ALFA 卡的接口名 (只挑 wlx 开头, 不动内置 wlP9s9)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# 确认绑定的驱动为 mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# 列出该 phy 声明支持的接口模式 (决定后面哪些能力能用)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

依本轮实测，`mt76x2u` 可用的接口模式比 Realtek `rtw88` 完整：managed / AP / monitor 之外，IBSS 与 mesh point 在单机上也都建得起来（见第 4 节）。这就是 ACM 后面能在单机跑 mesh / IBSS 的底气；同平台的 Realtek 卡（如 AWUS036ACH）虽然单机也能创建 IBSS，但 802.11s mesh 与 active monitor 在本平台起不来。

---

## 3. 实测能力：Monitor / Injection / AP / WPA3

先看内核能力总表（取自九卡总表第 1 列），再逐项展开。所有项目都在自有 `YUPITEK` AP + 自有 iPhone 7 Plus 上完成。

| 能力 | 2.4 GHz | 5 GHz | 说明 |
|---|---|---|---|
| Monitor（监听接收） | ✅ | ✅ | 两频皆可进 monitor、正常截取 |
| Injection（数据包注入） | ✅ 63–83% | ✅ 76% | 标准 injection test 的注入成功率 |
| AP 热点（hostapd） | ✅ | ✅ 80MHz | 5G 可开到 VHT 80 MHz |
| WPA3-SAE（AP 端） | ✅ | 未实测 | WPA3-SAE 仅在 2.4 GHz 实测；5 GHz 未实测 |

### 3-1. Monitor（2.4 GHz + 5 GHz）✅

2.4 GHz 与 5 GHz 都能正常进入 monitor 并截取数据包，是这张卡最没有争议的能力。对 2T2R 的双天线卡来说，两频监听接收稳定，足以支撑现场频道盘点与数据包诊断。

### 3-2. Injection（数据包注入）✅（中段水准）

以标准 injection test 量测数据包注入可靠度，AWUS036ACM 在 2.4 GHz 是 63–83%、5 GHz 是 76%。放进九卡里属中段，明显不如 Realtek RTL8812AU（AWUS036ACH，两频 100%）和 RTL8821CU（AWUS036EACS，两频 100%），但功能完整、实务上够用。ACM 能注入，只是稳定度不是班上最高；要是客户把「注入成功率要顶」摆第一，它就不是首选（见第 5 节选型）。

5 GHz 注入前要留意一个设置细节：默认法规网域会锁住部分 UNII 频段的主动发送，测试前需先把 regulatory domain 切到允许发射的设置、测完再设回在地网域（`iw reg set US` → 测试 → `iw reg set TW`）。这是 5 GHz 能否正常发射的前提，与卡本身能力无关。

### 3-3. AP 热点与 WPA3-SAE ✅

AWUS036ACM 可作为 AP，2.4 GHz 与 5 GHz 都行，5 GHz 还能开到 80 MHz 带宽（VHT80）。AP 端在 2.4 GHz 激活 WPA3-SAE 后，自有测试手机可正常连上（5 GHz 的 WPA3 未实测）。

这里值得对照同为 mt76 的单天线型号 AWUS036ACHM：ACHM 的 WPA3 得特别把 hostapd 的 `sae_pwe` 设成 0，不然 iPhone 7 Plus 会连不上。AWUS036ACM 本轮没碰到这个限制，WPA3-SAE 直接可用。

---

## 4. 高级能力：VIF / mesh / IBSS 单机与限制

再往深一层看 handshake、虚拟接口（VIF）、active monitor 与 mesh / IBSS。这一节也是 AWUS036ACM 跟 Realtek 卡拉开差距的地方。

| 高级项目 | ACM 结果 | 说明 |
|---|---|---|
| WPA handshake 截取 | ✅ 端到端（.22000） | deauth 自有 iPhone 7 Plus，截取完整 4-way M1–M4，转出 hashcat `.22000` |
| VIF（多接口并发） | ✅ STA+AP / AP+mon | 可同时 STA+AP 或 AP+monitor |
| Active monitor | 🟡 可设置，ACK 未验 | 模式可创建，ACK 回复行为未验证 |
| Ad-hoc（IBSS） | 🟡 单机 | 单机可创建接口，互连需第二台 |
| Mesh（802.11s） | 🟡 单机 | 单机可创建接口，互连需第二台 |
| Wi-Fi Direct（P2P） | ⬜ 需第二台 | 本轮未测 |

### 4-1. VIF（虚拟接口并发）— ACM 的强项 ✅

这张卡能同时跑两个虚拟接口。本轮实测 STA+AP（一边连上游、一边开热点）和 AP+monitor（一边开热点、一边监听）两种组合都成立，适合「边连接边观测」或「单卡同时当 client 与基地台」这类场景。这是 `mt76` 驱动多接口并发较完整的地方。

### 4-2. mesh / IBSS「单机可」— mt76 的关键差异 🟡

AWUS036ACM 在单机上能把 802.11s mesh 与 ad-hoc（IBSS）接口建起来；Realtek `rtw88` / `rtw89`（AWUS036ACH、AWUS036AX 等）虽然单机也能创建 IBSS，但在本平台不支持 802.11s mesh。所以要做 802.11s mesh 实验，mt76 卡（ACM / ACHM）就有 Realtek 卡没有的起点。

要把边界标清楚：本轮确认的是「单机可创建接口」，完整的多节点互连还需要第二张卡 / 第二台节点，尚未进行，所以这里标 🟡（单机）而不是 ✅。

### 4-3. 诚实的能力边界

- **handshake**：ACM 已跑完整端到端链（deauth 自有设备 → 截取完整 4-way M1–M4 → `hcxpcapngtool --all` 转出 hashcat `.22000`），尽管其注入成功率（2.4G 63–83% / 5G 76%）低于 Realtek 卡。
- **active monitor**：模式可以设置起来，但 ACK 回复行为本轮未验证（标 🟡）。相关的是，平台层级的 `hcxdumptool` 8.x 除 AWUS036EACS 在 2.4 GHz 外，在所有卡上都 `failed to arm`（它要 active-monitor，本平台的三频内置与现行驱动没提供），所以 ACM 的 handshake 流程改走 `airodump-ng` + `aireplay-ng`。
- **Wi-Fi Direct（P2P）**：本轮未测，需第二台设备。

### 4-4. 平台操作注意（GX10 ARM64，ACM 相关）

1. **别切断自己的网络**：绝不运行 `airmon-ng check kill`（会关掉 NetworkManager 使 GX10 断网）；只动 `wlx*`，不碰内置对外的 `wlP9s9`。
2. **RX stall 排除**：反复切换 monitor / AP 后若突然扫不到东西，把卡**拔插一次**即可复原（USB 重枚举，接口名由 MAC 决定、不变）。
3. **5 GHz TX 解锁**：做 5 GHz injection 前先设置正确法规网域解锁 TX 功率，测完设回在地网域。
4. **handshake 截取技巧**：办公室常有多台同名 AP，实务上不锁单一 `--bssid`、改截取整个频道较稳；转档用 `hcxpcapngtool --all`。
5. **ARM64 工具链**：`aircrack-ng` 需自源代码编译；`wifite` 用 git 3.0.0 版（绕过 apt 依赖冲突）。

平台层级的 Kali 工具（`airmon-ng`、`kismet`、`bettercap`、`wifite` git 版、Wireshark / tshark）都能正常把 ACM 当 data source 使用；唯一例外是前述需要 active-monitor 的 `hcxdumptool`。

---

## 5. 适用情境与选型（连回 Hub）

把上面的能力对回产品定位，AWUS036ACM 的角色其实很清楚：一张能力均衡、驱动免装，又独有 mt76 mesh / IBSS / VIF 优势的 Wi-Fi 5 2T2R 卡。那它该用在哪些情境？

- **mesh（802.11s）实验的首选**：这批九卡里，只有 mt76 的 ACM / ACHM 能在单机创建 802.11s mesh 接口；Realtek `rtw88` / `rtw89` 虽可创建单机 IBSS，但不支持 802.11s mesh。要做 mesh 实验，ACM 是对的起点。
- **需要 VIF 并发**：STA+AP、AP+monitor 都成立，适合单卡同时当 client 与 AP、或边连接边监听。
- **重视免驱动维运**：in-kernel `mt76x2u`，kernel 升级不卡驱动，ARM64 上免去编译 out-of-tree 模块的麻烦。
- **不是最佳解的情境**：若核心需求是「最高 injection 成功率」，ACM 的注入（2.4G 63–83% / 5G 76%）不是班上最高，建议改用 Realtek 的 AWUS036EACS / ACH / ACS；若追求最强接收 / 长距离 monitor，则看 AWUS036AXER / ACH。

和同家族相比，定位差异如下：

| 需求 | 建议卡 | 理由 |
|---|---|---|
| mesh（802.11s）单机实验 | **AWUS036ACM** / AWUS036ACHM | `mt76` 驱动单机可创建 802.11s mesh（Realtek 仅能单机 IBSS、不支持 mesh） |
| VIF 并发（STA+AP / AP+mon） | **AWUS036ACM** | 多接口并发成立 |
| 双频注入都要 100% / 端到端 handshake | AWUS036EACS、AWUS036ACH、AWUS036ACS | 两频注入最佳，`.22000` 端到端已佐证 |
| 最强接收 / 长距离 monitor | AWUS036AXER、AWUS036ACH | 跳频扫到更多目标 / 双天线高增益 |

一句话选型：要玩 mesh / IBSS、要 VIF 并发、又想免驱动维运，AWUS036ACM 是这批里最对口的 mt76 卡；要双频注入都 100%，就往 EACS / ACH 走。完整九卡横向比较与选型决策，见 [ALFA 无线网卡总评 Hub（九卡总表）](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)。

---

## 常见问题（FAQ）

**Q：AWUS036ACM 在 Ubuntu 或 Kali 需要装驱动吗？**
不需要。MT7612U 由 kernel 内置的 mt76x2u 驱动接管，Ubuntu 24.04（kernel 6.17）插上即认，不用 DKMS、不用手动灌固件。本次实测平台是 Ubuntu 24.04 ARM64，Kali 只要内核够新原则上相同，但本次未在 Kali 实机验证。

**Q：AWUS036ACM 可以进 monitor mode 和做数据包注入吗？成功率多少？**
可以。2.4GHz 与 5GHz 都能进 monitor mode 并正常截取；aireplay-ng 注入测试 2.4GHz 为 63–83%、5GHz 为 76%，在九张卡中属中段。要双频注入都 100%，Yopitek 实测以 AWUS036ACH、AWUS036EACS 为佳。

**Q：AWUS036ACM 可以同时开热点又连上网（VIF）吗？**
可以。实测 STA+AP（一边连上游、一边开热点）与 AP+monitor（开热点同时监听）两种组合都成立，这是 mt76 驱动多接口并发较完整的地方；5GHz 热点可开到 VHT 80 MHz。

**Q：AWUS036ACM 支持 mesh（802.11s）和 IBSS 吗？**
单机可创建。在 Ubuntu 24.04 / kernel 6.17 上，AWUS036ACM 能创建 802.11s mesh 与 IBSS（Ad-hoc）接口；但本次没有第二台节点，尚未验证多节点互连，所以只能说单机可创建。

**Q：AWUS036ACM 可以截取 WPA handshake 吗？**
可以。针对自有 AP 与自有 iPhone 7 Plus，端到端已实测成功：deauth、截取完整 4-way（M1–M4），并以 hcxpcapngtool --all 转出 hashcat .22000。仅限自有或已取得授权的网络。

---

## 6. 延伸阅读

- 九张 ALFA 卡的完整能力比较与选型总评 → [ALFA 无线网卡总评 Hub（九卡总表）](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- 免装驱动：Ubuntu 24.04 + kernel 6.17 激活 Monitor / AP（rtw88 / rtw89 / mt76 实测）（placeholder，链接施工中）
- WPA3-SAE 与端到端 handshake 截取逐步教学（placeholder，链接施工中）
- 同为 mt76 的单天线型号 → AWUS036ACHM 逐卡实测（placeholder，链接施工中）

---

*测试单位：Yopitek（ALFA Network 台湾经销）— https://www.yupitek.com ｜ 测试环境：ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）*
