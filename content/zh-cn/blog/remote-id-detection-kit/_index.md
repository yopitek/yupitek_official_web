---
title: "ALFA AWUS036ACH × 树莓派：标准 Remote ID 无人机侦测套件完整教学（2026）"
description: "用 ALFA AWUS036ACH ＋ 树莓派打造合法被动式 Remote ID 无人机侦测套件，涵盖 ASTM F3411 标准解析、硬件清单、Step-by-Step 设定，以及与 DJI OcuSync 的技术厘清。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "无人机侦测", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "为什么 AWUS036ACH 是首选，而不是更新的 Wi-Fi 6/6E 网卡？"
    answer: "Remote ID 撷取需要稳定的监听模式与原始封包注入，目前社群驱动最成熟的是 Realtek rtl88xxau 分支（RTL8812AU / RTL8814AU）。Wi-Fi 6/6E（MediaTek MT7921AUN、Realtek RTL8832BU）在主流渗透／监听工具链中尚无对应注入驱动，会被忽略。AWUS036ACH 是经社群与本套件双重验证的选择。"
  - question: "nRF52840 是必要的吗？"
    answer: "若只需 Wi-Fi Remote ID（NAN / Beacon），不需要；AWUS036ACH 即可。若要同时撷取 Bluetooth 5 Long Range 广播，则需要 nRF52840（烧录 sniffer 韧体）。建议套件含此模块以达完整覆盖。"
  - question: "这套件能解码 DJI 无人机吗？"
    answer: "能处理 DJI 的标准 Wi-Fi / BT Remote ID 广播；但 DJI 私有 OcuSync 的 DroneID 不在标准协议内，ALFA 卡无法解码，需另购 SDR（ANTSDR / HackRF）＋ Kismet 外挂。两者可并行部署。"
  - question: "树莓派用哪一代？"
    answer: "Raspberry Pi 4（2 GB+）最平衡；Pi 3B 已被 unix_rid_capture 原作者在测试中验证可用；Pi 5 亦可（注意散热与电源）。Pi 内置 Wi-Fi 因无法稳定进监听模式，必须外接 AWUS036ACH。"
  - question: "被动接收合法吗？"
    answer: "接收无人机公开广播的 Remote ID 属合法接收，等同读取公开信息；但主动干扰（jamming）受严格管制，不在此套件范围。"
---
> 榆合科技 Yupitek 技术团队｜ALFA Network 台湾授权代理

{{< tldr >}}
Remote ID 侦测套件用 **ALFA AWUS036ACH** 网卡的监听模式，被动接收无人机依法必须广播的身份与位置信息（等同无人机的「空中车牌」），是场域安全管理者合法、低成本的态势感知手段。
{{< /tldr >}}

---

## 1. 为什么需要 Remote ID 侦测套件

各国无人机监管已进入「广播式身份识别」时代。依照标准，无人机必须在空中持续广播自身信息：

| 广播字段 | 说明 |
|---|---|
| UAS / 操作者 ID | 序号或注册码 |
| 即时位置（经纬度、高度） | WGS-84 / 气压高度 |
| 速度、航向 | 水平 / 垂直速度 |
| 操作者位置 | 起降点或即时位置 |

广播透过两类无线载波：

- **Bluetooth**：BT4 Legacy Advertising、BT5 Long Range（Extended Advertising）
- **Wi-Fi**：NAN（Wi-Fi Aware，2.4 / 5 GHz）、Beacon（2.4 / 5 GHz）

对机场、园区、监狱、大型活动等场域管理者而言，**被动接收这些公开广播**（等同于看见无人机的「机尾编号」）是合规且低成本的态势感知手段，无须主动干扰。

{{< alert "triangle-exclamation" >}}
**合法性提示**：本文所有做法均为**被动接收公开广播**；主动干扰（jamming）受各国严格管制，不在本套件范围内，也不建议导入。
{{< /alert >}}

---

## 2. 产品定位：技术风险最低的开源路径

我们评估多条技术路径后，选定以 **ALFA AWUS036ACH** 为核心的组合：

- ALFA AWUS036ACH 采用 **Realtek RTL8812AU**，双频 2.4 + 5 GHz（802.11ac）、2×2 MIMO，双根可拆卸 5 dBi 高增益天线（RP-SMA），USB 3.0 带宽充足。
- 社群维护的 `rtl88xxau` 驱动让它能稳定进入**监听模式（Monitor Mode）**并支持**原始封包注入（raw packet injection）**——这正是撷取 Wi-Fi RID Beacon / NAN 讯框的前提。
- 最重要的是：`sxjack/unix_rid_capture` 的 README **明载「Tested using an rtl8812au based WiFi dongle, an nRF52840 dongle and a Raspberry Pi 3B」**，等于社群已帮我们完成硬件验证。直接复制其架构做产品化，技术风险最低。

---

## 3. 硬件清单

