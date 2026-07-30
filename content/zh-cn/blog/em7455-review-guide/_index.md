---
title: "EM7455 完整评测：为什么它是 Maker 与工程师最爱的 Sierra 网卡"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - 产品评测
series:
  - sierra-wireless-selection
series_order: 2
description: "EM7455 完整评测：规格、EM7430 差异、OpenWrt/Linux 设置、Dell/Lenovo 兼容性。本文由 Yupitek（榆合科技）整理提供技术资料。"
author: "yupitek"
draft: false
faq:
  - question: "EM7455 支持 5G 吗？"
    answer: "不支持。EM7455 是 LTE-A Cat 6 模块，最高 300 Mbps。若需要 5G（Sub-6 或 mmWave），可参考 EM9190（Sub-6）或 EM9191（Sub-6 + mmWave）。"
  - question: "EM7455 在中国大陆可以用吗？"
    answer: "EM7455 主要涵盖美洲与 EMEA 频段，在中国大陆的实际可用性取决于当地运营商的频段部署。建议下单前与我们确认你的具体地区与运营商的兼容性。"
  - question: "EM7455 跟 MC7455 差在哪？"
    answer: "核心芯片相同，皆为 Qualcomm MDM9230，规格一致。唯一差别是封装：EM7455 为 M.2，MC7455 为 mPCIe。选哪颗纯看你的插槽。"
  - question: "EM7455 跟 EM7430 差在哪？"
    answer: "同一颗 MDM9230 芯片，核心规格相同。主要差异在于目标频段配置：EM7455 主要涵盖美洲与 EMEA 频段，EM7430 主要涵盖亚太频段，详细频段清单请洽询确认最新官方规格书。"
  - question: "Dell DW5811e 就是 EM7455 吗？"
    answer: "是的，DW5811e 是 Dell 品牌版的 EM7455，核心为同一颗 Qualcomm MDM9230。多数 Dell 笔记本社区反馈不锁 BIOS 白名单，但实际情况建议以你的机型为准。"
---

EM7455 是 Sierra Wireless 的 LTE-A Cat 6 M.2 蜂窝模块，采用 Qualcomm MDM9230 芯片，支持最高 300 Mbps 下载、50 Mbps 上传，内置 GNSS 定位，工作温度 -40°C 至 +85°C。本文由榆合科技（Yupitek）整理提供规格解析与设置参考。

Sierra Wireless EM7455 为 M.2 B-Key 封装的 4G LTE-Advanced Cat 6 模块，广泛应用于 OpenWrt 路由器、树莓派移动基站、工业网关与商用笔记本 WWAN。以下设置步骤为社区与官方文档常见流程整理，实际指令请依你的操作系统版本、固件版本自行核对后执行，执行前建议先备份现有设置。

