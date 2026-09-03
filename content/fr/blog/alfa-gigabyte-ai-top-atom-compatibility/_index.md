---
title: "Carte sans fil ALFA : Prise en charge par le processeur AI TOP ATOM (GB10) de GIGABYTE ?"
date: 2026-09-03
draft: false
slug: "alfa-gigabyte-ai-top-atom-compatibility"
tags:
  - "ALFA"
  - "GIGABYTE"
  - "AI-TOP-ATOM"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "ARM64"
categories:
  - "Guide Matériel"
description: "GIGABYTE AI TOP ATOM & NVIDIA DGX Spark : compatibilité ALFA, support MediaTek et Realtek, USB-C ports, adaptateurs nécessaires."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « Peut-on utiliser la carte réseau USB sans fil de la série ALFA sur l'ordinateur personnel AI TOP ATOM de GIGABYTE (modèle ATAGB10-9000, NVIDIA GB10 Grace Blackwell) ? »

Conclusion rapide : L'ordinateur personnel AI TOP ATOM de GIGABYTE et le NVIDIA DGX Spark partagent la même plateforme matérielle GB10 et l'environnement logiciel DGX OS, ce qui garantit une compatibilité complète avec les cartes ALFA (évaluée sur les 9 modèles de cartes réseau USB actuels ALFA). Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modèles) utilisent des pilotes in-kernel et sont prêts à l'emploi dès l'ouverture de la boîte ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modèles) nécessitent la compilation de pilotes out-of-tree sur ARM64. Attention : tous les ports USB de l'AI TOP ATOM sont de type USB Type-C, les cartes ALFA (à l'exception de l'AXML) nécessitent un adaptateur USB-C to USB-A.

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles du GIGABYTE AI TOP ATOM

| Élément | Spécification |
|---|---|
| Nom du produit | GIGABYTE AI TOP ATOM (modèle : ATAGB10-9000 / ATAGB10-9001) |
| Puce de cœur | NVIDIA GB10 Grace Blackwell Superchip (plateforme DGX Spark) |
| CPU | 20-coeurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell de NVIDIA, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performance AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS, prend en charge des modèles de paramètres jusqu'à 20 milliards |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | Jusqu'à 4TB M.2 NVMe SSD (ATAGB10-9000 pour PCIe Gen5 4TB ; 9001 pour Gen4 4TB) |
| USB | 4× USB 3.2 Gen 2×2 Type-C (20Gbps), dont 1 pour l'entrée d'alimentation (conforme au design de référence GB10) |
| Sortie vidéo | 1× HDMI 2.1a (extensible via DP Alt Mode via USB-C) |
| Réseau câblé | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC |
| Réseau sans fil | Wi-Fi 7 + Bluetooth 5.3 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimension | 150 × 150 × 50.5 mm (1.13L) |
| Poids | Environ 1.2 kg |
| Alimentation | Alimentation USB-C de 240W |
| Garantie | 1 an de garantie d'origine |

> Notes de vérification des spécifications : Les dimensions 50.5mm / poids 1.2kg sont conformes aux spécifications officielles de GIGABYTE ; la version Bluetooth est **BT 5.3** (le texte original indiquait 5.4, corrigé). La configuration USB est de 3 ports de données + 1 port d'alimentation (les spécifications officielles sont 4× Type-C, dont 1 dédié à l'alimentation du système).

### 2.2 Environnement logiciel : NVIDIA DGX OS

| Élément | Contenu |
|---|---|
| OS de base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | NVIDIA AI Software Stack (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, Ollama, etc.) + GIGABYTE AI TOP Utility |
| Gestion des paquets | apt |

### 2.3 Différences avec DGX Spark

| Critère de différence | AI TOP ATOM | NVIDIA DGX Spark |
|---|---|---|
| Conception de l'appareil | Boîtier personnalisé GIGABYTE / AORUS | Boîtier de référence NVIDIA |
| Position de marque | Superordinateur AI personnel (desktop / bureau) | Plateforme de développement AI de bureau NVIDIA |
| Stockage | Jusqu'à 4TB (versions Gen5 / Gen4) | Jusqu'à 4TB |
| Accessoires | Pièces d'origine GIGABYTE + AI TOP Utility | Pièces d'origine NVIDIA |
| Garantie | 1 an | Selon le canal de vente |
| Impact sur la compatibilité ALFA | Aucun impact. Les contrôleurs USB, les versions du kernel et les frameworks de pilotes sont complètement identiques à ceux de DGX Spark.

### 2.4 Besoins en adaptateurs USB Type-C

