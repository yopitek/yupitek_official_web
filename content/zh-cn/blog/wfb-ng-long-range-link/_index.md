---
title: "ALFA AWUS036ACH 自制长距离无人机数位图传／遥测链路：wfb-ng 开源教学（2026）"
description: "用 ALFA AWUS036ACH 网卡＋开源 wfb-ng，打造低延迟、可加密的长距离无人机数位图传与 MAVLink 遥测链路。完整硬件清单、Raspberry Pi 设定教学、供电踩坑排错全攻略。"
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "无人机图传", "数位图传", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "长距离图传", "遥测链路"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "wfb-ng 跟一般 WiFi 有什么不同？"
    answer: "一般 WiFi 需要连线（association）与 ACK 确认，在长距离下效率差、延迟高。wfb-ng 改用 raw 封包注入，绕过 802.11 连线机制，直接用 FEC 前向纠错抗丢包，端到端延迟可压到数十毫秒等级。"
  - question: "为什么机载端 ALFA 网卡需要独立供电？"
    answer: "AWUS036ACH 在发射（TX）时瞬间耗电很大，直接插 Raspberry Pi 的 USB 2.0 埠会因供电不足导致网卡端口被 reset、链路断线、封包损坏。建议用 5V BEC 独立供电，并在 +5V 与 GND 间并联 470µF 低 ESR 电容滤波。"
  - question: "连线后没有影像也没有遥测怎么办？"
    answer: "最常见的原因是密钥不对应——检查机载端的 drone.key 与地面站的 gs.key 是否为同一组。其次确认两端的 wifi_channel 与 link_domain 设定完全一致。可用 journalctl -xu wifibroadcast@gs 查看即时日志排错。"
  - question: "wfb-ng 一定要用 ALFA AWUS036ACH 吗？"
    answer: "任何 RTL8812AU 芯片网卡理论上都可用，但 AWUS036ACH 是 wfb-ng 专案官方实测的硬件，驱动支持最稳定。尤其在高功率、长距离场景下，ALFA 的功率设计与可拆式天线优势明显。"
---
> 作者：榆合科技 Yupitek（ALFA Network 台湾授权代理商）技术团队
> 适用对象：无人机同好、Maker、资安研究员、农喷／巡检机开发者
> 难度：★★★☆☆（需基本 Linux 与飞控概念）

{{< tldr >}}
wfb-ng 是一套开源软件，能把 **ALFA AWUS036ACH** 这类支持 monitor mode 的 WiFi 网卡「变成」无人机专用的长距离无线电，让操作者自行架设低延迟、可加密的影像与 MAVLink 遥测传输链路。
{{< /tldr >}}

---

## 一、为什么用 ALFA 卡自制数位图传？

如果你玩过传统类比 FPV（5.8GHz 类比图传），一定对那根「雪花天线」不陌生：信号一被遮挡就满屏噪声，飞远了就开始掉画面，而且**任何人都拿一台接收机就能偷看你画面**——既不加密、也没有遥测回传。

我们团队最近一年帮不少农喷、巡检、甚至资安教育训练的客户架设链路，发现一个很务实的需求：**能不能用一张常见的 ALFA USB 网卡，搭开源软件，自己做出一套「数位化、可加密、同时传影像＋遥测」的长距离链路？**

答案是可以，而且比你想的简单。

对比传统类比图传，用 ALFA 网卡跑开源 **wfb-ng** 做数位图传有几个压倒性优势：

- **低延迟**：raw WiFi 注入模式绕过一般 802.11 的 ACK 与连线握手，端到端延迟可以压到数十毫秒等级，FPV 手感接近类比。
- **数位加密**：影像与遥测封包走 libsodium 加密，别人拿接收机也解不开你的画面与飞控数据。
- **一条链路多工**：同一张网卡、同一个频点，可以**同时**传：
  - 即时影像（RTP / RTSP）
  - MAVLink 遥测（双向，飞控 ↔ 地面站）
  - 一条 TCP/IP 隧道（可拿来跑 VPN、SSH、文件传输）
- **TX 分集（发射分集）**：多张网卡可做发射端分集，抗遮蔽、提升稳健性。
- **开源可客制**：主角 ALFA AWUS036ACH 搭配开源 wfb-ng，整套自制链路的成本远低于市售数位图传（DJI O3 / Walksnail 等），且**全部开源、可客制**。

