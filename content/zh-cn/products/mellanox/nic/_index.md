---
title: "NVIDIA Mellanox ConnectX 网络接口卡 (NIC / 网卡)"
description: "对比 NVIDIA Mellanox ConnectX-4 Lx、ConnectX-5、ConnectX-6 Dx/Lx 及 ConnectX-7 网卡。提供 10G、25G、50G、100G、200G 和 400G 规格，支持 PCIe Gen3/4/5。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Mellanox / NVIDIA ConnectX 网卡 — 10G 至 400G

NVIDIA Mellanox ConnectX 网卡为企业级服务器和 AI 集群提供领先的带宽与超低延迟表现。以下是 Yupitek 分销的完整产品目录，已按速率进行分类。

---

## 10GbE / 25GbE 网卡

非常适合常规企业服务器、虚拟化环境 (VMware ESXi) 以及高性能 NAS 存储。

### 10G 型号

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 挡板类型 |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | 双端口 | 10GbE | PCIe 3.0 x8 | SFP28 | 以太网 | 全高挡板 |

### 25G 型号

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*NVIDIA ConnectX-4 Lx 25GbE 双端口网卡*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*NVIDIA ConnectX-5 25GbE 双端口网卡*

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 挡板与外形规格 | 特性与说明 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | 双端口 | 25GbE | PCIe 3.0 x8 | SFP28 | 以太网 | 全高挡板 | 标准 PCIe 卡 |
| **MCX4121A-ACUT** | ConnectX-4 Lx | 双端口 | 25GbE | PCIe 3.0 x8 | SFP28 | 以太网 | 全高挡板 | 启用 UEFI 引导 |
| **MCX512A-ACAT** | ConnectX-5 EN | 双端口 | 25GbE | PCIe 3.0 x8 | SFP28 | 以太网 | 全高挡板 | 增强型 RoCEv2 |
| **MCX512A-ACUT** | ConnectX-5 EN | 双端口 | 25GbE | PCIe 3.0 x8 | SFP28 | 以太网 | 全高挡板 | UEFI (x86/ARM) 引导 |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | 双端口 | 25GbE | PCIe 4.0 x8 | SFP28 | 以太网 | 全高挡板 | 安全启动，无硬件加密 |
| **MCX623432AS-ADAB**| ConnectX-6 Lx | 双端口 | 25GbE | PCIe 4.0 x8 | SFP28 | 以太网 | OCP 3.0 手拧螺丝式 | 安全启动，OCP 3.0 规格 |

---

## 50GbE / 100GbE 网卡

适用于高速 NVMe-oF 存储、超融合基础设施 (HCI) 以及数据库服务器。

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*NVIDIA ConnectX-5 100GbE 网卡*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*NVIDIA ConnectX-6 Dx 100GbE 双端口网卡*

### 50G 型号

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 挡板类型 |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | 单端口 | 50GbE | PCIe 3.0 x16 | QSFP28 | 以太网 | 全高挡板 |

### 100G 型号

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 外形规格 | 特性与说明 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | 单端口 | 100GbE | PCIe 3.0 x16 | QSFP28 | 以太网 | 全高 PCIe 卡 | 标准 100G 网卡 |
| **MCX555A-ECAT** | ConnectX-5 VPI | 单端口 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 支持 EDR IB 及 100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | 双端口 | 100GbE | PCIe 3.0 x16 | QSFP28 | 以太网 | 全高 PCIe 卡 | 双端口 100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | 双端口 | 100GbE | PCIe 4.0 x16 | QSFP28 | 以太网 | 全高 PCIe 卡 | PCIe 4.0 接口 |
| **MCX556A-ECAT** | ConnectX-5 VPI | 双端口 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 双端口 EDR IB |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| 双端口 | 100G | PCIe 4.0 x16 | QSFP28 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | PCIe 4.0 双端口 EDR |
| **MCX653105A-ECAT**| ConnectX-6 VPI | 单端口 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 支持 HDR100 IB 及 100GbE|
| **MCX653106A-ECAT**| ConnectX-6 VPI | 双端口 | 100G | PCIe 3.0 x16 | QSFP28 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 支持 HDR100 IB 及 100GbE|
| **MCX623106AN-CDAT**| ConnectX-6 Dx | 双端口 | 100GbE | PCIe 4.0 x16 | QSFP56 | 以太网 | 全高 PCIe 卡 | 双端口 SFP56/QSFP56 100G|
| **MCX623436AN-CDAB**| ConnectX-6 Dx | 双端口 | 100GbE | PCIe 4.0 x16 | QSFP56 | 以太网 | OCP 3.0 手拧螺丝式 | OCP 规格 |

