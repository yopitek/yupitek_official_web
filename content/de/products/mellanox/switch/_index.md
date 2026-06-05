---
title: "NVIDIA Mellanox InfiniBand- & Ethernet-Switches"
description: "Enterprise-Netzwerkswitches mit hoher Portdichte. Wählen Sie Mellanox EDR- (100G), HDR- (200G) und NDR-Switches (400G). Entwickelt für High-Performance Computing und KI-Cluster."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# NVIDIA Mellanox InfiniBand- & Ethernet-Switches – EDR, HDR & NDR

NVIDIA Mellanox InfiniBand-Switches bilden das Rückgrat moderner KI-Trainingscluster und HPC-Umgebungen (High-Performance Computing). Mit hoher Portdichte, extrem niedrigen Latenzzeiten und intelligentem Überlastungsmanagement (Congestion Management) ermöglichen sie eine nahtlose Skalierung von Systemen mit vielen Rechenknoten.

---

## Portfolio Netzwerk-Switches

Nachfolgend finden Sie die managed und unmanaged 1U-Rack-Switches aus unserem Sortiment.

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*NVIDIA Mellanox Quantum HDR 40-Port InfiniBand-Switch*

| Artikelnummer | Chipsatz-Generation | Managed | Port-Konfiguration | Port-Geschwindigkeit | Formfaktor | Luftstromrichtung | Stromversorgung |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | Ja (x86) | 36x QSFP28 | 100 Gbit/s | 1U Standard | Port-to-Power (P2C) | Redundantes AC-Netzteil (Dual AC PSU) |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | Nein | 36x QSFP28 | 100 Gbit/s | 1U Standard | Power-to-Port (C2P) | Redundantes AC-Netzteil (Dual AC PSU) |
| **MQM8700-HS2F** | Quantum (HDR) | Ja (x86) | 40x QSFP56 | 200 Gbit/s | 1U Standard | Port-to-Power (P2C) | Redundantes AC-Netzteil (Dual AC PSU) |
| **MQM8790-HS2F** | Quantum (HDR) | Nein | 40x QSFP56 | 200 Gbit/s | 1U Standard | Port-to-Power (P2C) | Redundantes AC-Netzteil (Dual AC PSU) |
| **MQM9700-NS2F** | Quantum 2 (NDR) | Ja | 32x OSFP (64x NDR-Ports) | 400 Gbit/s (OSFP) | 1U Standard | Port-to-Power (P2C) | Redundantes AC-Netzteil (Dual AC PSU) |
| **MQM9790-NS2F** | Quantum 2 (NDR) | Nein | 32x OSFP (64x NDR-Ports) | 400 Gbit/s (OSFP) | 1U Standard | Port-to-Power (P2C) | Redundantes AC-Netzteil (Dual AC PSU) |

---

## Vergleich der InfiniBand-Generationen

| Generation | Chipsatz | Max. Port-Geschwindigkeit | Switch-Kapazität | Übertragungsrate / Modulation | Latenz |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gbit/s | 7,2 Tbit/s | 25 Gbit/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gbit/s | 16,0 Tbit/s | 50 Gbit/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gbit/s (bereit für 800G) | 51,2 Tbit/s | 100 Gbit/s PAM4 | 205 ns |

---

## InfiniBand-Netzwerktopologien: Ein Leitfaden

Der Aufbau skalierbarer Cluster für KI-Training oder physikalische Simulationen erfordert optimierte Netzwerktopologien:

![NVIDIA Mellanox Fat-Tree InfiniBand-Topologie](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. Fat-Tree-Topologie (Non-Blocking CLOS)
Die klassische Architektur für InfiniBand-Netzwerke. Sie ordnet Switches in hierarchischen Ebenen (Leaf und Spine) an, um mehrere parallele Datenpfade bereitzustellen.
- **Non-Blocking (1:1-Verhältnis)**: Jeder Rechenknoten kann gleichzeitig mit voller Leitungsgeschwindigkeit kommunizieren. Dies erfordert die gleiche Uplink-Bandbreite zu den Spine-Switches wie Downlink-Bandbreite zu den Rechenknoten.
- **Oversubscribed (z. B. 2:1)**: Reduziert die Kosten für Switches durch weniger Verbindungen zur Spine-Ebene. Eignet sich für Anwendungen, bei denen die Kommunikation hauptsächlich innerhalb lokaler Gruppen stattfindet.

### 2. Rail-optimierte KI-Netzwerke
In Systemen mit mehreren GPUs (wie NVIDIA HGX H100 mit 8 GPUs) ist jeder GPU eine eigene ConnectX-NIC zugewiesen. Eine Rail-Optimierung verbindet alle Adapter der jeweiligen ersten GPUs („GPU 1“) über alle Server hinweg mit einem dedizierten ersten Switch („Rail-Switch 1“), alle zweiten GPUs („GPU 2“) mit „Rail-Switch 2“ usw. Dies bildet die Ring-Kommunikationsmuster von Deep-Learning-Bibliotheken (wie NCCL) direkt auf die physische Switch-Infrastruktur ab und minimiert die Latenz.

---

## Managed vs. Unmanaged Switches & Subnet Manager (SM)

Im Gegensatz zu Ethernet-Netzwerken, die dank ARP direkt betriebsbereit sind, kann ein InfiniBand-Netzwerk **ohne einen aktiven Subnet Manager (SM) keinen Datenverkehr übertragen**. Der SM ermittelt die Topologie, weist lokale Identifikatoren (LIDs) zu und berechnet die Routing-Pfade.
- **Managed Switches**: Verfügen über eine integrierte CPU mit MLNX-OS/Onyx, auf der ein Subnet Manager läuft. Optimal für eigenständige, kleinere Cluster (bis zu ca. 36 Knoten).
- **Unmanaged Switches**: Bieten extrem niedrige Latenzzeiten, besitzen jedoch keine eigene CPU. Sie erfordern einen externen SM, der entweder auf einem Host-Server (über OpenSM) oder auf einem anderen Managed Switch im Netzwerk ausgeführt wird.

---

{{< alert >}}
Benötigen Sie ein Produktangebot? Bitte [kontaktieren Sie uns](/de/contact/).
{{< /alert >}}