{{< alert "circle-info" >}}
小语：这篇文章不是要「取代」大疆原厂图传，而是给想要**自己掌握链路、做二类备援、或做客制化载荷**的同好一条务实的开源路径。
{{< /alert >}}

---

## 二、这是什么：wfb-ng 简介

**wfb-ng**（Wireless Fibre / WiFi Broadcast – next generation）是一套开源数位 FPV 与遥测专案，核心想法很聪明：

> 它不把 WiFi 当「网络」用，而是把 WiFi 当「无线电」用。

一般 802.11 为了当区域网络，会做连线（association）、ACK 确认、重传——这些机制在长距离、移动、低信号的场景下反而拖慢速度、吃掉距离。wfb-ng 则改用 **raw WiFi 注入（raw WiFi injection）**：

- 网卡进入 **monitor mode（监控模式）**，不跟任何人「连线」。
- 直接注入底层 WiFi 封包，**不需要 ACK、不重传**（改用 FEC 前向纠错来抗丢包）。
- 绕过一般 802.11 的距离与延迟限制，把传输距离与稳定性拉到硬件极限。

简单说，它把一张常见的 USB 网卡，变成一对「数位无线电」，上面可以跑 RTP 影像、MAVLink 遥测、甚至一条 IP 隧道。

- 专案首页（GitHub）：https://github.com/svpcom/wfb-ng.git
- 目前广泛用于 PX4 / ArduPilot 生态的自制数位图传，社群活跃，也是乌克兰自制无人机社群常用的开源链路方案。

---

## 三、主角介绍：ALFA AWUS036ACH

这套链路的「无线电」就是它——**ALFA AWUS036ACH**。

它用的是 **Realtek RTL8812AU** 芯片，支持 **802.11ac（WiFi 5）**、**2.4GHz / 5GHz 双频**、USB 3.0 Type-C 接口、可拆式天线（RP-SMA）。更重要的是：**wfb-ng 的官方实测硬件，就是在两端都用 AWUS036ACH、跑 5GHz 模式**。换句话说，这张卡是被专案作者验证过、驱动支持最稳定的型号。

为什么选它？三个关键理由：

1. **功率够**：ALFA 一贯的高功率设计，搭配外接高增益天线，长距离表现远胜一般笔电内置网卡。
2. **监控模式 ＋ 注入支持**：RTL8812AU 在打过 patch 的驱动（见下文）下，稳定支持 monitor mode 与 raw 封包注入，这是 wfb-ng 运作的先决条件。
3. **通用耐用**：USB 接口，机载端、地面站端通用，不用为不同机器买不同网卡；单张网卡损坏时也只需更换该卡，维护容易。

{{< alert "triangle-exclamation" >}}
**注意**：wfb-ng 需要**打过 patch 的专用驱动**（如 `rtl88xxau_wfb`），一般 Linux 内置驱动无法进入 wfb-ng 需要的注入模式。安装方式见下文「软件清单」与「Step-by-step 设定」。
{{< /alert >}}

---

## 四、硬件清单（Hardware List）

整个链路分成**机载端（Drone）**与**地面站（Ground Station）**两组。下面分开列出。

### 机载端（Drone）

| 项目 | 建议型号 / 说明 |
|---|---|
| 机载电脑 | Raspberry Pi 3B / 3B+ / Zero 2 W / 4（任选；若要跑 1080p 建议用 **Pi 4 或 Zero 2 W**） |
| 摄影机 | Raspberry Pi Camera（CSI 接口）或 Logitech C920（USB 接口） |
| WiFi 模块 | **ALFA AWUS036ACH**（或任何 RTL8812AU 芯片网卡） |
| 供电 | **5V BEC**（给网卡独立供电，见下文「踩坑提醒」） |
| 滤波电容 | **470µF 低 ESR 电容**（并联在网卡 +5V 与 GND 间） |
| 飞控 | Pixhawk 等（走 MAVLink 协议，经 UART 接机载电脑） |

### 地面站（Ground Station）

| 项目 | 建议型号 / 说明 |
|---|---|
| 电脑 | Linux 电脑（Ubuntu / Debian x86-64），或另一台 Raspberry Pi |
| WiFi 模块 | **ALFA AWUS036ACH** |
| 监控软件 | 执行 **QGroundControl** 的机器（可与地面站电脑同一台） |

> 注：如果**只做接收端（RX）**，任何支持 monitor mode 的网卡都行，例如刷了 OpenWRT 的路由器也能拿来当地面接收。但官方实测与本文设定仍以 AWUS036ACH 为准。