| 项目 | 型号 / 规格 | 角色 | 必要性 |
|---|---|---|---|
| **核心网卡** | ALFA **AWUS036ACH**（RTL8812AU，双频 2.4/5 GHz，USB 3.0，双 5 dBi RP-SMA 天线） | Wi-Fi Remote ID 撷取（监听模式） | **必要** |
| 单板电脑 | Raspberry Pi 4（建议 2 GB+；3B / 5 亦可） | 运算主机 | **必要** |
| 储存 | microSD 16 GB+（Samsung / SanDisk Endurance 建议） | 系统碟 | **必要** |
| Bluetooth 5 撷取 | **nRF52840** USB Dongle（烧录 sniffer 韧体，如 Nordic Sniffer） | 撷取 BT5 Long Range Remote ID | 推荐（可选） |
| 电源 | 5 V / 3 A USB-C（官方 Pi PSU） | 供电 | **必要** |
| 网络 | 以太网线 或 Wi-Fi 凭证 | 上传 / 管理 | **必要** |
| 天线升级 | ALFA **APA-M25** 定向面板天线 | 拉长接收距离、抑制环境噪声 | 选用 |

> 注：社群专案 `DroneAware` 原始清单指定 **AWUS036N（Ralink RT3070，2.4 GHz 单频）**。本套件升级为 **AWUS036ACH（双频）**，可同时涵盖 2.4 / 5 GHz 的 **NAN 与 Beacon** 两种 Wi-Fi RID 传输方式，覆盖更完整、未来扩充性更好。

---

## 4. 软件清单

| 软件 / 套件 | 用途 | 来源 |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | 操作系统（headless） | raspberrypi.com |
| **rtl88xxau 驱动** | RTL8812AU 监听 / 注入驱动 | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`、`libbluetooth-dev`、`libncurses-dev` | `unix_rid_capture` 编译依赖 | APT |
| **opendroneid-core-c** | Open Drone ID 消息编解码 C 函数库（ASTM F3411 / EN 4709-002） | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Linux Wi-Fi / BT RID 撷取程序（JSON 输出） | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node（选用） | 一键接入社群即时地图 | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + ANTSDR 外挂（DJI 路径） | 解码 DJI OcuSync DroneID（需 SDR 硬件） | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) ＋ [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. GitHub 专案链接

```text
# 核心解码库（ASTM F3411 / EN 4709-002 消息编解码）
https://github.com/opendroneid/opendroneid-core-c

# Linux 撷取程序（本套件主程序，已验证 rtl8812au + nRF52840 + RPi）
https://github.com/sxjack/unix_rid_capture

# 社群即时地图网络（一键安装，自动上传 droneaware.io）
https://github.com/fduflyer/DroneAware-Node-Releases

# 无线侦测框架（DJI OcuSync 路径需搭配 SDR 外挂）
https://github.com/kismetwireless/kismet

# RTL8812AU 监听 / 注入驱动（AWUS036ACH 必装）
https://github.com/morrownr/8812au-20210629
```

---

## 6. Step-by-Step 设定

### 步骤 1 — 烧录系统

使用 **Raspberry Pi Imager** 写入 **Raspberry Pi OS Lite (64-bit)**。点齿轮（进阶设定）：

- 主机名：`droneid-kit`
- 开启 SSH 并设定帐号密码
- 填入 Wi-Fi 凭证（避免后续接以太）

### 步骤 2 — 连接与硬件验证

将 AWUS036ACH 直接插上 Pi 的 **USB 3.0** 埠（蓝色 / 标 `SS`），确认双天线锁紧。启动后 SSH 进入：

```bash
ssh <user>@droneid-kit.local
sudo -i
lsusb
```

应见：

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### 步骤 3 — 安装 rtl88xxau 监听驱动

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### 步骤 4 — 验证监听模式

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

输出应显示 **`Mode:Monitor`**。

### 步骤 5 — 安装编译依赖

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### 步骤 6 — 编译 opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# 产出 libopendroneid/libopendroneid.so 与 test/odidtest
```

### 步骤 7 — 编译 unix_rid_capture

`unix_rid_capture` 需要 `opendroneid.c` / `opendroneid.h`，将其从上一步复制进来：

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### 步骤 8 — 执行撷取

需 root 权限或 `cap_net_raw`：

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # 撷取并存 JSON
```

即时 UDP 输出（另开终端）：

```bash
nc -lu 32001
```

### 步骤 9 — 视觉化轨迹（GPX → Google Earth）

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # 产生 .gpx
```

用 Google Earth 开启即可看到无人机飞行路径。典型侦测 JSON 范例：

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### 步骤 10 —（选用）接入 DroneAware 社群即时地图

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**安全提醒**：对任何 `curl ... | sudo bash` 第三方脚本，建议先下载审阅再执行：`curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`。安装程序会自动侦测 USB 网卡、提示节点名称并引导至 droneaware.io 注册，侦测结果即时显示于 live map。
{{< /alert >}}

