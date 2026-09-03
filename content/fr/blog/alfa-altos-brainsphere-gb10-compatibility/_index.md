---
title: "Carte réseau sans fil ALFA : prise en charge du système ALTOS BrainSphere GB10 F1 ?"
date: 2026-09-03
draft: false
slug: "alfa-altos-brainsphere-gb10-compatibility"
tags:
  - "ALFA"
  - "Altos"
  - "BrainSphere-GB10"
  - "NVIDIA-GB10"
  - "AWUS036ACM"
  - "ARM64"
  - "DGX-OS"
categories:
  - "Guide Matériel"
description: "Altos GB10 F1 & NVIDIA DGX Spark: compatibilité ALFA, MediaTek et Realtek, drivers inclus, USB-C ports."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « L'ALFA série USB carte sans fil peut-elle être utilisée sur l'ALTOS BrainSphere GB10 F1 (NVIDIA GB10 Grace Blackwell) station de travail IA ? »

Conclusion rapide : L'ALTOS BrainSphere GB10 F1 et le NVIDIA DGX Spark partagent la même plateforme matérielle GB10 et l'environnement logiciel DGX OS, ce qui garantit une compatibilité complète avec les cartes ALFA (évaluée sur les 9 modèles de cartes USB ALFA en service). Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modèles) utilisent des pilotes in-kernel, prêts à l'emploi ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modèles) nécessitent la compilation de pilotes out-of-tree sur ARM64. Attention : le BrainSphere GB10 F1 dispose de 3 ports USB-C données + 1 port d'entrée USB-C PD, les cartes ALFA (à l'exception de l'AXML) doivent utiliser un adaptateur USB-C to USB-A.

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles de l'ALTOS BrainSphere GB10 F1

| Élément | Spécification |
|---|---|
| Nom du produit | ALTOS BrainSphere GB10 F1 (Acer / Altos Computing) |
| Processeur central | NVIDIA GB10 Grace Blackwell Superchip (plateforme DGX Spark) |
| CPU | 20-coeurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell de NVIDIA, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performance AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, prend en charge des modèles jusqu'à 20 milliards de paramètres |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | 4TB NVMe M.2 SSD (cryptage intégré) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode) + 1× USB 3.2 Gen 2×2 Type-C (alimentation PD, 180W EPR PD3.1) |
| Sortie vidéo | 1× HDMI 2.1a |
| Réseau câblé | 1× 10GbE RJ45 + NVIDIA ConnectX-7 NIC (200G × 2 QSFP) |
| Réseau sans fil | Wi-Fi 7 + Bluetooth 5.4 with LE |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 50 mm (1.13L) |
| Poids | < 1.5 kg |
| Consommation maximale | 170W |
| Logiciels inclus | Altos aiGeni (plateforme de développement AI en un clic, prend en charge TensorFlow / PyTorch / Jupyter / Ollama) |

> Vérification des spécifications : Les dimensions / poids / consommation / configuration USB mentionnées ci-dessus sont conformes au document de spécification produit officiel d'Altos (voir la section 10 Sources de référence).

### 2.2 Environnement logiciel : NVIDIA DGX OS + Altos aiGeni

