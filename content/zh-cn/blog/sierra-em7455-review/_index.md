---
title: "Sierra EM7455 完整评测：为什么它是 Maker 与实验室做课题最爱的 Sierra 网卡"
description: "EM7455 完整评测：规格、与 EM7430 的差异、OpenWrt/Linux 配置、Dell/Lenovo 兼容性。本文由 Yupitek（榆合科技）整理提供技术资料。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "EM7455 支持 5G 吗？"
    answer: "不支持。它是一张 LTE-A Cat 6 的模块，速度最快是 300 Mbps。如果需要 5G，要看 EM9190 或 EM9191。"
  - question: "EM7455 在国内能用吗？"
    answer: "需要搭配支持对应频段的运营商使用，实际信号与支持频段依基站位置而定，建议下单前先确认你所在地区与运营商的兼容性。"
  - question: "EM7455 和 MC7455 有什么区别？"
    answer: "核心都是 Qualcomm MDM9230 芯片，规格完全一致。唯一差别是外观封装：EM7455 为 M.2，MC7455 为 mPCIe。选哪张只看你的插槽。"
  - question: "EM7455 和 EM7430 有什么区别？"
    answer: "同一颗 MDM9230 芯片，核心规格一样。主要差异在支持的频段不同：EM7455 覆盖美洲与 EMEA 频段，EM7430 覆盖亚太频段。"
  - question: "Dell DW5811e 就是 EM7455 吗？"
    answer: "是的，DW5811e 是 Dell 贴牌版的 EM7455，核心为同一颗 Qualcomm MDM9230。"
---

# Sierra EM7455 完整评测：为什么它是 Maker 与实验室做课题最爱的 Sierra 网卡

如果你在玩树莓派加 OpenWrt，或者想帮实验室的设备升级 4G 网络，那你一定听过 Sierra EM7455 这张神卡！它是 Sierra Wireless 推出的一款 LTE-A Cat 6 M.2 蜂窝模块，搭载 Qualcomm MDM9230 芯片，最高支持 300 Mbps 的下载和 50 Mbps 的上传速度，还内置了 GNSS 定位功能，工作温度甚至能扛住 -40°C 到 +85°C 的极端环境。

这篇文章由榆合科技（Yupitek）整理，带大家看懂这张 M.2 B-Key 封装的 4G LTE-Advanced Cat 6 模块为什么这么火，以及怎么在 Linux 系统下把驱动和配置搞定。

> 产品链接：[EM7455 — Yupitek 产品页](/zh-cn/products/sierra/em7455/) | 官方规格书：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完整规格表：硬核数据一次看

下面的数字都是从 Sierra Wireless 官方规格书整理出来的。老话一句，如果真的要下单做项目，建议先找我们索取最新版的官方文档核对一下，尤其是频段或固件版本这类可能会更新的项目。

| 项目 | 规格 |
|---|---|
| **型号** | AirPrime EM7455 |
| **蜂窝标准** | LTE-A Cat 6 |
| **芯片组** | Qualcomm MDM9230（Snapdragon X7 LTE） |
| **下载峰值** | 300 Mbps（LTE-A，2×CA） |
| **上传峰值** | 50 Mbps（LTE-A） |
| **载波聚合** | 2×CA（支持多种组合，详见官方 AT 指令参考） |
| **封装** | PCI Express M.2 B-Key（52-pin） |
| **尺寸** | 42 × 30 × 2.3 mm |
| **工作温度** | -40°C ~ +85°C（工业级） |
| **GNSS** | GPS、GLONASS、BeiDou、Galileo |
| **通信接口** | USB 3.0 / USB 2.0 High Speed |
| **LTE 频段** | 覆盖美洲与 EMEA（欧洲/中东/非洲）主流频段，详细频段清单请咨询确认最新官方规格书 |
| **3G WCDMA 频段** | 请咨询确认最新官方规格书 |
| **通用 VID:PID** | `1199:9079`（EM7455，一般版本） |
| **Dell DW5811e VID:PID** | `413c:81b6`（品牌版本，请以实机 `lsusb` 结果为准） |
| **Linux 驱动** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主流发行版基本都内置了） |
| **通用固件** | 请以官方 source.sierrawireless.com 最新版本为准 |
| **运营商认证** | 依地区时有变动（例如 AT&T、Verizon、Vodafone 等），请咨询确认最新清单 |

---

## EM7455 适合拿来做什么项目？

