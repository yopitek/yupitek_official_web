---
title: "NVIDIA BlueField Data Processing Units (DPU)"
description: "Explore NVIDIA BlueField DPU solutions. Offload, accelerate, and isolate network, storage, and security infrastructure services with ARM-based programmable SmartNICs."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField Data Processing Units (DPU)

NVIDIA® BlueField® Data Processing Units (DPUs) represent a revolutionary shift in data center architecture. By combining industry-leading ConnectX network adapters with programmable ARM® CPU cores and hardware acceleration engines, DPUs offload, accelerate, and isolate infrastructure tasks from the server CPU.

---

## BlueField DPU Inventory

We distribute BlueField DPUs configured for cloud-scale virtualization, software-defined storage, and zero-trust security.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField Programmable Infrastructure Adapter*

| Part Number | Marketing Name | Core Networking | ARM CPU Cores | Memory | Interface | Protocol | Form Factor |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | Dual-port 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | Dual-port 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (Crypto Enabled) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | Single-port 100GbE / EDR IB| 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (Crypto Enabled) |

---

## Key DPU Technologies

### 1. Infrastructure Offloads (SmartNIC+)
Rather than using valuable host CPU cycles to manage hypervisor network switching (OVS), virtualization tunnels (VXLAN, NVGRE), or network address translation (NAT), the DPU handles these tasks at wire-speed directly in hardware using **NVIDIA ASAP² (Accelerated Switch and Packet Processing)** technology.

### 2. Software-Defined Storage Acceleration
Using **NVMe SNAP™ (Software-defined Network Accelerated Processing)**, a BlueField DPU can present remote network storage (over RoCEv2 or TCP) as a local NVMe physical drive to the host operating system. The emulation, encryption, and compression are handled entirely on the DPU, eliminating virtualization storage bottlenecks.

### 3. Zero-Trust Security & Isolation
The DPU runs its own independent Linux operating system (typically Ubuntu) on its embedded ARM cores, completely isolated from the host server. Even if the host OS is compromised, security agents, agentless firewalls, and network encryption (IPsec, TLS) running on the DPU continue to operate untampered.

### 4. NVIDIA DOCA Software Framework
BlueField DPUs are programmed using the **NVIDIA DOCA™** software framework, which provides industry-standard APIs for developing accelerated applications for networking, security, storage, and telemetry.

---

## Common Use Cases

- **Next-Generation Cloud Providers**: Enabling bare-metal hosting where infrastructure management is fully isolated on the DPU.
- **Enterprise Hyperconverged Infrastructure (HCI)**: Offloading storage and network overlays (VMware NSX / Proxmox OVS) to maximize VM density.
- **High-Security Environments**: Running network security monitoring (IDS/IPS) and encryption workloads directly on the network boundary.

---

For technical integration support or to request a quote, please [contact Yupitek sales](/en/contact/).