| Élément | Contenu |
|---|---|
| OS de base | Ubuntu Linux (personnalisé par NVIDIA, DGX OS) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Plateforme AI | Altos aiGeni (déploiement d'environnement en un clic, sauvegarde automatique, surveillance en temps réel, outils intelligents) |
| Cadres préinstallés | TensorFlow, PyTorch, Jupyter, Ollama |
| Gestion des paquets | apt |

### 2.3 Différences avec DGX Spark

| Critère de différence | BrainSphere GB10 F1 | NVIDIA DGX Spark |
|---|---|---|
| Logiciels inclus | Plateforme de développement AI Altos aiGeni | Ensemble de logiciels de référence NVIDIA |
| Conception de l'architecture | Châssis personnalisé par Altos / Acer | Châssis de référence NVIDIA |
| Marché cible | Entreprise AI / Organismes de recherche / Éducation | Développement AI de bureau |
| Consommation maximale | 170W | Environ 240W (y compris la conversion d'alimentation) |

Impact sur la compatibilité avec ALFA : Aucun impact. Altos aiGeni est un logiciel d'application, il n'affecte pas le cadre de pilote du kernel. Les contrôleurs USB, la version du kernel et l'architecture des pilotes sont complètement identiques à ceux du DGX Spark.

### 2.4 Besoins en adaptateurs USB Type-C

Les 4 ports USB du BrainSphere GB10 F1 sont tous de type-C (3 ports de données + 1 port d'entrée PD), tandis que la gamme complète des cartes réseau ALFA (sauf AXML qui est en USB-C) est en USB Type-A. Un adaptateur est nécessaire.

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante :

| Modèle | Niveau Wi-Fi | Puce | Interface | État du pilote Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Comme ci-dessus |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Recommandé |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au couvert) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Modèles et SoC applicables

### 4.1 Catégorie recommandée

| Catégorie recommandée | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé | AWUS036ACM (MT7612U) | Pilote in-kernel, prêt à l'emploi, AC1200 double bande, supporte AP / Monitor / Injection |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote in-kernel, faible consommation d'énergie, AC433 double bande |
| ✅ Recommandé (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Pilote in-kernel, Wi-Fi 6E, AXML peut être inséré directement en USB-C |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACH (RTL8812AU) | Nécessite la compilation de morrownr/8812au (ARM64), fonctionnalités complètes après compilation |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACS / EACS | Nécessite la compilation du pilote out-of-tree correspondant |
| ⚠️ Disponible mais à utiliser avec précaution | AWUS036AX / AXER (RTL8832BU) | Le rtw89 du kernel 6.x pourrait déjà le prendre en charge ; pas besoin de compiler |

### 4.2 Suggestions de scénarios d'utilisation

| Scénario d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Laboratoire d'entreprise pour les expériences AI sans fil | AWUS036ACM / ACHM | Pilote in-kernel, stable, sans maintenance, adapté à l'environnement d'entreprise |
| Tests de pénétration sans fil / Recherche en sécurité | AWUS036ACH ou AWUS036ACM | Les deux supportent Monitor + Injection |
| Wi-Fi 6E / Fréquence 6GHz | AWUS036AXML / AXM | Pilote in-kernel MT7921AUN |
| Pas besoin de Wi-Fi externe | — | BrainSphere est intégré avec Wi-Fi 7, l'accès à Internet en général n'a pas besoin d'un Wi-Fi externe |

## 5. Besoins Environnementaux

### 5.1 Besoins Hardware

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur USB-C vers USB-A ou câble de transmission (sauf pour AXML), recommandé pour prendre en charge USB 3.2 Gen 2×2 |
| Alimentation | Alimentation USB-C d'origine ALTOS (180W EPR PD3.1) |

### 5.2 Besoins Logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Version en service (kernel 6.x) |
| Outils de compilation (nécessaire pour les puces Realtek) | build-essential, git, bc, dkms |
| Outils de gestion sans fil | iw, network-manager (installé par défaut dans DGX OS) |
| Remarques pour aiGeni | Si vous utilisez l'environnement de conteneurs d'aiGeni, assurez-vous que les appareils USB sont correctement montés dans le conteneur (pour une connexion Internet, il est recommandé de le configurer au niveau de l'OS hôte). |

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × ALTOS BrainSphere GB10 F1

| Modèle | Processeur | Mode de pilotage | Détection USB | STA Internet | Mode AP | Monitor | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sans installation | ⭐ Meilleur |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Moyen（compilation） | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |

Critère de détermination : ALTOS BrainSphere GB10 F1 et DGX Spark partagent la même plateforme matérielle GB10 et le même DGX OS (kernel 6.x, aarch64), la détermination de la compatibilité est complètement identique à celle de DGX Spark. Altos aiGeni est un logiciel d'application, il n'affecte pas la compatibilité des pilotes.

## 7. Détails ultra détaillés des étapes de configuration

Les étapes d'installation de l'ALTOS BrainSphere GB10 F1 sont identiques à celles de l'installation de NVIDIA DGX Spark. Voici une version raccourcie ; pour les étapes complètes, consultez la section 7 de l'article [ALFA 无线网卡是否支持 NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modèle de puce MediaTek (prêt à l'emploi)

- Utilisez un adaptateur USB-C to USB-A (AXML peut être inséré directement) pour insérer la carte réseau ALFA dans le port USB-C du BrainSphere
- Confirmez la détection : `lsusb`
- Confirmez l'interface : `ip link show` (wlan0 devrait apparaître automatiquement)
- Connectez-vous au WiFi : `nmcli dev wifi connect "SSID" password "mot de passe"`

### 7.2 Modèle de puce Realtek (nécessite la compilation)

Prenez AWUS036ACH (RTL8812AU) comme exemple :

```bash
# 1. Installez les outils de compilation
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Téléchargez et compilez le pilote
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Vérifiez que CONFIG_PLATFORM_ARM64 = y est confirmé dans Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Confirmez l'interface après l'insertion de la carte réseau
ip link show

# 4. Connectez-vous au WiFi
nmcli dev wifi connect "SSID" password "mot de passe"
```

### 7.3 Mode écoute (test d'intrusion)

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo aireplay-ng --test wlan0
```

### 7.4 Utilisation du WiFi dans le conteneur aiGeni (avancé)

Si vous souhaitez utiliser la carte réseau ALFA dans le conteneur Docker d'Altos aiGeni :

1. Terminez d'installer le pilote et de vous connecter au WiFi sur l'OS hôte (DGX OS)
2. Lancez le conteneur avec `--network=host` ou montez l'interface réseau correspondante
3. Il est recommandé de terminer les connexions Internet sur l'OS hôte, et le conteneur utilise `--network=bridge` pour partager le réseau

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / Seulement en charge | Changer un adaptateur USB 3.2 Gen 2×2 compatible avec la transmission de données ; essayer un autre port USB-C |
| Interface wlan du processeur MediaTek absente | Module non chargé automatiquement / Firmware manquant | `sudo modprobe mt76x2u` ; `sudo apt install linux-firmware` ; vérifier `dmesg | grep mt76` |
| Échec de la compilation du pilote Realtek | Paramètres de compilation croisée incorrects | Vérifier la compilation native sur BrainSphere ; le Makefile ne devrait pas définir CROSS_COMPILE |
| Vitesse WiFi lente | Adaptateur ne supporte que USB 2.0 | Changer un adaptateur USB 3.2 Gen 2×2 |
| Conflit entre le Wi-Fi intégré et externe | Conflit de routeur | `sudo nmcli radio wifi off` pour désactiver le Wi-Fi intégré avant d'utiliser le Wi-Fi externe |
| Impossible de voir le WiFi dans le conteneur aiGeni | Problème de mode réseau du conteneur | Utiliser `--network=host` ; ou permettre au conteneur de partager le réseau après la connexion sur l'OS hôte |
| Impossible d'utiliser la bande 6GHz | Limitation du domaine réglementaire | `sudo iw reg set US` ; vérifier les dernières réglementations |

## 9. Conditions Connues

- Nécessité de convertisseur USB Type-C : tous les cartes réseaux ALFA, sauf AXML, nécessitent un adaptateur USB-C to USB-A
- Nécessité de traduction manuelle pour les puces Realtek : RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU ne sont pas intégrés dans le mainline
- Possibilité de conflit avec Wi-Fi intégré : BrainSphere intègre déjà Wi-Fi 7 + BT 5.4
- Configuration manuelle du mode AP : DGX OS est par défaut un environnement de développement
- Limitations réglementaires pour la bande 6GHz : la disponibilité du Wi-Fi 6E dépend des zones réglementaires
- Mise à jour des pilotes dépendante de l'upstream : les pilotes out-of-tree pour Realtek sont maintenus par la communauté, et nécessitent une recompilation après une mise à jour du kernel
- Isolation de conteneurs aiGeni : si vous utilisez WiFi dans un conteneur aiGeni, veillez à la gestion des espaces de noms réseau et des montage de périphériques ; il est recommandé de gérer le WiFi au niveau du système d'exploitation hôte
- Différences de logiciel Altos n'affectent pas la compatibilité : aiGeni est une plateforme d'application, elle n'affecte pas la compatibilité des pilotes USB WiFi pour le kernel

Conditions de réfutation : les jugements ci-dessus sont basés sur DGX OS (basé sur Ubuntu, kernel 6.x). Si Altos passe à un OS maison non basé sur Ubuntu à l'avenir, ou si le kernel de DGX OS change de version principale, les jugements in-kernel / out-of-tree devront être réévalués.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Fiche produit officielle ALTOS BrainSphere GB10 F1 (PDF) | Spécifications matérielles (170W / 50mm / configuration USB) | https://www.altoscomputing.com/filepic/pdf/Altos_BrainSphere_GB10_F1_Product_Sheet_TW.pdf | ✅ Vérifié | 2026-09-03 |
| Site officiel d'Altos Computing | Informations sur le produit BrainSphere GB10 F1 | https://www.altoscomputing.com/en-Us | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA DGX Spark | Informations sur la plate-forme GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux pour RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yupitek) | Spécifications des produits actuels ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec ASUS Ascent GX10 ?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec GIGABYTE AI TOP ATOM ?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec MSI EdgeXpert ?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article est basée sur le NVIDIA DGX OS préinstallé sur ALTOS BrainSphere GB10 F1 (kernel 6.x, aarch64). BrainSphere et DGX Spark partagent la même plate-forme matérielle, la compatibilité est complètement identique. Altos aiGeni est un logiciel d'application, il n'affecte pas la compatibilité du pilote. Les pilotes de puce MediaTek sont du Linux mainline, leur stabilité est élevée ; les pilotes de puce Realtek sont maintenus par la communauté. BrainSphere est intégré avec Wi-Fi 7, l'ALFA externe est principalement utilisé pour des tests de pénétration ou des besoins spéciaux de puce.
