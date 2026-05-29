---
title: "NVIDIA Mellanox InfiniBand & Ethernet Switches"
description: "High-density enterprise network switches. Select Mellanox EDR (100G), HDR (200G), and NDR (400G) switches. Built for high-performance computing and AI clusters."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox InfiniBand & Ethernet Switches — EDR, HDR & NDR

NVIDIA Mellanox InfiniBand switches represent the backbone of modern AI training clusters and high-performance computing (HPC) environments. Featuring high port density, low switch latency, and advanced congestion management, these switches enable seamless scaling of multi-node systems.

---

## Switch Product Catalog

Below is the list of unmanaged and managed 1U rack-mount switches in our inventory.

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*NVIDIA Mellanox Quantum HDR 40-Port InfiniBand Switch*

| Part Number | Chipset Generation | Managed | Ports Configuration | Port Speed | Form Factor | Airflow | Power Supply |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | Yes (x86) | 36x QSFP28 | 100Gb/s | 1U Standard | Port-to-Power (P2C) | Dual AC PSU |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | No | 36x QSFP28 | 100Gb/s | 1U Standard | Power-to-Port (C2P) | Dual AC PSU |
| **MQM8700-HS2F** | Quantum (HDR) | Yes (x86) | 40x QSFP56 | 200Gb/s | 1U Standard | Port-to-Power (P2C) | Dual AC PSU |
| **MQM8790-HS2F** | Quantum (HDR) | No | 40x QSFP56 | 200Gb/s | 1U Standard | Port-to-Power (P2C) | Dual AC PSU |
| **MQM9700-NS2F** | Quantum 2 (NDR) | Yes | 32x OSFP (64x NDR ports) | 400Gb/s (OSFP) | 1U Standard | Port-to-Power (P2C) | Dual AC PSU |
| **MQM9790-NS2F** | Quantum 2 (NDR) | No | 32x OSFP (64x NDR ports) | 400Gb/s (OSFP) | 1U Standard | Port-to-Power (P2C) | Dual AC PSU |

---

## InfiniBand Generations Comparison

| Generation | Chipset | Max Port Speed | Switch Capacity | Signaling Rate / Modulation | Latency |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gb/s | 7.2 Tb/s | 25 Gb/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gb/s | 16.0 Tb/s | 50 Gb/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gb/s (800G ready) | 51.2 Tb/s | 100 Gb/s PAM4 | 205 ns |

---

## InfiniBand Network Topology Guide

Building a scale-out cluster for AI training or physics simulation requires specialized topologies:

```
                  ┌─────────────────┐       ┌─────────────────┐
  Spine Level     │ Spine Switch 1  │.......│ Spine Switch N  │
                  └────────┬────────┘       └────────┬────────┘
                           │                         │
            ┌──────────────┼──────────────┐          │
            │              │              │          │
     ┌──────┴──────┐┌──────┴──────┐┌──────┴──────┐   │
Leaf │Leaf Switch 1││Leaf Switch 2││Leaf Switch 3│...│
Level└──────┬──────┘└──────┬──────┘└──────┬──────┘   │
            │              │              │          │
      ┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐    │
Nodes │  Node 1   │  │  Node 2   │  │  Node 3   │....│
      └───────────┘  └───────────┘  └───────────┘
```

### 1. Fat-Tree (non-blocking CLOS) Topology
The standard architecture for InfiniBand networks. It organizes switches in hierarchical tiers (Leaf and Spine) to provide multiple parallel paths.
- **Non-blocking (1:1 subscription)**: Every node can communicate at full wire speed concurrently. Requires equal uplink bandwidth to the spine as downlink bandwidth to the nodes.
- **Over-subscribed (e.g., 2:1)**: Lowers switch costs by reducing the number of spine links, suitable for workloads with localized compute communication.

### 2. Rail-Optimized AI Networks
In multi-GPU nodes (like NVIDIA HGX H100 with 8 GPUs), each GPU has a dedicated ConnectX NIC. Rail-optimization connects all "GPU 1" adapters across all servers to a dedicated "Rail Switch 1," all "GPU 2" to "Rail Switch 2," and so on. This maps the ring-communication pattern of deep learning libraries (NCCL) directly onto physical switches, minimizing latency.

---

## Managed vs Unmanaged Switches & Subnet Manager (SM)

Unlike Ethernet networks which are plug-and-play via ARP, an InfiniBand network **cannot pass traffic without an active Subnet Manager (SM)**. The SM discovers topology, assigns Local Identifiers (LIDs), and calculates routing paths.
- **Managed Switches**: Feature an internal CPU running MLNX-OS/Onyx that hosts an embedded Subnet Manager. Ideal for standalone small clusters (up to ~36 nodes).
- **Unmanaged Switches**: Staggeringly low-latency, but have no onboard CPU. They require an external SM running either on a host server (via OpenSM) or on a separate managed switch within the fabric.

---

Need architecture design or configuration advice for your cluster? [Contact Yupitek engineers](/en/contact/).
