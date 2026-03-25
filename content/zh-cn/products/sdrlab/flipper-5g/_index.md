---
title: "SDRLab Flipper Zero 5G 扩充板 — 双频 Wi-Fi 安全研究模组"
description: "Flipper Zero 5G 扩充板，RTL8720DN 双频（2.4+5GHz）Wi-Fi，BLE 5.0，预烧 Deauth 固件，GPIO 供电，兼容 Momentum/Unleashed。"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Flipper Zero 扩充", "5GHz", "Wi-Fi", "Deauth", "信息安全研究"]
---

{{< alert "warning" >}}
**合法使用声明**：本扩充板仅供授权的信息安全研究及合法研究使用。请确认符合当地无线频率使用法规。
{{< /alert >}}

## 产品特色

![SDRLab Flipper Zero 5G 扩充板](/images/products/sdrlab/flipper-5g.png)

- **双频覆盖** — 2.4 GHz + 5 GHz（IEEE 802.11 a/b/g/n）；可探测过去仅 2.4 GHz 扩充板无法访问的现代 5 GHz 网络
- **Realtek RTL8720DN（AI Thinker BW16 模块）** — 行业标准双频 SoC，具 FCC/CE 预认证模块
- **双核心 CPU** — ARM Cortex-M4 @ 200 MHz 处理主动协议；Cortex-M0 @ 20 MHz 执行低功耗后台任务
- **预载 Marauder 5G 固件** — 包含扫描、Deauth、Beacon 洪水、数据包嗅探（EAPOL/PMKID）及 Evil Portal 模式；即插即用
- **BLE 5.0** — 蓝牙低功耗设备枚举与信标分析，与 Wi-Fi 研究并行
- **GPIO 供电** — 直接取用 Flipper Zero GPIO 排针的 5 V；无需额外电源供应器
- **天线升级路径** — 支持版本配备 IPEX（U.FL）连接器，可外接高增益天线
- **固件生态兼容** — 兼容 Momentum 与 Unleashed 自定义固件框架
- **PlatformIO 开发** — 通过 Arduino 兼容的 Ameba D 框架提供完整自定义固件开发支持
- **坚固工作范围** — −40°C 至 85°C，适合各种气候环境的野外使用

## 产品规格

| 规格项目 | 数值／说明 |
|---------|-----------|
| 主芯片 | Realtek RTL8720DN（AI Thinker BW16 模块）|
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Wi-Fi 标准 | IEEE 802.11 a/b/g/n（2.4 GHz + 5 GHz 双频）|
| Wi-Fi 发射功率 | ~17 dBm（受地区法规限制）|
| 蓝牙 | BLE 5.0 |
| Flash | 4 MB |
| 供电来源 | Flipper Zero GPIO（5 V）|
| 典型电流消耗 | 150–250 mA（主动扫描时）|
| 连接接口 | Flipper Zero 标准 GPIO 排针（2×8 针）|
| 预载固件 | Marauder 5G（扫描、Deauth、Beacon、嗅探、Evil Portal）|
| 固件兼容 | Momentum、Unleashed |
| 二次开发 | PlatformIO（Ameba D / RTL8720DN 框架）|
| 工作温度 | −40°C 至 85°C |
| 天线接口 | IPEX（U.FL）或板载 PCB 天线（依版本）|
| 外形规格 | Flipper Zero GPIO 扩充板 |

## 应用环境

- **双频 Wi-Fi 扫描** — 被动枚举 2.4 GHz 与 5 GHz 网络；获取 SSID、BSSID、频道、RSSI、加密类型及连接客户端
- **Wi-Fi Deauth 安全研究** — 发送 802.11 Deauth 数据包测试网络韧性，并评估已授权网络的 802.11w/PMF（受保护管理帧）防护能力
- **WPA 握手包捕获** — 嗅探 EAPOL/PMKID 握手包，用于授权网络安全审计
- **Evil Portal 开发** — 在授权环境下原型设计恶意 AP 入口，用于网络钓鱼意识测试
- **Beacon 洪水测试** — 广播自定义 SSID 以研究射频拥塞影响及客户端行为
- **BLE 设备枚举** — 扫描并识别附近的 BLE 5.0 外围设备，与 Wi-Fi 研究同步进行
- **网格网络拓扑映射** — 识别网格 AP 关系、回程频道及隐藏 SSID 配置
- **IoT 无线协议研究** — 在受控实验室环境中分析 IoT 设备在双频上的行为
- **授权渗透测试教育** — 在授权环境下学习 Wi-Fi 安全基础的实践平台

---

{{< alert "warning" >}}
**初次使用此扩充板？** 请参考我们的分步骤初学者指南，涵盖前置条件、固件设置、首次 5G 扫描及所有核心功能。
[📖 打开在线使用手册](/zh-cn/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
需要询问报价？[联系我们](/zh-cn/contact/)
{{< /alert >}}
