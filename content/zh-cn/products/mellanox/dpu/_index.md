---
title: "NVIDIA BlueField 数据处理器 (DPU)"
description: "了解 NVIDIA BlueField DPU 解决方案。使用基于 ARM 的可编程智能网卡 (SmartNIC)，卸载、加速并隔离网络、存储与安全等基础设施服务。"
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField 数据处理器 (DPU)

NVIDIA® BlueField® 数据处理器 (DPU) 引领了数据中心架构的变革。它将业界领先的 ConnectX 网络适配器与可编程 ARM® CPU 核心以及硬件加速引擎融合在一起，能够将基础设施任务从服务器 CPU 中卸载、加速并隔离开来。

---

## BlueField DPU 产品列表

我们分销的 BlueField DPU 适用于云级虚拟化、软件定义存储以及零信任安全架构。

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField 可编程基础设施适配卡*

| 产品料号 (PN) | 市场名称 | 核心网络规格 | ARM CPU 核心 | 内存 | 接口类型 | 网络协议 | 外形规格 |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | 双端口 100GbE / EDR IB | 8核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (支持 IB/以太网) | FHHL PCIe (半长全高) |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | 双端口 100GbE / EDR IB | 8核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (支持 IB/以太网) | FHHL PCIe (启用硬件加密) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | 单端口 100GbE / EDR IB| 8核 ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (支持 IB/以太网) | FHHL PCIe (启用硬件加密) |

---

## DPU 核心技术

### 1. 基础设施卸载（智能网卡增强）
管理虚拟化网络交换 (OVS)、虚拟化隧道 (VXLAN、NVGRE) 或网络地址转换 (NAT) 通常会消耗宝贵的服务器 CPU 周期。而 DPU 采用 **NVIDIA ASAP²（加速交换和数据包处理）**技术，能够直接在硬件中以线速处理这些任务，彻底解放服务器 CPU。

### 2. 软件定义存储加速
借助 **NVMe SNAP™（软件定义网络加速处理）**技术，BlueField DPU 可以将通过 RoCEv2 或 TCP 传输的远程网络存储，模拟为本地 NVMe 物理硬盘直接呈现给主机操作系统。存储的模拟、加密和压缩完全在 DPU 上处理，消除了虚拟化存储的性能瓶颈。

### 3. 零信任安全与隔离
DPU 在其内置的 ARM 核心上运行独立的 Linux 操作系统（通常是 Ubuntu），与主机服务器完全隔离。即使主机操作系统受到安全威胁，在 DPU 上运行的安全代理、无代理防火墙以及网络加密（IPsec、TLS）仍能不受干扰地保持正常运行。

### 4. NVIDIA DOCA 软件框架
BlueField DPU 的开发基于 **NVIDIA DOCA™** 软件框架。它为开发网络、安全、存储以及遥测等加速应用提供了符合行业标准的 API 接口。

---

## 典型应用场景

- **下一代云服务商**：实现物理机托管（Bare-Metal），将基础设施管理完全隔离在 DPU 上。
- **企业超融合基础设施 (HCI)**：将存储和网络叠加层 (VMware NSX / Proxmox OVS) 卸载至 DPU，从而最大化虚拟机部署密度。
- **高安全需求环境**：在网络物理边界直接运行网络安全监控（IDS/IPS）和数据加密任务。

---

{{< alert >}}
需要询问产品报价?请来信[与我们联系](/zh-cn/contact/)
{{< /alert >}}
