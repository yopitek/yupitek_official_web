---
title: "Sierra Wireless 十款蜂窝模块完整选购指南：LTE Cat 4 到 5G mmWave 怎么选"
description: "榆合科技整理 Sierra Wireless（Semtech）十款蜂窝模块 EM/MC 系列规格对比与选型建议，覆盖 LTE Cat 4 到 5G mmWave。全系列 Sierra Wireless 模块采购请联系 Yupitek。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Sierra Wireless 有哪些型号？彼此有什么区别？"
    answer: "Sierra Wireless 现有 EM 与 MC 两大系列共十款模块，覆盖 LTE Cat 4 / Cat 6 / Cat 12 到 5G Sub-6 与 mmWave。最大差异在封装：EM 为 M.2、MC 为 mPCIe；同芯片型号（如 EM7455 与 MC7455）性能相同，只差插槽形状。"
  - question: "EM7455 和 MC7455 是同一颗芯片吗？"
    answer: "是的。两者都采用 Qualcomm MDM9230 芯片组，下载/上传峰值同为 300 / 50 Mbps、支持 2×CA 载波聚合，规格完全一致，唯一差别是 EM7455 为 M.2、MC7455 为 mPCIe 封装。"
  - question: "5G 模块一定要选 mmWave（EM9191）吗？国内能用吗？"
    answer: "不一定。国内运营商目前以 Sub-6 为主，mmWave 主要部署于美规场景（如 n260/n261）。一般应用选 EM9190（Sub-6 平价 5G）即可；只有美规毫米波需求才需要 EM9191。"
  - question: "M.2 和 mPCIe 蜂窝模块该怎么选？"
    answer: "看你的设备插槽。笔记本、现代嵌入式主板多为 M.2 B-Key，选 EM 系列；旧款工业路由器、工控机若是 mPCIe 槽，选 MC 系列。若主板只有 M.2 却想用 MC，需要加 M.2 to mPCIe 转接板。"
  - question: "Sierra Wireless 哪里买？"
    answer: "可通过榆合科技（Yupitek）采购 Sierra Wireless 全系列蜂窝模块。请到 Yupitek 官网产品页查询型号与报价，或直接 email: sales@yupitek.com"
---

# Sierra Wireless 十款蜂窝模块完整选购指南：LTE Cat 4 到 5G mmWave 怎么选

无论你是在做物联网课题的大学生，还是在实验室里做网络设备，买通信模块最怕遇到什么？绝对是「规格表看半天、型号分不清，最后买错封装根本插不进设备」！

这篇文章帮大家把 Sierra Wireless（现隶属于 Semtech）现役与常青款的 10 款模块一次讲清楚，带你从基础的 LTE Cat 4 一路看懂到 5G mmWave。本文提到的 EM 系列全部是 M.2 封装，而 MC 系列则是 mPCIe 封装。

本文技术资料由榆合科技（Yupitek）整理提供。

## 十款规格总表：直接看数据最准

先上重点表格！里面的数字都是按照官方 Spec Sheet 整理的，方便大家直接对比。另外提醒一下，EM9190/EM9191 的上行峰值在不同数据来源可能会有一点点出入，如果真的要采购做项目，建议先去翻一下最新的官方 Spec Sheet 或直接找我们确认（文末有附录链接）。