---

## 200GbE / 400GbE 网卡

专为 AI GPU 服务器节点（例如 NVIDIA HGX/DGX 架构）、高频交易 (HFT) 以及高性能计算 (HPC) 网络骨干设计的旗舰级适配卡。

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*NVIDIA ConnectX-7 400G OSFP 网卡*

### 200G 型号

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 外形规格 | 特性与说明 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | 单端口 | 200G | PCIe 4.0 x16 | QSFP56 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 支持 HDR IB 及 200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | 双端口 | 200G | PCIe 4.0 x16 | QSFP56 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 双端口 HDR/200G|
| **MCX623105A-VDAT**| ConnectX-6 Dx | 单端口 | 200GbE | PCIe 4.0 x16 | QSFP56 | 以太网 | 全高 PCIe 卡 | 单端口 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | 单端口 | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | 全高 PCIe 卡 | NDR200，支持 Socket Direct|
| **MCX755106AS-HEAT**| ConnectX-7 VPI | 双端口 | 200G | PCIe 5.0 x16 | QSFP112 | VPI (支持 IB/以太网) | 全高 PCIe 卡 | 端口1支持 IB，端口2支持 VPI|
| **MCX753436MS-HEAB**| ConnectX-7 VPI | 双端口 | 200G | PCIe 5.0 x16 | QSFP112 | VPI (支持 IB/以太网) | OCP 3.0 手拧螺丝式 | OCP 多主机 / 支持 Socket Direct|

### 400G 型号

| 产品料号 (PN) | 代次 / 芯片 | 端口数量 | 速率 | PCIe 插槽规格 | 接口类型 | 网络协议 | 外形规格 | 特性与说明 |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | 单端口 | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | 全高 PCIe 卡 | NDR InfiniBand 规格 |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | 单端口 | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | 全高 PCIe 卡 | NDR OSFP，支持 Socket Direct|

---

## 技术选型指南

在选择 ConnectX 网卡时，建议重点关注以下几个关键要素：

### 1. 协议模式 (VPI 与 EN)
- **EN（以太网）网卡**：仅支持以太网环境。
- **VPI（虚拟协议互连）网卡**：可以通过固件配置成 InfiniBand 或以太网卡，具备极高的部署灵活性。

### 2. PCIe 带宽需求
请确保主服务器的 PCIe 版本和插槽宽度能够满足网卡满载运行的需求：
- 例如，双端口 100G 网卡需要 PCIe 4.0 x16 插槽，才能让两个端口同时跑满带宽。
- 将 PCIe 4.0 网卡插入 PCIe 3.0 插槽时虽能向下兼容，但实际吞吐量会受限于 PCIe 3.0 的上限（x8 插槽约为 64Gbps，x16 插槽约为 128Gbps）。

### 3. OCP 3.0 与标准 PCIe 外形规格
料号后缀为 `-ADAB`、`-CDAB`、`-HEAB` 的型号采用的是 **OCP NIC 3.0** 规格。这类网卡是直接推入服务器后部专用插槽的（在 Supermicro、Dell、HPE 以及 Lenovo 的较新一代服务器中非常普遍），无法插入标准的 PCIe 插槽中。

---

需要配套的连接线缆？欢迎查看我们的[直连铜缆 (DAC)](/zh-cn/products/mellanox/cable-dac/)和[主动式光缆 (AOC)](/zh-cn/products/mellanox/cable-aoc/)目录。若要获取价格或了解库存情况，请直接[申请报价](/zh-cn/contact/)。
