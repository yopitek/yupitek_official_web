---
title: "NVIDIA Mellanox InfiniBand 与以太网交换机"
description: "高密度企业级 network 交换机。精选 Mellanox EDR (100G)、HDR (200G) 和 NDR (400G) 交换机，专为高性能计算与 AI 集群打造。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox InfiniBand 与以太网交换机 — EDR, HDR & NDR

NVIDIA Mellanox InfiniBand 交换机是现代 AI 训练集群和高性能计算 (HPC) 环境的骨干基石。这些交换机具备超高端口密度、微乎其微的交换延迟以及先进的拥塞控制机制，可实现多节点系统的无缝扩展。

---

## 交换机产品目录

以下是我们的 1U 机架式管理型与非管理型交换机现货列表。

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*NVIDIA Mellanox Quantum HDR 40 端口 InfiniBand 交换机*

| 产品料号 (PN) | 芯片代次 | 是否受管 (管理型) | 端口配置 | 端口速率 | 外形规格 | 风道方向 | 电源模块 |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | 是 (x86) | 36x QSFP28 | 100Gb/s | 1U 标准机架式 | 端口到电源风道 (P2C) | 双交流电源 (AC) |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | 否 | 36x QSFP28 | 100Gb/s | 1U 标准机架式 | 电源到端口风道 (C2P) | 双交流电源 (AC) |
| **MQM8700-HS2F** | Quantum (HDR) | 是 (x86) | 40x QSFP56 | 200Gb/s | 1U 标准机架式 | 端口到电源风道 (P2C) | 双交流电源 (AC) |
| **MQM8790-HS2F** | Quantum (HDR) | 否 | 40x QSFP56 | 200Gb/s | 1U 标准机架式 | 端口到电源风道 (P2C) | 双交流电源 (AC) |
| **MQM9700-NS2F** | Quantum 2 (NDR) | 是 | 32x OSFP (可分拆为 64x NDR 端口) | 400Gb/s (OSFP) | 1U 标准机架式 | 端口到电源风道 (P2C) | 双交流电源 (AC) |
| **MQM9790-NS2F** | Quantum 2 (NDR) | 否 | 32x OSFP (可分拆为 64x NDR 端口) | 400Gb/s (OSFP) | 1U 标准机架式 | 端口到电源风道 (P2C) | 双交流电源 (AC) |

---

## InfiniBand 技术世代对比

| 技术代次 | 芯片组 | 最高端口速率 | 交换容量 | 信号速率与调制方式 | 交换延迟 |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7.2 Tb/s | 25 Gb/s NRZ | 90 纳秒 |
| **HDR** | Quantum | 200 Gb/s | 16.0 Tb/s | 50 Gb/s PAM4 | 130 纳秒 |
| **NDR** | Quantum 2 | 400 Gb/s (支持 800G) | 51.2 Tb/s | 100 Gb/s PAM4 | 205 纳秒 |

---

## InfiniBand 网络拓扑指南

为 AI 训练或物理仿真构建大规模横向扩展集群时，需要采用特定的网络拓扑结构：

![NVIDIA Mellanox Fat-Tree InfiniBand Topology](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. 胖树 (Fat-Tree / 无阻塞 CLOS) 拓扑
这是 InfiniBand 网络最标准的架构。它通过分层（叶交换机 Leaf 与脊交换机 Spine）的方式组织交换机，提供多条平行的物理路径。
- **无阻塞（1:1 收敛比）**：所有节点均可同时以满线速进行双向通信。这要求叶交换机到脊交换机的上行带宽与连接服务器节点的基本下行带宽完全一致。
- **非对称/有收敛比（例如 2:1）**：通过减少脊交换机的上行链路数量来降低交换机采购成本，适用于计算通信局域化明显的业务场景。

### 2. 导轨优化型 (Rail-Optimized) AI 网络
在多 GPU 节点（例如配备 8 颗 GPU 的 NVIDIA HGX H100 服务器）中，每颗 GPU 都配有专属的 ConnectX 网卡。导轨优化设计将所有服务器中的“GPU 1”适配器连接到同一台专用的“导轨交换机 1”上，将“GPU 2”连接到“导轨交换机 2”上，以此类推。这种物理连线方式能直接匹配深度学习通信库 (NCCL) 的环形通信模式，将数据传输延迟降到极低。

---

## 管理型与非管理型交换机及子网管理器 (SM)

以太网能够通过 ARP 协议实现即插即用，但 InfiniBand 网络**在没有子网管理器 (SM) 处于活动状态时，是完全无法传输任何流量的**。SM 负责发现网络拓扑、分配本地标识符 (LID) 并计算路由路径。
- **管理型交换机**：内置主控 CPU，运行 MLNX-OS/Onyx 操作系统，并搭载嵌入式子网管理器 (SM)。非常适合大约 36 个节点以内的小型独立集群。
- **非管理型交换机**：拥有极低的物理延迟，但没有板载 CPU。它们依赖于在服务器主机上（通过 OpenSM 软件）或在同网络中其他管理型交换机上运行的外部子网管理器。

---

需要为您的大型集群提供网络拓扑设计或配置建议？请直接[联系 Yupitek 工程师团队](/zh-cn/contact/)。