---

## 7. 重要技术厘清：标准 RID vs DJI OcuSync

这是专业价值所在，请务必讲清楚给客户：

| 路径 | 负责对象 | 硬件 | 能否用 ALFA AWUS036ACH |
|---|---|---|---|
| **标准 Remote ID** | ASTM F3411 Wi-Fi / BT 广播 | AWUS036ACH + nRF52840 | ✅ 可以（本文主体） |
| **DJI OcuSync DroneID** | DJI 私有协议（非标准 Wi-Fi） | 完整 SDR（ANTSDR / HackRF / USRP）＋ Kismet `kismet_cap_antsdr_droneid` 外挂 | ❌ 不行 |

- ALFA AWUS036ACH 是 **Wi-Fi 频段（2.4 / 5 / 6 GHz）接收器**，能完整处理标准 RID。
- DJI 私有 **OcuSync** 的 DroneID 不走标准 Wi-Fi 协议，**ALFA 卡无法解码**；必须用覆盖到 2.4 / 5.8 GHz 的 SDR（如 ANTSDR E200）配合 `alphafox02/antsdr_dji_droneid` + Kismet 外挂。
- ⚠️ 注意：**RTL-SDR 带宽上限约 1.7 GHz**，看不到 2.4 / 5.8 GHz 的 OcuSync，必须选支持高频的 SDR。
- 两条路径**互补**：ALFA 卡做标准 RID 广播侦测，SDR 做 DJI 私有协议解码，组成完整的 Counter-UAV / RF 态势感知前端。

---

{{< faq >}}

---

## 附录：新手必懂名词表（关键字白话文）

如果你是第一次接触无人机监管 / 反无人机（Counter-UAV）技术，以下用白话文快速说明本文常出现的名词：

| 名词 | 白话解释 |
|---|---|
| **Remote ID（远程识别）** | 无人机的「空中车牌」。法规要求无人机起飞后要一直对外广播自己的身份、位置等信息，让地面上的人（尤其是监管单位）能知道「这是谁的机、飞去哪」。 |
| **ASTM F3411 / EN 4709-002** | 分别是美国、欧盟制定的 Remote ID 广播标准规格，规定广播的内容、格式该长什么样子，让不同厂牌的无人机与侦测设备能互通。 |
| **被动侦测（Passive Detection）** | 只是「听」广播出来的公开消息，不会主动发射信号去干扰或攻击无人机，合法性与主动干扰（jamming）完全不同。 |
| **monitor mode（监听模式）** | 让 WiFi 网卡不去连任何路由器，改成「单纯听」空气中的无线电封包，是撷取 Remote ID 广播的前提。 |
| **NAN（Wi-Fi Aware）／ Beacon** | 两种无人机用来广播 Remote ID 的 Wi-Fi 讯框格式，本套件会同时尝试解析这两种。 |
| **Bluetooth 5 Long Range** | 除了 Wi-Fi，部分无人机也会用蓝牙广播 Remote ID，需要额外的 nRF52840 才能撷取。 |
| **DJI OcuSync / DroneID** | DJI 自家的私有影像 / 遥测传输协议，**不是**标准 Wi-Fi，也不是本文能解的 Remote ID；需要完全不同的 SDR 硬件与外挂才能解读，本文有特别在第 7 节说明。 |
| **SDR（Software Defined Radio，软件定义无线电）** | 一种可以用软件调整接收频率范围与解调方式的通用无线电硬件，像 ANTSDR、HackRF，能涵盖 ALFA 网卡收不到的频段（如 DJI OcuSync）。 |
| **RTL8812AU** | ALFA AWUS036ACH 网卡内部使用的 Realtek 芯片型号，决定了这张卡支不支持监听模式。 |
| **GPX 文件** | 一种记录 GPS 坐标轨迹的通用格式，可以直接用 Google Earth 等软件开启，画出无人机飞过的路径。 |

> 一句话总结：本文教你把 ALFA 网卡变成一台「无人机身份扫描器」——被动接收天上无人机依法必须广播的公开信息，属于场域安全管理的合法手段。

---

## 参考来源

1. [opendroneid/opendroneid-core-c — Open Drone ID Core C Library](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — WiFi/BT RID capture（rtl8812au + nRF52840 + RPi 验证）](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — 社群 Remote ID 侦测网络](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — 无线侦测框架](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — DJI OcuSync DroneID SDR 解码](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — RTL8812AU Linux 监听 / 注入驱动](https://github.com/morrownr/8812au-20210629)
7. [ALFA AWUS036ACH 产品页（Yupitek）](https://yupitek.com/zh-cn/products/alfa/awus036ach/)
8. [Yupitek 联络与订购](https://www.yupitek.com/zh-cn/contact/)

---

*本文由榆合科技 Yupitek 技术团队整理。AWUS036ACH 与相关硬件均可经 Yupitek 取得授权代理与技术支援。*
