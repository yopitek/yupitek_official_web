---
title: "NVIDIA Mellanox LinkX 光模块"
description: "选择原装 NVIDIA Mellanox LinkX 光收发模块。提供适用于多模和单模网络的高速 25G、100G、400G 和 800G 光模块。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox LinkX 光模块 — 25G 至 800G

NVIDIA LinkX® 光模块专为满足高性能计算、企业级存储以及超大规模数据中心环境的严苛要求而设计。使用原装光模块可确保卓越的信号完整性、极低的误码率 (BER)，并与 ConnectX 网卡以及 Quantum 交换机实现无缝兼容。

---

## 光模块产品目录

以下是我们的常备现货光模块型号列表。

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="25G SFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 25G SFP28 SR 光模块</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="100G QSFP28 Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA Mellanox 100G QSFP28 SR4 光模块</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="400G OSFP Transceiver" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">NVIDIA 400G OSFP NDR 光模块</p>
  </div>
</div>

| 产品料号 (PN) | 速率 | 封装接口 | 接口类型 | 工作波长 | 光纤类型 | 最大传输距离 | 产品说明 |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | 双工 LC | 850nm | 多模 (MMF) | 150m (OM4) / 100m (OM3) | 25GbE SR 光模块 |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850nm | 多模 (MMF) | 100m (OM4) / 70m (OM3) | 100GbE SR4 光模块，支持 DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC | 850nm | 多模 (MMF) | 50m (OM4) | NDR IB/以太网 SR 光模块（Flat Top 扁平顶盖） |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC | 850nm | 多模 (MMF) | 50m (OM4) | 2xNDR 双端口 SR 光模块（Finned 翅片散热顶盖） |

---

## 传输距离与布线参考指南

### 1. SR 与 SR4 与 NDR（多模方案对比）
- **25G SR (SFP28)**：使用标准 LC-LC 双工多模光纤跳线。通过单通道进行数据的发送和接收。
- **100G SR4 (QSFP28)**：使用 12 芯 MPO (MPO-12) 带状光纤跳线（通常为 B 类极性，Type-B），通过 4 个并行的 25G 通道进行传输。
- **400G/800G NDR (OSFP)**：采用 PAM4 调制，通过 MPO-12 APC（角度物理接触）连接器传输超高带宽。8°斜角端面设计能将回波反射降到最低，这在高速率传输下是保持信号稳定的关键。

### 2. 单模 (LR4/FR4) 与 多模 (SR/SR4) 对比
- **多模 (MMF)**：适用于机柜内或相邻机柜间的短距离布线（最长 100–150 米），模块采购成本较低。
- **单模 (SMF)**：传输距离超过 150 米时必须使用（如 LR4 最长支持 10 公里）。在 9/125µm 光纤上使用双工 LC 连接器。

---

## 技术建议：原装模块与第三方兼容模块

在采购光模块时，客户常问的一个问题是：“我们能不能用市面上的第三方兼容模块或改码模块？”

### 为什么我们强烈建议使用 NVIDIA 原装 LinkX 模块：
1. **固件兼容性风险**：NVIDIA ConnectX 网卡和 Quantum 交换机运行专用的操作系统（如 MLNX-OS 或 Onyx）。系统固件更新经常会导致第三方改码模块失效或被标记，从而造成端口下线（Port Link Down）。
2. **诊断数据的准确性 (DDM/DOM)**：原装模块能够将精准的温度、电压、发射功率 (TX) 和接收功率 (RX) 直接报告给系统控制器（如 iDRAC、HPE iLO 或 MLNX-OS），避免因数据偏差引发系统误报温度故障。
3. **高级特性开箱即用**：LinkX 模块经过完整认证，原生支持前向纠错 (FEC) 等关键设置，可有效防止高负载数据库业务在满载时出现丢包现象。

---

需要匹配的光纤跳线？欢迎查看我们的[光纤跳线产品目录](/zh-cn/products/mellanox/cable-fiber/)。如有定制化的网络规划需求，请直接[联系 Yupitek 工程师团队](/zh-cn/contact/)。
