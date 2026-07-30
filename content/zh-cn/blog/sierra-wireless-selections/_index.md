---
title: "Sierra Wireless 十款蜂窝模块完整选购指南：LTE Cat 4 到 5G mmWave 怎么选"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - cellular-module
  - 4g-lte
  - 5g-nr
  - module-selection
  - em7455
  - em9190
  - m2-pcie
  - wireless-communication
categories:
  - 产品选型指南
series:
  - sierra-wireless-selection
series_order: 1
description: "榆阖科技整理 Sierra Wireless（Semtech）十款蜂窝模块 EM/MC 系列规格比较与选型建议，横跨 LTE Cat 4 到 5G mmWave。全系列 Sierra Wireless 模块采购请洽 Yupitek。"
author: "yupitek"
draft: false
faq:
  - question: "Sierra Wireless 有哪些型号？彼此差在哪？"
    answer: "Sierra Wireless 现有 EM 与 MC 两大系列共十款模块，横跨 LTE Cat 4 / Cat 6 / Cat 12 到 5G Sub-6 与 mmWave。最大差异在封装：EM 为 M.2、MC 为 mPCIe；同芯片型号（如 EM7455 与 MC7455）效能相同，只差插槽形状。"
  - question: "EM7455 跟 MC7455 是同一颗芯片吗？"
    answer: "是的。两者都采用 Qualcomm MDM9230 芯片组，下载/上传峰值同为 300 / 50 Mbps、支持 2×CA 载波聚合，规格完全一致，唯一差别是 EM7455 为 M.2、MC7455 为 mPCIe 封装。"
  - question: "5G 模块一定要选 mmWave（EM9191）吗？台湾可以用吗？"
    answer: "不一定。台湾电信目前以 Sub-6 为主，mmWave 主要部署于美规场域（如 n260/n261）。一般台湾应用选 EM9190（Sub-6 平价 5G）即可；仅有美规毫米波需求才需 EM9191。"
  - question: "M.2 和 mPCIe 蜂窝模块该怎么选？"
    answer: "看你的设备插槽。笔电、现代嵌入式主板多为 M.2 B-Key，选 EM 系列；旧款工业路由器、工控机若为 mPCIe 槽，选 MC 系列。若板子只有 M.2 却想用 MC，需加 M.2 to mPCIe 转接板。"
  - question: "Sierra Wireless 台湾哪里买？"
    answer: "台湾可通过榆阖科技（Yupitek）采购 Sierra Wireless 全系列蜂窝模块。请至 Yupitek 官网产品页查询型号与报价，或直接 email: sales@yupitek.com"
---

采购蜂窝模块最怕「规格表看不懂、型号一堆搞不清、买错封装插不进机器」。这篇文章把 Sierra Wireless 现役与长青款共十款模块一次讲清楚，帮你从 LTE Cat 4 一路选到 5G mmWave。

Sierra Wireless 现隶属 Semtech。本文由榆阖科技（Yupitek）整理，涵盖 Sierra Wireless 共十款蜂窝模块：EM7430、EM7455、EM7511、EM7565、EM9190、EM9191、MC7304、MC7350、MC7354、MC7455。其中 EM 系列为 M.2 封装、MC 系列为 mPCIe 封装。

本文技术资料由榆阖科技（Yupitek）整理。

Sierra Wireless 十款模块横跨 LTE Cat 4 / 6 / 12 到 5G Sub-6 与 mmWave。EM 与 MC 系列只差封装：EM 为 M.2、MC 为 mPCIe。

## 十款规格总表

先上表格，数字依官方 Spec Sheet 填写，方便你直接比对。EM9190/EM9191 的上行峰值目前不同资料来源略有出入，实际采购前请以最新官方 Spec Sheet 或洽询确认（详见文末附录链接）。

