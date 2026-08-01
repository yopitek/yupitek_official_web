---
title: "树莓派 + OpenWrt 打造 4G/5G 路由器：Sierra 模块完整支持矩阵与实操教程"
description: "用树莓派加 Sierra Wireless 4G/5G 模块（EM7455、EM7565、EM7511、EM919x、MC7455）自制 OpenWrt 路由器。完整支持矩阵、QMI/MBIM 设置、wwan0 上网教程，含供电与天线注意事项，帮你搞定硬件到软件的疑难杂症。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/zh-cn/products/sierra/"
faq:
  - question: "在树莓派上做 OpenWrt 路由器，Sierra 模块该选哪颗？"
    answer: "新手建议选教程多的 EM7455；要高上传选 EM7565/EM7511；要 5G 选 EM919x；旧设备 mPCIe 选 MC7455。"
  - question: "QMI 和 MBIM 有什么区别？"
    answer: "QMI 是 Qualcomm 的协议，MBIM 是后续的标准化协议。在 OpenWrt 上两者都能用，但网络教程以 QMI 居多。"
  - question: "树莓派识别不到模块怎么办？"
    answer: "通常是树莓派 USB 供电不足（需应付 2.5A 浪涌电流），建议检查转接板供电、线材，并等待十秒让设备完全开机。"
---

树莓派能不能拿 Sierra Wireless 的 4G/5G 模块直接做成 OpenWrt 路由器？答案是肯定的。EM7455、EM7565、EM7511、EM919x 这些 M.2 模块，在 Linux 系统里早就是原生可用的乖宝宝。只要装好 `kmod-usb-net-qmi-wwan` 或 `kmod-usb-net-cdc-mbim` 软件包，设置一下 `wwan0`，就能轻松上网。这篇文章整理了完整的模块支持矩阵、设置步骤、供电天线等避坑指南，带你轻松动手做！

{{< tldr >}}
用树莓派加 Sierra 4G/5G 模块当路由器完全可行。多数 M.2 模块（EM7455、EM7565、EM7511）走 USB 接口，EM919x 多一个 PCIe Gen3 通道，MC7455 是 mPCIe 版本的 EM7455。OpenWrt 上最推荐用 QMI 协议加 `wwan0`：装好 `kmod-usb-net-qmi-wwan`、`uqmi`、`luci-proto-qmi`，在 `/etc/config/network` 设置 APN 后重启网络即可连接。速度上：EM7455 / MC7455 是 LTE Cat 6（300/50 Mbps），EM7565 / EM7511 是 Cat 12（600/150 Mbps），EM919x 提供 5G Sub-6（EM9190 支持 mmWave）。
{{< /tldr >}}

## Sierra 模块在 OpenWrt 的完整支持矩阵

动手之前，先来对照一下你手边的模块规格：

| 型号 | 速度等级 | 基带芯片 | 封装形式 | Linux 数据通道 | GNSS 卫星定位 |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM（Linux 均支持） | 多了 QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | 多了 QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6（9190 有 mmWave） | SDX55 | M.2（长度 52mm） | Windows/Linux 均支持 | L1 + L5（选配） |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50.95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### 该怎么选型号？

- **新手玩家**：选 **EM7455**，教程多，出错最好找解答。
- **需要高上传（开直播、监控）**：选 **EM7565** 或 **EM7511**，上传高达 150 Mbps。
- **就是要 5G**：选 **EM9190** 体验 5G 网速。
- **只有旧的 mPCIe 插槽**：那就老老实实买 **MC7455**。

## 硬件该怎么接？三种接法一次看懂

### A. Raspberry Pi 5 + M.2 HAT（走 PCIe）

Pi 5 有 PCIe，加个 M.2 HAT+ 扩展板就能直接插 M.2 WWAN 模块（记得确认是 B-Key）。

### B. Raspberry Pi 4B 或更旧 + USB WWAN 转接盒

因为 EM 系列模块也支持 USB 2.0/3.0，买个 M.2 转 USB 的盒子（里面通常有 SIM 卡座）插到树莓派的 USB 孔上就好，这是最平易近人的做法。

### C. MC7455（mPCIe）转接

这颗是旧的 mPCIe 接口，必须买 mPCIe 转 USB 或转 M.2 的板子。

> ⚠️ **供电大魔王**：模块吃 3.135 至 4.4 V（一般 3.3V）。「识别不到模块」通常是因为树莓派 USB 供电不足！瞬时电流可能会飙到 2.5A，所以电源的余量一定要留宽裕一点。

## 搞懂 QMI 和 MBIM 协议

这两个都是控制 4G/5G 模块上网的协议：

- **QMI**：Qualcomm 自己搞的协议，Linux/OpenWrt 上的教程大多是用这个（网卡叫 `wwan0`）。
- **MBIM**：后来标准化的协议，Windows 和 Linux 都能用（网卡也叫 `wwan0`）。

**选哪个？** 大部分人直接用 QMI 就好。如果你的固件特别要求 MBIM，再换成 MBIM。

## 实战 Part 1：在 OpenWrt 设置 QMI 上网

只要四个步骤，不用自己编译任何东西。

### 1. 装好软件包

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. 确认树莓派识别到了模块

```bash
lsusb                                  # 看看有没有 Sierra 设备
ls /dev/cdc-wdm*                       # QMI 的控制通道
dmesg | grep qmi_wwan                  # 看看驱动有没有加载
ip link show wwan0                     # 看看有没有出现网卡
```

### 3. 设置网络配置文件（`/etc/config/network`）

添加一段 QMI 的设置，记得把 APN 改成你运营商的：

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option auth 'none'
```

### 4. 重启网络

```bash
/etc/init.d/network restart
ifup wwan
```

搞定！`wwan0` 获得 IP 后就能上网了。

## 天线和 SIM 卡：千万别漏掉

模块本身**没有**内置天线！天线的好坏直接决定了你的网速。

- **主天线（Main）**：一定要接。
- **辅助天线（Aux）**：接上才能跑到 MIMO 高速，不接网速打折扣。
- **GNSS 天线**：要用定位才接，别和主天线搞混了。

## 常见踩坑清单（新手必看）

1. **`lsusb` 看不到设备**：99% 是供电不足、转接板没接好或线坏了。
2. **太心急**：模块插上去需要时间开机，等个 10 秒再敲命令。
3. **5G 模块（EM919x）太热**：5G 模块温度高达 100 度都很常见（极限 115°C），记得帮它散热。
4. **树莓派 ModemManager 冲突**：如果在原生 Linux 上手动敲命令，记得先把 `ModemManager` 关掉（`systemctl stop ModemManager`），免得控制权被抢走。

## 总结

用树莓派加 OpenWrt 来驱动 Sierra 模块，其实就是按步骤操作。先确认硬件规格（封装、电压、天线），再到系统装好 QMI/MBIM 相关驱动，最后设置好 APN。希望这篇教程能帮你的项目少走一点弯路，顺利让你的树莓派飙上 4G/5G 网络！

## 采购信息（Call To Action）

如果你需要购买 EM7455、EM7565、EM7511 等模块，或者想找搭配的 M.2 转接板和天线，Yupitek（榆閤科技）提供完整的硬件方案和技术咨询。

欢迎来信：**sales@yupitek.com**

产品入口：[Yupitek Sierra Wireless 全系列](https://yupitek.com/zh-cn/products/sierra/)