---

## 五、软件清单（Software List）

### 操作系统

- **Raspberry Pi OS** / **Debian** / **Ubuntu**（Linux kernel ≥ 4.x）

### 核心专案

- **wfb-ng**（svpcom/wfb-ng）：数位图传 / 遥测主程序
- **修补版驱动**：
  - RTL8812AU → `svpcom/rtl8812au`（branch **v5.2.20**，用 dkms 安装）
  - RTL8812EU → `svpcom/rtl8812eu`
  - 驱动加载后网卡名称会显示为 `rtl88xxau_wfb`（或 `rtl8812eu`）

### 系统依赖套件

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### 加密

- **libsodium**：用 `wfb_keygen` 产生 `drone.key`（机载端）与 `gs.key`（地面站端）

### 地面站播放

- **QGroundControl**：地面站监控飞控状态与遥测
- **GStreamer / RTSP**：接收并播放机载端串流的影像

---

## 六、GitHub 链接与 ALFA AWUS036ACH 规格小卡

### 官方链接

| 项目 | 链接 |
|---|---|
| wfb-ng 专案 | https://github.com/svpcom/wfb-ng.git |
| 修补版驱动（RTL8812AU） | https://github.com/svpcom/rtl8812au |
| 修补版驱动（RTL8812EU） | https://github.com/svpcom/rtl8812eu |
| ALFA AWUS036ACH 产品页 | https://yupitek.com/zh-cn/products/alfa/awus036ach/ |
| PX4 WFB-ng 教学 | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### ALFA AWUS036ACH 规格小卡

| 规格 | 内容 |
|---|---|
| 芯片 | Realtek **RTL8812AU** |
| 无线标准 | 802.11a / b / g / n / **ac（WiFi 5）** |
| 频段 | **2.4GHz ＋ 5GHz** 双频 |
| 接口 | USB 3.0 **Type-C** |
| 天线 | 2 × 可拆式 **RP-SMA**（2T2R MIMO） |
| 监控模式 | 支持 monitor mode ＋ 封包注入（需 wfb-ng patch 驱动） |
| wfb-ng 驱动 | `rtl88xxau_wfb`（svpcom/rtl8812au, v5.2.20） |
| 定位 | wfb-ng **官方实测卡**（两端 5GHz 模式） |

---

## 七、Step-by-step 设定（核心章节）

下面分四段。最推荐的路径是 **A（Raspberry Pi 快速起步）**，几乎是烧录即用的体验；**B** 则适合想在 x86 Linux 桌面手动安装地面站的人；**C / D** 是密钥配对与设定档重点，两条路都会用到。

### A. Raspberry Pi 快速起步（最推荐）

wfb-ng 官方提供预先打包好的 Raspberry Pi 映像档，机载端与地面站端各烧一张，开机就能用。

**1. 下载并烧录映像档**

到 wfb-ng 的 GitHub **Releases** 页面，下载最新的 `*.img.gz`，解压后烧录到**两张** SD 卡（机载、地面站各一张）。

```bash
# 解压映像档（范例，档名依实际 Release 为准）
gunzip wfb-ng-*.img.gz
# 用 Raspberry Pi Imager 或 dd / balenaEtcher 烧录到 SD 卡
```

**2. 插入网卡、开机、SSH 登录**

两张卡都插上 ALFA AWUS036ACH，上电开机，透过 SSH 登录（预设 IP 与帐密如下）：

```bash
ssh pi@192.168.0.111
# 密码：raspberry
```

**3. 启用地面站（Ground Station）服务**

在**地面站那张 Pi** 上执行：

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. 启用机载端（Drone）服务**

在**机载那张 Pi** 上执行：

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. 在地面站监控链路状态**

```bash
wfb-cli gs
```

> 看到连线、频道、丢包率等信息就代表链路通了。接着打开 QGroundControl，就能看到遥测与影像。

---

### B. Debian / Ubuntu 地面站手动安装

如果你是用 x86-64 的 Linux 桌机 / 笔电当地面站，可以手动安装。

**1. 安装 dkms 与修补版驱动**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. 确认网卡已被 wfb-ng 驱动接管**