Les ports USB de l'AI TOP ATOM sont tous de type-C, tandis que la gamme complète de cartes réseau ALFA (sauf AXML pour USB-C) sont de type-A, nécessitant un adaptateur. Il est recommandé de choisir un adaptateur prenant en charge USB 3.2 Gen 2×2 (20Gbps) pour assurer que les modèles USB 3.x tels que AWUS036ACH / ACM / AX peuvent fonctionner à pleine vitesse.

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

### 4.1 Catégorie de recommandation

| Catégorie de recommandation | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé | AWUS036ACM (MT7612U) | Pilote in-kernel, prêt à l'emploi, AC1200 double bande, supporte AP / Monitor / Injection |
| ✅ Recommandé | AWUS036ACHM (MT7610U) | Pilote in-kernel, faible consommation d'énergie, AC433 double bande |
| ✅ Recommandé (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Pilote in-kernel, Wi-Fi 6E, AXML est directement insérable en USB-C |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACH (RTL8812AU) | Nécessite la compilation de morrownr/8812au (ARM64), fonctionnalités complètes après compilation |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACS / EACS | Nécessite la compilation du pilote out-of-tree correspondant |
| ⚠️ Disponible mais à utiliser avec précaution | AWUS036AX / AXER (RTL8832BU) | Le rtw89 du kernel 6.x pourrait déjà le prendre en charge ; pas besoin de compiler |

### 4.2 Recommandations d'utilisation

| Scène d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Développement d'AI desktop et connexion sans fil | AWUS036ACM / ACHM | Pilote in-kernel, stable, sans maintenance |
| Tests de pénétration sans fil / Recherche en sécurité | AWUS036ACH ou AWUS036ACM | Les deux supportent Monitor + Injection |
| Wi-Fi 6E / Fréquence 6GHz | AWUS036AXML / AXM | Pilote in-kernel MT7921AUN |
| Pas besoin de Wi-Fi externe | — | AI TOP ATOM est intégré avec Wi-Fi 7, connexion Internet générale sans besoin d'extension externe |

## 5. Besoins Environnementaux

### 5.1 Besoins Matériels

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur USB-C vers USB-A ou câble de transmission (sauf pour AXML), recommandé pour le support USB 3.2 Gen 2×2 |
| Alimentation | Alimentation USB-C de 240W de la marque GIGABYTE |

### 5.2 Besoins Logiciels

| Élément | Besoin |
|---|---|
| Version DGX OS | Version en service (kernel 6.x) |
| Outils de compilation (nécessaire pour les puces Realtek) | build-essential, git, bc, dkms |
| Outils de gestion sans fil | iw, network-manager (installé par défaut dans DGX OS) |

## 6. Détermination de la compatibilité

### Matrices de compatibilité entre les modèles en service d'ALFA et GIGABYTE AI TOP ATOM (GB10)

| Modèle | Processeur | Mode de pilotage | Détection USB | STA Internet | Mode AP | Moniteur | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | Sans installation | ⭐ Meilleur |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limité | Sans installation | ✅ Bon |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Moyen (traduction) | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Moyen (traduction) | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Moyen (traduction) | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ✅ | ⚠️ | ⚠️ | ❌ | Moyen-Haut | ⚠️ Disponible |

Critère de détermination : GIGABYTE AI TOP ATOM et DGX Spark partagent la même plateforme matérielle GB10 et le même DGX OS (kernel 6.x, aarch64), la détermination de la compatibilité est identique à celle de DGX Spark.

## 7. Détails ultra détaillés : Étapes de configuration étape par étape

Les étapes d'installation de GIGABYTE AI TOP ATOM sont identiques à celles de NVIDIA DGX Spark. Voici une version résumée ; pour les étapes complètes, consultez le chapitre 7 de l'article [ALFA : Carte réseau sans fil, est-elle compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modèles de puces MediaTek (prêt à l'emploi)

- Utilisez un adaptateur USB-C to USB-A (AXML peut être inséré directement), insérez la carte réseau ALFA dans le port USB-C de l'AI TOP ATOM
- Confirmez la détection : `lsusb`
- Confirmez l'interface : `ip link show` (wlan0 devrait apparaître automatiquement)
- Connectez-vous au WiFi : `nmcli dev wifi connect "SSID" password "mot de passe"`

### 7.2 Modèles de puces Realtek (nécessite compilation)

Prenez AWUS036ACH (RTL8812AU) comme exemple :

```bash
# 1. Installez les outils de compilation
sudo apt update && sudo apt install -y build-essential git bc dkms

# 2. Téléchargez et compilez le pilote
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
# Vérifiez que CONFIG_PLATFORM_ARM64 = y dans Makefile
make
sudo make install
sudo modprobe 8812au

# 3. Confirmez l'interface après insertion de la carte réseau
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

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| `lsusb` ne voit pas la carte réseau ALFA | Adaptateur USB-C défectueux / Seulement en charge | Changer un adaptateur USB 3.2 Gen 2×2 compatible avec la transmission de données ; essayer un autre port USB-C |
| Interface wlan du processeur MediaTek introuvable | Module non chargé automatiquement / Firmware manquant | `sudo modprobe mt76x2u` ; `sudo apt install linux-firmware` ; vérifier `dmesg | grep mt76` |
| Échec de la compilation du pilote Realtek | Paramètres de compilation croisée incorrects | Vérifier que la compilation est native sur AI TOP ATOM ; le Makefile ne devrait pas définir CROSS_COMPILE |
| Vitesse WiFi lente | Adaptateur ne supporte que USB 2.0 | Changer un adaptateur USB 3.2 Gen 2×2 |
| Conflit entre le Wi-Fi intégré et externe | Conflit de routeur | `sudo nmcli radio wifi off` pour désactiver le WiFi intégré avant d'utiliser le WiFi externe |
| Impossible d'utiliser la bande 6GHz | Limitations réglementaires | `sudo iw reg set US` ; vérifier les dernières réglementations |
| Carte réseau disparait après le réveil du système | Arrêt automatique USB | `echo 'options usbcore autosuspend=-1' | sudo tee /etc/modprobe.d/usb.conf` |

## 9. Limites connues

- Nécessité de convertisseur USB Type-C : tous les cartes réseau ALFA, sauf l'AXML, nécessitent un adaptateur USB-C to USB-A
- Nécessité de traduction manuelle pour les puces Realtek : RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU ne sont pas intégrés dans le mainline
- Possibilité de conflit avec le Wi-Fi intégré : AI TOP ATOM intègre déjà le Wi-Fi 7 + BT 5.3
- Configuration manuelle du mode AP : DGX OS est par défaut un environnement de développement
- Limites réglementaires pour la bande 6GHz : la disponibilité du Wi-Fi 6E dépend de la zone réglementaire
- Mise à jour des pilotes dépendante de l'upstream : les pilotes out-of-tree pour Realtek sont maintenus par la communauté, et doivent être recompilés après une mise à jour du kernel
- Différences matérielles de GIGABYTE sans incidence sur la compatibilité : les différences de conception mécanique et de refroidissement n'affectent pas la compatibilité des pilotes USB WiFi
- Modifications matérielles dans la période de garantie : la compilation et l'installation de pilotes tiers n'affectent pas la garantie matérielle, mais le support technique GIGABYTE peut ne pas couvrir les problèmes des pilotes tiers

Conditions de contestation : les jugements ci-dessus sont basés sur DGX OS (basé sur Ubuntu, kernel 6.x). Si GIGABYTE sort une version de firmware propre non compatible avec DGX OS, les jugements doivent être réévalués ; la version Bluetooth (5.3) suit les spécifications de la série de livraison, il est recommandé de vérifier la page officielle après réception.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Page produit officielle GIGABYTE AI TOP ATOM | Spécifications matérielles AI TOP ATOM (ATAGB10-9000) | https://www.gigabyte.com/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ Vérifié | 2026-09-03 |
| Page officielle GIGABYTE AI TOP ATOM (version en chinois simplifié) | Caractéristiques et spécifications du produit | https://www.gigabyte.cn/AI-TOP-PC/GIGABYTE-AI-TOP-ATOM | ✅ Vérifié | 2026-09-03 |
| Review GIGABYTE AI TOP ATOM (LinuxGizmos) | Tests tiers et confirmation des spécifications (BT 5.3 / 50.5mm) | https://linuxgizmos.com/gigabyte-ai-top-atom-introduces-nvidia-grace-blackwell-gb10-performance-for-the-desktop/ | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA DGX Spark | Informations sur la plate-forme GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux pour RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yupitek) | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte sans fil ALFA est compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec ASUS Ascent GX10 ?](https://yupitek.com/zh-tw/blog/alfa-asus-ascent-gx10-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec ALTOS BrainSphere GB10 F1 ?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec MSI EdgeXpert ?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article est basée sur le système d'exploitation NVIDIA DGX OS préinstallé sur GIGABYTE AI TOP ATOM (kernel 6.x, aarch64). AI TOP ATOM et DGX Spark partagent la même plate-forme matérielle, la compatibilité est parfaitement identique. Les pilotes de puces MediaTek sont pour Linux mainline, avec une stabilité élevée ; les pilotes de puces Realtek sont maintenus par la communauté. AI TOP ATOM est intégré avec Wi-Fi 7, et l'ALFA externe est principalement utilisée pour des tests de pénétration ou des besoins spécifiques de puces.