> 产品链接：[EM7455 — Yupitek 产品页](https://yupitek.com/zh-tw/products/sierra/em7455/) | 官方规格书：[AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## EM7455 完整规格表

以下规格数字整理自 Sierra Wireless 官方规格书与公开资料，实际下单前建议向我们索取最新官方文件逐项核对，尤其是频段、固件版本等会随时间更新的项目。

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
| **LTE 频段** | 涵盖美洲与 EMEA（欧洲/中东/非洲）主流频段，详细频段清单请洽询确认最新官方规格书 |
| **3G WCDMA 频段** | 请洽询确认最新官方规格书 |
| **通用 VID:PID** | `1199:9079`（EM7455，一般版本） |
| **Dell DW5811e VID:PID** | `413c:81b6`（品牌版本，请以实机 `lsusb` 结果为准） |
| **Linux 驱动** | `qcserial`、`qmi_wwan`、`cdc_mbim`（主流发行版皆已内置，具体最低 kernel 版本请以你的发行版说明为准） |
| **通用固件** | 请以官方 source.sierrawireless.com 最新版本为准，本文不写死特定版本号以免过时 |
| **运营商认证** | 依运营商与地区时有变动（如 AT&T、Verizon、T-Mobile、Bell、Rogers、Telus、Vodafone 等），请洽询确认你所在地区最新认证清单 |

---

## EM7455 适合什么用途？

**EM7455 最适合三类用途：（1）自组 4G LTE 路由器（OpenWrt / ROOter），（2）笔记本 WWAN 升级（Dell / Lenovo），（3）工业物联网网关与车联网 telematics。** 它的核心优势在于 Linux 驱动成熟度高、社区资源丰富，以及美洲/EMEA 频段覆盖较广。

### 个人 Maker 场景

| 应用 | 搭配 | 理由 |
|---|---|---|
| 树莓派 4G 路由器 | 树莓派 4/5 + M.2→USB 转接板 + OpenWrt / ROOter | EM7455 在 OpenWrt 社区案例中兼容性稳定，uqmi 套件成熟 |
| GL.iNet 路由器升级 | GL-MT1300 / GL-AR750S + USB 转接 | 社区已有 ROOter 挂钩与 `create_connect.sh` 相关讨论可参考 |
| 户外便携式 LTE 热点 | 电池供电 + USB 转接 + 小型路由器 | EM7455 发热低、散热良好，适合物件追踪 |

### 企业 / 工业场景

| 应用 | 搭配 | 理由 |
|---|---|---|
| 工业路由器 | M.2 插槽工业网关（如 Advantech、Cincoze） | 宽温 -40~85°C，频段涵盖范围广 |
| 车联网 telematics | 车载网关 + GNSS 天线 | 内置 GPS/GLONASS/BeiDou/Galileo，单一模块解决联网＋定位 |
| 笔记本 WWAN 升级 | Dell Latitude / Precision / Lenovo ThinkPad | M.2 B-Key 直插，Linux 驱动支持度高 |
| 备用 WAN | OpenWrt / pfSense 双 WAN 备用 | QMI/MBIM 双模式支持，惟 pfSense 支持度相对较弱，建议优先评估 OpenWrt |

---

## EM7455 跟 EM7430 差在哪？

**EM7455 与 EM7430 采用同一颗 Qualcomm MDM9230 芯片，核心规格相同（Cat 6、300/50 Mbps、2×CA、GNSS），主要差异在于目标频段配置：EM7455 主要涵盖美洲与 EMEA 频段，EM7430 主要涵盖亚太（APAC）频段。**

| 项目 | EM7455 | EM7430 |
|---|---|---|
| **芯片组** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **蜂窝标准** | LTE-A Cat 6 | LTE-A Cat 6 |
| **下载峰值** | 300 Mbps | 300 Mbps |
| **上传峰值** | 50 Mbps | 50 Mbps |
| **载波聚合** | 2×CA | 2×CA |
| **封装** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **目标区域** | 美洲、EMEA（欧洲/中东/非洲） | 亚太（APAC） |
| **详细频段清单** | 请洽询确认最新官方规格书 | 请洽询确认最新官方规格书 |

> 两款模块的精确逐频段清单目前建议以官方最新 Spec Sheet 为准，本文暂不列出逐频段编号，避免信息随官方版本更新而过时或不准确。若您已知道所在地区使用的运营商与频段需求，欢迎直接与我们联系核对哪一款更适合。

**选型建议**：若你的 SIM 卡运营商以北美或欧洲为主，可优先评估 **EM7455**；若主要使用亚太地区运营商（如中国大陆、日本、澳洲等），可优先评估 **EM7430**。

---

## EM7455 vs MC7455：同一颗芯片，只差封装

EM7455（M.2）与 MC7455（mPCIe）采用同一个 Qualcomm MDM9230 芯片组，核心电气规格相同。主要差别是**封装接口**：

| 项目 | EM7455 | MC7455 |
|---|---|---|
| **封装** | M.2（B-Key） | Mini PCIe（mPCIe） |
| **尺寸** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **适合设备** | 笔记本 WWAN 槽、现代 M.2 主板 | 旧款工业路由器 mPCIe 插槽 |
| **通用 VID:PID** | `1199:9079` | `1199:9071` |

**选哪个纯看你的设备插槽**。若主板只有 M.2，选 EM7455；若只有 mPCIe，选 MC7455。若选错封装，可通过转接板（M.2→mPCIe 或 mPCIe→M.2）解决。

---

## Linux 设置（Ubuntu / Debian / Linux Mint）

EM7455 在主流 Linux 发行版上驱动支持度较高，以下为社区常见的基本设置步骤，实际环境（发行版版本、kernel 版本、固件版本）可能造成细节差异，建议先在测试环境验证过再导入正式系统。

### 步骤 1：硬件检测

```bash
lsusb | grep -i sierra
# 预期输出类似：Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### 步骤 2：安装工具套件

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### 步骤 3：切换 USB 组合模式为 QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# 验证组合模式
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# 预期结果类似：USB composition 6: DM, NMEA, AT, QMI
```

> 若只要 MBIM 模式（部分运营商要求），可查询 `AT!USBCOMP` 相关设置并使用 `mbimcli`，实际数值请以官方 AT 指令参考文件为准。

### 步骤 4：FCC Auth 解锁

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# 若使用 ModemManager 内置自动化：
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### 步骤 5：NetworkManager 连接

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn '你的APN'
sudo nmcli connection up 'EM7455 LTE'
```

### 步骤 6：手动 QMI 连接（进阶/排错）

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='你的APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## OpenWrt QMI 设置

EM7455 在 OpenWrt 上是社区反馈兼容性较好的型号之一，以下是 QMI 模式的基本设置范例。

### 安装套件

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### 编辑网络配置文件

编辑 `/etc/config/network`，新增以下接口设置：

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn '你的APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### 重启网络

```bash
/etc/init.d/network restart
```

若用 LUCI Web 界面：网络 → 接口 → 新增新接口 → 协议选「QMI」，设备选 `/dev/cdc-wdm0`，填入 APN 即可。

> ROOter（基于 OpenWrt 的蜂窝路由固件）对 Sierra QMI 模块有社区反馈的支持案例，内置 `create_connect.sh` 相关挂钩，若你是树莓派玩家，可评估直接使用 ROOter 固件，惟正式支持范围建议以 ROOter 官方公告为准。

---

## 品牌机兼容性：Dell / Lenovo 笔记本

### Dell 笔记本（DW5811e 对应 EM7455 平台）

Dell DW5811e 是 Dell 品牌版的 EM7455（VID `413c`、PID `81b6`），核心芯片同为 Qualcomm MDM9230。多数主流 Linux 发行版的 `qmi_wwan` 驱动已收录常见品牌版 ID，实际是否需要额外设置，建议先实测确认：

```bash
lsusb | grep 413c
# 预期类似：Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

Dell 多数机型（Latitude、Precision、XPS）过往社区反馈不设 BIOS 白名单，DW5811e 多可直接安装使用，但实际情况可能因机型与 BIOS 版本而异，建议以你手上的实际机型为准。

### Lenovo 笔记本（EM7455 FRU）

Lenovo ThinkPad 有 BIOS 白名单限制的相关社区反馈——部分机型只认 Lenovo FRU 版本的模块。以下是社区讨论中曾出现、用于尝试绕过此限制的 AT 指令范例：

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **这组指令我们尚未逐一核对原始出处与正确性，且属于改动模块底层固件行为的操作，执行错误有导致模块无法使用（俗称「变砖」）的风险**。这是整理自公开社区讨论的范例，并非 Yupitek 已验证过的标准流程。若你要尝试，强烈建议：先确认并备份当前固件版本、仅在非关键测试环境操作、且自行承担操作风险。若不确定，建议直接与我们联系讨论你的实际需求与可行方案。

### ThinkPad 机型（社区反馈曾用于此类设置的机型）

以下清单整理自社区讨论，实际是否适用及是否需要 BIOS/固件更新，请以你手上机型的官方规格与 BIOS 版本为准，我们建议下手前先与我们或 Lenovo 官方渠道确认：

- 60 系列：T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- 70 系列：T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## 平台兼容性总览

| 平台 | 支持度 | 连接方式 | 备注 |
|---|---|---|---|
| 树莓派 + OpenWrt | ✅✅ 社区案例较多 | QMI / MBIM | 需 M.2→USB 转接板 |
| 树莓派 + ROOter | ✅✅ | QMI（社区反馈内置挂钩） | 建议树莓派玩家优先评估 |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | 主流发行版驱动支持度较高 |
| DD-WRT | ⚠️ 支持度较弱 | QMI / PPP | 需较新 BETA build，社区案例有限 |
| pfSense / FreeBSD | ⚠️ 支持度较弱 | QMI / PPP（多走 AT command） | FreeBSD 原生蜂窝驱动有限，需个案评估 |
| Dell 笔记本（DW5811e） | ✅ | QMI / MBIM | 多数主流发行版可识别，个别机型建议实测 |
| Lenovo 笔记本 | ⚠️ 需额外设置 | QMI | 部分机型有 BIOS 白名单限制，处理方式风险较高，见上方说明 |

---

## 社区资源与延伸阅读

以下是与 EM7455 相关、公开可查的社区与官方资源，供进一步研究参考：

- **danielewood/sierra-wireless-modems**：EM7455/MC7455 相关设置脚本与社区讨论：[GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)**：Linux 设置相关社区整理（含 kernel 选项、固件更新、疑难排解）：[Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE 维基**：官方 LTE 调制解调器支持列表与设置：[OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen**：工程模式相关工具，可能涉及 PRI 与频段设置：[GitHub](https://github.com/bkerler/SierraWirelessGen)

> 以上第三方资源链接内容非我们维护，实际使用前请自行评估其正确性与时效性。

---

## 常见问题 FAQ

**Q1：EM7455 支持 5G 吗？**
不支持。EM7455 是 LTE-A Cat 6 模块，最高 300 Mbps。若需要 5G（Sub-6 或 mmWave），可参考 EM9190（Sub-6）或 EM9191（Sub-6 + mmWave）。

**Q2：EM7455 在中国大陆可以用吗？**
EM7455 主要涵盖美洲与 EMEA 频段，在中国大陆的实际可用性取决于当地运营商的频段部署。建议下单前与我们确认你的具体地区与运营商的兼容性。

**Q3：EM7455 跟 MC7455 差在哪？**
核心芯片相同，皆为 Qualcomm MDM9230，规格一致。唯一差别是封装：EM7455 为 M.2，MC7455 为 mPCIe。选哪颗纯看你的插槽。

**Q4：EM7455 在 Ubuntu 上识别不到怎么办？**
先确认 `lsusb` 是否看到 `1199:9079`，若没有可尝试改用 USB 2.0 端口（部分案例中 USB 3.0 可能造成干扰）。接着确认 `qcserial` 与 `qmi_wwan` 已加载：执行 `lsmod | grep qmi`。也可尝试停用 ModemManager（`systemctl stop ModemManager`）再手动执行 `qmicli` 排查。若仍无法解决，建议与我们联系协助排查。

**Q5：Dell DW5811e 就是 EM7455 吗？**
是的，DW5811e 是 Dell 品牌版的 EM7455，核心为同一颗 Qualcomm MDM9230 芯片。Dell 版本在二手市场流通量较大、取得成本相对较低，且多数 Dell 笔记本社区反馈不锁 BIOS 白名单，但实际情况建议以你的机型为准。

---

## 联系采购

以上 EM7455 规格与设置信息由榆合科技（Yupitek）整理提供。若需采购 EM7455、EM7430、MC7455 或 Sierra Wireless 全系列蜂窝模块，请至产品页查询报价或联系技术团队。

- **产品页**：[https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **全系列产品**：[https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **Email**：sales@yupitek.com
