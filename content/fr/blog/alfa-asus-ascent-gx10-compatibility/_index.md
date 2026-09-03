---
title: "Carte réseau sans fil ALFA : prise en charge du modèle ASUS Ascent GX10 (GB10) ?"
date: 2026-09-03
draft: false
slug: "alfa-asus-ascent-gx10-compatibility"
tags:
  - "ALFA"
  - "ASUS"
  - "Ascent-GX10"
  - "GB10"
  - "DGX-OS"
  - "AWUS036ACM"
  - "AWUS036AXML"
  - "ARM64"
categories:
  - "Guide Matériel"
description: "ASUS GX10 & NVIDIA DGX Spark : compatibilité ALFA, MediaTek et Realtek, USB-C, adaptateur nécessaire pour AXML"
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Client demande : « L'ALFA série USB carte sans fil peut-elle être utilisée sur l'ordinateur portable ASUS Ascent GX10 (NVIDIA GB10 Grace Blackwell) supercomputer AI ? »

Conclusion rapide : L'ASUS Ascent GX10 et le NVIDIA DGX Spark partagent la même plateforme matérielle GB10 et l'environnement logiciel DGX OS, la compatibilité avec la carte ALFA est parfaitement identique (jugement de base : 9 cartes USB ALFA en service). Les modèles de puces MediaTek (AWUS036ACM / ACHM / AXML / AXM, 4 modèles) utilisent des pilotes in-kernel, prêts à l'emploi à l'ouverture de la boîte ; les modèles de puces Realtek (AWUS036ACH / ACS / EACS / AX / AXER, 5 modèles) nécessitent la compilation de pilotes out-of-tree sur ARM64. Attention : tous les ports USB du GX10 sont de type USB Type-C (3 ports de données + 1 port d'entrée PD), les cartes ALFA (à l'exception de l'AXML) nécessitent un adaptateur USB-C to USB-A.

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles ASUS Ascent GX10

| Élément | Spécification |
|---|---|
| Nom du produit | ASUS Ascent GX10 |
| Processeur central | NVIDIA GB10 Grace Blackwell Superchip (plateforme DGX Spark) |
| CPU | 20 cœurs Arm (10× Cortex-X925 + 10× Cortex-A725), ARMv9.2-A |
| GPU | Architecture Blackwell de NVIDIA, 6144 cœurs CUDA, cinquième génération Tensor Core, quatrième génération RT Core |
| Performances AI | Jusqu'à 1 PetaFLOP (FP4, Sparse) / 1000 TOPS |
| Mémoire système | 128GB LPDDR5x mémoire unifiée (256-bit, 273 GB/s) |
| Stockage | Jusqu'à 4TB NVMe M.2 SSD (cryptage intégré) |
| USB | 3× USB 3.2 Gen 2×2 Type-C (20Gbps, DP Alt Mode / DisplayPort 2.1) + 1× USB 3.2 Gen 2×2 Type-C (alimentation PD, 180W EPR PD3.1) |
| Sortie vidéo | 1× HDMI 2.1 (peut être utilisé avec DP Alt Mode pour une sortie multi-écrans) |
| Réseau câblé | 1× 10GbE RJ45 + NVIDIA ConnectX-7 SmartNIC (2× 200G QSFP112) |
| Réseau sans fil | Wi-Fi 7 (MediaTek AW-EM637, 2×2 MIMO) + Bluetooth 5.4 |
| Système d'exploitation | NVIDIA DGX OS (basé sur Ubuntu Linux, kernel 6.x) |
| Architecture | aarch64 (ARM64) |
| Dimensions | 150 × 150 × 51 mm (5.91 × 5.91 × 2.01 pouces) |
| Poids | 1.48 kg |
| Refroidissement | Système de refroidissement exclusif ASUS (ventilateur silencieux + dissipateurs thermiques) |
| Autres | Port de verrouillage Kensington |

> ⚠️ Note de correction des spécifications : Le dimensions initiale était écrite comme « 150 × 150 × 50 mm » et sans poids. Après vérification des spécifications techniques officielles d'ASUS, il est **150 × 150 × 51 mm / 1.48 kg**. Les dimensions ont été corrigées. La version HDMI est également corrigée à 2.1 (l'original était écrite 2.1b). Voir la section 10 pour les sources de référence.

### 2.2 Environnement logiciel : NVIDIA DGX OS

| Élément | Contenu |
|---|---|
| OS de base | Ubuntu Linux (personnalisé par NVIDIA) |
| Kernel | Linux 6.x |
| Architecture | aarch64 (ARM64) |
| Logiciels préinstallés | Stack de logiciels AI NVIDIA (CUDA, cuDNN, TensorRT, PyTorch, Jupyter, etc.) |
| Gestion des paquets | apt |

### 2.3 Différences avec DGX Spark

