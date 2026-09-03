---
title: "Carte sans fil ALFA : prise en charge par le NVIDIA Jetson Nano ?"
date: 2026-09-03
draft: false
slug: "alfa-nvidia-jetson-nano-compatibility"
tags:
  - "ALFA"
  - "AWUS036ACH"
  - "AWUS036ACM"
  - "NVIDIA"
  - "Jetson-Nano"
  - "JetPack"
  - "ARM64"
  - "Linux-WiFi"
categories:
  - "Guide Matériel"
description: "Jetson Nano compatible with most ALFA network cards, limited by older JetPack 4.x kernel. Realtek models (AWUS036ACH) practical, MediaTek MT7612U/MT7610U need backport, Wi-Fi 6E MT7921AUN not avail..."
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

## 1. Résumé du problème

Le client demande : « Peut-on utiliser la carte réseau USB ALFA série sur le développement board NVIDIA Jetson Nano ? »

Conclusion rapide : Le Jetson Nano peut utiliser la plupart des cartes réseau ALFA, mais la limitation principale réside dans le fait que le kernel Linux 4.9 de JetPack 4.x est assez ancien (évaluation : 9 modèles de cartes réseau USB ALFA en service, dont 3 sont utilisables, 2 nécessitent une compilation avancée, 2 ne sont pas vérifiés et 2 ne sont pas utilisables). Les modèles de puces Realtek (AWUS036ACH / ACS / EACS) peuvent être directement compilés avec des pilotes out-of-tree, ce qui en fait une option pratique pour le Jetson Nano ; les modèles MediaTek MT7612U / MT7610U nécessitent un backport ou une compilation personnalisée du pilote mt76 ; le modèle MT7921AUN de Wi-Fi 6E (AWUS036AXML / AXM) n'est pas utilisable sur le Jetson Nano en raison de la nécessité d'un kernel 5.19+. Pour des scénarios de tests d'intrusion, le AWUS036ACH (RTL8812AU) est le choix privilégié ; pour des scénarios de navigation générale, le AWUS036ACH (stabilisé) ou le AWUS036ACM (nécessitant une compilation mt76) sont les options préférées.

## 2. Analyse des spécifications matérielles cibles

### 2.1 Spécifications matérielles de NVIDIA Jetson Nano

| Item | Spécification |
|---|---|
| Module | Module Jetson Nano (P3448) |
| CPU | Quad-core ARM Cortex-A57 (ARMv8-A / aarch64) |
| GPU | NVIDIA Maxwell architecture, 128 CUDA cores |
| Mémoire | 4GB LPDDR4 (64-bit, 25.6 GB/s) |
| Stockage | microSD (carte de développement) / eMMC (module de production) |
| USB | 4x USB 3.0 Type-A + 1x USB 2.0 Micro-B (Mode Device / Alimentation) |
| Réseau | 1x Gigabit Ethernet (RJ45) |
| Sans fil | Aucun WiFi / Bluetooth intégré (nécessite un USB ou une extension M.2) |
| Alimentation | Connecteur DC 5V/4A (recommandé) ou micro-USB 5V/2A |
| Dimensions | 100mm × 80mm (carte de développement) |

### 2.2 Environnement logiciel : JetPack 4.x

| Item | Contenu |
|---|---|
| Système d'exploitation | Linux for Tegra (L4T), basé sur Ubuntu 18.04 LTS |
| Version du kernel | Linux 4.9 (L4T R32.x / JetPack 4.6.x) |
| Architecture | aarch64 (ARM64) |
| Compilateur | GCC 7.5 (par défaut) / GCC 8 (installable) |
| Version la plus récente | JetPack 4.6.4 (L4T R32.7.4), en mode maintenance |
| Mise à jour ultérieure | Jetson Nano ne prend pas en charge JetPack 5.x (kernel 5.10) en raison des limitations matérielles |

### 2.3 Limitations clés : Kernel 4.9