| 型号 | 蜂窝标准 | 芯片组 | 下载 / 上传峰值 | 载波聚合 | 5G | mmWave | 封装 | GNSS | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/zh-cn/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 入门 Cat 6（实际频段配置请咨询确认） |
| [EM7455](/zh-cn/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 开源社区最热门、网络教程最多 |
| [EM7511](/zh-cn/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 高上行 Cat 12 |
| [EM7565](/zh-cn/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 支持 CBRS/LAA 频段、支持频段最多且上行最高 |
| [EM9190](/zh-cn/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 下行 2.5 Gbps（上行峰值请咨询确认） | 8×CA | ✓ | — | M.2 | ✓ | Sub-6 平价 5G 入门款 |
| [EM9191](/zh-cn/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | 下行最高 4.5 Gbps（含 mmWave）/ Sub-6 2.5 Gbps（上行峰值请咨询确认） | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 旗舰 5G，把毫米波也包进来了 |
| [MC7304](/zh-cn/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | 入门 Cat 4（已接近 EOL 停产周期） |
| [MC7350](/zh-cn/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、主打北美频段 |
| [MC7354](/zh-cn/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4、主打全球频段 |
| [MC7455](/zh-cn/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | 简单来说就是 mPCIe 版本的 EM7455 |

> 备注：EM9190 和 EM9191 其实共用同一份 EM919x/EM7690 规格书。EM9190 是 Sub-6 的平价 5G，而 EM9191 加上了 mmWave 算是旗舰款。官方规格书需要登录会员才能下载，上面表格的下行峰值是我们从公开资料整理的，至于上行峰值等细节，建议下单前还是找我们确认一下最新版本比较稳妥。

## 第一道关卡：EM 系列（M.2）和 MC 系列（mPCIe）有什么区别？

这绝对是新手选型最容易踩坑的地方！买错插不进去真的很尴尬。

**EM 系列 = M.2 B-Key 封装**：你可以想象成笔记本里插 SSD 的那种接口，体积很小（大约 30×42 mm）。它是专门为笔记本 WWAN 插槽、嵌入式 M.2 插槽设计的，现在比较新的工控主板或迷你 PC 大多用这种。

**MC 系列 = Mini PCIe（mPCIe）封装**：外观看起来就像以前电脑的扩展卡，比较适合旧款的工业路由器或工控机的 mPCIe 插槽。如果你的主板只有 M.2 插槽，想用 MC 系列就必须另外买一块转接板（M.2 转 mPCIe）才行。

**它们的共同点**：两种都需要外接 SIM 卡座和天线。天线接头通常是 U.FL，标准配置是 2×2 MIMO（一根主天线 + 一根分集天线），还会额外有一根 GNSS 定位天线。

**大家常问的问题**：EM7455 和 MC7455 到底有什么区别？答案是：「同一颗芯片，只差封装」。两张卡都用 Qualcomm MDM9230，规格一模一样，所以选哪张真的就是看你的板子长什么样。

## 根据你的课题或应用场景，我们推荐这样选：

### 1. 自己搭无线路由器 / CPE（用 OpenWrt 或 ROOter）

**推荐：[EM7455](/zh-cn/products/sierra/em7455/) / [MC7455](/zh-cn/products/sierra/mc7455/)**
理由很简单，因为网络上的开源社区资源最多！如果你用 ROOter（一个基于 OpenWrt 的固件），相关的教程和 QMI/MBIM 配置示例非常完整，踩坑了随便 google 都有救。

### 2. 给旧笔记本升级 WWAN 网卡

**推荐：[EM7430](/zh-cn/products/sierra/em7430/) / [EM7455](/zh-cn/products/sierra/em7455/)**
这两款都是 M.2 封装，很适合对应 Dell、Lenovo 等商务笔记本的 WWAN 插槽。特别是 EM7455 二手价通常很划算，是升级首选（但实际频段能不能匹配你的运营商，下单前还是先找我们确认一下）。

### 3. 工业路由器 / 物联网网关（需要耐造、宽温）

**推荐：EM75 系列（[EM7511](/zh-cn/products/sierra/em7511/)、[EM7565](/zh-cn/products/sierra/em7565/)）、[EM9190](/zh-cn/products/sierra/em9190/)/[EM9191](/zh-cn/products/sierra/em9191/)、[MC7455](/zh-cn/products/sierra/mc7455/)**
做工业项目最在意的就是宽温（例如 -40°C ~ +85°C 这种严苛环境）、认证完不完整以及能不能长期供货。Cat 12 和 5G 模块上传带宽比较大，未来扩展性也更好。不过实际的宽温规格请以官方最新文件为准。

### 4. 车联网 / 车队追踪（需要 GNSS 定位）

**推荐：[EM7455](/zh-cn/products/sierra/em7455/) / [EM7565](/zh-cn/products/sierra/em7565/) / [EM9191](/zh-cn/products/sierra/em9191/)**
做车联网课题通常需要精准定位，这三款都内置 GNSS，可以一次解决联网和定位的需求。如果要用到 5G 的大带宽，直接上 EM9191 准没错。

### 5. 5G 专网 / CBRS 私有网络实验

**推荐：[EM9191](/zh-cn/products/sierra/em9191/)（支持 CBRS 频段）、[EM7565](/zh-cn/products/sierra/em7565/)（支持 CBRS/LAA 频段）**
如果你在实验室研究 CBRS（美规 3.5 GHz 共享频段）或 LAA，这两款在硬件上都支持。但要注意，真正在当地测试私网还是要看当地法规和运营商环境，建议部署前跟我们讨论一下技术细节。

### 6. 视频监控 / 高清音视频回传

**推荐：[EM9190](/zh-cn/products/sierra/em9190/) / [EM9191](/zh-cn/products/sierra/em9191/)**
因为 5G 带宽够大（下行最高 Sub-6 有 2.5 Gbps、如果算上 mmWave 最高可以到 4.5 Gbps），非常适合用来做多路视频实时回传或 4K 视频流。

### 7. 旧设备维修 / 实验室老设备备件（Cat 4）

**推荐：[MC7304](/zh-cn/products/sierra/mc7304/) / [MC7350](/zh-cn/products/sierra/mc7350/) / [MC7354](/zh-cn/products/sierra/mc7354/)**
这是 mPCIe 封装的老设备维修首选。不过要老实说：MC73xx 系列已经接近 EOL（停产周期）了，如果是长期项目，建议大家考虑改用 [EM7455](/zh-cn/products/sierra/em7455/) 或 [EM7565](/zh-cn/products/sierra/em7565/) 会更有保障。

## 选型还是一头雾水？找我们帮忙吧

如果看完还是不知道怎么挑，你可以通过 Yupitek 榆合科技采购这十款 EM/MC 系列的蜂窝模块，连天线、SIM 转接板或评估板都可以一起搞定。不管是确认规格、对比频段，还是项目需要的报价与技术支持，都可以找我们。

## 常见问题快速 Q&A

{{< faq >}}

## 附录：十款型号官方 Spec Sheet 直达链接

下面这些链接都指向 Sierra Wireless 官方的技术资源库（source.sierrawireless.com）。**有些文档需要注册登录才能下载 PDF**。文章里的数据整理自公开资料，如果你需要逐项确认超细节的规格（例如 EM9190/EM9191 的上行峰值），建议直接联系我们索取最新的官方文档。

- **EM7430**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**：https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**：https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**：https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
