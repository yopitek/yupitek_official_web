---
title: "Carte réseau sans fil ALFA : prise en charge par MSI EdgeXpert (GB10) ?"
date: 2026-09-03
draft: false
slug: "alfa-msi-edgexpert-compatibility"
tags:
  - "ALFA"
  - "MSI"
  - "EdgeXpert"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guide Matériel"
description: "MSI EdgeXpert & NVIDIA DGX Spark : compatibilité ALFA, MediaTek et Realtek, USB Type-C, conversion nécessaire."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Le client demande : « L'ALFA série USB carte réseau sans fil peut-elle être utilisée sur l'ordinateur portable MSI EdgeXpert (NVIDIA GB10 Grace Blackwell) superordinateur AI ? »

Conclusion rapide : MSI EdgeXpert et NVIDIA DGX Spark partagent la même plateforme matérielle GB10 et l'environnement logiciel DGX OS, ce qui garantit une compatibilité complète avec les cartes ALFA. Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM) utilisent un pilote in-kernel, prêt à l'emploi ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER) nécessitent la compilation d'un pilote out-of-tree sur ARM64. Attention : les 4 ports USB d'EdgeXpert sont tous de type USB Type-C (20Gbps), les cartes ALFA (à l'exception de l'AXML) doivent utiliser un adaptateur USB-C to USB-A.

Évaluation des modèles : ALFA dispose de 9 cartes réseau USB en service (AWUS036ACM / ACHM / ACS / EACS / ACH / AX / AXER / AXML / AXM).

## 2. Analyser les spécifications matérielles cibles

### 2.1 Spécifications matérielles de MSI EdgeXpert

