---
title: "Commutateurs InfiniBand et Ethernet NVIDIA Mellanox"
description: "Commutateurs réseau haute densité. Sélectionnez les commutateurs Mellanox EDR (100G), HDR (200G) et NDR (400G). Conçus pour le HPC et les clusters d'IA."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Commutateurs InfiniBand et Ethernet NVIDIA Mellanox — EDR, HDR et NDR

Les commutateurs InfiniBand NVIDIA Mellanox constituent le cœur des clusters d'apprentissage de l'IA et des environnements de calcul haute performance (HPC) modernes. Grâce à une densité de ports élevée, une latence de commutation extrêmement faible et une gestion avancée de la congestion, ces équipements permettent de faire évoluer vos systèmes multi-nœuds en toute fluidité.

---

## Catalogue de commutateurs

Voici la liste des commutateurs 1U rackables (gérés et non gérés) disponibles dans notre stock.

![Mellanox HDR InfiniBand Switch](/images/products/mellanox/official/switch/switch-hdr-40port-official.png)
*Commutateur InfiniBand NVIDIA Mellanox Quantum HDR 40 ports*

| Référence (P/N) | Génération du chipset | Géré (Managed) | Configuration des ports | Vitesse de port | Format | Sens du flux d'air | Alimentation |
|-------------|--------------------|---------|---------------------|------------|-------------|---------|--------------|
| **MSB7800-ES2F** | Switch-IB 2 (EDR) | Oui (x86) | 36x QSFP28 | 100 Gbit/s | 1U standard | Du port vers l'alimentation (P2C) | Double alimentation AC |
| **MSB7890-ES2R** | Switch-IB 2 (EDR) | Non | 36x QSFP28 | 100 Gbit/s | 1U standard | De l'alimentation vers le port (C2P) | Double alimentation AC |
| **MQM8700-HS2F** | Quantum (HDR) | Oui (x86) | 40x QSFP56 | 200 Gbit/s | 1U standard | Du port vers l'alimentation (P2C) | Double alimentation AC |
| **MQM8790-HS2F** | Quantum (HDR) | Non | 40x QSFP56 | 200 Gbit/s | 1U standard | Du port vers l'alimentation (P2C) | Double alimentation AC |
| **MQM9700-NS2F** | Quantum 2 (NDR) | Oui | 32x OSFP (64 ports NDR) | 400 Gbit/s (OSFP) | 1U standard | Du port vers l'alimentation (P2C) | Double alimentation AC |
| **MQM9790-NS2F** | Quantum 2 (NDR) | Non | 32x OSFP (64 ports NDR) | 400 Gbit/s (OSFP) | 1U standard | Du port vers l'alimentation (P2C) | Double alimentation AC |

---

## Comparatif des générations InfiniBand

| Génération | Chipset | Vitesse de port max. | Capacité de commutation | Débit de signal / Modulation | Latence |
|------------|---------|----------------|-----------------|-----------------------------|---------|
| **EDR** | Switch-IB 2 | 100 Gbit/s | 7,2 Tbit/s | 25 Gbit/s NRZ | 90 ns |
| **HDR** | Quantum | 200 Gbit/s | 16,0 Tbit/s | 50 Gbit/s PAM4 | 130 ns |
| **NDR** | Quantum 2 | 400 Gbit/s (compatible 800G) | 51,2 Tbit/s | 100 Gbit/s PAM4 | 205 ns |

---

## Guide des topologies réseau InfiniBand

La création d'un cluster d'apprentissage d'IA ou de simulation physique nécessite des topologies réseau spécifiques :

![NVIDIA Mellanox Fat-Tree InfiniBand Topology](/images/products/mellanox/ai-generated/switch_topology@2x.png)

### 1. Topologie Fat-Tree (CLOS non bloquant)
Il s'agit de l'architecture de référence pour les réseaux InfiniBand. Elle structure les commutateurs en niveaux hiérarchiques (niveaux Leaf et Spine) afin d'offrir des chemins d'accès redondants et parallèles.
- **Non bloquant (taux de sursouscription 1:1)** : chaque nœud peut communiquer simultanément à la vitesse maximale du support (*wire-speed*). Cette configuration exige une bande passante identique pour la liaison montante (uplink vers le spine) et pour la liaison descendante (downlink vers les nœuds).
- **Sursouscrit (ex. 2:1)** : réduit le coût des équipements en limitant le nombre de liaisons vers le niveau spine. Convient aux charges de travail dont les échanges de données s'effectuent principalement à l'échelle locale.

### 2. Réseaux d'IA optimisés par rails (Rail-Optimized)
Dans les nœuds serveurs multi-GPU (tels que NVIDIA HGX H100 dotés de 8 GPU), chaque GPU possède sa propre carte d'interface réseau ConnectX. L'optimisation par rails consiste à raccorder tous les adaptateurs liés au « GPU 1 » de chaque serveur à un commutateur dédié (« Rail Switch 1 »), tous les adaptateurs du « GPU 2 » à un « Rail Switch 2 », et ainsi de suite. Ce schéma fait correspondre le modèle de communication en anneau des bibliothèques d'apprentissage profond (comme NCCL) directement aux commutateurs physiques, ce qui réduit considérablement la latence.

---

## Commutateurs gérés (Managed) vs non gérés (Unmanaged) & Subnet Manager (SM)

À la différence des réseaux Ethernet, qui sont prêts à l'emploi grâce au protocole ARP, un réseau InfiniBand **ne peut pas transmettre de trafic sans un gestionnaire de sous-réseau (Subnet Manager - SM) actif**. Le SM est chargé de découvrir la topologie, d'attribuer les identifiants locaux (LID) et de calculer les chemins de routage.
- **Commutateurs gérés (Managed)** : équipés d'un processeur interne exécutant MLNX-OS ou Onyx, ils intègrent un gestionnaire de sous-réseau (SM). C'est la solution idéale pour les petits clusters autonomes (jusqu'à environ 36 nœuds).
- **Commutateurs non gérés (Unmanaged)** : dotés d'une latence extrêmement faible, ils ne possèdent pas de CPU interne. Ils nécessitent l'utilisation d'un SM externe, qui s'exécute soit sur l'un des serveurs hôtes (via OpenSM), soit sur un commutateur géré dédié présent au sein du réseau.

---

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
