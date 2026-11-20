---
title: "AWUS036AXML 实测：Wi-Fi 6 + 蓝牙复合卡在 ASUS GX10（ARM64 / Ubuntu 24.04）——AP 稳定、注入失败的诚实报告"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML（Wi-Fi＋蓝牙）在 ASUS GX10／Ubuntu 24.04 ARM64 实测：AP、WPA3、monitor 可用，但 injection 失败、无法截取 handshake，不建议渗透测试。"
faq:
  - question: "AWUS036AXML 能做数据包注入（packet injection）吗？"
    answer: "在我们的测试平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。aireplay-ng --test 回报 No Answer、Found 0 APs；指定 AP 逐台测也只得到 No such BSSID available。即使一般扫描看得到该 AP（约 -54 dBm），注入工具情境下仍收不到它的 beacon，所以 deauth 与 handshake 截取（0 笔）都无法使用。根因是 kernel 6.16+ 的 mac80211 chanctx 回归，非芯片先天不能注入；AWUS036AXM 结果相同。需要注入请改选 AWUS036EACS、ACH 或 ACS。"
  - question: "AWUS036AXML 的蓝牙在 Ubuntu 上能用吗？"
    answer: "本机实测蓝牙可用：以 bluetoothctl／hciconfig 确认 hci 控制器为 UP，可扫到 BLE 与经典蓝牙设备，且 Wi-Fi 与蓝牙能同时使用（共存）。它是 Wi-Fi＋蓝牙复合设备；提醒：重插偶尔会卡在 WiFi probe、生不出 wlx 接口，换一个 USB 孔重插即可恢复。"
  - question: "AWUS036AXML 在 Ubuntu 24.04 要另外装驱动吗？"
    answer: "不用。mt7921u 驱动在 kernel 6.17 内置，插上后 dmesg 会看到 mt7921u 把接口改名为 wlx 加 MAC（USB ID 0e8d:7961），免 DKMS、免编译。驱动不提供 IBSS 与 mesh 模式。"
  - question: "AWUS036AXML 可以开 AP、支持 WPA3 吗？"
    answer: "可以，这是它最稳的用途。2.4 GHz（802.11n，MCS 10）与 5 GHz VHT80（VHT-NSS2）都有 iPhone 连入并 authorized；WPA3-SAE 以 sae_pwe=0 让 iPhone 15 Pro 连入（MFP: yes；于 2.4 GHz 与 6 GHz 实测，5 GHz 未实测）；STA＋AP 并行时 STA 端 ping 约 4.4 ms。虽然定位为 Wi-Fi 6 芯片，本机另实测 6 GHz band 可用（自架 6135 MHz AP，iPhone 15 Pro 以 802.11ax 连上并取得 IP）。"
  - question: "AWUS036AXML 和 AWUS036AXM 差在哪、该选哪张？"
    answer: "在本平台两张的 Wi-Fi 行为相同：同用 mt7921u、injection 同样失败、monitor 接收同样偏弱，AP、WPA3、VIF 同样可用。差别是 AXML 另有蓝牙（本机实测可用）且本机实测 6 GHz band 可用，而 AXM 的蓝牙与 6 GHz 本轮未单独实测。纯 AP 或一般连接选哪张都可以；要 injection 或 handshake，两张都不要选。"
draft: false
---

{{< tldr >}}AWUS036AXML 在 ASUS GX10／Ubuntu 24.04 ARM64 上 AP、WPA3、VIF 与被动 monitor 可用，蓝牙与 6 GHz band 本机实测亦可用，但 injection 实测失败（No Answer／Found 0 APs），无法 deauth 或截取 handshake，不建议用于渗透测试；定位纯 AP 与一般连接。{{< /tldr >}}

ALFA AWUS036AXML 是这批 9 款网卡里唯一「MediaTek Wi-Fi 6 + 蓝牙」的复合型号。它和不带蓝牙的 AWUS036AXM 是同一世代芯片（MT7921，走 `mt7921u` 驱动），差别就在多了一组蓝牙。客户最常问的还是那三题：monitor 进得去吗？能不能 injection？能不能架 AP？这篇把 AWUS036AXML 单独拉出来，在 ASUS GX10（ARM64）搭配 Ubuntu 24.04 逐项实测，做得到、做不到的一次讲清楚，尤其是最关键的那条限制：**injection 在这个平台上失败**。

