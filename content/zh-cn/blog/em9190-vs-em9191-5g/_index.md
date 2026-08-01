---
title: "EM9190 vs EM9191：5G Sub-6 与 mmWave 该怎么选？帮你破除网络谣言"
description: "EM9190 vs EM9191 怎么选？依据官方规格书（41113174 Rev 8）：EM9190 支持 5G Sub-6 + mmWave（n257/258/260/261，仅 NSA），EM9191 仅 Sub-6。均采用 Qualcomm SDX55、M.2，附台湾 5G 频段对照，Yupitek 整理。"
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM9190_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "EM9190 和 EM9191 到底差在哪？哪一颗支持 mmWave？"
    answer: "依据官方规格书（41113174, Rev 8），两颗的 Sub-6（FR1）、LTE、3G、GNSS 能力相同，唯一重大差异是 5G mmWave（FR2）：EM9190 支持 LTE+FR2 NSA EN-DC（需搭配 QTM525/QTM527 mmWave 天线模块，仅 NSA 模式），EM9191 标注为 Not supported。所以是 EM9190 才有 mmWave。"
  - question: "EM9191 适合台湾的 5G 应用吗？"
    answer: "适合。台湾 5G 主网的核心频段是 3.5GHz，对应 3GPP n78（3300–3800MHz，TDD），EM9190 与 EM9191 都支持 n78。台湾 28GHz（对应 n257）部署场域较少，只有该类场域才需要 EM9190 + mmWave 天线模块。一般 5G FWA、工业路由器选 EM9191 即可。"
  - question: "EM9190 的 mmWave 是买一颗模块就有吗？"
    answer: "不是。EM9190 本身没有内置天线，mmWave 需要额外搭配 1–4 组 Qualcomm QTM525（低功率，EIRP 23dBm）或 QTM527（高功率，EIRP 45dBm）mmWave 天线模块，每组以两条 MHF7S IF 缆线连接（最多 8 条），并由外部 3.8V 供电；且 FR2 仅支持 NSA 模式。"
  - question: "两颗模块的功耗差多少？"
    answer: "依据规格书 Table 3-2：峰值电流 EM9190（含 mmWave）5.0A、EM9190（不含 mmWave）3.0A、EM9191 2.7A；连续电流分别为 4.0A、2.3A、2.0A。电池供电或散热受限的终端，EM9191 在电源设计上较轻松。"
  - question: "EM9190 与 EM9191 的主板设计能共用吗？"
    answer: "高度共通：同为 M.2（WWAN Type 3042-S3-B，长 52mm）、同 75-pin 引脚、同 USB 3.1 Gen2 / PCIe Gen3 接口、同 4× MHF4 Sub-6 天线端口。差异在 EM9190 多了 8× MHF7S mmWave IF 连接器与 QTM 控制引脚（pin 40/42/44/46/48，EM9191 为 NC）。"
---

# EM9190 vs EM9191：5G Sub-6 与 mmWave 该怎么选？帮你破除网络谣言

如果你在学校跟着教授做 5G 项目，或者刚好在公司负责 5G 模块的选型，你上网搜资料一定经常看到这句话：「EM9190 是平价 Sub-6 版本，EM9191 才是包含 mmWave（毫米波）的旗舰款」。

**错了！这完全是写反的！**

这篇文章不靠网络转述，直接拿出 Sierra Wireless 官方规格书《EM919X/EM7690 Product Technical Specification》（Doc 41113174, Rev 8, 2023 年 5 月）来当唯一标准，一项一项核对这两颗模块的差异。特别是针对台湾读者最在意的 n78 和 28GHz 频段到底能不能用，帮大家把关，让你做 5G 设备采购时不会买错。

