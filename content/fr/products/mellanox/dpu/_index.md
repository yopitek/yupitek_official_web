---
title: "Unités de traitement de données (DPU) NVIDIA BlueField"
description: "Découvrez les DPU NVIDIA BlueField. Déchargez, accélérez et isolez les services d'infrastructure réseau, de stockage et de sécurité avec des SmartNICs programmables ARM."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Unités de traitement de données (DPU) NVIDIA BlueField

Les unités de traitement de données (DPU) NVIDIA® BlueField® marquent un tournant technologique majeur dans l'architecture des centres de données. En associant les cartes réseau ConnectX de pointe à des cœurs de processeur ARM® programmables et des moteurs d'accélération matérielle, les DPU déchargent, accélèrent et isolent les tâches d'infrastructure pour libérer le processeur (CPU) du serveur.

---

## Gamme de DPU BlueField

Nous distribuons des DPU BlueField optimisés pour la virtualisation à l'échelle du cloud, le stockage défini par logiciel et la sécurité Zero Trust.

![NVIDIA BlueField DPU](/images/products/mellanox/official/dpu/bluefield2-dpu-official.jpg)
*Adaptateur d'infrastructure programmable NVIDIA BlueField*

| Référence (P/N) | Nom commercial | Connectivité réseau | Cœurs CPU ARM | Mémoire | Interface | Protocole | Format |
|-------------|----------------|-----------------|---------------|--------|-----------|----------|-------------|
| **900-9D3B6-00CV-AA0** | BlueField-2 DPU | Double port 100GbE / EDR IB | 8x ARMv8 A72 | 16 Go DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe |
| **900-9D3B6-00CC-EA0** | BlueField-2 DPU | Double port 100GbE / EDR IB | 8x ARMv8 A72 | 16 Go DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (chiffrement activé) |
| **900-9D3B4-00CC-EA0** | BlueField-2 DPU | Simple port 100GbE / EDR IB | 8x ARMv8 A72 | 16 Go DDR4 | PCIe 4.0 x16 | VPI (IB/ETH) | FHHL PCIe (chiffrement activé) |

---

## Technologies clés des DPU

### 1. Déchargement de l'infrastructure (SmartNIC+)
Au lieu de consommer de précieux cycles du processeur hôte pour gérer le routage réseau de l'hyperviseur (OVS), les tunnels de virtualisation (VXLAN, NVGRE) ou la traduction d'adresses réseau (NAT), le DPU traite ces tâches au débit de la ligne (wire-speed) directement au niveau matériel grâce à la technologie **NVIDIA ASAP² (Accelerated Switch and Packet Processing)**.

### 2. Accélération du stockage défini par logiciel
Grâce à **NVMe SNAP™ (Software-defined Network Accelerated Processing)**, un DPU BlueField présente le stockage réseau distant (via RoCEv2 ou TCP) comme un disque physique NVMe local au système d'exploitation hôte. L'émulation, le chiffrement et la compression sont gérés intégralement par le DPU, éliminant les goulets d'étranglement de stockage liés à la virtualisation.

### 3. Sécurité Zero Trust et isolation
Le DPU exécute son propre système d'exploitation Linux indépendant (généralement Ubuntu) sur ses cœurs ARM intégrés, de manière totalement isolée du serveur hôte. Même si le système d'exploitation hôte est compromis, les agents de sécurité, les pare-feux sans agent et le chiffrement réseau (IPsec, TLS) s'exécutant sur le DPU continuent de fonctionner en toute sécurité.

### 4. Framework logiciel NVIDIA DOCA
Les DPU BlueField se programment à l'aide de l'environnement logiciel **NVIDIA DOCA™**, qui fournit des API standards pour le développement d'applications accélérées destinées au réseau, à la sécurité, au stockage et à la télémétrie.

---

## Cas d'usage fréquents

- **Fournisseurs de cloud de nouvelle génération** : hébergement bare-metal où la gestion de l'infrastructure est entièrement isolée sur le DPU.
- **Infrastructures hyperconvergées d'entreprise (HCI)** : déchargement des couches réseau et stockage (VMware NSX / Proxmox OVS) pour maximiser la densité des machines virtuelles (VM).
- **Environnements haute sécurité** : exécution de la surveillance de la sécurité réseau (IDS/IPS) et du chiffrement directement à la frontière du réseau.

---

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