先把定位讲明白：以下所有量测都在 Yupitek 自有设备、自有办公室 Wi-Fi（SSID `YUPITEK`）、对自有测试手机（iPhone 7 Plus，WPA3 另以 iPhone 15 Pro 复测）上完成。这是经销商对产品兼容性与能力边界的硬件验证，不是针对第三方网络的操作教学。文中的 monitor、AP、injection 自我测试，全部在自有封闭环境、对自有设备进行。

## 一、这张卡与测试平台

- **运算平台**：ASUS GX10（ARM64 / aarch64）
- **操作系统**：Ubuntu 24.04 LTS
- **内核版本**：kernel 6.17.0-1014-nvidia
- **受测网卡**：ALFA AWUS036AXML（MediaTek MT7921AUN，Wi-Fi 6 / 2x2 / +BT）
- **测试设备**：Apple iPhone 7 Plus（WPA3-SAE 另以 iPhone 15 Pro 复测）
- **测试环境**：自有办公室 Wi-Fi，SSID `YUPITEK`，2.4GHz ch5 / 5GHz ch36、ch157
- **测试期间**：2026-11-16 至 2026-11-18 实机量测

所有结果都以实际量到的数字或状态记录，不以规格书推测；MAC 地址于输出中以 `xx` 屏蔽。

## 二、硬件与驱动：MT7921AUN，插上即用

| 项目 | 规格 |
|---|---|
| 型号 | AWUS036AXML |
| 芯片 | MediaTek MT7921AUN |
| USB ID | `0e8d:7961`（MediaTek Inc. Wireless_Device） |
| in-kernel 驱动 | `mt7921u` |
| 世代 / 串流 | Wi-Fi 6 / 2x2（2T2R） |
| 蓝牙 | 有（BT + WiFi 复合设备；本机实测 hci 控制器 UP、可扫到 BLE 与经典蓝牙设备、WiFi+BT 共存） |
| USB 枚举 | USB 3 |
| 接口命名 | `wlx<MAC>`（例：`wlx00c0cabd65b9`） |

辨识方式很直接：插上后用 `lsusb` 看到 MediaTek 的 USB ID，`dmesg` 看到 `mt7921u` 挂载、把接口改名：

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

两个重点。第一是免编译：AWUS036AXML 走 kernel 6.17 内置的 `mt7921u` 驱动，插上即辨识，不必在 aarch64 上处理任何 out-of-tree DKMS 模块，这在 ARM64 平台特别省事。第二是它以 USB 3 枚举（前代部分型号的 OTG 线只有 USB 2.0），传输带宽不是瓶颈。

补一个常被误会的点：AWUS036AXML 定位是 Wi-Fi 6（非 6E）芯片，但**本机实测 6 GHz band 可用**——我们自架 6135 MHz 的 AP，iPhone 15 Pro 以 802.11ax 连上并取得 IP。另外蓝牙也实测可用：`hciconfig`／`bluetoothctl` 看到 hci 控制器状态 UP，可扫到 BLE 与经典蓝牙设备，Wi-Fi 与蓝牙能同时运作（共存）。

再查一下支持的接口模式，会看到一个对选型有意义的细节，就是没有 IBSS、也没有 mesh point：

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

也就是说，managed、AP、monitor、P2P 都有，但 ad-hoc（IBSS）与 802.11s mesh 这两种模式，`mt7921u` 驱动根本不提供。要做 mesh / IBSS 实验的客户，这张直接排除（改看 `mt76` 的 ACM / ACHM）。

## 三、实测能力：Monitor / AP / WPA3，以及 injection 的诚实限制

内核能力一次看完：

| 能力 | 2.4GHz | 5GHz | 说明 |
|---|---|---|---|
| Monitor | ✅（弱） | ✅（弱） | 可侧录 beacon；client / data 数据包常漏接 |
| **Injection** | ❌ **失败** | ❌ **失败** | `aireplay-ng` 注入 / deauth 无法运作；根因为 kernel 6.16+ mac80211 chanctx 回归（非芯片先天） |
| AP 热点 | ✅ 含 802.11n | ✅ VHT80（80MHz） | iPhone 7 Plus 连入，`authorized: yes` |
| WPA3-SAE | ✅ | 未实测 | iPhone 15 Pro 连入，`MFP: yes`（`sae_pwe=0`）；另于 6 GHz（ch37，6135 MHz）实测 |