Le kernel 4.9 de Jetson Nano est un facteur clé pour la compatibilité :

| Ppilote | Version du kernel entrant dans le mainline | Utilisabilité sur Jetson Nano (kernel 4.9) |
|---|---|---|
| mt76x2u (MT7612U) | 4.19 | ❌ Besoin de backport / compilation personnelle |
| mt76x0u (MT7610U) | 4.19 | ❌ Besoin de backport / compilation personnelle |
| mt7921u (MT7921AUN) | 5.19 | ❌ Inutilisable (écart trop grand) |
| rtl8812au (RTL8812AU) | Jamais entré dans le mainline | ✅ Compilable en out-of-tree driver |
| rtl8821cu (RTL8811CU) | Jamais entré dans le mainline | ✅ Compilable en out-of-tree driver |
| rtw89 (RTL8832BU) | 5.16 (PCIe) / USB intégré progressivement | ❌ Besoin de compilation personnelle, compatibilité inconnue |

### 2.4 Limitations d'alimentation USB

Les 4 ports USB 3.0 Type-A de la carte de développement Jetson Nano partagent un budget d'alimentation :

- Utilisation de l'alimentation DC (5V/4A) : sortie totale environ 1.5A (5V)
- Utilisation de l'alimentation micro-USB (5V/2A) : sortie totale environ 0.5A
- Carte réseau haute puissance ALFA (AWUS036ACH) peut atteindre un pic de 800mA-1A
- Recommandation : utilisez l'alimentation DC + un Hub USB 3.0 alimenté, pour éviter les coupures d'alimentation ou redémarrage du système

## 3. Analyse des spécifications et des puces des cartes réseau ALFA

Au 9 septembre 2026, la gamme de produits de cartes réseau USB sans fil actuels d'ALFA Network est la suivante :

| Modèle | Niveau Wi-Fi | Puce | Interface |Compatibilité avec Jetson Nano |
|---|---|---|---|---|
| AWUS036AXML | Wi-Fi 6E | MediaTek MT7921AUN | USB-C / USB 3.2 | ❌ Besoin de kernel 5.19+, inutilisable |
| AWUS036AXM | Wi-Fi 6E | MediaTek MT7921AUN | USB 3.2 + BT 5.2 | ❌ Idem |
| AWUS036AX | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Besoin de rtl8852bu personnalisé, non vérifié |
| AWUS036AXER | Wi-Fi 6 | Realtek RTL8832BU | USB 3.2 | ⚠️ Idem |
| AWUS036ACH | Wi-Fi 5 (AC1200) | Realtek RTL8812AU | USB 3.0 | ✅ Traduction morrownr/8812au, mature |
| AWUS036ACHM | Wi-Fi 5 (AC433) | MediaTek MT7610U | USB 2.0 | ⚠️ Besoin de backport mt76x0u |
| AWUS036ACM | Wi-Fi 5 (AC1200) | MediaTek MT7612U | USB 3.0 | ⚠️ Besoin de backport mt76x2u |
| AWUS036ACS | Wi-Fi 5 (AC433) | Realtek RTL8811AU | USB 2.0 | ✅ Couvert par le pilote 8812au |
| AWUS036EACS | Wi-Fi 5 (AC600) | Realtek RTL8811CU | USB 2.0 | ✅ Traduction morrownr/8821cu |

## 4. Modèles et SoC applicables

### 4.1 Catégorie recommandée

