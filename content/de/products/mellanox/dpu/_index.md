---
title: "NVIDIA BlueField-Datenverarbeitungseinheiten (DPU)"
description: "Entdecken Sie NVIDIA BlueField-DPU-Lösungen. Entlasten, beschleunigen und isolieren Sie Netzwerk-, Storage- und Sicherheitsinfrastruktur-Dienste mit ARM-basierten, programmierbaren SmartNICs."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA BlueField-Datenverarbeitungseinheiten (DPU)

NVIDIA® BlueField® Data Processing Units (DPUs) verändern die Rechenzentrumsarchitektur grundlegend. Sie kombinieren ConnectX-Netzwerkadapter mit programmierbaren ARM®-CPU-Kernen und dedizierten Hardware-Beschleunigern. Dadurch entlasten, beschleunigen und isolieren DPUs Infrastrukturaufgaben, die sonst die Server-CPU belasten würden.

---

## BlueField DPU Portfolio

Wir vertreiben BlueField-DPUs, die für Cloud-Virtualisierung, softwaredefinierten Speicher und Zero-Trust-Sicherheitskonzepte ausgelegt sind.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*NVIDIA BlueField Programmierbarer Infrastruktur-Adapter*

| Artikelnummer | Marketingname | Netzwerkschnittstelle | ARM-CPU-Kerne | Arbeitsspeicher | Schnittstelle | Protokoll | Formfaktor |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | Dual-Port 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | Dual-Port 100GbE / EDR IB | 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (Krypto aktiviert) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | Single-Port 100GbE / EDR IB| 8x ARMv8 A72 | 16GB DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (Krypto aktiviert) |

---

## Zentrale DPU-Technologien

### 1. Entlastung der Infrastruktur (SmartNIC+)
Statt wertvolle CPU-Zyklen des Host-Servers für das virtuelle Switching (OVS), Virtualisierungs-Tunnel (VXLAN, NVGRE) oder die Netzwerkadressübersetzung (NAT) zu verbrauchen, übernimmt die DPU diese Aufgaben in Leitungsgeschwindigkeit direkt auf Hardware-Ebene. Basis dafür ist die **NVIDIA ASAP²-Technologie (Accelerated Switch and Packet Processing)**.

### 2. Beschleunigung für softwaredefinierten Speicher
Mit **NVMe SNAP™ (Software-defined Network Accelerated Processing)** stellt eine BlueField-DPU dem Host-Betriebssystem entfernten Netzwerkspeicher (über RoCEv2 oder TCP) als lokale physische NVMe-Festplatte zur Verfügung. Die Emulation, Verschlüsselung und Komprimierung erfolgen komplett auf der DPU, was Speicherengpässe in virtualisierten Umgebungen verhindert.

### 3. Zero-Trust-Sicherheit & Isolation
Die DPU führt ein eigenes, unabhängiges Linux-Betriebssystem (meist Ubuntu) auf den integrierten ARM-Kernen aus – völlig isoliert vom Host-Server. Selbst wenn das Betriebssystem des Hosts kompromittiert wird, laufen Sicherheits-Agents, agentenlose Firewalls und die Netzwerkverschlüsselung (IPsec, TLS) auf der DPU manipulationssicher weiter.

### 4. NVIDIA DOCA Software Framework
BlueField-DPUs werden über das **NVIDIA DOCA™** Software-Framework programmiert. Es bietet Standard-APIs zur Entwicklung beschleunigter Anwendungen für Netzwerke, Sicherheit, Storage und Telemetrie.

---

## Typische Einsatzbereiche

- **Cloud-Provider der nächsten Generation**: Ermöglicht Bare-Metal-Hosting, bei dem das Infrastrukturmanagement vollständig auf der DPU isoliert ist.
- **Hyperkonvergente Infrastrukturen (HCI) in Unternehmen**: Auslagerung von Storage- und Netzwerk-Overlays (VMware NSX / Proxmox OVS) zur Maximierung der VM-Dichte.
- **Hochsicherheitsumgebungen**: Ausführung von Netzwerk-Sicherheitsüberwachung (IDS/IPS) und Verschlüsselungsprozessen direkt an der Netzwerkgrenze.

---

Für technische Unterstützung bei der Integration oder zur Anforderung eines Angebots [kontaktieren Sie bitte den Yupitek-Vertrieb](/de/contact/).