**简单来说，EM7455 绝对是以下三种应用的救星：（1）自己用开源系统搭 4G LTE 路由器（比如 OpenWrt 或 ROOter）、（2）帮 Dell 或 Lenovo 笔记本升级 WWAN 上网卡、（3）工控实验室做的物联网网关或车联网追踪。**

它最大的优势就在于 Linux 驱动太成熟了，社区网络上一堆教程资源，而且支持的频段也很广。

### 如果你是 Maker 或学生在做课题

| 应用 | 怎么搭配 | 为什么选它 |
|---|---|---|
| 树莓派 4G 路由器 | 树莓派 4/5 + M.2转USB板 + OpenWrt / ROOter | 在 OpenWrt 社区里兼容性超稳，uqmi 套件也很好用 |
| GL.iNet 路由器升级 | GL-MT1300 / GL-AR750S + USB 转接 | 网上找得到 ROOter 的 `create_connect.sh` 配置讨论可以直接抄作业 |
| 户外便携 LTE 热点 | 电池供电 + USB 转接 + 小型路由器 | 发热低散热好，带出去做物件追踪很合适 |

### 如果是企业项目或工业应用

| 应用 | 怎么搭配 | 为什么选它 |
|---|---|---|
| 工业路由器 | 带 M.2 插槽的工业网关（如 Advantech） | 耐造，-40~85°C 的宽温规格很安心，频段也够多 |
| 车联网 telematics | 车载网关 + GNSS 天线 | 有内置 GPS/GLONASS 等定位功能，联网加定位一张卡搞定 |
| 笔记本 WWAN 升级 | Dell Latitude / Lenovo ThinkPad 系列 | M.2 B-Key 直接插上去，Linux 即插即用概率很高 |
| 备份 WAN | OpenWrt / pfSense 双 WAN 备份 | 支持 QMI/MBIM 双模式（不过 pfSense 支持度比较玄学，建议用 OpenWrt） |

---

## EM7455 和 EM7430 到底有什么区别？

大家经常问这个问题。其实 **EM7455 和 EM7430 用的根本是同一颗 Qualcomm MDM9230 芯片，所以核心规格（比如 Cat 6、300/50 Mbps、2×CA、GNSS）一模一样。它们最大的差别在于「主打的市场频段不同」**。EM7455 主要面向美洲和欧洲/中东/非洲（EMEA），而 EM7430 主要面向亚太（APAC）地区。

| 项目 | EM7455 | EM7430 |
|---|---|---|
| **芯片组** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **蜂窝标准** | LTE-A Cat 6 | LTE-A Cat 6 |
| **下载峰值** | 300 Mbps | 300 Mbps |
| **上传峰值** | 50 Mbps | 50 Mbps |
| **载波聚合** | 2×CA | 2×CA |
| **封装** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **目标区域** | 美洲、EMEA | 亚太（APAC） |

**选型小建议**：如果你课题或设备的 SIM 卡以北美或欧洲为主，选 **EM7455**；如果在亚太区（像日本、澳洲等），理论上 **EM7430** 更对口。不过因为各运营商频段配置差异比较大，下单前最好先找我们确认一下你的运营商配哪一张更合适。

---

## EM7455 vs MC7455：完全一样的芯片，只差引脚形状

前面讲过，EM7455（M.2）和 MC7455（mPCIe）都用同一颗 Qualcomm MDM9230，电气规格完全一样。唯一的差别就是那层「皮」（封装）：

| 项目 | EM7455 | MC7455 |
|---|---|---|
| **封装** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **尺寸** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **适合设备** | 笔记本 WWAN 槽、现代开发板 | 比较旧的工控机 mPCIe 插槽 |
| **通用 VID:PID** | `1199:9079` | `1199:9071` |

**这题很简单，看你的设备插槽长什么样就选哪张。** 万一选错了，其实也能买转接板（M.2 转 mPCIe 或反过来）来补救。

---

## 在 Linux 下怎么配置？（Ubuntu / Debian / Linux Mint 适用）

EM7455 在常见的 Linux 系统上支持度非常好，下面分享社区常用的基础配置步骤。不过记得，每台机器的系统版本或 kernel 都不太一样，建议先在测试机上试一遍，不要直接上生产环境。

### 步骤 1：检查有没有抓到硬件

```bash
lsusb | grep -i sierra
# 应该会看到类似这个输出：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 步骤 2：把该装的工具装一装

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 步骤 3：把 USB 模式切换成 QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# 检查一下模式切换成功没
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 应该会看到：USB composition 6: DM, NMEA, AT, QMI
```

