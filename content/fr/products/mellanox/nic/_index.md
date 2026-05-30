---
title: "Cartes d'interface réseau (NIC) NVIDIA Mellanox ConnectX"
description: "Comparez les cartes réseau NVIDIA Mellanox ConnectX-4 Lx, ConnectX-5, ConnectX-6 Dx/Lx et ConnectX-7. Options 10G à 400G en PCIe Gen3/4/5."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Cartes réseau Mellanox / NVIDIA ConnectX — De 10G à 400G

Les adaptateurs NVIDIA Mellanox ConnectX offrent une bande passante et une latence de premier ordre pour les serveurs d'entreprise et les clusters d'intelligence artificielle. Voici le catalogue complet des modèles distribués par Yupitek, classés par vitesse.

---

## Cartes réseau 10GbE / 25GbE

Idéales pour les serveurs d'entreprise généralistes, la virtualisation (VMware ESXi) et le stockage NAS haute performance.

### Modèle 10G

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Équerre |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX4121A-XCAT** | ConnectX-4 Lx | Double | 10GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Standard |

### Modèles 25G

![NVIDIA ConnectX-4 Lx 25G](/images/products/mellanox/official/nic/connectx4-lx-25g-official.jpg)
*Adaptateur double port NVIDIA ConnectX-4 Lx 25GbE*

![NVIDIA ConnectX-5 25G](/images/products/mellanox/official/nic/connectx5-25g-official.jpg)
*Adaptateur double port NVIDIA ConnectX-5 25GbE*

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Équerre / Format | Caractéristiques |
|-------------|---------------|-------|-------|-----------|-----------|----------|-----------------------|------------------|
| **MCX4121A-ACAT** | ConnectX-4 Lx | Double | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Équerre standard | Carte PCIe standard |
| **MCX4121A-ACUT** | ConnectX-4 Lx | Double | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Équerre standard | UEFI activé |
| **MCX512A-ACAT** | ConnectX-5 EN | Double | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Équerre standard | RoCEv2 amélioré |
| **MCX512A-ACUT** | ConnectX-5 EN | Double | 25GbE | PCIe 3.0 x8 | SFP28 | Ethernet | Équerre standard | UEFI (x86/ARM) |
| **MCX631102AN-ADAT**| ConnectX-6 Lx | Double | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | Équerre standard | Secure Boot, sans chiffrement|
| **MCX623432AS-ADAB**| ConnectX-6 Lx | Double | 25GbE | PCIe 4.0 x8 | SFP28 | Ethernet | OCP 3.0 (vis à main) | Secure Boot, format OCP 3.0 |

---

## Cartes réseau 50GbE / 100GbE

Conçues pour le stockage NVMe over Fabrics (NVMe-oF) ultra-rapide, les infrastructures hyperconvergées (HCI) et les serveurs de bases de données.

![NVIDIA ConnectX-5 100G](/images/products/mellanox/official/nic/connectx5-100g-official.jpg)
*Adaptateur NVIDIA ConnectX-5 100GbE*

![NVIDIA ConnectX-6 Dx 100G](/images/products/mellanox/official/nic/connectx6-dx-100g-official.png)
*Adaptateur double port NVIDIA ConnectX-6 Dx 100GbE*

### Modèle 50G

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Équerre |
|-------------|---------------|-------|-------|-----------|-----------|----------|---------|
| **MCX515A-GCAT** | ConnectX-5 EN | Simple | 50GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | Standard |

### Modèles 100G

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Format | Caractéristiques |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX515A-CCAT** | ConnectX-5 EN | Simple | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | PCIe standard | Carte 100G standard |
| **MCX555A-ECAT** | ConnectX-5 VPI | Simple | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe standard | EDR InfiniBand & 100GbE |
| **MCX516A-CCAT** | ConnectX-5 EN | Double | 100GbE | PCIe 3.0 x16 | QSFP28 | Ethernet | PCIe standard | Double port 100G |
| **MCX516A-CDAT** | ConnectX-5 Ex | Double | 100GbE | PCIe 4.0 x16 | QSFP28 | Ethernet | PCIe standard | Interface PCIe 4.0 |
| **MCX556A-ECAT** | ConnectX-5 VPI | Double | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe standard | Double port EDR InfiniBand |
| **MCX556A-EDAT** | ConnectX-5 Ex VPI| Double | 100G | PCIe 4.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe standard | Double port EDR, PCIe 4.0 |
| **MCX653105A-ECAT**| ConnectX-6 VPI | Simple | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe standard | HDR100 InfiniBand & 100GbE|
| **MCX653106A-ECAT**| ConnectX-6 VPI | Double | 100G | PCIe 3.0 x16 | QSFP28 | VPI (IB/ETH) | PCIe standard | HDR100 InfiniBand & 100GbE|
| **MCX623106AN-CDAT**| ConnectX-6 Dx | Double | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | PCIe standard | 100G double port SFP56/QSFP56|
| **MCX623436AN-CDAB**| ConnectX-6 Dx | Double | 100GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | OCP 3.0 (vis à main) | Format OCP |