| Catégorie recommandée | Modèle (SoC) | Description |
|---|---|---|
| ⭐ Fortement recommandé (tests de pénétration) | AWUS036ACH (RTL8812AU) | Pilotes matures, supporte Monitor Mode + Packet Injection, carte réseau ALFA la plus utilisée sur Jetson Nano |
| ✅ Recommandé (accès Internet) | AWUS036ACH (RTL8812AU) | AC1200, installation de pilotes simple, stable |
| ✅ Recommandé (faible consommation d'énergie) | AWUS036EACS (RTL8811CU) | AC600 double bande, faible consommation d'énergie USB 2.0, adapté pour un accès Internet simple |
| ✅ Recommandé (entrée) | AWUS036ACS (RTL8811AU) | AC433 double bande, couvert par les pilotes 8812au |
| ⚠️ Disponible mais nécessite une traduction manuelle | AWUS036ACM (MT7612U) | Nécessite le backport du pilote mt76 au kernel 4.9, seuil technique élevé |
| ⚠️ Disponible mais nécessite une traduction manuelle | AWUS036ACHM (MT7610U) | Comme ci-dessus, seulement 433Mbps |
| ⚠️ Non vérifié / Déconseillé | AWUS036AX / AXER (RTL8832BU) | Wi-Fi 6, nécessite la compilation de rtl8852bu, compatibilité kernel 4.9 non vérifiée |
| ❌ Inutilisable | AWUS036AXML / AXM (MT7921AUN) | Wi-Fi 6E, nécessite le kernel 5.19+, Jetson Nano ne peut pas être mis à jour |

### 4.2 Recommandations d'utilisation

| Scène d'utilisation | Modèle recommandé | Description |
|---|---|---|
| Tests de pénétration / Surveillance / Injection sans fil | AWUS036ACH | Pilotes RTL8812AU supportant Monitor + Injection, vérification communautaire suffisante |
| Contrôle sans fil de robots / drones | AWUS036ACH ou AWUS036EACS | Connexion stable, faible délai |
| Accès Internet pour IoT | AWUS036EACS / ACS | Faible consommation d'énergie, USB 2.0 suffisant, économie d'énergie |
| Accès Internet à haute vitesse 5GHz | AWUS036ACH | AC1200, 5GHz 867Mbps |
| Nécessité de Wi-Fi 6 / 6E | ❌ Aucune option disponible | Jetson Nano ne prend pas en charge les puces Wi-Fi 6/6E modernes |

## 5. Besoins Environnementaux

### 5.1 Besoins Hardware

| Élément | Besoins Minimum | Recommandé |
|---|---|---|
| Carte de développement Jetson Nano | Version B01 / A02 | B01 (2 ports CSI pour caméras) |
| Mode de alimentation | 5V/2A micro-USB | 5V/4A connecteur DC (nécessaire en cas de multiples appareils USB) |
| Hub USB | Non obligatoire | Hub USB 3.0 avec alimentation (nécessaire pour les cartes réseau haute puissance) |
| Refroidissement | Radiateur (fourni par défaut) | Ventilateur + radiateur (pour les charges lourdes prolongées) |
| Stockage | 16GB microSD | 32GB+ UHS-I microSD (nécessaire pour l'espace de compilation des pilotes) |

### 5.2 Besoins Logiciels

| Élément | Besoins |
|---|---|
| Version JetPack | 4.6.x (L4T R32.7.x) |
| Outils de base | build-essential, git, bc, libssl-dev, flex, bison |
| Code source du Kernel | Nécessite le téléchargement du code source du kernel pour la version L4T correspondante (nécessaire pour la compilation du backport mt76) |
| Réseau | Connexion réseau filaire nécessaire pendant la compilation (via le port Ethernet Gigabit) |

## 6. Détermination de la compatibilité

### Matrice de compatibilité ALFA modèles actuels × NVIDIA Jetson Nano

| Modèle | Processeur | Mode de pilotage | Détecteur USB | STA Internet | Mode AP | Moniteur | Difficulté d'installation | Évaluation globale |
|---|---|---|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | Traduction 8812au | ✅ | ✅ | ✅ | ✅ | Moyen | ⭐ Meilleur |
| AWUS036ACS | RTL8811AU | Couverture 8812au | ✅ | ✅ | ⚠️ | ❌ | Moyen | ✅ Bon |
| AWUS036EACS | RTL8811CU | Traduction 8821cu | ✅ | ⚠️ | ❌ | ❌ | Moyen | ✅ Bon |
| AWUS036ACM | MT7612U | Backport mt76x2u | ✅ | ✅ | ✅ | ✅ | Élevé | ⚠️ Disponible |
| AWUS036ACHM | MT7610U | Backport mt76x0u | ✅ | ✅ | ⚠️ | ⚠️ | Élevé | ⚠️ Disponible |
| AWUS036AX | RTL8832BU | Traduction rtl8852bu | ⚠️ | ❌ | ❌ | ❌ | Élevé | ❌ Non recommandé |
| AWUS036AXER | RTL8832BU | Comme ci-dessus | ⚠️ | ❌ | ❌ | ❌ | Élevé | ❌ Non recommandé |
| AWUS036AXML | MT7921AUN | Nécessite kernel 5.19+ | ❌ | ❌ | ❌ | ❌ | — | ❌ Inutilisable |
| AWUS036AXM | MT7921AUN | Comme ci-dessus | ❌ | ❌ | ❌ | ❌ | — | ❌ Inutilisable |

Critère de détermination : Disponibilité des pilotes pour le kernel 4.9 du Jetson Nano JetPack 4.x + retours d'expérience de la communauté (forum Jetson Nano, GitHub morrownr pilotes issue). MT7921AUN est jugé inutilisable car Jetson Nano ne peut pas être mis à jour au kernel 5.19+.

## 7. Détails ultra détaillés des étapes de configuration

### 7.1 Préparations initiales : mise à jour du système et environnement de compilation

**Étape 1 : Démarrage et connexion via SSH au Jetson Nano**

```bash
ssh username@<jetson-nano-ip>
```

**Étape 2 : Mise à jour des paquets système**

```bash
sudo apt update
sudo apt upgrade -y
```

**Étape 3 : Installation des outils de compilation et des dépendances**

```bash
sudo apt install -y build-essential git bc libssl-dev flex bison dkms
```

**Étape 4 : Vérification de la version du kernel**

```bash
uname -r
# Sortie prévue : 4.9.337-tegra (ou similaire 4.9.x-tegra)
```

### 7.2 Chemin A : Modèles de puces Realtek (AWUS036ACH / ACS / EACS) — Recommandé

Prenez l'AWUS036ACH (RTL8812AU) comme exemple :

**Étape 1 : Téléchargement du code source du pilote**

```bash
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
```

**Étape 2 : (Optionnel) Ajustement des paramètres de compilation pour ARM64**

Éditez Makefile et vérifiez les paramètres suivants :

```
CONFIG_PLATFORM_ARM64 = y
```

(Le plus souvent, les versions récentes de Makefile détectent automatiquement aarch64)

**Étape 3 : Compilation et installation**

```bash
make
sudo make install
```

**Étape 4 : Chargement du module de pilote**

```bash
sudo modprobe 8812au
# Ou redémarrez
sudo reboot
```

**Étape 5 : Insérez la carte réseau ALFA et vérifiez l'interface réseau**

```bash
ip link show
# Sortie prévue : wlan0 (si rien, vérifiez dmesg)
dmesg | grep -i "8812au\|rtl8812\|usb"
```

**Étape 6 : Scan WiFi (vérification des fonctionnalités)**

```bash
sudo iw dev wlan0 scan | grep -E "SSID|signal"
```

**Étape 7 : Connexion au réseau WiFi (utilisez NetworkManager / nmcli)**

```bash
# Jetson Nano avec NetworkManager installé par défaut
nmcli dev wifi list
nmcli dev wifi connect "nom de votre WiFi" password "mot de passe de votre WiFi"
```

**Étape 8 : (Optionnel) Configuration en mode AP (point d'accès sans fil)**

```bash
# Installation de hostapd et dnsmasq
sudo apt install -y hostapd dnsmasq
# Référez-vous à la guide ALFA Soft AP pour la configuration
# https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/
```

**Étape 9 : Activation du mode écoute (pour les tests d'intrusion)**

```bash
sudo apt install -y aircrack-ng
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Vérification
sudo iw dev wlan0 info
# type devrait afficher monitor
# Test d'injection de paquets
sudo aireplay-ng --test wlan0
```

### 7.3 Chemin B : Modèles de puces MediaTek (AWUS036ACM / ACHM) — Avancé

Prenez l'AWUS036ACM (MT7612U) comme exemple, il est nécessaire de backport le pilote mt76 :

**Étape 1 : Téléchargement des sources du kernel du Jetson Nano**

```bash
# Téléchargez les sources du kernel correspondant à la version L4T
# Par exemple, pour L4T R32.7.4 :
wget https://developer.nvidia.com/embedded/l4t/r32_release_v7.4/sources/public_sources.tbz2
tar -xjf public_sources.tbz2
cd Linux_for_Tegra/source/public
tar -xjf kernel_src.tbz2
```

**Étape 2 : Préparation de l'environnement de compilation du kernel**

```bash
cd kernel/kernel-4.9
# Générer les configurations par défaut
make tegra_defconfig
# Activer les options mt76
make menuconfig
# Naviguez vers : Device Drivers > Network device support > Wireless LAN
# Sélectionnez : <M> MediaTek MT76x2U USB support
# Sélectionnez : <M> MediaTek MT76x0U USB support
```

**Étape 3 : Compilation des modules du kernel**

```bash
make modules_prepare
make M=drivers/net/wireless/mediatek/mt76 modules
```

**Étape 4 : Installation des modules**

```bash
sudo make M=drivers/net/wireless/mediatek/mt76 modules_install
sudo depmod -a
```

**Étape 5 : Chargement du pilote**

```bash
sudo modprobe mt76x2u
# Insérez l'AWUS036ACM
dmesg | grep mt76
ip link show
```

⚠️ Attention : backporter mt76 dans le kernel 4.9 peut entraîner des erreurs de compilation, nécessitant des corrections manuelles du code source. C'est une opération avancée, il est recommandé de ne la tenter que si vous avez de l'expérience dans la compilation du kernel. En cas de difficultés, il est préférable de passer à l'AWUS036ACH (RTL8812AU).

### 7.4 Chemin C : Modèles Wi-Fi 6 / 6E (AWUS036AX / AXER / AXML / AXM)

- AWUS036AXML / AXM (MT7921AUN) : Non disponible. Le kernel 4.9 du Jetson Nano ne peut pas être mis à jour à 5.19+, et le pilote mt7921u ne peut pas être backporté (gap trop grand, dépendances de bases du kernel moderne).
- AWUS036AX / AXER (RTL8832BU) : Non recommandé. Théoriquement, il est possible d'essayer de compiler le pilote morrownr/rtl8852bu, mais la compatibilité avec le kernel 4.9 n'a pas été vérifiée par la communauté, et les fonctionnalités Wi-Fi 6 peuvent ne pas fonctionner correctement. Si vous avez besoin de Wi-Fi 6, il est recommandé d'utiliser le Jetson Orin Nano (JetPack 5.x, kernel 5.10+) ou un ordinateur x86.

## 8. Erreurs Courantes et Solutions

| Symptômes | Causes Probables | Solutions |
|---|---|---|
| Aucune réaction de dmesg après l'insertion de la carte réseau | Alimentation USB insuffisante / Mauvais contact | Utilisez l'alimentation DC (5V/4A) ; Changez de port USB ; Utilisez un Hub USB avec alimentation |
| Erreur de compilation de make pour 8812au : gcc : erreur : option de ligne de commande non reconnue | Version GCC trop ancienne | Installer GCC 8 : `sudo apt install gcc-8 g++-8` et spécifier `CC = gcc-8` dans le Makefile |
| Erreur de modprobe 8812au : clé requise non disponible | Secure Boot activé (le Jetson Nano ne devrait pas avoir ce problème) | Vérifiez que le Jetson Nano n'a pas activé Secure Boot ; résignez le module ou désactivez Secure Boot |
| L'interface wlan0 apparaît mais ne peut pas scanner d'AP | Région réglementaire non définie / Pilote manquant | Définir la région réglementaire : `sudo iw reg set TW` ; Vérifiez dmesg pour des erreurs de chargement du firmware |
| Redémarrage du système ou déconnexion de la carte réseau lors de l'output à haute puissance | Alimentation USB insuffisante | Utilisez l'alimentation DC + Hub USB avec alimentation ; Réduisez la puissance TX : `sudo iw dev wlan0 set txpower fixed 2000` |
| Injection fonctionne dans le mode d'écoute avec aireplay-ng --test, mais l'attaque est inefficace | Fonctionnalité d'injection limitée du pilote / Conflit de canal | La fonction d'injection RTL8812AU est généralement utilisable ; Vérifiez que `airmon-ng check kill` a arrêté NetworkManager ; Essayez un autre canal |
| Échec de la compilation du mt76 backport | Écart trop grand entre le kernel 4.9 et le code original mt76 | Essayez une version plus ancienne du mt76 (correspondant au commit de la période kernel 4.19) ; ou utilisez AWUS036ACH |
| La carte réseau disparaît après le réveil du système | Réglage d'économie d'énergie USB | Désactiver l'arrêt automatique USB : `echo 'options usbcore autosuspend=-1' \| sudo tee /etc/modprobe.d/usb.conf` |
| Le 5GHz de AWUS036ACH ne peut pas être utilisé | Limitation de la région réglementaire / Table des canaux du pilote | Définir `sudo iw reg set US` (les réglementations américaines ouvrent plus de canaux 5GHz) ; Vérifiez que le canal utilisé est autorisé par les réglementations locales |

## 9. Limites connues

- Version du kernel bloquée à 4.9 : le Jetson Nano ne supporte pas JetPack 5.x, il n'est pas possible de mettre à jour le kernel, ce qui est la source de tous les problèmes de compatibilité
- MT7921AUN (Wi-Fi 6E) complètement inutilisable : nécessite un kernel 5.19+, impossible de backport sur 4.9
- Chips MediaTek mt76 nécessitent un backport manuel : les utilisateurs d'AWUS036ACM / ACHM doivent compiler eux-mêmes le module du kernel, le seuil technique est élevé
- ⚠️ **Le pilote Wi-Fi 6 (RTL8832BU) est déconseillé par le responsable du pilote** : le responsable du pilote morrownr a clairement indiqué dans son公告 que les séries rtl8852/32au sont "très mauvais pilotes, soupçonnant que le chip en lui-même a des problèmes", et recommande aux utilisateurs Linux d'éviter ce chip pour le moment (voir la section 10 pour la source). Cela est plus grave que simplement "la compatibilité avec le kernel 4.9 n'a pas été vérifiée", et la détermination de AWUS036AX / AXER dans ce document et d'autres documents pertinents doit être comprise comme "déconseillé" plutôt que "essayable mais plus compliqué"
- Limites de alimentation USB : 4 ports USB partagent environ 1.5A (alimentation DC), les cartes réseau à haute puissance doivent utiliser un Hub avec alimentation
- Performances en mode AP : la performance du CPU du Jetson Nano est limitée, la capacité de transmission du USB WiFi en mode AP peut être inférieure aux attentes
- Différences de fonctionnalités de surveillance/injection : RTL8812AU supporte le mieux ; les fonctionnalités d'injection des chips MediaTek après le backport du kernel 4.9 peuvent être instables
- Maintenance à long terme : JetPack 4.x est entré en mode maintenance, il n'y aura pas de nouvelles fonctionnalités ou mises à jour de pilotes à l'avenir
- Fonctionnalités Bluetooth : la fonction Bluetooth 5.2 de AWUS036AXM n'est pas vérifiée sur le Jetson Nano (nécessite le support de BlueZ)
- Refroidissement : en utilisant le USB WiFi à haute puissance pendant une longue période, la température globale du Jetson Nano peut augmenter, il est recommandé d'ajouter un ventilateur

Conditions de réfutation : les jugements ci-dessus sont basés sur JetPack 4.6.x (kernel 4.9). Si NVIDIA libère à l'avenir une prise en charge de JetPack 5.x pour le Jetson Nano (actuellement pas supporté officiellement), ou si la communauté propose un backport stable du kernel 5.x, la détermination de l'inutilité dans la section 4 devra être réévaluée.

## 10. Sources de référence URL

| Source | Description | URL | État de vérification | Date de vérification |
|---|---|---|---|---|
| Page officielle NVIDIA Jetson Nano | Spécifications matérielles du Jetson Nano | https://developer.nvidia.com/embedded/jetson-nano | ✅ Vérifié | 2026-09-03 |
| Page officielle NVIDIA JetPack SDK | Informations sur les versions JetPack et les kernels | https://developer.nvidia.com/embedded/jetpack | ✅ Vérifié | 2026-09-03 |
| morrownr/8812au GitHub | Pilotes Linux pour RTL8812AU (compatibles avec Jetson Nano) | https://github.com/morrownr/8812au-20210820 | ✅ Vérifié | 2026-09-03 |
| morrownr/8821cu GitHub | Pilotes Linux pour RTL8811CU | https://github.com/morrownr/8821cu-20210916 | ✅ Vérifié | 2026-09-03 |
| ALFA Soft AP WiFi Hotspot Linux Guide（Yupitek） | Guide de configuration en mode AP pour ALFA sous Linux | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Vérifié | 2026-09-03 |
| ALFA Network Produit Overview（Yupitek） | Spécifications des produits actuels d'ALFA | https://yupitek.com/zh-tw/products/alfa/ | ✅ Vérifié | 2026-09-03 |
| morrownr/USB-WiFi Issue #314 | Déclaration officielle du mainteneur de pilotes : il est recommandé d'éviter les puces rtl8852/32au（RTL8832BU） | https://github.com/morrownr/USB-WiFi/issues/314 | ✅ Vérifié | 2026-09-03 |
| morrownr/USB-WiFi Discussion #292 | mt7921u.ko nécessite un kernel 5.19+ pour apparaître dans le noyau (dépôt original du mainteneur) | https://github.com/morrownr/USB-WiFi/discussions/292 | ✅ Vérifié | 2026-09-03 |

Articles associés : [Est-ce que la carte sans fil ALFA est compatible avec NVIDIA DGX Spark](https://yupitek.com/zh-tw/blog/alfa-nvidia-dgx-spark-compatibility/)（Comparaison avec la plate-forme GB10, environnement kernel 6.x）｜[Est-ce que la carte sans fil ALFA est compatible avec OpenWrt](https://yupitek.com/zh-tw/blog/alfa-openwrt-router-compatibility/)

Déclaration de non-responsabilité : La détermination de la compatibilité de cet article est basée sur Jetson Nano JetPack 4.6.x (kernel 4.9). Les pilotes pour les puces Realtek sont maintenus par la communauté (morrownr), et la stabilité réelle peut varier selon la version. L'opération de backport pour les puces MediaTek mt76 nécessite de l'expérience en compilation du kernel, et il n'est pas garanti à 100% de réussir. Si vous avez besoin de prise en charge Wi-Fi 6/6E ou de kernel moderne, il est recommandé de passer à la série Jetson Orin (JetPack 5.x+) ou d'utiliser un ordinateur x86.