> 如果有些特定的运营商要求走 MBIM 模式，你可以去查 `AT!USBCOMP` 这个指令然后改用 `mbimcli` 来连接。

### 步骤 4：解锁 FCC Auth

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# 如果你是用 ModemManager 想要全自动的话：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 步骤 5：用 NetworkManager 连上网

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn '你的APN'
sudo nmcli connection up 'EM7455 LTE'
```

### 步骤 6：手动 QMI 连接（如果你想进阶排错的话）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='你的APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## 如果你玩 OpenWrt，可以这样配置 QMI

EM7455 在 OpenWrt 社区里的评价很高，如果你有台路由器刷了 OpenWrt，可以参考下面的 QMI 配置方式。

### 安装必要套件

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### 编辑网络配置文件

打开 `/etc/config/network`，加上这段接口配置：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### 把网络重新启动

```bash
/etc/init.d/network restart
```

如果你比较喜欢点鼠标（LUCI Web 界面）：到「网络」→「接口」→ 新增接口，协议选「QMI」，设备选 `/dev/cdc-wdm0`，把你的 APN 填进去就搞定了。

> 小贴士：如果你是玩树莓派的同学，强烈建议可以试试 ROOter（一个基于 OpenWrt 专门搞 4G/5G 路由的固件），里面内置了很多方便的配置钩子。

---

## 品牌笔记本兼容性问答：Dell 与 Lenovo

### Dell 笔记本（有张卡叫 DW5811e 就是它）

网上经常看到 Dell DW5811e，其实它就是 Dell 贴牌版的 EM7455（VID 变成了 `413c`、PID 变成了 `81b6`），里面的芯片一模一样是 MDM9230。大部分的 Linux `qmi_wwan` 驱动早就认识它了。

```bash
lsusb | grep 413c
# 应该会看到类似：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

好消息是，Dell 大部分笔记本（像 Latitude, Precision 等等）据社区讨论，通常没有锁讨厌的 BIOS 白名单，所以常常可以直接插上去用。

### Lenovo 笔记本（麻烦的白名单）

如果你用的是 Lenovo ThinkPad，就要小心了。这家有时候会在 BIOS 里设白名单，只准你用 Lenovo 原厂 FRU 版本的卡。论坛上有些大神分享了绕过限制的 AT 指令，给有挑战精神的同学参考：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **警告：这些指令是从论坛扒下来的，如果执行不当可能会把网卡变成砖头！** 如果你不是那种喜欢拆装硬件、承担风险的进阶玩家，建议下单前先问问我们有没有更安全的替代方案。

---

## 到底支持哪些平台？一张表看懂

| 你的平台 | 支持度 | 连接方式 | 备注 |
|---|---|---|---|
| 树莓派 + OpenWrt | ✅✅ 超稳，教程多 | QMI / MBIM | 要自己买一张 M.2 转 USB 的小板子 |
| 树莓派 + ROOter | ✅✅ | QMI | 强烈推荐给树莓派玩家 |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | 即插即用概率非常高 |
| DD-WRT | ⚠️ 要看运气 | QMI / PPP | 网上没什么人讨论，不建议新手碰 |
| pfSense | ⚠️ 很玄学 | QMI / PPP | 建议评估改用 OpenWrt 比较不折腾 |
| Dell 笔记本 | ✅ | QMI / MBIM | 基本上 Linux 都抓得到 |
| Lenovo 笔记本 | ⚠️ 可能要破解 | QMI | 小心 BIOS 白名单，乱刷指令有变砖风险 |

---

## 哪里找更多资源？

做课题如果卡住，可以去这几个开源社区挖宝：

- **danielewood 的 GitHub**：有 EM7455/MC7455 很完整的脚本和讨论区。
- **Gentoo Wiki**：Linux 大神们在那里整理了很详尽的故障排查。
- **OpenWrt LTE Wiki**：官方的文档，配置网络前必看。

## 常见问题快速 Q&A

{{< faq >}}

---

## 实验室想采购？找我们就对了

这篇文章是由榆合科技（Yupitek）的工程团队整理出来的。不管是做大学课题、实验室项目，还是企业需要大量采购 EM7455 或其他 Sierra 模块，都可以来找我们讨论！

- **逛逛这张卡**：[https://yupitek.com/zh-cn/products/sierra/em7455/](/zh-cn/products/sierra/em7455/)
- **看所有 Sierra 型号**：[https://yupitek.com/zh-cn/products/sierra/](/zh-cn/products/sierra/)
- **寄信问我们**：sales@yupitek.com