---

## Cartes réseau 200GbE / 400GbE

Adaptateurs de pointe conçus pour les nœuds de serveurs GPU d'intelligence artificielle (architectures NVIDIA HGX/DGX), le trading haute fréquence (HFT) et les cœurs de réseau HPC.

![NVIDIA ConnectX-7 400G](/images/products/mellanox/official/nic/connectx7-400g-official.png)
*Adaptateur NVIDIA ConnectX-7 400G au format OSFP*

### Modèles 200G

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Format | Caractéristiques |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX653105A-HDAT**| ConnectX-6 VPI | Simple | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe standard | HDR InfiniBand & 200GbE |
| **MCX653106A-HDAT**| ConnectX-6 VPI | Double | 200G | PCIe 4.0 x16 | QSFP56 | VPI (IB/ETH) | PCIe standard | Double port HDR/200G|
| **MCX623105A-VDAT**| ConnectX-6 Dx | Simple | 200GbE | PCIe 4.0 x16 | QSFP56 | Ethernet | PCIe standard | Simple port 200G |
| **MCX75310AAS-HEAT**| ConnectX-7 IB | Simple | 200G | PCIe 5.0 x16 | OSFP | InfiniBand | PCIe standard | NDR200, technologie Socket Direct|
| **MCX755106AS-HEAT**| ConnectX-7 VPI | Double | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | PCIe standard | 1 port InfiniBand, 2e port VPI|
| **MCX753436MS-HEAB**| ConnectX-7 VPI | Double | 200G | PCIe 5.0 x16 | QSFP112 | VPI (IB/ETH) | OCP 3.0 (vis à main) | Format OCP Multi-Host / Socket Direct|

### Modèles 400G

| Référence (P/N) | Génération / Chipset | Ports | Vitesse | Emplacement PCIe | Connecteur | Protocole | Format | Caractéristiques |
|-------------|---------------|-------|-------|-----------|-----------|----------|-------------|------------------|
| **MCX75310AAS-NEAT**| ConnectX-7 IB | Simple | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe standard | NDR InfiniBand |
| **MCX75510AAS-NEAT**| ConnectX-7 IB | Simple | 400Gb/s| PCIe 5.0 x16 | OSFP | InfiniBand | PCIe standard | NDR OSFP, prêt pour Socket Direct|

---

## Guide de sélection technique

Lors du choix de votre carte réseau ConnectX, veillez à prendre en compte les éléments suivants :

### 1. Mode de protocole (VPI ou Ethernet uniquement)
- **Les adaptateurs EN** prennent uniquement en charge les réseaux Ethernet.
- **Les adaptateurs VPI (Virtual Protocol Interconnect)** peuvent être configurés via leur firmware pour fonctionner soit en InfiniBand, soit en Ethernet, ce qui offre une flexibilité de déploiement maximale.

### 2. Besoins en bande passante PCIe
Vérifiez que la génération PCIe et la largeur du bus (lignes x8 ou x16) du serveur hôte peuvent alimenter la carte à plein débit :
- Une carte réseau double port 100G requiert du PCIe 4.0 x16 pour exploiter les deux ports simultanément à leur débit maximal.
- L'insertion d'une carte PCIe 4.0 dans un emplacement PCIe 3.0 est possible (compatibilité descendante), mais le débit sera limité par le bus PCIe 3.0 (environ 64 Gbit/s en x8, 128 Gbit/s en x16).

### 3. Format OCP 3.0 ou format PCIe standard
Les modèles se terminant par des suffixes comme `-ADAB`, `-CDAB` ou `-HEAB` adoptent le format **OCP NIC 3.0**. Ces cartes se glissent dans des baies serveurs dédiées (courantes chez Supermicro, Dell, HPE ou Lenovo de dernière génération) et ne peuvent pas être installées dans un emplacement PCIe standard.

---

Besoin de câbles compatibles ? Consultez nos gammes de [câbles DAC](/fr/products/mellanox/cable-dac/) et de [câbles AOC](/fr/products/mellanox/cable-aoc/). Pour connaître les tarifs et les disponibilités, [demandez un devis](/fr/contact/).