```bash
# 应看到 wlan0，且 MTU 为 2312
ifconfig

# 驱动名称应显示 rtl88xxau_wfb（RTL8812AU）或 rtl8812eu（RTL8812EU）
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
如果 `ethtool -i wlan0` 显示的是一般 `rtl8812au` 而非 `rtl88xxau_wfb`，代表 patch 驱动没装好，wfb-ng 会无法进入注入模式。请回头检查 dkms 安装有无报错。
{{< /alert >}}

**3. 执行官方自动安装脚本**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. 监控链路**

```bash
wfb-cli gs
```

---

### C. 密钥与配对

wfb-ng 的影像与遥测是加密的，机载端与地面站端必须用**对应的密钥**才能通讯。

```bash
# 产生密钥（在机载端产生，再分发）
wfb_keygen

# drone.key 放到机载端
# gs.key    放到地面站端
# 两端必须对应，否则无法解密、链路显示「已连线但无数据」
```

> 如果你是用 **B 段的自動安装脚本（install_gs.sh）**，脚本会自动产生并配置密钥，省去手动配对步骤。手动安装则请务必确认 `drone.key` 与 `gs.key` 是同一组。

---

### D. 设定档重点：/etc/wifibroadcast.cfg

`/etc/wifibroadcast.cfg` 是 wfb-ng 的核心设定档。以下是最常需要调整的几个参数：

```ini
[common]
# 频道 165 = 5825 MHz（5.8GHz 频段）
wifi_channel = 165

# 国码设为 'BO'（玻利维亚）可解锁最大发射功率
wifi_region = 'BO'

[drone]
# 机载端与地面站的 link_domain 必须「完全一致」
link_domain = "my_wfb_link_01"