### Monitor：两频都进得去，但收讯偏弱

AWUS036AXML 在 2.4GHz（ch1 / 6 / 11）与 5GHz（ch36 / 149 / 157）都能进 monitor mode，侧录 beacon 没问题。设置流程是标准的 `iw dev` 四步：

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # 2.4GHz 改用 set channel 6
```

诚实说一句：它的 monitor 收讯明显比同批的 MT7612U（ACM）或 Wi-Fi 6 的 AXER 弱。beacon 抓得到，但 client / data 数据包常常漏接；用 `airodump-ng` 跳频扫描时容易漏掉部分 AP。实务上建议锁定单一频道（`-c <ch>`）而不是跳频，收获会稳一些。另外，monitor 模式下 `iw info` 会回报 txpower 只有 3 dBm，这是**回报假象**（硬件实际 TX 约 20–23 dBm，已由 `txpower_sku` 验证），并不是功率真被压到 3 dBm，这点后面「注意事项」会一起谈。

### AP 热点：2.4GHz 含 HT、5GHz 上得了 VHT80

AP 是 AWUS036AXML 最稳的一块。2.4GHz 可以直接保留 802.11n（HT），不必像单天线的 ACHM 那样关掉 HT；5GHz 则能开到 VHT 80MHz。两频都实测让 iPhone 7 Plus 连入、`authorized: yes`。

5GHz VHT80 的 hostapd 关键设置：

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

实测连入后是 VHT-NSS2、80MHz。2.4GHz 版本把 `hw_mode` 换成 `g`、`channel=6`，保留 `ieee80211n=1` 与 `ht_capab=[HT20]` 即可，iPhone 连入是 MCS 10（802.11n）。

### WPA3-SAE：可用，记得 sae_pwe=0

把 AP 的 `wpa_key_mgmt` 换成 `SAE`、加上 `ieee80211w=2` 与 `sae_pwe=0`，就能开 WPA3-SAE。实测 iPhone 15 Pro 于 2.4 GHz（以及 6 GHz；5 GHz 未实测）连入、`authorized: yes`、`MFP: yes`。`sae_pwe=0` 是为了兼容旧款 iPhone，这点和 ACHM 的雷一样，`sae_pwe=2` 时旧机常常连不上。

### VIF：一边上网一边当热点，可行

AWUS036AXML 支持多接口并存。建一个 AP VIF（不同 MAC、unmanage）、主接口连上 Wi-Fi、同频道开 AP，实测 iPhone 7 Plus 连入 AP VIF 时，STA 对 `YUPITEK` 的 ping 是 4.4 ms。对「一张卡同时上网 + 分享热点」的需求是成立的。

### 诚实限制：injection 在本平台失败

这是 AWUS036AXML（以及它的无蓝牙双胞胎 AXM）最需要讲清楚的一条。在 ASUS GX10 + kernel 6.17 上，我们对自有测试环境做 injection 自我测试，结果是失败：

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

就算指定自家 AP 的 BSSID 逐台测，也只回 `No such BSSID available`。关键在于：一般扫描明明看得到该 AP（信号 -54 dBm），但一进到注入工具的情境，这张卡就「听不到」目标的 beacon，deauth 送不出去，4-way handshake 截取数为 0。

这不是参数没调好，也不是单张网卡故障。真正的根因在**软件层**：kernel 6.16 之后 mac80211 的 channel context（chanctx）出现回归，让 stock 驱动在注入情境下收不到目标 beacon，`aireplay-ng` 因此判定 `No Answer`，并**不是 MT7921 芯片先天不能注入**。现象记录在 morrownr/USB-WiFi issue #387，根因分析在 morrownr/mt76 issue #18。社区实测指出，在同型号上以 git／patched 驱动可让 active monitor 加注入运作，但 MT7921 firmware 仍把注入锁在 1 Mbps／6 Mbps 基础速率、无法以 HT／VHT 注入；AXM 与 AXML 两款在 **stock kernel 6.17** 上同样中奖，截至 2026-11-18 无法靠调参解决。

因此，凡是牵涉 injection 的能力，像 deauth、WPA handshake 截取、以注入为前提的渗透测试，AWUS036AXML 在本平台都做不到。这类用途请改用实测注入可用的型号（见下方选型）。

### 其他高级模式一览

| 高级功能 | 状态 | 说明 |
|---|---|---|
| VIF（STA + AP 并存） | ✅ | 同频道 ch36；iPhone 连入时 STA ping 4.4 ms |
| WPA handshake 截取 | ❌ | 注入失败 → deauth 送不出、handshake 0 |
| Active monitor | 🟡 | `set monitor active` 被接受，ACK 未验证 |
| Ad-hoc（IBSS） | N/A | `mt7921u` 驱动不具此模式 |
| Mesh（802.11s） | N/A | `mt7921u` 驱动不具此模式 |
| Wi-Fi Direct（P2P） | ⬜ | 驱动声明支持，需第二台设备，略过 |

## 四、蓝牙复合注意事项与适用／不适用用途

### BT + WiFi 复合卡的实务副作用

AWUS036AXML 内含蓝牙，是这批里两款复合设备之一（另一款是 Realtek 的 EACS）。蓝牙本机已实测可用（hci 控制器 UP、可扫到 BLE 与经典蓝牙设备、与 Wi-Fi 共存，见前文），这里补一个复合设备的实务副作用：重插时偶尔会卡在 WiFi probe、生不出 `wlx` 接口，症状是拔插后 `ls /sys/class/net` 迟迟等不到网卡。解法很单纯：**换一个 USB 孔**重插，通常就能正常枚举。

另一个要记住的小动作：AP 模式下如果手机突然扫不到你的 SSID，把网卡**拔插一次**重置即可，不必改设置。（注意：前面提到 monitor 回报的 3 dBm 是假象、非真实功率，不是 SSID 消失的主因。）

### 平台安全守则

- 绝对不要运行 `airmon-ng check kill`：它会关掉 NetworkManager，让整台 GX10 断网。操作时只动外置的 `wlx*` 接口，不要碰内置的对外上网主线。
- `hcxdumptool 8.x` 在这台机器上会 `failed to arm`（AWUS036EACS 在 2.4 GHz 除外；GX10 三频内置卡枚举冲突 + 驱动无 active-monitor），这是全平台通病、与 AXML 无关；需要类似功能时改用 `airodump-ng` 搭配其他 aircrack-ng 工具。
- ARM64 补充：`aircrack-ng` 需自源代码编译，`wifite` 建议用 git 版以绕过 apt 依赖冲突。

### 适用 / 不适用一览

| 适用情境 | 不适用情境 |
|---|---|
| 纯 AP / 热点（2.4G 含 HT、5G VHT80） | injection / deauth |
| WPA3-SAE 热点 | WPA handshake 截取 |
| 一般 managed 连接 | 以注入为前提的渗透测试主力卡 |
| 被动 monitor / 频谱盘点（锁单一频道） | mesh / IBSS 实验 |
| STA + AP 并存（VIF、一边上网一边分享） | 需要强收讯的长距离侧录 |

## 五、选型建议（连回总表）

把 AWUS036AXML 放回 9 款的全貌来看，它的定位很清楚：MediaTek 的连接稳定、免编译、两频 AP 都上得了 VHT80，是一张称职的「纯连接 / 纯 AP」卡；只要沾到 injection，就不是它的场子。

| 需求 | 建议型号 |
|---|---|
| 纯 AP / 一般连接（不需注入） | **AWUS036AXML / AWUS036AXM**（本卡适用） |
| injection + handshake（渗透测试） | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| mesh / IBSS 实验 | AWUS036ACM / AWUS036ACHM |
| 最强接收 / 长距离 monitor | AWUS036AXER / AWUS036ACH |

如果你正在 9 款之间做取舍，完整的 Monitor / Injection / AP / WPA3 全矩阵与依用途的选型，请看总表：

- [2026 最完整实测：9 款 ALFA 无线网卡在 ASUS GX10 的全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

一句话避雷：**要 injection 或 handshake，别选 AWUS036AXML / AWUS036AXM**；要纯连接或架热点，它很好用。

## 常见问题（FAQ）

**Q1. AWUS036AXML 能做数据包注入（packet injection）吗？**
在我们的测试平台（ASUS GX10／Ubuntu 24.04 ARM64／stock kernel 6.17.0-1014-nvidia）不能。`aireplay-ng --test` 回报 `No Answer`、`Found 0 APs`；指定 AP 逐台测也只得到 `No such BSSID available`。即使一般扫描看得到该 AP（约 -54 dBm），注入工具情境下仍收不到它的 beacon，所以 deauth 与 handshake 截取（0 笔）都无法使用。根因是 kernel 6.16+ 的 mac80211 chanctx 回归，非芯片先天不能注入；AWUS036AXM 结果相同。需要注入请改选 AWUS036EACS、ACH 或 ACS。

**Q2. AWUS036AXML 的蓝牙在 Ubuntu 上能用吗？**
本机实测蓝牙可用：以 `bluetoothctl`／`hciconfig` 确认 hci 控制器为 UP，可扫到 BLE 与经典蓝牙设备，且 Wi-Fi 与蓝牙能同时使用（共存）。它是 Wi-Fi＋蓝牙复合设备；提醒：重插偶尔会卡在 WiFi probe、生不出 `wlx` 接口，换一个 USB 孔重插即可恢复。

**Q3. AWUS036AXML 在 Ubuntu 24.04 要另外装驱动吗？**
不用。mt7921u 驱动在 kernel 6.17 内置，插上后 dmesg 会看到 mt7921u 把接口改名为 `wlx` 加 MAC（USB ID `0e8d:7961`），免 DKMS、免编译。驱动不提供 IBSS 与 mesh 模式。

**Q4. AWUS036AXML 可以开 AP、支持 WPA3 吗？**
可以，这是它最稳的用途。2.4 GHz（802.11n，MCS 10）与 5 GHz VHT80（VHT-NSS2）都有 iPhone 连入并 authorized；WPA3-SAE 以 `sae_pwe=0` 让 iPhone 15 Pro 连入（`MFP: yes`；于 2.4 GHz 与 6 GHz 实测，5 GHz 未实测）；STA＋AP 并行时 STA 端 ping 约 4.4 ms。虽然定位为 Wi-Fi 6 芯片，本机另实测 6 GHz band 可用（自架 6135 MHz AP，iPhone 15 Pro 以 802.11ax 连上并取得 IP）。

**Q5. AWUS036AXML 和 AWUS036AXM 差在哪、该选哪张？**
在本平台两张的 Wi-Fi 行为相同：同用 mt7921u、injection 同样失败、monitor 接收同样偏弱，AP、WPA3、VIF 同样可用。差别是 AXML 另有蓝牙（本机实测可用）且本机实测 6 GHz band 可用，而 AXM 的蓝牙与 6 GHz 本轮未单独实测。纯 AP 或一般连接选哪张都可以；要 injection 或 handshake，两张都不要选。

## 延伸阅读

（链接陆续上线，施工中）

- 同芯片无蓝牙版：[AWUS036AXM 单卡实测](/zh-cn/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- 注入可用的替代方案：[AWUS036EACS 单卡实测](/zh-cn/blog/awus036eacs-asus-gx10-ubuntu-test-report/)、[AWUS036ACH 单卡实测](/zh-cn/blog/awus036ach-asus-gx10-ubuntu-test-report/)、[AWUS036ACS 单卡实测](/zh-cn/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- 主题文：[免装驱动：在 Ubuntu（ARM64）上激活 Monitor 与 AP 模式](/zh-cn/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- 主题文：[WPA3-SAE 连接与 handshake 实务（自有环境验证）](/zh-cn/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- 总表 Hub：[9 款 ALFA 网卡在 ASUS GX10 的全矩阵](/zh-cn/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*测试单位：Yupitek（ALFA Network 台湾经销）｜ 测试平台：ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia ｜ 测试设备：Apple iPhone 7 Plus（WPA3 另测 iPhone 15 Pro）｜ 测试环境：自有办公室 Wi-Fi（SSID YUPITEK）。本文为产品兼容性与能力验证，非针对第三方网络之操作教学。*