| 型号 | 蜂窝标准 | 芯片组 | 下载 / 上传峰值 | 载波聚合 | 5G | mmWave | 封装 | GNSS | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/zh-CN/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 入门 Cat 6（实际频段配置请洽询确认） |
| [EM7455](https://yupitek.com/zh-CN/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 社群最热门、教学最多 |
| [EM7511](https://yupitek.com/zh-CN/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 高上行 Cat 12 |
| [EM7565](https://yupitek.com/zh-CN/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 支持 CBRS/LAA 频段（实际认证范围请洽询确认）、最多频段、最高上行 |
| [EM9190](https://yupitek.com/zh-CN/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下行 2.5 Gbps（上行峰值请洽询确认） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 平价 5G 入门 |
| [EM9191](https://yupitek.com/zh-CN/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下行最高 4.5 Gbps（含 mmWave）/ Sub-6 2.5 Gbps（上行峰值请洽询确认） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 旗舰 5G、含毫米波 |
| [MC7304](https://yupitek.com/zh-CN/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | 入门 Cat 4（接近 EOL） |
| [MC7350](https://yupitek.com/zh-CN/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、北美频段 |
| [MC7354](https://yupitek.com/zh-CN/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、全球频段 |
| [MC7455](https://yupitek.com/zh-CN/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | mPCIe 版 EM7455 |

> 备注：EM9190 与 EM9191 共用同一份 EM919x/EM7690 规格书；EM9190 为 Sub-6 平价 5G，EM9191 加 mmWave 为旗舰。该份官方规格书为会员登录下载，我们目前引用的下行峰值数字系整理自公开资料，上行峰值等细节数字建议下单前直接向我们确认最新版本。

## EM 系列（M.2）vs MC 系列（mPCIe）封装差异

这是选型第一道关卡，也是最多人买错的地方。

**EM 系列 = M.2 B-Key 封装**：体积小（约 30×42 mm），专为笔电 WWAN 槽、嵌入式 M.2 插槽设计，现代工控主板与迷你 PC 多数采用。

**MC 系列 = Mini PCIe（mPCIe）封装**：外观与一般电脑扩展卡相同，适合旧款工业路由器、工控机的 mPCIe 插槽。若你的板子只有 M.2 槽，MC 系列需加转接板（M.2 to mPCIe）才能使用。

**共同硬件需求**：两者都需外接 SIM 卡座与天线。天线多为 U.FL 接头，典型配置为 2×2 MIMO（主天线 + 分集天线）再加上一支 GNSS 定位天线。

**一个常被问的重点**：EM7455 与 MC7455 是「同一颗芯片、只差封装」——两者皆采用 Qualcomm MDM9230，规格完全相同，差别只在 M.2 与 mPCIe。所以选哪颗，纯看你的机器插槽长怎样。

## 依应用场景的选型建议

### 无线路由器 / CPE（OpenWrt / ROOter）

**推荐：[EM7455](https://yupitek.com/zh-CN/products/sierra/em7455/) / [MC7455](https://yupitek.com/zh-CN/products/sierra/mc7455/)**
理由：社群资源最多，ROOter（基于 OpenWrt 的蜂窝路由固件）教学与 QMI/MBIM 设定范例最完整，出问题 google 得到答案。

### 笔电 WWAN 升级

**推荐：[EM7430](https://yupitek.com/zh-CN/products/sierra/em7430/) / [EM7455](https://yupitek.com/zh-CN/products/sierra/em7455/)**
理由：皆为 M.2 封装，对应 Dell、Lenovo 等商用机的 WWAN 插槽；EM7455 频段配置较为广为人知、二手价低，是升级首选（实际频段与您所在电信商兼容性建议下单前先跟我们确认）。

### 工业路由器 / 网关（宽温、认证、长供货）

**推荐：EM75 系列（[EM7511](https://yupitek.com/zh-CN/products/sierra/em7511/)、[EM7565](https://yupitek.com/zh-CN/products/sierra/em7565/)）、[EM9190](https://yupitek.com/zh-CN/products/sierra/em9190/)/[EM9191](https://yupitek.com/zh-CN/products/sierra/em9191/)、[MC7455](https://yupitek.com/zh-CN/products/sierra/mc7455/)**
理由：工业场域重视宽温（−40°C 等级选项）、认证完整性与长期供货保证；Cat 12 与 5G 模块提供更高上行与未来带宽余裕。实际宽温规格与认证清单以官方规格书为准，建议正式选型时向我们索取最新版本确认。

### 车联网 / 车队 Telematics（GNSS 定位）

**推荐：[EM7455](https://yupitek.com/zh-CN/products/sierra/em7455/) / [EM7565](https://yupitek.com/zh-CN/products/sierra/em7565/) / [EM9191](https://yupitek.com/zh-CN/products/sierra/em9191/)**
理由：三者皆内建 GNSS，适合车载追踪与定位回传；需要 5G 高带宽车载应用时选 EM9191。

### 5G 专网 / CBRS 私有网络

**推荐：[EM9191](https://yupitek.com/zh-CN/products/sierra/em9191/)（支持 CBRS 频段）、[EM7565](https://yupitek.com/zh-CN/products/sierra/em7565/)（支持 CBRS/LAA 频段）**
理由：CBRS（美规 3.5 GHz 共享频段）与 LAA 为私有网络常见需求；EM9191、EM7565 硬件皆支持对应频段。实际导入私网前，频段搭配与相关认证仍需依当地法规与电信环境确认，建议与我们联系做完整技术评估。

### 视频监控 / 数字看板高带宽回传

**推荐：[EM9190](https://yupitek.com/zh-CN/products/sierra/em9190/) / [EM9191](https://yupitek.com/zh-CN/products/sierra/em9191/)**
理由：5G 高带宽（下行最高 Sub-6 2.5 Gbps、含 mmWave 最高 4.5 Gbps）适合多路影像实时回传与 4K 看板串流。

### 旧机维修 / 长期备料（Cat 4）

**推荐：[MC7304](https://yupitek.com/zh-CN/products/sierra/mc7304/) / [MC7350](https://yupitek.com/zh-CN/products/sierra/mc7350/) / [MC7354](https://yupitek.com/zh-CN/products/sierra/mc7354/)**
理由：mPCIe 封装的 Cat 4 老机维修料首选。但需诚实提醒：MC73xx 系列已接近 EOL（停产周期），长期备料建议评估迁移至 [EM7455](https://yupitek.com/zh-CN/products/sierra/em7455/) 或 [EM7565](https://yupitek.com/zh-CN/products/sierra/em7565/)，以取得更长的供货保证。

## 联络采购

选型还是拿不准？台湾可通过Yupitek榆阖科技采购本文十款 EM/MC 系列 Sierra 蜂窝模块，包含相关天线、SIM 转接与评估板。我们提供规格确认、频段比对、量价报价与技术导入支持。

## 常见问题 FAQ

**Q1：Sierra Wireless 有哪些型号？彼此差在哪？**
Sierra Wireless 现有 EM 与 MC 两大系列共十款模块，横跨 LTE Cat 4 / Cat 6 / Cat 12 到 5G Sub-6 与 mmWave。最大差异在封装：EM 为 M.2、MC 为 mPCIe；同芯片型号（如 EM7455 与 MC7455）效能相同，只差插槽形状。

**Q2：EM7455 跟 MC7455 是同一颗芯片吗？**
是的。两者都采用 Qualcomm MDM9230 芯片组，下载/上传峰值同为 300 / 50 Mbps、支持 2×CA 载波聚合，规格完全一致，唯一差别是 EM7455 为 M.2、MC7455 为 mPCIe 封装。

**Q3：5G 模块一定要选 mmWave（EM9191）吗？台湾可以用吗？**
不一定。台湾电信目前以 Sub-6 为主，mmWave 主要部署于美规场域（如 n260/n261）。一般台湾应用选 EM9190（Sub-6 平价 5G）即可；仅有美规毫米波需求才需 EM9191。

**Q4：M.2 和 mPCIe 蜂窝模块该怎么选？**
看你的设备插槽。笔电、现代嵌入式主板多为 M.2 B-Key，选 EM 系列；旧款工业路由器、工控机若为 mPCIe 槽，选 MC 系列。若板子只有 M.2 却想用 MC，需加 M.2 to mPCIe 转接板。

**Q5：Sierra Wireless 台湾哪里买？**
台湾可通过榆阖科技（Yupitek）采购 Sierra Wireless 全系列蜂窝模块。请至 Yupitek 官网产品页查询型号与报价，或直接 email: sales@yupitek.com

## 附录：十款型号官方 Spec Sheet 链接

以下链接提供各型号规格书 PDF 副本（可直接下载，无需登录），来源为 Sierra Wireless 官方技术资源库（source.sierrawireless.com）。本文规格数字整理自公开资料，若需逐项核对的最终规格数字（尤其是 EM9190/EM9191 上行峰值），建议直接向我们索取官方文件确认：

- **EM7430**：https://yupitek.com/docs/sierra/em7430_spec.pdf
- **EM7455**：https://yupitek.com/docs/sierra/em7455_spec.pdf
- **EM7511**：https://yupitek.com/docs/sierra/EM7511_spec.pdf
- **EM7565**：https://yupitek.com/docs/sierra/EM7565_spec.pdf
- **EM9190 / EM9191**：https://yupitek.com/docs/sierra/EM919x.pdf
- **MC7304**：https://yupitek.com/docs/sierra/MC7304_spec.pdf
- **MC7350**：https://yupitek.com/docs/sierra/MC7350_7354.pdf
- **MC7354**：https://yupitek.com/docs/sierra/MC7350_7354.pdf
- **MC7455**：https://yupitek.com/docs/sierra/mc7455_spec.pdf