| Élément | Spécification |
|---|---|
| Nom du produit | MSI EdgeXpert (modèles : EdgeXpert-MS-C931 / 59STW et autres) |
| Processeur central | NVIDIA GB10 Grace Blackwell Superchip (plateforme DGX Spark) |
| CPU | 20-coeurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell de NVIDIA, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performance AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | 1TB ou 4TB SSD NVMe M.2 (cryptage intégré, PCIe Gen5) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (jusqu'à 20Gbps) |
| Sortie vidéo | 1× HDMI 2.1a (4× DP1.4a via USB-C Alt Mode) |
| Réseau filaire | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (QSFP 200GbE, interconnexions système) |
| Réseau sans fil | Wi-Fi 7 + Bluetooth 5.4 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 151 × 151 × 52 mm (environ 5.95" × 5.95" × 2.05") |
| Poids | Environ 1.2 kg (2.65 lbs) |
| Alimentation | Alimentation USB-C de 240W |
| Version | Version de consommation / version industrielle (EdgeXpert-MS-C931, application à température large / industrielle) |

### 2.2 Environnement logiciel : NVIDIA DGX OS

MSI EdgeXpert est préinstallé avec NVIDIA DGX OS, tout comme les DGX Spark et ASUS GX10 :

| Élément | Description |
|---|---|
| Base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestion des paquets | apt |

### 2.3 Différences avec DGX Spark

MSI EdgeXpert est une version OEM de la plateforme DGX Spark, avec du matériel et des logiciels identiques :

| Élément | MSI EdgeXpert | NVIDIA DGX Spark |
|---|---|---|
| Conception de l'institution | Châssis personnalisé MSI, option industrielle | Châssis de référence NVIDIA |
| Options de stockage | 1TB / 4TB | Jusqu'à 4TB |
| Marché cible | AI à la périphérie / AI industrielle / Développement de bureau | Développement de bureau AI |
| Accessoires | Accessoires d'origine MSI | Accessoires d'origine NVIDIA |

Impact sur la compatibilité avec ALFA : Aucun impact. Les contrôleurs USB, les versions du kernel et les frameworks de pilotes sont identiques à ceux du DGX Spark.

### 2.4 Besoins en adaptateurs USB Type-C

Les 4 ports USB de l'EdgeXpert sont de type-C. La gamme complète de cartes réseau ALFA (sauf AXML en USB-C) est de type-A, il est nécessaire d'utiliser un adaptateur. Il est recommandé de choisir un adaptateur compatible avec USB 3.2 Gen 2×2 (20Gbps).

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante (base : 9 modèles) :

| Modèle | Niveau Wi-Fi | Puce | Interface | État du pilote Linux |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ✅ in-kernel (mt7921u) |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ✅ in-kernel (mt7921u) |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ rtw89 / out-of-tree |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Comme ci-dessus |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ⚠️ out-of-tree (8812au) |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ✅ in-kernel (mt76x0u) |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ✅ in-kernel (mt76x2u)⭐ Préférable |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ⚠️ out-of-tree (8812au couvert) |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ⚠️ out-of-tree (8821cu) |

## 4. Modèles et SoC applicables

### 4.1 Catégorie de recommandation

| Catégorie de recommandation | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé | AWUS036ACM (MT7612U) | Pilote in-kernel, prêt à l'emploi, AC1200 double bande, supporte AP / Monitor / Injection |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote in-kernel, faible consommation d'énergie, AC433 double bande |
| ✅ Recommandé (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Pilote in-kernel, Wi-Fi 6E, AXML peut être inséré directement en USB-C |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACH (RTL8812AU) | Nécessite la compilation de morrownr/8812au (ARM64), fonctionnalités complètes après compilation |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACS / EACS | Nécessite la compilation du pilote out-of-tree correspondant |
| ⚠️ Disponible mais à utiliser avec précaution | AWUS036AX / AXER (RTL8832BU) | Le rtw89 du kernel 6.x pourrait déjà le prendre en charge ; pas besoin de compiler |

### 4.2 Recommandations d'utilisation

| Scène d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Connexion sans fil pour passerelle AI à la périphérie | AWUS036ACM / ACHM | Pilote in-kernel, stable, sans maintenance |
| Tests de pénétration sans fil dans l'environnement industriel | AWUS036ACH ou AWUS036ACM | Les deux supportent Monitor + Injection |
| Fréquence 6GHz / Wi-Fi 6E | AWUS036AXML / AXM | Pilote in-kernel MT7921AUN |
| Pas besoin de Wi-Fi externe | — | EdgeXpert intègre déjà Wi-Fi 7, pas besoin d'ajouter un Wi-Fi externe pour la navigation sur Internet |

## 5. Besoins Environnementaux

### 5.1 Besoins Hardware

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur USB-C vers USB-A ou câble de transmission (sauf pour AXML), recommandé pour le support USB 3.2 Gen 2×2 |
| Alimentation | Alimentation USB-C 240W MSI EdgeXpert d'origine |

### 5.2 Besoins Logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Version en service (kernel 6.x) |
| Outils de compilation (nécessaire pour les puces Realtek) | build-essential, git, bc, dkms |
| Outils de gestion sans fil | iw, network-manager (installé par défaut dans DGX OS) |

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × MSI EdgeXpert（GB10）

| Modèle | Processeur | Mode de pilotage | Détection USB | STA Internet | Mode AP | Monitor | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel（mt76x2u） | ✅ | ✅ | ✅ | ✅ | Sans installation | ⭐ Meilleur |
| AWUS036ACHM | MT7610U | in-kernel（mt76x0u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXML | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXM | MT7921AUN | in-kernel（mt7921u） | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036ACH | RTL8812AU | out-of-tree（8812au） | ✅ | ✅ | ✅ | ✅ | Moyen（traduction） | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree（8812au） | ✅ | ✅ | ⚠️ | ❌ | Moyen（traduction） | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree（8821cu） | ✅ | ⚠️ | ❌ | ❌ | Moyen（traduction） | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |

Critère de détermination : MSI EdgeXpert et DGX Spark partagent la même plateforme matérielle GB10 et le même système d'exploitation DGX OS (kernel 6.x, aarch64), la détermination de la compatibilité est identique à celle de DGX Spark.

## 7. Détails ultra détaillés : Étapes de configuration étape par étape

Les étapes d'installation de MSI EdgeXpert sont identiques à celles de NVIDIA DGX Spark. Voici une version raccourcie ; pour les étapes complètes, consultez le chapitre 7 de l'article [ALFA : Carte réseau sans fil, est-elle compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modèles de puces MediaTek (prêt à l'emploi)

**Étape 1 : Insérer la carte réseau**

Utilisez un adaptateur USB-C to USB-A (AXML peut être inséré directement) pour insérer la carte réseau ALFA dans le port USB-C d'EdgeXpert.

**Étape 2 : Vérifier la détection USB**

```bash
lsusb
# Sortie prévue (AWUS036ACM / MT7612U) :
# Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

**Étape 3 : Vérifier l'interface réseau**

```bash
ip link show
# Doit automatiquement apparaître wlan0 (pilote in-kernel automatiquement chargé)
```

**Étape 4 : Se connecter au WiFi**

```bash
nmcli dev wifi connect "SSID" password "mot de passe"
```

### 7.2 Modèles de puces Realtek (nécessite la compilation)

Prenez AWUS036ACH (RTL8812AU) comme exemple :

**Étape 1 : Installer les outils de compilation**

```bash
sudo apt update && sudo apt install -y build-essential git bc dkms
```

**Étape 2 : Télécharger et compiler le pilote**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Vérifier que CONFIG_PLATFORM_ARM64 = y dans Makefile
make
sudo make install
sudo modprobe 8812au
```

**Étape 3 : Vérifier l'interface après insertion de la carte réseau**

```bash
ip link show
```

**Étape 4 : Se connecter au WiFi**

```bash
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

## 8. Erreurs courantes et solutions

| Symptômes | Causes possibles | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / Seulement en charge | Changer un adaptateur USB 3.2 Gen 2×2 compatible avec la transmission de données ; essayer un autre port USB-C |
| Interface wlan du processeur MediaTek absente | Module non chargé automatiquement / Firmware manquant | `sudo modprobe mt76x2u` ; `sudo apt install linux-firmware` ; vérifier `dmesg | grep mt76` |
| Échec de la compilation du pilote Realtek | Paramètres de compilation croisée incorrects | Confirmer la compilation native sur EdgeXpert ; le Makefile ne devrait pas définir CROSS_COMPILE |
| Vitesse WiFi lente | Adaptateur ne supporte que USB 2.0 | Changer un adaptateur USB 3.2 Gen 2×2 |
| Conflit entre le Wi-Fi intégré et externe | Conflit de routeur | `sudo nmcli radio wifi off` désactiver le WiFi intégré avant d'utiliser le WiFi externe |
| Instabilité sous forte chaleur dans un environnement industriel | Refroidissement / Différences entre les versions industrielles | Confirmer l'utilisation de la version industrielle EdgeXpert (MS-C931) ; s'assurer que la température de l'environnement est dans les limites spécifiées |

## 9. Conditions connues

- Nécessité de convertisseur USB Type-C : tous les cartes réseaux ALFA, sauf l'AXML, nécessitent un adaptateur USB-C to USB-A
- Nécessité de traduction manuelle pour les puces Realtek : RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU ne sont pas intégrés dans le mainline
- Possibilité de conflit avec Wi-Fi intégré 7 : EdgeXpert intègre déjà Wi-Fi 7 + BT 5.4
- Mode AP à configurer manuellement : DGX OS est par défaut un environnement de développement
- Limitations réglementaires pour la bande 6GHz : la disponibilité de Wi-Fi 6E dépend des zones réglementaires
- Mise à jour des pilotes dépendante des contributions supérieures : les pilotes out-of-tree pour Realtek sont maintenus par la communauté, et doivent être recompilés après une mise à jour du kernel
- Différences de version industrielle sans incidence sur la compatibilité : la version industrielle MSI (MS-C931) a les mêmes spécifications matérielles que la version de consommation, et la compatibilité USB WiFi est identique

Conditions de réfutation : si la page de spécifications officielle de MSI change (ajustement des spécifications des ports USB, version du kernel inférieure à 6.x), ou si des tests réels montrent que mt76x2u / mt7921u ne peuvent pas être chargés automatiquement sur DGX OS, le tableau de compatibilité de l'article 6 doit être révisé ; si le pilote morrownr cesse de maintenir la branche ARM64, l'évaluation des modèles Realtek doit être réexaminée.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| MSI EdgeXpert商城（US） | Spécifications de la version de consommation d'EdgeXpert | https://us-store.msi.com/MSI-EdgeXpert-Blackwell-AI-Supercomputer | ✅ Vérifié | 2026-09-03 |
| MSI EdgeXpert商城（TW） | Spécifications de la version de consommation d'EdgeXpert（23STW） | https://tw-store.msi.com/products/edgexpert-23stw-bgb104tg4 | ✅ Vérifié | 2026-09-03 |
| MSI公告官方工业电脑 | Informations de publication de produits EdgeXpert | https://ipc.msi.com/en/news/146241 | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA DGX Spark | Informations sur la plate-forme GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux pour RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| ALFA Network produits (Yupitek) | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec ASUS Ascent GX10 ?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec ALTOS BrainSphere GB10 F1 ?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec GIGABYTE AI TOP ATOM ?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Est-ce que la carte réseau sans fil ALFA est compatible avec NVIDIA Jetson Nano ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-jetson-nano-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article est basée sur le système d'exploitation NVIDIA DGX OS préinstallé dans MSI EdgeXpert (kernel 6.x, aarch64). EdgeXpert et DGX Spark partagent la même plate-forme matérielle, et leur compatibilité est complètement identique. Les pilotes de puces MediaTek sont pour Linux mainline, avec une stabilité élevée ; les pilotes de puces Realtek sont maintenus par la communauté. EdgeXpert intègre Wi-Fi 7, et l'ALFA externe est principalement utilisée pour des tests de pénétration ou des besoins spécifiques de puces.