[drone_mavlink]
# 从飞控 UART 接收 MAVLink（需飞控端 UART 设为 1500000 baud）
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# 同上，两端一致
link_domain = "my_wfb_link_01"
```

**三个最容易出错的点：**

1. **`wifi_channel` 两端要一致**：本文用 165（5825 MHz, 5.8GHz），机载与地面站都要设同一个。
2. **`link_domain` 两端要一致**：这是链路的「识别码」，不一样就连不上。
3. **飞控 UART 鲍率要设 1500000**：`peer = 'serial:ttyS0:1500000'` 要求飞控那端的 UART 也设成 1500000 baud，否则 MAVLink 收不到。

{{< alert "triangle-exclamation" >}}
**注意**：`wifi_region = 'BO'` 是为了解锁发射功率上限，但**这不代表你在当地可以合法这样用**。请务必参考下方「法规提醒」。
{{< /alert >}}

---

## 八、实作注意事项 / 踩坑提醒

这一节是我们实作时真正踩过的坑，请务必看。

### ⚠️ 坑 1：网卡供电不足会 reset 端口、疯狂掉包

AWUS036ACH 在**发射（TX）时瞬间耗电很大**。如果直接插在 Raspberry Pi 的一般 USB2 埠，Pi 的 USB 供电不足以撑住瞬间电流，结果是：**网卡端口被 reset、链路断线、封包损坏、画面卡死**。

解法（机载端一定要做）：

- 网卡**直接从 5V BEC 供电**（不要从 Pi 的 USB 取电），BEC 输出接网卡。
- 在网卡的 **+5V 与 GND 之间并联一颗 470µF 低 ESR 电容**做滤波，吸收 TX 瞬间的电流尖峰。
- 地面站端如果是**笔电的 USB3 埠、用原厂 USB3 线**，一般可以直接供电，不必额外 BEC。

> 这一步是「稳不稳」的关键。我们看过太多人卡在掉包，最后都是供电没处理好。

### 坑 2：加密错误 / 连不上

如果 `wfb-cli gs` 显示已连线但**没有影像也没有遥测**，多半是以下两种：

- **密钥不对应**：检查机载的 `drone.key` 与地面的 `gs.key` 是否为同一组。
- **频道或 link_domain 不一致**：两端的 `wifi_channel` 与 `link_domain` 必须完全相同。

排错指令：

```bash
# 看地面站服务的即时日志，找加密 / 连线相关错误
journalctl -xu wifibroadcast@gs
```

### ⚠️ 坑 3：法规（非常重要）

这套链路会主动发射无线电波，属于无线电设备使用行为。

- **使用前请确认你所在地区允许此种 WiFi 用途的发射功率与频段。**
- 台湾、中国、欧美对 5.8GHz ISM 频段的发射功率、可用频点、以及「非连线式发射」各有规范。
- 本文 `wifi_region = 'BO'` 是为了解锁硬件功率上限，但**不代表在当地合法**。请依你所在国家／地区的无线电管理法规调整频道与功率，必要时降低发射功率或改合法频点。
- 仅用于合法场域（如自有农地、闭场测试、教育训练），勿干扰他人通讯。

---

## 九、结语

回头看，我们用一张 ALFA AWUS036ACH，加上开源的 wfb-ng，就做出了一套：

- **成本优势**：整套自制链路的材料费远低于市售数位图传方案；
- **开源**：所有程序代码、驱动、设定都公开可查；
- **可客制**：频道、功率、密钥、MAVLink 对外方式全部自己掌控；
- **长距离**：数位图传 ＋ 遥测一条龙，5GHz 下实测距离远超类比、且抗遮蔽、可加密。

对农喷、巡检、资安教育训练，或是纯粹想搞懂「数位图传背后原理」的同好来说，这是一条非常值得动手走的路。

我们团队会持续在部落格分享 ALFA 网卡在无人机链路上的实作笔记。如果你在架设过程遇到问题，欢迎留言交流——**动手做，才是最快的学习方式**。

---

{{< faq >}}

---

## 附录：新手必懂名词表（关键字白话文）

如果你是第一次接触这类技术，以下用白话文快速说明本文常出现的名词：

| 名词 | 白话解释 |
|---|---|
| **FPV**（First Person View） | 「第一人称视角」，就是坐在无人机的「驾驶座」上看它飞，画面即时从机上镜头传回你眼前的屏幕或眼镜。 |
| **数位图传 vs 类比图传** | 类比图传像老式电视信号，信号差就满屏噪声、可被任何人截收；数位图传把画面转成数位封包传输，可加密、抗噪声能力较好，但硬件与设定较复杂。 |
| **monitor mode（监听模式）** | 一般 WiFi 网卡只能「连上」路由器收发数据。monitor mode 让网卡改成「什么都不连、直接听 / 发空气中的无线电信号」，是本文技术的地基。 |
| **packet injection（封包注入）** | 在 monitor mode 下，直接把自定义的无线电封包「射」到空气中，不透过一般 WiFi 连线流程。wfb-ng 就是利用这个机制传影像与遥测。 |
| **wfb-ng** | 一套开源软件，把 WiFi 网卡「借尸还魂」变成无人机专用的无线电，而不是当一般网络用。本文的核心软件。 |
| **FEC（前向纠错，Forward Error Correction）** | 传输时故意多送一些「备份信息」，就算部分封包在空中遗失，接收端也能用备份信息补回原始画面，不必要求重传（重传在长距离、高速移动场景会拖慢速度）。 |
| **MAVLink** | 无人机飞控（如 Pixhawk）与地面站沟通的「共同语言」协议，用来传飞行状态、下达飞行指令等遥测数据。 |
| **RTP / RTSP** | 网络上传输即时影像常用的协议，你的手机 IP CAM、监视器很多也是用这一类协议串流画面。 |
| **libsodium 加密** | 本文用来加密影像与遥测数据的开源加密函数库，确保只有配对好密钥的机载端与地面站能解密画面内容。 |
| **TX 分集（发射分集）** | 用多张网卡同时发射同一份数据，其中一张信号被遮蔽时，另一张还能补上，类似「双重保险」。 |
| **BEC（Battery Eliminator Circuit）** | 一种稳压供电模块，把无人机电池的电压降到网卡需要的 5V，且能承受网卡瞬间大电流需求，避免供电不稳导致断线。 |
| **RTL8812AU** | ALFA AWUS036ACH 网卡内部使用的 Realtek 芯片型号，决定了这张卡支不支持 monitor mode 与封包注入。 |

> 一句话总结：wfb-ng 把 ALFA 网卡「伪装」成无人机专属的无线电台，让画面与飞控数据能用开源、可加密的方式长距离传输——这是你（操作者）主动架设的一条「自家专属频道」。

---

## 参考资源

- **wfb-ng 专案（svpcom/wfb-ng）**：https://github.com/svpcom/wfb-ng.git
- **ALFA AWUS036ACH 产品页**：https://yupitek.com/zh-cn/products/alfa/awus036ach/
- **修补版驱动（RTL8812AU）**：https://github.com/svpcom/rtl8812au
- **修补版驱动（RTL8812EU）**：https://github.com/svpcom/rtl8812eu
- **PX4 WFB-ng 教学文件**：https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*本文由榆合科技 Yupitek（ALFA Network 台湾授权代理商）技术团队撰写，基于 wfb-ng 官方文件与实作经验整理。实作前请务必确认所在地区无线电法规，并依规范调整发射功率与频段。*