> 产品链接：[EM9190 — Yupitek 产品页](/zh-cn/products/sierra/em9190/) | [EM9191 — Yupitek 产品页](/zh-cn/products/sierra/em9191/) | 官方规格书：[EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## 破除谣言：EM9190 和 EM9191 到底差在哪？

**简单来说，EM9190 和 EM9191 就是同一个妈生的（同一系列、同一颗基带芯片），两边都支持 5G Sub-6、4G LTE 和 GNSS 定位。唯一的差别就是：EM9190 多支持了 5G mmWave（毫米波，FR2），而 EM9191 不支持。**

如果要有 mmWave，你买了 EM9190 之后还要另外搭配 Qualcomm QTM525 或 QTM527 天线模块才行（而且只能跑 NSA 模式）。

| 你的问题 | 官方规格书的正确答案 |
|---|---|
| **这两张卡差在哪？** | 就差在 mmWave（FR2）。EM9190 规格书写「LTE+FR2 NSA EN-DC Supported」；EM9191 则写「Not supported」。其他 Sub-6 频段、LTE 等等全部都一样。 |
| **EM9190 有 mmWave 吗？** | 有。但不是买这张卡就直接有，你需要外接 Qualcomm 的 mmWave 天线模块（最多接 4 组），支持 n257/n258/n260/n261，而且限定只能在 NSA（非独立组网）模式下跑。 |
| **EM9191 有 mmWave 吗？** | 没有。官方 Table 1-1 明确标注「Not supported」，而且板子上跟 mmWave 有关的信号引脚全都是 NC（未接通）。 |
| **在台湾做 5G 课题要买哪颗？** | 台湾 5G 最常跑的是 3.5GHz（n78），这两颗都有支持；至于 28GHz（对应 n257）在台湾比较少见，如果你刚好要做这块的实验，才需要买 EM9190 加上 mmWave 天线。 |
| **谁适合买哪一颗？** | **EM9190**：美规/日规市场、实验室做毫米波测试、需要极大带宽的户外 CPE 设备。<br>**EM9191**：在台湾或亚洲跑 Sub-6、希望模块不要太耗电、预算有限的项目。 |

> **再强调一次**：请不要再相信网络上「EM9191 才是 mmWave 旗舰」的说法了，官方规格书白纸黑字写着 **EM9190 才有 mmWave 能力**，买错就尴尬了。

---

## 同一个家族的兄弟：EM9190 / EM9191 / EM7690 怎么分？

其实 EM91 这个家族有三兄弟。根据规格书定义：

- **EM9190**：全配吃满（LTE + 5G Sub-6 + 5G mmWave）
- **EM9191**：标配实用款（LTE + 5G Sub-6，没有 mmWave）
- **EM7690**：降级版（只有 LTE，没有 5G）

这篇文章主要只比较前两位 5G 兄弟，EM7690 只是让你顺便知道有这号人物。

---

## 规格硬核对报表（来自官方 41113174 Rev 8）

以下这些数字都是根据官方规格书来的。如果你是工程师，直接看这张表最快：

| 项目 | EM9190 | EM9191 | 来源 |
|---|---|---|---|
| **5G NR Sub-6（FR1）** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave（FR2）** | ✓（限 NSA 模式，需外接天线模块） | ✗ | Table 1-1 |
| **FR2 毫米波频段** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **FR1 Sub-6 频段** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | 两者相同 | Table 4-4 |
| **核心基带芯片** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **蜂窝标准** | 5G 3GPP Release 15；LTE Release 15 | 两者相同 | Table 2-1 |
| **封装尺寸** | M.2（WWAN Type 3042-S3-B，长 52mm） | 两者相同 | §1.2 |
| **电脑/主板接口** | USB 3.1 Gen2、PCIe Gen3 单通道 | 两者相同 | §1.3 |
| **Sub-6 专用天线孔** | 4 个 MHF4 孔（MAIN/MIMO1/MIMO2/AUX） | 两者相同 | §4.1 |
| **mmWave 专用天线孔** | 8 个 MHF7S 孔（最多接 4 组外接天线模块） | 无 | §4.1 |
| **最大瞬时耗电（峰值）** | 5.0A（含 mmWave）/ 3.0A（不含） | 2.7A | Table 3-2 |
| **工作温度** | -30°C ~ +70°C（Class A）；-40°C ~ +85°C（Class B，效能会降） | 两者相同 | Table 7-1 |
| **定位功能 (GNSS)** | L1（GPS/GLONASS等）＋L5（选配） | 两者相同 | Table 4-13 |

> **小小提醒**：这份规格书是 2023 年 5 月的版本。有些频段（像 n7, n8, n20 等）会因为固件或是出货的 SKU 不同而有变化，真要下单做项目前，记得向我们索取最新的官方文件对照一下。

---

## mmWave 不是买了模块就有：EM9190 隐藏的成本

很多大学生或 Maker 以为买了 EM9190 就可以直接测毫米波，这是大错特错的。

规格书里写得很清楚：「**EM9190 只有在搭配选购的 Qualcomm mmWave 天线模块时才支持 5G mmWave。**」而且，它只支持 NSA（非独立组网）模式，也就是说你还必须有 4G LTE 的信号当作锚点（Anchor）才连得上。

### 毫米波天线要怎么配？

你要去买 Qualcomm QTM525（低功率版）或是 QTM527（高功率版）天线模块。而且不同的天线模块支持的频段还不一样（见官方 Table 4-2）：

- 如果你的实验室想测 **n257**（台湾 28GHz 的频段），你必须买 QTM525-2、QTM525-5 或 QTM527-2，如果你买到 QTM527-1 就没有 n257 哦！

**工程师要注意的坑**：
如果你要用 EM9190 做户外的 5G 接收器（CPE），你可能要挂满 4 颗高功率的 QTM527 天线。这代表你要拉 8 条很贵的 MHF7S 线，还要另外设计 3.8V 的供电给这些天线，外加超强的散热。这部分的开发成本往往比单买这张网卡还要贵很多！

---

## 如果在台湾做 5G，其实选 EM9191 就够了

**因为台湾 5G 的主力是 3.5GHz（也就是 3GPP 讲的 n78），而 EM9190 和 EM9191 两颗都完美支持 n78。**

如果你的课题只是要在台湾跑 5G，或者你要做工业路由器卖给一般客户：

- 两颗都支持台湾的 5G n78（3300–3800MHz）。
- 两颗都支持台湾现有的 4G 频段（当作 NSA 的锚点没问题）。

**为什么推荐你买 EM9191 呢？**
因为既然用不到毫米波，就不要花钱买 EM9190。而且 EM9191 因为没有毫米波硬件，它的峰值电流只有 2.7A，比 EM9190 轻松很多（见下一段），对电路板的供电负担小非常多。

---

## 耗电量比一比：电源设计别搞砸

做硬件的都知道，电源没推上去机器就会重启。根据官方 Table 3-2 给的数据：

| 耗电参数 | EM9190（接了 mmWave） | EM9190（不接 mmWave） | EM9191 |
|---|---|---|---|
| 峰值瞬时电流 | 5.0A | 3.0A | 2.7A |
| 连续使用电流 | 4.0A | 2.3A | 2.0A |

所有模块吃的电压都是 3.135V 到 4.4V（通常设计为 3.3V）。你可以看到，如果 EM9190 把 mmWave 开下去，瞬时电流会飙到 5.0A！这对电池供电或是体积小的设备来说是个很大的挑战。如果你只是要跑 Sub-6 5G，选 EM9191 只要搞定 2.7A 的峰值就好，电源设计会简单很多。

---

## 电路板的引脚设计：两者可以共用吗？

**可以共用 Sub-6 的设计。**

这两颗模块都是 M.2 封装（长 52mm，比一般笔记本用的 42mm 长一点，要注意机构空间），有相同的 75-pin 引脚。

唯一的差别是，EM9190 为了要控制那一堆毫米波天线，它用掉了一些原本空着的引脚（例如 pin 40/42/44/46 的 QTM_PON 以及 pin 48 的 1.9V 供电）。这些引脚在 EM9191 上是空接（NC）的。
所以你大可以先画一块通用 EM9191 的板子，等哪天真的要玩毫米波了，再把 EM9190 需要的控制线补上去就好。

---

## 总结：该买哪一张？

| 你的需求条件 | 选 EM9190 | 选 EM9191 |
|---|---|---|
| 需要测试 28GHz 等 mmWave 频段 | ✅ 只能选它（记得加购天线） | ❌ 不支持 |
| 项目在台湾跑，只用 5G Sub-6 (n78) | 可用（但有点浪费） | ✅ 推荐，省钱又省电 |
| 电路板的电源推不动大电流 | ⚠️ 峰值可能到 5.0A | ✅ 峰值 2.7A 比较好搞定 |

**避坑指南**：

1. 别再搞错了，EM9190 才有 mmWave。
2. 买 EM9190 不代表就有 mmWave，你还要买特殊天线和拉线。
3. 很多频段（像 n7, n8, n28）会受固件版本和地区限制，买之前一定要跟供应商确认你的 SKU 到底能不能解锁这些频段。

---

## 常见问题快速 Q&A

{{< faq >}}

---

## 需要采购或讨论？来找我们吧

看完这篇如果还有硬件集成的问题，或者你们实验室/公司需要采购这两款 5G 模块，欢迎联系榆合科技（Yupitek）的工程团队，我们也有提供对应的天线和转接板。

- **EM9190（含 mmWave 的真旗舰）产品页**：[https://yupitek.com/zh-cn/products/sierra/em9190/](/zh-cn/products/sierra/em9190/)
- **EM9191（实用的 Sub-6 款）产品页**：[https://yupitek.com/zh-cn/products/sierra/em9191/](/zh-cn/products/sierra/em9191/)
- **看 Sierra 全系列型号**：[https://yupitek.com/zh-cn/products/sierra/](/zh-cn/products/sierra/)
- **联系邮箱**：sales@yupitek.com