| Critère de différence | ASUS GX10 | NVIDIA DGX Spark |
|---|---|---|
| Conception de refroidissement | Système de refroidissement exclusif ASUS | Refroidissement de référence NVIDIA |
| Conception de la machine | Châssis personnalisé par ASUS | Châssis de référence NVIDIA |
| Module sans fil | MediaTek AW-EM637 (Wi-Fi 7) | Module Wi-Fi 7 de niveau équivalent |
| Accessoires | Accessoires d'usine ASUS | Accessoires d'usine NVIDIA |
| Garantie | Garantie ASUS | Garantie NVIDIA |
| Influence sur la compatibilité ALFA | Aucune influence. Les contrôleurs USB, les versions du kernel et les frameworks de pilotes sont identiques à ceux du DGX Spark. |

### 2.4 Besoins en adaptateurs USB Type-C

Les 4 ports USB de l'GX10 sont de type Type-C :

- 3 ports de données (soutiennent DP Alt Mode, peuvent être utilisés pour connecter des écrans)
- 1 port d'entrée PD (utilisé pour l'alimentation)

Tous les cartes réseau de la gamme ALFA (sauf l'AXML qui est USB-C) sont de type USB Type-A, nécessitant un adaptateur.

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
| ✅ Recommandé (Wi-Fi 6E) | AWUS036AXML / AXM (MT7921AUN) | Pilote in-kernel, Wi-Fi 6E, AXML est directement insérable en USB-C |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACH (RTL8812AU) | Nécessite la compilation de morrownr/8812au (ARM64), fonctionnalités complètes après compilation |
| ⚠️ Disponible mais nécessite la compilation | AWUS036ACS / EACS | Nécessite la compilation du pilote out-of-tree correspondant |
| ⚠️ Disponible mais à utiliser avec précaution | AWUS036AX / AXER (RTL8832BU) | Le rtw89 du kernel 6.x pourrait déjà le prendre en charge ; pas besoin de compiler |

### 4.2 Suggestions de scénarios d'utilisation

| Scénario d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Internet sans fil général (le plus simple) | AWUS036ACM / ACHM | Pilote in-kernel, sans compilation |
| Tests de pénétration / Surveillance / Injection sans fil | AWUS036ACH ou AWUS036ACM | Les deux supportent Monitor + Injection |
| Wi-Fi 6E / 6GHz | AWUS036AXML / AXM | Pilote in-kernel MT7921AUN |
| Pas besoin d'WiFi externe | — | GX10 est intégré avec Wi-Fi 7, le surf sur Internet ne nécessite pas d'extension externe |

## 5. Besoins Environnementaux

### 5.1 Besoins En Matériel

| Élément | Besoin |
|---|---|
| Adaptateur USB | Adaptateur USB-C vers USB-A ou câble de transmission (sauf pour AXML), recommandé pour prendre en charge USB 3.2 Gen 2×2 |
| Alimentation | Alimentation USB-C d'origine ASUS GX10 (180W EPR PD3.1) |

### 5.2 Besoins En Logiciel

| Élément | Besoin |
|---|---|
| Version DGX OS | Version en service (kernel 6.x) |
| Outils de compilation (nécessaire pour le chip Realtek) | build-essential, git, bc, dkms |
| Outils de gestion sans fil | iw, network-manager (installé par défaut sur DGX OS) |

## 6. Détermination de la compatibilité

### Matrice de compatibilité entre les modèles en service ALFA et ASUS Ascent GX10 (GB10)

| Modèle | Processeur | Mode de pilotage | Détection USB | STA Internet | Mode AP | Moniteur | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACM | MT7612U | in-kernel (mt76x2u) | ✅ | ✅ | ✅ | ✅ | Sans installation | ⭐ Meilleure |
| AWUS036ACHM | MT7610U | in-kernel (mt76x0u) | ✅ | ✅ | ✅ | ⚠️ Limitée | Sans installation | ✅ Bonne |
| AWUS036AXML | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitée | Sans installation | ✅ Bonne |
| AWUS036AXM | MT7921AUN | in-kernel (mt7921u) | ✅ | ✅ | ✅ | ⚠️ Limitée | Sans installation | ✅ Bonne |
| AWUS036ACH | RTL8812AU | out-of-tree (8812au) | ✅ | ✅ | ✅ | ✅ | Moyenne (traduction) | ⚠️ Disponible |
| AWUS036ACS | RTL8811AU | out-of-tree (8812au) | ✅ | ✅ | ⚠️ | ❌ | Moyenne (traduction) | ⚠️ Disponible |
| AWUS036EACS | RTL8811CU | out-of-tree (8821cu) | ✅ | ⚠️ | ❌ | ❌ | Moyenne (traduction) | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | rtw89 / out-of-tree | ✅ | ⚠️ | ⚠️ | ❌ | Moyenne-Haute | ⚠️ Disponible |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ✅ | ⚠️ | ⚠️ | ❌ | Moyenne-Haute | ⚠️ Disponible |

Critère de détermination : L'ASUS GX10 et le DGX Spark partagent la même plateforme matérielle GB10 et le même DGX OS (kernel 6.x, aarch64), la détermination de la compatibilité est identique à celle du DGX Spark.

## 7. Détails ultra détaillés : Étapes de configuration étape par étape

Les étapes d'installation de l'ASUS GX10 sont identiques à celles de l'installation de NVIDIA DGX Spark. Voici une version raccourcie ; pour les étapes complètes, consultez le chapitre 7 de l'article [ALFA : Carte réseau sans fil, est-elle compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/).

### 7.1 Modèles de puces MediaTek (prêt à l'emploi)

- Utilisez un adaptateur USB-C to USB-A (AXML peut être directement inséré), insérez la carte réseau ALFA dans le port USB-C du GX10
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
| Échec de la compilation du pilote Realtek | Configuration de la compilation croisée incorrecte | Confirmer la compilation native sur le GX10 ; le Makefile ne devrait pas définir CROSS_COMPILE |
| Vitesse WiFi lente | Adaptateur ne supporte que USB 2.0 | Changer un adaptateur USB 3.2 Gen 2×2 |
| Conflit entre le Wi-Fi intégré et externe | Conflit de routeur | `sudo nmcli radio wifi off` désactiver le WiFi intégré avant d'utiliser le Wi-Fi externe |
| Impossible d'utiliser la bande 6GHz | Limitation du domaine réglementaire | `sudo iw reg set US` ; vérifier les dernières réglementations |

## 9. Conditions connues

- Nécessité de convertisseur USB Type-C : tous les cartes réseaux ALFA, à l'exception de l'AXML, nécessitent un adaptateur USB-C to USB-A.
- Traduction manuelle nécessaire pour les puces Realtek : RTL8812AU / RTL8811AU / RTL8811CU / RTL8832BU ne sont pas intégrés dans le mainline.
- Possibilité de conflit avec Wi-Fi intégré 7 : le GX10 est intégré avec Wi-Fi 7 (MediaTek AW-EM637).
- Configuration manuelle du mode AP : DGX OS est par défaut un environnement de développement.
- Limitations réglementaires 6GHz : la disponibilité du Wi-Fi 6E dépend de la zone réglementaire.
- Mise à jour des pilotes dépendante des上游 : les pilotes out-of-tree Realtek sont maintenus par la communauté, et doivent être recompilés après une mise à jour du kernel.
- Différences matérielles ASUS n'affectent pas la compatibilité : les différences de refroidissement et de conception mécanique n'affectent pas la compatibilité des pilotes USB WiFi.

Conditions de réfutation : les jugements ci-dessus sont basés sur DGX OS (basé sur Ubuntu, kernel 6.x). Si ASUS sort des versions de système d'exploitation non DGX OS (comme des versions Android ou personnalisées), les jugements devront être réévalués.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| ASUS Ascent GX10 Techspec officiel | Spécifications matérielles GX10 (150×150×51mm / 1.48kg / configuration USB / HDMI 2.1) | https://www.asus.com/ph/networking-iot-servers/desktop-ai-supercomputer/ultra-small-ai-supercomputers/asus-ascent-gx10/techspec/ | ✅ Vérifié | 2026-09-03 |
| ASUS Ascent GX10 Boutique officielle (Royaume-Uni) | Page produit GX10 (150 × 150 × 51mm) | https://uk.store.asus.com/asus-ascent-gx105004-33389.html | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA DGX Spark | Informations sur la plateforme GB10 | https://www.nvidia.com/en-us/products/workstations/dgx-spark/ | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilote Linux RTL8812AU | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| Guide Linux ALFA Soft AP WiFi Hotspot (Yupitek) | Guide pour le mode AP Linux de ALFA | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Vérifié | 2026-09-03 |
| Vue d'ensemble des produits ALFA Network (Yupitek) | Spécifications des produits actuels ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte sans fil ALFA est compatible avec NVIDIA DGX Spark ?](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec ALTOS BrainSphere GB10 F1 ?](https://yupitek.com/zh-tw/blog/alfa-altos-brainsphere-gb10-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec GIGABYTE AI TOP ATOM ?](https://yupitek.com/zh-tw/blog/alfa-gigabyte-ai-top-atom-compatibility/)｜[Est-ce que la carte sans fil ALFA est compatible avec MSI EdgeXpert ?](https://yupitek.com/zh-tw/blog/alfa-msi-edgexpert-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article est basée sur l'OS NVIDIA DGX préinstallé sur ASUS Ascent GX10 (kernel 6.x, aarch64). Le GX10 et le DGX Spark partagent la même plateforme matérielle, la compatibilité est complètement identique. Les pilotes de puces MediaTek sont pour Linux mainline, avec une haute stabilité ; les pilotes de puces Realtek sont maintenus par la communauté. Le GX10 est intégré avec Wi-Fi 7, l'ALFA est principalement utilisée pour des tests de pénétration ou des besoins de puces spéciales.
